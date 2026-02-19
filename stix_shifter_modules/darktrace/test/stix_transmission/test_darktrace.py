from unittest.mock import patch
import unittest
import json
from stix_shifter_modules.darktrace.stix_transmission.api_client import APIClient
from stix_shifter.stix_transmission import stix_transmission
from stix_shifter.stix_transmission.stix_transmission import run_in_thread
from tests.utils.async_utils import get_mock_response


class TestDarktraceConnection(unittest.TestCase, object):
    """ class for test Darktrace connection"""

    _configuration = {'auth': {'private_token': '', 'public_token': ''}}
    _connection = {'host': 'www.test.com', 'options': {'timeout': 30}}

    @staticmethod
    def config():
        """format for configuration"""
        return {
            "auth": {
                "private_token": "bla",
                "public_token": "bla"
            }}

    @staticmethod
    def connection():
        """format for connection"""
        return {
            "host": "hostbla"
        }

    @patch('stix_shifter_modules.darktrace.stix_transmission.api_client.APIClient.ping_box')
    def test_ping_endpoint(self, mock_ping_source):
        """ test to check ping_data_source function"""

        pingmock = """{"status":"SUCCESS"}"""
        pingresponse = get_mock_response(200, pingmock, 'byte', response=pingmock)
        mock_ping_source.return_value = pingresponse

        transmission = stix_transmission.StixTransmission('darktrace', self.connection(), self.config())

        ping_response = transmission.ping()

        assert ping_response is not None
        assert ping_response['success'] is True

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_ping_box(self, mock_ping_source):
        """ test to check ping_data_source function"""

        pingmock = """{"status":"SUCCESS"}"""
        pingresponse = get_mock_response(200, pingmock, response=pingmock)
        mock_ping_source.return_value = pingresponse

        apiclient = APIClient(self._connection, self._configuration)
        ping_response = run_in_thread(apiclient.ping_box)

        assert ping_response is not None
        assert ping_response.code== 200

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_get_search_results(self, mock_ping_source):
        """ test to check ping_data_source function"""

        pingmock = """{"status":"SUCCESS"}"""
        pingresponse = get_mock_response(200, pingmock, response=pingmock)
        mock_ping_source.return_value = pingresponse

        apiclient = APIClient(self._connection, self._configuration)
        ping_response = run_in_thread(apiclient.get_search_results, 'query')

        assert ping_response is not None
        assert ping_response.code == 200

    def test_http_query(self):
        """ test to check query of process element """
        query = json.dumps({
            "queries": [
                "{\"search\": \"((@fields.method:GET) AND (@fields.epochdate:>1647409125.029 AND "
                "@fields.epochdate:<1647409425.029))\", \"fields\": [], \"timeframe\": \"custom\", "
                "\"time\": {\"from\": \"2022-03-16T05:38:45.029000Z\", "
                "\"to\": \"2022-03-16T05:43:45.029000Z\"}}"
            ]
        })

        transmission = stix_transmission. \
            StixTransmission('darktrace', self.connection(), self.config())
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert query_response['search_id'] is not None
        assert query_response['search_id'] == query

    @patch('stix_shifter_modules.darktrace.stix_transmission.api_client.APIClient.get_search_results')
    def test_http_results(self, mock_results_response):
        mock_response_dict = json.dumps({
            'took': 2, 'timed_out': False, '_shards': {'total': 2, 'successful': 2, 'skipped': 0, 'failed': 0},
            'hits': {
                'total': 4,
                'max_score': None,
                'hits': [{
                    '_index': 'logstash-vmprobe-2022.03.15',
                    '_type': 'doc',
                    '_id': 'AX-NRncogOn5vlEO2Z2B',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647342620.459522,
                            'source_port': 62283,
                            'host': 'www.darktrace.com',
                            'trans_depth': 1,
                            'uri': '/en/darktrace-antigena/',
                            'dest_port': 80,
                            'source_ip': '172.31.81.98',
                            'response_body_len': 0,
                            'redirect_location': 'https://www.darktrace.com/en/darktrace-antigena/',
                            'dest_ip': '104.20.203.23',
                            'client_header_names': ['HOST', 'CONNECTION', 'UPGRADE-INSECURE-REQUESTS', 'USER-AGENT',
                                                    'ACCEPT', 'ACCEPT-ENCODING', 'ACCEPT-LANGUAGE', 'COOKIE'],
                            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
                            'uid': 'CSVt7v2rT7aukksv3e01',
                            'version': '1.1',
                            'status_msg': 'Moved Permanently',
                            'method': 'GET',
                            'status_code': 301,
                            'request_body_len': 0
                        },
                        '@type': 'http',
                        '@timestamp': '2022-03-15T11:10:20',
                        '@message': '1647342620.4595\tCSVt7v2rT7aukksv3e01\t172.31.81.98'
                                    '\t62283\t104.20.203.23\t80\t-\t-\twww.darktrace.com\t1'
                                    '\t/en/darktrace-antigena/\t0\thttps://www.darktrace.com'
                                    '/en/darktrace-antigena/\t[HOST,CONNECTION,UPGRADE-INSECURE-'
                                    'REQUESTS,USER-AGENT,ACCEPT,ACCEPT-ENCODING,ACCEPT-LANGUAGE,'
                                    'COOKIE]\tMozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 '
                                    'Safari/537.36\t1.1\tMoved Permanently\tGET\t301\t0',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647342620000]
                }]
            }, 'darktraceChildError': '',
            'kibana': {
                'index': ['logstash-darktrace-2022.03.15'], 'per_page': 50,
                'time': {'from': '2022-03-15T10:18:00.003Z', 'to': '2022-03-15T11:18:00.003Z'},
                'default_fields': ['@type', '@message']}
        })
        mock_results_response.return_value = get_mock_response(200, mock_response_dict, 'byte')
        query = json.dumps({
            "queries": [
                "{\"search\": \"((@fields.method:GET) AND (@fields.epochdate:>1647409125.029 AND "
                "@fields.epochdate:<1647409425.029))\", \"fields\": [], \"timeframe\": \"custom\", "
                "\"time\": {\"from\": \"2022-03-16T05:38:45.029000Z\", "
                "\"to\": \"2022-03-16T05:43:45.029000Z\"}}"]})
        offset = 0
        length = 1
        transmission = stix_transmission.StixTransmission('darktrace', self.connection(), self.config())
        results_response = transmission.results(query, offset, length)
        assert results_response is not None
        assert results_response['success'] is True
        assert 'data' in results_response
        assert len(results_response['data']) > 0

    def test_x509_query(self):
        """ test to check query of process element """
        query = json.dumps({
            "queries": [
                "{\"search\": \"((@fields.certificate_serial:76FDB38B8D5AA88844250EFE0EA89026) AND "
                "(@fields.epochdate:>1647411908.389 AND @fields.epochdate:<1647412208.389))\", "
                "\"fields\": [], \"timeframe\": \"custom\", \"time\": "
                "{\"from\": \"2022-03-16T06:25:08.389000Z\", \"to\": \"2022-03-16T06:30:08.389000Z\"}}"
            ]
        })

        transmission = stix_transmission.StixTransmission('darktrace', self.connection(), self.config())
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert query_response['search_id'] is not None
        assert query_response['search_id'] == query

    def test_multievent_query(self):
        """ test to check query of process element """
        query = json.dumps({
            "queries": [
                "{\"search\": \"(((@fields.query:pop.gmail.com) OR "
                "(@fields.cipher:TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA))"
                " AND (@fields.epochdate:>1647422600.894 AND @fields.epochdate:<1647422900.894))\", "
                "\"fields\": [], \"timeframe\": \"custom\", \"time\": "
                "{\"from\": \"2022-03-16T09:23:20.894000Z\","
                " \"to\": \"2022-03-16T09:28:20.894000Z\"}}"
            ]})

        transmission = stix_transmission.StixTransmission('darktrace', self.connection(), self.config())
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert query_response['search_id'] is not None
        assert query_response['search_id'] == query

    @patch('stix_shifter_modules.darktrace.stix_transmission.api_client.APIClient.get_search_results')
    def test_invalid_auth(self, mock_results_response):
        mock_response_dict = json.dumps({"advancedsearch": "API SIGNATURE ERROR"})
        mock_results_response.return_value = get_mock_response(400, mock_response_dict, 'byte', response=mock_response_dict)

        query = json.dumps({"queries": ["{\"search\": \"(@fields.query:pop.gmail.com)\", \"fields\": [], \"timeframe\":"
                                        " \"custom\", \"time\": {\"from\": \"2022-03-16T09:23:20.894000Z\", "
                                        "\"to\": \"2022-03-16T09:28:20.894000Z\"}}"]})

        transmission = stix_transmission.StixTransmission('darktrace', self.connection(), self.config())
        results_response = transmission.results(query, 0, 1)

        assert results_response is not None
        assert results_response['success'] is False
        assert results_response['code'] == 'authentication_fail'

    @patch('stix_shifter_modules.darktrace.stix_transmission.api_client.APIClient.get_search_results')
    def test_invalid_args(self, mock_results_response):
        mock_response_dict = json.dumps({'error': 'Invalid to/from fields in custom range'})
        mock_results_response.return_value = get_mock_response(200, mock_response_dict, 'byte')

        query = json.dumps({"queries": ["{\"search\": \"(@fields.query:pop.gmail.com)\", \"fields\": [], \"timeframe\":"
                                        " \"custom\", \"time\": {\"frommm\": \"2022-03-16T09:23:20.894000Z\", "
                                        "\"to\": \"2022-03-16T09:28:20.894000Z\"}}"]})

        transmission = stix_transmission.StixTransmission('darktrace', self.connection(), self.config())
        results_response = transmission.results(query, 0, 1)
        assert results_response is not None
        assert results_response['code'] == 'invalid_parameter'

    @patch('stix_shifter_modules.darktrace.stix_transmission.api_client.APIClient.get_search_results')
    def test_connection_error(self, mock_results_response):
        mock_response_dict = json.dumps({'error': 'Invalid Host/Port'})
        mock_results_response.return_value = get_mock_response(500, mock_response_dict)
        query = {'queries': []}
        transmission = stix_transmission.StixTransmission('darktrace', self.connection(), self.config())
        results_response = transmission.results(query, 0, 1)
        assert results_response is not None
        assert results_response['success'] is False

    @patch('stix_shifter_modules.darktrace.stix_transmission.api_client.APIClient.ping_box')
    def test_ping_invalid_auth(self, mock_results_response):
        pingmock = json.dumps({'error': 'Invalid Authentication'})
        pingresponse = get_mock_response(400, pingmock, 'byte', response=pingmock)
        mock_results_response.return_value = pingresponse

        transmission = stix_transmission.StixTransmission('darktrace', self.connection(), self.config())
        results_response = transmission.ping()

        assert results_response is not None
        assert results_response['success'] is False
        assert results_response['code'] == 'authentication_fail'

    @patch('stix_shifter_modules.darktrace.stix_transmission.api_client.APIClient.ping_box')
    def test_ping_invalid_args(self, mock_results_response):
        pingmock = json.dumps({'error': 'Invalid to/from fields in custom range'})
        pingresponse = get_mock_response(200, pingmock, 'byte', response=pingmock)
        mock_results_response.return_value = pingresponse

        transmission = stix_transmission.StixTransmission('darktrace', self.connection(), self.config())
        results_response = transmission.ping()

        assert results_response is not None
        assert results_response['success'] is False
        assert 'Invalid to/from fields in custom range' in results_response['error']

    @patch('stix_shifter_modules.darktrace.stix_transmission.api_client.APIClient.ping_box')
    def test_ping_connection_error(self, mock_results_response):
        mock_results_response.return_value = get_mock_response(500, '')
        transmission = stix_transmission.StixTransmission('darktrace', self.connection(), self.config())
        results_response = transmission.ping()

        assert results_response is not None
        assert results_response['success'] is False

    @patch('stix_shifter_modules.darktrace.stix_transmission.api_client.APIClient.get_search_results')
    def test_timeout_error(self, mock_results_response):
        mock_results_response.side_effect = TimeoutError("Request Timeout")

        query = json.dumps({"queries": ["{\"search\": \"(@fields.query:pop.gmail.com)\", \"fields\": [], \"timeframe\":"
                                        " \"custom\", \"time\": {\"from\": \"2022-03-16T09:23:20.894000Z\", "
                                        "\"to\": \"2022-03-16T09:28:20.894000Z\"}}"]})

        transmission = stix_transmission.StixTransmission('darktrace', self.connection(), self.config())
        results_response = transmission.results(query, 0, 1)

        assert results_response is not None
        assert results_response['success'] is False
        assert results_response['code'] == 'service_unavailable'
        assert 'Request Timeout' in results_response['error']

    @patch('stix_shifter_modules.darktrace.stix_transmission.api_client.APIClient.get_search_results')
    def test_invalid_request(self, mock_results_response):

        inner_mock = '<html><body><h1>400 Bad request</h1>\nYour browser sent an invalid request.'
        mock_results_response.return_value = get_mock_response(400, inner_mock, 'byte', response=inner_mock)

        query = json.dumps({"queries": ["{\"search\": \"(@fields.query:pop.gmail.com)\", \"fields\": [], \"timeframe\":"
                                        " \"custom\", \"time\": {\"from\": \"2022-03-16T09:23:20.894000Z\", "
                                        "\"to\": \"2022-03-16T09:28:20.894000Z\"}}"]})

        transmission = stix_transmission.StixTransmission('darktrace', self.connection(), self.config())
        results_response = transmission.results(query, 0, 1)

        assert results_response is not None
        assert results_response['success'] is False
        assert results_response['code'] == 'invalid_query'
        assert 'Bad Request' in results_response['error']
