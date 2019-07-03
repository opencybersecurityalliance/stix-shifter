from ..utils.RestApiClient import RestApiClient


class APIClient():

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

        # Placeholder client to allow dummy transmission calls.
        # Remove when implementing data source API client.                            )
        self.client = "data source API client"

    def ping_box(self):
        # Pings the data source
        return {"code": 200, "results": "Was able to hit the data source"}

    def run_search(self, query_expression, offset=None, length=None):
        # headers = dict()
        # return self.client.call_api(endpoint, 'GET', headers, urldata=data)

        # Return the search results. Results must be in JSON format before being translated into STIX
        return {"code": 200, "search_id": query_expression, "results": "Results from search"}
