"""Apiclient for MSATP"""
import json
from azure.identity.aio import ClientSecretCredential
from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync

DEFAULT_LIMIT = 10000
DEFAULT_OFFSET = 0


class APIClient:
    """API Client to handle all calls."""

    def __init__(self, connection, configuration):
        """Initialization.
        :param connection: dict, connection dict
        :param configuration: dict,config dict"""

        self.endpoint = 'api/advancedqueries/run'
        self.host = connection.get('host')
        self.auth = configuration.get('auth')
        self.timeout = connection['options'].get('timeout')
        self.connection = connection

    async def init_async_client(self):
        url_modifier_function = None
        headers = dict()

        self.credential = ClientSecretCredential(tenant_id=self.auth["tenant"],
                                                 client_id=self.auth["clientId"],
                                                 client_secret=self.auth["clientSecret"])
        async with self.credential:
            self.access_token = await self.credential.get_token("https://{host}/.default".format(host=self.host))
            headers['Authorization'] = "Bearer " + self.access_token.token

        self.client = RestApiClientAsync(self.host,
                                         self.connection.get('port', None),
                                         headers,
                                         url_modifier_function=url_modifier_function,
                                         cert_verify=self.connection.get(
                                             'selfSignedCert', True)
                                         )
        return self.client

    async def ping_box(self):
        """Ping the endpoint."""
        endpoint = '/api'
        await self.init_async_client()
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
        await self.init_async_client()
        return await self.client.call_api(endpoint, 'POST', headers=headers, data=query_expression, timeout=self.timeout)
