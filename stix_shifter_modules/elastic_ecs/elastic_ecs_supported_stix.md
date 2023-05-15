##### Updated on 05/15/23
## Elasticsearch ECS
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
| > | :> |
| >= | :>= |
| < | :< |
| <= | :<= |
| = | : |
| != | NOT |
| LIKE | : |
| IN | : |
| MATCHES | : |
| ISSUBSET | : |
| ISSUPERSET | : |
| OR (Observation) | OR |
| AND (Observation) | OR |
| <br> | |
### Searchable STIX objects and properties
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **ipv4-addr**:value | source.ip, destination.ip, client.ip, server.ip, host.ip, dns.resolved_ip, source.nat.ip, destination.nat.ip, client.nat.ip, server.nat.ip |
| **ipv6-addr**:value | source.ip, destination.ip, client.ip, server.ip, host.ip, dns.resolved_ip, source.nat.ip, destination.nat.ip, client.nat.ip, server.nat.ip |
| **mac-addr**:value | source.mac, destination.mac, client.mac, server.mac, host.mac |
| **network-traffic**:src_port | source.port, client.port, source.nat.port, client.nat.port |
| **network-traffic**:dst_port | destination.port, server.port, destination.nat.port, server.nat.port |
| **network-traffic**:protocols[*] | network.transport, network.type, network.protocol |
| **network-traffic**:src_ref.value | source.ip, client.ip |
| **network-traffic**:dst_ref.value | destination.ip, server.ip |
| **network-traffic**:src_byte_count | source.bytes, client.bytes |
| **network-traffic**:dst_byte_count | destination.bytes, server.bytes |
| **network-traffic**:src_packets | source.packets, client.packets |
| **network-traffic**:dst_packets | destination.packets, server.packets |
| **network-traffic**:x_vlan.id | network.vlan.id |
| **network-traffic**:x_vlan.name | network.vlan.name |
| **network-traffic**:x_vlan.inner.id | network.inner.vlan.id |
| **network-traffic**:x_vlan.inner.name | network.inner.vlan.name |
| **network-traffic**:x_name | network.name |
| **network-traffic**:x_application | network.application |
| **network-traffic**:x_direction | network.direction |
| **network-traffic**:x_forwarded_ip | network.forwarded_ip |
| **network-traffic**:x_community_id | network.community_id |
| **artifact**:payload_bin | event.original |
| **file**:name | file.name, dll.name, file.path, process.name, process.executable, process.parent.name, process.parent.executable |
| **file**:created | file.created, file.ctime |
| **file**:modified | file.mtime |
| **file**:accessed | file.accessed |
| **file**:size | file.size |
| **file**:mime_type | file.mime_type |
| **file**:hashes.MD5 | file.hash.md5 |
| **file**:hashes.'SHA-1' | file.hash.sha1 |
| **file**:hashes.'SHA-256' | file.hash.sha256 |
| **file**:hashes.'SHA-512' | file.hash.sha512 |
| **file**:parent_directory_ref.path | file.directory |
| **file**:x_attributes | file.attributes |
| **file**:x_extension | file.extension |
| **file**:x_path | file.path, dll.path |
| **file**:x_target_path | file.target_path |
| **file**:x_type | file.type |
| **file**:x_unix.device | file.device |
| **file**:x_unix.group_id | file.gid |
| **file**:x_unix.group | file.group |
| **file**:x_unix.inode | file.inode |
| **file**:x_unix.mode | file.mode |
| **file**:x_owner_ref.user_id | file.uid |
| **file**:x_owner_ref.account_login | file.owner |
| **file**:x_win_drive_letter | file.drive_letter |
| **file**:x_software_ref.name | file.pe.original_file_name, dll.pe.original_file_name |
| **file**:x_software_ref.vendor | file.pe.company, dll.pe.company |
| **file**:x_software_ref.version | file.pe.file_version, dll.pe.file_version |
| **file**:x_code_signature.exists | file.code_signature.exists, dll.code_signature.exists |
| **file**:x_code_signature.status | file.code_signature.status, dll.code_signature.status |
| **file**:x_code_signature.subject_name | file.code_signature.subject_name, dll.code_signature.subject_name |
| **file**:x_code_signature.trusted | file.code_signature.trusted, dll.code_signature.trusted |
| **file**:x_code_signature.valid | file.code_signature.valid, dll.code_signature.valid |
| **directory**:path | file.directory, file.path |
| **user-account**:user_id | user.name, user.id |
| **user-account**:account_login | user.name |
| **user-account**:display_name | user.full_name |
| **user-account**:x_domain | user.domain |
| **user-account**:x_hash | user.hash |
| **user-account**:x_group.domain | user.group.domain |
| **user-account**:x_group.id | user.group.id |
| **user-account**:x_group.name | user.group.name |
| **process**:command_line | process.command_line, powershell.command.value |
| **process**:created | process.start |
| **process**:cwd | process.working_directory |
| **process**:pid | process.pid, process.ppid, process.parent.pid, process.parent.ppid |
| **process**:name | process.name, process.parent.name |
| **process**:creator_user_ref.user_id | user.name |
| **process**:parent_ref.pid | process.ppid, process.parent.ppid |
| **process**:parent_ref.name | process.parent.name |
| **process**:parent_ref.x_exit_code | process.parent.exit_code |
| **process**:parent_ref.pgid | process.parent.pgid |
| **process**:parent_ref.x_window_title | process.parent.title |
| **process**:parent_ref.x_thread_id | process.parent.thread.id |
| **process**:parent_ref.x_uptime | process.parent.uptime |
| **process**:parent_ref.cwd | process.parent.working_directory |
| **process**:parent_ref.binary_ref.path | process.parent.executable |
| **process**:parent_ref.binary_ref.parent_directory_ref.path | process.parent.executable |
| **process**:binary_ref.name | process.executable, process.parent.executable |
| **process**:binary_ref.parent_directory_ref.path | process.executable, process.parent.executable |
| **process**:binary_ref.hashes.MD5 | process.hash.md5 |
| **process**:binary_ref.hashes.'SHA-1' | process.hash.sha1 |
| **process**:binary_ref.hashes.'SHA-256' | process.hash.sha256 |
| **process**:binary_ref.hashes.'SHA-512' | process.hash.sha512 |
| **process**:x_window_title | process.title |
| **process**:x_exit_code | process.exit_code |
| **process**:x_thread_id | process.thread.id |
| **process**:x_ttp_tags | tags |
| **process**:x_unique_id | process.entity_id, process.parent.entity_id |
| **process**:x_uptime | process.uptime |
| **url**:value | url.original |
| **domain-name**:value | url.domain, dns.question.name, dns.question.registered_domain, host.hostname, source.domain, destination.domain, server.domain, client.domain, source.registered_domain, destination.registered_domain, server.registered_domain, client.registered_domain, source.top_level_domain, destination.top_level_domain, server.top_level_domain, client.top_level_domain |
| **windows-registry-key**:key | registry.key |
| **software**:name | agent.name, process.pe.original_file_name, file.pe.original_file_name, dll.pe.original_file_name |
| **software**:vendor | process.pe.company, file.pe.company, dll.pe.company |
| **software**:version | process.pe.file_version, file.pe.file_version, dll.pe.file_version |
| **software**:x_product | process.pe.product, file.pe.product, dll.pe.product |
| **software**:x_description | process.pe.description, file.pe.description, dll.pe.description |
| **autonomous-system**:value | client.as.organization.name, server.as.organization.name, source.as.organization.name, destination.as.organization.name |
| **autonomous-system**:number | client.as.number, server.as.number, source.as.number, destination.as.number |
| **email-addr**:name | user.email |
| **x-oca-event**:action | event.action |
| **x-oca-event**:id | event.id |
| **x-oca-event**:category | event.category |
| **x-oca-event**:code | event.code |
| **x-oca-event**:created | event.created |
| **x-oca-event**:dataset | event.dataset |
| **x-oca-event**:duration | event.duration |
| **x-oca-event**:end | event.end |
| **x-oca-event**:hash | event.hash |
| **x-oca-event**:ingested | event.ingested |
| **x-oca-event**:kind | event.kind |
| **x-oca-event**:module | event.module |
| **x-oca-event**:outcome | event.outcome |
| **x-oca-event**:provider | event.provider |
| **x-oca-event**:risk_score | event.risk_score |
| **x-oca-event**:risk_score_norm | event.risk_score_norm |
| **x-oca-event**:sequence | event.sequence |
| **x-oca-event**:severity | event.severity |
| **x-oca-event**:start | event.start |
| **x-oca-event**:timezone | event.timezone |
| **x-oca-event**:type | event.type |
| **x-oca-event**:url | event.url |
| **x-oca-event**:original | message, powershell.file.script_block_text |
| **x-oca-event**:process_ref.pid | process.pid |
| **x-oca-event**:process_ref.name | process.name |
| **x-oca-event**:process_ref.command_line | process.command_line, powershell.command.value |
| **x-oca-event**:process_ref.binary_ref.name | file.name, process.executable |
| **x-oca-event**:process_ref.parent_ref.pid | process.ppid, process.parent.ppid |
| **x-oca-event**:process_ref.parent_ref.command_line | process.parent.command_line |
| **x-oca-event**:process_ref.creator_user_ref.user_id | user.name |
| **x-oca-event**:parent_process_ref.pid | process.ppid, process.parent.ppid |
| **x-oca-event**:parent_process_ref.command_line | process.parent.command_line |
| **x-oca-event**:domain_ref.value | url.domain, dns.question.name, dns.question.registered_domain, host.hostname |
| **x-oca-event**:file_ref.name | file.name |
| **x-oca-event**:host_ref.hostname | host.hostname |
| **x-oca-event**:host_ref.name | host.name |
| **x-oca-event**:registry_ref.key | registry.key, registry.path |
| **x-ecs-cloud**:account.id | cloud.account.id |
| **x-ecs-cloud**:availability_zone | cloud.availability_zone |
| **x-ecs-cloud**:instance.id | cloud.instance.id |
| **x-ecs-cloud**:instance.name | cloud.instance.name |
| **x-ecs-cloud**:machine.type | cloud.machine.type |
| **x-ecs-cloud**:provider | cloud.provider |
| **x-ecs-cloud**:region | cloud.region |
| **x-ecs-dns**:answers_class | dns.answers.class |
| **x-ecs-dns**:answers_data | dns.answers.data |
| **x-ecs-dns**:answers_name | dns.answers.name |
| **x-ecs-dns**:answers_ttl | dns.answers.ttl |
| **x-ecs-dns**:answers_type | dns.answers.type |
| **x-ecs-dns**:header_flags | dns.header_flags |
| **x-ecs-dns**:id | dns.id |
| **x-ecs-dns**:op_code | dns.op_code |
| **x-ecs-dns**:question_class | dns.question.class |
| **x-ecs-dns**:question_name | dns.question.name |
| **x-ecs-dns**:question_registered_domain | dns.question.registered_domain |
| **x-ecs-dns**:question_subdomain | dns.question.subdomain |
| **x-ecs-dns**:question_top_level_domain | dns.question.top_level_domain |
| **x-ecs-dns**:question_type | dns.question.type |
| **x-ecs-dns**:resolved_ip | dns.resolved_ip |
| **x-ecs-dns**:response_code | dns.response_code |
| **x-ecs-dns**:type | dns.type |
| **x-ecs**:version | ecs.version |
| **x-ecs-error**:code | error.code |
| **x-ecs-error**:id | error.id |
| **x-ecs-error**:message | error.message |
| **x-ecs-error**:stack_trace | error.stack_trace |
| **x-ecs-error**:type | error.type |
| **x-ecs-group**:domain | group.domain |
| **x-ecs-group**:id | group.id |
| **x-ecs-group**:name | group.name |
| **x-oca-asset**:architecture | host.architecture |
| **x-oca-asset**:domain | host.domain |
| **x-oca-asset**:hostname | host.hostname, observer.hostname |
| **x-oca-asset**:id | host.id, observer.serial_number |
| **x-oca-asset**:ip | host.ip, observer.ip |
| **x-oca-asset**:mac | host.mac, observer.mac |
| **x-oca-asset**:name | host.name, observer.name |
| **x-oca-asset**:type | host.type, observer.type |
| **x-oca-asset**:ingress.zone | observer.ingress.zone |
| **x-oca-asset**:ingress.interface.alias | observer.ingress.interface.alias |
| **x-oca-asset**:ingress.interface.id | observer.ingress.interface.id |
| **x-oca-asset**:ingress.interface.name | observer.ingress.interface.name |
| **x-oca-asset**:egress.zone | observer.egress.zone |
| **x-oca-asset**:egress.interface.alias | observer.egress.interface.alias |
| **x-oca-asset**:egress.interface.id | observer.egress.interface.id |
| **x-oca-asset**:egress.interface.name | observer.egress.interface.name |
| **x-oca-asset**:uptime | host.uptime |
| **x-oca-asset**:os_ref.name | host.os.name, observer.os.name, observer.product |
| **x-oca-asset**:os_ref.vendor | host.os.platform, observer.os.platform, observer.vendor |
| **x-oca-asset**:os_ref.version | host.os.version, observer.os.version, observer.version |
| **x-oca-asset**:container.id | container.id |
| **x-oca-asset**:container.image.name | container.image.name |
| **x-oca-asset**:container.image.tag | container.image.tag |
| **x-oca-asset**:container.labels | container.labels |
| **x-oca-asset**:container.name | container.name |
| **x-oca-asset**:container.runtime | container.runtime |
| **x-oca-geo**:city_name | server.geo.city_name, client.geo.city_name, source.geo.city_name, destination.geo.city_name |
| **x-oca-geo**:continent_name | server.geo.continent_name, client.geo.continent_name, source.geo.continent_name, destination.geo.continent_name |
| **x-oca-geo**:country_iso_code | server.geo.country_iso_code, client.geo.country_iso_code, source.geo.country_iso_code, destination.geo.country_iso_code |
| **x-oca-geo**:country_name | server.geo.country_name, client.geo.country_name, source.geo.country_name, destination.geo.country_name |
| **x-oca-geo**:location | server.geo.location, client.geo.location, source.geo.location, destination.geo.location |
| **x-oca-geo**:name | server.geo.name, client.geo.name, source.geo.name, destination.geo.name |
| **x-oca-geo**:region_iso_code | server.geo.region_iso_code, client.geo.region_iso_code, source.geo.region_iso_code, destination.geo.region_iso_code |
| **x-oca-geo**:region_name | server.geo.region_name, client.geo.region_name, source.geo.region_name, destination.geo.region_name |
| **x-ecs-http**:request_body_bytes | http.request.body.bytes |
| **x-ecs-http**:request_body_content | http.request.body.content |
| **x-ecs-http**:request_bytes | http.request.bytes |
| **x-ecs-http**:request_method | http.request.method |
| **x-ecs-http**:request_referrer | http.request.referrer |
| **x-ecs-http**:response_body_bytes | http.response.body.bytes |
| **x-ecs-http**:response_body_content | http.response.body.content |
| **x-ecs-http**:response_bytes | http.response.bytes |
| **x-ecs-http**:response_status_code | http.response.method |
| **x-ecs-http**:version | http.version |
| **x-ecs-log**:level | log.level |
| **x-ecs-log**:logger | log.logger |
| **x-ecs-log**:origin_file_line | log.origin.file.line |
| **x-ecs-log**:origin_file_name | log.origin.file.name |
| **x-ecs-log**:origin_function | log.origin.function |
| **x-ecs-log**:original | log.original |
| **x-ecs-log**:syslog_facility_code | log.syslog.facility.code |
| **x-ecs-log**:syslog_facility_name | log.syslog.facility.name |
| **x-ecs-log**:syslog_priority | log.syslog.priority |
| **x-ecs-log**:severity_syslog_code | log.syslog.severity.code |
| **x-ecs-log**:severity_syslog_name | log.syslog.severity.name |
| **x-ecs-organization**:id | organization.id |
| **x-ecs-organization**:name | organization.name |
| **x-ecs-pe**:company | dll.pe.company, process.pe.company, file.pe.company |
| **x-ecs-pe**:description | dll.pe.description, process.pe.description, file.pe.description |
| **x-ecs-pe**:file_version | dll.pe.file_version, process.pe.file_version, file.pe.file_version |
| **x-ecs-pe**:original_file_name | dll.pe.original_file_name, process.pe.original_file_name, file.pe.original_file_name |
| **x-ecs-pe**:product | dll.pe.product, process.pe.product, file.pe.product |
| **x-ecs-related**:hash | related.hash |
| **x-ecs-related**:ip | related.ip |
| **x-ecs-related**:user | related.user |
| **x-ecs-rule**:author | rule.author |
| **x-ecs-rule**:category | rule.category |
| **x-ecs-rule**:description | rule.description |
| **x-ecs-rule**:id | rule.id |
| **x-ecs-rule**:license | rule.license |
| **x-ecs-rule**:name | rule.name |
| **x-ecs-rule**:reference | rule.reference |
| **x-ecs-rule**:ruleset | rule.ruleset |
| **x-ecs-rule**:uuid | rule.uuid |
| **x-ecs-rule**:version | rule.version |
| **x-ecs-service**:id | service.id |
| **x-ecs-service**:name | service.name |
| **x-ecs-service**:state | service.state |
| **x-ecs-service**:type | service.type |
| **x-ecs-service**:version | service.version |
| **x-ecs-threat**:framework | threat.framework |
| **x-ecs-threat**:tactic_id | threat.tactic.id |
| **x-ecs-threat**:tactic_name | threat.tactic.name |
| **x-ecs-threat**:tactic_reference | threat.tactic.reference |
| **x-ecs-threat**:technique_id | threat.technique.id |
| **x-ecs-threat**:technique_name | threat.technique.name |
| **x-ecs-threat**:technique_reference | threat.technique.reference |
| **x-ecs-trace**:id | trace.id |
| **x-ecs-transaction**:id | transaction.id |
| **x-ecs-user-agent**:name | user_agent.name |
| **x-ecs-user-agent**:original | user_agent.original |
| **x-ecs-user-agent**:version | user_agent.version |
| **x-ecs-user-agent**:device_name | user_agent.device.name |
| **x-ecs-vulnerability**:category | vulnerability.category |
| **x-ecs-vulnerability**:classification | vulnerability.classification |
| **x-ecs-vulnerability**:description | vulnerability.description |
| **x-ecs-vulnerability**:enumeration | vulnerability.enumeration |
| **x-ecs-vulnerability**:id | vulnerability.id |
| **x-ecs-vulnerability**:reference | vulnerability.reference |
| **x-ecs-vulnerability**:report_id | vulnerability.report_id |
| **x-ecs-vulnerability**:severity | vulnerability.severity |
| **x-ecs-vulnerability**:scanner_vendor | vulnerability.scanner.vendor |
| **x-ecs-vulnerability**:score_base | vulnerability.score.base |
| **x-ecs-vulnerability**:score_environmental | vulnerability.score.environmental |
| **x-ecs-vulnerability**:score_temporal | vulnerability.score.temporal |
| **x-ecs-vulnerability**:score_version | vulnerability.score.version |
| <br> | |
### Searchable STIX objects and properties for Beats dialect
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **ipv4-addr**:value | source.ip.keyword, destination.ip.keyword, client.ip.keyword, server.ip.keyword, host.ip.keyword, dns.resolved_ip.keyword, source.nat.ip.keyword, destination.nat.ip.keyword, client.nat.ip.keyword, server.nat.ip.keyword |
| **ipv6-addr**:value | source.ip.keyword, destination.ip.keyword, client.ip.keyword, server.ip.keyword, host.ip.keyword, dns.resolved_ip.keyword, source.nat.ip.keyword, destination.nat.ip.keyword, client.nat.ip.keyword, server.nat.ip.keyword |
| **mac-addr**:value | source.mac.keyword, destination.mac.keyword, client.mac.keyword, server.mac.keyword, host.mac.keyword |
| **network-traffic**:src_port | source.port, client.port, source.nat.port, client.nat.port |
| **network-traffic**:dst_port | destination.port, server.port, destination.nat.port, server.nat.port |
| **network-traffic**:protocols[*] | network.transport.keyword, network.type.keyword, network.protocol.keyword |
| **network-traffic**:src_ref.value | source.ip.keyword, client.ip |
| **network-traffic**:dst_ref.value | destination.ip.keyword, server.ip |
| **network-traffic**:src_byte_count | source.bytes, client.bytes |
| **network-traffic**:dst_byte_count | destination.bytes, server.bytes |
| **network-traffic**:src_packets | source.packets, client.packets |
| **network-traffic**:dst_packets | destination.packets, server.packets |
| **network-traffic**:x_vlan.id | network.vlan.id |
| **network-traffic**:x_vlan.name | network.vlan.name |
| **network-traffic**:x_vlan.inner.id | network.inner.vlan.id |
| **network-traffic**:x_vlan.inner.name | network.inner.vlan.name |
| **network-traffic**:x_name | network.name |
| **network-traffic**:x_application | network.application |
| **network-traffic**:x_direction | network.direction.keyword |
| **network-traffic**:x_forwarded_ip | network.forwarded_ip.keyword |
| **network-traffic**:x_community_id | network.community_id.keyword |
| **artifact**:payload_bin | event.original |
| **file**:name | file.name, dll.name, file.path, process.name.keyword, process.executable.keyword, process.parent.name.keyword, process.parent.executable.keyword |
| **file**:created | file.created, file.ctime |
| **file**:modified | file.mtime |
| **file**:accessed | file.accessed |
| **file**:size | file.size |
| **file**:mime_type | file.mime_type |
| **file**:hashes.MD5 | file.hash.md5 |
| **file**:hashes.'SHA-1' | file.hash.sha1 |
| **file**:hashes.'SHA-256' | file.hash.sha256 |
| **file**:hashes.'SHA-512' | file.hash.sha512 |
| **file**:parent_directory_ref.path | file.directory |
| **file**:x_attributes | file.attributes |
| **file**:x_extension | file.extension |
| **file**:x_path | file.path, dll.path |
| **file**:x_target_path | file.target_path |
| **file**:x_type | file.type |
| **file**:x_unix.device | file.device |
| **file**:x_unix.group_id | file.gid |
| **file**:x_unix.group | file.group |
| **file**:x_unix.inode | file.inode |
| **file**:x_unix.mode | file.mode |
| **file**:x_owner_ref.user_id | file.uid |
| **file**:x_owner_ref.account_login | file.owner |
| **file**:x_win_drive_letter | file.drive_letter |
| **file**:x_software_ref.name | file.pe.original_file_name, dll.pe.original_file_name |
| **file**:x_software_ref.vendor | file.pe.company, dll.pe.company |
| **file**:x_software_ref.version | file.pe.file_version, dll.pe.file_version |
| **file**:x_code_signature.exists | file.code_signature.exists, dll.code_signature.exists |
| **file**:x_code_signature.status | file.code_signature.status, dll.code_signature.status |
| **file**:x_code_signature.subject_name | file.code_signature.subject_name, dll.code_signature.subject_name |
| **file**:x_code_signature.trusted | file.code_signature.trusted, dll.code_signature.trusted |
| **file**:x_code_signature.valid | file.code_signature.valid, dll.code_signature.valid |
| **directory**:path | file.directory, file.path |
| **user-account**:user_id | user.name.keyword, user.id.keyword |
| **user-account**:account_login | user.name.keyword |
| **user-account**:display_name | user.full_name.keyword |
| **user-account**:x_domain | user.domain.keyword |
| **user-account**:x_hash | user.hash |
| **user-account**:x_group.domain | user.group.domain |
| **user-account**:x_group.id | user.group.id |
| **user-account**:x_group.name | user.group.name |
| **process**:command_line | process.command_line.keyword, powershell.command.value |
| **process**:created | process.start |
| **process**:cwd | process.working_directory.keyword |
| **process**:pid | process.pid, process.ppid, process.parent.pid, process.parent.ppid |
| **process**:name | process.name.keyword, process.parent.name.keyword |
| **process**:creator_user_ref.user_id | user.name.keyword |
| **process**:parent_ref.pid | process.ppid, process.parent.ppid |
| **process**:parent_ref.name | process.parent.name.keyword |
| **process**:parent_ref.x_exit_code | process.parent.exit_code |
| **process**:parent_ref.pgid | process.parent.pgid |
| **process**:parent_ref.x_window_title | process.parent.title.keyword |
| **process**:parent_ref.x_thread_id | process.parent.thread.id |
| **process**:parent_ref.x_uptime | process.parent.uptime |
| **process**:parent_ref.cwd | process.parent.working_directory |
| **process**:parent_ref.binary_ref.path | process.parent.executable |
| **process**:parent_ref.binary_ref.parent_directory_ref.path | process.parent.executable |
| **process**:binary_ref.name | process.executable.keyword, process.parent.executable.keyword |
| **process**:binary_ref.parent_directory_ref.path | process.executable, process.parent.executable |
| **process**:binary_ref.hashes.MD5 | process.hash.md5 |
| **process**:binary_ref.hashes.'SHA-1' | process.hash.sha1 |
| **process**:binary_ref.hashes.'SHA-256' | process.hash.sha256 |
| **process**:binary_ref.hashes.'SHA-512' | process.hash.sha512 |
| **process**:x_window_title | process.title |
| **process**:x_exit_code | process.exit_code |
| **process**:x_thread_id | process.thread.id |
| **process**:x_ttp_tags | tags |
| **process**:x_unique_id | process.entity_id.keyword, process.parent.entity_id.keyword |
| **process**:x_uptime | process.uptime |
| **url**:value | url.original |
| **domain-name**:value | url.domain, dns.question.name, dns.question.registered_domain, host.hostname.keyword, source.domain, destination.domain, server.domain, client.domain, source.registered_domain, destination.registered_domain, server.registered_domain, client.registered_domain, source.top_level_domain, destination.top_level_domain, server.top_level_domain, client.top_level_domain |
| **windows-registry-key**:key | registry.key |
| **software**:name | agent.name.keyword, process.pe.original_file_name.keyword, file.pe.original_file_name.keyword, dll.pe.original_file_name.keyword |
| **software**:vendor | process.pe.company.keyword, file.pe.company.keyword, dll.pe.company.keyword |
| **software**:version | process.pe.file_version.keyword, file.pe.file_version.keyword, dll.pe.file_version.keyword |
| **software**:x_product | process.pe.product.keyword, file.pe.product.keyword, dll.pe.product.keyword |
| **software**:x_description | process.pe.description.keyword, file.pe.description.keyword, dll.pe.description.keyword |
| **autonomous-system**:value | client.as.organization.name, server.as.organization.name, source.as.organization.name, destination.as.organization.name |
| **autonomous-system**:number | client.as.number, server.as.number, source.as.number, destination.as.number |
| **email-addr**:name | user.email |
| **x-oca-event**:action | event.action.keyword |
| **x-oca-event**:id | event.id |
| **x-oca-event**:category | event.category.keyword |
| **x-oca-event**:code | event.code |
| **x-oca-event**:created | event.created |
| **x-oca-event**:dataset | event.dataset |
| **x-oca-event**:duration | event.duration |
| **x-oca-event**:end | event.end |
| **x-oca-event**:hash | event.hash |
| **x-oca-event**:ingested | event.ingested |
| **x-oca-event**:kind | event.kind.keyword |
| **x-oca-event**:module | event.module.keyword |
| **x-oca-event**:outcome | event.outcome.keyword |
| **x-oca-event**:provider | event.provider.keyword |
| **x-oca-event**:risk_score | event.risk_score |
| **x-oca-event**:risk_score_norm | event.risk_score_norm |
| **x-oca-event**:sequence | event.sequence |
| **x-oca-event**:severity | event.severity |
| **x-oca-event**:start | event.start |
| **x-oca-event**:timezone | event.timezone |
| **x-oca-event**:type | event.type.keyword |
| **x-oca-event**:url | event.url |
| **x-oca-event**:original | message, powershell.file.script_block_text.keyword |
| **x-oca-event**:process_ref.pid | process.pid |
| **x-oca-event**:process_ref.name | process.name.keyword |
| **x-oca-event**:process_ref.command_line | process.command_line.keyword, powershell.command.value |
| **x-oca-event**:process_ref.binary_ref.name | file.name, process.executable.keyword |
| **x-oca-event**:process_ref.parent_ref.pid | process.ppid, process.parent.ppid |
| **x-oca-event**:process_ref.parent_ref.command_line | process.parent.command_line.keyword |
| **x-oca-event**:process_ref.creator_user_ref.user_id | user.name.keyword |
| **x-oca-event**:parent_process_ref.pid | process.ppid, process.parent.ppid |
| **x-oca-event**:parent_process_ref.command_line | process.parent.command_line.keyword |
| **x-oca-event**:domain_ref.value | url.domain, dns.question.name, dns.question.registered_domain, host.hostname.keyword |
| **x-oca-event**:file_ref.name | file.name |
| **x-oca-event**:host_ref.hostname | host.hostname.keyword |
| **x-oca-event**:host_ref.name | host.name.keyword |
| **x-oca-event**:registry_ref.key | registry.key, registry.path |
| **x-ecs-cloud**:account.id | cloud.account.id |
| **x-ecs-cloud**:availability_zone | cloud.availability_zone |
| **x-ecs-cloud**:instance.id | cloud.instance.id |
| **x-ecs-cloud**:instance.name | cloud.instance.name |
| **x-ecs-cloud**:machine.type | cloud.machine.type |
| **x-ecs-cloud**:provider | cloud.provider |
| **x-ecs-cloud**:region | cloud.region |
| **x-ecs-dns**:answers_class | dns.answers.class |
| **x-ecs-dns**:answers_data | dns.answers.data |
| **x-ecs-dns**:answers_name | dns.answers.name |
| **x-ecs-dns**:answers_ttl | dns.answers.ttl |
| **x-ecs-dns**:answers_type | dns.answers.type |
| **x-ecs-dns**:header_flags | dns.header_flags |
| **x-ecs-dns**:id | dns.id |
| **x-ecs-dns**:op_code | dns.op_code |
| **x-ecs-dns**:question_class | dns.question.class |
| **x-ecs-dns**:question_name | dns.question.name |
| **x-ecs-dns**:question_registered_domain | dns.question.registered_domain |
| **x-ecs-dns**:question_subdomain | dns.question.subdomain |
| **x-ecs-dns**:question_top_level_domain | dns.question.top_level_domain |
| **x-ecs-dns**:question_type | dns.question.type |
| **x-ecs-dns**:resolved_ip | dns.resolved_ip |
| **x-ecs-dns**:response_code | dns.response_code |
| **x-ecs-dns**:type | dns.type |
| **x-ecs**:version | ecs.version.keyword |
| **x-ecs-error**:code | error.code |
| **x-ecs-error**:id | error.id |
| **x-ecs-error**:message | error.message |
| **x-ecs-error**:stack_trace | error.stack_trace |
| **x-ecs-error**:type | error.type |
| **x-ecs-group**:domain | group.domain |
| **x-ecs-group**:id | group.id |
| **x-ecs-group**:name | group.name |
| **x-oca-asset**:architecture | host.architecture.keyword |
| **x-oca-asset**:domain | host.domain |
| **x-oca-asset**:hostname | host.hostname.keyword, observer.hostname.keyword |
| **x-oca-asset**:id | host.id.keyword, observer.serial_number.keyword |
| **x-oca-asset**:ip | host.ip.keyword, observer.ip.keyword |
| **x-oca-asset**:mac | host.mac.keyword, observer.mac.keyword |
| **x-oca-asset**:name | host.name.keyword, observer.name.keyword |
| **x-oca-asset**:type | host.type, observer.type |
| **x-oca-asset**:ingress.zone | observer.ingress.zone |
| **x-oca-asset**:ingress.interface.alias | observer.ingress.interface.alias |
| **x-oca-asset**:ingress.interface.id | observer.ingress.interface.id |
| **x-oca-asset**:ingress.interface.name | observer.ingress.interface.name |
| **x-oca-asset**:egress.zone | observer.egress.zone |
| **x-oca-asset**:egress.interface.alias | observer.egress.interface.alias |
| **x-oca-asset**:egress.interface.id | observer.egress.interface.id |
| **x-oca-asset**:egress.interface.name | observer.egress.interface.name |
| **x-oca-asset**:uptime | host.uptime |
| **x-oca-asset**:os_ref.name | host.os.name.keyword, observer.os.name.keyword, observer.product.keyword |
| **x-oca-asset**:os_ref.vendor | host.os.platform.keyword, observer.os.platform.keyword, observer.vendor.keyword |
| **x-oca-asset**:os_ref.version | host.os.version.keyword, observer.os.version.keyword, observer.version.keyword |
| **x-oca-asset**:container.id | container.id |
| **x-oca-asset**:container.image.name | container.image.name |
| **x-oca-asset**:container.image.tag | container.image.tag |
| **x-oca-asset**:container.labels | container.labels |
| **x-oca-asset**:container.name | container.name |
| **x-oca-asset**:container.runtime | container.runtime |
| **x-oca-geo**:city_name | server.geo.city_name, client.geo.city_name, source.geo.city_name, destination.geo.city_name |
| **x-oca-geo**:continent_name | server.geo.continent_name, client.geo.continent_name, source.geo.continent_name, destination.geo.continent_name |
| **x-oca-geo**:country_iso_code | server.geo.country_iso_code, client.geo.country_iso_code, source.geo.country_iso_code, destination.geo.country_iso_code |
| **x-oca-geo**:country_name | server.geo.country_name, client.geo.country_name, source.geo.country_name, destination.geo.country_name |
| **x-oca-geo**:location | server.geo.location, client.geo.location, source.geo.location, destination.geo.location |
| **x-oca-geo**:name | server.geo.name, client.geo.name, source.geo.name, destination.geo.name |
| **x-oca-geo**:region_iso_code | server.geo.region_iso_code, client.geo.region_iso_code, source.geo.region_iso_code, destination.geo.region_iso_code |
| **x-oca-geo**:region_name | server.geo.region_name, client.geo.region_name, source.geo.region_name, destination.geo.region_name |
| **x-ecs-http**:request_body_bytes | http.request.body.bytes |
| **x-ecs-http**:request_body_content | http.request.body.content |
| **x-ecs-http**:request_bytes | http.request.bytes |
| **x-ecs-http**:request_method | http.request.method |
| **x-ecs-http**:request_referrer | http.request.referrer |
| **x-ecs-http**:response_body_bytes | http.response.body.bytes |
| **x-ecs-http**:response_body_content | http.response.body.content |
| **x-ecs-http**:response_bytes | http.response.bytes |
| **x-ecs-http**:response_status_code | http.response.method |
| **x-ecs-http**:version | http.version |
| **x-ecs-log**:level | log.level.keyword |
| **x-ecs-log**:logger | log.logger |
| **x-ecs-log**:origin_file_line | log.origin.file.line |
| **x-ecs-log**:origin_file_name | log.origin.file.name |
| **x-ecs-log**:origin_function | log.origin.function |
| **x-ecs-log**:original | log.original |
| **x-ecs-log**:syslog_facility_code | log.syslog.facility.code |
| **x-ecs-log**:syslog_facility_name | log.syslog.facility.name |
| **x-ecs-log**:syslog_priority | log.syslog.priority |
| **x-ecs-log**:severity_syslog_code | log.syslog.severity.code |
| **x-ecs-log**:severity_syslog_name | log.syslog.severity.name |
| **x-ecs-organization**:id | organization.id |
| **x-ecs-organization**:name | organization.name |
| **x-ecs-pe**:company | dll.pe.company, process.pe.company.keyword, file.pe.company |
| **x-ecs-pe**:description | dll.pe.description, process.pe.description.keyword, file.pe.description |
| **x-ecs-pe**:file_version | dll.pe.file_version, process.pe.file_version.keyword, file.pe.file_version |
| **x-ecs-pe**:original_file_name | dll.pe.original_file_name, process.pe.original_file_name.keyword, file.pe.original_file_name |
| **x-ecs-pe**:product | dll.pe.product, process.pe.product.keyword, file.pe.product |
| **x-ecs-related**:hash | related.hash.keyword |
| **x-ecs-related**:ip | related.ip.keyword |
| **x-ecs-related**:user | related.user.keyword |
| **x-ecs-rule**:author | rule.author |
| **x-ecs-rule**:category | rule.category |
| **x-ecs-rule**:description | rule.description |
| **x-ecs-rule**:id | rule.id |
| **x-ecs-rule**:license | rule.license |
| **x-ecs-rule**:name | rule.name |
| **x-ecs-rule**:reference | rule.reference |
| **x-ecs-rule**:ruleset | rule.ruleset |
| **x-ecs-rule**:uuid | rule.uuid |
| **x-ecs-rule**:version | rule.version |
| **x-ecs-service**:id | service.id |
| **x-ecs-service**:name | service.name |
| **x-ecs-service**:state | service.state |
| **x-ecs-service**:type | service.type |
| **x-ecs-service**:version | service.version |
| **x-ecs-threat**:framework | threat.framework |
| **x-ecs-threat**:tactic_id | threat.tactic.id |
| **x-ecs-threat**:tactic_name | threat.tactic.name |
| **x-ecs-threat**:tactic_reference | threat.tactic.reference |
| **x-ecs-threat**:technique_id | threat.technique.id |
| **x-ecs-threat**:technique_name | threat.technique.name |
| **x-ecs-threat**:technique_reference | threat.technique.reference |
| **x-ecs-trace**:id | trace.id |
| **x-ecs-transaction**:id | transaction.id |
| **x-ecs-user-agent**:name | user_agent.name |
| **x-ecs-user-agent**:original | user_agent.original |
| **x-ecs-user-agent**:version | user_agent.version |
| **x-ecs-user-agent**:device_name | user_agent.device.name |
| **x-ecs-vulnerability**:category | vulnerability.category |
| **x-ecs-vulnerability**:classification | vulnerability.classification |
| **x-ecs-vulnerability**:description | vulnerability.description |
| **x-ecs-vulnerability**:enumeration | vulnerability.enumeration |
| **x-ecs-vulnerability**:id | vulnerability.id |
| **x-ecs-vulnerability**:reference | vulnerability.reference |
| **x-ecs-vulnerability**:report_id | vulnerability.report_id |
| **x-ecs-vulnerability**:severity | vulnerability.severity |
| **x-ecs-vulnerability**:scanner_vendor | vulnerability.scanner.vendor |
| **x-ecs-vulnerability**:score_base | vulnerability.score.base |
| **x-ecs-vulnerability**:score_environmental | vulnerability.score.environmental |
| **x-ecs-vulnerability**:score_temporal | vulnerability.score.temporal |
| **x-ecs-vulnerability**:score_version | vulnerability.score.version |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| artifact | payload_bin | original |
| artifact | mime_type | mime_type_event |
| <br> | | |
| autonomous-system | number | number |
| autonomous-system | name | name |
| <br> | | |
| directory | path | executable |
| directory | path | directory |
| <br> | | |
| domain-name | value | domain |
| domain-name | resolves_to_refs | domain |
| domain-name | value | registered_domain |
| domain-name | resolves_to_refs | registered_domain |
| domain-name | value | top_level_domain |
| domain-name | resolves_to_refs | top_level_domain |
| domain-name | value | url |
| domain-name | value | name |
| <br> | | |
| email-addr | value | email |
| email-addr | belongs_to_ref | email |
| <br> | | |
| file | name | executable |
| file | parent_directory_ref | executable |
| file | x_software_ref | executable |
| file | hashes.MD5 | md5 |
| file | hashes.SHA-1 | sha1 |
| file | hashes.SHA-256 | sha256 |
| file | hashes.SHA-512 | sha512 |
| file | x_owner_ref | name |
| file | x_owner_ref | id |
| file | name | name |
| file | dll_ref | name |
| file | x_path | path |
| file | x_software_ref.vendor | company |
| file | x_software_ref.version | file_version |
| file | x_software_ref.name | original_file_name |
| file | x_code_signature.exists | exists |
| file | x_code_signature.subject_name | subject_name |
| file | created | created |
| file | parent_directory_ref | directory |
| file | size | size |
| file | x_code_signature_subject_name | subject_name |
| file | accessed | accessed |
| file | x_attributes | attributes |
| file | created | ctime |
| file | x_unix.device | device |
| file | x_win_drive_letter | drive_letter |
| file | x_extension | extension |
| file | x_unix.group_id | gid |
| file | x_unix.group | group |
| file | x_unix.inode | inode |
| file | mime_type | mime_type |
| file | x_unix.mode | mode |
| file | modified | mtime |
| file | x_owner | owner |
| file | x_target_path | target_path |
| file | x_type | type |
| file | x_unix.user_id | uid |
| <br> | | |
| ipv4-addr | value | ip |
| ipv4-addr | resolves_to_refs | mac |
| ipv4-addr | belongs_to_refs | number |
| ipv4-addr | value | resolved_ip |
| <br> | | |
| ipv6-addr | value | ip |
| ipv6-addr | resolves_to_refs | mac |
| ipv6-addr | value | resolved_ip |
| <br> | | |
| mac-addr | value | mac |
| <br> | | |
| network-traffic | src_ref | ip |
| network-traffic | src_port | port |
| network-traffic | src_byte_count | bytes |
| network-traffic | src_packets | packets |
| network-traffic | dst_ref | ip |
| network-traffic | dst_port | port |
| network-traffic | dst_byte_count | bytes |
| network-traffic | dst_packets | packets |
| network-traffic | protocols | transport |
| network-traffic | protocols | type |
| network-traffic | protocols | protocol |
| network-traffic | x_vlan.id | id |
| network-traffic | x_vlan.name | name |
| network-traffic | x_vlan.inner.id | id |
| network-traffic | x_vlan.inner.name | name |
| network-traffic | x_name | name |
| network-traffic | x_application | application |
| network-traffic | x_direction | direction |
| network-traffic | x_forwarded_ip | forwarded_ip |
| network-traffic | x_community_id | community_id |
| network-traffic | extensions.dns-ext.answers | answers |
| network-traffic | extensions.dns-ext.header_flags | header_flags |
| network-traffic | extensions.dns-ext.dns_id | id |
| network-traffic | extensions.dns-ext.op_code | op_code |
| network-traffic | extensions.dns-ext.question.class | class |
| network-traffic | extensions.dns-ext.question.domain_ref | name |
| network-traffic | extensions.dns-ext.question.registered_domain_ref | registered_domain |
| network-traffic | extensions.dns-ext.question.subdomain | subdomain |
| network-traffic | extensions.dns-ext.question.top_level_domain | top_level_domain |
| network-traffic | extensions.dns-ext.question.type | type |
| network-traffic | extensions.dns-ext.resolved_ip_refs | resolved_ip |
| network-traffic | extensions.dns-ext.response_code | response_code |
| network-traffic | extensions.dns-ext.type | type |
| <br> | | |
| process | opened_connection_refs | transport |
| process | opened_connection_refs | type |
| process | opened_connection_refs | protocol |
| process | created | start |
| process | pid | pid |
| process | name | name |
| process | pid | ppid |
| process | parent_ref | ppid |
| process | command_line | command_line |
| process | binary_ref | executable |
| process | x_unique_id | entity_id |
| process | x_exit_code | exit_code |
| process | parent_ref | name |
| process | parent_ref.pgid | pgid |
| process | parent_ref | pid |
| process | parent_ref.ppid | ppid |
| process | x_thread_id | id |
| process | x_window_title | title |
| process | x_uptime | uptime |
| process | cwd | working_directory |
| process | x_exit_code | pgid |
| process | creator_user_ref | name |
| process | creator_user_ref | id |
| process | x_ttp_tags | tags |
| <br> | | |
| software | vendor | company |
| software | version | file_version |
| software | name | original_file_name |
| software | x_product | product |
| software | x_description | description |
| software | name | name |
| software | vendor | type |
| software | version | version |
| software | vendor | platform |
| software | name | product |
| software | vendor | vendor |
| <br> | | |
| url | value | original |
| <br> | | |
| user-account | user_id | name |
| user-account | account_login | name |
| user-account | x_domain | domain |
| user-account | display_name | full_name |
| user-account | x_hash | hash |
| user-account | user_id | id |
| user-account | x_group.domain | domain |
| user-account | x_group.id | id |
| user-account | x_group.name | name |
| <br> | | |
| windows-registry-key | key | registry |
| windows-registry-key | values | registry |
| <br> | | |
| x-ecs | version | version |
| <br> | | |
| x-ecs-client | address | address |
| <br> | | |
| x-ecs-cloud | account_id | id |
| x-ecs-cloud | availability_zone | availability_zone |
| x-ecs-cloud | instance_id | id |
| x-ecs-cloud | instance_name | name |
| x-ecs-cloud | machine_type | type |
| x-ecs-cloud | provider | provider |
| x-ecs-cloud | region | region |
| <br> | | |
| x-ecs-destination | address | address |
| <br> | | |
| x-ecs-error | code | code |
| x-ecs-error | error_id | id |
| x-ecs-error | message | message |
| x-ecs-error | stack_trace | stack_trace |
| x-ecs-error | type | type |
| <br> | | |
| x-ecs-group | domain | domain |
| x-ecs-group | group_id | id |
| x-ecs-group | name | name |
| <br> | | |
| x-ecs-http | request_body_bytes | bytes |
| x-ecs-http | request_body_content | content |
| x-ecs-http | request_bytes | bytes |
| x-ecs-http | request_method | method |
| x-ecs-http | request_referrer | referrer |
| x-ecs-http | response_body_bytes | bytes |
| x-ecs-http | response_body_content | content |
| x-ecs-http | response_bytes | bytes |
| x-ecs-http | response_status_code | status_code |
| x-ecs-http | version | version |
| <br> | | |
| x-ecs-log | level | level |
| x-ecs-log | logger | logger |
| x-ecs-log | origin_file_line | line |
| x-ecs-log | origin_file_name | name |
| x-ecs-log | origin_function | function |
| x-ecs-log | original | original |
| x-ecs-log | syslog_facility_code | code |
| x-ecs-log | syslog_facility_name | name |
| x-ecs-log | syslog_priority | priority |
| x-ecs-log | severity_syslog_code | code |
| x-ecs-log | severity_syslog_name | name |
| <br> | | |
| x-ecs-organization | organization_id | id |
| x-ecs-organization | name | name |
| <br> | | |
| x-ecs-registry | key | registry |
| x-ecs-registry | data_bytes | bytes |
| x-ecs-registry | data_strings | strings |
| x-ecs-registry | data_type | type |
| x-ecs-registry | hive | registry |
| x-ecs-registry | path | registry |
| x-ecs-registry | value | registry |
| <br> | | |
| x-ecs-related | hash | hash |
| x-ecs-related | ip | ip |
| x-ecs-related | user | user |
| <br> | | |
| x-ecs-rule | author | author |
| x-ecs-rule | category | category |
| x-ecs-rule | description | description |
| x-ecs-rule | rule_id | id |
| x-ecs-rule | license | license |
| x-ecs-rule | name | name |
| x-ecs-rule | reference | reference |
| x-ecs-rule | ruleset | ruleset |
| x-ecs-rule | uuid | uuid |
| x-ecs-rule | version | version |
| <br> | | |
| x-ecs-server | address | address |
| <br> | | |
| x-ecs-service | service_id | id |
| x-ecs-service | name | name |
| x-ecs-service | state | state |
| x-ecs-service | type | type |
| x-ecs-service | version | version |
| x-ecs-service | ephemeral_id | ephemeral_id |
| x-ecs-service | node_name | name |
| <br> | | |
| x-ecs-threat | framework | framework |
| x-ecs-threat | tactic_id | id |
| x-ecs-threat | tactic_name | name |
| x-ecs-threat | tactic_reference | reference |
| x-ecs-threat | technique_id | id |
| x-ecs-threat | technique_name | name |
| x-ecs-threat | technique_reference | reference |
| <br> | | |
| x-ecs-tls | client_certificate | certificate |
| x-ecs-tls | client_certificate_chain | certificate_chain |
| x-ecs-tls | client_ja3 | ja3 |
| x-ecs-tls | client_supported_ciphers | supported_ciphers |
| x-ecs-tls | server_certificate | certificate |
| x-ecs-tls | server_certificate_chain | certificate_chain |
| x-ecs-tls | server_ja3s | ja3s |
| x-ecs-tls | cipher | cipher |
| x-ecs-tls | curve | curve |
| x-ecs-tls | established | established |
| x-ecs-tls | next_protocol | next_protocol |
| x-ecs-tls | resumed | resumed |
| x-ecs-tls | version | version |
| x-ecs-tls | version_protocol | version_protocol |
| <br> | | |
| x-ecs-trace | trace_id | id |
| <br> | | |
| x-ecs-transaction | transaction_id | id |
| <br> | | |
| x-ecs-user_agent | name | name |
| x-ecs-user_agent | original | original |
| x-ecs-user_agent | version | version |
| x-ecs-user_agent | device_name | name |
| <br> | | |
| x-ecs-vulnerability | category | category |
| x-ecs-vulnerability | classification | classification |
| x-ecs-vulnerability | description | description |
| x-ecs-vulnerability | enumeration | enumeration |
| x-ecs-vulnerability | vulnerability_id | id |
| x-ecs-vulnerability | reference | reference |
| x-ecs-vulnerability | report_id | report_id |
| x-ecs-vulnerability | severity | severity |
| x-ecs-vulnerability | scanner_vendor | vendor |
| x-ecs-vulnerability | score_base | base |
| x-ecs-vulnerability | score_environmental | environmental |
| x-ecs-vulnerability | score_temporal | temporal |
| x-ecs-vulnerability | score_version | version |
| <br> | | |
| x-oca-asset | extensions.x-oca-container-ext.id | id |
| x-oca-asset | extensions.x-oca-container-ext.image.name | name |
| x-oca-asset | extensions.x-oca-container-ext.image.tag | tag |
| x-oca-asset | extensions.x-oca-container-ext.labels | labels |
| x-oca-asset | extensions.x-oca-container-ext.name | name |
| x-oca-asset | extensions.x-oca-container-ext.container_type | runtime |
| x-oca-asset | architecture | architecture |
| x-oca-asset | domain_ref | domain |
| x-oca-asset | hostname | hostname |
| x-oca-asset | device_id | id |
| x-oca-asset | ip_refs | ip |
| x-oca-asset | mac_refs | mac |
| x-oca-asset | name | name |
| x-oca-asset | host_type | type |
| x-oca-asset | uptime | uptime |
| x-oca-asset | geo_ref | city_name |
| x-oca-asset | os_ref | name |
| x-oca-asset | user_domain | domain |
| x-oca-asset | user_email | email |
| x-oca-asset | user_full_name | full_name |
| x-oca-asset | user_hash | hash |
| x-oca-asset | user_id | id |
| x-oca-asset | user_name | name |
| x-oca-asset | user_group_domain | domain |
| x-oca-asset | user_group_id | id |
| x-oca-asset | user_group_name | name |
| x-oca-asset | egress.zone | zone |
| x-oca-asset | egress.interface.alias | alias |
| x-oca-asset | egress.interface.id | id |
| x-oca-asset | egress.interface.name | name |
| x-oca-asset | egress.vlan.id | id |
| x-oca-asset | egress.vlan.name | name |
| x-oca-asset | ingress.zone | zone |
| x-oca-asset | ingress.interface.alias | alias |
| x-oca-asset | ingress.interface.id | id |
| x-oca-asset | ingress.interface.name | name |
| x-oca-asset | ingress.vlan.id | id |
| x-oca-asset | ingress.vlan.name | name |
| x-oca-asset | os_ref | product |
| x-oca-asset | device_id | serial_number |
| x-oca-asset | os_ref | vendor |
| <br> | | |
| x-oca-event | network_ref | transport |
| x-oca-event | network_ref | type |
| x-oca-event | network_ref | protocol |
| x-oca-event | original_ref | original |
| x-oca-event | action | action |
| x-oca-event | event_id | id |
| x-oca-event | category | category |
| x-oca-event | code | code |
| x-oca-event | created | created |
| x-oca-event | dataset | dataset |
| x-oca-event | duration | duration |
| x-oca-event | end | end |
| x-oca-event | hash | hash |
| x-oca-event | ingested | ingested |
| x-oca-event | kind | kind |
| x-oca-event | module | module |
| x-oca-event | outcome | outcome |
| x-oca-event | provider | provider |
| x-oca-event | reference | reference |
| x-oca-event | risk_score | risk_score |
| x-oca-event | risk_score_norm | risk_score_norm |
| x-oca-event | sequence | sequence |
| x-oca-event | severity | severity |
| x-oca-event | start | start |
| x-oca-event | timezone | timezone |
| x-oca-event | event_type | type |
| x-oca-event | url | url |
| x-oca-event | domain_ref | url |
| x-oca-event | url_ref | original |
| x-oca-event | domain_ref | domain |
| x-oca-event | process_ref | pid |
| x-oca-event | process_ref | name |
| x-oca-event | process_ref | executable |
| x-oca-event | parent_process_ref | name |
| x-oca-event | parent_process_ref | pid |
| x-oca-event | parent_process_ref | executable |
| x-oca-event | user_ref | name |
| x-oca-event | user_ref | id |
| x-oca-event | agent | name |
| x-oca-event | domain_ref | name |
| x-oca-event | network_ref | name |
| x-oca-event | ip_refs | resolved_ip |
| x-oca-event | file_ref | name |
| x-oca-event | host_ref | hostname |
| x-oca-event | host_ref | name |
| x-oca-event | registry_ref | registry |
| <br> | | |
| x-oca-geo | city_name | city_name |
| x-oca-geo | continent_name | continent_name |
| x-oca-geo | country_iso_code | country_iso_code |
| x-oca-geo | country_name | country_name |
| x-oca-geo | location | location |
| x-oca-geo | name | name |
| x-oca-geo | region_iso_code | region_iso_code |
| x-oca-geo | region_name | region_name |
| <br> | | |
| x509-certificate | issuer | issuer |
| x509-certificate | hashes.SHA-256 | sha256 |
| x509-certificate | hashes.SHA-1 | sha1 |
| x509-certificate | hashes.MD5 | md5 |
| x509-certificate | validity_not_after | not_after |
| x509-certificate | validity_not_before | not_before |
| x509-certificate | subject | subject |
| <br> | | |
