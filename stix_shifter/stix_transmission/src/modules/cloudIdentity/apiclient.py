import base64
from ..utils.RestApiClient import RestApiClient
from . import CloudIdentity_Request, CloudIdentity_Token
import json
import re



class APIClient():

    def __init__(self, connection, configuration):
        headers = { "Accept": "application/json, text/plain, */*","Content-Type": "application/json", "authorization": "Bearer "+CloudIdentity_Token.getToken()}
        url_modifier_function = None
        auth = configuration.get('auth')
        self.indices = configuration.get('elastic_ecs', {}).get('indices', None)

        if isinstance(self.indices, list):  # Get list of all indices
            self.indices = ",".join(self.indices)

        if self.indices:
            self.endpoint = self.indices + '/' +'_search'
        else:
            self.endpoint = '_search'
        

    def ping_data_source(self):
        # Pings the data source
        return "async ping"

    def create_search(self, query_expression):
        # Queries the data source
        print("In APICLIENT, query: " + query_expression)
        return {
            "code": 200,
            "query_id": "uuid_1234567890"
        }

    def get_search_status(self, search_id):
        # Check the current status of the search
        return {"code": 200, "search_id": search_id, "status": "COMPLETED"}

    def get_search_results(self, search_id, range_start=None, range_end=None):
        # Return the search results. Results must be in JSON format before being translated into STIX
        return {"code": 200, "search_id": search_id, "data": "Results for search"}

    def delete_search(self, search_id):
        # Optional since this may not be supported by the data source API
        # Delete the search
        return "Deleted query: {}".format(search_id)
