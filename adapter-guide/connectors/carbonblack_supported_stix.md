##### Updated on 02/04/22
## Carbon Black CB Response
### Supported STIX Operators
| STIX Operator | Data Source Operator |
|--|--|
| AND | or |
| OR | or |
| = | : |
| != | : |
| > | : |
| >= | : |
| < | : |
| <= | : |
| <br> | |
### Supported STIX Objects and Properties
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
