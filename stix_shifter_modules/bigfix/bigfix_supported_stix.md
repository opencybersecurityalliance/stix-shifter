##### Updated on 05/15/23
## HCL BigFix
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
| = | = |
| != | != |
| LIKE | contains |
| MATCHES | matches |
| > | is greater than |
| >= | is greater than or equal to |
| < | is less than |
| <= | is less than or equal to |
| IN | = |
| OR (Observation) | OR |
| AND (Observation) | OR |
| <br> | |
### Searchable STIX objects and properties
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **file**:name | file.name |
| **file**:hashes.'SHA-256' | file.sha256 |
| **file**:hashes.'SHA-1' | file.sha1 |
| **file**:hashes.MD5 | file.md5 |
| **file**:parent_directory_ref.path | file.folder |
| **file**:size | file.size |
| **process**:name | process.name |
| **process**:pid | process.pid, process.process id |
| **process**:parent_ref.pid | process.ppid |
| **process**:binary_ref.name | file.name |
| **process**:binary_ref.hashes.'SHA-256' | file.sha256 |
| **process**:binary_ref.hashes.'SHA-1' | file.sha1 |
| **process**:binary_ref.hashes.MD5 | file.md5 |
| **process**:binary_ref.parent_directory_ref.path | file.pathname |
| **process**:binary_ref.size | file.size |
| **process**:creator_user_ref.user_id | process.user, process.name of user |
| **ipv4-addr**:value | socket.local address, socket.remote address |
| **ipv6-addr**:value | socket.local address, socket.remote address |
| **network-traffic**:src_port | socket.local port |
| **network-traffic**:dst_port | socket.remote port |
| **network-traffic**:src_ref.value | socket.local address |
| **network-traffic**:dst_ref.value | socket.remote address |
| **mac-addr**:value | adapter.mac address |
| <br> | |
### Supported STIX Objects and Properties for Query Results
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
