##### Updated on 12/20/23
## Crowdstirke Logscale
### Results STIX Domain Objects
* Identity
* Observed Data

### Supported STIX Operators
*Comparison AND/OR operators are inside the observation while observation AND/OR operators are between observations (square brackets).*

| STIX Operator | Data Source Operator |
|--|--|
| AND (Comparison) | and |
| OR (Comparison) | or |
| > | > |
| < | < |
| >= | >= |
| <= | <= |
| = | = |
| LIKE | = |
| IN | = |
| MATCHES | = |
| != | != |
| ISSUBSET | =~ |
| OR (Observation) | or |
| AND (Observation) | or |
| <br> | |
### Searchable STIX objects and properties
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **ipv4-addr**:value | device.local_ip, device.external_ip |
| **ipv6-addr**:value | device.local_ip, device.external_ip |
| **mac-addr**:value | device.mac_address |
| **process**:name | behaviors[*].filename |
| **process**:command_line | behaviors[*].cmdline |
| **process**:x_process_graph_id | behaviors[*].triggering_process_graph_id |
| **process**:parent_ref.command_line | behaviors[*].parent_details.parent_cmdline |
| **process**:parent_ref.x_process_graph_id | behaviors[*].parent_details.parent_process_graph_id |
| **process**:binary_ref.name | behaviors[*].filename |
| **process**:binary_ref.hashes.MD5 | behaviors[*].md5 |
| **process**:binary_ref.hashes.'SHA-256' | behaviors[*].sha256 |
| **process**:creator_user_ref.user_id | behaviors[*].user_id |
| **file**:name | behaviors[*].filename |
| **file**:hashes.MD5 | behaviors[\*].parent_details.parent_md5, behaviors[\*].md5 |
| **file**:hashes.'SHA-256' | behaviors[\*].parent_details.parent_sha256, behaviors[\*].sha256 |
| **file**:x_extension | behaviors[*].alleged_filetype |
| **file**:x_path | behaviors[*].filepath |
| **file**:parent_directory_ref.path | behaviors[*].filepath |
| **directory**:path | behaviors[*].filepath |
| **user-account**:user_id | behaviors[*].user_id |
| **user-account**:display_name | behaviors[*].user_name |
| **software**:name | device.platform_name |
| **software**:version | device.os_version |
| **software**:x_id | device.platform_id |
| **software**:x_minor_version | device.minor_version |
| **software**:x_major_version | device.major_version |
| **x-ibm-finding**:name | detection_id |
| **x-ibm-finding**:severity | max_severity |
| **x-ibm-finding**:confidence | max_confidence |
| **x-ibm-finding**:time_observed | created_timestamp |
| **x-ibm-finding**:x_first_behavior_observed | first_behavior |
| **x-ibm-finding**:x_last_behavior_observed | last_behavior |
| **x-ibm-finding**:src_ip_ref.value | device.external_ip |
| **x-ibm-finding**:x_severity_name | max_severity_displayname |
| **x-ibm-finding**:x_status | status |
| **x-ibm-finding**:x_last_updated | date_updated |
| **x-ibm-finding**:x_behaviors_processed[*] | behaviors_processed[*] |
| **x-ibm-finding**:x_behavior_refs[*].behavior_id | behaviors[*].behavior_id |
| **x-ibm-finding**:src_os_ref.name | device.platform_name |
| **x-ibm-finding**:ttp_tagging_refs.name | behaviors[*].tactic |
| **x-oca-asset**:hostname | device.hostname |
| **x-oca-asset**:device_id | device.device_id |
| **x-oca-asset**:ip_refs[*].value | device.local_ip, device.external_ip |
| **x-oca-asset**:mac_refs[*].value | device.mac_address |
| **x-oca-asset**:host_type | device.product_type_desc |
| **x-oca-asset**:x_instance_id | device.instance_id |
| **x-oca-asset**:x_host_type_number | device.product_type |
| **x-oca-asset**:x_first_seen | device.first_seen |
| **x-oca-asset**:x_last_seen | device.last_seen |
| **x-oca-asset**:x_bios_manufacturer | device.bios_manufacturer |
| **x-oca-asset**:x_bios_version | device.bios_version |
| **x-oca-asset**:x_last_modified | device.modified_timestamp |
| **x-oca-asset**:x_service_provider | device.service_provider |
| **x-oca-asset**:x_service_account_id | device.service_provider_account_id |
| **x-oca-asset**:x_status | device.status |
| **x-oca-asset**:x_system_product_name | device.system_product_name |
| **x-oca-asset**:x_system_manufacturer | device.system_manufacturer |
| **x-oca-asset**:x_agent_ref.version | device.agent_version |
| **x-oca-asset**:x_cid | cid |
| **x-oca-asset**:x_device_groups[*] | device.groups[*] |
| **x-oca-asset**:os_ref.name | device.platform_name |
| **x-ibm-ttp-tagging**:name | behaviors[*].tactic |
| **x-ibm-ttp-tagging**:extensions.'mitre-attack-ext'.technique_name | behaviors[*].technique |
| **x-ibm-ttp-tagging**:extensions.'mitre-attack-ext'.technique_id | behaviors[*].technique_id |
| **x-ibm-ttp-tagging**:extensions.'mitre-attack-ext'.tactic_id | behaviors[*].tactic_id |
| **x-crowdstrike-detection-behavior**:description | behaviors[*].description |
| **x-crowdstrike-detection-behavior**:objective | behaviors[*].objective |
| **x-crowdstrike-detection-behavior**:behavior_id | behaviors[*].behavior_id |
| **x-crowdstrike-detection-behavior**:display_name | behaviors[*].display_name |
| **x-crowdstrike-detection-behavior**:rule_instance_version | behaviors[*].rule_instance_version |
| **x-crowdstrike-detection-behavior**:pattern_disposition | behaviors[*].pattern_disposition |
| **x-crowdstrike-detection-behavior**:rule_instance_id | behaviors[*].rule_instance_id |
| **x-crowdstrike-detection-behavior**:created_time | behaviors[*].timestamp |
| **x-crowdstrike-detection-behavior**:control_graph_id | behaviors[*].control_graph_id |
| **x-crowdstrike-detection-behavior**:severity | behaviors[*].severity |
| **x-crowdstrike-detection-behavior**:confidence | behaviors[*].confidence |
| **x-crowdstrike-detection-behavior**:template_instance_id | behaviors[*].template_instance_id |
| **x-crowdstrike-detection-behavior**:scenario | behaviors[*].scenario |
| **x-crowdstrike-detection-behavior**:ioc_description | behaviors[*].ioc_description |
| **x-crowdstrike-detection-behavior**:ioc_source | behaviors[*].ioc_source |
| **x-crowdstrike-detection-behavior**:ioc_type | behaviors[*].ioc_type |
| **x-crowdstrike-detection-behavior**:ioc_value | behaviors[*].ioc_value |
| **x-crowdstrike-detection-behavior**:ttp_tagging_ref.name | behaviors[*].tactic |
| **x-crowdstrike-detection-behavior**:process_ref.name | behaviors[*].filename |
| **x-crowdstrike-detection-behavior**:user_ref.user_id | behaviors[*].user_id |
| **x-crowdstrike-edr-agent**:local_time | device.agent_local_time |
| **x-crowdstrike-edr-agent**:version | device.agent_version |
| **x-crowdstrike-edr-agent**:config_id_platform | device.config_id_platform |
| **x-crowdstrike-edr-agent**:config_id_base | device.config_id_base |
| **x-crowdstrike-edr-agent**:config_id_build | device.config_id_build |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property                              | Data Source Field |
|--|--------------------------------------------|--|
| domain-name | value                                      | domain |
| <br> |                                            | |
| ipv4-addr | value                                      | local_ip |
| ipv4-addr | value                                      | external_ip |
| ipv4-addr | resolves_to_refs                           | local_ip |
| <br> |                                            | |
| ipv6-addr | value                                      | local_ip |
| ipv6-addr | value                                      | external_ip |
| ipv6-addr | resolves_to_refs                           | local_ip |
| <br> |                                            | |
| mac-addr | value                                      | mac_address |
| process | name                                       | filename |
| process | command_line                               | cmdline |
| process | command_line                               | parent_cmdline |
| process | x_process_graph_id                         | triggering_process_graph_id |
| process | x_process_graph_id                         | parent_process_graph_id |
| process | parent_ref                                 | parent_cmdline |
| process | parent_ref                                 | parent_process_graph_id |
| process | binary_ref                                 | md5 |
| process | binary_ref                                 | parent_sha256 |
| process | binary_ref                                 | parent_md5 |
| process | binary_ref                                 | filename |
| process | creator_user_ref                           | user_id |
| <br> |                                            | |
| file | name                                       | filename |
| file | hashes.MD5                                 | md5 |
| file | hashes.MD5                                 | parent_md5 |
| file | hashes.SHA-256                             | parent_sha256 |
| file | hashes.SHA-256                             | sha256 |
| file | x_extension                                | alleged_filetype |
| file | x_path                                     | filepath |
| file | parent_directory_ref                       | filepath |
| <br> |                                            | |
| directory | path                                       | filepath |
| <br> |                                            | |
| user-account | user_id                                    | user_id |
| user-account | display_name                               | user_name |
| <br> |                                            | |
| software | name                                       | platform_name |
| software | version                                    | os_version |
| software | x_id                                       | platform_id |
| software | x_minor_version                            | minor_version |
| software | x_major_version                            | major_version |
| <br> |                                            | |
| x-crowdstrike-detection-behavior | description                                | description |
| x-crowdstrike-detection-behavior | objective                                  | objective |
| x-crowdstrike-detection-behavior | behavior_id                                | behavior_id |
| x-crowdstrike-detection-behavior | display_name                               | display_name |
| x-crowdstrike-detection-behavior | rule_instance_version                      | rule_instance_version |
| x-crowdstrike-detection-behavior | pattern_disposition                        | pattern_disposition |
| x-crowdstrike-detection-behavior | pattern_disposition                        | pattern_disposition_details |
| x-crowdstrike-detection-behavior | rule_instance_id                           | rule_instance_id |
| x-crowdstrike-detection-behavior | created_time                               | timestamp |
| x-crowdstrike-detection-behavior | control_graph_id                           | control_graph_id |
| x-crowdstrike-detection-behavior | severity                                   | severity |
| x-crowdstrike-detection-behavior | confidence                                 | confidence |
| x-crowdstrike-detection-behavior | template_instance_id                       | template_instance_id |
| x-crowdstrike-detection-behavior | scenario                                   | scenario |
| x-crowdstrike-detection-behavior | ioc_description                            | ioc_description |
| x-crowdstrike-detection-behavior | ioc_source                                 | ioc_source |
| x-crowdstrike-detection-behavior | ioc_type                                   | ioc_type |
| x-crowdstrike-detection-behavior | ioc_value                                  | ioc_value |
| x-crowdstrike-detection-behavior | ttp_tagging_ref                            | tactic |
| x-crowdstrike-detection-behavior | ttp_tagging_ref                            | tactic_id |
| x-crowdstrike-detection-behavior | process_ref                                | filename |
| x-crowdstrike-detection-behavior | user_ref                                   | user_id |
| <br> |                                            | |
| x-ibm-finding | name                                       | detection_id |
| x-ibm-finding | confidence                                 | max_confidence |
| x-ibm-finding | time_observed                              | created_timestamp |
| x-ibm-finding | severity                                   | max_severity |
| x-ibm-finding | x_severity_name                            | max_severity_displayname |
| x-ibm-finding | x_status                                   | status |
| x-ibm-finding | x_first_behavior_observed                  | first_behavior |
| x-ibm-finding | x_last_behavior_observed                   | last_behavior |
| x-ibm-finding | x_last_updated                             | date_updated |
| x-ibm-finding | x_behaviors_processed                      | behaviors_processed |
| x-ibm-finding | src_ip_ref                                 | external_ip |
| x-ibm-finding | src_os_ref                                 | platform_name |
| x-ibm-finding | ttp_tagging_refs                           | sensor_name |
| x-ibm-finding | x_is_email_sent                            | email_sent |
| x-ibm-finding | ioc_refs                                   | domain |
| x-ibm-finding | x_seconds_to_resolved                      | seconds_to_resolved |
| x-ibm-finding | x_seconds_to_triaged                       | seconds_to_triaged |
| <br> |                                            | |
| x-ibm-ttp-tagging | name                                       | tactic |
| x-ibm-ttp-tagging | extensions.mitre-attack-ext.tactic_id      | tactic_id |
| x-ibm-ttp-tagging | extensions.mitre-attack-ext.technique_name | technique |
| x-ibm-ttp-tagging | extensions.mitre-attack-ext.technique_id   | technique_id |
| <br> |                                            | |
| x-oca-asset | ip_refs                                    | local_ip |
| x-oca-asset | ip_refs                                    | external_ip |
| x-oca-asset | mac_refs                                   | mac_address |
| x-oca-asset | hostname                                   | hostname |
| x-oca-asset | device_id                                  | device_id |
| x-oca-asset | x_cid                                      | cid |
| x-oca-asset | host_type                                  | product_type_desc |
| x-oca-asset | x_instance_id                              | instance_id |
| x-oca-asset | x_host_type_number                         | product_type |
| x-oca-asset | x_first_seen                               | first_seen |
| x-oca-asset | x_last_seen                                | last_seen |
| x-oca-asset | x_bios_manufacturer                        | bios_manufacturer |
| x-oca-asset | x_bios_version                             | bios_version |
| x-oca-asset | x_last_modified                            | modified_timestamp |
| x-oca-asset | x_service_provider                         | service_provider |
| x-oca-asset | x_service_account_id                       | service_provider_account_id |
| x-oca-asset | x_status                                   | status |
| x-oca-asset | x_system_product_name                      | system_product_name |
| x-oca-asset | x_system_manufacturer                      | system_manufacturer |
| x-oca-asset | x_agent_ref                                | agent_local_time |
| x-oca-asset | x_agent_ref                                | agent_version |
| x-oca-asset | x_device_groups                            | groups |
| x-oca-asset | os_ref                                     | platform_name |
| <br> |                                            | |
| x-crowdstrike-edr-agent | load_flags | agent_load_flags |
| x-crowdstrike-edr-agent | local_time                                 | agent_local_time |
| x-crowdstrike-edr-agent | version                                    | agent_version |
| x-crowdstrike-edr-agent | config_id_base                             | config_id_base |
| x-crowdstrike-edr-agent | config_id_build                      | config_id_build |
| x-crowdstrike-edr-agent | config_id_platform                   | config_id_platform |
| <br> |                                            | | 
