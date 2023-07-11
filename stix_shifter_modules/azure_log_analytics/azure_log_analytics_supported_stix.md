##### Updated on 25/05/23
## Azure Log Analytics
### Supported STIX Operators
*Comparison AND/OR operators are inside the observation while observation AND/OR operators are between observations (square brackets).*

| STIX Operator | Data Source Operator |
|--|--|
| AND (Comparision) | and |
| OR (Comparision) | or |
| = | == |
| != | != |
| IN | in~ |
| MATCHES | matches |
| > | > |
| >= | >= |
| < | < |
| <= | <= |
| LIKE | contains |
| OR (Observation) | OR |
| AND (Observation) | OR |
| <br> | |
### Searchable STIX objects and properties for Securityalert dialect
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **ipv4-addr**:value | Entities.Address |
| **ipv4-addr**:x_location_ref.country | Entities.Location.CountryName |
| **ipv4-addr**:x_location_ref.city | Entities.Location.City |
| **ipv4-addr**:x_location_ref.carrier | Entities.Location.Carrier |
| **ipv4-addr**:x_location_ref.longitude | Entities.Location.Longitude |
| **ipv4-addr**:x_location_ref.latitude | Entities.Location.Latitude |
| **ipv4-addr**:x_location_ref.organization | Entities.Location.Organization |
| **ipv6-addr**:value | Entities.Address |
| **ipv6-addr**:x_location_ref.country | Entities.Location.CountryName |
| **ipv6-addr**:x_location_ref.city | Entities.Location.City |
| **ipv6-addr**:x_location_ref.carrier | Entities.Location.Carrier |
| **ipv6-addr**:x_location_ref.longitude | Entities.Location.Longitude |
| **ipv6-addr**:x_location_ref.latitude | Entities.Location.Latitude |
| **ipv6-addr**:x_location_ref.organization | Entities.Location.Organization |
| **user-account**:name | Entities.Name |
| **user-account**:user_id | Entities.AadUserId |
| **user-account**:display_name | Entities.DisplayName |
| **user-account**:x_nt_domain | Entities.NTDomain |
| **user-account**:x_dns_domain | Entities.DnsDomain |
| **user-account**:x_upn_suffix | Entities.UPNSuffix |
| **user-account**:x_passport_userid | Entities.PUID |
| **user-account**:x_account_sid | Entities.Sid |
| **user-account**:x_is_domain_account | Entities.IsDomainJoined |
| **network-traffic**:dst_port | Entities.DestinationPort |
| **network-traffic**:protocols[*] | Entities.Protocol |
| **network-traffic**:src_ref.value | Entities.Address |
| **file**:name | Entities.Name |
| **file**:hashes.'SHA-256' | Entities.Value |
| **file**:hashes.'SHA-1' | Entities.Value |
| **file**:hashes.MD5 | Entities.Value |
| **file**:parent_directory_ref.path | Entities.Directory |
| **directory**:path | Entities.Directory |
| **process**:pid | Entities.ProcessId |
| **process**:command_line | Entities.CommandLine |
| **process**:created | Entities.CreationTimeUtc |
| **process**:x_elevation_token | Entities.ElevationToken |
| **process**:creator_user_ref.user_id | Entities.Name |
| **process**:binary_ref.hashes.MD5 | Entities.Value |
| **process**:binary_ref.hashes.'SHA-256' | Entities.Value |
| **process**:binary_ref.hashes.'SHA1' | Entities.Value |
| **process**:parent_ref.pid | Entities.ProcessId |
| **process**:parent_ref.command_line | Entities.CommandLine |
| **process**:parent_ref.binary_ref.hashes.MD5 | Entities.Value |
| **process**:parent_ref.binary_ref.hashes.'SHA-256' | Entities.Value |
| **process**:parent_ref.binary_ref.hashes.'SHA1' | Entities.Value |
| **domain-name**:value | Entities.DomainName |
| **url**:value | Entities.Url |
| **software**:name | Entities.OSFamily, ProductName |
| **software**:version | Entities.OSVersion |
| **software**:vendor | VendorName |
| **software**:x_product_component_name | ProductComponentName |
| **software**:x_provider | ProviderName |
| **x-oca-asset**:hostname | Entities.HostName |
| **x-oca-asset**:x_resource_id | ResourceId |
| **x-oca-asset**:x_nt_domain | Entities.NTDomain |
| **x-oca-asset**:x_netbios_name | Entities.NetBiosName |
| **x-oca-asset**:x_oms_agent_id | Entities.OMSAgentID |
| **x-oca-asset**:os_ref.name | Entities.OSFamily |
| **x-oca-asset**:os_ref.version | Entities.OSVersion |
| **x-oca-asset**:x_is_domain_host | Entities.IsDomainJoined |
| **x-ibm-finding**:x_alert_link | AlertLink |
| **x-ibm-finding**:name | AlertName |
| **x-ibm-finding**:severity | AlertSeverity |
| **x-ibm-finding**:x_alert_type | AlertType |
| **x-ibm-finding**:x_compromised_entity | CompromisedEntity |
| **x-ibm-finding**:x_confidence_level | ConfidenceLevel |
| **x-ibm-finding**:confidence | ConfidenceScore |
| **x-ibm-finding**:description | Description |
| **x-ibm-finding**:end | EndTime |
| **x-ibm-finding**:x_processing_endtime | ProcessingEndTime |
| **x-ibm-finding**:x_remediationSteps | RemediationSteps |
| **x-ibm-finding**:start | StartTime |
| **x-ibm-finding**:x_status | Status |
| **x-ibm-finding**:x_system_alert_id | SystemAlertId |
| **x-ibm-finding**:alert_id | VendorOriginalId |
| **x-ibm-finding**:time_observed | TimeGenerated |
| **x-ibm-finding**:finding_type | Type |
| **x-ibm-finding**:ttp_tagging_refs[*].name | AlertName |
| **x-ibm-finding**:ttp_tagging_refs[*].confidence | ConfidenceScore |
| **x-ibm-finding**:ttp_tagging_refs[*].extensions.'mitre-attack-ext'.tactic_name | Tactics |
| **x-ibm-finding**:ttp_tagging_refs[*].extensions.'mitre-attack-ext'.technique_name | Techniques |
| **x-ibm-finding**:ioc_refs[*].value | Entities.Name, Entities.Address, Entities.Url, Entities.DomainName |
| **x-ibm-finding**:dst_application_ref.name | ProductName |
| **x-ibm-finding**:dst_application_ref.vendor | VendorName |
| **x-ibm-finding**:dst_os_ref.name | Entities.OSFamily |
| **x-ibm-finding**:dst_os_ref.version | Entities.OSVersion |
| **x-ibm-finding**:dst_os_user_ref.user_id | Entities.Name |
| **x-ibm-ttp-tagging**:name | AlertName |
| **x-ibm-ttp-tagging**:confidence | ConfidenceScore |
| **x-ibm-ttp-tagging**:extensions.'mitre-attack-ext'.tactic_name | Tactics |
| **x-ibm-ttp-tagging**:extensions.'mitre-attack-ext'.technique_name | Techniques |
| **x-geo-location**:country | Entities.Location.CountryName |
| **x-geo-location**:city | Entities.Location.City |
| **x-geo-location**:carrier | Entities.Location.Carrier |
| **x-geo-location**:longitude | Entities.Location.Longitude |
| **x-geo-location**:latitude | Entities.Location.Latitude |
| **x-geo-location**:organization | Entities.Location.Organization |
| **x-cloud-provider**:tenant_id | TenantId |
| **x-cloud-resource**:resource_type | ExtendedProperties.resourceType |
| **x-cloud-resource**:resource_id | ResourceId |
| **x-host-logon-session**:session_id | Entities.SessionId |
| **x-host-logon-session**:start_time | Entities.StartTimeUtc |
| **x-host-logon-session**:end_time | Entities.EndTimeUtc |
| **x-azure-blob**:name | Entities.Name |
| **x-azure-blob**:etag | Entities.Etag |
| **x-azure-blob**:blob_container | Entities.Name |
| **x-azure-malware**:name | Entities.Name |
| **x-azure-malware**:category | Entities.Category |
| **x-azure-container**:container_id | Entities.ContainerId |
| **x-azure-container**:image_id | Entities.ImageId |
| **x-azure-container**:image_type | Entities.Type |
| **x-k8s-cluster**:name | Entities.Name |
| <br> | |
### Searchable STIX objects and properties for Securityevent dialect
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **ipv4-addr**:value | IpAddress, ClientIPAddress |
| **ipv6-addr**:value | IpAddress, ClientIPAddress |
| **user-account**:account_login | TargetUserName, SubjectUserName |
| **user-account**:user_id | TargetUserName, SubjectUserName |
| **user-account**:display_name | TargetAccount, SubjectAccount |
| **user-account**:x_domain_name | TargetDomainName, SubjectDomainName |
| **user-account**:x_login_id | TargetLogonId, SubjectLogonId |
| **user-account**:x_user_sid | TargetUserSid, SubjectUserSid |
| **directory**:path | HomeDirectory, HomePath, ProcessName, ParentProcessName, NewProcessName |
| **file**:name | FilePath |
| **file**:path | FilePath |
| **file**:hashes.'SHA-256' | FileHash |
| **file**:hashes.MD5 | FileHash |
| **file**:hashes.'SHA-1' | FileHash |
| **file**:parent_directory_ref | ProcessName, ParentProcessName |
| **file**:x_fqbn | Fqbn |
| **process**:parent_ref.name | ParentProcessName |
| **process**:command_line | CommandLine |
| **process**:pid | ProcessId, NewProcessId |
| **process**:x_token_elevation_type | TokenElevationType |
| **process**:x_mandatory_label | MandatoryLabel |
| **url**:value | QuarantineHelpURL |
| **x-ibm-finding**:alert_id | EventOriginId |
| **x-ibm-finding**:start | PreviousTime |
| **x-ibm-finding**:name | Activity |
| **x-ibm-finding**:finding_type | Type |
| **x-ibm-finding**:time_observed | TimeGenerated |
| **x-ibm-finding**:src_ip_ref | IpAddress |
| **x-ibm-finding**:dst_device | WorkstationName, TargetServerName |
| **x-ibm-finding**:src_application_user_ref | TargetUserName |
| **x-ibm-finding**:dst_application_user_ref | SubjectUserName |
| **x-ibm-finding**:ioc_refs | FilePath, IpAddress, ClientIPAddress |
| **x-oca-event**:module | Channel |
| **x-oca-event**:provider | EventSourceName |
| **x-oca-event**:action | Activity |
| **x-oca-event**:created | TimeCollected |
| **x-oca-event**:modified | TimeCollected |
| **x-oca-event**:code | EventID |
| **x-oca-event**:dataset | EventData |
| **x-oca-event**:host_ref | Computer |
| **x-oca-event**:url_ref | QuarantineHelpURL |
| **x-oca-event**:process_ref | NewProcessName, Process, ProcessName |
| **x-oca-event**:file_ref.hash | FileHash |
| **x-oca-event**:file_ref.path | FilePath |
| **x-oca-event**:parent_process_ref | ParentProcessName |
| **x-oca-event**:user_ref | TargetUserName |
| **x-oca-event**:ip_refs.ip | IpAddress, ClientIPAddress |
| **x-oca-event**:x_service_file | ServiceFileName |
| **x-oca-event**:x_service_name | ServiceName |
| **x-oca-event**:x_modified_account_sid | TargetSid |
| **x-oca-event**:x_description | DeviceDescription |
| **x-oca-event**:x_task | Task |
| **x-oca-event**:x_user_parameter | UserParameters |
| **x-oca-event**:x_member_name | MemberName |
| **x-oca-event**:x_requester | Requester |
| **x-cloud-resource**:resource_id | _ResourceId |
| **x-oca-asset**:device_id | DeviceId, SourceComputerId |
| **x-oca-asset**:hostname | Computer |
| **x-logon-info**:guid | LogonGuid |
| **x-logon-info**:logon_process | LogonProcessName |
| **x-logon-info**:logon_type | LogonType |
| **x-logon-info**:logon_type_name | LogonTypeName |
| **x-logon-info**:authentication_package_name | AuthenticationPackageName |
| <br> | |
### Searchable STIX objects and properties for Securityincident dialect
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **url**:value | IncidentUrl |
| **email-addr**:value | Owner.email, Owner.userPrincipalName |
| **email-addr**:display_name | Owner.assignedTo |
| **x-ibm-finding**:description | Description |
| **x-ibm-finding**:name | Title |
| **x-ibm-finding**:start | CreatedTime |
| **x-ibm-finding**:end | LastModifiedTime |
| **x-ibm-finding**:severity | Severity |
| **x-ibm-finding**:time_observed | TimeGenerated |
| **x-ibm-finding**:finding_type | Type |
| **x-ibm-finding**:rule_names[*] | RelatedAnalyticRuleIds |
| **x-ibm-finding**:x_owner_ref | Owner.email, Owner.userPrincipalName, Owner.assignedTo |
| **x-ibm-finding**:x_incident_name | IncidentName |
| **x-ibm-finding**:x_provider_incident_id | ProviderIncidentId |
| **x-ibm-finding**:x_modified_by | ModifiedBy |
| **x-ibm-finding**:x_status | Status |
| **x-ibm-finding**:x_provider | ProviderName |
| **x-ibm-finding**:ttp_tagging_refs[*].name | Title |
| **x-ibm-finding**:ttp_tagging_refs[*].extensions.'mitre-attack-ext'.tactic_name | AdditionalData.tactics |
| **x-ibm-finding**:ttp_tagging_refs[*].extensions.'mitre-attack-ext'.technique_name | AdditionalData.techniques |
| **x-ibm-finding**:x_owner_ref.value | Owner.email, Owner.userPrincipalName |
| **x-ibm-finding**:x_owner_ref.display_name | Owner.assignedTo |
| **x-ibm-finding**:x_alert_count | AdditionalData.alertsCount |
| **x-ibm-finding**:x_alert_product_names | AdditionalData.alertProductNames |
| **x-ibm-finding**:x_alert_ids[*] | AlertIds |
| **x-ibm-ttp-tagging**:name | Title |
| **x-ibm-ttp-tagging**:extensions.'mitre-attack-ext'.tactic_name | AdditionalData.tactics |
| **x-ibm-ttp-tagging**:extensions.'mitre-attack-ext'.technique_name | AdditionalData.techniques |
| **x-cloud-provider**:tenant_id | TenantId |
| **x-incident-info**:classification | Classification |
| **x-incident-info**:classification_comment | ClassificationComment |
| **x-incident-info**:classification_reason | ClassificationReason |
| **x-incident-info**:closed_time | ClosedTime |
| **x-incident-info**:comments | Comments |
| **x-incident-info**:first_activity | FirstActivityTime |
| **x-incident-info**:first_modified | FirstModifiedTime |
| **x-incident-info**:labels | Labels |
| **x-incident-info**:last_active | LastActivityTime |
| **x-incident-info**:tasks | Tasks |
| **x-incident-info**:incident_url_ref.value | IncidentUrl |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| ipv4-addr | value | Entities.Address |
| ipv4-addr | x_location_ref.country | Entities.Location.CountryName |
| ipv4-addr | x_location_ref.city | Entities.Location.City |
| ipv4-addr | x_location_ref.carrier | Entities.Location.Carrier |
| ipv4-addr | x_location_ref.longitude | Entities.Location.Longitude |
| ipv4-addr | x_location_ref.latitude | Entities.Location.Latitude |
| ipv4-addr | x_location_ref.organization | Entities.Location.Organization |
| <br> | | |
| ipv6-addr | value | Entities.Address |
| ipv6-addr | x_location_ref.country | Entities.Location.CountryName |
| ipv6-addr | x_location_ref.city | Entities.Location.City |
| ipv6-addr | x_location_ref.carrier | Entities.Location.Carrier |
| ipv6-addr | x_location_ref.longitude | Entities.Location.Longitude |
| ipv6-addr | x_location_ref.latitude | Entities.Location.Latitude |
| ipv6-addr | x_location_ref.organization | Entities.Location.Organization |
| <br> | | |
| user-account | user_id | Entities.Name |
| user-account | x_aad_user_id | Entities.AadUserId |
| user-account | display_name | Entities.DisplayName |
| user-account | x_nt_domain | Entities.NTDomain |
| user-account | x_dns_domain | Entities.DnsDomain |
| user-account | x_upn_suffix | Entities.UPNSuffix |
| user-account | x_passport_userid | Entities.PUID |
| user-account | x_account_sid | Entities.Sid |
| user-account | x_is_domain_account | Entities.IsDomainJoined |
| <br> | | |
| network-traffic | dst_port | Entities.DestinationPort |
| network-traffic | protocols | Entities.Protocol |
| network-traffic | src_ref.value | Entities.Address |
| <br> | | |
| file | name | Entities.Name |
| file | hashes.'SHA-256' | Entities.Value |
| file | hashes.'SHA-1' | Entities.Value |
| file | hashes.MD5 | Entities.Value |
| file | parent_directory_ref.path | Entities.Directory |
| <br> | | |
| directory | path | Entities.Directory |
| <br> | | |
| process | pid | Entities.ProcessId |
| process | command_line | Entities.CommandLine |
| process | created | Entities.CreationTimeUtc |
| process | x_elevation_token | Entities.ElevationToken |
| process | creator_user_ref.user_id | Entities.Name |
| process | binary_ref.hashes.MD5 | Entities.Value |
| process | binary_ref.hashes.'SHA-256' | Entities.Value |
| process | binary_ref.hashes.'SHA1' | Entities.Value |
| process | parent_ref.pid | Entities.ProcessId |
| process | parent_ref.command_line | Entities.CommandLine |
| process | parent_ref.binary_ref.hashes.MD5 | Entities.Value |
| process | parent_ref.binary_ref.hashes.'SHA-256' | Entities.Value |
| process | parent_ref.binary_ref.hashes.'SHA1' | Entities.Value |
| <br> | | |
| domain-name | value | Entities.DomainName |
| <br> | | |
| url | value | Entities.Url |
| <br> | | |
| software | name | Entities.OSFamily |
| software | name | ProductName |
| software | version | Entities.OSVersion |
| software | vendor | VendorName |
| software | x_product_component_name | ProductComponentName |
| software | x_provider | ProviderName |
| <br> | | |
| x-oca-asset | hostname | Entities.HostName |
| x-oca-asset | x_resource_id | ResourceId |
| x-oca-asset | x_nt_domain | Entities.NTDomain |
| x-oca-asset | x_netbios_name | Entities.NetBiosName |
| x-oca-asset | x_oms_agent_id | Entities.OMSAgentID |
| x-oca-asset | os_ref.name | Entities.OSFamily |
| x-oca-asset | os_ref.version | Entities.OSVersion |
| x-oca-asset | x_is_domain_host | Entities.IsDomainJoined |
| <br> | | |
| x-ibm-finding | x_alert_link | AlertLink |
| x-ibm-finding | name | AlertName |
| x-ibm-finding | severity | AlertSeverity |
| x-ibm-finding | x_alert_type | AlertType |
| x-ibm-finding | x_compromised_entity | CompromisedEntity |
| x-ibm-finding | x_confidence_level | ConfidenceLevel |
| x-ibm-finding | confidence | ConfidenceScore |
| x-ibm-finding | description | Description |
| x-ibm-finding | end | EndTime |
| x-ibm-finding | x_processing_endtime | ProcessingEndTime |
| x-ibm-finding | x_remediationSteps | RemediationSteps |
| x-ibm-finding | start | StartTime |
| x-ibm-finding | x_status | Status |
| x-ibm-finding | x_system_alert_id | SystemAlertId |
| x-ibm-finding | alert_id | VendorOriginalId |
| x-ibm-finding | time_observed | TimeGenerated |
| x-ibm-finding | finding_type | Type |
| x-ibm-finding | ttp_tagging_refs.name | AlertName |
| x-ibm-finding | ttp_tagging_refs.confidence | ConfidenceScore |
| x-ibm-finding | ttp_tagging_refs.extensions.'mitre-attack-ext'.tactic_name | Tactics |
| x-ibm-finding | ttp_tagging_refs.extensions.'mitre-attack-ext'.technique_name | Techniques |
| x-ibm-finding | ioc_refs.value | Entities.Name |
| x-ibm-finding | ioc_refs.value | Entities.Address |
| x-ibm-finding | ioc_refs.value | Entities.Url |
| x-ibm-finding | ioc_refs.value | Entities.DomainName |
| x-ibm-finding | dst_application_ref.name | ProductName |
| x-ibm-finding | dst_application_ref.vendor | VendorName |
| x-ibm-finding | dst_os_ref.name | Entities.OSFamily |
| x-ibm-finding | dst_os_ref.version | Entities.OSVersion |
| x-ibm-finding | dst_os_user_ref.user_id | Entities.Name |
| <br> | | |
| x-ibm-ttp-tagging | name | AlertName |
| x-ibm-ttp-tagging | confidence | ConfidenceScore |
| x-ibm-ttp-tagging | extensions.'mitre-attack-ext'.tactic_name | Tactics |
| x-ibm-ttp-tagging | extensions.'mitre-attack-ext'.technique_name | Techniques |
| <br> | | |
| x-geo-location | country | Entities.Location.CountryName |
| x-geo-location | city | Entities.Location.City |
| x-geo-location | carrier | Entities.Location.Carrier |
| x-geo-location | longitude | Entities.Location.Longitude |
| x-geo-location | latitude | Entities.Location.Latitude |
| x-geo-location | organization | Entities.Location.Organization |
| <br> | | |
| x-cloud-provider | tenant_id | TenantId |
| <br> | | |
| x-cloud-resource | resource_type | ExtendedProperties.resourceType |
| x-cloud-resource | resource_id | ResourceId |
| <br> | | |
| x-host-logon-session | session_id | Entities.SessionId |
| x-host-logon-session | start_time | Entities.StartTimeUtc |
| x-host-logon-session | end_time | Entities.EndTimeUtc |
| <br> | | |
| x-azure-blob | name | Entities.Name |
| x-azure-blob | etag | Entities.Etag |
| x-azure-blob | blob_container | Entities.Name |
| <br> | | |
| x-azure-malware | name | Entities.Name |
| x-azure-malware | category | Entities.Category |
| <br> | | |
| x-azure-container | container_id | Entities.ContainerId |
| x-azure-container | image_id | Entities.ImageId |
| x-azure-container | image_type | Entities.Type |
| <br> | | |
| x-k8s-cluster | name | Entities.Name |
| <br> | | |
| ipv4-addr | value | IpAddress |
| ipv4-addr | value | ClientIPAddress |
| <br> | | |
| ipv6-addr | value | IpAddress |
| ipv6-addr | value | ClientIPAddress |
| <br> | | |
| user-account | account_login | TargetAccount |
| user-account | account_login | SubjectAccount |
| user-account | user_id | TargetUserName |
| user-account | user_id | SubjectUserName |
| user-account | display_name | TargetUserName |
| user-account | display_name | SubjectUserName |
| user-account | x_domain_name | TargetDomainName |
| user-account | x_domain_name | SubjectDomainName |
| user-account | x_login_id | TargetLogonId |
| user-account | x_login_id | SubjectLogonId |
| user-account | x_user_sid | TargetUserSid |
| user-account | x_user_sid | SubjectUserSid |
| <br> | | |
| directory | path | HomeDirectory |
| directory | path | HomePath |
| directory | path | ProcessName |
| directory | path | ParentProcessName |
| directory | path | NewProcessName |
| <br> | | |
| file | name | FilePath |
| file | path | FilePath |
| file | hashes.'SHA-256' | FileHash |
| file | hashes.MD5 | FileHash |
| file | hashes.'SHA-1' | FileHash |
| file | parent_directory_ref | ProcessName |
| file | parent_directory_ref | ParentProcessName |
| file | x_fqbn | Fqbn |
| <br> | | |
| process | parent_ref.name | ParentProcessName |
| process | command_line | CommandLine |
| process | pid | ProcessId |
| process | pid | NewProcessId |
| process | x_token_elevation_type | TokenElevationType |
| process | x_mandatory_label | MandatoryLabel |
| <br> | | |
| url | value | QuarantineHelpURL |
| <br> | | |
| x-ibm-finding | alert_id | EventOriginId |
| x-ibm-finding | start | PreviousTime |
| x-ibm-finding | name | Activity |
| x-ibm-finding | finding_type | Type |
| x-ibm-finding | time_observed | TimeGenerated |
| x-ibm-finding | src_ip_ref | IpAddress |
| x-ibm-finding | dst_device | WorkstationName |
| x-ibm-finding | dst_device | TargetServerName |
| x-ibm-finding | src_application_user_ref | TargetUserName |
| x-ibm-finding | dst_application_user_ref | SubjectUserName |
| x-ibm-finding | ioc_refs | FilePath |
| x-ibm-finding | ioc_refs | IpAddress |
| x-ibm-finding | ioc_refs | ClientIPAddress |
| <br> | | |
| x-oca-event | agent | Account |
| x-oca-event | x_provider_type | AccountType |
| x-oca-event | module | Channel |
| x-oca-event | provider | EventSourceName |
| x-oca-event | action | Activity |
| x-oca-event | created | TimeCollected |
| x-oca-event | code | EventID |
| x-oca-event | dataset | EventData |
| x-oca-event | host_ref | Computer |
| x-oca-event | url_ref | QuarantineHelpURL |
| x-oca-event | process_ref | NewProcessName |
| x-oca-event | process_ref | Process |
| x-oca-event | process_ref | ProcessName |
| x-oca-event | file_ref.hash | FileHash |
| x-oca-event | file_ref.path | FilePath |
| x-oca-event | parent_process_ref | ParentProcessName |
| x-oca-event | user_ref | TargetUserName |
| x-oca-event | ip_refs.ip | IpAddress |
| x-oca-event | ip_refs.ip | ClientIPAddress |
| x-oca-event | x_service_file | ServiceFileName |
| x-oca-event | x_service_name | ServiceName |
| x-oca-event | x_modified_account_sid | TargetSid |
| x-oca-event | x_description | DeviceDescription |
| x-oca-event | x_task | Task |
| x-oca-event | x_user_parameter | UserParameters |
| x-oca-event | x_member_name | MemberName |
| x-oca-event | x_requester | Requester |
| <br> | | |
| x-cloud-resource | resource_id | _ResourceId |
| <br> | | |
| x-oca-asset | device_id | DeviceId |
| x-oca-asset | device_id | SourceComputerId |
| x-oca-asset | hostname | Computer |
| <br> | | |
| x-logon-info | guid | LogonGuid |
| x-logon-info | logon_process | LogonProcessName |
| x-logon-info | logon_type | LogonType |
| x-logon-info | logon_type_name | LogonTypeName |
| x-logon-info | authentication_package_name | AuthenticationPackageName |
| <br> | | |
| url | value | IncidentUrl |
| <br> | | |
| email-addr | value | Owner.email |
| email-addr | value | Owner.userPrincipalName |
| email-addr | display_name | Owner.assignedTo |
| <br> | | |
| x-ibm-finding | description | Description |
| x-ibm-finding | name | Title |
| x-ibm-finding | start | CreatedTime |
| x-ibm-finding | end | LastModifiedTime |
| x-ibm-finding | severity | Severity |
| x-ibm-finding | time_observed | TimeGenerated |
| x-ibm-finding | finding_type | Type |
| x-ibm-finding | rule_names | RelatedAnalyticRuleIds |
| x-ibm-finding | x_owner_ref | Owner.email |
| x-ibm-finding | x_owner_ref | Owner.userPrincipalName |
| x-ibm-finding | x_owner_ref | Owner.assignedTo |
| x-ibm-finding | x_incident_name | IncidentName |
| x-ibm-finding | x_provider_incident_id | ProviderIncidentId |
| x-ibm-finding | x_modified_by | ModifiedBy |
| x-ibm-finding | x_status | Status |
| x-ibm-finding | x_provider | ProviderName |
| x-ibm-finding | x_alert_count | AdditionalData.alertsCount |
| x-ibm-finding | x_alert_product_names | AdditionalData.alertProductNames |
| x-ibm-finding | x_alert_ids | AlertIds |
| x-ibm-finding | ttp_tagging_refs.name | Title |
| x-ibm-finding | ttp_tagging_refs.extensions.'mitre-attack-ext'.tactic_name | AdditionalData.tactics |
| x-ibm-finding | ttp_tagging_refs.extensions.'mitre-attack-ext'.technique_name | AdditionalData.techniques |
| x-ibm-finding | x_owner_ref.value | Owner.email |
| x-ibm-finding | x_owner_ref.value | Owner.userPrincipalName |
| x-ibm-finding | x_owner_ref.display_name | Owner.assignedTo |
| <br> | | |
| x-ibm-ttp-tagging | name | Title |
| x-ibm-ttp-tagging | extensions.'mitre-attack-ext'.tactic_name | AdditionalData.tactics |
| x-ibm-ttp-tagging | extensions.'mitre-attack-ext'.technique_name | AdditionalData.techniques |
| <br> | | |
| x-cloud-provider | tenant_id | TenantId |
| <br> | | |
| x-incident-info | classification | Classification |
| x-incident-info | classification_comment | ClassificationComment |
| x-incident-info | classification_reason | ClassificationReason |
| x-incident-info | closed_time | ClosedTime |
| x-incident-info | comments | Comments |
| x-incident-info | first_activity | FirstActivityTime |
| x-incident-info | first_modified | FirstModifiedTime |
| x-incident-info | labels | Labels |
| x-incident-info | last_active | LastActivityTime |
| x-incident-info | tasks | Tasks |
| x-incident-info | incident_url_ref.value | IncidentUrl |
| <br> | | |
