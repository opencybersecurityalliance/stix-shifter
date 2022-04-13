from unittest.mock import patch
import unittest
import json
from stix_shifter_modules.darktrace.stix_transmission.api_client import APIClient
from stix_shifter.stix_transmission import stix_transmission
from requests.exceptions import ConnectionError


class DarktraceMockResponse:
    """ class for Darktrace mock response"""

    def __init__(self, response_code, obj):
        self.code = response_code
        self.object = obj

    def read(self):
        """ to read contents of results returned by api"""
        return bytearray(self.object, 'utf-8')


class PingResponse:
    """ class for ping response"""

    def __init__(self, responseobject):
        self.response = responseobject


class InnerResponse:
    """ class for capturing response"""

    def __init__(self, st_code, txt):
        self.status_code = st_code
        self.text = txt
        self.history = []


class TestDarktraceConnection(unittest.TestCase, object):
    """ class for test Darktrace connection"""

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

        pingmock = InnerResponse(200, """{"status":"SUCCESS"}""")
        pingresponse = PingResponse(pingmock)
        mock_ping_source.return_value = pingresponse

        transmission = stix_transmission.StixTransmission('darktrace', self.connection(), self.config())

        ping_response = transmission.ping()

        assert ping_response is not None
        assert ping_response['success'] is True

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_ping_box(self, mock_ping_source):
        """ test to check ping_data_source function"""

        pingmock = InnerResponse(200, """{"status":"SUCCESS"}""")
        pingresponse = PingResponse(pingmock)
        mock_ping_source.return_value = pingresponse

        configuration = {'auth': {'private_token': '', 'public_token': ''}}
        connection = {'host': 'www.test.com'}
        apiclient = APIClient(connection, configuration)
        ping_response = apiclient.ping_box()

        assert ping_response is not None
        assert ping_response.response.status_code == 200

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_get_search_results(self, mock_ping_source):
        """ test to check ping_data_source function"""

        pingmock = InnerResponse(200, """{"status":"SUCCESS"}""")
        pingresponse = PingResponse(pingmock)
        mock_ping_source.return_value = pingresponse

        configuration = {'auth': {'private_token': '', 'public_token': ''}}
        connection = {'host': 'www.test.com'}
        apiclient = APIClient(connection, configuration)
        ping_response = apiclient.get_search_results('query')

        assert ping_response is not None
        assert ping_response.response.status_code == 200

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_http_query(self, mock_ping_source):
        """ test to check query of process element """

        pingmock = InnerResponse(200, """{"status":"SUCCESS"}""")
        pingresponse = PingResponse(pingmock)
        mock_ping_source.return_value = pingresponse

        query = json.dumps({
            "queries": [
                "{\"search\": \"((@fields.method:GET) AND (@fields.epochdate:>1647409125.029 AND "
                "@fields.epochdate:<1647409425.029))\", \"fields\": [], \"timeframe\": \"custom\", "
                "\"time\": {\"from\": \"2022-03-16T05:38:45.029000Z\", "
                "\"to\": \"2022-03-16T05:43:45.029000Z\"}}"
            ]
        })

        transmission = stix_transmission.\
            StixTransmission('darktrace', self.connection(), self.config())
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert query_response['search_id'] is not None
        assert query_response['search_id'] == query

    @patch('stix_shifter_modules.darktrace.stix_transmission.api_client.APIClient.get_search_results')
    def test_http_results(self, mock_results_response):
        mock_response_dict = json.dumps({
            'took': 2,
            'timed_out': False,
            '_shards': {
                'total': 2,
                'successful': 2,
                'skipped': 0,
                'failed': 0
            },
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
                }, {
                    '_index': 'logstash-vmprobe-2022.03.15',
                    '_type': 'doc',
                    '_id': 'AX-NRncogOn5vlEO2Z2A',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647342605.613303,
                            'source_port': 62264,
                            'host': 'www.darktrace.com',
                            'trans_depth': 1,
                            'uri': '/en/',
                            'dest_port': 80,
                            'source_ip': '172.31.81.98',
                            'response_body_len': 0,
                            'redirect_location': 'https://www.darktrace.com/en/',
                            'dest_ip': '104.20.203.23',
                            'client_header_names': ['HOST', 'CONNECTION', 'UPGRADE-INSECURE-REQUESTS', 'USER-AGENT',
                                                    'ACCEPT', 'ACCEPT-ENCODING', 'ACCEPT-LANGUAGE', 'COOKIE'],
                            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                          '(KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
                            'uid': 'C7q5KW3O7OoHzgvAEf01',
                            'version': '1.1',
                            'status_msg': 'Moved Permanently',
                            'method': 'GET',
                            'status_code': 301,
                            'request_body_len': 0
                        },
                        '@type': 'http',
                        '@timestamp': '2022-03-15T11:10:05',
                        '@message': '1647342605.6133\tC7q5KW3O7OoHzgvAEf01\t172.31.81.98\t62264'
                                    '\t104.20.203.23\t80\t-\t-\twww.darktrace.com\t1\t/en/\t0'
                                    '\thttps://www.darktrace.com/en/'
                                    '\t[HOST,CONNECTION,UPGRADE-'
                                    'INSECURE-REQUESTS,USER-AGENT,ACCEPT,ACCEPT-ENCODING,'
                                    'ACCEPT-LANGUAGE,COOKIE]\tMozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari'
                                    '/537.36\t1.1\tMoved Permanently\tGET\t301\t0',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647342605000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.15',
                    '_type': 'doc',
                    '_id': 'AX-NOTPQgOn5vlEO2ZFM',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647341796.473949,
                            'content_type': 'text/html',
                            'source_port': 61459,
                            'resp_mime_types': 'text/html',
                            'host': '169.254.169.254',
                            'trans_depth': 1,
                            'uri': '/latest/meta-data/iam/security-credentials/',
                            'client_header_names': ['HOST', 'USER-AGENT', 'X-AWS-EC2-METADATA-TOKEN',
                                                    'ACCEPT-ENCODING'],
                            'source_ip': '172.31.81.98',
                            'response_body_len': 337,
                            'dest_port': 80,
                            'dest_ip': '169.254.169.254',
                            'resp_fuids': 'Fs06ZE44IYGH8PbjOg01',
                            'user_agent': 'aws-sdk-go/1.41.4 (go1.17.5; windows; amd64)',
                            'uid': 'C3gsuv17GQOAFa2nvb01',
                            'version': '1.0',
                            'status_msg': 'Not Found',
                            'method': 'GET',
                            'status_code': 404,
                            'request_body_len': 0
                        },
                        '@type': 'http',
                        '@timestamp': '2022-03-15T10:56:36',
                        '@message': '1647341796.4739\tC3gsuv17GQOAFa2nvb01\t172.31.81.98\t61459\t169.254.169.254'
                                    '\t80\t-\t-\ttext/html\t[text/html]\t169.254.169.254\t1'
                                    '\t/latest/meta-data/iam/security-credentials/\t[HOST,USER-AGENT,X-AWS-EC2-'
                                    'METADATA-TOKEN,ACCEPT-ENCODING]\t337\t[Fs06ZE44IYGH8PbjOg01]\taws-sdk-go/1.'
                                    '41.4 (go1.17.5; windows; amd64)\t1.0\tNot Found\tGET\t404\t0',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647341796000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.15',
                    '_type': 'doc',
                    '_id': 'AX-NOTPQgOn5vlEO2ZFL',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647341796.473926,
                            'content_type': 'text/plain',
                            'source_port': 61458,
                            'resp_mime_types': 'text/plain',
                            'host': '169.254.169.254',
                            'trans_depth': 1,
                            'uri': '/latest/meta-data/services/domain',
                            'client_header_names': ['HOST', 'USER-AGENT', 'X-AWS-EC2-METADATA-TOKEN',
                                                    'ACCEPT-ENCODING'],
                            'source_ip': '172.31.81.98',
                            'response_body_len': 13,
                            'dest_port': 80,
                            'dest_ip': '169.254.169.254',
                            'resp_fuids': 'FUdyIV36fEy8fo0KOb01',
                            'user_agent': 'aws-sdk-go/1.41.4 (go1.17.5; windows; amd64)',
                            'uid': 'CB7ppC40oo2UeaHFb201',
                            'version': '1.0',
                            'status_msg': 'OK',
                            'method': 'GET',
                            'status_code': 200,
                            'request_body_len': 0
                        },
                        '@type': 'http',
                        '@timestamp': '2022-03-15T10:56:36',
                        '@message': '1647341796.4739\tCB7ppC40oo2UeaHFb201\t172.31.81.98\t61458'
                                    '\t169.254.169.254\t80\t-\t-\ttext/plain\t[text/plain]'
                                    '\t169.254.169.254\t1\t/latest/meta-data/services/domain'
                                    '\t[HOST,USER-AGENT,X-AWS-EC2-METADATA-TOKEN,ACCEPT-ENCODING]'
                                    '\t13\t[FUdyIV36fEy8fo0KOb01]\taws-sdk-go/1.41.4 '
                                    '(go1.17.5; windows; amd64)\t1.0\tOK\tGET\t200\t0',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647341796000]
                }]
            },
            'darktraceChildError': '',
            'kibana': {
                'index': ['logstash-darktrace-2022.03.15'],
                'per_page': 50,
                'time': {
                    'from': '2022-03-15T10:18:00.003Z',
                    'to': '2022-03-15T11:18:00.003Z'
                },
                'default_fields': ['@type', '@message']
            }
        })
        mock_results_response.return_value = DarktraceMockResponse(200, mock_response_dict)
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

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_x509_query(self, mock_ping_source):
        """ test to check query of process element """

        pingmock = InnerResponse(200, """{"status":"SUCCESS"}""")
        pingresponse = PingResponse(pingmock)
        mock_ping_source.return_value = pingresponse

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

    @patch('stix_shifter_modules.darktrace.stix_transmission.api_client.APIClient.get_search_results')
    def test_x509_results(self, mock_results_response):
        mock_response_dict = json.dumps({
            'took': 2,
            'timed_out': False,
            '_shards': {
                'total': 2,
                'successful': 2,
                'skipped': 0,
                'failed': 0
            },
            'hits': {
                'total': 104,
                'max_score': None,
                'hits': [{
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RatG0gOn5vlEO3Sw4',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412159.700335,
                            'source_port': 57990,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'FSne9FVehr5qzFONl01',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '193.93.62.11',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'CPgY6C2m1WXehA0Nsa01',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:29:19',
                        '@message': '1647412159.7003\tCPgY6C2m1WXehA0Nsa01\t193.93.62.11\t57990'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tFSne9FVehr5qzFONl01'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412159000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RatG0gOn5vlEO3Sw1',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412158.67431,
                            'source_port': 1048,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'F8hRKYCf0f4G3ifG301',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'CP18N32fkN6iL7P1D701',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:29:18',
                        '@message': '1647412158.6743\tCP18N32fkN6iL7P1D701\t94.232.47.58\t1048'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tF8hRKYCf0f4G3ifG301'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412158000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RatG0gOn5vlEO3Swt',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412156.651457,
                            'source_port': 45892,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'Frglgj21MPHYvHQU5a01',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '193.93.62.101',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'C38v7qNGQwkHhUSi401',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:29:16',
                        '@message': '1647412156.6515\tC38v7qNGQwkHhUSi401\t193.93.62.101\t45892'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tFrglgj21MPHYvHQU5a01'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412156000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RatG0gOn5vlEO3Sws',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412156.651431,
                            'source_port': 50145,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'FTIWKM2o8zrhy8be0701',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'CM7mPB2PH0UcnuHxBl01',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:29:16',
                        '@message': '1647412156.6514\tCM7mPB2PH0UcnuHxBl01\t94.232.47.58\t50145'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tFTIWKM2o8zrhy8be0701'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412156000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-Raro6gOn5vlEO3Swj',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412154.59548,
                            'source_port': 52542,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'FT3WAy1vHe3b3r3xGi01',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '193.93.62.10',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'C0GgltMZoRM3zsWDi01',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:29:14',
                        '@message': '1647412154.5955\tC0GgltMZoRM3zsWDi01\t193.93.62.10\t52542\t172.31.81.98'
                                    '\t3389\t-\t-\t1660562534\tFT3WAy1vHe3b3r3xGi01\trsa'
                                    '\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412154000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-Raro6gOn5vlEO3Swi',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412154.595466,
                            'source_port': 39612,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'FBnoj7UQUhBU7ClHg01',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'CvJirO3ednYGyabEDj01',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:29:14',
                        '@message': '1647412154.5955\tCvJirO3ednYGyabEDj01\t94.232.47.58\t39612'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tFBnoj7UQUhBU7ClHg01'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412154000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-Raro6gOn5vlEO3Swd',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412153.569256,
                            'source_port': 51618,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'FOvy463PGUhWTuhtje01',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '142.132.248.164',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'C5Rxpc2cebXOB5Lebd01',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:29:13',
                        '@message': '1647412153.5693\tC5Rxpc2cebXOB5Lebd01\t142.132.248.164\t51618'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tFOvy463PGUhWTuhtje01'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412153000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-Raro6gOn5vlEO3Swc',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412153.569251,
                            'source_port': 36856,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'FABjF94YSFEROb9t3e01',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '193.93.62.33',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'CzcOXd1Keys7qhHOzi01',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:29:13',
                        '@message': '1647412153.5693\tCzcOXd1Keys7qhHOzi01\t193.93.62.33\t36856'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tFABjF94YSFEROb9t3e01'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412153000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-Raro6gOn5vlEO3SwY',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412152.542133,
                            'source_port': 28995,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'FYzZe41LtZHJCopHQ601',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'CfXXPl3lBBYqjrQBL301',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:29:12',
                        '@message': '1647412152.5421\tCfXXPl3lBBYqjrQBL301\t94.232.47.58'
                                    '\t28995\t172.31.81.98\t3389\t-\t-\t1660562534'
                                    '\tFYzZe41LtZHJCopHQ601\trsa\tsha256WithRSAEncryption'
                                    '\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ\t65537\t2048\t1644751334'
                                    '\t3\t76FDB38B8D5AA88844250EFE0EA89026\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412152000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-Raro6gOn5vlEO3SwQ',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412150.498488,
                            'source_port': 18158,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'FpDML2BlLVKH6IRm201',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'CEsruZJWtXpsbMFB801',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:29:10',
                        '@message': '1647412150.4985\tCEsruZJWtXpsbMFB801\t94.232.47.58\t18158'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tFpDML2BlLVKH6IRm201'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412150000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RapMkgOn5vlEO3SwN',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412149.478787,
                            'source_port': 45608,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'F4auYJHOqi1emmkxi01',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '193.93.62.22',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'CTEP573u738pTikBu201',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:29:09',
                        '@message': '1647412149.4788\tCTEP573u738pTikBu201\t193.93.62.22\t45608'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tF4auYJHOqi1emmkxi01'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412149000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RapMkgOn5vlEO3SwM',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412149.47875,
                            'source_port': 46616,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'FLO8Gu39zHI0viSX4h01',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '84.242.35.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'CMd47I2WF3XTOnV0Yg01',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:29:09',
                        '@message': '1647412149.4787\tCMd47I2WF3XTOnV0Yg01\t84.242.35.58\t46616'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tFLO8Gu39zHI0viSX4h01'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412149000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RapMkgOn5vlEO3SwH',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412148.459066,
                            'source_port': 7370,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'FwxnKlzWATcuqwV2k01',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'CuJQn7LQdw1AR6zqg01',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:29:08',
                        '@message': '1647412148.4591\tCuJQn7LQdw1AR6zqg01\t94.232.47.58'
                                    '\t7370\t172.31.81.98\t3389\t-\t-\t1660562534\tFwxnKlzWATcuqwV2k01'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412148000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RapMkgOn5vlEO3Sv_',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412146.413368,
                            'source_port': 55921,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'F9Y03q3forWFr3CXa201',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'CxfTD52fQPoTq4m9301',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:29:06',
                        '@message': '1647412146.4134\tCxfTD52fQPoTq4m9301\t94.232.47.58\t55921'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tF9Y03q3forWFr3CXa201'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412146000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RapMkgOn5vlEO3Sv1',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412144.374805,
                            'source_port': 45094,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'FhHJBC4nTacYe9nTKe01',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'CQcFIf3xQ5ltZdmI6c01',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:29:04',
                        '@message': '1647412144.3748\tCQcFIf3xQ5ltZdmI6c01\t94.232.47.58\t45094'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tFhHJBC4nTacYe9nTKe01'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412144000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RanuzgOn5vlEO3Svx',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412143.355467,
                            'source_port': 59316,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'FjNB1kJoftLC9nM4g01',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '193.93.62.11',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'C7JPFw3fzGLW4ubPoh01',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:29:03',
                        '@message': '1647412143.3555\tC7JPFw3fzGLW4ubPoh01\t193.93.62.11\t59316'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tFjNB1kJoftLC9nM4g01'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412143000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RanuzgOn5vlEO3Svw',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412142.336135,
                            'source_port': 35183,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'F0P1OFZVe8vSl9QMc01',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'CJIcV6eD5ZupPF4O601',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:29:02',
                        '@message': '1647412142.3361\tCJIcV6eD5ZupPF4O601\t94.232.47.58\t35183'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tF0P1OFZVe8vSl9QMc01'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412142000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RanuzgOn5vlEO3Svr',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412141.310497,
                            'source_port': 24348,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'F9rMjNSZyKfbZtvfj01',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'C5rCdohe1vCLndtPh01',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:29:01',
                        '@message': '1647412141.3105\tC5rCdohe1vCLndtPh01\t94.232.47.58\t24348'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tF9rMjNSZyKfbZtvfj01'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412141000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RanuzgOn5vlEO3Svl',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412139.267698,
                            'source_port': 5685,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'F3lUqbOtxs5ceHs1601',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '193.93.62.81',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'ChdyCG4m7XS2GYgpja01',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:28:59',
                        '@message': '1647412139.2677\tChdyCG4m7XS2GYgpja01\t193.93.62.81\t5685'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tF3lUqbOtxs5ceHs1601'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412139000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RanuzgOn5vlEO3Svj',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412138.248729,
                            'source_port': 13481,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'FQ9Nrh0H6pQLFAcTl01',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'C1WsrU1f9LW1sDCLJk01',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:28:58',
                        '@message': '1647412138.2487\tC1WsrU1f9LW1sDCLJk01\t94.232.47.58\t13481'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tFQ9Nrh0H6pQLFAcTl01'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412138000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RanuzgOn5vlEO3Svi',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412138.248702,
                            'source_port': 13964,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'FsyIy9mlqAuqsF7Sh01',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '193.93.62.33',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'CThvVb3aswKVHhZVX101',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:28:58',
                        '@message': '1647412138.2487\tCThvVb3aswKVHhZVX101\t193.93.62.33\t13964'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tFsyIy9mlqAuqsF7Sh01'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412138000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RanfLgOn5vlEO3Svd',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412137.229202,
                            'source_port': 2818,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'FwgCUM1GCho5cOpHtc01',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'CsZdmm2JYc7dDi5Bl201',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:28:57',
                        '@message': '1647412137.2292\tCsZdmm2JYc7dDi5Bl201\t94.232.47.58\t2818'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tFwgCUM1GCho5cOpHtc01'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412137000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RanfLgOn5vlEO3SvY',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412135.206381,
                            'source_port': 51195,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'F6UQbt3ObL6SdpgwG401',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'CUUONk3GPqf3xw0PI701',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:28:55',
                        '@message': '1647412135.2064\tCUUONk3GPqf3xw0PI701\t94.232.47.58\t51195'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tF6UQbt3ObL6SdpgwG401'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412135000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RanfLgOn5vlEO3SvQ',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412133.185144,
                            'source_port': 40418,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'FVieHHUc0YtF1ZI3501',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'CSrxjZ3h7hXKxMLJFk01',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:28:53',
                        '@message': '1647412133.1851\tCSrxjZ3h7hXKxMLJFk01\t94.232.47.58\t40418'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tFVieHHUc0YtF1ZI3501'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412133000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-Ram_5gOn5vlEO3SvL',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412131.125667,
                            'source_port': 29130,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'FIEfGo1In9FFd4TKW901',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'CxO6Xs3kLXpb5rlH5601',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:28:51',
                        '@message': '1647412131.1257\tCxO6Xs3kLXpb5rlH5601\t94.232.47.58\t29130'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tFIEfGo1In9FFd4TKW901'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412131000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-Ram_5gOn5vlEO3SvG',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412129.062136,
                            'source_port': 17915,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'FPdpAP38I0LwOfEIs701',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'CNs9Es3HGFOF8hU08201',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:28:49',
                        '@message': '1647412129.0621\tCNs9Es3HGFOF8hU08201\t94.232.47.58\t17915'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tFPdpAP38I0LwOfEIs701'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412129000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-Ram_5gOn5vlEO3SvC',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412127.028687,
                            'source_port': 63700,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'FWoEPd1o5Xs6DEZEmd01',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '193.93.62.11',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'CMMnT41AVfxSaf3n3a01',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:28:47',
                        '@message': '1647412127.0287\tCMMnT41AVfxSaf3n3a01\t193.93.62.11\t63700'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tFWoEPd1o5Xs6DEZEmd01'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412127000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-Ram_5gOn5vlEO3Su-',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412126.003879,
                            'source_port': 7730,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'FEHf4h1p2CwiLlbSPb01',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'C69BY24mn0RuMlMskj01',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:28:46',
                        '@message': '1647412126.0039\tC69BY24mn0RuMlMskj01'
                                    '\t94.232.47.58\t7730\t172.31.81.98\t3389'
                                    '\t-\t-\t1660562534\tFEHf4h1p2CwiLlbSPb01'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption'
                                    '\tCN=EC2AMAZ-2GNPPAQ\t65537\t2048\t1644751334'
                                    '\t3\t76FDB38B8D5AA88844250EFE0EA89026\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412126000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RakjlgOn5vlEO3Su5',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412123.967443,
                            'source_port': 55851,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'Fh9Bd8Uo6kcVc73V601',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'CA8MzC1u07VhRfKPpe01',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:28:43',
                        '@message': '1647412123.9674\tCA8MzC1u07VhRfKPpe01\t94.232.47.58'
                                    '\t55851\t172.31.81.98\t3389\t-\t-\t1660562534'
                                    '\tFh9Bd8Uo6kcVc73V601\trsa\tsha256WithRSAEncryption'
                                    '\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ\t65537\t2048'
                                    '\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412123000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RakjlgOn5vlEO3Su2',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412122.93909,
                            'source_port': 44791,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'FPN2L14elW3SpFo9pk01',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'C6DD0r2CuHdkbRLqE701',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:28:42',
                        '@message': '1647412122.9391\tC6DD0r2CuHdkbRLqE701\t94.232.47.58\t44791'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tFPN2L14elW3SpFo9pk01'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412122000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RakjlgOn5vlEO3Suv',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412120.916151,
                            'source_port': 33417,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'F9UcZYOz3JIPhslFh01',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'Cp1Rxiq5cmgBF7Pge01',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:28:40',
                        '@message': '1647412120.9162\tCp1Rxiq5cmgBF7Pge01\t94.232.47.58\t33417'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tF9UcZYOz3JIPhslFh01'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412120000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RaimkgOn5vlEO3Sur',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412118.893799,
                            'source_port': 22708,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'Fuielx3NNwdkLxIeq601',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'CPrjJttELiqpq5gDj01',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:28:38',
                        '@message': '1647412118.8938\tCPrjJttELiqpq5gDj01\t94.232.47.58\t22708'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tFuielx3NNwdkLxIeq601'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412118000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RaimkgOn5vlEO3Suf',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412115.836866,
                            'source_port': 13169,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'FMGxIL39RkiZH6iTdc01',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'ClWd8S2LQcK0ufBVsj01',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:28:35',
                        '@message': '1647412115.8369\tClWd8S2LQcK0ufBVsj01\t94.232.47.58\t13169'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tFMGxIL39RkiZH6iTdc01'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412115000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RaimkgOn5vlEO3Sue',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412115.836766,
                            'source_port': 49741,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'FaheVX1louxaFvbPw901',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '185.190.24.86',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'CjyKCB4MiP94hUjrL601',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:28:35',
                        '@message': '1647412115.8368\tCjyKCB4MiP94hUjrL601\t185.190.24.86\t49741'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tFaheVX1louxaFvbPw901'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412115000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RaimkgOn5vlEO3Sub',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412114.810719,
                            'source_port': 2483,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'Fy8rN44ARJT9t8WVQj01',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'CJ4ywX1qesSykIEfH601',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:28:34',
                        '@message': '1647412114.8107\tCJ4ywX1qesSykIEfH601\t94.232.47.58\t2483\t172.31.81.98'
                                    '\t3389\t-\t-\t1660562534\tFy8rN44ARJT9t8WVQj01\trsa'
                                    '\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412114000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RagpjgOn5vlEO3SuU',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412112.757499,
                            'source_port': 50591,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'FPvAvm1sOwdhdMFZ6701',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'C4I5iZ3oUmdahBR77d01',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:28:32',
                        '@message': '1647412112.7575\tC4I5iZ3oUmdahBR77d01\t94.232.47.58\t50591'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tFPvAvm1sOwdhdMFZ6701'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412112000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RagpjgOn5vlEO3SuP',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412110.718674,
                            'source_port': 54154,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'FTP5VK2ULnifP0Tjcb01',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '65.108.102.39',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'Cic8Wu3RnckLeZ1uVd01',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:28:30',
                        '@message': '1647412110.7187\tCic8Wu3RnckLeZ1uVd01\t65.108.102.39\t54154'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tFTP5VK2ULnifP0Tjcb01'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412110000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RagpjgOn5vlEO3SuO',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412110.718652,
                            'source_port': 40651,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'FLGL3u2cKuzNjIgSxf01',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'CONFoz4g5jJ8dbxWk101',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:28:30',
                        '@message': '1647412110.7187\tCONFoz4g5jJ8dbxWk101\t94.232.47.58\t40651'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tFLGL3u2cKuzNjIgSxf01'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412110000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RagpjgOn5vlEO3SuI',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412108.675559,
                            'source_port': 29585,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'FUTAj03o1ImaMR4Od01',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'CCIfKZ3U26RUFlKM1601',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:28:28',
                        '@message': '1647412108.6756\tCCIfKZ3U26RUFlKM1601\t94.232.47.58\t29585'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tFUTAj03o1ImaMR4Od01'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412108000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RafLygOn5vlEO3SuD',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412106.602258,
                            'source_port': 18433,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'FWr2Mx3uOobjVWLN1l01',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'C3Dl6o37TMWeDAPVgg01',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:28:26',
                        '@message': '1647412106.6023\tC3Dl6o37TMWeDAPVgg01\t94.232.47.58\t18433'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tFWr2Mx3uOobjVWLN1l01'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412106000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RafLygOn5vlEO3St-',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412104.54375,
                            'source_port': 8391,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'Fvnnw14icHb7H3402901',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'ClMiUn2amL5F2mYeV501',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:28:24',
                        '@message': '1647412104.5438\tClMiUn2amL5F2mYeV501\t94.232.47.58\t8391'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tFvnnw14icHb7H3402901'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412104000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RafLygOn5vlEO3St6',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412102.521058,
                            'source_port': 55814,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'Fh5BwM3lg3HyPdcy2j01',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'CRwOsj1xDP0du1dc6101',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:28:22',
                        '@message': '1647412102.5211\tCRwOsj1xDP0du1dc6101\t94.232.47.58\t55814'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tFh5BwM3lg3HyPdcy2j01'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412102000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-Rae8KgOn5vlEO3Stx',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412100.498113,
                            'source_port': 45223,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'FDisDH1vTAHU1bWqll01',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'CLxVyP4bZnJrovG7k01',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:28:20',
                        '@message': '1647412100.4981\tCLxVyP4bZnJrovG7k01\t94.232.47.58\t45223'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tFDisDH1vTAHU1bWqll01'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412100000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-Rae8KgOn5vlEO3Str',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412098.452758,
                            'source_port': 33904,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'FRqrxI1QtWHojRi5Xf01',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'ChEkFLsPcmPtWcIxc01',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:28:18',
                        '@message': '1647412098.4528\tChEkFLsPcmPtWcIxc01\t94.232.47.58\t33904\t172.31.81.98'
                                    '\t3389\t-\t-\t1660562534\tFRqrxI1QtWHojRi5Xf01\trsa'
                                    '\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412098000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-Rae8KgOn5vlEO3Stk',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412096.41468,
                            'source_port': 24130,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'Fexh4V3gZerWxGBplk01',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'CEmVZr3rS7U4Ddl1g301',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:28:16',
                        '@message': '1647412096.4147\tCEmVZr3rS7U4Ddl1g301\t94.232.47.58\t24130\t172.31.81.98'
                                    '\t3389'
                                    '\t-\t-\t1660562534\tFexh4V3gZerWxGBplk01\trsa\tsha256WithRSAEncryption'
                                    '\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ\t65537\t2048\t1644751334\t3'
                                    '\t76FDB38B8D5AA88844250EFE0EA89026\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412096000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-Rae8KgOn5vlEO3Stj',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412096.414675,
                            'source_port': 57245,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'FpFqDl3l8isyXmpUpc01',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '193.93.62.101',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'CX6gNH1hKqM6isMeIj01',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:28:16',
                        '@message': '1647412096.4147\tCX6gNH1hKqM6isMeIj01\t193.93.62.101\t57245'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tFpFqDl3l8isyXmpUpc01'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412096000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RadOxgOn5vlEO3Stc',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412094.398405,
                            'source_port': 13371,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'FODK0c2H4OVxmQ7lgc01',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'Cu6KAE2cgkAzleQdk301',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:28:14',
                        '@message': '1647412094.3984\tCu6KAE2cgkAzleQdk301\t94.232.47.58\t13371'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tFODK0c2H4OVxmQ7lgc01'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412094000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RadOxgOn5vlEO3StN',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412092.353342,
                            'source_port': 2328,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'Few3nB1jr6Er6HZ7ve01',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'Cy2hFbS0nZvXzJkD101',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:28:12',
                        '@message': '1647412092.3533\tCy2hFbS0nZvXzJkD101\t94.232.47.58\t2328'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tFew3nB1jr6Er6HZ7ve01'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412092000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RadOxgOn5vlEO3StM',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412092.353309,
                            'source_port': 52475,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'FXNlk737vGLCMIJKF201',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '185.190.24.86',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'Cvl3H13IJ2ggEpeNHc01',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:28:12',
                        '@message': '1647412092.3533\tCvl3H13IJ2ggEpeNHc01\t185.190.24.86\t52475'
                                    '\t172.31.81.98\t3389\t-\t-\t1660562534\tFXNlk737vGLCMIJKF201'
                                    '\trsa\tsha256WithRSAEncryption\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ'
                                    '\t65537\t2048\t1644751334\t3\t76FDB38B8D5AA88844250EFE0EA89026'
                                    '\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412092000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-RadOxgOn5vlEO3Ss-',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647412090.303098,
                            'source_port': 50445,
                            'certificate_not_valid_after': 1660562534,
                            'fid': 'FClE471IeQHrKqtGck01',
                            'certificate_key_type': 'rsa',
                            'certificate_sig_alg': 'sha256WithRSAEncryption',
                            'certificate_key_alg': 'rsaEncryption',
                            'certificate_subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'source_ip': '94.232.47.58',
                            'certificate_exponent': '65537',
                            'certificate_key_length': 2048,
                            'dest_ip': '172.31.81.98',
                            'certificate_not_valid_before': 1644751334,
                            'uid': 'CBRGkeDyiGZjYMzSd01',
                            'dest_port': 3389,
                            'certificate_version': 3,
                            'certificate_serial': '76FDB38B8D5AA88844250EFE0EA89026',
                            'certificate_issuer': 'CN=EC2AMAZ-2GNPPAQ'
                        },
                        '@type': 'x509',
                        '@timestamp': '2022-03-16T06:28:10',
                        '@message': '1647412090.3031\tCBRGkeDyiGZjYMzSd01\t94.232.47.58\t50445'
                                    '\t172.31.81.98\t3389'
                                    '\t-\t-\t1660562534\tFClE471IeQHrKqtGck01\trsa\tsha256WithRSAEncryption'
                                    '\trsaEncryption\tCN=EC2AMAZ-2GNPPAQ\t65537\t2048\t1644751334\t3\
                                    t76FDB38B8D5AA88844250EFE0EA89026\tCN=EC2AMAZ-2GNPPAQ',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647412090000]
                }]
            },
            'darktraceChildError': '',
            'kibana': {
                'index': ['logstash-darktrace-2022.03.16'],
                'per_page': 50,
                'time': {
                    'from': '2022-03-16T06:25:08.389Z',
                    'to': '2022-03-16T06:30:08.389Z'
                },
                'default_fields': ['@type', '@message']
            }
        })

        mock_results_response.return_value = DarktraceMockResponse(200, mock_response_dict)
        # result_data = {}
        query = json.dumps({
            "queries": [
                "{\"search\": \"((@fields.certificate_serial:76FDB38B8D5AA88844250EFE0EA89026) AND "
                "(@fields.epochdate:>1647411908.389 AND @fields.epochdate:<1647412208.389))\", "
                "\"fields\": [], \"timeframe\": \"custom\", \"time\": "
                "{\"from\": \"2022-03-16T06:25:08.389000Z\", "
                "\"to\": \"2022-03-16T06:30:08.389000Z\"}}"]})
        offset = 0
        length = 1
        transmission = stix_transmission.StixTransmission('darktrace', self.connection(), self.config())
        results_response = transmission.results(query, offset, length)
        assert results_response is not None
        assert results_response['success'] is True
        assert 'data' in results_response
        assert results_response['data'] is not None

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_multievent_query(self, mock_ping_source):
        """ test to check query of process element """

        pingmock = InnerResponse(200, """{"status":"SUCCESS"}""")
        pingresponse = PingResponse(pingmock)
        mock_ping_source.return_value = pingresponse

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
    def test_multievent_results(self, mock_results_response):
        mock_response_dict = json.dumps({
            'took': 1,
            'timed_out': False,
            '_shards': {
                'total': 2,
                'successful': 2,
                'skipped': 0,
                'failed': 0
            },
            'hits': {
                'total': 33,
                'max_score': None,
                'hits': [{
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-SDQY1gOn5vlEO3XYJ',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647422782.822214,
                            'total_client_ciphers': 50,
                            'validation_status': 'unable to get local issuer certificate',
                            'client_hello_seen': True,
                            'ja3_client_fingerprint': '75fb48a465416d66291fb52a733d4787',
                            'source_port': 51797,
                            'dest_port': 3389,
                            'established': True,
                            'source_ip': '185.190.24.86',
                            'issuer': 'CN=EC2AMAZ-2GNPPAQ',
                            'cipher': 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                            'dest_ip': '172.31.81.98',
                            'cert_chain_fuids': 'FZ0NMJ17z414GCruTl01',
                            'curve': 'secp384r1',
                            'uid': 'Cl1dpm2TNyrsDI6yM801',
                            'version': 'TLS1.0',
                            'ja3s_server_fingerprint': 'bcf3a836c82d12ee988005fb0c011445',
                            'subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'resumed': False
                        },
                        '@type': 'ssl',
                        '@timestamp': '2022-03-16T09:26:22',
                        '@message': '1647422782.8222\tCl1dpm2TNyrsDI6yM801\t185.190.24.86\t51797'
                                    '\t172.31.81.98\t3389'
                                    '\t-\t-\t50\tunable to get local issuer certificate\ttrue'
                                    '\t75fb48a465416d66291fb52a733d4787\ttrue\tCN=EC2AMAZ-2GNPPAQ'
                                    '\tTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\t[FZ0NMJ17z414GCruTl01]'
                                    '\tsecp384r1\tTLS1.0'
                                    '\tbcf3a836c82d12ee988005fb0c011445\tCN=EC2AMAZ-2GNPPAQ\tfalse',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647422782000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-SDQY1gOn5vlEO3XYK',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647422782.822188,
                            'total_client_ciphers': 50,
                            'validation_status': 'unable to get local issuer certificate',
                            'client_hello_seen': True,
                            'ja3_client_fingerprint': '75fb48a465416d66291fb52a733d4787',
                            'source_port': 63672,
                            'dest_port': 3389,
                            'established': True,
                            'source_ip': '193.93.62.11',
                            'issuer': 'CN=EC2AMAZ-2GNPPAQ',
                            'cipher': 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                            'dest_ip': '172.31.81.98',
                            'cert_chain_fuids': 'FZbq3q3UjmNrc7WPIc01',
                            'curve': 'secp384r1',
                            'uid': 'C04eTb1UC4u4x5wYNi01',
                            'version': 'TLS1.0',
                            'ja3s_server_fingerprint': 'bcf3a836c82d12ee988005fb0c011445',
                            'subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'resumed': False
                        },
                        '@type': 'ssl',
                        '@timestamp': '2022-03-16T09:26:22',
                        '@message': '1647422782.8222\tC04eTb1UC4u4x5wYNi01\t193.93.62.11\t63672\t172.31.81.98\t3389\t-\t-\t50'
                                    '\tunable to get local issuer certificate\ttrue\t75fb48a465416d66291fb52a733d4787'
                                    '\ttrue\tCN=EC2AMAZ-2GNPPAQ\tTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\t[FZbq3q3UjmNrc7WPIc01]'
                                    '\tsecp384r1\tTLS1.0\tbcf3a836c82d12ee988005fb0c011445\tCN=EC2AMAZ-2GNPPAQ\tfalse',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647422782000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-SDObxgOn5vlEO3XX8',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647422776.716088,
                            'total_client_ciphers': 55,
                            'validation_status': 'unable to get local issuer certificate',
                            'client_hello_seen': True,
                            'ja3_client_fingerprint': '0b63812a99e66c82a20d30c3b9ba6e06',
                            'source_port': 62339,
                            'dest_port': 3389,
                            'established': True,
                            'source_ip': '64.44.139.184',
                            'issuer': 'CN=EC2AMAZ-2GNPPAQ',
                            'cipher': 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                            'dest_ip': '172.31.81.98',
                            'cert_chain_fuids': 'FCQ88z1RPnGxafzggj01',
                            'curve': 'secp384r1',
                            'uid': 'CwivzD3KLRyyoJuMx401',
                            'version': 'TLS1.0',
                            'ja3s_server_fingerprint': 'bcf3a836c82d12ee988005fb0c011445',
                            'subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'resumed': False
                        },
                        '@type': 'ssl',
                        '@timestamp': '2022-03-16T09:26:16',
                        '@message': '1647422776.7161\tCwivzD3KLRyyoJuMx401\t64.44.139.184\t62339\t172.31.81.98\t3389'
                                    '\t-\t-\t55\tunable to get local issuer certificate\ttrue'
                                    '\t0b63812a99e66c82a20d30c3b9ba6e06'
                                    '\ttrue\tCN=EC2AMAZ-2GNPPAQ\tTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\t[FCQ88z1RPnGxafzggj01]'
                                    '\tsecp384r1\tTLS1.0\tbcf3a836c82d12ee988005fb0c011445\tCN=EC2AMAZ-2GNPPAQ\tfalse',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647422776000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-SDM-AgOn5vlEO3XXf',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647422770.641147,
                            'total_client_ciphers': 50,
                            'validation_status': 'unable to get local issuer certificate',
                            'client_hello_seen': True,
                            'ja3_client_fingerprint': '75fb48a465416d66291fb52a733d4787',
                            'source_port': 52032,
                            'dest_port': 3389,
                            'established': True,
                            'source_ip': '193.93.62.6',
                            'issuer': 'CN=EC2AMAZ-2GNPPAQ',
                            'cipher': 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                            'dest_ip': '172.31.81.98',
                            'cert_chain_fuids': 'Feg9ABQWxv9k4YYsb01',
                            'curve': 'secp384r1',
                            'uid': 'C8CfnG4SjWPaWOG3Ij01',
                            'version': 'TLS1.0',
                            'ja3s_server_fingerprint': 'bcf3a836c82d12ee988005fb0c011445',
                            'subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'resumed': False
                        },
                        '@type': 'ssl',
                        '@timestamp': '2022-03-16T09:26:10',
                        '@message': '1647422770.6411\tC8CfnG4SjWPaWOG3Ij01\t193.93.62.6\t52032\t172.31.81.98\t3389'
                                    '\t-\t-\t50\tunable to get local issuer certificate\ttrue'
                                    '\t75fb48a465416d66291fb52a733d4787'
                                    '\ttrue\tCN=EC2AMAZ-2GNPPAQ\tTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\t[Feg9ABQWxv9k4YYsb01]'
                                    '\tsecp384r1\tTLS1.0\tbcf3a836c82d12ee988005fb0c011445\tCN=EC2AMAZ-2GNPPAQ\tfalse',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647422770000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-SDKhvgOn5vlEO3XXM',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647422765.574854,
                            'total_client_ciphers': 50,
                            'validation_status': 'unable to get local issuer certificate',
                            'client_hello_seen': True,
                            'ja3_client_fingerprint': '75fb48a465416d66291fb52a733d4787',
                            'source_port': 25826,
                            'dest_port': 3389,
                            'established': True,
                            'source_ip': '193.93.62.6',
                            'issuer': 'CN=EC2AMAZ-2GNPPAQ',
                            'cipher': 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                            'dest_ip': '172.31.81.98',
                            'cert_chain_fuids': 'FudD634kGUm8PYsM8k01',
                            'curve': 'secp384r1',
                            'uid': 'CJFQUv1BdSgmtD6Hb401',
                            'version': 'TLS1.0',
                            'ja3s_server_fingerprint': 'bcf3a836c82d12ee988005fb0c011445',
                            'subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'resumed': False
                        },
                        '@type': 'ssl',
                        '@timestamp': '2022-03-16T09:26:05',
                        '@message': '1647422765.5749\tCJFQUv1BdSgmtD6Hb401\t193.93.62.6\t25826\t172.31.81.98\t3389'
                                    '\t-\t-\t50\tunable to get local issuer certificate\ttrue'
                                    '\t75fb48a465416d66291fb52a733d4787'
                                    '\ttrue\tCN=EC2AMAZ-2GNPPAQ\tTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\t[FudD634kGUm8PYsM8k01]'
                                    '\tsecp384r1\tTLS1.0\tbcf3a836c82d12ee988005fb0c011445\tCN=EC2AMAZ-2GNPPAQ\tfalse',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647422765000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-SDJD7gOn5vlEO3XXF',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647422763.531261,
                            'total_client_ciphers': 50,
                            'validation_status': 'unable to get local issuer certificate',
                            'client_hello_seen': True,
                            'ja3_client_fingerprint': '75fb48a465416d66291fb52a733d4787',
                            'source_port': 17813,
                            'dest_port': 3389,
                            'established': True,
                            'source_ip': '193.93.62.6',
                            'issuer': 'CN=EC2AMAZ-2GNPPAQ',
                            'cipher': 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                            'dest_ip': '172.31.81.98',
                            'cert_chain_fuids': 'FR3BF3sg3pyIPm30201',
                            'curve': 'secp384r1',
                            'uid': 'Ct4RLG2B9VcS7LAwLf01',
                            'version': 'TLS1.0',
                            'ja3s_server_fingerprint': 'bcf3a836c82d12ee988005fb0c011445',
                            'subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'resumed': False
                        },
                        '@type': 'ssl',
                        '@timestamp': '2022-03-16T09:26:03',
                        '@message': '1647422763.5313\tCt4RLG2B9VcS7LAwLf01\t193.93.62.6\t17813\t172.31.81.98'
                                    '\t3389\t-\t-\t50\tunable to get local issuer certificate\ttrue'
                                    '\t75fb48a465416d66291fb52a733d4787\ttrue\tCN=EC2AMAZ-2GNPPAQ'
                                    '\tTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\t[FR3BF3sg3pyIPm30201]\tsecp384r1\tTLS1.0'
                                    '\tbcf3a836c82d12ee988005fb0c011445\tCN=EC2AMAZ-2GNPPAQ\tfalse',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647422763000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-SDHmKgOn5vlEO3XWr',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647422755.389662,
                            'total_client_ciphers': 41,
                            'validation_status': 'unable to get local issuer certificate',
                            'client_hello_seen': True,
                            'ja3_client_fingerprint': '43e25370946f1b41b411e6d0bf378456',
                            'source_port': 54725,
                            'dest_port': 3389,
                            'established': True,
                            'source_ip': '135.181.0.29',
                            'issuer': 'CN=EC2AMAZ-2GNPPAQ',
                            'cipher': 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                            'dest_ip': '172.31.81.98',
                            'cert_chain_fuids': 'FMuXWG2O3dAEs1icQa01',
                            'curve': 'secp384r1',
                            'uid': 'CnKVba2wQqBy5A8lR501',
                            'version': 'TLS1.0',
                            'ja3s_server_fingerprint': 'bcf3a836c82d12ee988005fb0c011445',
                            'subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'resumed': False
                        },
                        '@type': 'ssl',
                        '@timestamp': '2022-03-16T09:25:55',
                        '@message': '1647422755.3897\tCnKVba2wQqBy5A8lR501\t135.181.0.29\t54725\t172.31.81.98'
                                    '\t3389\t-\t-\t41\tunable to get local issuer certificate\ttrue'
                                    '\t43e25370946f1b41b411e6d0bf378456\ttrue\tCN=EC2AMAZ-2GNPPAQ'
                                    '\tTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\t[FMuXWG2O3dAEs1icQa01]\tsecp384r1\tTLS1.0'
                                    '\tbcf3a836c82d12ee988005fb0c011445\tCN=EC2AMAZ-2GNPPAQ\tfalse',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647422755000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-SDHmKgOn5vlEO3XWl',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647422753.350397,
                            'total_client_ciphers': 50,
                            'validation_status': 'unable to get local issuer certificate',
                            'client_hello_seen': True,
                            'ja3_client_fingerprint': '75fb48a465416d66291fb52a733d4787',
                            'source_port': 58909,
                            'dest_port': 3389,
                            'established': True,
                            'source_ip': '193.93.62.81',
                            'issuer': 'CN=EC2AMAZ-2GNPPAQ',
                            'cipher': 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                            'dest_ip': '172.31.81.98',
                            'cert_chain_fuids': 'FnSAYX3IF0PKzmH7y401',
                            'curve': 'secp384r1',
                            'uid': 'C5MxAj3XioZcEeiyla01',
                            'version': 'TLS1.0',
                            'ja3s_server_fingerprint': 'bcf3a836c82d12ee988005fb0c011445',
                            'subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'resumed': False
                        },
                        '@type': 'ssl',
                        '@timestamp': '2022-03-16T09:25:53',
                        '@message': '1647422753.3504\tC5MxAj3XioZcEeiyla01\t193.93.62.81\t58909\t172.31.81.98\t3389'
                                    '\t-\t-\t50\tunable to get local issuer certificate\ttrue'
                                    '\t75fb48a465416d66291fb52a733d4787'
                                    '\ttrue\tCN=EC2AMAZ-2GNPPAQ\tTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\t[FnSAYX3IF0PKzmH7y401]'
                                    '\tsecp384r1\tTLS1.0\tbcf3a836c82d12ee988005fb0c011445\tCN=EC2AMAZ-2GNPPAQ\tfalse',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647422753000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-SDHWigOn5vlEO3XWY',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647422751.313045,
                            'total_client_ciphers': 50,
                            'validation_status': 'unable to get local issuer certificate',
                            'client_hello_seen': True,
                            'ja3_client_fingerprint': '75fb48a465416d66291fb52a733d4787',
                            'source_port': 51510,
                            'dest_port': 3389,
                            'established': True,
                            'source_ip': '185.190.24.90',
                            'issuer': 'CN=EC2AMAZ-2GNPPAQ',
                            'cipher': 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                            'dest_ip': '172.31.81.98',
                            'cert_chain_fuids': 'FR2Mkq4MuNbqhyQYi501',
                            'curve': 'secp384r1',
                            'uid': 'CT2f4ZpShJ6yAjZwc01',
                            'version': 'TLS1.0',
                            'ja3s_server_fingerprint': 'bcf3a836c82d12ee988005fb0c011445',
                            'subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'resumed': False
                        },
                        '@type': 'ssl',
                        '@timestamp': '2022-03-16T09:25:51',
                        '@message': '1647422751.313\tCT2f4ZpShJ6yAjZwc01\t185.190.24.90\t51510\t172.31.81.98\t3389\t-\t-\t50'
                                    '\tunable to get local issuer certificate\ttrue\t75fb48a465416d66291fb52a733d4787\ttrue'
                                    '\tCN=EC2AMAZ-2GNPPAQ\tTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\t[FR2Mkq4MuNbqhyQYi501]'
                                    '\tsecp384r1\tTLS1.0\tbcf3a836c82d12ee988005fb0c011445\tCN=EC2AMAZ-2GNPPAQ\tfalse',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647422751000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-SDFZggOn5vlEO3XVw',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647422742.164141,
                            'total_client_ciphers': 50,
                            'validation_status': 'unable to get local issuer certificate',
                            'client_hello_seen': True,
                            'ja3_client_fingerprint': '75fb48a465416d66291fb52a733d4787',
                            'source_port': 50607,
                            'dest_port': 3389,
                            'established': True,
                            'source_ip': '185.190.24.83',
                            'issuer': 'CN=EC2AMAZ-2GNPPAQ',
                            'cipher': 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                            'dest_ip': '172.31.81.98',
                            'cert_chain_fuids': 'FJrXwu3x0YtbIBZ3dd01',
                            'curve': 'secp384r1',
                            'uid': 'ChMygJ29kpdlDFj48i01',
                            'version': 'TLS1.0',
                            'ja3s_server_fingerprint': 'bcf3a836c82d12ee988005fb0c011445',
                            'subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'resumed': False
                        },
                        '@type': 'ssl',
                        '@timestamp': '2022-03-16T09:25:42',
                        '@message': '1647422742.1641\tChMygJ29kpdlDFj48i01\t185.190.24.83\t50607\t172.31.81.98\t3389\t-\t-\t50'
                                    '\tunable to get local issuer certificate\ttrue\t75fb48a465416d66291fb52a733d4787\ttrue'
                                    '\tCN=EC2AMAZ-2GNPPAQ\tTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\t[FJrXwu3x0YtbIBZ3dd01]'
                                    '\tsecp384r1\tTLS1.0\tbcf3a836c82d12ee988005fb0c011445\tCN=EC2AMAZ-2GNPPAQ\tfalse',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647422742000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-SDFZggOn5vlEO3XVq',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647422741.138536,
                            'total_client_ciphers': 50,
                            'validation_status': 'unable to get local issuer certificate',
                            'client_hello_seen': True,
                            'ja3_client_fingerprint': '75fb48a465416d66291fb52a733d4787',
                            'source_port': 49562,
                            'dest_port': 3389,
                            'established': True,
                            'source_ip': '185.190.24.83',
                            'issuer': 'CN=EC2AMAZ-2GNPPAQ',
                            'cipher': 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                            'dest_ip': '172.31.81.98',
                            'cert_chain_fuids': 'FDl9cG247FSMltk2kh01',
                            'curve': 'secp384r1',
                            'uid': 'CaqTBp2Q8wSknFIDij01',
                            'version': 'TLS1.0',
                            'ja3s_server_fingerprint': 'bcf3a836c82d12ee988005fb0c011445',
                            'subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'resumed': False
                        },
                        '@type': 'ssl',
                        '@timestamp': '2022-03-16T09:25:41',
                        '@message': '1647422741.1385\tCaqTBp2Q8wSknFIDij01\t185.190.24.83\t49562\t172.31.81.98\t3389\t-\t-\t50'
                                    '\tunable to get local issuer certificate\ttrue\t75fb48a465416d66291fb52a733d4787\ttrue'
                                    '\tCN=EC2AMAZ-2GNPPAQ\tTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA'
                                    '\t[FDl9cG247FSMltk2kh01]\tsecp384r1'
                                    '\tTLS1.0\tbcf3a836c82d12ee988005fb0c011445\tCN=EC2AMAZ-2GNPPAQ\tfalse',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647422741000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-SDFZggOn5vlEO3XVp',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647422740.113726,
                            'total_client_ciphers': 50,
                            'validation_status': 'unable to get local issuer certificate',
                            'client_hello_seen': True,
                            'ja3_client_fingerprint': '75fb48a465416d66291fb52a733d4787',
                            'source_port': 56578,
                            'dest_port': 3389,
                            'established': True,
                            'source_ip': '185.190.24.83',
                            'issuer': 'CN=EC2AMAZ-2GNPPAQ',
                            'cipher': 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                            'dest_ip': '172.31.81.98',
                            'cert_chain_fuids': 'FZmVxD29YlmWb7pgg01',
                            'curve': 'secp384r1',
                            'uid': 'CqU8Sr4elArBGhoYK901',
                            'version': 'TLS1.0',
                            'ja3s_server_fingerprint': 'bcf3a836c82d12ee988005fb0c011445',
                            'subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'resumed': False
                        },
                        '@type': 'ssl',
                        '@timestamp': '2022-03-16T09:25:40',
                        '@message': '1647422740.1137\tCqU8Sr4elArBGhoYK901\t185.190.24.83\t56578\t172.31.81.98\t3389\t-\t-\t50'
                                    '\tunable to get local issuer certificate\ttrue\t75fb48a465416d66291fb52a733d4787\ttrue'
                                    '\tCN=EC2AMAZ-2GNPPAQ\tTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA'
                                    '\t[FZmVxD29YlmWb7pgg01]\tsecp384r1'
                                    '\tTLS1.0\tbcf3a836c82d12ee988005fb0c011445\tCN=EC2AMAZ-2GNPPAQ\tfalse',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647422740000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-SDDcfgOn5vlEO3XVm',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647422740.113664,
                            'total_client_ciphers': 50,
                            'validation_status': 'unable to get local issuer certificate',
                            'client_hello_seen': True,
                            'ja3_client_fingerprint': '75fb48a465416d66291fb52a733d4787',
                            'source_port': 58866,
                            'dest_port': 3389,
                            'established': True,
                            'source_ip': '185.190.24.90',
                            'issuer': 'CN=EC2AMAZ-2GNPPAQ',
                            'cipher': 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                            'dest_ip': '172.31.81.98',
                            'cert_chain_fuids': 'FLiP5ju2AQMhEjhw201',
                            'curve': 'secp384r1',
                            'uid': 'C3CyxK3OcUn41DqRb401',
                            'version': 'TLS1.0',
                            'ja3s_server_fingerprint': 'bcf3a836c82d12ee988005fb0c011445',
                            'subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'resumed': False
                        },
                        '@type': 'ssl',
                        '@timestamp': '2022-03-16T09:25:40',
                        '@message': '1647422740.1137\tC3CyxK3OcUn41DqRb401\t185.190.24.90\t58866\t172.31.81.98\t3389\t-\t-\t50'
                                    '\tunable to get local issuer certificate\ttrue\t75fb48a465416d66291fb52a733d4787\ttrue'
                                    '\tCN=EC2AMAZ-2GNPPAQ\tTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA'
                                    '\t[FLiP5ju2AQMhEjhw201]\tsecp384r1'
                                    '\tTLS1.0\tbcf3a836c82d12ee988005fb0c011445\tCN=EC2AMAZ-2GNPPAQ\tfalse',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647422740000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-SDDcfgOn5vlEO3XVl',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647422740.113623,
                            'total_client_ciphers': 50,
                            'validation_status': 'unable to get local issuer certificate',
                            'client_hello_seen': True,
                            'ja3_client_fingerprint': '75fb48a465416d66291fb52a733d4787',
                            'source_port': 53279,
                            'dest_port': 3389,
                            'established': True,
                            'source_ip': '185.190.24.90',
                            'issuer': 'CN=EC2AMAZ-2GNPPAQ',
                            'cipher': 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                            'dest_ip': '172.31.81.98',
                            'cert_chain_fuids': 'FxiXK32K0rDJZfDKq401',
                            'curve': 'secp384r1',
                            'uid': 'CtQ0to32uDIULdlVv701',
                            'version': 'TLS1.0',
                            'ja3s_server_fingerprint': 'bcf3a836c82d12ee988005fb0c011445',
                            'subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'resumed': False
                        },
                        '@type': 'ssl',
                        '@timestamp': '2022-03-16T09:25:40',
                        '@message': '1647422740.1136\tCtQ0to32uDIULdlVv701\t185.190.24.90\t53279\t172.31.81.98\t3389\t-\t-\t50'
                                    '\tunable to get local issuer certificate\ttrue\t75fb48a465416d66291fb52a733d4787\ttrue'
                                    '\tCN=EC2AMAZ-2GNPPAQ\tTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA'
                                    '\t[FxiXK32K0rDJZfDKq401]\tsecp384r1'
                                    '\tTLS1.0\tbcf3a836c82d12ee988005fb0c011445\tCN=EC2AMAZ-2GNPPAQ\tfalse',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647422740000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-SDDcfgOn5vlEO3XVW',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647422738.072301,
                            'total_client_ciphers': 50,
                            'validation_status': 'unable to get local issuer certificate',
                            'client_hello_seen': True,
                            'ja3_client_fingerprint': '75fb48a465416d66291fb52a733d4787',
                            'source_port': 56833,
                            'dest_port': 3389,
                            'established': True,
                            'source_ip': '193.93.62.6',
                            'issuer': 'CN=EC2AMAZ-2GNPPAQ',
                            'cipher': 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                            'dest_ip': '172.31.81.98',
                            'cert_chain_fuids': 'FgUQEZ2FZnfrXs9rPb01',
                            'curve': 'secp384r1',
                            'uid': 'CdhdlH163WOfOr8Xwe01',
                            'version': 'TLS1.0',
                            'ja3s_server_fingerprint': 'bcf3a836c82d12ee988005fb0c011445',
                            'subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'resumed': False
                        },
                        '@type': 'ssl',
                        '@timestamp': '2022-03-16T09:25:38',
                        '@message': '1647422738.0723\tCdhdlH163WOfOr8Xwe01\t193.93.62.6\t56833\t172.31.81.98\t3389\t-\t-\t50'
                                    '\tunable to get local issuer certificate\ttrue\t75fb48a465416d66291fb52a733d4787\ttrue'
                                    '\tCN=EC2AMAZ-2GNPPAQ\tTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\t[FgUQEZ2FZnfrXs9rPb01]'
                                    '\tsecp384r1\tTLS1.0\tbcf3a836c82d12ee988005fb0c011445\tCN=EC2AMAZ-2GNPPAQ\tfalse',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647422738000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-SDB-ugOn5vlEO3XVD',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647422732.978413,
                            'total_client_ciphers': 50,
                            'validation_status': 'unable to get local issuer certificate',
                            'client_hello_seen': True,
                            'ja3_client_fingerprint': '75fb48a465416d66291fb52a733d4787',
                            'source_port': 37887,
                            'dest_port': 3389,
                            'established': True,
                            'source_ip': '193.93.62.46',
                            'issuer': 'CN=EC2AMAZ-2GNPPAQ',
                            'cipher': 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                            'dest_ip': '172.31.81.98',
                            'cert_chain_fuids': 'FtGntD1KIjUwvMygVd01',
                            'curve': 'secp384r1',
                            'uid': 'CPbmyW2pzVNNR9wlx101',
                            'version': 'TLS1.0',
                            'ja3s_server_fingerprint': 'bcf3a836c82d12ee988005fb0c011445',
                            'subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'resumed': False
                        },
                        '@type': 'ssl',
                        '@timestamp': '2022-03-16T09:25:32',
                        '@message': '1647422732.9784\tCPbmyW2pzVNNR9wlx101\t193.93.62.46\t37887\t172.31.81.98\t3389\t-\t-\t50'
                                    '\tunable to get local issuer certificate\ttrue\t75fb48a465416d66291fb52a733d4787'
                                    '\ttrue\tCN=EC2AMAZ-2GNPPAQ\tTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\t[FtGntD1KIjUwvMygVd01]'
                                    '\tsecp384r1\tTLS1.0\tbcf3a836c82d12ee988005fb0c011445\tCN=EC2AMAZ-2GNPPAQ\tfalse',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647422732000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-SDB-ugOn5vlEO3XVC',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647422731.961836,
                            'total_client_ciphers': 50,
                            'validation_status': 'unable to get local issuer certificate',
                            'client_hello_seen': True,
                            'ja3_client_fingerprint': '75fb48a465416d66291fb52a733d4787',
                            'source_port': 39982,
                            'dest_port': 3389,
                            'established': True,
                            'source_ip': '193.93.62.35',
                            'issuer': 'CN=EC2AMAZ-2GNPPAQ',
                            'cipher': 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                            'dest_ip': '172.31.81.98',
                            'cert_chain_fuids': 'FBg3ui32csfwxkBb2j01',
                            'curve': 'secp384r1',
                            'uid': 'C64uJw1MXjcYV8zj1g01',
                            'version': 'TLS1.0',
                            'ja3s_server_fingerprint': 'bcf3a836c82d12ee988005fb0c011445',
                            'subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'resumed': False
                        },
                        '@type': 'ssl',
                        '@timestamp': '2022-03-16T09:25:31',
                        '@message': '1647422731.9618\tC64uJw1MXjcYV8zj1g01\t193.93.62.35\t39982\t172.31.81.98\t3389'
                                    '\t-\t-\t50\tunable to get local issuer certificate\ttrue'
                                    '\t75fb48a465416d66291fb52a733d4787\ttrue\tCN=EC2AMAZ-2GNPPAQ'
                                    '\tTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\t[FBg3ui32csfwxkBb2j01]\tsecp384r1\tTLS1.0'
                                    '\tbcf3a836c82d12ee988005fb0c011445\tCN=EC2AMAZ-2GNPPAQ\tfalse',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647422731000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-SDBvFgOn5vlEO3XUq',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647422726.858067,
                            'total_client_ciphers': 50,
                            'validation_status': 'unable to get local issuer certificate',
                            'client_hello_seen': True,
                            'ja3_client_fingerprint': '75fb48a465416d66291fb52a733d4787',
                            'source_port': 11617,
                            'dest_port': 3389,
                            'established': True,
                            'source_ip': '193.93.62.35',
                            'issuer': 'CN=EC2AMAZ-2GNPPAQ',
                            'cipher': 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                            'dest_ip': '172.31.81.98',
                            'cert_chain_fuids': 'FOY49y2sh5FHlARML101',
                            'curve': 'secp384r1',
                            'uid': 'C2MZcQX5FgCL2O2db01',
                            'version': 'TLS1.0',
                            'ja3s_server_fingerprint': 'bcf3a836c82d12ee988005fb0c011445',
                            'subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'resumed': False
                        },
                        '@type': 'ssl',
                        '@timestamp': '2022-03-16T09:25:26',
                        '@message': '1647422726.8581\tC2MZcQX5FgCL2O2db01\t193.93.62.35\t11617\t172.31.81.98\t3389'
                                    '\t-\t-\t50\tunable to get local issuer certificate\ttrue'
                                    '\t75fb48a465416d66291fb52a733d4787\ttrue\tCN=EC2AMAZ-2GNPPAQ'
                                    '\tTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\t[FOY49y2sh5FHlARML101]\tsecp384r1\tTLS1.0'
                                    '\tbcf3a836c82d12ee988005fb0c011445\tCN=EC2AMAZ-2GNPPAQ\tfalse',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647422726000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-SDBvFgOn5vlEO3XUg',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647422724.81939,
                            'total_client_ciphers': 41,
                            'validation_status': 'unable to get local issuer certificate',
                            'client_hello_seen': True,
                            'ja3_client_fingerprint': '43e25370946f1b41b411e6d0bf378456',
                            'source_port': 49524,
                            'dest_port': 3389,
                            'established': True,
                            'source_ip': '142.132.248.164',
                            'issuer': 'CN=EC2AMAZ-2GNPPAQ',
                            'cipher': 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                            'dest_ip': '172.31.81.98',
                            'cert_chain_fuids': 'F9psnH1U2EoRSeoYpa01',
                            'curve': 'secp384r1',
                            'uid': 'C7dKp74oxrH7L2ysmf01',
                            'version': 'TLS1.0',
                            'ja3s_server_fingerprint': 'bcf3a836c82d12ee988005fb0c011445',
                            'subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'resumed': False
                        },
                        '@type': 'ssl',
                        '@timestamp': '2022-03-16T09:25:24',
                        '@message': '1647422724.8194\tC7dKp74oxrH7L2ysmf01\t142.132.248.164\t49524\t172.31.81.98\t3389'
                                    '\t-\t-\t41\tunable to get local issuer certificate\ttrue'
                                    '\t43e25370946f1b41b411e6d0bf378456\ttrue\tCN=EC2AMAZ-2GNPPAQ'
                                    '\tTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\t[F9psnH1U2EoRSeoYpa01]\tsecp384r1'
                                    '\tTLS1.0\tbcf3a836c82d12ee988005fb0c011445\tCN=EC2AMAZ-2GNPPAQ\tfalse',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647422724000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-SC_icgOn5vlEO3XUP',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647422720.739912,
                            'total_client_ciphers': 41,
                            'validation_status': 'unable to get local issuer certificate',
                            'client_hello_seen': True,
                            'ja3_client_fingerprint': '43e25370946f1b41b411e6d0bf378456',
                            'source_port': 55814,
                            'dest_port': 3389,
                            'established': True,
                            'source_ip': '138.122.71.235',
                            'issuer': 'CN=EC2AMAZ-2GNPPAQ',
                            'cipher': 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                            'dest_ip': '172.31.81.98',
                            'cert_chain_fuids': 'FrZAsh3JqdbM3iWdWa01',
                            'curve': 'secp384r1',
                            'uid': 'CnrUm54gPmquymOn2j01',
                            'version': 'TLS1.0',
                            'ja3s_server_fingerprint': 'bcf3a836c82d12ee988005fb0c011445',
                            'subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'resumed': False
                        },
                        '@type': 'ssl',
                        '@timestamp': '2022-03-16T09:25:20',
                        '@message': '1647422720.7399\tCnrUm54gPmquymOn2j01\t138.122.71.235\t55814'
                                    '\t172.31.81.98\t3389\t-\t-\t41'
                                    '\tunable to get local issuer certificate\ttrue\t43e25370946f1b41b411e6d0bf378456\ttrue'
                                    '\tCN=EC2AMAZ-2GNPPAQ\tTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA'
                                    '\t[FrZAsh3JqdbM3iWdWa01]\tsecp384r1'
                                    '\tTLS1.0\tbcf3a836c82d12ee988005fb0c011445\tCN=EC2AMAZ-2GNPPAQ\tfalse',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647422720000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-SC_icgOn5vlEO3XUU',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647422719.716853,
                            'total_client_ciphers': 41,
                            'validation_status': 'unable to get local issuer certificate',
                            'client_hello_seen': True,
                            'ja3_client_fingerprint': '43e25370946f1b41b411e6d0bf378456',
                            'source_port': 61833,
                            'dest_port': 3389,
                            'established': True,
                            'source_ip': '135.181.0.29',
                            'issuer': 'CN=EC2AMAZ-2GNPPAQ',
                            'cipher': 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                            'dest_ip': '172.31.81.98',
                            'cert_chain_fuids': 'FAcAvm360jC7Ac7se701',
                            'curve': 'secp384r1',
                            'uid': 'CECH7vfgwvxcwul8701',
                            'version': 'TLS1.0',
                            'ja3s_server_fingerprint': 'bcf3a836c82d12ee988005fb0c011445',
                            'subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'resumed': False
                        },
                        '@type': 'ssl',
                        '@timestamp': '2022-03-16T09:25:19',
                        '@message': '1647422719.7169\tCECH7vfgwvxcwul8701\t135.181.0.29\t61833\t172.31.81.98\t3389'
                                    '\t-\t-\t41\tunable to get local issuer certificate\ttrue'
                                    '\t43e25370946f1b41b411e6d0bf378456'
                                    '\ttrue\tCN=EC2AMAZ-2GNPPAQ\tTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\t[FAcAvm360jC7Ac7se701]'
                                    '\tsecp384r1\tTLS1.0\tbcf3a836c82d12ee988005fb0c011445\tCN=EC2AMAZ-2GNPPAQ\tfalse',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647422719000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-SC-ErgOn5vlEO3XT3',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647422714.64765,
                            'total_client_ciphers': 41,
                            'validation_status': 'unable to get local issuer certificate',
                            'client_hello_seen': True,
                            'ja3_client_fingerprint': '43e25370946f1b41b411e6d0bf378456',
                            'source_port': 58733,
                            'dest_port': 3389,
                            'established': True,
                            'source_ip': '142.132.248.164',
                            'issuer': 'CN=EC2AMAZ-2GNPPAQ',
                            'cipher': 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                            'dest_ip': '172.31.81.98',
                            'cert_chain_fuids': 'FW0W4b12P2dPJ2sc2701',
                            'curve': 'secp384r1',
                            'uid': 'CQnwKr2jeaHj3XFyv301',
                            'version': 'TLS1.0',
                            'ja3s_server_fingerprint': 'bcf3a836c82d12ee988005fb0c011445',
                            'subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'resumed': False
                        },
                        '@type': 'ssl',
                        '@timestamp': '2022-03-16T09:25:14',
                        '@message': '1647422714.6477\tCQnwKr2jeaHj3XFyv301\t142.132.248.164\t58733\t172.31.81.98\t3389'
                                    '\t-\t-\t41\tunable to get local issuer certificate\ttrue'
                                    '\t43e25370946f1b41b411e6d0bf378456'
                                    '\ttrue\tCN=EC2AMAZ-2GNPPAQ\tTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\t[FW0W4b12P2dPJ2sc2701]'
                                    '\tsecp384r1\tTLS1.0\tbcf3a836c82d12ee988005fb0c011445\tCN=EC2AMAZ-2GNPPAQ\tfalse',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647422714000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-SC-ErgOn5vlEO3XT1',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647422713.62296,
                            'total_client_ciphers': 50,
                            'validation_status': 'unable to get local issuer certificate',
                            'client_hello_seen': True,
                            'ja3_client_fingerprint': '75fb48a465416d66291fb52a733d4787',
                            'source_port': 53762,
                            'dest_port': 3389,
                            'established': True,
                            'source_ip': '193.93.62.10',
                            'issuer': 'CN=EC2AMAZ-2GNPPAQ',
                            'cipher': 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                            'dest_ip': '172.31.81.98',
                            'cert_chain_fuids': 'FNekFq3Ap1Is0wwop501',
                            'curve': 'secp384r1',
                            'uid': 'C7uh1sun4PkLQVycl01',
                            'version': 'TLS1.0',
                            'ja3s_server_fingerprint': 'bcf3a836c82d12ee988005fb0c011445',
                            'subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'resumed': False
                        },
                        '@type': 'ssl',
                        '@timestamp': '2022-03-16T09:25:13',
                        '@message': '1647422713.623\tC7uh1sun4PkLQVycl01\t193.93.62.10\t53762\t172.31.81.98\t3389'
                                    '\t-\t-\t50\tunable to get local issuer certificate\ttrue'
                                    '\t75fb48a465416d66291fb52a733d4787'
                                    '\ttrue\tCN=EC2AMAZ-2GNPPAQ\tTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\t[FNekFq3Ap1Is0wwop501]'
                                    '\tsecp384r1\tTLS1.0\tbcf3a836c82d12ee988005fb0c011445\tCN=EC2AMAZ-2GNPPAQ\tfalse',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647422713000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-SC-ErgOn5vlEO3XTu',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647422711.572542,
                            'total_client_ciphers': 50,
                            'validation_status': 'unable to get local issuer certificate',
                            'client_hello_seen': True,
                            'ja3_client_fingerprint': '75fb48a465416d66291fb52a733d4787',
                            'source_port': 36335,
                            'dest_port': 3389,
                            'established': True,
                            'source_ip': '193.93.62.101',
                            'issuer': 'CN=EC2AMAZ-2GNPPAQ',
                            'cipher': 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                            'dest_ip': '172.31.81.98',
                            'cert_chain_fuids': 'F7ppn63i9WnISZgWFk01',
                            'curve': 'secp384r1',
                            'uid': 'ChPG9O30D5Q06GBMTf01',
                            'version': 'TLS1.0',
                            'ja3s_server_fingerprint': 'bcf3a836c82d12ee988005fb0c011445',
                            'subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'resumed': False
                        },
                        '@type': 'ssl',
                        '@timestamp': '2022-03-16T09:25:11',
                        '@message': '1647422711.5725\tChPG9O30D5Q06GBMTf01\t193.93.62.101\t36335\t172.31.81.98'
                                    '\t3389\t-\t-\t50\tunable to get local issuer certificate\ttrue'
                                    '\t75fb48a465416d66291fb52a733d4787\ttrue\tCN=EC2AMAZ-2GNPPAQ'
                                    '\tTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\t[F7ppn63i9WnISZgWFk01]'
                                    '\tsecp384r1\tTLS1.0\tbcf3a836c82d12ee988005fb0c011445\tCN=EC2AMAZ-2GNPPAQ'
                                    '\tfalse',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647422711000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-SC74AgOn5vlEO3XTX',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647422704.430529,
                            'total_client_ciphers': 50,
                            'validation_status': 'unable to get local issuer certificate',
                            'client_hello_seen': True,
                            'ja3_client_fingerprint': '75fb48a465416d66291fb52a733d4787',
                            'source_port': 58722,
                            'dest_port': 3389,
                            'established': True,
                            'source_ip': '193.93.62.23',
                            'issuer': 'CN=EC2AMAZ-2GNPPAQ',
                            'cipher': 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                            'dest_ip': '172.31.81.98',
                            'cert_chain_fuids': 'FZXTJhEK2qXFehfWf01',
                            'curve': 'secp384r1',
                            'uid': 'CJ0GENWzwPtp9Vo6701',
                            'version': 'TLS1.0',
                            'ja3s_server_fingerprint': 'bcf3a836c82d12ee988005fb0c011445',
                            'subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'resumed': False
                        },
                        '@type': 'ssl',
                        '@timestamp': '2022-03-16T09:25:04',
                        '@message': '1647422704.4305\tCJ0GENWzwPtp9Vo6701\t193.93.62.23\t58722\t172.31.81.98'
                                    '\t3389\t-\t-\t50\tunable to get local issuer certificate\ttrue'
                                    '\t75fb48a465416d66291fb52a733d4787\ttrue\tCN=EC2AMAZ-2GNPPAQ'
                                    '\tTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\t[FZXTJhEK2qXFehfWf01]'
                                    '\tsecp384r1\tTLS1.0\tbcf3a836c82d12ee988005fb0c011445\tCN=EC2AMAZ-2GNPPAQ'
                                    '\tfalse',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647422704000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-SC6KmgOn5vlEO3XTA',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647422699.327037,
                            'total_client_ciphers': 55,
                            'validation_status': 'unable to get local issuer certificate',
                            'client_hello_seen': True,
                            'ja3_client_fingerprint': '0b63812a99e66c82a20d30c3b9ba6e06',
                            'source_port': 41080,
                            'dest_port': 3389,
                            'established': True,
                            'source_ip': '79.124.62.201',
                            'issuer': 'CN=EC2AMAZ-2GNPPAQ',
                            'cipher': 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                            'dest_ip': '172.31.81.98',
                            'cert_chain_fuids': 'FuP9ykK3cRL9hoGX901',
                            'curve': 'secp384r1',
                            'uid': 'CzuOM7106ITZwezgb501',
                            'version': 'TLS1.0',
                            'ja3s_server_fingerprint': 'bcf3a836c82d12ee988005fb0c011445',
                            'subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'resumed': False
                        },
                        '@type': 'ssl',
                        '@timestamp': '2022-03-16T09:24:59',
                        '@message': '1647422699.327\tCzuOM7106ITZwezgb501\t79.124.62.201\t41080\t172.31.81.98\t3389'
                                    '\t-\t-\t55\tunable to get local issuer certificate\ttrue'
                                    '\t0b63812a99e66c82a20d30c3b9ba6e06'
                                    '\ttrue\tCN=EC2AMAZ-2GNPPAQ\tTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\t[FuP9ykK3cRL9hoGX901]'
                                    '\tsecp384r1\tTLS1.0\tbcf3a836c82d12ee988005fb0c011445\tCN=EC2AMAZ-2GNPPAQ\tfalse',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647422699000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-SC563gOn5vlEO3XS1',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647422696.263117,
                            'total_client_ciphers': 50,
                            'validation_status': 'unable to get local issuer certificate',
                            'client_hello_seen': True,
                            'ja3_client_fingerprint': '75fb48a465416d66291fb52a733d4787',
                            'source_port': 55752,
                            'dest_port': 3389,
                            'established': True,
                            'source_ip': '185.190.24.86',
                            'issuer': 'CN=EC2AMAZ-2GNPPAQ',
                            'cipher': 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                            'dest_ip': '172.31.81.98',
                            'cert_chain_fuids': 'FheQTw10eAKdDrN4Ff01',
                            'curve': 'secp384r1',
                            'uid': 'CaEhdI1SpZBPadiGt801',
                            'version': 'TLS1.0',
                            'ja3s_server_fingerprint': 'bcf3a836c82d12ee988005fb0c011445',
                            'subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'resumed': False
                        },
                        '@type': 'ssl',
                        '@timestamp': '2022-03-16T09:24:56',
                        '@message': '1647422696.2631\tCaEhdI1SpZBPadiGt801\t185.190.24.86\t55752\t172.31.81.98\t3389'
                                    '\t-\t-\t50\tunable to get local issuer certificate\ttrue'
                                    '\t75fb48a465416d66291fb52a733d4787\ttrue\tCN=EC2AMAZ-2GNPPAQ'
                                    '\tTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\t[FheQTw10eAKdDrN4Ff01]'
                                    '\tsecp384r1\tTLS1.0\tbcf3a836c82d12ee988005fb0c011445\tCN=EC2AMAZ-2GNPPAQ\tfalse',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647422696000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-SC563gOn5vlEO3XSt',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647422692.193503,
                            'total_client_ciphers': 50,
                            'validation_status': 'unable to get local issuer certificate',
                            'client_hello_seen': True,
                            'ja3_client_fingerprint': '75fb48a465416d66291fb52a733d4787',
                            'source_port': 51491,
                            'dest_port': 3389,
                            'established': True,
                            'source_ip': '193.93.62.23',
                            'issuer': 'CN=EC2AMAZ-2GNPPAQ',
                            'cipher': 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                            'dest_ip': '172.31.81.98',
                            'cert_chain_fuids': 'F84qdd3rHYTIsZdWte01',
                            'curve': 'secp384r1',
                            'uid': 'C824rv1rPuHK7YZhla01',
                            'version': 'TLS1.0',
                            'ja3s_server_fingerprint': 'bcf3a836c82d12ee988005fb0c011445',
                            'subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'resumed': False
                        },
                        '@type': 'ssl',
                        '@timestamp': '2022-03-16T09:24:52',
                        '@message': '1647422692.1935\tC824rv1rPuHK7YZhla01\t193.93.62.23\t51491\t172.31.81.98'
                                    '\t3389\t-\t-\t50\tunable to get local issuer certificate\ttrue'
                                    '\t75fb48a465416d66291fb52a733d4787\ttrue\tCN=EC2AMAZ-2GNPPAQ'
                                    '\tTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\t[F84qdd3rHYTIsZdWte01]'
                                    '\tsecp384r1\tTLS1.0\tbcf3a836c82d12ee988005fb0c011445\tCN=EC2AMAZ-2GNPPAQ\tfalse',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647422692000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-SC0jAgOn5vlEO3XR4',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647422673.884023,
                            'total_client_ciphers': 50,
                            'validation_status': 'unable to get local issuer certificate',
                            'client_hello_seen': True,
                            'ja3_client_fingerprint': '75fb48a465416d66291fb52a733d4787',
                            'source_port': 25870,
                            'dest_port': 3389,
                            'established': True,
                            'source_ip': '193.93.62.91',
                            'issuer': 'CN=EC2AMAZ-2GNPPAQ',
                            'cipher': 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                            'dest_ip': '172.31.81.98',
                            'cert_chain_fuids': 'Fh49iM3r9HpesBuJmi01',
                            'curve': 'secp384r1',
                            'uid': 'CdkpnG3wiwkiq6owH401',
                            'version': 'TLS1.0',
                            'ja3s_server_fingerprint': 'bcf3a836c82d12ee988005fb0c011445',
                            'subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'resumed': False
                        },
                        '@type': 'ssl',
                        '@timestamp': '2022-03-16T09:24:33',
                        '@message': '1647422673.884\tCdkpnG3wiwkiq6owH401\t193.93.62.91\t25870\t172.31.81.98\t3389\t-\t-\t50'
                                    '\tunable to get local issuer certificate\ttrue\t75fb48a465416d66291fb52a733d4787\ttrue'
                                    '\tCN=EC2AMAZ-2GNPPAQ\tTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\t[Fh49iM3r9HpesBuJmi01]'
                                    '\tsecp384r1\tTLS1.0\tbcf3a836c82d12ee988005fb0c011445\tCN=EC2AMAZ-2GNPPAQ\tfalse',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647422673000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-SC0TXgOn5vlEO3XRm',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647422669.823534,
                            'total_client_ciphers': 50,
                            'validation_status': 'unable to get local issuer certificate',
                            'client_hello_seen': True,
                            'ja3_client_fingerprint': '75fb48a465416d66291fb52a733d4787',
                            'source_port': 15522,
                            'dest_port': 3389,
                            'established': True,
                            'source_ip': '193.93.62.33',
                            'issuer': 'CN=EC2AMAZ-2GNPPAQ',
                            'cipher': 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                            'dest_ip': '172.31.81.98',
                            'cert_chain_fuids': 'FNhKcd4j9bSuV2HLM201',
                            'curve': 'secp384r1',
                            'uid': 'Cs0ihL1fgDqEwKOw4201',
                            'version': 'TLS1.0',
                            'ja3s_server_fingerprint': 'bcf3a836c82d12ee988005fb0c011445',
                            'subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'resumed': False
                        },
                        '@type': 'ssl',
                        '@timestamp': '2022-03-16T09:24:29',
                        '@message': '1647422669.8235\tCs0ihL1fgDqEwKOw4201\t193.93.62.33\t15522\t172.31.81.98\t3389'
                                    '\t-\t-\t50\tunable to get local issuer certificate'
                                    '\ttrue\t75fb48a465416d66291fb52a733d4787'
                                    '\ttrue\tCN=EC2AMAZ-2GNPPAQ\tTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\t[FNhKcd4j9bSuV2HLM201]'
                                    '\tsecp384r1\tTLS1.0\tbcf3a836c82d12ee988005fb0c011445\tCN=EC2AMAZ-2GNPPAQ\tfalse',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647422669000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-SCyWWgOn5vlEO3XRT',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647422664.736282,
                            'total_client_ciphers': 41,
                            'validation_status': 'unable to get local issuer certificate',
                            'client_hello_seen': True,
                            'ja3_client_fingerprint': '43e25370946f1b41b411e6d0bf378456',
                            'source_port': 62401,
                            'dest_port': 3389,
                            'established': True,
                            'source_ip': '142.132.248.164',
                            'issuer': 'CN=EC2AMAZ-2GNPPAQ',
                            'cipher': 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                            'dest_ip': '172.31.81.98',
                            'cert_chain_fuids': 'F2RMhV19f6OPxHVUT01',
                            'curve': 'secp384r1',
                            'uid': 'CgBRPsJvpGqoQppnf01',
                            'version': 'TLS1.0',
                            'ja3s_server_fingerprint': 'bcf3a836c82d12ee988005fb0c011445',
                            'subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'resumed': False
                        },
                        '@type': 'ssl',
                        '@timestamp': '2022-03-16T09:24:24',
                        '@message': '1647422664.7363\tCgBRPsJvpGqoQppnf01\t142.132.248.164\t62401\t172.31.81.98\t3389'
                                    '\t-\t-\t41\tunable to get local issuer certificate\ttrue'
                                    '\t43e25370946f1b41b411e6d0bf378456'
                                    '\ttrue\tCN=EC2AMAZ-2GNPPAQ\tTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\t[F2RMhV19f6OPxHVUT01]'
                                    '\tsecp384r1\tTLS1.0\tbcf3a836c82d12ee988005fb0c011445\tCN=EC2AMAZ-2GNPPAQ\tfalse',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647422664000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-SCyWWgOn5vlEO3XRS',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647422662.713172,
                            'total_client_ciphers': 50,
                            'validation_status': 'unable to get local issuer certificate',
                            'client_hello_seen': True,
                            'ja3_client_fingerprint': '75fb48a465416d66291fb52a733d4787',
                            'source_port': 55848,
                            'dest_port': 3389,
                            'established': True,
                            'source_ip': '193.93.62.11',
                            'issuer': 'CN=EC2AMAZ-2GNPPAQ',
                            'cipher': 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                            'dest_ip': '172.31.81.98',
                            'cert_chain_fuids': 'FoX7VB44dZGRFss0G201',
                            'curve': 'secp384r1',
                            'uid': 'C7tQVd4aJ1aVlOiTP301',
                            'version': 'TLS1.0',
                            'ja3s_server_fingerprint': 'bcf3a836c82d12ee988005fb0c011445',
                            'subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'resumed': False
                        },
                        '@type': 'ssl',
                        '@timestamp': '2022-03-16T09:24:22',
                        '@message': '1647422662.7132\tC7tQVd4aJ1aVlOiTP301\t193.93.62.11\t55848\t172.31.81.98\t3389'
                                    '\t-\t-\t50\tunable to get local issuer certificate\ttrue'
                                    '\t75fb48a465416d66291fb52a733d4787'
                                    '\ttrue\tCN=EC2AMAZ-2GNPPAQ\tTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\t[FoX7VB44dZGRFss0G201]'
                                    '\tsecp384r1\tTLS1.0\tbcf3a836c82d12ee988005fb0c011445\tCN=EC2AMAZ-2GNPPAQ\tfalse',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647422662000]
                }, {
                    '_index': 'logstash-vmprobe-2022.03.16',
                    '_type': 'doc',
                    '_id': 'AX-SCwo9gOn5vlEO3XRJ',
                    '_score': None,
                    '_source': {
                        '@fields': {
                            'epochdate': 1647422661.693776,
                            'total_client_ciphers': 41,
                            'validation_status': 'unable to get local issuer certificate',
                            'client_hello_seen': True,
                            'ja3_client_fingerprint': '43e25370946f1b41b411e6d0bf378456',
                            'source_port': 57635,
                            'dest_port': 3389,
                            'established': True,
                            'source_ip': '135.181.0.29',
                            'issuer': 'CN=EC2AMAZ-2GNPPAQ',
                            'cipher': 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                            'dest_ip': '172.31.81.98',
                            'cert_chain_fuids': 'FKFYDd2zkrNkhBsJu301',
                            'curve': 'secp384r1',
                            'uid': 'CIIe7Q1dyfRzssO89601',
                            'version': 'TLS1.0',
                            'ja3s_server_fingerprint': 'bcf3a836c82d12ee988005fb0c011445',
                            'subject': 'CN=EC2AMAZ-2GNPPAQ',
                            'resumed': False
                        },
                        '@type': 'ssl',
                        '@timestamp': '2022-03-16T09:24:21',
                        '@message': '1647422661.6938\tCIIe7Q1dyfRzssO89601\t135.181.0.29\t57635\t172.31.81.98\t3389'
                                    '\t-\t-\t41\tunable to get local issuer certificate\ttrue'
                                    '\t43e25370946f1b41b411e6d0bf378456'
                                    '\ttrue\tCN=EC2AMAZ-2GNPPAQ\tTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\t[FKFYDd2zkrNkhBsJu301]'
                                    '\tsecp384r1'
                                    '\tTLS1.0\tbcf3a836c82d12ee988005fb0c011445\tCN=EC2AMAZ-2GNPPAQ\tfalse',
                        '@darktrace_probe': '1'
                    },
                    'sort': [1647422661000]
                }]
            },
            'darktraceChildError': '',
            'kibana': {
                'index': ['logstash-darktrace-2022.03.16'],
                'per_page': 50,
                'time': {
                    'from': '2022-03-16T09:23:20.894Z',
                    'to': '2022-03-16T09:28:20.894Z'
                },
                'default_fields': ['@type', '@message']
            }
        })
        mock_results_response.return_value = DarktraceMockResponse(200, mock_response_dict)
        # result_data = {}
        query = json.dumps({
            "queries": [
                "{\"search\": \"(((@fields.query:pop.gmail.com) OR (@fields.cipher:TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA))"
                " AND (@fields.epochdate:>1647422600.894 AND @fields.epochdate:<1647422900.894))\", "
                "\"fields\": [], \"timeframe\": \"custom\", \"time\": {\"from\": \"2022-03-16T09:23:20.894000Z\", "
                "\"to\": \"2022-03-16T09:28:20.894000Z\"}}"
            ]})
        offset = 0
        length = 1
        transmission = stix_transmission.StixTransmission('darktrace', self.connection(), self.config())
        results_response = transmission.results(query, offset, length)
        assert results_response is not None
        assert results_response['success'] is True
        assert 'data' in results_response
        assert len(results_response['data']) > 0

    @patch('stix_shifter_modules.darktrace.stix_transmission.api_client.APIClient.get_search_results')
    def test_invalid_auth(self, mock_results_response):
        mock_response_dict = json.dumps({'error': 'Invalid Authentication'})
        mock_results_response.return_value = DarktraceMockResponse(400, mock_response_dict)

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
        mock_results_response.return_value = DarktraceMockResponse(200, mock_response_dict)

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
        mock_results_response.return_value = DarktraceMockResponse(500, mock_response_dict)

        query = json.dumps({"queries": ["{\"search\": \"(@fields.query:pop.gmail.com)\", \"fields\": [], \"timeframe\":"
                                        " \"custom\", \"time\": {\"from\": \"2022-03-16T09:23:20.894000Z\", "
                                        "\"to\": \"2022-03-16T09:28:20.894000Z\"}}"]})

        query = {'queries': []}
        transmission = stix_transmission.StixTransmission('darktrace', self.connection(), self.config())
        results_response = transmission.results(query, 0, 1)
        assert results_response is not None
        assert results_response['success'] is False

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_service_unavailable(self, mock_ping):

        mock_ping.side_effect = ConnectionError("Invalid Host")
        query = json.dumps({"queries": ["{\"search\": \"(@fields.query:pop.gmail.com)\", \"fields\": [], \"timeframe\":"
                                        " \"custom\", \"time\": {\"from\": \"2022-03-16T09:23:20.894000Z\", "
                                        "\"to\": \"2022-03-16T09:28:20.894000Z\"}}"]})

        transmission = stix_transmission.StixTransmission('darktrace', self.connection(), self.config())
        results_response = transmission.results(query, 0, 1)
        assert results_response is not None
        assert results_response['success'] is False
        assert results_response['code'] == 'service_unavailable'

    @patch('stix_shifter_modules.darktrace.stix_transmission.api_client.APIClient.ping_box')
    def test_ping_invalid_auth(self, mock_results_response):
        error = json.dumps({'error': 'Invalid Authentication'})
        pingmock = InnerResponse(400, error)
        pingresponse = PingResponse(pingmock)
        mock_results_response.return_value = pingresponse

        transmission = stix_transmission.StixTransmission('darktrace', self.connection(), self.config())
        results_response = transmission.ping()

        assert results_response is not None
        assert results_response['success'] is False
        assert results_response['code'] == 'authentication_fail'

    @patch('stix_shifter_modules.darktrace.stix_transmission.api_client.APIClient.ping_box')
    def test_ping_invalid_args(self, mock_results_response):
        error = json.dumps({'error': 'Invalid to/from fields in custom range'})
        pingmock = InnerResponse(200, error)
        pingresponse = PingResponse(pingmock)
        mock_results_response.return_value = pingresponse

        transmission = stix_transmission.StixTransmission('darktrace', self.connection(), self.config())
        results_response = transmission.ping()

        assert results_response is not None
        assert results_response['success'] is False
        assert 'Invalid to/from fields in custom range' in results_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_ping_service_unavailable(self, mock_ping):
        mock_ping.side_effect = ConnectionError("Invalid Host")
        transmission = stix_transmission.StixTransmission('darktrace', self.connection(), self.config())
        results_response = transmission.ping()
        assert results_response is not None
        assert results_response['success'] is False
        assert results_response['code'] == 'service_unavailable'

    @patch('stix_shifter_modules.darktrace.stix_transmission.api_client.APIClient.ping_box')
    def test_ping_connection_error(self, mock_results_response):
        mock_results_response.return_value = DarktraceMockResponse(500, '')
        transmission = stix_transmission.StixTransmission('darktrace', self.connection(), self.config())
        results_response = transmission.ping()

        assert results_response is not None
        assert results_response['success'] is False
