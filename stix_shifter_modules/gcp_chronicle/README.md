# Google Cloud Platform (GCP) Chronicle

## Supported STIX Mappings

See the [table of mappings](gcp_chronicle_supported_stix.md) for the STIX objects and operators supported by this connector.

**Table of Contents**

- [GCP Chronicle API Endpoints](#gcp-chronicle-api-endpoints)
- [Pattern expression with STIX attributes](#pattern-expression-with-stix-attributes)
- [Pattern expression with CUSTOM attributes](#pattern-expression-with-custom-attributes)
- [STIX Execute Query](#stix-execute-query)
- [Pattern expression with STIX attributes - Multiple Observation](#stix-multiple-observation)
- [Limitations](#limitations)
- [Observations](#observations)
- [References](#references)

### GCP Chronicle API Endpoints

   | Connector Method | GCP Chronicle API Endpoint  | Method |
   |-----------------|------|   ------|
   | Ping Endpoint   | https://< server >/v2/detect/rules                                                                       | GET  |
   | Query Endpoint  | 1)  https://< server >/v2/detect/rules/<br/> 2) https://< server >/v2/detect/rules/{ruleId}:runRetrohunt | POST |
   | Status Endpoint | https://< server >/v2/detect/rules/{ruleId}/retrohunts/{retrohuntId}                                     | GET|                                                                             
   | Results Endpoint | https://< server >/v2/detect/rules/{ruleId}/detections                                                   | GET  |
   | Delete Endpoint | https://< server >/v2/detect/rules/{ruleId}                                                              | DELETE |

### Format for calling stix-shifter from the command line
```
python main.py `<translator_module>` `<query or result>` `<STIX identity object>` `<data>`
```
### Pattern expression with STIX attributes

### Single Observation

#### STIX Translate query to get the events associated with the process name and the file hash
```shell
translate gcp_chronicle query '{}' "[process:name = 'powershell.exe' AND file:hashes.'SHA-1' = 'ded8fd7f36417f66eb6ada10e0c0d7c0022986e9'] START t'2022-06-05T16:43:26.000Z' STOP t'2022-06-10T16:43:26.003Z'"
```
#### STIX Translate query - output
```json
{
    "queries": [
        {
            "ruleText": "rule cp4s_gcp_udi_rule_1659699862 { meta: author = \"ibm cp4s user\" description = \"Create event rule that should generate detections\" events: ($udm.src.file.sha1 = \"ded8fd7f36417f66eb6ada10e0c0d7c0022986e9\" nocase or $udm.target.file.sha1 = \"ded8fd7f36417f66eb6ada10e0c0d7c0022986e9\" nocase or $udm.src.process.file.sha1 = \"ded8fd7f36417f66eb6ada10e0c0d7c0022986e9\" nocase or $udm.target.process.file.sha1 = \"ded8fd7f36417f66eb6ada10e0c0d7c0022986e9\" nocase or $udm.principal.process.file.sha1 = \"ded8fd7f36417f66eb6ada10e0c0d7c0022986e9\" nocase or $udm.about.file.sha1 = \"ded8fd7f36417f66eb6ada10e0c0d7c0022986e9\" nocase) and ($udm.src.process.file.full_path = /(?s)powershell\\.exe/ nocase or $udm.target.process.file.full_path = /(?s)powershell\\.exe/ nocase or $udm.principal.process.file.full_path = /(?s)powershell\\.exe/ nocase or $udm.target.process.parent_process.file.full_path = /(?s)powershell\\.exe/ nocase or $udm.principal.process.parent_process.file.full_path = /(?s)powershell\\.exe/ nocase) condition: $udm}",
            "startTime": "2022-06-05T16:43:26.000Z",
            "endTime": "2022-06-10T16:43:26.003Z"
        }
    ]
}

```

#### STIX Transmit query 

```shell
transmit
gcp_chronicle
"{\"host\":\"xx.xx.xx\"}"
"{\"auth\":{ \"client_email\": \"xyz.com\",\"private_key\": \"-----BEGIN PRIVATE KEY-----\nxxx\n-----END PRIVATE KEY-----\n\"}}"
query
" { \"ruleText\": \"rule cp4s_gcp_udi_rule_1659699862 { meta: author = \\"ibm cp4s user\\" description = \\"Create event rule that should generate detections\\" events: ($udm.src.file.sha1 = \\"ded8fd7f36417f66eb6ada10e0c0d7c0022986e9\\" nocase or $udm.target.file.sha1 = \\"ded8fd7f36417f66eb6ada10e0c0d7c0022986e9\\" nocase or $udm.src.process.file.sha1 = \\"ded8fd7f36417f66eb6ada10e0c0d7c0022986e9\\" nocase or $udm.target.process.file.sha1 = \\"ded8fd7f36417f66eb6ada10e0c0d7c0022986e9\\" nocase or $udm.principal.process.file.sha1 = \\"ded8fd7f36417f66eb6ada10e0c0d7c0022986e9\\" nocase or $udm.about.file.sha1 = \\"ded8fd7f36417f66eb6ada10e0c0d7c0022986e9\\" nocase) and ($udm.src.process.file.full_path = /(?s)powershell\\.exe/ nocase or $udm.target.process.file.full_path = /(?s)powershell\\.exe/ nocase or $udm.principal.process.file.full_path = /(?s)powershell\\.exe/ nocase or $udm.target.process.parent_process.file.full_path = /(?s)powershell\\.exe/ nocase or $udm.principal.process.parent_process.file.full_path = /(?s)powershell\\.exe/ nocase) condition: $udm}\", \"startTime\": \"2022-06-05T16:43:26.000Z\", \"endTime\": \"2022-06-10T16:43:26.003Z\" }"
```

#### STIX Transmit query - output
```json
{
    "success": true,
    "search_id": "oh_cda1ea4f-87d8-4f21-b80c-9eb3c5e8bf6d:ru_2fec7add-f727-41e1-a839-9de344d2a98d"
}
```
#### STIX Transmit status 

```shell
transmit
gcp_chronicle
"{\"host\":\"xx.xx.xx\"}"
"{\"auth\":{ \"client_email\": \"xyz.com\",\"private_key\": \"-----BEGIN PRIVATE KEY-----\nxxx\n-----END PRIVATE KEY-----\n\"}}"
status
"oh_cda1ea4f-87d8-4f21-b80c-9eb3c5e8bf6d:ru_2fec7add-f727-41e1-a839-9de344d2a98d"
```

#### STIX Transmit status - output
```json
{
    "success": true,
    "status": "COMPLETED",
    "progress": 100
}
```
#### STIX Transmit results 

```shell
transmit
gcp_chronicle
"{\"host\":\"xx.xx.xx\"}"
"{\"auth\":{ \"client_email\": \"xyz.com\",\"private_key\": \"-----BEGIN PRIVATE KEY-----\nxxx\n-----END PRIVATE KEY-----\n\"}}"
results
"oh_cda1ea4f-87d8-4f21-b80c-9eb3c5e8bf6d:ru_2fec7add-f727-41e1-a839-9de344d2a98d" 0 1
```

#### STIX Transmit results - output
```json
{
    "success": true,
    "data": [
        {
            "event": {
                "metadata": {
                    "productLogId": "4f22ab5dc4be96566ee3c9adb3b77280dc08bfdb",
                    "eventTimestamp": "2022-06-06T11:27:47.531824Z",
                    "eventType": "PROCESS_LAUNCH",
                    "vendorName": "Microsoft Defender ATP",
                    "productName": "AdvancedHunting-DeviceProcessEvents",
                    "productEventType": "ProcessCreated",
                    "ingestedTimestamp": "2022-06-06T14:57:54.955806Z"
                },
                "principal": {
                    "hostname": "alert-windows",
                    "user": {
                        "userid": "defenderadm",
                        "windowsSid": "S-1-5-21-2421154212-3139753733-2135342675-1000"
                    },
                    "process": {
                        "pid": "6772",
                        "file": {
                            "sha256": "bc866cfcdda37e24dc2634dc282c7a0e6f55209da17a8fa105b07414c0e7c527",
                            "md5": "911d039e71583a07320b32bde22f8e22",
                            "sha1": "ded8fd7f36417f66eb6ada10e0c0d7c0022986e9",
                            "size": "278528",
                            "fullPath": "c:\\windows\\system32\\cmd.exe"
                        },
                        "commandLine": "\"cmd.exe\" ",
                        "parentProcess": {
                            "pid": "6720",
                            "file": {
                                "fullPath": "svchost.exe"
                            }
                        }
                    },
                    "administrativeDomain": "alert-windows"
                },
                "target": {
                    "process": {
                        "pid": "6856",
                        "file": {
                            "sha256": "de96a6e69944335375dc1ac238336066889d9ffc7d73628ef4fe1b1b160ab32c",
                            "md5": "7353f60b1739074eb17c5f4dddefe239",
                            "sha1": "6cbce4a295c163791b60fc23d285e6d84f28ee4c",
                            "size": "448000",
                            "fullPath": "powershell.exe"
                        },
                        "commandLine": "powershell.exe  -ExecutionPolicy Bypass -NoProfile -Command \"Add-Type 'using System; using System.Diagnostics; using System.Diagnostics.Tracing; namespace Sense { [EventData(Name = \\\"Onboarding\\\")]public struct Onboarding{public string Message { get; set; }} public class Trace {public static EventSourceOptions TelemetryCriticalOption = new EventSourceOptions(){Level = EventLevel.Informational, Keywords = (EventKeywords)0x0000200000000000, Tags = (EventTags)0x0200000}; public void WriteOnboardingMessage(string message){es.Write(\\\"OnboardingScript\\\", TelemetryCriticalOption, new Onboarding {Message = message});} private static readonly string[] telemetryTraits = { \\\"ETW_GROUP\\\", \\\"{5ECB0BAC-B930-47F5-A8A4-E8253529EDB7}\\\" }; private EventSource es = new EventSource(\\\"Microsoft.Windows.Sense.Client.Management\\\",EventSourceSettings.EtwSelfDescribingEventFormat,telemetryTraits);}}'; $logger = New-Object -TypeName Sense.Trace; $logger.WriteOnboardingMessage('Successfully onboarded machine to Microsoft Defender for Endpoint')\" "
                    },
                    "file": {
                        "fullPath": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"
                    }
                },
                "observer": {
                    "cloud": {
                        "project": {
                            "id": "b73e5ba8-34d5-495a-9901-06bdb84cf13e"
                        }
                    }
                },
                "about": [
                    {
                        "labels": [
                            {
                                "key": "ReportId",
                                "value": "14720"
                            },
                            {
                                "key": "InitiatingProcessTokenElevation",
                                "value": "TokenElevationTypeFull"
                            },
                            {
                                "key": "InitiatingProcessIntegrityLevel",
                                "value": "High"
                            }
                        ]
                    }
                ],
                "securityResult": [{
                    "category": "alert",
			        "summary": "ProcessCreated"
                }]
            },
            "detection": {
                "ruleName": "cp4s_gcp_udi_rule_1659699862",
                "urlBackToProduct": "https://hcllab.backstory.chronicle.security/ruleDetections?ruleId=ru_568c1be7-476b-494d-a1b3-b6d6b06e8988&selectedList=RuleDetectionsViewTimeline&selectedParentDetectionId=de_e38651d7-ea4e-7b39-c36e-0e42d590b981&selectedTimestamp=2022-06-06T11:27:47.531824Z&versionTimestamp=2022-08-05T12:53:43.162079Z",
                "ruleId": "ru_568c1be7-476b-494d-a1b3-b6d6b06e8988",
                "ruleVersion": "ru_568c1be7-476b-494d-a1b3-b6d6b06e8988@v_1659704023_162079000",
                "alertState": "NOT_ALERTING",
                "ruleType": "SINGLE_EVENT",
                "ruleLabels": [
                    {
                        "key": "author",
                        "value": "ibm cp4s user"
                    },
                    {
                        "key": "description",
                        "value": "Create event rule that should generate detections"
                    }
                ]
            }
        }
    ],
   "metadata": {
      "result_count": 1,
      "next_page_token": "abc"
   }
}
```


#### STIX Translate results

```json
{
    "type": "bundle",
    "id": "bundle--15d030d9-7696-476e-815a-fe381e369958",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "gcp",
            "identity_class": "events",
            "created": "2022-07-22T13:22:50.336Z",
            "modified": "2022-07-22T13:22:50.336Z"
        },
        {
            "id": "observed-data--6923575f-57fe-40cf-bb47-94b9b9baa804",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-07-22T13:22:50.336Z",
            "modified": "2022-07-22T13:22:50.336Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "code": "4f22ab5dc4be96566ee3c9adb3b77280dc08bfdb",
                    "created": "2022-06-06T11:27:47.531824Z",
                    "action": "PROCESS_LAUNCH",
                    "provider": "Microsoft Defender ATP",
                    "agent": "AdvancedHunting-DeviceProcessEvents",
                    "outcome": "ProcessCreated",
                    "host_ref": "1",
                    "user_ref": "2",
                    "file_ref": "4",
                    "process_ref": "3",
                    "parent_process_ref": "6",
                    "cross_process_target_ref": "8"
                },
                "1": {
                    "type": "x-oca-asset",
                    "hostname": "alert-windows"
                },
                "2": {
                    "type": "user-account",
                    "user_id": "defenderadm",
                    "extensions": {
                        "windows-account-ext": {
                            "sid": "S-1-5-21-2421154212-3139753733-2135342675-1000"
                        }
                    }
                },
                "3": {
                    "type": "process",
                    "creator_user_ref": "2",
                    "pid": 6772,
                    "binary_ref": "4",
                    "name": "cmd.exe",
                    "command_line": "\"cmd.exe\" ",
                    "parent_ref": "6"
                },
                "4": {
                    "type": "file",
                    "hashes": {
                        "SHA-256": "bc866cfcdda37e24dc2634dc282c7a0e6f55209da17a8fa105b07414c0e7c527",
                        "MD5": "911d039e71583a07320b32bde22f8e22",
                        "SHA-1": "ded8fd7f36417f66eb6ada10e0c0d7c0022986e9"
                    },
                    "size": 278528,
                    "name": "cmd.exe",
                    "parent_directory_ref": "5"
                },
                "5": {
                    "type": "directory",
                    "path": "c:\\windows\\system32"
                },
                "6": {
                    "type": "process",
                    "pid": 6720,
                    "name": "svchost.exe",
                    "binary_ref": "7"
                },
                "7": {
                    "type": "file",
                    "name": "svchost.exe"
                },
                "8": {
                    "type": "process",
                    "pid": 6856,
                    "binary_ref": "9",
                    "name": "powershell.exe",
                    "command_line": "powershell.exe  -ExecutionPolicy Bypass -NoProfile -Command \"Add-Type 'using System; using System.Diagnostics; using System.Diagnostics.Tracing; namespace Sense { [EventData(Name = \\\"Onboarding\\\")]public struct Onboarding{public string Message { get; set; }} public class Trace {public static EventSourceOptions TelemetryCriticalOption = new EventSourceOptions(){Level = EventLevel.Informational, Keywords = (EventKeywords)0x0000200000000000, Tags = (EventTags)0x0200000}; public void WriteOnboardingMessage(string message){es.Write(\\\"OnboardingScript\\\", TelemetryCriticalOption, new Onboarding {Message = message});} private static readonly string[] telemetryTraits = { \\\"ETW_GROUP\\\", \\\"{5ECB0BAC-B930-47F5-A8A4-E8253529EDB7}\\\" }; private EventSource es = new EventSource(\\\"Microsoft.Windows.Sense.Client.Management\\\",EventSourceSettings.EtwSelfDescribingEventFormat,telemetryTraits);}}'; $logger = New-Object -TypeName Sense.Trace; $logger.WriteOnboardingMessage('Successfully onboarded machine to Microsoft Defender for Endpoint')\" "
                },
                "9": {
                    "type": "file",
                    "hashes": {
                        "SHA-256": "de96a6e69944335375dc1ac238336066889d9ffc7d73628ef4fe1b1b160ab32c",
                        "MD5": "7353f60b1739074eb17c5f4dddefe239",
                        "SHA-1": "6cbce4a295c163791b60fc23d285e6d84f28ee4c"
                    },
                    "size": 448000,
                    "name": "powershell.exe"
                },
                "10": {
                    "type": "file",
                    "name": "powershell.exe",
                    "parent_directory_ref": "11"
                },
                "11": {
                    "type": "directory",
                    "path": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0"
                },
                "12": {
                    "type": "x-ibm-finding",
                    "name": "ProcessCreated",
                    "finding_type": "alert"
                }
            },
            "first_observed": "2022-06-06T11:27:47.531824Z",
            "last_observed": "2022-06-06T11:27:47.531824Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```


### Pattern expression with CUSTOM attributes 
### Single Observation

#### STIX Translate query to find the threats in an email transaction
```shell
translate gcp_chronicle query '{}' "[x-ibm-finding:finding_type = 'threat' AND x-oca-event:action = 'EMAIL_TRANSACTION'] START t'2022-06-21T16:43:26.000Z' STOP t'2022-06-24T16:43:26.003Z'"
```

#### STIX Translate query - output

```json
{
    "queries": [
        {
            "ruleText": "rule cp4s_gcp_udi_rule_1659715234 { meta: author = \"ibm cp4s user\" description = \"Create event rule that should generate detections\" events: $udm.metadata.event_type = \"EMAIL_TRANSACTION\" and (any $udm.security_result.category = \"SOFTWARE_MALICIOUS\" or any $udm.security_result.category = \"SOFTWARE_PUA\" or any $udm.security_result.category = \"NETWORK_MALICIOUS\" or any $udm.security_result.category = \"MAIL_SPAM\" or any $udm.security_result.category = \"MAIL_PHISHING\" or any $udm.security_result.category = \"MAIL_SPOOFING\") condition: $udm}",
            "startTime": "2022-06-21T16:43:26.000Z",
            "endTime": "2022-06-24T16:43:26.003Z"
        }
    ]
}

```


#### STIX Transmit query

```shell
transmit
gcp_chronicle
"{\"host\":\"xx.xx.xx\"}"
"{\"auth\":{ \"client_email\": \"xyz.com\",\"private_key\": \"-----BEGIN PRIVATE KEY-----\nxxx\n-----END PRIVATE KEY-----\n\"}}"
query
"{ \"ruleText\": \"rule cp4s_gcp_udi_rule_1659715234 { meta: author = \\"ibm cp4s user\\" description = \\"Create event rule that should generate detections\\" events: $udm.metadata.event_type = \\"EMAIL_TRANSACTION\\" and (any $udm.security_result.category = \\"SOFTWARE_MALICIOUS\\" or any $udm.security_result.category = \\"SOFTWARE_PUA\\" or any $udm.security_result.category = \\"NETWORK_MALICIOUS\\" or any $udm.security_result.category = \\"MAIL_SPAM\\" or any $udm.security_result.category = \\"MAIL_PHISHING\\" or any $udm.security_result.category = \\"MAIL_SPOOFING\\") condition: $udm}\", \"startTime\": \"2022-06-21T16:43:26.000Z\", \"endTime\": \"2022-06-24T16:43:26.003Z\" }"
```

#### STIX Transmit query - output

```json
{
    "success": true,
    "search_id": "oh_7111ae97-b1bc-4393-a305-ec88dd13fbb2:ru_d9341b46-4cea-4cbc-9890-5dabe1d2b62f"
}
```
#### STIX Transmit status 

```shell
transmit
gcp_chronicle
"{\"host\":\"xx.xx.xx\"}"
"{\"auth\":{ \"client_email\": \"xyz.com\",\"private_key\": \"-----BEGIN PRIVATE KEY-----\nxxx\n-----END PRIVATE KEY-----\n\"}}"
status
"oh_7111ae97-b1bc-4393-a305-ec88dd13fbb2:ru_d9341b46-4cea-4cbc-9890-5dabe1d2b62f"
```

#### STIX Transmit status - output
```json
{
    "success": true,
    "status": "COMPLETED",
    "progress": 100
}

```
#### STIX Transmit results 

```shell
transmit
gcp_chronicle
"{\"host\":\"xx.xx.xx\"}"
"{\"auth\":{ \"client_email\": \"xyz.com\",\"private_key\": \"-----BEGIN PRIVATE KEY-----\nxxx\n-----END PRIVATE KEY-----\n\"}}"
results
"oh_7111ae97-b1bc-4393-a305-ec88dd13fbb2:ru_d9341b46-4cea-4cbc-9890-5dabe1d2b62f" 0 1
```

#### STIX Transmit results - output
```json
{
    "success": true,
    "data": [
        {
            "event": {
                "metadata": {
                    "productLogId": "MYhRuvkA0N4NtUSOmiBIumilYcKRlBcy",
                    "eventTimestamp": "2022-06-22T11:19:20Z",
                    "eventType": "EMAIL_TRANSACTION",
                    "vendorName": "PROOFPOINT",
                    "productName": "TAP",
                    "productEventType": "messagesDelivered",
                    "ingestedTimestamp": "2022-06-22T11:43:29.036379Z"
                },
                "additional": {
                    "phishScore": 0,
                    "spamScore": 0,
                    "headerFrom": "test user1 <user1@iscgalaxy.com>"
                },
                "principal": {
                    "user": {
                        "emailAddresses": [
                            "user1@iscgalaxy.com"
                        ]
                    },
                    "ip": [
                        "1.1.1.1"
                    ]
                },
                "target": {
                    "user": {
                        "emailAddresses": [
                            "user2@iscgalaxy.com"
                        ]
                    }
                },
                "intermediary": [
                    {
                        "user": {
                            "emailAddresses": [
                                "testuser21@iscgalaxy.com",
                                "user2@iscgalaxy.com"
                            ]
                        }
                    }
                ],
                "about": [
                    {
                        "file": {
                            "sha256": "b025e6114db79f3a891740c45ed264231ec77b07ab9e7ff9156b6d73eb35861e",
                            "md5": "ff357be90b834ed71da60df190124592",
                            "fullPath": "text.txt",
                            "mimeType": "text/plain"
                        }
                    }
                ],
                "securityResult": [
                    {
                        "about": {
                            "url": "https://testurl.com"
                        },
                        "category": "threat",
                        "categoryDetails": [
                            "malware"
                        ],
                        "threatName": "url",
                        "action": [
                            "ALLOW_WITH_MODIFICATION"
                        ],
                        "urlBackToProduct": "https://threatinsight.proofpoint.com/a7929edb-9295-4c75-8767-8a8ddf8a5807/threat/email/d00309e12e797021511111456056ff434c2b85c908d72b8c0dc138259182b9a0",
                        "threatId": "d00309e12e797021511111456056ff434c2b85c908d72b8c0dc138259182b9a0",
                        "threatStatus": "ACTIVE",
                        "detectionFields": [
                            {
                                "key": "completelyRewritten",
                                "value": "True"
                            }
                        ]
                    }
                ],
                "network": {
                    "email": {
                        "from": "010001818b22f94b-c1c1b98b-16f5-40d0-a911-a7f562a5d1d1-000000@amazonses.com",
                        "to": [
                            "user2@iscgalaxy.com"
                        ],
                        "mailId": "010001818b22f94b-c1c1b98b-16f5-40d0-a911-a7f562a5d1d1-000000@email.amazonses.com",
                        "subject": [
                            "https://testurl.com"
                        ],
                        "isMultipart": false
                    }
                }
            },
            "detection": {
                "ruleName": "cp4s_gcp_udi_rule_1659715234",
                "urlBackToProduct": "https://hcllab.backstory.chronicle.security/ruleDetections?ruleId=ru_d9341b46-4cea-4cbc-9890-5dabe1d2b62f&selectedList=RuleDetectionsViewTimeline&selectedParentDetectionId=de_1022f4e7-70ea-db83-ac0f-ff550fad631d&selectedTimestamp=2022-06-22T11:19:20Z&versionTimestamp=2022-08-05T16:03:39.150767Z",
                "ruleId": "ru_d9341b46-4cea-4cbc-9890-5dabe1d2b62f",
                "ruleVersion": "ru_d9341b46-4cea-4cbc-9890-5dabe1d2b62f@v_1659715419_150767000",
                "alertState": "NOT_ALERTING",
                "ruleType": "SINGLE_EVENT",
                "ruleLabels": [
                    {
                        "key": "author",
                        "value": "ibm cp4s user"
                    },
                    {
                        "key": "description",
                        "value": "Create event rule that should generate detections"
                    }
                ]
            }
        }
    ],
   "metadata": {
	"result_count": 1,
	"next_page_token": "abc"
   }
}
```


#### STIX Translate results

```json
{
    "type": "bundle",
    "id": "bundle--d01a64a1-c2b1-4477-9e5f-7f47a031419e",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "gcp",
            "identity_class": "events",
            "created": "2022-08-05T13:22:50.336Z",
            "modified": "2022-08-05T13:22:50.336Z"
        },
        {
            "id": "observed-data--7425dc2d-a247-47c8-b4df-c5c508fe6ccd",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-08-05T13:22:50.336Z",
            "modified": "2022-08-05T13:22:50.336Z",
            "objects": {
                   "0": {
                    "type": "x-oca-event",
                    "code": "MYhRuvkA0N4NtUSOmiBIumilYcKRlBcy",
                    "created": "2022-06-22T11:19:20Z",
                    "action": "EMAIL_TRANSACTION",
                    "provider": "PROOFPOINT",
                    "agent": "TAP",
                    "outcome": "messagesDelivered",
                    "ip_refs": [
                        "2"
                    ],
                    "extensions": {
                        "x-gcp-chronicle-event": {
                            "email_message_ref": "8"
                        }
                    }
                },
                "1": {
                    "type": "email-addr",
                    "value": "user1@iscgalaxy.com"
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "4": {
                    "type": "x-ibm-finding",
                    "src_ip_ref": "2",
                    "extensions": {
                        "x-gcp-chronicle-security-result": {
                            "url_ref": "9",
                            "threat_name": "url",
                            "actions_taken": [
                                "ALLOW_WITH_MODIFICATION"
                            ],
                            "threat_id": "d00309e12e797021511111456056ff434c2b85c908d72b8c0dc138259182b9a0",
                            "threat_status": "ACTIVE"
                        }
                    },
                    "finding_type": "threat"
                },
                "6": {
                    "type": "email-addr",
                    "value": "user2@iscgalaxy.com"
                },
                "7": {
                    "type": "file",
                    "hashes": {
                        "SHA-256": "b025e6114db79f3a891740c45ed264231ec77b07ab9e7ff9156b6d73eb35861e",
                        "MD5": "ff357be90b834ed71da60df190124592"
                    },
                    "name": "text.txt",
                    "extensions": {
                        "x-gcp-chronicle-file": {
                            "mime_type": "text/plain"
                        }
                    }
                },
                "8": {
                    "type": "email-message",
                    "extensions": {
                        "x-gcp-chronicle-email-message": {
                            "file_ref": "7"
                        }
                    },
                    "from_ref": "10",
                    "to_refs": [
                        "11"
                    ],
                    "subject": "https://testurl.com",
                    "is_multipart": false
                },
                "9": {
                    "type": "url",
                    "value": "https://testurl.com"
                },
                "10": {
                    "type": "email-addr",
                    "value": "010001818b22f94b-c1c1b98b-16f5-40d0-a911-a7f562a5d1d1-000000@amazonses.com"
                },
                "11": {
                    "type": "email-addr",
                    "value": "user2@iscgalaxy.com"
                }
            },
            "first_observed": "2022-06-22T11:19:20Z",
            "last_observed": "2022-06-22T11:19:20Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```


### STIX Execute query
```shell
execute
gcp_chronicle
gcp_chronicle
"{\"type\":\"identity\",\"id\":\"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\",\"name\":\"gcp_chronicle\",\"identity_class\":\"events\",\"created\":\"2022-08-05T13:22:50.336Z\",\"modified\":\"2022-08-05T13:22:50.336Z\"}"
"{\"host\":\"xx.xx.xx\"}"
"{\"auth\":{ \"client_email\": \"xyz.com\",\"private_key\": \"-----BEGIN PRIVATE KEY-----\nxxx\n-----END PRIVATE KEY-----\n\"}}"
"[ipv4-addr:value = '1.0.0.1' AND network-traffic:src_port = '52221'] START t'2022-06-06T00:00:00.000000Z' STOP t'2022-06-15T00:00:00.000000Z'"
```
#### STIX Execute query - output
```json
{
    "type": "bundle",
    "id": "bundle--c5711d18-3ba9-4356-ada6-45c6c6b30c9c",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "chronicle",
            "identity_class": "system",
            "created": "2022-08-05T13:22:50.336Z",
            "modified": "2022-08-05T13:22:50.336Z"
        },
        {
            "id": "observed-data--920eb15d-f959-4112-a9b6-cbf7195ad231",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-08-05T13:22:50.336Z",
            "modified": "2022-08-05T13:22:50.336Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "code": "10190",
                    "created": "2022-06-13T14:14:54.409074800Z",
                    "action": "NETWORK_CONNECTION",
                    "provider": "Microsoft",
                    "agent": "AdvancedHunting-DeviceNetworkEvents",
                    "outcome": "DeviceNetworkEvents",
                    "host_ref": "1",
                    "user_ref": "2",
                    "file_ref": "4",
                    "process_ref": "3",
                    "parent_process_ref": "6",
                    "ip_refs": [
                        "8",
                        "11"
                    ],
                    "network_ref": "9",
                    "extensions": {
                        "x-gcp-chronicle-event": {
                            "target_hostname": "v20.events.data.microsoft.com"
                        }
                    }
                },
                "1": {
                    "type": "x-oca-asset",
                    "hostname": "alert-windows",
                    "extensions": {
                        "x-gcp-chronicle-asset": {
                            "asset_id": "DeviceId:4f22ab5dc4be96566ee3c9adb3b77280dc08bfdb"
                        }
                    },
                    "ip_refs": [
                        "8"
                    ]
                },
                "2": {
                    "type": "user-account",
                    "user_id": "system",
                    "extensions": {
                        "windows-account-ext": {
                            "sid": "S-1-5-18"
                        }
                    }
                },
                "3": {
                    "type": "process",
                    "creator_user_ref": "2",
                    "pid": 2788,
                    "binary_ref": "4",
                    "name": "svchost.exe",
                    "command_line": "svchost.exe -k utcsvc -p",
                    "parent_ref": "6"
                },
                "4": {
                    "type": "file",
                    "hashes": {
                        "SHA-256": "2b3efaca2e57e433e6950286f7a6fb46ed48411322a26d657e58f02f7d232224",
                        "MD5": "53a2c077e868af30525019e9d070eddd",
                        "SHA-1": "ed68d965d3572218fa5b17b54e7726df3b18dee3"
                    },
                    "size": 56352,
                    "name": "svchost.exe",
                    "parent_directory_ref": "5"
                },
                "5": {
                    "type": "directory",
                    "path": "c:\\windows\\system32"
                },
                "6": {
                    "type": "process",
                    "pid": 756,
                    "name": "services.exe",
                    "binary_ref": "7"
                },
                "7": {
                    "type": "file",
                    "name": "services.exe"
                },
                "8": {
                    "type": "ipv4-addr",
                    "value": "1.0.0.1"
                },
                "9": {
                    "type": "network-traffic",
                    "src_ref": "8",
                    "src_port": 52221,
                    "dst_ref": "11",
                    "dst_port": 443,
                    "protocols": [
                        "tcp"
                    ],
                    "extensions": {
                        "x-gcp-chronicle-network": {
                            "direction": "OUTBOUND"
                        }
                    }
                },
               "10": {
                    "type": "x-ibm-finding",
                    "src_ip_ref": "8",
                    "dst_ip_ref": "11",
                    "name": "ConnectionSuccess",
                    "extensions": {
                        "x-gcp-chronicle-security-result": {
                            "actions_taken": [
                                "ALLOW"
                            ]
                        }
                    },
                    "finding_type": "alert"
                },
                "11": {
                    "type": "ipv4-addr",
                    "value": "1.0.0.2"
                }
            },
            "first_observed": "2022-06-13T14:14:54.409074800Z",
            "last_observed": "2022-06-13T14:14:54.409074800Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}

```

### STIX Multiple Observation
```shell
translate gcp_chronicle query '{}' "([file:hashes.'SHA-1' = '6cbce4a295c163791b60fc23d285e6d84f28ee4c' OR file:size >10  ] OR [network-traffic:src_port IN (52221,443)] AND [process:command_line LIKE 'MsMpEng.exe']) START t'2022-06-01T00:00:00.030Z' STOP t'2022-07-05T00:00:00.030Z' OR [ipv4-addr:value != '1.1.1.2']"
```
#### STIX Multiple observation - output
```json
{
    "queries": [
        {
            "ruleText": "rule cp4s_gcp_udi_rule_1659763825 { meta: author = \"ibm cp4s user\" description = \"Create event rule that should generate detections\" events: (($udm.src.file.size > 10 or $udm.target.file.size > 10 or $udm.src.process.file.size > 10 or $udm.target.process.file.size > 10 or $udm.principal.process.file.size > 10 or $udm.about.file.size > 10) or ($udm.src.file.sha1 = \"6cbce4a295c163791b60fc23d285e6d84f28ee4c\" nocase or $udm.target.file.sha1 = \"6cbce4a295c163791b60fc23d285e6d84f28ee4c\" nocase or $udm.src.process.file.sha1 = \"6cbce4a295c163791b60fc23d285e6d84f28ee4c\" nocase or $udm.target.process.file.sha1 = \"6cbce4a295c163791b60fc23d285e6d84f28ee4c\" nocase or $udm.principal.process.file.sha1 = \"6cbce4a295c163791b60fc23d285e6d84f28ee4c\" nocase or $udm.about.file.sha1 = \"6cbce4a295c163791b60fc23d285e6d84f28ee4c\" nocase)) or (($udm.src.port = 52221 or $udm.src.port = 443) or ($udm.principal.port = 52221 or $udm.principal.port = 443)) or ($udm.src.process.command_line = /(?s)MsMpEng\\.exe/ nocase or $udm.target.process.command_line = /(?s)MsMpEng\\.exe/ nocase or $udm.principal.process.command_line = /(?s)MsMpEng\\.exe/ nocase or $udm.target.process.parent_process.command_line = /(?s)MsMpEng\\.exe/ nocase or $udm.principal.process.parent_process.command_line = /(?s)MsMpEng\\.exe/ nocase) condition: $udm}",
            "startTime": "2022-06-01T00:00:00.030Z",
            "endTime": "2022-07-05T00:00:00.030Z"
        },
        {
            "ruleText": "rule cp4s_gcp_udi_rule_1659763825 { meta: author = \"ibm cp4s user\" description = \"Create event rule that should generate detections\" events: ( all $udm.src.ip != \"1.1.1.2\" nocase  and all $udm.src.ip != \"\" ) or ( all $udm.target.ip != \"1.1.1.2\" nocase  and all $udm.target.ip != \"\" ) or ( all $udm.principal.ip != \"1.1.1.2\" nocase  and all $udm.principal.ip != \"\" ) condition: $udm}",
            "startTime": "2022-08-06T05:25:25.414Z",
            "endTime": "2022-08-06T05:30:25.414Z"
        }
    ]
}
```
### Limitations

- Delete method is not automatically available to all customers
- As per the chronicle documentation, after the rule has been saved, we cannot delete it from the Rules Editor or the Rules Dashboard in UI.  It can be deleted only through Delete Rule API.
Reference: [Managing rules using the Rules Editor](#https://cloud.google.com/chronicle/docs/detection/manage-all-rules)

### Observations

- It is recommended to use LIKE operator for substring match and MATCHES operator for regular expression match.
- Supported values for the stix attribute x-ibm-finding:severity is 16,32,48,64,80,100. This has been mapped with chronicle severity value 'INFORMATIONAL','ERROR',LOW','MEDIUM','HIGH','CRITICAL' correspondingly.

### References
- [Chronicle Detection Engine API](https://cloud.google.com/chronicle/docs/reference/detection-engine-api)
- [YARA-L 2.0 Language syntax](https://cloud.google.com/chronicle/docs/detection/yara-l-2-0-syntax)
- [UDM fields list](https://cloud.google.com/chronicle/docs/reference/udm-field-list)
