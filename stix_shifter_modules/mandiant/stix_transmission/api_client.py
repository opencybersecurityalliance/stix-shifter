
from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, date
from base64 import b64encode
import json
class APIClient():
    def __init__(self, connection, configuration):
        self.connection = connection
        self.namespace = connection.get('namespace')
        self.auth_data = configuration.get('auth')
        self.token = None
        self.token_url = 'api.intelligence.fireeye.com'
        self.url = 'api.intelligence.mandiant.com'

        # We create a new self.client after get_token w/ new headers
        APIv4_key = self.auth_data['key']
        APIv4_secret = self.auth_data['pwd']
        token = b64encode(f"{APIv4_key}:{APIv4_secret}".encode('utf-8')).decode('utf-8')
        headers = dict()
        headers['Authorization'] = f'Basic {token}'
        self.url_modifier_function = None
        self.client = RestApiClientAsync(host=self.token_url, port=None, headers=headers, url_modifier_function=self.url_modifier_function)

    async def ping_mandiant(self):
        ping_endpoint = 'token'
        ping_body = { 'grant_type': 'client_credentials' }
        ping_response = await self.client.call_api(ping_endpoint, 'POST', data=ping_body)
        return ping_response.read().decode('utf-8'), ping_response.code


    async def delete_search(self, search_id):
        # Delete the search - Optional since this may not be supported by the data source API
        return {"code": 200, "success": True}


    async def get_token(self):
        API_URL = 'token'
        data = { 'grant_type': 'client_credentials' }
        r = await self.client.call_api(API_URL, 'POST', data=data)
        data = json.loads(r.read().decode('utf-8'))
        auth_token = data.get('access_token')
        status = 'error'
        if r.code == 200: 
            status = 'ok'
            self.token = auth_token
        return {'status': status, 'token': auth_token}

    async def get_search_results(self, query_expression):
        auth = await self.get_token()
        headers = {
            'Accept': 'application/json',
            'X-App-Name': 'ibm-app',
            'Authorization': f"Bearer {auth['token']}"
        }
        self.client = RestApiClientAsync(host=self.url, port=None, headers=headers, url_modifier_function=self.url_modifier_function)
        data_type = query_expression['dataType']
        data = query_expression['data']
        query_url = 'v4/indicator/{type}/{value}?explainer=true'

        if data_type == 'ip':
            url = query_url.format(type="ipv4", value=str(data))
        elif data_type == 'url':
            url  = query_url.format(type="url", value=str(data))
        elif data_type == 'domain':
            url  = query_url.format(type="fqdn", value=str(data))
        elif data_type == 'hash':
            url  = query_url.format(type="md5", value=str(data))
        else:
            return {"code": 401, "error": "IoC Type not supported"}, self.namespace
        try:
            resp = await self.client.call_api(url, 'GET')
            json_data = json.loads(resp.read().decode('utf-8'))
        except Exception as e:
            return {'code': 500, 'error': f'OS error: {e}'}, self.namespace

        query_result = dict()    
        query_result["code"] = 200
        query_result["data"] = dict()
        query_result["data"]["success"] = True
        if json_data is None: 
            query_result["data"]["full"] = {
                "message": "IOC Not Found."
            }
        else:
            query_result["data"]["full"] = json_data

        return query_result, self.namespace
