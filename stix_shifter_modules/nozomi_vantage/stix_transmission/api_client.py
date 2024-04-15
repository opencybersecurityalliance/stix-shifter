import json
from urllib import parse
from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync


class APIClient:
    QUERY_ENDPOINT = "api/open/query/do?"
    PING_ENDPOINT = "api/v1/health_logs"
    TOKEN_ENDPOINT = "api/v1/keys/sign_in"

    def __init__(self, connection, configuration):
        self.auth = configuration.get('auth')
        self.headers = {'Content-Type': 'application/json'}
        self.client = RestApiClientAsync(connection.get('host'), connection.get('port'), headers=self.headers,
                                         cert_verify=connection.get('selfSignedCert'))
        self.result_limit = connection['options'].get('result_limit')
        self.max_page_size = connection['options'].get('api_page_size')
        self.timeout = connection['options'].get('timeout')

    async def ping_data_source(self, token):
        """
        Ping the Data Source
        :param token: Authentication token
        :return: Response object
        """
        self.headers['Authorization'] = token
        return await self.client.call_api(self.PING_ENDPOINT, 'GET', headers=self.headers, data={},
                                          timeout=self.timeout)

    async def get_search_results(self, query, token):
        """
        Get results from Data Source
        :param query: Data Source Query
        :param token: Authentication token
        :return: Response Object
        """
        self.headers['Authorization'] = token
        query = self.QUERY_ENDPOINT + parse.quote(query, safe='&,=')
        return await self.client.call_api(query, 'GET', headers=self.headers, data={}, timeout=self.timeout)

    async def generate_token(self):
        """Get Authorization token"""

        if 'Authorization' in self.headers:
            self.headers.pop('Authorization')

        return await self.client.call_api(self.TOKEN_ENDPOINT, 'POST', headers=self.headers, data=json.dumps(self.auth),
                                          timeout=self.timeout)
