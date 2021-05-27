"""Apiclient for MSATP"""
import json
from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient
from datetime import datetime, timedelta
import requests

DEFAULT_LIMIT = 10000
DEFAULT_OFFSET = 0


class APIClient:
    INCIDENTS_IDS_ENDPOINT = 'detects/queries/detects/v1'
    INCIDENTS_INFO_ENDPOINT = 'detects/entities/summaries/GET/v1'
    TOKEN_ENDPOINT = 'https://api.crowdstrike.com/oauth2/token'
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

        # if auth:
        #     if 'access_token' in auth:
        #         headers['Authorization'] = "Bearer " + auth['access_token']

        self.client = RestApiClient(connection.get('host'),
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

    def get_detections_IDs(self, filter, sort=None):
        """get the response from MSatp endpoints
        :param filter: filter incidents by certain value
        :param sort: sort incidents according to sort value
        :return: response, json object"""
        headers = dict()
        data = dict()
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'
        headers['Authorization'] = f'Bearer {self.get_token()}'
        endpoint = self.INCIDENTS_IDS_ENDPOINT
        data['filter'] = filter
        if sort:
            data['sort'] = sort
        return self.client.call_api(endpoint, 'GET', headers=headers, urldata=data, timeout=self.timeout)

    def get_detections_info(self, ids, offset=DEFAULT_OFFSET, length=DEFAULT_LIMIT):
        """get the response from crowdstrike endpoints
        :param ids: Provide one or more incident IDs
        :return: response, json object"""
        headers = dict()
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'
        headers['Authorization'] = f'Bearer {self.get_token()}'
        endpoint = self.INCIDENTS_INFO_ENDPOINT
        ids_expression = json.dumps({'ids': ids}).encode("utf-8")
        return self.client.call_api(endpoint, 'POST', headers=headers, data=ids_expression, timeout=self.timeout)

    def get_token(self) -> str:
        """Request a new OAuth2 token.
        :return: [description]
        :rtype: str
        """
        if self.token_expired():
            resp = requests.request(
                'POST',
                self.TOKEN_ENDPOINT,
                headers={
                    'accept': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                data=(
                    f'client_id={self._client_id}'
                    f'&client_secret={self._client_secret}'
                )
            )
            self._token = resp.json()['access_token']
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
