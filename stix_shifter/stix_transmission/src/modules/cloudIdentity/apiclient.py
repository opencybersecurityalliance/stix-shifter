import base64
from ..utils.RestApiClient import RestApiClient
from . import CloudIdentity_Request
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
        self.uri = auth.get('tenant')
        print(self.uri)
        self.indices = configuration.get('cloudIdentity', {}).get('indices', None)

        #Check for authentication type and create a cloud identity token used from requests
        if auth:
           if 'tenant' in auth and 'clientId' in auth and 'clientSecret' in auth:
               #get token from specified cloud identity tenant
               self.token = self.getToken(auth['tenant'], auth['clientId'], auth['clientSecret'])
           elif 'token' in auth: 
               self.token = auth['token']

        if isinstance(self.indices, list):  # Get list of all indices
            self.indices = ",".join(self.indices)

        if self.indices:
            self.endpoint = self.indices + '/' +'_search'
        else:
            self.endpoint = 'v2.0/Users'

    def run_search(self, query_expression):
        #Creates variables for CI
        ip, FROM, TO = self._parse_query(query_expression)

        #REST call to CI 
        report_response = self.postReports("auth_audit_trail", FROM, TO, 10, 'time', 'asc')

        #Makes return json easier to read 
        pp = pprint.PrettyPrinter(indent=1)
        #pp.pprint(response)

        #refine json response to individual hits
        hits = report_response['response']['report']['hits']
        user_response = dict()
        
        #Iterate over hits object
        for index in hits:
            #Compare CI report origin/ip to input IP 
            if(str(index['_source']['data']['origin'] == ip)):
                #REST call to CI on specified user_id
                user_response = self.getUser(id=hits[0]['_source']['data']['subject'])

        
        pp.pprint(user_response)
        return report_response

    #Retrieve valid token from Cloud Identity
    def getToken(self, uri, clientId, clientSecret):
        options = {
            'uri': uri+"/v2.0/endpoint/default/token",
            'client_id': clientId,
            'client_secret': clientSecret,
            'grant_type': "client_credentials"
        }
        try:
            resp = requests.post(uri+"/v2.0/endpoint/default/token", data=options)

        except Exception as e:
            print("failed to create token")
            print(e)

        json_data = json.loads(resp.text)
        token = json_data['access_token']
        return token

    #Returns given report from cloud identity tenant
    def postReports(self, reportName, FROM, TO, SIZE, SORT_BY, SORT_ORDER, SEARCH_AFTER = None):
        url = self.uri + f"/v1.0/reports/{reportName}"
        headers = { "Accept": "application/json, text/plain, */*","Content-Type": "application/json", "authorization": "Bearer "+ self.token}
        body = {
            "FROM": FROM,
            "TO": TO,
            "SIZE": SIZE,
            "SORT_BY": SORT_BY,
            "SORT_ORDER": SORT_ORDER
        }
        if ("after" in reportName):
            body.update(SEARCH_AFTER)

        try:
            res = requests.post(url, json=body, headers=headers)

            jsonData = res.json()
            return jsonData
        except Exception as e:
            print("Could not retrieve report "+ reportName)
            print(e)

    def getUser(self, id):
        url = self.uri + f"/v2.0/Users/{id}"

        headers = { "Accept": "application/json, text/plain, */*","authorization": "Bearer "+self.token}
        try:
            res = requests.get(url, headers=headers)

            jsonData = res.json()
            return jsonData
        except Exception as e:
            print("User id invalid")
            print(e)

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
