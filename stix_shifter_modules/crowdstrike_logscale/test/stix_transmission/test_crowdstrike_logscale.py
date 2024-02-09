from stix_shifter_modules.crowdstrike_logscale.entry_point import EntryPoint
import unittest
from unittest.mock import patch
from stix_shifter.stix_transmission import stix_transmission
import json
from stix_shifter.stix_transmission.stix_transmission import run_in_thread
from tests.utils.async_utils import get_mock_response


class CrowdStrikeLogscaleResponse:
    """ class for CrowdStrike Logscale mock response"""

    def __init__(self, code, data, headers):
        self.code = code
        self.content = data
        self.headers = headers

    def read(self):
        return bytearray(self.content, 'utf-8')


class TestCrowdStrikeLogscaleConnection(unittest.TestCase, object):
    mocked_ping_response = {"status": "OK",
                            "version": "1.x.0--build-4xxx0--sha-9638xxxxb376"}

    mock_search_result = [
        {
            'behaviors[0].pattern_disposition_details.inddet_mask': 'false',
            'behaviors[0].pattern_disposition_details.kill_action_failed': 'false',
            'behaviors[0].technique': 'Indicator of Attack',
            'seconds_to_resolved': '0',
            'device.local_ip': '172.0.0.1',
            'behaviors[0].pattern_disposition_details.handle_operation_downgraded': 'false',
            'device.product_type_desc': 'Server',
            'device.os_version': 'Windows Server 2019',
            'behaviors[0].tactic': 'Custom Intelligence',
            'behaviors[0].ioc_description': '\\Dev\\HDD\\Windows\\System32\\cmd.exe',
            'max_severity': '50',
            'behaviors[0].pattern_disposition_details.suspend_process': 'false',
            '@timestamp': 1695184200000,
            '@ingesttimestamp': '1695225528387',
            'hostinfo.domain': '',
            '#type': 'zeek-json',
            'behaviors[0].pattern_disposition_details.rooting': 'false',
            'device.product_type': '3',
            '@error': 'true',
            'behaviors[0].description': 'A process triggered a medium severity custom rule.',
            'behaviors[0].pattern_disposition_details.kill_process': 'false',
            'device.config_id_platform': '3',
            'behaviors[0].behavior_id': '41002',
            'behaviors[0].ioc_source': 'library_load',
            'device.platform_name': 'Windows',
            'behaviors[0].pattern_disposition_details.sensor_only': 'false',
            'behaviors[0].pattern_disposition_details.quarantine_machine': 'false',
            'behaviors[0].user_name': 'Administrator', 'behaviors[1].filename': 'cmd1234.exe',
            'show_in_ui': 'true',
            'detection_id': 'ldt:621axxxx84c3:318006871309',
            'device.external_ip': '1.1.1.1',
            'device.bios_manufacturer': 'Xen',
            'behaviors[0].technique_id': 'CST0004',
            'behaviors[0].parent_details.parent_md5': '911dxxxxx8e22',
            'device.platform_id': '0',
            '#repo': 'testrepo',
            'device.minor_version': '0',
            'device.bios_version': '4.11.amazon',
            'behaviors[0].display_name': 'CustomIOAWinMedium',
            'device.hostname': 'testhost',
            'behaviors[0].parent_details.parent_cmdline': 'C:\\Windows\\System32\\cmd.exe /c (type '
                                                          '"C:\\Users\\user~1\\AppData\\Local\\Temp\\2\\vscode-linux'
                                                          '-multi-line-command-cp4s-754957376.sh" | '
                                                          '"C:\\Windows\\System32\\OpenSSH\\ssh.exe" -T -D 5x7 cp4s '
                                                          'bash) & exit /b 0',
            'device.service_provider': 'cloud',
            '#humioBackfill': '0',
            'behaviors[0].pattern_disposition_details.blocking_unsupported_or_disabled': 'false',
            'behaviors[0].filepath': '\\dev\\hdd\\Windows\\System32\\cmd.exe',
            'behaviors[0].pattern_disposition_details.operation_blocked': 'false',
            'behaviors[0].md5': '911dxxxxx8e22',
            '#source': 'crowdstrike',
            'behaviors[0].pattern_disposition_details.kill_subprocess': 'false',
            'max_severity_displayname': 'Medium',
            'behaviors[0].pattern_disposition_details.registry_operation_blocked': 'false',
            'behaviors[0].pattern_disposition': '2048',
            'email_sent': 'true',
            'behaviors[0].triggering_process_graph_id': 'pid:621axxxx84c3:383827847524',
            'device.status': 'normal', 'behaviors[0].rule_instance_id': '3',
            'behaviors[0].objective': 'Falcon Detection Method',
            'behaviors[0].pattern_disposition_details.kill_parent': 'false',
            'behaviors[0].pattern_disposition_details.bootup_safeguard_enabled': 'false',
            'cid': 'ef21xxxx440d',
            'device.instance_id': 'odcxxxxxdco',
            'behaviors[0].parent_details.parent_sha256': 'bc86xxxxxc527',
            'device.config_id_base': '65xxx63',
            'behaviors[0].user_id': 'S-1-5-21-37xxx13xxx500',
            'behaviors_processed[0]': 'pid:621axxxxx84c3:383xxxx524:41002',
            'behaviors[0].pattern_disposition_details.policy_disabled': 'false',
            'behaviors[0].pattern_disposition_details.critical_process_disabled': 'false',
            'seconds_to_triaged': '0',
            'status': 'new',
            'device.major_version': '10',
            'max_confidence': '100',
            'device.agent_version': '6.58.11111.0',
            '@timezone': 'Z',
            'behaviors[0].filename': 'cmdhello.exe',
            'behaviors[0].parent_details.parent_process_graph_id': 'pid:621axxxx84c3:383xxxx251',
            'behaviors[0].control_graph_id': 'ctg:621axxxx84c3:318xxx309',
            'device.system_product_name': 'HVM domU',
            'behaviors[0].sha256': 'bc86xxxxc527',
            'device.config_id_build': '17212',
            'behaviors[0].cmdline': 'C:\\Windows\\system32\\cmd.exe  xxxxp\\2xxx.sh" "',
            'behaviors[0].ioc_type': 'hash_sha256',
            'behaviors[0].tactic_id': 'CSTA0005',
            'behaviors[0].pattern_disposition_details.quarantine_file': 'false',
            '#host': 'testhost',
            'behaviors[0].severity': '50',
            'device.system_manufacturer': 'Xen',
            'device.agent_load_flags': '1',
            'behaviors[0].confidence': '100',
            '@timestamp.nanos': '0',
            'behaviors[0].ioc_value': 'bc86xxxxc527',
            'behaviors[0].pattern_disposition_details.suspend_parent': 'false',
            'behaviors[0].template_instance_id': '3',
            'device.mac_address': '0a-2e-f9-27-ea-8b',
            '@rawstring': '{\n  "device.system_manufacturer": "Xen",\n  "device.platform_name": ... '
                          ' "seconds_to_triaged": "0"\n}',
            'behaviors[0].pattern_disposition_details.process_blocked': 'true',
            'behaviors[0].pattern_disposition_details.fs_operation_blocked': 'false'
        }
    ]

    @staticmethod
    def connection():
        """format for connection"""
        return {"host": "hostbla",
                "repository": "testrepo"
                }

    @staticmethod
    def configuration():
        """format for configuration"""
        return {
            "auth": {
                "api_token": "abcxxxxxyz"
            }
        }

    def test_is_async(self):
        """check for synchronous or asynchronous"""
        entry_point = EntryPoint(self.connection(), self.configuration())
        check_async = entry_point.is_async()
        assert check_async is False

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_success_ping(self, mock_ping_response):
        """test ping connection"""
        mock_ping_response.return_value = \
            get_mock_response(200, json.dumps(TestCrowdStrikeLogscaleConnection.mocked_ping_response), 'byte')
        entry_point = EntryPoint(self.connection(), self.configuration())
        ping_response = run_in_thread(entry_point.ping_connection)
        assert ping_response is not None
        assert ping_response['success'] is True

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_success_query_results(self, mock_result_response):
        """ test success result response"""
        query = '{"source": "edr", "queryString": "cmd.exe", "start": 1694596586561, "end": 1695295666000}'
        mock_result_response.return_value = get_mock_response(200, json.dumps(TestCrowdStrikeLogscaleConnection.
                                                                              mock_search_result), 'byte')
        transmission = stix_transmission.StixTransmission('crowdstrike_logscale', self.connection(),
                                                          self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is True
        assert 'data' in result_response

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_results_invalid_repository(self, mock_results_response):
        """Test invalid authentication for results"""
        error = b"could not find view=TestRepositor"
        query = '{"source": "edr", "queryString": "cmd.exe", "start": 1694596586561,"end": 1695295666000}'
        mock_results_response.return_value = get_mock_response(404, error)
        transmission = stix_transmission.StixTransmission('crowdstrike_logscale', self.connection(),
                                                          self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert result_response['code'] == "no_results"
        assert 'could not find view=TestRepositor' in result_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_results_invalid_auth(self, mock_results_response):
        """Test invalid authentication for results"""
        error = b"The supplied authentication is invalid"
        query = '{"source": "edr", "queryString": "cmd.exe", "start": 1694596586561,"end": 1695295666000}'
        mock_results_response.return_value = get_mock_response(401, error)
        transmission = stix_transmission.StixTransmission('crowdstrike_logscale', self.connection(),
                                                          self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert result_response['code'] == "authentication_fail"
        assert 'supplied authentication is invalid' in result_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_time_out_exception_for_results(self, mock_result_response):
        """Test timeout exception for results"""
        mock_result_response.side_effect = Exception("timeout_error")
        query = '{"source": "edr", "queryString": "cmd.exe", "start": 1694596586561,"end": 1695295666000}'
        transmission = stix_transmission.StixTransmission('crowdstrike_logscale', self.connection(),
                                                          self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert 'error' in result_response
        assert 'timeout_error' in result_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_time_out_exception_for_ping(self, mock_ping_response):
        """Test timeout exception for ping"""
        mock_ping_response.side_effect = Exception("timeout_error")
        transmission = stix_transmission.StixTransmission('crowdstrike_logscale', self.connection(),
                                                          self.configuration())
        result_response = transmission.ping()
        assert result_response is not None
        assert result_response['success'] is False
        assert 'error' in result_response
        assert 'timeout_error' in result_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_results_invalid_query(self, mock_results_response):
        """Test invalid query for results"""
        error = b"The request content was malformed:Object is missing required member \'queryString\'"
        query = '{"source": "edr", "quryString": "cmd.exe", "start": 1694596586561,"end": 1695295666000}'
        mock_results_response.return_value = get_mock_response(400, error)
        transmission = stix_transmission.StixTransmission('crowdstrike_logscale', self.connection(),
                                                          self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert result_response['code'] == "invalid_query"
        assert 'malformed:Object is missing required member' in result_response['error']
