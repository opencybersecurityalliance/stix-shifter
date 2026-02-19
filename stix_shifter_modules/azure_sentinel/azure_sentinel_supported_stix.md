##### Updated on 05/23/24
## Microsoft Graph Security
### Results STIX Domain Objects
* Identity
* Observed Data
<br>
### Supported STIX Operators
*Comparison AND/OR operators are inside the observation while observation AND/OR operators are between observations (square brackets).*

| STIX Operator | Data Source Operator |
|--|--|
| AND (Comparison) | and |
| OR (Comparison) | or |
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
### Searchable STIX objects and properties for Alert dialect
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **ipv4-addr**:value | networkConnections.sourceAddress, networkConnections.destinationAddress, networkConnections.natSourceAddress, networkConnections.natDestinationAddress |
| **ipv6-addr**:value | networkConnections.sourceAddress, networkConnections.destinationAddress |
| **network-traffic**:src_port | networkConnections.sourcePort, networkConnections.natSourcePort, networkConnections.natDestinationPort |
| **network-traffic**:dst_port | networkConnections.destinationPort, networkConnections.natDestinationPort |
| **network-traffic**:protocols[*] | networkConnections.protocol |
| **network-traffic**:src_ref.value | networkConnections.sourceAddress |
| **network-traffic**:dst_ref.value | networkConnections.destinationAddress |
| **network-traffic**:x_applicationName | networkConnections.applicationName |
| **network-traffic**:x_direction | networkConnections.direction |
| **network-traffic**:x_domainRegisteredDateTime | networkConnections.domainRegisteredDateTime |
| **network-traffic**:x_localDnsName | networkConnections.localDnsName |
| **network-traffic**:x_riskScore | networkConnections.riskScore |
| **network-traffic**:x_status | networkConnections.status |
| **network-traffic**:x_urlParameters | networkConnections.urlParameters |
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
| **process**:x_integrityLevel | processes.integrityLevel |
| **process**:x_isElevated | processes.isElevated |
| **domain-name**:value | hostStates.fqdn, hostStates.netBiosName, networkConnections.destinationDomain, userStates.domainName |
| **user-account**:user_id | userStates.accountName, processes.accountName, userStates.aadUserId |
| **user-account**:account_login | userStates.logonId |
| **user-account**:account_type | userStates.userAccountType |
| **user-account**:account_last_login | userStates.logonDateTime |
| **user-account**:x_aadUserId | userStates.aadUserId |
| **user-account**:x_emailRole | userStates.emailRole |
| **user-account**:x_isVpn | userStates.isVpn |
| **user-account**:x_logonLocation | userStates.logonLocation |
| **user-account**:x_logonType | userStates.logonType |
| **user-account**:x_onPremisesSecurityIdentifier | userStates.onPremisesSecurityIdentifier |
| **user-account**:x_riskScore | userStates.riskScore |
| **user-account**:x_userAccountType | userStates.userAccountType |
| **user-account**:x_userPrincipalName | userStates.userPrincipalName |
| **software**:name | vendorInformation.provider, networkConnections.applicationName |
| **software**:vendor | vendorInformation.vendor |
| **software**:version | vendorInformation.providerVersion |
| **url**:value | networkConnections.destinationUrl |
| **windows-registry-key**:key | registryKeyStates.key |
| **windows-registry-key**:values[*].data | registryKeyStates.valueData |
| **windows-registry-key**:values[*].name | registryKeyStates.valueName |
| **windows-registry-key**:values[*].data_type | registryKeyStates.valueType |
| **x-msazure-sentinel**:tenant_id | azureTenantId |
| **x-msazure-sentinel**:subscription_id | azureSubscriptionId |
| **x-ibm-finding**:name | title |
| **x-ibm-finding**:alert_id | id |
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
| **x-ibm-finding**:src_application_ref | networkConnections.applicationName |
| **x-ibm-finding**:src_application_user_ref.user_id | userStates.aadUserId |
| **x-ibm-finding**:src_application_user_ref.type | userStates.logonType |
| **x-ibm-finding**:time_observed | lastModifiedDateTime |
| **x-ibm-finding**:x_activityGroupName | activityGroupName |
| **x-ibm-finding**:x_assignedTo | assignedTo |
| **x-ibm-finding**:x_comments | comments |
| **x-ibm-finding**:confidence | confidence |
| **x-ibm-finding**:x_detectionIds | detectionIds |
| **x-ibm-finding**:x_feedback | feedback |
| **x-ibm-finding**:x_incidentIds | incidentIds |
| **x-ibm-finding**:x_recommendedActions | recommendedActions |
| **x-ibm-finding**:x_sourceMaterials | sourceMaterials |
| **x-ibm-finding**:x_status | status |
| **x-ibm-finding**:x_tags | tags |
| **x-ibm-finding**:x_cloudAppStates.destinationServiceName | cloudAppStates.destinationServiceName |
| **x-ibm-finding**:x_cloudAppStates.destinationServiceIp | cloudAppStates.destinationServiceIp |
| **x-ibm-finding**:x_cloudAppStates.riskScore | cloudAppStates.riskScore |
| **x-ibm-finding**:x_hostStates.isAzureAadJoined | hostStates.isAzureAadJoined |
| **x-ibm-finding**:x_hostStates.isAzureAadRegistered | hostStates.isAzureAadRegistered |
| **x-ibm-finding**:x_hostStates.isHybridAzureDomainJoined | hostStates.isHybridAzureDomainJoined |
| **x-ibm-finding**:x_hostStates.os | hostStates.os |
| **x-ibm-finding**:x_hostStates.publicIpAddress | hostStates.publicIpAddress |
| **x-ibm-finding**:x_hostStates.privateIpAddress | hostStates.privateIpAddress |
| **x-ibm-finding**:x_hostStates.riskScore | hostStates.riskScore |
| **x-ibm-finding**:x_malwareStates.category | malwareStates.category |
| **x-ibm-finding**:x_malwareStates.family | malwareStates.family |
| **x-ibm-finding**:x_malwareStates.name | malwareStates.family |
| **x-ibm-finding**:x_malwareStates.severity | malwareStates.family |
| **x-ibm-finding**:x_malwareStates.wasRunning | malwareStates.family |
| **x-ibm-finding**:x_securityResources.resource | securityResources.resource |
| **x-ibm-finding**:x_securityResources.resourceType | securityResources.resourceType |
| **x-ibm-finding**:x_triggers.name | triggers.name |
| **x-ibm-finding**:x_triggers.type | triggers.type |
| **x-ibm-finding**:x_triggers.value | triggers.value |
| **x-ibm-finding**:x_vulnerabilityStates.cve | vulnerabilityStates.cve |
| **x-ibm-finding**:x_vulnerabilityStates.severity | vulnerabilityStates.severity |
| **x-ibm-finding**:x_vulnerabilityStates.wasRunning | vulnerabilityStates.wasRunning |
| **x-oca-event**:action | title |
| **x-oca-event**:category | category |
| **x-oca-event**:created | createdDateTime |
| **x-oca-event**:provider | vendorInformation.subProvider |
| <br> | |
### Searchable STIX objects and properties for Alertv2 dialect
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **software**:name | serviceSource |
| **x-ibm-finding**:severity | severity |
| **x-ibm-finding**:x_assignedTo | assignedTo |
| **x-ibm-finding**:x_classification | classification |
| **x-ibm-finding**:x_determination | determination |
| **x-ibm-finding**:x_lastUpdateDateTime | lastUpdateDateTime |
| **x-ibm-finding**:x_status | status |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| directory | path | path |
| directory | path | filePath |
| <br> | | |
| domain-name | value | fqdn |
| domain-name | value | destinationDomain |
| domain-name | value | domainName |
| domain-name | value | deviceDnsName |
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
| file | x_detectionStatus | detectionStatus |
| file | x_mdeDeviceId | mdeDeviceId |
| file | name | fileName |
| file | parent_directory_ref | filePath |
| file | size | fileSize |
| file | x_filePublisher | filePublisher |
| file | x_signer | signer |
| file | x_issuer | issuer |
| <br> | | |
| ipv4-addr | value | privateIpAddress |
| ipv4-addr | value | publicIpAddress |
| ipv4-addr | value | destinationAddress |
| ipv4-addr | value | natDestinationAddress |
| ipv4-addr | value | natSourceAddress |
| ipv4-addr | value | sourceAddress |
| ipv4-addr | value | logonIp |
| ipv4-addr | value | ipAddress |
| ipv4-addr | x_country_letter_code | countryLetterCode |
| <br> | | |
| network-traffic | dst_ref | destinationAddress |
| network-traffic | dst_port | destinationPort |
| network-traffic | x_direction | direction |
| network-traffic | x_domainRegisteredDateTime | domainRegisteredDateTime |
| network-traffic | x_localDnsName | localDnsName |
| network-traffic | x_nat_destination_address | natDestinationAddress |
| network-traffic | x_nat_destination_port | natDestinationPort |
| network-traffic | x_nat_src_ref | natSourceAddress |
| network-traffic | x_nat_source_port | natSourcePort |
| network-traffic | protocols | protocol |
| network-traffic | x_riskScore | riskScore |
| network-traffic | src_ref | sourceAddress |
| network-traffic | src_port | sourcePort |
| network-traffic | x_status | status |
| network-traffic | x_url_parameters | urlParameters |
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
| process | command_line | processCommandLine |
| process | created | processCreationDateTime |
| process | created | parentProcessCreationDateTime |
| process | x_detectionStatus | detectionStatus |
| process | x_mdeDeviceId | mdeDeviceId |
| process | binary_ref | fileName |
| <br> | | |
| processes | x_integrityLevel | integrityLevel |
| processes | x_isElevated | isElevated |
| <br> | | |
| software | name | destinationServiceName |
| software | name | os |
| software | name | applicationName |
| software | name | provider |
| software | vendor | vendor |
| software | version | providerVersion |
| software | name | serviceSource |
| software | name | detectionSource |
| software | name | osPlatform |
| software | version | version |
| <br> | | |
| url | value | destinationUrl |
| url | value | alertWebUrl |
| url | value | incidentWebUrl |
| url | value | url |
| <br> | | |
| user-account | user_id | accountName |
| user-account | x_aad_user_id | aadUserId |
| user-account | x_email_role | emailRole |
| user-account | x_isvpn | isVpn |
| user-account | account_last_login | logonDateTime |
| user-account | account_login | logonId |
| user-account | x_logon_location | logonLocation |
| user-account | x_logon_type | logonType |
| user-account | x_on_premises_security_identifier | onPremisesSecurityIdentifier |
| user-account | x_riskScore | riskScore |
| user-account | x_user_account_type | userAccountType |
| user-account | x_user_principal_name | userPrincipalName |
| user-account | user_id | actorDisplayName |
| user-account | x_azure_domain_name | domainName |
| user-account | x_userSid | userSid |
| user-account | x_azureAdUserId | azureAdUserId |
| user-account | x_userPrincipalName | userPrincipalName |
| user-account | x_user_sid | userSid |
| user-account | x_azure_ad_userid | azureAdUserId |
| <br> | | |
| windows-registry-key | key | registryKeyStates |
| windows-registry-key | values.data | registryKeyStates |
| windows-registry-key | values.name | registryKeyStates |
| windows-registry-key | values.data_type | registryKeyStates |
| windows-registry-key | key | registryKey |
| windows-registry-key | x_registryHive | registryHive |
| windows-registry-key | x_registry_hive | registryHive |
| windows-registry-key | values.data | registryValue |
| windows-registry-key | values.name | registryValueName |
| windows-registry-key | values.data_type | registryValueType |
| <br> | | |
| x-alert-evidence | evidence_type | @odata.type |
| x-alert-evidence | process_ref | @odata.type |
| x-alert-evidence | created | createdDateTime |
| x-alert-evidence | verdict | verdict |
| x-alert-evidence | remediationStatus | remediationStatus |
| x-alert-evidence | remediationStatusDetails | remediationStatusDetails |
| x-alert-evidence | roles | roles |
| x-alert-evidence | tags | tags |
| x-alert-evidence | registry_ref | @odata.type |
| x-alert-evidence | ip_ref | @odata.type |
| x-alert-evidence | user_ref | @odata.type |
| <br> | | |
| x-ibm-finding | x_activityGroupName | activityGroupName |
| x-ibm-finding | x_assignedTo | assignedTo |
| x-ibm-finding | dst_application_ref | destinationServiceName |
| x-ibm-finding | x_cloudAppStates.destinationServiceIp | destinationServiceIp |
| x-ibm-finding | x_cloudAppStates.riskScore | riskScore |
| x-ibm-finding | x_comments | comments |
| x-ibm-finding | confidence | confidence |
| x-ibm-finding | description | description |
| x-ibm-finding | x_detectionids | detectionIds |
| x-ibm-finding | x_feedback | feedback |
| x-ibm-finding | x_fileStates.riskScore | riskScore |
| x-ibm-finding | x_hostStates.isAzureAadJoined | isAzureAadJoined |
| x-ibm-finding | x_hostStates.isAzureAadRegistered | isAzureAadRegistered |
| x-ibm-finding | x_hostStates.isHybridAzureDomainJoined | isHybridAzureDomainJoined |
| x-ibm-finding | src_os_ref | os |
| x-ibm-finding | x_hostStates.riskScore | riskScore |
| x-ibm-finding | alert_id | id |
| x-ibm-finding | x_incidentIds | incidentIds |
| x-ibm-finding | time_observed | lastModifiedDateTime |
| x-ibm-finding | x_malwareStates.category | category |
| x-ibm-finding | x_malwareStates.family | family |
| x-ibm-finding | x_malwareStates.name | name |
| x-ibm-finding | x_malwareStates.severity | severity |
| x-ibm-finding | x_malwareStates.wasRunning | wasRunning |
| x-ibm-finding | src_application_ref | applicationName |
| x-ibm-finding | dst_geolocation | destinationLocation |
| x-ibm-finding | src_geolocation | sourceLocation |
| x-ibm-finding | x_recommendedactions | recommendedActions |
| x-ibm-finding | x_registryKeyStates.hive | registryKeyStates |
| x-ibm-finding | x_registryKeyStates.oldKey | registryKeyStates |
| x-ibm-finding | x_registryKeyStates.oldValueData | registryKeyStates |
| x-ibm-finding | x_registryKeyStates.oldValueName | registryKeyStates |
| x-ibm-finding | x_registryKeyStates.operation | registryKeyStates |
| x-ibm-finding | x_securityresources.resource | resource |
| x-ibm-finding | x_securityresources.resourcetype | resourceType |
| x-ibm-finding | severity | severity |
| x-ibm-finding | x_sourcematerials | sourceMaterials |
| x-ibm-finding | x_status | status |
| x-ibm-finding | x_tags | tags |
| x-ibm-finding | name | title |
| x-ibm-finding | x_triggers.name | name |
| x-ibm-finding | x_triggers.type | type |
| x-ibm-finding | x_triggers.value | value |
| x-ibm-finding | x_vulnerabilityStates.cve | cve |
| x-ibm-finding | x_vulnerabilityStates.severity | severity |
| x-ibm-finding | x_vulnerabilityStates.wasRunning | wasRunning |
| x-ibm-finding | finding_type | @odata.type |
| x-ibm-finding | alert_id | providerAlertId |
| x-ibm-finding | x_incidentId | incidentId |
| x-ibm-finding | x_classification | classification |
| x-ibm-finding | x_determination | determination |
| x-ibm-finding | x_detectorId | detectorId |
| x-ibm-finding | x_tenantId | tenantId |
| x-ibm-finding | x_threatDisplayName | threatDisplayName |
| x-ibm-finding | x_threatFamilyName | threatFamilyName |
| x-ibm-finding | x_mitreTechniques | mitreTechniques |
| x-ibm-finding | x_lastUpdateDateTime | lastUpdateDateTime |
| x-ibm-finding | end | resolvedDateTime |
| x-ibm-finding | start | firstActivityDateTime |
| x-ibm-finding | x_lastActivityDateTime | lastActivityDateTime |
| <br> | | |
| x-microsoft-graph | tenant_id | azureTenantId |
| x-microsoft-graph | subscription_id | azureSubscriptionId |
| <br> | | |
| x-oca-asset | x_firstSeenDateTime | firstSeenDateTime |
| x-oca-asset | device_id | mdeDeviceId |
| x-oca-asset | x_azureAdDeviceId | azureAdDeviceId |
| x-oca-asset | os_ref | osPlatform |
| x-oca-asset | x_tags | osBuild |
| x-oca-asset | x_tags | healthStatus |
| x-oca-asset | x_tags | riskScore |
| x-oca-asset | x_tags | rbacGroupId |
| x-oca-asset | x_tags | rbacGroupName |
| x-oca-asset | x_tags | onboardingStatus |
| x-oca-asset | x_tags | defenderAvStatus |
| x-oca-asset | x_tags | loggedOnUsers |
| x-oca-asset | x_vmMetadata | vmMetadata |
| <br> | | |
| x-oca-event | category | category |
| x-oca-event | created | createdDateTime |
| x-oca-event | action | title |
| x-oca-event | provider | subProvider |
| <br> | | |
