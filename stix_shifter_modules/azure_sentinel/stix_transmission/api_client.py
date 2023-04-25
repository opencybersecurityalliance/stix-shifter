from azure.identity.aio import ClientSecretCredential
from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync


class APIClient:
    """API Client to handle all calls."""
    credential = None
    DEFAULT_API_VERSION = 'v1.0'
    LEGACY_ALERT = 'security/alerts'
    ALERT_V2 = 'security/alerts_v2'
    
    def __init__(self, base_uri, connection, configuration):
        """Initialization.
        :param connection: dict, connection dict
        :param configuration: dict,config dict"""
        self.host = base_uri
        self.legacy_alert = connection['options'].get('alert')
        self.alert_v2 = connection['options'].get('alertV2')

        if self.legacy_alert:
            self.query_alert_type = 'alert'
            self.endpoint = '{api_version}/{api_resource}'.format(api_version=self.DEFAULT_API_VERSION, api_resource=self.LEGACY_ALERT)
        elif self.alert_v2:
            self.query_alert_type = 'alertV2'
            self.endpoint = '{api_version}/{api_resource}'.format(api_version=self.DEFAULT_API_VERSION, api_resource=self.ALERT_V2)
        else:
            raise Exception('Invalid alert resource type. At least one alert type must be selected.')
        
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
                                    cert_verify=self.connection.get('selfSignedCert', True),
                                    sni=self.connection.get('sni', None)
                                    )
        return self.client

    async def ping_box(self):
        """Ping the endpoint."""
        params = dict()
        params['$top'] = 1
        await self.init_async_client()
        return await self.client.call_api(self.endpoint, 'GET', urldata=params, timeout=self.timeout)

    async def run_search(self, query_expression, length):
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
        return await self.client.call_api(self.endpoint, 'GET', headers, urldata=params, timeout=self.timeout)

    async def next_page_run_search(self, next_page_url):
        """get the response from azure_sentinel endpoints
        :param next_page_url: str, search_id
        :return: response, json object"""
        headers = dict()
        headers['Accept'] = 'application/json'
        url = next_page_url.split('?', maxsplit=1)[1]
        endpoint = self.endpoint + '?' + url
        await self.init_async_client()
        return await self.client.call_api(endpoint, 'GET', headers, timeout=self.timeout)
