import base64
from ..utils.RestApiClient import RestApiClient


class APIClient():

    PING_ENDPOINT = 'help/clientquery'
    QUERY_ENDPOINT = 'clientquery'
    RESULT_ENDPOINT = 'clientqueryresults/'
    SYNC_QUERY_ENDPOINT = 'query'

    def __init__(self, connection, configuration):
        self.endpoint_start = 'api/'
        auth = configuration.get('auth')
        headers = dict()
        headers['Authorization'] = b"Basic " + base64.b64encode(
                (auth['username'] + ':' + auth['password']).encode('ascii'))
        self.client = RestApiClient(connection.get('host'),
                                    connection.get('port'),
                                    connection.get('cert', None),
                                    headers,
                                    cert_verify=connection.get('cert_verify', 'True')
                                    )

    def ping_box(self):
        endpoint = self.endpoint_start + self.PING_ENDPOINT
        return self.client.call_api(endpoint, 'GET')

    def create_search(self, query_expression):
        headers = dict()
        headers['Content-type'] = 'application/xml'
        endpoint = self.endpoint_start + self.QUERY_ENDPOINT
        data = query_expression
        data = data.encode('utf-8')
        return self.client.call_api(endpoint, 'POST', headers, data=data)

    def get_search_results(self, search_id, offset, length):
        headers = dict()
        headers['Accept'] = 'application/json'
        endpoint = self.endpoint_start + self.RESULT_ENDPOINT + search_id
        params = dict()
        params['output'] = 'json'
        params['stats'] = '1'
        params['start'] = offset
        params['count'] = length
        return self.client.call_api(endpoint, 'GET', headers, urldata=params)

    def get_sync_query_results(self, relevance):
        headers = dict()
        endpoint = self.endpoint_start + self.SYNC_QUERY_ENDPOINT
        params = dict()
        params['relevance'] = relevance
        return self.client.call_api(endpoint, 'GET', headers, urldata=params)
