##### Updated on 04/05/22
## sentinelone
### Supported STIX Operators
| STIX Operator | Data Source Operator |
|--|--|
| AND | AND |
| OR  | OR |
| > | > |
| >= | >= |
| < | < |
| <= | <= |
| = | = |
| != | != |
| LIKE | in contains anycase |
| IN | IN |
| MATCHES | regexp |
| <br> | |
### Supported STIX Objects and Properties
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
| file | hashes.SHA-1 | tgtFileSha1 |
| file | hashes.SHA-1 | tgtFileOldSha1 |
| file | hashes.SHA-1 | srcProcImageSha1 |
| file | hashes.SHA-1 | tgtProcImageSha1 |
| file | hashes.SHA-256 | tgtFileSha256 |
| file | hashes.SHA-256 | tgtFileOldSha256 |
| file | hashes.SHA-256 | srcProcImageSha256 |
| file | hashes.SHA-256 | tgtProcImageSha256 |
| file | hashes.MD5 | tgtFileMd5 |
| file | hashes.MD5 | tgtFileOldMd5 |
| file | hashes.MD5 | srcProcImageMd5 |
| file | hashes.MD5 | tgtProcImageMd5 |
| file | created | tgtFileCreatedAt |
| file | modified | tgtFileModifiedAt |
| file | size | tgtFileSize |
| file | parent_directory_ref | tgtFilePath |
| file | parent_directory_ref | tgtFileOldPath |
| file | parent_directory_ref | srcProcImagePath |
| file | parent_directory_ref | tgtProcImagePath |
| file | parent_directory_ref | srcProcParentImagePath |
| file | extensions.x-sentinelone-file.file_type | tgtFileType |
| file | extensions.x-sentinelone-file.file_extension | tgtFileExtension |
| file | extensions.x-sentinelone-file.file_description | tgtFileDescription |
| file | extensions.x-sentinelone-file.file_location | tgtFileLocation |
| file | extensions.x-sentinelone-file.file_id | tgtFileId |
| file | extensions.x-sentinelone-file.convicted_by | tgtFileConvictedBy |
| <br> | | |
| ipv4-addr | value | srcIp |
| ipv4-addr | value | dstIp |
| ipv4-addr | value | srcMachineIP |
| <br> | | |
| ipv6-addr | value | srcIp |
| ipv6-addr | value | dstIp |
| ipv6-addr | value | srcMachineIP |
| <br> | | |
| network-traffic | src_ref | srcIp |
| network-traffic | protocols | netProtocolName |
| network-traffic | dst_ref | dstIp |
| network-traffic | dst_port | dstPort |
| network-traffic | src_port | srcPort |
| network-traffic | extensions.x-sentinelone-network-action.connection_status | netConnStatus |
| network-traffic | extensions.x-sentinelone-network-action.event_direction | netEventDirection |
| <br> | | |
| process | name | srcProcName |
| process | name | tgtProcName |
| process | name | srcProcParentName |
| process | pid | tgtProcPid |
| process | pid | srcProcPid |
| process | pid | srcProcParentPid |
| process | command_line | srcProcCmdLine |
| process | command_line | tgtProcCmdLine |
| process | created | srcProcStartTime |
| process | created | tgtProcStartTime |
| process | created | srcProcParentStartTime |
| process | parent_ref | srcProcParentName |
| process | parent_ref | srcProcParentPid |
| process | creator_user_ref | srcProcUser |
| process | creator_user_ref | tgtProcUser |
| process | extensions.x-sentinelone-process.integrity_level | srcProcIntegrityLevel |
| process | extensions.x-sentinelone-process.integrity_level | tgtProcIntegrityLevel |
| process | extensions.x-sentinelone-process.publisher | srcProcPublisher |
| process | extensions.x-sentinelone-process.publisher | tgtProcPublisher |
| process | extensions.x-sentinelone-process.story_line_id | srcProcStorylineId |
| process | extensions.x-sentinelone-process.story_line_id | tgtProcStorylineId |
| process | extensions.x-sentinelone-process.process_unique_id | srcProcUid |
| process | extensions.x-sentinelone-process.process_unique_id | tgtProcUid |
| process | extensions.x-sentinelone-process.process_unique_id | srcProcParentUid |
| process | extensions.x-sentinelone-process.signed_status | srcProcSignedStatus |
| process | extensions.x-sentinelone-process.signed_status | tgtProcSignedStatus |
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
| <br> | | |
| url | value | url |
| <br> | | |
| user-account | user_id | loginAccountSid |
| user-account | user_id | srcProcUser |
| user-account | user_id | tgtProcUser |
| user-account | display_name | loginAccountName |
| user-account | is_privileged | loginIsAdministratorEquivalent |
| user-account | extensions.x-sentinelone-login.login_type | loginType |
| user-account | extensions.x-sentinelone-login.base_type | loginsBaseType |
| user-account | extensions.x-sentinelone-login.login_failure_reason | loginFailureReason |
| user-account | extensions.x-sentinelone-login.session_id | loginSessionId |
| user-account | account_login | loginsUserName |
| <br> | | |
| windows-registry-key | extensions.x-sentinelone-registry.path | registryPath |
| windows-registry-key | extensions.x-sentinelone-registry.full_size | registryValueFullSize |
| windows-registry-key | extensions.x-sentinelone-registry.value_type | registryValueType |
| windows-registry-key | extensions.x-sentinelone-registry.old_value_type | registryOldValueType |
| windows-registry-key | extensions.x-sentinelone-registry.old_value | registryOldValue |
| windows-registry-key | extensions.x-sentinelone-registry.old_value_full_size | registryOldValueFullSize |
| windows-registry-key | key | registryKeyPath |
| windows-registry-key | values | registryValue |
| <br> | | |
| x-sentinelone-indicator | indicator_name | indicatorName |
| x-sentinelone-indicator | indicator_category | indicatorCategory |
| x-sentinelone-indicator | indicator_description | indicatorDescription |
| x-sentinelone-indicator | indicator_metadata | indicatorMetadata |
| <br> | | |
| x-oca-asset | hostname | endpointName |
| x-oca-asset | ip_refs | srcIp |
| x-oca-asset | ip_refs | dstIp |
| x-oca-asset | extensions.x-sentinelone-endpoint.endpoint_os | endpointOs |
| x-oca-asset | extensions.x-sentinelone-endpoint.agent_version | agentVersion |
| x-oca-asset | extensions.x-sentinelone-endpoint.machine_type | endpointMachineType |
| x-oca-asset | extensions.x-sentinelone-endpoint.agent_uuid | agentUuid |
| <br> | | |
| x-oca-event | action | eventType |
| x-oca-event | created | eventTime |
| x-oca-event | category | objectType |
| x-oca-event | host_ref | endpointName |
| x-oca-event | url_ref | url |
| x-oca-event | file_ref | fileFullName |
| x-oca-event | process_ref | srcProcPid |
| x-oca-event | process_ref | tgtProcPid |
| x-oca-event | process_ref | srcProcParentPid |
| x-oca-event | parent_process_ref | srcProcParentPid |
| x-oca-event | agent | agentName |
| x-oca-event | user_ref | srcProcUser |
| x-oca-event | user_ref | tgtProcUser |
| x-oca-event | domain_ref | dnsRequest |
| x-oca-event | domain_ref | dnsResponse |
| x-oca-event | domain_ref | loginAccountDomain |
| x-oca-event | registry_ref | registryKeyPath |
| <br> | | |

