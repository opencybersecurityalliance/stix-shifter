##### Updated on 05/23/24
## CrowdStrike Falcon
### Results STIX Domain Objects
* Identity
* Observed Data
<br>
### Supported STIX Operators
*Comparison AND/OR operators are inside the observation while observation AND/OR operators are between observations (square brackets).*

| STIX Operator | Data Source Operator |
|--|--|
| AND (Comparison) | + |
| OR (Comparison) | , |
| = | : |
| != | :! |
| > | :> |
| >= | :>= |
| < | :< |
| <= | :<= |
| IN | : |
| <br> | |
### Searchable STIX objects and properties
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **ipv4-addr**:value | device.external_ip, device.local_ip |
| **ipv6-addr**:value | device.external_ip, device.local_ip |
| **mac-addr**:value | device.mac_address |
| **file**:name | behaviors.filename |
| **file**:hashes.MD5 | behaviors.md5, behaviors.parent_details.parent_md5 |
| **file**:hashes.'SHA-256' | behaviors.sha256, behaviors.parent_details.parent_sha256 |
| **file**:hashes.parent_MD5 | behaviors.parent_details.parent_md5 |
| **file**:hashes.parent_SHA-256 | behaviors.parent_details.parent_sha256 |
| **file**:hashes.child_MD5 | behaviors.md5 |
| **file**:hashes.child_SHA-256 | behaviors.sha256 |
| **file**:parent_directory_ref.path | behaviors.filepath |
| **process**:command_line | behaviors.cmdline |
| **process**:created | behaviors.timestamp |
| **process**:name | behaviors.filename |
| **process**:creator_user_ref.user_id | behaviors.user_id |
| **process**:creator_user_ref.account_login | behaviors.user_name |
| **process**:binary_ref.hashes.MD5 | behaviors.md5 |
| **process**:binary_ref.hashes.'SHA-256' | behaviors.sha256 |
| **process**:parent_ref.name | behaviors.filename |
| **process**:parent_ref.command_line | behaviors.parent_cmdline |
| **process**:parent_ref.binary_ref.hashes.MD5 | behaviors.parent_details.parent_md5 |
| **process**:parent_ref.binary_ref.hashes.'SHA-256' | behaviors.parent_details.parent_sha256 |
| **url**:value | device.hostinfo.domain |
| **domain-name**:value | ioc_type.domain |
| **user-account**:user_id | behaviors.user_id |
| **user-account**:account_login | behaviors.user_name |
| **directory**:path | behaviors.filepath |
| **x-oca-event**:process_ref.name | behaviors.filename |
| **x-oca-event**:process_ref.command_line | behaviors.cmdline |
| **x-oca-event**:process_ref.binary_ref.name | behaviors.filename |
| **x-oca-event**:process_ref.creator_user_ref.user_id | behaviors.user_id |
| **x-oca-event**:process_ref.creator_user_ref.account_login | behaviors.user_name |
| **x-oca-event**:process_ref.parent_ref.name | behaviors.filename |
| **x-oca-event**:process_ref.parent_ref.command_line | behaviors.parent_details.parent_cmdline |
| **x-oca-event**:process_ref.parent_ref.binary_ref.hashes.MD5 | behaviors.parent_details.parent_md5 |
| **x-oca-event**:process_ref.parent_ref.binary_ref.hashes.'SHA-256' | behaviors.parent_details.parent_sha256 |
| **x-oca-event**:parent_process_ref.name | behaviors.filename |
| **x-oca-event**:parent_process_ref.command_line | behaviors.parent_details.parent_cmdline |
| **x-oca-event**:parent_process_ref.binary_ref.hashes.MD5 | behaviors.parent_details.parent_md5 |
| **x-oca-event**:parent_process_ref.binary_ref.hashes.'SHA-256' | behaviors.parent_details.parent_sha256 |
| **x-oca-event**:parent_process_ref.creator_user_ref.user_id | behaviors.user_id |
| **x-oca-event**:parent_process_ref.creator_user_ref.account_login | behaviors.user_name |
| **x-oca-event**:domain_ref.value | device.hostname |
| **x-oca-event**:file_ref.name | behaviors.filename |
| **x-oca-event**:host_ref.hostname | device.hostname |
| **x-oca-event**:host_ref.name | device.machine_domain |
| **x-oca-asset**:name | device.machine_domain |
| **x-oca-asset**:hostname | device.hostname |
| **x-oca-asset**:ip_refs | device.external_ip, device.local_ip |
| **x-oca-asset**:os_name | device.platform_name |
| **x-oca-asset**:os_platform | device.platform_name |
| **x-crowdstrike**:device_id | device.device_id |
| **x-crowdstrike**:detection_id | device.detection_id |
| **x-crowdstrike**:scenario | behaviors.scenario |
| **x-crowdstrike**:tactic_id | device.tactic_id |
| **x-crowdstrike**:severity | device.severity |
| **x-crowdstrike**:tactic | behaviors.tactic |
| **x-crowdstrike**:technique | behaviors.technique |
| **x-crowdstrike**:technique_id | device.technique_id |
| **x-crowdstrike**:agent_local_time | device.agent_local_time |
| **x-crowdstrike**:agent_version | device.agent_version |
| **x-crowdstrike**:first_seen | device.first_seen |
| **x-crowdstrike**:last_seen | device.last_seen |
| **x-crowdstrike**:confidence | device.confidence |
| **x-crowdstrike**:bios_manufacturer | device.bios_manufacturer |
| **x-crowdstrike**:bios_version | device.bios_version |
| **x-crowdstrike**:config_id_base | device.config_id_base |
| **x-crowdstrike**:config_id_build | device.config_id_build |
| **x-crowdstrike**:config_id_platform | device.config_id_platform |
| **x-crowdstrike**:platform_id | device.platform_id |
| **x-crowdstrike**:product_type | device.product_type |
| **x-crowdstrike**:product_type_desc | device.product_type_desc |
| **x-crowdstrike**:site_name | device.site_name |
| **x-crowdstrike**:system_manufacturer | device.system_manufacturer |
| **x-crowdstrike**:system_product_name | device.system_product_name |
| **x-crowdstrike**:modified_timestamp | device.modified_timestamp |
| **x-crowdstrike**:instance_id | device.instance_id |
| **x-crowdstrike**:service_provider | device.service_provider |
| **x-crowdstrike**:status | device.status |
| **x-crowdstrike**:event_status | behaviors.status |
| **x-crowdstrike**:max_severity_displayname | behaviors.max_severity_displayname |
| **x-crowdstrike**:control_graph_id | behaviors.control_graph_i |
| **x-crowdstrike**:display_name_1 | behaviors.display_name |
| **x-crowdstrike**:objective | behaviors.objective |
| <br> | |
### Supported STIX Objects and Properties for Query Results
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
| x-crowdstrike | control_graph_id | control_graph_id |
| x-crowdstrike | display_name_1 | display_name_1 |
| x-crowdstrike | objective | objective |
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
| x-crowdstrike | instance_id | instance_id |
| x-crowdstrike | service_provider | service_provider |
| x-crowdstrike | status | status |
| x-crowdstrike | event_status | event_status |
| x-crowdstrike | max_severity_displayname | max_severity_displayname |
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
| x-oca-event | domain_ref | domain_ioc |
| x-oca-event | file_ref | sha256_ioc |
| x-oca-event | file_ref | quarantined_file_sha256 |
| x-oca-event | file_ref | md5_ioc |
| x-oca-event | parent_process_ref | parent_md5 |
| x-oca-event | host_ref | hostname |
| x-oca-event | provider | provider |
| x-oca-event | severity | severity |
| <br> | | |
