# Microfocus ArcSight

## Supported STIX Mappings

See the [table of mappings](arcsight_supported_stix.md) for the STIX objects and operators supported by this connector.

## Data Source: 
Micro Focus ArcSight is a cyber security product, that provides big data security analytics and intelligence software for security information and event management (SIEM) and log management.

## Microfocus-ArcSight Logger API Endpoints:

Login Service : `https://<hostname>:<port>/core-service/rest/LoginService/login`

Status Endpoint : `https://<hostname>:<port>/server/search/status`

Query Endpoint : `https://<hostname>:<port>/server/search`

Result Endpoint : `https://<hostname>:<port>server/search/events`

Delete Endpoint : `https://<hostname>:<port>/server/search/close`

`Ref:  https://community.microfocus.com/dcvta86296/attachments/dcvta86296/logger/204/1/Logger_Web_Services_API_Guide.pdf`

## Format for calling stix-shifter from the command line

python main.py `<translator_module>` `<query or result>` `<STIX identity object>` `<data>`

## Pattern expression with STIX attributes:

### STIX patterns:
```
`translate arcsight query ‘{}’ "[file:name = 'svchost.exe'] START t'2020-06-17T14:20:00Z' STOP t'2020-08-18T14:30:00Z'"`
```

### Translated query:
```
`["{"query": "fileName = svchost.exe", "start_time": "2020-06-17T14:20:00.000Z", "end_time": "2020-08-18T14:30:00.000Z"}"]`
```
### Above translated query is passed as parameter to STIX transmission module:
### Transmit Search Call :
```
transmit "arcsight" "{"host": "xxxx", "port": 443}" "{"auth":{"login": "xxx", "password": "xxx"}}" query "{"query": "file:name = 'svchost.exe'", "start_time": "2020-06-17T14:20:00.000Z", "end_time": "2020-08-18T14:30:00.000Z"}"
```

### Transmit Results Call :
```
transmit "arcsight" "{"host": "xxxx", "port": 443}" "{"auth":{"login": "xxx", "password": "xxx"}}" results "search id" "offset" "length"
```

### Transmit result output:
```
"[{'network_events': {'_rowId': '2053B-B5@Local', 'Event Time': 1593431344528, 'Logger': 'Local', 'Device': 'ip-172-31-62-249.ec2.internal [ESMToLogger Receiver]', 'Receipt Time': 1593431344882, 'modelConfidence': '0', 'categoryObject': '/Host/Application/Service', 'sourceZoneURI': '/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 172.16.0.0-172.31.255.255', 'originalAgentZoneURI': '/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 172.16.0.0-172.31.255.255', 'deviceVersion': 'Windows Server 2012 R2', 'destinationZoneID': 'Mbp432AABABCDUVpYAT3UdQ==', 'sourceZoneID': 'Mbp432AABABCDUVpYAT3UdQ==', 'originalAgentId': '3sdGZ73IBABCDMQjbx1dwOQ==', 'agentHostName': 'ip-172-31-62-249.ec2.internal', 'name': 'The Windows Filtering Platform has allowed a connection.', 'agentAddress': '172.31.62.249', 'eventAnnotationModificationTime': '1593158145145', 'deviceSeverity': 'Audit_success', 'categoryOutcome': '/Success', 'dlat': '0.0', 'Version': '0', 'originalAgentType': 'winc', 'eventAnnotationVersion': '1', 'originalAgentMacAddress': '16-AE-7D-3C-02-11', 'eventId': 3208543, 'fileName': 'svchost.exe', 'bytesIn': -2147483648, 'categoryBehavior': '/Communicate/Query', 'atz': 'UTC', 'assetCriticality': '0', 'locality': '1', 'eventAnnotationAuditTrail': '1,1593151196874,root,Queued,,,,\n', 'categorySignificance': '/Informational', 'priority': 3, 'relevance': '10', 'oldFileHash': 'en_US|UTF-8', 'sourceAssetId': '49Y2d73IBABCDULfrMYOBPw==', 'agentType': 'superagent_ng', 'eventAnnotationStageUpdateTime': '1593158145145', 'av': '7.15.0.8296.0', 'sourcePort': 64023, 'transportProtocol': 'UDP', 'deviceProduct': 'Microsoft Windows', 'deviceEventClassId': 'Microsoft-Windows-Security-Auditing:5156', 'deviceDirection': '1', 'aid': '35wbCuHIBABCABElyDkfrAA==', 'destinationHostName': 'WIN-SD458DHHD07', 'eventAnnotationManagerReceiptTime': '1593158145142', '_cefVer': '0.1', 'deviceReceiptTime': 1593158033615, 'deviceCustomString2': 'Filtering Platform Connection', 'destinationAddress': '172.31.0.2', 'catdt': 'Operating System', 'globalEventId': 938321594551173381, 'ad.arcSightEventPath': '3sdGZ73IBABCDMQjbx1dwOQ==', 'bytesOut': -2147483648, 'destinationAssetId': '', 'dlong': '0.0', 'deviceVendor': 'Microsoft', 'deviceHostName': 'WIN-SD458DHHD07', 'deviceEventCategory': 'Security', 'endTime': 1593158033615, 'eventAnnotationFlags': '0', 'originalAgentHostName': '172.31.59.74', 'originalAgentAddress': '172.31.59.74', 'originalAgentVersion': '7.15.0.8295.0', 'severity': '0', 'art': '1593158138113', 'amac': '16-D9-1F-0F-B6-F1', 'sourceAddress': '172.31.59.74', 'filePath': '\\device\\harddiskvolume2\\windows\\system32', 'baseEventCount': 1, 'slong': '0.0', 'eventAnnotationEndTime': '1593158033615', 'startTime': 1593158033615, 'externalId': '5156', 'destinationPort': 53, 'agentSeverity': 'Low', 'dtz': 'UTC', 'mrt': '1593158145142', 'slat': '0.0', 'categoryDeviceGroup': '/Operating System', 'deviceCustomString2Label': 'EventlogCategory', 'fileType': 'Application', 'destinationZoneURI': '/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 172.16.0.0-172.31.255.255', 'c6a2Label': '', 'c6a3': '', 'c6a2': '', 'deviceAddress': '172.31.59.74', 'deviceAssetId': '49Y2d73IBABCDULfrMYOBPw==', 'deviceZoneExternalID': 'RFC1918: 172.16.0.0-172.31.255.255', 'sourceZoneExternalID': 'RFC1918: 172.16.0.0-172.31.255.255', 'deviceZoneURI': '/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 172.16.0.0-172.31.255.255', 'deviceZoneID': 'Mbp432AABABCDUVpYAT3UdQ==', 'destinationZoneExternalID': 'RFC1918: 172.16.0.0-172.31.255.255', 'protocols': ['UDP']}}]"
```

### ArcSight logger response to STIX object (STIX attributes)

### STIX observable output:

```json
{
    "type": "bundle",
    "id": "bundle--3309fa00-c6fa-4547-8ef3-c0494e12eccc",
    "spec_version": "2.0",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "arcsight",
            "identity_class": "events"
        },
        {
            "id": "observed-data--feeb98ad-95f8-41bc-8ea6-f2e4851e8e83",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2020-11-06T17:05:15.268Z",
            "modified": "2020-11-06T17:05:15.268Z",
            "objects": {
                "0": {
                    "type": "x-ibm-finding",
                    "time_observed": "2020-06-29T11:49:04.528Z",
                    "name": "The Windows Filtering Platform has allowed a connection.",
                    "finding_type": "/Informational",
                    "src_device": "49Y2d73IBABCDULfrMYOBPw==",
                    "dst_ip_ref": "7",
                    "severity": "0",
                    "src_ip_ref": "8"
                },
                "1": {
                    "type": "x-arcsight-event",
                    "model_confidence": "0",
                    "event_name": "The Windows Filtering Platform has allowed a connection.",
                    "event_id": 3208543,
                    "asset_criticality": "0",
                    "priority": 3,
                    "relevance": "10",
                    "event_end_time": "2020-06-26T07:53:53.615Z",
                    "base_event_count": 1,
                    "event_start_time": "2020-06-26T07:53:53.615Z",
                    "external_id": "5156"
                },
                "2": {
                    "type": "x-arcsight-event-category",
                    "category_object": "/Host/Application/Service",
                    "category_outcome": "/Success",
                    "category_behavior": "/Communicate/Query",
                    "category_significance": "/Informational",
                    "category_device_group": "/Operating System"
                },
                "3": {
                    "type": "x-arcsight-event-device",
                    "device_version": "Windows Server 2012 R2",
                    "device_severity": "Audit_success",
                    "device_product": "Microsoft Windows",
                    "device_receipt_time": "2020-06-26T07:53:53.615Z",
                    "device_vendor": "Microsoft",
                    "device_event_category": "Security",
                    "device_time_zone": "UTC",
                    "device_address_ref": "10",
                    "device_asset_id": "49Y2d73IBABCDULfrMYOBPw=="
                },
                "4": {
                    "type": "file",
                    "name": "svchost.exe",
                    "parent_directory_ref": "9"
                },
                "5": {
                    "type": "x-arcsight-event-source",
                    "source_asset_id": "49Y2d73IBABCDULfrMYOBPw=="
                },
                "6": {
                    "type": "network-traffic",
                    "src_port": 64023,
                    "dst_ref": "7",
                    "src_ref": "8",
                    "dst_port": 53,
                    "protocols": [
                        "udp"
                    ]
                },
                "7": {
                    "type": "ipv4-addr",
                    "value": "172.31.0.2"
                },
                "8": {
                    "type": "ipv4-addr",
                    "value": "172.31.59.74"
                },
                "9": {
                    "type": "directory",
                    "path": "\\device\\harddiskvolume2\\windows"
                },
                "10": {
                    "type": "ipv4-addr",
                    "value": "172.31.59.74"
                }
            },
            "first_observed": "2020-06-29T11:49:04.528Z",
            "last_observed": "2020-06-29T11:49:04.528Z",
            "number_observed": 1
        }
    ]
}
```

### Pattern expression with Custom attributes:
### STIX patterns:
```
`translate arcsight query ‘{}’ "([x-arcsight-event-category:category_significance LIKE '%Suspicious'] AND [x-arcsight-event:priority < '7']) START t'2020-06-01T08:43:10Z' STOP t'2020-07-31T10:43:10Z'"`
```

### Translated query:
```
`['{"query": "(categorySignificance = *Suspicious) AND (priority < 7)", "start_time": "2020-06-01T08:43:10.000Z", "end_time": "2020-07-31T10:43:10.000Z"}']`
```

### Above translated query is passed as parameter to STIX transmission module:
### Search API Call :

```
transmit "arcsight" "{"host": "xxxx", "port": 443}" "{"auth":{"login": "xxx", "password": "xxx"}}" query "{"query": "(categorySignificance = *Suspicious) AND (priority < 7)", "start_time": "2020-06-01T08:43:10.000Z", "end_time": "2020-07-31T10:43:10.000Z"}"
```
### Results API Call :
```
transmit "arcsight" "{"host": "xxxx", "port": 443}" "{"auth":{"login": "xxx", "password": "xxx"}}" results "search id" "offset" "length"
```

### Transmit result output:
```
"[{'network_events': {'_rowId': 'A560-9@Local', 'Event Time': 1592378453924, 'Logger': 'Local', 'Device': 'ip-172-31-62-249.ec2.internal [ESMToLogger Receiver]', 'Receipt Time': 1592378459297, 'modelConfidence': '0', 'categoryObject': '/Host/Resource/File', 'sourceZoneURI': '/All Zones/ArcSight System/Public Address Space Zones/RIPE NCC/77.0.0.0-95.255.255.255 (RIPE NCC)', 'originalAgentZoneURI': '/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 172.16.0.0-172.31.255.255', 'deviceVersion': '1.8', 'destinationZoneID': 'ML8022AABABCDTFpYAT3UdQ==', 'sourceZoneID': 'ML87gVA8BABCAOtgm7Ba7Kw==', 'originalAgentId': '3SgsPeXIBABCF9nAkLdozUA==', 'agentHostName': 'ip-172-31-62-249.ec2.internal', 'name': 'NETBIOS SMB-DS C$ share unicode access', 'agentAddress': '172.31.62.249', 'deviceAddress': '10.10.20.50', 'eventAnnotationModificationTime': '1592378443972', 'deviceSeverity': '3', 'categoryOutcome': '/Attempt', 'dlat': '0.0', 'Version': '0', 'originalAgentType': 'snort_db', 'eventAnnotationVersion': '1', 'sourceHostName': 'i53874A7E.versanet.de', 'eventId': 1721582, 'bytesIn': -2147483648, 'categoryBehavior': '/Access/Start', 'atz': 'UTC', 'assetCriticality': '0', 'locality': '1', 'eventAnnotationAuditTrail': '1,1592292620702,root,Queued,,,,\n', 'categorySignificance': '/Suspicious', 'sourceGeoPostalCode': '65933', 'priority': 5, 'relevance': '10', 'sourceGeoRegionCode': 'HE', 'agentType': 'superagent_ng', 'eventAnnotationStageUpdateTime': '1592378443972', 'sourceGeoLocationInfo': 'Frankfurt am Main', 'av': '7.15.0.8296.0', 'sourcePort': 3950, 'transportProtocol': 'TCP', 'deviceProduct': 'Snort', 'deviceEventClassId': '[1:2472]', 'aid': '35wbCuHIBABCABElyDkfrAA==', 'destinationHostName': '10.10.20.7', 'eventAnnotationManagerReceiptTime': '1592378443821', '_cefVer': '0.1', 'deviceReceiptTime': 1099211345000, 'deviceCustomString2': '5', 'destinationAddress': '10.10.20.7', 'categoryTechnique': '/Exploit/Weak Configuration', 'globalEventId': 446772548332802, 'ad.arcSightEventPath': '3SgsPeXIBABCF9nAkLdozUA==', 'bytesOut': -2147483648, 'dlong': '0.0', 'deviceVendor': 'Snort', 'deviceHostName': '10.10.20.50', 'deviceEventCategory': 'protocol-command-decode', 'endTime': 1592378762526, 'eventAnnotationFlags': '0', 'originalAgentHostName': 'ip-172-31-62-249.ec2.internal', 'deviceZoneURI': '/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 10.0.0.0-10.255.255.255', 'originalAgentAddress': '172.31.62.249', 'originalAgentVersion': '7.2.1.2648.0', 'severity': '3', 'art': '1099207748195', 'amac': '16-D9-1F-0F-B6-F1', 'sourceAddress': '83.135.74.126', 'deviceZoneID': 'ML8022AABABCDTFpYAT3UdQ==', 'baseEventCount': 1, 'startTime': 1592378762526, 'slong': '8.5952', 'eventAnnotationEndTime': '1592378762526', 'destinationPort': 445, 'agentSeverity': 'Medium', 'dtz': 'America/Los_Angeles', 'devicePayloadId': 'AK:1471209|4', 'mrt': '1592378443821', 'sourceGeoCountryCode': 'DE', 'slat': '50.0971', 'categoryDeviceGroup': '/IDS/Network', 'deviceCustomString2Label': 'sig_rev', 'destinationZoneURI': '/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 10.0.0.0-10.255.255.255', 'protocols': ['TCP']}}]"
```

### ArcSight logger response to STIX objects (Custom attributes)

### STIX observable output:


```json
{
    "type": "bundle",
    "id": "bundle--70e2ff95-dd13-47e9-976f-20e9f2ea560f",
    "spec_version": "2.0",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "arcsight",
            "identity_class": "events"
        },
        {
            "id": "observed-data--bf9c1651-5942-476b-8808-e358bb1d26c7",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2020-11-06T17:09:25.833Z",
            "modified": "2020-11-06T17:09:25.833Z",
            "objects": {
                "0": {
                    "type": "x-ibm-finding",
                    "time_observed": "2020-06-17T07:20:53.924Z",
                    "name": "NETBIOS SMB-DS C$ share unicode access",
                    "finding_type": "/Suspicious",
                    "src_geolocation": "Frankfurt am Main",
                    "dst_ip_ref": "7",
                    "severity": "3",
                    "src_ip_ref": "9"
                },
                "1": {
                    "type": "x-arcsight-event",
                    "model_confidence": "0",
                    "event_name": "NETBIOS SMB-DS C$ share unicode access",
                    "event_id": 1721582,
                    "asset_criticality": "0",
                    "priority": 5,
                    "relevance": "10",
                    "event_end_time": "2020-06-17T07:26:02.526Z",
                    "base_event_count": 1,
                    "event_start_time": "2020-06-17T07:26:02.526Z"
                },
                "2": {
                    "type": "x-arcsight-event-category",
                    "category_object": "/Host/Resource/File",
                    "category_outcome": "/Attempt",
                    "category_behavior": "/Access/Start",
                    "category_significance": "/Suspicious",
                    "category_technique": "/Exploit/Weak Configuration",
                    "category_device_group": "/IDS/Network"
                },
                "3": {
                    "type": "x-arcsight-event-device",
                    "device_version": "1.8",
                    "device_address_ref": "4",
                    "device_severity": "3",
                    "device_product": "Snort",
                    "device_receipt_time": "2004-10-31T08:29:05.000Z",
                    "device_vendor": "Snort",
                    "device_domain_name_ref": "8",
                    "device_event_category": "protocol-command-decode",
                    "device_time_zone": "America/Los_Angeles"
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "10.10.20.50"
                },
                "5": {
                    "type": "x-arcsight-event-source",
                    "source_geo_postal_code": "65933",
                    "source_geo_region_code": "HE",
                    "source_geo_location_info": "Frankfurt am Main",
                    "source_geo_country_code": "DE"
                },
                "6": {
                    "type": "network-traffic",
                    "src_port": 3950,
                    "dst_ref": "7",
                    "src_ref": "9",
                    "dst_port": 445,
                    "protocols": [
                        "tcp"
                    ]
                },
                "7": {
                    "type": "ipv4-addr",
                    "value": "10.10.20.7"
                },
                "8": {
                    "type": "domain-name",
                    "value": "10.10.20.50"
                },
                "9": {
                    "type": "ipv4-addr",
                    "value": "83.135.74.126"
                }
            },
            "first_observed": "2020-06-17T07:20:53.924Z",
            "last_observed": "2020-06-17T07:20:53.924Z",
            "number_observed": 1
        }
    ]
}
```

### Using Custom Categorical fields for advanced searches.
##### Commonly used custom fields:
|  Description  |  STIX Pattern  |  Sample Values  |
| --- | --- | --- |
| The product (smart-connector) name of the sensor device. | x-arcsight-event-device:product = "Sysmon" | [Sysmon, Unix, Snort, IntruShield, Tomcat, Microsoft Windows] |
| The vendor who manufactured or sold the sensor device. | x-arcsight-event-device:vendor = "Unix" | [Unix, Microsoft, Apache, Windows, ArcSight, Oracle, CISCO, Juniper, McAfee] |
| The device-specific description of some activity associated with the event. | x-arcsight-event-device:device_action = "Registry value set" | [Registry value set, Process Create, Process Terminated, login, destroy] |
| Describes the action taken with or by the object. | x-arcsight-event-category:category_behavior = "/Execute/Query" | [/Execute/Query, /Modify/Content, /Authentication/Verify, /Access/Start, /Found/Defective] |
| Indicates whether the action was successfully applied to the object. | x-arcsight-event-category:category_outcome = "/Success" | [/Success, /Failure, /Attempt] |
| Characterizes the event from a network intrusion - detection perspective. | x-arcsight-event-category:category_significance = "/Informational/Warning" | [/Informational/Warning, /Suspicious, /Hostile, /Recon, /Rule/Action/Success] |
| Describes the physical or virtual object that was the focus of the event. | x-arcsight-event-category:category_object = "/Host/Resource/Memory" | [/Host/Resource/Memory, /Host/Application/Database, /Actor/User, /Host/Operating System, Network] |
| Describes the type of event this event represents. | x-arcsight-event-category:device_group = "/Application" | [/Application, /Operating System, /Firewall, /VPN, /Security Information Manager] |

### STIX pattern - Example Usage:
```
translate arcsight query {} "[x-arcsight-event-device: product = 'Sysmon' AND windows-registry-key:key LIKE '%driverVersion'] START t'2020-06-20T01:00:00Z' STOP t'2020-06-30T01:00:00Z'"
```
### Translated Query:
```
{'queries': ['{"query": "deviceProduct = Sysmon AND filePath = *driverVersion", "start_time": "2020-06-20T01:00:00.000Z", "end_time": "2020-06-30T01:00:00.000Z"}']}
```

### Using Full Text search for searching non-indexed fields.

Full text search is implemented with a value-only search format (without the field name in the query) and hence only 'Equals' operator is supported for these attributes. <br/>
### STIX pattern - Example Usage:
```
translate arcsight query {} "[ipv6-addr:value = 'fe80:0:0:0:1411:a12d:7746:e3a'] START t'2020-06-20T01:00:00Z' STOP t'2020-06-30T01:00:00Z'"
```
### Translated Query:
```
{'queries': ['{"query": "fe80:0:0:0:1411:a12d:7746:e3a", "start_time": "2020-06-20T01:00:00.000Z", "end_time": "2020-06-30T01:00:00.000Z"}']}
```

### Exclusions 
ArcSight Logger does not provide operator support for the following attributes,
 
`IN / NOT IN Operator`
* Full text search attributes.

`LIKE Operator` 

* Integer type fields in ArcSight are not supported. Example: network-traffic:dst_port, src_port attributes.

* 'LIKE' Operator is not supported for fields with '_' wildcard character in the search query.

`MATCHES Operator` 

* Integer type fields in ArcSight are not supported. Example: network-traffic:dst_port, src_port attributes.


`NOT (Negation) Operator` 

* 'NOT' Operator is not supported for LIKE operation.

* 'NOT' Operator is not supported for full text search fields.