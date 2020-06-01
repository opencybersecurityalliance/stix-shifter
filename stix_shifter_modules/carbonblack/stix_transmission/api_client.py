from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient


class APIClient():
    PING_ENDPOINT = 'sensor'
    PING_TIMEOUT_IN_SECONDS = 10
    DEFAULT_SEARCH_TIMEOUT_IN_SECONDS = 30

    @staticmethod
    def _dialect_to_endpoint(dialect):
        assert dialect in ["binary", "process"]
        return dialect

    def __init__(self, connection, configuration):
        self.endpoint_start = 'api/v1/'
        auth = configuration.get('auth')
        headers = dict()
        headers['X-Auth-Token'] = auth.get('token')
        self.client = RestApiClient(connection.get('host'),
                                    connection.get('port'),
                                    connection.get('cert', None),
                                    headers,
                                    cert_verify=connection.get('selfSignedCert', True),
                                    mutual_auth=connection.get('use_securegateway', False),
                                    sni=connection.get('sni', None)
                                    )
        options = connection.get('options')
        if options:
            self.search_timeout = options.get('timeout')
        else:
            self.search_timeout = self.DEFAULT_SEARCH_TIMEOUT_IN_SECONDS

    def ping_box(self):
        endpoint = self.endpoint_start + self.PING_ENDPOINT
        return self.client.call_api(endpoint, 'GET', timeout=self.PING_TIMEOUT_IN_SECONDS)

    def run_search(self, query_expression, dialect, start=0, rows=10):
        headers = dict()
        endpoint = self.endpoint_start + self._dialect_to_endpoint(dialect)
        data = [("q", query_expression), ("start", start), ("rows", rows)]

        # The purpose of this is to maintain order stability when doing paging
        if dialect == 'binary':
            sort_by = 'server_added_timestamp asc'
        else:  # process
            sort_by = 'start asc'
        data.append(("sort", sort_by))

        return self.client.call_api(endpoint, 'GET', headers, urldata=data, timeout=self.search_timeout)
