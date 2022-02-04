##### Updated on 02/04/22
## HCL BigFix
### Supported STIX Operators
| STIX Operator | Data Source Operator |
|--|--|
| AND | OR |
| OR | OR |
| = | = |
| != | != |
| LIKE | contains |
| MATCHES | matches |
| > | is greater than |
| >= | is greater than or equal to |
| < | is less than |
| <= | is less than or equal to |
| IN | = |
| <br> | |
### Supported STIX Objects and Properties
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| directory | path | file_path |
| <br> | | |
| file | name | file_name |
| file | parent_directory_ref | file_path |
| file | hashes.SHA-256 | sha256hash |
| file | hashes.SHA-1 | sha1hash |
| file | hashes.MD5 | md5hash |
| file | size | file_size |
| <br> | | |
| ipv4-addr | value | local_address |
| ipv4-addr | value | remote_address |
| <br> | | |
| ipv6-addr | value | local_address |
| ipv6-addr | value | remote_address |
| <br> | | |
| mac-addr | value | mac |
| <br> | | |
| network-traffic | src_ref | local_address |
| network-traffic | dst_ref | remote_address |
| network-traffic | src_port | local_port |
| network-traffic | dst_port | remote_port |
| network-traffic | protocols | protocol |
| <br> | | |
| process | binary_ref | file_path |
| process | name | process_name |
| process | pid | process_id |
| process | pid | process_ppid |
| process | parent_ref | process_ppid |
| process | creator_user_ref | process_user |
| <br> | | |
| user-account | user_id | process_user |
| <br> | | |
| x-bigfix-relevance | computer_identity | computer_identity |
| <br> | | |
