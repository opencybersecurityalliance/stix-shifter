from ..utils.RestApiClient import RestApiClient
from requests.models import Response
import base64
import urllib.parse
import pprint
import json, requests
import re
import datetime



class APIClient():
    
    def __init__(self, connection, configuration):
        
        self.connection = connection
        self.configuration = configuration
        self.headers = dict()
        self.search_id = None
        self.query = None 
        self.authorization = None
        self.credentials = None
        self.headers = dict()

        self.client = RestApiClient(host=connection.get('host'), 
                                    port=connection.get('port', None))
        #Init connections
        client_id = configuration.get('auth').get("clientId", None)
        client_secret = configuration.get('auth').get("clientSecret", None)
        tenant = configuration.get('auth').get('tenant', None)
        self.token = configuration.get('auth').get('token', None)

        #Init host/port
        host = connection.get('host')
        port = connection.get('port', None)

        #TODO enable a proxy to connect to Cloud Identity
        if(client_id is not None and client_secret is not None and tenant is not None):
            self.credentials = {"tenant": tenant, "client_id": client_id, "client_secret": client_secret}
            self.token = self.getToken()
        else: 
            self.credentials = None           
            raise IOError (3001, "Cloud Identity Credentials not provided in connection/configuration")

        #Init communication to Cloud Identity Tenant
        

        # Init base headers
        self._add_headers('Accept', "application/json, text/plain, */*")
        self._add_headers("Content-Type", "application/json")

    # Searches both reports and events from Cloud Identity 
    def run_search(self, query_expression):
        #Run search on Cloud identity reports  
        report_response = self.search_reports(query_expression)

        #Run search on cloud identity events
        #events_response = self.search_events(query_expression)
        
        #TODO integrate event/report responses
        
        return report_response

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
        return self.run_search(search_id)

    def delete_search(self, search_id):
        # Optional since this may not be supported by the data source API
        # Delete the search
        return "Deleted query: {}".format(search_id)


    #NOTE All functions below are either Cloud Identity REST calls or modifier functions 


    def search_reports(self, params):
        #Creates variables for CI
        

        resp = self.postReports("auth_audit_trail", params["FROM"], params["TO"], 10, 'time', 'asc')
        #refine json response to individual hits and events
        report_hits = resp['response']['report']['hits']
        
        #Makes return json easier to read 
        pp = pprint.PrettyPrinter(indent=1)
        pp.pprint(report_hits)

        return resp
    #Using search params to envoke event search -- target is used to pull out data from
    #event if present
    def search_events(self, params, target):
        return_obj = dict()
        resp = self.getEvents(params["FROM"], params["TO"])

        #refine json response to individual hits and events
        event_hits = resp['response']['events']['events']
        pp = pprint.PrettyPrinter(indent=1)
        #pp.pprint(event_hits[0])
        #Search events for target origin
        return_obj = self._parse_events(event_hits, target, params[target])
        #pp.pprint(return_obj)
        return return_obj

    def get_credentials(self):
        if self.credentials is None:
            raise IOError("Cloud Identity Credential object is None")
        else: 
            data = self.credentials

        return data

    #Retrieve valid token from Cloud Identity
    def getToken(self):

        success = False
        if(self.authorization is not None):
            if (self.isTokenExpired((self.authorization).get("expiresTimestamp"))):
                success = True 
                self._addAuthHeader()
                return success

        
        if(self._getToken()):
            success = True
            self._addAuthHeader()

        return success

    def _getToken(self):
        success = False

        auth = self.get_credentials()

        options = {
            "client_id": auth.get("client_id"),
            "client_secret": auth.get("client_secret"),
            "grant_type": "client_credentials"
        }

        endpoint = "v2.0/endpoint/default/token"

        time = datetime.datetime.now()
        resp = self.client.call_api(endpoint, "POST", data=options)
        jresp = json.loads(str(resp.read(), 'utf-8')) 

        if(resp.code != 200):
            raise ValueError(str(jresp) + " -- Access Token not received")
        else:
            success = True
            exTime = (time + datetime.timedelta(seconds=jresp.get("expires_in"))).timestamp()
            self.authorization = json.loads('{"access_token":"' + jresp.get("access_token") + '", "expiresTimestamp":' + str(exTime) + '}')

        return success
        
    def isTokenExpired(self, exTime):
        if exTime is not None:
            if(exTime > (datetime.datetime.now()).timestamp()):
                return True
        return False

    #Returns given report from cloud identity tenant
    def postReports(self, reportName, FROM, TO, SIZE, SORT_BY, SORT_ORDER, SEARCH_AFTER = None):
        endpoint = "v1.0/reports/" + reportName

        data = dict()
        data["FROM"] = FROM
        data["TO"] = TO
        data["SIZE"] = SIZE
        data["SORT_BY"] = SORT_BY
        data["SORT_ORDER"] = SORT_ORDER

        data = json.dumps(data)
        resp = self.client.call_api(endpoint, "POST", headers = self.headers, data=data)
        jresp = json.loads(str(resp.read(), 'utf-8'))
    
        return jresp

    def getEvents(self, FROM, TO):
        
        endpoint = f"/v1.0/events?&from={FROM}&to={TO}&range_type=time"

        response = self.client.call_api(endpoint, 'GET', headers=self.headers)
        jresp = json.loads(str(response.read(), 'utf-8'))
        obj = jresp['response']['events']['events']

        #pp = pprint.PrettyPrinter(indent=1)
        #pp.pprint(obj)

        return jresp
       
    def getUser(self, id):
        
        endpoint = "/v2.0/Users/" + id
        response = self.client.call_api(endpoint, 'GET', headers=self.headers)
        jresp = json.loads(str(response.read(), 'utf-8'))

        return response
    
    def getUserWithFilters(self, params):
        endpoint = "/v2.0/Users?filter="
        if "username" in params:
            endpoint = endpoint + "userName%20eq%20%20%22" + params['username'] + "%22"

        response = self.client.call_api(endpoint, 'GET', headers=self.headers)
        jresp = json.loads(str(response.read(), 'utf-8'))

        return response

    #Iterate over eventsObj searching for target to create a return_obj
    #NOTE for now target = ipv4/origin

    def _parse_events(self, eventsObj, target, value):

        pp = pprint.PrettyPrinter(indent=1)
        numResponse = 0 
        return_obj = dict()
        #hit is each individual event that occurs
        for hit in eventsObj:
            #test if event has target variable and target value = input value
            if target in hit['data'] and hit['data'][target] == value:
                return_obj['data'] = hit['data']
                if "geoip" in hit:
                    return_obj["geoip"] = hit['geoip']

        pp.pprint(return_obj)
        return return_obj

    def _add_headers(self, key, value):
        self.headers[key] = value
        return

    def _addAuthHeader(self):
        auth = "Bearer " + str(self.authorization.get("access_token"))
        self._add_headers("authorization", auth)
        return