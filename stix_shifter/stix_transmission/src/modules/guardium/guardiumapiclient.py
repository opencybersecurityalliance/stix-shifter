from .utils.RestApiClient import RestApiClient
from .utils.RestApiClient import ResponseWrapper
from requests.models import Response
import urllib.parse
import sys
import json
import datetime
import os
import base64


class APIClient():

    # API METHODS

    # These methods are used to retrive a) authorization token using
    #   a rest api (sending credentials as params)
    #   b) reports (sending token and report query) using a different rest api

    # This class will encode any data or query parameters which will then be
    # sent to the call_api() method of the RestApiClient
    def __init__(self, connection, configuration):
#
        self.endpoint_start = 'restAPI/'
        self.connection = connection
        self.configuration = configuration
        self.headers = dict()
        self.search_id = None
        self.query = None
        self.authorization = None
        self.credential = None
#
# Check if connection object contains the following

        username = configuration.get('auth').get("username", None)
        password = configuration.get('auth').get("password", None)
        grant_type = connection.get('options',{}).get("grant_type", 'password')
        client_id = connection.get('options',{}).get("client_id", None)
        client_secret = connection.get('options',{}).get("client_secret", None)
# It is decided the authorization will not be sent by UDS
#
        if(username is None or password is None or grant_type is None or client_id is None or client_secret is None):
            self.credential = None
            raise IOError(
                    3001, "Guardium Credential not provided in the connection / configuration object")
        else:
            self.credential = {"username": username, "password": password, "grant_type": grant_type,
                               "client_id": client_id, "client_secret": client_secret}
#
        host_port = connection.get('host') + ':' + \
            str(connection.get('port', ''))

        url_modifier_function = None
        proxy = connection.get('proxy')
        if proxy is not None:
            proxy_url = proxy.get('url')
            proxy_auth = proxy.get('auth')
            if (proxy_url is not None and proxy_auth is not None):
                self.headers['proxy'] = proxy_url
                self.headers['proxy-authorization'] = 'Basic ' + proxy_auth
            if proxy.get('x_forward_proxy', None) is not None:
                self.headers['x-forward-url'] = 'https://' + \
                    host_port + '/'  # + endpoint, is set by 'add_endpoint_to_url_header'
                host_port = proxy.get('x_forward_proxy')
                if proxy.get('x_forward_proxy_auth', None) is not None:
                    self.headers['x-forward-auth'] = proxy.get(
                        'x_forward_proxy_auth')
                self.headers['user-agent'] = 'UDS'
                url_modifier_function = self.add_endpoint_to_url_header

        self.client = RestApiClient(host_port,
                                    None,
                                    connection.get('cert', None),
                                    self.headers,
                                    url_modifier_function,
                                    cert_verify=connection.get(
                                        'selfSignedCert', True),
                                    mutual_auth=connection.get(
                                        'use_securegateway', False),
                                    sni=connection.get('sni', None)
                                    )
#        self.client = RestApiClient(host_port,None,connection.get('cert', None),self.headers,
#                                    url_modifier_function,
#                                    connection.get('cert_verify', 'True'))
#
    def add_endpoint_to_url_header(self, url, endpoint, headers):
        # this function is called from 'call_api' with proxy forwarding,
        # it concatenates the endpoint to the header containing the url.
        headers['x-forward-url'] += endpoint
        # url is returned since it points to the proxy for initial call
        return url

    def add_header_elements(self, key, value):
        self.headers[key] = value
        return

    def ping_box(self):
        # Subroto -- Guardium does not have ping facility
        # We test if we can get the access token if we can then success = true
        #
        respObj = Response()
        if (self.fetch_accessToken()):
            respObj.code = "200"
            respObj.error_type = ""
            respObj.status_code = 200
            content = '{"status":"OK", "data": {"message": "Service is up."}}'
            respObj._content = bytes(content, 'utf-8')
        else:
            respObj.code = "503"
            respObj.error_type = "Service Unavailable"
            respObj.status_code = 503
            content = '{"status":"Failed", "data": {"message": "Service is down."}}'
            respObj._content = bytes(content, 'utf-8')
        # return
        return ResponseWrapper(respObj)
#
    def get_databases(self):
        # Sends a GET request
        endpoint = self.endpoint_start + 'databases'
        return self.client.call_api(endpoint, 'GET')

    def get_database(self, database_name):
        # Sends a GET request
        endpoint = self.endpoint_start + 'databases' + '/' + database_name
        return self.client.call_api(endpoint, 'GET')

    def isTimestampValid(self, tstamp):
        if tstamp is not None:
            if(tstamp > (datetime.datetime.now()).timestamp()):
                return True
        return False
#
    def get_credential(self):
        # Subroto -- Assumption: credential object will contain the full
        # guardium credential for the call in json format.  
        if self.credential is None:
            raise IOError(3001, "Guardium Credential object is found to be None. Error Raised.")
#
        else:
            data = urllib.parse.urlencode(self.credential)
#
        return data
#
    def fetch_accessToken(self):
        # process new authorization token
        # Get access token if not present
        # credential is a string contain a json
        #
        successVal = False
        #
        data = self.get_credential()
        #print(data)
        endpoint = "oauth/token"
        tNow = datetime.datetime.now()
        response = self.client.call_api(
            endpoint, "POST", params=data, data=None)
        jResp = json.loads(str(response.read(), 'utf-8'))
#
        #print(jResp)
        if (response.code != 200):
            #print(response.code)
            errMsg = str(jResp) + " -- " + "Authorization Token not received."
            raise ValueError(3002, errMsg)
        else:
            successVal = True
            tExp = (tNow + datetime.timedelta(seconds=jResp.get("expires_in"))).timestamp()
            self.authorization = json.loads(
                '{"access_token":"' + jResp.get("access_token") + '", "expiresTimestamp":' + str(tExp) + '}')
#
        #print(self.authorization)
        return successVal
#
    def get_accessToken(self):
        successVal = False
        if (self.authorization is not None):
            # Test for Authorization validity
            if self.isTimestampValid((self.authorization).get("expiresTimestamp")):
                successVal = True
                self.setAuthorizationHeader()
                return successVal
#
# We could not find a valid token from the  and now we request one
#
        if(self.fetch_accessToken()):
            successVal = True
            self.setAuthorizationHeader()
#
        return successVal
#
    def setAuthorizationHeader(self):
        auth = "Bearer " + \
                        str((self.authorization).get("access_token"))
#
# Test  -- uncomment to test token failure
        #auth = "Bearer 575d161c-9a91-4c05-bf0a-1c2d415a8c40"
        self.add_header_elements("authorization", auth)
        return
#
# NOTE: connector architecture forces sync connector behave as async connector
#       therefore, the state of the connector has to preserved in the search_id
#       which is not generated by Guardium.  We generate and store necessary status_code
#       such as self.credential, self.query (may be self.authorization)
#       IF search_id originally generated is changed then the state is lost

    def set_searchId(self, search_id):
        self.search_id = search_id
        return
#
    def build_searchId(self):
        #       It should be called only ONCE when transmit query is called
        # Structure of the search id is
        # '{"query": ' + json.dumps(self.query) + ', "credential" : ' + json.dumps(self.credential) + '}'
        s_id = None
#
        if(self.query is None or self.authorization is None or self.credential is None):
            raise IOError(3001, 
            "Could not generate search id because 'query' or 'authorization token' or 'credential info' is not available.")
#
        else:
            id_str = '{"query": ' + json.dumps(self.query) + ', "credential" : ' + json.dumps(self.credential) + '}'
            #print(id_str)
            id_byt = id_str.encode('utf-8')
            s_id = base64.b64encode(id_byt).decode()
            self.set_searchId(s_id)
#
        #print(s_id)
        return s_id
#
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
        self.credential = jObj.get("credential", None)
        self.authorization = jObj.get("authorization", None)
        return
#
    def get_searches(self):
        # CAN NOT be implemented for Guardium
        # 
        endpoint = self.endpoint_start + "searches"
        return self.client.call_api(endpoint, 'GET')
#
    def create_search(self, query_expression):
        # validate credential and create search_id.  No query submission -- Sync call
        # 
        respObj = Response()
        respObj.code = "401"
        respObj.error_type = ""
        respObj.status_code = 401
        if (self.get_accessToken()):
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
#
    def get_status(self, search_id):
        # Subroto we do not need to send anything to Guardium
        # We create response object and send "COMPLETED"
        # Note: we may have an issue with this simplistic approach
        respObj = Response()
        if (self.fetch_accessToken()):
            respObj.code = "200"
            respObj.error_type = ""
            respObj.status_code = 200
            content = '{"search_id": "' + search_id + \
                '", "progress":"Completed", "status":"COMPLETED", "data": {"message":"Completed for the search id provided."}}'
            respObj._content = bytes(content, 'utf-8')
        else:
            respObj.code = "503"
            respObj.error_type = "Service Unavailable"
            respObj.status_code = 503
            content = '{"status":"Failed", "data": {"message": "Could obtain status: Authentication issue / service unavailable."}}'
            respObj._content = bytes(content, 'utf-8')
        #
        return ResponseWrapper(respObj)
#
    def set_IndexAndFsize(self, indexFrom=None, fetchSize=None):
        data = json.loads(self.query)
        try:
            indx = int(indexFrom)
            fsize = int(fetchSize)
        except ValueError:
            print("Offset (indexFrom) or length (fetchSize) is not an integer")
#
#       replace the data string
        data["indexFrom"] = str(indx)
        data["fetchSize"] = str(fsize)
        return json.dumps(data)
#
    def get_search_results(self, search_id, response_type, indexFrom=None, fetchSize=None):
        # Sends a GET request from guardium
        # This function calls Guardium to get data
        self.set_searchId(search_id)
        self.decode_searchId()
#  replacement indexFrom and fetchSize
        data = self.set_IndexAndFsize(indexFrom, fetchSize)
#
        if (self.get_accessToken()):
            endpoint = self.endpoint_start + "online_report"
#
            response = self.client.call_api(endpoint, 'POST', params=None, data=data)
            status_code = response.response.status_code
#
#           Though the connector gets the authorization token just before fetching the actual result
#           there is a possibility that the token returned is only valid for a second and response_code = 401
#           is returned.  Catch that situation (though remote) and process again.
            if status_code != 200:
                error_msg = json.loads(str(response.read(), 'utf-8'))
                error_code = error_msg.get('error', None)
                if status_code == 401 and error_code == "invalid_token":
                    self.authorization = None
                    if (self.get_accessToken()):
                        response = self.client.call_api(endpoint, 'POST', params=None, data=data)
                        status_code = response.response.status_code
                    else:
                        raise ValueError(3002, "Authorization Token not received ")
#
# Now START and STOP are optional -- A situation can occur that data set can be empty -- handle this situation here
            if status_code == 200:
#
# Determine if the response is empty if empty Guardium sends {"ID": 0,
# "Message": "ID=0 The Query did not retrieve any records"} 
# Raise an error -->  1010: ErrorCode.TRANSMISSION_RESPONSE_EMPTY_RESULT
                # response_content = self.raiseErrorIfEmptyResult(response)
                return response
            else:
                raise ValueError(1020, "Error -- Status Code is NOT 200!")
        else:
            raise ValueError(3002, "Authorization Token not received ")
#           End of this function
    def raiseErrorIfEmptyResult(self, response):
        # Determine if the response is empty if empty Guardium sends {"ID": 0,
        # "Message": "ID=0 The Query did not retrieve any records"} <-- check that an raise and Error
        #               1010: ErrorCode.TRANSMISSION_RESPONSE_EMPTY_RESULT
        r_content_str = (response.read()).decode('utf8').replace("'", '"')
        response_content = json.loads(r_content_str)
        #print(r_content_str)
        if "ID" in response_content:
            #print(response_content)
            errMsg = response_content.get("Message", "Default Message - NO Records Fetched using this Query.")
            raise ValueError(1010, errMsg)
        else:
            return response_content
#
#
    def update_search(self, search_id, save_results=None, status=None):
        # Subroto -- not used in Guardium context
        # posts search result to site
        endpoint = self.endpoint_start + "searches/" + search_id
        data = {}
        if save_results:
            data['save_results'] = save_results
        if status:
            data['status'] = status
        data = urllib.parse.urlencode(data)
        data = data.encode('utf-8')
        return self.client.call_api(endpoint, 'POST', params=None, data=data)
#
    def delete_search(self, search_id):
        # Subroto -- not used.
        # deletes search created earlier.
        #endpoint = self.endpoint_start + "searches" + '/' + search_id
        #return self.client.call_api(endpoint, 'DELETE')
        return {"success": True, "search_id": search_id}
#
