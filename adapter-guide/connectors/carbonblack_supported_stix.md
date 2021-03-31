## Carbon Black CB Response
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| directory | path | path |
| <br> | | |
| file | name | process_name |
| file | hashes.MD5 | process_md5 |
| file | hashes.SHA-256 | process_sha256 |
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
| process | pid | parent_pid |
| process | parent_ref | parent_pid |
| process | x_id | parent_id |
| process | x_unique_id | parent_unique_id |
| process | command_line | cmdline |
| <br> | | |
| user-account | user_id | username |
| <br> | | |
| x_cb_response | host_name | hostname |
| x_cb_response | host_type | host_type |
| x_cb_response | comms_ip | comms_ip |
| x_cb_response | os_type | os_type |
| x_cb_response | sensor_id | sensor_id |
| x_cb_response | group | group |
| x_cb_response | segment_id | segment_id |
| x_cb_response | terminated | terminated |
| x_cb_response | regmod_count | regmod_count |
| x_cb_response | netconn_count | netconn_count |
| x_cb_response | filemod_count | filemod_count |
| x_cb_response | modload_count | modload_count |
| x_cb_response | childproc_count | childproc_count |
| x_cb_response | crossproc_count | crossproc_count |
| x_cb_response | emet_count | emet_count |
| x_cb_response | emet_config | emet_config |
| x_cb_response | processblock_count | processblock_count |
| x_cb_response | filtering_known_dlls | filtering_known_dlls |
| x_cb_response | last_server_update | last_server_update |
| x_cb_response | logon_type | logon_type |
| x_cb_response | alliance_score_srstrust | alliance_score_srstrust |
| x_cb_response | alliance_link_srstrust | alliance_link_srstrust |
| x_cb_response | alliance_data_srstrust | alliance_data_srstrust |
| x_cb_response | alliance_updated_srstrust | alliance_updated_srstrust |
| <br> | | |
