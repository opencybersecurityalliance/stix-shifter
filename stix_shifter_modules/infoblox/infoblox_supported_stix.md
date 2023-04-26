## Infoblox
### TIDE DB
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| domain-name | value | domain |
|--|--|--|
| email-addr | value | email |
|--|--|--|
| ipv4-addr | value | ip |
| ipv6-addr | value | ip |
|--|--|--|
| x-infoblox-threat | id | id |
| x-infoblox-threat | threat_class | class |
| x-infoblox-threat | x_infoblox_confidence | confidence |
| x-infoblox-threat | dga | dga |
| x-infoblox-threat | domain_ref | domain |
| x-infoblox-threat | email_ref | email |
| x-infoblox-threat | ip_ref | ip |
| x-infoblox-threat | expiration | expiration |
| x-infoblox-threat | hash | hash |
| x-infoblox-threat | host_name | host |
| x-infoblox-threat | imported | imported |
| x-infoblox-threat | origin | origin |
| x-infoblox-threat | profile | profile |
| x-infoblox-threat | property | property |
| x-infoblox-threat | target | target |
| x-infoblox-threat | threat_level | threat_level |
| x-infoblox-threat | top_level_domain | tld |
| x-infoblox-threat | threat_type | type |
| x-infoblox-threat | active | up |
| x-infoblox-threat | url | url |


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
| network-traffic | extensions.dns-ext.type | qtype |
| network-traffic | extensions.dns-ext.question.domain_ref | qname |
| network-traffic | extensions.dns-ext.answers.data | rdata |
| network-traffic | extensions.dns-ext.response_code | rcode |
| <br> | | |
| x-infoblox-dns-event | x_infoblox_severity | severity |
| x-infoblox-dns-event | threat_class | tclass |
| x-infoblox-dns-event | threat_indicator | threat_indicator |
| x-infoblox-dns-event | threat_property | tproperty |
| x-infoblox-dns-event | policy_name | policy_name |
| x-infoblox-dns-event | os_version | os_version |
| x-infoblox-dns-event | network | network |
| x-infoblox-dns-event | user_ref | user |
| x-infoblox-dns-event | src_ip_ref | qip |
| x-infoblox-dns-event | category | category |
| x-infoblox-dns-event | x_infoblox_confidence | confidence |
| x-infoblox-dns-event | country | country |
| x-infoblox-dns-event | device | device |
| x-infoblox-dns-event | dhcp_fingerprint | dhcp_fingerprint |
| x-infoblox-dns-event | feed_name | feed_name |
| x-infoblox-dns-event | feed_type | feed_type |

### Dossier
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| domain-name | value | results[0].data.items[0].Domain |
| domain-name | value | results[0].data.items[0].Hostname |
|--|--|--|
| ipv4-addr | value | results[0].data.items[0].IP |
| ipv6-addr | value | results[0].data.items[0].IP |
|--|--|--|
| x-infoblox-dossier-event-result-pdns | domain_ref | results[0].data.items[0].Domain |
| x-infoblox-dossier-event-result-pdns | hostname_ref | results[0].data.items[0].Hostname |
| x-infoblox-dossier-event-result-pdns | ip_ref | results[0].data.items[0].IP |
| x-infoblox-dossier-event-result-pdns | last_seen | results[0].data.items[0].Last_Seen |
| x-infoblox-dossier-event-result-pdns | name_server | results[0].data.items[0].NameServer |
| x-infoblox-dossier-event-result-pdns | record_type | results[0].data.items[0].Record_Type |
