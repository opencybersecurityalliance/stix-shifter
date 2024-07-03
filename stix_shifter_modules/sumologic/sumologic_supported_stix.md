##### Updated on 05/23/24
## Sumo Logic
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
| = | = |
| != | = |
| LIKE | = |
| IN | OR |
| OR (Observation) | OR |
| AND (Observation) | AND |
| LIKE | = |
| <br> | |
### Searchable STIX objects and properties
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **artifact**:payload_bin | _raw |
| **domain-name**:value | _sourcehost |
| **x-ibm-finding**:event_count | _messagecount |
| **x-ibm-finding**:time_observed | _messagetime |
| **x-ibm-finding**:src_device | _collector |
| **x-ibm-finding**:start | _receipttime |
| **x-oca-event**:code | _messageid |
| **x-oca-event**:created | _messagetime |
| **x-oca-event**:agent | _collector |
| **x-oca-event**:module | _source |
| **x-oca-event**:provider | _sourcecategory |
| **x-oca-event**:original_ref.payload_bin | _raw |
| **x-oca-event**:domain_ref.value | _sourcehost |
| **x-oca-event**:user_ref.account_login | _useremail |
| **x-sumologic-source**:collectorid | _collectorid |
| **x-sumologic-source**:sourcename | _sourcename |
| **user-account**:user_id | id |
| **user-account**:account_login | email |
| **user-account**:display_name | displayName |
| **user-account**:account_created | createdAt |
| **user-account**:account_last_login | lastLoginTimestamp |
| <br> | |
### Searchable STIX objects and properties for Cloud_Siem dialect
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **ipv4-addr**:value | device_ip, device_natIp, dns_replyIp, dstDevice_ip, srcDevice_ip, dstDevice_natIp, srcDevice_natIp |
| **ipv4-addr**:resolves-to-ref.value | srcDevice_mac, dstDevice_mac |
| **network-traffic**:dst_port | dstPort |
| **network-traffic**:src_port | srcPort |
| **network-traffic**:dst_ref.value | dstDevice_ip |
| **network-traffic**:src_ref.value | srcDevice_ip |
| **x-oca-event**:network_ref.src_ref.value | srcDevice_ip |
| **x-oca-event**:network_ref.dst_ref.value | dstDevice_ip |
| **x-oca-event**:process_ref.binary_ref.name | baseImage |
| **x-oca-event**:process_ref.command_line | commandLine |
| **x-oca-event**:parent_process_ref.binary_ref.name | parentBaseImage |
| **x-oca-event**:user_ref.user_id | user_username, user_username_raw |
| **x-oca-event**:code | metadata_deviceEventId |
| **mac-addr**:value | device_mac, srcDevice_mac, dstDevice_mac |
| **file**:name | baseImage, parentBaseImage, file_basename, file_path |
| **file**:parent_directory_ref.binary_ref.name | baseImage, parentBaseImage |
| **file**:hashes.SHA-256 | file_hash_sha256 |
| **file**:hashes.MD5 | file_hash_md5 |
| **file**:hashes.SHA-1 | file_hash_sha1 |
| **directory**:path | baseImage, parentBaseImage, file_path |
| **process**:binary_ref.name | baseImage, parentBaseImage |
| **process**:command_line | commandLine |
| **process**:parent_ref.binary_ref.name | parentBaseImage |
| **process**:creator_user_ref.user_id | user_username, user_username_raw |
| **user-account**:user_id | user_username, user_username_raw, fromUser_username, fromUser_username_raw |
| **user-account**:display_name | user_username, user_username_raw, fromUser_username, fromUser_username_raw |
| **domain-name**:value | http_referer_fqdn, http_url_fqdn |
| **url**:value | http_url |
| **email-addr**:value | targetUser_email, user_email |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| artifact | payload_bin | _raw |
| <br> | | |
| domain-name | value | _sourcehost |
| <br> | | |
| user-account | user_id | id |
| user-account | account_login | email |
| user-account | display_name | displayName |
| user-account | account_created | createdAt |
| user-account | account_last_login | lastLoginTimestamp |
| <br> | | |
| x-ibm-finding | event_count | _messagecount |
| x-ibm-finding | time_observed | _messagetime |
| x-ibm-finding | src_device | _collector |
| x-ibm-finding | start | _receipttime |
| <br> | | |
| x-oca-event | original_ref | _raw |
| x-oca-event | domain_ref | _sourcehost |
| x-oca-event | created | _messagetime |
| x-oca-event | code | _messageid |
| x-oca-event | agent | _collector |
| x-oca-event | module | _source |
| x-oca-event | provider | _sourcecategory |
| x-oca-event | user_ref | email |
| <br> | | |
| x-sumologic-source | collectorid | _collectorid |
| x-sumologic-source | sourcename | _sourcename |
| <br> | | |
