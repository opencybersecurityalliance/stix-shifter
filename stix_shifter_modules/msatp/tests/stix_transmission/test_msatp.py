from stix_shifter_modules.msatp.entry_point import EntryPoint
from unittest.mock import patch
import unittest
from stix_shifter.stix_transmission import stix_transmission
from stix_shifter.stix_transmission.stix_transmission import run_in_thread
from stix_shifter_modules.msatp.stix_transmission import connector
from stix_shifter_utils.utils.error_response import ErrorCode
from tests.utils.async_utils import get_mock_response, get_adal_mock_response


@patch('stix_shifter_modules.msatp.stix_transmission.connector.adal.AuthenticationContext')
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

    def test_is_async(self, mock_adal_auth):
        mock_adal_auth.return_value = get_adal_mock_response()
        entry_point = EntryPoint(self.connection(), self.config())
        check_async = entry_point.is_async()

        assert check_async is False

    @patch('stix_shifter_modules.msatp.stix_transmission.api_client.APIClient.ping_box')
    def test_ping_endpoint(self, mock_ping_response, mock_adal_auth):
        mock_adal_auth.return_value = get_adal_mock_response()
        mocked_return_value = '["mock", "placeholder"]'

        mock_ping_response.return_value = get_mock_response(200, mocked_return_value)
        transmission = stix_transmission.StixTransmission('msatp', self.connection(), self.config())
        ping_response = transmission.ping()

        assert ping_response is not None
        assert ping_response['success']

    @patch('stix_shifter_modules.msatp.stix_transmission.api_client.APIClient.ping_box')
    def test_ping_endpoint_exception(self, mock_ping_response, mock_adal_auth):
        mock_adal_auth.return_value = get_adal_mock_response()
        mocked_return_value = '["mock", "placeholder"]'
        mock_ping_response.return_value = get_mock_response(400, mocked_return_value)

        transmission = stix_transmission.StixTransmission('msatp', self.connection(), self.config())
        ping_response = transmission.ping()

        assert ping_response is not None
        assert ping_response['success'] is False
        assert ping_response['code'] == ErrorCode.TRANSMISSION_UNKNOWN.value

    def test_query_connection(self, mock_adal_auth):
        mock_adal_auth.return_value = get_adal_mock_response()

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
    def test_results_file_response(self, mock_results_response, mock_adal_auth):
        mock_adal_auth.return_value = get_adal_mock_response()
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

    @patch('stix_shifter_modules.msatp.stix_transmission.api_client.APIClient.run_search',
           autospec=True)
    def test_results_registry_response(self, mock_results_response, mock_adal_auth):
        mock_adal_auth.return_value = get_adal_mock_response()
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

    @patch('stix_shifter_modules.msatp.stix_transmission.api_client.APIClient.run_search',
           autospec=True)
    def test_results_response_exception(self, mock_results_response, mock_adal_auth):
        mock_adal_auth.return_value = get_adal_mock_response()
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

    @patch('stix_shifter_modules.msatp.stix_transmission.api_client.APIClient.run_search',
           autospec=True)
    def test_query_flow(self, mock_results_response, mock_adal_auth):
        mock_adal_auth.return_value = get_adal_mock_response()
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

    def test_delete_query(self, mock_adal_auth):
        mock_adal_auth.return_value = get_adal_mock_response()

        search_id = '(find withsource = TableName in (DeviceFileEvents) where Timestamp >= datetime(' \
                    '2019-09-01T08:43:10.003Z) and Timestamp < datetime(2019-10-01T10:43:10.003Z) | order by ' \
                    'Timestamp desc | where FileName !~ "updater.exe" or InitiatingProcessFileName !~ "updater.exe" ' \
                    'or InitiatingProcessParentFileName !~ "updater.exe")'

        entry_point = EntryPoint(self.connection(), self.config())
        status_response = run_in_thread(entry_point.delete_query_connection, search_id)
        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is True

    def test_status_query(self, mock_adal_auth):
        mock_adal_auth.return_value = get_adal_mock_response()

        search_id = '(find withsource = TableName in (DeviceFileEvents) where Timestamp >= datetime(' \
                    '2019-09-01T08:43:10.003Z) and Timestamp < datetime(2019-10-01T10:43:10.003Z) | order by ' \
                    'Timestamp desc | where FileName !~ "updater.exe" or InitiatingProcessFileName !~ "updater.exe" ' \
                    'or InitiatingProcessParentFileName !~ "updater.exe")'

        entry_point = EntryPoint(self.connection(), self.config())
        status_response = run_in_thread(entry_point.create_status_connection, search_id)
        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is True

    @patch('stix_shifter_modules.msatp.stix_transmission.api_client.APIClient.__new__', autospec=True)
    def test_join_query_with_alerts(self, mock_api_client, mock_adal_auth):
        mock_adal_auth.return_value = get_adal_mock_response()
        query = 'union (find withsource = TableName in (DeviceNetworkEvents)  where Timestamp >= datetime(2023-02-13T14:25:46.000Z) and Timestamp < datetime(2023-02-13T14:26:55.500Z)  | order by Timestamp desc | where (LocalIP =~ "9.9.9.9") or (RemoteIP =~ "9.9.9.9")),(find withsource = TableName in (DeviceEvents)  where Timestamp >= datetime(2023-02-13T14:25:46.000Z) and Timestamp < datetime(2023-02-13T14:26:55.500Z)  | order by Timestamp desc | where (RemoteIP =~ "9.9.9.9") or (LocalIP =~ "9.9.9.9"))'
        entry_point = connector.Connector(self.connection(), self.config())
        joined_query, partial_query = entry_point.join_query_with_alerts(query)
        assert joined_query == '(((union (find withsource = TableName in (DeviceNetworkEvents)  where Timestamp >= datetime(2023-02-13T14:25:46.000Z) and Timestamp < datetime(2023-02-13T14:26:55.500Z)  | order by Timestamp desc | where (LocalIP =~ "9.9.9.9") or (RemoteIP =~ "9.9.9.9")),(find withsource = TableName in (DeviceEvents)  where Timestamp >= datetime(2023-02-13T14:25:46.000Z) and Timestamp < datetime(2023-02-13T14:26:55.500Z)  | order by Timestamp desc | where (RemoteIP =~ "9.9.9.9") or (LocalIP =~ "9.9.9.9"))| join kind=leftouter (DeviceAlertEvents | summarize AlertId=make_list(AlertId), Severity=make_list(Severity), Title=make_list(Title), Category=make_list(Category), AttackTechniques=make_list(AttackTechniques) by DeviceName, ReportId, Timestamp) on ReportId, DeviceName, Timestamp)| join kind=leftouter (DeviceNetworkInfo | where NetworkAdapterStatus == "Up" | project Timestamp, DeviceId, MacAddress, IPAddresses| summarize IPAddressesSet=make_set(IPAddresses), MacAddressSet=make_set(MacAddress) by DeviceId, Timestamp) on DeviceId) | where Timestamp2 < Timestamp | summarize arg_max(Timestamp2, *) by ReportId, DeviceName, Timestamp) | join kind=leftouter (DeviceInfo | project Timestamp, DeviceId, PublicIP, OSArchitecture, OSPlatform, OSVersion) on DeviceId | where Timestamp3 < Timestamp | summarize arg_max(Timestamp3, *) by ReportId, DeviceName, Timestamp'
        assert partial_query == '(union (find withsource = TableName in (DeviceNetworkEvents)  where Timestamp >= datetime(2023-02-13T14:25:46.000Z) and Timestamp < datetime(2023-02-13T14:26:55.500Z)  | order by Timestamp desc | where (LocalIP =~ "9.9.9.9") or (RemoteIP =~ "9.9.9.9")),(find withsource = TableName in (DeviceEvents)  where Timestamp >= datetime(2023-02-13T14:25:46.000Z) and Timestamp < datetime(2023-02-13T14:26:55.500Z)  | order by Timestamp desc | where (RemoteIP =~ "9.9.9.9") or (LocalIP =~ "9.9.9.9")) | join kind=leftouter (DeviceAlertEvents | summarize AlertId=make_list(AlertId), Severity=make_list(Severity), Title=make_list(Title), Category=make_list(Category), AttackTechniques=make_list(AttackTechniques) by DeviceName, ReportId, Timestamp) on ReportId, DeviceName, Timestamp)'

        query = '(find withsource = TableName in (DeviceAlertEvents)  where Timestamp >= datetime(2023-03-16T17:21:30.000Z) and Timestamp < datetime(2023-03-18T17:30:36.000Z)  | order by Timestamp desc | where AlertId =~ "123123")'
        entry_point = connector.Connector(self.connection(), self.config())
        joined_query, partial_query = entry_point.join_query_with_alerts(query)
        assert joined_query == query
        assert partial_query is None

    @patch('stix_shifter_modules.msatp.stix_transmission.api_client.APIClient.__new__', autospec=True)
    def test_unify_alert_fields(self, mock_api_client, mock_adal_auth):
        mock_adal_auth.return_value = get_adal_mock_response()
        entry_point = connector.Connector(self.connection(), self.config())
        data = {
            'AlertId': ['da111111111111111111_-1111111111'],
            'Timestamp': '2023-03-17T16:59:12.3036191Z',
            'Severity': ['High'],
            'Category': ['InitialAccess'],
            'Title': ['Suspicious URL clicked'],
            'AttackTechniques': ['["Spearphishing Link (T1566.002)"]'],
            'ReportId': 1234,
            'Table': 'DeviceEvents'
        }

        unified = entry_point.unify_alert_fields(data)
        assert unified is not None
        alerts = unified.get("Alerts")
        assert alerts is not None
        assert len(alerts) == 1
        alert = alerts[0]
        assert alert.get("AlertId") == 'da111111111111111111_-1111111111'
        assert alert.get("Title") == 'Suspicious URL clicked'
        ttps = alert.get("AttackTechniques")
        assert ttps is not None
        assert len(ttps) == 1
        ttp = ttps[0]
        assert ttp == 'Spearphishing Link (T1566.002)'
