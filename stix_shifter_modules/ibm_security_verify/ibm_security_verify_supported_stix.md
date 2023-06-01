##### Updated on 05/15/23
## IBM Security Verify
### Results STIX Domain Objects
* Identity
* Observed Data
<br>
### Supported STIX Operators
*Comparison AND/OR operators are inside the observation while observation AND/OR operators are between observations (square brackets).*

| STIX Operator | Data Source Operator |
|--|--|
| AND (Comparision) | & |
| = | = |
| AND (Observation) | = |
| IN | = |
| <br> | |
### Searchable STIX objects and properties
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **user-account**:user_id | data.userid |
| **user-account**:account_login | data.username |
| **user-account**:account_type | data.sourcetype |
| **ipv4-addr**:value | data.origin |
| **domain-name**:type | domain-name |
| **domain-name**:value | tenantname |
| **x-oca-event**:action | data.action |
| **x-oca-event**:category | event_type |
| **x-oca-event**:module | servicename |
| **x-oca-event**:outcome | data.result |
| **x-oca-event**:agent | data.sourcetype |
| **x-oca-event**:ip_refs[*].value | ip |
| **x-oca-event**:domain_ref.value | tenantname |
| **x-oca-event**:user_ref | username |
| **x-oca-event**:provider | 'IBM Security Verify Event' |
| **x-oca-event**:extensions.'x-iam-ext'.subcategory | data.subtype |
| **x-oca-event**:extensions.'x-iam-ext'.realm | data.realm |
| **x-oca-event**:extensions.'x-iam-ext'.browser_agent | data.devicetype |
| **x-oca-event**:extensions.'x-iam-ext'.provider_id | data.providerid |
| **x-oca-event**:extensions.'x-iam-ext'.application_id | data.applicationid |
| **x-oca-event**:extensions.'x-iam-ext'.application_type | data.applicationtype |
| **x-oca-event**:extensions.'x-iam-ext'.application_name | data.applicationname |
| **x-oca-event**:extensions.'x-iam-ext'.cause | data.cause |
| **x-oca-event**:extensions.'x-iam-ext'.target | data.target |
| **x-oca-event**:extensions.'x-iam-ext'.performedby_clientname | data.performedby_clientname |
| **x-oca-event**:extensions.'x-iam-ext'.performedby_realm | data.performedby_realm |
| **x-oca-event**:extensions.'x-iam-ext'.performedby_username | data.performedby_username |
| **x-oca-event**:extensions.'x-iam-ext'.targetid | data.targetid |
| **x-oca-event**:extensions.'x-iam-ext'.targetid_realm | data.targetid_realm |
| **x-oca-event**:extensions.'x-iam-ext'.targetid_username | data.targetid_username |
| **x-oca-event**:extensions.'x-iam-ext'.continent_name | geoip.continent_name |
| **x-oca-event**:extensions.'x-iam-ext'.country_iso_code | geoip.country_iso_code |
| **x-oca-event**:extensions.'x-iam-ext'.country_name | geoip.country_name |
| **x-oca-event**:extensions.'x-iam-ext'.city_name | geoip.city_name |
| **x-oca-event**:extensions.'x-iam-ext'.policy_action | data.policy_action |
| **x-oca-event**:extensions.'x-iam-ext'.policy_name | data.policy_name |
| **x-oca-event**:extensions.'x-iam-ext'.rule_name | data.rule_name |
| **x-oca-event**:extensions.'x-iam-ext'.decision_reason | data.decision_reason |
| **x-oca-event**:extensions.'x-iam-ext'.risk_level | data.risk_level |
| **x-oca-event**:extensions.'x-iam-ext'.risk_score | data.risk_score |
| **x-oca-event**:extensions.'x-iam-ext'.deviceid | data.deviceid |
| **x-oca-event**:extensions.'x-iam-ext'.is_device_compliant | data.mdmiscompliant |
| **x-oca-event**:extensions.'x-iam-ext'.is_device_managed | data.mdmismanaged |
| **x-oca-event**:extensions.'x-iam-ext'.mdm_customerid | data.billingid |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| domain-name | value | tenantname |
| <br> | | |
| ipv4-addr | value | ip |
| <br> | | |
| user-account | account_login | username |
| user-account | user_id | userid |
| user-account | account_type | sourcetype |
| <br> | | |
| x-oca-event | user_ref | username |
| x-oca-event | agent | sourcetype |
| x-oca-event | module | servicename |
| x-oca-event | ip_refs | ip |
| x-oca-event | domain_ref | tenantname |
| x-oca-event | outcome | result |
| x-oca-event | extensions.x-iam-ext.subcategory | subtype |
| x-oca-event | extensions.x-iam-ext.cause | cause |
| x-oca-event | action | action |
| x-oca-event | extensions.x-iam-ext.realm | realm |
| x-oca-event | extensions.x-iam-ext.browser_agent | devicetype |
| x-oca-event | extensions.x-iam-ext.application_id | applicationid |
| x-oca-event | extensions.x-iam-ext.application_type | applicationtype |
| x-oca-event | extensions.x-iam-ext.applicationname | applicationname |
| x-oca-event | extensions.x-iam-ext.target | target |
| x-oca-event | category | event_type |
| x-oca-event | provider | event_type |
| x-oca-event | created | time |
| x-oca-event | extensions.x-iam-ext.performedby_username | performedby_username |
| x-oca-event | extensions.x-iam-ext.deleted | deleted |
| x-oca-event | extensions.x-iam-ext.performedby_clientname | performedby_clientname |
| x-oca-event | extensions.x-iam-ext.performedby_realm | performedby_realm |
| x-oca-event | extensions.x-iam-ext.targetid | targetid |
| x-oca-event | extensions.x-iam-ext.targetid_realm | targetid_realm |
| x-oca-event | extensions.x-iam-ext.taregetid_username | targetid_username |
| x-oca-event | extensions.x-iam-ext.continent_name | continent_name |
| x-oca-event | extensions.x-iam-ext.city_name | city_name |
| x-oca-event | extensions.x-iam-ext.country_iso_code | country_iso_code |
| x-oca-event | extensions.x-iam-ext.country_name | country_name |
| x-oca-event | extensions.x-iam-ext.provider_id | providerid |
| x-oca-event | extensions.x-iam-ext.rule_name | rule_name |
| x-oca-event | extensions.x-iam-ext.policy_name | policy_name |
| x-oca-event | extensions.x-iam-ext.decision_reason | decision_reason |
| x-oca-event | extensions.x-iam-ext.policy_action | policy_action |
| x-oca-event | extensions.x-iam-ext.risk_level | risk_level |
| x-oca-event | extensions.x-iam-ext.risk_score | risk_score |
| x-oca-event | extensions.x-iam-ext.deviceid | deviceid |
| x-oca-event | extensions.x-iam-ext.is_device_compliant | mdmiscompliant |
| x-oca-event | extensions.x-iam-ext.is_device_managed | mdmismanaged |
| x-oca-event | extensions.x-iam-ext.mdm_customerid | billingid |
| x-oca-event | extensions.x-iam-ext.location_lat | lat |
| x-oca-event | extensions.x-iam-ext.location_lon | lon |
| x-oca-event | extensions.x-iam-ext.add | add |
| <br> | | |
