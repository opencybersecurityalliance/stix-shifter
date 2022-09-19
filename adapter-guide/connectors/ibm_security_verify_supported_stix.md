##### Updated on 09/09/22
## IBM Security Verify
### Supported STIX Operators
| STIX Operator | Data Source Operator |
|--|--|
| AND | = |
| = | = |
| IN | = |
| <br> | |
### Supported STIX Objects and Properties
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| domain-name | value | tenantname |
| <br> | | |
| ipv4-addr | value | ip |
| <br> | | |
| user-account | user_id | username |
| user-account | account_login | username |
| user-account | account_type | username |
| user-account | user_id | userid |
| <br> | | |
| x-oca-event | user_ref | username |
| x-oca-event | module | servicename |
| x-oca-event | agent | sourcetype |
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
| <br> | | |
