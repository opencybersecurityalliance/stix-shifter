# Tanium Threat Response Alerts

## Table of Contents

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

####General Response

When a query is sent to the Tanium Threat Response API Alerts endpoint the expected response is a json formatted list of alerts.

A request with no query will look something like the example below
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
    {
        "id": 2,
        ......
    }
  ],
  "meta": {
    "totalCount": 33,
    "filteredCount": 33
  }

#### A response containing the intel doc information

This response is missing crucial information provided by the Inteldocument associated with the response. Hence any request that is made with STIX-Shifter will include the &expand=intelDoc. When this is included the output looks like this.

NOTE:Depending on the query, the API can ignore the "&expand=intelDoc" option.

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
  ]

#### The details field.

  One more thing worth noting is that there is a massive amount information in the details field. This field is returned as a string formatted json object. An example is provided below

{\"match\":{\"hash\":\"17914125682699366401\",\"type\":\"process\",\"source\":\"recorder\",\"version\":1,\"contexts\":[{\"file\":{\"uniqueEventId\":\"4611686018427965350\"},\"event\":{\"fileMove\":{\"srcPath\":\"C:\\\\Users\\\\user\\\\Downloads\\\\ded2b98d-52fb-4b4a-832e-00000000000.tmp\",\"destPath\":\"C:\\\\Users\\\\user\\\\Downloads\\\\eicar_com (2).zip.crdownload\"},\"timestampMs\":\"1697459178054\"}}],\"properties\":{\"pid\":9080,\"args\":\"\\\"C:\\\\Program Files (x86)\\\\Microsoft\\\\Edge\\\\Application\\\\msedge.exe\\\" --no-startup-window --continue-active-setup\",\"file\":{\"md5\":\"d193ea4b8d102d020c02dc45af23ff0d\",\"sha1\":\"469e259b884043aedac879a96356fb741f82daa8\",\"sha256\":\"9ba39dd15eff718ff357db346d0fda3a12c9dbb216511cbb41050fb0d6b3d9c9\",\"fullpath\":\"C:\\\\Program Files (x86)\\\\Microsoft\\\\Edge\\\\Application\\\\msedge.exe\"},\"name\":\"C:\\\\Program Files (x86)\\\\Microsoft\\\\Edge\\\\Application\\\\msedge.exe\",\"user\":\"devicename\\\\user\",\"start_time\":\"2023-10-13T14:46:31.000Z\",\"recorder_unique_id\":\"3994044258139188996\"}},\"finding\":{\"whats\":[{\"source_name\":\"recorder\",\"intel_intra_ids\":[{\"id_v2\":\"901388892329936882\"}],\"artifact_activity\":{\"acting_artifact\":{\"process\":{\"pid\":9080,\"file\":{\"file\":{\"hash\":{\"md5\":\"d193ea4b8d102d020c02dc45af23ff0d\",\"sha1\":\"469e259b884043aedac879a96356fb741f82daa8\",\"sha256\":\"9ba39dd15eff718ff357db346d0fda3a12c9dbb216511cbb41050fb0d6b3d9c9\"},\"path\":\"C:\\\\Program Files (x86)\\\\Microsoft\\\\Edge\\\\Application\\\\msedge.exe\",\"signature_data\":{\"issuer\":\"Microsoft Code Signing PCA 2011\",\"status\":1,\"subject\":\"Microsoft Corporation\"}},\"artifact_hash\":\"15257803663505479322\",\"instance_hash\":\"15257803663505479322\"},\"user\":{\"user\":{\"name\":\"user\",\"domain\":\"device\",\"user_id\":\"S-1-5-21-1252622098-4149316198-505502587-500\"}},\"handles\":[],\"arguments\":\"\\\"C:\\\\Program Files (x86)\\\\Microsoft\\\\Edge\\\\Application\\\\msedge.exe\\\" --no-startup-window --continue-active-setup\",\"start_time\":\"2023-10-13T14:46:31.000Z\",\"tanium_unique_id\":\"3994044258139188996\"},\"artifact_hash\":\"17914125682699366401\",\"instance_hash\":\"8890920941823507809\",\"is_intel_target\":true},\"relevant_actions\":[{\"verb\":7,\"origin\":{\"file\":{\"path\":\"C:\\\\Users\\\\user\\\\Downloads\\\\ded2b98d-52fb-4b4a-832e-d09664b8099a.tmp\"},\"artifact_hash\":\"642322984173040938\",\"instance_hash\":\"642322984173040938\"},\"target\":{\"file\":{\"path\":\"C:\\\\Users\\\\user\\\\Downloads\\\\eicar_com (2).zip.crdownload\"},\"artifact_hash\":\"11534804092509109490\",\"instance_hash\":\"11534804092509109490\"},\"timestamp\":\"2023-10-16T12:26:18.000Z\",\"tanium_recorder_context\":{\"file\":{\"unique_event_id\":\"4611686018427965350\"},\"event\":{\"file_move\":{\"src_path\":\"C:\\\\Users\\\\user\\\\Downloads\\\\ded2b98d-52fb-4b4a-832e-d09664b8099a.tmp\",\"dest_path\":\"C:\\\\Users\\\\user\\\\Downloads\\\\eicar_com (2).zip.crdownload\"},\"timestamp_ms\":\"1697459178054\"}},\"tanium_recorder_event_table_id\":\"4611686018427965350\"}]}}],\"domain\":\"threatresponse\",\"hunt_id\":\"2\",\"intel_id\":\"700:1:8ebe28bf-1acb-41b7-9f30-7b40a9145b1d\",\"last_seen\":\"2023-10-16T12:26:51.000Z\",\"threat_id\":\"901388892329936882\",\"finding_id\":\"1245935966959239109\",\"first_seen\":\"2023-10-16T12:26:51.000Z\",\"source_name\":\"recorder\",\"system_info\":{\"os\":\"Microsoft Windows 11 Pro\",\"bits\":64,\"platform\":\"Windows\",\"patch_level\":\"10.0.22621.0.0\",\"build_number\":\"22621\"},\"reporting_id\":\"reporting-id-placeholder\"},\"intel_id\":700,\"config_id\":2,\"config_rev_id\":1}

### Curl Example of a query being made to the Tanium Threat Response API

curl --request GET --header 'Content-Type: application/json' --header 'session: [TOKEN]' 'https://tk-ibmlab-api.titankube.com/plugin/products/threat-response/api/v1/alerts?expand=intelDoc&limit=1'

### How the Tanium Connector Module sends request

Each request the connector makes will be in the following format

https://[hostname]/plugin/products/threat-response/api/v1/alerts?[query]&expand=intelDoc&offset=[currentOffset]&limit=[limit]
The [query] is the transformed STIX output from the translation input.
The [hostname] is provided by the user.
The [currentOffset] is provided by the user.
The [limit] is the lower of the user provided limit or the default (500). IE: If the user provides 600, it will be 500. If the user provides 20, it will be 20.

### STIX Shifter translate
Takes the input STIX formatted request and converts it to a valid Tanium Threat Response output 

NOTE: The API only supports "&" as an operator and "=" as a comparison. The "=' acts a contains, for example putting in "field = tes" would return all the values in "field" that contain "tes".

CLI Input
translate tanium query "{}" "[x-oca-event:host_ref.ip_ref.value = '1.1.1.1'] START t'2023-01-01T11:00:00.000Z' STOP t'2023-03-08T11:00:00.003Z'"

CLI Output
{
    "queries": [
        "computerIpAddress=1.1.1.1&alertedAtFrom=2023-01-01T11:00:00.000Z&alertedAtUntil=2023-03-08T11:00:00.003Z"
    ]
}


### STIX Shifter ping

CLI Input
transmit tanium '{"host":"tk-ibmlab-api.titankube.com","port":443}' '{"auth":{"accessToken":"[TOKEN]"}}' ping

CLI Output
{
    "success": true
}

### STIX Shifter 

### TODO: 
4. Finish this document
