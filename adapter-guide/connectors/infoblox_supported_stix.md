## Infoblox
### TIDE DB
### DNS Event
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| ipv4-addr | value | private_ip |
| ipv4-addr | resolves_to_refs | mac_address |
| ipv4-addr | value | qip |
| ipv4-addr | value | rip |
| <br> | | |
| mac-addr | value | mac_address |
| <br> | | |
| domain-name | value | qname |
| <br> | | |
| user-account | user_id | user |
| <br> | | |
| network-traffic | src_ref | qip |
| network-traffic | extensions.dns-ext.resolved_ip_refs | rip |
| network-traffic | extensions.dns-ext.question.type | qtype |
| network-traffic | extensions.dns-ext.question.domain_ref | qname |
| network-traffic | extensions.dns-ext.answers.data | rdata |
| network-traffic | extensions.dns-ext.response_code | rcode |
| <br> | | |
| x-infoblox-dns-event | severity | severity |
| x-infoblox-dns-event | tclass | tclass |
| x-infoblox-dns-event | threat_indicator | threat_indicator |
| x-infoblox-dns-event | tproperty | tproperty |
| x-infoblox-dns-event | policy_name | policy_name |
| x-infoblox-dns-event | os_version | os_version |
| x-infoblox-dns-event | network | network |
| x-infoblox-dns-event | user_ref | user |
| x-infoblox-dns-event | src_ip_ref | qip |
| x-infoblox-dns-event | category | category |
| x-infoblox-dns-event | confidence | confidence |
| x-infoblox-dns-event | country | country |
| x-infoblox-dns-event | device | device |
| x-infoblox-dns-event | dhcp_fingerprint | dhcp_fingerprint |
| x-infoblox-dns-event | event_time | event_time |
| x-infoblox-dns-event | feed_name | feed_name |
| x-infoblox-dns-event | feed_type | feed_type |

### Dossier
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| user-account | user_id | job.user |
|--|--|--|
| domain-name | value | results[0].data.items[0].Domain |
| domain-name | value | results[0].data.items[0].Hostname |
|--|--|--|
| ipv4-addr | value | results[0].data.items[0].IP |
| ipv6-addr | value | results[0].data.items[0].IP |
|--|--|--|
| x-infoblox-dossier-event | status | status |
| x-infoblox-dossier-event | job_id | job_id |
| x-infoblox-dossier-event | job.id | job.id |
| x-infoblox-dossier-event | job.state | job.state |
| x-infoblox-dossier-event | job.status | job.status |
| x-infoblox-dossier-event | job.create_ts | job.create_ts |
| x-infoblox-dossier-event | job.create_time | job.create_time |
| x-infoblox-dossier-event | job.request_ttl | job.request_ttl |
| x-infoblox-dossier-event | job.result_ttl | job.result_ttl |
| x-infoblox-dossier-event | job.org | job.org |
| x-infoblox-dossier-event | job.user_ref | job.user |
| x-infoblox-dossier-event | job.tasks_tbc | job.tasks_tbc |
| x-infoblox-dossier-event | job.task_refs | tasks |
|--|--|--|
| x-infoblox-dossier-event-task | id | tasks.id |
| x-infoblox-dossier-event-task | state | tasks.state |
| x-infoblox-dossier-event-task | status | tasks.status |
| x-infoblox-dossier-event-task | create_ts | tasks.create_ts |
| x-infoblox-dossier-event-task | create_time | tasks.create_time |
| x-infoblox-dossier-event-task | start_ts | tasks.start_ts |
| x-infoblox-dossier-event-task | start_time | tasks.start_time |
| x-infoblox-dossier-event-task | end_ts | tasks.end_ts |
| x-infoblox-dossier-event-task | end_time | tasks.end_time |
| x-infoblox-dossier-event-task | params | tasks.params |
| x-infoblox-dossier-event-task | options | tasks.options |
| x-infoblox-dossier-event-task | results | tasks.results |
| x-infoblox-dossier-event-task | rl | tasks.rl |
| x-infoblox-dossier-event-task | results_refs | results |
|--|--|--|
| x-infoblox-dossier-event-result-pdns | domain_ref | results[0].data.items[0].Domain |
| x-infoblox-dossier-event-result-pdns | hostname_ref | results[0].data.items[0].Hostname |
| x-infoblox-dossier-event-result-pdns | src_ip_ref | results[0].data.items[0].IP |
| x-infoblox-dossier-event-result-pdns | last_seen | results[0].data.items[0].Last_Seen |
| x-infoblox-dossier-event-result-pdns | name_server | results[0].data.items[0].NameServer |
| x-infoblox-dossier-event-result-pdns | record_type | results[0].data.items[0].Record_Type |
