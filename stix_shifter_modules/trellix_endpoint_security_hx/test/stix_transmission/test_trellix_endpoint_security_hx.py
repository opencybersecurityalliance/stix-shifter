from stix_shifter_modules.trellix_endpoint_security_hx.entry_point import EntryPoint
from stix_shifter.stix_transmission.stix_transmission import run_in_thread
from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import Status
from tests.utils.async_utils import get_mock_response
from unittest.mock import patch
import unittest
import json
import copy


class TestTrellixEndpointSecurityHxConnection(unittest.TestCase, object):

    def connection(self):
        return {
            "host": "hostbla",
            "port": 1,
            "selfSignedCert": "cert",
            "options": {"host_sets": "hostset1"}
        }

    def connection_with_result_limit(self):
        return {
            "host": "hostbla",
            "port": 1,
            "selfSignedCert": "cert",
            "options": {"host_sets": "hostset1", "result_limit": 2}
        }

    def configuration(self):
        return {
            "auth": {
                "username": "user",
                "password": "123"
            }
        }

    mock_host_set_response = {
        "data": {
            "total": 1,
            "query": {
                "name": "host_set1"
            },
            "sort": {},
            "offset": 0,
            "limit": 50,
            "entries": [
                {
                    "_id": 1001,
                    "name": "host_set1",
                    "type": "static",
                    "_revision": "20240214070201917815249051",
                    "url": "/hx/api/v3/host_sets/1001"
                }
            ]
        },
        "message": "OK",
        "details": [],
        "route": "/hx/api/v3/host_sets"
    }

    mocked_ping_response = {
        "data": {
            "total": 2,
            "query": {},
            "sort": {},
            "offset": 0,
            "limit": 50,
            "entries": [
                {
                    "data": {"hostname": "EC2AMAZ1"}
                },
                {
                    "data": {"hostname": "EC2AMAZ2"}
                }
            ]}}

    mocked_status_response = {
        "data": {
            "_id": 2285,
            "state": "RUNNING",
            "stats": {
                "running_state": {
                    "NEW": 0,
                    "QUEUED": 0,
                    "FAILED": 0,
                    "COMPLETE": 3,
                    "ABORTED": 0,
                    "DELETED": 0,
                    "REFRESH": 0,
                    "CANCELLED": 0
                },
                "hosts": 5
            },
            "settings": {
                "query_terms": {
                    "terms": [
                        {"field": "Local Port", "value": 50, "operator": "greater than"},
                        {"field": "Timestamp - Event", "operator": "between", "value": ["2024-05-27T11:10:17.682Z",
                                                                                        "2024-05-27T11:15:17.682Z"]}
                    ]
                },
                "mode": "HOST"
            }
        }
    }

    mocked_result_response = {
        "data": {
            "total": 5,
            "query": {},
            "sort": {},
            "offset": 0,
            "limit": 1,
            "entries": [
                {
                    "host": {
                        "_id": "abcd",
                        "url": "/hx/api/v3/hosts/abcd",
                        "hostname": "Ec21"
                    },
                    "results": [
                        {
                            "id": 1,
                            "type": "IPv4 Network Event",
                            "data": {
                                "Process Name": "chrome.exe",
                                "Process ID": "6536",
                                "Username": "user1",
                                "Local IP Address": "1.1.1.1",
                                "Remote IP Address": "5.6.7.8",
                                "IP Address": "5.6.7.8",
                                "Port": "443",
                                "Local Port": "53842",
                                "Remote Port": "443",
                                "Timestamp - Event": "2024-05-24T07:10:03.554Z",
                                "Timestamp - Accessed": "2024-05-24T07:10:03.554Z"
                            }
                        }

                    ]
                }]
        },
        "message": "OK",
        "details": [],
        "route": "/hx/api/v3/searches/id/results"
    }

    mocked_result_response_2 = {
        "data": {
            "total": 5,
            "query": {},
            "sort": {},
            "offset": 1,
            "limit": 1,
            "entries": [
                {
                    "host": {
                        "_id": "efgh",
                        "url": "/hx/api/v3/hosts/efgh",
                        "hostname": "Ec22"
                    },
                    "results": [
                        {
                            "id": 2,
                            "type": "IPv4 Network Event",
                            "data": {
                                "Process Name": "svchost.exe",
                                "Process ID": "1956",
                                "Username": "NT AUTHORITY\\NETWORK SERVICE",
                                "Local IP Address": "2.2.2.2",
                                "Remote IP Address": "3.2.2.3",
                                "IP Address": "3.2.2.3",
                                "Port": "53",
                                "Local Port": "64013",
                                "Remote Port": "53",
                                "Timestamp - Event": "2024-05-24T07:10:05.041Z",
                                "Timestamp - Accessed": "2024-05-24T07:10:05.041Z"
                            }
                        },
                        {
                            "id": 3,
                            "type": "IPv4 Network Event",
                            "data": {
                                "Process Name": "ssm-agent-worker.exe",
                                "Process ID": "4932",
                                "Username": "NT AUTHORITY\\SYSTEM",
                                "Local IP Address": "2.2.2.2",
                                "Remote IP Address": "1.0.0.1",
                                "IP Address": "1.0.0.1",
                                "Port": "443",
                                "Local Port": "53843",
                                "Remote Port": "443",
                                "Timestamp - Event": "2024-05-24T07:10:05.042Z",
                                "Timestamp - Accessed": "2024-05-24T07:10:05.042Z"
                            }
                        },
                        {
                            "id": 4,
                            "type": "IPv4 Network Event",
                            "data": {
                                "Process Name": "chrome.exe",
                                "Process ID": "6536",
                                "Username": "user1",
                                "Local IP Address": "2.2.2.2",
                                "Remote IP Address": "5.6.7.8",
                                "IP Address": "5.6.7.8",
                                "Port": "443",
                                "Local Port": "53844",
                                "Remote Port": "443",
                                "Timestamp - Event": "2024-05-24T07:10:19.559Z",
                                "Timestamp - Accessed": "2024-05-24T07:10:19.559Z"
                            }
                        }
                    ]
                }
            ]
        },
        "message": "OK",
        "details": [],
        "route": "/hx/api/v3/searches/id/results"
    }

    def test_is_async(self):
        """ test async"""
        entry_point = EntryPoint()
        check_async = entry_point.is_async()
        assert check_async

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    @patch('ssl.SSLContext.load_verify_locations')
    def test_ping_success(self, mock_ssl, mock_ping_response):
        """ test success response for ping"""
        mock_ping_response.side_effect = [
            get_mock_response(204, "", 'byte',
                              headers={'X-FeApi-Token': "****"}),
            get_mock_response(200, json.dumps(TestTrellixEndpointSecurityHxConnection.mocked_ping_response), 'byte'),
            get_mock_response(204, "", 'byte')]
        entry_point = EntryPoint(self.connection(), self.configuration())
        ping_result = run_in_thread(entry_point.ping_connection)
        assert ping_result["success"] is True

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    @patch('ssl.SSLContext.load_verify_locations')
    def test_query_success(self, mock_ssl, mock_query_response):
        """ test success response for query"""
        query = {"host_set": {"_id": "host_set1"},
                 "query": [
                     {"field": "Local Port", "value": 50, "operator": "greater than"},
                     {"field": "Timestamp - Event", "operator": "between", "value": ["2024-05-27T11:10:17.682Z",
                                                                                     "2024-05-27T11:15:17.682Z"]}]
                 }
        query_response = '{"data": {"_id": 2285, "state": "RUNNING"}}'
        mock_query_response.side_effect = \
            [get_mock_response(204, "", 'byte', headers={'X-FeApi-Token': "****"}),
             get_mock_response(200, json.dumps(TestTrellixEndpointSecurityHxConnection.mock_host_set_response), 'byte'),
             get_mock_response(201, query_response, 'byte'),
             get_mock_response(204, "", 'byte')]
        entry_point = EntryPoint(self.connection(), self.configuration())
        query_response = run_in_thread(entry_point.create_query_connection, json.dumps(query))
        assert query_response['success'] is True
        assert query_response['search_id'] == "2285:host_set1"

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    @patch('ssl.SSLContext.load_verify_locations')
    def test_status_completed(self, mock_ssl, mock_status_response):
        """" test success response for status with completed status"""
        search_id = "2285:host_set1"
        mock_status_response.side_effect = \
            [get_mock_response(204, "", 'byte', headers={'X-FeApi-Token': "****"}),
             get_mock_response(200, json.dumps(TestTrellixEndpointSecurityHxConnection.mocked_status_response),
                               'byte'),
             get_mock_response(204, "", 'byte')]
        entry_point = EntryPoint(self.connection(), self.configuration())
        status_response = run_in_thread(entry_point.create_status_connection, search_id)
        success = status_response["success"]
        assert success
        status = status_response["status"]
        assert status == Status.COMPLETED.value

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    @patch('ssl.SSLContext.load_verify_locations')
    def test_status_running(self, mock_ssl, mock_status_response):
        """ test success response for status with running status"""
        search_id = "2285:host_set1"
        mock_status_response_1 = copy.deepcopy(TestTrellixEndpointSecurityHxConnection.mocked_status_response)
        mock_status_response_1['data']["stats"]["running_state"]["COMPLETE"] = 2
        mock_status_response.side_effect = \
            [get_mock_response(204, "", 'byte', headers={'X-FeApi-Token': "****"}),
             get_mock_response(200, json.dumps(mock_status_response_1),
                               'byte'),
             get_mock_response(204, "", 'byte')]
        entry_point = EntryPoint(self.connection(), self.configuration())
        status_response = run_in_thread(entry_point.create_status_connection, search_id)
        success = status_response["success"]
        assert success
        status = status_response["status"]
        assert status == Status.RUNNING.value

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    @patch('ssl.SSLContext.load_verify_locations')
    def test_results_success_response(self, mock_ssl, mock_results_response):
        """ test results with success response"""
        search_id = "2285:host_set1"
        first_response = get_mock_response(200,
                                           json.dumps(TestTrellixEndpointSecurityHxConnection.mocked_result_response),
                                           'byte')
        second_response = get_mock_response(200, json.dumps(
            TestTrellixEndpointSecurityHxConnection.mocked_result_response_2), 'byte')
        mock_results_response.side_effect = [
            get_mock_response(204, "", 'byte', headers={'X-FeApi-Token': "****"}),
            first_response, second_response,
            get_mock_response(204, "", 'byte'),
            get_mock_response(204, "", 'byte')
        ]
        entry_point = EntryPoint(self.connection(), self.configuration())
        results_response = run_in_thread(entry_point.create_results_connection, search_id, 0, 2)
        success = results_response["success"]
        assert success
        data = results_response["data"]
        assert data
        assert len(data) == 2
        assert results_response['metadata'] == {'host_offset': 1, 'host_record_index': 2}

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    @patch('ssl.SSLContext.load_verify_locations')
    def test_results_success_response_with_metadata(self, mock_ssl, mock_results_response):
        """ test results with success response with metadata"""
        search_id = "2285:host_set1"
        metadata = {'host_offset': 1, 'host_record_index': 2}
        first_response = get_mock_response(200,
                                           json.dumps(TestTrellixEndpointSecurityHxConnection.mocked_result_response_2),
                                           'byte')
        mock_results_response.side_effect = [
            get_mock_response(204, "", 'byte', headers={'X-FeApi-Token': "****"}),
            first_response,
            get_mock_response(204, "", 'byte'),
            get_mock_response(204, "", 'byte')
        ]
        entry_point = EntryPoint(self.connection(), self.configuration())
        results_response = run_in_thread(entry_point.create_results_connection, search_id, 2, 1, metadata)
        success = results_response["success"]
        assert success
        data = results_response["data"]
        assert data
        assert results_response['metadata'] == {'host_offset': 1, 'host_record_index': 3}

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    @patch('ssl.SSLContext.load_verify_locations')
    def test_results_success_response_with_result_limit_less_than_length(self, mock_ssl, mock_results_response):
        """ test results with success response with modified result limit"""
        search_id = "2285:host_set1"
        metadata = {'host_offset': 1, 'host_record_index': 1}
        first_response = get_mock_response(200,
                                           json.dumps(TestTrellixEndpointSecurityHxConnection.mocked_result_response_2),
                                           'byte')
        mock_results_response.side_effect = [
            get_mock_response(204, "", 'byte', headers={'X-FeApi-Token': "****"}),
            first_response,
            get_mock_response(204, "", 'byte'),
            get_mock_response(204, "", 'byte')
        ]
        entry_point = EntryPoint(self.connection_with_result_limit(), self.configuration())
        results_response = run_in_thread(entry_point.create_results_connection, search_id, 0, 3, metadata)
        success = results_response["success"]
        assert success
        data = results_response["data"]
        assert data
        assert len(data) == 2

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    @patch('ssl.SSLContext.load_verify_locations')
    def test_results_and_format_url_registry_event(self, mock_ssl, mock_results_response):
        """ test results to verify the formatted url and registry events"""
        search_id = "2286:host_set2"
        mocked_response = {
            "data": {
                "total": 5,
                "query": {},
                "sort": {},
                "offset": 0,
                "limit": 1,
                "entries": [
                    {
                        "host": {
                            "_id": "abcd",
                            "url": "/hx/api/v3/hosts/abcd",
                            "hostname": "Ec21"
                        },
                        "results": [
                            {
                                "id": 1,
                                "type": "URL Event",
                                "data": {
                                    "Process Name": "EC2Launch.exe",
                                    "Process ID": "3664",
                                    "Username": "NT AUTHORITY\\SYSTEM",
                                    "Remote IP Address": "10.20.10.20",
                                    "IP Address": "10.20.10.20",
                                    "Port": "80",
                                    "Local Port": "49726",
                                    "Remote Port": "80",
                                    "DNS Hostname": "10.20.10.20",
                                    "URL": "/latest/meta-data//hibernation/configured",
                                    "HTTP Header": "GET /latest/meta-data//hibernation/configured HTTP/1.1"
                                                   "\nHost: 10.20.10.20\nUser-Agent: Go-http-client/1.1\nX-Aws-"
                                                   "Ec2-Metadata-Token: AQAAACbkzU35XT2PUWZWf6WfwHTdKFFF4n_dottlg8D_0-"
                                                   "PIkAsoOA==\nAccept-Encoding: gzip\n\n",
                                    "HTTP Method": "GET",
                                    "Timestamp - Event": "2024-03-07T09:09:10.836Z",
                                    "Timestamp - Accessed": "2024-03-07T09:09:10.836Z"
                                }
                            },
                            {
                                "id": 2,
                                "type": "Registry Event",
                                "data": {
                                    "Process Name": "svchost.exe",
                                    "Process ID": "1484",
                                    "Username": "NT AUTHORITY\\LOCAL SERVICE",
                                    "Registry Key Full Path": "HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services"
                                                              "\\Tcpip\\Parameters\\Interfaces\\{d7f2a7dc-ea23-44ef-"
                                                              "8ebe-84bad862a9d8}\\LeaseObtainedTime",
                                    "Registry Key Value Name": "LeaseObtainedTime",
                                    "Registry Key Value Type": "REG_DWORD",
                                    "Registry Key Value Text": "fJm.",
                                    "Timestamp - Event": "2024-05-19T21:24:02.365Z",
                                    "Timestamp - Modified": "2024-05-19T21:24:02.365Z"
                                }
                            },
                            {
                                "id": 3,
                                "type": "File Write Event",
                                "data": {
                                    "File Name": "SRU.chk",
                                    "File Full Path": "C:\\Windows\\SRU.chk",
                                    "File Text Written": "C:\\Windows\\syste",
                                    "File Bytes Written": "8192",
                                    "Size in bytes": "8192",
                                    "File MD5 Hash": "5b9eb9cdf514a50f676d0cb63118ff41",
                                    "Process Name": "svchost.exe",
                                    "Process ID": "4344",
                                    "Username": "NT AUTHORITY\\LOCAL SERVICE",
                                    "Timestamp - Event": "2024-05-21T05:41:06.141Z",
                                    "Timestamp - Modified": "2024-05-21T05:41:06.141Z"
                                }
                            }

                        ]
                    }]
            },
            "message": "OK",
            "details": [],
            "route": "/hx/api/v3/searches/id/results"
        }
        mock_results_response.side_effect = [
            get_mock_response(204, "", 'byte', headers={'X-FeApi-Token': "****"}),
            get_mock_response(200,
                              json.dumps(mocked_response),
                              'byte'),
            get_mock_response(204, "", 'byte'),
            get_mock_response(204, "", 'byte')
        ]
        entry_point = EntryPoint(self.connection(), self.configuration())
        results_response = run_in_thread(entry_point.create_results_connection, search_id, 0, 3)
        success = results_response["success"]
        assert success
        data = results_response["data"]
        assert data[0]['HTTP Header']['Host'] == '10.20.10.20'
        assert data[0]['HTTP Header']['User-Agent'] == 'Go-http-client/1.1'
        assert data[0]['HTTP Header']['Accept-Encoding'] == 'gzip'
        assert (data[1]['Registry Key Values'] == 
                [{'name': 'LeaseObtainedTime', 'data': 'fJm.', 'data_type': 'REG_DWORD'}])
        assert data[2]['Write Event File Bytes Written'] == "8192"
        assert data[2]["Write Event File Text Written"] == "C:\\Windows\\syste"
        assert data[2]["Write Event File Name"] == "SRU.chk"
        assert data[2]["File Name"] == "svchost.exe"

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    @patch('ssl.SSLContext.load_verify_locations')
    def test_empty_records_in_results(self, mock_ssl, mock_result_response):
        """ test empty records in results"""
        search_id = "2287:host_set3"
        mocked_response = {
            "data": {
                "total": 5,
                "query": {},
                "sort": {},
                "offset": 0,
                "limit": 1,
                "entries": []
            },
            "message": "OK",
            "details": [],
            "route": "/hx/api/v3/searches/id/results"
        }
        mock_result_response.side_effect = [
            get_mock_response(204, "", 'byte', headers={'X-FeApi-Token': "****"}),
            get_mock_response(200,
                              json.dumps(mocked_response),
                              'byte'),
            get_mock_response(204, "", 'byte'),
            get_mock_response(204, "", 'byte')
        ]
        entry_point = EntryPoint(self.connection(), self.configuration())
        results_response = run_in_thread(entry_point.create_results_connection, search_id, 0, 2)
        assert results_response is not None
        success = results_response["success"]
        assert success
        data = results_response["data"]
        assert data == []

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    @patch('ssl.SSLContext.load_verify_locations')
    def test_deletion_success(self, mock_ssl, mock_delete_response):
        """ test delete query success response"""
        search_id = "2287:host_set3"
        mock_delete_response.side_effect = [
            get_mock_response(204, "", 'byte', headers={'X-FeApi-Token': "****"}),
            get_mock_response(204, "", 'byte'),
            get_mock_response(204, "", 'byte')
        ]
        entry_point = EntryPoint(self.connection(), self.configuration())
        del_response = run_in_thread(entry_point.delete_query_connection, search_id)
        assert del_response is not None
        success = del_response["success"]
        assert success

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    @patch('ssl.SSLContext.load_verify_locations')
    def test_deletion_failure(self, mock_ssl, mock_delete_response):
        """ test invalid search id in delete results"""
        search_id = "2289:host_set3"
        mock_del_response = {
            "details": [{"type": "error", "code": 1005, "message": "Search not found.", "path": "id"}],
            "route": "/hx/api/v3/searches/id", "message": "Not Found"}
        mock_delete_response.side_effect = [
            get_mock_response(204, "", 'byte', headers={'X-FeApi-Token': "****"}),
            get_mock_response(404, json.dumps(mock_del_response), 'byte'),
            get_mock_response(204, "", 'byte')
        ]
        entry_point = EntryPoint(self.connection(), self.configuration())
        del_response = run_in_thread(entry_point.delete_query_connection, search_id)
        assert del_response is not None
        assert del_response['success'] is False
        assert 'error' in del_response
        assert 'Search not found' in del_response['error']
        assert del_response['code'] == 'no_results'

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    @patch('ssl.SSLContext.load_verify_locations')
    def test_timeout_for_results(self, mock_ssl, mock_result_response):
        """ test timeout for results"""
        search_id = "2286:host_set2"
        mock_result_response.side_effect = [Exception("'server timeout_error (2 sec)'")]
        entry_point = EntryPoint(self.connection(), self.configuration())
        results_response = run_in_thread(entry_point.create_results_connection, search_id, 0, 2)
        assert results_response is not None
        assert results_response['success'] is False
        assert 'error' in results_response
        assert 'timeout_error' in results_response['error']
        assert results_response['code'] == 'service_unavailable'

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    @patch('ssl.SSLContext.load_verify_locations')
    def test_invalid_authentication_for_results(self, mock_ssl, mock_result_response):
        """ test invalid authentication for results"""
        search_id = "2286:host_set2"
        mock_result_response.side_effect = \
            [get_mock_response(401, json.dumps(
                {'details': [{'code': 1105, 'message': 'Incorrect user id or password.', 'type': 'error'}],
                 'message': 'Unauthorized'}), 'byte')]
        entry_point = EntryPoint(self.connection(), self.configuration())
        results_response = run_in_thread(entry_point.create_results_connection, search_id, 0, 2)
        assert results_response is not None
        assert results_response['success'] is False
        assert 'error' in results_response
        assert 'Incorrect user id or password.' in results_response['error']
        assert results_response['code'] == 'authentication_fail'

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    @patch('ssl.SSLContext.load_verify_locations')
    def test_timeout_for_status(self, mock_ssl, mock_status_response):
        """ test timeout for status"""

        mock_status_response.side_effect = [Exception("'server timeout_error (2 sec)'")]
        entry_point = EntryPoint(self.connection(), self.configuration())
        status_response = run_in_thread(entry_point.create_status_connection, "1255")
        assert status_response is not None
        assert status_response['success'] is False
        assert 'error' in status_response
        assert 'timeout_error' in status_response['error']
        assert status_response['code'] == 'service_unavailable'

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    @patch('ssl.SSLContext.load_verify_locations')
    def test_invalid_search_id_for_status(self, mock_ssl, mock_status_response):
        """ test invalid search id for status"""
        mock_search_response = {
            "details": [{"type": "error", "code": 1005, "message": "Search not found.", "path": "id"}],
            "route": "/hx/api/v3/searches/id", "message": "Not Found"}
        mock_status_response.side_effect = \
            [get_mock_response(204, "", 'byte', headers={'X-FeApi-Token': "****"}),
             get_mock_response(404, json.dumps(mock_search_response), 'byte'),
             get_mock_response(204, "", 'byte')]
        entry_point = EntryPoint(self.connection(), self.configuration())
        status_response = run_in_thread(entry_point.create_status_connection, "1255")
        assert status_response is not None
        assert status_response['success'] is False
        assert 'error' in status_response
        assert 'Search not found' in status_response['error']
        assert status_response['code'] == 'no_results'

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    @patch('ssl.SSLContext.load_verify_locations')
    def test_invalid_host_set_for_query(self, mock_ssl, mock_query_response):
        """ test invalid host set name for query"""
        mock_host_set_response = {
            "data": {
                "total": 1,
                "query": {
                    "name": "invalid host set"
                },
                "entries": []
            },
            "route": "/hx/api/v3/host_sets"
        }
        mock_query_response.side_effect = \
            [get_mock_response(204, "", 'byte', headers={'X-FeApi-Token': "****"}),
             get_mock_response(200, json.dumps(mock_host_set_response), 'byte'),
             get_mock_response(204, "", 'byte')]
        entry_point = EntryPoint(self.connection(), self.configuration())
        query = {"host_set": {"_id": "invalid host set"},
                 "query": [
                     {"field": "Local Port", "value": 50, "operator": "greater than"}]
                 }
        query_response = run_in_thread(entry_point.create_query_connection, json.dumps(query))
        assert query_response is not None
        assert query_response['success'] is False
        assert 'error' in query_response
        assert 'Invalid Host Set Name' in query_response['error']
        assert query_response['code'] == 'invalid_parameter'

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    @patch('ssl.SSLContext.load_verify_locations')
    def test_invalid_authentication_for_query(self, mock_ssl, mock_query_response):
        """ test invalid authentication for query"""

        mock_query_response.side_effect = \
            [get_mock_response(401, json.dumps(
                {'details': [{'code': 1105, 'message': 'Incorrect user id or password.', 'type': 'error'}],
                 'message': 'Unauthorized'}), 'byte')]
        entry_point = EntryPoint(self.connection(), self.configuration())
        query = {"host_set": {"_id": "invalid host set"},
                 "query": [
                     {"field": "Local Port", "value": 50, "operator": "greater than"}]
                 }
        query_response = run_in_thread(entry_point.create_query_connection, json.dumps(query))
        assert query_response is not None
        assert query_response['success'] is False
        assert 'error' in query_response
        assert 'Incorrect user id or password.' in query_response['error']
        assert query_response['code'] == 'authentication_fail'

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    @patch('ssl.SSLContext.load_verify_locations')
    def test_time_out_exception_for_query(self, mock_ssl, mock_query_response):
        """ test timeout exception for query"""
        query = {"host_set": {"_id": "host set 1"},
                 "query": [
                     {"field": "Local Port", "value": 50, "operator": "greater than"}]
                 }
        mock_query_response.side_effect = Exception("'server timeout_error (2 sec)'")
        entry_point = EntryPoint(self.connection(), self.configuration())
        query_response = run_in_thread(entry_point.create_query_connection, json.dumps(query))
        assert query_response is not None
        assert query_response['success'] is False
        assert 'error' in query_response
        assert 'timeout_error' in query_response['error']
        assert query_response['code'] == 'service_unavailable'

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    @patch('ssl.SSLContext.load_verify_locations')
    def test_invalid_query(self, mock_ssl, mock_query_response):
        """ test invalid field name in query"""
        mock_response = {"details": [{"type": "error", "code": 1006, "message": "Invalid search term field.",
                                      "path": "query"}], "route": "/hx/api/v3/searches",
                         "message": "Unprocessable Entity"}

        mock_query_response.side_effect = \
            [get_mock_response(204, "", 'byte', headers={'X-FeApi-Token': "****"}),
             get_mock_response(422, json.dumps(mock_response), 'byte'),
             get_mock_response(204, "", 'byte')]
        entry_point = EntryPoint(self.connection(), self.configuration())
        query = {"host_set": {"_id": "host_set1"},
                 "query": [
                     {"field": "Local Port1", "value": 50, "operator": "greater than"}]
                 }
        query_response = run_in_thread(entry_point.create_query_connection, json.dumps(query))
        assert query_response is not None
        assert query_response['success'] is False
        assert 'error' in query_response
        assert 'Invalid search term field.' in query_response['error']
        assert query_response['code'] == 'invalid_query'

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    @patch('ssl.SSLContext.load_verify_locations')
    def test_invalid_authentication_for_ping(self, mock_ssl, mock_ping_response):
        """ test invalid authentication for ping"""
        mock_ping_response.side_effect = [get_mock_response(401, json.dumps(
            {'details': [{'code': 1105, 'message': 'Incorrect user id or password.', 'type': 'error'}],
             'message': 'Unauthorized'}), 'byte')]
        entry_point = EntryPoint(self.connection(), self.configuration())
        ping_result = run_in_thread(entry_point.ping_connection)
        assert ping_result is not None
        assert ping_result['success'] is False
        assert 'error' in ping_result
        assert 'Incorrect user id or password' in ping_result['error']
        assert ping_result['code'] == 'authentication_fail'

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    @patch('ssl.SSLContext.load_verify_locations')
    def test_time_out_exception_for_ping(self, mock_ssl, mock_ping_response):
        """ test timeout exception for ping"""
        mock_ping_response.side_effect = Exception("'server timeout_error (2 sec)'")
        entry_point = EntryPoint(self.connection(), self.configuration())
        ping_result = run_in_thread(entry_point.ping_connection)
        assert ping_result is not None
        assert ping_result['success'] is False
        assert 'error' in ping_result
        assert 'timeout_error' in ping_result['error']
        assert ping_result['code'] == 'service_unavailable'
