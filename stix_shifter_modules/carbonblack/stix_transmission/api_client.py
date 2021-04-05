from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient


class APIClient():
    PING_ENDPOINT = 'sensor'
    PROCESS_ENDPOINT = 'process'

    def __init__(self, connection, configuration):
        self.endpoint_start_v1 = 'api/v1/'  # Uses API v1 for `ping` and `processes search` endpoints.
        self.endpoint_start_v4 = 'api/v4/'  # Uses API v4 for `events search` endpoint.
        auth = configuration.get('auth')
        headers = dict()
        headers['X-Auth-Token'] = auth.get('token')
        self.client = RestApiClient(connection.get('host'),
                                    connection.get('port'),
                                    headers,
                                    cert_verify=connection.get('selfSignedCert', True),
                                    sni=connection.get('sni', None)
                                    )
        self.timeout = connection['options'].get('timeout')

    def ping_box(self):
        endpoint = self.endpoint_start_v1 + self.PING_ENDPOINT
        return self.client.call_api(endpoint, 'GET', timeout=self.timeout)

    def run_processes_search(self, query_expression, start=0, rows=10):
        """
            https://developer.carbonblack.com/reference/enterprise-response/6.3/rest-api/#process-search
            Processes search using `/api/v1/process`
        """
        headers = dict()
        process_endpoint = self.endpoint_start_v1 + self.PROCESS_ENDPOINT
        data = [("q", query_expression), ("start", start), ("rows", rows), ("sort", 'start asc')]
        return self.client.call_api(process_endpoint, 'GET', headers, urldata=data, timeout=self.timeout)

    def run_events_search(self, process_id, segment_id):
        """
            https://developer.carbonblack.com/reference/enterprise-response/6.3/rest-api/#process-event-details
            Event details search for process X at segment Y using `/api/v4/process/(process_id)/(segment_id)/event`
        """
        headers = dict()
        event_endpoint = self.endpoint_start_v4 + self.PROCESS_ENDPOINT + '/{}/{}/event'.format(process_id, segment_id)
        data = []
        return self.client.call_api(event_endpoint, 'GET', headers, urldata=data, timeout=self.timeout)
