##### Updated on 02/27/23
## Microsoft Defender for Endpoint
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
| **ipv4-addr**:value | DeviceNetworkEvents.LocalIP, DeviceNetworkEvents.RemoteIP |
| **ipv6-addr**:value | DeviceNetworkEvents.LocalIP, DeviceNetworkEvents.RemoteIP |
| **network-traffic**:src_port | DeviceNetworkEvents.LocalPort |
| **network-traffic**:dst_port | DeviceNetworkEvents.RemotePort |
| **network-traffic**:protocols[*] | DeviceNetworkEvents.Protocol |
| **network-traffic**:src_ref.value | DeviceNetworkEvents.LocalIP, DeviceNetworkInfo.MacAddress |
| **network-traffic**:dst_ref.value | DeviceNetworkEvents.RemoteIP |
| **url**:value | DeviceNetworkEvents.RemoteUrl |
| **domain-name**:value | DeviceFileEvents.DeviceName, DeviceProcessEvents.DeviceName, DeviceNetworkEvents.DeviceName, DeviceRegistryEvents.DeviceName, DeviceEvents.DeviceName, DeviceInfo.DeviceName, DeviceAlertEvents.DeviceName, DeviceImageLoadEvents.DeviceName, DeviceLogonEvents.DeviceName, DeviceNetworkInfo.DeviceName |
| **file**:name | DeviceFileEvents.FileName, DeviceFileEvents.InitiatingProcessFileName, DeviceFileEvents.InitiatingProcessParentFileName, DeviceProcessEvents.FileName, DeviceProcessEvents.InitiatingProcessFileName, DeviceProcessEvents.InitiatingProcessParentFileName, DeviceNetworkEvents.InitiatingProcessFileName, DeviceNetworkEvents.InitiatingProcessParentFileName, DeviceRegistryEvents.InitiatingProcessFileName, DeviceRegistryEvents.InitiatingProcessParentFileName |
| **file**:hashes.'SHA-1' | DeviceFileEvents.SHA1, DeviceFileEvents.InitiatingProcessSHA1, DeviceProcessEvents.SHA1, DeviceProcessEvents.InitiatingProcessSHA1, DeviceNetworkEvents.InitiatingProcessSHA1, DeviceRegistryEvents.InitiatingProcessSHA1 |
| **file**:hashes.'SHA-256' | DeviceFileEvents.SHA256, DeviceFileEvents.InitiatingProcessSHA256, DeviceProcessEvents.SHA256, DeviceProcessEvents.InitiatingProcessSHA256, DeviceNetworkEvents.InitiatingProcessSHA256, DeviceRegistryEvents.InitiatingProcessSHA256 |
| **file**:hashes.MD5 | DeviceFileEvents.MD5, DeviceFileEvents.InitiatingProcessMD5, DeviceProcessEvents.MD5, DeviceProcessEvents.InitiatingProcessMD5, DeviceNetworkEvents.InitiatingProcessMD5, DeviceRegistryEvents.InitiatingProcessMD5 |
| **file**:parent_directory_ref.path | DeviceFileEvents.FolderPath, DeviceFileEvents.InitiatingProcessFolderPath, DeviceProcessEvents.FolderPath, DeviceProcessEvents.InitiatingProcessFolderPath, DeviceNetworkEvents.InitiatingProcessFolderPath, DeviceRegistryEvents.InitiatingProcessFolderPath |
| **process**:name | DeviceProcessEvents.FileName, DeviceProcessEvents.InitiatingProcessFileName, DeviceProcessEvents.InitiatingProcessParentFileName, DeviceNetworkEvents.InitiatingProcessFileName, DeviceNetworkEvents.InitiatingProcessParentFileName, DeviceRegistryEvents.InitiatingProcessFileName, DeviceRegistryEvents.InitiatingProcessParentFileName |
| **process**:parent_ref.name | DeviceProcessEvents.InitiatingProcessFileName, DeviceProcessEvents.InitiatingProcessFileName, DeviceNetworkEvents.InitiatingProcessFileName, DeviceRegistryEvents.InitiatingProcessFileName, DeviceProcessEvents.InitiatingProcessParentFileName, DeviceProcessEvents.InitiatingProcessParentFileName, DeviceNetworkEvents.InitiatingProcessParentFileName, DeviceRegistryEvents.InitiatingProcessParentFileName |
| **process**:command_line | DeviceProcessEvents.ProcessCommandLine, DeviceProcessEvents.InitiatingProcessCommandLine, DeviceNetworkEvents.InitiatingProcessCommandLine, DeviceRegistryEvents.InitiatingProcessCommandLine |
| **process**:pid | DeviceProcessEvents.ProcessId, DeviceProcessEvents.InitiatingProcessId, DeviceProcessEvents.InitiatingProcessParentId, DeviceNetworkEvents.InitiatingProcessId, DeviceNetworkEvents.InitiatingProcessParentId, DeviceRegistryEvents.InitiatingProcessId, DeviceRegistryEvents.InitiatingProcessParentId, DeviceFileEvents.InitiatingProcessId, DeviceFileEvents.InitiatingProcessParentId |
| **process**:parent_ref.pid | DeviceProcessEvents.InitiatingProcessId, DeviceNetworkEvents.InitiatingProcessId, DeviceRegistryEvents.InitiatingProcessId, DeviceFileEvents.InitiatingProcessId, DeviceProcessEvents.InitiatingProcessParentId, DeviceNetworkEvents.InitiatingProcessParentId, DeviceRegistryEvents.InitiatingProcessParentId, DeviceFileEvents.InitiatingProcessParentId |
| **process**:child_refs.pid | DeviceProcessEvents.ProcessId, DeviceProcessEvents.InitiatingProcessId, DeviceNetworkEvents.InitiatingProcessId, DeviceRegistryEvents.InitiatingProcessId, DeviceFileEvents.InitiatingProcessId |
| **process**:creator_user_ref.user_id | DeviceProcessEvents.AccountSid, DeviceProcessEvents.InitiatingProcessAccountSid |
| **process**:child_refs.creator_user_ref.account_login | DeviceProcessEvents.AccountName |
| **process**:creator_user_ref.account_login | DeviceProcessEvents.InitiatingProcessAccountName |
| **process**:binary_ref.hashes.'SHA-1' | DeviceFileEvents.SHA1, DeviceFileEvents.InitiatingProcessSHA1, DeviceProcessEvents.SHA1, DeviceProcessEvents.InitiatingProcessSHA1, DeviceNetworkEvents.InitiatingProcessSHA1, DeviceRegistryEvents.InitiatingProcessSHA1 |
| **process**:binary_ref.hashes.'SHA-256' | DeviceFileEvents.SHA256, DeviceFileEvents.InitiatingProcessSHA256, DeviceProcessEvents.SHA256, DeviceProcessEvents.InitiatingProcessSHA256, DeviceNetworkEvents.InitiatingProcessSHA256, DeviceRegistryEvents.InitiatingProcessSHA256 |
| **process**:child_refs.binary_ref.hashes.MD5 | DeviceProcessEvents.MD5 |
| **process**:child_refs.binary_ref.hashes.'SHA-256' | DeviceProcessEvents.SHA256 |
| **process**:child_refs.binary_ref.hashes.'SHA-1' | DeviceProcessEvents.SHA1 |
| **process**:binary_ref.hashes.MD5 | DeviceFileEvents.MD5, DeviceFileEvents.InitiatingProcessMD5, DeviceProcessEvents.MD5, DeviceProcessEvents.InitiatingProcessMD5, DeviceNetworkEvents.InitiatingProcessMD5, DeviceRegistryEvents.InitiatingProcessMD5 |
| **process**:created | DeviceProcessEvents.ProcessCreationTime, DeviceProcessEvents.InitiatingProcessParentCreationTime, DeviceNetworkEvents.InitiatingProcessCreationTime, DeviceNetworkEvents.InitiatingProcessParentCreationTime, DeviceRegistryEvents.InitiatingProcessCreationTime, DeviceRegistryEvents.InitiatingProcessParentCreationTime, DeviceFileEvents.InitiatingProcessCreationTime, DeviceFileEvents.InitiatingProcessParentCreationTime |
| **process**:parent_ref.created | DeviceProcessEvents.InitiatingProcessParentCreationTime, DeviceNetworkEvents.InitiatingProcessParentCreationTime, DeviceRegistryEvents.InitiatingProcessParentCreationTime, DeviceFileEvents.InitiatingProcessParentCreationTime |
| **process**:binary_ref.parent_directory_ref.path | DeviceProcessEvents.InitiatingProcessFolderPath, DeviceNetworkEvents.InitiatingProcessFolderPath, DeviceRegistryEvents.InitiatingProcessFolderPath, DeviceFileEvents.InitiatingProcessFolderPath |
| **process**:child_refs.binary_ref.parent_directory_ref.path | DeviceProcessEvents.FolderPath |
| **user-account**:user_id | DeviceProcessEvents.AccountSid, DeviceNetworkEvents.InitiatingProcessAccountSid, DeviceRegistryEvents.InitiatingProcessAccountSid |
| **user-account**:account_login | DeviceProcessEvents.AccountName, DeviceNetworkEvents.InitiatingProcessAccountName, DeviceRegistryEvents.InitiatingProcessAccountName |
| **windows-registry-key**:key | DeviceRegistryEvents.RegistryKey |
| **windows-registry-key**:values[*] | DeviceRegistryEvents.RegistryValueName |
| **mac-addr**:value | DeviceNetworkInfo.MacAddress |
| **x-msatp**:computer_name | DeviceProcessEvents.DeviceName, DeviceNetworkEvents.DeviceName, DeviceRegistryEvents.DeviceName, DeviceFileEvents.DeviceName |
| **x-msatp**:machine_id | DeviceProcessEvents.DeviceId, DeviceNetworkEvents.DeviceId, DeviceRegistryEvents.DeviceId, DeviceFileEvents.DeviceId |
| **directory**:path | DeviceFileEvents.FolderPath, DeviceFileEvents.InitiatingProcessFolderPath, DeviceProcessEvents.FolderPath, DeviceProcessEvents.InitiatingProcessFolderPath, DeviceNetworkEvents.InitiatingProcessFolderPath, DeviceRegistryEvents.InitiatingProcessFolderPath |
| **x-oca-asset**:domain | DeviceFileEvents.DeviceName, DeviceProcessEvents.DeviceName, DeviceNetworkEvents.DeviceName, DeviceRegistryEvents.DeviceName, DeviceEvents.DeviceName, DeviceInfo.DeviceName, DeviceAlertEvents.DeviceName, DeviceImageLoadEvents.DeviceName, DeviceLogonEvents.DeviceName, DeviceNetworkInfo.DeviceName |
| **x-oca-asset**:hostname | DeviceFileEvents.DeviceName, DeviceProcessEvents.DeviceName, DeviceNetworkEvents.DeviceName, DeviceRegistryEvents.DeviceName, DeviceEvents.DeviceName, DeviceInfo.DeviceName, DeviceAlertEvents.DeviceName, DeviceImageLoadEvents.DeviceName, DeviceLogonEvents.DeviceName, DeviceNetworkInfo.DeviceName |
| **x-oca-asset**:name | DeviceFileEvents.DeviceName, DeviceProcessEvents.DeviceName, DeviceNetworkEvents.DeviceName, DeviceRegistryEvents.DeviceName, DeviceEvents.DeviceName, DeviceInfo.DeviceName, DeviceAlertEvents.DeviceName, DeviceImageLoadEvents.DeviceName, DeviceLogonEvents.DeviceName, DeviceNetworkInfo.DeviceName |
| **x-oca-asset**:ip | DeviceNetworkEvents.LocalIP |
| **x-oca-asset**:os.name | DeviceInfo.OSPlatform |
| **x-oca-asset**:os.platform | DeviceInfo.OSPlatform |
| **x-oca-event**:process_ref.pid | DeviceProcessEvents.InitiatingProcessId, DeviceNetworkEvents.InitiatingProcessId, DeviceRegistryEvents.InitiatingProcessId, DeviceFileEvents.InitiatingProcessId |
| **x-oca-event**:process_ref.child_refs.pid | DeviceProcessEvents.ProcessId |
| **x-oca-event**:process_ref.name | DeviceProcessEvents.InitiatingProcessFileName, DeviceNetworkEvents.InitiatingProcessFileName, DeviceRegistryEvents.InitiatingProcessFileName, DeviceFileEvents.InitiatingProcessFileName |
| **x-oca-event**:process_ref.child_refs.name | DeviceProcessEvents.FileName |
| **x-oca-event**:process_ref.binary_ref.name | DeviceProcessEvents.InitiatingProcessFileName, DeviceNetworkEvents.InitiatingProcessFileName, DeviceRegistryEvents.InitiatingProcessFileName, DeviceFileEvents.InitiatingProcessFileName |
| **x-oca-event**:process_ref.creator_user_ref.account_login | DeviceProcessEvents.AccountName |
| **x-oca-event**:process_ref.parent_ref.name | DeviceProcessEvents.InitiatingProcessParentFileName, DeviceNetworkEvents.InitiatingProcessParentFileName, DeviceRegistryEvents.InitiatingProcessParentFileName, DeviceFileEvents.InitiatingProcessParentFileName |
| **x-oca-event**:process_ref.parent_ref.pid | DeviceProcessEvents.InitiatingProcessParentId, DeviceNetworkEvents.InitiatingProcessParentId, DeviceRegistryEvents.InitiatingProcessParentId, DeviceFileEvents.InitiatingProcessParentId |
| **x-oca-event**:process_ref.command_line | DeviceProcessEvents.InitiatingProcessCommandLine, DeviceNetworkEvents.InitiatingProcessCommandLine, DeviceRegistryEvents.InitiatingProcessCommandLine, DeviceFileEvents.InitiatingProcessCommandLine |
| **x-oca-event**:process_ref.binary_ref.hashes.'SHA-256' | DeviceProcessEvents.InitiatingProcessSHA256, DeviceNetworkEvents.InitiatingProcessSHA256, DeviceRegistryEvents.InitiatingProcessSHA256, DeviceFileEvents.InitiatingProcessSHA256 |
| **x-oca-event**:process_ref.process_ref.creator_user_ref.account_login | DeviceProcessEvents.AccountName |
| **x-oca-event**:parent_process_ref.name | DeviceProcessEvents.InitiatingProcessParentFileName, DeviceNetworkEvents.InitiatingProcessParentFileName, DeviceRegistryEvents.InitiatingProcessParentFileName, DeviceFileEvents.InitiatingProcessParentFileName |
| **x-oca-event**:parent_process_ref.pid | DeviceProcessEvents.InitiatingProcessParentId, DeviceNetworkEvents.InitiatingProcessParentId, DeviceRegistryEvents.InitiatingProcessParentId, DeviceFileEvents.InitiatingProcessParentId |
| **x-oca-event**:process_ref.binary_ref.hashes.MD5 | DeviceProcessEvents.InitiatingProcessMD5, DeviceNetworkEvents.InitiatingProcessMD5, DeviceRegistryEvents.InitiatingProcessMD5, DeviceFileEvents.InitiatingProcessMD5 |
| **x-oca-event**:process_ref.creator_user_ref.user_id | DeviceProcessEvents.InitiatingProcessAccountSid, DeviceNetworkEvents.InitiatingProcessAccountSid, DeviceRegistryEvents.InitiatingProcessAccountSid, DeviceFileEvents.InitiatingProcessAccountSid |
| **x-oca-event**:domain_ref.value | DeviceProcessEvents.DeviceName, DeviceNetworkEvents.DeviceName, DeviceRegistryEvents.DeviceName, DeviceFileEvents.DeviceName |
| **x-oca-event**:file_ref.name | DeviceProcessEvents.InitiatingProcessFileName, DeviceNetworkEvents.InitiatingProcessFileName, DeviceRegistryEvents.InitiatingProcessFileName |
| **x-oca-event**:registry_ref.key | DeviceRegistryEvents.RegistryKey |
| **x-oca-event**:host_ref.hostname | DeviceFileEvents.DeviceName, DeviceProcessEvents.DeviceName, DeviceNetworkEvents.DeviceName, DeviceRegistryEvents.DeviceName, DeviceEvents.DeviceName, DeviceInfo.DeviceName, DeviceAlertEvents.DeviceName, DeviceImageLoadEvents.DeviceName, DeviceLogonEvents.DeviceName, DeviceNetworkInfo.DeviceName |
| **x-oca-event**:host_ref.name | DeviceFileEvents.DeviceName, DeviceProcessEvents.DeviceName, DeviceNetworkEvents.DeviceName, DeviceRegistryEvents.DeviceName, DeviceEvents.DeviceName, DeviceInfo.DeviceName, DeviceAlertEvents.DeviceName, DeviceImageLoadEvents.DeviceName, DeviceLogonEvents.DeviceName, DeviceNetworkInfo.DeviceName |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| directory | path | InitiatingProcessFolderPath |
| directory | path | FolderPath |
| <br> | | |
| file | hashes.SHA-1 | InitiatingProcessSHA1 |
| file | hashes.SHA-256 | InitiatingProcessSHA256 |
| file | hashes.MD5 | InitiatingProcessMD5 |
| file | name | InitiatingProcessFileName |
| file | name | InitiatingProcessParentFileName |
| file | parent_directory_ref | InitiatingProcessFolderPath |
| file | name | FileName |
| file | parent_directory_ref | FolderPath |
| file | hashes.SHA-1 | SHA1 |
| file | hashes.SHA-256 | SHA256 |
| file | hashes.MD5 | MD5 |
| <br> | | |
| ipv4-addr | value | LocalIP |
| ipv4-addr | value | RemoteIP |
| ipv4-addr | resolves_to_refs | MacAddress |
| ipv4-addr | value | IpAddresses |
| <br> | | |
| ipv6-addr | value | LocalIP |
| ipv6-addr | value | RemoteIP |
| ipv6-addr | value | IpAddresses |
| <br> | | |
| mac-addr | value | MacAddress |
| <br> | | |
| network-traffic | src_ref | LocalIP |
| network-traffic | dst_ref | RemoteIP |
| network-traffic | src_port | LocalPort |
| network-traffic | dst_port | RemotePort |
| network-traffic | protocols | Protocol |
| network-traffic | src_ref | MacAddress |
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
| process | creator_user_ref | InitiatingProcessAccountSid |
| process | creator_user_ref | InitiatingProcessAccountName |
| process | binary_ref | InitiatingProcessFolderPath |
| process | name | FileName |
| process | binary_ref | FileName |
| process | child_refs | FileName |
| process | pid | ProcessId |
| process | child_refs | ProcessId |
| process | command_line | ProcessCommandLine |
| process | child_refs | ProcessCommandLine |
| process | created | ProcessCreationTime |
| process | child_refs | ProcessCreationTime |
| process | creator_user_ref | AccountSid |
| process | creator_user_ref | AccountName |
| <br> | | |
| url | value | RemoteUrl |
| <br> | | |
| user-account | user_id | InitiatingProcessAccountSid |
| user-account | account_login | InitiatingProcessAccountName |
| user-account | user_id | AccountSid |
| user-account | account_login | AccountName |
| <br> | | |
| windows-registry-key | key | RegistryKey |
| windows-registry-key | values | RegistryValues |
| <br> | | |
| x-msatp | computer_name | DeviceName |
| x-msatp | machine_id | DeviceId |
| <br> | | |
| x-oca-asset | device_id | DeviceId |
| x-oca-asset | hostname | DeviceName |
| x-oca-asset | ip_refs | IpAddresses |
| x-oca-asset | mac_refs | MacAddress |
| <br> | | |
| x-oca-event | network_ref | MacAddress |
| x-oca-event | created | Timestamp |
| x-oca-event | action | ActionType |
| x-oca-event | process_ref | FileName |
| x-oca-event | process_ref | ProcessId |
| x-oca-event | file_ref | FileName |
| x-oca-event | process_ref | InitiatingProcessId |
| x-oca-event | parent_process_ref | InitiatingProcessParentId |
| x-oca-event | user_ref | InitiatingProcessAccountSid |
| x-oca-event | host_ref | DeviceName |
| <br> | | |
