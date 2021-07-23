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

### Limitations
