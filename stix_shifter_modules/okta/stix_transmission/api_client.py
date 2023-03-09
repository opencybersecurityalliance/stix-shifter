from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient


class APIClient:
    QUERY_ENDPOINT = "api/v1/logs?"
    PING_ENDPOINT = "api/v1/org"

    def __init__(self, connection, configuration):
        auth = configuration.get('auth')
        self.headers = {'Authorization': auth['api_token'],
                        'Content-Type': 'application/json', 'Accept': 'application/json'}

        self.client = RestApiClient(connection.get('host'), port=None, headers=self.headers)
        self.timeout = connection['options'].get('timeout')
        self.result_limit = connection['options'].get('result_limit')

    def ping_data_source(self):
        """
        Ping the Data Source
        :return: Response object
        """
        return self.client.call_api(self.PING_ENDPOINT, 'GET', headers=self.headers, data={})

    def get_search_results(self, query, after_number):
        """
        Get results from Data Source
        :param query: Data Source Query
        :param after_number: next page token number
        :return: Response Object
        """
        query = self.QUERY_ENDPOINT + query
        if after_number != '0':
            query = query + '&' + after_number

        return self.client.call_api(query, 'GET', headers=self.headers, data={})
