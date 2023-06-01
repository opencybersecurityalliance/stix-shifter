##### Updated on 05/15/23
## IBM Guardium Data Protection
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
| OR (Observation) | OR |
| AND (Observation) | OR |
| IN | = |
| <br> | |
### Searchable STIX objects and properties for Qsearch dialect
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **x-ibm-finding**:finding_type | datacategory |
| **x-ibm-finding**:start | startTime |
| **x-ibm-finding**:end | endTime |
| **x-ibm-finding**:database_name | Database |
| **x-ibm-finding**:dst_device | Database |
| **ipv4-addr**:value | ClientIP, Server |
| **ipv4-addr**:src_ip | ClientIP |
| **ipv4-addr**:dst_ip | Server |
| **ipv6-addr**:value | ClientIP, Server |
| **ipv6-addr**:src_ip | ClientIP |
| **ipv6-addr**:dst_ip | Server |
| **network-traffic**:dst_ref.value | Server |
| **network-traffic**:src_ref.value | ClientIP |
| **user-account**:value | DB User, OS User |
| **user-account**:db_user | DB User |
| **user-account**:os_user | OS User |
| **user-account**:user_id | DB User |
| **user-account**:login_name | OS User |
| **x-guardium**:severity | Severity |
| <br> | |
### Searchable STIX objects and properties for Report dialect
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **x-ibm-finding**:finding_type | datacategory |
| **x-ibm-finding**:start | QUERY_FROM_DATE |
| **x-ibm-finding**:end | QUERY_TO_DATE |
| **x-ibm-finding**:database_name | Database |
| **x-ibm-finding**:dst_device | Database |
| **ipv4-addr**:value | ServerIP |
| **ipv4-addr**:dst_ip | ServerIP |
| **ipv6-addr**:value | ServerIP |
| **ipv6-addr**:dst_ip | ServerIP |
| **network-traffic**:dst_ref.value | ServerIP |
| **user-account**:value | DBUser, OSUser |
| **user-account**:db_user | DBUser |
| **user-account**:os_user | OSUser |
| **user-account**:user_id | DBUser |
| **user-account**:login_name | OSUser |
| **artifact**:payload_bin | Payload-dialect1 |
| **domain-name**:value | DomainName-dialect1 |
| **x-guardium**:severity | Severity |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| artifact | payload_bin | Payload |
| <br> | | |
| domain-name | value | DomainName |
| <br> | | |
| file | name | FileName |
| <br> | | |
| ipv4-addr | value | SourceIpV4 |
| ipv4-addr | value | client_ip |
| ipv4-addr | value | server |
| ipv4-addr | value | Server IP |
| <br> | | |
| ipv6-addr | value | client_ip |
| ipv6-addr | value | server |
| ipv6-addr | value | Server IP |
| <br> | | |
| network-traffic | src_ref | SourceIpV4 |
| network-traffic | dst_port | DestinationPort |
| network-traffic | src_port | SourcePort |
| network-traffic | protocols | NetworkProtocol |
| <br> | | |
| process | command_line | Path |
| process | pid | Pid |
| <br> | | |
| software | name | db_type |
| software | name | Server Type |
| software | name | source_program |
| <br> | | |
| url | value | Url |
| <br> | | |
| user-account | user_id | DB User |
| user-account | user_id | db_user |
| user-account | login_name | OSUser |
| <br> | | |
| x-guardium | log_source_id | LogSourceId |
| x-guardium | magnitude | Magnitude |
| x-guardium | severity | severity |
| x-guardium | severity | Severity |
| <br> | | |
| x-ibm-finding | src_database_user_ref | DB User |
| x-ibm-finding | src_database_user_ref | db_user |
| x-ibm-finding | src_os_user_ref | OSUser |
| x-ibm-finding | src_ip_ref | client_ip |
| x-ibm-finding | dst_ip_ref | server |
| x-ibm-finding | dst_ip_ref | Server IP |
| x-ibm-finding | dst_application_ref | db_type |
| x-ibm-finding | dst_application_ref | Server Type |
| x-ibm-finding | src_application_ref | source_program |
| x-ibm-finding | name | violation |
| x-ibm-finding | name | Threat Category |
| x-ibm-finding | details | details |
| x-ibm-finding | dst_device | database |
| x-ibm-finding | dst_device | Database |
| x-ibm-finding | finding_type | severity |
| x-ibm-finding | finding_type | Severity |
| x-ibm-finding | source | guardium_appliance |
| x-ibm-finding | source | Originating Unit |
| <br> | | |
