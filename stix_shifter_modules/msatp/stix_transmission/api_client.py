"""Apiclient for MSATP"""
import json
from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync

DEFAULT_LIMIT = 10000
DEFAULT_OFFSET = 0


class APIClient:
    """API Client to handle all calls."""

    def __init__(self, connection, configuration):
        """Initialization.
        :param connection: dict, connection dict
        :param configuration: dict,config dict"""

        headers = dict()
        url_modifier_function = None
        auth = configuration.get('auth')
        self.endpoint = 'api/advancedqueries/run'
        self.host = connection.get('host')

        if auth:
            if 'access_token' in auth and auth['access_token']:
                headers['Authorization'] = "Bearer " + auth['access_token']

        self.client = RestApiClientAsync(connection.get('host'),
                                    connection.get('port', None),
                                    headers,
                                    url_modifier_function=url_modifier_function,
                                    cert_verify=connection.get('selfSignedCert', True),
                                    sni=connection.get('sni', None)
                                    )
        self.timeout = connection['options'].get('timeout')

    async def ping_box(self):
        """Ping the endpoint."""
        endpoint = '/api'
        return await self.client.call_api(endpoint, 'GET', timeout=self.timeout)

    async def run_search(self, query_expression, offset=DEFAULT_OFFSET, length=DEFAULT_LIMIT):
        """get the response from MSatp endpoints
        :param query_expression: str, search_id
        :param offset: int,offset value
        :param length: int,length value
        :return: response, json object"""
        serialize = '| serialize rn = row_number() | where rn >= {offset} | limit {length}'
        headers = dict()
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'
        endpoint = self.endpoint
        query_expression = query_expression + serialize.format(offset=offset, length=length)
        query_expression = json.dumps({'Query': query_expression}).encode("utf-8")
        return await self.client.call_api(endpoint, 'POST', headers=headers, data=query_expression, timeout=self.timeout)
