import json
from datetime import datetime, timedelta
from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync
from stix_shifter_utils.utils import logger


class APIClient:

    endpoint_start = 'v1.0/events'
    token_endpoint = 'v1.0/endpoint/default/token'

    def __init__(self, connection, configuration):
        self.logger = logger.set_logger(__name__)

        headers = dict()
        url_modifier_function = None
        auth = configuration.get('auth')
        # self.endpoint_start = 'incidents/'
        self.host = connection.get('host')
        self.client = RestApiClientAsync(connection.get('host'), connection.get('port', None),
            headers,url_modifier_function=url_modifier_function,
            cert_verify=connection.get('selfSignedCert', False)
            )
        self.timeout = connection['options'].get('timeout')
        self._client_id = auth['clientId']
        self._client_secret = auth['clientSecret']
        self._token = None
        self._token_time = None
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

    async def get_token(self):
        """get the token and if expired re-generate and store in token variable"""
        return await self.generate_token()

    async def generate_token(self):
        """To generate the Token"""
        if self.token_expired():
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            data=(
                f'client_id={self._client_id}'
                f'&client_secret={self._client_secret}'
                f'&grant_type=client_credentials'
                f'&scope=openid'
            )
            response = await self.client.call_api(self.token_endpoint, 'POST', headers=headers, data=data, timeout=self.timeout)
            response_txt = response.read().decode('utf-8')

            try: 
                response_dict = json.loads(response_txt)
                self._token = response_dict.get('access_token')
                self._token_time = datetime.now()
            except Exception as e:
                pass

        return self._token

    def token_expired(self) -> bool:
        """Check if the verify token is expired.
        :return: True if token is expired, False if not expired
        :return type: bool
        """
        expired = True
        if self._token:
            expired = (datetime.now() - self._token_time) >= timedelta(minutes=30)
        return expired

    async def run_search(self, query_expr, range_end=None):
        """get the response from verify endpoints
        :param quary_expr: dict, filter parameters
        :param range_end: int,length value
        :return: response, json object"""
        events = []
        # if self._token :
        events = await self.get_events(query_expr)
        return self.response_handler(events, query_expr)

    async def get_events(self, query_expr):
        token = await self.get_token()
        self.headers['Authorization'] = f'Bearer {token}'
        return await self.client.call_api(
            self.endpoint_start,
            'GET',
            self.headers,
            urldata=query_expr,
            timeout=self.timeout)

    def response_handler(self, data, query_expr=None):
        response = {}
        try:
            buf = data.read()
            buf = json.loads(buf)
        except json.JSONDecodeError:
            buf = ''
        response['data'] = buf
        response['error'] = data.code
        response['code'] = data.code
        response['error_msg'] = data.response.reason
        response['success'] = data.code
        if response['code'] == 200:
            response['search_after'] = response.get("data")['response']['events']['search_after']

            try:
               response['event_data'] = self.parseJson(response.get("data")['response']['events']['events'])
            except KeyError:
                self.logger.debug('events data not found in respose object %s', response)
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
                self.logger.debug('key not found: %s', key)
                return False
        return True

    async def get_search(self, search_id):
        # Sends a GET request to
        # https://<server_ip>/api/ariel/searches/<search_id>
        response = await self.run_search(search_id)
        return response
        
    async def delete_search(self,search_id):
        return await self.run_search(search_id)
