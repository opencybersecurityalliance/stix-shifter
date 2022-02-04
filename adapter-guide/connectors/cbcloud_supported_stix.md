##### Updated on 02/04/22
## Carbon Black Cloud
### Supported STIX Operators
| STIX Operator | Data Source Operator |
|--|--|
| AND | AND |
| OR | OR |
| = | : |
| != | : |
| > | : |
| >= | : |
| < | : |
| <= | : |
| IN | : |
| <br> | |
### Supported STIX Objects and Properties
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
