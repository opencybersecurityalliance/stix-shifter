# Symantec

## Supported STIX Mappings

See the [table of mappings](symantec_supported_stix.md) for the STIX objects and operators supported by this connector.


**Table of Contents**

- [Symantec API Endpoints](#symantec-api-endpoints)
- [Curl Command to test the API Endpoints](#curl-command-to-test-api-endpoints)
- [Format for calling stix-shifter from the command line](#format-for-calling-stix-shifter-from-the-command-line) 
- [Pattern expression with STIX and CUSTOM attributes - Single Observation](#single-observation)
- [Pattern expression with STIX and CUSTOM attributes - Multiple Observation](#multiple-observation)
- [STIX Execute Query](#stix-execute-query)
- [Types of Attributes](#types-of-attributes)
- [Limitations](#limitations)
- [Observations](#observations)
- [References](#references)
- [List of specific values for STIX attributes](#list-of-specific-values-for-STIX-attributes)
- [STIX pattern for custom attributes and sample values](#STIX-pattern-for-custom-attributes-and-sample-values)

### Symantec API Endpoints
| Connector Method | Symantec API Endpoint     | Method |
|-----|------|------|
| Ping Endpoint   | https://< server >/api/v1/oauth2/tokens | POST  | 
| Token Endpoint  | https://< server >/api/v1/oauth2/tokens | POST  |
| Results Endpoint | https://< server >/api/v1/event-search | POST  |


### CURL command to test API Endpoints
#### Ping 
```
curl -X POST https://api.sep.securitycloud.symantec.com/v1/oauth2/tokens -H “accept: application/json” -H “authorization: {{OAuth Credentials value}}" -H “content-type: application/x-www-form-urlencoded”
```
#### Token
```
curl -X POST https://api.sep.securitycloud.symantec.com/v1/oauth2/tokens -H “accept: application/json” -H “authorization: {{OAuth Credentials value}}" -H “content-type: application/x-www-form-urlencoded”
```
#### Results
```
curl --location --request POST "https://api.sep.securitycloud.symantec.com/v1/event-search" \
--header "Content-Type: application/json" \
--header "authorization: {bearer token}"
--data "{
    \"feature_name\": \"ALL\",
    \"query\": \"type_id:8020\",
    \"start_date\": \"2024-04-12T00:00:00.000+05:30\",
    \"end_date\": \"2024-05-11T00:00:00.000+05:30\",
    \"product\": \"SAEP\",
    \"limit\":2
}"
```

### Format for calling stix-shifter from the command line
```
python main.py `<translator_module>` `<query or result>` `<STIX identity object>` `<data>`
```
### Pattern expression with STIX and CUSTOM attributes

#### Single Observation

#### STIX Translate query to fetch the messages from a specific ipaddress
```shell
translate symantec_endpoint_security query {} "[x-oca-event:x_event_type=8003] START t'2024-04-01T11:00:00.000Z' STOP t'2024-04-10T00:00:00.000Z'"
```
#### STIX Translate query - output
```json
{
    "queries": [
        {
            "feature_name": "ALL",
            "product": "SAEP",
            "query": "type_id:\"8003\"",
            "start_date": "2024-04-01T11:00:00.000+00:00",
            "end_date": "2024-04-10T00:00:00.000+00:00"
        }
    ]
}
```

#### STIX Transmit results 

```shell
transmit symantec_endpoint_security "{\"host\":\"api.sep.securitycloud.symantec.com\"}" "{\"auth\":{\"token\":\"TzJJRC5JS2hTQi15lDSzJnLkIzZEt6TFN0NmYxNWNoMGs6MXY1bDUxdDc4cmIzNG0OWMyZDIy\"}}" results "{\"feature_name\":\"ALL\",\"query\":\"type_id:8003\", \"start_date\":\"2024-05-01T00:00:00.000+05:30\", \"end_date\": \"2024-05-06T09:00:00.000+05:30\",\"product\":\"SAEP\",\"limit\":1}"
0
1
```

#### STIX Transmit results - output
```json
{
    "success": true,
    "data": [
        {
            "device_os_type_id": 100,
            "lineage": [
                "C:\\Windows\\System32\\services.exe",
                "C:\\Windows\\System32\\wininit.exe"
            ],
            "feature_uid": "1DF0351C-146D-4F07-B155-BF5C7077FF40",
            "type": "event_query_results",
            "seq_num": 1,
            "ref_uid": "1DFB782F-A766-4675-9E54-C054F8B2BAAA",
            "legacy_product_uid": "ad66b334-9eb8-bf35-3f4e-f172b06200b0",
            "id": 5,
            "product_uid": "31B0C880-0229-49E8-94C5-48D56B1BD7B9",
            "feature_name": "DETECTION_RESPONSE",
            "device_group": "Default/TestEDRGroup",
            "product_name": "Symantec Endpoint Security",
            "version": "1.0.0",
            "command_uid": "",
            "device_ip": "1.1.1.1",
            "device_vhost": 12,
            "user_name": "SYSTEM",
            "timezone": 0,
            "device_domain": "WORKGROUP",
            "product_ver": "14.3.10148.8000",
            "is_npvdi_client": false,
            "device_name": "HOST_NAME",
            "category_id": 5,
            "device_networks": [
                {
                    "ipv4": "1.1.1.1",
                    "ipv6": "xx00:0000:0000:0000:00xx:xx0x:0000:00x0",
                    "mac": "0x:1x:11:11:0x:11"
                }
            ],
            "device_os_name": "Windows Server 2019 Datacenter Edition",
            "type_id": 8003,
            "actor": {
                "session_id": 0,
                "pid": 1880,
                "uid": "C03AA311-0907-F1EF-848A-EAEACDB378C2",
                "tid": 1132,
                "start_time": "2024-05-03T04:44:04.920Z",
                "cmd_line": "C:\\Windows\\system32\\svchost.exe -k netsvcs -p -s Schedule",
                "integrity_id": 6,
                "file": {
                    "type_id": 1,
                    "created": "2022-09-14T16:17:52.744Z",
                    "modified": "2022-09-14T16:17:52.744Z",
                    "md5": "4dd18f001ac31d5f48f50f99e4aa1761",
                    "sha2": "2b105fb111b1bcd111b1111111b3a11c60b111eef1111d3bb0099e1111aaf6b",
                    "size": 51736,
                    "security_descriptor": "O:S-1-5-5-0-11111G:SYD:(A;;0x1fffff;;;S-1-5-5-0-71241)(A;;0x1400;;;BA)S:AI",
                    "normalized_path": "CSIDL_SYSTEM\\svchost.exe",
                    "path": "c:\\windows\\system32\\svchost.exe",
                    "uid": "281474976968790",
                    "name": "svchost.exe",
                    "folder": "c:\\windows\\system32",
                    "original_name": "svchost.exe"
                },
                "user": {
                    "name": "SYSTEM",
                    "sid": "S-1-5-11",
                    "domain": "NT AUTHORITY"
                },
                "cmd_line_raw_length": 57
            },
            "device_mac": "0x:1x:11:11:0x:11",
            "device_uid": "X4oOxiAoQO6SuZAfO6lm4Q",
            "org_unit_uid": "_RE5UsoeSKSrteDkP3U2Mw",
            "severity_id": 1,
            "logging_device_post_time": "2024-05-03T04:56:13.704Z",
            "device_time": "2024-05-03T04:56:13.704Z",
            "file": {
                "path": "c:\\windows\\system32\\tasks\\microsoft\\windows\\windowsupdate\\scheduled start",
                "normalized_path": "CSIDL_SYSTEM\\tasks\\microsoft\\windows\\windowsupdate\\scheduled start",
                "size": 5208,
                "name": "scheduled start",
                "folder": "c:\\windows\\system32\\tasks\\microsoft\\windows\\windowsupdate",
                "content_type": {
                    "family_id": 0,
                    "type_id": 1
                }
            },
            "file_result": {
                "size": 5034
            },
            "edr_enriched_data": {
                "category_name": "Generic Data to be sent to ATP",
                "category_id": 201,
                "rule_id": 2101451,
                "rule_name": "IF.SchtasksChange!g1"
            },
            "feature_ver": "edr/1.3.0",
            "is_user_present": false,
            "event_data_type": "fdr",
            "user": {
                "domain": "NT AUTHORITY",
                "name": "SYSTEM",
                "sid": "S-1-5-18"
            },
            "device_os_ver": "10.0.17763",
            "policy": {
                "uid": "a7124b68-abc1-43a4-8e44-716fb1966646",
                "name": "Default Detection and Response Policy",
                "version": "1"
            },
            "trans_event_raw_length": 2874,
            "attacks": [
                {
                    "technique_uid": "T1053",
                    "technique_name": "Scheduled Task/Job",
                    "tactic_ids": [
                        2,
                        3,
                        4
                    ],
                    "tactic_uids": [
                        "TA0002",
                        "TA0003",
                        "TA0004"
                    ],
                    "sub_technique_name": "Scheduled Task",
                    "sub_technique_uid": "T1053.005"
                }
            ],
            "customer_uid": "IKhSB-yfRK2xeUR-xyCK2g",
            "device_public_ip": "22.22.22.22",
            "domain_uid": "B3dKzLSzR9CScPYAGhkgxA",
            "time": "2024-05-03T04:56:13.704Z",
            "log_time": "2024-05-03T04:56:19.401Z",
            "uuid": "8003:778fc080-0909-11ef-e17f-0000061b19b7",
            "indexDate": "2024-05-03",
            "indexHash": "fdr_4_t2",
            "log_name": "c1.fdr_4_t2_2024-05-03",
            "es.mapping.id": "uuid",
            "epochLogTime": 1714712179401,
            "es.mapping.version": "epochLogTime"
        }
    ]
}
```


#### STIX Translate results

```json
{
    "type": "bundle",
    "id": "bundle--e35ce5e3-6575-4026-a8d7-39227df87836",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "Symantec Endpoint Security",
            "identity_class": "events",
            "created": "2023-04-11T16:11:11.878Z",
            "modified": "2023-04-11T16:11:11.878Z"
        },
        {
            "id": "observed-data--186b1e27-0fd5-44c4-a15b-71e7a89c4ea5",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2024-05-06T11:54:14.689Z",
            "modified": "2024-05-06T11:54:14.689Z",
            "objects": {
                "0": {
                    "type": "software",
                    "x_os_type": "Windows",
                    "name": "Windows Server 2019 Datacenter Edition",
                    "version": "10.0.17763"
                },
                "1": {
                    "type": "x-oca-event",
                    "action": "event_query_results",
                    "outcome": "Command Script Run",
                    "x_feature_name": "DETECTION_RESPONSE",
                    "provider": "Symantec Endpoint Security",
                    "x_event_type_version": "1.0.0",
                    "timezone": 0,
                    "x_provider_version": "14.3.10148.8000",
                    "host_ref": "2",
                    "category": "System Activity",
                    "x_event_type": 8003,
                    "process_ref": "6",
                    "file_ref": "7",
                    "severity": 15,
                    "user_ref": "11",
                    "x_policy_ref": "12",
                    "created": "2024-05-03T04:56:13.704Z",
                    "code": "8003:778fc080-0909-11ef-e17f-0000061b19b7"
                },
                "2": {
                    "type": "x-oca-asset",
                    "x_host_group": "Default/TestEDRGroup",
                    "ip_refs": [
                        "3",
                        "15"
                    ],
                    "hostname": "HOST_NAME",
                    "mac_refs": [
                        "4"
                    ],
                    "os_ref": "0"
                },
                "3": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1",
                    "resolves_to_refs": [
                        "4"
                    ]
                },
                "4": {
                    "type": "mac-addr",
                    "value": "0x:1x:11:11:0x:11"
                },
                "6": {
                    "type": "process",
                    "pid": 1880,
                    "x_process_tid": 1132,
                    "created": "2024-05-03T04:44:04.920Z",
                    "command_line": "C:\\Windows\\system32\\svchost.exe -k netsvcs -p -s Schedule",
                    "binary_ref": "7",
                    "creator_user_ref": "9"
                },
                "7": {
                    "type": "file",
                    "x_file_type": "File",
                    "created": "2022-09-14T16:17:52.744Z",
                    "modified": "2022-09-14T16:17:52.744Z",
                    "hashes": {
                        "MD5": "4xx18x001xx31x5x48x50x99x4xx1761",
                        "SHA-256": "2b105fb111b1bcd111b1111111b3a11c60b111eef1111d3bb0099e1111aaf6b"
                    },
                    "size": 51736,
                    "name": "svchost.exe",
                    "parent_directory_ref": "8"
                },
                "8": {
                    "type": "directory",
                    "path": "c:\\windows\\system32"
                },
                "9": {
                    "type": "user-account",
                    "user_id": "SYSTEM",
                    "x_user_sid": "S-1-5-11",
                    "x_user_domain": "NT AUTHORITY"
                },
                "10": {
                    "type": "file",
                    "parent_directory_ref": "8",
                    "size": 5208,
                    "name": "scheduled start",
                    "x_family_type": "Unknown",
                    "x_file_type": "Application"
                },
                "11": {
                    "type": "user-account",
                    "x_user_domain": "NT AUTHORITY",
                    "user_id": "SYSTEM",
                    "x_user_sid": "S-1-5-18"
                },
                "12": {
                    "type": "x-symantec-policy",
                    "name": "Default Detection and Response Policy",
                    "version": "1"
                },
                "14": {
                    "type": "x-ibm-ttp-tagging",
                    "extensions": {
                        "'mitre-attack-ext'": {
                            "technique_id": "T1053",
                            "technique_name": "Scheduled Task/Job",
                            "tactic_id": [
                                "TA0002",
                                "TA0003",
                                "TA0004"
                            ]
                        }
                    },
                    "name": "Scheduled Task/Job"
                },
                "15": {
                    "type": "ipv4-addr",
                    "value": "22.22.22.22"
                }
            },
            "last_observed": "2024-05-03T04:56:13.704Z",
            "first_observed": "2024-05-03T04:56:13.704Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```

#### Multiple Observation

```shell
translate 
symantec_endpoint_security 
query {} 
"[x-oca-event:category='Security' AND x-oca-event:action='SCAN'] START t'2024-04-01T11:00:00.000Z' STOP t'2024-04-10T00:00:00.000Z'"
```

#### STIX Multiple observation - output
```json
{
    "queries": [
        {
            "feature_name": "ALL",
            "product": "SAEP",
            "query": "(category_id:\"1\") AND (type:\"SCAN\")",
            "start_date": "2024-04-01T11:00:00.000+00:00",
            "end_date": "2024-04-10T00:00:00.000+00:00"
        }
    ]
}
```

### STIX Execute query
```shell
execute 
symantec_endpoint_security 
symantec_endpoint_security 
"{\"type\":\"identity\",\"id\":\"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\",\"name\":\"Symantec Endpoint Security\",\"identity_class\":\"events\", \"created\": \"2024-05-01T00:00:00.000Z\",\"modified\": \"2024-05-10T00:00:00.000Z\"}" 
"{\"host\":\"api.sep.securitycloud.symantec.com\"}" "{\"auth\":{\"token\":\"TzJJRC5JS2hTDUxdDc4cmIzNGE5NGVjZm50ZmkzcWd2aGh0OWMyZDIy\"}}" 
"[x-oca-event:category='Security' AND x-oca-event:action='SCAN'] START t'2024-04-01T11:00:00.000Z' STOP t'2024-04-10T00:00:00.000Z'"
```

#### STIX Execute query - output
```json
{
    "type": "bundle",
    "id": "bundle--7c7aae92-e863-454e-b7bd-7ca2f04bbc0a",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "Symantec Endpoint Security",
            "identity_class": "events",
            "created": "2023-04-11T16:11:11.878Z",
            "modified": "2023-04-11T16:11:11.878Z"
        },
        {
            "id": "observed-data--0e0cd275-588a-4fd1-9213-a267caa8a586",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2024-05-06T13:21:47.927Z",
            "modified": "2024-05-06T13:21:47.927Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "category": "Security",
                    "host_ref": "2",
                    "duration": 0,
                    "x_feature_name": "MALWARE_PROTECTION",
                    "outcome": "Blocked",
                    "description": "Scan started on selected drives and folders and all extensions.",
                    "x_policy_ref": "5",
                    "x_provider_version": "14.3.10148.8000",
                    "severity": 15,
                    "action": "SCAN",
                    "x_event_type": 8020,
                    "x_event_type_version": "1.0",
                    "provider": "Symantec Endpoint Security",
                    "timezone": 0,
                    "user_ref": "13",
                    "created": "2024-05-06T08:33:25Z",
                    "code": "8020:4e0ef880-0b83-11ef-ea5d-000006df1b0c"
                },
                "1": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1",
                    "resolves_to_refs": [
                        "4"
                    ]
                },
                "2": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "1",
                        "12"
                    ],
                    "geo_ref": [
                        "3"
                    ],
                    "mac_refs": [
                        "4"
                    ],
                    "hostname": "HOST_NAME",
                    "x_host_group": "Default/TestDevGroup",
                    "os_ref": "11"
                },
                "3": {
                    "type": "x-oca-geo",
                    "name": "Default",
                    "x_is_on_premises": false
                },
                "4": {
                    "type": "mac-addr",
                    "value": "11:1X:XX:X1:11:X1"
                },
                "5": {
                    "type": "x-symantec-policy",
                    "name": "Default Antimalware Policy",
                    "version": "1"
                },
                "7": {
                    "type": "ipv6-addr",
                    "value": "xx11::1x1x:11xx:11xx:x1x1",
                    "resolves_to_refs": [
                        "4"
                    ]
                },
                "8": {
                    "type": "ipv4-addr",
                    "value": "2.2.2.2",
                    "resolves_to_refs": [
                        "10"
                    ]
                },
                "9": {
                    "type": "ipv6-addr",
                    "value": "xx22::22x2:x0xx:22x2:22xx",
                    "resolves_to_refs": [
                        "10"
                    ]
                },
                "10": {
                    "type": "mac-addr",
                    "value": "22:X2:22:X2:X2:22"
                },
                "11": {
                    "type": "software",
                    "name": "Windows Server 2019 Datacenter Edition",
                    "x_os_type": "Windows"
                },
                "12": {
                    "type": "ipv4-addr",
                    "value": "3.3.3.3"
                },
                "13": {
                    "type": "user-account",
                    "user_id": "SYSTEM"
                }
            },
            "number_observed": 1,
            "last_observed": "2024-05-06T08:33:25Z",
            "first_observed": "2024-05-06T08:33:25Z"
        }
    ],
    "spec_version": "2.0"
}
```
### Types of Attributes

| Type                      | Description                                | Example                                                                                                            |
|---------------------------|--------------------------------------------|--------------------------------------------------------------------------------------------------------------------|
| Dictionary fields         | A key value pair attributes.               | {"user_name": "SYSTEM"}, {"feature_name": "MALWARE_PROTECTION"}                                                              |
| List of dictionary fields | A list containing one or more dictionaries | "device_networks": [{"ipv4": "1.1.1.1", "ipv6": "xx22::2x2x:22xx:22xx:x2x2", "mac": "11:1X:XX:X1:11:X1" }, { "ipv4": "2.2.2.2", "ipv6": "xx11::1x1x:11xx:11xx:x1x1", "mac": "22:X2:22:X2:X2:22"}] |

### Observations
- Attribute "x-oca-asset.host_type" mapped to data source attribute "device_type" is currently not 
  available for value "Server" in Symantec Endpoint Security client version (14.3 RU8) and may be available in future versions.

### Limitations
- The maximum number of API calls for events is limited to 500 per hour.

### References
- [Symantec Endpoint Security](https://techdocs.broadcom.com/us/en/symantec-security-software/endpoint-security-and-management/endpoint-security/sescloud.html)
- [Symantec ICD Schema](https://icd-schema.symantec.com/)
- [Symantec API](https://apidocs.in.securitycloud.symantec.com/)

### List of specific values for STIX attributes

### x-oca-event:category specific values
| Searchable Values |
|-------------------|
| Security |
| Application Activity |
| System Activity |

### x-oca-event:outcome specific values
| Searchable Values |
|-------------------|
| Unknown |
| Blocked |
| Allowed |
| No Action |
| Logged |
| Command Script Run |
| Corrected |
| Partially Corrected |
| Uncorrected |
| Delayed |
| Deleted |
| Quarantined |
| Restored |
| Detected |
| Exonerated |
| Tagged |

### x-oca-event:x_event_status specific values
| Searchable Values |
|-------------------|
| Unknown |
| Success |
| Failure |
| In Progress |
| Partial Success |

### x-ibm-finding:finding_type specific values
| Searchable Values |
|-------------------|
| policy |
| threat |

### x-ibm-finding:x_threat_type_id specific values
| Searchable Values |
|-------------------|
| Malware |
| Behavioral |
| Potentially Unwanted Applications |
| Exploit (PEP) |
| Heuristic |
| Security Risk |

### file:x_type specific values
| Searchable Values |
|-------------------|
| File |
| Directory |
| Hard Link |
| Mount |
| Node |
| Symbolic Link |
| Named Pipe |
| Socket |
| Device |
| Email |
| Memory File |
| File in container |

### software:x_os_type specific values
| Searchable Values |
|-------------------|
| Unknown |
| Windows |
| Linux |
| Solaris |
| AIX |
| HP-UX |
| Macintosh |
| iOS |
| Android |
| Windows Mobile |
| iPadOS |
| Other |

### network-traffic:x_direction, email-message:x_direction specific values
| Searchable Values |
|-------------------|
| Unknown |
| Inbound |
| Outbound |

### x-kernel-resource.type_id values
| Searchable Values |
|-------------------|
| Unknown |
| Shared mutex |
| System call |
| Named pipe |

### STIX pattern for custom attributes and sample values
|  Description  |  STIX Pattern  |  Sample Values  |
| --- | --- | --- |
| Network Connection Direction  | network-traffic:x_direction | [network-traffic:x_direction = 'Inbound'] |
| The Identifier of the thread associated with the event, as returned by the operating system.  | process:x_process_tid | [process:x_process_tid = 1234] |
| The user security identifier (SID).  | user-account:x_sid | [user-account:x_sid = 'S-1-1-11'] |
| The file type.  | file:x_type | [file:x_type = 'Directory'] |
| The company name on the certificate that signed the file..  | file:x_signature_company_name | [file:x_signature_company_name LIKE 'Amazon'] |
| The general content type of a file. | file:x_content_type | [file:x_content_type = 'Application'] |
| The type of the operating system. | software:x_os_type | [software:x_os_type = 'Windows'] |
| The event type. | x-oca-event:x_event_type | [x-oca-event:x_event_type = 8001] |
| The event type category. | x-oca-event:category | [x-oca-event:category = 'Security'] |
| The outcome of the event. | x-oca-event:outcome | [x-oca-event:outcome = 'Blocked'] |
| The cross-platform event status. | x-oca-event:x_event_status | [x-oca-event:x_event_status  = 'Success'] |
| The description of the location. | x-oca-geo:name | [x-oca-geo:name = 'Default'] |
| The name given to the policy. | x-symantec-policy:name | [x-symantec-policy:name = 'Default Detection and Response Policy'] |
| The name of the kernel resource. | x-kernel-resource:name | [x-kernel-resource:name = 'Default name'] |
| The type of the kernel resource. | x-kernel-resource:type_id | [x-kernel-resource:type_id  = 'System call'] |
| The name of the peripheral device. | x-peripheral-device:name | [x-peripheral-device:name  = 'keyboard'] |
| The command line used to launch the startup application, service, process or job. | process:command_line | [process:command_line = 'C:\\Windows\\system32\\services.exe']|
| The registry key object describes a Windows registry key. | windows-registry-key:key | [windows-registry-key:key = 'HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\W32Time\\SecureTimeLimits\\RunTime\\'] |