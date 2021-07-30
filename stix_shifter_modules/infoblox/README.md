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
{
  "threat": [
    {
      "id": "1af2936f-9d33-11eb-8943-6962d4bdf9de",
      "type": "HOST",
      "host": "1-lntesasanpaolo-portaleweb.xyz",
      "domain": "1-lntesasanpaolo-portaleweb.xyz",
      "tld": "xyz",
      "profile": "IID",
      "property": "Phishing_Generic",
      "class": "Phishing",
      "threat_level": 100,
      "confidence": 100,
      "detected": "2021-04-14T15:04:26.116Z",
      "received": "2021-04-14T15:07:18.592Z",
      "imported": "2021-04-14T15:07:18.592Z",
      "expiration": "2022-04-14T15:04:26.116Z",
      "dga": false,
      "up": true,
      "batch_id": "1af24549-9d33-11eb-8943-6962d4bdf9de",
      "threat_score": 6,
      "threat_score_rating": "Medium",
      "threat_score_vector": "TSIS:1.0/AV:N/AC:L/PR:L/UI:R/EX:H/MOD:N/AVL:N/CI:N/ASN:N/TLD:H/DOP:N/P:F",
      "confidence_score": 8.2,
      "confidence_score_rating": "High",
      "confidence_score_vector": "COSIS:1.0/SR:H/POP:N/TLD:H/CP:F",
      "risk_score": 7.9,
      "risk_score_rating": "High",
      "risk_score_vector": "RSIS:1.0/TSS:M/TLD:H/CVSS:L/EX:H/MOD:N/AVL:N/T:M/DT:L",
      "extended": {
        "cyberint_guid": "dadbdde3eaf7fd97bae0bdec8c6ceb07"
      }
    }
  ],
  "record_count": 1
}
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

##### dossierData - pdns

```json
{
  "status": "success",
  "job_id": "37918a72-1588-4d25-b7e9-578419e5bb00",
  "job": {
    "id": "37918a72-1588-4d25-b7e9-578419e5bb00",
    "state": "completed",
    "status": "success",
    "create_ts": 1627170288716,
    "create_time": "2021-07-24T23:44:48.716Z",
    "request_ttl": 0,
    "result_ttl": 3600,
    "completed_tasks": [
      "a5183e5d-788d-41d0-8fc0-6264fdb83d04"
    ],
    "org": "BLOXINT00000000264",
    "user": "user.service.03283b68-bceb-49c6-b706-2a4ec650067f@infoblox.invalid",
    "tasks_tbc": 0
  },
  "tasks": {
    "a5183e5d-788d-41d0-8fc0-6264fdb83d04": {
      "id": "a5183e5d-788d-41d0-8fc0-6264fdb83d04",
      "state": "completed",
      "status": "success",
      "create_ts": 1627170288716,
      "create_time": "2021-07-24T23:44:48.716Z",
      "start_ts": 1627170289717,
      "start_time": "2021-07-24T23:44:49.717Z",
      "end_ts": 1627170290087,
      "end_time": "2021-07-24T23:44:50.087Z",
      "params": {
        "type": "host",
        "target": "vm1988182.11ssd.had.wf",
        "source": "pdns"
      },
      "options": {},
      "results": null,
      "rl": false
    }
  },
  "results": [
    {
      "task_id": "a5183e5d-788d-41d0-8fc0-6264fdb83d04",
      "params": {
        "type": "host",
        "target": "vm1988182.11ssd.had.wf",
        "source": "pdns"
      },
      "status": "success",
      "time": 369,
      "v": "3.0.0",
      "data": {
        "duration": 369905951,
        "items": [
          {
            "Domain": "",
            "Hostname": "vm1988182.11ssd.had.wf",
            "IP": "185.203.242.211",
            "Last_Seen": 1627160591,
            "NameServer": "",
            "Record_Type": "A"
          }
        ],
        "status": 200,
        "total_results": 1
      }
    }
  ]
}
```

### Infoblox response to STIX object (STIX attributes)

#### STIX observable output

##### tideDbData

```json
{
    "type": "bundle",
    "id": "bundle--9a76f81f-f2d5-4d3e-92dd-5359cf77b957",
    "spec_version": "2.0",
    "objects": [
        {
            "id": "identity--b1898903-f26b-43fb-982e-4b35cb35f060",
            "name": "Infoblox",
            "type": "identity",
            "identity_class": "individual",
            "created": "2021-06-28T08:58:24.239Z",
            "modified": "2021-06-28T08:58:24.239Z"
        },
        {
            "id": "observed-data--ab261396-0c22-468b-8bfc-53becb3223fc",
            "type": "observed-data",
            "created_by_ref": "identity--b1898903-f26b-43fb-982e-4b35cb35f060",
            "created": "2021-07-20T18:06:38.598Z",
            "modified": "2021-07-20T18:06:38.598Z",
            "objects": {
                "0": {
                    "type": "x-infoblox-threat",
                    "threat_class": "Policy",
                    "x_infoblox_confidence": 100,
                    "dga": false,
                    "domain_ref": "1",
                    "expiration": "2022-04-14T15:04:26.116Z",
                    "host_name": "1-lntesasanpaolo-portaleweb.xyz",
                    "imported": "2021-04-14T15:07:18.592Z",
                    "profile": "IID",
                    "property": "Phishing_Generic",
                    "threat_level": 100,
                    "top_level_domain": "xyz",
                    "threat_type": "HOST",
                    "active": true
                },
                "1": {
                    "type": "domain-name",
                    "value": "1-lntesasanpaolo-portaleweb.xyz"
                }
            },
            "first_observed": "2021-07-20T18:01:56.645Z",
            "last_observed": "2021-07-20T18:01:56.645Z",
            "number_observed": 1
        }
    ]
}
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
            "name": "Infoblox",
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
                    "value": "total-update.com"
                },
                "4": {
                    "type": "network-traffic",
                    "protocols": [
                       "domain"
                    ],
                    "src_ref": "2",
                    "extensions": {
                      "dns-ext": {
                        "question": {
                          "domain_ref": "3"
                        },
                        "type": "A",
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
                },
                "6": {
                    "type": "x-infoblox-dns-event",
                    "user_ref": "5",
                    "src_ip_ref": "2",
                    "x_infoblox_severity": "HIGH",
                    "threat_class": "APT",
                    "threat_indicator": "total-update.com",
                    "threat_property": "MalwareC2",
                    "policy_name": "DFND",
                    "os_version": "Windows 10 Enterprise",
                    "network": "BloxOne Endpoint",
                    "category": "",
                    "x_infoblox_confidence": "HIGH",
                    "country": "unknown",
                    "device": "DESKTOP-VT5P2QT",
                    "dhcp_fingerprint": "",
                    "feed_name": "Base",
                    "feed_type": "FQDN"
                }
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
{
    "type": "bundle",
    "id": "bundle--9a76f81f-f2d5-4d3e-92dd-5359cf77b957",
    "spec_version": "2.0",
    "objects": [
        {
            "id": "identity--b1898903-f26b-43fb-982e-4b35cb35f060",
            "name": "Infoblox",
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
                    "type": "domain-name",
                    "value": "vm1988182.11ssd.had.wf"
                },
                "1": {
                    "type": "ipv4-addr",
                    "value": "185.203.242.211"
                },
                "2": {
                    "type": "x-infoblox-dossier-event-result-pdns",
                    "hostname_ref": "0",
                    "ip_ref": "1",
                    "last_seen": 1627160591,
                    "record_type": "A"
                }
            },
            "first_observed": "2021-05-18T03:56:52.801Z",
            "last_observed": "2021-05-18T03:56:52.801Z",
            "number_observed": 1
        }
    ]
}
```

### Limitations
