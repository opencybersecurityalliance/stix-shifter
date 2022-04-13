from unittest.mock import patch
import unittest
import json
from stix_shifter_modules.darktrace.stix_transmission.api_client import APIClient
from stix_shifter.stix_transmission import stix_transmission


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

        transmission = stix_transmission. \
            StixTransmission('darktrace', self.connection(), self.config())
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert query_response['search_id'] is not None
        assert query_response['search_id'] == query

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
