# Tanium Threat Response Alerts

## Table of Contents
- [Cisco Secure Email API Endpoints](#cisco-secure-email-api-endpoints)
- [Pattern expression with STIX and CUSTOM attributes - Single Observation](#single-observation)
- [Pattern expression with STIX and CUSTOM attributes - Multiple Observation](#multiple-observation)
- [STIX Execute Query](#stix-execute-query)

### Tanium Connector Module Overview
The Tanium Connector Module is a connector that uses the Tanium Threat Response API to obtain a list of Alerts.

### Tanium Threat Response API Alert Request Overview
Communication to the Tanium Threat Response service is done using an API Request. Each request will return back a list of Alerts based off the query parameters.

Request Type - "GET"
Required Headers - "Session" - This represents the API Token being used to access the API.
Endpoint - https://hostname/plugin/products/threat-response/api/v1/alerts - The hostname of the Tanium instance you are using.
Operators - This API only supports the "&" operator. This can act as an "AND" or an "OR" depending on context.
Query Parameters -
   |Parameter Name | Description 
   | ----          |   ----
   | state | Filter alerts by the specified states.
   | type | Filter alerts by the specified types.
   | matchType | Filter alerts by the specified matchType.
   | path | Filter alerts by the specified path.
   | priority | Filter alerts by the specified priorities.
   | severity | Filter alerts by the specified severities.
   | intelDocId | Filter alerts by the specified intelDocIds.
   | intelType | Filter alerts by the specified intelType.
   | intelDocName | Filter alerts by the specified intelDocName.
   | intelSource | Filter alerts by the specified Source Name.
   | labelName | Filter alerts by the specified labelName.
   | mitreId | Filter alerts by the specified mitreId.
   | scanConfigId | Filter alerts by the specified scanConfigIds.
   | computerName | Filter alerts by the specified computerNames.
   | computerIpAddress | Filter alerts by the specified computerIpAddresses.
   | platform | Filter alerts by the specified platform.
   | details | Filter alerts by the specified details.
   | alertedAtFrom | Filter alerts from the specified time (inclusive).
   | alertedAtUntil | Filter alerts until the specified time (exclusive).
   | guid | Filter alerts by the specified GUID.
   | include | The comma-separated list of field names to include that would ordinarily be omitted, e.g. "findingBase64Zip".
   | sort | A comma-separated list of COLUMN controlling sort ordering. [Defaults to ascending sort order. -COLUMN indicates descending sort order.].
   | expand | If expand = 'endpoint', include expanded impact/endpoint data within the payload.
   | limit | The maximum number of alerts to return. [Max: 500]. Default value: 100
   | offset | The offset number to begin listing alerts.

### Tanium Threat Response API Alert Limitations.

It should be stated that the API is limited to only working with an & operator. This heavily limits the filtering on the API.

The & operator has two properties.
1. When used between two different parameters, it treat the & operator as an "AND". It will only get events that match both properties. An example would be the following
alert?computerIpAddress=1.1.1.1&computerName=example

In this case it will only get alerts that have the IP Address "1.1.1.1" and Computer Name "example".

2. When used with the same parameter twice, it will treat the parameter as an "OR" operator. It will get events that match either property. An example would be the following

alert?computerIpAddress=1.1.1.1&computerIpAddress=2.2.2.2

In this case it will get any even that contains either 1.1.1.1 or 2.2.2.2.

### Tanium Threat Response API Alert Response Overview

#### General Response

When a query is sent to the Tanium Threat Response API Alerts endpoint the expected response is a json formatted list of alerts.

A request with no query will look something like the example below
```json
  "data": [
    {
      "id": 1,
      "eid": 1003,
      "state": "unresolved",
      "type": "detect.match",
      "guid": "00000000-0000-0000-0000-000000000000",
      "priority": "high",
      "severity": "info",
      "details": "{...}",
      "intelDocId": 700,
      "groupingId": 2,
      "intelDocRevisionId": 1,
      "scanConfigId": 2,
      "scanConfigRevisionId": 1,
      "computerName": "computerName",
      "computerIpAddress": "1.1.1.1",
      "matchType": "process",
      "path": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
      "receivedAt": "2023-10-16T12:29:34.609Z",
      "suppressedAt": null,
      "alertedAt": "2023-10-16T12:26:51.000Z",
      "findingId": "-4758370623356219688",
      "ackedAt": "2023-10-16T12:38:03.961Z",
      "firstEIDResolutionAttempt": "2023-10-16T12:29:37.091Z",
      "lastEIDResolutionAttempt": "2023-10-16T12:29:37.091Z",
      "createdAt": "2023-10-16T12:29:34.903Z",
      "updatedAt": "2023-10-16T12:38:03.968Z"
    }
  ],
  "meta": {
    "totalCount": 33,
    "filteredCount": 33
  }
```
#### A response containing the intel doc information

This response is missing crucial information provided by the Inteldocument associated with the response. Hence any request that is made with STIX-Shifter will include the &expand=intelDoc. When this is included the output looks like this.

NOTE:Depending on the query, the API can ignore the "&expand=intelDoc" option.

```json
{
 "id": 2,
      "eid": 1003,
      "state": "unresolved",
      "type": "detect.match",
      "guid": "00000000-0000-0000-114a-000000000000",
      "priority": "high",
      "severity": "info",
      "details": "{...}",
      "intelDocId": 700,
      "groupingId": 2,
      "intelDocRevisionId": 1,
      "scanConfigId": 2,
      "scanConfigRevisionId": 1,
      "computerName": "ComputerName",
      "computerIpAddress": "1.1.1.1",
      "matchType": "process",
      "path": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
      "receivedAt": "2023-10-16T12:29:34.609Z",
      "suppressedAt": null,
      "alertedAt": "2023-10-16T12:26:51.000Z",
      "findingId": "1245935966959239109",
      "ackedAt": "2023-10-16T12:38:03.961Z",
      "firstEIDResolutionAttempt": "2023-10-16T12:29:37.091Z",
      "lastEIDResolutionAttempt": "2023-10-16T12:29:37.091Z",
      "createdAt": "2023-10-16T12:29:34.849Z",
      "updatedAt": "2023-10-16T12:38:03.968Z",
      "intelDoc": {
        "id": 700,
        "type": "tanium-signal",
        "typeVersion": "1.0",
        "md5": "b5050a54c2556267931541b944ab0481",
        "blobId": "4ef7353d-ae4c-4eac-9c0b-75522592b438",
        "revisionId": 1,
        "intrinsicId": null,
        "name": "Testing eicar",
        "description": "Alerting on eicar file present on windows system",
        "size": 276,
        "compiled": {
          "expressions": [],
          "terms": [
            {
              "condition": "contains",
              "negate": false,
              "value": "eicar",
              "object": "file",
              "property": "path"
            }
          ],
          "operator": "or",
          "text": "file.path contains 'eicar'",
          "syntax_version": 6
        },
        "isSchemaValid": true,
        "sourceId": 2,
        "alertCount": 8,
        "unresolvedAlertCount": 8,
        "customHash": null,
        "mitreAttack": {
          "techniques": [
            {
              "id": "T1134.002",
              "name": "Access Token Manipulation Mitigation: Create Process with Token"
            }
          ]
        },
        "platforms": [
          "windows"
        ],
        "createdAt": "2023-10-11T19:47:06.485Z",
        "updatedAt": "2023-11-28T18:50:31.943Z",
        "throttledFindingCount": 0,
        "allowAutoDisable": true,
        "disabled": false,
        "disabledEndpointCount": 0,
        "firstDeploymentTimestamp": "2023-10-13T19:28:05.584Z",
        "lastDeploymentTimestamp": "2023-11-28T18:50:31.920Z",
        "status": "HIGH_FIDELITY"
      }
    }
```

#### The details field.
  One more thing worth noting is that there is a massive amount information in the details field. This field is returned as a string formatted json object. An example is provided below

```json
{
  "match": {
    "hash": "17914125682699366401",
    "type": "process",
    "source": "recorder",
    "version": 1,
    "contexts": [
      {
        "file": {
          "uniqueEventId": "4611686018427965350"
        },
        "event": {
          "fileMove": {
            "srcPath": "C:\\Users\\user\\Downloads\\ded2b98d-52fb-4b4a-832e-00000000000.tmp",
            "destPath": "C:\\Users\\user\\Downloads\\eicar_com (2).zip.crdownload"
          },
          "timestampMs": "1697459178054"
        }
      }
    ],
    "properties": {
      "pid": 9080,
      "args": "\"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe\" --no-startup-window --continue-active-setup",
      "file": {
        "md5": "d193ea4b8d102d020c02dc45af23ff0d",
        "sha1": "469e259b884043aedac879a96356fb741f82daa8",
        "sha256": "9ba39dd15eff718ff357db346d0fda3a12c9dbb216511cbb41050fb0d6b3d9c9",
        "fullpath": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
      },
      "name": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
      "user": "devicename\\user",
      "start_time": "2023-10-13T14:46:31.000Z",
      "recorder_unique_id": "3994044258139188996"
    }
  },
  "finding": {
    "whats": [
      {
        "source_name": "recorder",
        "intel_intra_ids": [
          {
            "id_v2": "901388892329936882"
          }
        ],
        "artifact_activity": {
          "acting_artifact": {
            "process": {
              "pid": 9080,
              "file": {
                "file": {
                  "hash": {
                    "md5": "d193ea4b8d102d020c02dc45af23ff0d",
                    "sha1": "469e259b884043aedac879a96356fb741f82daa8",
                    "sha256": "9ba39dd15eff718ff357db346d0fda3a12c9dbb216511cbb41050fb0d6b3d9c9"
                  },
                  "path": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
                  "signature_data": {
                    "issuer": "Microsoft Code Signing PCA 2011",
                    "status": 1,
                    "subject": "Microsoft Corporation"
                  }
                },
                "artifact_hash": "15257803663505479322",
                "instance_hash": "15257803663505479322"
              },
              "user": {
                "user": {
                  "name": "user",
                  "domain": "device",
                  "user_id": "S-1-5-21-1252622098-4149316198-505502587-500"
                }
              },
              "handles": [],
              "arguments": "\"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe\" --no-startup-window --continue-active-setup",
              "start_time": "2023-10-13T14:46:31.000Z",
              "tanium_unique_id": "3994044258139188996"
            },
            "artifact_hash": "17914125682699366401",
            "instance_hash": "8890920941823507809",
            "is_intel_target": true
          },
          "relevant_actions": [
            {
              "verb": 7,
              "origin": {
                "file": {
                  "path": "C:\\Users\\user\\Downloads\\ded2b98d-52fb-4b4a-832e-d09664b8099a.tmp"
                },
                "artifact_hash": "642322984173040938",
                "instance_hash": "642322984173040938"
              },
              "target": {
                "file": {
                  "path": "C:\\Users\\user\\Downloads\\eicar_com (2).zip.crdownload"
                },
                "artifact_hash": "11534804092509109490",
                "instance_hash": "11534804092509109490"
              },
              "timestamp": "2023-10-16T12:26:18.000Z",
              "tanium_recorder_context": {
                "file": {
                  "unique_event_id": "4611686018427965350"
                },
                "event": {
                  "file_move": {
                    "src_path": "C:\\Users\\user\\Downloads\\ded2b98d-52fb-4b4a-832e-d09664b8099a.tmp",
                    "dest_path": "C:\\Users\\user\\Downloads\\eicar_com (2).zip.crdownload"
                  },
                  "timestamp_ms": "1697459178054"
                }
              },
              "tanium_recorder_event_table_id": "4611686018427965350"
            }
          ]
        }
      }
    ],
    "domain": "threatresponse",
    "hunt_id": "2",
    "intel_id": "700:1:8ebe28bf-1acb-41b7-9f30-7b40a9145b1d",
    "last_seen": "2023-10-16T12:26:51.000Z",
    "threat_id": "901388892329936882",
    "finding_id": "1245935966959239109",
    "first_seen": "2023-10-16T12:26:51.000Z",
    "source_name": "recorder",
    "system_info": {
      "os": "Microsoft Windows 11 Pro",
      "bits": 64,
      "platform": "Windows",
      "patch_level": "10.0.22621.0.0",
      "build_number": "22621"
    },
    "reporting_id": "reporting-id-placeholder"
  },
  "intel_id": 700,
  "config_id": 2,
  "config_rev_id": 1
}
```

### Curl Example of a query being made to the Tanium Threat Response API

curl --request GET --header 'Content-Type: application/json' --header 'session: [TOKEN]' 'https://tk-ibmlab-api.titankube.com/plugin/products/threat-response/api/v1/alerts?expand=intelDoc&limit=1'

### How the Tanium Connector Module sends request

Each request the connector makes will be in the following format

https://[hostname]/plugin/products/threat-response/api/v1/alerts?[query]&expand=intelDoc&offset=[currentOffset]&limit=[limit]
The [query] is the transformed STIX output from the translation input.
The [hostname] is provided by the user.
The [currentOffset] is provided by the user.
The [limit] is the lower of the user provided limit or the default (500). IE: If the user provides 600, it will be 500. If the user provides 20, it will be 20.

### Observations
- Only supports AND/OR and IN operator
- AND can only be used with different fields
- OR can only be used with the same fields
- IN acts as multiple OR operators

For example : 
"[(x-ibm-finding:dst_ip_ref.value = '10.0.0.4'" \
  " OR x-ibm-finding:dst_ip_ref.value = '10.0.0.2'" \
  " OR x-ibm-finding:dst_ip_ref.value = '10.0.0.1')" \
  " AND (x-ibm-finding:dst_os_ref.name IN ('windows','osx','linux'))" \
  " AND (x-ibm-finding:x_priority = 'high'" \
  " OR x-ibm-finding:x_priority = 'low')" \
  " AND (x-ibm-finding:x_scan_config_id = '2'" \
  " OR x-ibm-finding:x_scan_config_id = '3'" \
  " OR x-ibm-finding:x_scan_config_id = '4'" \
  " OR x-ibm-finding:x_scan_config_id = '5')" \
  " AND (x-ibm-finding:x_label_name = 't')" \
  " AND (x-ibm-finding:x_details = 'te')]" \
  " START t'2022-07-01T00:00:00.000Z'" \
  " STOP t'2024-07-27T00:05:00.000Z'"

is valid because all of the AND's are between different fields and all of the OR's are between the same field.

Be aware that if the query does not match the above rules, than it may return false results that do not match the query.
If a query does not work, the Connector will try to throw an exception. If it does not, than it will simply batch all the terms as
field1&field2&field3 etc. As mentioned, the API can only support "&" which acts as both AND and OR.

### Limitations
- There are likely unmapped fields in the "Details" field, however due to the nature of how flexible it is, some observations may not be mapped as you'd expect. Use the unmapped_fallback : "true" option to map these fields.
- Regex is not supported in any query. All values will be interpreted literally.
- MATCH and LIKE are not supported
- Greater than (>, >=) and Less than (>, >=) are not supported.
- NOT (!) is not supported
- "=" is not an exact match, but a contains. It will return all values that contain the value.
- Observation expressions do not currently check for invalid request that are not possible with this API. 
- Comparison expressions should check for invalid request.

### References
- Most documentation requires a Tanium account to access.
- The API Documentation is specific to your Tanium Instance. For access, discuss it with your Tanium support representitive. 
- https://help.tanium.com/bundle/ug_threat_response_cloud/page/threat_response/reference_alert_data.html provides some information on the "details field.
- For obtaining your Tanium API Key (session token) refer to Taniums support documentation https://help.tanium.com 

### STIX Shifter 

#### Single Observation

#### STIX Translate query to fetch the messages from a specific ipaddress
```shell
translate 
tanium 
query 
{} 
"[ipv4-addr:value='1.1.1.1'] START t'2023-12-01T11:00:00.000Z' STOP t'2024-01-31T21:00:00.003Z'"
```
#### STIX Translate query - output
```json
{
    "queries": [
        "computerIpAddress=1.1.1.1&alertedAtFrom=2023-12-01T11:00:00.000Z&alertedAtUntil=2024-01-31T21:00:00.003Z"
    ]
}
```

#### STIX Transmit results 

```shell
transmit 
tanium 
'{"host":"tk-ibmlab-api.titankube.com","port":443}'
'{"auth":{"accessToken":"token-XXXXXXX"}}'
 results 
 "computerIpAddress=1.1.1.1&alertedAtFrom=2023-12-01T11:00:00.000Z&alertedAtUntil=2024-01-31T21:00:00.003Z" 
 0 
 1
```

#### STIX Transmit results - output
```json
{
    "success": true,
    "data": [
        {
            "id": 67,
            "eid": 1003,
            "state": "unresolved",
            "type": "detect.match",
            "guid": "00000000-0000-0000-625e-1335991c35da",
            "priority": "high",
            "severity": "info",
            "details": {},
            "intelDocId": 700,
            "groupingId": 2,
            "intelDocRevisionId": 1,
            "scanConfigId": 2,
            "scanConfigRevisionId": 1,
            "computerName": "EndpointDevice-",
            "computerIpAddress": "1.1.1.1",
            "matchType": "process",
            "path": "C:\\Windows\\explorer.exe",
            "receivedAt": "2024-01-03T17:22:29.404Z",
            "suppressedAt": null,
            "alertedAt": "2024-01-03T15:50:10.000Z",
            "findingId": "7088123984450696666",
            "ackedAt": "2024-01-03T17:46:59.598Z",
            "firstEIDResolutionAttempt": "2024-01-03T17:22:39.256Z",
            "lastEIDResolutionAttempt": "2024-01-03T17:22:39.256Z",
            "createdAt": "2024-01-03T17:22:29.596Z",
            "updatedAt": "2024-01-03T17:46:59.608Z",
            "intelDoc": {
                "id": 700,
                "type": "tanium-signal",
                "typeVersion": "1.0",
                "md5": "b5050a54c2556267931541b944ab0481",
                "blobId": "4ef7353d-ae4c-4eac-9c0b-75522592b438",
                "revisionId": 1,
                "intrinsicId": null,
                "name": "Testing eicar",
                "description": "Alerting on eicar file present on windows system",
                "size": 276,
                "compiled": {
                    "expressions": [],
                    "terms": [
                        {
                            "condition": "contains",
                            "negate": false,
                            "value": "eicar",
                            "object": "file",
                            "property": "path"
                        }
                    ],
                    "operator": "or",
                    "text": "file.path contains 'eicar'",
                    "syntax_version": 6
                },
                "isSchemaValid": true,
                "sourceId": 2,
                "alertCount": 1,
                "unresolvedAlertCount": 1,
                "customHash": null,
                "mitreAttack": {
                    "techniques": [
                        {
                            "id": "T1134.002",
                            "name": "Access Token Manipulation Mitigation: Create Process with Token"
                        }
                    ]
                },
                "platforms": [
                    "windows"
                ],
                "createdAt": "2023-10-11T19:47:06.485Z",
                "updatedAt": "2024-01-10T19:22:23.966Z",
                "throttledFindingCount": 0,
                "allowAutoDisable": true,
                "disabled": false,
                "disabledEndpointCount": 0,
                "firstDeploymentTimestamp": "2023-10-13T19:28:05.584Z",
                "lastDeploymentTimestamp": "2024-01-10T19:22:23.931Z",
                "status": "HIGH_FIDELITY"
            }
        }
    ],
    "metadata": {
        "next_offset": 1,
        "total_result_count": 1
    }
}
```


#### STIX execute results
```shell
transmit 
tanium 
'{"host":"tk-ibmlab-api.titankube.com","port":443}'
'{"auth":{"accessToken":"token-XXXXXXX"}}'
 results 
 "computerIpAddress=1.1.1.1&alertedAtFrom=2023-12-01T11:00:00.000Z&alertedAtUntil=2024-01-31T21:00:00.003Z" 
 0 
 1
```

#### STIX Transmit results - output
```json
{
    "type": "bundle",
    "id": "bundle--2c1844d5-7e75-4a6c-8dbf-71ad73cb8b5c",
    "objects": [
        {
            "type": "identity",
            "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
            "name": "Tanium",
            "identity_class": "events"
        },
        {
            "id": "observed-data--485f64bb-e201-4535-9b80-c33e51576c55",
            "type": "observed-data",
            "created_by_ref": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
            "created": "2024-01-18T13:50:45.957Z",
            "modified": "2024-01-18T13:50:45.957Z",
            "objects": {
                "0": {
                    "type": "x-ibm-finding",
                    "finding_type": "alert",
                    "alert_id": 67,
                    "x_eid": 1003,
                    "x_type": "detect.match",
                    "x_guid": "00000000-0000-0000-625e-1335991c35da",
                    "x_priority": "high",
                    "severity": 0,
                    "x_match_hash": "4271502581873229387",
                    "x_match_type": "process",
                    "x_match_source": "recorder",
                    "x_match_version": 1,
                    "x_match_unique_event_id": "4611686018457109193",
                    "x_match_path": "C:\\Users\\user\\Desktop\\eicar - Copy",
                    "x_match_timestamp": "1704296770143",
                    "x_match_process_ref": "2",
                    "x_match_recorder_id": "13121309559364419859",
                    "x_finding_source_name": "recorder",
                    "x_finding_intel_intra_ids": [
                        {
                            "id_v2": "901388892329936882"
                        }
                    ],
                    "x_finding_process_ref": "2",
                    "dst_os_user_ref": "6",
                    "x_action": [
                        "12"
                    ],
                    "x_finding_domain": "threatresponse",
                    "x_finding_hunt_id": "2",
                    "x_finding_intel_id": "700:1:8ebe28bf-1acb-41b7-9f30-7b40a9145b1d",
                    "x_finding_last_seen": "2024-01-03T15:50:10.000Z",
                    "x_finding_threat_id": "901388892329936882",
                    "x_finding_finding_id": "7088123984450696666",
                    "x_finding_first_seen": "2024-01-03T15:50:10.000Z",
                    "dst_os_ref": "15",
                    "x_finding_reporting_id": "reporting-id-placeholder",
                    "x_intel_id": 700,
                    "x_config_id": 2,
                    "x_config_rev_id": 1,
                    "x_intel_doc_id": 700,
                    "x_grouping_id": 2,
                    "x_intel_doc_revision_id": 1,
                    "x_scan_config_id": 2,
                    "x_scan_config_revision_id": 1,
                    "dst_ip_ref": "17",
                    "x_path": "C:\\Windows\\explorer.exe",
                    "x_received_at": "2024-01-03T17:22:29.404Z",
                    "x_alertedAt": "2024-01-03T15:50:10.000Z",
                    "x_finding_id": "7088123984450696666",
                    "x_acked_at": "2024-01-03T17:46:59.598Z",
                    "x_first_eid_resolution_attempt": "2024-01-03T17:22:39.256Z",
                    "x_last_eid_resolution_attempt": "2024-01-03T17:22:39.256Z",
                    "time_observed": "2024-01-03T17:22:29.596Z",
                    "x_intel_doc_ref": "18",
                    "name": "Testing eicar",
                    "description": "Alerting on eicar file present on windows system",
                    "event_count": 1,
                    "ttp_tagging_refs": "20"
                },
                "1": {
                    "type": "x-oca-event",
                    "outcome": "unresolved",
                    "severity": 0,
                    "process_ref": "2",
                    "file_ref": "3",
                    "user_ref": "6",
                    "parent_process_ref": "2",
                    "host_ref": "16",
                    "category": "process",
                    "provider": "tanium-signal",
                    "action": "Testing eicar",
                    "description": "Alerting on eicar file present on windows system",
                    "ttp_tagging_refs": "20"
                },
                "2": {
                    "type": "process",
                    "pid": 17148,
                    "arguments": [
                        "explorer.exe"
                    ],
                    "binary_ref": "3",
                    "name": "explorer.exe",
                    "cwd": "C:/Windows",
                    "parent_ref": "5",
                    "creator_user_ref": "6",
                    "created": "2024-01-03T15:11:39.000Z",
                    "x_unique_id": "13121309559364419859",
                    "x_artifact_hash": "4271502581873229387",
                    "x_instance_hash": "14467857814682859733",
                    "x_intel_target": true
                },
                "3": {
                    "type": "file",
                    "name": "explorer.exe",
                    "parent_directory_ref": "4",
                    "hashes": {
                        "md5": "c8a00f2fd7f7a580a8638e8a08270dd3",
                        "sha1": "3db68ccbfdd35f8bce7202d48d81b0da2f803b1c",
                        "sha256": "bfedd99ac382f96707ae8ee95664c1ef47c8504ff0933411dcf1a68ea77f8e1d"
                    },
                    "x_artifact_hash": "4668134681718746372",
                    "x_instance_hash": "4668134681718746372"
                },
                "4": {
                    "type": "directory",
                    "path": "C:/Windows",
                    "contains_refs": [
                        "3"
                    ]
                },
                "5": {
                    "type": "process",
                    "pid": 4148,
                    "child_ref": "2",
                    "binary_ref": "8",
                    "creator_user_ref": "11",
                    "arguments": [
                        "winlogon.exe"
                    ],
                    "created": "2023-10-13T14:45:56.000Z",
                    "x_unique_id": "11929269699007748715",
                    "x_artifact_hash": "15202984064548280121",
                    "x_instance_hash": "11058433479713752051"
                },
                "6": {
                    "type": "user-account",
                    "x_full_username": "EndpointDevice-\\user",
                    "display_name": "user",
                    "is_service_account": true,
                    "user_id": "id"
                },
                "7": {
                    "type": "x509-certificate",
                    "issuer": "Microsoft Windows Production PCA 2011",
                    "x_status": 1,
                    "subject": "Microsoft Windows"
                },
                "8": {
                    "type": "file",
                    "hashes": {
                        "md5": "576637f6cfe9601ad0a40a6373c2c232",
                        "sha1": "cbde2a666a20cbd9c9b3ab1f85b7ba9f0fa04170",
                        "sha256": "3ff7ad170b2b232d8cfce26dbfc98229b1755c8faeee1b8ed71ba6ced9ddf194"
                    },
                    "name": "winlogon.exe",
                    "parent_directory_ref": "9",
                    "x_artifact_hash": "13433015920877340112"
                },
                "9": {
                    "type": "directory",
                    "path": "C:/Windows/System32",
                    "contains_refs": [
                        "8"
                    ]
                },
                "10": {
                    "type": "x509-certificate",
                    "issuer": "Microsoft Windows Production PCA 2011",
                    "x_status": 1,
                    "subject": "Microsoft Windows"
                },
                "11": {
                    "type": "user-account",
                    "display_name": "user",
                    "is_service_account": true,
                    "user_id": "id"
                },
                "12": {
                    "type": "x-action",
                    "verb": 6,
                    "binary_ref": "13",
                    "artifact_hash": "2199692353440625464",
                    "instance_hash": "2199692353440625464",
                    "timestamp": "2024-01-03T15:46:10.000Z",
                    "event_id": "4611686018457109193",
                    "timestamp_ms": "1704296770143",
                    "recorder_event_table_id": "4611686018457109193"
                },
                "13": {
                    "type": "file",
                    "name": "eicar - Copy",
                    "parent_directory_ref": "14"
                },
                "14": {
                    "type": "directory",
                    "path": "C:/Users/user/Desktop",
                    "contains_refs": [
                        "13"
                    ]
                },
                "15": {
                    "type": "software",
                    "name": "Microsoft Windows 11 Pro",
                    "x_bits": 64,
                    "x_platform_list": "Windows",
                    "version": "10.0.22621.0.0",
                    "x_build_number": "22621"
                },
                "16": {
                    "type": "x-oca-asset",
                    "hostname": "EndpointDevice-",
                    "ip_refs": [
                        "17"
                    ]
                },
                "17": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "18": {
                    "type": "x-tanium-inteldocument",
                    "intel_doc_id": 700,
                    "type_version": "1.0",
                    "md5": "b5050a54c2556267931541b944ab0481",
                    "blob_id": "4ef7353d-ae4c-4eac-9c0b-75522592b438",
                    "revision_id": 1,
                    "size": 276,
                    "x_compiled_terms": [
                        "19"
                    ],
                    "operator": "or",
                    "text": "file.path contains 'eicar'",
                    "syntax_version": 6,
                    "is_schema_valid": true,
                    "source_id": 2,
                    "unresolvedAlertCount": 1,
                    "x_platform_list": [
                        "windows"
                    ],
                    "x_created": "2023-10-11T19:47:06.485Z",
                    "x_updated": "2024-01-10T19:22:23.966Z",
                    "throttledFindingCount": 0,
                    "allowAutoDisable": true,
                    "disabled": false,
                    "disabledEndpointCount": 0,
                    "firstDeploymentTimestamp": "2023-10-13T19:28:05.584Z",
                    "lastDeploymentTimestamp": "2024-01-10T19:22:23.931Z",
                    "status": "HIGH_FIDELITY"
                },
                "19": {
                    "type": "x-compiled-terms",
                    "condition": "contains",
                    "negate": false,
                    "value": "eicar",
                    "object": "file",
                    "property": "path"
                },
                "20": {
                    "type": "x-ibm-ttp-tagging",
                    "extensions": {
                        "technique_id": "T1134.002",
                        "technique_name": "Access Token Manipulation Mitigation: Create Process with Token",
                        "tactic_name": ""
                    },
                    "name": "Access Token Manipulation Mitigation: Create Process with Token"
                }
            },
            "first_observed": "2024-01-03T17:22:29.596Z",
            "last_observed": "2024-01-03T17:46:59.608Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```
