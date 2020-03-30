from stix_shifter_utils.modules.base.stix_transmission.base_sync_connector import BaseSyncConnector

from stix2matcher.matcher import Pattern
from stix2matcher.matcher import MatchListener
from stix2validator import validate_instance
import json
import requests
from stix_shifter_utils.utils.error_response import ErrorResponder


class UnexpectedResponseException(Exception):
    pass


class Connector(BaseSyncConnector):
    def __init__(self, connection, configuration):
        self.connection = connection
        self.configuration = configuration
        self.bundle_url = None

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
                matching_sdos = matching_sdos + matcher.get_sdos_from_binding(binding)
        else:
            matching_sdos = []

        return matching_sdos

    def ping_connection(self):
        return_obj = dict()

        if not self.bundle_url:
            self.bundle_url = self.connection.get('host')
        auth = self.configuration.get('auth')

        response = self.call_api(self.bundle_url, auth, 'head')
        response_txt = response.raise_for_status()
        response_code = response.status_code

        if response_code == 200:
            return_obj['success'] = True
        elif response_code == 301:
            self.bundle_url = response.headers.get('Location')
            return self.ping_connection()
        else:
            ErrorResponder.fill_error(return_obj, response_txt, ['message'])
        return return_obj

    def create_results_connection(self, search_id, offset, length):
        # search_id is the pattern
        observations = []
        return_obj = dict()

        bundle_url = self.connection.get('host')
        auth = self.configuration.get('auth')

        response = self.call_api(bundle_url, auth, 'get')

        response_code = response.status_code

        if response_code != 200:
            response_txt = response.raise_for_status()
            if ErrorResponder.is_plain_string(response_txt):
                ErrorResponder.fill_error(return_obj, message=response_txt)
            elif ErrorResponder.is_json_string(response_txt):
                response_json = json.loads(response_txt)
                ErrorResponder.fill_error(return_obj, response_json, ['reason'])
            else:
                raise UnexpectedResponseException
        else:
            bundle = response.json()

            if "validate" in self.configuration and self.configuration["validate"] is True:
                results = validate_instance(bundle)

                if results.is_valid is not True:
                    return {"success": False, "message": "Invalid STIX received: " + json.dumps(results)}

            for obj in bundle["objects"]:
                if obj["type"] == "observed-data":
                    observations.append(obj)

            # Pattern match
            results = self.match(search_id, observations, False)

            if len(results) != 0:
                return_obj['success'] = True
                return_obj['data'] = results[int(offset):int(offset + length)]
            else:
                return_obj['success'] = True
                return_obj['data'] = []

        return return_obj

    def delete_query_connection(self, search_id):
        return_obj = dict()
        return_obj['success'] = True
        return return_obj

    def call_api(self, bundle_url, auth, method):
        call = getattr(requests, method.lower())

        if auth is not None:
            username = auth.get('username')
            password = auth.get('password')
            if username is not None or password is not None:
                response = call(bundle_url, auth=(auth.get('username'), auth.get('password')))
            else:
                response = call(bundle_url)
        else:
            response = call(bundle_url)
        
        return response