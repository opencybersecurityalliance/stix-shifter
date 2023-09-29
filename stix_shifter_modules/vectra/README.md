# Vectra NDR Connector

**Table of Contents**

- [Vectra NDR API Endpoints](#Vectra NDR-api-endpoints)
- [Pattern expression with STIX and CUSTOM attributes - Single Observation](#single-observation)
- [Pattern expression with STIX and CUSTOM attributes - Multiple Observation](#multiple-observation)
- [STIX Execute Query](#stix-execute-query)
- [Limitations](#limitations)
- [Observations](#observations)
- [References](#references)

### Vectra NDR API Endpoints

   | Connector Method | Vectra NDR API Endpoint     | Method |
   |-----|------|   ------|
   | Ping Endpoint   | https://< server >/api/v2.4/health/connectivity | GET  | 
   | Results Endpoint | https://< server >/api/v2.4/search/detections  | GET  |

### Format for calling stix-shifter from the command line
```
python main.py `<translator_module>` `<query or result>` `<STIX identity object>` `<data>`
```
### Pattern expression with STIX and CUSTOM attributes

#### Single Observation

#### STIX Translate query to fetch the Hidden HTTP Tunnel detection on a specific ipaddress
```shell
translate vectra query {} "[ipv4-addr:value='1.1.1.1' AND x-ibm-finding:name='Hidden HTTP Tunnel'] START t'2023-06-01T00:00:00.000Z' STOP t'2023-06-12T00:00:00.000Z'"
```
#### STIX Translate query - output
```json
{
    "queries": [
        "query_string=(detection.detection:\"Hidden HTTP Tunnel\" AND (detection.src_ip:\"1.1.1.1\" OR detection.grouped_details.dst_ips:\"1.1.1.1\" OR detection.grouped_details.dst_hosts.dst_ip:\"1.1.1.1\" OR detection.grouped_details.origin_ip:\"1.1.1.1\" OR detection.grouped_details.sessions.dst_ip:\"1.1.1.1\" OR detection.grouped_details.subnet:\"1.1.1.1\" OR detection.grouped_details.event.dst_ip:\"1.1.1.1\" OR detection.grouped_details.event.dst_ips:\"1.1.1.1\" OR detection.grouped_details.events.sessions.dst_ip:\"1.1.1.1\" OR detection.grouped_details.connection_events.target_host.ip:\"1.1.1.1\") AND (detection.last_timestamp:[2023-06-01T0000 to 2023-06-12T0000]))"
    ]
}

```

#### STIX Transmit results 

```shell
transmit 
vectra 
"{\"host\":\"instance.vectra.com\", \"port\":xxxx}" 
"{\"auth\":{\"apitoken\": \"xxxx\"}}" 
results 
"[query_string=(detection.detection_type:\"Hidden HTTP Tunnel\" AND (detection.src_ip:\"1.1.1.1\" OR detection.grouped_details.dst_ips:\"1.1.1.1\" OR detection.grouped_details.dst_hosts.dst_ip:\"1.1.1.1\" OR detection.grouped_details.origin_ip:\"1.1.1.1\" OR detection.grouped_details.sessions.dst_ip:\"1.1.1.1\" OR detection.grouped_details.subnet:\"1.1.1.1\" OR detection.grouped_details.events.dst_ip:\"1.1.1.1\" OR detection.grouped_details.events.dst_ips:\"1.1.1.1\" OR detection.grouped_details.events.sessions.dst_ip:\"1.1.1.1\" OR detection.grouped_details.connection_events.target_host.ip:\"1.1.1.1\") AND (detection.last_timestamp:[2023-04-01T0000 to 2023-06-12T0000]))]"
0
1
```

#### STIX Transmit results - output
```json
{
    "success": true,
    "data": [
        {
            "id": 13660,
            "category": "COMMAND & CONTROL",
            "detection": "Hidden HTTP Tunnel",
            "detection_category": "COMMAND & CONTROL",
            "detection_type": "Hidden HTTP Tunnel",
            "custom_detection": null,
            "description": null,
            "src_ip": "1.1.1.1",
            "state": "inactive",
            "certainty": 0,
            "threat": 0,
            "created_timestamp": "2023-04-04T02:25:19Z",
            "first_timestamp": "2023-04-04T02:12:42Z",
            "last_timestamp": "2023-04-04T02:23:32Z",
            "targets_key_asset": false,
            "is_targeting_key_asset": false,
            "src_account": null,
            "src_host": {
                "id": 872,
                "ip": "1.1.1.1",
                "name": "VMAL #2 windows 1.1.1.1 (higaki-ha11)",
                "is_key_asset": false,
                "groups": [
                    {
                        "id": 145,
                        "name": "Super Test domain group",
                        "description": "created during API testing",
                        "last_modified": "2022-08-03T15:33:04Z",
                        "last_modified_by": "reliaquest",
                        "type": "host"
                    },
                    {
                        "id": 144,
                        "name": "Partner VLAB - User Devices",
                        "description": "",
                        "last_modified": "2022-01-27T12:05:24Z",
                        "last_modified_by": "user (Removed)",
                        "type": "ip"
                    }
                ],
                "threat": 82,
                "certainty": 71
            },
            "note": null,
            "note_modified_by": null,
            "note_modified_timestamp": null,
            "sensor": "eti2pc2s",
            "sensor_name": "Vec2c610896102c466a28f49a",
            "tags": [],
            "triage_rule_id": null,
            "assigned_to": "vectra_sir_admin",
            "assigned_date": "2022-12-14T06:59:22Z",
            "groups": [
                {
                    "id": 144,
                    "name": "Partner VLAB - User Devices",
                    "description": "",
                    "type": "ip",
                    "last_modified": "2022-01-27T12:05:24Z",
                    "last_modified_by": "user"
                }
            ],
            "is_marked_custom": false,
            "is_custom_model": false,
            "src_linked_account": null,
            "grouped_details": [
                {
                    "description": null,
                    "dst_geo": null,
                    "dst_geo_lat": null,
                    "dst_geo_lon": null,
                    "first_timestamp": "2023-04-04T02:12:42Z",
                    "last_timestamp": "2023-04-04T02:23:32Z",
                    "flex_json": {},
                    "detection_guid": null,
                    "distilled_context": {},
                    "sequence_id": null,
                    "is_host_detail": true,
                    "is_account_detail": false,
                    "account_uid": null,
                    "account_detection": null,
                    "host_detection": 13660,
                    "accounts": [],
                    "target_domains": [],
                    "dst_ports": [
                        80
                    ],
                    "protocol": "tcp",
                    "bytes_received": 336025,
                    "bytes_sent": 2699,
                    "dst_ips": [
                        "2.2.2.2"
                    ],
                    "src_ip": "1.1.1.1",
                    "num_sessions": 197
                }
            ],
            "summary": {
                "bytes_received": 336025,
                "bytes_sent": 2699,
                "dst_ips": [
                    "2.2.2.2"
                ],
                "dst_ports": [
                    80
                ],
                "num_sessions": 197
            },
            "campaign_summaries": [],
            "is_triaged": false,
            "filtered_by_ai": false,
            "filtered_by_user": false,
            "filtered_by_rule": false,
            "_doc_modified_ts": "2023-06-08T06:21:44.371724"
        }
    ]
}
```


#### STIX Translate results

```json
{
    "type": "bundle",
    "id": "bundle--828a180e-a942-4102-b62a-6e524f62c97d",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "vectra",
            "identity_class": "events",
            "created": "2022-04-11T16:11:11.878Z",
            "modified": "2022-04-11T16:11:11.878Z"
        },
        {
            "id": "observed-data--d72f6317-6771-4980-a33d-e773bb4cb94c",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2023-06-08T07:55:56.262Z",
            "modified": "2023-06-08T07:55:56.262Z",
            "objects": {
                "0": {
                    "type": "x-ibm-finding",
                    "alert_id": 13660,
                    "ttp_tagging_refs": [
                        "1"
                    ],
                    "name": "Hidden HTTP Tunnel",
                    "finding_type": "alert",
                    "src_ip_ref": "2",
                    "x_state": "inactive",
                    "confidence": 0,
                    "severity": 0,
                    "time_observed": "2023-04-04T02:25:19Z",
                    "start": "2023-04-04T02:12:42Z",
                    "end": "2023-04-04T02:23:32Z",
                    "x_sensor_name": "Vec2c610896102c466a28f49a",
                    "x_assigned_to": "vectra_sir_admin",
                    "x_assigned_date": "2022-12-14T06:59:22Z",
                    "ioc_refs": [
                        "5"
                    ],
                    "x_dst_ports": [
                        80
                    ],
                    "x_is_triaged": false
                },
                "1": {
                    "type": "x-ibm-ttp-tagging",
                    "kill_chain_phases": {
                        "kill_chain_name": "mitre-attack",
                        "phase_name": "COMMAND & CONTROL"
                    },
                    "name": "Hidden HTTP Tunnel",
                    "confidence": 0.0
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "3": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "2"
                    ],
                    "device_id": 872,
                    "hostname": "VMAL #2 windows 1.1.1.1 (higaki-ha11)",
                    "x_is_key_asset": false,
                    "x_threat": 82,
                    "x_certainty": 71
                },
                "4": {
                    "type": "network-traffic",
                    "start": "2023-04-04T02:12:42Z",
                    "end": "2023-04-04T02:23:32Z",
                    "dst_port": 80,
                    "protocols": [
                        "tcp"
                    ],
                    "dst_byte_count": 336025,
                    "src_byte_count": 2699,
                    "dst_ref": "5",
                    "src_ref": "2",
                    "x_num_sessions": 197
                },
                "5": {
                    "type": "ipv4-addr",
                    "value": "2.2.2.2"
                }
            },
            "first_observed": "2023-06-08T07:55:56.262Z",
            "last_observed": "2023-06-08T07:55:56.262Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}

```

#### Multiple Observation

```shell
translate vectra query {} "([x-ibm-finding:confidence>20 AND x-sql-request-info:response_code=404] AND [x-ibm-finding:severity>20 AND x-sql-request-info:user_agent LIKE 'Mozilla']) START t'2023-04-01T00:00:00.000Z' STOP t'2023-06-12T00:00:00.000Z'"
```

#### STIX Multiple observation - output
```json
{
   "queries": [
      "query_string=(detection.grouped_details.targets.events.response_code:\"404\" AND detection.certainty:>\"20\" AND (detection.last_timestamp:[2023-04-01T0000 to 2023-06-12T0000])) OR (detection.grouped_details.targets.events.user_agent:Mozilla AND detection.threat:>\"20\" AND (detection.last_timestamp:[2023-04-01T0000 to 2023-06-12T0000]))"
   ]
}
```

### STIX Execute query
```shell
execute
vectra
vectra
"{\"type\":\"identity\",\"id\":\"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\",\"name\":\"Vectra NDR\",\"identity_class\":\"system\",\"created\":\"2023-02-23T13:22:50.336Z\",\"modified\":\"2022-02-23T13:22:50.336Z\"}"
"{\"host\":\"xyz\", \"port\":xxxx}"
"{\"auth\":{\"api_token\": \"xxx\"}}"
"([x-ibm-finding:confidence>20 AND x-sql-request-info:response_code=404] AND [x-ibm-finding:severity>20 AND x-sql-request-info:user_agent LIKE 'Mozilla']) START t'2023-04-01T00:00:00.000Z' STOP t'2023-06-12T00:00:00.000Z'"
```

#### STIX Execute query - output
```json
{
    "type": "bundle",
    "id": "bundle--a819ae5e-d4ab-451c-b460-eee6ccf972aa",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "vectra",
            "identity_class": "events",
            "created": "2022-04-11T16:11:11.878Z",
            "modified": "2022-04-11T16:11:11.878Z"
        },
        {
            "id": "observed-data--d873c3cd-60fb-4ae8-9434-9bb15eda17e5",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2023-06-08T09:43:45.729Z",
            "modified": "2023-06-08T09:43:45.729Z",
            "objects": {
                "0": {
                    "type": "x-ibm-finding",
                    "alert_id": 13733,
                    "ttp_tagging_refs": [
                        "1"
                    ],
                    "name": "SQL Injection Activity",
                    "finding_type": "alert",
                    "src_ip_ref": "2",
                    "x_state": "active",
                    "confidence": 89,
                    "severity": 47,
                    "time_observed": "2023-06-06T10:12:30Z",
                    "start": "2023-06-06T10:11:12Z",
                    "end": "2023-06-06T10:51:20Z",
                    "x_sensor_name": "Vec2c610896a94728f49a",
                    "ioc_refs": [
                        "5"
                    ],
                    "x_is_triaged": false
                },
                "1": {
                    "type": "x-ibm-ttp-tagging",
                    "kill_chain_phases": {
                        "kill_chain_name": "mitre-attack",
                        "phase_name": "LATERAL MOVEMENT"
                    },
                    "name": "SQL Injection Activity",
                    "confidence": 0.89
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "3": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "2"
                    ],
                    "device_id": 1710,
                    "hostname": "dogrady150",
                    "x_is_key_asset": false,
                    "x_threat": 84,
                    "x_certainty": 82
                },
                "4": {
                    "type": "network-traffic",
                    "start": "2023-06-06T10:11:12Z",
                    "end": "2023-06-06T10:51:20Z",
                    "dst_ref": "5",
                    "src_ref": "2",
                    "x_sql_request_info_refs": [
                        "6",
                        "7"
                    ],
                    "dst_byte_count": 2766,
                    "src_byte_count": 598,
                    "protocols": [
                        "tcp"
                    ]
                },
                "5": {
                    "type": "ipv4-addr",
                    "value": "2.2.2.2"
                },
                "6": {
                    "type": "x-sql-request-info",
                    "http_segment": "/testing.asp?id=1+and+1=%28select%20%27MROwxCvP%27%2b%40%40servername%2b%27DEXMymnrh%27%29;--",
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36 Edg/97.0.1072.69",
                    "sql_fragment": "1 and 1=(select 'MROwxCvP'+@@servername+'DEXMymnrh');--",
                    "response_code": "404",
                    "bytes_received": 1383,
                    "last_seen": "2023-06-06T10:51:20Z"
                },
                "7": {
                    "type": "x-sql-request-info",
                    "http_segment": "/testing.asp?id=1+and+1=%28select%20%27UJCfFWifx%27%2b%40%40servername%2b%27vIHAyYiH%27%29;--",
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36 Edg/97.0.1072.69",
                    "sql_fragment": "1 and 1=(select 'UJCfFWifx'+@@servername+'vIHAyYiH');--",
                    "response_code": "404",
                    "bytes_received": 1383,
                    "last_seen": "2023-06-06T10:11:12Z"
                }
            },
            "first_observed": "2023-06-08T09:43:45.729Z",
            "last_observed": "2023-06-08T09:43:45.729Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```

### Limitations
- Detections are stored in Detect for Network and searchable for 180 days.
- It is observed that Vectra API returns 'Query too long' error if translated query string length is more than MAX_QUERY_LENGTH. To avoid this error, query is split at 'OR' conditions and multiple requests are made to vectra to get the result. However, the part of query joined by 'AND' operator won't be split and 'Query too long' error is returned if the length of that part is beyond MAX_QUERY_LENGTH.
- Operator 'NOT' is applicable to string type fields only.
- Operators 'LIKE' and 'MATCH' doesn't work if space(s) are present in the field value.

### Observations
- Invalid query error is returned if special character(s) is used in field value for '=' operator. To avoid this use 'LIKE' operator without special character(s) for this field. Example; For query '[x-ldap-event:request = '(&(objectClass=group))']' use '[x-ldap-event:request LIKE 'objectClass=group']'.
- UTC Format of any timestamp field value in query is converted to vectra timestamp format (YYYY-MM-DDTHHMM) during translation thereby dropping millisecond part of UTC format.
- Query on 'grouped-details:subnet' field works for the network ID part of the field only. For example to create query on "subnet": "10.250.50.0/24" following query shoud be used [x-grouped-details:subnet = '10.250.50']

### References
- [Vectra REST API Guide v2.4](https://support.vectra.ai/s/article/KB-VS-1626)
- [Advanced Search Reference Guide](https://support.vectra.ai/s/article/KB-VS-1116)
- [Understanding Vectra AI](https://support.vectra.ai/s/article/KB-VS-1285)
- [Detection and Campaign lifespan and retention periods](https://support.vectra.ai/s/article/KB-VS-1099)
