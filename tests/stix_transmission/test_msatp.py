from stix_shifter.stix_transmission.src.modules.msatp import msatp_connector
from unittest.mock import patch
import unittest
from stix_shifter.stix_transmission import stix_transmission
from stix_shifter.utils.error_response import ErrorCode


class MSATPMockResponse:
    def __init__(self, response_code, obj):
        self.code = response_code
        self.object = obj

    def read(self):
        return bytearray(self.object, 'utf-8')


@patch('stix_shifter.stix_transmission.src.modules.msatp.msatp_connector.Connector.generate_token')
@patch('stix_shifter.stix_transmission.src.modules.msatp.api_client.APIClient.__init__')
class TestMSATPConnection(unittest.TestCase):
    config = {
        "auth": {
            "SEC": "bla"
        }
    }
    connection = {
        "host": "hostbla",
        "port": "8080",
        "ceft": "cert"
    }

    def test_is_async(self, mock_api_client, mock_generate_token):
        mock_api_client.return_value = None
        mock_generate_token.return_value = 'test'
        module = msatp_connector
        check_async = module.Connector(self.connection, self.config).is_async

        assert check_async is False

    @patch('stix_shifter.stix_transmission.src.modules.msatp.api_client.APIClient.ping_box')
    def test_ping_endpoint(self, mock_ping_response, mock_api_client, mock_generate_token):
        mock_api_client.return_value = None
        mock_generate_token.return_value = None
        mocked_return_value = '["mock", "placeholder"]'

        mock_ping_response.return_value = MSATPMockResponse(200, mocked_return_value)

        transmission = stix_transmission.StixTransmission('msatp', self.connection, self.config)
        ping_response = transmission.ping()

        assert ping_response is not None
        assert ping_response['success']

    @patch('stix_shifter.stix_transmission.src.modules.msatp.api_client.APIClient.ping_box')
    def test_ping_endpoint_exception(self, mock_ping_response, mock_api_client, mock_generate_token):
        mock_api_client.return_value = None
        mock_generate_token.return_value = None
        mocked_return_value = '["mock", "placeholder"]'
        mock_ping_response.return_value = MSATPMockResponse(200, mocked_return_value)
        mock_ping_response.side_effect = Exception('exception')

        transmission = stix_transmission.StixTransmission('msatp', self.connection, self.config)
        ping_response = transmission.ping()

        assert ping_response is not None
        assert ping_response['success'] is False
        assert ping_response['code'] == ErrorCode.TRANSMISSION_UNKNOWN.value

    def test_query_connection(self, mock_api_client, mock_generate_token):
        mock_api_client.return_value = None
        mock_generate_token.return_value = None

        query = "(find withsource = TableName in (NetworkCommunicationEvents) where EventTime >= datetime(" \
                "2019-09-24T16:32:32.993821Z) and EventTime < datetime(2019-09-24T16:37:32.993821Z) | order by " \
                "EventTime desc | where LocalPort < 443)"
        transmission = stix_transmission.StixTransmission('msatp', self.connection, self.config)
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert 'search_id' in query_response
        assert query_response['search_id'] == query

    @patch('stix_shifter.stix_transmission.src.modules.msatp.api_client.APIClient.run_search',
           autospec=True)
    def test_results_file_response(self, mock_results_response, mock_api_client, mock_generate_token):
        mock_api_client.return_value = None
        mock_generate_token.return_value = None
        mocked_return_value = """{
                            "Results": [{
                                "TableName": "FileCreationEvents",
                                "EventTime": "2019-09-13T11:34:14.0075314Z",
                                "ComputerName": "desktop-536bt46",
                                "FileName": "runcit_tlm_hw.bat",
                                "SHA1": "93b458752aea37a257a7dd2ed51e98ffffc35be8",
                                "SHA256": "",
                                "MD5": "26a2fe38dc6f42386659e611219c563c"
                            }]
                            }"""
        mock_results_response.return_value = MSATPMockResponse(200, mocked_return_value)

        query = '(find withsource = TableName in (FileCreationEvents) where EventTime >= datetime(' \
                '2019-09-01T08:43:10.003Z) and EventTime < datetime(2019-10-01T10:43:10.003Z) | order by ' \
                'EventTime desc | where FileName !~ "updater.exe" or InitiatingProcessFileName !~ "updater.exe" ' \
                'or InitiatingProcessParentFileName !~ "updater.exe")'
        offset = 0
        length = 1
        transmission = stix_transmission.StixTransmission('msatp', self.connection, self.config)
        results_response = transmission.results(query, offset, length)

        assert results_response is not None
        assert results_response['success']
        assert 'data' in results_response
        assert results_response['data'] is not None

    @patch('stix_shifter.stix_transmission.src.modules.msatp.api_client.APIClient.run_search',
           autospec=True)
    def test_results_registry_response(self, mock_results_response, mock_api_client, mock_generate_token):
        mock_api_client.return_value = None
        mock_generate_token.return_value = None
        mocked_return_value = """{"Results": [{"TableName": "RegistryEvents","EventTime": "2019-10-10T10:43:07.2363291Z","MachineId":
"db40e68dd7358aa450081343587941ce96ca4777","ComputerName": "testmachine1","ActionType": "RegistryValueSet",
"RegistryKey": "HKEY_LOCAL_MACHINE\\\\SYSTEM\\\\ControlSet001\\\\Services\\\\WindowsAzureGuestAgent",
"RegistryValueType":
"Binary","RegistryValueName": "FailureActions","RegistryValueData": ""}]}"""
        mock_results_response.return_value = MSATPMockResponse(200, mocked_return_value)

        query = '(find withsource = TableName in (RegistryEvents) where EventTime >= datetime(' \
                '2019-09-01T08:43:10.003Z) and EventTime < datetime(2019-10-10T10:43:10.003Z) | order by EventTime ' \
                'desc | where RegistryKey !~ "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows ' \
                'NT\\CurrentVersion\\Schedule\\TaskCache\\Tree\\Microsoft\\Windows\\UpdateOrchestrator\\AC Power ' \
                'Install")'
        offset = 0
        length = 1
        transmission = stix_transmission.StixTransmission('msatp', self.connection, self.config)
        results_response = transmission.results(query, offset, length)

        assert results_response is not None
        assert results_response['success']
        assert 'data' in results_response
        assert results_response['data'] is not None

    @patch('stix_shifter.stix_transmission.src.modules.msatp.api_client.APIClient.run_search',
           autospec=True)
    def test_results_response_exception(self, mock_results_response, mock_api_client, mock_generate_token):
        mock_api_client.return_value = None
        mock_generate_token.return_value = None
        mocked_return_value = """ {    } """
        mock_results_response.return_value = MSATPMockResponse(404, mocked_return_value)

        query = "(find withsource = TableName in (NetworkCommunicationEvents) where EventTime >= datetime(" \
                "2019-09-24T16:32:32.993821Z) and EventTime < datetime(2019-09-24T16:37:32.993821Z) | order by " \
                "EventTime desc | where LocalPort < 443)"
        offset = 0
        length = 1
        transmission = stix_transmission.StixTransmission('msatp', self.connection, self.config)
        results_response = transmission.results(query, offset, length)

        assert results_response['code'] == 'unknown'
        assert results_response['success'] is False

    @patch('stix_shifter.stix_transmission.src.modules.msatp.api_client.APIClient.run_search',
           autospec=True)
    def test_query_flow(self, mock_results_response, mock_api_client, mock_generate_token):
        mock_api_client.return_value = None
        mock_generate_token.return_value = None
        results_mock = """{
                            "Results": [{
                                "TableName": "FileCreationEvents",
                                "EventTime": "2019-10-13T11:34:14.0075314Z",
                                "ComputerName": "desktop-536bt46",
                                "FileName": "runcit_tlm_hw.bat",
                                "SHA1": "93b458752aea37a257a7dd2ed51e98ffffc35be8",
                                "SHA256": "",
                                "MD5": "26a2fe38dc6f42386659e611219c563c"
                            }]
                            }"""

        mock_results_response.return_value = MSATPMockResponse(200, results_mock)
        module = msatp_connector

        query = '(find withsource = TableName in (FileCreationEvents) where EventTime >= datetime(' \
                '2019-09-01T08:43:10.003Z) and EventTime < datetime(2019-10-01T10:43:10.003Z) | order by EventTime ' \
                'desc | where FileName !~ "updater.exe" or InitiatingProcessFileName !~ "updater.exe" or ' \
                'InitiatingProcessParentFileName !~ "updater.exe")'

        transmission = stix_transmission.StixTransmission('msatp', self.connection, self.config)
        query_response = transmission.query(query)

        assert query_response is not None
        assert 'search_id' in query_response
        assert query_response['search_id'] == '(find withsource = TableName in (FileCreationEvents) where ' \
                                              'EventTime >= datetime(' \
                                              '2019-09-01T08:43:10.003Z) and EventTime < datetime(' \
                                              '2019-10-01T10:43:10.003Z) | ' \
                                              'order by EventTime desc | where FileName !~ "updater.exe" or ' \
                                              'InitiatingProcessFileName !~ "updater.exe" or ' \
                                              'InitiatingProcessParentFileName !~ ' \
                                              '"updater.exe")'
        offset = 0
        length = 1
        results_response = module.Connector(self.connection, self.config).create_results_connection(query, offset,
                                                                                                    length)

        assert results_response is not None
        assert 'data' in results_response
        assert results_response['data'] is not None

    def test_delete_query(self, mock_api_client, mock_generate_token):
        mock_api_client.return_value = None
        mock_generate_token.return_value = None

        search_id = '(find withsource = TableName in (FileCreationEvents) where EventTime >= datetime(' \
                    '2019-09-01T08:43:10.003Z) and EventTime < datetime(2019-10-01T10:43:10.003Z) | order by ' \
                    'EventTime desc | where FileName !~ "updater.exe" or InitiatingProcessFileName !~ "updater.exe" ' \
                    'or InitiatingProcessParentFileName !~ "updater.exe")'

        module = msatp_connector
        status_response = module.Connector(self.connection, self.config).delete_query_connection(search_id)
        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is True

    def test_status_query(self, mock_api_client, mock_generate_token):
        mock_api_client.return_value = None
        mock_generate_token.return_value = None

        search_id = '(find withsource = TableName in (FileCreationEvents) where EventTime >= datetime(' \
                    '2019-09-01T08:43:10.003Z) and EventTime < datetime(2019-10-01T10:43:10.003Z) | order by ' \
                    'EventTime desc | where FileName !~ "updater.exe" or InitiatingProcessFileName !~ "updater.exe" ' \
                    'or InitiatingProcessParentFileName !~ "updater.exe")'

        module = msatp_connector
        status_response = module.Connector(self.connection, self.config).create_status_connection(search_id)
        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is True
