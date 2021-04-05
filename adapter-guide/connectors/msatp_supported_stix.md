## Microsoft Defender Advanced Threat Protection
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
| file | hashes.SHA-1 | SHA1 |
| file | hashes.SHA-256 | SHA256 |
| file | hashes.MD5 | MD5 |
| file | name | FileName |
| file | parent_directory_ref | FolderPath |
| <br> | | |
| ipv4-addr | value | LocalIP |
| ipv4-addr | value | RemoteIP |
| ipv4-addr | resolves_to_refs | MacAddress |
| <br> | | |
| ipv6-addr | value | LocalIP |
| ipv6-addr | value | RemoteIP |
| ipv6-addr | resolves_to_refs | MacAddress |
| <br> | | |
| mac-addr | value | MacAddress |
| <br> | | |
| network-traffic | src_ref | LocalIP |
| network-traffic | dst_ref | RemoteIP |
| network-traffic | src_port | LocalPort |
| network-traffic | dst_port | RemotePort |
| network-traffic | protocols | Protocol |
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
| process | binary_ref | SHA1 |
| process | binary_ref | SHA256 |
| process | binary_ref | MD5 |
| process | parent_ref | InitiatingProcessSHA1 |
| process | parent_ref | InitiatingProcessSHA256 |
| process | parent_ref | InitiatingProcessMD5 |
| process | name | FileName |
| process | parent_ref | InitiatingProcessFileName |
| process | pid | ProcessId |
| process | parent_ref | InitiatingProcessId |
| process | command_line | ProcessCommandLine |
| process | parent_ref | InitiatingProcessCommandLine |
| process | created | ProcessCreationTime |
| process | parent_ref | InitiatingProcessCreationTime |
| process | creator_user_ref | AccountSid |
| process | creator_user_ref | AccountName |
| process | binary_ref | FolderPath |
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
| x_msatp | computer_name | ComputerName |
| x_msatp | machine_id | MachineId |
| <br> | | |
