##### Updated on 05/15/23
## Micro Focus ArcSight
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
| > | > |
| >= | >= |
| < | < |
| <= | <= |
| = | = |
| != | != |
| LIKE | = |
| IN | IN |
| MATCHES | CONTAINS |
| ISSUBSET | insubnet |
| OR (Observation) | OR |
| AND (Observation) | AND |
| <br> | |
### Searchable STIX objects and properties
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **ipv4-addr**:value | sourceAddress, destinationAddress |
| **ipv6-addr**:value | fulltextSearch |
| **mac-addr**:value | sourceMacAddress, destinationMacAddress |
| **network-traffic**:src_port | sourcePort |
| **network-traffic**:dst_port | destinationPort |
| **network-traffic**:protocols[*] | transportProtocol, applicationProtocol |
| **network-traffic**:src_ref.value | sourceAddress, sourceMacAddress |
| **network-traffic**:dst_ref.value | destinationAddress, destinationMacAddress |
| **directory**:path | filePath |
| **file**:parent_directory_ref.path | filePath |
| **file**:name | fileName |
| **file**:hashes.'SHA-256' | fulltextSearch |
| **file**:hashes.'SHA-1' | fulltextSearch |
| **file**:hashes.MD5 | fulltextSearch |
| **process**:name | destinationProcessName, sourceProcessName |
| **process**:parent_ref.name | sourceProcessName |
| **process**:command_line | destinationServiceName, sourceServiceName |
| **domain-name**:value | sourceHostName, destinationHostName |
| **user-account**:user_id | destinationUserId, sourceUserId |
| **user-account**:account_login | destinationUserName, sourceUserName |
| **windows-registry-key**:key | filePath |
| **windows-registry-key**:values[*] | deviceCustomString4 |
| **x-arcsight-event**:priority | priority |
| **x-arcsight-event**:base_event_count | baseEventCount |
| **x-arcsight-event**:event_id | eventId |
| **x-arcsight-event**:external_id | externalId |
| **x-arcsight-event**:name | name |
| **x-arcsight-event**:type | type |
| **x-arcsight-event**:start_time | startTime |
| **x-arcsight-event**:end_time | endTime |
| **x-arcsight-event**:request_url | requestUrl |
| **x-arcsight-event**:request_method | requestMethod |
| **x-arcsight-event-category**:category_behavior | categoryBehavior |
| **x-arcsight-event-category**:category_device_group | categoryDeviceGroup |
| **x-arcsight-event-category**:category_object | categoryObject |
| **x-arcsight-event-category**:category_outcome | categoryOutcome |
| **x-arcsight-event-category**:category_significance | categorySignificance |
| **x-arcsight-event-category**:category_technique | categoryTechnique |
| **x-arcsight-event-device**:product | deviceProduct |
| **x-arcsight-event-device**:vendor | deviceVendor |
| **x-arcsight-event-device**:device_action | deviceAction |
| **x-arcsight-event-device**:device_receipt_time | deviceReceiptTime |
| **x-arcsight-event-device**:device_event_category | deviceEventCategory |
| **x-arcsight-event-device**:device_severity | deviceSeverity |
| **x-arcsight-event-device**:device_version | deviceVersion |
| **x-arcsight-event-device**:device_address | deviceAddress |
| **x-arcsight-event-device**:device_external_id | deviceExternalId |
| **x-arcsight-event-device**:device_asset_id | fulltextSearch |
| **x-arcsight-event-device**:device_asset_name | fulltextSearch |
| **x-arcsight-event-device**:device_dns_domain | fulltextSearch |
| **x-arcsight-event-device**:device_domain | fulltextSearch |
| **x-arcsight-event-device**:device_nt_domain | fulltextSearch |
| **x-arcsight-event-destination**:destination_asset_id | fulltextSearch |
| **x-arcsight-event-destination**:destination_asset_name | fulltextSearch |
| **x-arcsight-event-destination**:destination_dns_domain | destinationDnsDomain |
| **x-arcsight-event-destination**:destination_fqdn | fulltextSearch |
| **x-arcsight-event-destination**:destination_nt_domain | destinationNtDomain |
| **x-arcsight-event-destination**:destination_geo_location_info | fulltextSearch |
| **x-arcsight-event-destination**:destination_geo_postal_code | fulltextSearch |
| **x-arcsight-event-source**:source_asset_id | fulltextSearch |
| **x-arcsight-event-source**:source_asset_name | fulltextSearch |
| **x-arcsight-event-source**:source_dns_domain | fulltextSearch |
| **x-arcsight-event-source**:source_fqdn | fulltextSearch |
| **x-arcsight-event-source**:source_nt_domain | sourceNtDomain |
| **x-arcsight-event-source**:source_geo_location_info | fulltextSearch |
| **x-arcsight-event-source**:source_geo_postal_code | fulltextSearch |
| **x-arcsight-event-vulnerability**:vulnerability | fulltextSearch |
| **x-arcsight-event-vulnerability**:vulnerability_external_id | vulnerabilityExternalID |
| **x-arcsight-event-vulnerability**:vulnerability_id | fulltextSearch |
| **x-arcsight-event-vulnerability**:vulnerability_name | fulltextSearch |
| **x-arcsight-event-vulnerability**:vulnerability_reference_id | fulltextSearch |
| **x-arcsight-event-vulnerability**:vulnerability_resource | fulltextSearch |
| **x-arcsight-event-vulnerability**:vulnerability_uri | vulnerabilityURI |
| **x-ibm-finding**:name | name |
| **x-ibm-finding**:finding_type | categorySignificance |
| **x-ibm-finding**:src_device | fulltextSearch |
| **x-ibm-finding**:dst_device | fulltextSearch |
| **x-ibm-finding**:src_geolocation | fulltextSearch |
| **x-ibm-finding**:dst_geolocation | fulltextSearch |
| **x-ibm-finding**:src_ip_ref.value | sourceAddress |
| **x-ibm-finding**:dst_ip_ref.value | destinationAddress |
| **x-oca-asset**:hostname | deviceHostName, deviceAssetName |
| **x-oca-asset**:host_id | deviceAssetId |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| directory | path | filePath |
| <br> | | |
| domain-name | value | destinationHostName |
| domain-name | value | sourceHostName |
| domain-name | value | deviceHostName |
| <br> | | |
| file | name | fileName |
| file | parent_directory_ref | filePath |
| file | hashes.MD5 | MD5 |
| file | hashes.SHA-1 | SHA1 |
| file | hashes.SHA-256 | SHA256 |
| <br> | | |
| ipv4-addr | value | destinationAddress |
| ipv4-addr | value | sourceAddress |
| ipv4-addr | resolves_to_refs | destinationMacAddress |
| ipv4-addr | resolves_to_refs | sourceMacAddress |
| ipv4-addr | value | deviceAddress |
| <br> | | |
| ipv6-addr | value | c6a3 |
| ipv6-addr | value | c6a2 |
| <br> | | |
| mac-addr | value | destinationMacAddress |
| mac-addr | value | sourceMacAddress |
| <br> | | |
| network-traffic | protocols | protocols |
| network-traffic | dst_ref | destinationAddress |
| network-traffic | src_ref | sourceAddress |
| network-traffic | dst_port | destinationPort |
| network-traffic | src_port | sourcePort |
| <br> | | |
| process | name | destinationProcessName |
| process | name | sourceProcessName |
| process | parent_ref | sourceProcessName |
| process | command_line | destinationServiceName |
| process | command_line | sourceServiceName |
| process | pid | dpid |
| process | pid | spid |
| process | parent_ref | spid |
| process | creator_user_ref | destinationUserId |
| process | creator_user_ref | sourceUserId |
| <br> | | |
| user-account | user_id | destinationUserId |
| user-account | user_id | sourceUserId |
| <br> | | |
| windows-registry-key | values | registry_data |
| windows-registry-key | key | registry_key |
| <br> | | |
| x-arcsight-event | event_id | eventId |
| x-arcsight-event | external_id | externalId |
| x-arcsight-event | event_name | name |
| x-arcsight-event | event_type | type |
| x-arcsight-event | event_start_time | startTime |
| x-arcsight-event | event_end_time | endTime |
| x-arcsight-event | base_event_count | baseEventCount |
| x-arcsight-event | priority | priority |
| x-arcsight-event | model_confidence | modelConfidence |
| x-arcsight-event | relevance | relevance |
| x-arcsight-event | request_url | requestUrl |
| x-arcsight-event | request_method | requestMethod |
| x-arcsight-event | protocols | protocols |
| <br> | | |
| x-arcsight-event-category | category_significance | categorySignificance |
| x-arcsight-event-category | category_behavior | categoryBehavior |
| x-arcsight-event-category | category_device_group | categoryDeviceGroup |
| x-arcsight-event-category | category_object | categoryObject |
| x-arcsight-event-category | category_outcome | categoryOutcome |
| x-arcsight-event-category | category_technique | categoryTechnique |
| <br> | | |
| x-arcsight-event-destination | destination_ipv6_address_ref | c6a3 |
| x-arcsight-event-destination | destination_domain_name_ref | destinationHostName |
| x-arcsight-event-destination | destination_username | destinationUserName |
| x-arcsight-event-destination | destination_dns_domain | destinationDnsDomain |
| x-arcsight-event-destination | destination_fqdn | destinationFqdn |
| x-arcsight-event-destination | destination_nt_domain | destinationNtDomain |
| x-arcsight-event-destination | destination_geo | destinationGeo |
| x-arcsight-event-destination | destination_geo_country_code | destinationGeoCountryCode |
| x-arcsight-event-destination | destination_geo_country_name | destinationGeoCountryName |
| x-arcsight-event-destination | destination_geo_location_info | destinationGeoLocationInfo |
| x-arcsight-event-destination | destination_geo_region_code | destinationGeoRegionCode |
| x-arcsight-event-destination | destination_geo_postal_code | destinationGeoPostalCode |
| x-arcsight-event-destination | destination_port | destinationPort |
| <br> | | |
| x-arcsight-event-device | device_product | deviceProduct |
| x-arcsight-event-device | device_vendor | deviceVendor |
| x-arcsight-event-device | device_action | deviceAction |
| x-arcsight-event-device | device_receipt_time | deviceReceiptTime |
| x-arcsight-event-device | device_version | deviceVersion |
| x-arcsight-event-device | device_dns_domain | deviceDnsDomain |
| x-arcsight-event-device | device_domain | deviceDomain |
| x-arcsight-event-device | device_nt_domain | deviceNtDomain |
| x-arcsight-event-device | device_external_id | deviceExternalId |
| x-arcsight-event-device | device_time_zone | dtz |
| x-arcsight-event-device | device_domain_name_ref | deviceHostName |
| <br> | | |
| x-arcsight-event-source | source_ipv6_address_ref | c6a2 |
| x-arcsight-event-source | source_domain_name_ref | sourceHostName |
| x-arcsight-event-source | source_username | sourceUserName |
| x-arcsight-event-source | source_dns_domain | sourceDnsDomain |
| x-arcsight-event-source | source_fqdn | sourceFqdn |
| x-arcsight-event-source | source_nt_domain | sourceNtDomain |
| x-arcsight-event-source | source_geo | sourceGeo |
| x-arcsight-event-source | source_geo_country_code | sourceGeoCountryCode |
| x-arcsight-event-source | source_geo_country_name | sourceGeoCountryName |
| x-arcsight-event-source | source_geo_location_info | sourceGeoLocationInfo |
| x-arcsight-event-source | source_geo_region_code | sourceGeoRegionCode |
| x-arcsight-event-source | source_geo_postal_code | sourceGeoPostalCode |
| x-arcsight-event-source | source_port | sourcePort |
| <br> | | |
| x-arcsight-event-vulnerability | vulnerability | vulnerability |
| x-arcsight-event-vulnerability | vulnerability_external_id | vulnerabilityExternalID |
| x-arcsight-event-vulnerability | vulnerability_id | vulnerabilityID |
| x-arcsight-event-vulnerability | vulnerability_name | vulnerabilityName |
| x-arcsight-event-vulnerability | vulnerability_reference_id | vulnerabilityReferenceID |
| x-arcsight-event-vulnerability | vulnerability_resource | vulnerabilityResource |
| x-arcsight-event-vulnerability | vulnerability_uri | vulnerabilityURI |
| <br> | | |
| x-ibm-finding | time_observed | Event Time |
| x-ibm-finding | dst_ip_ref | destinationAddress |
| x-ibm-finding | src_ip_ref | sourceAddress |
| x-ibm-finding | finding_type | categorySignificance |
| x-ibm-finding | name | name |
| x-ibm-finding | severity | severity |
| x-ibm-finding | dst_device | destinationAssetId |
| x-ibm-finding | dst_geolocation | destinationGeoLocationInfo |
| x-ibm-finding | src_device | sourceAssetId |
| x-ibm-finding | src_geolocation | sourceGeoLocationInfo |
| <br> | | |
| x-oca-asset | extensions.x-device-ext.asset_criticality | assetCriticality |
| x-oca-asset | extensions.x-device-ext.device_severity | deviceSeverity |
| x-oca-asset | hostname | deviceHostName |
| x-oca-asset | ip_refs | deviceAddress |
| x-oca-asset | host_id | deviceAssetId |
| x-oca-asset | hostname | deviceAssetName |
| x-oca-asset | extensions.x-destination-ext.destination_asset_id | destinationAssetId |
| x-oca-asset | extensions.x-destination-ext.destination_asset_name | destinationAssetName |
| x-oca-asset | extensions.x-source-ext.source_asset_id | sourceAssetId |
| x-oca-asset | extensions.x-source-ext.source_asset_name | sourceAssetName |
| x-oca-asset | destination_asset_id | destinationAssetId |
| x-oca-asset | destination_asset_name | destinationAssetName |
| x-oca-asset | source_asset_id | sourceAssetId |
| x-oca-asset | source_asset_name | sourceAssetName |
| <br> | | |
| x-oca-event | category | deviceEventCategory |
| <br> | | |
