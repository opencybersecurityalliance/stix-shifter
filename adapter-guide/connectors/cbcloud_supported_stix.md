## Carbon Black Cloud
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
| x_cbcloud | device_name | device_name |
| x_cbcloud | device_internal_ip | device_internal_ip |
| x_cbcloud | device_external_ip | device_external_ip |
| x_cbcloud | device_os | device_os |
| x_cbcloud | device_id | device_id |
| x_cbcloud | device_timestamp | device_timestamp |
| x_cbcloud | org_id | org_id |
| x_cbcloud | device_group_id | device_group_id |
| x_cbcloud | process_terminated | process_terminated |
| x_cbcloud | regmod_count | regmod_count |
| x_cbcloud | netconn_count | netconn_count |
| x_cbcloud | filemod_count | filemod_count |
| x_cbcloud | modload_count | modload_count |
| x_cbcloud | childproc_count | childproc_count |
| x_cbcloud | crossproc_count | crossproc_count |
| x_cbcloud | scriptload_count | scriptload_count |
| <br> | | |
