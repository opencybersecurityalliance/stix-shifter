##### Updated on 05/15/23
## Carbon Black CB Response
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
| = | : |
| IN | : |
| != | : |
| > | : |
| >= | : |
| < | : |
| <= | : |
| OR (Observation) | or |
| AND (Observation) | or |
| <br> | |
### Searchable STIX objects and properties
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **network-traffic**:src_port | ipport |
| **network-traffic**:dst_port | ipport |
| **network-traffic**:src_ref.value | ipaddr, ipv6addr |
| **network-traffic**:dst_ref.value | ipaddr, ipv6addr |
| **ipv4-addr**:value | ipaddr |
| **ipv6-addr**:value | ipv6addr |
| **file**:name | process_name, childproc_name |
| **file**:hashes.MD5 | md5 |
| **file**:hashes.'SHA-256' | sha256 |
| **file**:hashes.parent_MD5 | parent_md5 |
| **file**:hashes.parent_SHA-256 | parent_sha256 |
| **file**:hashes.child_MD5 | childproc_md5 |
| **file**:hashes.child_SHA-256 | childproc_sha256 |
| **file**:hashes.filewrite_MD5 | filewrite_md5 |
| **file**:hashes.filewrite_SHA-256 | filewrite_sha256 |
| **file**:hashes.blocked_MD5 | blocked_md5 |
| **file**:hashes.blocked_SHA-256 | blocked_sha256 |
| **file**:hashes.crossproc_MD5 | crossproc_md5 |
| **file**:hashes.crossproc_SHA-256 | crossproc_sha256 |
| **file**:parent_directory_ref.path | path, modload |
| **process**:command_line | cmdline |
| **process**:created | start |
| **process**:pid | process_pid |
| **process**:name | process_name, crossproc_name |
| **process**:creator_user_ref.user_id | username |
| **process**:creator_user_ref.account_login | username |
| **process**:binary_ref.hashes.MD5 | md5 |
| **process**:binary_ref.hashes.'SHA-256' | sha256 |
| **process**:parent_ref.pid | parent_pid |
| **process**:parent_ref.name | parent_name |
| **process**:parent_ref.command_line | cmdline |
| **process**:parent_ref.binary_ref.hashes.MD5 | parent_md5 |
| **process**:parent_ref.binary_ref.hashes.'SHA-256' | parent_sha256 |
| **url**:value | domain |
| **domain-name**:value | domain, hostname |
| **user-account**:user_id | username |
| **directory**:path | path |
| **windows-registry-key**:key | regmod |
| **x-oca-event**:process_ref.pid | process_pid |
| **x-oca-event**:process_ref.name | process_name, crossproc_name |
| **x-oca-event**:process_ref.command_line | cmdline |
| **x-oca-event**:process_ref.binary_ref.name | process_name, childproc_name |
| **x-oca-event**:process_ref.creator_user_ref.user_id | username |
| **x-oca-event**:process_ref.creator_user_ref.account_login | username |
| **x-oca-event**:process_ref.parent_ref.name | parent_name |
| **x-oca-event**:process_ref.parent_ref.pid | parent_pid |
| **x-oca-event**:process_ref.parent_ref.command_line | cmdline |
| **x-oca-event**:process_ref.parent_ref.binary_ref.hashes.MD5 | parent_md5 |
| **x-oca-event**:process_ref.parent_ref.binary_ref.hashes.'SHA-256' | parent_sha256 |
| **x-oca-event**:process_ref.process_ref.creator_user_ref.user_id | username |
| **x-oca-event**:process_ref.process_ref.creator_user_ref.account_login | username |
| **x-oca-event**:parent_process_ref.name | parent_name |
| **x-oca-event**:parent_process_ref.pid | parent_pid |
| **x-oca-event**:parent_process_ref.command_line | cmdline |
| **x-oca-event**:parent_process_ref.binary_ref.hashes.MD5 | parent_md5 |
| **x-oca-event**:parent_process_ref.binary_ref.hashes.'SHA-256' | parent_sha256 |
| **x-oca-event**:parent_process_ref.creator_user_ref.user_id | username |
| **x-oca-event**:parent_process_ref.creator_user_ref.account_login | username |
| **x-oca-event**:domain_ref.value | domain, hostname |
| **x-oca-event**:file_ref.name | process_name, childproc_name |
| **x-oca-event**:host_ref.hostname | hostname |
| **x-oca-event**:host_ref.name | hostname |
| **x-oca-event**:registry_ref.key | regmod |
| **x-oca-asset**:domain | domain |
| **x-oca-asset**:hostname | hostname |
| **x-oca-asset**:ip | ipaddr, ipv6addr |
| **x-oca-asset**:name | hostname |
| **x-oca-asset**:type | host_type |
| **x-oca-asset**:os.name | os_type |
| **x-oca-asset**:os.platform | os_type |
| **x-cb-response**:hostname | hostname |
| **x-cb-response**:host_count | host_count |
| **x-cb-response**:host_type | host_type |
| **x-cb-response**:group | group |
| **x-cb-response**:os_type | os_type |
| **x-cb-response**:crossproc_type | crossproc_type |
| **x-cb-response**:crossproc_count | crossproc_count |
| **x-cb-response**:crossproc_name | crossproc_name |
| **x-cb-response**:tampered | tampered |
| **x-cb-response**:block_status | block_status |
| **x-cb-response**:digsig_result | digsig_result |
| **x-cb-response**:digsig_publisher | digsig_publisher |
| **x-cb-response**:digsig_issuer | digsig_issuer |
| **x-cb-response**:digsig_prog_name | digsig_prog_name |
| **x-cb-response**:digsig_sign_time | digsig_sign_time |
| **x-cb-response**:digsig_subject | digsig_subject |
| **x-cb-response**:has_emet_event | has_emet_event |
| **x-cb-response**:has_emet_config | has_emet_config |
| **x-cb-response**:file_desc | file_desc |
| **x-cb-response**:file_version | file_version |
| **x-cb-response**:filemod_count | filemod_count |
| **x-cb-response**:filemod | filemod |
| **x-cb-response**:regmod_count | regmod_count |
| **x-cb-response**:regmod | regmod |
| **x-cb-response**:blocked_status | blocked_status |
| **x-cb-response**:childproc_count | childproc_count |
| **x-cb-response**:childproc_name | childproc_name |
| **x-cb-response**:company_name | company_name |
| **x-cb-response**:copied_mod_len | copied_mod_len |
| **x-cb-response**:internal_name | internal_name |
| **x-cb-response**:is_64bit | is_64bit |
| **x-cb-response**:is_executable_image | is_executable_image |
| **x-cb-response**:last_server_update | last_server_update |
| **x-cb-response**:last_update | last_update |
| **x-cb-response**:legal_copyright | legal_copyright |
| **x-cb-response**:legal_trademark | legal_trademark |
| **x-cb-response**:modload | modload |
| **x-cb-response**:modload_count | modload_count |
| **x-cb-response**:netconn_count | netconn_count |
| **x-cb-response**:observed_filename | observed_filename |
| **x-cb-response**:orig_mod_len | orig_mod_len |
| **x-cb-response**:original_filename | original_filename |
| **x-cb-response**:parent_id | parent_id |
| **x-cb-response**:parent_name | parent_name |
| **x-cb-response**:private_build | private_build |
| **x-cb-response**:process_id | process_id |
| **x-cb-response**:product_desc | product_desc |
| **x-cb-response**:product_name | product_name |
| **x-cb-response**:product_version | product_version |
| **x-cb-response**:sensor_id | sensor_id |
| **x-cb-response**:special_build | special_build |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| directory | path | path |
| <br> | | |
| file | name | process_name |
| file | hashes.MD5 | process_md5 |
| file | hashes.SHA-256 | process_sha256 |
| file | parent_directory_ref | path |
| file | created | server_added_timestamp |
| file | name | original_filename |
| file | size | orig_mod_length |
| file | hashes.MD5 | md5 |
| <br> | | |
| ipv4-addr | value | interface_ip |
| <br> | | |
| process | creator_user_ref | username |
| process | created | start |
| process | name | process_name |
| process | binary_ref | process_name |
| process | pid | process_pid |
| process | x_id | id |
| process | x_unique_id | unique_id |
| process | name | parent_name |
| process | parent_ref | parent_name |
| process | pid | parent_pid |
| process | parent_ref | parent_pid |
| process | x_id | parent_id |
| process | x_unique_id | parent_unique_id |
| process | command_line | cmdline |
| <br> | | |
| user-account | user_id | username |
| <br> | | |
| x-cb-response | host_name | hostname |
| x-cb-response | host_type | host_type |
| x-cb-response | comms_ip | comms_ip |
| x-cb-response | os_type | os_type |
| x-cb-response | sensor_id | sensor_id |
| x-cb-response | group | group |
| x-cb-response | segment_id | segment_id |
| x-cb-response | terminated | terminated |
| x-cb-response | regmod_count | regmod_count |
| x-cb-response | netconn_count | netconn_count |
| x-cb-response | filemod_count | filemod_count |
| x-cb-response | modload_count | modload_count |
| x-cb-response | childproc_count | childproc_count |
| x-cb-response | crossproc_count | crossproc_count |
| x-cb-response | emet_count | emet_count |
| x-cb-response | emet_config | emet_config |
| x-cb-response | processblock_count | processblock_count |
| x-cb-response | filtering_known_dlls | filtering_known_dlls |
| x-cb-response | last_server_update | last_server_update |
| x-cb-response | logon_type | logon_type |
| x-cb-response | alliance_score_srstrust | alliance_score_srstrust |
| x-cb-response | alliance_link_srstrust | alliance_link_srstrust |
| x-cb-response | alliance_data_srstrust | alliance_data_srstrust |
| x-cb-response | alliance_updated_srstrust | alliance_updated_srstrust |
| <br> | | |
| x-oca-asset | ip_refs | interface_ip |
| x-oca-asset | hostname | hostname |
| x-oca-asset | host_type | host_type |
| x-oca-asset | os_name | os_type |
| <br> | | |
