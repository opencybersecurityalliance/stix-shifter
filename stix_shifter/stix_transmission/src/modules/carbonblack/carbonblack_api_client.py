from ..utils.RestApiClient import RestApiClient


class APIClient():

    PING_ENDPOINT = 'sensor'
    QUERY_ENDPOINT = 'process'

    def __init__(self, connection, configuration):
        self.endpoint_start = 'api/v1/'
        auth = configuration.get('auth')
        headers = dict()
        headers['X-Auth-Token'] = auth.get('token')
        self.client = RestApiClient(connection.get('host'),
                                    connection.get('port'),
                                    connection.get('cert', None),
                                    headers,
                                    cert_verify=connection.get('cert_verify', 'True')
                                    )

    def ping_box(self):
        endpoint = self.endpoint_start + self.PING_ENDPOINT
        return self.client.call_api(endpoint, 'GET')

    def run_search(self, query_expression):
        headers = dict()
        endpoint = self.endpoint_start + self.QUERY_ENDPOINT
        data = { "q": query_expression }
        return self.client.call_api(endpoint, 'GET', headers, urldata=data)
