##### Updated on 06/01/22
## Microsoft Azure Sentinel
### Supported STIX Operators
| STIX Operator | Data Source Operator |
|--|--|
| AND | and |
| OR | or |
| > | gt |
| >= | ge |
| < | lt |
| <= | le |
| = | eq |
| != | ne |
| LIKE | contains |
| IN | eq |
| MATCHES | contains |
| <br> | |
### Supported STIX Objects and Properties
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| directory | path | path |
| <br> | | |
| domain-name | value | fqdn |
| domain-name | value | destinationDomain |
| domain-name | value | domainName |
| <br> | | |
| extensions | windows-registry-value-type.valueData | registryKeyStates |
| extensions | windows-registry-value-type.name | registryKeyStates |
| extensions | windows-registry-value-type.valuetype | registryKeyStates |
| <br> | | |
| file | hashes.SHA-256 | sha256 |
| file | hashes.SHA-1 | sha1 |
| file | hashes.MD5 | md5 |
| file | hashes.authenticodeHash256 | authenticodeHash256 |
| file | hashes.lsHash | lsHash |
| file | hashes.ctph | ctph |
| file | hashes.peSha1 | peSha1 |
| file | hashes.peSha256 | peSha256 |
| file | hashes.UNKNOWN | unknown |
| file | name | name |
| file | parent_directory_ref | path |
| <br> | | |
| ipv4-addr | value | privateIpAddress |
| ipv4-addr | value | publicIpAddress |
| ipv4-addr | value | destinationAddress |
| ipv4-addr | value | sourceAddress |
| ipv4-addr | value | logonIp |
| <br> | | |
| network-traffic | dst_ref | destinationAddress |
| network-traffic | dst_port | destinationPort |
| network-traffic | protocols | protocol |
| network-traffic | src_ref | sourceAddress |
| network-traffic | src_port | sourcePort |
| <br> | | |
| process | creator_user_ref | accountName |
| process | command_line | commandLine |
| process | created | createdDateTime |
| process | name | name |
| process | created | parentProcessCreatedDateTime |
| process | pid | parentProcessId |
| process | parent_ref | parentProcessId |
| process | name | parentProcessName |
| process | pid | processId |
| process | pid | registryKeyStates |
| <br> | | |
| software | name | destinationServiceName |
| software | name | os |
| software | name | applicationName |
| software | name | provider |
| software | vendor | vendor |
| software | version | providerVersion |
| <br> | | |
| url | value | destinationUrl |
| <br> | | |
| user-account | user_id | accountName |
| user-account | account_last_login | logonDateTime |
| user-account | account_login | logonId |
| <br> | | |
| windows-registry-key | key | registryKeyStates |
| <br> | | |
| x-ibm-finding | dst_application_ref | destinationServiceName |
| x-ibm-finding | createddatetime | createdDateTime |
| x-ibm-finding | description | description |
| x-ibm-finding | src_os_ref.name | os |
| x-ibm-finding | time_observed | lastModifiedDateTime |
| x-ibm-finding | dst_geolocation | destinationLocation |
| x-ibm-finding | dst_ip_ref.value | natDestinationAddress |
| x-ibm-finding | src_ip_ref.value | natSourceAddress |
| x-ibm-finding | src_geolocation | sourceLocation |
| x-ibm-finding | severity | severity |
| x-ibm-finding | name | title |
| x-ibm-finding | src_application_user_ref.user_id | aadUserId |
| x-ibm-finding | src_application_user_ref.type | logonType |
| <br> | | |
| x-msazure-sentinel | tenant_id | azureTenantId |
| x-msazure-sentinel | subscription_id | azureSubscriptionId |
| <br> | | |
| x-msazure-sentinel-alert | activityGroupName | activityGroupName |
| x-msazure-sentinel-alert | assignedTo | assignedTo |
| x-msazure-sentinel-alert | cloudAppStates.destinationServiceIp | destinationServiceIp |
| x-msazure-sentinel-alert | cloudAppStates.riskScore | riskScore |
| x-msazure-sentinel-alert | comments | comments |
| x-msazure-sentinel-alert | confidence | confidence |
| x-msazure-sentinel-alert | detectionids | detectionIds |
| x-msazure-sentinel-alert | feedback | feedback |
| x-msazure-sentinel-alert | fileStates.riskScore | riskScore |
| x-msazure-sentinel-alert | hostStates.isAzureAadJoined | isAzureAadJoined |
| x-msazure-sentinel-alert | hostStates.isAzureAadRegistered | isAzureAadRegistered |
| x-msazure-sentinel-alert | hostStates.isHybridAzureDomainJoined | isHybridAzureDomainJoined |
| x-msazure-sentinel-alert | hostStates.riskScore | riskScore |
| x-msazure-sentinel-alert | incidentIds | incidentIds |
| x-msazure-sentinel-alert | malwareStates.category | category |
| x-msazure-sentinel-alert | malwareStates.family | family |
| x-msazure-sentinel-alert | malwareStates.name | name |
| x-msazure-sentinel-alert | malwareStates.severity | severity |
| x-msazure-sentinel-alert | malwareStates.wasRunning | wasRunning |
| x-msazure-sentinel-alert | networkConnections.direction | direction |
| x-msazure-sentinel-alert | networkConnections.domainRegisteredDateTime | domainRegisteredDateTime |
| x-msazure-sentinel-alert | networkConnections.localDnsName | localDnsName |
| x-msazure-sentinel-alert | networkConnections.natDestinationPort | natDestinationPort |
| x-msazure-sentinel-alert | networkConnections.natSourcePort | natSourcePort |
| x-msazure-sentinel-alert | networkConnections.riskScore | riskScore |
| x-msazure-sentinel-alert | networkConnections.status | status |
| x-msazure-sentinel-alert | processes.integrityLevel | integrityLevel |
| x-msazure-sentinel-alert | processes.isElevated | isElevated |
| x-msazure-sentinel-alert | recommendedactions | recommendedActions |
| x-msazure-sentinel-alert | registryKeyStates.hive | registryKeyStates |
| x-msazure-sentinel-alert | registryKeyStates.oldKey | registryKeyStates |
| x-msazure-sentinel-alert | registryKeyStates.oldValueData | registryKeyStates |
| x-msazure-sentinel-alert | registryKeyStates.oldValueName | registryKeyStates |
| x-msazure-sentinel-alert | registryKeyStates.operation | registryKeyStates |
| x-msazure-sentinel-alert | securityresources.resource | resource |
| x-msazure-sentinel-alert | securityresources.resourcetype | resourceType |
| x-msazure-sentinel-alert | sourcematerials | sourceMaterials |
| x-msazure-sentinel-alert | status | status |
| x-msazure-sentinel-alert | tags | tags |
| x-msazure-sentinel-alert | triggers.name | name |
| x-msazure-sentinel-alert | triggers.type | type |
| x-msazure-sentinel-alert | triggers.value | value |
| x-msazure-sentinel-alert | userStates.emailrole | emailRole |
| x-msazure-sentinel-alert | userStates.isvpn | isVpn |
| x-msazure-sentinel-alert | userStates.logonLocation | logonLocation |
| x-msazure-sentinel-alert | userStates.onpremisessecurityidentifier | onPremisesSecurityIdentifier |
| x-msazure-sentinel-alert | userStates.riskScore | riskScore |
| x-msazure-sentinel-alert | userStates.useraccounttype | userAccountType |
| x-msazure-sentinel-alert | userStates.userPrincipalName | userPrincipalName |
| x-msazure-sentinel-alert | vulnerabilityStates.cve | cve |
| x-msazure-sentinel-alert | vulnerabilityStates.severity | severity |
| x-msazure-sentinel-alert | vulnerabilityStates.wasRunning | wasRunning |
| <br> | | |
| x-oca-event | category | category |
| x-oca-event | created | createdDateTime |
| x-oca-event | code | id |
| x-oca-event | domain_ref.value | urlParameters |
| x-oca-event | url_ref.value | urlParameters |
| x-oca-event | action | title |
| x-oca-event | provider | subProvider |
| <br> | | |
