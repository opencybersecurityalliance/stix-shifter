from ..utils.RestApiClient import RestApiClient
from ..utils.RestApiClient import ResponseWrapper
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

        respObj = Response()
        
        if(self.getToken()):
            self.query = query_expression
            response = self.build_searchId()
            if (response != None):
                respObj.code = "200"
                respObj.error_type = ""
                respObj.status_code = 200
                content = '{"search_id": "' + \
                    str(response) + \
                    '", "data": {"message":  "Search id generated."}}'
                respObj._content = bytes(content, 'utf-8')
            else:
                respObj.code = "404"
                respObj.error_type = "Not found"
                respObj.status_code = 404
                respObj.message = "Could not generate search id."
        else:
            respObj.error_type = "Unauthorized: Access token could not be generated."
            respObj.message = "Unauthorized: Access token could not be generated."
#
        return ResponseWrapper(respObj)

    def get_search_status(self, search_id):
        # Check the current status of the search
        return {"code": 200, "search_id": search_id, "status": "COMPLETED"}

    def get_search_results(self, search_id, FROM=None, TO=None):
        # Return the search results. Results must be in JSON format before being translated into STIX
        
        pp = pprint.PrettyPrinter(indent=1)
        self.build_searchId()
        self.decode_searchId()

        request_params = self.parse_query()
        return_obj = dict()

        #If input query contains user-account:user_id(MAPS TO)->user_id connector will getUser{user_id} in api_client
        if "user_id" in request_params:
            user_obj = self.getUser(request_params['user_id'])
            #if(self.checkResponse(user_obj)):
            return_obj = json.loads(user_obj.read())

                #pp.pprint(return_obj)

        if "username" in request_params:
            user_obj = self.getUserWithFilters(request_params)
            
            #pp.pprint(user_obj)
            return user_obj
            #return_obj = json.loads(user_obj.read())['Resources']
                #pp.pprint(return_obj)

        #If input query contains ipv4:value(MAPS TO)->origin -- if present call events and find all ip's that match
        if "origin" in request_params and "FROM" in request_params and "TO" in request_params:
            return_obj = self.search_events(request_params, "origin")
            #pp.pprint(return_obj)


        #retValue = json.dumps(return_obj)
        return retValue
       
    def delete_search(self, search_id):
        # Optional since this may not be supported by the data source API
        # Delete the search
        return "Deleted query: {}".format(search_id)

    def set_searchId(self, search_id):
        self.search_id = search_id
        return

    def build_searchId(self):
        #       It should be called only ONCE when transmit query is called
        # Structure of the search id is
        # '{"query": ' + json.dumps(self.query) + ', "credential" : ' + json.dumps(self.credential) + '}'
        s_id = None

        if(self.query is None or self.authorization is None or self.credentials is None):
            raise IOError(3001, 
            "Could not generate search id because 'query' or 'authorization token' or 'credential info' is not available.")
#
        else:
            id_str = '{"query": ' + json.dumps(self.query) + ', "credential" : ' + json.dumps(self.credentials) + '}'
            #print(id_str)
            id_byt = id_str.encode('utf-8')
            s_id = base64.b64encode(id_byt).decode()
            self.set_searchId(s_id)

        return s_id

    def decode_searchId(self):
        # These value (self.credential, self.query) must be present.  self.authorization may not.
        try:
            id_dec64 = base64.b64decode(self.search_id)
            jObj = json.loads(id_dec64.decode('utf-8'))
        except:
            raise IOError(
                3001, "Could not decode search id content - " + self.search_id)
#
        self.query = jObj.get("query", None)
        self.credentials = jObj.get("credentials", None)
        self.authorization = jObj.get("authorization", None)
        return

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

    def parse_query(self):
        
        requests = self.query.split(' ')
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