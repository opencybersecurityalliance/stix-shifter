from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync
import json
import urllib
import requests
from urllib3.exceptions import InsecureRequestWarning
from urllib.parse import urlparse
from ipaddress import ip_address, IPv4Address


class APIClient():

    def __init__(self, connection, configuration):
        headers = dict()
        auth = configuration.get('auth')
        headers['X-OTX-API-KEY'] = auth.get('key')
        headers['Accept'] = "application/json"
        url_modifier_function = get_url_endpoint
        self.url = "https://otx.alienvault.com"
        self.namespace = connection.get('namespace')
        self.verify = configuration.get("verify", True)
        self.timeout = connection['options'].get('timeout')
        if not self.verify:
            requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        self.client = RestApiClientAsync(host=self.url,
                                    port=None,
                                    headers=headers,
                                    url_modifier_function=url_modifier_function,
                                    cert_verify=self.verify
                                    )

    async def ping_alienvault(self):
        # Pings the data source
        ping_endpoint = "/api/v1/user/me"
        ping_return = await self.client.call_api(ping_endpoint, 'GET', timeout=self.timeout)
        return ping_return.read(), ping_return.code

    async def get_search_results(self, query_expression, range_start=None, range_end=None):
        # Queries the data source
        # extract the data
        self.data_type = query_expression['dataType']
        self.data = query_expression['data']
        if self.data_type == 'ip':
            rep = await ip_query(self, self.data)
            return rep, self.namespace
        elif self.data_type == 'domain':
            rep = await domain_query(self, self.data)
            return rep, self.namespace
        elif self.data_type == 'url':
            rep = await url_query(self, self.data)
            return rep, self.namespace
        elif self.data_type == 'hash':
            rep = await hash_query(self, self.data)
            return rep, self.namespace
        else:
            return {"code": 401, "error": "IoC Type not supported"}, self.namespace

    async def delete_search(self, search_id):
        # Optional since this may not be supported by the data source API
        # Delete the search
        return {"code": 200, "success": True}

def get_url_endpoint(url, endpoint, headers=None):
        return url + endpoint

async def ip_query(self, data):
    response_data = dict()
    baseurl = ":443/api/v1/indicators/IPv4/%s/" % data
    analysis_url = "/otxapi/indicators/ip/analysis/%s/" % data
    
    try:
        query1 = await self.client.call_api(baseurl, 'GET', timeout=self.timeout)
        response1 = json.loads(query1.read().decode('utf-8')) if query1.code == 200 else {}
        query2 = await self.client.call_api(analysis_url, 'GET', timeout=self.timeout)
        response2 = json.loads(query2.read().decode('utf-8')) if query2.code == 200 else {}

        response_data = {**response1, **response2}

        if response_data.get('detections', {}).get('ids_detections'):
            response_data['ids_detections'] = response_data['detections']['ids_detections']
            del response_data['detections']['ids_detections']

        return prepare_response(self, response_data)
    except Exception as e:
        response_data["code"] = 500
        response_data["error"] = "OS error: {0}".format(e)
    return response_data

async def domain_query(self, data):
    response_data = dict()
    baseurl = ":443/api/v1/indicators/domain/%s/" % data
    analysis_url = "/otxapi/indicators/domain/analysis/%s/" % data

    try:
        query1 = await self.client.call_api(baseurl, 'GET', timeout=self.timeout)
        response1 = json.loads(query1.read().decode('utf-8')) if query1.code == 200 else {}
        query2 = await self.client.call_api(analysis_url, 'GET', timeout=self.timeout)
        response2 = json.loads(query2.read().decode('utf-8')) if query2.code == 200 else {}

        response_data = {**response1, **response2}
        return prepare_response(self, response_data)

    except Exception as e:
        response_data["code"] = 500
        response_data["error"] = "OS error: {0}".format(e)
    
    return response_data

async def hash_query(self, data):
    response_data = dict()
    baseurl = ":443/api/v1/indicators/file/%s/" % data
    analysis_url = "/otxapi/indicators/file/analysis/%s/" % data
    try:
        query1 = await self.client.call_api(baseurl, 'GET', timeout=self.timeout)
        response1 = json.loads(query1.read().decode('utf-8')) if query1.code == 200 else {}
        query2 = await self.client.call_api(analysis_url, 'GET', timeout=self.timeout)
        response2 = json.loads(query2.read().decode('utf-8')) if query2.code == 200 else {}

        response_data = {**response1, **response2}

        rules = response_data.get('analysis', {}).get('plugins', {}).get('cuckoo', {}).get('result', {}).get('suricata', {}).get('rules', {})
        if rules:
            response_data['ids_detections'] = rules

        return prepare_response(self, response_data)
    except Exception as e:
        response_data["code"] = 500
        response_data["error"] = "OS error: {0}".format(e)

    return response_data

async def url_query(self, data):
    response_data = dict()
    # data = urllib.parse.quote_plus(data)
    data = data.replace('/', '%252F')
    analysis_url = "/otxapi/indicators/url/analysis/%s" % data
    try:
        query1 = await self.client.call_api(analysis_url, 'GET', timeout=self.timeout)
        response1 = json.loads(query1.read().decode('utf-8')) if query1.code == 200 else {}
        query2 = await self.client.call_api(analysis_url, 'GET', timeout=self.timeout)
        response2 = json.loads(query2.read().decode('utf-8')) if query2.code == 200 else {}
        response_data = {**response1, **response2}
        return prepare_response(self, response_data)

    except Exception as e:
        response_data["code"] = 500
        response_data["error"] = "OS error: {0}".format(e)
    
    return response_data

def prepare_response(self, response):
    response_data = dict()
    response_data["code"] = 200
    response_data["data"] = {
        "success" : True,
        "full" : response   
    }

    return response_data
