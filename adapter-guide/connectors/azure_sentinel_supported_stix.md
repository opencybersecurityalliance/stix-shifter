##### Updated on 05/02/23
## Microsoft Graph Security
### Supported STIX Operators
*Comparison AND/OR operators are inside the observation while observation AND/OR operators are between observations (square brackets).*

| STIX Operator | Data Source Operator |
|--|--|
| AND (Comparision) | and |
| OR (Comparision) | or |
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
### Searchable STIX objects and properties
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **ipv4-addr**:value | networkConnections.sourceAddress, networkConnections.destinationAddress, networkConnections.natSourceAddress, networkConnections.natDestinationAddress |
| **ipv6-addr**:value | networkConnections.sourceAddress, networkConnections.destinationAddress |
| **network-traffic**:src_port | networkConnections.sourcePort, networkConnections.natSourcePort |
| **network-traffic**:dst_port | networkConnections.destinationPort, networkConnections.natDestinationPort |
| **network-traffic**:protocols[*] | networkConnections.protocol |
| **network-traffic**:src_ref.value | networkConnections.sourceAddress |
| **network-traffic**:dst_ref.value | networkConnections.destinationAddress |
| **directory**:path | fileStates.path, process.path |
| **file**:parent_directory_ref.path | fileStates.path |
| **file**:name | fileStates.name |
| **file**:hashes.'SHA-256' | fileStates.fileHash.hashValue |
| **file**:hashes.'SHA-1' | fileStates.fileHash.hashValue |
| **file**:hashes.MD5 | fileStates.fileHash.hashValue |
| **file**:hashes.authenticodeHash256 | fileStates.fileHash.hashValue |
| **file**:hashes.lsHash | fileStates.fileHash.hashValue |
| **file**:hashes.ctph | fileStates.fileHash.hashValue |
| **file**:hashes.peSha1 | fileStates.fileHash.hashValue |
| **file**:hashes.peSha256 | fileStates.fileHash.hashValue |
| **file**:hashes.unknown | fileStates.fileHash.hashValue |
| **process**:name | processes.name, processes.parentProcessName |
| **process**:parent_ref.name | processes.parentProcessName |
| **process**:command_line | processes.commandLine |
| **process**:pid | processes.processId, processes.parentProcessId, registryKeyStates.processId |
| **process**:created | processes.createdDateTime |
| **process**:parent_ref.pid | processes.parentProcessId |
| **process**:binary_ref.parent_directory_ref.path | processes.path |
| **domain-name**:value | hostStates.fqdn, hostStates.netBiosName, networkConnections.destinationDomain, userStates.domainName |
| **user-account**:user_id | userStates.accountName, processes.accountName, userStates.aadUserId |
| **user-account**:account_login | userStates.logonId |
| **user-account**:account_type | userStates.userAccountType |
| **user-account**:account_last_login | userStates.logonDateTime |
| **software**:name | vendorInformation.provider |
| **software**:vendor | vendorInformation.vendor |
| **software**:version | vendorInformation.providerVersion |
| **url**:value | networkConnections.destinationUrl |
| **windows-registry-key**:key | registryKeyStates.key |
| **windows-registry-key**:values[*].data | registryKeyStates.valueData |
| **windows-registry-key**:values[*].name | registryKeyStates.valueName |
| **windows-registry-key**:values[*].data_type | registryKeyStates.valueType |
| **x-msazure-sentinel**:tenant_id | azureTenantId |
| **x-msazure-sentinel**:subscription_id | azureSubscriptionId |
| **x-msazure-sentinel-alert**:activityGroupName | activityGroupName |
| **x-msazure-sentinel-alert**:assignedTo | assignedTo |
| **x-msazure-sentinel-alert**:comments | comments |
| **x-msazure-sentinel-alert**:confidence | confidence |
| **x-msazure-sentinel-alert**:detectionIds | detectionIds |
| **x-msazure-sentinel-alert**:feedback | feedback |
| **x-msazure-sentinel-alert**:id | id |
| **x-msazure-sentinel-alert**:incidentIds | incidentIds |
| **x-msazure-sentinel-alert**:recommendedActions | recommendedActions |
| **x-msazure-sentinel-alert**:sourceMaterials | sourceMaterials |
| **x-msazure-sentinel-alert**:status | status |
| **x-msazure-sentinel-alert**:tags | tags |
| **x-msazure-sentinel-alert**:cloudAppStates.destinationServiceName | cloudAppStates.destinationServiceName |
| **x-msazure-sentinel-alert**:cloudAppStates.destinationServiceIp | cloudAppStates.destinationServiceIp |
| **x-msazure-sentinel-alert**:cloudAppStates.riskScore | cloudAppStates.riskScore |
| **x-msazure-sentinel-alert**:hostStates.isAzureAadJoined | hostStates.isAzureAadJoined |
| **x-msazure-sentinel-alert**:hostStates.isAzureAadRegistered | hostStates.isAzureAadRegistered |
| **x-msazure-sentinel-alert**:hostStates.isHybridAzureDomainJoined | hostStates.isHybridAzureDomainJoined |
| **x-msazure-sentinel-alert**:hostStates.os | hostStates.os |
| **x-msazure-sentinel-alert**:hostStates.publicIpAddress | hostStates.publicIpAddress |
| **x-msazure-sentinel-alert**:hostStates.privateIpAddress | hostStates.privateIpAddress |
| **x-msazure-sentinel-alert**:hostStates.riskScore | hostStates.riskScore |
| **x-msazure-sentinel-alert**:malwareStates.category | malwareStates.category |
| **x-msazure-sentinel-alert**:malwareStates.family | malwareStates.family |
| **x-msazure-sentinel-alert**:malwareStates.name | malwareStates.family |
| **x-msazure-sentinel-alert**:malwareStates.severity | malwareStates.family |
| **x-msazure-sentinel-alert**:malwareStates.wasRunning | malwareStates.family |
| **x-msazure-sentinel-alert**:networkConnections.applicationName | networkConnections.applicationName |
| **x-msazure-sentinel-alert**:networkConnections.direction | networkConnections.direction |
| **x-msazure-sentinel-alert**:networkConnections.domainRegisteredDateTime | networkConnections.domainRegisteredDateTime |
| **x-msazure-sentinel-alert**:networkConnections.localDnsName | networkConnections.localDnsName |
| **x-msazure-sentinel-alert**:networkConnections.natDestinationPort | networkConnections.natDestinationPort |
| **x-msazure-sentinel-alert**:networkConnections.natSourcePort | networkConnections.natSourcePort |
| **x-msazure-sentinel-alert**:networkConnections.riskScore | networkConnections.riskScore |
| **x-msazure-sentinel-alert**:networkConnections.status | networkConnections.status |
| **x-msazure-sentinel-alert**:processes.integrityLevel | processes.integrityLevel |
| **x-msazure-sentinel-alert**:processes.isElevated | processes.isElevated |
| **x-msazure-sentinel-alert**:securityResources.resource | securityResources.resource |
| **x-msazure-sentinel-alert**:securityResources.resourceType | securityResources.resourceType |
| **x-msazure-sentinel-alert**:triggers.name | triggers.name |
| **x-msazure-sentinel-alert**:triggers.type | triggers.type |
| **x-msazure-sentinel-alert**:triggers.value | triggers.value |
| **x-msazure-sentinel-alert**:userStates.logonIp | userStates.logonIp |
| **x-msazure-sentinel-alert**:userStates.aadUserId | userStates.aadUserId |
| **x-msazure-sentinel-alert**:userStates.emailRole | userStates.emailRole |
| **x-msazure-sentinel-alert**:userStates.isVpn | userStates.isVpn |
| **x-msazure-sentinel-alert**:userStates.logonLocation | userStates.logonLocation |
| **x-msazure-sentinel-alert**:userStates.logonType | userStates.logonType |
| **x-msazure-sentinel-alert**:userStates.onPremisesSecurityIdentifier | userStates.onPremisesSecurityIdentifier |
| **x-msazure-sentinel-alert**:userStates.riskScore | userStates.riskScore |
| **x-msazure-sentinel-alert**:userStates.userAccountType | userStates.userAccountType |
| **x-msazure-sentinel-alert**:userStates.userPrincipalName | userStates.userPrincipalName |
| **x-msazure-sentinel-alert**:vulnerabilityStates.cve | vulnerabilityStates.cve |
| **x-msazure-sentinel-alert**:vulnerabilityStates.severity | vulnerabilityStates.severity |
| **x-msazure-sentinel-alert**:vulnerabilityStates.wasRunning | vulnerabilityStates.wasRunning |
| **x-ibm-finding**:name | title |
| **x-ibm-finding**:description | description |
| **x-ibm-finding**:severity | severity |
| **x-ibm-finding**:start | createdDateTime |
| **x-ibm-finding**:end | closedDateTime |
| **x-ibm-finding**:finding_type | category |
| **x-ibm-finding**:src_ip_ref.value | networkConnections.natSourceAddress |
| **x-ibm-finding**:dst_ip_ref.value | networkConnections.natDestinationAddress |
| **x-ibm-finding**:src_os_ref.name | hostStates.os |
| **x-ibm-finding**:dst_application_ref.name | cloudAppStates.destinationServiceName |
| **x-ibm-finding**:src_geolocation | networkConnections.sourceLocation |
| **x-ibm-finding**:dst_geolocation | networkConnections.destinationLocation |
| **x-ibm-finding**:src_application_user_ref.user_id | userStates.aadUserId |
| **x-ibm-finding**:src_application_user_ref.type | userStates.logonType |
| **x-ibm-finding**:time_observed | lastModifiedDateTime |
| **x-oca-event**:action | title |
| **x-oca-event**:code | id |
| **x-oca-event**:category | category |
| **x-oca-event**:created | createdDateTime |
| **x-oca-event**:provider | vendorInformation.subProvider |
| **x-oca-event**:domain_ref.value | networkConnections.urlParameters |
| **x-oca-event**:url_ref.value | networkConnections.urlParameters |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| directory | path | path |
| <br> | | |
| domain-name | value | fqdn |
| domain-name | value | destinationDomain |
| domain-name | value | domainName |
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
| windows-registry-key | values.data | registryKeyStates |
| windows-registry-key | values.name | registryKeyStates |
| windows-registry-key | values.data_type | registryKeyStates |
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
