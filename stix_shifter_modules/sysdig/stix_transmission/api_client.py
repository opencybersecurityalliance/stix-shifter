from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync


class APIClient:
    PING_ENDPOINT = 'api/v1/secureEvents/status'
    EVENTS_ENDPOINT = 'api/v1/secureEvents?'

    def __init__(self, connection, configuration):
        self.auth = configuration.get('auth')
        self.result_limit = connection['options'].get("result_limit")
        headers = {}
        if 'token' in self.auth:
            headers['Authorization'] = "Bearer " + self.auth.get('token')
        headers["Accept"] = "application/json"
        headers["Content-Type"] = "application/json;charset=UTF-8"
        # Added self-signed certificate parameter for verification
        self.client = RestApiClientAsync(connection.get('host'),
                                         connection.get('port', None),
                                         headers,
                                         url_modifier_function=None,
                                         cert_verify=connection.get('selfSignedCert', True))
        self.timeout = connection['options'].get('timeout')

    async def ping_data_source(self):
        """
        ping the Data Source
        :return: Response object
        """
        return await self.client.call_api(self.PING_ENDPOINT, 'GET', headers=self.client.headers, timeout=self.timeout)

    async def get_search_results(self, query):
        """
        :param query: Data Source Query
        :return: Response Object
        """
        return await self.client.call_api(self.EVENTS_ENDPOINT, 'GET', urldata=query,
                                          headers=self.client.headers, timeout=self.timeout)
