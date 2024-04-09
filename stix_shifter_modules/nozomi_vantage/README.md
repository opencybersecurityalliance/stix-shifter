# Nozomi

## Supported STIX Mappings

See the [table of mappings](nozomi_vantage_supported_stix.md) for the STIX objects and operators supported by this connector.


**Table of Contents**

- [Nozomi API Endpoints](#nozomi-api-endpoints)
- [Curl Command to test the API Endpoints](#curl-command-to-test-api-endpoints)
- [Format for calling stix-shifter from the command line](#format-for-calling-stix-shifter-from-the-command-line) 
- [Pattern expression with STIX and CUSTOM attributes - Single Observation](#single-observation)
- [Pattern expression with STIX and CUSTOM attributes - Multiple Observation](#multiple-observation)
- [STIX Execute Query](#stix-execute-query)
- [Types of Attributes](#types-of-attributes)
- [Limitations](#limitations)
- [Observations](#observations)
- [References](#references)
- [Appendix](#appendix)

### Nozomi API Endpoints
| Connector Method | Nozomi API Endpoint     | Method |
|-----|------|------|
| Ping Endpoint   | https://< server >/api/v1/health_logs | GET  | 
| Token Endpoint  | https://< server >/api/v1/keys/sign_in  | POST  |
| Results Endpoint | https://< server >/api/open/query/do?  | GET  |


### CURL command to test API Endpoints
#### Ping 
```
curl -k -H “Authorization: Bearer <Bearer_Token>” https://<server>/api/v1/health_logs
```
#### Token
```
curl -k -H POST https://<server/api/v1/keys/sign_in -d {"key_name":"<key_name>","key_token": "<key_token>"}
```
#### Results
```
curl -k -H “Authorization: Bearer <Bearer_Token>” https://<server>/api/open/query/do?query=alerts
```

### Format for calling stix-shifter from the command line
```
python main.py `<translator_module>` `<query or result>` `<STIX identity object>` `<data>`
```
### Pattern expression with STIX and CUSTOM attributes

#### Single Observation

#### STIX Translate query to fetch the messages from a specific ipaddress
```shell
translate nozomi_vantage query {} "[ipv4-addr:value='1.1.1.1'] START t'2024-01-01T11:00:00.000Z' STOP t'2024-01-10T00:00:00.000Z'"
```
#### STIX Translate query - output
```json
{
    "queries": [
        "query=alerts | where ip_src==\"1.1.1.1\" OR ip_dst==\"1.1.1.1\" | where record_created_at>=1704106800000 | where record_created_at<=1704844800000"
    ]
}
```

#### STIX Transmit results 

```shell
transmit nozomi_vantage "{\"host\":\"nozomi-server.vantage.nozominetworks.io\", \"port\":443}" "{\"auth\":{\"key_name\":\"KEY NAME\", \"key_token\":\"KEY TOKEN\"}}" results "query=alerts | where ip_src==\"1.1.1.1\" OR ip_dst==\"1.1.1.1\" | where record_created_at>=1704106800000 | where record_created_at<=1704844800000"
0
1
```

#### STIX Transmit results - output
```json
{
    "success": true,
    "data": [
        {
            "id": "e2836408-55da-5d90-9601-398c1044ef16",
            "time": 1704791849000,
            "name": "Malformed traffic",
            "type_name": "Malformed traffic",
            "threat_name": "",
            "counter": 1,
            "description": "The UDP header in the packet contains a wrong data length. 1404 bytes are advertised, but 1380 bytes are found in the payload.",
            "ack": false,
            "note": null,
            "risk": 7.0,
            "id_src": "1.1.1.1",
            "id_dst": "2.2.2.2",
            "ip_src": "1.1.1.1",
            "ip_src:info": null,
            "ip_dst": "2.2.2.2",
            "ip_dst:info": null,
            "status": "open",
            "mac_src": "01:01:01:01:01:01",
            "mac_dst": "02:02:02:02:02:02",
            "port_dst": null,
            "port_src": null,
            "protocol": "",
            "transport_protocol": "unknown",
            "severity": 10,
            "zone_dst": "Broadcast",
            "zone_src": "PlantSmartDevices",
            "dst_roles": "other",
            "src_roles": "other",
            "label_dst": null,
            "label_src": null,
            "bpf_filter": "(ip host 1.1.1.1 and ip host 2.2.2.2) or (vlan and ip host 1.1.1.1 and ip host 2.2.2.2)",
            "properties": {
                "base_risk": 7.0,
                "raised_by": "n2os_ids",
                "is_dst_public": false,
                "is_src_public": false,
                "is_dst_node_learned": true,
                "is_src_node_learned": true,
                "mitre_attack_for_ics": {
                    "source": {
                        "levels": [
                            "2"
                        ]
                    }
                },
                "is_dst_reputation_bad": false,
                "is_src_reputation_bad": false,
                "mitre_attack_enterprise": {
                    "techniques": [
                        {
                            "id": "T1565",
                            "name": "Data Manipulation",
                            "tactic": "Impact"
                        }
                    ]
                },
                "incident_key_confidence:AnomalousPacket": 1.0
            },
            "closed_time": 0,
            "close_option": null,
            "is_incident": false,
            "is_security": true,
            "created_time": 1704791849000,
            "trigger_type": null,
            "capture_device": "em1",
            "sec_profile_visible": true,
            "grouped_visible": true,
            "mitre_attack_techniques": null,
            "mitre_attack_tactics": null,
            "playbook_contents": null,
            "trace_status": null,
            "appliance_host": "Demo Sensor standard 4959963c",
            "appliance_ip": null,
            "record_created_at": 1704796703262,
            "sensor:host": null,
            "site:name": null,
            "type_id": "SIGN:MALFORMED-TRAFFIC",
            "trigger_id": "udp.wrong-length"
        }
    ]
}
```


#### STIX Translate results

```json
{
    "type": "bundle",
    "id": "bundle--5f349bae-07c6-4bef-9f64-24e0c9bd0297",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "Nozomi",
            "identity_class": "events",
            "created": "2023-04-11T16:11:11.878Z",
            "modified": "2023-04-11T16:11:11.878Z"
        },
        {
            "id": "observed-data--bcbed7af-3cfb-4017-88ce-b33256a0fb26",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2024-01-22T10:53:54.953Z",
            "modified": "2024-01-22T10:53:54.953Z",
            "objects": {
                "0": {
                    "type": "x-ibm-finding",
                    "alert_id": "e2836408-55da-5d90-9601-398c1044ef16",
                    "time_observed": "2024-01-09T09:17:29.000Z",
                    "name": "Malformed traffic",
                    "finding_type": "alert",
                    "description": "The UDP header in the packet contains a wrong data length. 1404 bytes are advertised, but 1380 bytes are found in the payload.",
                    "x_is_acknowledged": false,
                    "severity": 70,
                    "src_ip_ref": "1",
                    "dst_ip_ref": "3",
                    "x_alert_status": "open",
                    "ttp_tagging_refs": [
                        "8"
                    ],
                    "x_is_incident_alert": false,
                    "x_is_cybersecurity_alert": true,
                    "start": "2024-01-09T09:17:29.000Z",
                    "x_sensor_interface": "em1",
                    "x_sensor_host": "Demo Sensor standard 4959963c",
                    "x_alert_type_id": "SIGN:MALFORMED-TRAFFIC",
                    "x_rule_id": "udp.wrong-length"
                },
                "1": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1",
                    "resolves_to_refs": [
                        "4"
                    ],
                    "x_nozomi_info_ref": "7"
                },
                "2": {
                    "type": "network-traffic",
                    "src_ref": "1",
                    "dst_ref": "3",
                    "protocols": [
                        "tcp"
                    ]
                },
                "3": {
                    "type": "ipv4-addr",
                    "value": "2.2.2.2",
                    "resolves_to_refs": [
                        "5"
                    ],
                    "x_nozomi_info_ref": "6"
                },
                "4": {
                    "type": "mac-addr",
                    "value": "01:01:01:01:01:01",
                    "x_nozomi_info_ref": "7"
                },
                "5": {
                    "type": "mac-addr",
                    "value": "02:02:02:02:02:02",
                    "x_nozomi_info_ref": "6"
                },
                "6": {
                    "type": "x-nozomi-info",
                    "zone": "Broadcast",
                    "roles": "other",
                    "is_public": false,
                    "is_node_learned": true,
                    "is_reputation_bad": false
                },
                "7": {
                    "type": "x-nozomi-info",
                    "zone": "PlantSmartDevices",
                    "roles": "other",
                    "is_public": false,
                    "is_node_learned": true,
                    "is_reputation_bad": false
                },
                "8": {
                    "type": "x-ibm-ttp-tagging",
                    "extensions": {
                        "mitre-attack-ext": {
                            "technique_id": "T1565",
                            "technique_name": "Data Manipulation",
                            "tactic_name": "Impact"
                        }
                    },
                    "name": "Data Manipulation",
                    "kill_chain_phases": [
                        {
                            "kill_chain_name": "mitre-attack",
                            "phase_name": "Impact"
                        }
                    ]
                }
            },
            "first_observed": "2024-01-22T10:53:54.953Z",
            "last_observed": "2024-01-22T10:53:54.953Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```

#### Multiple Observation

```shell
translate 
nozomi_vantage 
query {} 
"[(ipv4-addr:value = '1.1.1.1' AND network-traffic:dst_port == 22) OR network-traffic:protocols[*] == 'ssh'] START t'2024-01-01T00:00:00.000Z' STOP t'2024-01-16T11:54:00.000Z'"
```

#### STIX Multiple observation - output
```json
{
   "queries": [
        "query=alerts | where protocol==\"ssh\" OR transport_protocol==\"ssh\" OR port_dst==\"22\" | where protocol==\"ssh\" OR transport_protocol==\"ssh\" OR ip_src==\"1.1.1.1\" OR ip_dst==\"1.1.1.1\" | where record_created_at>=1704067200000 | where record_created_at<=1705406040000"
    ]
}
```

### STIX Execute query
```shell
execute 
nozomi_vantage 
nozomi_vantage 
"{\"type\":\"identity\",\"id\":\"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\",\"name\":\"Nozomi Vantage\",\"identity_class\":\"events\", \"created\": \"2023-04-11T16:11:11.878Z\",\"modified\": \"2023-04-11T16:11:11.878Z\"}" 
"{\"host\":\"nozomi-server.vantage.nozominetworks.io\", \"port\":443}" 
"{\"auth\":{\"key_name\":\"KEY NAME\", \"key_token\":\"KEY TOKEN\"}}" 
"[(ipv4-addr:value = '1.1.1.1' AND network-traffic:dst_port == 22) OR network-traffic:protocols[*] == 'ssh'] START t'2024-01-01T00:00:00.000Z' STOP t'2024-01-16T11:54:00.000Z'"
```

#### STIX Execute query - output
```json
{
    "type": "bundle",
    "id": "bundle--32c21e05-a8db-4247-8ae2-5f456d8714f8",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "Nozomi Vantage",
            "identity_class": "events",
            "created": "2023-04-11T16:11:11.878Z",
            "modified": "2023-04-11T16:11:11.878Z"
        },
        {
            "id": "observed-data--7b5e8c30-eee5-4d45-981f-f48cbcbb6097",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2024-01-22T11:59:09.665Z",
            "modified": "2024-01-22T11:59:09.665Z",
            "objects": {
                "0": {
                    "type": "x-ibm-finding",
                    "alert_id": "d2831312-17a9-53f2-b394-059e1de2202f",
                    "time_observed": "2024-01-09T09:19:33.000Z",
                    "name": "New global MAC vendor",
                    "finding_type": "alert",
                    "description": "A new Private MAC Address has been found in the network -- 02:02:02:02:02:02",
                    "x_is_acknowledged": false,
                    "severity": 50,
                    "src_ip_ref": "1",
                    "dst_ip_ref": "3",
                    "x_alert_status": "open",
                    "ioc_refs": [
                        "8"
                    ],
                    "ttp_tagging_refs": [
                        "9"
                    ],
                    "x_is_incident_alert": false,
                    "x_is_cybersecurity_alert": true,
                    "start": "2024-01-09T09:19:33.000Z",
                    "x_sensor_interface": "em1",
                    "x_sensor_host": "Demo Sensor standard 4959963c",
                    "x_alert_type_id": "VI:GLOBAL:NEW-MAC-VENDOR"
                },
                "1": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1",
                    "resolves_to_refs": [
                        "4"
                    ],
                    "x_nozomi_info_ref": "7"
                },
                "2": {
                    "type": "network-traffic",
                    "src_ref": "1",
                    "dst_ref": "3",
                    "dst_port": 22,
                    "src_port": 49739,
                    "protocols": [
                        "ssh",
                        "tcp"
                    ]
                },
                "3": {
                    "type": "ipv4-addr",
                    "value": "2.2.2.2",
                    "resolves_to_refs": [
                        "5"
                    ],
                    "x_nozomi_info_ref": "6"
                },
                "4": {
                    "type": "mac-addr",
                    "value": "01:01:01:01:01:01",
                    "x_nozomi_info_ref": "7"
                },
                "5": {
                    "type": "mac-addr",
                    "value": "02:02:02:02:02:02",
                    "x_nozomi_info_ref": "6"
                },
                "6": {
                    "type": "x-nozomi-info",
                    "zone": "ProdNet-A",
                    "roles": "producer",
                    "label": "label.com",
                    "is_public": false,
                    "is_node_learned": true,
                    "is_reputation_bad": false
                },
                "7": {
                    "type": "x-nozomi-info",
                    "zone": "ProdNet-A",
                    "roles": "consumer",
                    "is_public": false,
                    "is_node_learned": true,
                    "is_reputation_bad": false
                },
                "8": {
                    "type": "mac-addr",
                    "value": "02:02:02:02:02:02"
                },
                "9": {
                    "type": "x-ibm-ttp-tagging",
                    "extensions": {
                        "mitre-attack-ext": {
                            "technique_id": "T1200",
                            "technique_name": "Hardware Additions",
                            "tactic_name": "Initial Access"
                        }
                    },
                    "name": "Hardware Additions",
                    "kill_chain_phases": [
                        {
                            "kill_chain_name": "mitre-attack",
                            "phase_name": "Initial Access"
                        }
                    ]
                }
            },
            "first_observed": "2024-01-22T11:59:09.665Z",
            "last_observed": "2024-01-22T11:59:09.665Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```
### Types of Attributes

| Type                      | Description                                | Example                                                                                                            |
|---------------------------|--------------------------------------------|--------------------------------------------------------------------------------------------------------------------|
| Dictionary fields         | A key value pair attributes.               | {"type_name": "Malformed traffic"}, {""severity": 10}                                                              |
| List of dictionary fields | A list containing one or more dictionaries | "techniques": [{"id": "T1200", "name": "Hardware Additions"},{"id": "T1071","name": "Application Layer Protocol"}] |

### Observations
- Operators ==, !=  for some fields are translated to include?, !include?.(For example: x-ibm-ttp-tagging:name, process:parent_ref.binary_ref.name)
   Example: [x-ibm-ttp-tagging:name != 'Execution'] translates to query=alerts | where properties !include? \"Execution\"
- The JWT token expires 30 minutes after being created.
- It is observed that Nozomi API fails if translated query string length is more than MAX_QUERY_LENGTH. To avoid this failure, query is split at 'OR' conditions and multiple requests are made to Nozomi to get the result. However, the part of query joined by 'AND' operator won't be split and 'Query length is too long or Invalid Query' error is returned if the length of that part is beyond MAX_QUERY_LENGTH.


### Limitations
- The page param is the page number to return, and count is the page dimension. If count is not provided, the default value is 10,000; if page is not provided, the default page number is 1.
- If the provided count value is higher than 10,000, no more than 10,000 items are returned.
- The maximum allowable page number is 1,000. Requests for pages beyond this limit will result in an error response Bad request.

### References
- [API Documentation](https://technicaldocs.nozominetworks.com/products/n2os/sdk/open-api-index.html)
- [Query endpoint](https://technicaldocs.nozominetworks.com/products/n2os/sdk/open-api-query.html)

### Appendix
List of fields that is available in schema of Nozomi alert logs

| Data source Field                                    | Data Type                | Mapped STIX field                                                                                             |
|------------------------------------------------------|--------------------------|---------------------------------------------------------------------------------------------------------------|
| ip_dst                                               | Dictionary field         | ipv4-addr:value,ipv6-addr:value,network-traffic:dst_ref,x-ibm-finding:dst_ip_ref                              |
| mac_src                                              | Dictionary field         | mac-addr:value,network-traffic:src_ref,ipv4-addr:resolves_to_refs                                             |
| mac_dst                                              | Dictionary field         | mac-addr:value,network-traffic:dst_ref,ipv4-addr:resolves_to_refs                                             |
| port_dst                                             | Dictionary field         | network-traffic:dst_port                                                                                      | 
| port_src                                             | Dictionary field         | network-traffic:src_port                                                                                      | 
| protocol                                             | Dictionary field         | network-traffic:protocols                                                                                     | 
| transport_protocol                                   | Dictionary field         | network-traffic:protocols                                                                                     |
| id                                                   | Dictionary field         | x-ibm-finding:alert_id                                                                                        |
| time                                                 | Dictionary field         | x-ibm-finding:time_observed,first_observed,last_observed                                                      |
| type_name                                            | Dictionary field         | x-ibm-finding:name                                                                                            | 
| description                                          | Dictionary field         | x-ibm-finding:description                                                                                     |
| risk                                                 | Dictionary field         | x-ibm-finding:severity                                                                                        | 
| created_time                                         | Dictionary field         | x-ibm-finding:start                                                                                           | 
| closed_time                                          | Dictionary field         | x-ibm-finding:end                                                                                             | 
| type_id                                              | Dictionary field         | x-ibm-finding:x_alert_type_id                                                                                 | 
| is_security                                          | Dictionary field         | x-ibm-finding:x_is_cybersecurity_alert                                                                        | 
| is_incident                                          | Dictionary field         | x-ibm-finding:x_is_incident_alert                                                                             | 
| appliance_host                                       | Dictionary field         | x-ibm-finding:x_sensor_host                                                                                   | 
| capture_device                                       | Dictionary field         | x-ibm-finding:x_sensor_interface                                                                              | 
| threat_name                                          | Dictionary field         | x-ibm-finding:x_threat_name,x-ibm-finding:finding_type                                                        |
| trigger_id                                           | Dictionary field         | x-ibm-finding:x_rule_id                                                                                       | 
| trigger_type                                         | Dictionary field         | x-ibm-finding:rule_names                                                                                      | 
| zone_dst                                             | Dictionary field         | x-nozomi-info:zone,ipv4-addr:x_nozomi_info_ref                                                                |
| zone_src                                             | Dictionary field         | x-nozomi-info:zone,ipv4-addr:x_nozomi_info_ref                                                                |
| dst_roles                                            | Dictionary field         | x-nozomi-info:roles                                                                                           | 
| src_roles                                            | Dictionary field         | x-nozomi-info:roles                                                                                           | 
| label_src                                            | Dictionary field         | x-nozomi-info:label                                                                                           | 
| label_dst                                            | Dictionary field         | x-nozomi-info:label                                                                                           | 
| ack                                                  | Dictionary field         | x-ibm-finding:x_is_acknowledged                                                                               | 
| status                                               | Dictionary field         | x-ibm-finding:x_alert_status                                                                                  | 
| note                                                 | Dictionary field         | x-ibm-finding:x_user_note                                                                                     | 
| properties/cause                                     | Dictionary field         | x-ibm-finding:x_cause                                                                                         | 
| properties/victims                                   | Dictionary field         | ipv4-addr:value,ipv6-addr:value,x-ibm-finding:ioc_refs                                                        |
| properties/solution                                  | Dictionary field         | x-ibm-finding:x_solution                                                                                      | 
| properties/bad_actor                                 | Dictionary field         | mac-addr:value,x-ibm-finding:ioc_refs                                                                         |
| properties/message                                   | Dictionary field         | x-ibm-finding:x_message                                                                                       | 
| properties/cve_references                            | Dictionary field         | x-ibm-finding:x_cve_references                                                                                | 
| properties/is_dst_public                             | Dictionary field         | x-nozomi-info:is_public,ipv4-addr:x_nozomi_info_ref                                                           |
| properties/is_src_public                             | Dictionary field         | x-nozomi-info:is_public,ipv4-addr:x_nozomi_info_ref                                                           |
| properties/is_dst_node_learned                       | Dictionary field         | x-nozomi-info:is_node_learned,ipv4-addr:x_nozomi_info_ref,mac-addr:x_nozomi_info_ref                          |
| properties/is_src_node_learned                       | Dictionary field         | x-nozomi-info:is_node_learned,ipv4-addr:x_nozomi_info_ref,mac-addr:x_nozomi_info_ref                          |
| properties/is_dst_reputation_bad                     | Dictionary field         | x-nozomi-info:is_reputation_bad                                                                               | 
| properties/is_src_reputation_bad                     | Dictionary field         | x-nozomi-info:is_reputation_bad                                                                               | 
| properties/src_is_an_attacker                        | Dictionary field         | x-nozomi-info:is_an_attacker                                                                                  | 
| properties/network_learnable                         | Dictionary field         | x-ibm-finding:x_network_learnable                                                                             | 
| properties/process/pid                               | Dictionary field         | process:pid                                                                                                   | 
| properties/process/user                              | Dictionary field         | user-account:user_id,process:creator_user_ref                                                                 |
| properties/process/image_path                        | Dictionary field         | directory:path,file:name,file:parent_directory_ref,process:binary_ref,x-ibm-finding:ioc_refs                  |
| properties/process/command_line                      | Dictionary field         | process:command_line                                                                                          | 
| properties/process/image_hash_sha256                 | Dictionary field         | file:hashes:SHA-256                                                                                           | 
| properties/process/ancestry                          | Dictionary field         | directory:path,file:name,file:parent_directory_ref,process:command_line,process:binary_ref,process:parent_ref |
| properties/mitre_attack_enterprise/techniques/id     | List of Dictionary field | x-ibm-ttp-tagging:extensions:mitre-attack-ext:technique_id                                                    | 
| properties/mitre_attack_enterprise/techniques/name   | List of Dictionary field | x-ibm-ttp-tagging:extensions:mitre-attack-ext:technique_name,x-ibm-ttp-tagging:name                           |
| properties/mitre_attack_enterprise/techniques/tactic | List of Dictionary field | x-ibm-ttp-tagging:extensions:mitre-attack-ext:tactic_name,x-ibm-ttp-tagging:kill_chain_phases                 |
| properties/mitre_attack_for_ics/techniques/id        | List of Dictionary field | x-ibm-ttp-tagging:extensions:mitre-attack-ext:technique_id                                                    |
| properties/mitre_attack_for_ics/techniques/name      | List of Dictionary field | x-ibm-ttp-tagging:extensions:mitre-attack-ext:technique_name,x-ibm-ttp-tagging:name                           |
| properties/mitre_attack_for_ics/techniques/tactic    | List of Dictionary field | x-ibm-ttp-tagging:extensions:mitre-attack-ext:tactic_name,x-ibm-ttp-tagging:kill_chain_phases                 |
| properties/details_hash_MD5/value                    | Dictionary field         | file:hashes:MD5                                                                                               | 
| properties/details_hash_SHA256/value                 | Dictionary field         | file:hashes:SHA-256                                                                                           | 
| properties/details_hash_SHA1/value                   | Dictionary field         | file:hashes:SHA-1                                                                                             | 
| properties/details_yara_file/value                   | Dictionary field         | file:name,x-ibm-finding:ioc_refs                                                                              |
| properties/details_file_size/value                   | Dictionary field         | file:size                                                                                                     | 