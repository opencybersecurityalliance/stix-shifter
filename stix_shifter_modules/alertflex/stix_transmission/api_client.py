import base64
from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient


class APIClient():
    PING_TIMEOUT_IN_SECONDS = 10

    def __init__(self, connection, configuration):
        # Uncomment when implementing data source API client.
        # auth = configuration.get('auth')
        # headers = dict()
        # headers['X-Auth-Token'] = auth.get('token')
        # self.client = RestApiClient(connection.get('host'),
        #                             connection.get('port'),
        #                             connection.get('cert', None),
        #                             headers,
        #                             cert_verify=connection.get('cert_verify', 'True')
        #

        self.endpoint_start = 'alertflex-ctrl/rest/stix'
        headers = dict()
        url_modifier_function = None
        auth = configuration.get('auth')
        headers['Authorization'] = b"Basic " + base64.b64encode(
            (auth['username'] + ':' + auth['password']).encode('ascii'))
        self.client = RestApiClient(connection.get('host'),
                                    connection.get('port'),
                                    connection.get('cert', None),
                                    headers,
                                    cert_verify=False)

        # Placeholder client to allow dummy transmission calls.
        # Remove when implementing data source API client.                            )
        # self.client = "data source API client"


    def ping_box(self):
        endpoint = self.endpoint_start + '/status'
        return self.client.call_api(endpoint, 'GET', timeout=self.PING_TIMEOUT_IN_SECONDS)


    def run_search(self, query_expression, offset=None, length=None):
       # headers = dict()
       # return self.client.call_api(endpoint, 'GET', headers, urldata=data)

       # Return the search results. Results must be in JSON format before being translated into STIX
       return {"code": 200, "search_id": query_expression, "results": "Results from search"}
