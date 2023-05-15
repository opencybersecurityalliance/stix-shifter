##### Updated on 05/15/23
## SentinelOne
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
| != | != |
| LIKE | in contains anycase |
| MATCHES | regexp |
| > | > |
| >= | >= |
| < | < |
| <= | <= |
| IN | IN |
| OR (Observation) | OR |
| AND (Observation) | OR |
| <br> | |
### Searchable STIX objects and properties
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **ipv4-addr**:value | srcIp, dstIp, srcMachineIP |
| **ipv6-addr**:value | srcIp, dstIp, srcMachineIP |
| **network-traffic**:src_port | srcPort |
| **network-traffic**:dst_port | dstPort |
| **network-traffic**:protocols[*] | netProtocolName |
| **network-traffic**:src_ref.value | srcIp |
| **network-traffic**:dst_ref.value | dstIp |
| **network-traffic**:extensions.'x-sentinelone-network-action'.connection_status | netConnStatus |
| **network-traffic**:extensions.'x-sentinelone-network-action'.event_direction | netEventDirection |
| **domain-name**:value | dnsRequest, dnsResponse, loginAccountDomain |
| **url**:value | url |
| **process**:command_line | srcProcCmdLine, tgtProcCmdLine |
| **process**:created | srcProcStartTime, tgtProcStartTime, srcProcParentStartTime |
| **process**:pid | srcProcPid, tgtProcPid, srcProcParentPid |
| **process**:name | srcProcName, srcProcParentName, tgtProcName |
| **process**:parent_ref.name | srcProcParentName |
| **process**:creator_user_ref.user_id | srcProcUser, tgtProcUser |
| **process**:parent_ref.pid | srcProcParentPid |
| **process**:extensions.'x-sentinelone-process'.integrity_level | srcProcIntegrityLevel, tgtProcIntegrityLevel |
| **process**:extensions.'x-sentinelone-process'.publisher | srcProcPublisher, tgtProcPublisher |
| **process**:extensions.'x-sentinelone-process'.story_line_id | srcProcStorylineId, tgtProcStorylineId |
| **process**:x_unique_id | srcProcUid, tgtProcUid, srcProcParentUid |
| **process**:extensions.'x-sentinelone-process'.signed_status | srcProcSignedStatus, tgtProcSignedStatus |
| **process**:extensions.'x-sentinelone-process'.verified_status | srcProcVerifiedStatus, tgtProcVerifiedStatus |
| **process**:extensions.'x-sentinelone-process'.signature_invalid_reason | srcProcReasonSignatureInvalid, tgtProcReasonSignatureInvalid |
| **process**:extensions.'x-sentinelone-process'.sub_system | srcProcSubsystem, tgtProcSubsystem |
| **process**:extensions.'x-sentinelone-process'.session_id | srcProcSessionId, tgtProcSessionId |
| **process**:extensions.'x-sentinelone-process'.active_content_type | srcProcActiveContentType, tgtProcActiveContentType |
| **process**:extensions.'x-sentinelone-process'.active_content_fileid | srcProcActiveContentFileId, tgtProcActiveContentFileId |
| **process**:extensions.'x-sentinelone-process'.active_content_path | srcProcActiveContentPath, tgtProcActiveContentPath |
| **process**:extensions.'x-sentinelone-process'.active_content_hash | srcProcActiveContentHash, tgtProcActiveContentHash |
| **process**:extensions.'x-sentinelone-process'.active_content_signed_status | srcProcActiveContentSignedStatus, tgtProcActiveContentSignedStatus |
| **file**:name | fileFullName |
| **file**:size | tgtFileSize |
| **file**:hashes.MD5 | tgtFileMd5, tgtFileOldMd5, srcProcImageMd5, tgtProcImageMd5 |
| **file**:hashes.'SHA-1' | tgtFileSha1, tgtFileOldSha1, srcProcImageSha1, tgtProcImageSha1 |
| **file**:hashes.'SHA-256' | tgtFileSha256, tgtFileOldSha256, srcProcImageSha256, tgtProcImageSha256 |
| **file**:parent_directory_ref.path | tgtFilePath, tgtFileOldPath, srcProcImagePath, tgtProcImagePath, srcProcParentImagePath |
| **file**:created | tgtFileCreatedAt |
| **file**:modified | tgtFileModifiedAt |
| **file**:extensions.'x-sentinelone-file'.file_type | tgtFileType |
| **file**:extensions.'x-sentinelone-file'.file_extension | tgtFileExtension |
| **file**:extensions.'x-sentinelone-file'.file_description | tgtFileDescription |
| **file**:extensions.'x-sentinelone-file'.file_location | tgtFileLocation |
| **file**:extensions.'x-sentinelone-file'.file_id | tgtFileId |
| **file**:extensions.'x-sentinelone-file'.convicted_by | tgtFileConvictedBy |
| **directory**:path | tgtFilePath, tgtFileOldPath, srcProcImagePath, tgtProcImagePath, srcProcParentImagePath |
| **user-account**:user_id | loginAccountSid, srcProcUser, tgtProcUser |
| **user-account**:account_login | loginsUserName |
| **user-account**:is_privileged | loginIsAdministratorEquivalent |
| **user-account**:display_name | loginAccountName |
| **user-account**:extensions.'x-sentinelone-login'.login_type | loginType |
| **user-account**:extensions.'x-sentinelone-login'.base_type | loginsBaseType |
| **user-account**:extensions.'x-sentinelone-login'.login_failure_reason | loginFailureReason |
| **user-account**:extensions.'x-sentinelone-login'.session_id | loginSessionId |
| **windows-registry-key**:key | registryKeyPath, registryPath |
| **windows-registry-key**:values[*] | registryValue |
| **windows-registry-key**:extensions.'x-sentinelone-registry'.value_type | registryValueType |
| **windows-registry-key**:extensions.'x-sentinelone-registry'.full_size | registryValueFullSize |
| **windows-registry-key**:extensions.'x-sentinelone-registry'.old_value_type | registryOldValueType |
| **windows-registry-key**:extensions.'x-sentinelone-registry'.old_value | registryOldValue |
| **windows-registry-key**:extensions.'x-sentinelone-registry'.old_value_full_size | registryOldValueFullSize |
| **x-sentinelone-indicator**:indicator_name | indicatorName |
| **x-sentinelone-indicator**:indicator_category | indicatorCategory |
| **x-sentinelone-indicator**:indicator_description | indicatorDescription |
| **x-sentinelone-indicator**:indicator_metadata | indicatorMetadata |
| **x-oca-asset**:hostname | endpointName |
| **x-oca-asset**:ip_refs[*].value | srcIp, dstIp |
| **x-oca-asset**:extensions.'x-sentinelone-endpoint'.endpoint_os | endpointOs |
| **x-oca-asset**:extensions.'x-sentinelone-endpoint'.agent_version | agentVersion |
| **x-oca-asset**:extensions.'x-sentinelone-endpoint'.agent_uuid | agentUuid |
| **x-oca-asset**:extensions.'x-sentinelone-endpoint'.machine_type | endpointMachineType |
| **x-oca-event**:action | eventType |
| **x-oca-event**:created | eventTime |
| **x-oca-event**:category[*] | objectType |
| **x-oca-event**:host_ref | endpointName |
| **x-oca-event**:url_ref | url |
| **x-oca-event**:file_ref | fileFullName |
| **x-oca-event**:process_ref | srcProcPid, tgtProcPid, srcProcParentPid |
| **x-oca-event**:parent_process_ref | srcProcParentPid |
| **x-oca-event**:agent | agentName |
| **x-oca-event**:user_ref | srcProcUser, tgtProcUser |
| **x-oca-event**:domain_ref | dnsRequest, dnsResponse, loginAccountDomain |
| **x-oca-event**:registry_ref | registryPath, registryKeyPath |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| directory | path | tgtFilePath |
| directory | path | tgtFileOldPath |
| directory | path | srcProcImagePath |
| directory | path | tgtProcImagePath |
| directory | path | srcProcParentImagePath |
| <br> | | |
| domain-name | value | dnsRequest |
| domain-name | value | dnsResponse |
| domain-name | value | loginAccountDomain |
| <br> | | |
| file | name | fileFullName |
| file | size | tgtFileSize |
| file | hashes.MD5 | tgtFileMd5 |
| file | hashes.MD5 | tgtFileOldMd5 |
| file | hashes.MD5 | srcProcImageMd5 |
| file | hashes.MD5 | tgtProcImageMd5 |
| file | hashes.SHA-1 | tgtFileSha1 |
| file | hashes.SHA-1 | tgtFileOldSha1 |
| file | hashes.SHA-1 | srcProcImageSha1 |
| file | hashes.SHA-1 | tgtProcImageSha1 |
| file | hashes.SHA-256 | srcProcImageSha256 |
| file | hashes.SHA-256 | tgtProcImageSha256 |
| file | hashes.SHA-256 | tgtFileSha256 |
| file | hashes.SHA-256 | tgtFileOldSha256 |
| file | parent_directory_ref | tgtFilePath |
| file | parent_directory_ref | tgtFileOldPath |
| file | parent_directory_ref | srcProcImagePath |
| file | parent_directory_ref | tgtProcImagePath |
| file | parent_directory_ref | srcProcParentImagePath |
| file | created | tgtFileCreatedAt |
| file | modified | tgtFileModifiedAt |
| file | extensions.x-sentinelone-file.file_type | tgtFileType |
| file | extensions.x-sentinelone-file.file_extension | tgtFileExtension |
| file | extensions.x-sentinelone-file.file_id | tgtFileId |
| file | extensions.x-sentinelone-file.file_description | tgtFileDescription |
| file | extensions.x-sentinelone-file.file_location | tgtFileLocation |
| file | extensions.x-sentinelone-file.convicted_by | tgtFileConvictedBy |
| <br> | | |
| ipv4-addr | value | srcIp |
| ipv4-addr | value | srcMachineIP |
| ipv4-addr | value | dstIp |
| <br> | | |
| ipv6-addr | value | srcIp |
| ipv6-addr | value | srcMachineIP |
| ipv6-addr | value | dstIp |
| <br> | | |
| network-traffic | src_ref | srcIp |
| network-traffic | protocols | netProtocolName |
| network-traffic | dst_ref | dstIp |
| network-traffic | dst_port | dstPort |
| network-traffic | src_port | srcPort |
| network-traffic | extensions.x-sentinelone-network-action.event_direction | netEventDirection |
| network-traffic | extensions.x-sentinelone-network-action.connection_status | netConnStatus |
| <br> | | |
| process | binary_ref | srcProcImageMd5 |
| process | binary_ref | tgtProcImageMd5 |
| process | binary_ref | srcProcImageSha1 |
| process | binary_ref | tgtProcImageSha1 |
| process | binary_ref | srcProcImageSha256 |
| process | binary_ref | tgtProcImageSha256 |
| process | creator_user_ref | srcProcUser |
| process | creator_user_ref | tgtProcUser |
| process | command_line | srcProcCmdLine |
| process | command_line | tgtProcCmdLine |
| process | created | srcProcStartTime |
| process | created | tgtProcStartTime |
| process | created | srcProcParentStartTime |
| process | parent_ref | srcProcParentStartTime |
| process | pid | srcProcPid |
| process | pid | tgtProcPid |
| process | pid | srcProcParentPid |
| process | parent_ref | srcProcParentPid |
| process | name | srcProcParentName |
| process | parent_ref | srcProcParentName |
| process | name | tgtProcName |
| process | name | srcProcName |
| process | extensions.x-sentinelone-process.story_line_id | srcProcStorylineId |
| process | extensions.x-sentinelone-process.story_line_id | tgtProcStorylineId |
| process | extensions.x-sentinelone-process.integrity_level | srcProcIntegrityLevel |
| process | extensions.x-sentinelone-process.integrity_level | tgtProcIntegrityLevel |
| process | x_unique_id | srcProcUid |
| process | x_unique_id | tgtProcUid |
| process | extensions.x-sentinelone-process.signed_status | srcProcSignedStatus |
| process | extensions.x-sentinelone-process.signed_status | tgtProcSignedStatus |
| process | extensions.x-sentinelone-process.publisher | srcProcPublisher |
| process | extensions.x-sentinelone-process.publisher | tgtProcPublisher |
| process | extensions.x-sentinelone-process.verified_status | srcProcVerifiedStatus |
| process | extensions.x-sentinelone-process.verified_status | tgtProcVerifiedStatus |
| process | extensions.x-sentinelone-process.signature_invalid_reason | srcProcReasonSignatureInvalid |
| process | extensions.x-sentinelone-process.signature_invalid_reason | tgtProcReasonSignatureInvalid |
| process | extensions.x-sentinelone-process.sub_system | srcProcSubsystem |
| process | extensions.x-sentinelone-process.sub_system | tgtProcSubsystem |
| process | extensions.x-sentinelone-process.session_id | srcProcSessionId |
| process | extensions.x-sentinelone-process.session_id | tgtProcSessionId |
| process | extensions.x-sentinelone-process.active_content_type | srcProcActiveContentType |
| process | extensions.x-sentinelone-process.active_content_type | tgtProcActiveContentType |
| process | extensions.x-sentinelone-process.active_content_fileid | srcProcActiveContentFileId |
| process | extensions.x-sentinelone-process.active_content_fileid | tgtProcActiveContentFileId |
| process | extensions.x-sentinelone-process.active_content_path | srcProcActiveContentPath |
| process | extensions.x-sentinelone-process.active_content_path | tgtProcActiveContentPath |
| process | extensions.x-sentinelone-process.active_content_hash | srcProcActiveContentHash |
| process | extensions.x-sentinelone-process.active_content_hash | tgtProcActiveContentHash |
| process | extensions.x-sentinelone-process.active_content_signed_status | srcProcActiveContentSignedStatus |
| process | extensions.x-sentinelone-process.active_content_signed_status | tgtProcActiveContentSignedStatus |
| process | x_unique_id | srcProcParentUid |
| <br> | | |
| url | value | url |
| <br> | | |
| user-account | user_id | loginAccountSid |
| user-account | user_id | srcProcUser |
| user-account | user_id | tgtProcUser |
| user-account | account_login | loginsUserName |
| user-account | is_privileged | loginIsAdministratorEquivalent |
| user-account | display_name | loginAccountName |
| user-account | extensions.x-sentinelone-login.base_type | loginsBaseType |
| user-account | extensions.x-sentinelone-login.login_type | loginType |
| user-account | extensions.x-sentinelone-login.login_failure_reason | loginFailureReason |
| user-account | extensions.x-sentinelone-login.session_id | loginSessionId |
| <br> | | |
| windows-registry-key | key | registryKeyPath |
| windows-registry-key | key | registryPath |
| windows-registry-key | values | registryValue |
| windows-registry-key | extensions.x-sentinelone-registry.value_type | registryValueType |
| windows-registry-key | extensions.x-sentinelone-registry.full_size | registryValueFullSize |
| windows-registry-key | extensions.x-sentinelone-registry.old_value_type | registryOldValueType |
| windows-registry-key | extensions.x-sentinelone-registry.old_value | registryOldValue |
| windows-registry-key | extensions.x-sentinelone-registry.old_value_full_size | registryOldValueFullSize |
| <br> | | |
| x-oca-asset | ip_refs | srcIp |
| x-oca-asset | ip_refs | dstIp |
| x-oca-asset | hostname | endpointName |
| x-oca-asset | extensions.x-sentinelone-endpoint.endpoint_os | endpointOs |
| x-oca-asset | extensions.x-sentinelone-endpoint.agent_uuid | agentUuid |
| x-oca-asset | extensions.x-sentinelone-endpoint.agent_version | agentVersion |
| x-oca-asset | extensions.x-sentinelone-endpoint.machine_type | endpointMachineType |
| <br> | | |
| x-oca-event | file_ref | fileFullName |
| x-oca-event | user_ref | srcProcUser |
| x-oca-event | user_ref | tgtProcUser |
| x-oca-event | domain_ref | dnsRequest |
| x-oca-event | domain_ref | dnsResponse |
| x-oca-event | domain_ref | loginAccountDomain |
| x-oca-event | url_ref | url |
| x-oca-event | process_ref | srcProcPid |
| x-oca-event | process_ref | tgtProcPid |
| x-oca-event | parent_process_ref | srcProcParentPid |
| x-oca-event | process_ref | srcProcParentPid |
| x-oca-event | registry_ref | registryKeyPath |
| x-oca-event | registry_ref | registryPath |
| x-oca-event | host_ref | endpointName |
| x-oca-event | category | objectType |
| x-oca-event | action | eventType |
| x-oca-event | created | eventTime |
| x-oca-event | agent | agentName |
| <br> | | |
| x-sentinelone-indicator | indicator_name | indicatorName |
| x-sentinelone-indicator | indicator_category | indicatorCategory |
| x-sentinelone-indicator | indicator_description | indicatorDescription |
| x-sentinelone-indicator | indicator_metadata | indicatorMetadata |
| <br> | | |
