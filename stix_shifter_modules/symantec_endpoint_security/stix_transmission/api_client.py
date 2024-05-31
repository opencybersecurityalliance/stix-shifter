import json
from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync


class APIClient:
    QUERY_ENDPOINT = "v1/event-search"
    TOKEN_ENDPOINT = "v1/oauth2/tokens"

    def __init__(self, connection, configuration):
        self.auth = configuration.get('auth')
        self.headers = {"Content-Type": "application/json"}
        self.client = RestApiClientAsync(connection.get('host'), headers=self.headers,
                                         cert_verify=connection.get('selfSignedCert'))
        self.result_limit = connection['options'].get('result_limit')
        self.timeout = connection['options'].get('timeout')
        self.api_page_size = connection['options'].get('api_page_size')

    async def get_search_results(self, query, token):
        """
        Get results from Data Source
        :param query: Data Source Query
        :param token: Authentication token
        :return: Response Object
        """
        self.headers['Authorization'] = "Bearer " + token
        return await self.client.call_api(self.QUERY_ENDPOINT, 'POST', headers=self.headers, data=json.dumps(query),
                                          timeout=self.timeout)

    async def generate_token(self):
        """Get Authorization token"""
        self.headers['Authorization'] = 'Basic ' + self.auth['oauth_credentials']
        resp = await self.client.call_api(self.TOKEN_ENDPOINT, 'POST', headers=self.headers, timeout=self.timeout)
        return resp
