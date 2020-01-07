from ..utils.RestApiClient import RestApiClient
from requests.models import Response
import base64
import urllib.parse
import pprint
import json, requests
import re



class APIClient():
    
    def __init__(self, connection, configuration):
        
        self.connection = connection
        self.configuration = configuration
        self.headers = dict()
        self.search_id = None
        self.query = None 
        self.authroization = None
        self.credential = None
        self.host = connection.get('host')
        self.host_port = connection.get('port')
        self.client = RestApiClient(self.host)


        #Check for token 
        if(configuration.get('auth').get('token') is not None):
            self.token = configuration.get('auth').get('token')
        #Check for client_id and client_secret if true initialize token
        elif(configuration.get('auth').get("clientId") is not None 
        and configuration.get('auth').get("clientSecret") is not None
        and configuration.get('auth').get("tenant") is not None):
            self.uri = configuration.get('auth').get("tenant")
            self.token = self.getToken(self.uri, configuration.get('auth').get("clientId"),configuration.get('auth').get("clientSecret"))
        else:
            print("No Token initialized. Tenant client Id and client secret is required")

        
        


    def run_search(self, query_expression):
        #Creates variables for CI
        ip, FROM, TO = self._parse_query(query_expression)

        #Different types for reports to be called 
        report_response = self.postReports("auth_audit_trail", FROM, TO, 10, 'time', 'asc')
        #events_response = self.getEvents(FROM, TO)


        #Makes return json easier to read 
        pp = pprint.PrettyPrinter(indent=1)

        #refine json response to individual hits and events
        report_hits = report_response['response']['report']['hits']
        #event_hits = events_response['response']['events']['events']

        user_response = dict()

        #pp.pprint(events_response)
        
        #Iterate over hits object
        for index in report_hits:
            #Compare CI report origin/ip to input IP 
            if(str(index['_source']['data']['origin'] == ip)):
                #REST call to CI on specified user_id
                user_response = self.getUser(id=report_hits[0]['_source']['data']['subject'])

        #pp.pprint(user_response)
        
        return report_response

    #Retrieve valid token from Cloud Identity
    def getToken(self, uri, client_id, client_secret):

        options = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials"
        }

        endpoint = "v2.0/endpoint/default/token"
        resp = self.client.call_api(endpoint, "POST", data=options)

        jresp = json.loads(str(resp.read(), 'utf-8'))
        return jresp.get('access_token')
        

    #Returns given report from cloud identity tenant
    def postReports(self, reportName, FROM, TO, SIZE, SORT_BY, SORT_ORDER, SEARCH_AFTER = None):
        endpoint = "v1.0/reports/" + reportName

        headers = dict()
        headers["Accept"] = "application/json, text/plain, */*"
        headers["Content-Type"] = "application/json"
        headers["authorization"] = "Bearer "+ self.token

        data = dict()
        data["FROM"] = FROM
        data["TO"] = TO
        data["SIZE"] = SIZE
        data["SORT_BY"] = SORT_BY
        data["SORT_ORDER"] = SORT_ORDER

        d = json.dumps(data)
        resp = self.client.call_api(endpoint, "POST", headers = headers, data=d)
        jresp = json.loads(str(resp.read(), 'utf-8'))

        return jresp

    def getEvents(self, FROM, TO):
        
        endpoint = f"/v1.0/events?from={FROM}&to={TO}&range_type=time"

        headers = dict()
        headers['Accept'] = "application/json, text/plain, */*"
        headers['authorization'] = "Bearer "+self.token

        response = self.client.call_api(endpoint, 'GET', headers=headers)
        jresp = json.loads(str(response.read(), 'utf-8'))

        return jresp
       
    def getUser(self, id):
        endpoint = f"/v2.0/Users/{id}"

        headers = dict()
        headers['Accept'] = "application/json, text/plain, */*"
        headers['authorization'] = "Bearer "+self.token

        response = self.client.call_api(endpoint, 'GET', headers=headers)
        jresp = json.loads(str(response.read(), 'utf-8'))
        return jresp

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
