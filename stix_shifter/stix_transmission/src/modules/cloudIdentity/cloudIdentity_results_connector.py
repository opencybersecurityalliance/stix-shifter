from ..base.base_connector import BaseConnector
from ..base.base_results_connector import BaseResultsConnector
import json
import pprint
from .....utils.error_response import ErrorResponder


class CloudIdentityResultsConnector(BaseConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def create_results_connection(self, search_id, offset, length):
        
        pp = pprint.PrettyPrinter(indent=1)
        return_obj = dict()
        request_params = self.parse_query(search_id)

        #If input query contains user-account:user_id(MAPS TO)->user_id connector will getUser{user_id} in api_client
        if "user_id" in request_params:
            user_obj = self.api_client.getUser(request_params['user_id'])
            if(self.checkResponse(user_obj)):
                return_obj = json.loads(user_obj.read())
                #pp.pprint(return_obj)

        if "username" in request_params:
            user_obj = self.api_client.getUserWithFilters(request_params)
            if(self.checkResponse(user_obj)):
                return_obj = json.loads(user_obj.read())['Resources']
                #pp.pprint(return_obj)

        #If input query contains ipv4:value(MAPS TO)->origin -- if present call events and find all ip's that match
        if "origin" in request_params and "FROM" in request_params and "TO" in request_params:
            return_obj = self.api_client.search_events(request_params, "origin")
            pp.pprint(return_obj)

        retValue = json.dumps(return_obj)
        return retValue

    def parse_query(self, query):
        requests = query.split(' ')
        params = dict()

        #Iterate over query string and assign variables i.e. user-account, ipv4 etc
        for index in range(len(requests)):
            if(requests[index] == "user_id"):
                params["user_id"] = requests[index+2].strip("''")
            elif(requests[index] == "username"):
                params['username'] = requests[index+2].strip("''")
            elif(requests[index] == "origin"):
                params['origin'] = requests[index+2].strip("''")
            elif(requests[index] == "FROM"):
                params['FROM'] = requests[index+1].strip("t''")
            elif(requests[index] == "TO"):
                params['TO'] = requests[index+1].strip("t''")
    
        return params

    def checkResponse(self, response):
        if(response.code == 200):
            return True
        
        return False