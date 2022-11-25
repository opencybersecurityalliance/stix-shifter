"""Apiclient for MSATP"""
import json
from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync
from datetime import datetime, timedelta


class APIClient:
    INCIDENTS_IDS_ENDPOINT = 'detects/queries/detects/v1'
    INCIDENTS_INFO_ENDPOINT = 'detects/entities/summaries/GET/v1'
    TOKEN_ENDPOINT = 'oauth2/token'
    """API Client to handle all calls."""

    def __init__(self, connection, configuration):
        """Initialization.
        :param connection: dict, connection dict
        :param configuration: dict,config dict"""

        headers = dict()
        url_modifier_function = None
        auth = configuration.get('auth')
        # self.endpoint_start = 'incidents/'
        self.host = connection.get('host')
        self.client = RestApiClientAsync(connection.get('host'),
                                    connection.get('port', None),
                                    headers,
                                    url_modifier_function=url_modifier_function,
                                    cert_verify=connection.get('selfSignedCert', True),
                                    sni=connection.get('sni', None)
                                    )
        self.timeout = connection['options'].get('timeout')
        self._client_id = auth['client_id']
        self._client_secret = auth['client_secret']
        self._token = None
        self._token_time = None

    async def get_detections_IDs(self, filter, limit, sort=None):
        """get the response from MSatp endpoints
        :param filter: filter incidents by certain value
        :param sort: sort incidents according to sort value
        :return: response, json object"""
        headers = dict()
        data = dict()
        token = await self.get_token()
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'
        headers['Authorization'] = f'Bearer {token}'
        endpoint = self.INCIDENTS_IDS_ENDPOINT
        data['filter'] = filter
        data['limit'] = limit
        if sort:
            data['sort'] = sort
        return await self.client.call_api(endpoint, 'GET', headers=headers, urldata=data, timeout=self.timeout)

    async def ping_box(self):
        # Sends a GET request
        headers = dict()
        token = await self.get_token()
        headers['Authorization'] = f'Bearer {token}'
        endpoint = 'detects/queries/detects/v1'  # Test if system alive
        return await self.client.call_api(endpoint, 'GET', headers=headers, timeout=self.timeout)

    async def get_detections_info(self, ids):
        """get the response from crowdstrike endpoints
        :param ids: Provide one or more incident IDs
        :return: response, json object"""
        headers = dict()
        token = await self.get_token()
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'
        headers['Authorization'] = f'Bearer {token}'
        endpoint = self.INCIDENTS_INFO_ENDPOINT
        ids_expression = json.dumps({'ids': ids}).encode("utf-8")
        return await self.client.call_api(endpoint, 'POST', headers=headers, data=ids_expression, timeout=self.timeout)

    async def get_token(self) -> str:
        """Request a new OAuth2 token.
        :return: [description]
        :rtype: str
        """
        if self.token_expired():

            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            data = (
                f'client_id={self._client_id}'
                f'&client_secret={self._client_secret}'
            )
            resp = await self.client.call_api(self.TOKEN_ENDPOINT, 'POST', headers=headers, data=data, timeout=self.timeout)
            response_code = resp.code
            response_txt = resp.read().decode('utf-8')
            if 199 < response_code < 300:
                response_json = json.loads(response_txt)
                if 'access_token' in response_json:
                    token = response_json.get('access_token')
                    self._token = token
                    self._token_time = datetime.now()
        return self._token

    def token_expired(self) -> bool:
        """Check if the OAuth2 token is expired.
        :return: True if token is expired, False if not expired
        :rtype: bool
        """
        expired = True
        if self._token:
            expired = (datetime.now() - self._token_time) >= timedelta(minutes=30)
        return expired
