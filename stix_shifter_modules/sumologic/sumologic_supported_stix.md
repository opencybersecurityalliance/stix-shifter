##### Updated on 05/15/23
## Sumo Logic
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
| IN | OR |
| OR (Observation) | OR |
| AND (Observation) | AND |
| <br> | |
### Searchable STIX objects and properties
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **artifact**:payload_bin | _raw |
| **domain-name**:value | _sourcehost |
| **x-ibm-finding**:event_count | _messagecount |
| **x-ibm-finding**:time_observed | _messagetime |
| **x-ibm-finding**:src_device | _collector |
| **x-ibm-finding**:start | _receipttime |
| **x-oca-event**:code | _messageid |
| **x-oca-event**:created | _messagetime |
| **x-oca-event**:agent | _collector |
| **x-oca-event**:module | _source |
| **x-oca-event**:provider | _sourcecategory |
| **x-oca-event**:original_ref.payload_bin | _raw |
| **x-oca-event**:domain_ref.value | _sourcehost |
| **x-oca-event**:user_ref.account_login | _useremail |
| **x-sumologic-source**:collectorid | _collectorid |
| **x-sumologic-source**:sourcename | _sourcename |
| **user-account**:user_id | id |
| **user-account**:account_login | email |
| **user-account**:display_name | displayName |
| **user-account**:account_created | createdAt |
| **user-account**:account_last_login | lastLoginTimestamp |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| artifact | payload_bin | _raw |
| <br> | | |
| domain-name | value | _sourcehost |
| <br> | | |
| user-account | user_id | id |
| user-account | account_login | email |
| user-account | display_name | displayName |
| user-account | account_created | createdAt |
| user-account | account_last_login | lastLoginTimestamp |
| <br> | | |
| x-ibm-finding | event_count | _messagecount |
| x-ibm-finding | time_observed | _messagetime |
| x-ibm-finding | src_device | _collector |
| x-ibm-finding | start | _receipttime |
| <br> | | |
| x-oca-event | original_ref | _raw |
| x-oca-event | domain_ref | _sourcehost |
| x-oca-event | created | _messagetime |
| x-oca-event | code | _messageid |
| x-oca-event | agent | _collector |
| x-oca-event | module | _source |
| x-oca-event | provider | _sourcecategory |
| x-oca-event | user_ref | email |
| <br> | | |
| x-sumologic-source | collectorid | _collectorid |
| x-sumologic-source | sourcename | _sourcename |
| <br> | | |
