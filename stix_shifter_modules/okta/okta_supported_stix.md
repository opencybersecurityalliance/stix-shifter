##### Updated on 04/18/23
## Okta
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
| LIKE | co |
| IN | eq |
| MATCHES | co |
| OR (Observation) | or |
| AND (Observation) | or |
| <br> | |
### Searchable STIX objects and properties
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **ipv4-addr**:value | request.ipChain.ip |
| **autonomous-system**:number | securityContext.asNumber |
| **autonomous-system**:name | securityContext.asOrg |
| **autonomous-system**:x_isp | securityContext.isp |
| **autonomous-system**:x_domain_ref.name | securityContext.domain |
| **domain-name**:value | securityContext.domain |
| **user-account**:user_id | actor.id |
| **user-account**:display_name | actor.displayName |
| **user-account**:account_login | actor.alternateId |
| **user-account**:x_actor_type | actor.type |
| **x-okta-target**:target_id | target.id |
| **x-okta-target**:display_name | target.displayName |
| **x-okta-target**:alternate_id | target.alternateId |
| **x-okta-target**:target_type | target.type |
| **software**:name | client.userAgent.browser |
| **software**:x_raw_user_agent | client.userAgent.rawUserAgent |
| **software**:x_client_os | client.userAgent.os |
| **x-okta-client**:client_id | client.id |
| **x-okta-client**:client_ip | client.ipAddress |
| **x-okta-client**:device | client.device |
| **x-okta-client**:network_zone_name | client.zone |
| **x-okta-client**:software_ref.name | client.userAgent.browser |
| **x-okta-client**:autonomous_system_ref.number | securityContext.asNumber |
| **x-okta-client**:geolocation_country | client.geographicalContext.country |
| **x-okta-client**:geolocation_city | client.geographicalContext.city |
| **x-okta-client**:geolocation_state | client.geographicalContext.state |
| **x-okta-client**:geolocation_postalcode | client.geographicalContext.postalCode |
| **x-okta-authentication-context**:authentication_provider | authenticationContext.authenticationProvider |
| **x-okta-authentication-context**:credential_provider | authenticationContext.credentialProvider |
| **x-okta-authentication-context**:credential_type | authenticationContext.credentialType |
| **x-okta-authentication-context**:issuer_id | authenticationContext.issuer.id |
| **x-okta-authentication-context**:issuer_type | authenticationContext.issuer.type |
| **x-okta-authentication-context**:session_id | authenticationContext.externalSessionId |
| **x-okta-authentication-context**:interface | authenticationContext.interface |
| **x-oca-event**:action | eventType |
| **x-oca-event**:category[*] | transaction.type |
| **x-oca-event**:outcome | outcome.result |
| **x-oca-event**:ip_refs[*].value | request.ipChain.ip |
| **x-oca-event**:x_event_unique_id | uuid |
| **x-oca-event**:x_severity | severity |
| **x-oca-event**:x_event_description | displayMessage |
| **x-oca-event**:x_transaction_id | transaction.id |
| **x-oca-event**:x_request_api_token_id | transaction.detail.requestApiTokenId |
| **x-oca-event**:x_legacy_event_type | legacyEventType |
| **x-oca-event**:x_outcome_reason | outcome.reason |
| **x-oca-event**:x_actor_ref.account_login | actor.alternateId |
| **x-oca-event**:x_actor_ref.user_id | actor.id |
| **x-oca-event**:x_client_ref.client_ip | client.ipAddress |
| **x-oca-event**:x_authentication_context_ref.session_id | authenticationContext.externalSessionId |
| **x-oca-event**:x_target_refs[*].target_type | target.type |
| **x-oca-event**:x_target_refs[*].display_name | target.displayName |
| **x-oca-event**:x_target_refs[*].target_id | target.id |
| **x-oca-event**:x_client_ref.id | client.id |
| **x-okta-debug-context**:behaviors | debugContext.debugData.behaviors |
| **x-okta-debug-context**:request_uri | debugContext.debugData.requestUri |
| **x-okta-debug-context**:request_id | debugContext.debugData.requestId |
| **x-okta-debug-context**:risk | debugContext.debugData.risk |
| **x-okta-debug-context**:sign_on_mode | debugContext.debugData.signOnMode |
| **x-okta-debug-context**:agent_name | debugContext.debugData.agentName |
| **x-okta-debug-context**:threat_suspected | debugContext.debugData.threatSuspected |
| **x-okta-debug-context**:dt_hash | debugContext.debugData.dtHash |
| **x-okta-debug-context**:device_fingerprint | debugContext.debugData.deviceFingerprint |
| **x-okta-debug-context**:report_email_category | debugContext.debugData.category |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| autonomous-system | number | asNumber |
| autonomous-system | name | asOrg |
| autonomous-system | x_isp | isp |
| autonomous-system | x_domain_ref | domain |
| <br> | | |
| domain-name | value | domain |
| <br> | | |
| ipv4-addr | value | ip |
| ipv4-addr | value | ipAddress |
| <br> | | |
| software | x_raw_user_agent | rawUserAgent |
| software | x_client_os | os |
| software | name | browser |
| <br> | | |
| user-account | user_id | id |
| user-account | display_name | displayName |
| user-account | account_login | alternateId |
| user-account | x_actor_type | type |
| user-account | x_detail_entry | detailEntry |
| <br> | | |
| x-oca-event | action | eventType |
| x-oca-event | x_event_unique_id | uuid |
| x-oca-event | outcome | result |
| x-oca-event | x_outcome_reason | reason |
| x-oca-event | x_legacy_event_type | legacyEventType |
| x-oca-event | x_event_description | displayMessage |
| x-oca-event | x_severity | severity |
| x-oca-event | ip_refs | ip |
| x-oca-event | x_actor_ref | id |
| x-oca-event | x_target_refs | groupReference |
| x-oca-event | x_client_ref | id |
| x-oca-event | ip_refs | ipAddress |
| x-oca-event | x_client_ref | device |
| x-oca-event | x_client_ref | country |
| x-oca-event | x_transaction_id | id |
| x-oca-event | category | type |
| x-oca-event | x_request_api_token_id | requestApiTokenId |
| x-oca-event | x_debug_ref | groupReference |
| x-oca-event | x_authentication_context_ref | externalSessionId |
| <br> | | |
| x-okta-authentication-context | authentication_provider | authenticationProvider |
| x-okta-authentication-context | credential_provider | credentialProvider |
| x-okta-authentication-context | credential_type | credentialType |
| x-okta-authentication-context | session_id | externalSessionId |
| x-okta-authentication-context | interface | interface |
| x-okta-authentication-context | issuer_id | id |
| x-okta-authentication-context | issuer_type | type |
| <br> | | |
| x-okta-client | autonomous_system_ref | asNumber |
| x-okta-client | client_id | id |
| x-okta-client | ip_ref | ipAddress |
| x-okta-client | software_ref | browser |
| x-okta-client | device | device |
| x-okta-client | geolocation_country | country |
| x-okta-client | geolocation_city | city |
| x-okta-client | geolocation_state | state |
| x-okta-client | geolocation_postalcode | postalCode |
| x-okta-client | geolocation_coordinates | geolocation |
| x-okta-client | network_zone_name | zone |
| <br> | | |
| x-okta-debug-context | debug_data | debugData |
| <br> | | |
| x-okta-target | target_id | id |
| x-okta-target | display_name | displayName |
| x-okta-target | alternate_id | alternateId |
| x-okta-target | target_type | type |
| x-okta-target | detail_entry | detailEntry |
| <br> | | |
