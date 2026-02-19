##### Updated on 05/30/24
## Trellix Endpoint Security HX
### Results STIX Domain Objects
* Identity
* Observed Data

### Supported STIX Operators
*Comparison AND/OR operators are inside the observation while observation AND/OR operators are between observations (square brackets).*

| STIX Operator     | Data Source Operator |
|-------------------|----------------------|
| AND (Comparison)  | and                  |
| OR (Comparison)   | or                   |
| \>                | greater than         |
| <                 | less than            |
| =                 | equals               |
| LIKE              | contains             |
| IN                | equals               |
| MATCHES           | contains             |
| !=                | not equals           |
| OR (Observation)  | or                   |
| AND (Observation) | or                   |
| <br>              |                      |
### Searchable STIX objects and properties
| STIX Object and Property                                                           | Mapped Data Source Fields           |
|------------------------------------------------------------------------------------|-------------------------------------|
| **ipv4-addr**:value                                                                | Local IP Address, Remote IP Address |
| **ipv6-addr**:value                                                                | Local IP Address, Remote IP Address |
| **network-traffic**:src_port                                                       | Local Port                          |
| **network-traffic**:dst_port                                                       | Remote Port                         |
| **network-traffic**:src_ref.value                                                  | Local IP Address                    |
| **network-traffic**:dst_ref.value                                                  | Remote IP Address                   |
| **network-traffic**:extensions.'http-request-ext'.request_header.'Accept-Encoding' | HTTP Header                         |
| **network-traffic**:extensions.'http-request-ext'.request_header.'User-Agent'      | HTTP Header                         |
| **network-traffic**:extensions.'http-request-ext'.request_header.Host              | HTTP Header                         |
| **network-traffic**:extensions.'http-request-ext'.request_value                    | URL                                 |
| **process**:name                                                                   | Process Name,Parent Process Name    |
| **process**:command_line                                                           | Process Arguments                   |
| **process**:parent_ref.name                                                        | Parent Process Name                 |
| **process**:parent_ref.cwd                                                         | Parent Process Path                 |
| **process**:binary_ref.name                                                        | File Name                           |
| **process**:creator_user_ref.user_id                                               | Username                            |
| **file**:name                                                                      | File Name                           |
| **file**:hashes.MD5                                                                | File MD5 Hash                       |
| **file**:size                                                                      | Size in bytes                       |
| **file**:x_path                                                                    | File Full Path                      |
| **file**:parent_directory_ref.path                                                 | File Full Path                      |
| **directory**:path                                                                 | File Full Path                      |
| **user-account**:user_id                                                           | Username                            |
| **windows-registry-key**:key                                                       | Registry Key Full Path              |
| **windows-registry-key**:values[*].name                                            | Registry Key Value Name             |
| **windows-registry-key**:values[*].data                                            | Registry Key Value Text             |
| **domain-name**:value                                                              | DNS Hostname                        |
| **x-oca-event**:file_ref.name                                                      | File Name                           |
| **x-oca-event**:process_ref.name                                                   | Process Name, Parent Process Name   |
| **x-oca-event**:parent_process_ref.name                                            | Parent Process Name                 |
| **x-oca-event**:domain_ref.value                                                   | DNS Hostname                        |
| **x-oca-event**:registry_ref.key                                                   | Registry Key Full Path              |
| **x-oca-event**:network_ref.src_port                                               | Local Port                          |
| **x-oca-event**:ip_refs[*].value                                                   | Local IP Address, Remote IP Address |
| **x-oca-event**:user_ref.user_id                                                   | Username                            |

### Supported STIX Objects and Properties for Query Results
| STIX Object          | STIX Property                              | Data Source Field              |
|----------------------|--------------------------------------------|--------------------------------|
| domain-name          | value                                      | DNS Hostname                   |
| <br>                 |                                            |                                |
| ipv4-addr            | value                                      | Local IP Address               |
| ipv4-addr            | value                                      | Remote IP Address              |
| <br>                 |                                            |                                |
| ipv6-addr            | value                                      | Local IP Address               |
| ipv6-addr            | value                                      | Remote IP Address              |
| <br>                 |                                            |                                |
| network-traffic      | src_ref                                    | Local IP Address               |
| network-traffic      | dst_ref                                    | Remote IP Address              |
| network-traffic      | src_port                                   | Local Port                     |
| network-traffic      | dst_port                                   | Remote Port                    |
| network-traffic      | protocols                                  | Port Protocol                  |
| network-traffic      | extensions.http-request-ext.request_header | HTTP Header                    |
| network-traffic      | extensions.http-request-ext.request_value  | URL                            |
| network-traffic      | extensions.http-request-ext.request_method | HTTP Method                    |
| <br>                 |                                            |                                |
| process              | name                                       | Process Name                   |
| process              | name                                       | Parent Process Name            |
| process              | pid                                        | Process ID                     |
| process              | cwd                                        | Parent Process Path            |
| process              | command_line                               | Process Arguments              |
| process              | parent_ref                                 | Parent Process Path            |
| process              | parent_ref                                 | Parent Process Name            |
| process              | binary_ref                                 | File Name                      |
| process              | binary_ref                                 | Parent File Name               |
| process              | creator_user_ref                           | Username                       |
| process              | x_event_type                               | Process Event Type             |
| <br>                 |                                            |                                |
| artifact             | payload_bin                                | Write Event File Text Written  |
| <br>                 |                                            |                                |
| file                 | name                                       | File Name                      |
| file                 | name                                       | Write Event File Name          |
| file                 | name                                       | Parent File Name               |
| file                 | hashes.MD5                                 | File MD5 Hash                  |
| file                 | hashes.MD5                                 | Write Event File MD5 Hash      |
| file                 | size                                       | Size in bytes                  |
| file                 | size                                       | Write Event Size in bytes      |
| file                 | content_ref                                | Write Event File Text Written  |
| file                 | parent_directory_ref                       | File Full Path                 |
| file                 | parent_directory_ref                       | Write Event File Full Path     |
| file                 | x_path                                     | File Full Path                 |
| file                 | x_path                                     | Write Event File Full Path     |
| file                 | x_bytes_written                            | File Bytes Written             |
| file                 | x_bytes_written                            | Write Event File Bytes Written |
| <br>                 |                                            |                                |
| directory            | path                                       | File Full Path                 |
| directory            | path                                       | Write Event File Full Path     |
| <br>                 |                                            |                                |
| user-account         | user_id                                    | Username                       |
| <br>                 |                                            |                                |
| windows-registry-key | key                                        | Registry Key Full Path         |
| windows-registry-key | values                                     | Registry Key Values            |
| <br>                 |                                            |                                |
| x-oca-asset          | hostname                                   | Hostname                       |
| x-oca-asset          | device_id                                  | Host ID                        |
| x-oca-asset          | ip_refs                                    | Local IP Address               |
| x-oca-asset          | x_host_set                                 | Host Set                       |
| <br>                 |                                            |                                |
| x-oca-event          | action                                     | Event Type                     |
| x-oca-event          | start                                      | Timestamp - Started            |
| x-oca-event          | modified                                   | Timestamp - Modified           |
| x-oca-event          | created                                    | Timestamp - Event              |
| x-oca-event          | host_ref                                   | Hostname                       |
| x-oca-event          | user_ref                                   | Username                       |
| x-oca-event          | ip_refs                                    | Local IP Address               |
| x-oca-event          | ip_refs                                    | Remote IP Address              |
| x-oca-event          | network_ref                                | Remote Port                    |
| x-oca-event          | network_ref                                | Local Port                     |
| x-oca-event          | network_ref                                | Port Protocol                  |
| x-oca-event          | file_ref                                   | File Name                      |
| x-oca-event          | parent_process_ref                         | Parent Process Path            |
| x-oca-event          | parent_process_ref                         | Parent Process Name            |
| x-oca-event          | registry_ref                               | Registry Key Full Path         |
| x-oca-event          | domain_ref                                 | DNS Hostname                   |
| x-oca-event          | process_ref                                | Process Name                   |
| x-oca-event          | x_file_write_ref                           | Write Event File Name          |
| x-oca-event          | x_accessed_time                            | Timestamp - Accessed           |
| x-oca-event          | x_last_run                                 | Timestamp - Last Run           |
| <br>                 |                                            |                                |
