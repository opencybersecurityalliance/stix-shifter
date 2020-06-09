import base64
from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient


class APIClient():
    PING_TIMEOUT_IN_SECONDS = 10

    def __init__(self, connection, configuration):
        self.endpoint_start = 'alertflex-ctrl/rest/stix-alerts'
        headers = dict()
        auth = configuration.get('auth')
        headers['Authorization'] = b"Basic " + base64.b64encode(
            (auth['username'] + ':' + auth['password']).encode('ascii'))
        self.client = RestApiClient(connection.get('host'),
                                    connection.get('port'),
                                    connection.get('cert', None),
                                    headers,
                                    cert_verify=False)

    def ping_box(self):
        endpoint = self.endpoint_start + '/status'
        return self.client.call_api(endpoint, 'GET', timeout=self.PING_TIMEOUT_IN_SECONDS)

    def run_search(self, query_expression):
        endpoint = self.endpoint_start + '/search'
        data = {'query': query_expression}
        result = self.client.call_api(endpoint, 'GET', urldata=data)
        return result

