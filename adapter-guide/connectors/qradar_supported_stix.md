## IBM QRadar
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| artifact | payload_bin | UTF8(payload) |
| artifact | payload_bin | flowsourcepayload |
| artifact | payload_bin | flowdestinationpayload |
| artifact | payload_bin | Message |
| <br> | | |
| directory | path | "File Path" |
| directory | path | Image |
| directory | path | ParentImage |
| directory | path | ServiceFileName |
| <br> | | |
| domain-name | value | UrlHost |
| domain-name | value | DOMAINNAME(domainid) |
| domain-name | value | dnsdomainname |
| <br> | | |
| email-message | content_type | contenttype |
| <br> | | |
| file | name | Filename |
| file | hashes.SHA-256 | "SHA256 Hash" |
| file | hashes.SHA-1 | "SHA1 Hash" |
| file | hashes.MD5 | "MD5 Hash" |
| file | hashes.UNKNOWN | "File Hash" |
| file | size | filesize |
| file | parent_directory_ref | "File Path" |
| file | mime_type | contenttype |
| file | name | Image |
| file | parent_directory_ref | Image |
| file | name | ParentImage |
| file | parent_directory_ref | ParentImage |
| file | name | ServiceFileName |
| file | parent_directory_ref | ServiceFileName |
| <br> | | |
| ipv4-addr | value | identityip |
| ipv4-addr | value | destinationaddress |
| ipv4-addr | value | sourceaddress |
| ipv4-addr | resolves_to_refs | sourcemac |
| ipv4-addr | resolves_to_refs | destinationmac |
| <br> | | |
| ipv6-addr | value | identityip |
| ipv6-addr | value | destinationaddress |
| ipv6-addr | value | destinationv6 |
| ipv6-addr | value | sourceaddress |
| ipv6-addr | value | sourcev6 |
| ipv6-addr | resolves_to_refs | sourcemac |
| ipv6-addr | resolves_to_refs | destinationmac |
| <br> | | |
| mac-addr | value | sourcemac |
| mac-addr | value | destinationmac |
| <br> | | |
| network-traffic | dst_ref | destinationaddress |
| network-traffic | dst_ref | destinationv6 |
| network-traffic | src_ref | sourceaddress |
| network-traffic | src_ref | sourcev6 |
| network-traffic | extensions.dns-ext.question.domain_ref | UrlHost |
| network-traffic | src_payload_ref | flowsourcepayload |
| network-traffic | dst_payload_ref | flowdestinationpayload |
| network-traffic | dst_port | destinationport |
| network-traffic | src_port | sourceport |
| network-traffic | src_byte_count | sourcebytes |
| network-traffic | dst_byte_count | destinationbytes |
| network-traffic | src_packets | sourcepackets |
| network-traffic | dst_packets | destinationpackets |
| network-traffic | protocols | PROTOCOLNAME(protocolid) |
| network-traffic | extensions.http_request_ext.request_header.Host | httphost |
| network-traffic | extensions.http_request_ext.request_header.Referer | httpreferrer |
| network-traffic | extensions.http_request_ext.request_header.Server | httpserver |
| network-traffic | extensions.http_request_ext.request_header.User_Agent | httpuseragent |
| network-traffic | extensions.http_request_ext.request_version | httpversion |
| network-traffic | ipfix.flowId | flowid |
| network-traffic | extensions.http_request_ext.request_header.Content_Type | contenttype |
| <br> | | |
| process | creator_user_ref | username |
| process | binary_ref | Image |
| process | binary_ref | ParentImage |
| process | parent_ref | ParentImage |
| process | command_line | "Process CommandLine" |
| process | command_line | ParentCommandLine |
| process | parent_ref | ParentCommandLine |
| process | name | "Process Name" |
| process | pid | "Process ID" |
| process | pid | "Parent Process ID" |
| process | parent_ref | "Parent Process ID" |
| process | extensions.windows_service_ext.service_dll_refs | ServiceFileName |
| <br> | | |
| software | name | applicationname |
| <br> | | |
| url | value | URL |
| url | value | dnsdomainname |
| url | value | httphost |
| url | value | tlsservernameindication |
| <br> | | |
| user-account | user_id | username |
| <br> | | |
| windows-registry-key | key | ObjectName |
| windows-registry-key | values | "Registry Value Name" |
| <br> | | |
| x-ibm-finding | src_application_user_ref | username |
| x-ibm-finding | dst_ip_ref | destinationaddress |
| x-ibm-finding | event_count | eventcount |
| x-ibm-finding | finding_type | eventcount |
| x-ibm-finding | start | starttime |
| x-ibm-finding | end | endtime |
| x-ibm-finding | magnitude | magnitude |
| x-ibm-finding | src_ip_ref | sourceaddress |
| x-ibm-finding | src_geolocation | sourcegeographiclocation |
| x-ibm-finding | dst_geolocation | destinationgeographiclocation |
| x-ibm-finding | severity | severity |
| x-ibm-finding | rule_names | rulename(creeventlist) |
| x-ibm-finding | name | "CRE Name" |
| x-ibm-finding | description | "CRE Description" |
| <br> | | |
| x-ibm-windows | targetimage | TargetImage |
| x-ibm-windows | granted_access | "Granted Access" |
| x-ibm-windows | call_trace | "Call Trace" |
| x-ibm-windows | source_image | SourceImage |
| x-ibm-windows | pipe_name | PipeName |
| x-ibm-windows | start_module | StartModule |
| x-ibm-windows | start_function | StartFunction |
| x-ibm-windows | signed | Signed |
| x-ibm-windows | imphash | "IMP Hash" |
| <br> | | |
| x-oca-asset | ip_refs | identityip |
| x-oca-asset | hostname | identityhostname |
| x-oca-asset | ip_refs | sourceaddress |
| x-oca-asset | mac_refs | sourcemac |
| <br> | | |
| x-oca-event | user_ref | username |
| x-oca-event | outcome | CATEGORYNAME(category) |
| x-oca-event | category | CATEGORYNAME(highlevelcategory) |
| x-oca-event | host_ref | identityip |
| x-oca-event | host_ref | identityhostname |
| x-oca-event | action | QIDNAME(qid) |
| x-oca-event | created | devicetime |
| x-oca-event | network_ref | destinationaddress |
| x-oca-event | network_ref | destinationv6 |
| x-oca-event | agent | LOGSOURCENAME(logsourceid) |
| x-oca-event | provider | LOGSOURCETYPENAME(devicetype) |
| x-oca-event | network_ref | sourceaddress |
| x-oca-event | network_ref | sourcev6 |
| x-oca-event | url_ref | URL |
| x-oca-event | domain_ref | UrlHost |
| x-oca-event | network_ref | UrlHost |
| x-oca-event | file_ref | Filename |
| x-oca-event | file_ref | "File Path" |
| x-oca-event | original_ref | UTF8(payload) |
| x-oca-event | process_ref | Image |
| x-oca-event | parent_process_ref | ParentImage |
| x-oca-event | process_ref | "Process CommandLine" |
| x-oca-event | parent_process_ref | ParentCommandLine |
| x-oca-event | process_ref | "Process Name" |
| x-oca-event | process_ref | "Process ID" |
| x-oca-event | code | EventID |
| x-oca-event | parent_process_ref | "Parent Process ID" |
| x-oca-event | registry_ref | ObjectName |
| x-oca-event | registry_ref | "Registry Value Name" |
| x-oca-event | original_ref | Message |
| x-oca-event | original | Message |
| <br> | | |
| x-qradar | category_id | category |
| x-qradar | high_level_category_id | highlevelcategory |
| x-qradar | relevance | relevance |
| x-qradar | log_source_id | logsourceid |
| x-qradar | direction | eventdirection |
| x-qradar | qid | qid |
| x-qradar | domain_name | DOMAINNAME(domainid) |
| x-qradar | domain_name | dnsdomainname |
| x-qradar | flow_source | flowsource |
| x-qradar | flow_interface | flowinterface |
| x-qradar | flow_interface_id | flowinterfaceid |
| x-qradar | geographic | geographic |
| x-qradar | credibility | credibility |
| x-qradar | severity | flowseverity |
| x-qradar | first_packet_time | firstpackettime |
| x-qradar | last_packet_time | lastpackettime |
| x-qradar | application_id | applicationid |
| x-qradar | cre_event_list | creeventlist |
| x-qradar | domain_id | domainid |
| x-qradar | device_type | devicetype |
| x-qradar | flow_type | flowtype |
| x-qradar | file_entropy | fileentropy |
| x-qradar | http_response_code | httpresponsecode |
| x-qradar | tls_ja3_hash | tlsja3hash |
| x-qradar | tls_ja3s_hash | tlsja3shash |
| x-qradar | suspect_content_descriptions | suspectcontentdescriptions |
| x-qradar | tls_server_name_indication | tlsservernameindication |
| x-qradar | registry_key | "Registry Key" |
| x-qradar | has_offense | hasoffense |
| <br> | | |
