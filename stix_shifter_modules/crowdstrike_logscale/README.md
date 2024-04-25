# Crowdstrike Logscale

## Supported STIX Mappings

See the [table of mappings](crowdstrike_logscale_supported_stix.md) for the STIX objects and operators supported by this connector.

**Table of Contents**
- [Crowdstrike Logscale API Endpoints](#crowdstrike-logscale-api-endpoints)
- [Curl Command to test the API Endpoints](#curl-command-to-test-api-endpoints)
- [Format of calling Stix shifter from Command Line](#format-for-calling-stix-shifter-from-the-command-line)
- [Pattern expression with STIX attributes and CUSTOM attributes - Single Observation](#single-observation)
- [Pattern expression with STIX and CUSTOM attributes - Multiple Observation](#multiple-observation)
- [STIX Execute Query](#stix-execute-query)
- [Types of Attributes](#type-of-attributes)
- [Current Connector Features](#current-connector-features)
- [Connector Extension](#connector-extension)
- [Recommendations](#recommendations)
- [Limitations](#limitations)
- [References](#references)
- [Appendix](#appendix)

### Crowdstrike Logscale API Endpoints

   | Connector Method | Crowdstrike Logscale API Endpoint                                              | Method |
   |------------------|--------------------------------------------------------------------------------|--------|
   | Ping Endpoint    | Status API - api/v1/status                                                     | GET    |
   | Query Endpoint   | Query Job API - api/v1/repositories/{respository}/queryjobs                                 | POST   |
   | Status Endpoint  | Query Job Poll API - api/v1/repositories/{respository}/queryjobs/{Query Job id} | GET    |
   | Results Endpoint | Query Job Poll API - api/v1/repositories/{respository}/queryjobs/{Query Job id}                                       | GET    |
   | Delete Endpoint  | Query Job Poll API - api/v1/repositories/{respository}/queryjobs/{Query Job id}                                       | DELETE |


### CURL command to test API Endpoints
#### Ping 
```
curl --location 'https://{hostname}/api/v1/status' \
--header 'Accept: application/json'
```
#### Query
```
curl --location 'https://{hostname}/api/v1/repositories/{repository_name}/queryjobs' \
--header 'Accept: application/json' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer {Repository API token}' \
--data '{
    "queryString": "device.local_ip =~ cidr(subnet=\"1.1.1.1/32\") | tail(10)",
    "start": 1702598400000,
    "end": 1707461040000
}'
```

#### Results
```
curl --location 'https://{hostname}/api/v1/repositories/{repository_name}/queryjobs/{id}' \
--header 'Accept: application/json' \
--header 'Authorization: Bearer {Repository API token}'
```

### Format for calling stix-shifter from the command line
```
python main.py `<translator_module>` `<query or result>` `<STIX identity object>` `<data>`

```

### Pattern expression with STIX and CUSTOM attributes

#### Single Observation

#### STIX Translate query 
```shell
translate crowdstrike_logscale query "{}" "[process:name IN ('cmd.exe','calc.exe') AND x-oca-asset:hostname LIKE 'EC2' OR ipv4-addr:value ISSUBSET '1.1.1.1/32'] START t'2024-03-20T00:00:00.000Z' STOP t'2024-04-01T00:00:00.000Z'"
```
#### STIX Translate query - Output
```json
{
    "queries": [
        {
            "source": "crowdstrikeedr",
            "queryString": "device.local_ip =~ cidr(subnet=\"1.1.1.1/32\") | tail(10000)",
            "start": 1710892800000,
            "end": 1711929600000
        },
        {
            "source": "crowdstrikeedr",
            "queryString": "device.external_ip =~ cidr(subnet=\"1.1.1.1/32\") | tail(10000)",
            "start": 1710892800000,
            "end": 1711929600000
        },
        {
            "source": "crowdstrikeedr",
            "queryString": "(device.hostname = /EC2/i and @rawstring = /\"behaviors\"\\s*:\\s*\\[.*\"filename\"\\s*:\\s*(\"cmd\\.exe\"|\"calc\\.exe\")/) | tail(10000)",
            "start": 1710892800000,
            "end": 1711929600000
        }
    ]
}
```
#### STIX Transmit Query
```shell
transmit
crowdstrike_logscale
"{\"host\":\"xxx\",\"repository\":\"TestRepository\"}"
"{\"auth\":{\"api_token\": \"123\"}}"
results
"{ \"source\": \"crowdstrikeedr\", \"queryString\": \"device.external_ip =~ cidr(subnet=\\"1.1.1.1/32\\") | tail(10000)\", \"start\": 1710892800000, \"end\": 1711929600000 }"
0
1
```
#### STIX Transmit Query - Output

```json
{
    "success": true,
    "search_id": "P7-xxxxxxxxx:crowdstrikeedr"
}
```
#### STIX Transmit Status
```shell
transmit
crowdstrike_logscale
"{\"host\":\"xxx\",\"repository\":\"TestRepository\"}"
"{\"auth\":{\"api_token\": \"123\"}}"
status "P7-xxxxxxxxx:crowdstrikeedr"
```

#### STIX Transmit Status - Output

```json
{
    "success": true,
    "status": "COMPLETED",
    "progress": 100
}
```
#### STIX Transmit Results
```shell
transmit
crowdstrike_logscale
"{\"host\":\"xxx\",\"repository\":\"TestRepository\"}"
"{\"auth\":{\"api_token\": \"123\"}}"
results "P7-xxxxxxxxx:crowdstrikeedr" 0 1
```

#### STIX Transmit Results - Output
```json
{
    "success": true,
    "metadata": {
            "input_query_string": "cidr(subnet=\"1.1.1.1/32\",field=device.external_ip)",
            "start": 1710892800000,
             "last_event_id": "ATzrtyg4xCKOqQnD9NodpvsY_363_125_1711549348",
             "last_event_timestamp": 1711549348062
    },
    "data": [
        {
            "crowdstrikeedr": {
                "@timestamp": 1711549348062,
                "@timestamp.nanos": "194000",
                "#repo": "TestRepository",
                "#type": "CrowdStrike_Spotlight",
                "@id": "ATzrtyg4xCKOqQnD9NodpvsY_363_125_1711549348",
                "@ingesttimestamp": "1711549348586",
                "@rawstring": "{\"cid\": \"123\", \"created_timestamp\": \"2024-01-23T12:33:15.170758259Z\", \"detection_id\": \"ldt:xyz:123\", \"device\": {\"device_id\": \"7adb123\", \"cid\": \"123\", \"agent_load_flags\": \"1\", \"agent_local_time\": \"2024-01-23T12:32:59.287Z\", \"agent_version\": \"7.05.17706.0\", \"bios_manufacturer\": \"Xen\", \"bios_version\": \"4.11.amazon\", \"config_id_base\": \"65994763\", \"config_id_build\": \"17706\", \"config_id_platform\": \"3\", \"external_ip\": \"1.1.1.1\", \"hostname\": \"host\", \"first_seen\": \"2023-05-16T05:10:55Z\", \"last_login_timestamp\": \"2024-01-04T06:12:09Z\", \"last_login_user\": \"test user\", \"last_seen\": \"2024-01-23T12:33:10Z\", \"local_ip\": \"2.2.2.2\", \"mac_address\": \"01-01-01-01-01-01\", \"major_version\": \"10\", \"minor_version\": \"0\", \"os_version\": \"Windows Server 2022\", \"platform_id\": \"0\", \"platform_name\": \"Windows\", \"product_type\": \"3\", \"product_type_desc\": \"Server\", \"status\": \"normal\", \"system_manufacturer\": \"Xen\", \"system_product_name\": \"HVM domU\", \"groups\": [\"97350feebe4541e8a615c0d3f18acdf3\", \"bb1e1190b46348e69e10785030e8b23d\"], \"modified_timestamp\": \"2024-01-23T12:33:13Z\", \"instance_id\": \"i-123\", \"service_provider\": \"AWS_EC2_V2\", \"service_provider_account_id\": \"98765\"}, \"behaviors\": [{\"device_id\": \"7adb123\", \"timestamp\": \"2024-01-23T12:33:07Z\", \"template_instance_id\": \"3\", \"behavior_id\": \"41002\", \"filename\": \"conhost.exe\", \"filepath\": \"\\\\Device\\\\conhost.exe\", \"alleged_filetype\": \"exe\", \"cmdline\": \"C:\\\\conhost.exe 0xffffffff -ForceV1\", \"scenario\": \"suspicious_activity\", \"objective\": \"Falcon Detection Method\", \"tactic\": \"Custom Intelligence\", \"tactic_id\": \"CSTA0005\", \"technique\": \"Indicator of Attack\", \"technique_id\": \"CST0004\", \"display_name\": \"CustomIOAWinMedium\", \"description\": \"A process triggered a medium severity custom rule.\", \"severity\": 50, \"confidence\": 100, \"ioc_type\": \"\", \"ioc_value\": \"\", \"ioc_source\": \"\", \"ioc_description\": \"\", \"user_name\": \"user1\", \"user_id\": \"S-1-5-18\", \"control_graph_id\": \"ctg:xyz:123\", \"triggering_process_graph_id\": \"pid:7adb:123\", \"sha256\": \"1010101010101010101010100101100101010101010101010101010101010100\", \"md5\": \"11111111111111111111111111111111\", \"parent_details\": {\"parent_sha256\": \"\", \"parent_md5\": \"\", \"parent_cmdline\": \"\", \"parent_process_graph_id\": \"pid:xyz:123\"}, \"pattern_disposition\": 10240, \"pattern_disposition_details\": {\"indicator\": false, \"detect\": false, \"inddet_mask\": false, \"sensor_only\": false, \"rooting\": false, \"kill_process\": false, \"kill_subprocess\": false, \"quarantine_machine\": false, \"quarantine_file\": false, \"policy_disabled\": false, \"kill_parent\": false, \"operation_blocked\": false, \"process_blocked\": true, \"registry_operation_blocked\": false, \"critical_process_disabled\": true, \"bootup_safeguard_enabled\": false, \"fs_operation_blocked\": false, \"handle_operation_downgraded\": false, \"kill_action_failed\": false, \"blocking_unsupported_or_disabled\": false, \"suspend_process\": false, \"suspend_parent\": false}, \"rule_instance_id\": \"3\", \"rule_instance_version\": 3}], \"email_sent\": false, \"first_behavior\": \"2024-01-23T12:33:07Z\", \"last_behavior\": \"2024-01-23T12:33:07Z\", \"max_confidence\": 100, \"max_severity\": 50, \"max_severity_displayname\": \"Medium\", \"show_in_ui\": true, \"status\": \"new\", \"hostinfo\": {\"domain\": \"\"}, \"seconds_to_triaged\": 0, \"seconds_to_resolved\": 0, \"behaviors_processed\": [\"pid:7adb:123:41002\"], \"date_updated\": \"2024-03-27T14:22:28.062194Z\"}",
                "@timezone": "Z",
                "behaviors": [
                    {
                        "alleged_filetype": "exe",
                        "behavior_id": "41002",
                        "cmdline": "C:\\conhost.exe 0xffffffff -ForceV1",
                        "confidence": "100",
                        "control_graph_id": "ctg:xyz:123",
                        "description": "A process triggered a medium severity custom rule.",
                        "device_id": "7adb123",
                        "display_name": "CustomIOAWinMedium",
                        "filename": "conhost.exe",
                        "filepath": "\\Device\\conhost.exe",
                        "md5": "11111111111111111111111111111111",
                        "objective": "Falcon Detection Method",
                        "parent_details": {
                            "parent_process_graph_id": "pid:xyz:123"
                        },
                        "pattern_disposition": "10240",
                        "pattern_disposition_details": {
                            "blocking_unsupported_or_disabled": "false",
                            "bootup_safeguard_enabled": "false",
                            "critical_process_disabled": "true",
                            "detect": "false",
                            "fs_operation_blocked": "false",
                            "handle_operation_downgraded": "false",
                            "inddet_mask": "false",
                            "indicator": "false",
                            "kill_action_failed": "false",
                            "kill_parent": "false",
                            "kill_process": "false",
                            "kill_subprocess": "false",
                            "operation_blocked": "false",
                            "policy_disabled": "false",
                            "process_blocked": "true",
                            "quarantine_file": "false",
                            "quarantine_machine": "false",
                            "registry_operation_blocked": "false",
                            "rooting": "false",
                            "sensor_only": "false",
                            "suspend_parent": "false",
                            "suspend_process": "false"
                        },
                        "rule_instance_id": "3",
                        "rule_instance_version": "3",
                        "scenario": "suspicious_activity",
                        "severity": "50",
                        "sha256": "1010101010101010101010100101100101010101010101010101010101010100",
                        "tactic": "Custom Intelligence",
                        "tactic_id": "CSTA0005",
                        "technique": "Indicator of Attack",
                        "technique_id": "CST0004",
                        "template_instance_id": "3",
                        "timestamp": "2024-01-23T12:33:07Z",
                        "triggering_process_graph_id": "pid:7adb:123",
                        "user_id": "S-1-5-18",
                        "user_name": "user1"
                    }
                ],
                "behaviors_processed": [
                    "pid:7adb:123:41002"
                ],
                "cid": "123",
                "created_timestamp": "2024-01-23T12:33:15.170758259Z",
                "date_updated": "2024-03-27T14:22:28.062194Z",
                "detection_id": "ldt:xyz:123",
                "device": {
                    "agent_load_flags": "1",
                    "agent_local_time": "2024-01-23T12:32:59.287Z",
                    "agent_version": "7.05.17706.0",
                    "bios_manufacturer": "Xen",
                    "bios_version": "4.11.amazon",
                    "cid": "123",
                    "config_id_base": "65994763",
                    "config_id_build": "17706",
                    "config_id_platform": "3",
                    "device_id": "7adb123",
                    "external_ip": "1.1.1.1",
                    "first_seen": "2023-05-16T05:10:55Z",
                    "groups": [
                        "97350feebe4541e8a615c0d3f18acdf3",
                        "bb1e1190b46348e69e10785030e8b23d"
                    ],
                    "hostname": "host",
                    "instance_id": "i-123",
                    "last_login_timestamp": "2024-01-04T06:12:09Z",
                    "last_login_user": "test user",
                    "last_seen": "2024-01-23T12:33:10Z",
                    "local_ip": "2.2.2.2",
                    "mac_address": "01-01-01-01-01-01",
                    "major_version": "10",
                    "minor_version": "0",
                    "modified_timestamp": "2024-01-23T12:33:13Z",
                    "os_version": "Windows Server 2022",
                    "platform_id": "0",
                    "platform_name": "Windows",
                    "product_type": "3",
                    "product_type_desc": "Server",
                    "service_provider": "AWS_EC2_V2",
                    "service_provider_account_id": "98765",
                    "status": "normal",
                    "system_manufacturer": "Xen",
                    "system_product_name": "HVM domU"
                },
                "email_sent": "false",
                "first_behavior": "2024-01-23T12:33:07Z",
                "last_behavior": "2024-01-23T12:33:07Z",
                "max_confidence": "100",
                "max_severity": "50",
                "max_severity_displayname": "Medium",
                "seconds_to_resolved": "0",
                "seconds_to_triaged": "0",
                "show_in_ui": "true",
                "status": "new",
                "finding_type": "alert"
            }
        }
    ]
}
```

#### STIX Translate results
```json
{
    "type": "bundle",
    "id": "bundle--fc54a014-447c-4cde-88ee-129a4083ca24",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "crowdstrike_logscale",
            "identity_class": "events",
            "created": "2024-04-02T13:22:50.336Z",
            "modified": "2024-04-02T13:22:50.336Z"
        },
        {
            "id": "observed-data--3a204585-59bc-481b-898b-a065965f82e5",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2024-04-03T13:24:07.549Z",
            "modified": "2024-04-03T13:24:07.549Z",
            "objects": {
                "0": {
                    "type": "file",
                    "x_extension": "exe",
                    "name": "conhost.exe",
                    "x_path": "\\Device\\conhost.exe",
                    "parent_directory_ref": "3",
                    "hashes": {
                        "MD5": "11111111111111111111111111111111",
                        "SHA-256": "1010101010101010101010100101100101010101010101010101010101010100"
                    }
                },
                "1": {
                    "type": "x-crowdstrike-detection-behavior",
                    "behavior_id": "41002",
                    "confidence": 100,
                    "control_graph_id": "ctg:xyz:123",
                    "description": "A process triggered a medium severity custom rule.",
                    "display_name": "CustomIOAWinMedium",
                    "process_ref": "2",
                    "objective": "Falcon Detection Method",
                    "pattern_disposition": 10240,
                    "pattern_disposition_details": {
                        "blocking_unsupported_or_disabled": "false",
                        "bootup_safeguard_enabled": "false",
                        "critical_process_disabled": "true",
                        "detect": "false",
                        "fs_operation_blocked": "false",
                        "handle_operation_downgraded": "false",
                        "inddet_mask": "false",
                        "indicator": "false",
                        "kill_action_failed": "false",
                        "kill_parent": "false",
                        "kill_process": "false",
                        "kill_subprocess": "false",
                        "operation_blocked": "false",
                        "policy_disabled": "false",
                        "process_blocked": "true",
                        "quarantine_file": "false",
                        "quarantine_machine": "false",
                        "registry_operation_blocked": "false",
                        "rooting": "false",
                        "sensor_only": "false",
                        "suspend_parent": "false",
                        "suspend_process": "false"
                    },
                    "rule_instance_id": 3,
                    "rule_instance_version": "3",
                    "scenario": "suspicious_activity",
                    "severity": 50,
                    "ttp_tagging_ref": "5",
                    "template_instance_id": "3",
                    "created_time": "2024-01-23T12:33:07Z",
                    "user_ref": "6"
                },
                "2": {
                    "type": "process",
                    "command_line": "C:\\conhost.exe 0xffffffff -ForceV1",
                    "name": "conhost.exe",
                    "binary_ref": "0",
                    "parent_ref": "4",
                    "x_process_graph_id": "pid:7adb:123",
                    "creator_user_ref": "6"
                },
                "3": {
                    "type": "directory",
                    "path": "\\Device"
                },
                "4": {
                    "type": "process",
                    "x_process_graph_id": "pid:xyz:123"
                },
                "5": {
                    "type": "x-ibm-ttp-tagging",
                    "name": "Custom Intelligence",
                    "extensions": {
                        "mitre-attack-ext": {
                            "tactic_id": "CSTA0005",
                            "technique_name": "Indicator of Attack",
                            "technique_id": "CST0004"
                        }
                    }
                },
                "6": {
                    "type": "user-account",
                    "user_id": "S-1-5-18",
                    "display_name": "user1"
                },
                "7": {
                    "type": "x-ibm-finding",
                   "x_logscale_repository": "TestRepository",
                    "x_logscale_event_id": "ATzrtyg4xCKOqQnD9NodpvsY_363_125_1711549348",
                    "x_behavior_refs": [
                        "1"
                    ],
                    "ttp_tagging_refs": [
                        "5"
                    ],
                    "x_behaviors_processed": [
                        "pid:7adb:123:41002"
                    ],
                    "time_observed": "2024-01-23T12:33:15.170Z",
                    "x_last_updated": "2024-03-27T14:22:28.062194Z",
                    "name": "ldt:xyz:123",
                    "src_ip_ref": "10",
                    "src_os_ref": "13",
                    "x_is_email_sent": "false",
                    "x_first_behavior_observed": "2024-01-23T12:33:07Z",
                    "x_last_behavior_observed": "2024-01-23T12:33:07Z",
                    "confidence": 100,
                    "severity": 50,
                    "x_severity_name": "Medium",
                    "x_seconds_to_resolved": "0",
                    "x_seconds_to_triaged": "0",
                    "x_status": "new",
                    "finding_type": "alert"
                },
                "8": {
                    "type": "x-oca-asset",
                    "x_cid": "123",
                    "x_agent_ref": "9",
                    "x_bios_manufacturer": "Xen",
                    "x_bios_version": "4.11.amazon",
                    "device_id": "7adb123",
                    "ip_refs": [
                        "10",
                        "11"
                    ],
                    "x_first_seen": "2023-05-16T05:10:55Z",
                    "x_device_groups": [
                        "97350feebe4541e8a615c0d3f18acdf3",
                        "bb1e1190b46348e69e10785030e8b23d"
                    ],
                    "hostname": "host",
                    "x_instance_id": "i-123",
                    "x_last_seen": "2024-01-23T12:33:10Z",
                    "mac_refs": [
                        "12"
                    ],
                    "x_last_modified": "2024-01-23T12:33:13Z",
                    "os_ref": "13",
                    "x_host_type_number": "3",
                    "host_type": "Server",
                    "x_service_provider": "AWS_EC2_V2",
                    "x_service_account_id": "98765",
                    "x_status": "normal",
                    "x_system_manufacturer": "Xen",
                    "x_system_product_name": "HVM domU"
                },
                "9": {
                    "type": "x-crowdstrike-edr-agent",
                    "load_flags": "1",
                    "local_time": "2024-01-23T12:32:59.287Z",
                    "version": "7.05.17706.0",
                    "config_id_base": "65994763",
                    "config_id_build": "17706",
                    "config_id_platform": "3"
                },
                "10": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "11": {
                    "type": "ipv4-addr",
                    "value": "2.2.2.2",
                    "resolves_to_refs": [
                        "12"
                    ]
                },
                "12": {
                    "type": "mac-addr",
                    "value": "01:01:01:01:01:01"
                },
                "13": {
                    "type": "software",
                    "x_major_version": "10",
                    "x_minor_version": "0",
                    "version": "Windows Server 2022",
                    "x_id": "0",
                    "name": "Windows"
                }
            },
            "last_observed": "2024-03-27T14:22:28.062Z",
            "first_observed": "2024-01-23T12:33:15.170Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```
#### Multiple Observation
```shell
translate crowdstrike_logscale query {} 
"([x-ibm-ttp-tagging:extensions.'mitre-attack-ext'.technique_name = 'Indicator of Attack' OR ipv4-addr:value = '4.4.4.4'] AND [x-oca-asset:x_instance_id = 'i-0123' AND x-ibm-finding:severity > 30 AND file:hashes.MD5 = 'e7a6babc90f4'])START t'2023-12-19T16:43:26.000Z' STOP t'2023-12-24T05:22:26.003Z'"
  
```
#### STIX Multiple observation - Output
```json
{
    "queries": [
        {
            "source": "crowdstrikeedr",
            "queryString": "((device.local_ip = \"4.4.4.4\" or device.external_ip = \"4.4.4.4\") or @rawstring = /\"behaviors\"\\s*:\\s*\\[.*\"technique\"\\s*:\\s*\"Indicator\\ of\\ Attack\"/) or ((@rawstring = /\"behaviors\"\\s*:\\s*\\[.*\"parent_details\"\\s*:\\s*\\{.*\"parent_md5\"\\s*:\\s*\"e7a6babc90f4\"/ or @rawstring = /\"behaviors\"\\s*:\\s*\\[.*\"md5\"\\s*:\\s*\"e7a6babc90f4\"/) and (max_severity > 30 and device.instance_id = \"i-0123\")) | tail(10000)",
            "start": 1703004206000,
            "end": 1703395346003
        }
    ]
}
```

### STIX Execute query
```shell
execute
crowdstrike_logscale
crowdstrike_logscale
"{\"type\":\"identity\",\"id\":\"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\",\"name\":\"crowdstrike_logscale\",\"identity_class\":\"system\",\"created\":\"2023-12-24T13:22:50.336Z\",\"modified\":\"2022-12-24T13:22:50.336Z\"}"
"{\"host\":\"xyz\",\"repository\":\"TestRepository\"}"
"{\"auth\":{\"api_token\":  \"123\"}}" 
"[ipv4-addr:value = '3.4.5.6' AND software:version = 'Windows Server 2022' OR x-oca-asset:host_type = 'Server' OR x-crowdstrike-detection-behavior:control_graph_id IN ('ctg:654','ctg:123')] START t'2024-04-01T00:00:00.000Z' STOP t'2024-04-03T11:00:00.000Z'"
```

#### STIX Execute query - Output
```json
{
    "type": "bundle",
    "id": "bundle--44b07b95-fd6f-43b3-86a6-b98e8b9c1e01",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "crowdstrike_logscale",
            "identity_class": "system",
            "created": "2023-12-24T13:22:50.336Z",
            "modified": "2023-12-24T13:22:50.336Z"
        },
        {
            "id": "observed-data--5f3a0294-527a-4a68-adee-a7d93799a801",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2024-04-03T14:11:53.817Z",
            "modified": "2024-04-03T14:11:53.817Z",
            "objects": {
                "0": {
                    "type": "file",
                    "x_extension": "exe",
                    "name": "conhost.exe",
                    "x_path": "\\Device\\conhost.exe",
                    "parent_directory_ref": "3",
                    "hashes": {
                        "MD5": "1010101010101101010100101101010",
                        "SHA-256": "1111111111111111111111111111111111111111111111111111111111111111"
                    }
                },
                "1": {
                    "type": "x-crowdstrike-detection-behavior",
                    "behavior_id": "41002",
                    "confidence": 100,
                    "control_graph_id": "ctg:123",
                    "description": "A process triggered a medium severity custom rule.",
                    "display_name": "CustomIOAWinMedium",
                    "process_ref": "2",
                    "objective": "Falcon Detection Method",
                    "pattern_disposition": 10240,
                    "pattern_disposition_details": {
                        "blocking_unsupported_or_disabled": "false",
                        "bootup_safeguard_enabled": "false",
                        "critical_process_disabled": "true",
                        "detect": "false",
                        "fs_operation_blocked": "false",
                        "handle_operation_downgraded": "false",
                        "inddet_mask": "false",
                        "indicator": "false",
                        "kill_action_failed": "false",
                        "kill_parent": "false",
                        "kill_process": "false",
                        "kill_subprocess": "false",
                        "operation_blocked": "false",
                        "policy_disabled": "false",
                        "process_blocked": "true",
                        "quarantine_file": "false",
                        "quarantine_machine": "false",
                        "registry_operation_blocked": "false",
                        "rooting": "false",
                        "sensor_only": "false",
                        "suspend_parent": "false",
                        "suspend_process": "false"
                    },
                    "rule_instance_id": 3,
                    "rule_instance_version": "3",
                    "scenario": "suspicious_activity",
                    "severity": 50,
                    "ttp_tagging_ref": "6",
                    "template_instance_id": "3",
                    "created_time": "2024-01-25T07:06:28Z",
                    "user_ref": "7"
                },
                "2": {
                    "type": "process",
                    "command_line": "C:\\Windows\\system32\\conhost.exe 0xffffffff -ForceV1",
                    "name": "conhost.exe",
                    "binary_ref": "0",
                    "parent_ref": "4",
                    "x_process_graph_id": "pid:7adb:232202950915",
                    "creator_user_ref": "7"
                },
                "3": {
                    "type": "directory",
                    "path": "\\Device\\HarddiskVolume1\\Windows\\System32"
                },
                "4": {
                    "type": "process",
                    "command_line": "\"C:\\Windows\\System32\\cmd.exe\"  /c \"\"C:\\Program Files\\Amazon\\EC2Launch\\EC2Launch.exe\" wallpaper --path=\"C:\\ProgramData\\Amazon\\EC2Launch\\wallpaper\\Ec2Wallpaper.jpg\" --attributes=\"hostName,instanceId,privateIpAddress,publicIpAddress,instanceSize,availabilityZone,architecture,memory,network\" \"",
                    "binary_ref": "5",
                    "x_process_graph_id": "pid:7adb:232200947972"
                },
                "5": {
                    "type": "file",
                    "hashes": {
                        "MD5": "111111111111111111111111111111111111",
                        "SHA-256": "1212121212122121212121212121212121212121212212121121211212"
                    }
                },
                "6": {
                    "type": "x-ibm-ttp-tagging",
                    "name": "Custom Intelligence",
                    "extensions": {
                        "mitre-attack-ext": {
                            "tactic_id": "CSTA0005",
                            "technique_name": "Indicator of Attack",
                            "technique_id": "CST0004"
                        }
                    }
                },
                "7": {
                    "type": "user-account",
                    "user_id": "S-1-5-21",
                    "display_name": "test user"
                },
                "8": {
                    "type": "x-ibm-finding",
                   "x_logscale_repository": "TestRepository",
                    "x_logscale_event_id": "x456",
                    "x_behavior_refs": [
                        "1"
                    ],
                    "ttp_tagging_refs": [
                        "6"
                    ],
                    "x_behaviors_processed": [
                        "pid:7adb:232202950915:41002"
                    ],
                    "time_observed": "2024-01-25T07:06:36.831Z",
                    "x_last_updated": "2024-04-03T10:40:49.669334Z",
                    "name": "ldt:123",
                    "src_ip_ref": "11",
                    "src_os_ref": "14",
                    "x_is_email_sent": "false",
                    "x_first_behavior_observed": "2024-01-25T07:06:28Z",
                    "x_last_behavior_observed": "2024-01-25T07:06:28Z",
                    "confidence": 100,
                    "severity": 50,
                    "x_severity_name": "Medium",
                    "x_seconds_to_resolved": "0",
                    "x_seconds_to_triaged": "0",
                    "x_status": "new",
                    "finding_type": "alert"
                },
                "9": {
                    "type": "x-oca-asset",
                    "x_cid": "id123",
                    "x_agent_ref": "10",
                    "x_bios_manufacturer": "Xen",
                    "x_bios_version": "4.2.amazon",
                    "device_id": "7adb",
                    "ip_refs": [
                        "11",
                        "12"
                    ],
                    "x_first_seen": "2023-05-16T05:10:55Z",
                    "x_device_groups": [
                        "97350feebe4541e8a615c0d3f18acdf3",
                        "bb1e1190b46348e69e10785030e8b23d"
                    ],
                    "hostname": "host",
                    "x_instance_id": "i-123",
                    "x_last_seen": "2024-01-25T06:51:54Z",
                    "mac_refs": [
                        "13"
                    ],
                    "x_last_modified": "2024-01-25T07:06:13Z",
                    "os_ref": "14",
                    "x_host_type_number": "3",
                    "host_type": "Server",
                    "x_service_provider": "AWS_EC2_V2",
                    "x_service_account_id": "978657",
                    "x_status": "normal",
                    "x_system_manufacturer": "Xen",
                    "x_system_product_name": "HVM domU"
                },
                "10": {
                    "type": "x-crowdstrike-edr-agent",
                    "load_flags": "1",
                    "local_time": "2024-01-25T06:51:42.661Z",
                    "version": "7.05.17706.0",
                    "config_id_base": "65994763",
                    "config_id_build": "17706",
                    "config_id_platform": "3"
                },
                "11": {
                    "type": "ipv4-addr",
                    "value": "5.6.7.8"
                },
                "12": {
                    "type": "ipv4-addr",
                    "value": "2.3.4.5",
                    "resolves_to_refs": [
                        "13"
                    ]
                },
                "13": {
                    "type": "mac-addr",
                    "value": "10:10:10:10:10:10"
                },
                "14": {
                    "type": "software",
                    "x_major_version": "10",
                    "x_minor_version": "0",
                    "version": "Windows Server 2022",
                    "x_id": "0",
                    "name": "Windows"
                }
            },
            "last_observed": "2024-04-03T10:40:49.669Z",
            "first_observed": "2024-01-25T07:06:36.831Z",
            "number_observed": 1
        }],
    "spec_version": "2.0"
}
```
### Type of Attributes

   | Type                      | Description                     | Example |
   |---------------------------|---------------------------------|-----|
   | List of dictionary fields | A list containing one or more dictionaries  | "behaviors": [{"alleged_filetype": "exe"}, {"alleged_filetype": "txt"}] |
   | List of values fields/Array fields | A list containing one or more values | "behaviors_processed": ["123","abc"] |


### Current connector Features
- It has mappings which supports only Crowdstrike Falcon EDR detection logs.
- The Input repository which is provided to the connector should contain only Crowdstrike Falcon EDR detection logs in JSON format.

### Connector Extension
Recommendations to be followed to add new log source to the connector
- The structure of log source data which is ingested into logscale should be of type JSON .
- The JSON data which has been ingested into logscale should be inserted without new line and should be inserted as raw data.
- As Logscale doesn't have unified data schema, separate mapping files(from_stix_map.json, to_stix_map.json) needs to 
  be created for each log source that are newly added to this connector module. 
  Example: {custom}_from_stix_map.json, {custom}_to_stix_map.json
- The mapping of list (list of values/list of dictionary) fields in from_stix_map should be mentioned with [*] suffix. 
  Example, behaviors[*].id. Here 'behaviors' is a list of dictionaries with id as attribute key inside behaviors.

### Recommendations

- For connector usage, it is recommended to maintain logs from single log source per repository in Crowdstrike Logscale. 
  Example Crowdstrike Falcon EDR detection logs could be stored in repository_1 and Okta logs in repository_2.
- Make sure, there is no parsing error during ingestion of logs into Crowdstrike Logscale.

### Limitations
- LIKE,MATCHES, <, >, <=, >= operators are not supported for list of dictionary fields.
- IN, <, >, <=, >= operators are not supported for array fields


### References
- [LogScale Documentation](https://library.humio.com/)
- [Query Langauage Syntax](https://library.humio.com/data-analysis/syntax.html)
- [Search API | Integrations](https://library.humio.com/integrations/api-search.html)
- [Health Check API | Integrations](https://library.humio.com/integrations/api-health-check.html)
- [FalconLogScaleCollector | Falcon LogScaleCollector 1.3.0-1.5.1](https://library.humio.com/falcon-logscale-collector/log-shippers-log-collector.html)
- [Crowdstrike EDR Log injestion through log shippers](https://github.com/CrowdStrike/HEC-Log-Shipper/tree/main)

### Appendix
List of fields that available in schema of Crowdstrike Falcon EDR detection logs

   | Data source Field                                                      | Data Type                | Mapped STIX field                                                                                                |
   |------------------------------------------------------------------------|--------------------------|------------------------------------------------------------------------------------------------------------------|
   | behaviors.alleged_filetype                                             | List of Dictionary field | file:x_extension                                                                                                 |
   | behaviors.behavior_id                                                  | List of Dictionary field | x-ibm-finding:x_behavior_refs.behavior_id                                                                        |
   | behaviors.cmdline                                                      | List of Dictionary field | process:command_line                                                                                             |
   | behaviors.confidence                                                   | List of Dictionary field | x-crowdstrike-detection-behavior:confidence                                                                      |
   | behaviors.control_graph_id                                             | List of Dictionary field | x-crowdstrike-detection-behavior:control_graph_id                                                                |
   | behaviors.description                                                  | List of Dictionary field | x-crowdstrike-detection-behavior:description                                                                     |
   | behaviors.device_id                                                    | List of Dictionary field |                                                                                                                  |
   | behaviors.display_name                                                 | List of Dictionary field | x-crowdstrike-detection-behavior:display_name                                                                    |
   | behaviors.filename                                                     | List of Dictionary field | file:name, process:name, process: binary_ref.name,x-crowdstrike-detection-behavior:process_ref.name              |
   | behaviors.filepath                                                     | List of Dictionary field | file:x_path, file:parent_directory_ref.path, directory:path                                                      |
   | behaviors.ioc_description                                              | List of Dictionary field | x-crowdstrike-detection-behavior:ioc_description                                                                 |
   | behaviors.ioc_source                                                   | List of Dictionary field | x-crowdstrike-detection-behavior:ioc_source                                                                      |
   | behaviors.ioc_type                                                     | List of Dictionary field | x-crowdstrike-detection-behavior:ioc_type                                                                        |
   | behaviors.ioc_value                                                    | List of Dictionary field | x-crowdstrike-detection-behavior:ioc_value                                                                       |
   | behaviors.md5                                                          | List of Dictionary field | process: binary_ref.hashes.MD5 , file:hashes.MD5                                                                 |
   | behaviors.objective                                                    | List of Dictionary field | x-crowdstrike-detection-behavior:objective                                                                       |
   | behaviors.parent_details.parent_cmdline                                | List of Dictionary field | process: parent_ref.command_line                                                                                 |
   | behaviors.parent_details.parent_md5                                    | List of Dictionary field | file:hashes.MD5                                                                                                  |
   | behaviors.parent_details.parent_process_graph_id                       | List of Dictionary field | process:parent_ref.x_process_graph_id                                                                            |
   | behaviors.parent_details.parent_sha256                                 | List of Dictionary field | file:hashes.'SHA-256'                                                                                            |
   | behaviors.pattern_disposition                                          | List of Dictionary field | x-crowdstrike-detection-behavior:pattern_disposition                                                             |
   | behaviors.pattern_disposition_details.blocking_unsupported_or_disabled | List of Dictionary field |                                                                                                                  |
   | behaviors.pattern_disposition_details.bootup_safeguard_enabled         | List of Dictionary field |                                                                                                                  |
   | behaviors.pattern_disposition_details.critical_process_disabled        | List of Dictionary field |                                                                                                                  |
   | behaviors.pattern_disposition_details.detect                           | List of Dictionary field |                                                                                                                  |
   | behaviors.pattern_disposition_details.fs_operation_blocked             | List of Dictionary field |                                                                                                                  |
   | behaviors.pattern_disposition_details.handle_operation_downgraded      | List of Dictionary field |                                                                                                                  |
   | behaviors.pattern_disposition_details.inddet_mask                      | List of Dictionary field |                                                                                                                  |
   | behaviors.pattern_disposition_details.indicator                        | List of Dictionary field |                                                                                                                  |
   | behaviors.pattern_disposition_details.kill_action_failed               | List of Dictionary field |                                                                                                                  |
   | behaviors.pattern_disposition_details.kill_parent                      | List of Dictionary field |                                                                                                                  |
   | behaviors.pattern_disposition_details.kill_process                     | List of Dictionary field |                                                                                                                  |
   | behaviors.pattern_disposition_details.kill_subprocess                  | List of Dictionary field |                                                                                                                  |
   | behaviors.pattern_disposition_details.operation_blocked                | List of Dictionary field |                                                                                                                  |
   | behaviors.pattern_disposition_details.policy_disabled                  | List of Dictionary field |                                                                                                                  |
   | behaviors.pattern_disposition_details.process_blocked                  | List of Dictionary field |                                                                                                                  |
   | behaviors.pattern_disposition_details.quarantine_file                  | List of Dictionary field |                                                                                                                  |
   | behaviors.pattern_disposition_details.quarantine_machine               | List of Dictionary field |                                                                                                                  |
   | behaviors.pattern_disposition_details.registry_operation_blocked       | List of Dictionary field |                                                                                                                  |
   | behaviors.pattern_disposition_details.rooting                          | List of Dictionary field |                                                                                                                  |
   | behaviors.pattern_disposition_details.sensor_only                      | List of Dictionary field |                                                                                                                  |
   | behaviors.pattern_disposition_details.suspend_parent                   | List of Dictionary field |                                                                                                                  |
   | behaviors.pattern_disposition_details.suspend_process                  | List of Dictionary field |                                                                                                                  |
   | behaviors.rule_instance_id                                             | List of Dictionary field | x-crowdstrike-detection-behavior:rule_instance_id                                                                |
   | behaviors.rule_instance_version                                        | List of Dictionary field | x-crowdstrike-detection-behavior:rule_instance_version                                                           |
   | behaviors.scenario                                                     | List of Dictionary field | x-crowdstrike-detection-behavior:scenario                                                                        |
   | behaviors.severity                                                     | List of Dictionary field | x-crowdstrike-detection-behavior:severity                                                                        |
   | behaviors.sha256                                                       | List of Dictionary field | process:binary_ref.hashes.'SHA-256', file:hashes.'SHA-256'                                                       |
   | behaviors.tactic                                                       | List of Dictionary field | x-ibm-finding:ttp_tagging_refs.name,x-crowdstrike-detection-behavior:ttp_tagging_ref.name,x-ibm-ttp-tagging:name |
   | behaviors.tactic_id                                                    | List of Dictionary field | x-ibm-ttp-tagging:extensions.'mitre-attack-ext'.tactic_id                                                        |
   | behaviors.technique                                                    | List of Dictionary field | x-ibm-ttp-tagging:extensions.'mitre-attack-ext'.technique_name                                                   |
   | behaviors.technique_id                                                 | List of Dictionary field | x-ibm-ttp-tagging:extensions.'mitre-attack-ext'.technique_id                                                     |
   | behaviors.template_instance_id                                         | List of Dictionary field | x-crowdstrike-detection-behavior:template_instance_id                                                            |
   | behaviors.timestamp                                                    | List of Dictionary field | x-crowdstrike-detection-behavior:created_time                                                                    |
   | behaviors.triggering_process_graph_id                                  | List of Dictionary field | process:x_process_graph_id                                                                                       |
   | behaviors.user_id                                                      | List of Dictionary field | process:creator_user_ref.user_id, user-account:user_id,x-crowdstrike-detection-behavior:user_ref.user_id         |
   | behaviors.user_name                                                    | List of Dictionary field | user-account:display_name                                                                                        |
   | behaviors_processed                                                    | List field               | x-ibm-finding:x_behaviors_processed                                                                              |
   | cid                                                                    | Dictionary field         | x-oca-asset:x_cid                                                                                                |                                                                                       |
   | created_timestamp                                                      | Dictionary field         | x-ibm-finding:time_observed                                                                                      |  
   | date_updated                                                           | Dictionary field         | x-ibm-finding:x_last_updated                                                                                     | 
   | detection_id                                                           | Dictionary field         | x-ibm-finding:name                                                                                               |
   | device.agent_load_flags                                                | Dictionary field         |                                                                                                                  |
   | device.agent_local_time                                                | Dictionary field         | x-crowdstrike-edr-agent:local_time                                                                               |                                                                        
   | device.agent_version                                                   | Dictionary field         | x-oca-asset:x_agent_ref.version,x-crowdstrike-edr-agent:version                                                  |                                               
   | device.bios_manufacturer                                               | Dictionary field         | x-oca-asset:x_bios_manufacturer                                                                                  |                                              
   | device.bios_version                                                    | Dictionary field         | x-oca-asset:x_bios_version                                                                                       |                                             
   | device.cid                                                             | Dictionary field         | x-oca-asset:x_cid                                                                                                |                                            
   | device.config_id_base                                                  | Dictionary field         | x-crowdstrike-edr-agent:config_id_base                                                                           |                                           
   | device.config_id_build                                                 | Dictionary field         | x-crowdstrike-edr-agent:config_id_build                                                                          |                                          
   | device.config_id_platform                                              | Dictionary field         | x-crowdstrike-edr-agent:config_id_platform                                                                       |                                         
   | device.device_id                                                       | Dictionary field         | x-oca-asset:device_id                                                                                            |                                        
   | device.external_ip                                                     | Dictionary field         | ipv4-addr:value, ipv6-addr:value,x-ibm-finding:src_ip_ref.value                                                  |                                       |
   | device.first_seen                                                      | Dictionary field         | x-oca-asset:x_first_seen                                                                                         |                                        
   | device.groups                                                          | List Field               | x-oca-asset:x_device_groups                                                                                      |                                       
   | device.hostname                                                        | Dictionary field         | x-oca-asset:hostname                                                                                             |                                      
   | device.instance_id                                                     | Dictionary field         | x-oca-asset:x_instance_id                                                                                        |                                                           
   | device.last_login_timestamp                                            | Dictionary field         |                                                                                                                  |
   | device.last_login_user                                                 | Dictionary field         |                                                                                                                  |
   | device.last_seen                                                       | Dictionary field         | x-oca-asset:x_last_seen                                                                                          |                                                           
   | device.local_ip                                                        | Dictionary field         | ipv4-addr:value, ipv6-addr:value                                                                                 |                                                          | 
   | device.mac_address                                                     | Dictionary field         | mac-addr:value                                                                                                   |                                                                       |
   | device.major_version                                                   | Dictionary field         | software:x_major_version                                                                                         |                                                                      |
   | device.minor_version                                                   | Dictionary field         | software:x_minor_version                                                                                         |                                                                     |
   | device.modified_timestamp                                              | Dictionary field         | x-oca-asset:x_last_modified                                                                                      |                                                                    
   | device.os_version                                                      | Dictionary field         | software:version                                                                                                 |                                                                   |
   | device.platform_id                                                     | Dictionary field         | software:x_id                                                                                                    |                                                                  |
   | device.platform_name                                                   | Dictionary field         | software:name,x-oca-asset:os_ref.name,x-ibm-finding:src_os_ref.name                                              |                                    |
   | device.product_type                                                    | Dictionary field         | x-oca-asset:x_host_type_number                                                                                   |                                   
   | device.product_type_desc                                               | Dictionary field         | x-oca-asset:host_type                                                                                            |                                  
   | device.service_provider                                                | Dictionary field         | x-oca-asset:x_service_provider                                                                                   |                                 
   | device.service_provider_account_id                                     | Dictionary field         | x-oca-asset:x_service_account_id                                                                                 |                                
   | device.status                                                          | Dictionary field         | x-oca-asset:x_status                                                                                             |                               
   | device.system_manufacturer                                             | Dictionary field         | x-oca-asset:x_system_manufacturer                                                                                |                              
   | device.system_product_name                                             | Dictionary field         | x-oca-asset:x_system_product_name                                                                                |                             
   | email_sent                                                             | Dictionary field         |                                                                                                                  |
   | first_behavior                                                         | Dictionary field         | x-ibm-finding:x_first_behavior_observed                                                                          |                                                                
   | hostinfo.domain                                                        | Dictionary field         | domain-name:value                                                                                                |                                                               |
   | last_behavior                                                          | Dictionary field         | x-ibm-finding:x_last_behavior_observed                                                                           |                                                              
   | max_confidence                                                         | Dictionary field         | x-ibm-finding:confidence                                                                                         |                                                             
   | max_severity                                                           | Dictionary field         | x-ibm-finding:severity                                                                                           |                                                            
   | max_severity_displayname                                               | Dictionary field         | x-ibm-finding:x_severity_name                                                                                    |                                                           
   | seconds_to_resolved                                                    | Dictionary field         |                                                                                                                  |
   | seconds_to_triaged                                                     | Dictionary field         |                                                                                                                  |
   | show_in_ui                                                             | Dictionary field         |                                                                                                                  |
   | status                                                                 | Dictionary field         | x-ibm-finding:x_status                                                                                           |                                                                                   
   

