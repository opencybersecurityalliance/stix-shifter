##### Updated on 05/15/23
## Microsoft Defender for Endpoint
### Results STIX Domain Objects
* Identity
* Observed Data
<br>
### Supported STIX Operators
*Comparison AND/OR operators are inside the observation while observation AND/OR operators are between observations (square brackets).*

| STIX Operator | Data Source Operator |
|--|--|
| AND (Comparision) | and |
| OR (Comparision) | or |
| = | == |
| != | != |
| LIKE | contains |
| MATCHES | matches |
| > | > |
| >= | >= |
| < | < |
| <= | <= |
| IN | in~ |
| OR (Observation) | or |
| AND (Observation) | or |
| <br> | |
### Searchable STIX objects and properties
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **ipv4-addr**:value | DeviceNetworkEvents.LocalIP, DeviceNetworkEvents.RemoteIP, DeviceEvents.RemoteIP, DeviceEvents.LocalIP |
| **ipv6-addr**:value | DeviceNetworkEvents.LocalIP, DeviceNetworkEvents.RemoteIP, DeviceEvents.RemoteIP, DeviceEvents.LocalIP |
| **network-traffic**:src_port | DeviceNetworkEvents.LocalPort, DeviceEvents.LocalPort |
| **network-traffic**:dst_port | DeviceNetworkEvents.RemotePort, DeviceEvents.RemotePort |
| **network-traffic**:protocols[*] | DeviceNetworkEvents.Protocol |
| **network-traffic**:src_ref.value | DeviceNetworkEvents.LocalIP, DeviceNetworkInfo.MacAddress, DeviceEvents.LocalIP |
| **network-traffic**:dst_ref.value | DeviceNetworkEvents.RemoteIP, DeviceEvents.RemoteIP |
| **url**:value | DeviceNetworkEvents.RemoteUrl, DeviceEvents.RemoteUrl, DeviceFileEvents.FileOriginUrl, DeviceFileEvents.FileOriginReferrerUrl |
| **domain-name**:value | DeviceNetworkEvents.RemoteUrl, DeviceEvents.RemoteUrl |
| **file**:name | DeviceFileEvents.FileName, DeviceFileEvents.InitiatingProcessFileName, DeviceFileEvents.InitiatingProcessParentFileName, DeviceProcessEvents.FileName, DeviceProcessEvents.InitiatingProcessFileName, DeviceProcessEvents.InitiatingProcessParentFileName, DeviceNetworkEvents.InitiatingProcessFileName, DeviceNetworkEvents.InitiatingProcessParentFileName, DeviceRegistryEvents.InitiatingProcessFileName, DeviceRegistryEvents.InitiatingProcessParentFileName, DeviceEvents.FileName, DeviceEvents.InitiatingProcessFileName, DeviceEvents.InitiatingProcessParentFileName, DeviceImageLoadEvents.FileName, DeviceImageLoadEvents.InitiatingProcessFileName, DeviceImageLoadEvents.InitiatingProcessParentFileName |
| **file**:hashes.'SHA-1' | DeviceFileEvents.SHA1, DeviceFileEvents.InitiatingProcessSHA1, DeviceProcessEvents.SHA1, DeviceProcessEvents.InitiatingProcessSHA1, DeviceNetworkEvents.InitiatingProcessSHA1, DeviceRegistryEvents.InitiatingProcessSHA1, DeviceEvents.SHA1, DeviceEvents.InitiatingProcessSHA1, DeviceImageLoadEvents.SHA1, DeviceImageLoadEvents.InitiatingProcessSHA1 |
| **file**:hashes.'SHA-256' | DeviceFileEvents.SHA256, DeviceFileEvents.InitiatingProcessSHA256, DeviceProcessEvents.SHA256, DeviceProcessEvents.InitiatingProcessSHA256, DeviceNetworkEvents.InitiatingProcessSHA256, DeviceRegistryEvents.InitiatingProcessSHA256, DeviceEvents.SHA256, DeviceEvents.InitiatingProcessSHA256, DeviceImageLoadEvents.SHA256, DeviceImageLoadEvents.InitiatingProcessSHA256 |
| **file**:hashes.MD5 | DeviceFileEvents.MD5, DeviceFileEvents.InitiatingProcessMD5, DeviceProcessEvents.MD5, DeviceProcessEvents.InitiatingProcessMD5, DeviceNetworkEvents.InitiatingProcessMD5, DeviceRegistryEvents.InitiatingProcessMD5, DeviceEvents.MD5, DeviceEvents.InitiatingProcessMD5, DeviceImageLoadEvents.MD5, DeviceImageLoadEvents.InitiatingProcessMD5 |
| **file**:parent_directory_ref.path | DeviceFileEvents.FolderPath, DeviceFileEvents.InitiatingProcessFolderPath, DeviceProcessEvents.FolderPath, DeviceProcessEvents.InitiatingProcessFolderPath, DeviceNetworkEvents.InitiatingProcessFolderPath, DeviceRegistryEvents.InitiatingProcessFolderPath, DeviceEvents.FolderPath, DeviceEvents.InitiatingProcessFolderPath, DeviceImageLoadEvents.FolderPath, DeviceImageLoadEvents.InitiatingProcessFolderPath |
| **process**:name | DeviceProcessEvents.FileName, DeviceEvents.FileName, DeviceProcessEvents.InitiatingProcessFileName, DeviceEvents.InitiatingProcessFileName, DeviceFileEvents.InitiatingProcessFileName, DeviceNetworkEvents.InitiatingProcessFileName, DeviceRegistryEvents.InitiatingProcessFileName, DeviceImageLoadEvents.InitiatingProcessFileName |
| **process**:command_line | DeviceProcessEvents.ProcessCommandLine, DeviceProcessEvents.InitiatingProcessCommandLine, DeviceEvents.ProcessCommandLine, DeviceEvents.InitiatingProcessCommandLine, DeviceFileEvents.InitiatingProcessCommandLine, DeviceNetworkEvents.InitiatingProcessCommandLine, DeviceRegistryEvents.InitiatingProcessCommandLine, DeviceImageLoadEvents.InitiatingProcessCommandLine |
| **process**:pid | DeviceProcessEvents.ProcessId, DeviceEvents.ProcessId, DeviceProcessEvents.InitiatingProcessId, DeviceEvents.InitiatingProcessId, DeviceProcessEvents.InitiatingProcessId, DeviceNetworkEvents.InitiatingProcessId, DeviceRegistryEvents.InitiatingProcessId, DeviceFileEvents.InitiatingProcessId, DeviceImageLoadEvents.InitiatingProcessId |
| **process**:created | DeviceProcessEvents.ProcessCreationTime, DeviceEvents.ProcessCreationTime, DeviceNetworkEvents.InitiatingProcessCreationTime, DeviceRegistryEvents.InitiatingProcessCreationTime, DeviceFileEvents.InitiatingProcessCreationTime, DeviceImageLoadEvents.InitiatingProcessCreationTime |
| **process**:parent_ref.name | DeviceProcessEvents.InitiatingProcessFileName, DeviceEvents.InitiatingProcessFileName, DeviceFileEvents.InitiatingProcessParentFileName, DeviceNetworkEvents.InitiatingProcessParentFileName, DeviceRegistryEvents.InitiatingProcessParentFileName, DeviceImageLoadEvents.InitiatingProcessParentFileName |
| **process**:parent_ref.pid | DeviceProcessEvents.InitiatingProcessId, DeviceNetworkEvents.InitiatingProcessId, DeviceRegistryEvents.InitiatingProcessParentId, DeviceFileEvents.InitiatingProcessParentId, DeviceEvents.InitiatingProcessParentId, DeviceImageLoadEvents.InitiatingProcessParentId |
| **process**:parent_ref.created | DeviceProcessEvents.InitiatingProcessCreationTime, DeviceEvents.InitiatingProcessCreationTime, DeviceNetworkEvents.InitiatingProcessParentCreationTime, DeviceRegistryEvents.InitiatingProcessParentCreationTime, DeviceFileEvents.InitiatingProcessParentCreationTime, DeviceImageLoadEvents.InitiatingProcessParentCreationTime |
| **process**:parent_ref.parent_ref.name | DeviceProcessEvents.InitiatingProcessParentFileName, DeviceEvents.InitiatingProcessParentFileName |
| **process**:parent_ref.parent_ref.pid | DeviceProcessEvents.InitiatingProcessParentId, DeviceNetworkEvents.InitiatingProcessParentId |
| **process**:parent_ref.parent_ref.created | DeviceProcessEvents.InitiatingProcessParentCreationTime, DeviceEvents.InitiatingProcessParentCreationTime |
| **process**:creator_user_ref.user_id | DeviceProcessEvents.AccountName, DeviceEvents.AccountName, DeviceNetworkEvents.InitiatingProcessAccountName, DeviceRegistryEvents.InitiatingProcessAccountName, DeviceFileEvents.InitiatingProcessAccountName, DeviceImageLoadEvents.InitiatingProcessAccountName |
| **process**:creator_user_ref.account_login | DeviceProcessEvents.AccountUpn, DeviceEvents.AccountUpn, DeviceNetworkEvents.InitiatingProcessAccountUpn, DeviceRegistryEvents.InitiatingProcessAccountUpn, DeviceFileEvents.InitiatingProcessAccountUpn, DeviceImageLoadEvents.InitiatingProcessAccountUpn |
| **process**:parent_ref.creator_user_ref.user_id | DeviceProcessEvents.InitiatingProcessAccountName, DeviceEvents.InitiatingProcessAccountName |
| **process**:parent_ref.creator_user_ref.account_login | DeviceProcessEvents.InitiatingProcessAccountUpn, DeviceEvents.InitiatingProcessAccountUpn |
| **process**:binary_ref.hashes.'SHA-1' | DeviceProcessEvents.SHA1, DeviceEvents.SHA1, DeviceFileEvents.InitiatingProcessSHA1, DeviceNetworkEvents.InitiatingProcessSHA1, DeviceRegistryEvents.InitiatingProcessSHA1, DeviceImageLoadEvents.InitiatingProcessSHA1 |
| **process**:binary_ref.hashes.'SHA-256' | DeviceProcessEvents.SHA256, DeviceEvents.SHA256, DeviceFileEvents.InitiatingProcessSHA256, DeviceNetworkEvents.InitiatingProcessSHA256, DeviceRegistryEvents.InitiatingProcessSHA256, DeviceImageLoadEvents.InitiatingProcessSHA256 |
| **process**:binary_ref.hashes.MD5 | DeviceProcessEvents.MD5, DeviceEvents.MD5, DeviceFileEvents.InitiatingProcessMD5, DeviceNetworkEvents.InitiatingProcessMD5, DeviceRegistryEvents.InitiatingProcessMD5, DeviceImageLoadEvents.InitiatingProcessMD5 |
| **process**:binary_ref.parent_directory_ref.path | DeviceProcessEvents.FolderPath, DeviceEvents.FolderPath, DeviceNetworkEvents.InitiatingProcessFolderPath, DeviceRegistryEvents.InitiatingProcessFolderPath, DeviceFileEvents.InitiatingProcessFolderPath, DeviceImageLoadEvents.InitiatingProcessFolderPath |
| **process**:parent_ref.binary_ref.hashes.'SHA-1' | DeviceProcessEvents.InitiatingProcessSHA1, DeviceEvents.InitiatingProcessSHA1 |
| **process**:parent_ref.binary_ref.hashes.'SHA-256' | DeviceProcessEvents.InitiatingProcessSHA256, DeviceEvents.InitiatingProcessSHA256 |
| **process**:parent_ref.binary_ref.hashes.MD5 | DeviceProcessEvents.InitiatingProcessMD5, DeviceEvents.InitiatingProcessMD5 |
| **process**:parent_ref.binary_ref.parent_directory_ref.path | DeviceProcessEvents.InitiatingProcessFolderPath, DeviceEvents.InitiatingProcessFolderPath |
| **process**:child_refs.binary_ref.hashes.MD5 | DeviceProcessEvents.MD5 |
| **process**:child_refs.binary_ref.hashes.'SHA-256' | DeviceProcessEvents.SHA256 |
| **process**:child_refs.binary_ref.hashes.'SHA-1' | DeviceProcessEvents.SHA1 |
| **process**:child_refs.binary_ref.parent_directory_ref.path | DeviceProcessEvents.FolderPath |
| **process**:child_refs.creator_user_ref.account_login | DeviceProcessEvents.AccountName |
| **process**:child_refs.pid | DeviceProcessEvents.ProcessId |
| **user-account**:user_id | DeviceProcessEvents.AccountName, DeviceFileEvents.RequestAccountName, DeviceEvents.AccountName, DeviceProcessEvents.InitiatingProcessAccountName, DeviceNetworkEvents.InitiatingProcessAccountName, DeviceRegistryEvents.InitiatingProcessAccountName, DeviceFileEvents.InitiatingProcessAccountName, DeviceEvents.InitiatingProcessAccountName, DeviceImageLoadEvents.InitiatingProcessAccountName |
| **user-account**:account_login | DeviceProcessEvents.AccountUpn, DeviceEvents.AccountUpn, DeviceProcessEvents.InitiatingProcessAccountUpn, DeviceNetworkEvents.InitiatingProcessAccountUpn, DeviceRegistryEvents.InitiatingProcessAccountUpn, DeviceFileEvents.InitiatingProcessAccountUpn, DeviceEvents.InitiatingProcessAccountUpn, DeviceImageLoadEvents.InitiatingProcessAccountUpn |
| **windows-registry-key**:key | DeviceRegistryEvents.RegistryKey, DeviceEvents.RegistryKey |
| **windows-registry-key**:values[*] | DeviceRegistryEvents.RegistryValueName, DeviceEvents.RegistryValueName |
| **mac-addr**:value | DeviceNetworkInfo.MacAddress |
| **directory**:path | DeviceFileEvents.FolderPath, DeviceFileEvents.InitiatingProcessFolderPath, DeviceProcessEvents.FolderPath, DeviceProcessEvents.InitiatingProcessFolderPath, DeviceEvents.FolderPath, DeviceEvents.InitiatingProcessFolderPath, DeviceNetworkEvents.InitiatingProcessFolderPath, DeviceRegistryEvents.InitiatingProcessFolderPath, DeviceImageLoadEvents.FolderPath, DeviceImageLoadEvents.InitiatingProcessFolderPath |
| **x-oca-asset**:device_id | DeviceFileEvents.DeviceId, DeviceProcessEvents.DeviceId, DeviceNetworkEvents.DeviceId, DeviceRegistryEvents.DeviceId, DeviceEvents.DeviceId, DeviceImageLoadEvents.DeviceId, DeviceLogonEvents.DeviceId |
| **x-oca-asset**:hostname | DeviceFileEvents.DeviceName, DeviceProcessEvents.DeviceName, DeviceNetworkEvents.DeviceName, DeviceRegistryEvents.DeviceName, DeviceEvents.DeviceName, DeviceImageLoadEvents.DeviceName, DeviceLogonEvents.DeviceName |
| **x-oca-asset**:ip_refs[*].value | DeviceNetworkEvents.LocalIP |
| **x-oca-asset**:os.name | DeviceInfo.OSPlatform |
| **x-oca-asset**:os.platform | DeviceInfo.OSPlatform |
| **x-oca-event**:action | DeviceProcessEvents.ActionType, DeviceEvents.ActionType, DeviceNetworkEvents.ActionType, DeviceRegistryEvents.ActionType, DeviceFileEvents.ActionType, DeviceImageLoadEvents.ActionType |
| **x-oca-event**:process_ref.pid | DeviceProcessEvents.ProcessId, DeviceEvents.ProcessId, DeviceNetworkEvents.InitiatingProcessId, DeviceRegistryEvents.InitiatingProcessId, DeviceFileEvents.InitiatingProcessId, DeviceImageLoadEvents.InitiatingProcessId |
| **x-oca-event**:process_ref.name | DeviceProcessEvents.FileName, DeviceEvents.FileName, DeviceNetworkEvents.InitiatingProcessFileName, DeviceRegistryEvents.InitiatingProcessFileName, DeviceFileEvents.InitiatingProcessFileName, DeviceImageLoadEvents.InitiatingProcessFileName |
| **x-oca-event**:process_ref.binary_ref.name | DeviceProcessEvents.FileName, DeviceEvents.FileName, DeviceNetworkEvents.InitiatingProcessFileName, DeviceRegistryEvents.InitiatingProcessFileName, DeviceFileEvents.InitiatingProcessFileName, DeviceImageLoadEvents.InitiatingProcessFileName |
| **x-oca-event**:process_ref.creator_user_ref.account_login | DeviceProcessEvents.AccountUpn, DeviceEvents.AccountUpn, DeviceNetworkEvents.InitiatingProcessAccountUpn, DeviceRegistryEvents.InitiatingProcessAccountUpn, DeviceFileEvents.InitiatingProcessAccountUpn, DeviceImageLoadEvents.InitiatingProcessAccountUpn |
| **x-oca-event**:process_ref.creator_user_ref.user_id | DeviceProcessEvents.AccountName, DeviceEvents.AccountName, DeviceNetworkEvents.InitiatingProcessAccountName, DeviceRegistryEvents.InitiatingProcessAccountName, DeviceFileEvents.InitiatingProcessAccountName, DeviceImageLoadEvents.InitiatingProcessAccountName |
| **x-oca-event**:process_ref.command_line | DeviceProcessEvents.ProcessCommandLine, DeviceEvents.ProcessCommandLine, DeviceNetworkEvents.InitiatingProcessCommandLine, DeviceRegistryEvents.InitiatingProcessCommandLine, DeviceFileEvents.InitiatingProcessCommandLine, DeviceImageLoadEvents.InitiatingProcessCommandLine |
| **x-oca-event**:process_ref.parent_ref.name | DeviceProcessEvents.InitiatingProcessFileName, DeviceEvents.InitiatingProcessFileName, DeviceNetworkEvents.InitiatingProcessParentFileName, DeviceRegistryEvents.InitiatingProcessParentFileName, DeviceFileEvents.InitiatingProcessParentFileName, DeviceImageLoadEvents.InitiatingProcessParentFileName |
| **x-oca-event**:process_ref.parent_ref.pid | DeviceProcessEvents.InitiatingProcessId, DeviceEvents.InitiatingProcessId, DeviceNetworkEvents.InitiatingProcessParentId, DeviceRegistryEvents.InitiatingProcessParentId, DeviceFileEvents.InitiatingProcessParentId, DeviceImageLoadEvents.InitiatingProcessParentId |
| **x-oca-event**:process_ref.parent_ref.command_line | DeviceProcessEvents.InitiatingProcessCommandLine, DeviceEvents.InitiatingProcessCommandLine |
| **x-oca-event**:process_ref.binary_ref.hashes.'SHA-256' | DeviceProcessEvents.SHA256, DeviceEvents.SHA256, DeviceNetworkEvents.InitiatingProcessSHA256, DeviceRegistryEvents.InitiatingProcessSHA256, DeviceFileEvents.InitiatingProcessSHA256, DeviceImageLoadEvents.InitiatingProcessSHA256 |
| **x-oca-event**:process_ref.binary_ref.hashes.MD5 | DeviceProcessEvents.MD5, DeviceEvents.MD5, DeviceNetworkEvents.InitiatingProcessMD5, DeviceRegistryEvents.InitiatingProcessMD5, DeviceFileEvents.InitiatingProcessMD5, DeviceImageLoadEvents.InitiatingProcessMD5 |
| **x-oca-event**:process_ref.binary_ref.hashes.'SHA-1' | DeviceProcessEvents.SHA1, DeviceEvents.SHA1, DeviceNetworkEvents.InitiatingProcessSHA1, DeviceRegistryEvents.InitiatingProcessSHA1, DeviceFileEvents.InitiatingProcessSHA1, DeviceImageLoadEvents.InitiatingProcessSHA1 |
| **x-oca-event**:parent_process_ref.name | DeviceProcessEvents.InitiatingProcessFileName, DeviceEvents.InitiatingProcessFileName, DeviceNetworkEvents.InitiatingProcessParentFileName, DeviceRegistryEvents.InitiatingProcessParentFileName, DeviceFileEvents.InitiatingProcessParentFileName, DeviceImageLoadEvents.InitiatingProcessParentFileName |
| **x-oca-event**:parent_process_ref.pid | DeviceProcessEvents.InitiatingProcessId, DeviceEvents.InitiatingProcessId, DeviceNetworkEvents.InitiatingProcessParentId, DeviceRegistryEvents.InitiatingProcessParentId, DeviceFileEvents.InitiatingProcessParentId, DeviceImageLoadEvents.InitiatingProcessParentId |
| **x-oca-event**:domain_ref.value | DeviceNetworkEvents.RemoteUrl, DeviceEvents.RemoteUrl |
| **x-oca-event**:url_ref.value | DeviceNetworkEvents.RemoteUrl, DeviceEvents.RemoteUrl, DeviceEvents.FileOriginUrl, DeviceFileEvents.FileOriginUrl, DeviceFileEvents.FileOriginReferrerUrl |
| **x-oca-event**:file_ref.name | DeviceFileEvents.FileName, DeviceImageLoadEvents.FileName |
| **x-oca-event**:registry_ref.key | DeviceRegistryEvents.RegistryKey |
| **x-oca-event**:host_ref.hostname | DeviceFileEvents.DeviceName, DeviceProcessEvents.DeviceName, DeviceNetworkEvents.DeviceName, DeviceRegistryEvents.DeviceName, DeviceEvents.DeviceName, DeviceImageLoadEvents.DeviceName, DeviceLogonEvents.DeviceName |
| **x-oca-event**:host_ref.device_id | DeviceFileEvents.DeviceId, DeviceProcessEvents.DeviceId, DeviceNetworkEvents.DeviceId, DeviceRegistryEvents.DeviceId, DeviceEvents.DeviceId, DeviceImageLoadEvents.DeviceId, DeviceLogonEvents.DeviceId |
| **x-ibm-finding**:alert_id | DeviceAlertEvents.AlertId |
| **x-ibm-finding**:name | DeviceAlertEvents.Title |
| **x-ibm-finding**:time_observed | DeviceAlertEvents.Timestamp |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| artifact | payload_bin | original_ref |
| <br> | | |
| directory | path | FileName |
| directory | path | InitiatingProcessFileName |
| directory | path | InitiatingProcessParentFileName |
| directory | path | InitiatingProcessFolderPath |
| directory | path | FolderPath |
| <br> | | |
| domain-name | value | RemoteUrl |
| domain-name | value | FileOriginReferrerUrl |
| domain-name | value | FileOriginUrl |
| <br> | | |
| external-reference | url | event_link |
| <br> | | |
| file | name | FileName |
| file | parent_directory_ref | FileName |
| file | hashes.SHA-1 | SHA1 |
| file | hashes.SHA-256 | SHA256 |
| file | hashes.MD5 | MD5 |
| file | hashes.SHA-1 | InitiatingProcessSHA1 |
| file | hashes.SHA-256 | InitiatingProcessSHA256 |
| file | hashes.MD5 | InitiatingProcessMD5 |
| file | name | InitiatingProcessFileName |
| file | parent_directory_ref | InitiatingProcessFileName |
| file | name | InitiatingProcessParentFileName |
| file | parent_directory_ref | InitiatingProcessParentFileName |
| file | parent_directory_ref | InitiatingProcessFolderPath |
| file | parent_directory_ref | FolderPath |
| <br> | | |
| ipv4-addr | value | RemoteIP |
| ipv4-addr | value | LocalIP |
| ipv4-addr | resolves_to_refs | MacAddress |
| ipv4-addr | value | PublicIP |
| ipv4-addr | value | IPAddresses |
| ipv4-addr | value | FileOriginIP |
| ipv4-addr | value | IpAddresses |
| <br> | | |
| ipv6-addr | value | RemoteIP |
| ipv6-addr | value | LocalIP |
| ipv6-addr | value | IPAddresses |
| ipv6-addr | value | FileOriginIP |
| ipv6-addr | value | IpAddresses |
| <br> | | |
| mac-addr | value | MacAddress |
| mac-addr | value | MacAddressSet |
| <br> | | |
| network-traffic | dst_ref | RemoteIP |
| network-traffic | src_ref | LocalIP |
| network-traffic | src_port | LocalPort |
| network-traffic | dst_port | RemotePort |
| network-traffic | protocols | Protocol |
| network-traffic | src_ref | MacAddress |
| network-traffic | dst_ref | FileOriginIP |
| <br> | | |
| process | binary_ref | InitiatingProcessSHA1 |
| process | binary_ref | InitiatingProcessSHA256 |
| process | binary_ref | InitiatingProcessMD5 |
| process | name | InitiatingProcessFileName |
| process | binary_ref | InitiatingProcessFileName |
| process | name | InitiatingProcessParentFileName |
| process | parent_ref | InitiatingProcessParentFileName |
| process | binary_ref | InitiatingProcessParentFileName |
| process | pid | InitiatingProcessId |
| process | pid | InitiatingProcessParentId |
| process | parent_ref | InitiatingProcessParentId |
| process | command_line | InitiatingProcessCommandLine |
| process | created | InitiatingProcessCreationTime |
| process | created | InitiatingProcessParentCreationTime |
| process | parent_ref | InitiatingProcessParentCreationTime |
| process | creator_user_ref | InitiatingProcessAccountName |
| process | creator_user_ref | InitiatingProcessAccountUpn |
| process | binary_ref | InitiatingProcessFolderPath |
| process | name | FileName |
| process | binary_ref | FileName |
| process | child_refs | FileName |
| process | pid | ProcessId |
| process | child_refs | ProcessId |
| process | command_line | ProcessCommandLine |
| process | child_refs | ProcessCommandLine |
| process | created | ProcessCreationTime |
| process | parent_ref | InitiatingProcessFileName |
| process | parent_ref | InitiatingProcessId |
| process | creator_user_ref | AccountName |
| process | creator_user_ref | AccountUpn |
| <br> | | |
| url | value | RemoteUrl |
| url | value | FileOriginReferrerUrl |
| url | value | FileOriginUrl |
| <br> | | |
| user-account | user_id | InitiatingProcessAccountName |
| user-account | account_login | InitiatingProcessAccountUpn |
| user-account | user_id | AccountName |
| user-account | account_login | AccountUpn |
| <br> | | |
| windows-registry-key | key | RegistryKey |
| windows-registry-key | values | RegistryValues |
| <br> | | |
| x-ibm-finding | alert_id | AlertId |
| x-ibm-finding | severity | Severity |
| x-ibm-finding | ttp_tagging_refs | AttackTechniques |
| x-ibm-finding | ttp_tagging_refs | Category |
| x-ibm-finding | name | Title |
| x-ibm-finding | finding_type | Title |
| x-ibm-finding | ioc_refs | RemoteUrl |
| x-ibm-finding | ioc_refs | RemoteIP |
| x-ibm-finding | time_observed | Timestamp |
| <br> | | |
| x-ibm-ttp-tagging | extensions.mitre-attack-ext.technique_name | AttackTechniques |
| x-ibm-ttp-tagging | kill_chain_phases.phase_name | Category |
| <br> | | |
| x-json-alert | data | Alerts |
| <br> | | |
| x-msatp | ReportId | ReportId |
| x-msatp | Table | TableName |
| x-msatp | AdditionalFields | AdditionalFields |
| <br> | | |
| x-oca-asset | hostname | DeviceName |
| x-oca-asset | device_id | DeviceId |
| x-oca-asset | ip_refs | LocalIP |
| x-oca-asset | ip_refs | PublicIP |
| x-oca-asset | os_name | OSPlatform |
| x-oca-asset | architecture | OSArchitecture |
| x-oca-asset | os_version | OSVersion |
| x-oca-asset | mac_refs | MacAddressSet |
| x-oca-asset | ip_refs | IPAddresses |
| x-oca-asset | ip_refs | IpAddresses |
| x-oca-asset | mac_refs | MacAddress |
| <br> | | |
| x-oca-event | finding_refs | AlertId |
| x-oca-event | action | Title |
| x-oca-event | category | Title |
| x-oca-event | domain_ref | RemoteUrl |
| x-oca-event | url_ref | RemoteUrl |
| x-oca-event | network_ref | RemoteIP |
| x-oca-event | ip_refs | RemoteIP |
| x-oca-event | created | Timestamp |
| x-oca-event | file_ref | FileName |
| x-oca-event | host_ref | DeviceName |
| x-oca-event | host_ref | DeviceId |
| x-oca-event | original_ref | original_ref |
| x-oca-event | external_ref | event_link |
| x-oca-event | provider | provider |
| x-oca-event | network_ref | LocalIP |
| x-oca-event | network_ref | LocalPort |
| x-oca-event | network_ref | RemotePort |
| x-oca-event | process_ref | InitiatingProcessSHA1 |
| x-oca-event | process_ref | InitiatingProcessSHA256 |
| x-oca-event | process_ref | InitiatingProcessMD5 |
| x-oca-event | process_ref | InitiatingProcessFileName |
| x-oca-event | process_ref | InitiatingProcessId |
| x-oca-event | process_ref | InitiatingProcessCommandLine |
| x-oca-event | network_ref | MacAddress |
| x-oca-event | action | ActionType |
| x-oca-event | process_ref | FileName |
| x-oca-event | process_ref | ProcessId |
| x-oca-event | user_ref | AccountName |
| x-oca-event | user_ref | AccountUpn |
| x-oca-event | url_ref | FileOriginReferrerUrl |
| x-oca-event | domain_ref | FileOriginReferrerUrl |
| x-oca-event | network_ref | FileOriginIP |
| x-oca-event | ips_ref | FileOriginIP |
| x-oca-event | parent_process_ref | InitiatingProcessParentId |
| x-oca-event | user_ref | InitiatingProcessAccountName |
| x-oca-event | registry_ref | RegistryKey |
| x-oca-event | url_ref | FileOriginUrl |
| x-oca-event | domain_ref | FileOriginUrl |
| x-oca-event | missingChildShouldMapInitiatingPid | missingChildShouldMapInitiatingPid |
| <br> | | |
