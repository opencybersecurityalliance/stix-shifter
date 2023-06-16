from stix_shifter.stix_transmission.stix_transmission import run_in_thread
from stix_shifter_modules.azure_log_analytics.entry_point import EntryPoint
from stix_shifter.stix_transmission import stix_transmission
from tests.utils.async_utils import get_mock_response
from stix_shifter_modules.azure_log_analytics.stix_transmission.connector import Connector
from azure.core.exceptions import ODataV4Format, HttpResponseError, ClientAuthenticationError
import unittest
from unittest.mock import patch
import copy


class MockToken:
    token = "access_token123"


class ClientSecretMockResponse:
    @staticmethod
    async def get_token(scope):
        return MockToken

    @staticmethod
    async def close():
        pass


@patch('stix_shifter_modules.azure_log_analytics.stix_transmission.api_client.ClientSecretCredential')
class TestAzureLogAnalyticsConnection(unittest.TestCase, object):
    def connection(self):
        return {
            "host": "host",
            "port": 443,
            "workspaceId": "abc12345"
        }

    def config(self):
        return {
            "auth": {
                "tenant": "abc12345",
                "clientId": "abc12345",
                "clientSecret": "abc12345"
            }
        }

    def test_is_async(self, mock_generate_token):
        mock_generate_token.return_value = ClientSecretMockResponse
        entry_point = EntryPoint(self.connection(), self.config())
        check_async = entry_point.is_async()

        assert check_async is False

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_ping_endpoint(self, mock_ping_response, mock_generate_token):
        mock_generate_token.return_value = ClientSecretMockResponse
        mocked_return_value = '["mock", "placeholder"]'

        mock_ping_response.return_value = get_mock_response(200, mocked_return_value)
        transmission = stix_transmission.StixTransmission('azure_log_analytics', self.connection(), self.config())
        ping_response = transmission.ping()

        assert ping_response is not None
        assert ping_response['success']

    @patch('stix_shifter_modules.azure_log_analytics.stix_transmission.api_client.APIClient.ping_box')
    def test_ping_endpoint_invalid_workspace(self, mock_ping_response, mock_generate_token):
        mock_generate_token.return_value = ClientSecretMockResponse
        mocked_return_value = """
        {
            "error": {
                "message": "The workspace could not be found",
                "code": "WorkspaceNotFoundError",
                "correlationId": "a1bc1a2c-f975-180b-1243-111e17a11e1c"
            }
        }
        """

        mock_ping_response.return_value = get_mock_response(404, mocked_return_value)

        transmission = stix_transmission.StixTransmission('azure_log_analytics', self.connection(), self.config())
        ping_response = transmission.ping()
        assert ping_response['success'] is False
        assert ping_response['error'] == "azure_log_analytics connector error => Invalid Parameter: workspaceId"
        assert ping_response['code'] == "invalid_parameter"

    @patch('stix_shifter_modules.azure_log_analytics.stix_transmission.api_client.APIClient.ping_box')
    def test_ping_endpoint_auth_exception(self, mock_ping_response, mock_generate_token):
        mock_generate_token.return_value = ClientSecretMockResponse
        mock_ping_response.side_effect = ClientAuthenticationError()
        transmission = stix_transmission.StixTransmission('azure_log_analytics', self.connection(), self.config())
        ping_response = transmission.ping()
        assert ping_response['success'] is False
        assert ping_response['error'] == "azure_log_analytics connector error => Invalid Authentication"
        assert ping_response['code'] == "authentication_fail"

    @patch('stix_shifter_modules.azure_log_analytics.stix_transmission.api_client.APIClient.ping_box')
    def test_ping_endpoint_host_exception(self, mock_ping_response, mock_generate_token):
        mock_generate_token.return_value = ClientSecretMockResponse
        mock_ping_response.side_effect = ClientAuthenticationError('invalid_resource')
        transmission = stix_transmission.StixTransmission('azure_log_analytics', self.connection(), self.config())
        ping_response = transmission.ping()
        assert ping_response['success'] is False
        assert ping_response['error'] == "azure_log_analytics connector error => Invalid Host/Port"
        assert ping_response['code'] == "service_unavailable"

    @patch('stix_shifter_modules.azure_log_analytics.stix_transmission.api_client.APIClient.ping_box')
    def test_ping_endpoint_invalid_tenant(self, mock_ping_response, mock_generate_token):
        mock_generate_token.return_value = ClientSecretMockResponse
        mock_ping_response.side_effect = ValueError('Invalid tenant')
        transmission = stix_transmission.StixTransmission('azure_log_analytics', self.connection(), self.config())
        ping_response = transmission.ping()
        assert ping_response['success'] is False
        assert ping_response['error'] == "azure_log_analytics connector error => Invalid Parameter: tenant"
        assert ping_response['code'] == "invalid_parameter"

    @patch('stix_shifter_modules.azure_log_analytics.stix_transmission.api_client.APIClient.ping_box')
    def test_ping_endpoint_timeout(self, mock_ping_response, mock_generate_token):
        mock_generate_token.return_value = ClientSecretMockResponse
        mock_ping_response.side_effect = TimeoutError()
        transmission = stix_transmission.StixTransmission('azure_log_analytics', self.connection(), self.config())
        ping_response = transmission.ping()
        assert ping_response['success'] is False
        assert ping_response['error'] == "azure_log_analytics connector error => TimeoutError "
        assert ping_response['code'] == "service_unavailable"

    @patch('stix_shifter_modules.azure_log_analytics.stix_transmission.api_client.APIClient.ping_box')
    def test_ping_endpoint_exception(self, mock_ping_response, mock_generate_token):
        mock_generate_token.return_value = ClientSecretMockResponse
        mock_ping_response.return_value = {}
        transmission = stix_transmission.StixTransmission('azure_log_analytics', self.connection(), self.config())
        ping_response = transmission.ping()
        assert ping_response['success'] is False
        assert ping_response['error'] == "azure_log_analytics connector error => \'dict\' object has no attribute " \
                                         "\'code\'"
        assert ping_response['code'] == "unknown"

    def test_query_connection(self, mock_generate_token):
        mock_generate_token.return_value = ClientSecretMockResponse

        query = "SecurityEvent | where IpAddress == '11.11.11.111'"
        transmission = stix_transmission.StixTransmission('azure_log_analytics', self.connection(), self.config())
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert 'search_id' in query_response
        assert query_response['search_id'] == query

    def test_status_query(self, mock_generate_token):
        mock_generate_token.return_value = ClientSecretMockResponse

        search_id = "SecurityEvent | where IpAddress == '11.11.11.111'"

        entry_point = EntryPoint(self.connection(), self.config())
        status_response = run_in_thread(entry_point.create_status_connection, search_id)
        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is True

    def test_run_search_exception(self, mock_generate_token):
        mock_generate_token.return_value = ClientSecretMockResponse
        query = "'SecurityEvent | where InvalidField == 'test'"
        transmission = stix_transmission.StixTransmission('azure_log_analytics', self.connection(), self.config())
        results_response = transmission.results(query, 0, 1)
        assert results_response['success'] is False
        assert results_response['code'] == "invalid_query"

    @patch(
        'stix_shifter_modules.azure_log_analytics.stix_transmission.connector.Connector.create_results_connection')
    def test_results_all_response(self, mock_results_response, mock_generate_token):
        mock_generate_token.return_value = ClientSecretMockResponse
        mocked_return_value = {
            "success": True,
            "data": [
                {
                    "TenantId": "e00daaf8-d6a4-4410-b50b-f5ef61c9cb45",
                    "TimeGenerated": "2022-07-03 09:12:07.122000+00:00",
                    "DisplayName": "AlertLog",
                    "AlertName": "AlertLog",
                    "AlertSeverity": "Medium",
                    "Description": "",
                    "ProviderName": "ASI Scheduled Alerts",
                    "VendorName": "Microsoft",
                    "VendorOriginalId": "d38cf0b5-84bf-486d-8de3-26cc0a561be7",
                    "SystemAlertId": "6dfa10b7-7523-ecb0-646d-28ccf9c06772",
                    "ResourceId": "",
                    "SourceComputerId": "",
                    "AlertType": "e00daaf8-d6a4-4410-b50b-f5ef61c9cb45_9c4be437-b74c-440c-aa09-764367744a23",
                    "ConfidenceLevel": "",
                    "ConfidenceScore": "None",
                    "IsIncident": "False",
                    "StartTime": "2022-07-03 08:33:37.792000+00:00",
                    "EndTime": "2022-07-03 08:33:37.792000+00:00",
                    "ProcessingEndTime": "2022-07-03 09:12:06.758000+00:00",
                    "RemediationSteps": "",
                    "ExtendedProperties": "{\"Query Period\":\"00:05:00\",\"Trigger Operator\":\"GreaterThan\","
                                          "\"Trigger Threshold\":\"0\",\"Correlation "
                                          "Id\":\"e00daaf8-d6a4-4410-b50b-f5ef61c9cb45_9c4be437-b74c-440c-aa09"
                                          "-764367744a23_637924344629201027\",\"Search Query Results Overall "
                                          "Count\":\"1\",\"Data Sources\":\"[\\\"loganaly\\\"]\",\"Query\":\"// might "
                                          "contain sensitive data\\nlet alertedEvent = datatable(compressedRec: "
                                          "string)\\n[",
                    "Entities": "",
                    "SourceSystem": "Detection",
                    "WorkspaceSubscriptionId": "dc26ff57-0597-4cc8-8092-aa5b929f8f39",
                    "WorkspaceResourceGroup": "newresource",
                    "ExtendedLinks": "",
                    "ProductName": "Azure Sentinel",
                    "ProductComponentName": "Scheduled Alerts",
                    "AlertLink": "",
                    "Status": "New",
                    "CompromisedEntity": "",
                    "Tactics": "ResourceDevelopment",
                    "Techniques": "",
                    "Type": "SecurityAlert"
                }
            ]
        }
        mock_results_response.return_value = mocked_return_value
        offset = 0
        length = 1
        search_id = "SecurityAlert | where AlertName == 'AlertLog' | limit {len}".format(len=length)
        entry_point = EntryPoint(self.connection(), self.config())
        results_response = run_in_thread(entry_point.create_results_connection, search_id, offset, length)

        assert results_response is not None
        assert results_response['success']
        assert 'data' in results_response
        assert results_response['data'] is not None

    @patch(
        'stix_shifter_modules.azure_log_analytics.stix_transmission.connector.Connector.create_results_connection')
    def test_results_all_response_empty(self, mock_results_response, mock_generate_token):
        mock_generate_token.return_value = ClientSecretMockResponse
        mocked_return_value = {
            "success": True,
            "data": []
        }
        mock_results_response.return_value = mocked_return_value
        offset = 0
        length = 1
        search_id = "SecurityAlert | where AlertName == 'AlertLog' | limit {len}".format(len=length)
        entry_point = EntryPoint(self.connection(), self.config())
        results_response = run_in_thread(entry_point.create_results_connection, search_id, offset, length)

        assert 'success' in results_response
        assert results_response['success'] is True
        assert 'data' in results_response
        assert len(results_response['data']) == 0

    @patch('stix_shifter_modules.azure_log_analytics.stix_transmission.api_client.APIClient.run_search')
    def test_results_response_exception(self, mock_results_response, mock_generate_token):
        mock_generate_token.return_value = ClientSecretMockResponse
        mock_results_response.return_value = {}

        query = "'SecurityEvent | where InvalidField == 'test'"
        offset = 0
        length = 1
        transmission = stix_transmission.StixTransmission('azure_log_analytics', self.connection(), self.config())
        results_response = transmission.results(query, offset, length)

        assert results_response['success'] is False
        assert results_response['code'] == "unknown"

    @patch('stix_shifter_modules.azure_log_analytics.stix_transmission.api_client.APIClient.run_search')
    def test_results_response_exception_with_timestamp(self, mock_results_response, mock_generate_token):
        mock_generate_token.return_value = ClientSecretMockResponse
        mock_results_response.return_value = {}

        query = "SecurityEvent | where InvalidField == 'test' ) and TimeGenerated between (datetime(" \
                "2023-03-01T16:43:26.000Z) .. datetime(2023-05-15T16:43:26.003Z)) "
        offset = 0
        length = 1
        transmission = stix_transmission.StixTransmission('azure_log_analytics', self.connection(), self.config())
        results_response = transmission.results(query, offset, length)

        assert results_response['success'] is False
        assert results_response['code'] == "unknown"

    @patch('stix_shifter_modules.azure_log_analytics.stix_transmission.api_client.APIClient.run_search')
    def test_results_response_auth_exception(self, mock_results_response, mock_generate_token):
        mock_generate_token.return_value = ClientSecretMockResponse
        mock_results_response.side_effect = ClientAuthenticationError()
        transmission = stix_transmission.StixTransmission('azure_log_analytics', self.connection(), self.config())
        results_response = transmission.results("", 0, 1)
        assert results_response['success'] is False
        assert results_response['error'] == "azure_log_analytics connector error => Invalid Authentication"
        assert results_response['code'] == "authentication_fail"

    @patch('stix_shifter_modules.azure_log_analytics.stix_transmission.api_client.APIClient.run_search')
    def test_results_response_host_exception(self, mock_results_response, mock_generate_token):
        mock_generate_token.return_value = ClientSecretMockResponse
        mock_results_response.side_effect = ClientAuthenticationError('invalid_resource')
        transmission = stix_transmission.StixTransmission('azure_log_analytics', self.connection(), self.config())
        results_response = transmission.results("", 0, 1)
        assert results_response['success'] is False
        assert results_response['error'] == "azure_log_analytics connector error => Invalid Host/Port"
        assert results_response['code'] == "service_unavailable"

    @patch('stix_shifter_modules.azure_log_analytics.stix_transmission.api_client.APIClient.run_search')
    def test_results_response_invalid_tenant(self, mock_results_response, mock_generate_token):
        mock_generate_token.return_value = ClientSecretMockResponse
        mock_results_response.side_effect = ValueError('Invalid tenant')
        transmission = stix_transmission.StixTransmission('azure_log_analytics', self.connection(), self.config())
        results_response = transmission.results("", 0, 1)
        assert results_response['success'] is False
        assert results_response['error'] == "azure_log_analytics connector error => Invalid Parameter: tenant"
        assert results_response['code'] == "invalid_parameter"

    @patch('stix_shifter_modules.azure_log_analytics.stix_transmission.api_client.APIClient.run_search')
    def test_results_response_timeout(self, mock_results_response, mock_generate_token):
        mock_generate_token.return_value = ClientSecretMockResponse
        mock_results_response.side_effect = TimeoutError()
        transmission = stix_transmission.StixTransmission('azure_log_analytics', self.connection(), self.config())
        results_response = transmission.results("", 0, 1)
        assert results_response['success'] is False
        assert results_response['error'] == "azure_log_analytics connector error => TimeoutError "
        assert results_response['code'] == "service_unavailable"

    @patch('stix_shifter_modules.azure_log_analytics.stix_transmission.api_client.APIClient.run_search')
    def test_results_response_invalid_host(self, mock_results_response, mock_generate_token):
        mock_generate_token.return_value = ClientSecretMockResponse
        mock_results_response.side_effect = HttpResponseError()
        transmission = stix_transmission.StixTransmission('azure_log_analytics', self.connection(), self.config())
        results_response = transmission.results("", 0, 1)
        assert results_response['success'] is False
        assert results_response['error'] == "azure_log_analytics connector error => Invalid Host/Port"
        assert results_response['code'] == "service_unavailable"

    @patch('stix_shifter_modules.azure_log_analytics.stix_transmission.api_client.APIClient.run_search')
    def test_results_response_invalid_workspaceid(self, mock_results_response, mock_generate_token):
        mock_generate_token.return_value = ClientSecretMockResponse
        mock_res = HttpResponseError()
        mock_res.error = ODataV4Format({"code": "PathNotFoundError"})
        mock_results_response.side_effect = mock_res
        transmission = stix_transmission.StixTransmission('azure_log_analytics', self.connection(), self.config())
        results_response = transmission.results("", 0, 1)
        assert results_response['success'] is False
        assert results_response['error'] == "azure_log_analytics connector error => Invalid Parameter: workspaceId"
        assert results_response['code'] == "invalid_parameter"

    @patch('stix_shifter_modules.azure_log_analytics.stix_transmission.api_client.APIClient.run_search')
    def test_results_response_invalid_query(self, mock_results_response, mock_generate_token):
        mock_generate_token.return_value = ClientSecretMockResponse
        mock_res = HttpResponseError()
        mock_res.error = ODataV4Format({"code": "SyntaxError"})
        mock_results_response.side_effect = mock_res
        transmission = stix_transmission.StixTransmission('azure_log_analytics', self.connection(), self.config())
        results_response = transmission.results("", 0, 1)
        assert results_response['success'] is False
        assert results_response['error'] == "azure_log_analytics connector error => Invalid Query"
        assert results_response['code'] == "invalid_query"

    def test_format_responses(self, mock_generate_token):
        mock_generate_token.return_value = ClientSecretMockResponse
        data = [
            {
                'TenantId': 'f5e9aaeb-3c3c-4045-9889-41e1a8e13cf3',
                'TimeGenerated': '2023-03-18 23:52:09.956735+00:00',
                'IncidentName': '7f788595-0fcf-4cb2-a669-07a4b5e8de99',
                'Title': 'Traffic detected from IP addresses recommended for blocking',
                'Description': "Defender for Cloud detected inbound traffic from IP addresses that are recommended to "
                               "be blocked. This typically occurs when this IP address doesn't communicate regularly "
                               "with this resource.\r\nAlternatively, the IP address has been flagged as malicious by "
                               "Microsoft's threat intelligence sources.",
                'Severity': 'Low',
                'Status': 'New',
                'Classification': '',
                'ClassificationComment': '',
                'ClassificationReason': '',
                'Owner': '{"objectId":null,"email":null,"assignedTo":null,"userPrincipalName":null}',
                'ProviderName': 'Azure Sentinel',
                'ProviderIncidentId': '15216',
                'FirstActivityTime': '2023-03-17 00:00:00+00:00',
                'LastActivityTime': '2023-03-17 00:00:00+00:00',
                'FirstModifiedTime': 'None',
                'LastModifiedTime': '2023-03-18 23:52:09.956735+00:00',
                'CreatedTime': '2023-03-18 23:52:09.956735+00:00',
                'ClosedTime': 'None',
                'IncidentNumber': '15216',
                'RelatedAnalyticRuleIds': '["5dd7161f-f0dd-429f-931d-793922aa91a1"]',
                'AlertIds': '["41f7c150-9159-5412-8f48-ad360032db4b"]',
                'BookmarkIds': '[]',
                'Comments': '[]',
                'Tasks': '[]',
                'Labels': '[]',
                'IncidentUrl': 'https://portal.azure.com/#asset/Microsoft_Azure_Security_Insights/Incident'
                               '/subscriptions/083de1fb-cd2d-4b7c-895a-2b5af1d091e8/resourceGroups/eastus/providers'
                               '/Microsoft.OperationalInsights/workspaces/sentinelwseastus/providers/Microsoft'
                               '.SecurityInsights/Incidents/7f788595-0fcf-4cb2-a669-07a4b5e8de99',
                'AdditionalData': '{"alertsCount":1,"bookmarksCount":0,"commentsCount":0,"alertProductNames":["Azure '
                                  'Security Center"],"tactics":["PreAttack"],"techniques":[]}',
                'ModifiedBy': 'Incident created from alert',
                'SourceSystem': 'Azure',
                'Type': 'SecurityIncident',
                'rn': '1'
            },
            {
                'TenantId': '81a662b5-8541-481b-977d-5d956616ac5e',
                'TimeGenerated': '2023-03-28T07:44:06.0207991Z',
                'SourceSystem': 'OpsManager',
                'Account': 'NT AUTHORITY\\SYSTEM',
                'AccountType': 'User',
                'Computer': 'am-temp908cc196',
                'EventSourceName': 'Microsoft-Windows-AppLocker',
                'Channel': 'Microsoft-Windows-AppLocker/EXE and DLL',
                'Task': '0',
                'Level': '4',
                'EventData': '<UserData xmlns="http://schemas.microsoft.com/win/2004/08/events/event">\r\n  '
                             '<RuleAndFileData '
                             'xmlns="http://schemas.microsoft.com/schemas/event/Microsoft.Windows/1.0.0.0">\r\n    '
                             '<PolicyNameLength>3</PolicyNameLength>\r\n    <PolicyName>EXE</PolicyName>\r\n    '
                             '<RuleId>{E52B1C16-422A-405A-844C-6EC4393D2D2B}</RuleId>\r\n    '
                             '<RuleNameLength>24</RuleNameLength>\r\n    <RuleName>(Default Rule) All '
                             'Exe\'s</RuleName>\r\n    <RuleSddlLength>48</RuleSddlLength>\r\n    <RuleSddl>D:('
                             'XA;;FX;;;S-1-1-0;(APPID://PATH Contains "*"))</RuleSddl>\r\n    '
                             '<TargetUser>S-1-5-18</TargetUser>\r\n    <TargetProcessId>1196</TargetProcessId>\r\n    '
                             '<FilePathLength>22</FilePathLength>\r\n    '
                             '<FilePath>%SYSTEM32%\\CSCRIPT.EXE</FilePath>\r\n    '
                             '<FileHashLength>32</FileHashLength>\r\n    '
                             '<FileHash>B33565E05C3D1B7AD77DF1803DDFB455EF5D30E2D6A52DF5828754DE8A0BC365</FileHash>\r'
                             '\n    <FqbnLength>116</FqbnLength>\r\n    <Fqbn>O=MICROSOFT CORPORATION, L=REDMOND, '
                             'S=WASHINGTON, C=US\\MICROSOFT ® WINDOWS SCRIPT '
                             'HOST\\CSCRIPT.EXE\\5.812.10240.16384</Fqbn>\r\n    '
                             '<TargetLogonId>0x3e7</TargetLogonId>\r\n  </RuleAndFileData>\r\n</UserData>',
                'EventID': '8002',
                'Activity': '8002 - A process was allowed to run.',
                'SourceComputerId': 'a61d1b11-50aa-416d-b297-830b91a64913',
                'EventOriginId': '77271620-a0ba-400a-8c13-de864ded672d',
                'MG': '00000000-0000-0000-0000-000000000001',
                'TimeCollected': '2023-03-28T07:44:37.7036876Z',
                'ManagementGroupName': 'AOI-81a662b5-8541-481b-977d-5d956616ac5e',
                'AccessList': '',
                'AccessMask': '',
                'AccessReason': '',
                'AccountDomain': '',
                'AccountExpires': '',
                'AccountName': '',
                'AccountSessionIdentifier': '',
                'AdditionalInfo': '',
                'AdditionalInfo2': '',
                'AllowedToDelegateTo': '',
                'Attributes': '',
                'AuditPolicyChanges': '',
                'AuditsDiscarded': 'None',
                'AuthenticationLevel': 'None',
                'AuthenticationPackageName': '',
                'AuthenticationProvider': '',
                'AuthenticationServer': '',
                'AuthenticationService': 'None',
                'AuthenticationType': '',
                'CACertificateHash': '',
                'CalledStationID': '',
                'CallerProcessId': '',
                'CallerProcessName': '',
                'CallingStationID': '',
                'CAPublicKeyHash': '',
                'CategoryId': '',
                'CertificateDatabaseHash': '',
                'ClassId': '',
                'ClassName': '',
                'ClientAddress': '',
                'ClientIPAddress': '',
                'ClientName': '',
                'CommandLine': '',
                'CompatibleIds': '',
                'DCDNSName': '',
                'DeviceDescription': '',
                'DeviceId': '',
                'DisplayName': '',
                'Disposition': '',
                'DomainBehaviorVersion': '',
                'DomainName': '',
                'DomainPolicyChanged': '',
                'DomainSid': '',
                'EAPType': '',
                'ElevatedToken': '',
                'ErrorCode': 'None',
                'ExtendedQuarantineState': '',
                'FailureReason': '',
                'FileHash': 'B33565E05C3D1B7AD77DF1803DDFB455EF5D30E2D6A52DF5828754DE8A0BC365',
                'FilePath': '%SYSTEM32%\\CSCRIPT.EXE',
                'FilePathNoUser': '',
                'Filter': '',
                'ForceLogoff': '',
                'Fqbn': 'O=MICROSOFT CORPORATION, L=REDMOND, S=WASHINGTON, C=US\\MICROSOFT ® WINDOWS SCRIPT '
                        'HOST\\CSCRIPT.EXE\\5.812.10240.16384',
                'FullyQualifiedSubjectMachineName': '',
                'FullyQualifiedSubjectUserName': '',
                'GroupMembership': '',
                'HandleId': '',
                'HardwareIds': '',
                'HomeDirectory': '',
                'HomePath': '',
                'ImpersonationLevel': '',
                'InterfaceUuid': '',
                'IpAddress': '',
                'IpPort': '',
                'KeyLength': 'None',
                'LmPackageName': '',
                'LocationInformation': '',
                'LockoutDuration': '',
                'LockoutObservationWindow': '',
                'LockoutThreshold': '',
                'LoggingResult': '',
                'LogonGuid': '',
                'LogonHours': '',
                'LogonID': '',
                'LogonProcessName': '',
                'LogonType': 'None',
                'LogonTypeName': '',
                'MachineAccountQuota': '',
                'MachineInventory': '',
                'MachineLogon': '',
                'MandatoryLabel': '',
                'MaxPasswordAge': '',
                'MemberName': '',
                'MemberSid': '',
                'MinPasswordAge': '',
                'MinPasswordLength': '',
                'MixedDomainMode': '',
                'NASIdentifier': '',
                'NASIPv4Address': '',
                'NASIPv6Address': '',
                'NASPort': '',
                'NASPortType': '',
                'NetworkPolicyName': '',
                'NewDate': '',
                'NewMaxUsers': '',
                'NewProcessId': '',
                'NewProcessName': '',
                'NewRemark': '',
                'NewShareFlags': '',
                'NewTime': '',
                'NewUacValue': '',
                'NewValue': '',
                'NewValueType': '',
                'ObjectName': '',
                'ObjectServer': '',
                'ObjectType': '',
                'ObjectValueName': '',
                'OemInformation': '',
                'OldMaxUsers': '',
                'OldRemark': '',
                'OldShareFlags': '',
                'OldUacValue': '',
                'OldValue': '',
                'OldValueType': '',
                'OperationType': '',
                'PackageName': '',
                'ParentProcessName': '',
                'PasswordHistoryLength': '',
                'PasswordLastSet': '',
                'PasswordProperties': '',
                'PreviousDate': '',
                'PreviousTime': '',
                'PrimaryGroupId': '',
                'PrivateKeyUsageCount': '',
                'PrivilegeList': '',
                'Process': 'CSCRIPT.EXE',
                'ProcessId': '',
                'ProcessName': '',
                'Properties': '',
                'ProfilePath': '',
                'ProtocolSequence': '',
                'ProxyPolicyName': '',
                'QuarantineHelpURL': '',
                'QuarantineSessionID': '',
                'QuarantineSessionIdentifier': '',
                'QuarantineState': '',
                'QuarantineSystemHealthResult': '',
                'RelativeTargetName': '',
                'RemoteIpAddress': '',
                'RemotePort': '',
                'Requester': '',
                'RequestId': '',
                'RestrictedAdminMode': '',
                'RowsDeleted': '',
                'SamAccountName': '',
                'ScriptPath': '',
                'SecurityDescriptor': '',
                'ServiceAccount': '',
                'ServiceFileName': '',
                'ServiceName': '',
                'ServiceStartType': 'None',
                'ServiceType': '',
                'SessionName': '',
                'ShareLocalPath': '',
                'ShareName': '',
                'SidHistory': '',
                'Status': '',
                'SubjectAccount': '',
                'SubcategoryGuid': '',
                'SubcategoryId': '',
                'Subject': '',
                'SubjectDomainName': '',
                'SubjectKeyIdentifier': '',
                'SubjectLogonId': '',
                'SubjectMachineName': '',
                'SubjectMachineSID': '',
                'SubjectUserName': '',
                'SubjectUserSid': '',
                'SubStatus': '',
                'TableId': '',
                'TargetAccount': '',
                'TargetDomainName': '',
                'TargetInfo': '',
                'TargetLinkedLogonId': '',
                'TargetLogonGuid': '',
                'TargetLogonId': '',
                'TargetOutboundDomainName': '',
                'TargetOutboundUserName': '',
                'TargetServerName': '',
                'TargetSid': '',
                'TargetUser': 'S-1-5-18',
                'TargetUserName': '',
                'TargetUserSid': '',
                'TemplateContent': '',
                'TemplateDSObjectFQDN': '',
                'TemplateInternalName': '',
                'TemplateOID': '',
                'TemplateSchemaVersion': '',
                'TemplateVersion': '',
                'TokenElevationType': '',
                'TransmittedServices': '',
                'UserAccountControl': '',
                'UserParameters': '',
                'UserPrincipalName': '',
                'UserWorkstations': '',
                'VirtualAccount': '',
                'VendorIds': '',
                'Workstation': '',
                'WorkstationName': '',
                'PartitionKey': '',
                'RowKey': '',
                'StorageAccount': '',
                'AzureDeploymentID': '',
                'AzureTableName': '',
                'Type': 'SecurityEvent',
                '_ResourceId': '/subscriptions/ebb79bc0-aa86-44a7-8111-cabbe0c43993/resourcegroups/ch1-liftnshiftrg'
                               '/providers/microsoft.compute/virtualmachines/am-temp908cc196 '
            },
            {
                'TenantId': 'f5e9aaeb-3c3c-4045-9889-41e1a8e13cf3',
                'TimeGenerated': '2023-03-22 07:27:56.188461+00:00',
                'DisplayName': '[SAMPLE ALERT] Digital currency mining related behavior detected',
                'AlertName': '[SAMPLE ALERT] Digital currency mining related behavior detected',
                'AlertSeverity': 'High',
                'Description': 'THIS IS A SAMPLE ALERT: Analysis of host data on Sample-VM detected the execution of '
                               'a process or command normally associated with digital currency mining.',
                'ProviderName': 'Azure Security Center',
                'VendorName': 'Microsoft',
                'VendorOriginalId': '2517228307705103557_15add4de-0b29-4827-a0e1-b5ff4d8d4802',
                'SystemAlertId': 'fac479ec-3566-dce6-0ae3-a90c4af39175',
                'ResourceId': '/SUBSCRIPTIONS/083de1fb-cd2d-4b7c-895a-2b5af1d091e8/RESOURCEGROUPS/Sample-RG/providers'
                              '/Microsoft.Compute/virtualMachines/Sample-VM',
                'SourceComputerId': '',
                'AlertType': 'SIMULATED_VM_DigitalCurrencyMining',
                'ConfidenceLevel': '',
                'ConfidenceScore': 'None',
                'IsIncident': 'False',
                'StartTime': '2023-03-22 07:27:09.489644+00:00',
                'EndTime': '2023-03-22 07:27:09.489644+00:00',
                'ProcessingEndTime': '2023-03-22 07:27:51.489644+00:00',
                'RemediationSteps': '["Review with Sample-account the suspicious command process and command line to '
                                    'confirm that this is legitimate activity that you expect to see on Sample-VM. If '
                                    'not, escalate the alert to the information security team."]',
                'ExtendedProperties': '{"resourceType":"Virtual Machine","User Name":"Sample-account","Compromised '
                                      'Host":"Sample-VM","Suspicious Command Line":"\\\\sample.exe -t 4","Suspicious '
                                      'Process Id":"0x1640","Suspicious Process":"sample.exe","Account Session '
                                      'Id":"0x427d8dd9","ProcessedBySentinel":"True","Alert generation status":"Full '
                                      'alert created"}',
                'Entities': '[{"$id":"2","DnsDomain":"","NTDomain":"","HostName":"Sample-VM",'
                            '"NetBiosName":"Sample-VM",'
                            '"AzureID":"/SUBSCRIPTIONS/083de1fb-cd2d-4b7c-895a-2b5af1d091e8/RESOURCEGROUPS/Sample-RG'
                            '/providers/Microsoft.Compute/virtualMachines/Sample-VM",'
                            '"OMSAgentID":"00000000-0000-0000-0000-000000000001","OSFamily":"Windows",'
                            '"OSVersion":"Windows","IsDomainJoined":false,"Type":"host"},{"$id":"3",'
                            '"ProcessId":"0x1020","CommandLine":"","Host":{"$ref":"2"},"Type":"process"},{"$id":"4",'
                            '"Name":"Sample-account","NTDomain":"Sample-VM","Host":{"$ref":"2"},'
                            '"Sid":"S-1-5-21-3061399664-1673012318-3185014992-20022","IsDomainJoined":false,'
                            '"Type":"account","LogonId":"0x427d8dd9"},{"$id":"5","Directory":"c:\\\\temp",'
                            '"Name":"sample.exe","Type":"file"},{"$id":"6","ProcessId":"0x1640",'
                            '"CommandLine":".\\\\sample.exe -t 4","ElevationToken":"Default",'
                            '"CreationTimeUtc":"2023-03-22T07:27:09.4896442Z","ImageFile":{"$ref":"5"},"Account":{'
                            '"$ref":"4"},"ParentProcess":{"$ref":"3"},"Host":{"$ref":"2"},"Type":"process"},'
                            '{"$id":"7","SessionId":"0x427d8dd9","StartTimeUtc":"2023-03-22T07:27:09.4896442Z",'
                            '"EndTimeUtc":"2023-03-22T07:27:09.4896442Z","Type":"host-logon-session",'
                            '"Host":{"$ref":"2"},"Account":{"$ref":"4"}}, {"$id":"8","Algorithm":"SHA256",'
                            '"Value":"Sample-SHA","Type":"filehash"}, {"$id":"9",'
                            '"Directory":"https://Sample-Storage.blob.core.windows.net/Sample","Name":"Sample-Name",'
                            '"FileHashes":[{"$ref":"8"}],"Type":"file"}]',
                'SourceSystem': 'Detection',
                'WorkspaceSubscriptionId': '00000000-0000-0000-0000-000000000001',
                'WorkspaceResourceGroup': 'defaultresourcegroup-wus',
                'ExtendedLinks': '',
                'ProductName': 'Azure Security Center',
                'ProductComponentName': 'VirtualMachines',
                'AlertLink': 'https://portal.azure.com/#blade/Microsoft_Azure_Security_AzureDefenderForData'
                             '/AlertBlade/alertId/2517228307705103557_15add4de-0b29-4827-a0e1-b5ff4d8d4802'
                             '/subscriptionId/083de1fb-cd2d-4b7c-895a-2b5af1d091e8/resourceGroup/Sample-RG'
                             '/referencedFrom/alertDeepLink/location/centralus',
                'Status': 'New',
                'CompromisedEntity': 'Sample-VM',
                'Tactics': 'Execution',
                'Techniques': '',
                'Type': 'SecurityAlert',
                'rn': '1'
            },
            {
                 'TenantId': 'f5e9aaeb-3c3c-4045-9889-41e1a8e13c11', 'TimeGenerated': '2023-04-18 16:20:01.053681+00:00',
                 'DisplayName': '[Test Alert] Suspicious Powershell commandline',
                 'AlertName': '[Test Alert] Suspicious Powershell commandline', 'AlertSeverity': 'Informational',
                 'Description': ' This is a test alert \nA suspicious Powershell commandline was found on the machine.',
                 'ProviderName': 'MDATP', 'VendorName': 'Microsoft',
                 'VendorOriginalId': '3cb12a2f-33e5-42ea-9238-be9ffbc212e2_1',
                 'SystemAlertId': '6092461b-5418-9bae-c7c8-dd1e29b8f83a', 'ResourceId': '', 'SourceComputerId': '',
                 'AlertType': 'WindowsDefenderAtp', 'ConfidenceLevel': '', 'ConfidenceScore': 'None', 'IsIncident': '',
                 'StartTime': '2023-04-18 13:10:09.091320+00:00', 'EndTime': '2023-04-18 16:08:28.583668+00:00',
                 'ProcessingEndTime': '2023-04-18 16:20:00.910579+00:00',
                 'RemediationSteps': '["1. Make sure the machine is completely updated and all your software has the '
                                     'latest patch.","2. Contact your incident response team. NOTE: If you don’t have '
                                     'an incident response team, contact Microsoft Support for architectural '
                                     'remediation and forensic.","3. Install and run Microsoft’s Malicious Software '
                                     'Removal Tool (see '
                                     'https://www.microsoft.com/en-us/download/malicious-software-removal-tool'
                                     '-details.aspx).","4. Run Microsoft’s Autoruns utility and try to identify '
                                     'unknown applications that are configured to run at login (see '
                                     'https://technet.microsoft.com/en-us/sysinternals/bb963902.aspx).",'
                                     '"5. Run Process Explorer and try to identify unknown running processes (see '
                                     'https://technet.microsoft.com/en-us/sysinternals/bb896653.aspx)."]',
                 'ExtendedProperties': '',
                 'Entities': '[{"$id":"2","Name":"defenderadm","NTDomain":"alert-windows",'
                             '"Sid":"S-1-5-21-2421154212-3139753733-2135342675-1000","IsDomainJoined":true,'
                             '"Asset":true,"Type":"account"},{"$id":"3","ProcessId":"7548",'
                             '"CommandLine":"\\"cmd.exe\\" ","ElevationToken":"Full",'
                             '"CreationTimeUtc":"2023-04-18T13:09:24.245931Z","ImageFile":{"$id":"4",'
                             '"Directory":"C:\\\\Windows\\\\System32","Name":"cmd.exe","FileHashes":[{"$id":"5",'
                             '"Algorithm":"SHA1","Value":"ded8fd7f36417f66eb6ada10e0c0d7c0022986e9",'
                             '"Type":"filehash"},{"$id":"6","Algorithm":"MD5",'
                             '"Value":"911d039e71583a07320b32bde22f8e22","Type":"filehash"},{"$id":"7",'
                             '"Algorithm":"SHA256",'
                             '"Value":"bc866cfcdda37e24dc2634dc282c7a0e6f55209da17a8fa105b07414c0e7c527",'
                             '"Type":"filehash"}],"CreatedTimeUtc":"2021-01-09T03:02:17.7091389Z","Type":"file"},'
                             '"ParentProcess":{"$id":"8","ProcessId":"2056",'
                             '"CreationTimeUtc":"2023-04-18T13:08:41.4953968Z",'
                             '"CreatedTimeUtc":"2023-04-18T13:08:41.4953968Z","Type":"process"},'
                             '"CreatedTimeUtc":"2023-04-18T13:09:24.245931Z","Type":"process"},{"$ref":"8"},'
                             '{"$ref":"4"},{"$ref":"5"},{"$ref":"6"},{"$ref":"7"},{"$id":"9","ProcessId":"7908",'
                             '"CommandLine":"powershell.exe  -NoExit -ExecutionPolicy Bypass -WindowStyle Hidden '
                             '$ErrorActionPreference = \'silentlycontinue\';(New-Object '
                             'System.Net.WebClient).DownloadFile(\'http://127.0.0.1/1.exe\', '
                             '\'C:\\\\\\\\test-MDATP-test\\\\\\\\invoice.exe\');Start-Process '
                             '\'C:\\\\\\\\test-MDATP-test\\\\\\\\invoice.exe\'","ElevationToken":"Full",'
                             '"CreationTimeUtc":"2023-04-18T13:10:09.0734545Z","ImageFile":{"$id":"10",'
                             '"Directory":"C:\\\\Windows\\\\System32\\\\WindowsPowerShell\\\\v1.0",'
                             '"Name":"powershell.exe","FileHashes":[{"$id":"11","Algorithm":"SHA1",'
                             '"Value":"6cbce4a295c163791b60fc23d285e6d84f28ee4c","Type":"filehash"},{"$id":"12",'
                             '"Algorithm":"MD5","Value":"7353f60b1739074eb17c5f4dddefe239","Type":"filehash"},'
                             '{"$id":"13","Algorithm":"SHA256",'
                             '"Value":"de96a6e69944335375dc1ac238336066889d9ffc7d73628ef4fe1b1b160ab32c",'
                             '"Type":"filehash"}],"CreatedTimeUtc":"2018-09-15T07:14:14.4547673Z","Type":"file"},'
                             '"ParentProcess":{"$ref":"3"},"CreatedTimeUtc":"2023-04-18T13:10:09.0734545Z",'
                             '"Type":"process"},{"$ref":"10"},{"$ref":"11"},{"$ref":"12"},{"$ref":"13"},{"$id":"14",'
                             '"ProcessId":"7532","CommandLine":"\\"cmd.exe\\" ","ElevationToken":"Full",'
                             '"CreationTimeUtc":"2023-04-18T16:08:14.1738266Z","ImageFile":{"$ref":"4"},'
                             '"ParentProcess":{"$ref":"8"},"CreatedTimeUtc":"2023-04-18T16:08:14.1738266Z",'
                             '"Type":"process"},{"$id":"15","ProcessId":"5908","CommandLine":"powershell.exe  -NoExit '
                             '-ExecutionPolicy Bypass -WindowStyle Hidden $ErrorActionPreference = '
                             '\'silentlycontinue\';(New-Object System.Net.WebClient).DownloadFile('
                             '\'http://127.0.0.1/1.exe\', '
                             '\'C:\\\\\\\\test-MDATP-test\\\\\\\\invoice.exe\');Start-Process '
                             '\'C:\\\\\\\\test-MDATP-test\\\\\\\\invoice.exe\'","ElevationToken":"Full",'
                             '"CreationTimeUtc":"2023-04-18T16:08:28.5697525Z","ImageFile":{"$ref":"10"},'
                             '"ParentProcess":{"$ref":"14"},"CreatedTimeUtc":"2023-04-18T16:08:28.5697525Z",'
                             '"Type":"process"},{"$id":"16","HostName":"alert-windows","OSFamily":"Windows",'
                             '"OSVersion":"1809","Type":"host",'
                             '"MdatpDeviceId":"4f22ab5dc4be96566ee3c9adb3b77280dc08bfdb","FQDN":"alert-windows",'
                             '"RiskScore":"Medium","HealthStatus":"Active","LastSeen":"2023-04-18T13:01:26.0294235",'
                             '"LastExternalIpAddress":"111.11.111.111","LastIpAddress":"11.1.1.1",'
                             '"AvStatus":"NotSupported","OnboardingStatus":"Onboarded","LoggedOnUsers":[]}]',
                 'SourceSystem': 'Detection', 'WorkspaceSubscriptionId': '', 'WorkspaceResourceGroup': '',
                 'ExtendedLinks': '', 'ProductName': 'Microsoft Defender Advanced Threat Protection',
                 'ProductComponentName': '',
                 'AlertLink': 'https://security.microsoft.com/alerts/da3cb12a2f-33e5-42ea-9238-be9ffbc212e2_1',
                 'Status': 'New', 'CompromisedEntity': 'alert-windows', 'Tactics': 'Execution', 'Techniques': '',
                 'Type': 'SecurityAlert', 'rn': '1'
            }
        ]
        copied_data = copy.deepcopy(data)
        connector = Connector(self.connection(), self.config())
        processed_response = connector.format_response(data)
        assert processed_response != copied_data
