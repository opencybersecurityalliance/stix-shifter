import json
from stix_shifter_modules.arcsight.entry_point import EntryPoint
from stix_shifter.stix_transmission import stix_transmission
from tests.utils.async_utils import get_mock_response
from unittest.mock import patch
from unittest import TestCase

CONFIG = {
    "auth": {
        "login": "abc",
        "password": "xyz"
    }
}

CONNECTION = {
    "host": "logger_host",
    "port": 443,
    "selfSignedCert": "cert"
}

SEARCH_ID = "1594383044445:e929MKkCf6i7ngBa3laxFFUJIZtfXINHULlc0oiE6RA."


class TestArcsightConnection(TestCase):
    @staticmethod
    def test_is_async():
        """to check connector is async"""
        entry_point = EntryPoint(CONNECTION, CONFIG)
        check_async = entry_point.is_async()
        assert check_async

    @staticmethod
    @patch('stix_shifter_modules.arcsight.stix_transmission.api_client.APIClient.ping_data_source', autospec=True)
    def test_ping(mock_ping):
        """to check the ping status of connector"""
        mock_ping.return_value = get_mock_response(200, '{"sessionId":"2"}', 'byte')
        transmission = stix_transmission.StixTransmission('arcsight', CONNECTION, CONFIG)
        ping_response = transmission.ping()

        assert ping_response is not None
        assert 'success' in ping_response
        assert ping_response['success'] is True

    @staticmethod
    @patch('stix_shifter_modules.arcsight.stix_transmission.api_client.APIClient.ping_data_source', autospec=True)
    def test_ping_exception(mock_ping):
        """to check the ping exception of the connector"""
        mock_ping.return_value = get_mock_response(400, '{"errors": [{"code": 1009, "message": "Server session not '
                                                       'found"}]}', 'byte')
        transmission = stix_transmission.StixTransmission('arcsight', CONNECTION, CONFIG)
        ping_response = transmission.ping()
        
        assert ping_response is not None
        assert 'success' in ping_response
        assert ping_response['success'] is False
        assert 'error' in ping_response
        assert ping_response['code'] == 'service_unavailable'

    @staticmethod
    @patch('stix_shifter_modules.arcsight.stix_transmission.api_client.APIClient.ping_data_source', autospec=True)
    def test_auth_exception(mock_ping):
        """to check auth token generation exception"""
        mock_ping.return_value = get_mock_response(503, '{"error": "Unauthorized"}', 'byte')
        transmission = stix_transmission.StixTransmission('arcsight', CONNECTION, CONFIG)
        ping_response = transmission.ping()

        assert ping_response is not None
        assert 'success' in ping_response
        assert ping_response['success'] is False
        assert 'error' in ping_response
        assert ping_response['code'] == 'authentication_fail'

    @staticmethod
    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api', autospec=True)
    @patch('stix_shifter_modules.arcsight.stix_transmission.api_client.APIClient.get_user_session_id')
    def test_create_query_connection(mock_session_id, mock_query_res):
        """to create the query search and get search id"""
        mock_session_id.return_value = 'Dhoup23b3wL7tBlWWIeFPg8JHEf29qD1tNRJba4Jsyg.'
        mock_query_res.return_value = get_mock_response(200, '{"sessionId":"2"}', 'byte')
        query = "{\"query\": \"destinationPort = 22\", \"start_time\": \"2020-06-0111:20:20.000-05:00\", " \
                "\"end_time\": \"2020-07-01T12:00:44.000-05:00\"}"
        transmission = stix_transmission.StixTransmission('arcsight', CONNECTION, CONFIG)
        query_response = transmission.query(query)

        assert query_response is not None
        assert 'success' in query_response
        assert query_response['success'] is True
        assert 'search_id' in query_response

    @staticmethod
    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api', autospec=True)
    @patch('stix_shifter_modules.arcsight.stix_transmission.api_client.APIClient.get_user_session_id')
    def test_create_query_error(mock_session_id, mock_query_res):
        """query search error check"""
        mock_session_id.return_value = 'Dhoup23b3wL7tBlWWIeFPg8JHEf29qD1tNRJba4Jsyg.'
        mock_query_res.return_value = get_mock_response(400, '{"errors": [{"code": 1111, '
                                                                '"message": "Starting time '
                                                                '2020-06-0111:20:20.000-05:00 format is wrong"}]}', 'byte')
        query = "{\"query\": \"destinationPort = 22\", \"start_time\": \"2020-06-0111:20:20.000-05:00\", " \
                "\"end_time\": \"2020-07-01T12:00:44.000-05:00\"}"
        transmission = stix_transmission.StixTransmission('arcsight', CONNECTION, CONFIG)
        query_response = transmission.query(query)

        assert query_response is not None
        assert 'success' in query_response
        assert query_response['success'] is False
        assert 'error' in query_response
        assert query_response['code'] == "invalid_query"

    @staticmethod
    @patch('stix_shifter_modules.arcsight.stix_transmission.api_client.APIClient.create_search')
    def test_create_query_exception(mock_query_exception):
        """query search exception handling"""
        mock_query_exception.side_effect = ConnectionError(
            "('Connection aborted.', ConnectionResetError(10054, 'An existing "
            "connection was forcibly closed by the remote host', None, 10054, "
            "None))")
        query = "{\"query\": \"destinationPort = 22\", \"start_time\": \"2020-06-0111:20:20.000-05:00\", " \
                "\"end_time\": \"2020-07-01T12:00:44.000-05:00\"}"
        transmission = stix_transmission.StixTransmission('arcsight', CONNECTION, CONFIG)
        query_response = transmission.query(query)

        assert query_response is not None
        assert 'success' in query_response
        assert query_response['success'] is False
        assert 'error' in query_response
        assert query_response['code'] == 'service_unavailable'

    @staticmethod
    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_create_results(mock_create_results):
        """to get the search results"""
        response = {
            "fields": [{
                "name": "_rowId",
                "type": "string",
            }, {
                "name": "Event Time",
                "type": "date",
            }, {
                "name": "destinationProcessName",
                "type": "string",
            }, {
                "name": "applicationProtocol",
                "type": "string",
            }, {
                "name": "destinationPort",
                "type": "number",
            }, {
                "name": "transportProtocol",
                "type": "string",
            }, {
                "name": "destinationHostName",
                "type": "string",
            }, {
                "name": "fileHash",
                "type": "string",
            }, {
                "name": "message",
                "type": "string",
            }, {
                "name": "filePath",
                "type": "string",
            }, {
                "name": "spid",
                "type": "string",
            }
            ],
            "results": [
                ["189D1-2@Local", 1592820270803, "/usr/sbin/sshd", "http", 22,
                 "TCP", "ip-172-31-66-30.ec2.internal", "MD5=B66E3F36EDD5E0AC620C8FD08C55C0E1,"
                                                        "SHA256=B66D93926841E798F5AE1EF97158E74"
                                                        "D79263745C81501BF342AA9D0672419D8,"
                                                        "SHA1=4311466C7618176E1C51E56D8692E08E",
                 ' pid=20103 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:sshd_t:s0-s0:c0.c1023 '
                 'msg=\'op=start direction=from-client cipher=aes128-gcm@openssh.com ksize=128 mac= '
                 'pfs=curve25519-sha256@libssh.org ppid=20116 suid=74 rport=55804 laddr=172.31.66.30 lport=22  '
                 'exe="/usr/sbin/sshd" hostname=? addr=209.141.40.12 terminal=? res=success\'',
                 "C:\\Program Files\\ArcSightSmartConnectors\\current\\", "20103"
                 ]
            ]
        }
        mock_create_results.return_value = get_mock_response(200, json.dumps(response), 'byte')
        search_id = '1594383044445:e929MKkCf6i7ngBa3laxFFUJIZtfXINHULlc0oiE6RA.'
        offset = 0
        length = 10
        transmission = stix_transmission.StixTransmission('arcsight', CONNECTION, CONFIG)
        results_response = transmission.results(search_id, offset, length)

        assert results_response is not None
        assert 'success' in results_response
        assert results_response['success'] is True
        assert 'data' in results_response

    @staticmethod
    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_create_results_registry(mock_create_results):
        """to get search result with registry - connector specific"""
        response = {
            "fields": [{
                "name": "_rowId",
                "type": "string",
            }, {
                "name": "Event Time",
                "type": "date",
            }, {
                "name": "destinationPort",
                "type": "number",
            }, {
                "name": "transportProtocol",
                "type": "string",
            }, {
                "name": "destinationHostName",
                "type": "string",
            }, {
                "name": "deviceAction",
                "type": "string",
            }, {
                "name": "filePath",
                "type": "string",
            }, {
                'name': 'deviceProduct',
                'type': 'string',
            }, {
                'name': 'deviceCustomString4',
                'type': 'string'
            }, {
                'name': 'destinationMacAddress',
                'type': 'string'
            }, {
                'name': 'sourceMacAddress',
                'type': 'string'
            }],
            "results": [
                ["189D1-2@Local", 1592820270890, 22, "TCP", "ip-172-31-66-30.ec2.internal", "Registry value set",
                 "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Print\\Printers\\Microsoft XPS Document "
                 "Writer (redirected 2),1\\DsDriver\\driverVersion", "Sysmon", "DWORD (0x00000401)",
                 '00-0B-46-A8-98-81', '00-D0-09-D6-73-E9'
                 ]]}
        mock_create_results.return_value = get_mock_response(200, json.dumps(response), 'byte')
        search_id = '1594383044445:e929MKkCf6i7ngBa3laxFFUJIZtfXINHULlc0oiE6RA.'
        offset = 0
        length = 10
        transmission = stix_transmission.StixTransmission('arcsight', CONNECTION, CONFIG)
        results_response = transmission.results(search_id, offset, length)

        assert results_response is not None
        assert 'success' in results_response
        assert results_response['success'] is True
        assert 'data' in results_response

    @staticmethod
    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_create_results_empty(mock_create_results):
        """to get query results with empty response"""
        response = {}
        mock_create_results.return_value = get_mock_response(200, json.dumps(response), 'byte')
        search_id = '1594383044445:e929MKkCf6i7ngBa3laxFFUJIZtfXINHULlc0oiE6RA.:10'
        offset = 0
        length = 10
        transmission = stix_transmission.StixTransmission('arcsight', CONNECTION, CONFIG)
        results_response = transmission.results(search_id, offset, length)

        assert results_response is not None
        assert 'success' in results_response
        assert results_response['success'] is True
        assert 'data' in results_response

    @staticmethod
    @patch('stix_shifter_modules.arcsight.stix_transmission.api_client.APIClient.get_search_results')
    def test_create_results_exception(mock_create_results):
        """to get http exception in result search"""
        mock_create_results.side_effect = ConnectionError(
            "('Connection aborted.', ConnectionResetError(10054, 'An existing "
            "connection was forcibly closed by the remote host', None, 10054, "
            "None))")
        offset = 10
        length = 10000
        transmission = stix_transmission.StixTransmission('arcsight', CONNECTION, CONFIG)
        results_response = transmission.results(SEARCH_ID, offset, length)

        assert results_response is not None
        assert 'success' in results_response
        assert results_response['success'] is False
        assert 'error' in results_response
        assert results_response['code'] == 'service_unavailable'

    @staticmethod
    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_result_error(mock_delete_error):
        """to get error in result search"""
        error = {"errors": [{'code': 1009, 'message': 'Server session not found'}]}
        mock_delete_error.return_value = get_mock_response(400, json.dumps(error), 'byte')
        search_id = "1594383044445:BCP7NIkbiLBkXx2FwdkU7ma9O7bJAWng1k.:20"
        transmission = stix_transmission.StixTransmission('arcsight', CONNECTION, CONFIG)
        result_response = transmission.results(search_id, 0, 100)
        assert result_response is not None
        assert 'success' in result_response
        assert result_response['success'] is False
        assert 'error' in result_response
        assert result_response['code'] == 'service_unavailable'

    @staticmethod
    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_delete_query_connection(mock_delete_query):
        """to delete the query search using search id"""
        mock_delete_query.return_value = get_mock_response(200, "", 'byte')
        transmission = stix_transmission.StixTransmission('arcsight', CONNECTION, CONFIG)
        delete_response = transmission.delete(SEARCH_ID)

        assert delete_response is not None
        assert 'success' in delete_response
        assert delete_response['success'] is True

    @staticmethod
    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_delete_query_error(mock_delete_error):
        """to delete the query with invalid session id - error"""
        error = {"errors": [{"code": 1002, "message": "User session BCP7NIkbiLBkXx2FwdkU7ma9O7bJAWng1k. is not valid"}]}
        mock_delete_error.return_value = get_mock_response(400, json.dumps(error), 'byte')
        search_id = "1594383044445:BCP7NIkbiLBkXx2FwdkU7ma9O7bJAWng1k.:20"
        transmission = stix_transmission.StixTransmission('arcsight', CONNECTION, CONFIG)
        delete_response = transmission.delete(search_id)

        assert delete_response is not None
        assert 'success' in delete_response
        assert delete_response['success'] is False
        assert 'error' in delete_response
        assert delete_response['code'] == 'authentication_fail'

    @staticmethod
    @patch('stix_shifter_modules.arcsight.stix_transmission.api_client.APIClient.delete_search')
    def test_delete_query_exception(mock_delete_exception):
        """to get http exception when delete the query search"""
        mock_delete_exception.side_effect = ConnectionError(
            "('Connection aborted.', ConnectionResetError(10054, 'An existing "
            "connection was forcibly closed by the remote host', None, 10054, "
            "None))")
        transmission = stix_transmission.StixTransmission('arcsight', CONNECTION, CONFIG)
        delete_response = transmission.delete(SEARCH_ID)

        assert delete_response is not None
        assert 'success' in delete_response
        assert delete_response['success'] is False
        assert 'error' in delete_response
        assert delete_response['code'] == 'service_unavailable'

    @staticmethod
    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_create_status(mock_create_status):
        """to get search status of the query - COMPLETED"""
        response = {'status': 'complete', 'result_type': 'histogram', 'hit': 1004,
                    'scanned': 1561219, 'elapsed': '00:00:00.530', 'message': []}
        mock_create_status.return_value = get_mock_response(200, json.dumps(response), 'byte')
        transmission = stix_transmission.StixTransmission('arcsight', CONNECTION, CONFIG)
        status_response = transmission.status(SEARCH_ID)

        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is True
        assert 'status' in status_response
        assert status_response['status'] == 'COMPLETED'

    @staticmethod
    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_create_status_running(mock_create_status):
        """to get search status of the query - RUNNING"""
        response = {'status': 'running', 'result_type': 'histogram', 'hit': 2000,
                    'scanned': 1561210, 'elapsed': '00:00:00.530', 'message': []}
        search_id = "1594383044445:e929MKkCf6i7ngBa3laxFFUJIZtfXINHULlc0oiE6RA.:5000"
        mock_create_status.return_value = get_mock_response(200, json.dumps(response), 'byte')
        transmission = stix_transmission.StixTransmission('arcsight', CONNECTION, CONFIG)
        status_response = transmission.status(search_id)

        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is True
        assert 'status' in status_response
        assert status_response['status'] == 'RUNNING'

    @staticmethod
    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_create_status_complete(mock_create_status):
        """to get search status of the query - COMPLETED"""
        response = {'status': 'running', 'result_type': 'histogram', 'hit': 5000,
                    'scanned': 1561210, 'elapsed': '00:00:00.530', 'message': []}
        search_id = "1594383044445:e929MKkCf6i7ngBa3laxFFUJIZtfXINHULlc0oiE6RA.:1000"
        mock_create_status.return_value = get_mock_response(200, json.dumps(response), 'byte')
        transmission = stix_transmission.StixTransmission('arcsight', CONNECTION, CONFIG)
        status_response = transmission.status(search_id)

        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is True
        assert 'status' in status_response
        assert status_response['status'] == 'COMPLETED'

    @staticmethod
    @patch('stix_shifter_modules.arcsight.stix_transmission.api_client.APIClient.get_search_status')
    def test_create_status_exception(mock_status_exception):
        """to get http exception when status check"""
        mock_status_exception.side_effect = ConnectionError(
            "('Connection aborted.', ConnectionResetError(10054, 'An existing "
            "connection was forcibly closed by the remote host', None, 10054, "
            "None))")
        transmission = stix_transmission.StixTransmission('arcsight', CONNECTION, CONFIG)
        status_response = transmission.status(SEARCH_ID)
        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is False
        assert 'error' in status_response

    @staticmethod
    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_status_error(mock_delete_error):
        """to get error when check with invalid user session id"""
        error = {"errors": [{"code": 1002, "message": "User session BCP7NIkbiLBkXx2FwdkU7ma9O7bJAWng1k. is not valid"}]}
        mock_delete_error.return_value = get_mock_response(400, json.dumps(error), 'byte')
        search_id = "1594383044445:BCP7NIkbiLBkXx2FwdkU7ma9O7bJAWng1k.:20"
        transmission = stix_transmission.StixTransmission('arcsight', CONNECTION, CONFIG)
        status_response = transmission.status(search_id)
        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is False
        assert 'error' in status_response
        assert status_response['code'] == 'authentication_fail'

    @staticmethod
    @patch('stix_shifter_modules.arcsight.stix_transmission.api_client.APIClient.delete_search')
    @patch('stix_shifter_modules.arcsight.stix_transmission.api_client.APIClient.get_search_status')
    @patch('stix_shifter_modules.arcsight.stix_transmission.api_client.APIClient.get_search_results')
    def test_arcsight_logger_down(mock_results, mock_status, mock_delete):
        """arcsight logger down error"""
        error = 'The application is currently unavailable. Please retry shortly.'
        mock_results.return_value = get_mock_response(503, error, 'byte')
        mock_status.return_value = get_mock_response(503, error, 'byte')
        mock_delete.return_value = get_mock_response(503, error, 'byte')
        search_id = "1594383044445:BCP7NIkbiLBkXx2FwdkU7ma9O7bJAWng1k.:20"
        offset = 0
        length = 10
        transmission = stix_transmission.StixTransmission('arcsight', CONNECTION, CONFIG)

        delete_response = transmission.delete(search_id)
        assert delete_response['success'] is False
        assert 'error' in delete_response
        assert delete_response['code'] == 'service_unavailable'

        status_response = transmission.status(search_id)
        assert status_response['success'] is False
        assert 'error' in status_response
        assert status_response['code'] == 'service_unavailable'

        results_response = transmission.results(search_id, offset, length)
        assert results_response['success'] is False
        assert 'error' in results_response
        assert results_response['code'] == 'service_unavailable'
