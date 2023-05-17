##### Updated on 05/15/23
## Azure Log Analytics
### Results STIX Domain Objects
* Identity
* Observed Data
<br>
### Supported STIX Operators
*Comparison AND/OR operators are inside the observation while observation AND/OR operators are between observations (square brackets).*

| STIX Operator | Data Source Operator |
|--|--|
| AND (Comparision) | and |
| OR (Comparision) | or |
| = | == |
| != | != |
| IN | in |
| MATCHES | contains |
| LIKE | startswith, endswith |
| <br> | |
### Searchable STIX objects and properties for Securityalert dialect
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **x-ibm-finding**:start | StartTime, TimeGenerated |
| **x-ibm-finding**:end | EndTime, ProcessingEndTime |
| **x-ibm-finding**:name | AlertName |
| **x-ibm-finding**:time_observed | TimeGenerated, EventTime |
| **x-oca-event**:created | TimeGenerated |
| **x-oca-event**:provider | ProviderName |
| **x-oca-event**:domain_ref | DomainName |
| **x-azure-security-alert**:tenant_id | TenantId |
| **x-azure-security-alert**:subscription_id | WorkspaceSubscriptionId |
| **x-azure-security-alert**:resourceId | _ResourceId |
| **x-azure-security-alert**:alert_severity | AlertSeverity |
| **x-azure-security-alert**:description | Description |
| **x-azure-security-alert**:product_name | ProductName |
| **x-azure-security-alert**:vendor_name | VendorName |
| **x-azure-security-alert**:system_alertid | SystemAlertId |
| **x-azure-security-alert**:status | Status |
| **x-azure-security-alert**:extented_properties | ExtentedProperties |
| **x-azure-security-alert**:confidence_level | ConfidenceLevel |
| **x-azure-security-alert**:entities | Entities |
| **x-azure-security-alert**:display_name | DisplayName |
| **x-azure-security-alert**:workspace_resource_group | WorkspaceResourceGroup |
| **x-azure-security-alert**:compromised_entity | CompromisedEntity |
| <br> | |
### Searchable STIX objects and properties for Securityevent dialect
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **ipv4-addr**:value | IpAddress |
| **domain-name**:value | TargetDomainName |
| **user-account**:account_login | TargetUserName |
| **directory**:path | HomeDirectory, HomePath |
| **file**:path | FilePath |
| **file**:hashes.'SHA-256' | FileHash |
| **file**:hashes.MD5 | FileHash |
| **file**:hashes.'SHA-1' | FileHash |
| **process**:name | ProcessName, LogonProcessName |
| **process**:parent_ref.name | ParentProcessName |
| **process**:command_line | CommandLine |
| **process**:pid | ProcessId |
| **url**:value | QuarantineHelpURL |
| **x-ibm-finding**:start | TimeGenerated |
| **x-ibm-finding**:end | PreviousTime |
| **x-ibm-finding**:name | EventSourceName |
| **x-ibm-finding**:time_observed | TimeGenerated |
| **x-ibm-finding**:src_ip_ref | IpAddress |
| **x-ibm-finding**:dst_ip_ref | ClientIPAddress |
| **x-oca-event**:created | TimeGenerated |
| **x-oca-event**:code | EventID |
| **x-oca-event**:provider | Account |
| **x-oca-event**:url_ref | QuarantineHelpURL |
| **x-oca-event**:process_ref | ProcessName |
| **x-oca-event**:file_ref.hash | FileHash |
| **x-oca-event**:file_ref.path | FilePath |
| **x-oca-event**:file_ref.service | ServiceFileName |
| **x-oca-event**:parent_process_ref | ParentProcessName |
| **x-oca-event**:ip_refs.ip | IpAddress |
| **x-oca-event**:ip_refs.clientIp | ClientIPAddress |
| **x-azure-security-event**:title | Title |
| **x-azure-security-event**:text | Description, DeviceDescription |
| **x-azure-security-event**:device_name | DeviceId |
| **x-azure-security-event**:source | SourceSystem |
| **x-azure-security-event**:alert_type | AlertName |
| **x-azure-security-event**:activity | Activity |
| **x-azure-security-event**:computer | Computer |
| **x-azure-security-event**:event_data | EventData |
| **x-azure-security-event**:service_name | ServiceName |
| **x-azure-security-event**:task | Task |
| **x-azure-security-event**:user_parameter | UserParameter |
| **x-azure-security-event**:member_name | MemberName |
| **x-azure-security-event**:requester | Requester |
| <br> | |
### Searchable STIX objects and properties for Securityincident dialect
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **url**:value | IncidentUrl |
| **x-ibm-finding**:start | FirstActivityTime, FirstModifiedTime, TimeGenerated |
| **x-ibm-finding**:end | ClosedTime, LastActivityTime, LastModifiedTime |
| **x-ibm-finding**:name | IncidentName |
| **x-ibm-finding**:time_observed | TimeGenerated |
| **x-oca-event**:created | CreatedTime |
| **x-oca-event**:provider | ProviderName |
| **x-oca-event**:url_ref | IncidentUrl |
| **x-oca-event**:domain_ref | DomainName |
| **x-azure-security-incident**:incident_name | IncidentName |
| **x-azure-security-incident**:severity | Severity |
| **x-azure-security-incident**:owner | Owner |
| **x-azure-security-incident**:additional_data | AdditionalData |
| **x-azure-security-incident**:alertids | AlertIds |
| **x-azure-security-incident**:comments | Comments |
| **x-azure-security-incident**:description | Description |
| **x-azure-security-incident**:labels | Labels |
| **x-azure-security-incident**:modified_by | ModifiedBy |
| **x-azure-security-incident**:classification | Classification |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| directory | path | HomeDirectory |
| directory | path | HomePath |
| <br> | | |
| domain-name | value | TargetDomainName |
| <br> | | |
| file | path | FilePath |
| file | hashes | FileHash |
| <br> | | |
| ipv4-addr | value | IpAddress |
| <br> | | |
| process | name | ProcessName |
| process | command_line | CommandLine |
| process | pid | ProcessId |
| process | parent_ref | ParentProcessName |
| process | name | LogonProcessName |
| <br> | | |
| url | name | QuarantineHelpURL |
| url | name | IncidentUrl |
| <br> | | |
| user-account | account_login | TargetUserName |
| <br> | | |
| x-azure-security-alert | tenant_id | TenantId |
| x-azure-security-alert | subscription_id | WorkspaceSubscriptionId |
| x-azure-security-alert | resourceId | _ResourceId |
| x-azure-security-alert | alert_severity | AlertSeverity |
| x-azure-security-alert | description | Description |
| x-azure-security-alert | product_name | ProductName |
| x-azure-security-alert | vendor_name | VendorName |
| x-azure-security-alert | cloudAppStates.system_alertid | SystemAlertId |
| x-azure-security-alert | status | Status |
| x-azure-security-alert | extented_properties | ExtentedProperties |
| x-azure-security-alert | confidence_level | ConfidenceLevel |
| x-azure-security-alert | entities | Entities |
| x-azure-security-alert | display_name | DisplayName |
| x-azure-security-alert | workspace_resource_group | WorkspaceResourceGroup |
| x-azure-security-alert | compromised_entity | CompromisedEntity |
| <br> | | |
| x-azure-security-event | alert_type | AlertName |
| x-azure-security-event | description | Description |
| x-azure-security-event | event_id | eventId |
| x-azure-security-event | title | Title |
| x-azure-security-event | text | DeviceDescription |
| x-azure-security-event | source | SourceSystem |
| x-azure-security-event | activity | Activity |
| x-azure-security-event | computer | Computer |
| x-azure-security-event | event_data | EventData |
| x-azure-security-event | service_name | ServiceName |
| x-azure-security-event | task | Task |
| x-azure-security-event | user_parameter | UserParameter |
| x-azure-security-event | member_name | MemberName |
| x-azure-security-event | requester | Requester |
| <br> | | |
| x-azure-security-incident | incident_name | IncidentName |
| x-azure-security-incident | severity | Severity |
| x-azure-security-incident | owner | Owner |
| x-azure-security-incident | additional_data | AdditionalData |
| x-azure-security-incident | alertids | AlertIds |
| x-azure-security-incident | comments | Comments |
| x-azure-security-incident | description | Description__incident |
| x-azure-security-incident | labels | Labels |
| x-azure-security-incident | modified_by | ModifiedBy |
| <br> | | |
| x-ibm-finding | name | EventSourceName |
| x-ibm-finding | name | AlertName |
| x-ibm-finding | name | IncidentName |
| x-ibm-finding | start | TimeGenerated |
| x-ibm-finding | time_observed | TimeGenerated |
| x-ibm-finding | time_observed | EventTime |
| x-ibm-finding | start | PreviousTime |
| x-ibm-finding | src_ip_ref | IpAddress |
| x-ibm-finding | dst_ip_ref | ClientIPAddress |
| x-ibm-finding | start | StartTime |
| x-ibm-finding | end | EndTime |
| x-ibm-finding | end | ProcessingEndTime |
| x-ibm-finding | start | FirstActivityTime |
| x-ibm-finding | start | FirstModifiedTime |
| x-ibm-finding | end | ClosedTime |
| x-ibm-finding | end | LastActivityTime |
| x-ibm-finding | end | LastModifiedTime |
| <br> | | |
| x-oca-asset | device_id | DeviceId |
| <br> | | |
| x-oca-event | created | TimeGenerated |
| x-oca-event | provider | ProviderName |
| x-oca-event | code | EventID |
| x-oca-event | ip_refs | IpAddress |
| x-oca-event | ip_refs.clientIp | ClientIPAddress |
| x-oca-event | created | CreatedTime |
| x-oca-event | provider | Account |
| x-oca-event | url_ref | QuarantineHelpURL |
| x-oca-event | url_ref | IncidentUrl |
| x-oca-event | process_ref | ProcessName |
| x-oca-event | parent_process_ref | ParentProcessName |
| x-oca-event | file_ref.path | FilePath |
| x-oca-event | file_ref.path | FileHash |
| x-oca-event | file_ref.service | ServiceFileName |
| <br> | | |
