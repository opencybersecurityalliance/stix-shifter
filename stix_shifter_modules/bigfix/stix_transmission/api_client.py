import base64
from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient


class APIClient:

    PING_ENDPOINT = 'help/clientquery'
    QUERY_ENDPOINT = 'clientquery'
    RESULT_ENDPOINT = 'clientqueryresults/'
    SYNC_QUERY_ENDPOINT = 'query'
    PING_TIMEOUT_IN_SECONDS = 10

    def __init__(self, connection, configuration):
        self.endpoint_start = 'api/'
        auth = configuration.get('auth')
        self.headers = dict()
        self.headers['Authorization'] = b"Basic " + base64.b64encode(
                (auth['username'] + ':' + auth['password']).encode('ascii'))
        self.connection = connection
        self.configuration = configuration
        self.search_timeout = connection['options'].get('timeout')

    def ping_box(self):
        endpoint = self.endpoint_start + self.PING_ENDPOINT
        return self.get_api_client().call_api(endpoint, 'GET', timeout=self.PING_TIMEOUT_IN_SECONDS)

    def create_search(self, query_expression):
        headers = dict()
        headers['Content-type'] = 'application/xml'
        endpoint = self.endpoint_start + self.QUERY_ENDPOINT
        data = query_expression
        data = data.encode('utf-8')
        return self.get_api_client().call_api(endpoint, 'POST', headers, data=data, timeout=self.search_timeout)

    def get_search_results(self, search_id, offset, length):
        headers = dict()
        headers['Accept'] = 'application/json'
        endpoint = self.endpoint_start + self.RESULT_ENDPOINT + search_id
        params = dict()
        params['output'] = 'json'
        params['stats'] = '1'
        params['start'] = offset
        params['count'] = length
        return self.get_api_client().call_api(endpoint, 'GET', headers, urldata=params, timeout=self.search_timeout)

    def get_sync_query_results(self, relevance):
        headers = dict()
        endpoint = self.endpoint_start + self.SYNC_QUERY_ENDPOINT
        params = dict()
        params['relevance'] = relevance
        return self.get_api_client().call_api(endpoint, 'GET', headers, urldata=params, timeout=self.search_timeout)

    def get_api_client(self):
        api_client = RestApiClient(self.connection.get('host'),
                                   self.connection.get('port'),
                                   self.headers, cert_verify=self.connection.get('selfSignedCert', True),
                                   sni=self.connection.get('sni', None)
                                   )
        return api_client
