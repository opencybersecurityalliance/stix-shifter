# Infoblox Connector

TBD

### Dialects

* tideDbData
* dnsEventsData
* dossierData

### Infoblox API Endpoints:

TBD

##### Reference - [Infoblox API Documentation](https://docs.infoblox.com/display/BloxOneThreatDefense/Infoblox+TIDE+and+Dossier+Guides+for+the+Cloud+Services+Portal)

### Format for calling stix-shifter from the command line:

python main.py `<translator_module>` `<query or result>` `<STIX identity object>` `<data>`

### Pattern expression with STIX attributes

#### STIX patterns

TBD

#### Translated query

TBD

#### Above translated query is passed as parameter to STIX transmission module

##### Transmit Search Call

TBD

#### Transmit Search Output

TBD

##### Transmit Results Call

TBD

#### Transmit Results Output

##### tideDbData

```json
```

##### dnsEventsData

```json
{
  "result": [
    {
      "category": "",
      "confidence": "HIGH",
      "country": "unknown",
      "device": "DESKTOP-VT5P2QT",
      "dhcp_fingerprint": "",
      "event_time": "2021-06-05T10:11:05.000Z",
      "feed_name": "Base",
      "feed_type": "FQDN",
      "mac_address": "00:50:56:0b:06:58",
      "network": "BloxOne Endpoint",
      "os_version": "Windows 10 Enterprise",
      "policy_name": "DFND",
      "private_ip": "192.168.24.198",
      "qip": "208.50.179.13",
      "qname": "total-update.com.",
      "qtype": "A",
      "rcode": "PASSTHRU",
      "rdata": "18.185.74.46",
      "rip": "",
      "severity": "HIGH",
      "tclass": "APT",
      "threat_indicator": "total-update.com",
      "tproperty": "MalwareC2",
      "user": "rdp"
    }
  ],
  "status_code": "200"
}
```

##### dossierData

```json
```

### Trend Micro Vision One response to STIX object (STIX attributes)

#### STIX observable output

##### tideDbData

```json
```

##### dnsEventsData

```json
{
    "type": "bundle",
    "id": "bundle--9a76f81f-f2d5-4d3e-92dd-5359cf77b957",
    "spec_version": "2.0",
    "objects": [
        {
            "id": "identity--b1898903-f26b-43fb-982e-4b35cb35f060",
            "name": "name",
            "type": "identity",
            "identity_class": "individual",
            "created": "2021-06-28T08:58:24.239Z",
            "modified": "2021-06-28T08:58:24.239Z"
        },
        {
            "id": "observed-data--ab261396-0c22-468b-8bfc-53becb3223fc",
            "type": "observed-data",
            "created_by_ref": "identity--b1898903-f26b-43fb-982e-4b35cb35f060",
            "created": "2021-06-28T08:58:29.505Z",
            "modified": "2021-06-28T08:58:29.505Z",
            "objects": {
                "0": {
                    "type": "ipv4-addr",
                    "value": "192.168.24.198",
                    "resolves_to_refs": [
                      "1"
                    ]
                },
                "1": {
                    "type": "mac-addr",
                    "value": "00:50:56:0b:06:58"
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "208.50.179.13"
                },
                "3": {
                    "type": "domain-name",
                    "value": "total-update.com."
                },
                "4": {
                    "type": "network-traffic",
                    "src_ref": "2",
                    "extensions": {
                      "dns-ext": {
                        "question": {
                          "type": "A",
                          "domain_ref": "3"
                        },
                        "response_code": "PASSTHRU",
                        "answers": {
                          "data": "18.185.74.46"
                        }
                      }
                    }
                },
                "5": {
                    "type": "user-account",
                    "user_id": "rdp"
                }
            },
            "x_infoblox_dns_event": {
                "severity": "HIGH",
                "tclass": "APT",
                "threat_indicator": "total-update.com",
                "tproperty": "MalwareC2",
                "policy_name": "DFND",
                "os_version": "Windows 10 Enterprise",
                "network": "BloxOne Endpoint",
                "user_ref": "5",
                "src_ip_ref": "0",
                "category": "",
                "confidence": "HIGH",
                "country": "unknown",
                "device": "DESKTOP-VT5P2QT",
                "dhcp_fingerprint": "",
                "event_time": "2021-06-05T10:11:05.000Z",
                "feed_name": "Base",
                "feed_type": "FQDN"
            },
            "first_observed": "2021-05-18T03:56:52.801Z",
            "last_observed": "2021-05-18T03:56:52.801Z",
            "number_observed": 1
        }
    ]
}
```

##### dossierData

```json
```

##### endpointActivityData

```json
{
    "type": "bundle",
    "id": "bundle--9a76f81f-f2d5-4d3e-92dd-5359cf77b957",
    "spec_version": "2.0",
    "objects": [
        {
            "id": "identity--b1898903-f26b-43fb-982e-4b35cb35f060",
            "name": "name",
            "type": "identity",
            "identity_class": "individual",
            "created": "2021-06-28T08:58:24.239Z",
            "modified": "2021-06-28T08:58:24.239Z"
        },
        {
            "id": "observed-data--ab261396-0c22-468b-8bfc-53becb3223fc",
            "type": "observed-data",
            "created_by_ref": "identity--b1898903-f26b-43fb-982e-4b35cb35f060",
            "created": "2021-06-28T08:58:29.505Z",
            "modified": "2021-06-28T08:58:29.505Z",
            "objects": {
                "0": {
                    "type": "ipv4-addr",
                    "value": "10.10.58.51"
                },
                "1": {
                    "type": "ipv4-addr",
                    "value": "127.0.0.1"
                },
                "2": {
                    "type": "ipv6-addr",
                    "value": "fe80::f8e9:b28:a7a5:4b89"
                },
                "3": {
                    "type": "ipv6-addr",
                    "value": "::1"
                },
                "4": {
                    "type": "user-account",
                    "account_login": [
                        "sam"
                    ]
                },
                "5": {
                    "type": "process",
                    "command_line": "c:\\windows\\system32\\ping.exe 127.0.0.1 -n 10 ",
                    "binary_ref": "6"
                },
                "6": {
                    "type": "file",
                    "name": "ping.exe",
                    "parent_directory_ref": "7",
                    "hashes": {
                        "SHA-1": "02dba0a590629deb688b743173496ce664c535ff"
                    }
                },
                "7": {
                    "type": "directory",
                    "path": "c:\\windows\\system32"
                },
                "8": {
                    "type": "process",
                    "command_line": "c:\\windows\\system32\\cmd.exe",
                    "binary_ref": "9"
                },
                "9": {
                    "type": "file",
                    "name": "cmd.exe",
                    "parent_directory_ref": "10",
                    "hashes": {
                        "SHA-1": "3ce71813199abae99348f61f0caa34e2574f831c"
                    }
                },
                "10": {
                    "type": "directory",
                    "path": "c:\\windows\\system32"
                },
                "11": {
                    "type": "ipv4-addr",
                    "value": "127.0.0.1"
                }
            },
            "first_observed": "2021-05-18T03:56:52.801Z",
            "last_observed": "2021-05-18T03:56:52.801Z",
            "number_observed": 1
        }
    ]
}
```

##### messageActivityData

```json
{
  "type": "bundle",
  "id": "bundle--9ab37dda-9c99-48fe-91ab-be55691b0f9d",
  "spec_version": "2.0",
  "objects": [
    {
      "id": "identity--966c214b-0976-443a-8c1a-bd0684d9c9d6",
      "name": "name",
      "type": "identity",
      "identity_class": "individual",
      "created": "2021-06-28T09:11:32.022Z",
      "modified": "2021-06-28T09:11:32.022Z"
    },
    {
      "id": "observed-data--da94602d-78ca-4ac0-a52d-1ff0cb99d796",
      "type": "observed-data",
      "created_by_ref": "identity--966c214b-0976-443a-8c1a-bd0684d9c9d6",
      "created": "2021-06-28T09:11:36.775Z",
      "modified": "2021-06-28T09:11:36.775Z",
      "objects": {
        "0": {
          "type": "email-addr",
          "value": "o365mc@aaa.bbb.com"
        },
        "1": {
          "type": "email-message",
          "sender_ref": "0",
          "is_multipart": true,
          "to_refs": [
            "2"
          ],
          "subject": "Message Center Major Change Update Notification",
          "date": "2021-04-13T08:30:56.000Z",
          "additional_header_fields": {
            "Return-Path": "o365mc@aaa.bbb.com",
            "Authentication-Results": "spf=pass (sender IP is 207.46.55.222) smtp.mailfrom=aaa.bbb.com;compauth=pass reason=100",
            "Message-ID": "<89ca86fa053847de8bd45aeb658a4d36-JFBVALKQOJXWILKNK4YVA7CPGM3DKTLFONZWCZ3FINSW45D=@aaa.bbb.com>"
          }
        },
        "2": {
          "type": "email-addr",
          "value": "xdrwbtest@aaa.bbb.com"
        },
        "3": {
          "type": "domain-name",
          "value": "aaa.bbb.com"
        },
        "4": {
          "type": "ipv4-addr",
          "value": "207.46.55.222"
        },
        "5": {
          "type": "network-traffic",
          "src_ref": "4",
          "protocols": [
            "tcp"
          ]
        }
      },
      "first_observed": "2021-04-13T08:30:56.000Z",
      "last_observed": "2021-04-13T08:30:56.000Z",
      "number_observed": 1
    }
  ]
}
```

### Limitations

#### messageActivityData

* Does not support `NOT` operator.
* Does not support using `AND` and `OR` operators simultaneously.
* Does not support using multiple criteria in one field.