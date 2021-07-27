import base64
import json
import re
import datetime
import requests
from requests import Response
from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient, ResponseWrapper
from .secretserver_utils import SecretServerApiClient
import random

class APIClient():

    def __init__(self, connection, configuration):
         self.url = "http://"+connection["host"]
         self.auth_token_url = "http://"+connection["host"]+"/SecretServer/oauth2/token"
         self.event_url = "http://" + connection["host"]+"/SecretServer/api/v1/reports/execute"
         self.user_detail = self.url + "/SecretServer/api/v1/secrets"
         self.payload = 'username=%s&password=%s&grant_type=password' % (configuration["auth"]["username"], configuration["auth"]["password"])
         self.headers = {
             'Authorization': 'Basic YWRtaW46cGFzc3dvcmRAMTI=',
             'Content-Type': 'application/x-www-form-urlencoded'
         }
         self.data = self.payload
         self.response = requests.request("POST", self.auth_token_url, headers=self.headers, data=self.payload)
         self.res = self.response.text
         self.json_obj = json.loads(self.res)
         self.token = self.json_obj.get('access_token')
         self.accessToken = 'Bearer' + " " + self.token
         self.client = SecretServerApiClient(self.url)

    def ping_data_source(self):
        # Pings the data source
        # return SecretServerApiClient.ping(self)
        data = self.payload
        response = requests.request("POST", self.auth_token_url, headers=self.headers, data=self.payload)
        return response.status_code

    def create_search(self, query_expression):
        respObj = Response()
        respObj.code = "401"
        respObj.error_type = ""
        respObj.status_code = 401
        if (self.token):
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

    def get_status(self, search_id):
        # It is a synchronous connector.
        # return {"code": 200, "status": "COMPLETED"}
        respObj = Response()
        respObj.code = "200"
        respObj.error_type = ""
        respObj.status_code = 200
        content = '{"search_id": "' + search_id + \
                  '", "progress":100, "status":"COMPLETED", "data": {"message":"Completed for the search id provided."}}'
        respObj._content = bytes(content, 'utf-8')
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
        if (self.token):
            self.search_id = search_id
            date = self.decode_searchId()
            if len(date) is not 0:
                self.startDate = date[0]
                self.endDate = date[1]
            else:
                lastupdate = (datetime.datetime.now() - datetime.timedelta(days=90)).replace(tzinfo=datetime.timezone.utc).timestamp()
                self.startDate = datetime.datetime.date(datetime.fromtimestamp(lastupdate)).strftime("%s")
                self.endDate =date.today()
            resp = SecretServerApiClient.get_events(self)
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
        date = re.findall(r'\d{4}-\d{2}-\d{2}', self.query)
        if date == []:
           print("Please enter the date")
        return date

    def delete_search(self, search_id):
        # Optional since this may not be supported by the data source API
        # Delete the search
        return {"code": 200, "success": True}

