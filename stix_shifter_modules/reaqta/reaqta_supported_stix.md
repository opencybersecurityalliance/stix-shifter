##### Updated on 05/15/23
## IBM Security ReaQta
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
| >= | = |
| <= | = |
| = | = |
| != | != |
| LIKE | = |
| IN | = |
| MATCHES | = |
| OR (Observation) | OR |
| AND (Observation) | AND |
| <br> | |
### Searchable STIX objects and properties
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **directory**:path | __etwHomePath, accessor.path, consumer.workingDirectory, path |
| **file**:extensions.'x-reaqta-data'.arch | eventdata.arch |
| **file**:extensions.'x-reaqta-data'.file_type | eventdata.filetype |
| **file**:extensions.'x-reaqta-data'.fsname | fsName |
| **file**:extensions.'x-reaqta-program'.arch | service.arch |
| **file**:extensions.'x-reaqta-program'.fsname | fsName |
| **file**:hashes.MD5 | md5 |
| **file**:hashes.'SHA-1' | sha1 |
| **file**:hashes.'SHA-256' | sha256 |
| **file**:name | consumer.script.filename, fsName |
| **file**:parent_directory_ref.path | path |
| **file**:size | eventdata.size |
| **ipv4-addr**:value | ip, login.ip |
| **ipv6-addr**:value | ip |
| **network-traffic**:dst_port | eventdata.remotePort |
| **network-traffic**:dst_ref.value | ip |
| **network-traffic**:extensions.'x-reaqta-network'.outbound | isOutbound |
| **network-traffic**:src_port | eventdata.localPort |
| **network-traffic**:src_ref.value | ip |
| **process**:binary_ref.name | fsName |
| **process**:creator_user_ref.user_id |  |
| **process**:extensions.'windows-process-ext'.owner_sid | user.sid |
| **process**:extensions.'x-reaqta-process'.logon_id | service.login.id |
| **process**:extensions.'x-reaqta-process'.no_gui | service.hasGui |
| **process**:extensions.'x-reaqta-process'.privilege_level | service.privilege |
| **process**:name | __etwCallerProcessName, __etwLogonProcessName, __etwProcessName, login.processName, filename |
| **process**:parent_ref.binary_ref.name | service.ppid |
| **process**:pid | __etwCallerProcessId, __etwProcessId, accessor.pid, accessor.ppid, allocator.pid, allocator.ppid, engine.pid, engine.ppid, eventdata.targetProcessId, host.pid, pid, ppid, service.pid, service.ppid, wmi.clientPid, wmiHost.pid |
| **url**:value | eventdata.url |
| **user-account**:user_id | __etwNewTargetUserName, __etwOldTargetUserName, __etwTargetOutboundUserName, accessor.user, allocator.user, engine.user, login.dst.username, login.src.username, service.user, user, wmi.user |
| **windows-process-ext**:owner_sid | accessor.user.sid, allocator.user.sid, engine.user.sid, login.src.sid, service.user.sid, user.sid |
| **x-ibm-finding**:dst_ip_ref.value | ip |
| **x-ibm-finding**:extensions.'x-reaqta-avdetection'.av_scan_reason | antimalware.scanReason |
| **x-ibm-finding**:extensions.'x-reaqta-avdetection'.av_threat_info_array | antimalware.threatInfo |
| **x-ibm-finding**:finding_type | antimalware.threatType |
| **x-ibm-finding**:name | antimalware.objectStatus |
| **x-ibm-finding**:src_ip_ref.value | ip |
| **x-oca-asset**:extensions.'x-reaqta-consumer'.command_line_template_tokens | consumer.cmdline |
| **x-oca-asset**:extensions.'x-reaqta-consumer'.consumer_name | wmi.consumerName |
| **x-oca-asset**:extensions.'x-reaqta-consumer'.consumer_type | wmi.consumerType |
| **x-oca-asset**:extensions.'x-reaqta-consumer'.event_namespace | wmi.eventNamespace |
| **x-oca-asset**:extensions.'x-reaqta-consumer'.executablePath | consumer.execPath |
| **x-oca-asset**:extensions.'x-reaqta-consumer'.runInteractively | consumer.runInteractively |
| **x-oca-asset**:extensions.'x-reaqta-consumer'.scriptingEngine | consumer.script.engine |
| **x-oca-asset**:extensions.'x-reaqta-consumer'.showWindowCommand | consumer.showWindowCmd |
| **x-oca-asset**:extensions.'x-wmi-event'.client_machine_fqn | wmi.clientMachineFqn |
| **x-oca-asset**:host_id | __etwWorkstation, endpointId |
| **x-oca-asset**:hostname | __etwWorkstationName, wmi.clientMachine, wmi.machineName |
| **x-oca-asset**:ip_refs[*].value | ip |
| **x-oca-event**:agent | antimalware.appName |
| **x-oca-event**:category | eventType |
| **x-oca-event**:code | eventId, eventdata.etwEventId |
| **x-oca-event**:extensions.'x-reaqta-amsi'.content_name | antimalware.contentName |
| **x-oca-event**:extensions.'x-reaqta-amsi'.scan_result | antimalware.scanResult |
| **x-oca-event**:extensions.'x-reaqta-etw'.etw_event_record_id | eventdata.etwEventVersion |
| **x-oca-event**:extensions.'x-reaqta-etw'.etw_failure_reason | __etwFailureReason |
| **x-oca-event**:extensions.'x-reaqta-etw'.etw_home_directory | __etwHomeDirectory |
| **x-oca-event**:file_ref.name | path |
| **x-oca-event**:host_ref.x-oca-asset.hostname | wmi.clientMachine |
| **x-oca-event**:ip_refs[*].value | login.ip |
| **x-oca-event**:network_ref.dst_ref.value | ip |
| **x-oca-event**:network_ref.src_ref.value | ip |
| **x-oca-event**:parent_process_ref.pid | service.ppid |
| **x-oca-event**:process_ref.pid | wmi.clientPid |
| **x-oca-event**:user_ref.user_id |  |
| **x-reaqta-amsi**:content_name | antimalware.contentName |
| **x-reaqta-amsi**:scan_result | antimalware.scanResult |
| **x-reaqta-avdetection**:av_scan_reason | antimalware.scanReason |
| **x-reaqta-avdetection**:av_threat_info_array | antimalware.threatInfo |
| **x-reaqta-cert**:expired | accessor.expired, allocator.expired, engine.expired, eventdata.cert.expired, expired, service.expired |
| **x-reaqta-cert**:signer | accessor.signer, allocator.signer, engine.signer, eventdata.cert.signer, service.signer, signer |
| **x-reaqta-cert**:trusted | accessor.trusted, allocator.trusted, engine.trusted, eventdata.cert.trusted, service.trusted, trusted |
| **x-reaqta-consumer**:command_line_template_tokens | consumer.cmdline |
| **x-reaqta-consumer**:consumer_name | wmi.consumerName |
| **x-reaqta-consumer**:consumer_type | wmi.consumerType |
| **x-reaqta-consumer**:event_namespace | wmi.eventNamespace |
| **x-reaqta-consumer**:executablePath | consumer.execPath |
| **x-reaqta-consumer**:runInteractively | consumer.runInteractively |
| **x-reaqta-consumer**:scriptingEngine | consumer.script.engine |
| **x-reaqta-consumer**:showWindowCommand | consumer.showWindowCmd |
| **x-reaqta-data**:arch | eventdata.arch |
| **x-reaqta-data**:file_type | eventdata.filetype |
| **x-reaqta-data**:fsname | filename |
| **x-reaqta-etw**:etwRestrictedAdminMode | __etwRestrictedAdminMode |
| **x-reaqta-etw**:etwSamAccountName | __etwSamAccountName |
| **x-reaqta-etw**:etwScriptPath | __etwScriptPath |
| **x-reaqta-etw**:etwServiceName | __etwServiceName |
| **x-reaqta-etw**:etwServiceSid | __etwServiceSid |
| **x-reaqta-etw**:etwSidHistory | __etwSidHistory |
| **x-reaqta-etw**:etwSidList | __etwSidList |
| **x-reaqta-etw**:etwStatus | __etwStatus |
| **x-reaqta-etw**:etwSubStatus | __etwSubStatus, login.src.domain |
| **x-reaqta-etw**:etwSubjectLogonId | login.subjectLogonId |
| **x-reaqta-etw**:etwTargetDomainName | login.dst.domain |
| **x-reaqta-etw**:etwTargetInfo | __etwTargetInfo |
| **x-reaqta-etw**:etwTargetLinkedLogonId | __etwTargetLinkedLogonId |
| **x-reaqta-etw**:etwTargetLogonGuid | __etwTargetLogonGuid |
| **x-reaqta-etw**:etwTargetLogonId | login.targetLogonId |
| **x-reaqta-etw**:etwTargetOutboundDomainName | __etwTargetOutboundDomainName, __etwTargetServerName |
| **x-reaqta-etw**:etwTargetSid | __etwTargetSid |
| **x-reaqta-etw**:etwTargetUserSid | login.dst.sid |
| **x-reaqta-etw**:etwTask | eventdata.etwTask |
| **x-reaqta-etw**:etwTicketEncryptionType | __etwTicketEncryptionType |
| **x-reaqta-etw**:etwTicketOptions | __etwTicketOptions |
| **x-reaqta-etw**:etwTransmittedServices | __etwTransmittedServices |
| **x-reaqta-etw**:etwUserAccountControl | __etwUserAccountControl |
| **x-reaqta-etw**:etwUserParameters | __etwUserParameters |
| **x-reaqta-etw**:etwUserPrincipalName | __etwUserPrincipalName |
| **x-reaqta-etw**:etwUserWorkstations | __etwUserWorkstations |
| **x-reaqta-etw**:etwVirtualAccount | __etwVirtualAccount |
| **x-reaqta-etw**:etw_allowed_to_delegateto | __etwAllowedToDelegateTo |
| **x-reaqta-etw**:etw_authentication_packagename | login.authenticationPackage |
| **x-reaqta-etw**:etw_cert_thumbprint | __etwCertThumbprint |
| **x-reaqta-etw**:etw_display_name | __etwDisplayName |
| **x-reaqta-etw**:etw_dummy | __etwDummy |
| **x-reaqta-etw**:etw_elevated_token | __etwElevatedToken |
| **x-reaqta-etw**:etw_event_record_id | __etwEventRecordId, eventdata.etwEventVersion |
| **x-reaqta-etw**:etw_failure_reason | __etwFailureReason |
| **x-reaqta-etw**:etw_home_directory | __etwHomeDirectory |
| **x-reaqta-etw**:etw_impersonation_level | __etwImpersonationLevel |
| **x-reaqta-etw**:etw_ip_port | login.port |
| **x-reaqta-etw**:etw_key_length | __etwKeyLength |
| **x-reaqta-etw**:etw_lm_package_name | login.packageName |
| **x-reaqta-etw**:etw_logon_guid | __etwLogonGuid |
| **x-reaqta-etw**:etw_logon_hours | __etwLogonHours |
| **x-reaqta-etw**:etw_logon_type | login.type |
| **x-reaqta-etw**:etw_member_name | __etwMemberName |
| **x-reaqta-etw**:etw_member_sid | __etwMemberSid |
| **x-reaqta-etw**:etw_new_uac_value | __etwNewUacValue |
| **x-reaqta-etw**:etw_old_uac_value | __etwOldUacValue |
| **x-reaqta-etw**:etw_package_name | __etwPackageName |
| **x-reaqta-etw**:etw_password_last_set | __etwPasswordLastSet |
| **x-reaqta-etw**:etw_pre_auth_type | __etwPreAuthType |
| **x-reaqta-etw**:etw_primary_groupId | __etwPrimaryGroupId |
| **x-reaqta-etw**:etw_privilege_list | __etwPrivilegeList |
| **x-reaqta-etw**:etw_profile_path | __etwProfilePath |
| **x-reaqta-event**:action_name | task.actionName |
| **x-reaqta-event**:custom_name | customName |
| **x-reaqta-event**:custom_type | customType |
| **x-reaqta-event**:data | reg.data |
| **x-reaqta-event**:display_name | service.displayName |
| **x-reaqta-event**:filter_name | wmi.filterName |
| **x-reaqta-event**:is_local | wmi.isLocal |
| **x-reaqta-event**:name | reg.name |
| **x-reaqta-event**:namespace_name | wmi.namespaceName |
| **x-reaqta-event**:operation | wmi.operation |
| **x-reaqta-event**:operation_type | wmi.operationType |
| **x-reaqta-event**:pe_type | eventdata.peType |
| **x-reaqta-event**:query | wmi.query |
| **x-reaqta-event**:queryLanguage | wmi.queryLanguage |
| **x-reaqta-event**:queryName | eventdata.dns |
| **x-reaqta-event**:region_size | eventdata.regionSize |
| **x-reaqta-event**:relevance | eventdata.relevance |
| **x-reaqta-event**:return_code | eventdata.returnCode |
| **x-reaqta-event**:root_object | path |
| **x-reaqta-event**:service_name | service.name |
| **x-reaqta-event**:service_type | service.type |
| **x-reaqta-event**:start_type | service.startType |
| **x-reaqta-event**:tactics | mitre.tactic |
| **x-reaqta-event**:tags | eventdata.tag |
| **x-reaqta-event**:task_name | task.name |
| **x-reaqta-event**:technique | mitre.technique |
| **x-reaqta-event**:version | eventdata.version |
| **x-reaqta-network**:outbound | isOutbound |
| **x-reaqta-process**:logon_id | accessor.login.id, allocator.login.id, engine.login.id, login.id, service.login.id |
| **x-reaqta-process**:no_gui | accessor.hasGui, allocator.hasGui, engine.hasGui, hasGui, service.hasGui |
| **x-reaqta-process**:privilege_level | accessor.privilege, allocator.privilege, engine.privilege, privilege, service.privilege |
| **x-reaqta-program**:arch | accessor.arch, allocator.arch, arch, engine.arch, service.arch |
| **x-reaqta-program**:fsname | filename |
| **x-wmi-event**:client_machine_fqn | wmi.clientMachineFqn |
| **x509-certificate**:extensions.'x-reaqta-cert'.expired | service.expired |
| **x509-certificate**:extensions.'x-reaqta-cert'.signer | signer |
| **x509-certificate**:extensions.'x-reaqta-cert'.trusted | trusted |
| **x509-certificate**:extensions.'x-reaqta-etw'.etw_cert_thumbprint | __etwCertThumbprint |
| **x509-certificate**:issuer | __etwCertIssuerName, accessor.issuer, allocator.issuer, engine.issuer, eventdata.cert.issuer, issuer, service.issuer |
| **x509-certificate**:serial_number | __etwCertSerialNumber |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| directory | path | path |
| directory | path | workingDirectory |
| directory | path | etwHomePath |
| <br> | | |
| file | extensions.x-reaqta-program.arch | arch |
| file | name | fsName |
| file | hashes.MD5 | md5 |
| file | parent_directory_ref | path |
| file | hashes.SHA-1 | sha1 |
| file | hashes.SHA-256 | sha256 |
| file | size | size |
| file | extensions.x-reaqta-program.filename | filename |
| file | extensions.x-reaqta-data.arch | arch |
| file | name | scriptFileName |
| file | parent_directory_ref | workingDirectory |
| file | parent_directory_ref | etwHomePath |
| file | name | file |
| file | extensions.x-reaqta-data.file_type | fileType |
| file | extensions.x-reaqta-data.fsname | fsName |
| file | created | creationTime |
| <br> | | |
| ipv4-addr | value | etwIpAddress |
| ipv4-addr | value | localAddrV4 |
| ipv4-addr | value | remoteAddrV4 |
| <br> | | |
| ipv6-addr | value | localAddrV6 |
| ipv6-addr | value | remoteAddrV6 |
| <br> | | |
| network-traffic | extensions.x-reaqta-network.address_family | addressFamily |
| network-traffic | src_ref | localAddrV4 |
| network-traffic | src_ref | localAddrV6 |
| network-traffic | src_port | localPort |
| network-traffic | extensions.x-reaqta-network.outbound | outbound |
| network-traffic | protocols | protocol |
| network-traffic | dst_ref | remoteAddrV4 |
| network-traffic | dst_ref | remoteAddrV6 |
| network-traffic | dst_port | remotePort |
| <br> | | |
| process | x_unique_id | id |
| process | extensions.x-reaqta-process.logon_id | logonId |
| process | extensions.x-reaqta-process.no_gui | noGui |
| process | x_unique_id | parentId |
| process | pid | pid |
| process | pid | ppid |
| process | parent_ref | ppid |
| process | extensions.x-reaqta-process.privilege_level | privilegeLevel |
| process | binary_ref | fsName |
| process | name | filename |
| process | created | pstartTime |
| process | created | startTime |
| process | creator_user_ref | user |
| process | extensions.windows-process-ext.owner_sid | userSID |
| process | pid | clientPid |
| process | command_line | cmdLine |
| process | extensions.x-reaqta-process.command_line_args | cmdLineArgs |
| process | pid | etwCallerProcessId |
| process | name | etwCallerProcessName |
| process | name | etwLogonProcessName |
| process | pid | etwProcessId |
| process | name | etwProcessName |
| process | creator_user_ref | etwSubjectUserName |
| process | extensions.windows-process-ext.owner_sid | etwSubjectUserSid |
| process | pid | hostPid |
| process | pid | targetProcessId |
| process | pid | wmiHostPid |
| <br> | | |
| url | value | url |
| <br> | | |
| user-account | user_id | user |
| user-account | user_id | etwNewTargetUserName |
| user-account | user_id | etwOldTargetUserName |
| user-account | user_id | etwSubjectUserName |
| user-account | user_id | etwTargetOutboundUserName |
| user-account | user_id | etwTargetUserName |
| <br> | | |
| x-ibm-finding | extensions.x-reaqta-alert.incidents | incidents |
| x-ibm-finding | extensions.x-reaqta-alert.triggered_incidents | triggeredIncidents |
| x-ibm-finding | name | avObjectStatus |
| x-ibm-finding | extensions.x-reaqta-avdetection.av_scan_reason | avScanReason |
| x-ibm-finding | extensions.x-reaqta-avdetection.av_threat_info_array | avThreatInfoArray |
| x-ibm-finding | finding_type | avThreatType |
| x-ibm-finding | src_ip_ref | localAddrV4 |
| x-ibm-finding | src_ip_ref | localAddrV6 |
| x-ibm-finding | dst_ip_ref | remoteAddrV4 |
| x-ibm-finding | dst_ip_ref | remoteAddrV6 |
| <br> | | |
| x-oca-asset | host_id | endpointId |
| x-oca-asset | hostname | clientMachine |
| x-oca-asset | extensions.x-wmi-event.client_machine_fqn | clientMachineFqn |
| x-oca-asset | extensions.x-reaqta-consumer.command_line_template_tokens | commandLineTemplateTokens |
| x-oca-asset | extensions.x-reaqta-consumer.executablePath | executablePath |
| x-oca-asset | extensions.x-reaqta-consumer.runInteractively | runInteractively |
| x-oca-asset | extensions.x-reaqta-consumer.scriptingEngine | scriptingEngine |
| x-oca-asset | extensions.x-reaqta-consumer.showWindowCommand | showWindowCommand |
| x-oca-asset | extensions.x-reaqta-consumer.consumer_name | consumerName |
| x-oca-asset | extensions.x-reaqta-consumer.consumer_type | consumerType |
| x-oca-asset | ip_refs | etwIpAddress |
| x-oca-asset | host_id | etwWorkstation |
| x-oca-asset | hostname | etwWorkstationName |
| x-oca-asset | extensions.x-reaqta-consumer.event_namespace | eventNamespace |
| x-oca-asset | ip_refs | localAddrV4 |
| x-oca-asset | ip_refs | localAddrV6 |
| x-oca-asset | hostname | machineName |
| <br> | | |
| x-oca-event | code | eventId |
| x-oca-event | created | receivedAt |
| x-oca-event | action | eventName |
| x-oca-event | category | eventType |
| x-oca-event | process_ref | pid |
| x-oca-event | parent_process_ref | ppid |
| x-oca-event | file_ref | fsName |
| x-oca-event | file_ref | path |
| x-oca-event | user_ref | user |
| x-oca-event | agent | appName |
| x-oca-event | host_ref | clientMachine |
| x-oca-event | process_ref | clientPid |
| x-oca-event | extensions.x-reaqta-amsi.content_name | contentName |
| x-oca-event | start | startTime |
| x-oca-event | process_ref | etwCallerProcessId |
| x-oca-event | code | etwEventId |
| x-oca-event | extensions.x-reaqta-etw.etw_event_record_id | etwEventRecordId |
| x-oca-event | extensions.x-reaqta-etw.etw_event_version | etwEventVersion |
| x-oca-event | extensions.x-reaqta-etw.etw_failure_reason | etwFailureReason |
| x-oca-event | extensions.x-reaqta-etw.etw_home_directory | etwHomeDirectory |
| x-oca-event | file_ref | etwHomePath |
| x-oca-event | ip_refs | etwIpAddress |
| x-oca-event | process_ref | etwProcessId |
| x-oca-event | user_ref | etwSubjectUserName |
| x-oca-event | file_ref | file |
| x-oca-event | process_ref | hostPid |
| x-oca-event | network_ref | localAddrV4 |
| x-oca-event | network_ref | localAddrV6 |
| x-oca-event | network_ref | remoteAddrV4 |
| x-oca-event | network_ref | remoteAddrV6 |
| x-oca-event | extensions.x-reaqta-amsi.scan_result | scanResult |
| x-oca-event | process_ref | targetProcessId |
| <br> | | |
| x-reaqta-etw | etw_allowed_to_delegateto | etwAllowedToDelegateTo |
| x-reaqta-etw | etw_authentication_packagename | etwAuthenticationPackageName |
| x-reaqta-etw | etw_display_name | etwDisplayName |
| x-reaqta-etw | etw_dummy | etwDummy |
| x-reaqta-etw | etw_elevated_token | etwElevatedToken |
| x-reaqta-etw | etw_impersonation_level | etwImpersonationLevel |
| x-reaqta-etw | etw_ip_port | etwIpPort |
| x-reaqta-etw | etw_key_length | etwKeyLength |
| x-reaqta-etw | etw_lm_package_name | etwLmPackageName |
| x-reaqta-etw | etw_logon_guid | etwLogonGuid |
| x-reaqta-etw | etw_logon_hours | etwLogonHours |
| x-reaqta-etw | etw_logon_type | etwLogonType |
| x-reaqta-etw | etw_member_name | etwMemberName |
| x-reaqta-etw | etw_member_sid | etwMemberSid |
| x-reaqta-etw | etw_new_uac_value | etwNewUacValue |
| x-reaqta-etw | etw_old_uac_value | etwOldUacValue |
| x-reaqta-etw | etw_package_name | etwPackageName |
| x-reaqta-etw | etw_password_last_set | etwPasswordLastSet |
| x-reaqta-etw | etw_pre_auth_type | etwPreAuthType |
| x-reaqta-etw | etw_primary_groupId | etwPrimaryGroupId |
| x-reaqta-etw | etw_privilege_list | etwPrivilegeList |
| x-reaqta-etw | etw_profile_path | etwProfilePath |
| x-reaqta-etw | etwRestrictedAdminMode | etwRestrictedAdminMode |
| x-reaqta-etw | etwSamAccountName | etwSamAccountName |
| x-reaqta-etw | etwScriptPath | etwScriptPath |
| x-reaqta-etw | etwServiceName | etwServiceName |
| x-reaqta-etw | etwServiceSid | etwServiceSid |
| x-reaqta-etw | etwSidHistory | etwSidHistory |
| x-reaqta-etw | etwSidList | etwSidList |
| x-reaqta-etw | etwStatus | etwStatus |
| x-reaqta-etw | etwSubStatus | etwSubStatus |
| x-reaqta-etw | etwSubStatus | etwSubjectDomainName |
| x-reaqta-etw | etwSubjectLogonId | etwSubjectLogonId |
| x-reaqta-etw | etwTargetDomainName | etwTargetDomainName |
| x-reaqta-etw | etwTargetInfo | etwTargetInfo |
| x-reaqta-etw | etwTargetLinkedLogonId | etwTargetLinkedLogonId |
| x-reaqta-etw | etwTargetLogonGuid | etwTargetLogonGuid |
| x-reaqta-etw | etwTargetLogonId | etwTargetLogonId |
| x-reaqta-etw | etwTargetOutboundDomainName | etwTargetOutboundDomainName |
| x-reaqta-etw | etwTargetOutboundDomainName | etwTargetServerName |
| x-reaqta-etw | etwTargetSid | etwTargetSid |
| x-reaqta-etw | etwTargetUserSid | etwTargetUserSid |
| x-reaqta-etw | etwTask | etwTask |
| x-reaqta-etw | etwTicketEncryptionType | etwTicketEncryptionType |
| x-reaqta-etw | etwTicketOptions | etwTicketOptions |
| x-reaqta-etw | etwTransmittedServices | etwTransmittedServices |
| x-reaqta-etw | etwUserAccountControl | etwUserAccountControl |
| x-reaqta-etw | etwUserParameters | etwUserParameters |
| x-reaqta-etw | etwUserPrincipalName | etwUserPrincipalName |
| x-reaqta-etw | etwUserWorkstations | etwUserWorkstations |
| x-reaqta-etw | etwVirtualAccount | etwVirtualAccount |
| <br> | | |
| x-reaqta-event | local_id | localId |
| x-reaqta-event | action_name | actionName |
| x-reaqta-event | custom_name | customName |
| x-reaqta-event | custom_type | customType |
| x-reaqta-event | data | data |
| x-reaqta-event | display_name | displayName |
| x-reaqta-event | filter_name | filterName |
| x-reaqta-event | is_local | isLocal |
| x-reaqta-event | name | name |
| x-reaqta-event | namespace_name | namespaceName |
| x-reaqta-event | operation | operation |
| x-reaqta-event | operation_type | operationType |
| x-reaqta-event | pe_type | peType |
| x-reaqta-event | query | query |
| x-reaqta-event | queryLanguage | queryLanguage |
| x-reaqta-event | queryName | queryName |
| x-reaqta-event | region_size | regionSize |
| x-reaqta-event | relevance | relevance |
| x-reaqta-event | return_code | returnCode |
| x-reaqta-event | root_object | rootObject |
| x-reaqta-event | service_name | serviceName |
| x-reaqta-event | service_type | serviceType |
| x-reaqta-event | start_type | startType |
| x-reaqta-event | tactics | tactics |
| x-reaqta-event | tags | tags |
| x-reaqta-event | task_name | taskName |
| x-reaqta-event | technique | technique |
| x-reaqta-event | version | version |
| <br> | | |
| x509-certificate | extensions.x-reaqta-cert.expired | expired |
| x509-certificate | issuer | issuer |
| x509-certificate | extensions.x-reaqta-cert.signer | signer |
| x509-certificate | extensions.x-reaqta-cert.trusted | trusted |
| x509-certificate | issuer | etwCertIssuerName |
| x509-certificate | serial_number | etwCertSerialNumber |
| x509-certificate | extensions.x-reaqta-etw.etw_cert_thumbprint | etwCertThumbprint |
| <br> | | |
