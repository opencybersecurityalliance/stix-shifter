##### Updated on 02/04/22
## IBM Guardium Data Protection
### Supported STIX Operators
| STIX Operator | Data Source Operator |
|--|--|
| AND | OR |
| OR | OR |
| = | = |
| <br> | |
### Supported STIX Objects and Properties
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
| process | id | Pid |
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
