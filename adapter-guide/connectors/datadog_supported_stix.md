## Datadog
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| <br> | | |
| domain-name | value | host |
| <br> | | |
| artifact | payload_bin | text |
| <br> | | |
| user-account | user_id | user |
| <br> | | |
| process | command_line | cmdline
| process | pid | pid
| process | creator_user_ref | user
| process | created_time | timestamp
| process | created_time | start
| process | parent_ref | ppid
| process | host | host
| <br> | | |
| x-ibm-finding | start | start |
| x-ibm-finding | end | end |
| x-ibm-finding | time_observed | date_happened |
| <br> | | |
| x-oca-event | code | id |
| x-oca-event | code | id_str |
| x-oca-event | outcome | title |
| x-oca-event | module | source |
| x-oca-event | agent | device_name |
| x-oca-event | created | date_happened |
| x-oca-event | original_ref.payload_bin | text |
| x-oca-event | domain_ref.value | host |
| <br> | | |
| x-datadog-event | priority | priority |
| x-datadog-event | monitor_id | monitor_id |
| x-datadog-event | tags | tags |
| x-datadog-event | is_aggregate | unaggregated |
| x-datadog-event | alert_type | alert_type |
| <br> | | |
