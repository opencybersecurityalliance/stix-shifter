##### Updated on 02/04/22
## CrowdStrike Falcon
### Supported STIX Operators
| STIX Operator | Data Source Operator |
|--|--|
| AND | + |
| OR | , |
| = | : |
| != | :! |
| > | :> |
| >= | :>= |
| < | :< |
| <= | :<= |
| <br> | |
### Supported STIX Objects and Properties
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| directory | path | filepath |
| <br> | | |
| domain-name | value | domain_ioc |
| <br> | | |
| file | name | filename |
| file | parent_directory_ref | filepath |
| file | hashes.SHA-256 | sha256 |
| file | hashes.MD5 | md5 |
| file | hashes.SHA-256 | parent_sha256 |
| file | hashes.SHA-256 | sha256_ioc |
| file | hashes.SHA-256 | quarantined_file_sha256 |
| file | hashes.MD5 | md5_ioc |
| file | hashes.MD5 | parent_md5 |
| <br> | | |
| ipv4-addr | value | external_ip |
| ipv4-addr | value | local_ip |
| <br> | | |
| mac-addr | value | mac_address |
| <br> | | |
| network-traffic | dst_ref | domain_ioc |
| <br> | | |
| process | binary_ref | filename |
| process | name | filename |
| process | binary_ref | filepath |
| process | command_line | cmdline |
| process | creator_user_ref | user_name |
| process | creator_user_ref | user_id |
| process | binary_ref | parent_sha256 |
| process | parent_ref | parent_sha256 |
| process | pid | parent_process_graph_id |
| process | parent_ref | parent_process_graph_id |
| process | pid | triggering_process_graph_id |
| process | binary_ref | parent_md5 |
| process | parent_ref | parent_md5 |
| process | command_line | parent_cmdline |
| process | parent_ref | parent_cmdline |
| <br> | | |
| user-account | account_login | user_name |
| user-account | user_id | user_id |
| <br> | | |
| windows-registry-key | key | registry_key |
| <br> | | |
| x-crowdstrike | machine_domain | machine_domain |
| x-crowdstrike | device_id | device_id |
| x-crowdstrike | detection_id | detection_id |
| x-crowdstrike | scenario | scenario |
| x-crowdstrike | technique | technique |
| x-crowdstrike | tactic | tactic |
| x-crowdstrike | tactic_id | tactic_id |
| x-crowdstrike | technique_id | technique_id |
| x-crowdstrike | agent_local_time | agent_local_time |
| x-crowdstrike | agent_version | agent_version |
| x-crowdstrike | first_seen | first_seen |
| x-crowdstrike | last_seen | last_seen |
| x-crowdstrike | platform_id | platform_id |
| x-crowdstrike | confidence | confidence |
| x-crowdstrike | ioc_type | ioc_type |
| x-crowdstrike | ioc_value | ioc_value |
| x-crowdstrike | ioc_value | bios_manufacturer |
| x-crowdstrike | ioc_value | bios_version |
| x-crowdstrike | ioc_value | config_id_base |
| x-crowdstrike | ioc_value | config_id_build |
| x-crowdstrike | ioc_value | config_id_platform |
| x-crowdstrike | ioc_value | product_type |
| x-crowdstrike | ioc_value | product_type_desc |
| x-crowdstrike | ioc_value | site_name |
| x-crowdstrike | ioc_value | system_product_name |
| x-crowdstrike | ioc_value | modified_timestamp |
| <br> | | |
| x-oca-asset | ip_refs | external_ip |
| x-oca-asset | hostname | hostname |
| x-oca-asset | ip_refs | local_ip |
| x-oca-asset | mac_refs | mac_address |
| x-oca-asset | os_version | os_version |
| x-oca-asset | os_platform | platform_name |
| <br> | | |
| x-oca-event | created | timestamp |
| x-oca-event | process_ref | filename |
| x-oca-event | action | display_name |
| x-oca-event | outcome | description |
| x-oca-event | registry_ref | registry_key |
| x-oca-event | network_ref | domain_ioc |
| x-oca-event | file_ref | sha256_ioc |
| x-oca-event | file_ref | quarantined_file_sha256 |
| x-oca-event | file_ref | md5_ioc |
| x-oca-event | parent_process_ref | parent_md5 |
| x-oca-event | host_ref | hostname |
| x-oca-event | provider | provider |
| x-oca-event | severity | severity |
| <br> | | |
