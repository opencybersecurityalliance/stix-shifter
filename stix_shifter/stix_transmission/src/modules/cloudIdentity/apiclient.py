import base64
from ..utils.RestApiClient import RestApiClient
from . import CloudIdentity_Request, CloudIdentity_Token
import pprint
import json, requests
import re



class APIClient():
    PING_ENDPOINT = "v2.0/Users"
    def __init__(self, connection, configuration):
        
        headers = dict()
        url_modifier_function = None
        auth = configuration.get('auth')
        headers["Accept"] = "application/json, text/plain, */*"
        headers["Content-type"] = "application/json"

        self.indices = configuration.get('cloudIdentity', {}).get('indices', None)

        #Check for authentication type
        if auth:
           if 'tenant' in auth and 'clientId' in auth and 'clientSecret' in auth:
               #get token from specified cloud identity tenant
               headers["Authorization"] =  "Bearer " + self.getToken(auth['tenant'], auth['clientId'], auth['clientSecret'])
           elif 'token' in auth: 
               headers['Authorization'] = "Bearer " + auth['token']

        if isinstance(self.indices, list):  # Get list of all indices
            self.indices = ",".join(self.indices)

        if self.indices:
            self.endpoint = self.indices + '/' +'_search'
        else:
            self.endpoint = 'v2.0/Users'

    def run_search(self, query_expression):
        print("RUNNING SEARCH")
        
        ip, FROM, TO = self._parse_query(query_expression)
        try:
            #response = CloudIdentity_Request.postReports(token,"admin_activity", FROM, TO, 10, 'time', 'asc')
            #pp = pprint.PrettyPrinter(indent=1)
            #pp.pprint(response)
            

            return 
        except Exception as e:
            return

    #Retrieve valid token from Cloud Identity
    def getToken(self, uri, clientId, clientSecret):
        options = {
            'uri': uri+"/v2.0/endpoint/default/token",
            'client_id': clientId,
            'client_secret': clientSecret,
            'grant_type': "client_credentials"
        }
        resp = requests.post(uri+"/v2.0/endpoint/default/token", data=options)
        json_data = json.loads(resp.text)
        token = json_data['access_token']
        return token


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
