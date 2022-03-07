import unittest
from copy import deepcopy
from unittest.mock import patch
from stix_shifter_modules.carbonblack.entry_point import EntryPoint
from stix_shifter_modules.carbonblack.tests.stix_transmission.test_carbonblack import RequestMockResponse

config = {
    "auth": {
        "token": "bla"
    }
}
connection = {
    "host": "hostbla",
    "port": 8080,
    "options": {
        "events_mode": True
    }
}


class TestCarbonBlackEventsConnection(unittest.TestCase, object):

    @staticmethod
    def _get_mock_process_and_events_data():
        mocked_process_return_value = """
{
  "terms": [
    "process_name:erl.exe and last_update:[2021-03-15T16:20:00 TO 2021-03-15T16:30:00]"
  ],
  "results": [
    {
      "process_md5": "5746bd7e255dd6a8afa06f7c42c1ba41",
      "sensor_id": 49,
      "filtering_known_dlls": true,
      "modload_count": 3,
      "parent_unique_id": "00000031-0000-09cc-01d4-b1e61979dd7c-000000000001",
      "emet_count": 0,
      "alliance_score_srstrust": -100,
      "cmdline": "C:\\\\Windows\\\\system32\\\\cmd.exe /c tasklist",
      "alliance_updated_srstrust": "2018-04-05T16:04:34Z",
      "filemod_count": 0,
      "id": "00000031-0000-0768-01d4-b1e6197c3edd",
      "parent_name": "cmd.exe",
      "parent_md5": "000000000000000000000000000000",
      "group": "lab1",
      "parent_id": "00000031-0000-09cc-01d4-b1e61979dd7c",
      "hostname": "lab1-host1",
      "last_update": "2019-01-22T00:04:52.937Z",
      "start": "2019-01-22T00:04:52.875Z",
      "alliance_link_srstrust": "https://example.com",
      "comms_ip": 212262914,
      "regmod_count": 0,
      "interface_ip": 183439304,
      "process_pid": 1896,
      "username": "SYSTEM",
      "terminated": true,
      "alliance_data_srstrust": [
        "5746bd7e255dd6a8afa06f7c42c1ba41"
      ],
      "process_name": "erl.exe",
      "emet_config": "",
      "last_server_update": "2019-01-22T00:07:07.064Z",
      "path": "c:\\\\windows\\\\system32\\\\cmd.exe",
      "netconn_count": 0,
      "parent_pid": 2508,
      "crossproc_count": 2,
      "segment_id": 1548115627056,
      "host_type": "workstation",
      "processblock_count": 0,
      "os_type": "windows",
      "childproc_count": 4,
      "unique_id": "00080031-0000-0748-01d4-b1e61c7c3edd-016872e1cb30"
    }
  ],

  "elapsed": 0.05147600173950195,
  "comprehensive_search": true,
  "all_segments": true,
  "total_results": 1,
  "highlights": [],
  "facets": {},
  "tagged_pids": {},
  "start": 0,
  "incomplete_results": false,
  "filtered": {}
}
"""
        mocked_events_return_value = """
{
  "elapsed": 0.00452113151550293,
  "process": {
    "unique_id": "00000001-0000-0f10-01d7-179ac0bc1400-017836b69e2c",
    "sensor_id": 1,
    "hostname": "win01",
    "group": "default group",
    "os_type": "windows",
    "host_type": "server",
    "interface_ip": 160756778,
    "comms_ip": -1626848542,
    "parent_unique_id": "00000001-0000-003c-01d7-179a8c44ed5c-000000000001",
    "start": "2021-03-12T23:52:25.667Z",
    "process_pid": 3856,
    "parent_pid": 60,
    "process_md5": "06c66ff5ccdc2d22344a3eb761a4d38a",
    "process_sha256": "b5c78bef3883e3099f7ef844da1446db29107e5c0223b97f29e7fafab5527f15",
    "cmdline": "C:\\\\Windows\\\\system32\\\\wbem\\\\wmiprvse.exe -secured -Embedding",
    "uid": "s-1-5-20",
    "username": "NT AUTHORITY\\\\NETWORK SERVICE",
    "parent_name": "svchost.exe",
    "path": "c:\\\\windows\\\\system32\\\\wbem\\\\wmiprvse.exe",
    "process_name": "wmiprvse.exe",
    "modload_count": 671,
    "filemod_count": 70,
    "regmod_count": 2,
    "netconn_count": 2,
    "childproc_count": 0,
    "crossproc_count": 107,
    "emet_count": 0,
    "processblock_count": 0,
    "logon_type": 5,
    "modload_complete": [
      "2021-03-15 16:26:14.566|450e6430481940a25e7b268dcc29a6d4|c:\\\\windows\\\\system32\\\\security.dll|b25396c5300483595967adce4eb4d2337876695bba7b1f6021f2a63788c60af4",
      "2021-03-15 16:26:14.566|6e13163214c64bd6453fbe3af96f8944|c:\\\\windows\\\\system32\\\\secur32.dll|1cafa15cba7a29317359c6851292470e01b36ff92d9df2e2c9474c3b02036305",
      "2021-03-15 16:26:14.582|fa6aa982ddf1b76de85e7dcee1a929a7|c:\\\\windows\\\\system32\\\\netapi32.dll|4f13048a6699d50c780db9d072a2ca3c30294ccedcc411167e49c4e8fdedca6e",
      "2021-03-15 16:36:14.582|6debee59947584cfcb818ed7d4017ed8|c:\\\\windows\\\\system32\\\\schedcli.dll|5100efdacdf9c3f323d9240190e31c4953e7a0440d4ee6385e33de52467f1396"
    ],
    "last_update": "2021-03-15T16:26:14.582Z",
    "last_server_update": "2021-03-15T16:27:21.017Z",
    "terminated": false,
    "id": "00000001-0000-0f10-01d7-179ac0bc1400",
    "parent_id": "00000001-0000-003c-01d7-179a8c44ed5c",
    "segment_id": 1615825641004,
    "filtering_known_dlls": false,
    "min_last_server_update": "2021-03-15T16:27:21.017Z",
    "max_last_server_update": "2021-03-15T16:27:21.017Z",
    "min_last_update": "2021-03-15T16:26:14.582Z",
    "max_last_update": "2021-03-15T16:26:14.582Z",
    "binaries": {
      "06C66FF5CCDC2D22344A3EB761A4D38A": {
        "digsig_result": "Signed",
        "digsig_publisher": "Microsoft Corporation"
      }
    }
  }
}
        """
        return mocked_process_return_value, mocked_events_return_value

    @staticmethod
    def _create_query_list(query_string):
        return [query_string]

    @patch('requests.sessions.Session.get')
    def test_no_results_response(self, mock_requests_response):
        mocked_process_return_value = """
{"terms": ["process_name:notepad.exe"],
 "results": [],
 "elapsed": 0.01921701431274414,
 "comprehensive_search": true,
 "all_segments": true,
 "total_results": 0,
 "highlights": [],
 "facets": {},
 "tagged_pids": {"00000036-0000-0a02-01d4-97e70c22b346-0167c881d4b3": [{"name": "Default Investigation", "id": 1}, {"name": "Default Investigation", "id": 1}]},
 "start": 0,
 "incomplete_results": false,
 "filtered": {}
}
"""
        mock_requests_response.side_effect = [
            RequestMockResponse(200, mocked_process_return_value.encode())
        ]

        entry_point = EntryPoint(connection, config)
        query_expression = self._create_query_list("process_name:empty.exe")[0]
        results_response = entry_point.create_results_connection(query_expression, 0, 10)

        assert results_response is not None
        assert 'success' in results_response
        assert results_response['success']
        assert 'data' in results_response
        assert len(results_response['data']) == 0

    @patch('requests.sessions.Session.get')
    def test_one_results_response_limited(self, mock_requests_response):
        mocked_process_return_value, mocked_events_return_value = \
            TestCarbonBlackEventsConnection._get_mock_process_and_events_data()
        mock_requests_response.side_effect = [
            RequestMockResponse(200, mocked_process_return_value.encode()),
            RequestMockResponse(200, mocked_events_return_value.encode()),
        ]
        _connection = deepcopy(connection)
        _connection['options']['result_limit'] = 1
        entry_point = EntryPoint(_connection, config)
        query_expression = self._create_query_list("process_name:erl.exe and last_update:[2021-03-15T16:20:00 TO 2021-03-15T16:30:00]")[0]
        results_response = entry_point.create_results_connection(query_expression, 0, 10)

        assert results_response is not None
        assert 'success' in results_response
        assert results_response['success']
        assert 'data' in results_response
        assert len(results_response['data']) == 1

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
        mocked_return_value = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>401 Unauthorized</title>
<h1>Unauthorized</h1>
<p>The server could not verify that you are authorized to access the URL requested.  You either supplied the wrong credentials (e.g. a bad password), or your browser doesn't understand how to supply the credentials required.</p>
"""

        mock_requests_response.side_effect = [
            RequestMockResponse(401, mocked_return_value.encode())
        ]
        entry_point = EntryPoint(connection, config)
        query_expression = self._create_query_list("process_name:cmd.exe")[0]
        results_response = entry_point.create_results_connection(query_expression, 0, 10)

        assert results_response is not None
        assert 'success' in results_response
        assert results_response['success'] == False
        assert 'error' in results_response
        assert results_response['error'] == 'carbonblack connector error => ' + mocked_return_value
        assert 'code' in results_response
        assert  results_response['code'] == 'authentication_fail'
