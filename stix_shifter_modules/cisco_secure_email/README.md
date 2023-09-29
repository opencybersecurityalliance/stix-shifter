# Cisco Secure Email

**Table of Contents**

- [Cisco Secure Email API Endpoints](#Cisco Secure Email-api-endpoints)
- [Pattern expression with STIX and CUSTOM attributes - Single Observation](#single-observation)
- [Pattern expression with STIX and CUSTOM attributes - Multiple Observation](#multiple-observation)
- [STIX Execute Query](#stix-execute-query)
- [Limitations](#limitations)
- [Observations](#observations)
- [References](#references)

### Cisco Secure Email API Endpoints

   | Connector Method | Cisco Secure Email API Endpoint     | Method |
   |-----|------|   ------|
   | Ping Endpoint   | https://< server >/esa/api/v2.0/login/privileges | GET  | 
   | Token Endpoint  | https://< server >/esa/api/v2.0/login  | POST  |
   | Results Endpoint | https://< server >/esa/api/v2.0/message-tracking/messages  | GET  |

### Format for calling stix-shifter from the command line
```
python main.py `<translator_module>` `<query or result>` `<STIX identity object>` `<data>`
```
### Pattern expression with STIX and CUSTOM attributes

#### Single Observation

#### STIX Translate query to fetch the messages from a specific ipaddress
```shell
translate cisco_secure_email query {} "[ipv4-addr:value='1.1.1.1'] START t'2023-08-01T11:00:00.000Z' STOP t'2023-08-31T21:00:00.003Z'"
```
#### STIX Translate query - output
```json
{
    "queries": [
        "senderIp=1.1.1.1&startDate=2023-08-01T11:00:00.000Z&endDate=2023-08-31T21:00:00.000Z"
    ]
}

```

#### STIX Transmit results 

```shell
transmit
cisco_secure_email
"{\"host\":\"instance.cisco_secure_email\", \"port\":xxxx, \"selfSignedCert\":\"-----BEGIN CERTIFICATE-----xxxxx-----END CERTIFICATE-----\"}"
"{\"auth\":{\"username\":\"apiuser\", \"password\":\"xxxx\"}}"
results
"senderIp=1.1.1.1&startDate=2023-08-01T11:00:00.000Z&endDate=2023-08-31T21:00:00.000Z"
0
1
```

#### STIX Transmit results - output
```json
{
    "success": true,
    "data": [
        {
            "attributes": {
                "hostName": "host",
                "friendly_from": [
                    "user1@dummydomain.com"
                ],
                "isCompleteData": "N/A",
                "messageStatus": {
                    "1757": "Delivered"
                },
                "recipientMap": {
                    "1756": [
                        "user1@dummydomain.com"
                    ],
                    "1757": [
                        "user1@dummydomain.com"
                    ]
                },
                "senderIp": "1.1.1.1",
                "mailPolicy": [
                    "DEFAULT"
                ],
                "senderGroup": "UNKNOWNLIST",
                "morInfo": {
                    "midVsState": {
                        "1757": "Delivered"
                    }
                },
                "subject": "URL - https://www.indianexpress.com",
                "mid": [
                    1756,
                    1757
                ],
                "senderDomain": "amazonses.com",
                "finalSubject": {
                    "1757": "URL - https://www.indianexpress.com"
                },
                "direction": "incoming",
                "icid": 1625,
                "morDetails": {},
                "replyTo": "user3@dummydomain.com",
                "timestamp": "29 Aug 2023 10:00:48 (GMT +00:00)",
                "messageID": {
                    "1756": "<0100018a404d1371-34997a47-abde-49df-bb90-d6c22aaee8ba-000000@email.amazonses.com>"
                },
                "verdictChart": {
                    "1757": "01101110"
                },
                "recipient": [
                    "user1@dummydomain.com"
                ],
                "sender": "0100018a404d1371-34997a47-abde-49df-bb90-d6c22aaee8ba-000000@amazonses.com",
                "serialNumber": "EC2CD1D95C273722A23A-CA0C47E74D1B",
                "allIcid": [
                    1625
                ],
                "sbrs": "3.5"
            }
        }
    ]
}
```


#### STIX Translate results

```json
{
    "type": "bundle",
    "id": "bundle--31b224bc-75a0-4598-b4a6-c12c0855c2e5",
    "objects": [
        {
            "type": "identity",
            "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
            "name": "cisco secure email",
            "identity_class": "events"
        },
        {
            "id": "observed-data--c9200bf6-57ef-49df-8a9c-40cbe88359fd",
            "type": "observed-data",
            "created_by_ref": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
            "created": "2023-09-19T08:43:16.582Z",
            "modified": "2023-09-19T08:43:16.582Z",
            "objects": {
                "0": {
                    "type": "x-oca-asset",
                    "hostname": "host"
                },
                "1": {
                    "type": "email-message",
                    "x_cisco_host_ref": "0",
                    "from_ref": "2",
                    "is_multipart": true,
                    "x_sender_ip_ref": "4",
                    "x_sender_group": "UNKNOWNLIST",
                    "subject": "URL - https://www.indianexpress.com",
                    "x_cisco_mid": 1756,
                    "x_cisco_icid": 1625,
                    "date": "2023-08-29T10:00:00.000Z",
                    "x_message_id_header": "<0100018a404d1371-34997a47-abde-49df-bb90-d6c22aaee8ba-000000@email.amazonses.com>",
                    "to_refs": [
                        "7"
                    ],
                    "sender_ref": "8",
                    "x_serial_number": "EC2CD1D95C273722A23A-CA0C47E74D1B"
                },
                "2": {
                    "type": "email-addr",
                    "value": "user1@dummydomain.com"
                },
                "3": {
                    "type": "x-cisco-email-msgevent",
                    "message_status": "Delivered",
                    "mail_policy": [
                        "DEFAULT"
                    ],
                    "direction": "incoming",
                    "reply_to": "6",
                    "sbrs_score": "3.5"
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "5": {
                    "type": "domain-name",
                    "value": "amazonses.com",
                    "resolves_to_refs": [
                        "4"
                    ]
                },
                "6": {
                    "type": "email-addr",
                    "value": "user3@dummydomain.com"
                },
                "7": {
                    "type": "email-addr",
                    "value": "user1@dummydomain.com"
                },
                "8": {
                    "type": "email-addr",
                    "value": "0100018a404d1371-34997a47-abde-49df-bb90-d6c22aaee8ba-000000@amazonses.com"
                }
            },
            "first_observed": "2023-08-29T10:00:00.000Z",
            "last_observed": "2023-08-29T10:00:00.000Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```

#### Multiple Observation

```shell
translate 
cisco_secure_email 
query {} 
"[ipv4-addr:value = '1.1.1.1' AND file:hashes.'SHA-256' = '271c0119ac4455fc8db4ef4a8caf8e2bfcfb8bbd3b8c894e117a9ae9f743894b' ] OR [x-cisco-email-msgevent:message_status = 'DELIVERED']START t'2023-07-19T01:56:00.000Z' STOP t'2023-09-01T01:57:00.003Z'"
```

#### STIX Multiple observation - output
```json
{
   "queries": [
      "fileSha256=271c0119ac4455fc8db4ef4a8caf8e2bfcfb8bbd3b8c894e117a9ae9f743894b&senderIp=1.1.1.1&startDate=2023-09-05T10:52:00.000Z&endDate=2023-09-05T10:57:00.000Z",
        "deliveryStatus=DELIVERED&startDate=2023-07-19T01:56:00.000Z&endDate=2023-09-01T01:57:00.000Z"
   ]
}
```

### STIX Execute query
```shell
execute
cisco_secure_email
cisco_secure_email
"{\"type\":\"identity\",\"id\":\"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\",\"name\":\"cisco_secure_email\",\"identity_class\":\"events\",\"created\":\"2023-02-23T13:22:50.336Z\",\"modified\":\"2022-02-23T13:22:50.336Z\"}"
"{\"host\":\"instance.cisco_secure_email\", \"port\":xxxx, \"selfSignedCert\":\"-----BEGIN CERTIFICATE-----xxxxx-----END CERTIFICATE-----\"}"
"{\"auth\":{\"username\":\"apiuser\", \"password\":\"xxxx\"}}"
"[ipv4-addr:value = '1.1.1.1' AND file:hashes.'SHA-256' = '271c0119ac4455fc8db4ef4a8caf8e2bfcfb8bbd3b8c894e117a9ae9f743894b' ] OR [x-cisco-email-msgevent:message_status = 'DELIVERED']START t'2023-07-19T01:56:00.000Z' STOP t'2023-09-01T01:57:00.003Z'"
```

#### STIX Execute query - output
```json
{
    "type": "bundle",
    "id": "bundle--dc608fc4-f6e6-4d7e-8ea5-124441153e77",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "cisco_secure_email",
            "identity_class": "events",
            "created": "2023-02-23T13:22:50.336Z",
            "modified": "2022-02-23T13:22:50.336Z"
        },
        {
            "id": "observed-data--c0129c6d-9251-46b2-9b01-62bfbabeea45",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2023-09-05T11:06:27.543Z",
            "modified": "2023-09-05T11:06:27.543Z",
            "objects": {
                "0": {
                    "type": "email-addr",
                    "value": "user1@dummydomain.com"
                },
                "1": {
                    "type": "email-message",
                    "from_ref": "0",
                    "is_multipart": true,
                    "x_sender_ip_ref": "3",
                    "x_sender_group": "UNKNOWNLIST",
                    "subject": "new site test",
                    "x_cisco_mid": 1786,
                    "x_cisco_icid": 1697,
                    "date": "2023-08-31T09:54:00.000Z",
                    "x_message_id_header": "<0100018a4b044014-40f605c5-fb57-497c-b6d3-87e5cc7e661d-000000@email.amazonses.com>",
                    "to_refs": [
                        "6"
                    ],
                    "sender_ref": "7",
                    "x_serial_number": "EC2CD1D95C273722A23A-CA0C47E74D1B"
                },
                "2": {
                    "type": "x-cisco-email-msgevent",
                    "message_status": "Delivered",
                    "mail_policy": [
                        "DEFAULT"
                    ],
                    "direction": "incoming",
                    "reply_to": "5",
                    "sbrs_score": "5.2"
                },
                "3": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "4": {
                    "type": "domain-name",
                    "value": "amazonses.com",
                    "resolves_to_refs": [
                        "3"
                    ]
                },
                "5": {
                    "type": "email-addr",
                    "value": "user11@dummydomain.com"
                },
                "6": {
                    "type": "email-addr",
                    "value": "user1@dummydomain.com"
                },
                "7": {
                    "type": "email-addr",
                    "value": "0100018a4b044014-40f605c5-fb57-497c-b6d3-87e5cc7e661d-000000@amazonses.com"
                }
            },
            "first_observed": "2023-09-05T11:06:27.543Z",
            "last_observed": "2023-09-05T11:06:27.543Z",
            "number_observed": 1
        },
       {
            "id": "observed-data--0affd03f-d76d-4729-a546-9f7a9c666bce",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2023-09-05T11:06:27.547Z",
            "modified": "2023-09-05T11:06:27.547Z",
            "objects": {
                "0": {
                    "type": "email-addr",
                    "value": "user1@dummydomain.com"
                },
                "1": {
                    "type": "email-message",
                    "from_ref": "0",
                    "is_multipart": true,
                    "x_sender_ip_ref": "3",
                    "x_sender_group": "UNKNOWNLISTTEST",
                    "subject": "Fwd: image",
                    "x_cisco_mid": 1783,
                    "x_cisco_icid": 1693,
                    "date": "2023-08-31T08:31:00.000Z",
                    "x_message_id_header": "<0100018a4ab7bcc1-2de5bed1-70f4-412c-aa19-478aca21b37c-000000@email.amazonses.com>",
                    "to_refs": [
                        "6"
                    ],
                    "sender_ref": "7",
                    "x_serial_number": "EC2CD1D95C273722A23A-CA0C47E74D1B"
                },
                "2": {
                    "type": "x-cisco-email-msgevent",
                    "message_status": "Delivered",
                    "mail_policy": [
                        "DEFAULT"
                    ],
                    "direction": "incoming",
                    "reply_to": "5",
                    "sbrs_score": "3.5"
                },
                "3": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "4": {
                    "type": "domain-name",
                    "value": "amazonses.com",
                    "resolves_to_refs": [
                        "3"
                    ]
                },
                "5": {
                    "type": "email-addr",
                    "value": "user11@dummydomain.com"
                },
                "6": {
                    "type": "email-addr",
                    "value": "user3@dummydomain.com"
                },
                "7": {
                    "type": "email-addr",
                    "value": "0100018a4ab7bcc1-2de5bed1-70f4-412c-aa19-478aca21b37c-000000@amazonses.com"
                }
            },
            "first_observed": "2023-09-05T11:06:27.547Z",
            "last_observed": "2023-09-05T11:06:27.547Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```

### Observations
- LIKE, IN operators are supported for certain fields only.(For example: envelopeRecipientfilterValue, 
  envelopeSenderfilterValue, subjectfilterValue, domainNameValue, replyToValue, attachmentNameValue,
  contentFiltersDirection, quarantinedTo, urlCategories)
- AND isn’t supported within the attributes belonging to x-cisco-email-msgevent group. 
      Example: "[x-cisco-email-msgevent:spam_positive='true' AND x-cisco-email-msgevent:virus_positive='true']"
      Wrong Parameter error is returned in such case.  
- The user inactivity timeout settings in the email gateway applies to the validity of a JWT(5 - 1440 Minutes (24 hours)). 
  The email gateway checks every API query with a JWT, for its time validity. So based on the response code a new refresh JWT is generated, and to be used with API calls.


### Limitations
- Due to a Cisco API limitation, the recommended maximum value for result limit is 800. If timeout error occurs it is recommended to use smaller value for result limit.
- ‘NOT’, <, >, <=, >= operators are not supported.

### References
- [Cisco Secure Email Product Overview](https://www.cisco.com/c/en/us/products/security/email-security/what-is-secure-email.html)
- [Overview Guide for Cisco Cloud/Hybrid Secure Email](https://www.cisco.com/c/dam/en/us/td/docs/security/ces/overview_guide/Cisco_Cloud_Hybrid_Email_Security_Overview_Guide.pdf)
- [AsyncOS 15.0 API for Cisco Secure Email](https://www.cisco.com/c/en/us/td/docs/security/esa/esa15-0/api_guide/b_Secure_Email_API_Guide_15-0/b_ESA_API_Guide_chapter_01.html)
- [AsyncOS 15.0 API - Addendum to the Getting Started Guide for Cisco Secure Email](https://www.cisco.com/c/en/us/support/security/email-security-appliance/products-programming-reference-guides-list.html)