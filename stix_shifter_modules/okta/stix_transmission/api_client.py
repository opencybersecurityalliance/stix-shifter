from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient


class APIClient:
    QUERY_ENDPOINT = "api/v1/logs?"

    def __init__(self, connection, configuration):
        auth = configuration.get('auth')
        self.headers = {'Authorization': auth['api_token'],
                        'Content-Type': 'application/json', 'Accept': 'application/json'}

        self.client = RestApiClient(connection.get('host'),
                                    None,
                                    self.headers)
        self.timeout = connection['options'].get('timeout')
        self.result_limit = connection['options'].get('result_limit')

    def ping_data_source(self):
        """
        Ping the Data Source
        :return: Response object
        """
        query = 'filter = actor.type eq "User"&limit=10'
        query = self.QUERY_ENDPOINT + query
        return self.client.call_api(query, 'GET', headers=self.headers, data={})

    def get_search_results(self, query):
        """
        Get results from Data Source
        :param query: Data Source Query
        :return: Response Object
        """
        query = self.QUERY_ENDPOINT + query
        return self.client.call_api(query, 'GET', headers=self.headers, data={})
