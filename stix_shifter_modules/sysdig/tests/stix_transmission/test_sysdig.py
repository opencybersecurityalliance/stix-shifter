""" test script to perform unit test case for sysdig transmit module """
import json
import unittest
from unittest.mock import patch
from stix_shifter_modules.sysdig.entry_point import EntryPoint
from stix_shifter.stix_transmission import stix_transmission
from stix_shifter.stix_transmission.stix_transmission import run_in_thread
from tests.utils.async_utils import get_mock_response


class sysdigMockResponse:
    """ class for sysdig mock response"""

    def __init__(self, code, data):
        self.code = code
        self.content = data

    def read(self):
        return bytearray(self.content, 'utf-8')


class TestsysdigConnection(unittest.TestCase):
    mocked_response = {'page': {'total': 1, 'prev': 'ABC3ODI4OFHIwM2EzZTY1ODJkYzMzYWEwODBhMTVmMGM123',
                                'next': 'ABCzE3ODI4OGYwM2EzZTY1ODJkYzMzYWEwODBhMTVmMGM123'},
                       'data': [
                           {
                               "id": "12345678910",
                               "cursor": "ABCDEFGHIJKLMN",
                               "timestamp": "2023-11-22T11:16:28.101680299Z",
                               "customerId": 10101010,
                               "originator": "policy",
                               "category": "runtime",
                               "source": "syscall",
                               "name": "sysdig custom",
                               "description": "updated network rules with network tag",
                               "severity": 0,
                               "agentId": 111111,
                               "containerId": "1010101010",
                               "machineId": "11:11:1b:11:11:11",
                               "content": {
                                   "falsePositive": "false",
                                   "fields": {
                                       "container.id": "1010101010",
                                       "container.image.repository": "docker.io",
                                       "container.image.tag": "curl",
                                       "container.name": "curl-sample-app1",
                                       "evt.res": "EINPROGRESS",
                                       "evt.type": "connect",
                                       "falco.rule": "Contact EC2",
                                       "fd.name": "111.111.11.111:10000->101.101.101.101:10",
                                       "group.gid": "0",
                                       "group.name": "root",
                                       "proc.aname[2]": "containerd-shim",
                                       "proc.aname[3]": "systemd",
                                       "proc.aname[4]": "",
                                       "proc.args": "-s http://101.101.101.101:10/iam/security-credentials",
                                       "proc.cmdline": "curl -s http://101.101.101.101:10/iam/security-credentials",
                                       "proc.cwd": "/",
                                       "proc.exepath": "/usr/bin/curl",
                                       "proc.name": "curl",
                                       "proc.pcmdline": "sh",
                                       "proc.pid": "12345",
                                       "proc.pname": "sh",
                                       "proc.ppid": "11111",
                                       "proc.sid": "1",
                                       "user.loginname": "",
                                       "user.loginuid": "-1",
                                       "user.name": "root",
                                       "user.uid": "0"
                                   },
                                   "internalRuleName": "Contact",
                                   "matchedOnDefault": "false",
                                   "origin": "Secure UI",
                                   "policyId": 100100,
                                   "ruleName": "Contact EC2",
                                   "ruleSubType": 0,
                                   "ruleTags": [
                                       "container",
                                       "network",
                                       "aws",
                                       "SOC2",
                                       "SOC2_CC6.8",
                                       "SOC2_CC6.1",
                                       "NIST",
                                       "NIST_800-171",
                                       "NIST_800-171_3.1.1",
                                       "NIST_800-171_3.1.2",
                                       "NIST_800-171_3.1.3",
                                       "NIST_800-171_3.14.6",
                                       "NIST_800-171_3.14.7",
                                       "NIST_800-171_3.4.6",
                                       "NIST_800-53",
                                       "NIST_800-53_AC-4",
                                       "NIST_800-53_AC-17",
                                       "NIST_800-53_SI-4(18)",
                                       "NIST_800-53_SI-4",
                                       "NIST_800-53_CM-7",
                                       "FedRAMP",
                                       "FedRAMP_CM-7",
                                       "ISO",
                                       "ISO_27001",
                                       "ISO_27001_A.9.1.2",
                                       "HIPAA",
                                       "HIPAA_164.308(a)",
                                       "HIPAA_164.310(b)",
                                       "HITRUST",
                                       "HITRUST_CSF",
                                       "HITRUST_CSF_01.c",
                                       "HITRUST_CSF_01.i",
                                       "HITRUST_CSF_01.j",
                                       "HITRUST_CSF_01.l",
                                       "HITRUST_CSF_01.n",
                                       "HITRUST_CSF_01.x",
                                       "HITRUST_CSF_01.y",
                                       "HITRUST_CSF_09.ab",
                                       "HITRUST_CSF_09.ac",
                                       "HITRUST_CSF_09.i",
                                       "HITRUST_CSF_09.m",
                                       "HITRUST_CSF_09.s",
                                       "HITRUST_CSF_10.j",
                                       "HITRUST_CSF_10.m",
                                       "HITRUST_CSF_11.a",
                                       "HITRUST_CSF_11.b",
                                       "GDPR",
                                       "GDPR_32.1",
                                       "GDPR_32.2",
                                       "MITRE",
                                       "MITRE_T1552_unsecured_credentials",
                                       "MITRE_T1552.005_unsecured_credentials_cloud_instance_metadata_api",
                                       "MITRE_TA0006_credential_access",
                                       "MITRE_TA0007_discovery",
                                       "MITRE_T1552.007_unsecured_credentials_container_api",
                                       "MITRE_T1033_system_owner_user_discovery",
                                       "MITRE_T119_automated-collection",
                                       "MITRE_TA0009_collection"
                                   ],
                                   "ruleType": 6
                               },
                               "labels": {
                                   "aws.accountId": "111111111111",
                                   "aws.instanceId": "i-1111111111",
                                   "aws.region": "us-east-1",
                                   "cloudProvider.account.id": "111111111111",
                                   "cloudProvider.name": "aws",
                                   "cloudProvider.region": "us-east-1",
                                   "container.image.digest": "sha256:12345",
                                   "container.image.id": "10101010",
                                   "container.image.repo": "docker.io/radial/busyboxplus",
                                   "container.image.tag": "curl",
                                   "container.label.io.kubernetes.container.name": "curl-sample-app1",
                                   "container.label.io.kubernetes.pod.name": "curl-sample-app1",
                                   "container.label.io.kubernetes.pod.namespace": "default",
                                   "container.name": "curl-sample-app1",
                                   "host.hostName": "ip-111-111-11-111.ec2.internal",
                                   "host.mac": "11:11:11:11:11:11",
                                   "kubernetes.cluster.name": "sysdig",
                                   "kubernetes.namespace.name": "default",
                                   "kubernetes.node.name": "ip-111-111-11-111.ec2.internal",
                                   "kubernetes.pod.name": "curl-sample-app1",
                                   "process.name": "curl -s http://101.101.101.101/iam/security-credentials"
                               },
                               "finding_type": "threat",
                               "direction": "out",
                               "clientIpv4": "111.111.11.111",
                               "clientPort": "10000",
                               "serverIpv4": "101.101.101.101",
                               "serverPort": "10",
                               "l4protocol": "tcp"
                           }
                       ]
                       }

    replicated_data = []
    for _ in range(1000):
        replicated_data += mocked_response['data']
    mocked_response['data'] = replicated_data
    network_mocked_response = {'page': {'total': 1, 'prev': 'ABC3ODI4OFHIwM2EzZTY1ODJkYzMzYWEwODBhMTVmMGM123',
                                        'next': 'ABCzE3ODI4OGYwM2EzZTY1ODJkYzMzYWEwODBhMTVmMGM123'},
                               'data': [
                                   {
                                       "id": "12345678910",
                                       "cursor": "ABCDEFGHIJKLMN",
                                       "timestamp": "2023-11-22T11:16:28.101680299Z",
                                       "customerId": 10101010,
                                       "originator": "policy",
                                       "category": "runtime",
                                       "source": "syscall",
                                       "name": "sysdig custom",
                                       "description": "updated network rules with network tag",
                                       "severity": 0,
                                       "agentId": 111111,
                                       "containerId": "1010101010",
                                       "machineId": "11:11:1b:11:11:11",
                                       "content": {
                                           "falsePositive": "false",
                                           "fields": {
                                               "container.id": "1010101010",
                                               "container.image.repository": "docker.io",
                                               "container.image.tag": "curl",
                                               "container.name": "curl-sample-app1",
                                               "evt.res": "EINPROGRESS",
                                               "evt.type": "connect",
                                               "falco.rule": "Contact EC2",
                                               "fd.name": "111.111.11.111:10000<-101.101.101.101:10",
                                               "group.gid": "0",
                                               "group.name": "root",
                                               "proc.aname[2]": "containerd-shim",
                                               "proc.aname[3]": "systemd",
                                               "proc.aname[4]": "",
                                               "proc.args": "-s http://101.101.101.101:10/iam/security-credentials",
                                               "proc.cmdline": "curl -s http://101.101.101.101:10/"
                                                               "iam/security-credentials",
                                               "proc.cwd": "/",
                                               "proc.exepath": "/usr/bin/curl",
                                               "proc.name": "curl",
                                               "proc.pcmdline": "sh",
                                               "proc.pid": "12345",
                                               "proc.pname": "sh",
                                               "proc.ppid": "11111",
                                               "proc.sid": "1",
                                               "user.loginname": "",
                                               "user.loginuid": "-1",
                                               "user.name": "root",
                                               "user.uid": "0"
                                           },
                                           "internalRuleName": "Contact",
                                           "matchedOnDefault": "false",
                                           "origin": "Secure UI",
                                           "policyId": 100100,
                                           "ruleName": "Contact EC2",
                                           "ruleSubType": 0,
                                           "ruleTags": [
                                               "container",
                                               "network",
                                               "aws",
                                               "SOC2",
                                               "SOC2_CC6.8",
                                               "SOC2_CC6.1",
                                               "NIST",
                                               "NIST_800-171",
                                               "NIST_800-171_3.1.1",
                                               "NIST_800-171_3.1.2",
                                               "NIST_800-171_3.1.3",
                                               "NIST_800-171_3.14.6",
                                               "NIST_800-171_3.14.7",
                                               "NIST_800-171_3.4.6",
                                               "NIST_800-53",
                                               "NIST_800-53_AC-4",
                                               "NIST_800-53_AC-17",
                                               "NIST_800-53_SI-4(18)",
                                               "NIST_800-53_SI-4",
                                               "NIST_800-53_CM-7",
                                               "FedRAMP",
                                               "FedRAMP_CM-7",
                                               "ISO",
                                               "ISO_27001",
                                               "ISO_27001_A.9.1.2",
                                               "HIPAA",
                                               "HIPAA_164.308(a)",
                                               "HIPAA_164.310(b)",
                                               "HITRUST",
                                               "HITRUST_CSF",
                                               "HITRUST_CSF_01.c",
                                               "HITRUST_CSF_01.i",
                                               "HITRUST_CSF_01.j",
                                               "HITRUST_CSF_01.l",
                                               "HITRUST_CSF_01.n",
                                               "HITRUST_CSF_01.x",
                                               "HITRUST_CSF_01.y",
                                               "HITRUST_CSF_09.ab",
                                               "HITRUST_CSF_09.ac",
                                               "HITRUST_CSF_09.i",
                                               "HITRUST_CSF_09.m",
                                               "HITRUST_CSF_09.s",
                                               "HITRUST_CSF_10.j",
                                               "HITRUST_CSF_10.m",
                                               "HITRUST_CSF_11.a",
                                               "HITRUST_CSF_11.b",
                                               "GDPR",
                                               "GDPR_32.1",
                                               "GDPR_32.2",
                                               "MITRE",
                                               "MITRE_T1552_unsecured_credentials",
                                               "MITRE_T1552.005_unsecured_credentials_cloud_instance_metadata_api",
                                               "MITRE_TA0006_credential_access",
                                               "MITRE_TA0007_discovery",
                                               "MITRE_T1552.007_unsecured_credentials_container_api",
                                               "MITRE_T1033_system_owner_user_discovery",
                                               "MITRE_T119_automated-collection",
                                               "MITRE_TA0009_collection"
                                           ],
                                           "ruleType": 6
                                       },
                                       "labels": {
                                           "aws.accountId": "111111111111",
                                           "aws.instanceId": "i-1111111111",
                                           "aws.region": "us-east-1",
                                           "cloudProvider.account.id": "111111111111",
                                           "cloudProvider.name": "aws",
                                           "cloudProvider.region": "us-east-1",
                                           "container.image.digest": "sha256:12345",
                                           "container.image.id": "10101010",
                                           "container.image.repo": "docker.io/radial/busyboxplus",
                                           "container.image.tag": "curl",
                                           "container.label.io.kubernetes.container.name": "curl-sample-app1",
                                           "container.label.io.kubernetes.pod.name": "curl-sample-app1",
                                           "container.label.io.kubernetes.pod.namespace": "default",
                                           "container.name": "curl-sample-app1",
                                           "host.hostName": "ip-111-111-11-111.ec2.internal",
                                           "host.mac": "11:11:11:11:11:11",
                                           "kubernetes.cluster.name": "sysdig",
                                           "kubernetes.namespace.name": "default",
                                           "kubernetes.node.name": "ip-111-111-11-111.ec2.internal",
                                           "kubernetes.pod.name": "curl-sample-app1",
                                           "process.name": "curl -s http://101.101.101.101/iam/security-credentials",
                                       },
                                       "finding_type": "threat",
                                       "direction": "in",
                                       "clientIpv4": "101.101.101.101",
                                       "clientPort": "10",
                                       "serverIpv4": "111.111.111.111",
                                       "serverPort": "10000",
                                       "l4protocol": "tcp"
                                   }
                               ]
                               }

    @staticmethod
    def connection():
        """format for connection"""
        return {
            "host": "testhost",
            "port": 123
        }

    @staticmethod
    def configuration():
        """format for configuration"""
        return {
            "auth": {
                "token": "test"

            }
        }

    def test_is_async(self):
        """check for synchronous or asynchronous"""
        entry_point = EntryPoint(self.connection(), self.configuration())
        check_async = entry_point.is_async()
        assert check_async is False

    @patch('stix_shifter_modules.sysdig.stix_transmission.api_client.APIClient.ping_data_source')
    def test_get_ping_results(self, mock_ping_response):
        """test ping connection"""
        mock_ping_response.return_value = get_mock_response(200, json.dumps(TestsysdigConnection.mocked_response),
                                                            'byte')
        entry_point = EntryPoint(self.connection(), self.configuration())
        ping_response = run_in_thread(entry_point.ping_connection)
        assert ping_response is not None
        assert ping_response['success'] is True

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_ping_timeout_error(self, mock_result_response):
        """Test timeout error for ping"""
        mock_result_response.side_effect = Exception(" server timeout_error")
        transmission = stix_transmission.StixTransmission('sysdig', self.connection(), self.configuration())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert "server timeout_error" in ping_response['error']
        assert ping_response['code'] == "service_unavailable"

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_ping_invalid_host(self, mock_result_response):
        """Test Invalid host for ping"""
        mock_result_response.side_effect = Exception("client_connector_error")
        transmission = stix_transmission.StixTransmission('sysdig', self.connection(), self.configuration())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert "client_connector_error" in ping_response['error']
        assert ping_response['code'] == "service_unavailable"

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_ping_invalid_token_results(self, mock_result_response):
        """ test invalid token results response"""
        mocked_return_value = json.dumps({
            "success": 'false',
            "connector": "sysdig",
            "error": "sysdig connector error => cannot verify credentials'",
            "code": "authentication_fail"
        })
        mock_result_response.return_value = sysdigMockResponse(401, mocked_return_value)
        transmission = stix_transmission.StixTransmission('sysdig', self.connection(), self.configuration())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert ping_response['code'] == 'authentication_fail'

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_success_query_results(self, mock_result_response):
        """ test success result response"""
        mocked_return_value = json.dumps(TestsysdigConnection.mocked_response)
        query = "from=1693526400000000000&to=1694512800000000000&filter=kubernetes.cluster.name=\"cp5s-cluster\""
        mock_result_response.return_value = sysdigMockResponse(200, mocked_return_value)
        transmission = stix_transmission.StixTransmission('sysdig', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is True
        assert 'data' in result_response
        assert result_response['data'] is not None

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_success_query_results_with_pagination(self, mock_result_response):
        """ test success pagination result response"""
        mocked_return_value = json.dumps(TestsysdigConnection.mocked_response)
        query = "from=1697388206000000000&to=1698511406003000064&filter=(source=\"syscall\"andoriginator=\"policy\"" \
                "andcategory=\"runtime\")andsource!=\"auditTrail\""
        mock_result_response.return_value = sysdigMockResponse(200, mocked_return_value)
        transmission = stix_transmission.StixTransmission('sysdig', self.connection(), self.configuration())
        offset = 0
        length = 2000
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is True
        assert 'data' in result_response
        assert result_response['data'] is not None

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_success_query_results_with_network_data(self, mock_result_response):
        """ test success network fields result response"""
        mocked_return_value = json.dumps(TestsysdigConnection.network_mocked_response)
        query = "from=1697388206000000000&to=1698511406003000064&filter=(source=\"syscall\"andoriginator=\"policy\"" \
                "andcategory=\"runtime\")andsource!=\"auditTrail\""
        mock_result_response.return_value = sysdigMockResponse(200, mocked_return_value)
        transmission = stix_transmission.StixTransmission('sysdig', self.connection(), self.configuration())
        offset = 0
        length = 2000
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is True
        assert 'data' in result_response
        assert result_response['data'] is not None

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_success_query_with_metadata_parameter(self, mock_result_response):
        """ test success result response with metadata parameter"""
        mocked_return_value = json.dumps(TestsysdigConnection.mocked_response)
        metadata = {"result_count": 1, "prev_page_token": "a12b3c"}
        query = "from=1693526400000000000&to=1694512800000000000&filter=kubernetes.cluster.name=\"ap4s-cluster\""
        mock_result_response.return_value = sysdigMockResponse(200, mocked_return_value)
        transmission = stix_transmission.StixTransmission('sysdig', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length, metadata)
        assert result_response is not None
        assert result_response['success'] is True
        assert 'data' in result_response

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_success_with_invalid_metadata_parameter(self, mock_result_response):
        """ test invalid metadata parameter"""
        mocked_return_value = json.dumps(TestsysdigConnection.mocked_response)
        metadata = {"prev_page_token": "a12b3c"}
        query = "from=1693526400000000000&to=1694512800000000000&filter=kubernetes.cluster.name=\"ap4s-cluster\""
        mock_result_response.return_value = sysdigMockResponse(200, mocked_return_value)
        transmission = stix_transmission.StixTransmission('sysdig', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length, metadata)
        assert result_response is not None
        assert result_response['success'] is False
        assert "Invalid metadata" in result_response['error']
        assert result_response['code'] == "invalid_parameter"

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_query_results_with_invalid_host(self, mock_result_response):
        """ test invalid host """
        mock_result_response.side_effect = Exception("client_connector_error")
        query = "from=1693526400000000000&to=1694512800000000000&filter=kubernetes.cluster.name=\"ap5s-cluster\""
        mock_result_response.return_value = sysdigMockResponse(200, mock_result_response)
        transmission = stix_transmission.StixTransmission('sysdig', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert 'client_connector_error' in result_response['error']
        assert result_response['code'] == 'service_unavailable'

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_query_server_timeout_error(self, mock_result_response):
        """ test query server timeout error"""
        mock_result_response.side_effect = Exception("server timeout_error")
        query = "from=1693526400000000000&to=1694512800000000000&filter=kubernetes.cluster.name=\"cp5s-cluster\""
        mock_result_response.return_value = sysdigMockResponse(200, mock_result_response)
        transmission = stix_transmission.StixTransmission('sysdig', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert 'server timeout_error' in result_response['error']
        assert result_response['code'] == 'service_unavailable'

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_query_timeout_error(self, mock_result_response):
        """ test query timeout error"""
        mock_result_response.side_effect = Exception("timeout_error")
        query = "from=1697388206000000000&to=1698511406003000064&filter=(source=\"syscall\"andoriginator=\"policy\"" \
                "andcategory=\"runtime\")andsource!=\"auditTrail\""
        mock_result_response.return_value = sysdigMockResponse(200, mock_result_response)
        transmission = stix_transmission.StixTransmission('sysdig', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert 'timeout_error' in result_response['error']
        assert result_response['code'] == 'service_unavailable'

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_invalid_query_results(self, mock_result_response):
        """ test error result response"""
        mocked_return_value = json.dumps({
            "success": 'false',
            "connector": "sysdig",
            "error": "sysdig connector error => bad request",
            "code": "invalid_parameter"})

        query = "from=1693526400000000000&to=1694512800000000000&filter=kubernetes.cluster.name=\"cp5s-cluster\""
        mock_result_response.return_value = sysdigMockResponse(400, mocked_return_value)
        transmission = stix_transmission.StixTransmission('sysdig', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert result_response['code'] == 'invalid_parameter'

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_invalid_token_results(self, mock_result_response):
        """ test invalid token response"""
        mocked_return_value = json.dumps({
            "success": 'false',
            "connector": "sysdig",
            "error": "sysdig connector error => cannot verify credentials",
            "code": "authentication_fail"
        })
        query = "from=1693526400000000000&to=1694512800000000000&filter=kubernetes.cluster.name=\"cp5s-cluster\""
        mock_result_response.return_value = sysdigMockResponse(401, mocked_return_value)
        transmission = stix_transmission.StixTransmission('sysdig', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert result_response['code'] == 'authentication_fail'

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_exception_query_check(self, mock_result_response):
        """ test error result response"""
        mocked_return_value = json.dumps({
            "success": 'false',
            "connector": "sysdig",
            "error": "sysdig connector error => unsupported metric",
            "code": "invalid_query"
        })

        query = "from=1693526400000000000&to=1694512800000000000&filter=kubernetes.cluster.name=\"cp5s-cluster\""
        mock_result_response.return_value = sysdigMockResponse(422, mocked_return_value)
        transmission = stix_transmission.StixTransmission('sysdig', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert result_response['code'] == 'invalid_query'
