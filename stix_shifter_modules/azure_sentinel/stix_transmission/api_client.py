from azure.identity.aio import ClientSecretCredential
from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync


class APIClient:
    """API Client to handle all calls."""
    credential = None
    
    def __init__(self, connection, configuration):
        """Initialization.
        :param connection: dict, connection dict
        :param configuration: dict,config dict"""
        self.host = connection['host']
        self.connection = connection
        self.configuration = configuration
        self.timeout = connection['options'].get('timeout')
    
    async def init_async_client(self):
        headers = dict()

        if 'access_token' in self.configuration.get("auth"):
            self.access_token = self.configuration["auth"]['access_token']
            headers['Authorization'] = "Bearer " + self.access_token
        else:
            self.credential = ClientSecretCredential(tenant_id=self.configuration["auth"]["tenant"],
                                                    client_id=self.configuration["auth"]["clientId"],
                                                    client_secret=self.configuration["auth"]["clientSecret"])
            async with self.credential:
                self.access_token = await self.credential.get_token("https://{host}/.default".format(host=self.host))
                headers['Authorization'] = "Bearer " + self.access_token.token

        self.client = RestApiClientAsync(self.host,
                                    self.connection.get('port', None),
                                    headers,
                                    cert_verify=self.connection.get('selfSignedCert', True)
                                    )
        return self.client

    async def ping_box(self, endpoint):
        """Ping the endpoint."""
        params = dict()
        params['$top'] = 1
        await self.init_async_client()
        return await self.client.call_api(endpoint, 'GET', urldata=params, timeout=self.timeout)

    async def run_search(self, query_expression, length, endpoint):
        """get the response from azure_sentinel endpoints
        :param query_expression: str, search_id
        :param length: int,length value
        :return: response, json object"""
        headers = dict()
        headers['Accept'] = 'application/json'
        params = dict()
        params['$filter'] = query_expression
        params['$top'] = length
        await self.init_async_client()
        return await self.client.call_api(endpoint, 'GET', headers, urldata=params, timeout=self.timeout)

    async def next_page_run_search(self, next_page_url, endpoint):
        """get the response from azure_sentinel endpoints
        :param next_page_url: str, search_id
        :return: response, json object"""
        headers = dict()
        headers['Accept'] = 'application/json'
        url = next_page_url.split('?', maxsplit=1)[1]
        endpoint = endpoint + '?' + url
        await self.init_async_client()
        return await self.client.call_api(endpoint, 'GET', headers, timeout=self.timeout)
