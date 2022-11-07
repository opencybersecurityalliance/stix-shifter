import json
import time
from aiohttp import BasicAuth
from stix2matcher.matcher import Pattern
from stix2matcher.matcher import MatchListener
from stix2validator import validate_instance

from stix_shifter_utils.modules.base.stix_transmission.base_connector import BaseConnector
from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import Status
from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync
from stix_shifter_utils.utils.error_response import ErrorResponder

ERROR_TYPE_TIMEOUT = 'timeout'
ERROR_TYPE_BAD_CONNECTION = 'bad_connection'
ERROR_TYPE_STATUS_DELAY = 'status_delay_sec_'

class UnexpectedResponseException(Exception):
    pass


class Connector(BaseConnector):
    def __init__(self, connection, configuration):
        self.connector = __name__.split('.')[1]
        self.connection = connection
        self.configuration = configuration
        self.timeout = connection['options'].get('timeout')
        self.bundle_url = self.connection.get('url')
        auth = None
        conf_auth = configuration.get('auth', {})
        if 'username' in conf_auth and 'password' in conf_auth:
            auth = BasicAuth(conf_auth['username'], conf_auth['password'])
        self.client = RestApiClientAsync(None,
                                    auth=auth,
                                    url_modifier_function=lambda host_port, endpoint, headers: f'{endpoint}')

    # We re-implement this method so we can fetch all the "bindings", as their method only
    # returns the first for some reason
    def match(self, pattern, observed_data_sdos, verbose=False):
        compiled_pattern = Pattern(pattern)
        matcher = MatchListener(observed_data_sdos, verbose)
        compiled_pattern.walk(matcher)

        found_bindings = matcher.matched()

        if found_bindings:
            matching_sdos = []
            for binding in found_bindings:
                matches = [match for match in matcher.get_sdos_from_binding(binding) if match not in matching_sdos]
                matching_sdos.extend(matches)
        else:
            matching_sdos = []

        return matching_sdos

    async def ping_connection(self):
        return_obj = dict()

        response = await self.client.call_api(self.bundle_url, 'head', timeout=self.timeout)
        response_txt = response.raise_for_status()

        if response.code == 200:
            return_obj['success'] = True
        elif response.code == 301:
            self.bundle_url = response.headers.get('Location')
            return self.ping_connection()
        else:
            ErrorResponder.fill_error(return_obj, response_txt, ['message'], connector=self.connector)
        return return_obj

    async def create_query_connection(self, query):
        return {"success": True, "search_id": query}

    async def create_status_connection(self, search_id, metadata=None):
        error_type = self.connection['options'].get('error_type')
        if error_type.startswith(ERROR_TYPE_STATUS_DELAY):
            delay = int(error_type[len(ERROR_TYPE_STATUS_DELAY):])
            current_time = int(time.time())
            if metadata:
                stop_time = metadata['stop_time']
            else:
                stop_time = current_time + delay
            if stop_time > current_time:
                return {"success": True, "status": Status.RUNNING.value, "progress": int((delay - (stop_time - current_time)) / delay * 100), "metadata": {"stop_time": stop_time}}
        return {"success": True, "status": Status.COMPLETED.value, "progress": 100}

    async def create_results_connection(self, search_id, offset, length):
        observations = []
        return_obj = dict()

        response = None
        if self.connection['options'].get('error_type') == ERROR_TYPE_TIMEOUT:
            # httpstat.us/200?sleep=60000 for slow connection that is valid
            await self.client.call_api('https://httpstat.us/200?sleep=60000', 'get', timeout=self.timeout)
        elif self.connection['options'].get('error_type') == ERROR_TYPE_BAD_CONNECTION:
            # www.google.com:81 for a bad connection that will timeout
            response = await self.client.call_api('https://www.google.com:81', 'get', timeout=self.timeout)
        if not response:
            response = await self.client.call_api(self.bundle_url, 'get', timeout=self.timeout)
        if response.code != 200:
            response_txt = response.raise_for_status()
            if ErrorResponder.is_plain_string(response_txt):
                ErrorResponder.fill_error(return_obj, message=response_txt, connector=self.connector)
            elif ErrorResponder.is_json_string(response_txt):
                response_json = json.loads(response_txt)
                ErrorResponder.fill_error(return_obj, response_json, ['reason'], connector=self.connector)
            else:
                raise UnexpectedResponseException
        else:
            try:
                response_txt = response.read().decode('utf-8')
                bundle = json.loads(response_txt)

                if "stix_validator" in self.connection['options'] and self.connection['options'].get("stix_validator") is True:
                    results = validate_instance(bundle)

                    if results.is_valid is not True:
                        ErrorResponder.fill_error(return_obj,  message='Invalid Objects in STIX Bundle.', connector=self.connector)
                        return return_obj

                for obj in bundle["objects"]:
                    if obj["type"] == "observed-data":
                        observations.append(obj)

                # Pattern match
                try:
                    results = self.match(search_id, observations, False)

                    if len(results) != 0:
                        return_obj['success'] = True
                        return_obj['data'] = results[int(offset):int(offset + length)]
                    else:
                        return_obj['success'] = True
                        return_obj['data'] = []
                except Exception as ex:
                    ErrorResponder.fill_error(return_obj,  message='Object matching error: ' + str(ex), connector=self.connector)
            except Exception as ex:
                ErrorResponder.fill_error(return_obj,  message='Invalid STIX bundle. Malformed JSON: ' + str(ex), connector=self.connector)
        return return_obj

    async def delete_query_connection(self, search_id):
        return_obj = dict()
        return_obj['success'] = True
        return return_obj
