from stix_shifter_modules.crowdstrike_logscale.entry_point import EntryPoint
from stix_shifter.stix_transmission.stix_transmission import run_in_thread
from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import Status
from tests.utils.async_utils import get_mock_response
from unittest.mock import patch
import unittest
import json


class TestCrowdstrikeLogscaleConnection(unittest.TestCase, object):

    def connection(self):
        return {
                "host": "hostbla",
                "repository": "testrepo",
                }
    def connection_with_result_limit(self):
        return {
            "host": "hostbla",
            "repository": "testrepo",
            "options": {"result_limit": 2}
        }

    def configuration(self):
        return {
                "auth": {
                    "api_token": "123"
                }
        }

    mocked_ping_response = {"status": "OK",
                            "version": "1.x.0--build-4xxx0--sha-123"}

    mocked_result_response = {
    "cancelled": False,
    "done": True,
    "events": [
        {
            "behaviors[0].technique": "Indicator of Attack",
            "seconds_to_resolved": "0",
            "device.local_ip": "1.1.1.1",
            "device.product_type_desc": "Server",
            "device.os_version": "Windows Server 2022",
            "behaviors[0].tactic": "Custom Intelligence",
            "behaviors[0].ioc_description": "",
            "max_severity": "50",
            "@timestamp": 1711549347952,
            "@ingesttimestamp": "1711549348586",
            "hostinfo.domain": "",
            "#type": "CrowdStrike_Spotlight",
            "device.product_type": "3",
            "behaviors[0].description": "A process triggered a medium severity custom rule.",
            "device.agent_local_time": "2024-03-13T07:33:59.693Z",
            "device.config_id_platform": "3",
            "behaviors[0].behavior_id": "41002",
            "behaviors[0].ioc_source": "",
            "device.platform_name": "Windows",
            "behaviors[0].user_name": "user1",
            "device.first_seen": "2023-05-16T05:10:55Z",
            "detection_id": "ldt:123:123",
            "device.external_ip": "2.2.2.2",
            "device.bios_manufacturer": "Xen",
            "first_behavior": "2024-03-13T07:34:08Z",
            "behaviors[0].technique_id": "CST0004",
            "behaviors[0].parent_details.parent_md5": "",
            "device.platform_id": "0",
            "#repo": "TestRepository",
            "device.modified_timestamp": "2024-03-13T07:34:11Z",
            "device.minor_version": "0",
            "device.bios_version": "4.2.amazon",
            "behaviors[0].display_name": "CustomIOAWinMedium",
            "device.hostname": "host",
            "behaviors[0].parent_details.parent_cmdline": "",
            "device.service_provider": "aws",
            "behaviors[0].filepath": "\\Device\\conhost.exe",
            "date_updated": "2024-03-27T14:22:27.952818Z",
            "behaviors[0].md5": "1234xxxxxxxxxxxx",
            "max_severity_displayname": "Medium",
            "behaviors[0].pattern_disposition": "10240",
            "email_sent": "false",
            "behaviors[0].triggering_process_graph_id": "pid:12:12",
            "device.last_login_user": "Administrator",
            "device.status": "normal",
            "behaviors[0].rule_instance_id": "3",
            "behaviors[0].objective": "Falcon Detection Method",
            "behaviors[0].timestamp": "2024-03-13T07:34:08Z",
            "device.instance_id": "i-123ab",
            "behaviors[0].parent_details.parent_sha256": "",
            "device.config_id_base": "65994763",
            "behaviors[0].user_id": "S-1-5-18",
            "behaviors_processed[0]": "pid:12:33221:42",
            "seconds_to_triaged": "0",
            "status": "new",
            "device.major_version": "10",
            "max_confidence": "100",
            "device.agent_version": "7.06.1xxx.0",
            "@timezone": "Z",
            "behaviors[0].filename": "conhost.exe",
            "behaviors[0].parent_details.parent_process_graph_id": "pid:12:33",
            "last_behavior": "2024-03-13T07:34:08Z",
            "device.last_seen": "2024-03-13T07:34:10Z",
            "behaviors[0].control_graph_id": "ctg:xx:yy",
            "device.system_product_name": "HVM domU",
            "behaviors[0].sha256": "1234567000",
            "created_timestamp": "2024-03-13T07:34:15.869091531Z",
            "device.config_id_build": "17807",
            "behaviors[0].cmdline": "C:\\conhost.exe 0xffffffff -ForceV1",
            "behaviors[0].ioc_type": "",
            "behaviors[0].tactic_id": "CSTA0005",
            "device.last_login_timestamp": "2024-03-12T16:50:17Z",
            "behaviors[0].severity": "50",
            "device.system_manufacturer": "Xen",
            "device.agent_load_flags": "1",
            "behaviors[0].confidence": "100",
            "@timestamp.nanos": "818000",
            "behaviors[0].ioc_value": "",
            "behaviors[0].template_instance_id": "3",
            "device.mac_address": "01-01-01-01-01-01",
            "behaviors[0].alleged_filetype": "exe",
            "behaviors[0].device_id": "device",
            "behaviors[0].scenario": "suspicious_activity",
            "behaviors[0].rule_instance_version": "3",
            "device.service_provider_account_id": "1234",
            "@id": "ATzrtyg4xCKOqQnD9NodpvsY_363_23_1711549347"
        }],
        "metaData":
            {"eventCount": 0,
             "filterQuery":
                 {"end": 1711549347952,
                  "queryString": "behaviors[0].filename=\"cmd.exe\" OR behaviors[0].filename=\"conhost.exe\"",
                  "start": 1710921332365}},
        "warnings": []}

    mocked_result_response_2 = {
    "cancelled": False,
    "done": True,
    "events": [{
            "behaviors[0].technique": "Indicator of Attack",
            "seconds_to_resolved": "0",
            "device.local_ip": "2.2.2.2",
            "device.product_type_desc": "Server",
            "device.os_version": "Windows Server 2022",
            "behaviors[0].tactic": "Custom Intelligence",
            "behaviors[0].ioc_description": "\\Device\\cmd.exe",
            "max_severity": "50",
            "@timestamp": 1711549342830,
            "@ingesttimestamp": "1711549348586",
            "device.groups[0]": "1234",
            "hostinfo.domain": "",
            "#type": "CrowdStrike_Spotlight",
            "device.product_type": "3",
            "behaviors[0].description": "A process triggered a medium severity custom rule.",
            "device.agent_local_time": "2024-03-14T14:40:04.490Z",
            "device.config_id_platform": "3",
            "behaviors[0].behavior_id": "41002",
            "behaviors[0].ioc_source": "library_load",
            "device.platform_name": "Windows",
            "behaviors[0].user_name": "user2",
            "device.first_seen": "2023-05-16T05:10:55Z",
            "detection_id": "ldt:7adxxxx00d49:33",
            "device.external_ip": "4.5.6.7",
            "device.bios_manufacturer": "Xen",
            "first_behavior": "2024-03-14T14:40:26Z",
            "behaviors[0].technique_id": "CST0004",
            "behaviors[0].parent_details.parent_md5": "",
            "device.platform_id": "0",
            "#repo": "TestRepository",
            "device.modified_timestamp": "2024-03-14T14:40:19Z",
            "device.minor_version": "0",
            "device.bios_version": "4.11.amazon",
            "behaviors[0].display_name": "CustomIOAWinMedium",
            "device.hostname": "host",
            "behaviors[0].parent_details.parent_cmdline": "",
            "device.service_provider": "aws",
            "behaviors[0].filepath": "\\Device\\cmd.exe",
            "date_updated": "2024-03-27T14:22:27.952818Z",
            "behaviors[0].md5": "axxtyya",
            "max_severity_displayname": "Medium",
            "behaviors[0].pattern_disposition": "2048",
            "email_sent": "false",
            "behaviors[0].triggering_process_graph_id": "pid:11:00",
            "device.last_login_user": "Administrator",
            "device.status": "normal",
            "behaviors[0].rule_instance_id": "3",
            "behaviors[0].objective": "Falcon Detection Method",
            "behaviors[0].timestamp": "2024-03-14T14:40:26Z",
            "device.instance_id": "i-123",
            "behaviors[0].parent_details.parent_sha256": "",
            "device.config_id_base": "65994763",
            "behaviors[0].user_id": "user_id_1",
            "behaviors_processed[0]": "pid:22:33:41002",
            "seconds_to_triaged": "0",
            "status": "new",
            "device.major_version": "10",
            "max_confidence": "100",
            "device.agent_version": "7.11.xx.0",
            "@timezone": "Z",
            "behaviors[0].filename": "cmd.exe",
            "behaviors[0].parent_details.parent_process_graph_id": "pid:22:33",
            "last_behavior": "2024-03-14T14:40:26Z",
            "device.last_seen": "2024-03-14T14:40:18Z",
            "behaviors[0].control_graph_id": "ctg:xx:33",
            "device.system_product_name": "HVM domU",
            "behaviors[0].sha256": "exxxx123",
            "created_timestamp": "2024-03-14T14:41:22.092316953Z",
            "device.config_id_build": "18110",
            "behaviors[0].cmdline": "C:\\cmd.exe /c reg query \"HKLM\\Software\\Npcap\" /ve 2>nul | find \"REG_SZ\"",
            "behaviors[0].ioc_type": "hash_sha256",
            "behaviors[0].tactic_id": "CSTA0005",
            "device.last_login_timestamp": "2024-03-14T13:14:27Z",
            "behaviors[0].severity": "50",
            "device.system_manufacturer": "Xen",
            "device.agent_load_flags": "1",
            "behaviors[0].confidence": "100",
            "@timestamp.nanos": "818000",
            "behaviors[0].ioc_value": "xxyy",
            "behaviors[0].template_instance_id": "3",
            "device.groups[1]": "bb1",
            "device.mac_address": "01-01-01-01-01-01",
            "behaviors[0].alleged_filetype": "exe",
            "behaviors[0].scenario": "suspicious_activity",
            "behaviors[0].rule_instance_version": "3",
            "device.service_provider_account_id": "123",
            "@id": "ATzrtyg4xCKOqQnD9NodpvsY_363_21_1711549347"
        }],
        "metaData":
            {"eventCount": 0,
             "filterQuery":
                 {"end": 1711549347952,
                  "queryString": "behaviors[0].filename=\"cmd.exe\" OR behaviors[0].filename=\"conhost.exe\"",
                  "start": 1710921332365}},
        "warnings": []}


    def test_is_async(self):
        """ test async"""
        entry_point = EntryPoint(self.connection(), self.configuration())
        check_async = entry_point.is_async()
        assert check_async

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_ping_success(self, mock_ping_response):
        """ test success response for ping"""
        mock_ping_response.return_value = \
            get_mock_response(200, json.dumps(TestCrowdstrikeLogscaleConnection.mocked_ping_response), 'byte')
        entry_point = EntryPoint(self.connection(), self.configuration())
        ping_result = run_in_thread(entry_point.ping_connection)
        assert ping_result["success"] is True


    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_query_success(self, mock_query_response):
        """ test success response for query"""
        query = {"source": "edr", "queryString": "behaviors[0].filename=\"cmd.exe\" OR behaviors[0].filename=\"conhost.exe\" | tail(10000)", "start": 1710921332365, "end": 1711549347952}
        query_response = '{"hashedQueryOnView": "123ac", "id": "P3-ohFBXrfxvfy3U1xk28PLFJKL"}'
        mock_query_response.return_value = \
            get_mock_response(200, query_response, 'byte')
        entry_point = EntryPoint(self.connection(), self.configuration())
        query_response = run_in_thread(entry_point.create_query_connection, json.dumps(query))
        assert query_response['success'] is True
        assert query_response['search_id'] == "P3-ohFBXrfxvfy3U1xk28PLFJKL:edr"


    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_status_completed(self, mock_status_response):
        """" test success response for status with completed status"""
        search_id = "P3-ohFBXrfxvfy3U1xk28PLFJKL:edr"
        status_response = ('{"cancelled": false,"done": true,"events": [], "metaData": {"eventCount": 1,'
                           '"filterQuery": {"end": 1711549347952,"queryString": "behaviors[0].filename=\\\"cmd.exe\\\" OR '
                           'behaviors[0].filename=\\\"conhost.exe\\\"","start": 1710921332365}},"warnings": []}')
        mock_status_response.return_value = \
            get_mock_response(200, status_response, 'byte')
        entry_point = EntryPoint(self.connection(), self.configuration())
        status_response = run_in_thread(entry_point.create_status_connection, search_id)
        success = status_response["success"]
        assert success
        status = status_response["status"]
        assert status == Status.COMPLETED.value

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_status_running(self, mock_status_response):
        """ test success response for status with running status"""
        search_id = "P3-ohFBXrfxvfy3U1xk28PLFJKL:edr"
        status_response = ('{"cancelled": false,"done": false,"events": [], "metaData": {"eventCount": 3000,'
                           '"filterQuery": {"end": 1711549347952,"queryString": "behaviors[0].filename=\\\"cmd.exe\\\" OR '
                           'behaviors[0].filename=\\\"conhost.exe\\\"","start": 1710921332365}},"warnings": []}')
        mock_status_response.return_value = \
            get_mock_response(200, status_response, 'byte')
        entry_point = EntryPoint(self.connection(), self.configuration())
        status_response = run_in_thread(entry_point.create_status_connection, search_id)
        success = status_response["success"]
        assert success
        status = status_response["status"]
        assert status == Status.RUNNING.value
        assert status_response['progress'] == 30

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_status_running_using_metadata(self, mock_status_response):
        """ test success response for status when called from results connector with metadata"""
        search_id = "P3-ohFBXrfxvfy3U1xk28PLFJKL:edr"
        status_response = ('{"cancelled": false,"done": false,"events": [], "metaData": {"eventCount": 1000,'
                           '"filterQuery": {"end": 1711549347952,"queryString": "behaviors[0].filename=\\\"cmd.exe\\\" OR '
                           'behaviors[0].filename=\\\"conhost.exe\\\"","start": 1710921332365}},"warnings": []}')
        metadata = {'length': 2000}
        mock_status_response.return_value = \
            get_mock_response(200, status_response, 'byte')
        entry_point = EntryPoint(self.connection(), self.configuration())
        status_response = run_in_thread(entry_point.create_status_connection, search_id, metadata)
        success = status_response["success"]
        assert success
        status = status_response["status"]
        assert status == Status.RUNNING.value
        assert status_response['progress'] == 50

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_status_canceled(self, mock_status_response):
        """ test success response with status as cancelled """
        search_id = "P3-ohFBXrfxvfy3U1xk28PLFJKL:edr"
        status_response = ('{"cancelled": true,"done": false,"events": [], "metaData": {"eventCount": 0,'
                           '"filterQuery": {"end": 1711549347952,"queryString": "behaviors[0].filename=\\\"cmd.exe\\\" OR '
                           'behaviors[0].filename=\\\"conhost.exe\\\"","start": 1710921332365}},"warnings": []}')
        mock_status_response.return_value = \
            get_mock_response(200, status_response, 'byte')
        entry_point = EntryPoint(self.connection(), self.configuration())
        status_response = run_in_thread(entry_point.create_status_connection, search_id)
        success = status_response["success"]
        assert success
        status = status_response["status"]
        assert status == Status.CANCELED.value

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_results_success_response(self, mock_results_response):
        """ test results with success response"""
        search_id = "P3-ohFBXrfxvfy3U1xk28PLFJKL:edr"
        mock_delete_job_id_response = get_mock_response(204, "", 'byte')
        query_response = get_mock_response(200, '{"hashedQueryOnView": "123ac", "id": "P3-ohFBXrfxvfy3U1xk28PLFJKL"}', 'byte')
        first_response = get_mock_response(200, json.dumps(TestCrowdstrikeLogscaleConnection.mocked_result_response), 'byte')
        second_response = get_mock_response(200, json.dumps(TestCrowdstrikeLogscaleConnection.mocked_result_response_2), 'byte')
        mock_results_response.side_effect = [first_response, query_response, second_response, second_response, mock_delete_job_id_response]

        entry_point = EntryPoint(self.connection(), self.configuration())
        results_response = run_in_thread(entry_point.create_results_connection, search_id, 0, 2)
        success = results_response["success"]
        assert success
        data = results_response["data"]
        assert data
        assert (results_response['metadata'] ==
                {'input_query_string': 'behaviors[0].filename="cmd.exe" OR '
                                       'behaviors[0].filename="conhost.exe"',
                 'last_event_id': 'ATzrtyg4xCKOqQnD9NodpvsY_363_21_1711549347',
                 'last_event_timestamp': 1711549342830,
                 'start': 1710921332365})

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_results_success_response_with_result_limit_less_than_length(self, mock_results_response):
        """ test results with success response"""
        search_id = "P3-ohFBXrfxvfy3U1xk28PLFJKL:edr"
        mock_delete_job_id_response = get_mock_response(204, "", 'byte')
        query_response = get_mock_response(200, '{"hashedQueryOnView": "123ac", "id": "P3-ohFBXrfxvfy3U1xk28PLFJKL"}', 'byte')
        first_response = get_mock_response(200, json.dumps(TestCrowdstrikeLogscaleConnection.mocked_result_response), 'byte')
        second_response = get_mock_response(200, json.dumps(TestCrowdstrikeLogscaleConnection.mocked_result_response_2), 'byte')
        mock_results_response.side_effect = [first_response, query_response, second_response, second_response, mock_delete_job_id_response]

        entry_point = EntryPoint(self.connection_with_result_limit(), self.configuration())
        results_response = run_in_thread(entry_point.create_results_connection, search_id, 0, 5)
        success = results_response["success"]
        assert success
        data = results_response["data"]
        assert data
        assert len(data) == 2

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_results_success_response_using_metadata_for_next_iteration(self, mock_results_response):
        """ test success response for results with metadata as input to be used for next iteration"""
        search_id = "P3-ohFBXrfxvfy3U1xk28PLFJKL:edr"
        metadata = {'input_query_string': 'behaviors[0].filename="cmd.exe" OR '
                                          'behaviors[0].filename="conhost.exe"',
                           'start': 1710921332365,
                           'last_event_id': 'ATzrtyg4xCKOqQnD9NodpvsY_363_23_1711549347',
                                      'last_event_timestamp': 1711549347952}
        mock_delete_job_id_response = get_mock_response(204, "", 'byte')
        mock_query_job_id_response = get_mock_response(200, json.dumps({"hashedQueryOnView": "456ac", "id": "P6-o1FbXrfxvfy3U1xk28PLFijk"}), 'byte')
        mock_query_poll_response = get_mock_response(200, json.dumps(TestCrowdstrikeLogscaleConnection.mocked_result_response_2), 'byte')
        mock_results_response.side_effect = [mock_query_job_id_response,mock_query_poll_response, mock_query_poll_response,mock_delete_job_id_response]

        entry_point = EntryPoint(self.connection_with_result_limit(), self.configuration())
        results_response = run_in_thread(entry_point.create_results_connection, search_id, 0, 1, metadata)
        success = results_response["success"]
        assert success
        data = results_response["data"]
        assert data
        assert (results_response['metadata'] ==
                {'input_query_string': 'behaviors[0].filename="cmd.exe" OR '
                                          'behaviors[0].filename="conhost.exe"',
                           'start': 1710921332365,
                           'last_event_id': 'ATzrtyg4xCKOqQnD9NodpvsY_363_21_1711549347',
                            'last_event_timestamp': 1711549342830})


    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_results_using_metadata_for_next_iteration_and_call_status(self, mock_results_response):
        """ test success response for results with metadata as input and call status connector to check status for
        intermediate query job id"""
        search_id = "P3-ohFBXrfxvfy3U1xk28PLFJKL:edr"
        mocked_running_result_response = {
            "cancelled": False,
            "done": False,
            "events": [],
            "metaData":
                {"eventCount": 0,
                 "filterQuery":
                     {"end": 1711549347952,
                      "queryString": "behaviors[0].filename=\"cmd.exe\" OR behaviors[0].filename=\"conhost.exe\"",
                      "start": 1710921332365}},
            "warnings": []}

        metadata = {'input_query_string': 'behaviors[0].filename="cmd.exe" OR '
                                          'behaviors[0].filename="conhost.exe"',
                           'start': 1710921332365,
                           'last_event_id': 'ATzrtyg4xCKOqQnD9NodpvsY_363_23_1711549347',
                    'last_event_timestamp': 1711549347952}

        mock_delete_job_id_response = get_mock_response(204, "", 'byte')
        mock_query_job_id_response = get_mock_response(200, json.dumps({"hashedQueryOnView": "456ac", "id": "P6-o1FbXrfxvfy3U1xk28PLFijk"}), 'byte')
        mock_query_poll_response = get_mock_response(200, json.dumps(TestCrowdstrikeLogscaleConnection.mocked_result_response_2), 'byte')
        mock_query_poll_running_response = get_mock_response(200, json.dumps(mocked_running_result_response), 'byte')

        mock_results_response.side_effect = [mock_query_job_id_response,mock_query_poll_running_response,mock_query_poll_running_response,mock_query_poll_response,mock_query_poll_response,mock_delete_job_id_response]
        entry_point = EntryPoint(self.connection(), self.configuration())
        results_response = run_in_thread(entry_point.create_results_connection, search_id, 0, 1, metadata)
        success = results_response["success"]
        assert success
        data = results_response["data"]
        assert data
        assert (results_response['metadata'] ==
                {'input_query_string': 'behaviors[0].filename="cmd.exe" OR '
                                          'behaviors[0].filename="conhost.exe"',
                           'start': 1710921332365,
                           'last_event_id': 'ATzrtyg4xCKOqQnD9NodpvsY_363_21_1711549347',
                                      'last_event_timestamp': 1711549342830})


    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_results_using_metadata_for_next_iteration_with_timeout_exception(self, mock_results_response):
        """ test failure response for results with timeout exception when status connector
        is called to check status of intermediate query job id from results"""
        search_id = "P3-ohFBXrfxvfy3U1xk28PLFJKL:edr"
        mocked_running_result_response = {
            "cancelled": False,
            "done": False,
            "events": [],
            "metaData":
                {"eventCount": 0,
                 "filterQuery":
                     {"end": 1711549347952,
                      "queryString": "behaviors[0].filename=\"cmd.exe\" OR behaviors[0].filename=\"conhost.exe\"",
                      "start": 1710921332365}},
            "warnings": []}

        metadata = {'input_query_string': 'behaviors[0].filename="cmd.exe" OR '
                                          'behaviors[0].filename="conhost.exe"',
                           'start': 1710921332365,
                           'last_event_id': 'ATzrtyg4xCKOqQnD9NodpvsY_363_23_1711549347',
                             'last_event_timestamp': 1711549347952}

        mock_delete_job_id_response = get_mock_response(204, "", 'byte')
        mock_query_job_id_response = get_mock_response(200, json.dumps({"hashedQueryOnView": "456ac", "id": "P6-o1FbXrfxvfy3U1xk28PLFijk"}), 'byte')
        mock_query_poll_running_response = get_mock_response(200, json.dumps(mocked_running_result_response), 'byte')
        mock_results_response.side_effect = [mock_query_job_id_response,mock_query_poll_running_response,mock_query_poll_running_response,Exception("timeout_error"),mock_delete_job_id_response]
        entry_point = EntryPoint(self.connection_with_result_limit(), self.configuration())
        results_response = run_in_thread(entry_point.create_results_connection, search_id, 2000, 1, metadata)
        assert results_response["success"] is False
        assert 'timeout_error' in results_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_results_using_metadata_for_next_iteration_with_status_cancelled(self, mock_results_response):
        """ test response for results with status connector being called to check status
        for cancelled intermediate query job id """
        search_id = "P3-ohFBXrfxvfy3U1xk28PLFJKL:edr"
        mocked_running_result_response = {
            "cancelled": False,
            "done": False,
            "events": [],
            "metaData":
                {"eventCount": 0,
                 "filterQuery":
                     {"end": 1711549347952,
                      "queryString": "behaviors[0].filename=\"cmd.exe\" OR behaviors[0].filename=\"conhost.exe\"",
                      "start": 1710921332365}},
            "warnings": []}
        mocked_cancelled_result_response = {
            "cancelled": True,
            "done": False,
            "events": [],
            "metaData":
                {"eventCount": 0,
                 "filterQuery":
                     {"end": 1711549347952,
                      "queryString": "behaviors[0].filename=\"cmd.exe\" OR behaviors[0].filename=\"conhost.exe\"",
                      "start": 1710921332365}},
            "warnings": []}

        metadata = {'input_query_string': 'behaviors[0].filename="cmd.exe" OR '
                                          'behaviors[0].filename="conhost.exe"',
                           'start': 1710921332365,
                           'last_event_id': 'ATzrtyg4xCKOqQnD9NodpvsY_363_23_1711549347',
                             'last_event_timestamp': 1711549347952}

        mock_delete_job_id_response = get_mock_response(204, "", 'byte')
        mock_query_job_id_response = get_mock_response(200, json.dumps({"hashedQueryOnView": "456ac", "id": "P6-o1FbXrfxvfy3U1xk28PLFijk"}), 'byte')
        mock_query_poll_running_response = get_mock_response(200, json.dumps(mocked_running_result_response), 'byte')
        mock_status_cancelled_response = get_mock_response(200, json.dumps(mocked_cancelled_result_response), 'byte')

        mock_results_response.side_effect = [mock_query_job_id_response,mock_query_poll_running_response,mock_query_poll_running_response,mock_status_cancelled_response,mock_delete_job_id_response]
        entry_point = EntryPoint(self.connection_with_result_limit(), self.configuration())
        results_response = run_in_thread(entry_point.create_results_connection, search_id, 2000, 1, metadata)
        assert results_response["success"] is True
        assert results_response["data"] == []

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_results_with_failure_response_during_job_id_creation_with_metadata(self, mock_results_response):
        """ test failure response for results when query job id creation failed when metadata is passed"""
        search_id = "P3-ohFBXrfxvfy3U1xk28PLFJKL:edr"
        mock_results_response.return_value = \
            get_mock_response(401, "The supplied authentication is invalid", 'byte')

        metadata = {'input_query_string': 'behaviors[0].filename="cmd.exe" OR '
                                          'behaviors[0].filename="conhost.exe"',
                    'start': 1710921332365,
                    'last_event_id': 'ATzrtyg4xCKOqQnD9NodpvsY_363_23_1711549347',
                    'last_event_timestamp': 1711549347952}
        entry_point = EntryPoint(self.connection_with_result_limit(), self.configuration())
        results_response = run_in_thread(entry_point.create_results_connection, search_id, 2000, 1, metadata)
        assert results_response["success"] is False
        assert "The supplied authentication is invalid" in results_response["error"]
        assert results_response["code"] == "authentication_fail"

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_results_with_failure_response_during_status_check_with_metadata(self, mock_results_response):
        """ test failure response for results during status check with metadata"""
        search_id = "P3-ohFBXrfxvfy3U1xk28PLFJKL:edr"
        invalid_response = \
            get_mock_response(401, "The supplied authentication is invalid", 'byte')
        mock_query_job_id_response = get_mock_response(200, json.dumps(
            {"hashedQueryOnView": "456ac", "id": "P6-o1FbXrfxvfy3U1xk28PLFijk"}), 'byte')
        mock_results_response.side_effect = [mock_query_job_id_response, invalid_response]

        metadata = {'input_query_string': 'behaviors[0].filename="cmd.exe" OR '
                                          'behaviors[0].filename="conhost.exe"',
                    'start': 1710921332365,
                    'last_event_id': 'ATzrtyg4xCKOqQnD9NodpvsY_363_23_1711549347',
                    'last_event_timestamp': 1711549347952}
        entry_point = EntryPoint(self.connection_with_result_limit(), self.configuration())
        results_response = run_in_thread(entry_point.create_results_connection, search_id, 2000, 1, metadata)
        assert results_response["success"] is False
        assert "The supplied authentication is invalid" in results_response["error"]
        assert results_response["code"] == "authentication_fail"


    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_invalid_authentication_failure_in_transmit_query(self, mock_query_response):
        """ test authentication fail"""
        query = {"source": "edr",
                 "queryString": "behaviors[0].filename=\"cmd.exe\" OR behaviors[0].filename=\"conhost.exe\" | tail(10000)",
                 "start": 1710921332365, "end": 1711549347952}
        mock_query_response.return_value = \
            get_mock_response(401, "The supplied authentication is invalid", 'byte')
        entry_point = EntryPoint(self.connection(), self.configuration())
        query_result = run_in_thread(entry_point.create_query_connection, json.dumps(query))
        assert query_result["success"] is False
        assert "The supplied authentication is invalid" in query_result["error"]
        assert query_result["code"] == "authentication_fail"


    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_invalid_query_in_transmit(self, mock_query_response):
        query = {"source": "edr",
                 "querystring": "behaviors[0].filename=\"cmd.exe\" OR behaviors[0].filename=\"conhost.exe\" | tail(10000)",
                 "start": 1710921332365, "end": 1711549347952}
        mock_query_response.return_value = \
            get_mock_response(400, "The request content was malformed:\nObject is missing required member 'queryString'", 'byte')
        entry_point = EntryPoint(self.connection(), self.configuration())
        query_result = run_in_thread(entry_point.create_query_connection, json.dumps(query))
        assert query_result["success"] is False
        assert "The request content was malformed:\nObject is missing required member 'queryString'" in query_result["error"]
        assert query_result["code"] == "invalid_query"

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_invalid_search_id_in_status(self, mock_status_response):
        """ test invalid search id in status"""
        search_id = "P3-ohFBXrfxvfy3U1xk28PLFJKL:edr"
        mock_status_response.return_value = \
            get_mock_response(404, "No query with id=P3-ohFBXrfxvfy3U1xk28PLFJKL", 'byte')
        entry_point = EntryPoint(self.connection(), self.configuration())
        status_response = run_in_thread(entry_point.create_status_connection, search_id)
        assert status_response["success"] is False
        assert "No query with id=P3-ohFBXrfxvfy3U1xk28PLFJKL" in status_response[
            "error"]
        assert status_response["code"] == "no_results"

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_invalid_search_id_in_results(self, mock_results_response):
        """ test invalid search id in results"""
        search_id = "P3-ohFBXrfxvfy3U1xk28PLFJKL:edr"
        mock_results_response.return_value = \
            get_mock_response(404, "No query with id=P3-ohFBXrfxvfy3U1xk28PLFJKL", 'byte')
        entry_point = EntryPoint(self.connection(), self.configuration())
        results_response = run_in_thread(entry_point.create_results_connection, search_id, 0, 10000)
        assert results_response["success"] is False
        assert "No query with id=P3-ohFBXrfxvfy3U1xk28PLFJKL" in results_response[
            "error"]
        assert results_response["code"] == "no_results"

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_time_out_exception_for_results(self, mock_result_response):
        """ test time out exception in results"""
        mock_result_response.side_effect = Exception("timeout_error")
        search_id = "P3-ohFBXrfxvfy3U1xk28PLFJKL:edr"
        entry_point = EntryPoint(self.connection(), self.configuration())
        result_response = run_in_thread(entry_point.create_results_connection, search_id, 0, 10000)
        assert result_response is not None
        assert result_response['success'] is False
        assert 'error' in result_response
        assert 'timeout_error' in result_response['error']
        assert result_response['code'] == 'service_unavailable'


    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_time_out_exception_for_ping(self, mock_ping_response):
        """ test timeout exception for ping"""
        mock_ping_response.side_effect = Exception("timeout_error")
        entry_point = EntryPoint(self.connection(), self.configuration())
        ping_result = run_in_thread(entry_point.ping_connection)
        assert ping_result is not None
        assert ping_result['success'] is False
        assert 'error' in ping_result
        assert 'timeout_error' in ping_result['error']
        assert ping_result['code'] == 'service_unavailable'









