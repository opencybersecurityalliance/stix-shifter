# Azure Log Analytics

## Supported STIX Mappings

See the [table of mappings](azure_log_analytics_supported_stix.md) for the STIX objects and operators supported by this connector.

## Data Source 
Microsoft Azure Log Analytics is a tool to run queries on data collected by different Azure services. A Log Analytics workspace needs to be created to collect logs from Azure services. The connector can run Kusto Query Language (KQL) queries to search logs in the workspace.

## API and Logs

Currently, [Log Analytics REST API](https://learn.microsoft.com/en-us/rest/api/loganalytics/) has been used to search three types of Azure logs:

1. Security Alert
2. Security Events 
3. Security Incidents

Therefore, three dialects has been set in the from_stix mapping file. More data tables will be supported in future.

Azure SDK for Python is used in order to make API calls to Log Analytics API. Mainly two libraries are used:

1. [Azure Identity library](https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python)
    - It mainly enables the Azure SDK clients to authenticate with AAD
2. [Azure Monitor Query client library](https://learn.microsoft.com/en-us/python/api/overview/azure/monitor-query-readme?view=azure-python)
    - It provides functions to run queries on the logs available in Azure Log Analytics
    - [Kusto Query Language (KQL)](https://learn.microsoft.com/en-us/azure/data-explorer/kusto/query/) has been used as a query language to run search using this client.

### Format for calling stix-shifter from the command line

python main.py `<translator_module>` `<query or result>` `<STIX identity object>` `<data>`

### Example I - Converting from STIX patterns to KQL (STIX attributes)
STIX to KQL field mapping is defined in `<dialects>_from_stix_map.json` <br/>

This example input pattern:

`translate azure_log_analytics query '{}' "[process:name = 'svchost.exe'] START t'2023-03-09T05:18:21.746Z' STOP t'2023-03-11T05:18:21.746Z'"`

Returns the following translated query:

```
{
    "queries": [
        "SecurityEvent | where ((NewProcessName == 'svchost.exe' or Process == 'svchost.exe' or ParentProcessName == 'svchost.exe' or LogonProcessName == 'svchost.exe')) and (TimeGenerated between (datetime(2023-03-09T05:18:21.746Z) .. datetime(2023-03-11T05:18:21.746Z)))"
    ]
}
```

### Example II - Converting from STIX patterns to KQL Custom STIX attributes)

This example input pattern:

`translate azure_log_analytics query ‘{}’ "[x-ibm-finding:name = 'Microsoft-Windows-Security-Auditing'] START t'2019-01-01T08:43:10Z' STOP t'2019-12-31T08:43:10Z'"`

Returns the following translated queries:
```
{
    "queries": [
        "SecurityAlert | where (AlertName == 'Microsoft-Windows-Security-Auditing') and (TimeGenerated between (datetime(2019-01-01T08:43:10Z) .. datetime(2019-12-31T08:43:10Z)))",
        "SecurityEvent | where (Activity == 'Microsoft-Windows-Security-Auditing') and (TimeGenerated between (datetime(2019-01-01T08:43:10Z) .. datetime(2019-12-31T08:43:10Z)))",
        "SecurityIncident | where (Title == 'Microsoft-Windows-Security-Auditing') and (TimeGenerated between (datetime(2019-01-01T08:43:10Z) .. datetime(2019-12-31T08:43:10Z)))"
    ]
}
```

### Pattern expression with STIX and CUSTOM attributes

#### Single Observation

#### STIX Translate query to fetch the Executable found running from a suspicious location
```shell
translate azure_log_analytics query '{}' "[x-ibm-finding:name LIKE 'Executable found running from a suspicious location'] START t'2023-03-01T00:00:00.000Z' STOP t'2023-03-26T11:00:00.000Z'"
```
#### STIX Translate query - output
```json
{
    "queries": [
        "SecurityAlert | where (AlertName contains 'Executable found running from a suspicious location') and (TimeGenerated between (datetime(2023-03-01T00:00:00.000Z) .. datetime(2023-03-26T11:00:00.000Z)))",
        "SecurityEvent | where (Activity contains 'Executable found running from a suspicious location') and (TimeGenerated between (datetime(2023-03-01T00:00:00.000Z) .. datetime(2023-03-26T11:00:00.000Z)))",
        "SecurityIncident | where (Title contains 'Executable found running from a suspicious location') and (TimeGenerated between (datetime(2023-03-01T00:00:00.000Z) .. datetime(2023-03-26T11:00:00.000Z)))"
    ]
}

```

#### STIX Transmit results 

```shell
transmit
azure_log_analytics
"{\"host\":\"xxx\",\"workspaceId\":\"xxx\"}"
"{\"auth\":{\"tenant\": \"xxx\", \"clientId\": \"xxx\", \"clientSecret\": \"xxx\"}}"
results
"SecurityAlert | where (AlertName contains 'Executable found running from a suspicious location') and (TimeGenerated between (datetime(2023-03-01T00:00:00.000Z) .. datetime(2023-03-26T11:00:00.000Z)))"
0
1
```

#### STIX Transmit results - output
```json
{
    "success": true,
    "data": [
        {
            "TenantId": "xxx",
            "TimeGenerated": "2023-03-10 04:58:00.613814+00:00",
            "DisplayName": "[SAMPLE ALERT] Executable found running from a suspicious location",
            "AlertName": "[SAMPLE ALERT] Executable found running from a suspicious location",
            "AlertSeverity": "75",
            "Description": "THIS IS A SAMPLE ALERT: Analysis of host data detected an executable file on Sample-VM that is running from a location in common with known suspicious files. This executable could either be legitimate activity, or an indication of a compromised host.",
            "ProviderName": "Azure Security Center",
            "VendorName": "Microsoft",
            "VendorOriginalId": "2517238771573679907_7692caa7-0d1b-432f-9865-ef7932a3514d",
            "SystemAlertId": "e6b0d35f-c7c8-373b-3ff3-5c903c9a2060",
            "ResourceId": "/SUBSCRIPTIONS/xxx/RESOURCEGROUPS/Sample-RG/providers/Microsoft.Compute/virtualMachines/Sample-VM",
            "SourceComputerId": "",
            "AlertType": "SIMULATED_VM_SuspectExecutablePath",
            "ConfidenceLevel": "",
            "ConfidenceScore": "None",
            "IsIncident": "False",
            "StartTime": "2023-03-10 04:47:22.632009+00:00",
            "EndTime": "2023-03-10 04:47:22.632009+00:00",
            "ProcessingEndTime": "2023-03-10 04:48:02.632009+00:00",
            "RemediationSteps": "Review with WORKGROUP\\\\Sample-account the suspicious process in this alert to see if you recognise this as legitimate administrative activity. If not, Escalate the alert to the information security team.",
            "ExtendedProperties": {
                "resourceType": "Virtual Machine",
                "Suspicious Process Id": "0x1eec",
                "Compromised Host": "Sample-VM",
                "Account Session Id": "0x3e7",
                "Suspicious Process": "c:\\windows\\inf\\sample.exe",
                "Suspicious Command Line": "c:\\windows\\inf\\sample.exe",
                "User Name": "WORKGROUP\\Sample-account",
                "ProcessedBySentinel": "True",
                "Alert generation status": "Full alert created"
            },
            "Entities": {
                "host": {
                    "$id": "2",
                    "DnsDomain": "",
                    "NTDomain": "",
                    "HostName": "Sample-VM",
                    "NetBiosName": "Sample-VM",
                    "AzureID": "/SUBSCRIPTIONS/xxx/RESOURCEGROUPS/Sample-RG/providers/Microsoft.Compute/virtualMachines/Sample-VM",
                    "OMSAgentID": "00000000-0000-0000-0000-000000000001",
                    "OSFamily": "Windows",
                    "OSVersion": "Windows",
                    "IsDomainJoined": false,
                    "Type": "host",
                    "AccountType": "windows-local"
                },
                "account": {
                    "$id": "3",
                    "Name": "SAMPLE-account",
                    "NTDomain": "SAMPLE",
                    "Host": {
                        "$id": "2",
                        "DnsDomain": "",
                        "NTDomain": "",
                        "HostName": "Sample-VM",
                        "NetBiosName": "Sample-VM",
                        "AzureID": "/SUBSCRIPTIONS/xxx/RESOURCEGROUPS/Sample-RG/providers/Microsoft.Compute/virtualMachines/Sample-VM",
                        "OMSAgentID": "00000000-0000-0000-0000-000000000001",
                        "OSFamily": "Windows",
                        "OSVersion": "Windows",
                        "IsDomainJoined": false,
                        "Type": "host",
                        "AccountType": "windows-local"
                    },
                    "Sid": "S-0-0-00",
                    "IsDomainJoined": true,
                    "Type": "account",
                    "LogonId": "0x3e7",
                    "AccountType": "windows-domain"
                },
                "process": [
                    {
                        "$id": "6",
                        "ProcessId": "0x1eec",
                        "CommandLine": "",
                        "ElevationToken": "Default",
                        "CreationTimeUtc": "2023-03-10T04:47:22.6320092Z",
                        "ImageFile": {
                            "$id": "5",
                            "Directory": "c:\\windows\\inf",
                            "Name": "sample.exe",
                            "Type": "file"
                        },
                        "Account": {
                            "$id": "3",
                            "Name": "SAMPLE-account",
                            "NTDomain": "SAMPLE",
                            "Host": {
                                "$id": "2",
                                "DnsDomain": "",
                                "NTDomain": "",
                                "HostName": "Sample-VM",
                                "NetBiosName": "Sample-VM",
                                "AzureID": "/SUBSCRIPTIONS/xxx/RESOURCEGROUPS/Sample-RG/providers/Microsoft.Compute/virtualMachines/Sample-VM",
                                "OMSAgentID": "00000000-0000-0000-0000-000000000001",
                                "OSFamily": "Windows",
                                "OSVersion": "Windows",
                                "IsDomainJoined": false,
                                "Type": "host",
                                "AccountType": "windows-local"
                            },
                            "Sid": "S-0-0-00",
                            "IsDomainJoined": true,
                            "Type": "account",
                            "LogonId": "0x3e7",
                            "AccountType": "windows-domain"
                        },
                        "ParentProcess": {
                            "$id": "4",
                            "ProcessId": "0x1038",
                            "CommandLine": "",
                            "Host": {
                                "$id": "2",
                                "DnsDomain": "",
                                "NTDomain": "",
                                "HostName": "Sample-VM",
                                "NetBiosName": "Sample-VM",
                                "AzureID": "/SUBSCRIPTIONS/xxx/RESOURCEGROUPS/Sample-RG/providers/Microsoft.Compute/virtualMachines/Sample-VM",
                                "OMSAgentID": "00000000-0000-0000-0000-000000000001",
                                "OSFamily": "Windows",
                                "OSVersion": "Windows",
                                "IsDomainJoined": false,
                                "Type": "host",
                                "AccountType": "windows-local"
                            },
                            "Type": "process"
                        },
                        "Host": {
                            "$id": "2",
                            "DnsDomain": "",
                            "NTDomain": "",
                            "HostName": "Sample-VM",
                            "NetBiosName": "Sample-VM",
                            "AzureID": "/SUBSCRIPTIONS/xxx/RESOURCEGROUPS/Sample-RG/providers/Microsoft.Compute/virtualMachines/Sample-VM",
                            "OMSAgentID": "00000000-0000-0000-0000-000000000001",
                            "OSFamily": "Windows",
                            "OSVersion": "Windows",
                            "IsDomainJoined": false,
                            "Type": "host",
                            "AccountType": "windows-local"
                        },
                        "Type": "process"
                    }
                ],
                "file": {
                    "$id": "5",
                    "Directory": "c:\\windows\\inf",
                    "Name": "sample.exe",
                    "Type": "file"
                },
                "host-logon-session": {
                    "$id": "7",
                    "SessionId": "0x3e7",
                    "StartTimeUtc": "2023-03-10T04:47:22.6320092Z",
                    "EndTimeUtc": "2023-03-10T04:47:22.6320092Z",
                    "Type": "host-logon-session",
                    "Host": {
                        "$id": "2",
                        "DnsDomain": "",
                        "NTDomain": "",
                        "HostName": "Sample-VM",
                        "NetBiosName": "Sample-VM",
                        "AzureID": "/SUBSCRIPTIONS/xxx/RESOURCEGROUPS/Sample-RG/providers/Microsoft.Compute/virtualMachines/Sample-VM",
                        "OMSAgentID": "00000000-0000-0000-0000-000000000001",
                        "OSFamily": "Windows",
                        "OSVersion": "Windows",
                        "IsDomainJoined": false,
                        "Type": "host",
                        "AccountType": "windows-local"
                    },
                    "Account": {
                        "$id": "3",
                        "Name": "SAMPLE-account",
                        "NTDomain": "SAMPLE",
                        "Host": {
                            "$id": "2",
                            "DnsDomain": "",
                            "NTDomain": "",
                            "HostName": "Sample-VM",
                            "NetBiosName": "Sample-VM",
                            "AzureID": "/SUBSCRIPTIONS/xxx/RESOURCEGROUPS/Sample-RG/providers/Microsoft.Compute/virtualMachines/Sample-VM",
                            "OMSAgentID": "00000000-0000-0000-0000-000000000001",
                            "OSFamily": "Windows",
                            "OSVersion": "Windows",
                            "IsDomainJoined": false,
                            "Type": "host",
                            "AccountType": "windows-local"
                        },
                        "Sid": "S-0-0-00",
                        "IsDomainJoined": true,
                        "Type": "account",
                        "LogonId": "0x3e7",
                        "AccountType": "windows-domain"
                    }
                }
            },
            "SourceSystem": "Detection",
            "WorkspaceSubscriptionId": "00000000-0000-0000-0000-000000000001",
            "WorkspaceResourceGroup": "defaultresourcegroup-wus",
            "ExtendedLinks": "",
            "ProductName": "Azure Security Center",
            "ProductComponentName": "",
            "AlertLink": "https://portal.azure.com/#blade/Microsoft_Azure_Security_AzureDefenderForData/AlertBlade/alertId/2517238771573679907_7692caa7-0d1b-432f-9865-ef7932a3514d/subscriptionId/xxx/resourceGroup/Sample-RG/referencedFrom/alertDeepLink/location/centralus",
            "Status": "New",
            "CompromisedEntity": "Sample-VM",
            "Tactics": "Execution",
            "Techniques": null,
            "Type": "SecurityAlert",
            "rn": "1",
            "entity": {
                "2": {
                    "$id": "2",
                    "DnsDomain": "",
                    "NTDomain": "",
                    "HostName": "Sample-VM",
                    "NetBiosName": "Sample-VM",
                    "AzureID": "/SUBSCRIPTIONS/xxx/RESOURCEGROUPS/Sample-RG/providers/Microsoft.Compute/virtualMachines/Sample-VM",
                    "OMSAgentID": "00000000-0000-0000-0000-000000000001",
                    "OSFamily": "Windows",
                    "OSVersion": "Windows",
                    "IsDomainJoined": false,
                    "Type": "host",
                    "AccountType": "windows-local"
                },
                "3": {
                    "$id": "3",
                    "Name": "SAMPLE-account",
                    "NTDomain": "SAMPLE",
                    "Host": {
                        "$id": "2",
                        "DnsDomain": "",
                        "NTDomain": "",
                        "HostName": "Sample-VM",
                        "NetBiosName": "Sample-VM",
                        "AzureID": "/SUBSCRIPTIONS/xxx/RESOURCEGROUPS/Sample-RG/providers/Microsoft.Compute/virtualMachines/Sample-VM",
                        "OMSAgentID": "00000000-0000-0000-0000-000000000001",
                        "OSFamily": "Windows",
                        "OSVersion": "Windows",
                        "IsDomainJoined": false,
                        "Type": "host",
                        "AccountType": "windows-local"
                    },
                    "Sid": "S-0-0-00",
                    "IsDomainJoined": true,
                    "Type": "account",
                    "LogonId": "0x3e7",
                    "AccountType": "windows-domain"
                },
                "4": {
                    "$id": "4",
                    "ProcessId": "0x1038",
                    "CommandLine": "",
                    "Host": {
                        "$id": "2",
                        "DnsDomain": "",
                        "NTDomain": "",
                        "HostName": "Sample-VM",
                        "NetBiosName": "Sample-VM",
                        "AzureID": "/SUBSCRIPTIONS/xxx/RESOURCEGROUPS/Sample-RG/providers/Microsoft.Compute/virtualMachines/Sample-VM",
                        "OMSAgentID": "00000000-0000-0000-0000-000000000001",
                        "OSFamily": "Windows",
                        "OSVersion": "Windows",
                        "IsDomainJoined": false,
                        "Type": "host",
                        "AccountType": "windows-local"
                    },
                    "Type": "process"
                },
                "5": {
                    "$id": "5",
                    "Directory": "c:\\windows\\inf",
                    "Name": "sample.exe",
                    "Type": "file"
                },
                "6": {
                    "$id": "6",
                    "ProcessId": "0x1eec",
                    "CommandLine": "",
                    "ElevationToken": "Default",
                    "CreationTimeUtc": "2023-03-10T04:47:22.6320092Z",
                    "ImageFile": {
                        "$id": "5",
                        "Directory": "c:\\windows\\inf",
                        "Name": "sample.exe",
                        "Type": "file"
                    },
                    "Account": {
                        "$id": "3",
                        "Name": "SAMPLE-account",
                        "NTDomain": "SAMPLE",
                        "Host": {
                            "$id": "2",
                            "DnsDomain": "",
                            "NTDomain": "",
                            "HostName": "Sample-VM",
                            "NetBiosName": "Sample-VM",
                            "AzureID": "/SUBSCRIPTIONS/xxx/RESOURCEGROUPS/Sample-RG/providers/Microsoft.Compute/virtualMachines/Sample-VM",
                            "OMSAgentID": "00000000-0000-0000-0000-000000000001",
                            "OSFamily": "Windows",
                            "OSVersion": "Windows",
                            "IsDomainJoined": false,
                            "Type": "host",
                            "AccountType": "windows-local"
                        },
                        "Sid": "S-0-0-00",
                        "IsDomainJoined": true,
                        "Type": "account",
                        "LogonId": "0x3e7",
                        "AccountType": "windows-domain"
                    },
                    "ParentProcess": {
                        "$id": "4",
                        "ProcessId": "0x1038",
                        "CommandLine": "",
                        "Host": {
                            "$id": "2",
                            "DnsDomain": "",
                            "NTDomain": "",
                            "HostName": "Sample-VM",
                            "NetBiosName": "Sample-VM",
                            "AzureID": "/SUBSCRIPTIONS/xxx/RESOURCEGROUPS/Sample-RG/providers/Microsoft.Compute/virtualMachines/Sample-VM",
                            "OMSAgentID": "00000000-0000-0000-0000-000000000001",
                            "OSFamily": "Windows",
                            "OSVersion": "Windows",
                            "IsDomainJoined": false,
                            "Type": "host",
                            "AccountType": "windows-local"
                        },
                        "Type": "process"
                    },
                    "Host": {
                        "$id": "2",
                        "DnsDomain": "",
                        "NTDomain": "",
                        "HostName": "Sample-VM",
                        "NetBiosName": "Sample-VM",
                        "AzureID": "/SUBSCRIPTIONS/xxx/RESOURCEGROUPS/Sample-RG/providers/Microsoft.Compute/virtualMachines/Sample-VM",
                        "OMSAgentID": "00000000-0000-0000-0000-000000000001",
                        "OSFamily": "Windows",
                        "OSVersion": "Windows",
                        "IsDomainJoined": false,
                        "Type": "host",
                        "AccountType": "windows-local"
                    },
                    "Type": "process"
                },
                "7": {
                    "$id": "7",
                    "SessionId": "0x3e7",
                    "StartTimeUtc": "2023-03-10T04:47:22.6320092Z",
                    "EndTimeUtc": "2023-03-10T04:47:22.6320092Z",
                    "Type": "host-logon-session",
                    "Host": {
                        "$id": "2",
                        "DnsDomain": "",
                        "NTDomain": "",
                        "HostName": "Sample-VM",
                        "NetBiosName": "Sample-VM",
                        "AzureID": "/SUBSCRIPTIONS/xxx/RESOURCEGROUPS/Sample-RG/providers/Microsoft.Compute/virtualMachines/Sample-VM",
                        "OMSAgentID": "00000000-0000-0000-0000-000000000001",
                        "OSFamily": "Windows",
                        "OSVersion": "Windows",
                        "IsDomainJoined": false,
                        "Type": "host",
                        "AccountType": "windows-local"
                    },
                    "Account": {
                        "$id": "3",
                        "Name": "SAMPLE-account",
                        "NTDomain": "SAMPLE",
                        "Host": {
                            "$id": "2",
                            "DnsDomain": "",
                            "NTDomain": "",
                            "HostName": "Sample-VM",
                            "NetBiosName": "Sample-VM",
                            "AzureID": "/SUBSCRIPTIONS/xxx/RESOURCEGROUPS/Sample-RG/providers/Microsoft.Compute/virtualMachines/Sample-VM",
                            "OMSAgentID": "00000000-0000-0000-0000-000000000001",
                            "OSFamily": "Windows",
                            "OSVersion": "Windows",
                            "IsDomainJoined": false,
                            "Type": "host",
                            "AccountType": "windows-local"
                        },
                        "Sid": "S-0-0-00",
                        "IsDomainJoined": true,
                        "Type": "account",
                        "LogonId": "0x3e7",
                        "AccountType": "windows-domain"
                    }
                }
            }
        }
    ]
}
```

#### STIX Translate results

```json
{
    "type": "bundle",
    "id": "bundle--fec593b7-a79c-4644-af68-f7f0a03e48a6",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "azure_log_analytics",
            "identity_class": "events",
            "created": "2022-04-11T16:11:11.878Z",
            "modified": "2022-04-11T16:11:11.878Z"
        },
        {
            "id": "observed-data--d824c87c-7cfa-4e07-8395-538e28f2a2dd",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2023-04-11T06:07:41.162Z",
            "modified": "2023-04-11T06:07:41.162Z",
            "objects": {
                "0": {
                    "type": "x-cloud-provider",
                    "tenant_id": "xxx"
                },
                "1": {
                    "type": "x-ibm-finding",
                    "time_observed": "2023-03-22 07:28:13.169899+00:00",
                    "name": "[SAMPLE ALERT] Executable found running from a suspicious location",
                    "ttp_tagging_refs": [
                        "2"
                    ],
                    "severity": "75",
                    "description": "THIS IS A SAMPLE ALERT: Analysis of host data detected an executable file on Sample-VM that is running from a location in common with known suspicious files. This executable could either be legitimate activity, or an indication of a compromised host.",
                    "alert_id": "2517228307685103557_54bad678-9725-4c5f-a7ca-4a48aaa4cd92",
                    "x_system_alert_id": "ee8aabb9-59bb-135f-aab1-84724102fa94",
                    "x_alert_type": "SIMULATED_VM_SuspectExecutablePath",
                    "confidence": 0,
                    "start": "2023-03-22 07:27:11.489644+00:00",
                    "end": "2023-03-22 07:27:11.489644+00:00",
                    "x_processing_endtime": "2023-03-22 07:27:51.489644+00:00",
                    "x_remediationSteps": "Review with WORKGROUP\\\\Sample-account the suspicious process in this alert to see if you recognise this as legitimate administrative activity. If not, Escalate the alert to the information security team.",
                    "dst_os_ref": "7",
                    "dst_os_user_ref": "8",
                    "ioc_refs": [
                        "12"
                    ],
                    "dst_application_ref": "3",
                    "x_alert_link": "https://portal.azure.com/#blade/Microsoft_Azure_Security_AzureDefenderForData/AlertBlade/alertId/2517228307685103557_54bad678-9725-4c5f-a7ca-4a48aaa4cd92/subscriptionId/xxx/resourceGroup/Sample-RG/referencedFrom/alertDeepLink/location/centralus",
                    "x_status": "New",
                    "x_compromised_entity": "Sample-VM",
                    "finding_type": "alert"
                },
                "2": {
                    "type": "x-ibm-ttp-tagging",
                    "name": "[SAMPLE ALERT] Executable found running from a suspicious location",
                    "confidence": 0.0,
                    "extensions": {
                        "mitre-attack-ext": {
                            "tactic_name": "Execution"
                        }
                    }
                },
                "3": {
                    "type": "software",
                    "x_provider": "Azure Security Center",
                    "vendor": "Microsoft",
                    "name": "Azure Security Center",
                    "x_product_component_name": "VirtualMachines"
                },
                "4": {
                    "type": "x-cloud-resource",
                    "resource_id": "/SUBSCRIPTIONS/xxx/RESOURCEGROUPS/Sample-RG/providers/Microsoft.Compute/virtualMachines/Sample-VM",
                    "resource_type": "Virtual Machine"
                },
                "5": {
                    "type": "x-oca-asset",
                    "hostname": "Sample-VM",
                    "x_netbios_name": "Sample-VM",
                    "x_oms_agent_id": "00000000-0000-0000-0000-000000000001",
                    "os_ref": "7",
                    "x_is_domain_host": false
                },
                "6": {
                    "type": "x-host-logon-session",
                    "host_ref": "5",
                    "account_ref": "8",
                    "session_id": 999,
                    "start_time": "2023-03-22T07:27:11.4896442Z",
                    "end_time": "2023-03-22T07:27:11.4896442Z"
                },
                "7": {
                    "type": "software",
                    "name": "Windows",
                    "version": "Windows"
                },
                "8": {
                    "type": "user-account",
                    "user_id": "SAMPLE-account",
                    "x_nt_domain": "SAMPLE",
                    "x_account_sid": "S-0-0-00",
                    "is_service_account": true,
                    "account_type": "windows-domain"
                },
                "9": {
                    "type": "process",
                    "creator_user_ref": "8",
                    "pid": 7916,
                    "x_elevation_token": "Default",
                    "created": "2023-03-22T07:27:11.4896442Z",
                    "parent_ref": "10",
                    "binary_ref": "12"
                },
                "10": {
                    "type": "process",
                    "creator_user_ref": "8",
                    "pid": 4152
                },
                "11": {
                    "type": "directory",
                    "path": "c:\\windows\\inf"
                },
                "12": {
                    "type": "file",
                    "parent_directory_ref": "11",
                    "name": "sample.exe"
                }
            },
            "first_observed": "2023-04-11T06:07:41.162Z",
            "last_observed": "2023-04-11T06:07:41.162Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```


#### STIX Translate query to fetch the Incident having greater or equal to three alerts count.
```shell
translate azure_log_analytics query '{}' "[x-alerts-info:alert_count >=3] START t'2023-03-01T11:00:00.003Z' STOP t'2023-03-30T11:00:00.003Z'"
```
#### STIX Translate query - output
```json
{
    "queries": [
        "SecurityIncident | where (AdditionalData.alertsCount >= 3) and (TimeGenerated between (datetime(2023-03-01T11:00:00.003Z) .. datetime(2023-03-30T11:00:00.003Z)))"
    ]
}

```

#### STIX Transmit results 

```shell
{
    "success": true,
    "data": [
        {
            "TenantId": "xxx",
            "TimeGenerated": "2023-03-09 13:40:51.080319+00:00",
            "IncidentName": "d5c17060-b17b-490b-8895-0aa12da7db0c",
            "Title": "Preview: Possible SQL based multistage attack detected by Fusion",
            "Description": "Multiple alerts related to a potential SQL based attack was detected on IP: 00.00.00.00 and on Resource Group: /subscriptions/083de1fb-cd2d-4b7c-895a-2b5af1d091e8/resourcegroups/sample-rg. SQL databases are often targeted by attackers in threat campaigns as they may contain lots of valuable information including personally identifiable information, intellectual property, etc. A successful compromise of an insecurely configured SQL installation could be exploited to get full system admin privileges.<br><br>Recommended Remediation Steps:<br>&nbsp;&nbsp;&nbsp;&nbsp;1) Check if the alerts reveal the initial source of compromise and other stages of the attack that could help in expediating the investigation and containment of the incident.<br>&nbsp;&nbsp;&nbsp;&nbsp;2) Disable \u2018sa\u2019 account and rename the sa account.<br>&nbsp;&nbsp;&nbsp;&nbsp;3) To prevent future brute force attempts, <a href=\"https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/scm-services-change-the-password-of-the-accounts-used\">change and harden the \u2018sa\u2019 password</a> and set the sa Login to \u2018Disabled\u2019.<br>&nbsp;&nbsp;&nbsp;&nbsp;4) It\u2019s also a good idea to <a href=\"https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/xp-cmdshell-server-configuration-option\">ensure that \u2018xp_cmdshell\u2019 is disabled</a>. Again, note that this should be disabled by default.<br>&nbsp;&nbsp;&nbsp;&nbsp;5) If TCP port 1433 is not required to be opened to the internet, ensure that there are no rules in Network Security Group that allows 1433. <br>&nbsp;&nbsp;&nbsp;&nbsp;6) Inspect all stored procedures that may have been enabled in SQL and look for stored procedures that may be implementing \u2018xp_cmdshell\u2019 and & running unusual commands.<br>&nbsp;&nbsp;&nbsp;&nbsp;7) AAD authentication could also be used to further enhance the security system against such threats.<br>&nbsp;&nbsp;&nbsp;&nbsp;8) It is recommended to explore the audit records around the time of the alert in order to determine the nature of the anomalous activity.<br>&nbsp;&nbsp;&nbsp;&nbsp;9) Check the SQL firewall rules that defines which IPs are allowed to access and consider checking the range of IP addresses that allow to access the database to minimize the attack surface on the server.<br>&nbsp;&nbsp;&nbsp;&nbsp;10) We recommend to backup & and rebuild the SQL Server if possible and reset all user accounts. <br>&nbsp;&nbsp;&nbsp;&nbsp;11) Leverage resources available on Microsoft\u2019s <a href=\"https://github.com/Azure/Azure-Sentinel\">Sentinel GitHub</a> for further investigation on these attacks. <a href=\"https://learn.microsoft.com/en-us/azure/sentinel/detect-threats-custom\">Scheduled rules</a> could be used to build advanced hunting scenarios to discover more related threats and anomalous behaviors in your environment.<br><br>For more information about this detection, please visit\u202fhttps://aka.ms/SentinelFusion <br><br>**PLEASE NOTE:** <br>1) Your feedback is critical to help Microsoft deliver the highest quality detections. When you close this incident, please provide feedback on whether this incident was a True Positive, Benign True Positive, or a False Positive, along with any amplifying details in the comments. <br>2) Fusion may generate incidents based on a new alert AND an alert that has been included in a previous incident. This means Fusion has identified a new attack scenario and we recommend that you take actions to investigate. To find previous incidents included the same alert, you can: <br>&nbsp;&nbsp;&nbsp;&nbsp;1). Navigate to \"Logs\" page <br>&nbsp;&nbsp;&nbsp;&nbsp;2). Set preferred time range <br>&nbsp;&nbsp;&nbsp;&nbsp;3). Run the following KQL query:  <br> \r\n ````  \r\n SecurityIncident  \r\n | where AlertIds has_any (<list of alerts from this Fusion incident>)\r\n | where ProviderIncidentId != \"<incident id of this Fusion incident>\" \r\n````\r\n",
            "Severity": "100",
            "Status": "New",
            "Classification": "",
            "ClassificationComment": "",
            "ClassificationReason": "",
            "Owner": {
                "objectId": "223-345",
                "email": null,
                "assignedTo": "user1",
                "userPrincipalName": "user1@xyz.com"
            },
            "ProviderName": "XYZ",
            "ProviderIncidentId": "6284",
            "FirstActivityTime": "2023-03-09 05:03:47.436499+00:00",
            "LastActivityTime": "2023-03-09 05:04:35.311500+00:00",
            "FirstModifiedTime": "None",
            "LastModifiedTime": "2023-03-09 13:40:51.080319+00:00",
            "CreatedTime": "2023-03-09 13:40:51.080319+00:00",
            "ClosedTime": "2023-03-09 13:40:51.080319+00:00",
            "IncidentNumber": "6284",
            "RelatedAnalyticRuleIds": "[\"BuiltInFusion\"]",
            "AlertIds": [
                "ba4cee8e-d872-0138-9ca8-c019315c083d",
                "245d6d27-3a27-b072-493e-1f8e2acc4be4",
                "bbdef8ba-0ba6-5fe1-b8ae-700cd770a00c",
                "03d4afbf-aa96-d6d1-5168-f165ed66d8e5"
            ],
            "BookmarkIds": "[]",
            "Comments": "[]",
            "Tasks": "[]",
            "Labels": "[]",
            "IncidentUrl": "https://portal.azure.com/#asset/Microsoft_Azure_Security_Insights/Incident/subscriptions/083de1fb-cd2d-4b7c-895a-2b5af1d091e8/resourceGroups/eastus/providers/Microsoft.OperationalInsights/workspaces/sentinelwseastus/providers/Microsoft.SecurityInsights/Incidents/d5c17060-b17b-490b-8895-0aa12da7db0c",
            "AdditionalData": {
                "alertsCount": 4,
                "bookmarksCount": 0,
                "commentsCount": 0,
                "alertProductNames": [
                    "Azure Defender"
                ],
                "tactics": "PreAttack, Discovery, LateralMovement, Exfiltration",
                "techniques": null
            },
            "ModifiedBy": "Fusion",
            "SourceSystem": "Azure",
            "Type": "SecurityIncident",
            "rn": "1",
            "ProviderNameIncident": "Azure Sentinel"
        }
    ]
}
```

#### STIX Translate results

```json
{
    "type": "bundle",
    "id": "bundle--a0eb0bea-dbe7-4dfa-b834-771e97f87f6b",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "azure_log_analytics",
            "identity_class": "events",
            "created": "2022-04-11T16:11:11.878Z",
            "modified": "2022-04-11T16:11:11.878Z"
        },
        {
            "id": "observed-data--32f70391-5868-47c5-bbf3-b7c4fee5adac",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2023-04-11T06:34:44.081Z",
            "modified": "2023-04-11T06:34:44.081Z",
            "objects": {
                "0": {
                    "type": "x-cloud-provider",
                    "tenant_id": "xxx"
                },
                "1": {
                    "type": "x-ibm-finding",
                    "time_observed": "2023-03-09 13:40:51.080319+00:00",
                    "x_incident_name": "d5c17060-b17b-490b-8895-0aa12da7db0c",
                    "name": "Preview: Possible SQL based multistage attack detected by Fusion",
                    "ttp_tagging_refs": [
                        "2"
                    ],
                    "description": "Multiple alerts related to a potential SQL based attack was detected on IP: 00.00.00.00 and on Resource Group",
                    "severity": "100",
                    "x_status": "New",
                    "x_owner_ref": "3",
                    "x_provider_incident_id": "6284",
                    "end": "2023-03-09 13:40:51.080319+00:00",
                    "start": "2023-03-09 13:40:51.080319+00:00",
                    "rule_names": "[\"BuiltInFusion\"]",
                    "x_modified_by": "Fusion",
                    "finding_type": "violation",
                    "x_provider": "Azure Sentinel",
                    "x_alert_ids": [
                        "ba4cee8e-d872-0138-9ca8-c019315c083d",
                        "245d6d27-3a27-b072-493e-1f8e2acc4be4",
                        "bbdef8ba-0ba6-5fe1-b8ae-700cd770a00c",
                        "03d4afbf-aa96-d6d1-5168-f165ed66d8e5"
                    ],
                    "x_alert_count": 4,
                    "x_alert_product_names": [
                        "Azure Defender"
                    ]
                },
                "2": {
                    "type": "x-ibm-ttp-tagging",
                    "name": "Preview: Possible SQL based multistage attack detected by Fusion",
                    "extensions": {
                        "mitre-attack-ext": {
                            "tactic_name": "PreAttack, Discovery, LateralMovement, Exfiltration"
                        }
                    }
                },
                "3": {
                    "type": "email-addr",
                    "display_name": "user1",
                    "value": "user1@xyz.com"
                },
                "4": {
                    "type": "software",
                    "x_provider": "XYZ"
                },
                "5": {
                    "type": "x-incident-info",
                    "first_activity": "2023-03-09 05:03:47.436499+00:00",
                    "last_active": "2023-03-09 05:04:35.311500+00:00",
                    "first_modified": "None",
                    "closed_time": "2023-03-09 13:40:51.080319+00:00",
                    "comments": "[]",
                    "tasks": "[]",
                    "labels": "[]",
                    "incident_url_ref": "6"
                },
                "6": {
                    "type": "url",
                    "value": "https://portal.azure.com/#asset/Microsoft_Azure_Security_Insights/Incident/subscriptions/083de1fb-cd2d-4b7c-895a-2b5af1d091e8/resourceGroups/eastus/providers/Microsoft.OperationalInsights/workspaces/sentinelwseastus/providers/Microsoft.SecurityInsights/Incidents/d5c17060-b17b-490b-8895-0aa12da7db0c"
                }
            },
            "first_observed": "2023-04-11T06:34:44.081Z",
            "last_observed": "2023-04-11T06:34:44.081Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```

#### STIX Translate query to fetch the Incident having greater or equal to three alerts count.
```shell
translate azure_log_analytics query '{}' "[x-oca-event:action LIKE '4624'] START t'2023-01-01T08:43:10Z' STOP t'2023-03-31T08:43:10Z'"
```
#### STIX Translate query - output
```json
{
    "queries": [
        "SecurityEvent | where (Activity contains '4624') and (TimeGenerated between (datetime(2023-01-01T08:43:10Z) .. datetime(2023-03-31T08:43:10Z)))"
    ]
}

```
#### STIX Transmit results 

```shell
{
    "success": true,
    "data": [
        {
          "TenantId": "xxxx",
          "TimeGenerated": "2023-04-10T07:47:01.9710164Z",
          "SourceSystem": "OpsManager",
          "Account": "CH1-XXXX\\timadmin",
          "AccountType": "User",
          "Computer": "CH1-XXXX",
          "EventSourceName": "Microsoft-Windows-Security-Auditing",
          "Channel": "Security",
          "Task": 12544,
          "Level": "8",
          "EventID": 4624,
          "Activity": "4624 - An account was successfully logged on.",
          "SourceComputerId": "48fe7d27-1422-4005-abe8-2445b607f6f8",
          "EventOriginId": "73f10d80-1514-44d7-b13a-892fd7d6623a",
          "MG": "00000000-0000-0000-0000-000000000001",
          "TimeCollected": "2023-04-10T07:47:04.6777723Z",
          "ManagementGroupName": "AOI-81a662b5-8541-481b-977d-5d956616ac5e",
          "AuditsDiscarded": null,
          "AuthenticationLevel": null,
          "AuthenticationPackageName": "Negotiate",
          "AuthenticationService": null,
          "ElevatedToken": "%%1842",
          "ErrorCode": null,
          "ImpersonationLevel": "%%1833",
          "IpAddress": "1.1.1.1",
          "IpPort": "0",
          "KeyLength": 0,
          "LmPackageName": "-",
          "LogonGuid": "00000000-0000-0000-0000-000000000000",
          "LogonProcessName": "User32 ",
          "LogonType": 10,
          "LogonTypeName": "10 - RemoteInteractive",
          "Process": "svchost.exe",
          "ProcessId": "0x54c",
          "ProcessName": "C:\\Windows\\System32\\svchost.exe",
          "RestrictedAdminMode": "%%1843",
          "ServiceStartType": null,
          "SubjectAccount": "WORKGROUP\\CH1-XXXX$",
          "SubjectDomainName": "WORKGROUP",
          "SubjectLogonId": "0x3e7",
          "SubjectUserName": "CH1-XXXX$",
          "SubjectUserSid": "S-1-5-18",
          "TargetAccount": "CH1-XXXX\\timadmin",
          "TargetDomainName": "CH1-XXXX",
          "TargetLinkedLogonId": "0x0",
          "TargetLogonId": "0x1fc0ed",
          "TargetOutboundDomainName": "-",
          "TargetOutboundUserName": "-",
          "TargetUserName": "timadmin",
          "TargetUserSid": "S-1-5-21-3848374700-899364479-570268935-500",
          "TransmittedServices": "-",
          "VirtualAccount": "%%1843",
          "WorkstationName": "CH1-XXXX",
          "Type": "SecurityEvent",
          "_ResourceId": "/subscriptions/xxxx/resourcegroups/ch1-avsrg-swedencentral/providers/microsoft.compute/virtualmachines/ch1-XXXX"
        } 
    ]
}
```

#### STIX Translate results

```json
{
    "type": "bundle",
    "id": "bundle--e00f63cf-cf25-486a-a6fa-70605f36db2a",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "azure_log_analytics",
            "identity_class": "events",
            "created": "2022-04-11T16:11:11.878Z",
            "modified": "2022-04-11T16:11:11.878Z"
        },
        {
            "id": "observed-data--f2ff1bc1-2b92-4387-96ba-4e423c28d1e5",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2023-04-13T08:12:17.774Z",
            "modified": "2023-04-13T08:12:17.774Z",
            "objects": {
                "0": {
                    "type": "x-cloud-provider",
                    "tenant_id": "xxxx"
                },
                "1": {
                    "type": "x-ibm-finding",
                    "time_observed": "2023-04-10T07:47:01.9710164Z",
                    "name": "4624 - An account was successfully logged on.",
                    "alert_id": "73f10d80-1514-44d7-b13a-892fd7d6623a",
                    "src_ip_ref": "5",
                    "ioc_refs": [
                        "5"
                    ],
                    "dst_application_user_ref": "9",
                    "src_application_user_ref": "10",
                    "dst_device": "CH1-XXXX",
                    "finding_type": "event"
                },
                "2": {
                    "type": "x-oca-event",
                    "agent": "CH1-XXXX\\timadmin",
                    "x_provider_type": "User",
                    "host_ref": "3",
                    "provider": "Microsoft-Windows-Security-Auditing",
                    "module": "Security",
                    "x_task": 12544,
                    "code": 4624,
                    "action": "4624 - An account was successfully logged on.",
                    "created": "2023-04-10T07:47:04.6777723Z",
                    "ip_refs": [
                        "5"
                    ],
                    "user_ref": "10"
                },
                "3": {
                    "type": "x-oca-asset",
                    "hostname": "CH1-XXXX",
                    "device_id": "48fe7d27-1422-4005-abe8-2445b607f6f8"
                },
                "4": {
                    "type": "x-logon-info",
                    "authentication_package_name": "Negotiate",
                    "guid": "00000000-0000-0000-0000-000000000000",
                    "logon_process": "User32",
                    "logon_type": 10,
                    "logon_type_name": "10 - RemoteInteractive"
                },
                "5": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "6": {
                    "type": "process",
                    "pid": 1356,
                    "binary_ref": "8"
                },
                "7": {
                    "type": "directory",
                    "path": "C:\\Windows\\System32"
                },
                "8": {
                    "type": "file",
                    "name": "svchost.exe",
                    "parent_directory_ref": "7"
                },
                "9": {
                    "type": "user-account",
                    "display_name": "WORKGROUP\\CH1-XXXX$",
                    "x_domain_name": "WORKGROUP",
                    "x_login_id": 999,
                    "user_id": "CH1-XXXX$",
                    "account_login": "CH1-XXXX$",
                    "x_user_sid": "S-1-5-18"
                },
                "10": {
                    "type": "user-account",
                    "display_name": "CH1-XXXX\\timadmin",
                    "x_domain_name": "CH1-XXXX",
                    "x_login_id": 2081005,
                    "user_id": "timadmin",
                    "account_login": "timadmin",
                    "x_user_sid": "S-1-5-21-3848374700-899364479-570268935-500"
                },
                "11": {
                    "type": "x-cloud-resource",
                    "resource_id": "/subscriptions/xxxx/resourcegroups/ch1-avsrg-swedencentral/providers/microsoft.compute/virtualmachines/ch1-XXXX"
                }
            },
            "first_observed": "2023-04-13T08:12:17.774Z",
            "last_observed": "2023-04-13T08:12:17.774Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```
### Limitations
- process.pid for SecurityEvent table is of string type so this field in SecurityEvent & SecurityAlert tables will be set as string before sending it in query. For query, process.pid value can be set as integer or hexdecimal.
    However in STIX output it will be shown as integer.
- x-host-logon-session:session_id is converted to integer if hexadecimal value provided in query.  
- SecurityEvent table field "FileHash" isn't associated with algo like SHA-256, SHA-1 or MD5, so any STIX query for such file hash type will result in getting any of the FileHash types.
- While making query on entities fields, each entity is expanded first into a row(record). So 'AND' operator for different data source entities (corresponding to different STIX Cyber Observable (SCO) properties) won't give desired results.
        For example; network-traffic.dst_port == 10 AND ipv4-addr == '1.1.1.1'- (SecurityAlert | mv-expand parsed_entities = parse_json(Entities) | where (parsed_entities.DestinationPort == 3389 and parsed_entities.Address=='49.37.223.69')
        and (TimeGenerated between (datetime(2023-03-15T16:43:26.000Z) .. datetime(2023-04-25T16:43:26.003Z))) | summarize arg_max(TimeGenerated, *) by TimeGenerated, SystemAlertId) won't work as these belong to two different entities (two different rows on expanding).
- Query having 'NOT' operator applied on an entities field having multiple entities of that type won't work.

### References
- [Microsoft security alert schema reference](https://learn.microsoft.com/en-us/azure/sentinel/security-alert-schema)
- [Microsoft entity types reference](https://learn.microsoft.com/en-us/azure/sentinel/entities-reference#user-account)
- [SecurityIncident](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/securityincident)
- [SecurityEvent](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/securityevent)
