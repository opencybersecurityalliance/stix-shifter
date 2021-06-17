## Microsoft Azure Sentinel
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
| x-msazure-sentinel | tenant_id | azureTenantId |
| x-msazure-sentinel | subscription_id | azureSubscriptionId |
| <br> | | |
| x-msazure-sentinel-alert | activityGroupName | activityGroupName |
| x-msazure-sentinel-alert | assignedTo | assignedTo |
| x-msazure-sentinel-alert | category | category |
| x-msazure-sentinel-alert | closedDateTime | closedDateTime |
| x-msazure-sentinel-alert | cloudAppStates.destinationServiceName | destinationServiceName |
| x-msazure-sentinel-alert | cloudAppStates.destinationServiceIp | destinationServiceIp |
| x-msazure-sentinel-alert | cloudAppStates.riskScore | riskScore |
| x-msazure-sentinel-alert | comments | comments |
| x-msazure-sentinel-alert | confidence | confidence |
| x-msazure-sentinel-alert | createddatetime | createdDateTime |
| x-msazure-sentinel-alert | description | description |
| x-msazure-sentinel-alert | detectionids | detectionIds |
| x-msazure-sentinel-alert | feedback | feedback |
| x-msazure-sentinel-alert | fileStates.riskScore | riskScore |
| x-msazure-sentinel-alert | hostStates.isAzureAadJoined | isAzureAadJoined |
| x-msazure-sentinel-alert | hostStates.isAzureAadRegistered | isAzureAadRegistered |
| x-msazure-sentinel-alert | hostStates.isHybridAzureDomainJoined | isHybridAzureDomainJoined |
| x-msazure-sentinel-alert | hostStates.os | os |
| x-msazure-sentinel-alert | hostStates.riskScore | riskScore |
| x-msazure-sentinel-alert | providerid | id |
| x-msazure-sentinel-alert | incidentIds | incidentIds |
| x-msazure-sentinel-alert | lastmodifieddatetime | lastModifiedDateTime |
| x-msazure-sentinel-alert | malwareStates.category | category |
| x-msazure-sentinel-alert | malwareStates.family | family |
| x-msazure-sentinel-alert | malwareStates.name | name |
| x-msazure-sentinel-alert | malwareStates.severity | severity |
| x-msazure-sentinel-alert | malwareStates.wasRunning | wasRunning |
| x-msazure-sentinel-alert | networkConnections.destinationLocation | destinationLocation |
| x-msazure-sentinel-alert | networkConnections.direction | direction |
| x-msazure-sentinel-alert | networkConnections.domainRegisteredDateTime | domainRegisteredDateTime |
| x-msazure-sentinel-alert | networkConnections.localDnsName | localDnsName |
| x-msazure-sentinel-alert | networkConnections.natDestinationAddress | natDestinationAddress |
| x-msazure-sentinel-alert | networkConnections.natDestinationPort | natDestinationPort |
| x-msazure-sentinel-alert | networkConnections.natSourceAddress | natSourceAddress |
| x-msazure-sentinel-alert | networkConnections.natSourcePort | natSourcePort |
| x-msazure-sentinel-alert | networkConnections.riskScore | riskScore |
| x-msazure-sentinel-alert | networkConnections.sourceLocation | sourceLocation |
| x-msazure-sentinel-alert | networkConnections.status | status |
| x-msazure-sentinel-alert | networkConnections.urlParameters | urlParameters |
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
| x-msazure-sentinel-alert | severity | severity |
| x-msazure-sentinel-alert | sourcematerials | sourceMaterials |
| x-msazure-sentinel-alert | status | status |
| x-msazure-sentinel-alert | tags | tags |
| x-msazure-sentinel-alert | title | title |
| x-msazure-sentinel-alert | triggers.name | name |
| x-msazure-sentinel-alert | triggers.type | type |
| x-msazure-sentinel-alert | triggers.value | value |
| x-msazure-sentinel-alert | userStates.aaduserid | aadUserId |
| x-msazure-sentinel-alert | userStates.emailrole | emailRole |
| x-msazure-sentinel-alert | userStates.isvpn | isVpn |
| x-msazure-sentinel-alert | userStates.logonLocation | logonLocation |
| x-msazure-sentinel-alert | userStates.logonType | logonType |
| x-msazure-sentinel-alert | userStates.onpremisessecurityidentifier | onPremisesSecurityIdentifier |
| x-msazure-sentinel-alert | userStates.riskScore | riskScore |
| x-msazure-sentinel-alert | userStates.useraccounttype | userAccountType |
| x-msazure-sentinel-alert | userStates.userPrincipalName | userPrincipalName |
| x-msazure-sentinel-alert | vendorinformation.subprovider | subProvider |
| x-msazure-sentinel-alert | vulnerabilityStates.cve | cve |
| x-msazure-sentinel-alert | vulnerabilityStates.severity | severity |
| x-msazure-sentinel-alert | vulnerabilityStates.wasRunning | wasRunning |
| <br> | | |
