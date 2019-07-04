from ..base.base_connector import BaseConnector

from stix2matcher.matcher import Pattern
from stix2matcher.matcher import MatchListener
from stix2validator import validate_instance
import json
import requests
from .....utils.error_response import ErrorResponder


class UnexpectedResponseException(Exception):
    pass


class Connector(BaseConnector):
    def __init__(self, connection, configuration):

        self.is_async = False
        self.connection = connection
        self.configuration = configuration
        self.results_connector = self
        self.query_connector = self
        self.ping_connector = self
        self.status_connector = self

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

    def ping(self):
        return {"success": True}

    def create_query_connection(self, query):
        return {"success": True, "search_id": query}

    def create_status_connection(self, search_id):
        return {"success": True, "status": "COMPLETED", "progress": 100}

    def create_results_connection(self, search_id, offset, length):
        # search_id is the pattern
        observations = []
        return_obj = dict()

        bundle_url = self.connection.get('host')
        auth = self.configuration.get('auth')

        if auth is not None:
            response = requests.get(bundle_url, auth=(auth.get('username'), auth.get('password')))
        else:
            response = requests.get(bundle_url)

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
