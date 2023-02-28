##### Updated on 02/27/23
## Elasticsearch ECS
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
| **ipv4-addr**:value | source.ip, destination.ip, client.ip, server.ip, host.ip, dns.resolved_ip |
| **ipv6-addr**:value | source.ip, destination.ip, client.ip, server.ip, host.ip, dns.resolved_ip |
| **mac-addr**:value | source.mac, destination.mac, client.mac, server.mac, host.mac |
| **network-traffic**:src_port | source.port, client.port |
| **network-traffic**:dst_port | destination.port, server.port |
| **network-traffic**:protocols[*] | network.transport, network.type, network.protocol |
| **network-traffic**:src_ref.value | source.ip, client.ip |
| **network-traffic**:dst_ref.value | destination.ip, server.ip |
| **network-traffic**:src_byte_count | source.bytes, client.bytes |
| **network-traffic**:dst_byte_count | destination.bytes, server.bytes |
| **network-traffic**:src_packets | source.packets, client.packets |
| **network-traffic**:dst_packets | destination.packets, server.packets |
| **x-ecs-network**:inner.vlan.id | network.inner.vlan.id |
| **x-ecs-network**:inner.vlan.name | network.inner.vlan.name |
| **x-ecs-network**:name | network.name |
| **x-ecs-network**:application | network.application |
| **x-ecs-network**:direction | network.direction |
| **x-ecs-network**:forwarded_ip | network.forwarded_ip |
| **x-ecs-network**:community_id | network.community_id |
| **artifact**:payload_bin | event.original |
| **file**:name | file.name, file.path, process.name, process.executable, process.parent.name, process.parent.executable |
| **file**:created | file.created |
| **file**:size | file.size |
| **file**:hashes.MD5 | file.hash.md5 |
| **file**:hashes.'SHA-1' | file.hash.sha1 |
| **file**:hashes.'SHA-256' | file.hash.sha256 |
| **file**:hashes.'SHA-512' | file.hash.sha512 |
| **file**:parent_directory_ref.path | file.directory |
| **x-ecs-file**:accessed | file.accessed |
| **x-ecs-file**:attributes | file.attributes |
| **x-ecs-file**:ctime | file.ctime |
| **x-ecs-file**:device | file.device |
| **x-ecs-file**:drive_letter | file.drive_letter |
| **x-ecs-file**:extension | file.extension |
| **x-ecs-file**:gid | file.gid |
| **x-ecs-file**:group | file.group |
| **x-ecs-file**:inode | file.inode |
| **x-ecs-file**:mime_type | file.mime_type |
| **x-ecs-file**:mode | file.mode |
| **x-ecs-file**:mtime | file.mtime |
| **x-ecs-file**:owner | file.owner |
| **x-ecs-file**:path | file.path |
| **x-ecs-file**:target_path | file.target_path |
| **x-ecs-file**:type | file.type |
| **x-ecs-file**:uid | file.uid |
| **x-ecs-file**:pe.company | file.pe.company |
| **x-ecs-file**:pe.description | file.pe.description |
| **x-ecs-file**:pe.file_version | file.pe.file_version |
| **x-ecs-file**:pe.original_file_name | file.pe.original_file_name |
| **x-ecs-file**:pe.product | file.pe.product |
| **x-ecs-file**:code_signature.exists | file.code_signature.exists |
| **x-ecs-file**:code_signature.status | file.code_signature.status |
| **x-ecs-file**:code_signature.subject_name | file.code_signature.subject_name |
| **x-ecs-file**:code_signature.trusted | file.code_signature.trusted |
| **x-ecs-file**:code_signature.valid | file.code_signature.valid |
| **directory**:path | file.directory, file.path |
| **user-account**:user_id | user.name, user.id |
| **user-account**:account_login | user.name |
| **x-ecs-user**:domain | user.domain |
| **x-ecs-user**:full_name | user.full_name |
| **x-ecs-user**:hash | user.hash |
| **x-ecs-user**:id | user.id |
| **x-ecs-user**:group_domain | user.group.domain |
| **x-ecs-user**:group_id | user.group.id |
| **x-ecs-user**:group_name | user.group.name |
| **process**:command_line | process.command_line, powershell.command.value |
| **process**:created | process.start |
| **process**:pid | process.pid, process.ppid, process.parent.pid, process.parent.ppid |
| **process**:name | process.name, process.parent.name |
| **process**:creator_user_ref.user_id | user.name |
| **process**:parent_ref.pid | process.ppid, process.parent.ppid |
| **process**:parent_ref.name | process.parent.name |
| **process**:binary_ref.name | process.executable, process.parent.executable |
| **process**:x_ttp_tags | tags |
| **process**:x_unique_id | process.entity_id, process.parent.entity_id |
| **x-ecs-process**:args | process.args |
| **x-ecs-process**:args_count | process.args_count |
| **x-ecs-process**:executable | process.executable |
| **x-ecs-process**:exit_code | process.exit_code |
| **x-ecs-process**:thread.id | process.thread.id |
| **x-ecs-process**:thread.name | process.thread.name |
| **x-ecs-process**:title | process.title |
| **x-ecs-process**:uptime | process.uptime |
| **x-ecs-process**:working_directory | process.working_directory |
| **x-ecs-process**:parent.args | process.parent.args |
| **x-ecs-process**:parent.args_count | process.parent.args_count |
| **x-ecs-process**:parent.exit_code | process.parent.exit_code |
| **x-ecs-process**:parent.pgid | process.parent.pgid |
| **x-ecs-process**:parent.thread.id | process.parent.thread.id |
| **x-ecs-process**:parent.thread.name | process.parent.thread.name |
| **x-ecs-process**:parent.title | process.parent.title |
| **x-ecs-process**:parent.uptime | process.parent.uptime |
| **x-ecs-process**:parent.working_directory | process.parent.working_directory |
| **x-ecs-process**:pe.company | process.pe.company |
| **x-ecs-process**:pe.description | process.pe.description |
| **x-ecs-process**:pe.file_version | process.pe.file_version |
| **x-ecs-process**:pe.original_file_name | process.pe.original_file_name |
| **x-ecs-process**:pe.product | process.pe.product |
| **x-ecs-process**:code_signature.exists | process.code_signature.exists |
| **x-ecs-process**:code_signature.status | process.code_signature.status |
| **x-ecs-process**:code_signature.subject_name | process.code_signature.subject_name |
| **x-ecs-process**:code_signature.trusted | process.code_signature.trusted |
| **x-ecs-process**:code_signature.valid | process.code_signature.valid |
| **x-ecs-process**:parent.code_signature.exists | process.parent.code_signature.exists |
| **x-ecs-process**:parent.code_signature.status | process.parent.code_signature.status |
| **x-ecs-process**:parent.code_signature.subject_name | process.parent.code_signature.subject_name |
| **x-ecs-process**:parent.code_signature.trusted | process.parent.code_signature.trusted |
| **x-ecs-process**:parent.code_signature.valid | process.parent.code_signature.valid |
| **url**:value | url.original |
| **domain-name**:value | url.domain, dns.question.name, dns.question.registered_domain, host.hostname |
| **windows-registry-key**:key | registry.key |
| **software**:name | agent.name |
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
| **x-ecs-container**:id | container.id |
| **x-ecs-container**:image.name | container.image.name |
| **x-ecs-container**:image.tag | container.image.tag |
| **x-ecs-container**:labels | container.labels |
| **x-ecs-container**:name | container.name |
| **x-ecs-container**:runtime | container.runtime |
| **x-ecs-dll**:name | dll.name |
| **x-ecs-dll**:path | dll.path |
| **x-ecs-dll**:pe.company | dll.pe.company |
| **x-ecs-dll**:pe.description | dll.pe.description |
| **x-ecs-dll**:pe.file_version | dll.pe.file_version |
| **x-ecs-dll**:pe.original_file_name | dll.pe.original_file_name |
| **x-ecs-dll**:pe.product | dll.pe.product |
| **x-ecs-dll**:code_signature.exists | dll.code_signature.exists |
| **x-ecs-dll**:code_signature.status | dll.code_signature.status |
| **x-ecs-dll**:code_signature.subject_name | dll.code_signature.subject_name |
| **x-ecs-dll**:code_signature.trusted | dll.code_signature.trusted |
| **x-ecs-dll**:code_signature.valid | dll.code_signature.valid |
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
| **x-oca-asset**:hostname | host.hostname |
| **x-oca-asset**:id | host.id |
| **x-oca-asset**:ip | host.ip |
| **x-oca-asset**:mac | host.mac |
| **x-oca-asset**:name | host.name |
| **x-oca-asset**:type | host.type |
| **x-oca-asset**:uptime | host.uptime |
| **x-oca-asset**:os.name | host.os.name |
| **x-oca-asset**:os.platform | host.os.platform |
| **x-oca-asset**:os.version | host.os.version |
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
| **x-ecs-observer**:egress.zone | observer.egress.zone |
| **x-ecs-observer**:egress.interface.alias | observer.egress.interface.alias |
| **x-ecs-observer**:egress.interface.id | observer.egress.interface.id |
| **x-ecs-observer**:egress.interface.name | observer.egress.interface.name |
| **x-ecs-observer**:hostname | observer.hostname |
| **x-ecs-observer**:ingress.zone | observer.ingress.zone |
| **x-ecs-observer**:ingress.interface.alias | observer.ingress.interface.alias |
| **x-ecs-observer**:ingress.interface.id | observer.ingress.interface.id |
| **x-ecs-observer**:ingress.interface.name | observer.ingress.interface.name |
| **x-ecs-observer**:ip | observer.ip |
| **x-ecs-observer**:mac | observer.mac |
| **x-ecs-observer**:name | observer.name |
| **x-ecs-observer**:product | observer.product |
| **x-ecs-observer**:serial_number | observer.serial_number |
| **x-ecs-observer**:type | observer.type |
| **x-ecs-observer**:vendor | observer.vendor |
| **x-ecs-observer**:version | observer.version |
| **x-ecs-observer**:os.name | observer.os.name |
| **x-ecs-observer**:os.platform | observer.os.platform |
| **x-ecs-observer**:os.version | observer.os.version |
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
| **x-ecs-source**:address | source.address |
| **x-ecs-source**:domain | source.domain |
| **x-ecs-source**:nat.ip | source.nat.ip |
| **x-ecs-source**:nat.port | source.nat.port |
| **x-ecs-source**:registered_domain | source.registered_domain |
| **x-ecs-source**:top_level_domain | source.top_level_domain |
| **x-ecs-source**:geo.city_name | source.geo.city_name |
| **x-ecs-source**:geo.continent_name | source.geo.continent_name |
| **x-ecs-source**:geo.country_iso_code | source.geo.country_iso_code |
| **x-ecs-source**:geo.country_name | source.geo.country_name |
| **x-ecs-source**:geo.location | source.geo.location |
| **x-ecs-source**:geo.name | source.geo.name |
| **x-ecs-source**:geo.region_iso_code | source.geo.region_iso_code |
| **x-ecs-source**:geo.region_name | source.geo.region_name |
| **x-ecs-destination**:address | destination.address |
| **x-ecs-destination**:domain | destination.domain |
| **x-ecs-destination**:nat.ip | destination.nat.ip |
| **x-ecs-destination**:nat.port | destination.nat.port |
| **x-ecs-destination**:registered_domain | destination.registered_domain |
| **x-ecs-destination**:top_level_domain | destination.top_level_domain |
| **x-ecs-destination**:geo.city_name | destination.geo.city_name |
| **x-ecs-destination**:geo.continent_name | destination.geo.continent_name |
| **x-ecs-destination**:geo.country_iso_code | destination.geo.country_iso_code |
| **x-ecs-destination**:geo.country_name | destination.geo.country_name |
| **x-ecs-destination**:geo.location | destination.geo.location |
| **x-ecs-destination**:geo.name | destination.geo.name |
| **x-ecs-destination**:geo.region_iso_code | destination.geo.region_iso_code |
| **x-ecs-destination**:geo.region_name | destination.geo.region_name |
| **x-ecs-client**:address | client.address |
| **x-ecs-client**:domain | client.domain |
| **x-ecs-client**:nat.ip | client.nat.ip |
| **x-ecs-client**:nat.port | client.nat.port |
| **x-ecs-client**:registered_domain | client.registered_domain |
| **x-ecs-client**:top_level_domain | client.top_level_domain |
| **x-ecs-client**:geo.city_name | client.geo.city_name |
| **x-ecs-client**:geo.continent_name | client.geo.continent_name |
| **x-ecs-client**:geo.country_iso_code | client.geo.country_iso_code |
| **x-ecs-client**:geo.country_name | client.geo.country_name |
| **x-ecs-client**:geo.location | client.geo.location |
| **x-ecs-client**:geo.name | client.geo.name |
| **x-ecs-client**:geo.region_iso_code | client.geo.region_iso_code |
| **x-ecs-client**:geo.region_name | client.geo.region_name |
| **x-ecs-server**:address | server.address |
| **x-ecs-server**:domain | server.domain |
| **x-ecs-server**:nat.ip | server.nat.ip |
| **x-ecs-server**:nat.port | server.nat.port |
| **x-ecs-server**:registered_domain | server.registered_domain |
| **x-ecs-server**:top_level_domain | server.top_level_domain |
| **x-ecs-server**:geo.city_name | server.geo.city_name |
| **x-ecs-server**:geo.continent_name | server.geo.continent_name |
| **x-ecs-server**:geo.country_iso_code | server.geo.country_iso_code |
| **x-ecs-server**:geo.country_name | server.geo.country_name |
| **x-ecs-server**:geo.location | server.geo.location |
| **x-ecs-server**:geo.name | server.geo.name |
| **x-ecs-server**:geo.region_iso_code | server.geo.region_iso_code |
| **x-ecs-server**:geo.region_name | server.geo.region_name |
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
| domain-name | value | url |
| domain-name | value | domain |
| domain-name | value | name |
| domain-name | value | registered_domain |
| <br> | | |
| email-addr | value | email |
| email-addr | belongs_to_ref | email |
| <br> | | |
| file | name | executable |
| file | parent_directory_ref | executable |
| file | name | name |
| file | created | created |
| file | parent_directory_ref | directory |
| file | size | size |
| file | hashes.SHA-256 | sha256 |
| file | hashes.SHA-1 | sha1 |
| file | hashes.MD5 | md5 |
| file | hashes.SHA-512 | sha512 |
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
| process | parent_ref | name |
| process | parent_ref | pid |
| process | creator_user_ref | name |
| process | creator_user_ref | id |
| process | x_ttp_tags | tags |
| <br> | | |
| software | name | name |
| software | vendor | type |
| software | version | version |
| <br> | | |
| url | value | original |
| <br> | | |
| user-account | user_id | name |
| user-account | account_login | name |
| user-account | user_id | id |
| <br> | | |
| windows-registry-key | key | registry |
| windows-registry-key | values | registry |
| <br> | | |
| x-ecs | version | version |
| <br> | | |
| x-ecs-client | address | address |
| x-ecs-client | domain | domain |
| x-ecs-client | nat_ip | ip |
| x-ecs-client | nat_port | port |
| x-ecs-client | registered_domain | registered_domain |
| x-ecs-client | top_level_domain | top_level_domain |
| x-ecs-client | geo_city_name | city_name |
| x-ecs-client | geo_continent_name | continent_name |
| x-ecs-client | geo_country_iso_code | country_iso_code |
| x-ecs-client | geo_country_name | country_name |
| x-ecs-client | geo_location | location |
| x-ecs-client | geo_name | name |
| x-ecs-client | geo_region_iso_code | region_iso_code |
| x-ecs-client | geo_region_name | region_name |
| <br> | | |
| x-ecs-cloud | account_id | id |
| x-ecs-cloud | availability_zone | availability_zone |
| x-ecs-cloud | instance_id | id |
| x-ecs-cloud | instance_name | name |
| x-ecs-cloud | machine_type | type |
| x-ecs-cloud | provider | provider |
| x-ecs-cloud | region | region |
| <br> | | |
| x-ecs-container | container_id | id |
| x-ecs-container | image_name | name |
| x-ecs-container | image_tag | tag |
| x-ecs-container | labels | labels |
| x-ecs-container | name | name |
| x-ecs-container | runtime | runtime |
| <br> | | |
| x-ecs-destination | address | address |
| x-ecs-destination | domain | domain |
| x-ecs-destination | nat_ip | ip |
| x-ecs-destination | nat_port | port |
| x-ecs-destination | registered_domain | registered_domain |
| x-ecs-destination | top_level_domain | top_level_domain |
| x-ecs-destination | geo_city_name | city_name |
| x-ecs-destination | geo_continent_name | continent_name |
| x-ecs-destination | geo_country_iso_code | country_iso_code |
| x-ecs-destination | geo_country_name | country_name |
| x-ecs-destination | geo_location | location |
| x-ecs-destination | geo_name | name |
| x-ecs-destination | geo_region_iso_code | region_iso_code |
| x-ecs-destination | geo_region_name | region_name |
| <br> | | |
| x-ecs-dll | name | name |
| x-ecs-dll | path | path |
| x-ecs-dll | pe_company | company |
| x-ecs-dll | pe_description | description |
| x-ecs-dll | pe_file_version | file_version |
| x-ecs-dll | pe_original_file_name | original_file_name |
| x-ecs-dll | pe_product | product |
| x-ecs-dll | code_signature_exists | exists |
| x-ecs-dll | code_signature_subject_name | subject_name |
| x-ecs-dll | hashes.SHA-256 | sha256 |
| x-ecs-dll | hashes.SHA-1 | sha1 |
| x-ecs-dll | hashes.MD5 | md5 |
| x-ecs-dll | hashes.SHA-512 | sha512 |
| <br> | | |
| x-ecs-error | code | code |
| x-ecs-error | error_id | id |
| x-ecs-error | message | message |
| x-ecs-error | stack_trace | stack_trace |
| x-ecs-error | type | type |
| <br> | | |
| x-ecs-file | pe_company | company |
| x-ecs-file | pe_description | description |
| x-ecs-file | pe_file_version | file_version |
| x-ecs-file | pe_original_file_name | original_file_name |
| x-ecs-file | pe_product | product |
| x-ecs-file | code_signature_exists | exists |
| x-ecs-file | code_signature_subject_name | subject_name |
| x-ecs-file | accessed | accessed |
| x-ecs-file | attributes | attributes |
| x-ecs-file | ctime | ctime |
| x-ecs-file | device | device |
| x-ecs-file | drive_letter | drive_letter |
| x-ecs-file | extension | extension |
| x-ecs-file | gid | gid |
| x-ecs-file | group | group |
| x-ecs-file | inode | inode |
| x-ecs-file | mime_type | mime_type |
| x-ecs-file | mode | mode |
| x-ecs-file | mtime | mtime |
| x-ecs-file | owner | owner |
| x-ecs-file | path | path |
| x-ecs-file | target_path | target_path |
| x-ecs-file | type | type |
| x-ecs-file | uid | uid |
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
| x-ecs-network | vlan_id | id |
| x-ecs-network | vlan_name | name |
| x-ecs-network | inner_vlan_id | id |
| x-ecs-network | inner_vlan_name | name |
| x-ecs-network | name | name |
| x-ecs-network | application | application |
| x-ecs-network | direction | direction |
| x-ecs-network | forwarded_ip | forwarded_ip |
| x-ecs-network | community_id | community_id |
| <br> | | |
| x-ecs-observer | egress_zone | zone |
| x-ecs-observer | egress_interface_alias | alias |
| x-ecs-observer | egress_interface_id | id |
| x-ecs-observer | egress_interface_name | name |
| x-ecs-observer | egress_vlan_id | id |
| x-ecs-observer | egress_vlan_name | name |
| x-ecs-observer | hostname | hostname |
| x-ecs-observer | ingress_zone | zone |
| x-ecs-observer | ingress_interface_alias | alias |
| x-ecs-observer | ingress_interface_id | id |
| x-ecs-observer | ingress_interface_name | name |
| x-ecs-observer | ingress_vlan_id | id |
| x-ecs-observer | ingress_vlan_name | name |
| x-ecs-observer | ip | ip |
| x-ecs-observer | mac | mac |
| x-ecs-observer | name | name |
| x-ecs-observer | product | product |
| x-ecs-observer | serial_number | serial_number |
| x-ecs-observer | type | type |
| x-ecs-observer | vendor | vendor |
| x-ecs-observer | version | version |
| x-ecs-observer | os_name | name |
| x-ecs-observer | os_platform | platform |
| x-ecs-observer | os_version | version |
| x-ecs-observer | geo_city_name | city_name |
| x-ecs-observer | geo_continent_name | continent_name |
| x-ecs-observer | geo_country_iso_code | country_iso_code |
| x-ecs-observer | geo_country_name | country_name |
| x-ecs-observer | geo_location | location |
| x-ecs-observer | geo_name | name |
| x-ecs-observer | geo_region_iso_code | region_iso_code |
| x-ecs-observer | geo_region_name | region_name |
| <br> | | |
| x-ecs-organization | organization_id | id |
| x-ecs-organization | name | name |
| <br> | | |
| x-ecs-process | code_signature_exists | exists |
| x-ecs-process | code_signature_subject_name | subject_name |
| x-ecs-process | pe_company | company |
| x-ecs-process | pe_description | description |
| x-ecs-process | pe_file_version | file_version |
| x-ecs-process | pe_original_file_name | original_file_name |
| x-ecs-process | pe_product | product |
| x-ecs-process | args | args |
| x-ecs-process | args_count | args_count |
| x-ecs-process | exit_code | exit_code |
| x-ecs-process | parent_args | args |
| x-ecs-process | parent_args_count | args_count |
| x-ecs-process | parent_exit_code | exit_code |
| x-ecs-process | parent_pgid | pgid |
| x-ecs-process | parent_ppid | ppid |
| x-ecs-process | parent_thread_id | id |
| x-ecs-process | parent_thread_name | name |
| x-ecs-process | parent_title | title |
| x-ecs-process | parent_uptime | uptime |
| x-ecs-process | parent_working_directory | working_directory |
| x-ecs-process | exit_code | pgid |
| x-ecs-process | thread_id | id |
| x-ecs-process | thread_name | name |
| x-ecs-process | title | title |
| x-ecs-process | uptime | uptime |
| x-ecs-process | working_directory | working_directory |
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
| x-ecs-server | domain | domain |
| x-ecs-server | nat_ip | ip |
| x-ecs-server | nat_port | port |
| x-ecs-server | registered_domain | registered_domain |
| x-ecs-server | top_level_domain | top_level_domain |
| x-ecs-server | geo_city_name | city_name |
| x-ecs-server | geo_continent_name | continent_name |
| x-ecs-server | geo_country_iso_code | country_iso_code |
| x-ecs-server | geo_country_name | country_name |
| x-ecs-server | geo_location | location |
| x-ecs-server | geo_name | name |
| x-ecs-server | geo_region_iso_code | region_iso_code |
| x-ecs-server | geo_region_name | region_name |
| <br> | | |
| x-ecs-service | service_id | id |
| x-ecs-service | name | name |
| x-ecs-service | state | state |
| x-ecs-service | type | type |
| x-ecs-service | version | version |
| x-ecs-service | ephemeral_id | ephemeral_id |
| x-ecs-service | node_name | name |
| <br> | | |
| x-ecs-source | address | address |
| x-ecs-source | domain | domain |
| x-ecs-source | nat_ip | ip |
| x-ecs-source | nat_port | port |
| x-ecs-source | registered_domain | registered_domain |
| x-ecs-source | top_level_domain | top_level_domain |
| x-ecs-source | geo_city_name | city_name |
| x-ecs-source | geo_continent_name | continent_name |
| x-ecs-source | geo_country_iso_code | country_iso_code |
| x-ecs-source | geo_country_name | country_name |
| x-ecs-source | geo_location | location |
| x-ecs-source | geo_name | name |
| x-ecs-source | geo_region_iso_code | region_iso_code |
| x-ecs-source | geo_region_name | region_name |
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
| x-ecs-user | domain | domain |
| x-ecs-user | full_name | full_name |
| x-ecs-user | hash | hash |
| x-ecs-user | user_id | id |
| x-ecs-user | group_domain | domain |
| x-ecs-user | group_id | id |
| x-ecs-user | group_name | name |
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
| x-oca-asset | architecture | architecture |
| x-oca-asset | domain | domain |
| x-oca-asset | hostname | hostname |
| x-oca-asset | host_id | id |
| x-oca-asset | ip_refs | ip |
| x-oca-asset | mac_refs | mac |
| x-oca-asset | name | name |
| x-oca-asset | host_type | type |
| x-oca-asset | uptime | uptime |
| x-oca-asset | geo_city_name | city_name |
| x-oca-asset | geo_continent_name | continent_name |
| x-oca-asset | geo_country_iso_code | country_iso_code |
| x-oca-asset | geo_country_name | country_name |
| x-oca-asset | geo_location | location |
| x-oca-asset | geo_name | name |
| x-oca-asset | geo_region_iso_code | region_iso_code |
| x-oca-asset | geo_region_name | region_name |
| x-oca-asset | os_name | name |
| x-oca-asset | os_platform | platform |
| x-oca-asset | os_version | version |
| x-oca-asset | user_domain | domain |
| x-oca-asset | user_email | email |
| x-oca-asset | user_full_name | full_name |
| x-oca-asset | user_hash | hash |
| x-oca-asset | user_id | id |
| x-oca-asset | user_name | name |
| x-oca-asset | user_group_domain | domain |
| x-oca-asset | user_group_id | id |
| x-oca-asset | user_group_name | name |
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
| x509-certificate | issuer | issuer |
| x509-certificate | hashes.SHA-256 | sha256 |
| x509-certificate | hashes.SHA-1 | sha1 |
| x509-certificate | hashes.MD5 | md5 |
| x509-certificate | validity_not_after | not_after |
| x509-certificate | validity_not_before | not_before |
| x509-certificate | subject | subject |
| <br> | | |
