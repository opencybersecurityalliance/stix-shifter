from stix_shifter_modules.msatp.entry_point import EntryPoint
from unittest.mock import patch
import unittest
from stix_shifter.stix_transmission import stix_transmission
from stix_shifter.stix_transmission.stix_transmission import run_in_thread
from stix_shifter_utils.utils.error_response import ErrorCode
from tests.utils.async_utils import get_mock_response


def mocked_1():
    return get_mock_response(200, "{}", 'byte')


def mocked_2():
    mocked_return_value = """{
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
    return get_mock_response(200, mocked_return_value, 'byte')


class TestMSATPConnection(unittest.TestCase):
    def config(self):
        return {
            "auth": {
                "tenant": "bla",
                "clientId": "bla",
                "clientSecret": "bla"
            }
        }

    def connection(self):
        return {
            "host": "hostbla",
            "port": 8080,
            "selfSignedCert": "cert"
        }

    def test_is_async(self):
        entry_point = EntryPoint(self.connection(), self.config())
        check_async = entry_point.is_async()

        assert check_async is False

    @patch('stix_shifter_modules.msatp.stix_transmission.api_client.APIClient.ping_box')
    def test_ping_endpoint(self, mock_ping_response):
        mocked_return_value = '["mock", "placeholder"]'

        mock_ping_response.return_value = get_mock_response(200, mocked_return_value)
        transmission = stix_transmission.StixTransmission('msatp', self.connection(), self.config())
        ping_response = transmission.ping()

        assert ping_response is not None
        assert ping_response['success']

    @patch('stix_shifter_modules.msatp.stix_transmission.api_client.APIClient.ping_box')
    def test_ping_endpoint_exception(self, mock_ping_response):
        mocked_return_value = '["mock", "placeholder"]'
        mock_ping_response.return_value = get_mock_response(400, mocked_return_value)

        transmission = stix_transmission.StixTransmission('msatp', self.connection(), self.config())
        ping_response = transmission.ping()

        assert ping_response is not None
        assert ping_response['success'] is False
        assert ping_response['code'] == ErrorCode.TRANSMISSION_UNKNOWN.value

    def test_query_connection(self):

        query = "(find withsource = TableName in (DeviceNetworkEvents) where Timestamp >= datetime(" \
                "2019-09-24T16:32:32.993821Z) and Timestamp < datetime(2019-09-24T16:37:32.993821Z) | order by " \
                "Timestamp desc | where LocalPort < 443)"
        transmission = stix_transmission.StixTransmission('msatp', self.connection(), self.config())
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert 'search_id' in query_response
        assert query_response['search_id'] == query

    @patch('stix_shifter_modules.msatp.stix_transmission.api_client.APIClient.run_search',
           autospec=True)
    def test_results_file_response(self, mock_results_response):
        mocked_return_value = """{
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
        mock_results_response.return_value = get_mock_response(200, mocked_return_value, 'byte')

        query = '(find withsource = TableName in (DeviceFileEvents) where Timestamp >= datetime(' \
                '2019-09-01T08:43:10.003Z) and Timestamp < datetime(2019-10-01T10:43:10.003Z) | order by ' \
                'Timestamp desc | where FileName !~ "updater.exe" or InitiatingProcessFileName !~ "updater.exe" ' \
                'or InitiatingProcessParentFileName !~ "updater.exe")'
        offset = 0
        length = 1
        transmission = stix_transmission.StixTransmission('msatp', self.connection(), self.config())
        results_response = transmission.results(query, offset, length)

        assert results_response is not None
        assert results_response['success']
        assert 'data' in results_response
        assert results_response['data'] is not None

    @patch('stix_shifter_modules.msatp.stix_transmission.api_client.APIClient.run_search', autospec=True)
    def test_results_registry_response(self, mock_results_response):
        mocked_return_value = """{"Results": [{"TableName": "DeviceRegistryEvents","Timestamp": "2019-10-10T10:43:07.2363291Z","DeviceId":
"db40e68dd7358aa450081343587941ce96ca4777","DeviceName": "testmachine1","ActionType": "RegistryValueSet",
"RegistryKey": "HKEY_LOCAL_MACHINE\\\\SYSTEM\\\\ControlSet001\\\\Services\\\\WindowsAzureGuestAgent",
"RegistryValueType":
"Binary","RegistryValueName": "FailureActions","RegistryValueData": ""}]}"""
        mock_results_response.return_value = get_mock_response(200, mocked_return_value, 'byte')

        query = '(find withsource = TableName in (DeviceRegistryEvents) where Timestamp >= datetime(' \
                '2019-09-01T08:43:10.003Z) and Timestamp < datetime(2019-10-10T10:43:10.003Z) | order by Timestamp ' \
                'desc | where RegistryKey !~ "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows ' \
                'NT\\CurrentVersion\\Schedule\\TaskCache\\Tree\\Microsoft\\Windows\\UpdateOrchestrator\\AC Power ' \
                'Install")'
        offset = 0
        length = 1
        transmission = stix_transmission.StixTransmission('msatp', self.connection(), self.config())
        results_response = transmission.results(query, offset, length)

        assert results_response is not None
        assert results_response['success']
        assert 'data' in results_response
        assert results_response['data'] is not None

    @patch('stix_shifter_modules.msatp.stix_transmission.api_client.APIClient.run_search', autospec=True)
    def test_results_response_exception(self, mock_results_response):
        mocked_return_value = """ {    } """
        mock_results_response.return_value = get_mock_response(404, mocked_return_value)

        query = "(find withsource = TableName in (DeviceNetworkEvents) where " \
                "Timestamp >= datetime('2021-04-25T14:09:15.093Z) and Timestamp < datetime(2021-04-25T14:14:15.093Z) " \
                "| order by Timestamp desc | where LocalPort < 443) "
        offset = 0
        length = 1

        transmission = stix_transmission.StixTransmission('msatp', self.connection(), self.config())
        results_response = transmission.results(query, offset, length)

        assert results_response['code'] == 'unknown'
        assert results_response['success'] is False

    @patch('stix_shifter_modules.msatp.stix_transmission.api_client.APIClient.run_search', autospec=True)
    def test_query_flow(self, mock_results_response):
        results_mock = """{
                            "Results": [{
                                "TableName": "DeviceFileEvents",
                                "Timestamp": "2019-10-13T11:34:14.0075314Z",
                                "DeviceName": "desktop-536bt46",
                                "FileName": "runcit_tlm_hw.bat",
                                "SHA1": "93b458752aea37a257a7dd2ed51e98ffffc35be8",
                                "SHA256": "",
                                "MD5": "26a2fe38dc6f42386659e611219c563c"
                            }]
                            }"""

        mock_results_response.return_value = get_mock_response(200, results_mock, 'byte')

        query = '(find withsource = TableName in (DeviceFileEvents) where Timestamp >= datetime(' \
                '2019-09-01T08:43:10.003Z) and Timestamp < datetime(2019-10-01T10:43:10.003Z) | order by Timestamp ' \
                'desc | where FileName !~ "updater.exe" or InitiatingProcessFileName !~ "updater.exe" or ' \
                'InitiatingProcessParentFileName !~ "updater.exe")'

        transmission = stix_transmission.StixTransmission('msatp', self.connection(), self.config())
        query_response = transmission.query(query)

        assert query_response is not None
        assert 'search_id' in query_response
        assert query_response['search_id'] == '(find withsource = TableName in (DeviceFileEvents) where ' \
                                              'Timestamp >= datetime(' \
                                              '2019-09-01T08:43:10.003Z) and Timestamp < datetime(' \
                                              '2019-10-01T10:43:10.003Z) | ' \
                                              'order by Timestamp desc | where FileName !~ "updater.exe" or ' \
                                              'InitiatingProcessFileName !~ "updater.exe" or ' \
                                              'InitiatingProcessParentFileName !~ ' \
                                              '"updater.exe")'
        offset = 0
        length = 1

        results_response = transmission.results(query_response['search_id'], offset, length)

        assert results_response is not None
        assert 'data' in results_response
        assert results_response['data'] is not None

    def test_delete_query(self):

        search_id = '(find withsource = TableName in (DeviceFileEvents) where Timestamp >= datetime(' \
                    '2019-09-01T08:43:10.003Z) and Timestamp < datetime(2019-10-01T10:43:10.003Z) | order by ' \
                    'Timestamp desc | where FileName !~ "updater.exe" or InitiatingProcessFileName !~ "updater.exe" ' \
                    'or InitiatingProcessParentFileName !~ "updater.exe")'

        entry_point = EntryPoint(self.connection(), self.config())
        status_response = run_in_thread(entry_point.delete_query_connection, search_id)
        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is True

    def test_status_query(self):

        search_id = '(find withsource = TableName in (DeviceFileEvents) where Timestamp >= datetime(' \
                    '2019-09-01T08:43:10.003Z) and Timestamp < datetime(2019-10-01T10:43:10.003Z) | order by ' \
                    'Timestamp desc | where FileName !~ "updater.exe" or InitiatingProcessFileName !~ "updater.exe" ' \
                    'or InitiatingProcessParentFileName !~ "updater.exe")'

        entry_point = EntryPoint(self.connection(), self.config())
        status_response = run_in_thread(entry_point.create_status_connection, search_id)
        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is True

