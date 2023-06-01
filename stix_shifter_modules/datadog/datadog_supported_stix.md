##### Updated on 05/15/23
## Datadog
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
| = | : |
| IN | : |
| OR (Observation) | OR |
| AND (Observation) | OR |
| <br> | |
### Searchable STIX objects and properties for Events dialect
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **domain-name**:value | host |
| **artifact**:payload_bin | text |
| **x-datadog-event**:priority | priority |
| **x-datadog-event**:monitor_id | monitor_id |
| **x-datadog-event**:tags | tags |
| **x-datadog-event**:is_aggregate | unaggregated |
| **x-datadog-event**:alert_type | alert_type |
| **x-ibm-finding**:start | start |
| **x-ibm-finding**:end | end |
| **x-ibm-finding**:time_observed | date_happened |
| **x-oca-event**:code | id, id_str |
| **x-oca-event**:outcome | title |
| **x-oca-event**:module | source |
| **x-oca-event**:agent | device_name |
| **x-oca-event**:created | date_happened |
| **x-oca-event**:original_ref.payload_bin | text |
| **x-oca-event**:domain_ref.value | host |
| <br> | |
### Searchable STIX objects and properties for Processes dialect
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **domain-name**:value | host |
| **artifact**:payload_bin | text |
| **user-account**:user_id | user |
| **process**:command_line | cmdline |
| **process**:pid | pid |
| **process**:creator_user_ref | user |
| **process**:created_time | timestamp, start |
| **process**:parent_ref | ppid |
| **x-datadog-event**:priority | priority |
| **x-datadog-event**:monitor_id | monitor_id |
| **x-datadog-event**:tags | tags |
| **x-datadog-event**:is_aggregate | unaggregated |
| **x-datadog-event**:alert_type | alert_type |
| **x-ibm-finding**:start | start |
| **x-ibm-finding**:end | end |
| **x-ibm-finding**:time_observed | date_happened |
| **x-oca-event**:code | id, id_str |
| **x-oca-event**:outcome | title |
| **x-oca-event**:module | source |
| **x-oca-event**:agent | device_name |
| **x-oca-event**:created | date_happened |
| **x-oca-event**:original_ref.payload_bin | text |
| **x-oca-event**:domain_ref.value | host |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| artifact | payload_bin | text |
| <br> | | |
| domain-name | value | host |
| <br> | | |
| process | created_time | start |
| process | command_line | cmdline |
| process | pid | pid |
| process | created_time | timestamp |
| process | creator_user_ref | user |
| <br> | | |
| user-account | user_id | user |
| <br> | | |
| x-datadog-event | priority | priority |
| x-datadog-event | monitor_id | monitor_id |
| x-datadog-event | tags | tags |
| x-datadog-event | unaggregated | is_aggregate |
| x-datadog-event | alert_type | alert_type |
| <br> | | |
| x-ibm-finding | time_observed | date_happened |
| x-ibm-finding | start | start |
| x-ibm-finding | end | end |
| <br> | | |
| x-oca-event | domain_ref | host |
| x-oca-event | original_ref | text |
| x-oca-event | module | source |
| x-oca-event | code | id |
| x-oca-event | code | id_str |
| x-oca-event | outcome | title |
| x-oca-event | agent | device_name |
| x-oca-event | created | date_happened |
| <br> | | |
