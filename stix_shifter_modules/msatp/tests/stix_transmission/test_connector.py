from stix_shifter_modules.msatp.stix_transmission import connector
from stix_shifter_modules.msatp.tests.test_utils import all_keys_in_object


def test_merge_alert_events():
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
    merged = connector.merge_alert_events(data)
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


def test_remove_uplicate_fields():
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
    }
    cleaned = connector.remove_duplicate_fields(data)
    assert all_keys_in_object({'ReportId', 'DeviceName', 'DeviceId', 'Timestamp', 'TableName',
                               'InitiatingProcessSHA1', 'InitiatingProcessSHA256', 'InitiatingProcessMD5'}, cleaned)
    assert 'DeviceId1' not in cleaned
    assert 'DeviceId2' not in cleaned
    assert 'Timestamp1' not in cleaned
    assert 'Timestamp2' not in cleaned


def test_get_table_name():
    query = '(find withsource = TableName in (DeviceAlertEvents)  where Timestamp >= datetime(2023-03-16T17:21:30.000Z) and Timestamp < datetime(2023-03-18T17:30:36.000Z)  | order by Timestamp desc | where AlertId =~ "123123")'
    table = connector.get_table_name(query)
    assert table == "DeviceAlertEvents"
    query = 'union (find withsource = TableName in (DeviceProcessEvents)  where Timestamp >= datetime(2023-03-17T20:19:41.000Z) and Timestamp < datetime(2023-03-17T20:19:42.7016812Z)  | order by Timestamp desc | where ((DeviceId =~ "1234567890abcdef1234567890abcdef12345678") and (ActionType =~ "FileModified")) and ((tostring(ProcessId) == "3892") or (tostring(InitiatingProcessId) == "3892") or (tostring(InitiatingProcessId) == "3892"))),(find withsource = TableName in (DeviceEvents)  where Timestamp >= datetime(2023-03-17T20:19:41.000Z) and Timestamp < datetime(2023-03-17T20:19:42.7016812Z)  | order by Timestamp desc | where ((DeviceId =~ "1234567890abcdef1234567890abcdef12345678") and (ActionType =~ "FileModified")) and ((tostring(ProcessId) == "3892") or (tostring(InitiatingProcessId) == "3892"))),(find withsource = TableName in (DeviceNetworkEvents)  where Timestamp >= datetime(2023-03-17T20:19:41.000Z) and Timestamp < datetime(2023-03-17T20:19:42.7016812Z)  | order by Timestamp desc | where ((DeviceId =~ "1234567890abcdef1234567890abcdef12345678") and (ActionType =~ "FileModified")) and (tostring(InitiatingProcessId) == "3892")),(find withsource = TableName in (DeviceRegistryEvents)  where Timestamp >= datetime(2023-03-17T20:19:41.000Z) and Timestamp < datetime(2023-03-17T20:19:42.7016812Z)  | order by Timestamp desc | where ((DeviceId =~ "1234567890abcdef1234567890abcdef12345678") and (ActionType =~ "FileModified")) and (tostring(InitiatingProcessId) == "3892")),(find withsource = TableName in (DeviceFileEvents)  where Timestamp >= datetime(2023-03-17T20:19:41.000Z) and Timestamp < datetime(2023-03-17T20:19:42.7016812Z)  | order by Timestamp desc | where ((DeviceId =~ "1234567890abcdef1234567890abcdef12345678") and (ActionType =~ "FileModified")) and (tostring(InitiatingProcessId) == "3892")),(find withsource = TableName in (DeviceImageLoadEvents)  where Timestamp >= datetime(2023-03-17T20:19:41.000Z) and Timestamp < datetime(2023-03-17T20:19:42.7016812Z)  | order by Timestamp desc | where ((DeviceId =~ "1234567890abcdef1234567890abcdef12345678") and (ActionType =~ "FileModified")) and (tostring(InitiatingProcessId) == "3892"))'
    table = connector.get_table_name(query)
    assert table == "DeviceProcessEvents"

