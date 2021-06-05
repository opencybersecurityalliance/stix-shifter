from stix_shifter_modules.crowdstrike.entry_point import EntryPoint
from unittest.mock import patch
import unittest
from stix_shifter.stix_transmission import stix_transmission
from stix_shifter_utils.utils.error_response import ErrorCode


class CrowdStrikeMockResponse:
    def __init__(self, response_code, obj):
        self.code = response_code
        self.object = obj

    def read(self):
        return bytearray(self.object, 'utf-8')


@patch('stix_shifter_modules.crowdstrike.stix_transmission.api_client.APIClient.__init__')
class TestcrowdstrikeConnection(unittest.TestCase):
    def config(self):
        return {
            "auth": {
                "client_id": "bla",
                "client_secret": "bla"
            }
        }

    def connection(self):
        return {
            "host": "hostbla",
            "selfSignedCert": "cert"
        }

    def test_is_async(self, mock_api_client):
        mock_api_client.return_value = None
        entry_point = EntryPoint(self.connection(), self.config())
        check_async = entry_point.is_async()

        assert check_async is False

    def test_query_connection(self, mock_api_client):
        mock_api_client.return_value = None

        query = "((behaviors.timestamp:> '2019-09-04T09:29:29.0882Z') + device.last_seen:> '2002-05-27T03:51:40.090688')"

        transmission = stix_transmission.StixTransmission('crowdstrike', self.connection(), self.config())
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert 'search_id' in query_response
        assert query_response['search_id'] == query

    @patch('stix_shifter_modules.crowdstrike.stix_transmission.api_client.APIClient.get_detections_IDs')
    def test_query(self, mock_query_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = '{"job_id": "108cb8b0-0744-4dd9-8e35-ea8311cd6211"}'
        mock_query_response.return_value = CrowdStrikeMockResponse(200, mocked_return_value)

        entry_point = EntryPoint(self.connection(), self.config())
        query = [
            "((behaviors.timestamp:> '2019-09-04T09:29:29.0882Z') + device.last_seen:> '2002-05-27T03:51:40.090688')"]
        query_response = entry_point.create_query_connection(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert 'search_id' in query_response
        assert query_response['search_id'] == query

    @patch('stix_shifter_modules.crowdstrike.stix_transmission.api_client.APIClient.run_search',
           autospec=True)
    def test_results_file_response(self, mock_results_response, mock_api_client, mock_generate_token):


        mock_api_client.return_value = None
        mock_generate_token.return_value = None
        mocked_return_value = """{ # NOT SURE WHAT RESPONSE TO PUT HERE #
                            "Results": [{
                                "TableName": "DeviceFileEvents",
                                "Timestamp": "2019-09-13T11:34:14.0075314Z",
                                "DeviceName": "desktop-536bt46",
                                "FileName": "runcit_tlm_hw.bat",
                                "SHA1": "93b458752aea37a257a7dd2ed51e98ffffc35be8",
                                "SHA256": "",
                                "MD5": "26a2fe38dc6f42386659e611219c563c"
                            }]
                            }"""
        mock_results_response.return_value = CrowdStrikeMockResponse(200, mocked_return_value)

        query = 'behaviors.filename:"powershell.exe"'
        offset = 0
        length = 1
        transmission = stix_transmission.StixTransmission('crowdstrike', self.connection(), self.config())
        results_response = transmission.results(query, offset, length)

        assert results_response is not None
        assert results_response['success']
        assert 'data' in results_response
        assert results_response['data'] is not None

    def test_delete_query(self, mock_api_client, mock_generate_token): # Does this make sense to have? CS doesn't have the ability to delete a query in the API.
        mock_api_client.return_value = None
        mock_generate_token.return_value = None

        search_id = '(find withsource = TableName in (DeviceFileEvents) where Timestamp >= datetime(' \
                    '2019-09-01T08:43:10.003Z) and Timestamp < datetime(2019-10-01T10:43:10.003Z) | order by ' \
                    'Timestamp desc | where FileName !~ "updater.exe" or InitiatingProcessFileName !~ "updater.exe" ' \
                    'or InitiatingProcessParentFileName !~ "updater.exe")'

        entry_point = EntryPoint(self.connection(), self.config())
        status_response = entry_point.delete_query_connection(search_id)
        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is True

    def test_status_query(self, mock_api_client, mock_generate_token): # Does this make sense to have? CS doesn't have the ability to check a query status in the API.


        mock_api_client.return_value = None
        mock_generate_token.return_value = None

        search_id = '(find withsource = TableName in (DeviceFileEvents) where Timestamp >= datetime(' \
                    '2019-09-01T08:43:10.003Z) and Timestamp < datetime(2019-10-01T10:43:10.003Z) | order by ' \
                    'Timestamp desc | where FileName !~ "updater.exe" or InitiatingProcessFileName !~ "updater.exe" ' \
                    'or InitiatingProcessParentFileName !~ "updater.exe")'

        entry_point = EntryPoint(self.connection(), self.config())
        status_response = entry_point.create_status_connection(search_id)
        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is True

    @patch('requests.sessions.Session.get')
    def test_one_results_response(self, mock_requests_response):
        mocked_process_return_value, mocked_events_return_value = \
            TestCarbonBlackEventsConnection._get_mock_process_and_events_data()
        mock_requests_response.side_effect = [
            RequestMockResponse(200, mocked_process_return_value.encode()),
            RequestMockResponse(200, mocked_events_return_value.encode()),
        ]
        entry_point = EntryPoint(connection, config)
        query_expression = self._create_query_list("process_name:erl.exe and last_update:[2021-03-15T16:20:00 TO 2021-03-15T16:30:00]")[0]
        results_response = entry_point.create_results_connection(query_expression, 0, 10)

        assert results_response is not None
        assert 'success' in results_response
        assert results_response['success']
        assert 'data' in results_response
        assert len(results_response['data']) == 3
        assert 'process_name' in results_response['data'][0]
        assert results_response['data'][0]['process_name'] == 'erl.exe'
        assert 'modload_md5' in results_response['data'][0]
        assert results_response['data'][0]['modload_md5'] == '450e6430481940a25e7b268dcc29a6d4'

    @patch('requests.sessions.Session.get')
    def test_bad_token_response(self, mock_requests_response):
        mocked_return_value = """{'meta': {'query_time': 0.070233344, 'powered_by': 'csam', 'trace_id': '410f2f54-baa9-4658-85c7-93d8f9b28547'}, 'errors': [{'code': 403, 'message': 'Failed to issue access token - Not Authorized'}]}
        """

        mock_requests_response.side_effect = [
            RequestMockResponse(403, mocked_return_value.encode())
        ]
        entry_point = EntryPoint(connection, config)
        query_expression = self._create_query_list('behaviors.filename:"powershell.exe"')[0]
        results_response = entry_point.create_results_connection(query_expression, 0, 10)

        assert results_response is not None
        assert 'success' in results_response
        assert results_response['success'] == False
        assert 'error' in results_response
        assert results_response['error'] == mocked_return_value
        assert 'code' in results_response
        assert  results_response['code'] == 'authentication_fail'