# Okta

## Supported STIX Mappings

See the [table of mappings](okta_supported_stix.md) for the STIX objects and operators supported by this connector.

**Table of Contents**

- [Okta API Endpoints](#Okta-api-endpoints)
- [Pattern expression with STIX and CUSTOM attributes - Single Observation](#single-observation)
- [Pattern expression with STIX and CUSTOM attributes - Multiple Observation](#multiple-observation)
- [STIX Execute Query](#stix-execute-query)
- [Limitations](#limitations)
- [References](#references)

### Okta API Endpoints

   | Connector Method | Okta API Endpoint     | Method |
   |-----|------|   ------|
   | Ping Endpoint   | https://< server >/api/v1/org | GET  | 
   | Results Endpoint | https://< server >/api/v1/logs  | GET  |

### Format for calling stix-shifter from the command line
```
python main.py `<translator_module>` `<query or result>` `<STIX identity object>` `<data>`
```
### Pattern expression with STIX and CUSTOM attributes

#### Single Observation

#### STIX Translate query to fetch the suspicious activity reported by specific user
```shell
translate okta query '{}' "[ user-account:account_login = 'user@login.com' AND x-oca-event:action = 'user.account.report_suspicious_activity_by_enduser'] START t'2022-12-15T00:00:00.000Z' STOP t'2023-01-15T00:00:00.000Z'"
```
#### STIX Translate query - output
```json
{
    "queries": [
        "filter=eventType eq \"user.account.report_suspicious_activity_by_enduser\" and actor.alternateId eq \"user@login.com\" &since=2022-12-15T00:00:00.000Z&until=2023-01-15T00:00:00.000Z"
    ]
}

```

#### STIX Transmit results 

```shell
transmit
okta
"{\"host\":\"xyz\"}"
"{\"auth\":{\"api_token\": \"xxx\"}}"
results
"filter=eventType eq \"user.account.report_suspicious_activity_by_enduser\" and actor.alternateId eq \"user@login.com\" &since=2022-12-15T00:00:00.000Z&until=2023-01-15T00:00:00.000Z"
0
1
```

#### STIX Transmit results - output
```json
{
    "success": true,
    "data": [
        {
            "actor": {
                "id": "00u7rkrly9sNvp7sa5d7",
                "type": "User",
                "alternateId": "user@login.com",
                "displayName": "User1",
                "detailEntry": null
            },
            "client": {
                "userAgent": {
                    "rawUserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
                    "os": "Windows 10",
                    "browser": "CHROME"
                },
                "zone": "null",
                "device": "Computer",
                "id": null,
                "ipAddress": "1.0.0.1",
                "geographicalContext": {
                    "city": "Chennai",
                    "state": "Tamil Nadu",
                    "country": "India",
                    "postalCode": "600001",
                    "geolocation": {
                        "lat": 12.8996,
                        "lon": 80.2209
                    }
                }
            },
            "device": null,
            "authenticationContext": {
                "authenticationProvider": null,
                "credentialProvider": null,
                "credentialType": null,
                "issuer": null,
                "interface": null,
                "authenticationStep": 0,
                "externalSessionId": "trsb6xDfCvbQlyyOqs7VCtS3g"
            },
            "displayMessage": "User report suspicious activity",
            "eventType": "user.account.report_suspicious_activity_by_enduser",
            "outcome": {
                "result": "SUCCESS",
                "reason": null
            },
            "published": "2022-12-28T09:59:25.765Z",
            "securityContext": {
                "asNumber": 17488,
                "asOrg": "hathway cable and datacom limited",
                "isp": "hathway ip over cable internet",
                "isProxy": false
            },
            "severity": "WARN",
            "debugContext": [
                {
                    "debugData": {
                        "suspiciousActivityEventCountry": "India",
                        "suspiciousActivityBrowser": "CHROME",
                        "suspiciousActivityEventId": "151d9579-8696-11ed-90ed-cbc1a8ace225",
                        "suspiciousActivityEventState": "Tamil Nadu",
                        "suspiciousActivityTimestamp": "2022-12-28T09:57:47.583Z",
                        "requestUri": "/api/internal/users/me/report-suspicious-activity",
                        "suspiciousActivityOs": "Windows 10",
                        "suspiciousActivityEventLatitude": "12.8996",
                        "suspiciousActivityEventTransactionId": "Y6wTGxUh0VjE-LZiJLMMoAAABPk",
                        "url": "/api/internal/users/me/report-suspicious-activity?i=eyJ6aXAiOiJERUYiLCJ2ZXIiOiIxIiwiZW5jIjoiQTI1NkdDTSIsImFsZyI6ImRpciJ9..qARtayNpmEMV0CNA.GRk6HYGdXGjFT4uRsMPF1icztTc4SL9Yi_wmm4Is6ginIlqk8zriOdYvREuactglxvuxFLxQSa6XTPgsFt7TZIZOEKk3uDbNkf_9Z1n7Hij7CFvO-WQ_nOoh0l5hoTcNKU8GMJ5xR4p2W349vGTqok2Ey3SkckkIDyyaupRFmy4PwhezN5IPRG6I4XwRcX0ALGlCkRlE7C7E-w.EOk8zmJ7AFr4CUswFv9heQ",
                        "requestId": "Y6wTfThOwKPnxngKYrJ0pgAAB3g",
                        "dtHash": "50b7a2f07f21b3d7efb90c673afb756b57d7236f73bff7688edfec31451c10f9",
                        "suspiciousActivityEventCity": "Chennai",
                        "suspiciousActivityEventLongitude": "80.2209",
                        "suspiciousActivityEventIp": "1.0.0.1",
                        "suspiciousActivityEventType": "system.email.new_device_notification.sent_message"
                    }
                }
            ],
            "legacyEventType": "core.user.account.report_suspicious_activity_by_enduser",
            "transaction": {
                "type": "WEB",
                "id": "Y6wTfThOwKPnxngKYrJ0pgAAB3g",
                "detail": {}
            },
            "uuid": "4fa2f7e4-8696-11ed-8688-39c4b4d86042",
            "version": "0",
            "target": [
                {
                    "id": "00u7rkrly9sNvp7sa5d7",
                    "type": "User",
                    "alternateId": "user@login.com",
                    "displayName": "User1",
                    "detailEntry": null
                }
            ]
        }
    ],
    "metadata": {
        "result_count": 1,
        "next_page_token": "after=123"
    }
}
```


#### STIX Translate results

```json
{
    "type": "bundle",
    "id": "bundle--1fd10f98-950a-41cb-981d-968593e24056",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "okta",
            "identity_class": "events",
            "created": "2022-08-22T13:22:50.336Z",
            "modified": "2022-08-22T13:22:50.336Z"
        },
        {
            "id": "observed-data--a665a746-72e7-4bfb-896d-3bc936329999",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2023-02-24T09:27:32.436Z",
            "modified": "2023-02-24T09:27:32.436Z",
            "objects": {
                "0": {
                    "type": "user-account",
                    "user_id": "00u7rkrly9sNvp7sa5d7",
                    "x_actor_type": "User",
                    "account_login": "user@login.com",
                    "display_name": "User1"
                },
                "1": {
                    "type": "x-oca-event",
                    "x_actor_ref": "0",
                    "x_client_ref": "3",
                    "ip_refs": [
                        "4"
                    ],
                    "x_authentication_context_ref": "5",
                    "x_event_description": "User report suspicious activity",
                    "action": "user.account.report_suspicious_activity_by_enduser",
                    "outcome": "SUCCESS",
                    "x_severity": "WARN",
                    "x_debug_ref": "7",
                    "x_legacy_event_type": "core.user.account.report_suspicious_activity_by_enduser",
                    "category": [
                        "WEB"
                    ],
                    "x_transaction_id": "Y6wTfThOwKPnxngKYrJ0pgAAB3g",
                    "x_event_unique_id": "4fa2f7e4-8696-11ed-8688-39c4b4d86042",
                    "x_target_refs": [
                        "8"
                    ]
                },
                "2": {
                    "type": "software",
                    "x_raw_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
                    "x_client_os": "Windows 10",
                    "name": "CHROME"
                },
                "3": {
                    "type": "x-okta-client",
                    "software_ref": "2",
                    "network_zone_name": "null",
                    "device": "Computer",
                    "ip_ref": "4",
                    "geolocation_city": "Chennai",
                    "geolocation_state": "Tamil Nadu",
                    "geolocation_country": "India",
                    "geolocation_postalcode": "600001",
                    "geolocation_coordinates": {
                        "lat": 12.8996,
                        "lon": 80.2209
                    },
                    "autonomous_system_ref": "6"
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "1.0.0.1"
                },
                "5": {
                    "type": "x-okta-authentication-context",
                    "session_id": "trsb6xDfCvbQlyyOqs7VCtS3g"
                },
                "6": {
                    "type": "autonomous-system",
                    "number": 17488,
                    "name": "hathway cable and datacom limited",
                    "x_isp": "hathway ip over cable internet"
                },
                "7": {
                    "type": "x-okta-debug-context",
                    "debug_data": {
                        "suspiciousActivityEventCountry": "India",
                        "suspiciousActivityBrowser": "CHROME",
                        "suspiciousActivityEventId": "151d9579-8696-11ed-90ed-cbc1a8ace225",
                        "suspiciousActivityEventState": "Tamil Nadu",
                        "suspiciousActivityTimestamp": "2022-12-28T09:57:47.583Z",
                        "requestUri": "/api/internal/users/me/report-suspicious-activity",
                        "suspiciousActivityOs": "Windows 10",
                        "suspiciousActivityEventLatitude": "12.8996",
                        "suspiciousActivityEventTransactionId": "Y6wTGxUh0VjE-LZiJLMMoAAABPk",
                        "url": "/api/internal/users/me/report-suspicious-activity?i=eyJ6aXAiOiJERUYiLCJ2ZXIiOiIxIiwiZW5jIjoiQTI1NkdDTSIsImFsZyI6ImRpciJ9..qARtayNpmEMV0CNA.GRk6HYGdXGjFT4uRsMPF1icztTc4SL9Yi_wmm4Is6ginIlqk8zriOdYvREuactglxvuxFLxQSa6XTPgsFt7TZIZOEKk3uDbNkf_9Z1n7Hij7CFvO-WQ_nOoh0l5hoTcNKU8GMJ5xR4p2W349vGTqok2Ey3SkckkIDyyaupRFmy4PwhezN5IPRG6I4XwRcX0ALGlCkRlE7C7E-w.EOk8zmJ7AFr4CUswFv9heQ",
                        "requestId": "Y6wTfThOwKPnxngKYrJ0pgAAB3g",
                        "dtHash": "50b7a2f07f21b3d7efb90c673afb756b57d7236f73bff7688edfec31451c10f9",
                        "suspiciousActivityEventCity": "Chennai",
                        "suspiciousActivityEventLongitude": "80.2209",
                        "suspiciousActivityEventIp": "1.0.0.1",
                        "suspiciousActivityEventType": "system.email.new_device_notification.sent_message"
                    }
                },
                "8": {
                    "type": "x-okta-target",
                    "target_id": "00u7rkrly9sNvp7sa5d7",
                    "target_type": "User",
                    "alternate_id": "user@login.com",
                    "display_name": "User1"
                }
            },
            "first_observed": "2022-12-28T09:59:25.765Z",
            "last_observed": "2022-12-28T09:59:25.765Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}

```

#### Multiple Observation

```shell
translate okta query '{}' "([ipv4-addr:value NOT = '5.0.1.5' AND user-account:display_name MATCHES 'abc'] AND [x-okta-authentication-context:credential_type = 'IWA'])START t'2022-12-10T16:43:26.000Z' STOP t'2023-01-15T16:43:26.003Z' OR [x-oca-event:x_legacy_event_type = 'app.ldap.login.disabled_account' AND x-oca-event:outcome = 'FAILURE']START t'2023-01-01T16:43:26.000Z' STOP t'2023-02-10T16:43:26.003Z' AND [ x-oca-event:x_outcome_reason = 'NETWORK_ZONE_BLACKLIST']"
```

#### STIX Multiple observation - output
```json
{
   "queries": [
      "filter=(actor.displayName co \"abc\" and not(request.ipChain.ip eq \"5.0.1.5\")) or (authenticationContext.credentialType eq \"IWA\") &since=2022-12-10T16:43:26.000Z&until=2023-01-15T16:43:26.003Z",
      "filter=outcome.result eq \"FAILURE\" and legacyEventType eq \"app.ldap.login.disabled_account\" &since=2023-01-01T16:43:26.000Z&until=2023-02-10T16:43:26.003Z",
      "filter=outcome.reason eq \"NETWORK_ZONE_BLACKLIST\" &since=2023-02-24T11:35:13.120Z&until=2023-02-24T11:40:13.120Z"
   ]
}
```

### STIX Execute query
```shell
execute
okta
okta
"{\"type\":\"identity\",\"id\":\"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\",\"name\":\"okta\",\"identity_class\":\"system\",\"created\":\"2023-02-23T13:22:50.336Z\",\"modified\":\"2022-02-23T13:22:50.336Z\"}"
"{\"host\":\"xyz\"}"
"{\"auth\":{\"api_token\": \"xxx\"}}"
"[domain-name:value LIKE 'amazon' AND x-okta-target:target_type = 'AppInstance' OR (x-oca-event:action = 'user.authentication.auth_via_LDAP_agent' AND x-oca-event:outcome = 'FAILURE')]START t'2023-01-01T16:43:26.000Z' STOP t'2023-02-23T16:43:26.003Z'"
```

#### STIX Execute query - output
```json
{
    "type": "bundle",
    "id": "bundle--cfb1b466-2204-4381-bb0f-1a8b8f7b1ac2",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "okta",
            "identity_class": "system",
            "created": "2023-02-23T13:22:50.336Z",
            "modified": "2022-02-23T13:22:50.336Z"
        },
        {
            "id": "observed-data--6636db4b-aacd-423d-a505-fb37ca8394fe",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2023-02-24T10:30:59.523Z",
            "modified": "2023-02-24T10:30:59.523Z",
            "objects": {
                "0": {
                    "type": "user-account",
                    "user_id": "00u7rkrly9sNvp7sa5d7",
                    "x_actor_type": "User",
                    "account_login": "zbc@login.com",
                    "display_name": "zbc"
                },
                "1": {
                    "type": "x-oca-event",
                    "x_actor_ref": "0",
                    "x_client_ref": "3",
                    "ip_refs": [
                        "4"
                    ],
                    "x_authentication_context_ref": "5",
                    "x_event_description": "Evaluation of sign-on policy",
                    "action": "policy.evaluate_sign_on",
                    "outcome": "CHALLENGE",
                    "x_outcome_reason": "Sign-on policy evaluation resulted in CHALLENGE",
                    "x_severity": "INFO",
                    "x_debug_ref": "8",
                    "category": [
                        "WEB"
                    ],
                    "x_transaction_id": "Y7Jo7I8JgCIFXoYvGC9mYgAABc0",
                    "x_event_unique_id": "c2f00eb4-8a5c-11ed-b791-497a3600da6e",
                    "x_target_refs": [
                        "9",
                        "10",
                        "11"
                    ]
                },
                "2": {
                    "type": "software",
                    "x_raw_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
                    "x_client_os": "Windows 10",
                    "name": "CHROME"
                },
                "3": {
                    "type": "x-okta-client",
                    "software_ref": "2",
                    "network_zone_name": "null",
                    "device": "Computer",
                    "ip_ref": "4",
                    "geolocation_city": "Ashburn",
                    "geolocation_state": "Virginia",
                    "geolocation_country": "United States",
                    "geolocation_postalcode": "20149",
                    "geolocation_coordinates": {
                        "lat": 39.0469,
                        "lon": -77.4903
                    },
                    "autonomous_system_ref": "6"
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "2.3.4.5"
                },
                "5": {
                    "type": "x-okta-authentication-context",
                    "session_id": "idxWRXEwK76RdSihI1Py0VBeg"
                },
                "6": {
                    "type": "autonomous-system",
                    "number": 14618,
                    "name": "amazon technologies inc.",
                    "x_isp": "amazon.com  inc.",
                    "x_domain_ref": "7"
                },
                "7": {
                    "type": "domain-name",
                    "value": "amazonaws.com"
                },
                "8": {
                    "type": "x-okta-debug-context",
                    "debug_data": {
                        "authnRequestId": "Y7JovAXgLp7AZga3sy6V3wAADf4",
                        "deviceFingerprint": "5740d739064fe1bfde671e63a53959fb",
                        "behaviors": "{riskIP=POSITIVE, New Geo-Location=NEGATIVE, New Device=NEGATIVE, New IP=POSITIVE, New State=NEGATIVE, New Country=NEGATIVE, Velocity=POSITIVE, New City=NEGATIVE}",
                        "requestId": "Y7Jo7I8JgCIFXoYvGC9mYgAABc0",
                        "authMethodFirstVerificationTime": "2023-01-02T05:17:33.010Z",
                        "dtHash": "98af3fbc52613345f70c66a0ccef179ce4203c1f60207f962d5e986acb72a9cc",
                        "authMethodFirstType": "okta_password:password:aut4oewi7rc5cRsK25d7",
                        "authMethodFirstEnrollment": "laetgp32xjcQuvP1V5d6",
                        "risk": "{reasons=Anomalous Location, level=MEDIUM}",
                        "requestUri": "/idp/idx/identify",
                        "threatSuspected": "false",
                        "url": "/idp/idx/identify?"
                    }
                },
                "9": {
                    "type": "x-okta-target",
                    "target_id": "0oa4unchvq34zg0H35d7",
                    "target_type": "AppInstance",
                    "alternate_id": "RSA Demo Site",
                    "display_name": "RSA Demo Site",
                    "detail_entry": {
                        "signOnModeType": "SAML_2_0",
                        "signOnModeEvaluationResult": "CHALLENGE"
                    }
                },
                "10": {
                    "type": "x-okta-target",
                    "target_id": "0pr4wcsce0bhKUjqw5d7",
                    "target_type": "Rule",
                    "alternate_id": "unknown",
                    "display_name": "cp4s_global_rule"
                },
                "11": {
                    "type": "x-okta-target",
                    "target_id": "rul4wd559lmwLouuu5d7",
                    "target_type": "Rule",
                    "alternate_id": "unknown",
                    "display_name": "Catch-all Rule"
                }
            },
            "first_observed": "2023-01-02T05:17:33.049Z",
            "last_observed": "2023-01-02T05:17:33.049Z",
            "number_observed": 1
        }
    ]
}
```

### Limitations

- Okta system log doesn’t support regular expression pattern matching
- Okta APIs and Okta API token are subjected to rate limits.
Reference: [Okta Rate Limits](https://developer.okta.com/docs/reference/rate-limits/)
- Okta system log retains events for 90 days

### References
- [System Log - Okta Developer](https://developer.okta.com/docs/reference/api/system-log/)
- [Suspicious activity events](https://help.okta.com/oie/en-us/Content/Topics/Reports/suspicious-activity-report.htm)
- [Okta Developer Guide](https://developer.okta.com/docs/guides/)
