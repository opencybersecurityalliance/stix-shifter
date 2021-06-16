import unittest
from datetime import datetime, timedelta
from stix_shifter_modules.carbonblack.stix_transmission.event_parser import parse_raw_event_to_obj, \
  create_event_obj, str_event_fields, format_timestamp, get_common_fields_as_dict, get_timestamp_by_event_type, \
  extract_time_window, is_timestamp_in_window

process_response = {
                       "unique_id": "00000003-0000-6248-01d7-298f8ee90bb5-01789e8c0344",
                       "parent_unique_id": "00000003-0000-07f8-01d7-26d5147451aa-000000000001",
                       "id": "00000003-0000-6248-01d7-298f8ee90bb5",
                       "parent_id": "00000003-0000-07f8-01d7-26d5147451aa",
                       "path": "c:\\windows\\system32\\wermgr.exe",
                       "process_name": "wermgr.exe",
                       "process_md5": "df2ad28ac6bedf07422537cca6f1e637",
                       "parent_name": "svchost.exe",
                       "parent_md5": "00000000000000000000000000000000",
                       "hostname": "il009210-tp",
                       "host_type": "workstation",
                       "os_type": "windows",
                       "start": "2021-04-04T20:17:38.541Z",
                       "last_update": "2021-04-04T20:17:38.768Z",
                       "last_server_update": "2021-04-04T20:21:19.317Z",
                       "sensor_id": 3,
                       "group": "default group",
                       "segment_id": 1617567679300,
                       "username": "NT AUTHORITY\\SYSTEM",
                       "cmdline": "C:\\WINDOWS\\system32\\wermgr.exe -upload",
                       "process_pid": 25160,
                       "parent_pid": 2040,
                       "comms_ip": 1833104680,
                       "interface_ip": -1062728174,
                       "emet_config": "",
                       "terminated": True,
                       "filtering_known_dlls": False,
                       "logon_type": 0,
                       "process_sha256": "edce588f879e657b24037dd0ae3233c97ce9b0e4a115c62bbf00c983ef288a85",
                       "regmod_count": 0,
                       "netconn_count": 0,
                       "filemod_count": 4,
                       "modload_count": 9,
                       "childproc_count": 0,
                       "crossproc_count": 1,
                       "emet_count": 0,
                       "processblock_count": 0
                   }

events_response = {
    "elapsed": 0.015361785888671875,
    "process": {
        "unique_id": "00000003-0000-0dc8-01d7-26d53c822403-01789e14fa99",
        "sensor_id": 3,
        "hostname": "il009210-tp",
        "group": "default group",
        "os_type": "windows",
        "host_type": "workstation",
        "interface_ip": -1062728174,
        "comms_ip": 1833104680,
        "parent_unique_id": "00000003-0000-2384-01d7-26d52f68447c-000000000001",
        "start": "2021-04-01T08:58:51.577Z",
        "process_pid": 3528,
        "parent_pid": 9092,
        "process_md5": "51261edd1dc7e42b248933ce73233965",
        "process_sha256": "ec3e1a591bb2a45ce4ae235d897cfeac4b0a73e45ef6098fc2570ba3b6870587",
        "cmdline": "\"C:\\Program Files\\JetBrains\\PyCharm Community Edition 2020.1\\bin\\pycharm64.exe\" ",
        "uid": "S-1-12-1-112158317-1126071847-2977658009-3312164563",
        "username": "AzureAD\\BarHaim",
        "parent_name": "explorer.exe",
        "path": "c:\\program files\\jetbrains\\pycharm community edition 2020.1\\bin\\pycharm64.exe",
        "process_name": "pycharm64.exe",
        "modload_count": 157,
        "filemod_count": 2911,
        "regmod_count": 10,
        "netconn_count": 193,
        "childproc_count": 4,
        "crossproc_count": 22,
        "emet_count": 0,
        "processblock_count": 0,
        "logon_type": 2,
        "netconn_complete": [
            {
                "timestamp": "2021-04-04T18:10:24.835Z",
                "proto": 6,
                "domain": "resources.jetbrains.com",
                "direction": "true",
                "local_ip": "192.168.14.18",
                "local_port": 58380,
                "remote_ip": "99.86.3.45",
                "remote_port": 443,
                "ja3": "6f0d86606b7ca191fbd2c072e4f99f9f",
                "ja3s": "f4febc55ea12b31ae17cfb7e614afda8"
            }
        ],
        "childproc_complete": [
            {
                "md5": "b3c9a18f42d7ce1c170f25aaeabeeed9",
                "path": "c:\\program files\\jetbrains\\pycharm community edition 2020.1\\bin\\runnerw64.exe",
                "commandLine": "",
                "userName": "",
                "sha256": "2dc52cc1954d40065f80526bacb24c34914a89b3e5c56d095728d8e9bc88ea09",
                "pid": 10412,
                "processId": "00000003-0000-28ac-01d7-297dbe9666ff-000000000001",
                "is_suppressed": False,
                "is_tampered": False,
                "type": "end",
                "end": "2021-04-04T18:10:08.548000Z"
            }
        ],
        "regmod_complete": [
            "2|2021-04-04 18:11:40.309|\\\\registry\\\\machine\\\\software\\\\microsoft\\\\windows advanced threat protection\\\\crashheartbeat|false"
        ],
        "modload_complete": [
            "2021-04-04 18:11:41.244|756df8beaf018e982e2383702d905729|c:\\windows\\system32\\wbem\\wbemdisp.dll|59f90d11bd50cad4617151baea43bcf878cadc5fb0da5d07f461b2c2657b9ee1"
        ],
        "crossproc_complete": [
            "ProcessOpen|2021-04-04 18:11:31.938|00000003-0000-4e1c-01d7-297df0a23e43-000000000001|f586835082f632dc8d9404d83bc16316|c:\\windows\\system32\\svchost.exe|1|5200|false|false|643ec58e82e0272c97c2a59f6020970d881af19c0ad5029db9c958c13b6558c7"
        ],
        "filemod_complete": [
            "1|2021-04-04 20:17:38.590000|c:\\programdata\\microsoft\\windows\\wer\\temp\\7fb39f69-3a0a-4b59-8afb-0bd9667730d1||0||",
        ],
        "last_update": "2021-04-04T18:10:24.835Z",
        "last_server_update": "2021-04-04T18:11:18.321Z",
        "terminated": False,
        "id": "00000003-0000-0dc8-01d7-26d53c822403",
        "parent_id": "00000003-0000-2384-01d7-26d52f68447c",
        "segment_id": 1617559878297,
        "filtering_known_dlls": False,
        "min_last_server_update": "2021-04-04T18:11:18.321Z",
        "max_last_server_update": "2021-04-04T18:11:18.321Z",
        "min_last_update": "2021-04-04T18:10:24.835Z",
        "max_last_update": "2021-04-04T18:10:24.835Z",
        "binaries": {
            "B3C9A18F42D7CE1C170F25AAEABEEED9": {
                "digsig_result": "Signed",
                "digsig_publisher": "JetBrains s.r.o."
            }
        },
        "fork_children_count": 0,
        "exec_events_count": 0
    }
}


class TestCarbonBlackEventParser(unittest.TestCase, object):

    @staticmethod
    def check_str_event(event_type, raw_event_str):
        event_obj = parse_raw_event_to_obj(event_type, raw_event_str)  # str form transformed to obj
        assert isinstance(event_obj, dict) and len(event_obj.keys()) == len(str_event_fields[event_type])
        return event_obj

    def test_parse_raw_event(self):
        raw_event_obj = None
        assert parse_raw_event_to_obj('netconn', raw_event_obj) is None

        raw_event_str = ""
        assert parse_raw_event_to_obj('unknown', raw_event_str) is None

        unknown_event = create_event_obj(process_response, {'parsed_event_data': None})
        assert unknown_event is None

        raw_event_obj = events_response['process']['netconn_complete'][0]
        event_obj = parse_raw_event_to_obj('netconn', raw_event_obj)
        timestamp = get_timestamp_by_event_type(event_obj=event_obj, event_type='netconn')
        assert event_obj == raw_event_obj  # object form stays as-is
        event_obj['parsed_timestamp'] = format_timestamp(timestamp)
        netconn_event = create_event_obj(process_response, {'event_type': 'netconn', 'parsed_event_data': event_obj})
        assert netconn_event.get('process_name') == "wermgr.exe"
        assert netconn_event.get('domain') == "resources.jetbrains.com"
        assert netconn_event.get('netconn_remote_port') == 443
        assert netconn_event.get('netconn_remote_ipv4') == "99.86.3.45"
        assert netconn_event.get('netconn_local_port') == 58380
        assert netconn_event.get('netconn_local_ipv4') == "192.168.14.18"
        assert netconn_event.get('event_timestamp') == "2021-04-04T18:10:24.835000Z"

        raw_event_obj = events_response['process']['childproc_complete'][0]
        event_obj = parse_raw_event_to_obj('childproc', raw_event_obj)
        timestamp = get_timestamp_by_event_type(event_obj=event_obj, event_type='childproc')
        assert event_obj == raw_event_obj  # object form stays as-is
        event_obj['parsed_timestamp'] = format_timestamp(timestamp)
        childproc_event = create_event_obj(process_response, {'event_type': 'childproc', 'parsed_event_data': event_obj})
        assert childproc_event.get('process_name') == "wermgr.exe"
        assert childproc_event.get('childproc_name') == "c:\\program files\\jetbrains\\pycharm community edition 2020.1\\bin\\runnerw64.exe"
        assert childproc_event.get('childproc_md5') == "b3c9a18f42d7ce1c170f25aaeabeeed9"
        assert childproc_event.get('childproc_sha256') == "2dc52cc1954d40065f80526bacb24c34914a89b3e5c56d095728d8e9bc88ea09"
        assert childproc_event.get('childproc_cmdline') == ""
        assert childproc_event.get('childproc_username') == ""
        assert childproc_event.get('childproc_pid') == 10412
        assert childproc_event.get('event_timestamp') == "2021-04-04T18:10:08.548000Z"

        raw_event_str = events_response['process']['regmod_complete'][0]
        event_obj = TestCarbonBlackEventParser.check_str_event('regmod', raw_event_str)
        timestamp = get_timestamp_by_event_type(event_obj=event_obj, event_type='regmod')
        event_obj['parsed_timestamp'] = format_timestamp(timestamp)
        regmod_event = create_event_obj(process_response, {'event_type': 'regmod', 'parsed_event_data': event_obj})
        assert regmod_event.get('process_name') == "wermgr.exe"
        assert regmod_event.get('regmod_name') == "\\\\registry\\\\machine\\\\software\\\\microsoft\\\\windows advanced threat protection\\\\crashheartbeat"
        assert regmod_event.get('regmod_action') == "First wrote to the registry key"
        assert regmod_event.get('event_timestamp') == '2021-04-04T18:11:40.309000Z'

        raw_event_str = events_response['process']['modload_complete'][0]
        event_obj = TestCarbonBlackEventParser.check_str_event('modload', raw_event_str)
        timestamp = get_timestamp_by_event_type(event_obj=event_obj, event_type='modload')
        event_obj['parsed_timestamp'] = format_timestamp(timestamp)
        modload_event = create_event_obj(process_response, {'event_type': 'modload', 'parsed_event_data': event_obj})
        assert modload_event.get('process_name') == "wermgr.exe"
        assert modload_event.get('modload_name') == 'c:\\windows\\system32\\wbem\\wbemdisp.dll'
        assert modload_event.get('modload_md5') == "756df8beaf018e982e2383702d905729"
        assert modload_event.get('event_timestamp') == '2021-04-04T18:11:41.244000Z'

        raw_event_str = events_response['process']['crossproc_complete'][0]
        event_obj = TestCarbonBlackEventParser.check_str_event('crossproc', raw_event_str)
        timestamp = get_timestamp_by_event_type(event_obj=event_obj, event_type='crossproc')
        event_obj['parsed_timestamp'] = format_timestamp(timestamp)
        crossproc_event = create_event_obj(process_response, {'event_type': 'crossproc', 'parsed_event_data': event_obj})
        assert crossproc_event.get('process_name') == "wermgr.exe"
        assert crossproc_event.get('crossproc_name') == "c:\\windows\\system32\\svchost.exe"
        assert crossproc_event.get('crossproc_action') == "ProcessOpen"
        assert crossproc_event.get('crossproc_md5') == "f586835082f632dc8d9404d83bc16316"
        assert crossproc_event.get('event_timestamp') == '2021-04-04T18:11:31.938000Z'

        raw_event_str = events_response['process']['filemod_complete'][0]
        event_obj = TestCarbonBlackEventParser.check_str_event('filemod', raw_event_str)
        timestamp = get_timestamp_by_event_type(event_obj=event_obj, event_type='filemod')
        event_obj['parsed_timestamp'] = format_timestamp(timestamp)
        filemod_event = create_event_obj(process_response, {'event_type': 'filemod', 'parsed_event_data': event_obj})
        assert filemod_event.get('process_name') == "wermgr.exe"
        assert filemod_event.get('filemod_name') == "c:\\programdata\\microsoft\\windows\\wer\\temp\\7fb39f69-3a0a-4b59-8afb-0bd9667730d1"
        assert filemod_event.get('filemod_action') == "Created the file"
        assert filemod_event.get('filemod_md5') == ""
        assert filemod_event.get('event_timestamp') == '2021-04-04T20:17:38.590000Z'

        unknown_event = create_event_obj(process_response, {'event_type': 'unknown', 'parsed_event_data': event_obj})
        assert unknown_event is None

    def test_format_timestamp(self):
        input_timestamp = None
        assert format_timestamp(input_timestamp) is None

        input_timestamp = "not-datetime"
        assert format_timestamp(input_timestamp) == "not-datetime"

        input_timestamp = datetime.strptime('2021-04-04T20:17:38.59', '%Y-%m-%dT%H:%M:%S.%f')
        assert format_timestamp(input_timestamp) == '2021-04-04T20:17:38.590000Z'

    def test_extract_time_window(self):
        query = '(process_name:erl.exe)'
        time_window = extract_time_window(query)
        assert time_window is None

        query = '(process_name:erl.exe) and last_update:[2021-04-22T11:09:00 TO 2021-04-22T11:39:00]'
        time_window = extract_time_window(query)
        assert len(time_window) == 2
        assert time_window[0] == datetime(2021, 4, 22, 11, 9)
        assert time_window[1] == datetime(2021, 4, 22, 11, 39)

        query = '((process_name:erl.exe) and last_update:-5m)'
        time_window = extract_time_window(query)
        time_diff: timedelta = time_window[1] - time_window[0]
        assert len(time_window) == 2
        assert time_diff.total_seconds() == 5 * 60

    def test_get_timestamp_by_event_type(self):
        netconn_event = {'timestamp': "2021-04-04T18:10:24.835Z"}
        timestamp = get_timestamp_by_event_type(netconn_event, 'w00t')
        assert timestamp is None

        timestamp = get_timestamp_by_event_type(netconn_event, 'netconn')
        assert timestamp == datetime(2021, 4, 4, 18, 10, 24, 835000)

        childproc_event = {'end': "2021-04-04T18:10:24.835Z", 'type': 'end'}
        timestamp = get_timestamp_by_event_type(childproc_event, 'childproc')
        assert timestamp == datetime(2021, 4, 4, 18, 10, 24, 835000)

        childproc_event = {'end': "2021-04-04T18:10:24Z", 'type': 'end'}
        timestamp = get_timestamp_by_event_type(childproc_event, 'childproc')
        assert timestamp == datetime(2021, 4, 4, 18, 10, 24)

        childproc_event = {'end': "not-datetime", 'type': 'end'}
        timestamp = get_timestamp_by_event_type(childproc_event, 'childproc')
        assert timestamp is None

        regmod_event = {'event_time': '2021-04-04 18:11:40.309'}
        timestamp = get_timestamp_by_event_type(regmod_event, 'regmod')
        assert timestamp == datetime(2021, 4, 4, 18, 11, 40, 309000)

    def test_is_timestamp_in_window(self):
        query = '(process_name:erl.exe) and last_update:[2021-04-22T11:09:00 TO 2021-04-22T11:10:00]'
        time_window = extract_time_window(query)
        timestamp = datetime(2021, 4, 22, 11, 9, 40)
        assert is_timestamp_in_window(timestamp, time_window) is True

        timestamp = datetime(2021, 4, 22, 11, 5, 40)
        assert is_timestamp_in_window(timestamp, time_window) is False

        assert is_timestamp_in_window(timestamp, None) is False
        assert is_timestamp_in_window(None, time_window) is False

    def test_get_process_common_fields(self):
        common_fields = get_common_fields_as_dict(process_response)
        assert isinstance(common_fields, dict)
        assert 'device_os' in common_fields
        assert 'device_name' in common_fields
        assert 'host_type' in common_fields
        assert 'process_pid' in common_fields
        assert 'process_name' in common_fields
        assert 'parent_pid' in common_fields
        assert 'parent_name' in common_fields
        assert 'process_cmdline' in common_fields
        assert 'interface_ip' in common_fields
        assert 'device_external_ip' in common_fields
        assert 'provider' in common_fields
