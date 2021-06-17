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
| process | pid | ProcessId |
| process | command_line | ProcessCommandLine |
| process | created | ProcessCreationTime |
| process | parent_ref | InitiatingProcessSHA1 |
| process | parent_ref | InitiatingProcessSHA256 |
| process | parent_ref | InitiatingProcessMD5 |
| process | parent_ref | InitiatingProcessFileName |
| process | parent_ref | InitiatingProcessId |
| process | parent_ref | InitiatingProcessCommandLine |
| process | parent_ref | InitiatingProcessCreationTime |
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
| x-oca-asset | device_id | DeviceId |
| x-oca-asset | hostname | DeviceName |
| x-oca-asset | ip_refs | IpAddresses |
| x-oca-asset | mac_refs | MacAddress |
| <br> | | |
| x-oca-event | start | Timestamp |
| x-oca-event | end | Timestamp |
| x-oca-event | action | ActionType |
| x-oca-event | process_ref | FileName |
| x-oca-event | file_ref | FileName |
| x-oca-event | process_ref | ProcessId |
| x-oca-event | process_ref | InitiatingProcessId |
| x-oca-event | parent_process_ref | InitiatingProcessParentId |
| x-oca-event | user_ref | InitiatingProcessAccountSid |
| x-oca-event | host_ref | DeviceName |
| <br> | | |
| x_msatp | computer_name | DeviceName |
| x_msatp | machine_id | DeviceId |
| <br> | | |
