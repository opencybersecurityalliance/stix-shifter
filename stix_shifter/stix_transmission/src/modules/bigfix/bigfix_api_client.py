from .RestApiClient import RestApiClient


class APIClient(RestApiClient):

    PING_ENDPOINT = 'help/clientquery'
    QUERY_ENDPOINT = 'clientquery'
    RESULT_ENDPOINT = 'clientqueryresults/'
    SYNC_QUERY_ENDPOINT = 'query'

    def __init__(self, server_ip, user_name, password, cert):

        super(APIClient, self).__init__(server_ip, user_name, password, cert)

    def ping_box(self):
        endpoint = self.PING_ENDPOINT
        return self.call_api(endpoint, 'GET', self.headers)

    def create_search(self, query_expression):
        headers = self.headers.copy()
        self.headers['Content-type'] = 'application/xml'
        endpoint = self.QUERY_ENDPOINT
        data = query_expression
        data = data.encode('utf-8')
        return self.call_api(endpoint, 'POST', self.headers, data=data)

    def get_search_results(self, search_id, offset, length):
        headers = self.headers.copy()
        headers['Accept'] = 'application/json'
        endpoint = self.RESULT_ENDPOINT + search_id

        params = dict()
        params['output'] = 'json'
        params['stats'] = '1'
        params['start'] = offset
        params['count'] = length

        return self.call_api(endpoint, 'GET', headers, params=params)

    def get_sync_query_results(self, relevance):
        headers = self.headers.copy()
        endpoint = self.SYNC_QUERY_ENDPOINT
        params = dict()
        params['relevance'] = relevance
        return self.call_api(endpoint, 'GET', headers, params=params)
