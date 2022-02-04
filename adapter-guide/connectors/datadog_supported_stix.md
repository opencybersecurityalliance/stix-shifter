##### Updated on 02/04/22
## Datadog
### Supported STIX Operators
| STIX Operator | Data Source Operator |
|--|--|
| AND | OR |
| OR | OR |
| = | : |
| IN | : |
| <br> | |
### Supported STIX Objects and Properties
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
