##### Updated on 05/15/23
## Carbon Black Cloud
### Results STIX Domain Objects
* Identity
* Observed Data
<br>
### Supported STIX Operators
*Comparison AND/OR operators are inside the observation while observation AND/OR operators are between observations (square brackets).*

| STIX Operator | Data Source Operator |
|--|--|
| AND (Comparision) | AND |
| OR (Comparision) | OR |
| = | : |
| != | : |
| > | : |
| >= | : |
| < | : |
| <= | : |
| IN | : |
| OR (Observation) | OR |
| AND (Observation) | AND |
| <br> | |
### Searchable STIX objects and properties
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **ipv4-addr**:value | netconn_ipv4, netconn_local_ipv4 |
| **ipv6-addr**:value | netconn_ipv6, netconn_local_ipv6 |
| **file**:name | process_name |
| **file**:hashes.MD5 | process_hash |
| **file**:hashes.'SHA-256' | process_hash, process_sha256 |
| **process**:created | process_start_time |
| **process**:creator_user_ref.account_login | process_username |
| **process**:service_name | process_service_name |
| **process**:command_line | process_cmdline |
| **process**:pid | process_pid |
| **process**:name | process_name |
| **process**:binary_ref.name | process_name |
| **process**:binary_ref.hashes.MD5 | process_hash |
| **process**:binary_ref.hashes.'SHA-256' | process_hash, process_sha256 |
| **process**:parent_ref.command_line | parent_cmdline |
| **process**:parent_ref.pid | parent_pid |
| **process**:parent_ref.name | parent_name |
| **process**:parent_ref.binary_ref.name | parent_name |
| **process**:parent_ref.binary_ref.hashes.MD5 | parent_hash |
| **process**:parent_ref.binary_ref.hashes.'SHA-256' | parent_hash |
| **process**:x_unique_id | process_guid, parent_guid |
| **software**:name | process_file_description, process_internal_name |
| **software**:vendor | process_company_name, process_publisher |
| **software**:version | process_product_version |
| **network-traffic**:src_port | netconn_port |
| **network-traffic**:dst_port | netconn_port |
| **network-traffic**:protocols[*] | netconn_protocol |
| **network-traffic**:src_ref.value | netconn_local_ipv4, netconn_local_ipv6 |
| **network-traffic**:dst_ref.value | netconn_ipv4, netconn_ipv6 |
| **user-account**:user_id | process_username |
| **url**:value | netconn_domain |
| **domain-name**:value | netconn_domain |
| **x-cbcloud**:device_name | device_name |
| **x-cbcloud**:device_internal_ip | device_internal_ip |
| **x-cbcloud**:device_external_ip | device_external_ip |
| **x-cbcloud**:device_os | device_os |
| **x-cbcloud**:device_os_version | device_os_version |
| **x-cbcloud**:device_id | device_id |
| **x-cbcloud**:device_group | device_group |
| **x-cbcloud**:device_policy | device_policy |
| **x-cbcloud**:device_timestamp | device_timestamp |
| **x-cbcloud**:process_terminated | process_terminated |
| **x-cbcloud**:regmod_count | regmod_count |
| **x-cbcloud**:netconn_count | netconn_count |
| **x-cbcloud**:filemod_count | filemod_count |
| **x-cbcloud**:modload_count | modload_count |
| **x-cbcloud**:childproc_count | childproc_count |
| **x-cbcloud**:crossproc_count | crossproc_count |
| **x-cbcloud**:scriptload_count | scriptload_count |
| **x-cbcloud**:parent_cmdline_length | parent_cmdline_length |
| **x-cbcloud**:process_cmdline_length | process_cmdline_length |
| **x-cbcloud**:parent_publisher_state | parent_publisher_state |
| **x-cbcloud**:process_publisher_state | process_publisher_state |
| **x-cbcloud**:parent_reputation | parent_reputation |
| **x-cbcloud**:process_reputation | process_reputation |
| **x-cbcloud**:parent_effective_reputation | parent_effective_reputation |
| **x-cbcloud**:process_effective_reputation | process_effective_reputation |
| **x-cbcloud**:netconn_location | netconn_location |
| **x-cbcloud**:netconn_inbound | netconn_inbound |
| **x-cbcloud**:netconn_failed | netconn_failed |
| **x-cbcloud**:regmod_name | regmod_name |
| **x-cbcloud**:scriptload_name | scriptload_name |
| **x-cbcloud**:scriptload_hash | scriptload_hash |
| **x-cbcloud**:scriptload_publisher_state | scriptload_publisher_state |
| **x-cbcloud**:fileless_scriptload_hash | fileless_scriptload_hash |
| **x-cbcloud**:fileless_scriptload_cmdline | fileless_scriptload_cmdline |
| **x-cbcloud**:fileless_scriptload_cmdline_length | fileless_scriptload_cmdline_length |
| **x-cbcloud**:modload_name | modload_name |
| **x-cbcloud**:modload_hash | modload_hash |
| **x-cbcloud**:modload_publisher_state | modload_publisher_state |
| **x-cbcloud**:filemod_name | filemod_name |
| **x-cbcloud**:filemod_hash | filemod_hash |
| **x-cbcloud**:filemod_publisher_state | filemod_publisher_state |
| **x-cbcloud**:crossproc_action | crossproc_action |
| **x-cbcloud**:crossproc_api | crossproc_api |
| **x-cbcloud**:crossproc_hash | crossproc_hash |
| **x-cbcloud**:crossproc_name | crossproc_name |
| **x-cbcloud**:crossproc_target | crossproc_target |
| **x-cbcloud**:childproc_cmdline | childproc_cmdline |
| **x-cbcloud**:childproc_cmdline_length | childproc_cmdline_length |
| **x-cbcloud**:childproc_effective_reputation | childproc_effective_reputation |
| **x-cbcloud**:childproc_guid | childproc_guid |
| **x-cbcloud**:childproc_hash | childproc_hash |
| **x-cbcloud**:childproc_name | childproc_name |
| **x-cbcloud**:childproc_publisher_state | childproc_publisher_state |
| **x-cbcloud**:childproc_reputation | childproc_reputation |
| **x-cbcloud**:hash | hash |
| **x-cbcloud**:process_original_filename | process_original_filename |
| **x-cbcloud**:process_product_name | process_product_name |
| **x-cbcloud**:backend_timestamp | backend_timestamp |
| **x-cbcloud**:process_duration | process_duration |
| **x-cbcloud**:process_elevated | process_elevated |
| **x-cbcloud**:process_integrity_level | process_integrity_level |
| **x-cbcloud**:process_privileges | process_privileges |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| directory | path | process_path |
| directory | path | parent_path |
| <br> | | |
| file | name | process_name |
| file | hashes.MD5 | process_md5 |
| file | hashes.SHA-256 | process_sha256 |
| file | parent_directory_ref | process_path |
| file | name | parent_name |
| file | hashes.MD5 | parent_md5 |
| file | hashes.SHA-256 | parent_sha256 |
| file | parent_directory_ref | parent_path |
| <br> | | |
| process | creator_user_ref | process_username |
| process | created | process_start_time |
| process | name | process_name |
| process | binary_ref | process_name |
| process | pid | process_pid |
| process | x_unique_id | process_guid |
| process | command_line | process_cmdline |
| process | name | parent_name |
| process | binary_ref | parent_name |
| process | parent_ref | parent_name |
| process | pid | parent_pid |
| process | x_unique_id | parent_guid |
| process | command_line | parent_cmdline |
| <br> | | |
| user-account | user_id | process_username |
| <br> | | |
| x-cbcloud | device_name | device_name |
| x-cbcloud | device_internal_ip | device_internal_ip |
| x-cbcloud | device_external_ip | device_external_ip |
| x-cbcloud | device_os | device_os |
| x-cbcloud | device_id | device_id |
| x-cbcloud | device_timestamp | device_timestamp |
| x-cbcloud | org_id | org_id |
| x-cbcloud | device_group_id | device_group_id |
| x-cbcloud | process_terminated | process_terminated |
| x-cbcloud | regmod_count | regmod_count |
| x-cbcloud | netconn_count | netconn_count |
| x-cbcloud | filemod_count | filemod_count |
| x-cbcloud | modload_count | modload_count |
| x-cbcloud | childproc_count | childproc_count |
| x-cbcloud | crossproc_count | crossproc_count |
| x-cbcloud | scriptload_count | scriptload_count |
| <br> | | |
