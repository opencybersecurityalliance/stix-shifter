from ..utils.RestApiClient import RestApiClient
from ..utils.RestApiClient import ResponseWrapper
from requests.models import Response
import urllib.parse
import logging
import sys
import json
import datetime
import os
import base64


class APIClient():

    # API METHODS

    # These methods are used to call Ariel's API methods through http requests.
    # Each method makes use of the http methods below to perform the requests.

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
        self.credential = {}

#
# Check if connection object contains the following
 
        username = connection.get("username", None)
        password = connection.get("password", None)
        grant_type = connection.get("grant_type", None)
        client_id = connection.get("client_id", None)
        client_secret = connection.get("client_secret", None)
        access_token = connection.get("guardium_access_token", None)
        expiresTimestamp = connection.get(
            "guardium_token_expiryTimestamp", None)
#
#       if the connection object does not contain the credential -- it can be picked from this folder
#       this may not be implemented.
        self.credential_filepath = "./stix_shifter/stix_transmission/src/modules/guardium/credentials/"
#
        if(username is None or password is None or grant_type is None or client_id is None or client_secret is None):
            self.credential = {}
            logging.info(
                    "Guardium Credential not provided in the connection object")
            raise IOError(
                    3001, "Guardium Credential not provided in the connection object")
        else:
            self.credential = {"username": username, "password": password, "grant_type": grant_type,
                               "client_id": client_id, "client_secret": client_secret}
# Check if the access_token sent has not expired
        self.authorization = {}
        if access_token is not None:
            if self.isTimestampValid(expiresTimestamp):
                self.authorization = json.loads(
                    '{"access_token":"' + str(access_token) + '", "expiresTimestamp":' + str(expiresTimestamp) + "'}")
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
                                    connection.get('cert_verify', 'True')
                                    )

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
        logging.info("--------- Guardium ping_box ------\n")
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
        # changed by Subroto: https://<server_ip>/api/ariel/searches/<search_id>
        # endpoint = self.endpoint_start + "searches/" + search_id
        # return self.client.call_api(endpoint, 'GET')
        return ResponseWrapper(respObj)
        # Sends a GET request
        # to https://<server_ip>/api/help/resources
        # endpoint = 'api/help/resources'  # no 'ariel' in the path
        # return self.client.call_api(endpoint, 'GET')

    def get_databases(self):
        # Sends a GET request
        # to  https://<server_ip>/api/ariel/databases
        endpoint = self.endpoint_start + 'databases'
        return self.client.call_api(endpoint, 'GET')

    def get_database(self, database_name):
        # Sends a GET request
        # to https://<server_ip>/api/ariel/databases/<database_name>
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
        # guardium credential for the call.  There is an option to read it from a file too
        # proviee the path name if we want to read this credential from a file
        if self.credential is None:
            self.credential = self.read_credential_from_file()
#
        jCred = self.credential
#
        data = 'client_id=' + jCred.get("client_id") + '&grant_type=' + str(jCred.get("grant_type")) + \
               '&client_secret=' + str(jCred.get("client_secret")) + '&username=' + str(jCred.get("username")) + \
               '&password=' + str(jCred.get("password"))
        print("credential data: " + data)
        return data
#
    def read_credential_from_file(self):
        # Subroto -- Assumption: credential from a file if the setup is done 
        # self.credential_file is None.  Do not read from the file
        username = self.connection.get("username", "admin")
        host = self.connection.get("host")
        if self.credential_filepath is not None:
            path = self.credential_filepath
            credFile = path + username + "_" + host.replace(".", "_") + ".json"
            exists = os.path.isfile(credFile)
            if exists:
                with open(credFile, 'r') as f_cred:
                    jCred = json.loads(f_cred.read())
            else:
                logging.info(
                    "Credential not provided or could not get from the - " + credFile)
                raise IOError(
                    3001, "Credential not provided or could not get from the - " + credFile)
        else:
            jCred = None
            logging.info("Credential file path is not provided -- Need authorized credential")

        return jCred

    def fetch_accessToken(self):
        # process new authorization token
        # Get access token if not present
        # credential is a string contain a json
        #
        successVal = False
#        username = self.connection.get("username", "admin")
#        host = self.connection.get("host")
        #
        data = self.get_credential()
        endpoint = "oauth/token"
        tNow = datetime.datetime.now()
        logging.debug("Fetch Access Token: Calling:" + str(data))
        response = self.client.call_api(
            endpoint, "POST", params=data, data=None)
        #jResp = json.loads(response.read()) -- Changed
        jResp = json.loads(str(response.read(), 'utf-8'))
        print(response.code)
        print(jResp)

        if (response.code != 200):
            logging.info(
                "Authorization Token NOT Received. Response code: " + str(response.code))
            raise ValueError(3002, "Authorization Token not received ")
        else:
            successVal = True
            tExp = tNow.timestamp() + jResp.get("expires_in")
            self.authorization = json.loads(
                '{"access_token":"' + jResp.get("access_token") + '", "expiresTimestamp":' + str(tExp) + '}')
        return successVal

    def get_accessToken(self):
        successVal = False
        if (self.authorization is not None):
            # Test for Authorization validity
            if self.isTimestampValid((self.authorization).get("expiresTimestamp")):
                successVal = True
                self.setAuthorizationHeader()
                return successVal
            else:
                logging.info("Expired access token.  Get a new access token.")
        else:
            logging.info(
                "Authorization token is not found. Get a new access token")
#
# We could find a valid token from the  and now we request one
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
        self.add_header_elements("authorization", auth)
        return
#
# NOTE: connector architecture forces sync connector behave as async connector
#       therefore, the state of the connector has to preserved in the search_id
#       which is not generated by Guardium.  We generate and store necessary status_code
#       such as # self.authorization, self.credential, self.query
#       IF search_id originally generated is changed then the state is lost

    def set_searchId(self, search_id):
        self.search_id = search_id
        return
#

    def build_searchId(self):
        #       It should be called only ONCE
        s_id = None
#
        if(self.query is None or self.authorization is None or self.credential is None):
            logging.info(
                "Could not generate search id because 'query' or 'authorization token' or 'credential info' is not available.")
#
        else:
            id_str = '{"query": ' + json.dumps(self.query) + ', "credential" : ' + json.dumps(self.credential) + \
                     ', "authorization" : ' + \
                json.dumps(self.authorization) + '}'
            print(id_str)
            id_byt = id_str.encode('utf-8')
            s_id = base64.b64encode(id_byt)
            self.set_searchId(s_id)

#
        print(s_id)
        return s_id

    def decode_searchId(self):
        # self.authorization, self.credential, self.query
        try:
            id_dec64 = base64.b64decode(self.search_id)
            jObj = json.loads(id_dec64.decode('utf-8'))
        except:
            logging.info(
                "Could not decode search id content - " + self.search_id)
            raise IOError(
                3001, "Could not decode search id content - " + self.search_id)
#
        self.query = jObj.get("query", None)
        logging.debug("Query Decoded: \n")
        logging.debug(self.query)
        self.credential = jObj.get("credential", None)
        self.authorization = jObj.get("authorization", None)

        return

    def get_searches(self):
        # Sends a GET request
        # to https://<server_ip>/api/ariel/searches
        endpoint = self.endpoint_start + "searches"
        return self.client.call_api(endpoint, 'GET')

    def create_search(self, query_expression):
        # Sends a POST request
        # to https://<server_ip>/api/ariel/searches
        logging.info("--------- Guardium get access token: \n")
        respObj = Response()
        respObj.code = "401"
        respObj.error_type = ""
        respObj.status_code = 401
        if (self.get_accessToken()):
            logging.info("--------- Guardium create search: \n")
            self.query = query_expression
            response = self.build_searchId()
            if (response != None):
                respObj.code = "200"
                respObj.error_type = ""
                respObj.status_code = 200
                content = '{"search_id": "' + \
                    str(response) + \
                    '", "data": {"message":  "Search id generated."}}'
                # print(content)
                respObj._content = bytes(content, 'utf-8')
                logging.info(
                    "------ Return encoded search Id: " + str(response))
            else:
                respObj.code = "404"
                respObj.error_type = "Not found"
                respObj.status_code = 404
                respObj.message = "Could not generate search id."
                logging.info(
                    "------ Return encoded search Id: " + str(response))
        else:
            logging.info("Access Token -- could not be generated. ")
            respObj.error_type = "Unauthorized: Access token could not be generated."
            respObj.message = "Unauthorized: Access token could not be generated."

#
        return ResponseWrapper(respObj)

    def get_status(self, search_id):
        # Subroto we do not need to send anything to Guardium
        # We create response object and send "COMPLETED"
        # Note: we may have an issue with this simplistic approach
        logging.info("--------- Guardium get_status ------\n")
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
        # changed by Subroto: https://<server_ip>/api/ariel/searches/<search_id>
        # endpoint = self.endpoint_start + "searches/" + search_id
        # return self.client.call_api(endpoint, 'GET')
        return ResponseWrapper(respObj)

    def set_IndexAndFsize(self, indexFrom=None, fetchSize=None):
        #
        data = json.loads(self.query)
        try:
            indx = int(indexFrom)
            fsize = int(fetchSize)
        except ValueError:
            print("Offset (indexFrom) or length (fetchSize) is not an integer")
#
#       replace the data string
        # print(indx)
        # print(fsize)
        data["indexFrom"] = str(indx)
        data["fetchSize"] = str(fsize)
        # print(data)
        return (json.dumps(data))

    def get_search_results(self, search_id, response_type, indexFrom=None, fetchSize=None):
        # Sends a GET request from guardium
        # This function calls Guardium to get data
        self.set_searchId(search_id)
        self.decode_searchId()
        logging.info("--------- Guardium get result -- access token.")

        if (self.get_accessToken()):
            logging.info(" Access Token received.\n")
            endpoint = self.endpoint_start + "online_report"
#
#  replacement indexFrom and fetchSize
            data = self.set_IndexAndFsize(indexFrom, fetchSize)
            logging.info(
                "--------- Guardium get result -- decoded search id for query expression: " + data)
            response = self.client.call_api(
                endpoint, 'POST', params=None, data=data)
            logging.debug("Response code: " +
                          str(response.response.status_code) + "\n")
            #logging.debug("Response headers:\n " + str(response.response.headers) + "\n")
            #logging.debug("Response content: " + str(response.read()) + "\n")
            logging.info("------ Return Wrapped Response Object --------")
            return response
        else:
            logging.info("Access Token -- could not be generated. ")
            return None

    def update_search(self, search_id, save_results=None, status=None):
        # Subroto -- not used.
        # Sends a POST request to
        # https://<server_ip>/api/ariel/searches/<search_id>
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

    def delete_search(self, search_id):
        # Subroto -- not used.
        # Sends a DELETE request to
        # https://<server_ip>/api/ariel/searches/<search_id>
        # deletes search created earlier.
        # Subroto: we can delete the stored result file if present ... change this code.
        endpoint = self.endpoint_start + "searches" + '/' + search_id
        return self.client.call_api(endpoint, 'DELETE')

    def readResultFile(self, searchId):
        rFilename = "./stix_shifter/stix_transmission/src/modules/guardium/output/result_" + \
            str(searchId) + ".json"
        logging.debug("Reading file: " + rFilename)
        exists = os.path.isfile(rFilename)
        if exists:
            with open(rFilename, 'r') as f_res:
                jRes = json.loads(f_res.read())
            if not ("content" in jRes):
                jRes = None
        else:
            logging.debug("File does not exist.")
            jRes = None
        return jRes
