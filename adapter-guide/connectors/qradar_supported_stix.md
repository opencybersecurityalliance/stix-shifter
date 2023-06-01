##### Updated on 04/18/23
## IBM QRadar
### Supported STIX Operators
*Comparison AND/OR operators are inside the observation while observation AND/OR operators are between observations (square brackets).*

| STIX Operator | Data Source Operator |
|--|--|
| AND (Comparision) | AND |
| OR (Comparision) | OR |
| > | > |
| >= | >= |
| < | < |
| <= | <= |
| = | = |
| != | != |
| LIKE | LIKE |
| IN | IN |
| MATCHES | MATCHES |
| ISSUBSET | INCIDR |
| OR (Observation) | OR |
| AND (Observation) | OR |
| <br> | |
### Searchable STIX objects and properties for Events dialect
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **ipv4-addr**:value | sourceaddress, destinationaddress, identityip |
| **ipv6-addr**:value | sourceaddress, destinationaddress |
| **url**:value | URL |
| **mac-addr**:value | sourcemac, destinationmac |
| **file**:name | Filename |
| **file**:hashes.'SHA-256' | "SHA256 Hash" |
| **file**:hashes.MD5 | "MD5 Hash" |
| **file**:hashes.'SHA-1' | "SHA1 Hash" |
| **file**:parent_directory_ref | "File Path" |
| **file**:parent_directory_ref.path | "File Path" |
| **directory**:path | "File Path" |
| **network-traffic**:src_port | sourceport |
| **network-traffic**:dst_port | destinationport |
| **network-traffic**:protocols[*] | protocolid |
| **network-traffic**:start | starttime |
| **network-traffic**:end | endtime |
| **network-traffic**:src_ref.value | sourceaddress, sourcemac |
| **network-traffic**:dst_ref.value | destinationaddress, destinationmac |
| **user-account**:user_id | username |
| **user-account**:account_login | username |
| **artifact**:payload_bin | UTF8(payload) |
| **domain-name**:value | "DNS Request Domain", UrlHost |
| **x-qradar**:qid | qid |
| **x-qradar**:magnitude | magnitude |
| **x-qradar**:log_source_id | logsourceid |
| **x-qradar**:device_type | devicetype |
| **x-qradar**:category_id | category |
| **x-qradar**:high_level_category_id | highlevelcategory |
| **x-qradar**:direction | eventdirection |
| **x-qradar**:severity | severity |
| **x-qradar**:credibility | credibility |
| **x-qradar**:relevance | relevance |
| **x-qradar**:domain_id | domainid |
| **x-qradar**:has_offense | hasoffense |
| **x-qradar**:INOFFENSE | INOFFENSE |
| **x-ibm-finding**:name | "CRE Name" |
| **x-ibm-finding**:description | "CRE Description" |
| **x-ibm-finding**:severity | severity |
| **x-ibm-finding**:start | starttime |
| **x-ibm-finding**:end | endtime |
| **x-ibm-finding**:magnitude | magnitude |
| **x-ibm-finding**:event_count | eventcount |
| **x-ibm-finding**:src_geolocation | sourcegeographiclocation |
| **x-ibm-finding**:dst_geolocation | destinationgeographiclocation |
| **x-ibm-finding**:rule_names[*] | rulename(creeventlist) |
| **process**:pid | "Process ID" |
| **process**:name | "Process Name", Image, ParentImage, TargetImage |
| **process**:binary_ref.name | Image, TargetImage |
| **process**:binary_ref.parent_directory_ref.path | Image, TargetImage |
| **process**:parent_ref.binary_ref.name | ParentImage |
| **process**:command_line | "Process CommandLine", ParentCommandLine |
| **process**:parent_ref.command_line | ParentCommandLine |
| **process**:extensions.'windows-service-ext'.service_dll_refs[*].name | ServiceFileName |
| **process**:x_unique_id | "Process Guid" |
| **x-oca-event**:action | QIDNAME(qid) |
| **x-oca-event**:code | EventID |
| **x-oca-event**:outcome | CATEGORYNAME(category) |
| **x-oca-event**:category | CATEGORYNAME(highlevelcategory) |
| **x-oca-event**:created | devicetime |
| **x-oca-event**:agent | LOGSOURCENAME(logsourceid) |
| **x-oca-event**:provider | LOGSOURCETYPENAME(devicetype) |
| **x-oca-event**:process_ref.command_line | "Process CommandLine" |
| **x-oca-event**:process_ref.binary_ref.name | Image, TargetImage |
| **x-oca-event**:process_ref.parent_ref.command_line | ParentCommandLine |
| **x-oca-event**:process_ref.creator_user_ref.user_id | username |
| **x-oca-event**:process_ref.name | "Process Name" |
| **x-oca-event**:process_ref.pid | "Process ID" |
| **x-oca-event**:parent_process_ref.command_line | ParentCommandLine |
| **x-oca-event**:parent_process_ref.binary_ref.name | ParentImage |
| **x-oca-event**:domain_ref.value | "DNS Request Domain", UrlHost |
| **x-oca-event**:file_ref.name | Filename |
| **x-oca-event**:host_ref.hostname | identityhostname, "Machine ID" |
| **x-oca-event**:host_ref.ip_refs[*].value | identityip, sourceaddress |
| **x-oca-event**:registry_ref.key | ObjectName, "Registry Key" |
| **x-oca-event**:user_ref.user_id | username |
| **x-oca-event**:url_ref.value | URL |
| **x-oca-event**:original_ref.payload_bin | UTF8(payload), Message |
| **x-oca-asset**:hostname | identityhostname, "Machine ID" |
| **x-oca-asset**:ip_refs[*].value | identityip, sourceaddress |
| **x-oca-asset**:mac_refs[*].value | sourcemac |
| **windows-registry-key**:key | ObjectName, "Registry Key" |
| **windows-registry-key**:values[*].name | "Registry Value Name" |
| <br> | |
### Searchable STIX objects and properties for Flows dialect
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **ipv4-addr**:value | sourceaddress, destinationaddress |
| **ipv6-addr**:value | sourcev6, destinationv6 |
| **file**:name | Filename |
| **file**:size | filesize |
| **file**:hashes.'SHA-256' | "SHA256 Hash" |
| **file**:hashes.MD5 | "MD5 Hash" |
| **file**:hashes.'SHA-1' | "SHA1 Hash" |
| **file**:'mime-type' | contenttype |
| **domain-name**:value | "DNS Request Domain" |
| **url**:value | "DNS Request Domain", tlsservernameindication, httphost |
| **network-traffic**:src_port | sourceport |
| **network-traffic**:dst_port | destinationport |
| **network-traffic**:protocols[*] | protocolid |
| **network-traffic**:start | starttime |
| **network-traffic**:end | endtime |
| **network-traffic**:src_ref.value | sourceaddress, sourcev6 |
| **network-traffic**:dst_ref.value | destinationaddress, destinationv6 |
| **network-traffic**:src_byte_count | sourcebytes |
| **network-traffic**:dst_byte_count | destinationbytes |
| **network-traffic**:src_packets | sourcepackets |
| **network-traffic**:dst_packets | destinationpackets |
| **network-traffic**:extensions.'http-request-ext'.request_header.Host | httphost |
| **network-traffic**:extensions.'http-request-ext'.request_header.Referer | httpreferrer |
| **network-traffic**:extensions.'http-request-ext'.request_header.Server | httpserver |
| **network-traffic**:extensions.'http-request-ext'.request_header.'User-Agent' | httpuseragent |
| **network-traffic**:extensions.'http-request-ext'.request_header.'Content-Type' | contenttype |
| **network-traffic**:extensions.'http-request-ext'.request_version | httpversion |
| **network-traffic**:ipfix.flowId | flowid |
| **software**:name | applicationname |
| **artifact**:payload_bin | flowsourcepayload, flowdestinationpayload |
| **x-qradar**:qid | qid |
| **x-qradar**:qid_name | QIDNAME(qid) |
| **x-qradar**:flow_source | flowsource |
| **x-qradar**:flow_interface_id | flowinterfaceid |
| **x-qradar**:flow_interface | flowinterface |
| **x-qradar**:geographic | geographic |
| **x-qradar**:category_name | CATEGORYNAME(category) |
| **x-qradar**:credibility | credibility |
| **x-qradar**:severity | flowseverity |
| **x-qradar**:direction | eventdirection |
| **x-qradar**:relevance | relevance |
| **x-qradar**:first_packet_time | firstpackettime |
| **x-qradar**:last_packet_time | lastpackettime |
| **x-qradar**:application_id | applicationid |
| **x-qradar**:application_name | applicationname |
| **x-qradar**:flow_type | flowtype |
| **x-qradar**:file_entropy | fileentropy |
| **x-qradar**:http_response_code | httpresponsecode |
| **x-qradar**:tls_server_name_indication | tlsservernameindication |
| **x-qradar**:tls_ja3_hash | tlsja3hash |
| **x-qradar**:tls_ja3s_hash | tlsja3shash |
| **x-qradar**:suspect_content_descriptions | suspectcontentdescriptions |
| **x-qradar**:has_offense | hasoffense |
| **x-qradar**:INOFFENSE | INOFFENSE |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| artifact | payload_bin | UTF8(payload) |
| artifact | mime_type | mime_type_eventpayload |
| artifact | payload_bin | flowsourcepayload |
| artifact | mime_type | mime_type_flowsourcepayload |
| artifact | payload_bin | flowdestinationpayload |
| artifact | mime_type | mime_type_flowdestinationpayload |
| artifact | payload_bin | Message |
| artifact | mime_type | mime_type_message |
| <br> | | |
| directory | path | "File Path" |
| directory | path | Image |
| directory | path | ParentImage |
| directory | path | TargetImage |
| directory | path | ServiceFileName |
| <br> | | |
| domain-name | value | UrlHost |
| domain-name | value | "DNS Request Domain" |
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
| file | name | TargetImage |
| file | parent_directory_ref | TargetImage |
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
| network-traffic | extensions.http-request-ext.request_header.Host | httphost |
| network-traffic | extensions.http-request-ext.request_header.Referer | httpreferrer |
| network-traffic | extensions.http-request-ext.request_header.Server | httpserver |
| network-traffic | extensions.http-request-ext.request_header.User-Agent | httpuseragent |
| network-traffic | extensions.http-request-ext.request_version | httpversion |
| network-traffic | ipfix.flowId | flowid |
| network-traffic | extensions.http-request-ext.request_header.Content-Type | contenttype |
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
| process | binary_ref | TargetImage |
| process | extensions.windows-service-ext.service_dll_refs | ServiceFileName |
| process | x_unique_id | "Process Guid" |
| <br> | | |
| software | name | applicationname |
| <br> | | |
| url | value | URL |
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
| x-oca-asset | ip_refs | identityip |
| x-oca-asset | hostname | identityhostname |
| x-oca-asset | ip_refs | sourceaddress |
| x-oca-asset | mac_refs | sourcemac |
| x-oca-asset | hostname | "Machine ID" |
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
| x-oca-event | host_ref | "Machine ID" |
| <br> | | |
| x-qradar | category_id | category |
| x-qradar | high_level_category_id | highlevelcategory |
| x-qradar | relevance | relevance |
| x-qradar | log_source_id | logsourceid |
| x-qradar | direction | eventdirection |
| x-qradar | qid | qid |
| x-qradar | domain_name | DOMAINNAME(domainid) |
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
