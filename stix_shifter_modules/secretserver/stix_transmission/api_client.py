import base64
import json
import re
from datetime import date, timedelta
import requests
import os
from requests import Response
from stix_shifter_utils.utils import logger
from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient, ResponseWrapper
from .secretserver_utils import SecretServerApiClient
from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient, ResponseWrapper, \
    CONNECT_TIMEOUT_DEFAULT

import random

class APIClient():

    def __init__(self, connection, configuration):
         self.url = "https://"+connection["host"]
         self.auth_token_url = "https://"+connection["host"]+"/SecretServer/oauth2/token"
         self.event_url = "https://" + connection["host"]+"/SecretServer/api/v1/reports/execute"
         self.secret_detail = "/SecretServer/api/v1/secrets"
         self.payload = 'username=%s&password=%s&grant_type=password' % (
             configuration["auth"]["username"], configuration["auth"]["password"])
         self.server_ip = connection["host"]
         self.client = SecretServerApiClient(self.url)

    def get_token(self):

        self.headers = {
            'Authorization': 'Basic',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        self.data = self.payload
        self.response = requests.request("POST", self.auth_token_url, headers=self.headers, data=self.payload,
                                         verify=False)
        self.res = self.response.text
        self.json_obj = json.loads(self.res)
        self.token = self.json_obj.get('access_token')
        self.accessToken = 'Bearer' + " " + self.token
        return self.accessToken

    def ping_data_source(self):
        response = requests.request("POST", self.auth_token_url, headers=self.headers, data=self.payload)
        return response.status_code

    def create_search(self, query_expression):
        respObj = Response()
        if (self.get_token()):
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

    def build_searchId(self):
        # It should be called only ONCE when transmit query is called
        # Structure of the search id is
        # '{"query": ' + json.dumps(self.query) + ', "url" : ' + secretserverurl '}'
        s_id = None
        num = str(random.randint(0, 50))
        if (self.query is None):
            raise IOError(3001,
                          "Could not generate search id because 'query' or 'authorization token' or 'credential info' is not available.")
        else:
            # id_str = '{"query": ' + json.dumps(self.query) + ', "target" : "' + self.url + '" + "random" : "' + str(random.randint(0,22)) + '"}'
            id_str = '{"query": ' + json.dumps(
                self.query) + ', "target" : "' + self.url + '", "random":"' + num + '"}'
            id_byt = id_str.encode('utf-8')
            s_id = base64.b64encode(id_byt).decode()
            self.search_id = s_id
        return s_id

    def get_search_results(self, search_id, index_from=None, fetch_size=None):
        # Sends a GET request from secret server
        # This function calls secret server to get data
        if (self.get_token()):
            self.search_id = search_id
            timestamp = self.decode_searchId()
            if len(timestamp) is not 0:
                self.startDate = timestamp[0]
                self.endDate = timestamp[1]
            else:
                self.startDate = date.today()
                self.endDate = self.startDate - timedelta(days = 1)
            self.connect_timeout = os.getenv('STIXSHIFTER_CONNECT_TIMEOUT', CONNECT_TIMEOUT_DEFAULT)
            self.connect_timeout = int(self.connect_timeout)
            self.server_cert_content = False
            self.auth = None
            self.sni = None
            self.retry_max = 1
            self.logger = logger.set_logger(__name__)
            self.server_cert_file_content_exists = False
            self.url_modifier_function = None
            resp = SecretServerApiClient.get_response(self)
            return resp

    def decode_searchId(self):
        # These value (date, self.query) must be present.
        try:
            id_dec64 = base64.b64decode(self.search_id)
            jObj = json.loads(id_dec64.decode('utf-8'))
        except:
            raise IOError(
                3001, "Could not decode search id content - " + self.search_id)
        self.query = jObj.get("query", None)
        try:
            timestamp = re.findall(r'\d{4}-\d{2}-\d{2}', self.query)
        except:
            raise IOError(
                " Could not extract date- " + self.search_id)
        return timestamp

    def delete_search(self, search_id):
        # Optional since this may not be supported by the data source API
        # Delete the search
        return {"code": 200, "success": True}

