import base64
import json
import re
from datetime import date, timedelta
from dateutil import parser
import os
from datetime import datetime
from requests import Response
from stix_shifter_utils.utils import logger
from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync, ResponseWrapper, \
    CONNECT_TIMEOUT_DEFAULT
import random
from stix_shifter_utils.utils.error_response import ErrorResponder


class APIClient():
    
    def __init__(self, connection, configuration):
         self.url = "https://"+connection["host"]
         self.auth_token_url = "/SecretServer/oauth2/token"
         self.secret_detail = "/SecretServer/api/v1/secrets"
         self.connect_timeout = os.getenv('STIXSHIFTER_CONNECT_TIMEOUT', CONNECT_TIMEOUT_DEFAULT)
         self.connect_timeout = int(self.connect_timeout)
         self.server_cert_content = False
         self.auth = None
         self.sni = None
         self.retry_max = 1
         self.logger = logger.set_logger(__name__)
         self.server_cert_file_content_exists = False
         self.url_modifier_function = None
         self.headers = {
             'Content-Type': 'application/x-www-form-urlencoded'
         }
         self.payload = 'username=%s&password=%s&grant_type=password' % (
             configuration["auth"]["username"], configuration["auth"]["password"])
         self.server_ip = connection["host"]

    async def get_token(self):
        response = await RestApiClientAsync.call_api(self, self.auth_token_url, 'GET', headers=self.headers,
                                          data=self.payload,
                                          urldata=None,
                                          timeout=None)

        return_obj = {}
        response_code = response.code
        response_txt = response.response.text

        if (response_code == 200):
            json_obj = json.loads(response_txt)
            token = json_obj.get('access_token')
            self.accessToken = 'Bearer' + " " + token
            return self.accessToken
        else:
            ErrorResponder.fill_error(return_obj, message=response_txt)
            raise Exception(return_obj)

    async def ping_data_source(self):
        response = await RestApiClientAsync.call_api(self, self.auth_token_url, 'GET', headers=self.headers, data=self.payload,
                                          urldata=None,
                                          timeout=None)
        return response.code

    async def create_search(self, query_expression):
        respObj = Response()
        token = await self.get_token()
        if (token):
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
        return ResponseWrapper(respObj)

    def build_searchId(self):
        # It should be called only ONCE when transmit query is called
        # Structure of the search id is
        # '{"query": ' + json.dumps(self.query) + ', "url" : ' + secretserverurl '}'
        num = str(random.randint(0, 50))
        if (self.query is None):
            raise IOError(3001,
                          "Could not generate search id because 'query' or 'authorization token' or 'credential info' is not available.")
        else:
            id_str = '{"query": ' + json.dumps(
                self.query) + ', "target" : "' + self.url + '", "random":"' + num + '"}'
            id_byt = id_str.encode('utf-8')
            s_id = base64.b64encode(id_byt).decode()
            self.search_id = s_id
        return s_id

    async def get_search_results(self, search_id, index_from, fetch_size):
        # Sends a GET request from secret server
        # This function calls secret server to get data
        token = await self.get_token()
        if (token):

            self.search_id = search_id
            timestamp = self.decode_searchId()
            if len(timestamp) != 0:
                self.startDate = timestamp[0]
                self.endDate = timestamp[1]
            else:
                self.startDate = date.today()
                self.endDate = self.startDate - timedelta(days = 1)
            response = await self.get_response()
            return response
  
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
            pattern = re.compile("\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z")
            matcher = pattern.findall(self.query)
            matches = []
            for match in matcher:
                dt = parser.parse(match)
                matches.append(dt.strftime("%Y-%m-%d %H:%M:%S"))
        except:
            raise IOError(
                " Could not extract date- " + self.search_id)
        return matches

    async def get_events(self):
        payload = "{\"name\": \"Secret Server Events Logs\", \"parameters\": [{\"name\": \"startDate\", \"value\": '%s'} , {\"name\":\"endDate\",\"value\": '%s'}]}" % (
            self.startDate, self.endDate)
        headers = {
            'Authorization': self.accessToken,
            'Content-Type': 'application/json'
        }
        endpoint = "SecretServer/api/v1/reports/execute"

        response = await RestApiClientAsync.call_api(self, endpoint, 'POST', headers=headers, data=payload, urldata=None,
                                          timeout=None)
        return_obj = {}
        if response.code != 200:
            response_txt = response.response.text
            ErrorResponder.fill_error(return_obj, message=response_txt)
            raise Exception(return_obj)

        collection = []
        json_data = response.response.text
        eventData = json.loads(json_data)
        col = eventData['columns']
        for obj in eventData['rows']:
            obj = dict(zip(col, obj))
            collection.append(obj)
        return collection

    async def get_Secret(self):
        eventDetail = await self.get_events()
        secretIdList = []
        secretCollection = []
        for obj in eventDetail:
            item = (obj['ItemId'])
            secretIdList.append(item)
        unique = set(secretIdList)
        for id in unique:
            secret_server_user_url = self.secret_detail + "/%s" % id
            headers = {
                'Authorization': self.accessToken,
                'Content-Type': 'application/json'
            }
            payload = {}
            response = await RestApiClientAsync.call_api(self, secret_server_user_url, 'GET', headers=headers, data=payload,
                                              urldata=None,
                                              timeout=None)

            secretCollection.append(response.response.text)
        json_data = json.dumps(secretCollection)
        collection = json.loads(json_data)
        return collection

    async def get_response(self):
        eventDetail = await self.get_events()
        secretDetail = await self.get_Secret()
        updateSecret = []
        secretCollection = {}
        updateCollection = []
        for obj in secretDetail:
            next = json.loads(obj)
            updateSecret.append(next)
        for item in eventDetail:
            for getId in updateSecret:
                if (item['ItemId'] == getId['id']):
                    data = getId['items']
                    for secret in data:
                        if (secret['fieldName'] == 'Server'):
                            secretCollection[str(secret['fieldName'])] = str(secret['itemValue'])
                            item.update(secretCollection)
                            updateCollection.append(item)
        return updateCollection

    async def delete_search(self, search_id):
        # Optional since this may not be supported by the data source API
        # Delete the search
        return {"code": 200, "success": True}
