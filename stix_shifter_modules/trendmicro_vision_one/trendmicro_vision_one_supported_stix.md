##### Updated on 05/15/23
## Trend Micro Vision One
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
| LIKE | : |
| IN | : |
| OR (Observation) | OR |
| AND (Observation) | AND |
| <br> | |
### Searchable STIX objects and properties for Endpointactivitydata dialect
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **ipv4-addr**:value | src, dst, objectIp, objectIps |
| **ipv6-addr**:value | src, dst, objectIp, objectIps |
| **url**:value | request |
| **file**:hashes.'SHA-1' | srcFileHashSha1, objectFileHashSha1, parentFileHashSha1, processFileHashSha1 |
| **network-traffic**:src_ref.value | src |
| **network-traffic**:dst_ref.value | dst, objectIp |
| **network-traffic**:src_port | spt |
| **network-traffic**:dst_port | dpt, objectPort |
| **user-account**:account_login | logonUser |
| **user-account**:user_id | objectUser |
| **process**:command_line | processCmd, parentCmd, objectCmd |
| **windows-registry-key**:key | objectRegistryKeyHandle |
| **windows-registry-key**:values[*].name | objectRegistryValue |
| **windows-registry-key**:values[*].data | objectRegistryData |
| **domain-name**:value | hostName |
| <br> | |
### Searchable STIX objects and properties for Messageactivitydata dialect
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **ipv4-addr**:value | source_ip |
| **ipv6-addr**:value | source_ip |
| **url**:value | url |
| **network-traffic**:src_ref.value | source_ip |
| **file**:hashes.'SHA-1' | file_sha1 |
| **file**:name | file_name |
| **email-message**:sender_ref.value | sender, mailbox |
| **email-message**:to_refs[*].value | recipient, mailbox |
| **email-message**:subject | subject |
| **email-message**:message_id | message_id |
| **domain-name**:value | source_domain |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| directory | path | objectFilePath |
| directory | path | processFilePath |
| directory | path | parentFilePath |
| directory | path | srcFilePath |
| <br> | | |
| domain-name | value | hostName |
| domain-name | value | objectHostName |
| domain-name | value | source_domain |
| <br> | | |
| email-addr | value | mail_message_sender |
| email-addr | value | mail_message_recipient |
| <br> | | |
| email-message | sender_ref | mail_message_sender |
| email-message | is_multipart | mail_message_sender |
| email-message | to_refs | mail_message_recipient |
| email-message | is_multipart | mail_message_recipient |
| email-message | subject | mail_message_subject |
| email-message | is_multipart | mail_message_subject |
| email-message | date | mail_message_delivery_time |
| email-message | is_multipart | mail_message_delivery_time |
| email-message | additional_header_fields | mail_internet_headers |
| <br> | | |
| file | hashes.SHA-1 | objectFileHashSha1 |
| file | name | objectFilePath |
| file | parent_directory_ref | objectFilePath |
| file | hashes.SHA-1 | processFileHashSha1 |
| file | name | processFilePath |
| file | parent_directory_ref | processFilePath |
| file | hashes.SHA-1 | parentFileHashSha1 |
| file | name | parentFilePath |
| file | parent_directory_ref | parentFilePath |
| file | name | srcFilePath |
| file | parent_directory_ref | srcFilePath |
| file | hashes.SHA-1 | srcFileHashSha1 |
| file | name | file_name |
| file | hashes.SHA-1 | file_sha1 |
| <br> | | |
| ipv4-addr | value | src |
| ipv4-addr | value | dst |
| ipv4-addr | value | endpointIp |
| ipv4-addr | value | objectIp |
| ipv4-addr | value | objectIps |
| ipv4-addr | value | source_ip |
| <br> | | |
| ipv6-addr | value | src |
| ipv6-addr | value | dst |
| ipv6-addr | value | endpointIp |
| ipv6-addr | value | objectIps |
| ipv6-addr | value | source_ip |
| <br> | | |
| network-traffic | src_ref | src |
| network-traffic | protocols | src |
| network-traffic | src_port | spt |
| network-traffic | protocols | spt |
| network-traffic | dst_ref | dst |
| network-traffic | protocols | dst |
| network-traffic | dst_port | dpt |
| network-traffic | protocols | dpt |
| network-traffic | dst_ref | objectIp |
| network-traffic | protocols | objectIp |
| network-traffic | dst_port | objectPort |
| network-traffic | protocols | objectPort |
| network-traffic | src_ref | source_ip |
| network-traffic | protocols | source_ip |
| <br> | | |
| process | command_line | objectCmd |
| process | binary_ref | objectFileHashSha1 |
| process | binary_ref | objectFilePath |
| process | command_line | processCmd |
| process | binary_ref | processFileHashSha1 |
| process | binary_ref | processFilePath |
| process | command_line | parentCmd |
| process | binary_ref | parentFileHashSha1 |
| process | binary_ref | parentFilePath |
| <br> | | |
| url | value | request |
| url | value | mail_urls |
| <br> | | |
| user-account | account_login | logonUser |
| user-account | user_id | objectUser |
| <br> | | |
| windows-registry-key | key | objectRegistryKeyHandle |
| windows-registry-key | values | objectRegistryValueType |
| <br> | | |
