##### Updated on 01/22/24
## Nozomi
### Results STIX Domain Objects
* Identity
* Observed Data
<br>
### Supported STIX Operators
*Comparison AND/OR operators are inside the observation while observation AND/OR operators are between observations (square brackets).*

| STIX Operator | Data Source Operator |
|--|--|
| AND (Comparison) | \| |
| OR (Comparison) | OR |
| = | == |
| != | != |
| > | > |
| >= | >= |
| < | < |
| <= | <= |
| IN | in? |
| LIKE | include? |
| ISSUBSET | in_subnet? |
| OR (Observation) | OR |
| AND (Observation) | OR |
| <br> | |
### Searchable STIX objects and properties
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **ipv4-addr**:value | ip_src, ip_dst |
| **ipv6-addr**:value | ip_src, ip_dst |
| **network-traffic**:src_ref.value | ip_src |
| **network-traffic**:dst_ref.value | ip_dst |
| **network-traffic**:dst_port | port_dst |
| **network-traffic**:src_port | port_src |
| **network-traffic**:protocols[*] | protocol, transport_protocol |
| **mac-addr**:value | mac_src, mac_dst |
| **file**:name | properties/details_yara_file/value, properties/process/image_path |
| **file**:hashes.'SHA-256' | properties/details_hash_SHA256/value, properties/process/image_hash_sha256 |
| **file**:hashes.'SHA-1' | properties/details_hash_SHA1/value |
| **file**:hashes.MD5 | properties/details_hash_MD5/value |
| **file**:size | properties/details_file_size/value |
| **file**:parent_directory_ref.path | properties/process/image_path |
| **process**:pid | properties/process/pid |
| **process**:command_line | properties/process/command_line |
| **process**:creator_user_ref.user_id | properties/process/user |
| **process**:binary_ref.name | properties/process/image_path |
| **process**:binary_ref.parent_directory_ref.path | properties/process/image_path |
| **process**:parent_ref.command_line | properties/process/ancestry |
| **process**:parent_ref.binary_ref.name | properties/process/ancestry |
| **process**:parent_ref.binary_ref.parent_directory_ref.path | properties/process/ancestry |
| **user-account**:user_id | properties/process/user |
| **directory**:path | properties/process/image_path |
| **x-ibm-finding**:alert_id | id |
| **x-ibm-finding**:finding_type | threat_name |
| **x-ibm-finding**:name | type_name |
| **x-ibm-finding**:description | description |
| **x-ibm-finding**:time_observed | time |
| **x-ibm-finding**:start | created_time |
| **x-ibm-finding**:end | closed_time |
| **x-ibm-finding**:severity | risk |
| **x-ibm-finding**:src_ip_ref | ip_src |
| **x-ibm-finding**:dst_ip_ref | ip_dst |
| **x-ibm-finding**:rule_names[*] | trigger_type |
| **x-ibm-finding**:x_alert_type_id | type_id |
| **x-ibm-finding**:x_is_cybersecurity_alert | is_security |
| **x-ibm-finding**:x_is_incident_alert | is_incident |
| **x-ibm-finding**:x_sensor_host | appliance_host |
| **x-ibm-finding**:x_sensor_interface | capture_device |
| **x-ibm-finding**:x_threat_name | threat_name |
| **x-ibm-finding**:x_rule_id | trigger_id |
| **x-ibm-finding**:x_is_acknowledged | ack |
| **x-ibm-finding**:x_alert_status | status |
| **x-ibm-finding**:x_user_note | note |
| **x-ibm-finding**:x_cause | properties/cause |
| **x-ibm-finding**:x_solution | properties/solution |
| **x-ibm-finding**:x_message | properties/message |
| **x-ibm-finding**:x_cve_references | properties/cve_references |
| **x-ibm-finding**:x_network_learnable | properties/network_learnable |
| **x-ibm-ttp-tagging**:name | properties |
| **x-ibm-ttp-tagging**:extensions.'mitre-attack-ext'.technique_id | properties, mitre_attack_techniques |
| **x-ibm-ttp-tagging**:extensions.'mitre-attack-ext'.technique_name | properties |
| **x-ibm-ttp-tagging**:extensions.'mitre-attack-ext'.tactic_name | properties, mitre_attack_tactics |
| **x-nozomi-info**:zone | zone_dst, zone_src |
| **x-nozomi-info**:roles | dst_roles, src_roles |
| **x-nozomi-info**:label | label_src, label_dst |
| **x-nozomi-info**:is_public | properties/is_dst_public, properties/is_src_public |
| **x-nozomi-info**:is_node_learned | properties/is_dst_node_learned, properties/is_src_node_learned |
| **x-nozomi-info**:is_reputation_bad | properties/is_dst_reputation_bad, properties/is_src_reputation_bad |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| ipv4-addr | value | ip_src |
| ipv4-addr | value | ip_dst |
| <br> | | |
| ipv6-addr | value | ip_src |
| ipv6-addr | value | ip_dst |
| <br> | | |
| network-traffic | src_ref.value | ip_src |
| network-traffic | dst_ref.value | ip_dst |
| network-traffic | dst_port | port_dst |
| network-traffic | src_port | port_src |
| network-traffic | protocols[*] | protocol |
| network-traffic | protocols[*] | transport_protocol |
| <br> | | |
| mac-addr | value | mac_src |
| mac-addr | value | mac_dst |
| <br> | | |
| file | name | properties/details_yara_file/value |
| file | name | properties/process/image_path |
| file | hashes.'SHA-256' | properties/details_hash_SHA256/value |
| file | hashes.'SHA-256' | properties/process/image_hash_sha256 |
| file | hashes.'SHA-1' | properties/details_hash_SHA1/value |
| file | hashes.MD5 | properties/details_hash_MD5/value |
| file | size | properties/details_file_size/value |
| file | parent_directory_ref.path | properties/process/image_path |
| <br> | | |
| process | pid | properties/process/pid |
| process | command_line | properties/process/command_line |
| process | creator_user_ref.user_id | properties/process/user |
| process | binary_ref.name | properties/process/image_path |
| process | binary_ref.parent_directory_ref.path | properties/process/image_path |
| process | parent_ref.command_line | properties/process/ancestry |
| process | parent_ref.binary_ref.name | properties/process/ancestry |
| process | parent_ref.binary_ref.parent_directory_ref.path | properties/process/ancestry |
| <br> | | |
| user-account | user_id | properties/process/user |
| <br> | | |
| directory | path | properties/process/image_path |
| <br> | | |
| x-ibm-finding | alert_id | id |
| x-ibm-finding | finding_type | threat_name |
| x-ibm-finding | name | type_name |
| x-ibm-finding | description | description |
| x-ibm-finding | time_observed | time |
| x-ibm-finding | start | created_time |
| x-ibm-finding | end | closed_time |
| x-ibm-finding | severity | risk |
| x-ibm-finding | src_ip_ref | ip_src |
| x-ibm-finding | dst_ip_ref | ip_dst |
| x-ibm-finding | rule_names[*] | trigger_type |
| x-ibm-finding | x_alert_type_id | type_id |
| x-ibm-finding | x_is_cybersecurity_alert | is_security |
| x-ibm-finding | x_is_incident_alert | is_incident |
| x-ibm-finding | x_sensor_host | appliance_host |
| x-ibm-finding | x_sensor_interface | capture_device |
| x-ibm-finding | x_threat_name | threat_name |
| x-ibm-finding | x_rule_id | trigger_id |
| x-ibm-finding | x_is_acknowledged | ack |
| x-ibm-finding | x_alert_status | status |
| x-ibm-finding | x_user_note | note |
| x-ibm-finding | x_cause | properties/cause |
| x-ibm-finding | x_solution | properties/solution |
| x-ibm-finding | x_message | properties/message |
| x-ibm-finding | x_cve_references | properties/cve_references |
| x-ibm-finding | x_network_learnable | properties/network_learnable |
| <br> | | |
| x-ibm-ttp-tagging | name | properties |
| x-ibm-ttp-tagging | extensions.'mitre-attack-ext'.technique_id | properties |
| x-ibm-ttp-tagging | extensions.'mitre-attack-ext'.technique_id | mitre_attack_techniques |
| x-ibm-ttp-tagging | extensions.'mitre-attack-ext'.technique_name | properties |
| x-ibm-ttp-tagging | extensions.'mitre-attack-ext'.tactic_name | properties |
| x-ibm-ttp-tagging | extensions.'mitre-attack-ext'.tactic_name | mitre_attack_tactics |
| <br> | | |
| x-nozomi-info | zone | zone_dst |
| x-nozomi-info | zone | zone_src |
| x-nozomi-info | roles | dst_roles |
| x-nozomi-info | roles | src_roles |
| x-nozomi-info | label | label_src |
| x-nozomi-info | label | label_dst |
| x-nozomi-info | is_public | properties/is_dst_public |
| x-nozomi-info | is_public | properties/is_src_public |
| x-nozomi-info | is_node_learned | properties/is_dst_node_learned |
| x-nozomi-info | is_node_learned | properties/is_src_node_learned |
| x-nozomi-info | is_reputation_bad | properties/is_dst_reputation_bad |
| x-nozomi-info | is_reputation_bad | properties/is_src_reputation_bad |
| <br> | | |