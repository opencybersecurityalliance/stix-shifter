from ..base.base_connector import BaseConnector

from stix2matcher.matcher import Pattern
from stix2matcher.matcher import MatchListener
from stix2validator import validate_instance
import json, requests

class Connector(BaseConnector):
    def __init__(self, connection, configuration):

        self.is_async = False

        self.connection = connection
        self.configuration = configuration

        self.results_connector = self
        self.query_connector = self
        self.ping_connector = self

    #We re-implement this method so we can fetch all the "bindings", as their method only 
    #returns the first for some reason
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
        return {"success":True} 

    def create_query_connection(self, query):
        return { "success": True, "search_id": query }

    def create_results_connection(self, search_id, offset, length):
        #search_id is the pattern
        observations = []

        if "http_user" in self.configuration:
            response = requests.get(self.configuration["bundle_url"],auth=(self.configuration["http_user"], self.configuration["http_password"]))
        else:
            response = requests.get(self.configuration["bundle_url"])

        if response.status_code != 200:
            response.raise_for_status()

        bundle = response.json()

        if "validate" in self.configuration and self.configuration["validate"] is True:
            results = validate_instance(bundle)
 
            if results.is_valid is not True:
                return { "success":False, "message":"Invalid STIX recieved: " + json.dumps(results) }
        
        for obj in bundle["objects"]:
            if obj["type"] == "observed-data":
                observations.append( obj )

        #Pattern match
        results = self.match(search_id, observations, False)

        return results[ int(offset):int(offset + length) ]


