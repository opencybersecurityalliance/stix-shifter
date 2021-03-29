## Microsoft Azure Sentinel
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| directory | path | processes_0_path |
| directory | path | processes_1_path |
| directory | path | processes_2_path |
| directory | path | processes_3_path |
| directory | path | fileStates_0_path |
| directory | path | fileStates_1_path |
| directory | path | fileStates_2_path |
| directory | path | fileStates_3_path |
| <br> | | |
| domain-name | value | hostStates_0_fqdn |
| domain-name | value | hostStates_1_fqdn |
| domain-name | value | hostStates_2_fqdn |
| domain-name | value | hostStates_3_fqdn |
| domain-name | value | hostStates_0_netBiosName |
| domain-name | value | hostStates_1_netBiosName |
| domain-name | value | hostStates_2_netBiosName |
| domain-name | value | hostStates_3_netBiosName |
| <br> | | |
| file | name | fileStates_0_name |
| file | name | fileStates_1_name |
| file | name | fileStates_2_name |
| file | name | fileStates_3_name |
| file | hashes.SHA-1 | fileStates_0_sha1 |
| file | hashes.SHA-1 | fileStates_1_sha1 |
| file | hashes.SHA-1 | fileStates_2_sha1 |
| file | hashes.SHA-1 | fileStates_3_sha1 |
| file | hashes.SHA-256 | fileStates_0_sha256 |
| file | hashes.SHA-256 | fileStates_1_sha256 |
| file | hashes.SHA-256 | fileStates_2_sha256 |
| file | hashes.SHA-256 | fileStates_3_sha256 |
| file | name | processes_0_name |
| file | name | processes_1_name |
| file | parent_directory_ref | processes_0_path |
| file | parent_directory_ref | processes_1_path |
| file | parent_directory_ref | processes_2_path |
| file | parent_directory_ref | processes_3_path |
| file | parent_directory_ref | fileStates_0_path |
| file | parent_directory_ref | fileStates_1_path |
| file | parent_directory_ref | fileStates_2_path |
| file | parent_directory_ref | fileStates_3_path |
| <br> | | |
| ipv4-addr | value | networkConnections_0_sourceAddress |
| ipv4-addr | value | networkConnections_1_sourceAddress |
| ipv4-addr | value | networkConnections_2_sourceAddress |
| ipv4-addr | value | networkConnections_3_sourceAddress |
| ipv4-addr | value | networkConnections_0_destinationAddress |
| ipv4-addr | value | networkConnections_1_destinationAddress |
| ipv4-addr | value | networkConnections_2_destinationAddress |
| ipv4-addr | value | networkConnections_3_destinationAddress |
| <br> | | |
| network-traffic | src_ref | networkConnections_0_sourceAddress |
| network-traffic | src_ref | networkConnections_1_sourceAddress |
| network-traffic | src_ref | networkConnections_2_sourceAddress |
| network-traffic | src_ref | networkConnections_3_sourceAddress |
| network-traffic | dst_ref | networkConnections_0_destinationAddress |
| network-traffic | dst_ref | networkConnections_1_destinationAddress |
| network-traffic | dst_ref | networkConnections_2_destinationAddress |
| network-traffic | dst_ref | networkConnections_3_destinationAddress |
| network-traffic | protocols | networkConnections_0_protocol |
| network-traffic | protocols | networkConnections_1_protocol |
| network-traffic | protocols | networkConnections_2_protocol |
| network-traffic | protocols | networkConnections_3_protocol |
| network-traffic | dst_port | networkConnections_0_destinationPort |
| network-traffic | dst_port | networkConnections_1_destinationPort |
| network-traffic | dst_port | networkConnections_2_destinationPort |
| network-traffic | dst_port | networkConnections_3_destinationPort |
| network-traffic | src_port | networkConnections_0_sourcePort |
| <br> | | |
| process | name | processes_0_name |
| process | name | processes_1_name |
| process | name | processes_2_name |
| process | name | processes_3_name |
| process | binary_ref | processes_0_sha1 |
| process | binary_ref | processes_1_sha1 |
| process | binary_ref | processes_2_sha1 |
| process | binary_ref | processes_3_sha1 |
| process | binary_ref | processes_0_sha256 |
| process | binary_ref | processes_1_sha256 |
| process | binary_ref | processes_2_sha256 |
| process | binary_ref | processes_3_sha256 |
| process | binary_ref | processes_0_path |
| process | binary_ref | processes_1_path |
| process | binary_ref | processes_2_path |
| process | binary_ref | processes_3_path |
| process | name | processes_0_parentProcessName |
| process | parent_ref | processes_1_parentProcessName |
| process | name | processes_2_parentProcessName |
| process | parent_ref | processes_2_parentProcessName |
| process | name | processes_3_parentProcessName |
| process | parent_ref | processes_3_parentProcessName |
| <br> | | |
| user-account | user_id | userStates_0_accountName |
| user-account | user_id | userStates_1_accountName |
| user-account | user_id | userStates_2_accountName |
| user-account | user_id | userStates_3_accountName |
| user-account | account_last_login | userStates_0_logonDateTime |
| user-account | account_last_login | userStates_1_logonDateTime |
| user-account | account_last_login | userStates_2_logonDateTime |
| user-account | account_last_login | userStates_3_logonDateTime |
| <br> | | |
| x_msazure_sentinel | tenant_id | azureTenantId |
| x_msazure_sentinel | subscription_id | azureSubscriptionId |
| <br> | | |
| x_msazure_sentinel_alert | id | id |
| x_msazure_sentinel_alert | title | title |
| x_msazure_sentinel_alert | provider | vendorInformation_provider |
| x_msazure_sentinel_alert | vendor | vendorInformation_vendor |
| <br> | | |
