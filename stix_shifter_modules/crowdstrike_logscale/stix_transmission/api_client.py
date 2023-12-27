from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync

PING_ENDPOINT = 'api/v1/status'
QUERY_ENDPOINT = 'api/v1/repositories'


class APIClient:

    def __init__(self, connection, configuration):
        auth = configuration.get('auth')
        self.headers = {"Authorization": f"Bearer {auth.get('api_token')}", "Content-Type": "application/json",
                        "Accept": "application/json"}
        self.client = RestApiClientAsync(connection.get('host'), headers=self.headers)
        self.timeout = connection['options'].get('timeout')
        self.result_limit = connection['options'].get('result_limit')
        self.api_endpoint = f"{QUERY_ENDPOINT}/{auth.get('repository')}/query"

    async def ping_data_source(self):
        """
        Ping the Data Source
        :return: Response Object
        """
        return await self.client.call_api(PING_ENDPOINT, 'GET', headers=self.headers, data={})

    async def get_search_results(self, query):
        """
        Get results from Data Source
        :param query: Data Source Query
        :return: Response Object
        """
        return await self.client.call_api(self.api_endpoint, 'POST', headers=self.headers, data=query,
                                          timeout=self.timeout)
