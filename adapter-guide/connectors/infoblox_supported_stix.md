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