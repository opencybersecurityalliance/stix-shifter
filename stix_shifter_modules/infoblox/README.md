# Infoblox

## Supported STIX Mappings

See the [table of mappings](infoblox_supported_stix.md) for the STIX objects and operators supported by this connector.

### Dialects

* tideDbData
* dnsEventData
* dossierData

### Infoblox API Endpoints

Ping Endpoint: `https://<hostname>:<port>/tide/api/data/threats/state`

Result (tideDbData) Endpoint: `https://<hostname>:<port>/tide/api/data/threats/state`

Result (dnsEventData) Endpoint: `https://<hostname>:<port>/api/dnsdata/v2/dns_event`

Result (dossierData) Endpoint: `https://<hostname>:<port>/tide/api/services/intel/lookup/indicator`

##### Reference

[Infoblox API TIDE Documentation](https://docs.infoblox.com/display/BloxOneThreatDefense/Threat+API+Guide)
[Infoblox API DNS Event Documentation](https://docs.infoblox.com/display/BloxOneThreatDefense/DNS+Event)
[Infoblox API Dossier Documentation](https://docs.infoblox.com/display/BloxOneThreatDefense/Appendix+B%3A+Dossier+API+Reference)


### Format for calling stix-shifter from the command line:

python main.py `<translator_module>` `<query or result>` `<STIX identity object>` `<data>`

### Pattern expression with STIX attributes

#### STIX translate query
```shell
python main.py translate infoblox query '{}' "[ipv4-addr:value = '127.0.0.1'] START t'2021-06-01T08:43:10Z' STOP t'2021-08-31T10:43:10Z'" ;
```
#### STIX translate query - output
```json
{
    "queries": [
        "{\"offset\": 0, \"query\": \"from_date=2021-06-01T08:43:10.000Z&to_date=2021-08-31T10:43:10.000Z&ip=127.0.0.1\", \"threat_type\": \"ip\", \"source\": \"tideDbData\"}",
        "{\"offset\": 0, \"query\": \"t0=1622536990&t1=1630406590&qip=127.0.0.1\", \"source\": \"dnsEventData\"}",
        "{\"offset\": 0, \"query\": \"value=127.0.0.1\", \"threat_type\": \"ip\", \"source\": \"dossierData\"}"
    ]
}

```
#### STIX transmit query
```shell
export SS_CONNECTION='{"host":"xxx","port":443,"options":{"timeout":20}}'
export SS_AUTH='{"auth":{"token":"xxx"}}'

python main.py transmit infoblox:dnsEventData ${SS_CONNECTION} ${SS_AUTH} query '{"offset": 0, "query": "t0=1622536990&t1=1630406590&qip=127.0.0.1", "source": "dnsEventData"}'
```

#### STIX transmit query - output
```json
{
    "success": true,
    "search_id": "{\"offset\": 0, \"query\": \"t0=1622536990&t1=1630406590&qip=127.0.0.1\", \"source\": \"dnsEventData\"}"
}
```

#### STIX transmit results
```shell
export SS_CONNECTION='{"host":"xxx","port":443,"options":{"timeout":20}}'
export SS_AUTH='{"auth":{"token":"xxx"}}'

python main.py transmit infoblox:dnsEventData ${SS_CONNECTION} ${SS_AUTH} results '{"offset": 0, "query": "t0=1622536990&t1=1630406590&qip=127.0.0.1", "source": "dnsEventData"}' 0 5
```

#### STIX transmit results - output
```json
{
    "success": true,
    "data": [
        {
            "dnsEventData": {
                "category": "Streaming Media",
                "confidence": "",
                "country": "unknown",
                "device": "Device Name",
                "dhcp_fingerprint": "",
                "event_time": "2021-08-03T04:43:51.000Z",
                "feed_name": "CAT_Streaming Media",
                "feed_type": "FQDN",
                "mac_address": "00:00:00:00:00:00",
                "network": "Network Name",
                "os_version": "Windows 10 Enterprise",
                "policy_name": "Sentinel-Security-Policy",
                "private_ip": "1.1.1.1",
                "qip": "127.0.0.1",
                "qname": "example.com.",
                "qtype": "A",
                "rcode": "REDIRECT",
                "rdata": "1.1.1.1",
                "rip": "",
                "severity": "",
                "tclass": "",
                "threat_indicator": "CAT",
                "tproperty": "",
                "user": "rdp"
            }
        }
    ]
}
```

#### STIX execute
```shell
export SS_DATA_SOURCE='{"type": "identity", "id": "xxx", "name": "Infoblox", "identity_class": "events"}'
export SS_CONNECTION='{"host":"xxx","port":443,"options":{"timeout":20}}'
export SS_AUTH='{"auth":{"token":"xxx"}}'

python3 main.py execute infoblox:dnsEventData infoblox:dnsEventData $SS_DATA_SOURCE $SS_CONNECTION $SS_AUTH "[ipv4-addr:value = '208.50.179.13'] START t'2021-06-27T09:00:10Z' STOP t'2021-06-29T10:43:10Z'"
```

#### STIX execute - output
```json
{
    "type": "bundle",
    "id": "bundle--97b0f001-0022-4859-a6b6-06c748c02074",
    "spec_version": "2.0",
    "objects": [
        {
            "type": "identity",
            "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
            "name": "Infoblox",
            "identity_class": "events"
        },
        {
            "id": "observed-data--312451ed-26ab-4cd8-9fa5-54d018b0c0f5",
            "type": "observed-data",
            "created_by_ref": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
            "created": "2021-08-03T04:52:23.717Z",
            "modified": "2021-08-03T04:52:23.717Z",
            "objects": {
                "0": {
                    "type": "x-infoblox-dns-event",
                    "category": "Internet Services",
                    "country": "US",
                    "device": "Device Name",
                    "feed_name": "CAT_Internet Services",
                    "feed_type": "FQDN",
                    "network": "Network Name",
                    "os_version": "Windows 10 Enterprise",
                    "policy_name": "DFND",
                    "src_ip_ref": "3",
                    "threat_indicator": "CAT",
                    "user_ref": "6"
                },
                "1": {
                    "type": "mac-addr",
                    "value": "00:00:00:00:00:00"
                },
                "2": {
                    "type": "ipv4-addr",
                    "resolves_to_refs": [
                        "1"
                    ],
                    "value": "1.1.1.1"
                },
                "3": {
                    "type": "ipv4-addr",
                    "value": "127.0.0.1"
                },
                "4": {
                    "type": "network-traffic",
                    "src_ref": "3",
                    "protocols": [
                        "domain"
                    ],
                    "extensions": {
                        "dns-ext": {
                            "question": {
                                "domain_ref": "5"
                            },
                            "type": "A",
                            "response_code": "PASSTHRU",
                            "answers": {
                                "data": "1.1.1.1"
                            }
                        }
                    }
                },
                "5": {
                    "type": "domain-name",
                    "value": "example.com"
                },
                "6": {
                    "type": "user-account",
                    "user_id": "rdp"
                }
            },
            "first_observed": "2021-06-29T10:41:46.000Z",
            "last_observed": "2021-06-29T10:41:46.000Z",
            "number_observed": 1
        }
    ]
}

```

#### STIX ping
```json
export SS_AUTH='{"auth":{"token":"xxx"}}'
python3 main.py transmit infoblox '{"host":"csp.infoblox.com"}' $SS_AUTH ping
{
    "success": true
}
```

#### STIX additional translate queries
```
# translate
python main.py translate infoblox query '{}' "[ipv4-addr:value = '127.0.0.1'] START t'2021-06-01T08:43:10Z' STOP t'2021-08-31T10:43:10Z'" ;

# translate tideDbData
python main.py translate infoblox:tideDbData query '{}' "[ipv4-addr:value = '1.1.1.1'] START t'2021-08-07T11:16:30.330Z' STOP t'2021-08-09T11:16:30.330Z'" ;
python main.py translate infoblox:tideDbData query '{}' "[x-infoblox-threat:id = '00000000-1111-2222-3333-444444444444'] START t'2021-08-07T11:16:30.330Z' STOP t'2021-08-09T11:16:30.330Z'" ;
python main.py translate infoblox:tideDbData query '{}' "[x-infoblox-threat:host_name = 'example.host.com']"
python main.py translate infoblox:tideDbData query '{}' "[x-infoblox-threat:url = 'https://example.host.com/payload.tar' START t'2021-02-08T14:07:38.859Z' STOP t'2021-02-10T14:07:38.859Z'"
python main.py translate infoblox:tideDbData query '{}' "[domain-name:value = 'example.host.com' AND x-infoblox-threat:threat_type = 'url'] START t'2021-02-08T14:07:38.859Z' STOP t'2021-02-10T14:07:38.859Z'";
python main.py translate infoblox:tideDbData query '{}' "[x-infoblox-threat:top_level_domain = 'host.com' AND x-infoblox-threat:threat_type = 'url'] START t'2021-02-08T14:07:38.859Z' STOP t'2021-02-10T14:07:38.859Z'";
python main.py translate infoblox:tideDbData query '{}' "[x-infoblox-threat:profile = 'IID' AND x-infoblox-threat:threat_type = 'url'] START t'2021-02-08T14:07:38.859Z' STOP t'2021-02-10T14:07:38.859Z'";
python main.py translate infoblox:tideDbData query '{}' "[x-infoblox-threat:property = 'Proxy_DNST' AND x-infoblox-threat:threat_type = 'host']";
python main.py translate infoblox:tideDbData query '{}' "[x-infoblox-threat:threat_class = 'MalwareC2' AND x-infoblox-threat:threat_type = 'host']";
python main.py translate infoblox:tideDbData query '{}' "[x-infoblox-threat:threat_level = '100' AND x-infoblox-threat:threat_type = 'host']";
python main.py translate infoblox:tideDbData query '{}' "[x-infoblox-threat:target = 'target' AND x-infoblox-threat:threat_type = 'host'] START t'2021-08-08T05:55:36.341Z' STOP t'2021-08-08T07:55:36.341Z'";
python main.py translate infoblox:tideDbData query '{}' "[x-infoblox-threat:expiration = '2021-08-22T06:55:36.989Z' AND x-infoblox-threat:threat_type = 'host']";
python main.py translate infoblox:tideDbData query '{}' "[x-infoblox-threat:derivative = 'false' AND x-infoblox-threat:threat_type = 'host']";
python main.py translate infoblox:tideDbData query '{}' "[x-infoblox-threat:dga = 'true' AND x-infoblox-threat:threat_type = 'host']";
python main.py translate infoblox:tideDbData query '{}' "[x-infoblox-threat:active = 'true' AND x-infoblox-threat:threat_type = 'host']";
python main.py translate infoblox:tideDbData query '{}' "[x-infoblox-threat:x_infoblox_confidence = '0' AND x-infoblox-threat:threat_type = 'host']";
python main.py translate infoblox:tideDbData query '{}' "[x-infoblox-threat:imported > '2021-08-08T08:08:06.00Z' AND x-infoblox-threat:imported < '2021-08-08T08:08:07.00Z' AND x-infoblox-threat:threat_type = 'host']";
python main.py translate infoblox:tideDbData query '{}' "[x-infoblox-threat:hash = 'abcdef' AND x-infoblox-threat:threat_type = 'host']";
python main.py translate infoblox:tideDbData query '{}' "[x-infoblox-threat:profile LIKE 'searchText' AND x-infoblox-threat:threat_type = 'host']";
python main.py translate infoblox:tideDbData query '{}' "[x-infoblox-threat:origin LIKE 'searchText' AND x-infoblox-threat:threat_type = 'host']";
python main.py translate infoblox:tideDbData query '{}' "[x-infoblox-threat:host_name LIKE 'searchText' AND x-infoblox-threat:threat_type = 'host']";
python main.py translate infoblox:tideDbData query '{}' "[x-infoblox-threat:url LIKE 'searchText']";
python main.py translate infoblox:tideDbData query '{}' "[ipv4-addr:value LIKE 'searchText']";
python main.py translate infoblox:tideDbData query '{}' "[domain-name:value LIKE 'searchText' AND x-infoblox-threat:threat_type = 'host']";
python main.py translate infoblox:tideDbData query '{}' "[x-infoblox-threat:property LIKE 'searchText' AND x-infoblox-threat:threat_type = 'host']";
python main.py translate infoblox:tideDbData query '{}' "[x-infoblox-threat:threat_class LIKE 'searchText' AND x-infoblox-threat:threat_type = 'host']";
python main.py translate infoblox:tideDbData query '{}' "[x-infoblox-threat:target LIKE 'searchText' AND x-infoblox-threat:threat_type = 'host']";
python main.py translate infoblox:tideDbData query '{}' "[email-addr:value = 'name@email.com']";
python main.py translate infoblox:tideDbData query '{}' "[x-infoblox-threat:domain_ref.value = 'example.host.com' AND x-infoblox-threat:threat_type = 'url'] START t'2021-02-08T14:07:38.859Z' STOP t'2021-02-10T14:07:38.859Z'";
python main.py translate infoblox:tideDbData query '{}' "[x-infoblox-threat:email_ref.value = 'name@email.com']";
python main.py translate infoblox:tideDbData query '{}' "[x-infoblox-threat:ip_ref.value = '1.1.1.1']";
python main.py translate infoblox:tideDbData query '{}' "[x-infoblox-threat:origin = 'origin' AND x-infoblox-threat:threat_type = 'host']";


# translate dnsEventData
python main.py translate infoblox:dnsEventData query '{}' "[ipv4-addr:value = '127.0.0.1'] START t'2020-06-01T08:43:10Z' STOP t'2020-08-31T10:43:10Z'" ;
python main.py translate infoblox:dnsEventData query '{}' "[ipv4-addr:value = '127.0.0.1']" ;
python main.py translate infoblox:dnsEventData query '{}' "[x-infoblox-dns-event:network = 'Network Name']" ;
python main.py translate infoblox:dnsEventData query '{}' "[domain-name:value = 'example.com']" ;
python main.py translate infoblox:dnsEventData query '{}' "[x-infoblox-dns-event:policy_name = 'DFND']" ;
python main.py translate infoblox:dnsEventData query '{}' "[x-infoblox-dns-event:x_infoblox_severity = 'HIGH']" ;
python main.py translate infoblox:dnsEventData query '{}' "[x-infoblox-dns-event:threat_class = 'APT']" ;
python main.py translate infoblox:dnsEventData query '{}' "[network-traffic:extensions.'dns-ext'.question.domain_ref.value = 'example.com']" ;
python main.py translate infoblox:dnsEventData query '{}' "[network-traffic:src_ref.value = '127.0.0.1']" ;
python main.py translate infoblox:dnsEventData query '{}' "[(domain-name:value = 'example.com' AND x-infoblox-dns-event:policy_name = 'DFND') AND network-traffic:src_ref.value = '127.0.0.1']" ;


# translate dossierData
python main.py translate infoblox:dossierData query '{}' "[domain-name:value = 'example.com']" ;
python main.py translate infoblox:dossierData query '{}' "[ipv4-addr:value = '127.0.0.1']" ;
python main.py translate infoblox:dossierData query '{}' "[ipv6-addr:value = '1111:222:3333:4444:5555:6666:7777:8888']" ;
python main.py translate infoblox:dossierData query '{}' "[x-infoblox-dossier-event-result-pdns:ip_ref.value = '127.0.0.1']" ;
python main.py translate infoblox:dossierData query '{}' "[x-infoblox-dossier-event-result-pdns:hostname_ref.value = 'example.com']" ;
```
#### Transmit Results Output
##### Dialect: tideDbData
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

##### Dialect: dnsEventData
```json
{
    "success": true,
    "data": [
        {
            "dnsEventData": {
                "category": "Streaming Media",
                "confidence": "",
                "country": "unknown",
                "device": "Device Name",
                "dhcp_fingerprint": "",
                "event_time": "2021-08-03T04:43:51.000Z",
                "feed_name": "CAT_Streaming Media",
                "feed_type": "FQDN",
                "mac_address": "00:00:00:00:00:00",
                "network": "Network Name",
                "os_version": "Windows 10 Enterprise",
                "policy_name": "Sentinel-Security-Policy",
                "private_ip": "1.1.1.1",
                "qip": "127.0.0.1",
                "qname": "example.com.",
                "qtype": "A",
                "rcode": "REDIRECT",
                "rdata": "1.1.1.1",
                "rip": "",
                "severity": "",
                "tclass": "",
                "threat_indicator": "CAT",
                "tproperty": "",
                "user": "rdp"
            }
        }
    ]
}
```
##### Dialect: dossierData
```json
{
    "success": true,
    "data": [
        {
            "dossierData": {
                "job": {
                    "create_time": "2021-08-03T05:00:16.634Z"
                },
                "results": [
                    {
                        "data": {
                            "items": [
                                {
                                    "Domain": "",
                                    "Hostname": "example.com",
                                    "IP": "127.0.0.1",
                                    "Last_Seen": 1624531404,
                                    "NameServer": "",
                                    "Record_Type": "A"
                                }
                            ]
                        }
                    }
                ]
            }
        }
    ]
}
```

### Response to STIX object (STIX attributes)

#### STIX Observable Output

##### Dialect: tideDbData
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
                    "received": "2021-04-14T15:07:18.592Z",
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

##### Dialect: dnsEventData
```json
{
    "type": "bundle",
    "id": "bundle--6366eadb-cd6c-442b-9563-b240dc216fd6",
    "spec_version": "2.0",
    "objects": [
        {
            "type": "identity",
            "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
            "name": "Infoblox",
            "identity_class": "events"
        },
        {
            "id": "observed-data--c9b86145-7359-48ca-add5-0dd0afc1eb93",
            "type": "observed-data",
            "created_by_ref": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
            "created": "2021-08-03T05:05:37.391Z",
            "modified": "2021-08-03T05:05:37.391Z",
            "objects": {
                "0": {
                    "type": "x-infoblox-dns-event",
                    "x_infoblox_confidence": "HIGH",
                    "country": "unknown",
                    "device": "Device Name",
                    "feed_name": "Base",
                    "feed_type": "FQDN",
                    "network": "Network Name",
                    "os_version": "Windows 10 Enterprise",
                    "policy_name": "DFND",
                    "src_ip_ref": "3",
                    "x_infoblox_severity": "HIGH",
                    "threat_class": "APT",
                    "threat_indicator": "indicator",
                    "threat_property": "MalwareDownload",
                    "user_ref": "6",
                    "category": "category",
                    "dhcp_fingerprint": "fingerprint"
                },
                "1": {
                    "type": "mac-addr",
                    "value": "00:00:00:00:00:00"
                },
                "2": {
                    "type": "ipv4-addr",
                    "resolves_to_refs": [
                        "1"
                    ],
                    "value": "1.1.1.1"
                },
                "3": {
                    "type": "ipv4-addr",
                    "value": "127.0.0.1"
                },
                "4": {
                    "type": "network-traffic",
                    "src_ref": "3",
                    "protocols": [
                        "domain"
                    ],
                    "extensions": {
                        "dns-ext": {
                            "question": {
                                "domain_ref": "5"
                            },
                            "type": "A",
                            "response_code": "PASSTHRU",
                            "answers": {
                              "data": "1.1.1.1"
                            }
                        }
                    }
                },
                "5": {
                    "type": "domain-name",
                    "value": "example.com"
                },
                "6": {
                    "type": "user-account",
                    "user_id": "rdp"
                }
            },
            "first_observed": "2021-06-29T10:41:02.000Z",
            "last_observed": "2021-06-29T10:41:02.000Z",
            "number_observed": 1
        }
    ]
}
```

##### Dialect: dossierData
```json
{
    "type": "bundle",
    "id": "bundle--6a1e31f5-a5ee-40df-95ae-789e183f312e",
    "spec_version": "2.0",
    "objects": [
        {
            "type": "identity",
            "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
            "name": "Infoblox",
            "identity_class": "events"
        },
        {
            "id": "observed-data--1242a347-730a-4f93-96f1-2a7c1b8048b2",
            "type": "observed-data",
            "created_by_ref": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
            "created": "2021-08-03T05:03:36.715Z",
            "modified": "2021-08-03T05:03:36.715Z",
            "objects": {
                "0": {
                    "type": "domain-name",
                    "value": "example.com"
                },
                "1": {
                    "type": "x-infoblox-dossier-event-result-pdns",
                    "hostname_ref": "0",
                    "ip_ref": "2",
                    "last_seen": 1624531404,
                    "record_type": "A"
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "127.0.0.1"
                }
            },
            "first_observed": "2021-08-03T05:03:35.548Z",
            "last_observed": "2021-08-03T05:03:35.548Z",
            "number_observed": 1
        }
    ]
}
```



### Limitations
* Does not support `NOT` operator.
* Multiple individual queries can be produced from a single STIX Pattern, following examples:
- - Multiple Observation Expressions, ie [ipv4-addr:value = '1.1.1.1'] AND [domain-name:value = 'domain.com']
- - Patterns using `OR` operator, ie [ipv4-addr:value = '1.1.1.1' OR domain-name:value = 'domain.com']
- - Patterns with multiple criteria for the same field, ie [ipv4-addr:value = '1.1.1.1' AND ipv4-addr:value = '2.2.2.2']


### Recommendations
* To resolve timeout issues with the cli or proxy, you can increase the timeout on the proxy and on the module:
```bash
export SS_CONFIG='{"options": {"proxy_host": "192.168.2.15", "proxy_port": 6700, "timeout": 59, "destination": {"connection": {"options": {"timeout": 59}, "host": "csp.infoblox.com", "type": "infoblox"}, "configuration": {"auth": { "token": "xxx"} } } }}'
```
