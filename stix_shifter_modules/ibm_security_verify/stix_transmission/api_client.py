import json
from datetime import datetime, timedelta
from urllib.parse import urlencode

import requests
from requests.adapters import Response
from stix_shifter_utils.stix_transmission.utils.RestApiClient import \
    RestApiClient
from stix_shifter_utils.utils import logger


class APIClient:

    endpoint_start = '/v1.0/events'
    toeken_endpoint = '/v1.0/endpoint/default/token'

    def __init__(self, connection, configuration):
        self.logger = logger.set_logger(__name__)

        headers = dict()
        url_modifier_function = None
        auth = configuration.get('auth')
        # self.endpoint_start = 'incidents/'
        self.host = connection.get('host')
        self.client = RestApiClient(connection.get('host'), connection.get('port', None),
            headers,url_modifier_function=url_modifier_function,
            cert_verify=connection.get('selfSignedCert', False),
            sni=connection.get('sni', None)
            )
        self.timeout = connection['options'].get('timeout')
        self._client_id = auth['clientId']
        self._client_secret = auth['clientSecret']
        self._token = None
        self._token_time = None
         
    def get_token(self):
        """get the token and if expired re-generate and store in token variable"""
        tokenResponse = self.generate_token()
        return tokenResponse.json().get('access_token')

    def generate_token(self):
        """To generate the Token"""
        if self.token_expired():
            resp = requests.request(
                'POST',
                'https://'+self.host+self.toeken_endpoint,
                headers={
                    'accept': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                data=(
                    f'client_id={self._client_id}'
                    f'&client_secret={self._client_secret}'
                    f'&grant_type=client_credentials'
                    f'&scope=openid'
                )
            )
            token = resp.json().get('access_token')
            self._token = token
            self._token_time = datetime.now()
            self.resp =resp
        return self.resp

    def token_expired(self) -> bool:
        """Check if the verify token is expired.
        :return: True if token is expired, False if not expired
        :return type: bool
        """
        expired = True
        if self._token:
            expired = (datetime.now() - self._token_time) >= timedelta(minutes=30)
        return expired


    def run_search(self, query_expr, range_end=None):
        """get the response from verify endpoints
        :param quary_expr: dict, filter parameters
        :param range_end: int,length value
        :return: response, json object"""
        events = []
        # if self._token :
        events = self.get_events(query_expr)
        return self.response_handler(events,query_expr)


    def get_events(self,query_expr):
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {0}'.format(self.get_token())}
        if query_expr is None:
            data=None
        return self.client.call_api(self.endpoint_start,'GET',self.headers,urldata= query_expr)

    def response_handler(self, data=None,query_expr=None):
        if data is None:
            data = []
        response = dict()
        response['data'] =json.loads(data.read())
        response['error'] = data.code
        response['code'] =data.code
        response['error_msg'] = data.response.reason
        response['success'] =data.code
        if response['code'] ==200:
           
            response['search_after'] = response.get("data")['response']['events']['search_after']

            try:
               response['event_data'] = self.parseJson(response.get("data")['response']['events']['events'])
            except KeyError:
                self.logger.debug('events data not found in respose object',response)
                response['event_data'] = []

        elif response['error'] == 500 and "true" in response['error_msg']:
            response.update({"code": 200, "data": []})
        else:
            response["message"] = data.response.reason
        
        return response
    
    
    def parseJson(self, response):
        '''
        Iterate through the response and read the nested data like geoip and data object.
        '''
        jsonObj = response
        finalJson = dict()
        parsedJson = []
        for obj in jsonObj:
            dictC = obj
            if "geoip" in dictC:
                dictA= json.loads(json.dumps(obj["geoip"]))  
                del dictC["geoip"]          
                dictB= json.loads(json.dumps(obj["data"]))          
                del dictC["data"]     
                dict_geo_location = json.loads(json.dumps(dictA.get('location')))     
                del dictA['location']
                finalJson = {**dictA,**dictB,**dict_geo_location}
            else:
                dictB= json.loads(json.dumps(obj["data"]))          
                del dictC["data"]                    
                finalJson = dictB
            remainingJson = json.loads(json.dumps(dictC))
            finalJson = {**finalJson,**remainingJson}
            parsedJson.append(finalJson)
        return parsedJson


    def key_exist(self,data_element, *keysarr) :
        '''
        Check if *keys (nested) exists in `element` (dict).
        '''
        if not isinstance(data_element, dict):
            raise AttributeError('keys_exists() expects dict as first argument.')
        if len(keysarr) == 0:
            raise AttributeError('keys_exists() expects at least two arguments, one given.')

        _element = data_element
        for key in list(keysarr):
            try:
                _element = _element[key]
            except KeyError:
                self.logger.debug('key not found ',key )
                return False
        return True

    def get_search_results(self, search_id, response_type, range_start=None, range_end=None):
        # Sends a GET request to
        # https://<server_ip>//<search_id>
        # response object body should contain information pertaining to search.
        #https://isrras.ice.ibmcloud.com/v1.0/events?event_type="sso"&size=10&after="1640104162523","eeb40fd5-6b84-4dc9-9251-3f7a4cfd91c0"
        headers = dict()
        headers['Accept'] = response_type
        size = 1000
        if ((range_start is  None) and (range_end is  None)):
            size = range_end - range_start
        
        request_param = search_id+"& size="+str(size)
        endpoint = self.endpoint_start+ request_param

        return self.run_search(search_id)   

    def get_search(self, search_id):
        # Sends a GET request to
        # https://<server_ip>/api/ariel/searches/<search_id>
        response = self.run_search(search_id)
        return response
        
    def delete_search(self,search_id):
        return self.run_search(search_id)
