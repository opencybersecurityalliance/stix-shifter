import base64
from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient


class ThreatGraphAPIClient:
    INDICATOR_SEARCH_ENDPOINT = '/ran-on/v1'

    # VERTEX_SUMMARY_ENDPOINT = 'clientqueryresults/'

    def __init__(self, connection, configuration):
        self.endpoint_start = 'threatgraph/combined/'
        auth = configuration.get('auth')
        self.headers = dict()
        self.headers['Authorization'] = b"Basic " + base64.b64encode(
            (auth['username'] + ':' + auth['password']).encode('ascii'))
        self.connection = connection
        self.configuration = configuration
        self.timeout = connection['options'].get('timeout')

    def get_indicator_search_results(self, value, type, limit, offset, length):
        headers = dict()
        headers['Accept'] = 'application/json'
        endpoint = self.endpoint_start + self.INDICATOR_SEARCH_ENDPOINT
        params = dict()
        # check if value=sha256/md5/hostname/ipadder
        params['value'] = value
        params['type'] = type
        params['limit'] = limit
        return self.get_api_client().call_api(endpoint, 'GET', headers, urldata=params, timeout=self.timeout)

    def get_vertex_summary_results(self, path, offset, length):
        headers = dict()
        headers['Accept'] = 'application/json'
        return self.get_api_client().call_api(path, 'GET', headers, timeout=self.timeout)


