from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync
from stix_shifter_utils.utils import logger


class APIClient:
    QUERY_ENDPOINT = "/api/v2.4/search/detections"
    PING_ENDPOINT = "/api/v2.4/health/connectivity"

    def __init__(self, connection, configuration):
        self.logger = logger.set_logger(__name__)
        self.auth = configuration.get('auth')
        self.result_limit = connection['options'].get('result_limit')
        self.headers = {"Authorization": "Token " + self.auth["api_token"],
                        'Content-Type': "application/json",
                        'Cache-Control': "no-cache"}
        self.client = RestApiClientAsync(connection.get('host'), port=connection.get('port'), headers=self.headers)
        self.host = connection.get('host')

    async def ping_data_source(self):
        """
        Ping the Data Source
        :return: Response object
        """
        return await self.client.call_api(self.PING_ENDPOINT, 'GET', headers=self.headers, data=None)

    async def get_search_results(self, query):
        """
        Get results from Data Source
        :param query: Data Source Query
        :return: Response Object
        """
        self.logger.debug("query: %s", query)
        if self.QUERY_ENDPOINT not in query:
            url = self.QUERY_ENDPOINT + '/?' + query
        else:
            url = query.replace('https://' + self.host, '')   # removing host address for next page url
        return await self.client.call_api(url, 'GET', headers=self.headers, data=None)
