import requests
from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync


class APIClient:
    PING_ENDPOINT = 'v1/ping'
    ALERTS_ENDPOINT = 'v1/alerts'

    def __init__(self, connection, configuration):
        self.auth = configuration.get('auth')
        self.limit = connection['options'].get("result_limit")
        headers = {}
        if 'token' in self.auth:
            headers['Authorization'] = "Bearer " + self.auth.get('token')
        url_modifier_function = None
        # Added self-signed certificate parameter for verification
        self.client = RestApiClientAsync(connection.get('host'),
                                    connection.get('port', None),
                                    headers,
                                    url_modifier_function=url_modifier_function,
                                    sni=connection.get('sni', None),
                                    cert_verify=connection.get('selfSignedCert', True)
                                    )
        self.timeout = connection['options'].get('timeout')

    async def ping_data_source(self):
        """
              Ping the Data Source
              :return: Response object
        """
        return await self.client.call_api(self.PING_ENDPOINT, 'GET')

    async def get_search_results(self, query):
        """
           Get results from Data Source
           :param query: Data Source Query
           :return: Response Object
        """
        query = requests.utils.quote(query)
        endpoint = self.ALERTS_ENDPOINT + "?query=" + query
        return await self.client.call_api(endpoint, 'GET', headers=self.client.headers,
                                    timeout=self.timeout)

    async def get_inner_results(self, alertid):
        """
           Get result of specific alert id (second level api call)
           :param alertid: alertId
           :return: Response Object
        """
        endpoint = ""
        if alertid != '':
            endpoint = self.ALERTS_ENDPOINT + "/" + alertid
        return await self.client.call_api(endpoint, 'GET', headers=self.client.headers,
                                    timeout=self.timeout)

    def get_limit(self):
        """
           get the configured result limit
        """
        return self.limit
