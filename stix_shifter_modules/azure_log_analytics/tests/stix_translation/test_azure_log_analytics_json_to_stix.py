import unittest
from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_modules.azure_log_analytics.entry_point import EntryPoint
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers

MODULE = "azure_log_analytics"
options = {"api": "Log Analytics"}
entry_point = EntryPoint(options=options)
map_data = entry_point.get_results_translator().map_data
data_source = {
    "type": "identity",
    "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
    "name": "azure_log_analytics",
    "identity_class": "events"
}

# security alert sample
DATA1 = {
    'TenantId': 'f5e9aaeb-3c3c-4045-9889-41e1a8e13cf3',
    'TimeGenerated': '2023-03-22 07:27:56.188461+00:00',
    'DisplayName': '[SAMPLE ALERT] Digital currency mining related behavior detected',
    'AlertName': '[SAMPLE ALERT] Digital currency mining related behavior detected',
    'AlertSeverity': '100',
    'Description': 'THIS IS A SAMPLE ALERT: Analysis of host data on Sample-VM detected the execution of a '
                   'process or command normally associated with digital currency mining.',
    'ProviderName': 'Azure Security Center',
    'VendorName': 'Microsoft',
    'VendorOriginalId': '2517228307705103557_15add4de-0b29-4827-a0e1-b5ff4d8d4802',
    'SystemAlertId': 'fac479ec-3566-dce6-0ae3-a90c4af39175',
    'ResourceId': '/SUBSCRIPTIONS/083de1fb-cd2d-4b7c-895a-2b5af1d091e8/RESOURCEGROUPS/Sample-RG/providers'
                  '/Microsoft.Compute/virtualMachines/Sample-VM',
    'SourceComputerId': '',
    'AlertType': 'SIMULATED_VM_DigitalCurrencyMining',
    'ConfidenceLevel': '',
    'ConfidenceScore': '1.0',
    'IsIncident': 'False',
    'StartTime': '2023-03-22 07:27:09.489644+00:00',
    'EndTime': '2023-03-22 07:27:09.489644+00:00',
    'ProcessingEndTime': '2023-03-22 07:27:51.489644+00:00',
    'RemediationSteps': 'Review with Sample-account the suspicious command process and command line to confirm '
                        'that this is legitimate activity that you expect to see on Sample-VM. If not, '
                        'escalate the alert to the information security team.',
    'ExtendedProperties': {
        'resourceType': 'Virtual Machine',
        'User Name': 'Sample-account',
        'Compromised Host': 'Sample-VM',
        'Suspicious Command Line': '\\sample.exe -t 4',
        'Suspicious Process Id': '0x1640',
        'Suspicious Process': 'sample.exe',
        'Account Session Id': '0x427d8dd9',
        'ProcessedBySentinel': 'True',
        'Alert generation status': 'Full alert created'
    },
    'Entities': {
        'host': {
            '$id': '2',
            'DnsDomain': '',
            'NTDomain': '',
            'HostName': 'Sample-VM',
            'NetBiosName': 'Sample-VM',
            'AzureID': '/SUBSCRIPTIONS/083de1fb-cd2d-4b7c-895a-2b5af1d091e8/RESOURCEGROUPS/Sample-RG/providers'
                       '/Microsoft.Compute/virtualMachines/Sample-VM',
            'OMSAgentID': '00000000-0000-0000-0000-000000000001',
            'OSFamily': 'Windows',
            'OSVersion': 'Windows',
            'IsDomainJoined': False,
            'Type': 'host',
            'AccountType': 'windows-local'
        },
        'process': [{
            '$id': '6',
            'ProcessId': '0x1640',
            'CommandLine': '.\\sample.exe -t 4',
            'ElevationToken': 'Default',
            'CreationTimeUtc': '2023-03-22T07:27:09.4896442Z',
            'ImageFile': {
                '$id': '5',
                'Directory': 'c:\\temp',
                'Name': 'sample.exe',
                'Type': 'file'
            },
            'Account': {
                '$id': '4',
                'Name': 'Sample-account',
                'NTDomain': 'Sample-VM',
                'Host': {
                    '$id': '2',
                    'DnsDomain': '',
                    'NTDomain': '',
                    'HostName': 'Sample-VM',
                    'NetBiosName': 'Sample-VM',
                    'AzureID': '/SUBSCRIPTIONS/083de1fb-cd2d-4b7c-895a-2b5af1d091e8/RESOURCEGROUPS/Sample-RG'
                               '/providers/Microsoft.Compute/virtualMachines/Sample-VM',
                    'OMSAgentID': '00000000-0000-0000-0000-000000000001',
                    'OSFamily': 'Windows',
                    'OSVersion': 'Windows',
                    'IsDomainJoined': False,
                    'Type': 'host',
                    'AccountType': 'windows-local'
                },
                'Sid': 'S-1-5-21-3061399664-1673012318-3185014992-20022',
                'IsDomainJoined': False,
                'Type': 'account',
                'LogonId': '0x427d8dd9',
                'AccountType': 'windows-local'
            },
            'ParentProcess': {
                '$id': '3',
                'ProcessId': '0x1020',
                'CommandLine': '',
                'Host': {
                    '$id': '2',
                    'DnsDomain': '',
                    'NTDomain': '',
                    'HostName': 'Sample-VM',
                    'NetBiosName': 'Sample-VM',
                    'AzureID': '/SUBSCRIPTIONS/083de1fb-cd2d-4b7c-895a-2b5af1d091e8/RESOURCEGROUPS/Sample-RG'
                               '/providers/Microsoft.Compute/virtualMachines/Sample-VM',
                    'OMSAgentID': '00000000-0000-0000-0000-000000000001',
                    'OSFamily': 'Windows',
                    'OSVersion': 'Windows',
                    'IsDomainJoined': False,
                    'Type': 'host',
                    'AccountType': 'windows-local'
                },
                'Type': 'process'
            },
            'Host': {
                '$id': '2',
                'DnsDomain': '',
                'NTDomain': '',
                'HostName': 'Sample-VM',
                'NetBiosName': 'Sample-VM',
                'AzureID': '/SUBSCRIPTIONS/083de1fb-cd2d-4b7c-895a-2b5af1d091e8/RESOURCEGROUPS/Sample-RG'
                           '/providers/Microsoft.Compute/virtualMachines/Sample-VM',
                'OMSAgentID': '00000000-0000-0000-0000-000000000001',
                'OSFamily': 'Windows',
                'OSVersion': 'Windows',
                'IsDomainJoined': False,
                'Type': 'host',
                'AccountType': 'windows-local'
            },
            'Type': 'process'
        }],
        'account': {
            '$id': '4',
            'Name': 'Sample-account',
            'NTDomain': 'Sample-VM',
            'Host': {
                '$id': '2',
                'DnsDomain': '',
                'NTDomain': '',
                'HostName': 'Sample-VM',
                'NetBiosName': 'Sample-VM',
                'AzureID': '/SUBSCRIPTIONS/083de1fb-cd2d-4b7c-895a-2b5af1d091e8/RESOURCEGROUPS/Sample-RG'
                           '/providers/Microsoft.Compute/virtualMachines/Sample-VM',
                'OMSAgentID': '00000000-0000-0000-0000-000000000001',
                'OSFamily': 'Windows',
                'OSVersion': 'Windows',
                'IsDomainJoined': False,
                'Type': 'host',
                'AccountType': 'windows-local'
            },
            'Sid': 'S-1-5-21-3061399664-1673012318-3185014992-20022',
            'IsDomainJoined': False,
            'Type': 'account',
            'LogonId': '0x427d8dd9',
            'AccountType': 'windows-local'
        },
        'file': [{
            '$id': '5',
            'Directory': 'c:\\temp',
            'Name': 'sample.exe',
            'Type': 'file'
        }, {
            '$id': '9',
            'Directory': 'https://Sample-Storage.blob.core.windows.net/Sample',
            'Name': 'Sample-Name',
            'FileHashes': [{
                '$id': '8',
                'Algorithm': 'SHA256',
                'Value': 'Sample-SHA',
                'Type': 'filehash',
                'SHA256': 'Sample-SHA'
            }],
            'Type': 'file'
        }],
        'host-logon-session': {
            '$id': '7',
            'SessionId': '0x427d8dd9',
            'StartTimeUtc': '2023-03-22T07:27:09.4896442Z',
            'EndTimeUtc': '2023-03-22T07:27:09.4896442Z',
            'Type': 'host-logon-session',
            'Host': {
                '$id': '2',
                'DnsDomain': '',
                'NTDomain': '',
                'HostName': 'Sample-VM',
                'NetBiosName': 'Sample-VM',
                'AzureID': '/SUBSCRIPTIONS/083de1fb-cd2d-4b7c-895a-2b5af1d091e8/RESOURCEGROUPS/Sample-RG'
                           '/providers/Microsoft.Compute/virtualMachines/Sample-VM',
                'OMSAgentID': '00000000-0000-0000-0000-000000000001',
                'OSFamily': 'Windows',
                'OSVersion': 'Windows',
                'IsDomainJoined': False,
                'Type': 'host',
                'AccountType': 'windows-local'
            },
            'Account': {
                '$id': '4',
                'Name': 'Sample-account',
                'NTDomain': 'Sample-VM',
                'Host': {
                    '$id': '2',
                    'DnsDomain': '',
                    'NTDomain': '',
                    'HostName': 'Sample-VM',
                    'NetBiosName': 'Sample-VM',
                    'AzureID': '/SUBSCRIPTIONS/083de1fb-cd2d-4b7c-895a-2b5af1d091e8/RESOURCEGROUPS/Sample-RG'
                               '/providers/Microsoft.Compute/virtualMachines/Sample-VM',
                    'OMSAgentID': '00000000-0000-0000-0000-000000000001',
                    'OSFamily': 'Windows',
                    'OSVersion': 'Windows',
                    'IsDomainJoined': False,
                    'Type': 'host',
                    'AccountType': 'windows-local'
                },
                'Sid': 'S-1-5-21-3061399664-1673012318-3185014992-20022',
                'IsDomainJoined': False,
                'Type': 'account',
                'LogonId': '0x427d8dd9',
                'AccountType': 'windows-local'
            }
        },
        'filehash': {
            '$id': '8',
            'Algorithm': 'SHA256',
            'Value': 'Sample-SHA',
            'Type': 'filehash',
            'SHA256': 'Sample-SHA'
        }
    },
    'SourceSystem': 'Detection',
    'WorkspaceSubscriptionId': '00000000-0000-0000-0000-000000000001',
    'WorkspaceResourceGroup': 'defaultresourcegroup-wus',
    'ExtendedLinks': '',
    'ProductName': 'Azure Security Center',
    'ProductComponentName': 'VirtualMachines',
    'AlertLink': 'https://portal.azure.com/#blade/Microsoft_Azure_Security_AzureDefenderForData/AlertBlade'
                 '/alertId/2517228307705103557_15add4de-0b29-4827-a0e1-b5ff4d8d4802/subscriptionId/083de1fb-cd2d'
                 '-4b7c-895a-2b5af1d091e8/resourceGroup/Sample-RG/referencedFrom/alertDeepLink/location/centralus',
    'Status': 'New',
    'CompromisedEntity': 'Sample-VM',
    'Tactics': 'Execution',
    'Techniques': '',
    'Type': 'SecurityAlert',
    'rn': '1',
}

# security event sample
DATA2 = {
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
    'EventData': '<UserData xmlns="http://schemas.microsoft.com/win/2004/08/events/event">\r\n\xa0 '
                 '<RuleAndFileData xmlns="http://schemas.microsoft.com/schemas/event/Microsoft.Windows/1.0.0.0'
                 '">\r\n\xa0\xa0\xa0 <PolicyNameLength>3</PolicyNameLength>\r\n\xa0\xa0\xa0 '
                 '<PolicyName>EXE</PolicyName>\r\n\xa0\xa0\xa0 <RuleId>{'
                 'E52B1C16-422A-405A-844C-6EC4393D2D2B}</RuleId>\r\n\xa0\xa0\xa0 '
                 '<RuleNameLength>24</RuleNameLength>\r\n\xa0\xa0\xa0 <RuleName>(Default Rule) All '
                 'Exe\'s</RuleName>\r\n\xa0\xa0\xa0 <RuleSddlLength>48</RuleSddlLength>\r\n\xa0\xa0\xa0 '
                 '<RuleSddl>D:(XA;;FX;;;S-1-1-0;(APPID://PATH Contains "*"))</RuleSddl>\r\n\xa0\xa0\xa0 '
                 '<TargetUser>S-1-5-18</TargetUser>\r\n\xa0\xa0\xa0 '
                 '<TargetProcessId>1196</TargetProcessId>\r\n\xa0\xa0\xa0 '
                 '<FilePathLength>22</FilePathLength>\r\n\xa0\xa0\xa0 '
                 '<FilePath>%SYSTEM32%\\CSCRIPT.EXE</FilePath>\r\n\xa0\xa0\xa0 '
                 '<FileHashLength>32</FileHashLength>\r\n\xa0\xa0\xa0 '
                 '<FileHash>B33565E05C3D1B7AD77DF1803DDFB455EF5D30E2D6A52DF5828754DE8A0BC365</FileHash>\r\n\xa0'
                 '\xa0\xa0 <FqbnLength>116</FqbnLength>\r\n\xa0\xa0\xa0 <Fqbn>O=MICROSOFT CORPORATION, L=REDMOND, '
                 'S=WASHINGTON, C=US\\MICROSOFT ® WINDOWS SCRIPT '
                 'HOST\\CSCRIPT.EXE\\</Fqbn>\r\n\xa0\xa0\xa0 '
                 '<TargetLogonId>0x3e7</TargetLogonId>\r\n\xa0 </RuleAndFileData>\r\n</UserData>',
    'EventID': '8002',
    'Activity': '8002 - A process was allowed to run.',
    'SourceComputerId': 'a61d1b11-50aa-416d-b297-830b91a64913',
    'EventOriginId': '77271620-a0ba-400a-8c13-de864ded672d',
    'MG': '00000000-0000-0000-0000-000000000001',
    'TimeCollected': '2023-05-10 10:20:16.906375+00:00',
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
            'HOST\\CSCRIPT.EXE\\',
    'FullyQualifiedSubjectMachineName': '',
    'FullyQualifiedSubjectUserName': '',
    'GroupMembership': '',
    'HandleId': '',
    'HardwareIds': '',
    'HomeDirectory': '',
    'HomePath': '',
    'ImpersonationLevel': '',
    'InterfaceUuid': '',
    'IpAddress': '111.11.11.111',
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
    'ProcessName': 'test',
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
    'TargetUserName': 'test_user',
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
    '_ResourceId': '/subscriptions/ebb79bc0-aa86-44a7-8111-cabbe0c43993/resourcegroups/ch1-liftnshiftrg/providers'
                   '/microsoft.compute/virtualmachines/am-temp908cc196',
    'SHA-256': 'B33565E05C3D1B7AD77DF1803DDFB455EF5D30E2D6A52DF5828754DE8A0BC365'
}

# security incident sample
DATA3 = {
    'TenantId': 'f5e9aaeb-3c3c-4045-9889-41e1a8e13cf3',
    'TimeGenerated': '2023-03-18 23:52:09.956735+00:00',
    'IncidentName': '7f788595-0fcf-4cb2-a669-07a4b5e8de99',
    'Title': 'Traffic detected from IP addresses recommended for blocking',
    'Description': "Defender for Cloud detected inbound traffic from IP addresses that are recommended to be "
                   "blocked. This typically occurs when this IP address doesn't communicate regularly with this "
                   "resource.\r\nAlternatively, the IP address has been flagged as malicious by Microsoft's "
                   "threat intelligence sources.",
    'Severity': '50',
    'Status': 'New',
    'Classification': '',
    'ClassificationComment': '',
    'ClassificationReason': '',
    'Owner': {
        'objectId': None,
        'email': None,
        'assignedTo': None,
        'userPrincipalName': None
    },
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
    'AlertIds': ['41f7c150-9159-5412-8f48-ad360032db4b'],
    'BookmarkIds': '[]',
    'Comments': '[]',
    'Tasks': '[]',
    'Labels': '[]',
    'IncidentUrl': 'https://portal.azure.com/#asset/Microsoft_Azure_Security_Insights/Incident/subscriptions'
                   '/083de1fb-cd2d-4b7c-895a-2b5af1d091e8/resourceGroups/eastus/providers/Microsoft'
                   '.OperationalInsights/workspaces/sentinelwseastus/providers/Microsoft.SecurityInsights'
                   '/Incidents/7f788595-0fcf-4cb2-a669-07a4b5e8de99',
    'AdditionalData': {
        'alertsCount': 1,
        'bookmarksCount': 0,
        'commentsCount': 0,
        'alertProductNames': ['Azure Security Center'],
        'tactics': ['PreAttack'],
        'techniques': []
    },
    'ModifiedBy': 'Incident created from alert',
    'SourceSystem': 'Azure',
    'Type': 'SecurityIncident',
    'rn': '1'
}


class TestLogAnalyticsResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for azure_log_analytics translate results
    """

    @staticmethod
    def get_first(itr, constraint):
        """
        return the obj in the itr if constraint is true
        """
        return next(
            (obj for obj in itr if constraint(obj)),
            None
        )

    @staticmethod
    def get_first_of_type(itr, typ):
        """
        to check whether the object belongs to respective stix object
        """
        return TestLogAnalyticsResultsToStix.get_first(itr, lambda o: isinstance(o, dict) and o.get('type') == typ)

    @staticmethod
    def test_common_prop():
        """
        to test the common stix object properties
        """
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [DATA1], get_module_transformers(MODULE), options)
        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        assert result_bundle_identity['id'] == data_source['id']
        assert result_bundle_identity['name'] == data_source['name']
        assert result_bundle_identity['identity_class'] == data_source['identity_class']

        observed_data = result_bundle_objects[1]
        assert observed_data['id'] is not None
        assert observed_data['type'] == "observed-data"
        assert observed_data['created_by_ref'] == result_bundle_identity['id']

        assert observed_data['modified'] is not None
        assert observed_data['created'] is not None
        assert observed_data['first_observed'] is not None
        assert observed_data['last_observed'] is not None
        assert observed_data['number_observed'] is not None

    @staticmethod
    def test_x_ibm_finding_property():
        """
        to test the x-ibm finding object properties
        """
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [DATA1], get_module_transformers(MODULE), options)
        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]
        assert 'objects' in observed_data
        objects = observed_data['objects']

        x_ibm_finding = TestLogAnalyticsResultsToStix.get_first_of_type(objects.values(), 'x-ibm-finding')
        assert x_ibm_finding['finding_type'] == 'alert'
        assert x_ibm_finding['name'] == '[SAMPLE ALERT] Digital currency mining related behavior detected'
        assert x_ibm_finding['severity'] == '100'

    @staticmethod
    def test_x_alert_property():
        """
        to test the alert stix object properties
        """
        data = {
            "TenantId": "e00daaf8-d6a4-4410-b50b-f5ef61c9cb45",
            "TimeGenerated": "2022-05-04 16:47:08.560000+00:00",
            "DisplayName": "AlertLog",
            "AlertName": "AlertLog",
            "AlertSeverity": "Medium",
            'EventTime': '2022-05-24T14:27:36.370Z',
            "Description": "",
            "ProviderName": "ASI Scheduled Alerts",
            "VendorName": "Microsoft",
            "VendorOriginalId": "f1303f5e-daae-407e-ab87-e1d8ec3651da",
            "SystemAlertId": "50396c5f-2cb6-9d2f-e601-9f430bf17869",
            "ResourceId": "",
            "SourceComputerId": "",
            "AlertType": "e00daaf8-d6a4-4410-b50b-f5ef61c9cb45_9c4be437-b74c-440c-aa09-764367744a23",
            "ConfidenceLevel": "",
            "ConfidenceScore": "None",
            "IsIncident": "False",
            "StartTime": "2022-05-04 16:08:32.180000+00:00",
            "EndTime": "2022-05-04 16:08:32.180000+00:00",
            "ProcessingEndTime": "2022-05-04 16:47:08.560000+00:00",
            "RemediationSteps": "",
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
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        alert = TestLogAnalyticsResultsToStix.get_first_of_type(objects.values(), 'x-ibm-finding')

        assert alert is not None, 'Custom object type not found'
        assert alert['x_status'] == 'New'

    @staticmethod
    def test_x_incident_property():
        """
        to test incident stix object properties
        """
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [DATA3], get_module_transformers(MODULE), options)
        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']
        x_ibm_finding = TestLogAnalyticsResultsToStix.get_first_of_type(objects.values(), 'x-ibm-finding')
        assert x_ibm_finding is not None, 'Custom object type not found'
        assert x_ibm_finding['finding_type'] == 'violation'
        assert x_ibm_finding['severity'] == '50'

    @staticmethod
    def test_x_event_property():
        """
        to test event stix object properties
        """

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [DATA2], get_module_transformers(MODULE), options)
        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]
        assert 'objects' in observed_data
        objects = observed_data['objects']

        x_oca_event = TestLogAnalyticsResultsToStix.get_first_of_type(objects.values(), 'x-oca-event')
        assert x_oca_event is not None, 'Custom object type not found'
        assert x_oca_event['provider'] == 'Microsoft-Windows-AppLocker'
        assert x_oca_event['x_task'] == '0'

    @staticmethod
    def test_host_json_to_stix():
        """
        to test host stix object properties
        """
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [DATA2], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']
        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]
        assert 'objects' in observed_data
        objects = observed_data['objects']

        x_oca_asset = TestLogAnalyticsResultsToStix.get_first_of_type(objects.values(), 'x-oca-asset')

        assert x_oca_asset is not None, 'Custom object type not found'
        assert x_oca_asset['hostname'] == 'am-temp908cc196'

    @staticmethod
    def test_ipv4_addr_json_to_stix():
        """
        to test ipv4 stix object properties
        """
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [DATA2], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']
        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]
        assert 'objects' in observed_data
        objects = observed_data['objects']

        ip_obj = TestLogAnalyticsResultsToStix.get_first_of_type(objects.values(), 'ipv4-addr')

        assert ip_obj is not None, 'ip object type not found'
        assert ip_obj['value'] == '111.11.11.111'

    @staticmethod
    def test_url_json_to_stix():
        """
        to test url stix object properties
        """
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [DATA3], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']
        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]
        assert 'objects' in observed_data
        objects = observed_data['objects']

        url_obj = TestLogAnalyticsResultsToStix.get_first_of_type(objects.values(), 'url')

        assert url_obj is not None, 'url object type not found'
        assert url_obj['value'] == 'https://portal.azure.com/#asset/Microsoft_Azure_Security_Insights/Incident' \
                                   '/subscriptions/083de1fb-cd2d-4b7c-895a-2b5af1d091e8/resourceGroups/eastus' \
                                   '/providers/Microsoft.OperationalInsights/workspaces/sentinelwseastus/providers' \
                                   '/Microsoft.SecurityInsights/Incidents/7f788595-0fcf-4cb2-a669-07a4b5e8de99'

    @staticmethod
    def test_user_account_json_to_stix():
        """
        to test url stix object properties
        """
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [DATA2], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']
        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]
        assert 'objects' in observed_data
        objects = observed_data['objects']

        user_obj = TestLogAnalyticsResultsToStix.get_first_of_type(objects.values(), 'user-account')

        assert user_obj is not None, 'user object type not found'
        assert user_obj['user_id'] == 'test_user'

    @staticmethod
    def test_unmapped_attribute_with_mapped_attribute():
        message = "\"GET /blog HTTP/1.1\" 200 2571"
        data = {"message": message, "unmapped": "nothing to see here"}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]
        assert 'objects' in observed_data
        objects = observed_data['objects']
        assert objects == {}
        curr_obj = TestLogAnalyticsResultsToStix.get_first_of_type(objects.values(), 'message')
        assert (curr_obj is None), 'url object type not found'

    @staticmethod
    def test_unmapped_attribute_alone():
        data = {"unmapped": "nothing to see here"}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]
        assert 'objects' in observed_data
        objects = observed_data['objects']
        assert objects == {}
