import base64
from ..utils.RestApiClient import RestApiClient
from . import CloudIdentity_Request, CloudIdentity_Token
import pprint
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
        
    def run_search(self, query_expression):
        token = CloudIdentity_Token.getToken()
        
        ip, FROM, TO = self._parse_query(query_expression)
        try:
            response = CloudIdentity_Request.postReports(token,"admin_activity", FROM, TO, 10, 'time', 'asc')
            pp = pprint.PrettyPrinter(indent=1)
            pp.pprint(response)
            print(response)

            return response
        except Exception as e:
            return

        

    #Parse out meaningful data from input query   
    def _parse_query(self, query):

        request = query.split(' ')
        
        for index in range(len(request)):
            if(request[index] == "origin"):
                ip = request[index+2]
            if(request[index] == "FROM"):
                FROM = request[index+1]
            if(request[index] ==  "TO"):
                TO = request[index+1]
        
        FROM = FROM.strip("t''")
        TO = TO.strip("t''")
        return ip, FROM, TO

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

    def get_search_results(self, search_id, FROM=None, TO=None):
        # Return the search results. Results must be in JSON format before being translated into STIX
        return {"code": 200, "search_id": search_id, "data": "Results for search"}

    def delete_search(self, search_id):
        # Optional since this may not be supported by the data source API
        # Delete the search
        return "Deleted query: {}".format(search_id)
