import json

from stix_shifter_modules.msatp.stix_transmission.connector_post_processing import merge_alerts, \
    remove_duplicate_and_empty_fields, get_table_name, ConnectorPostProcessing, unify_alert_fields, \
    organize_registry_data, organize_ips, create_event_link, remove_duplicate_ips
from stix_shifter_modules.msatp.tests.test_utils import all_keys_in_object
from unittest.mock import patch
import unittest
from tests.utils.async_utils import get_mock_response


class TestMSATPConnectorPostProcessing(unittest.TestCase):
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
            "selfSignedCert": "cert",
            "options": {
                "includeAlerts": True,
                "includeHostOs": True,
                "includeNetworkInfo": True,
                "retainOriginal": True
            }
        }

    def test_merge_alert_events(self):
        data = [
            {
                'TableName': 'DeviceAlertEvents',
                'AlertId': 'da123456789012345678_-1111111111',
                'Timestamp': '2023-03-17T16:59:12.3036191Z',
                'DeviceId': '1234567890abcdef1234567890abcdef12345678',
                'DeviceName': 'host.test.com',
                'Severity': 'High',
                'Category': 'InitialAccess',
                'Title': 'Suspicious URL clicked',
                'FileName': '',
                'SHA1': '',
                'RemoteUrl': 'https://malicious.com',
                'RemoteIP': '',
                'AttackTechniques': '["Spearphishing Link (T1566.002)"]',
                'ReportId': 1234,
                'Table': 'DeviceEvents',
                'rn': 1
            },
            {
                'TableName': 'DeviceAlertEvents',
                'AlertId': 'da123456789012345678_-1111111111',
                'Timestamp': '2023-03-17T16:59:12.3036191Z',
                'DeviceId': '1234567890abcdef1234567890abcdef12345678',
                'DeviceName': 'host.test.com',
                'Severity': 'High',
                'Category': 'InitialAccess',
                'Title': 'Suspicious URL clicked',
                'FileName': '',
                'SHA1': '',
                'RemoteUrl': '',
                'RemoteIP': '9.9.9.9',
                'AttackTechniques': '["Spearphishing Link (T1566.002)"]',
                'ReportId': 1234,
                'Table': 'DeviceEvents',
                'rn': 1
            },
            {
                'TableName': 'DeviceAlertEvents',
                'AlertId': 'da123456789012345678_-1111111111',
                'Timestamp': '2023-03-17T16:59:12.3036191Z',
                'DeviceId': '1234567890abcdef1234567890abcdef12345678',
                'DeviceName': 'host.test.com',
                'Severity': 'High',
                'Category': 'InitialAccess',
                'Title': 'Suspicious URL clicked',
                'FileName': 'msedge.exe',
                'SHA1': '',
                'RemoteUrl': '',
                'RemoteIP': '',
                'AttackTechniques': '["Spearphishing Link (T1566.002)"]',
                'ReportId': 1234,
                'Table': 'DeviceEvents',
                'rn': 1
            },
            {
                'TableName': 'DeviceProcessEvents',
                'Timestamp': '2023-03-17T16:59:12.3036191Z',
                'DeviceId': '1234567890abcdef1234567890abcdef12345678',
                'DeviceName': 'host.test.com',
            },
            {
                'TableName': 'DeviceProcessEvents',
                'Timestamp': '2023-03-17T16:59:12.3036191Z',
                'DeviceId': '1234567890abcdef1234567890abcdef12345678',
                'DeviceName': 'host2.test.com',
            }
        ]
        merged = merge_alerts(data)
        assert len(merged) == 3
        alert = merged[0]
        assert alert.get("TableName") == "DeviceAlertEvents"
        assert all_keys_in_object(
            {'TableName', 'AlertId', 'Timestamp', 'DeviceId', 'DeviceName', 'Severity', 'Category', 'Title',
             'AttackTechniques', 'ReportId'}, alert)
        proc_event1 = merged[1]
        assert proc_event1.get("TableName") == "DeviceProcessEvents"
        assert proc_event1.get("DeviceName") == "host.test.com"
        proc_event2 = merged[2]
        assert proc_event2.get("TableName") == "DeviceProcessEvents"
        assert proc_event2.get("DeviceName") == "host2.test.com"

    def test_remove_duplicate_fields(self):
        data = {
            'ReportId': 1234,
            'DeviceName': 'host.example.com',
            'DeviceId': '1234567890abcdef1234567890abcdef12345678',
            'Timestamp': '2023-03-17T16:59:12.3036191Z',
            'Timestamp2': '2023-03-17T16:39:21.7061265Z',
            'Timestamp1': '2023-03-17T16:39:21.7061265Z',
            'TableName': 'DeviceEvents',
            'InitiatingProcessSHA1': '4a65b267d5fc37527f567f0300e1624845600be1',
            'InitiatingProcessSHA256': 'b84257d238582d3768799e08df03f0b3378a7f8d7342b8c8ffcc453cf6a7b867',
            'InitiatingProcessMD5': '58f918b86a4798177032abcb12c9c605',
            'DeviceId1': '1234567890abcdef1234567890abcdef12345678',
            'DeviceId2': '1234567890abcdef1234567890abcdef12345678',
            'DNI_TS': '2023-03-17T16:59:12.3036191Z',
            'DI_TS': '2023-03-17T16:59:12.3036191Z',
            'SHA1': None,
            'MD5': ''
        }
        remove_duplicate_and_empty_fields(data)
        assert all_keys_in_object({'ReportId', 'DeviceName', 'DeviceId', 'Timestamp', 'TableName',
                                   'InitiatingProcessSHA1', 'InitiatingProcessSHA256', 'InitiatingProcessMD5'}, data)
        assert 'DeviceId1' not in data
        assert 'DeviceId2' not in data
        assert 'Timestamp1' not in data
        assert 'Timestamp2' not in data
        assert 'DNI_TS' not in data
        assert 'DI_TS' not in data
        assert 'SHA1' not in data
        assert 'MD5' not in data

    def test_get_table_name(self):
        query = '(find withsource = TableName in (DeviceAlertEvents)  where Timestamp >= datetime(2023-03-16T17:21:30.000Z) and Timestamp < datetime(2023-03-18T17:30:36.000Z)  | order by Timestamp desc | where AlertId =~ "123123")'
        table = get_table_name(query)
        assert table == "DeviceAlertEvents"
        query = 'union (find withsource = TableName in (DeviceProcessEvents)  where Timestamp >= datetime(2023-03-17T20:19:41.000Z) and Timestamp < datetime(2023-03-17T20:19:42.7016812Z)  | order by Timestamp desc | where ((DeviceId =~ "1234567890abcdef1234567890abcdef12345678") and (ActionType =~ "FileModified")) and ((tostring(ProcessId) == "3892") or (tostring(InitiatingProcessId) == "3892") or (tostring(InitiatingProcessId) == "3892"))),(find withsource = TableName in (DeviceEvents)  where Timestamp >= datetime(2023-03-17T20:19:41.000Z) and Timestamp < datetime(2023-03-17T20:19:42.7016812Z)  | order by Timestamp desc | where ((DeviceId =~ "1234567890abcdef1234567890abcdef12345678") and (ActionType =~ "FileModified")) and ((tostring(ProcessId) == "3892") or (tostring(InitiatingProcessId) == "3892"))),(find withsource = TableName in (DeviceNetworkEvents)  where Timestamp >= datetime(2023-03-17T20:19:41.000Z) and Timestamp < datetime(2023-03-17T20:19:42.7016812Z)  | order by Timestamp desc | where ((DeviceId =~ "1234567890abcdef1234567890abcdef12345678") and (ActionType =~ "FileModified")) and (tostring(InitiatingProcessId) == "3892")),(find withsource = TableName in (DeviceRegistryEvents)  where Timestamp >= datetime(2023-03-17T20:19:41.000Z) and Timestamp < datetime(2023-03-17T20:19:42.7016812Z)  | order by Timestamp desc | where ((DeviceId =~ "1234567890abcdef1234567890abcdef12345678") and (ActionType =~ "FileModified")) and (tostring(InitiatingProcessId) == "3892")),(find withsource = TableName in (DeviceFileEvents)  where Timestamp >= datetime(2023-03-17T20:19:41.000Z) and Timestamp < datetime(2023-03-17T20:19:42.7016812Z)  | order by Timestamp desc | where ((DeviceId =~ "1234567890abcdef1234567890abcdef12345678") and (ActionType =~ "FileModified")) and (tostring(InitiatingProcessId) == "3892")),(find withsource = TableName in (DeviceImageLoadEvents)  where Timestamp >= datetime(2023-03-17T20:19:41.000Z) and Timestamp < datetime(2023-03-17T20:19:42.7016812Z)  | order by Timestamp desc | where ((DeviceId =~ "1234567890abcdef1234567890abcdef12345678") and (ActionType =~ "FileModified")) and (tostring(InitiatingProcessId) == "3892"))'
        table = get_table_name(query)
        assert table == "DeviceProcessEvents"

    def test_join_alerts_with_events(self):

        util = ConnectorPostProcessing(self.connection()['options'], False)
        joined_query = util.join_alert_with_events('<<timestamp>>', 'devicename', 1234)
        assert joined_query == ('(union (find withsource = TableName in (DeviceNetworkEvents)  where '
                                '(Timestamp == datetime(<<timestamp>>)) and (DeviceName == "devicename") and '
                                '(ReportId == 1234)),(find withsource = TableName in (DeviceProcessEvents)  '
                                'where (Timestamp == datetime(<<timestamp>>)) and (DeviceName == '
                                '"devicename") and (ReportId == 1234)),(find withsource = TableName in '
                                '(DeviceFileEvents)  where (Timestamp == datetime(<<timestamp>>)) and '
                                '(DeviceName == "devicename") and (ReportId == 1234)),(find withsource = '
                                'TableName in (DeviceRegistryEvents)  where (Timestamp == '
                                'datetime(<<timestamp>>)) and (DeviceName == "devicename") and (ReportId == '
                                '1234)),(find withsource = TableName in (DeviceEvents)  where (Timestamp == '
                                'datetime(<<timestamp>>)) and (DeviceName == "devicename") and (ReportId == '
                                '1234)),(find withsource = TableName in (DeviceImageLoadEvents)  where '
                                '(Timestamp == datetime(<<timestamp>>)) and (DeviceName == "devicename") and '
                                '(ReportId == 1234))) | join kind=leftouter '
                                '(DeviceInfo | project DI_TS = Timestamp, DeviceId, PublicIP, OSArchitecture, '
                                'OSPlatform, OSVersion) on DeviceId | where DI_TS < Timestamp | summarize '
                                'arg_max(DI_TS, *) by ReportId, DeviceName, Timestamp  | join kind=leftouter '
                                '(DeviceNetworkInfo | where NetworkAdapterStatus == "Up" | project DNI_TS = '
                                'Timestamp, DeviceId, MacAddress, IPAddresses | summarize '
                                'IPAddressesSet=make_set(IPAddresses), MacAddressSet=make_set(MacAddress) by '
                                'DeviceId, DNI_TS) on DeviceId | where DNI_TS < Timestamp | summarize '
                                'arg_max(DNI_TS, *) by ReportId, DeviceName, Timestamp ')

    def test_join_query_with_alerts(self):
        query = 'union (find withsource = TableName in (DeviceNetworkEvents)  where Timestamp >= datetime(2023-02-13T14:25:46.000Z) and Timestamp < datetime(2023-02-13T14:26:55.500Z)  | order by Timestamp desc | where (LocalIP =~ "9.9.9.9") or (RemoteIP =~ "9.9.9.9")),(find withsource = TableName in (DeviceEvents)  where Timestamp >= datetime(2023-02-13T14:25:46.000Z) and Timestamp < datetime(2023-02-13T14:26:55.500Z)  | order by Timestamp desc | where (RemoteIP =~ "9.9.9.9") or (LocalIP =~ "9.9.9.9"))'
        entry_point = ConnectorPostProcessing(self.connection()['options'], False)
        joined_query = entry_point.join_query_with_other_tables(query)
        assert joined_query == (
            "(union (find withsource = TableName in (DeviceNetworkEvents)  "
            "where Timestamp >= datetime(2023-02-13T14:25:46.000Z) and Timestamp < datetime(2023-02-13T14:26:55.500Z)  "
            "| order by Timestamp desc "
            "| where (LocalIP =~ \"9.9.9.9\") or (RemoteIP =~ \"9.9.9.9\")),"
            "(find withsource = TableName in (DeviceEvents)  "
            "where Timestamp >= datetime(2023-02-13T14:25:46.000Z) and Timestamp < datetime(2023-02-13T14:26:55.500Z)  "
            "| order by Timestamp desc | where (RemoteIP =~ \"9.9.9.9\") or (LocalIP =~ \"9.9.9.9\"))) "
            "| join kind=leftouter (DeviceAlertEvents | summarize AlertId=make_list(AlertId), "
            "Severity=make_list(Severity), Title=make_list(Title), Category=make_list(Category), "
            "AttackTechniques=make_list(AttackTechniques) by DeviceName, ReportId, Timestamp) "
            "on ReportId, DeviceName, Timestamp  "
            "| join kind=leftouter (DeviceInfo | project DI_TS = Timestamp, DeviceId, PublicIP, OSArchitecture, "
            "OSPlatform, OSVersion) on DeviceId | where DI_TS < Timestamp "
            "| summarize arg_max(DI_TS, *) by ReportId, DeviceName, Timestamp  "
            "| join kind=leftouter (DeviceNetworkInfo | where NetworkAdapterStatus == \"Up\" "
            "| project DNI_TS = Timestamp, DeviceId, MacAddress, IPAddresses "
            "| summarize IPAddressesSet=make_set(IPAddresses), MacAddressSet=make_set(MacAddress) by DeviceId, DNI_TS) "
            "on DeviceId | where DNI_TS < Timestamp | summarize arg_max(DNI_TS, *) by ReportId, DeviceName, Timestamp "
        )

        query = '(find withsource = TableName in (DeviceAlertEvents)  where Timestamp >= datetime(2023-03-16T17:21:30.000Z) and Timestamp < datetime(2023-03-18T17:30:36.000Z)  | order by Timestamp desc | where AlertId =~ "123123")'
        entry_point = ConnectorPostProcessing(self.connection()['options'], False)
        joined_query = entry_point.join_query_with_other_tables(query)
        assert joined_query == (
            '((find withsource = TableName in (DeviceAlertEvents)  where Timestamp >= datetime(2023-03-16T17:21:30.000Z)'
            ' and Timestamp < datetime(2023-03-18T17:30:36.000Z)  | order by Timestamp desc '
            '| where AlertId =~ "123123")) '
            '| join kind=leftouter (DeviceInfo | project DI_TS = Timestamp, DeviceId, PublicIP, OSArchitecture, '
            'OSPlatform, OSVersion) on DeviceId | where DI_TS < Timestamp | summarize arg_max(DI_TS, *) by ReportId, '
            'DeviceName, Timestamp  '
            '| join kind=leftouter (DeviceNetworkInfo | where NetworkAdapterStatus == "Up" | project DNI_TS = Timestamp,'
            ' DeviceId, MacAddress, IPAddresses | summarize IPAddressesSet=make_set(IPAddresses), '
            'MacAddressSet=make_set(MacAddress) by DeviceId, DNI_TS) on DeviceId | where DNI_TS < Timestamp '
            '| summarize arg_max(DNI_TS, *) by ReportId, DeviceName, Timestamp '
        )

    def test_join_query_no_info(self):
        query = 'union (find withsource = TableName in (DeviceNetworkEvents)  where Timestamp >= datetime(2023-02-13T14:25:46.000Z) and Timestamp < datetime(2023-02-13T14:26:55.500Z)  | order by Timestamp desc | where (LocalIP =~ "9.9.9.9") or (RemoteIP =~ "9.9.9.9")),(find withsource = TableName in (DeviceEvents)  where Timestamp >= datetime(2023-02-13T14:25:46.000Z) and Timestamp < datetime(2023-02-13T14:26:55.500Z)  | order by Timestamp desc | where (RemoteIP =~ "9.9.9.9") or (LocalIP =~ "9.9.9.9"))'
        opts = {
            "includeAlerts": True,
            "includeHostOs": False,
            "includeNetworkInfo": False,
            "retainOriginal": True
        }
        entry_point = ConnectorPostProcessing(opts, False)
        joined_query = entry_point.join_query_with_other_tables(query)
        assert joined_query == (
            "(union (find withsource = TableName in (DeviceNetworkEvents)  "
            "where Timestamp >= datetime(2023-02-13T14:25:46.000Z) and Timestamp < datetime(2023-02-13T14:26:55.500Z)  "
            "| order by Timestamp desc "
            "| where (LocalIP =~ \"9.9.9.9\") or (RemoteIP =~ \"9.9.9.9\")),"
            "(find withsource = TableName in (DeviceEvents)  "
            "where Timestamp >= datetime(2023-02-13T14:25:46.000Z) and Timestamp < datetime(2023-02-13T14:26:55.500Z)  "
            "| order by Timestamp desc | where (RemoteIP =~ \"9.9.9.9\") or (LocalIP =~ \"9.9.9.9\"))) "
            "| join kind=leftouter (DeviceAlertEvents | summarize AlertId=make_list(AlertId), "
            "Severity=make_list(Severity), Title=make_list(Title), Category=make_list(Category), "
            "AttackTechniques=make_list(AttackTechniques) by DeviceName, ReportId, Timestamp) "
            "on ReportId, DeviceName, Timestamp "
        )

        query = '(find withsource = TableName in (DeviceAlertEvents)  where Timestamp >= datetime(2023-03-16T17:21:30.000Z) and Timestamp < datetime(2023-03-18T17:30:36.000Z)  | order by Timestamp desc | where AlertId =~ "123123")'
        entry_point = ConnectorPostProcessing(opts, False)
        joined_query = entry_point.join_query_with_other_tables(query)
        assert joined_query == (
            '((find withsource = TableName in (DeviceAlertEvents)  where Timestamp >= datetime(2023-03-16T17:21:30.000Z)'
            ' and Timestamp < datetime(2023-03-18T17:30:36.000Z)  | order by Timestamp desc '
            '| where AlertId =~ "123123"))'
        )

    def test_join_query_no_alerts(self):
        query = 'union (find withsource = TableName in (DeviceNetworkEvents)  where Timestamp >= datetime(2023-02-13T14:25:46.000Z) and Timestamp < datetime(2023-02-13T14:26:55.500Z)  | order by Timestamp desc | where (LocalIP =~ "9.9.9.9") or (RemoteIP =~ "9.9.9.9")),(find withsource = TableName in (DeviceEvents)  where Timestamp >= datetime(2023-02-13T14:25:46.000Z) and Timestamp < datetime(2023-02-13T14:26:55.500Z)  | order by Timestamp desc | where (RemoteIP =~ "9.9.9.9") or (LocalIP =~ "9.9.9.9"))'
        opts = {
            "includeAlerts": False,
            "includeHostOs": True,
            "includeNetworkInfo": True,
            "retainOriginal": True
        }
        entry_point = ConnectorPostProcessing(opts, False)
        joined_query = entry_point.join_query_with_other_tables(query)
        assert joined_query == (
            "(union (find withsource = TableName in (DeviceNetworkEvents)  "
            "where Timestamp >= datetime(2023-02-13T14:25:46.000Z) and Timestamp < datetime(2023-02-13T14:26:55.500Z)  "
            "| order by Timestamp desc "
            "| where (LocalIP =~ \"9.9.9.9\") or (RemoteIP =~ \"9.9.9.9\")),"
            "(find withsource = TableName in (DeviceEvents)  "
            "where Timestamp >= datetime(2023-02-13T14:25:46.000Z) and Timestamp < datetime(2023-02-13T14:26:55.500Z)  "
            "| order by Timestamp desc | where (RemoteIP =~ \"9.9.9.9\") or (LocalIP =~ \"9.9.9.9\"))) "
            "| join kind=leftouter (DeviceInfo | project DI_TS = Timestamp, DeviceId, PublicIP, OSArchitecture, "
            "OSPlatform, OSVersion) on DeviceId | where DI_TS < Timestamp "
            "| summarize arg_max(DI_TS, *) by ReportId, DeviceName, Timestamp  "
            "| join kind=leftouter (DeviceNetworkInfo | where NetworkAdapterStatus == \"Up\" "
            "| project DNI_TS = Timestamp, DeviceId, MacAddress, IPAddresses "
            "| summarize IPAddressesSet=make_set(IPAddresses), MacAddressSet=make_set(MacAddress) by DeviceId, DNI_TS) "
            "on DeviceId | where DNI_TS < Timestamp | summarize arg_max(DNI_TS, *) by ReportId, DeviceName, Timestamp "
        )

        query = '(find withsource = TableName in (DeviceAlertEvents)  where Timestamp >= datetime(2023-03-16T17:21:30.000Z) and Timestamp < datetime(2023-03-18T17:30:36.000Z)  | order by Timestamp desc | where AlertId =~ "123123")'
        entry_point = ConnectorPostProcessing(opts, False)
        joined_query = entry_point.join_query_with_other_tables(query)
        assert joined_query == (
            '((find withsource = TableName in (DeviceAlertEvents)  where Timestamp >= datetime(2023-03-16T17:21:30.000Z)'
            ' and Timestamp < datetime(2023-03-18T17:30:36.000Z)  | order by Timestamp desc '
            '| where AlertId =~ "123123")) '
            '| join kind=leftouter (DeviceInfo | project DI_TS = Timestamp, DeviceId, PublicIP, OSArchitecture, '
            'OSPlatform, OSVersion) on DeviceId | where DI_TS < Timestamp | summarize arg_max(DI_TS, *) by ReportId, '
            'DeviceName, Timestamp  '
            '| join kind=leftouter (DeviceNetworkInfo | where NetworkAdapterStatus == "Up" | project DNI_TS = Timestamp,'
            ' DeviceId, MacAddress, IPAddresses | summarize IPAddressesSet=make_set(IPAddresses), '
            'MacAddressSet=make_set(MacAddress) by DeviceId, DNI_TS) on DeviceId | where DNI_TS < Timestamp '
            '| summarize arg_max(DNI_TS, *) by ReportId, DeviceName, Timestamp '
        )

    def test_join_query_only_events(self):
        query = 'union (find withsource = TableName in (DeviceNetworkEvents)  where Timestamp >= datetime(2023-02-13T14:25:46.000Z) and Timestamp < datetime(2023-02-13T14:26:55.500Z)  | order by Timestamp desc | where (LocalIP =~ "9.9.9.9") or (RemoteIP =~ "9.9.9.9")),(find withsource = TableName in (DeviceEvents)  where Timestamp >= datetime(2023-02-13T14:25:46.000Z) and Timestamp < datetime(2023-02-13T14:26:55.500Z)  | order by Timestamp desc | where (RemoteIP =~ "9.9.9.9") or (LocalIP =~ "9.9.9.9"))'
        opts = {
            "includeAlerts": False,
            "includeHostOs": False,
            "includeNetworkInfo": False,
            "retainOriginal": True
        }
        entry_point = ConnectorPostProcessing(opts, False)
        joined_query = entry_point.join_query_with_other_tables(query)
        assert joined_query == (
            "(union (find withsource = TableName in (DeviceNetworkEvents)  "
            "where Timestamp >= datetime(2023-02-13T14:25:46.000Z) and Timestamp < datetime(2023-02-13T14:26:55.500Z)  "
            "| order by Timestamp desc "
            "| where (LocalIP =~ \"9.9.9.9\") or (RemoteIP =~ \"9.9.9.9\")),"
            "(find withsource = TableName in (DeviceEvents)  "
            "where Timestamp >= datetime(2023-02-13T14:25:46.000Z) and Timestamp < datetime(2023-02-13T14:26:55.500Z)  "
            "| order by Timestamp desc | where (RemoteIP =~ \"9.9.9.9\") or (LocalIP =~ \"9.9.9.9\")))"
        )

        query = '(find withsource = TableName in (DeviceAlertEvents)  where Timestamp >= datetime(2023-03-16T17:21:30.000Z) and Timestamp < datetime(2023-03-18T17:30:36.000Z)  | order by Timestamp desc | where AlertId =~ "123123")'
        entry_point = ConnectorPostProcessing(opts, False)
        joined_query = entry_point.join_query_with_other_tables(query)
        assert joined_query == (
            '((find withsource = TableName in (DeviceAlertEvents)  where Timestamp >= datetime(2023-03-16T17:21:30.000Z)'
            ' and Timestamp < datetime(2023-03-18T17:30:36.000Z)  | order by Timestamp desc '
            '| where AlertId =~ "123123"))'
        )

    def test_unify_alert_fields(self):
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

        unify_alert_fields(data)
        alerts = data.get("Alerts")
        assert alerts is not None
        assert type(alerts) is str
        alerts = json.loads(alerts)
        assert len(alerts) == 1
        alert = alerts[0]
        assert alert.get("AlertId") == 'da111111111111111111_-1111111111'
        assert alert.get("Title") == 'Suspicious URL clicked'
        ttps = alert.get("AttackTechniques")
        assert ttps is not None
        assert len(ttps) == 1
        ttp = ttps[0]
        assert ttp == 'Spearphishing Link (T1566.002)'

    def test_organize_registry_data(self):
        data = {
            "DeviceRegistryEvents": {
                "TableName": "DeviceRegistryEvents",
                "Timestamp": "2019-10-10T10:43:07.2363291Z",
                "DeviceId": "db40e68dd7358aa450081343587941ce96ca4777",
                "DeviceName": "testmachine1",
                "ActionType": "RegistryValueSet",
                "RegistryKey": "HKEY_LOCAL_MACHINE\\\\SYSTEM\\\\ControlSet001\\\\Services\\\\WindowsAzureGuestAgent",
                "RegistryValueType": "Binary",
                "RegistryValueName": "FailureActions",
                "RegistryValueData": ""
            }
        }

        organize_registry_data(data["DeviceRegistryEvents"])
        assert "RegistryValues" in data["DeviceRegistryEvents"]
        values = data["DeviceRegistryEvents"]["RegistryValues"]
        assert len(values) == 1
        val = values[0]
        assert val.get("RegistryValueType") == "Binary"
        assert val.get("RegistryValueName") == "FailureActions"
        assert val.get("RegistryValueData") == ""

    def test_organize_ips(self):
        data = {
            "DeviceRegistryEvents": {
                "IPAddressesSet": ["[{\"IPAddress\":\"9.9.9.9\",\"SubnetPrefix\":24,\"AddressType\":\"Private\"}]"]
            }
        }
        organize_ips(data["DeviceRegistryEvents"])
        assert "IPAddresses" in data["DeviceRegistryEvents"]
        values = data["DeviceRegistryEvents"]["IPAddresses"]
        assert len(values) == 1
        assert values[0] == "9.9.9.9"

    def test_create_event_link(self):
        data = {
            "DeviceId": "deviceid"
        }
        create_event_link(data, "2019-10-10T10:43:07.2363291Z")
        assert data.get(
            "event_link") == "https://security.microsoft.com/machines/deviceid/timeline?from=2019-10-10T10:43:06.000Z&to=2019-10-10T10:43:08.000Z"

    def test_remove_duplicate_ips(self):
        data = {
            "PublicIP": "9.9.9.9",
            "LocalIP": "9.9.9.9",
            "IPAddresses": ["9.9.9.9", "9.9.9.1"]
        }
        remove_duplicate_ips(data)
        assert "PublicIP" not in data
        assert data.get("LocalIP") == "9.9.9.9"
        assert len(data["IPAddresses"]) == 1
        assert data["IPAddresses"][0] == "9.9.9.1"

    def test_do_not_remove_duplicate_ips(self):
        data = {
            "PublicIP": "9.9.9.1",
            "LocalIP": "9.9.9.2",
            "IPAddresses": ["9.9.9.3", "9.9.9.4"]
        }
        remove_duplicate_ips(data)
        assert data.get("PublicIP") == "9.9.9.1"
        assert data.get("LocalIP") == "9.9.9.2"
        assert len(data["IPAddresses"]) == 2
