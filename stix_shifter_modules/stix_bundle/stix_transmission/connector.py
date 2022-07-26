from stix_shifter_utils.modules.base.stix_transmission.base_sync_connector import BaseSyncConnector
from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient
from stix2matcher.matcher import Pattern
from stix2matcher.matcher import MatchListener
from stix2validator import validate_instance
import json
import re
from stix_shifter_utils.utils.error_response import ErrorResponder


class UnexpectedResponseException(Exception):
    pass


class Connector(BaseSyncConnector):
    def __init__(self, connection, configuration):
        self.connector = __name__.split('.')[1]
        self.connection = connection
        self.configuration = configuration
        self.timeout = connection['options'].get('timeout')
        self.bundle_url = self.connection.get('url')
        auth = None
        conf_auth = configuration.get('auth', {})
        if 'username' in conf_auth and 'password' in conf_auth:
            auth = (conf_auth['username'], conf_auth['password'])
        self.client = RestApiClient(None,
                                    auth=auth,
                                    url_modifier_function=lambda host_port, endpoint, headers: f'{endpoint}')

    # We re-implement this method so we can fetch all the "bindings", as their method only
    # returns the first for some reason
    def match(self, pattern, observed_data_sdos, verbose=False, stix_version='2.0'):
        compiled_pattern = Pattern(pattern, stix_version=stix_version)
        matcher = MatchListener(observed_data_sdos, verbose, stix_version=stix_version)
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

    def ping_connection(self):
        return_obj = dict()

        response = self.client.call_api(self.bundle_url, 'head', timeout=self.timeout)
        response_txt = response.raise_for_status()

        if response.code == 200:
            return_obj['success'] = True
        elif response.code == 301:
            self.bundle_url = response.headers.get('Location')
            return self.ping_connection()
        else:
            ErrorResponder.fill_error(return_obj, response_txt, ['message'], connector=self.connector)
        return return_obj

    def create_results_connection(self, search_id, offset, length):
        observations = []
        return_obj = dict()
        is_stix_21 = self.connection['options'].get("stix_2.1")
        stix_version = '2.1' if is_stix_21 else '2.0'

        if not is_stix_21 and self.test_START_STOP_format(search_id):
            # Remove leading 't' before timestamps from search_id. search_id is the stix pattern
            search_id = re.sub("(?<=START\s)t|(?<=STOP\s)t", "", search_id)

        response = self.client.call_api(self.bundle_url, 'get', timeout=self.timeout)

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
                    results = validate_instance(bundle, stix_version=stix_version)

                    if results.is_valid is not True:
                        ErrorResponder.fill_error(return_obj,  message='Invalid Objects in STIX Bundle.', connector=self.connector)
                        return return_obj

                if is_stix_21:
                    observations = [bundle]
                else:
                    for obj in bundle["objects"]:
                        if obj["type"] == "observed-data":
                            observations.append(obj)

                # Pattern match
                try:
                    results = self.match(search_id, observations, False, stix_version)
                    if is_stix_21:
                        v21_results = []
                        v21_observed_data = []
                        v21_cboxes = {}
                        for obs_obj in results:
                            if "objects" in obs_obj:
                                for obj in obs_obj["objects"]:
                                    if obj['type'] == "observed-data":
                                        v21_observed_data.append(obj)
                                    elif obj['type'] != "identity":
                                        v21_cboxes[obj['id']] = obj

                        v21_observed_data = v21_observed_data[int(offset):int(offset + length)]
                        v21_results.extend(v21_observed_data)
                        for observed_data in v21_observed_data:
                            for ref in observed_data['object_refs']:
                                if ref in v21_cboxes:
                                    v21_results.append(v21_cboxes[ref])
                                    del v21_cboxes[ref]
                        
                        results = v21_results
                    else:
                        results = results[int(offset):int(offset + length)]

                    if len(results) != 0:
                        return_obj['success'] = True
                        return_obj['data'] = results
                    else:
                        return_obj['success'] = True
                        return_obj['data'] = []
                except Exception as ex:
                    ErrorResponder.fill_error(return_obj,  message='Object matching error: ' + str(ex), connector=self.connector)
            except Exception as ex:
                ErrorResponder.fill_error(return_obj,  message='Invalid STIX bundle. Malformed JSON: ' + str(ex), connector=self.connector)
        return return_obj

    def delete_query_connection(self, search_id):
        return_obj = dict()
        return_obj['success'] = True
        return return_obj

    def test_START_STOP_format(self, query_string) -> bool:
        # Matches START t'1234-56-78T00:00:00.123Z' STOP t'1234-56-78T00:00:00.123Z'
        pattern = "START\s(t'\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z')\sSTOP"
        match = re.search(pattern, query_string)
        return bool(match)