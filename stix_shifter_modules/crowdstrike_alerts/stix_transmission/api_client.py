"""Apiclient for Crowdstrike Alerts"""
import json
from urllib.parse import urlencode
from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync
from datetime import datetime, timedelta
from stix_shifter_utils.utils import logger

class APIResponseException(Exception):
    def __init__(self, error_code, error_message, content_header_type, response):
        self.error_code = error_code
        self.error_message = error_message
        self.content_header_type = content_header_type
        self.response = response
    pass

class APIClient:
    ALERT_IDS_ENDPOINT = 'alerts/queries/alerts/v2'
    ALERT_INFO_ENDPOINT = 'alerts/entities/alerts/v2'
    TOKEN_ENDPOINT = 'oauth2/token'
    logger = logger.set_logger(__name__)

    """API Client to handle all calls."""

    def __init__(self, connection, configuration):
        """Initialization.
        :param connection: dict, connection dict
        :param configuration: dict,config dict"""
        headers = dict()
        self.client = RestApiClientAsync(connection.get('host'), connection.get('port', None), headers)
        
        self.timeout = connection['options'].get('timeout')

        self.headers = dict()
        self.headers['Content-Type'] = 'application/json'
        self.headers['Accept'] = 'application/json'
        self.headers['user-agent'] = 'oca_stixshifter_1.0'
        
        self.auth_headers = dict()
        self.auth_headers['accept'] = 'application/json'
        self.auth_headers['user-agent'] = 'oca_stixshifter_1.0'
        self.auth_headers['Content-Type'] = 'application/x-www-form-urlencoded'

        auth = configuration.get('auth')
        self.authentication_body=(f'client_id={auth["client_id"]}&client_secret={auth["client_secret"]}'
        )
        
        self._token_time = datetime.now() - timedelta(days=7)

    async def ping_box(self):
        self.headers['Authorization'] =f'Bearer {await self.get_token()}'
        return await self.client.call_api(self.ALERT_IDS_ENDPOINT, 'GET', headers=self.headers, timeout=self.timeout)

    async def get_alert_IDs(self, filter, offset, batch_size):
        self.headers['Authorization'] =f'Bearer {await self.get_token()}'
        endpoint = self.ALERT_IDS_ENDPOINT + "?filter=" + filter + "&limit=" + batch_size + "&offset=" + offset
        return await self.client.call_api(endpoint, 'GET', headers=self.headers, timeout=self.timeout)

    async def get_alert_info(self, ids):
        self.headers['Authorization'] =f'Bearer {await self.get_token()}'
        ids_expression = json.dumps({'composite_ids': ids}).encode("utf-8")
        return await self.client.call_api(self.ALERT_INFO_ENDPOINT, 'POST', headers=self.headers, data=ids_expression, timeout=self.timeout)

    async def get_token(self) -> str:
        self.logger.debug(f"Checking if the current token has expired. Token Creation time was {self._token_time}")
        if (datetime.now() - self._token_time) >= timedelta(minutes=30):
            self.logger.debug(f"Attempting to get a new authenctication token")

            get_token_response = await self.client.call_api(self.TOKEN_ENDPOINT, 'POST', headers=self.auth_headers, data=self.authentication_body, timeout=self.timeout)
            #A successful response can be 200 or 201.
            if get_token_response.code >= 200 and get_token_response.code < 300:
                
                self.logger.debug(f"Get authentication token was successful.")
                response_json = json.loads(get_token_response.read().decode('utf-8'))
                if 'access_token' in response_json:
                    self.logger.debug(f"Get authentication token included an authentication token. Setting the authentication values.")
                    token = response_json.get('access_token')
                    self._token = token
                    self._token_time = datetime.now()
            else:
                self.logger.debug(f"Get authentication token was not successful.")
                raise APIResponseException(get_token_response.code, get_token_response.content, get_token_response.headers.get('Content-Type'), get_token_response)
        return self._token