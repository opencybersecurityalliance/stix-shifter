##### Updated on 05/08/24
## Symantec
### Results STIX Domain Objects
* Identity
* Observed Data
<br>
### Supported STIX Operators
*Comparison AND/OR operators are inside the observation while observation AND/OR operators are between observations (square brackets).*

| STIX Operator | Data Source Operator |
|--|--|
| AND (Comparison) | AND |
| OR (Comparison) | OR |
| = | : |
| != | : |
| > | :{value TO \*} |
| >= | :\[value TO \*} |
| < | :{* TO value} |
| <= | :{* TO value] |
| IN | :(value) |
| LIKE | :value* |
| MATCHES | :/value/ |
| OR (Observation) | OR |
| AND (Observation) | OR |
| <br> | |
### Searchable STIX objects and properties
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **ipv4-addr**:value | device_ip, connection.src_ip, connection.dst_ip, device_public_ip, device_networks.ipv4, device_networks.gateway_ip |
| **ipv4-addr**:resolves_to_refs[*].value | device_mac, device_networks.mac, device_networks.gateway_mac |
| **ipv6-addr**:value | device_ip, connection.src_ip, connection.dst_ip, device_networks.ipv6 |
| **ipv6-addr**:resolves_to_refs[*].value | device_mac, device_networks.mac |
| **mac-addr**:value | device_mac, device_networks.mac, device_networks.gateway_mac |
| **network-traffic**:src_ref.value | connection.src_ip |
| **network-traffic**:dst_ref.value | connection.dst_ip |
| **network-traffic**:dst_port | connection.dst_port |
| **network-traffic**:src_port | connection.src_port |
| **network-traffic**:protocols[*] | connection.protocol_id |
| **network-traffic**:src_byte_count | connection.bytes_upload |
| **network-traffic**:dst_byte_count | connection.bytes_download |
| **network-traffic**:x_connection_direction | connection.direction_id |
| **process**:pid | actor.pid, process.pid, parent.pid |
| **process**:command_line | actor.cmd_line, process.cmd_line, parent.cmd_line, startup_app.cmd_line |
| **process**:name | actor.app_name, process.app_name, parent.app_name |
| **process**:created | actor.start_time, process.start_time, parent.start_time |
| **process**:x_process_tid | actor.tid, process.tid |
| **process**:x_process_uid | actor.uid, process.uid, parent.uid |
| **process**:creator_user_ref.user_id | actor.user.name, process.user.name |
| **process**:creator_user_ref.account_login | actor.user.logon_name |
| **process**:binary_ref.name | actor.file.name, process.file.name, parent.file.name, startup_app.file.name |
| **process**:binary_ref.parent_directory_ref.path | actor.file.path, process.file.path, parent.file.path, startup_app.file.path |
| **process**:binary_ref.hashes.MD5 | actor.file.md5, process.file.md5, parent.file.md5, startup_app.file.md5 |
| **process**:binary_ref.hashes.'SHA-256' | actor.file.sha2, process.file.sha2, parent.file.sha2, startup_app.file.sha2 |
| **process**:binary_ref.hashes.'SHA-1' | actor.file.c, process.file.sha1, parent.file.sha1, startup_app.file.sha1 |
| **process**:binary_ref.size | actor.file.size, process.file.size, startup_app.file.size |
| **user-account**:user_id | user.name, actor.user.name, session.user.name |
| **user-account**:account_login | actor.user.logon_name, session.user.logon_name |
| **user-account**:is_privileged | actor.user.is_admin, session.user.is_admin |
| **user-account**:x_user_domain | actor.user.domain, session.user.domain |
| **user-account**:x_user_sid | user.sid, actor.user.sid, session.user.sid |
| **user-account**:x_user_uid | user.uid |
| **file**:name | file.name, directory.name, actor.file.name, parent.file.name, process.file.name, module.name, startup_app.file.name |
| **file**:size | file.size, actor.file.size, module.size, process.file.size, startup_app.file.size |
| **file**:parent_directory_ref.path | file.folder, directory.folder, actor.file.folder, parent.file.folder, process.file.folder, module.folder, startup_app.file.folder |
| **file**:hashes.MD5 | file.md5, actor.file.md5, module.md5, parent.file.md5, process.file.md5, startup_app.file.md5 |
| **file**:hashes.'SHA-256' | file.sha2, actor.file.sha2, module.sha2, parent.file.sha2, process.file.sha2, startup_app.file.sha2 |
| **file**:hashes.'SHA-1' | file.sha1, actor.file.sha1, parent.file.sha1, process.file.sha1, startup_app.file.sha1 |
| **file**:created | actor.file.created, parent.file.created, process.file.created, startup_app.file.created |
| **file**:modified | actor.file.modified, process.file.modified, startup_app.file.modified |
| **file**:x_file_type | file.type_id, actor.file.type_id, process.file.type_id |
| **file**:x_rep_score | file.rep_score |
| **file**:x_file_version | file.version |
| **file**:x_open_mode | open_mode |
| **file**:x_content_type | file.content_type.type_id |
| **x509-certificate**:issuer | actor.file.signature_issuer |
| **x509-certificate**:serial_number | actor.file.signature_serial_number |
| **x509-certificate**:validity_not_before | actor.file.signature_created_date, actor.module.signature_created_date, file.signature_created_date, parent.signature_created_date, process.signature_created_date, directory.signature_created_date, startup_app.file.signature_created_date |
| **x509-certificate**:signature_algorithm | actor.file.signature_fingerprints.algorithm, actor.module.signature_fingerprints.algorithm, file.signature_fingerprints.algorithm, module.signature_fingerprints.algorithm, parent.file.signature_fingerprints.algorithm, parent.module.signature_fingerprints.algorithm, process.file.signature_fingerprints.algorithm, process.module.signature_fingerprints.algorithm, directory.signature_fingerprints.algorithm, startup_app.file.signature_fingerprints.algorithm |
| **x509-certificate**:x_signature_level_id | actor.file.signature_level_id, file.signature_level_id, parent.file.signature_level_id, process.file.signature_level_id, directory.signature_level_id, startup_app.file.signature_level_id |
| **x509-certificate**:x_signature_company_name | actor.file.signature_company_name, file.signature_company_name, module.signature_company_name, parent.file.signature_company_name, process.file.signature_company_name |
| **x509-certificate**:x_signature_value | actor.file.signature_value |
| **x509-certificate**:x_signature_value_ids | actor.file.signature_value_ids, process.file.signature_value_ids, startup_app.file.signature_value_ids |
| **directory**:path | file.folder, directory.folder, actor.file.folder, parent.file.folder, process.file.folder, module.folder, startup_app.file.folder |
| **email-addr**:value | email.header_from, email.header_to |
| **email-message**:from_ref | email.header_from |
| **email-message**:to_refs[*] | email.header_to |
| **email-message**:subject | email.header_subject |
| **email-message**:x_email_direction | email.direction_id |
| **email-message**:x_email_uid | email_uid |
| **windows-registry-key**:key | reg_key.path |
| **windows-registry-key**:values[*].data | reg_value.data |
| **windows-registry-key**:values[*].name | reg_value.name |
| **windows-registry-key**:values[*].data_type | reg_value.type_id |
| **software**:name | device_os_name |
| **software**:version | device_os_ver |
| **software**:x_os_type | device_os_type_id |
| **url**:value | url.text, file.url.text, connection.url.text |
| **domain-name**:value | device_domain |
| **x-oca-event**:code | uuid |
| **x-oca-event**:severity | severity_id |
| **x-oca-event**:category | category_id |
| **x-oca-event**:action | type |
| **x-oca-event**:description | message |
| **x-oca-event**:provider | product_name |
| **x-oca-event**:x_feature_name | feature_name |
| **x-oca-event**:outcome | id |
| **x-oca-event**:created | time |
| **x-oca-event**:x_event_status | status_id |
| **x-oca-event**:host_ref.hostname | device_name |
| **x-oca-event**:host_ref.host_type | device_type |
| **x-oca-event**:file_ref.name | file.name |
| **x-oca-event**:process_ref.pid | actor.pid |
| **x-oca-event**:process_ref.name | actor.app_name |
| **x-oca-event**:process_ref.command_line | actor.cmd_line |
| **x-oca-event**:parent_process_ref.pid | parent.pid |
| **x-oca-event**:parent_process_ref.name | parent.app_name |
| **x-oca-event**:parent_process_ref.command_line | parent.cmd_line |
| **x-oca-event**:process_ref.binary_ref.name | actor.file.name |
| **x-oca-event**:process_ref.creator_user_ref.user_id | actor.user.name |
| **x-oca-event**:registry_ref.key | reg_key.path, reg_value.path |
| **x-oca-event**:url_ref.value | url.text |
| **x-oca-event**:domain_ref.value | device_domain |
| **x-oca-event**:network_ref.protocols[*] | connection.protocol_id |
| **x-oca-event**:user_ref.user_id | user.name |
| **x-oca-event**:x_event_type | type_id |
| **x-oca-event**:x_event_id | event_id |
| **x-oca-event**:x_provider_version | product_ver |
| **x-oca-event**:x_command_uid | command_uid |
| **x-oca-event**:x_event_data | data |
| **x-oca-asset**:hostname | device_name |
| **x-oca-asset**:host_type | device_type |
| **x-oca-asset**:x_host_group | device_group |
| **x-oca-asset**:mac_refs[*].value | device_mac |
| **x-oca-asset**:ip_ref[*].value | device_ip |
| **x-oca-asset**:os_ref.name | device_os_name |
| **x-oca-asset**:os_ref.version | device_os_ver |
| **x-oca-asset**:domain_ref.value | device_domain |
| **x-oca-geo**:name | device_location.desc |
| **x-oca-geo**:x_is_on_premises | device_location.on_premises |
| **x-ibm-finding**:name | threat.name |
| **x-ibm-finding**:severity | threat.risk_id |
| **x-ibm-finding**:alert_id | threat.id |
| **x-ibm-finding**:finding_type | reason_id |
| **x-ibm-finding**:x_threat_type_id | threat.type_id |
| **x-ibm-finding**:x_info_provider | threat.provider |
| **x-ibm-finding**:ttp_tagging_refs[*].name | attacks.technique_name |
| **x-ibm-finding**:ttp_tagging_refs[*].extensions.'mitre-attack-ext'.technique_id | attacks.technique_uid |
| **x-ibm-finding**:ttp_tagging_refs[*].extensions.'mitre-attack-ext'.technique_name | attacks.technique_name |
| **x-ibm-finding**:ttp_tagging_refs[*].extensions.'mitre-attack-ext'.tactic_id | attacks.tactic_uids |
| **x-ibm-ttp-tagging**:name | attacks.technique_name |
| **x-ibm-ttp-tagging**:extensions.'mitre-attack-ext'.tactic_id | attacks.tactic_uids |
| **x-ibm-ttp-tagging**:extensions.'mitre-attack-ext'.technique_id | attacks.technique_uid |
| **x-ibm-ttp-tagging**:extensions.'mitre-attack-ext'.technique_name | attacks.technique_name |
| **x-symantec-policy**:name | policy.name |
| **x-symantec-policy**:effective_date | policy.effective_date |
| **x-symantec-policy**:rule_group_name | policy.rule_group_name |
| **x-symantec-policy**:rule_name | policy.rule_name |
| **x-symantec-policy**:rule_category | policy.rule_category_id |
| **x-symantec-policy**:type_id | policy.type_id |
| **x-symantec-policy**:rule_description | policy.rule_desc |
| **x-symantec-policy**:version | policy.version |
| **x-symantec-policy**:states | policy.state_ids |
| **x-user-session**:id | session.id, actor.session.id |
| **x-user-session**:is_admin | session.is_admin |
| **x-user-session**:is_remote | session.remote, actor.session.remote |
| **x-user-session**:user_ref.user_id | session.user.name, actor.session.user.name |
| **x-user-session**:user_ref.account_login | session.user.logon_name, actor.session.user.logon_name |
| **x-user-session**:user_ref.is_privileged | session.user.is_admin, actor.session.user.is_admin |
| **x-user-session**:user_ref.x_domain | session.user.domain, actor.session.user.domain |
| **x-user-session**:user_ref.x_sid | session.user.sid |
| **x-kernel-resource**:name | kernel.name |
| **x-kernel-resource**:type_id | kernel.type_id |
| **x-peripheral-device**:class | peripheral_device.class |
| **x-peripheral-device**:instance_uid | peripheral_device.instance_uid |
| **x-peripheral-device**:name | peripheral_device.name |
| **x-peripheral-device**:serial | peripheral_device.serial |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| ipv4-addr | value | device_ip |
| ipv4-addr | value | connection.src_ip |
| ipv4-addr | value | connection.dst_ip |
| ipv4-addr | value | device_public_ip |
| ipv4-addr | value | device_networks.ipv4 |
| ipv4-addr | value | device_networks.gateway_ip |
| ipv4-addr | resolves_to_refs[*].value | device_mac |
| ipv4-addr | resolves_to_refs[*].value | device_networks.mac |
| ipv4-addr | resolves_to_refs[*].value | device_networks.gateway_mac |
| <br> | | |
| ipv6-addr | value | device_ip |
| ipv6-addr | value | connection.src_ip |
| ipv6-addr | value | connection.dst_ip |
| ipv6-addr | value | device_networks.ipv6 |
| ipv6-addr | resolves_to_refs[*].value | device_mac |
| ipv6-addr | resolves_to_refs[*].value | device_networks.mac |
| <br> | | |
| mac-addr | value | device_mac |
| mac-addr | value | device_networks.mac |
| mac-addr | value | device_networks.gateway_mac |
| <br> | | |
| network-traffic | src_ref.value | connection.src_ip |
| network-traffic | dst_ref.value | connection.dst_ip |
| network-traffic | dst_port | connection.dst_port |
| network-traffic | src_port | connection.src_port |
| network-traffic | protocols[*] | connection.protocol_id |
| network-traffic | src_byte_count | connection.bytes_upload |
| network-traffic | dst_byte_count | connection.bytes_download |
| network-traffic | x_connection_direction | connection.direction_id |
| <br> | | |
| process | pid | actor.pid |
| process | pid | process.pid |
| process | pid | parent.pid |
| process | command_line | actor.cmd_line |
| process | command_line | process.cmd_line |
| process | command_line | parent.cmd_line |
| process | command_line | startup_app.cmd_line |
| process | name | actor.app_name |
| process | name | process.app_name |
| process | name | parent.app_name |
| process | created | actor.start_time |
| process | created | process.start_time |
| process | created | parent.start_time |
| process | x_process_tid | actor.tid |
| process | x_process_tid | process.tid |
| process | x_process_uid | actor.uid |
| process | x_process_uid | process.uid |
| process | x_process_uid | parent.uid |
| process | creator_user_ref.user_id | actor.user.name |
| process | creator_user_ref.user_id | process.user.name |
| process | creator_user_ref.account_login | actor.user.logon_name |
| process | binary_ref.name | actor.file.name |
| process | binary_ref.name | process.file.name |
| process | binary_ref.name | parent.file.name |
| process | binary_ref.name | startup_app.file.name |
| process | binary_ref.parent_directory_ref.path | actor.file.path |
| process | binary_ref.parent_directory_ref.path | process.file.path |
| process | binary_ref.parent_directory_ref.path | parent.file.path |
| process | binary_ref.parent_directory_ref.path | startup_app.file.path |
| process | binary_ref.hashes.MD5 | actor.file.md5 |
| process | binary_ref.hashes.MD5 | process.file.md5 |
| process | binary_ref.hashes.MD5 | parent.file.md5 |
| process | binary_ref.hashes.MD5 | startup_app.file.md5 |
| process | binary_ref.hashes.'SHA-256' | actor.file.sha2 |
| process | binary_ref.hashes.'SHA-256' | process.file.sha2 |
| process | binary_ref.hashes.'SHA-256' | parent.file.sha2 |
| process | binary_ref.hashes.'SHA-256' | startup_app.file.sha2 |
| process | binary_ref.hashes.'SHA-1' | actor.file.c |
| process | binary_ref.hashes.'SHA-1' | process.file.sha1 |
| process | binary_ref.hashes.'SHA-1' | parent.file.sha1 |
| process | binary_ref.hashes.'SHA-1' | startup_app.file.sha1 |
| process | binary_ref.size | actor.file.size |
| process | binary_ref.size | process.file.size |
| process | binary_ref.size | startup_app.file.size |
| <br> | | |
| user-account | user_id | user.name |
| user-account | user_id | actor.user.name |
| user-account | user_id | session.user.name |
| user-account | account_login | actor.user.logon_name |
| user-account | account_login | session.user.logon_name |
| user-account | is_privileged | actor.user.is_admin |
| user-account | is_privileged | session.user.is_admin |
| user-account | x_user_domain | actor.user.domain |
| user-account | x_user_domain | session.user.domain |
| user-account | x_user_sid | user.sid |
| user-account | x_user_sid | actor.user.sid |
| user-account | x_user_sid | session.user.sid |
| user-account | x_user_uid | user.uid |
| <br> | | |
| file | name | file.name |
| file | name | directory.name |
| file | name | actor.file.name |
| file | name | parent.file.name |
| file | name | process.file.name |
| file | name | module.name |
| file | name | startup_app.file.name |
| file | size | file.size |
| file | size | actor.file.size |
| file | size | module.size |
| file | size | process.file.size |
| file | size | startup_app.file.size |
| file | parent_directory_ref.path | file.folder |
| file | parent_directory_ref.path | directory.folder |
| file | parent_directory_ref.path | actor.file.folder |
| file | parent_directory_ref.path | parent.file.folder |
| file | parent_directory_ref.path | process.file.folder |
| file | parent_directory_ref.path | module.folder |
| file | parent_directory_ref.path | startup_app.file.folder |
| file | hashes.MD5 | file.md5 |
| file | hashes.MD5 | actor.file.md5 |
| file | hashes.MD5 | module.md5 |
| file | hashes.MD5 | parent.file.md5 |
| file | hashes.MD5 | process.file.md5 |
| file | hashes.MD5 | startup_app.file.md5 |
| file | hashes.'SHA-256' | file.sha2 |
| file | hashes.'SHA-256' | actor.file.sha2 |
| file | hashes.'SHA-256' | module.sha2 |
| file | hashes.'SHA-256' | parent.file.sha2 |
| file | hashes.'SHA-256' | process.file.sha2 |
| file | hashes.'SHA-256' | startup_app.file.sha2 |
| file | hashes.'SHA-1' | file.sha1 |
| file | hashes.'SHA-1' | actor.file.sha1 |
| file | hashes.'SHA-1' | parent.file.sha1 |
| file | hashes.'SHA-1' | process.file.sha1 |
| file | hashes.'SHA-1' | startup_app.file.sha1 |
| file | created | actor.file.created |
| file | created | parent.file.created |
| file | created | process.file.created |
| file | created | startup_app.file.created |
| file | modified | actor.file.modified |
| file | modified | process.file.modified |
| file | modified | startup_app.file.modified |
| file | x_file_type | file.type_id |
| file | x_file_type | actor.file.type_id |
| file | x_file_type | process.file.type_id |
| file | x_rep_score | file.rep_score |
| file | x_file_version | file.version |
| file | x_open_mode | open_mode |
| file | x_content_type | file.content_type.type_id |
| <br> | | |
| x509-certificate | issuer | actor.file.signature_issuer |
| x509-certificate | serial_number | actor.file.signature_serial_number |
| x509-certificate | validity_not_before | actor.file.signature_created_date |
| x509-certificate | validity_not_before | actor.module.signature_created_date |
| x509-certificate | validity_not_before | file.signature_created_date |
| x509-certificate | validity_not_before | parent.signature_created_date |
| x509-certificate | validity_not_before | process.signature_created_date |
| x509-certificate | validity_not_before | directory.signature_created_date |
| x509-certificate | validity_not_before | startup_app.file.signature_created_date |
| x509-certificate | signature_algorithm | actor.file.signature_fingerprints.algorithm |
| x509-certificate | signature_algorithm | actor.module.signature_fingerprints.algorithm |
| x509-certificate | signature_algorithm | file.signature_fingerprints.algorithm |
| x509-certificate | signature_algorithm | module.signature_fingerprints.algorithm |
| x509-certificate | signature_algorithm | parent.file.signature_fingerprints.algorithm |
| x509-certificate | signature_algorithm | parent.module.signature_fingerprints.algorithm |
| x509-certificate | signature_algorithm | process.file.signature_fingerprints.algorithm |
| x509-certificate | signature_algorithm | process.module.signature_fingerprints.algorithm |
| x509-certificate | signature_algorithm | directory.signature_fingerprints.algorithm |
| x509-certificate | signature_algorithm | startup_app.file.signature_fingerprints.algorithm |
| x509-certificate | x_signature_level_id | actor.file.signature_level_id |
| x509-certificate | x_signature_level_id | file.signature_level_id |
| x509-certificate | x_signature_level_id | parent.file.signature_level_id |
| x509-certificate | x_signature_level_id | process.file.signature_level_id |
| x509-certificate | x_signature_level_id | directory.signature_level_id |
| x509-certificate | x_signature_level_id | startup_app.file.signature_level_id |
| x509-certificate | x_signature_company_name | actor.file.signature_company_name |
| x509-certificate | x_signature_company_name | file.signature_company_name |
| x509-certificate | x_signature_company_name | module.signature_company_name |
| x509-certificate | x_signature_company_name | parent.file.signature_company_name |
| x509-certificate | x_signature_company_name | process.file.signature_company_name |
| x509-certificate | x_signature_value | actor.file.signature_value |
| x509-certificate | x_signature_value_ids | actor.file.signature_value_ids |
| x509-certificate | x_signature_value_ids | process.file.signature_value_ids |
| x509-certificate | x_signature_value_ids | startup_app.file.signature_value_ids |
| <br> | | |
| directory | path | file.folder |
| directory | path | directory.folder |
| directory | path | actor.file.folder |
| directory | path | parent.file.folder |
| directory | path | process.file.folder |
| directory | path | module.folder |
| directory | path | startup_app.file.folder |
| <br> | | |
| email-addr | value | email.header_from |
| email-addr | value | email.header_to |
| <br> | | |
| email-message | from_ref | email.header_from |
| email-message | to_refs[*] | email.header_to |
| email-message | subject | email.header_subject |
| email-message | x_email_direction | email.direction_id |
| email-message | x_email_uid | email_uid |
| <br> | | |
| windows-registry-key | key | reg_key.path |
| windows-registry-key | values[*].data | reg_value.data |
| windows-registry-key | values[*].name | reg_value.name |
| windows-registry-key | values[*].data_type | reg_value.type_id |
| <br> | | |
| software | name | device_os_name |
| software | version | device_os_ver |
| software | x_os_type | device_os_type_id |
| <br> | | |
| url | value | url.text |
| url | value | file.url.text |
| url | value | connection.url.text |
| <br> | | |
| domain-name | value | device_domain |
| <br> | | |
| x-oca-event | code | uuid |
| x-oca-event | severity | severity_id |
| x-oca-event | category | category_id |
| x-oca-event | action | type |
| x-oca-event | description | message |
| x-oca-event | provider | product_name |
| x-oca-event | x_feature_name | feature_name |
| x-oca-event | outcome | id |
| x-oca-event | created | time |
| x-oca-event | x_event_status | status_id |
| x-oca-event | host_ref.hostname | device_name |
| x-oca-event | host_ref.host_type | device_type |
| x-oca-event | file_ref.name | file.name |
| x-oca-event | process_ref.pid | actor.pid |
| x-oca-event | process_ref.name | actor.app_name |
| x-oca-event | process_ref.command_line | actor.cmd_line |
| x-oca-event | parent_process_ref.pid | parent.pid |
| x-oca-event | parent_process_ref.name | parent.app_name |
| x-oca-event | parent_process_ref.command_line | parent.cmd_line |
| x-oca-event | process_ref.binary_ref.name | actor.file.name |
| x-oca-event | process_ref.creator_user_ref.user_id | actor.user.name |
| x-oca-event | registry_ref.key | reg_key.path |
| x-oca-event | registry_ref.key | reg_value.path |
| x-oca-event | url_ref.value | url.text |
| x-oca-event | domain_ref.value | device_domain |
| x-oca-event | network_ref.protocols[*] | connection.protocol_id |
| x-oca-event | user_ref.user_id | user.name |
| x-oca-event | x_event_type | type_id |
| x-oca-event | x_event_id | event_id |
| x-oca-event | x_provider_version | product_ver |
| x-oca-event | x_command_uid | command_uid |
| x-oca-event | x_event_data | data |
| <br> | | |
| x-oca-asset | hostname | device_name |
| x-oca-asset | host_type | device_type |
| x-oca-asset | x_host_group | device_group |
| x-oca-asset | mac_refs[*].value | device_mac |
| x-oca-asset | ip_ref[*].value | device_ip |
| x-oca-asset | os_ref.name | device_os_name |
| x-oca-asset | os_ref.version | device_os_ver |
| x-oca-asset | domain_ref.value | device_domain |
| <br> | | |
| x-oca-geo | name | device_location.desc |
| x-oca-geo | x_is_on_premises | device_location.on_premises |
| <br> | | |
| x-ibm-finding | name | threat.name |
| x-ibm-finding | severity | threat.risk_id |
| x-ibm-finding | alert_id | threat.id |
| x-ibm-finding | finding_type | reason_id |
| x-ibm-finding | x_threat_type_id | threat.type_id |
| x-ibm-finding | x_info_provider | threat.provider |
| x-ibm-finding | ttp_tagging_refs[*].name | attacks.technique_name |
| x-ibm-finding | ttp_tagging_refs[*].extensions.'mitre-attack-ext'.technique_id | attacks.technique_uid |
| x-ibm-finding | ttp_tagging_refs[*].extensions.'mitre-attack-ext'.technique_name | attacks.technique_name |
| x-ibm-finding | ttp_tagging_refs[*].extensions.'mitre-attack-ext'.tactic_id | attacks.tactic_uids |
| <br> | | |
| x-ibm-ttp-tagging | name | attacks.technique_name |
| x-ibm-ttp-tagging | extensions.'mitre-attack-ext'.tactic_id | attacks.tactic_uids |
| x-ibm-ttp-tagging | extensions.'mitre-attack-ext'.technique_id | attacks.technique_uid |
| x-ibm-ttp-tagging | extensions.'mitre-attack-ext'.technique_name | attacks.technique_name |
| <br> | | |
| x-symantec-policy | name | policy.name |
| x-symantec-policy | effective_date | policy.effective_date |
| x-symantec-policy | rule_group_name | policy.rule_group_name |
| x-symantec-policy | rule_name | policy.rule_name |
| x-symantec-policy | rule_category | policy.rule_category_id |
| x-symantec-policy | type_id | policy.type_id |
| x-symantec-policy | rule_description | policy.rule_desc |
| x-symantec-policy | version | policy.version |
| x-symantec-policy | states | policy.state_ids |
| <br> | | |
| x-user-session | id | session.id |
| x-user-session | id | actor.session.id |
| x-user-session | is_admin | session.is_admin |
| x-user-session | is_remote | session.remote |
| x-user-session | is_remote | actor.session.remote |
| x-user-session | user_ref.user_id | session.user.name |
| x-user-session | user_ref.user_id | actor.session.user.name |
| x-user-session | user_ref.account_login | session.user.logon_name |
| x-user-session | user_ref.account_login | actor.session.user.logon_name |
| x-user-session | user_ref.is_privileged | session.user.is_admin |
| x-user-session | user_ref.is_privileged | actor.session.user.is_admin |
| x-user-session | user_ref.x_domain | session.user.domain |
| x-user-session | user_ref.x_domain | actor.session.user.domain |
| x-user-session | user_ref.x_sid | session.user.sid |
| <br> | | |
| x-kernel-resource | name | kernel.name |
| x-kernel-resource | type_id | kernel.type_id |
| <br> | | |
| x-peripheral-device | class | peripheral_device.class |
| x-peripheral-device | instance_uid | peripheral_device.instance_uid |
| x-peripheral-device | name | peripheral_device.name |
| x-peripheral-device | serial | peripheral_device.serial |
| <br> | | |