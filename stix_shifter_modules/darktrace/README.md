# Darktrace Connector

**Table of Contents**

- [Darktrace API Endpoints](#darktrace-api-endpoints)
- [Pattern expression with STIX attributes - Single Observation](#single-observation)
- [Pattern expression with STIX attributes - Multiple Observation](#multiple-observation)
- [Pattern expression with STIX attributes - Execute Query](#stix-execute-query)
- [Pattern expression with STIX attributes - Ping Query](#stix-ping-query)
- [Considerations](#considerations)
- [Observations](#observations)

### Darktrace API Endpoints

   |Connector Method|Darktrace API Endpoint| Method
   | ----           |   ------              | -----|
   |Query Endpoint|https://\<your server\>/advancedsearch/api/search/|GET
###Format for calling stix-shifter from the command line
python main.py `<translator_module>` `<query or result>` `<STIX identity object>` `<data>`

### Pattern expression with STIX attributes

### Single Observation

####STIX Translate query
```shell
translate darktrace query '{}' "[ipv4-addr:value = '0.0.0.0'] START t'2022-03-21T11:00:00.000Z' STOP t'2022-03-22T11:05:00.000Z'"
```
#### STIX Translate query - output
```json
{
    "queries": [
        {
            "search": "((@fields.source_ip:\"0.0.0.0\" OR @fields.dest_ip:\"0.0.0.0\" OR @fields.src:\"0.0.0.0\" OR @fields.dst:\"0.0.0.0\" OR @fields.ip:\"0.0.0.0\") AND (@fields.epochdate :>1647860400.0 AND @fields.epochdate :<1647947100.0))",
            "fields": [],
            "timeframe": "custom",
            "time": {
                "from": "2022-03-21T11:00:00.000000Z",
                "to": "2022-03-22T11:05:00.000000Z"
            },
            "size": 10000
        }
    ]
}
```
#### STIX Transmit query

```shell
transmit
darktrace
"{\"host\":\"xx.xx.xx\"}"
"{\"auth\":{\"private_token\": \"xxxxx\", \"public_token\": \"xxxxx\"}}"
results
"{\"search\":\"((@fields.source_ip:\\"0.0.0.0\\" OR @fields.dest_ip:\\"0.0.0.0\\" OR @fields.src:\\"0.0.0.0\\" OR @fields.dst:\\"0.0.0.0\\" OR @fields.ip:\\"0.0.0.0\\") AND (@fields.epochdate :>1647860400.0 AND @fields.epochdate :<1647946800.0))\",\"fields\":[],\"timeframe\":\"custom\",\"time\":{\"from\":\"2022-03-21T11:00:00.000000Z\",\"to\":\"2022-03-22T11:05:00.000000Z\"},\"size\":10000}"
0 2
```

#### STIX Transmit query - output
```json
{
    "success": true,
    "data": [
        {
            "conn": { "epochdate": 1647946686.995818, "source_port": 24178, "source_ip": "0.0.0.0", "dest_ip": "0.0.0.0", "uid": "CEfQ2a2ObXcyNJUvEk01", "dest_port": 3389, "proto": "null" },
            "x509": { "epochdate": 1647946686.995818, "source_port": 24178, "certificate_not_valid_after": 1660562534, "fid": "FxWXXc1uH1zQNF66T701", "certificate_key_type": "rsa", "certificate_sig_alg": "sha256WithRSAEncryption", "certificate_key_alg": "rsaEncryption", "certificate_subject": "CN=EC2AMAZ-2GNPPAQ", "source_ip": "0.0.0.0", "certificate_exponent": "65537", "certificate_key_length": 2048, "dest_ip": "0.0.0.0", "certificate_not_valid_before": 1644751334, "uid": "CEfQ2a2ObXcyNJUvEk01", "dest_port": 3389, "certificate_version": 3, "certificate_serial": "76FDB38B8D5AA88844250EFE0EA89026", "certificate_issuer": "CN=EC2AMAZ-2GNPPAQ", "proto": "null" } },
        {
            "conn": { "epochdate": 1647946686.995818, "source_port": 24178, "dest_port": 3389, "source_ip": "0.0.0.0", "dest_ip": "0.0.0.0", "uid": "CEfQ2a2ObXcyNJUvEk01", "proto": "null" },
            "ssl": { "epochdate": 1647946686.995818, "total_client_ciphers": 28, "validation_status": "unable to get local issuer certificate", "client_hello_seen": true, "ja3_client_fingerprint": "043c543b63b895881d9abfbc320cb863", "source_port": 24178, "dest_port": 3389, "established": true, "source_ip": "0.0.0.0", "issuer": "CN=EC2AMAZ-2GNPPAQ", "cipher": "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384", "dest_ip": "0.0.0.0", "cert_chain_fuids": "FxWXXc1uH1zQNF66T701", "curve": "secp384r1", "uid": "CEfQ2a2ObXcyNJUvEk01", "version": "TLS1.2", "ja3s_server_fingerprint": "ae4edc6faf64d08308082ad26be60767", "subject": "CN=EC2AMAZ-2GNPPAQ", "proto": "null" }
        }
    ]
}
```
#### STIX Translate results

```shell
translate darktrace results
"{\"type\":\"identity\",\"id\":\"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\",\"name\":\"darktrace\",\"identity_class \":\"events\"}"
"{\"conn\":{\"epochdate\":1647946686.995818,\"source_port\":24178,\"source_ip\":\"0.0.0.0\",\"dest_ip\":\"0.0.0.0\",\"uid\":\"CEfQ2a2ObXcyNJUvEk01\",\"dest_port\":3389,\"proto\":\"null\"},\"x509\":{\"epochdate\":1647946686.995818,\"source_port\":24178,\"certificate_not_valid_after\":1660562534,\"fid\":\"FxWXXc1uH1zQNF66T701\",\"certificate_key_type\":\"rsa\",\"certificate_sig_alg\":\"sha256WithRSAEncryption\",\"certificate_key_alg\":\"rsaEncryption\",\"certificate_subject\":\"CN=EC2AMAZ-2GNPPAQ\",\"source_ip\":\"0.0.0.0\",\"certificate_exponent\":\"65537\",\"certificate_key_length\":2048,\"dest_ip\":\"0.0.0.0\",\"certificate_not_valid_before\":1644751334,\"uid\":\"CEfQ2a2ObXcyNJUvEk01\",\"dest_port\":3389,\"certificate_version\":3,\"certificate_serial\":\"76FDB38B8D5AA88844250EFE0EA89026\",\"certificate_issuer\":\"CN=EC2AMAZ-2GNPPAQ\",\"proto\":\"null\"}},{\"conn\":{\"epochdate\":1647946686.995818,\"source_port\":24178,\"dest_port\":3389,\"source_ip\":\"0.0.0.0\",\"dest_ip\":\"0.0.0.0\",\"uid\":\"CEfQ2a2ObXcyNJUvEk01\",\"proto\":\"null\"},\"ssl\":{\"epochdate\":1647946686.995818,\"total_client_ciphers\":28,\"validation_status\":\"unable to get local issuer certificate\",\"client_hello_seen\":true,\"ja3_client_fingerprint\":\"043c543b63b895881d9abfbc320cb863\",\"source_port\":24178,\"dest_port\":3389,\"established\":true,\"source_ip\":\"0.0.0.0\",\"issuer\":\"CN=EC2AMAZ-2GNPPAQ\",\"cipher\":\"TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384\",\"dest_ip\":\"0.0.0.0\",\"cert_chain_fuids\":\"FxWXXc1uH1zQNF66T701\",\"curve\":\"secp384r1\",\"uid\":\"CEfQ2a2ObXcyNJUvEk01\",\"version\":\"TLS1.2\",\"ja3s_server_fingerprint\":\"ae4edc6faf64d08308082ad26be60767\",\"subject\":\"CN=EC2AMAZ-2GNPPAQ\",\"proto\":\"null\"}}"
"{\"stix_validator\": true}"
```

#### STIX Translate results - output
```json
{
    "type": "bundle",
    "id": "bundle--27b49396-68c0-4dc5-97ee-3acaa4cd8d44",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "darktrace",
            "identity_class ": "events"
        },
        {
            "id": "observed-data--5c33264f-21b4-4dbe-a8a1-dd96a895220b",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-07T05:24:20.208Z",
            "modified": "2022-04-07T05:24:20.208Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-03-22T11:04:31.000Z"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 11256,
                    "dst_port": 3389,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "protocols": [
                        "null"
                    ],
                    "extensions": {
                        "x-darktrace-ssl": {
                            "total_ciphers": 50,
                            "validation_status": "unable to get local issuer certificate",
                            "is_client_hello_seen": true,
                            "ja3_client_fingerprint": "75fb48a465416d66291fb52a733d4787",
                            "is_established": true,
                            "cipher_suite": "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA",
                            "cert_file_uids": "F2D8iX1YaTCWKlsoN01",
                            "elliptic_curve": "secp384r1",
                            "ssl_version": "TLS1.0",
                            "ja3s_server_fingerprint": "bcf3a836c82d12ee988005fb0c011445"
                        }
                    }
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
                },
                "3": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "2",
                        "4"
                    ],
                    "extensions": {
                        "x-darktrace-connection": {
                            "identifier": "CqQ5sRAFWzt7NRQmj01"
                        }
                    }
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "5": {
                    "type": "x509-certificate",
                    "issuer": "CN=EC2AMAZ-2GNPPAQ",
                    "subject": "CN=EC2AMAZ-2GNPPAQ"
                }
            },
            "first_observed": "2022-04-07T05:24:20.208Z",
            "last_observed": "2022-04-07T05:24:20.208Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--d92080dc-38ea-404e-8d25-62e0f2f65b43",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-07T05:24:20.219Z",
            "modified": "2022-04-07T05:24:20.219Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-03-22T11:04:31.000Z"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 11256,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "dst_port": 3389,
                    "protocols": [
                        "null"
                    ],
                    "extensions": {
                        "x-darktrace-x509": {
                            "file_id": "F2D8iX1YaTCWKlsoN01",
                            "certificate_key_type": "rsa",
                            "certificate_key_length": 2048
                        }
                    }
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
                },
                "3": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "2",
                        "4"
                    ],
                    "extensions": {
                        "x-darktrace-connection": {
                            "identifier": "CqQ5sRAFWzt7NRQmj01"
                        }
                    }
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "5": {
                    "type": "x509-certificate",
                    "validity_not_before": "2022-08-15T11:22:14.000Z",
                    "signature_algorithm": "sha256WithRSAEncryption",
                    "subject_public_key_algorithm": "rsaEncryption",
                    "subject": "CN=EC2AMAZ-2GNPPAQ",
                    "subject_public_key_exponent": 65537,
                    "validity_not_after": "2022-02-13T11:22:14.000Z",
                    "version": "3",
                    "serial_number": "76FDB38B8D5AA88844250EFE0EA89026",
                    "issuer": "CN=EC2AMAZ-2GNPPAQ"
                }
            },
            "first_observed": "2022-04-07T05:24:20.219Z",
            "last_observed": "2022-04-07T05:24:20.219Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--cd1c9052-4ee4-4d90-80e2-0cb4cb9bb92e",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-07T05:24:20.219Z",
            "modified": "2022-04-07T05:24:20.219Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-03-22T11:04:31.000Z"
                },
                "1": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
                },
                "2": {
                    "type": "network-traffic",
                    "src_ref": "1",
                    "src_port": 11256,
                    "dst_ref": "4",
                    "dst_port": 3389,
                    "protocols": [
                        "null"
                    ],
                    "extensions": {
                        "x-darktrace-rdp": {
                            "cookie": "hello",
                            "security_protocol": "HYBRID"
                        }
                    }
                },
                "3": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "1",
                        "4"
                    ],
                    "extensions": {
                        "x-darktrace-connection": {
                            "identifier": "CqQ5sRAFWzt7NRQmj01"
                        }
                    }
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                }
            },
            "first_observed": "2022-04-07T05:24:20.219Z",
            "last_observed": "2022-04-07T05:24:20.219Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--c566ab3b-beca-40fd-bcd2-088e48217f4b",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-07T05:24:20.219Z",
            "modified": "2022-04-07T05:24:20.219Z",
            "objects": {
                "0": {
                    "type": "network-traffic",
                    "src_packets": 10,
                    "extensions": {
                        "x-darktrace-conn": {
                            "originator_ttl": 108,
                            "connection_length": "00h00m03s",
                            "responder_ttl": 128,
                            "conn_state": "RSTO : Originator aborted : Connection established, originator aborted (sent a RST).",
                            "originator_asn": "AS39814 SIA IT Services",
                            "orig_country_code": "LV",
                            "history": "ShADdaR",
                            "start_ts": "2022-03-22T11:04:31.000Z",
                            "is_locally_responded": true,
                            "connection_state_desc": "Originator aborted",
                            "app_protocol": "ssl"
                        }
                    },
                    "dst_byte_count": 1613,
                    "src_port": 11256,
                    "dst_port": 3389,
                    "src_ref": "2",
                    "src_byte_count": 1170,
                    "dst_packets": 7,
                    "protocols": [
                        "tcp"
                    ],
                    "dst_ref": "4"
                },
                "1": {
                    "type": "x-oca-event",
                    "created": "2022-03-22T11:04:31.000Z"
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
                },
                "3": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "2",
                        "4"
                    ],
                    "extensions": {
                        "x-darktrace-connection": {
                            "identifier": "CqQ5sRAFWzt7NRQmj01"
                        }
                    }
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                }
            },
            "first_observed": "2022-04-07T05:24:20.219Z",
            "last_observed": "2022-04-07T05:24:20.219Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--7bfe5313-c408-4fce-83ec-b591bab38f84",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-07T05:24:20.219Z",
            "modified": "2022-04-07T05:24:20.219Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-03-22T11:04:31.000Z"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 33484,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "dst_port": 3389,
                    "protocols": [
                        "null"
                    ],
                    "extensions": {
                        "x-darktrace-x509": {
                            "file_id": "FcXA7Mkd1Wz0FwR4j01",
                            "certificate_key_type": "rsa",
                            "certificate_key_length": 2048
                        }
                    }
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
                },
                "3": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "2",
                        "4"
                    ],
                    "extensions": {
                        "x-darktrace-connection": {
                            "identifier": "CnqTYB1K38sGXvsZ0101"
                        }
                    }
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "5": {
                    "type": "x509-certificate",
                    "validity_not_before": "2022-08-15T11:22:14.000Z",
                    "signature_algorithm": "sha256WithRSAEncryption",
                    "subject_public_key_algorithm": "rsaEncryption",
                    "subject": "CN=EC2AMAZ-2GNPPAQ",
                    "subject_public_key_exponent": 65537,
                    "validity_not_after": "2022-02-13T11:22:14.000Z",
                    "version": "3",
                    "serial_number": "76FDB38B8D5AA88844250EFE0EA89026",
                    "issuer": "CN=EC2AMAZ-2GNPPAQ"
                }
            },
            "first_observed": "2022-04-07T05:24:20.219Z",
            "last_observed": "2022-04-07T05:24:20.219Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--40c5d652-6714-4975-a6fa-cf35a390e216",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-07T05:24:20.219Z",
            "modified": "2022-04-07T05:24:20.219Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-03-22T11:04:31.000Z"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 33484,
                    "dst_port": 3389,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "protocols": [
                        "null"
                    ],
                    "extensions": {
                        "x-darktrace-ssl": {
                            "total_ciphers": 28,
                            "validation_status": "unable to get local issuer certificate",
                            "is_client_hello_seen": true,
                            "ja3_client_fingerprint": "043c543b63b895881d9abfbc320cb863",
                            "is_established": true,
                            "cipher_suite": "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
                            "cert_file_uids": "FcXA7Mkd1Wz0FwR4j01",
                            "elliptic_curve": "secp384r1",
                            "ssl_version": "TLS1.2",
                            "ja3s_server_fingerprint": "ae4edc6faf64d08308082ad26be60767"
                        }
                    }
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
                },
                "3": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "2",
                        "4"
                    ],
                    "extensions": {
                        "x-darktrace-connection": {
                            "identifier": "CnqTYB1K38sGXvsZ0101"
                        }
                    }
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "5": {
                    "type": "x509-certificate",
                    "issuer": "CN=EC2AMAZ-2GNPPAQ",
                    "subject": "CN=EC2AMAZ-2GNPPAQ"
                }
            },
            "first_observed": "2022-04-07T05:24:20.219Z",
            "last_observed": "2022-04-07T05:24:20.219Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--e673ab3a-2547-4a7f-8eb5-431d07c647ff",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-07T05:24:20.219Z",
            "modified": "2022-04-07T05:24:20.219Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-03-22T11:04:31.000Z"
                },
                "1": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
                },
                "2": {
                    "type": "network-traffic",
                    "src_ref": "1",
                    "src_port": 33484,
                    "dst_ref": "4",
                    "dst_port": 3389,
                    "protocols": [
                        "null"
                    ],
                    "extensions": {
                        "x-darktrace-rdp": {
                            "cookie": "dpl",
                            "security_protocol": "HYBRID"
                        }
                    }
                },
                "3": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "1",
                        "4"
                    ],
                    "extensions": {
                        "x-darktrace-connection": {
                            "identifier": "CnqTYB1K38sGXvsZ0101"
                        }
                    }
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                }
            },
            "first_observed": "2022-04-07T05:24:20.219Z",
            "last_observed": "2022-04-07T05:24:20.219Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--076d2984-1880-4d24-8bf6-32a274512dcf",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-07T05:24:20.219Z",
            "modified": "2022-04-07T05:24:20.219Z",
            "objects": {
                "0": {
                    "type": "network-traffic",
                    "src_packets": 11,
                    "extensions": {
                        "x-darktrace-conn": {
                            "originator_ttl": 102,
                            "connection_length": "00h00m02s",
                            "responder_ttl": 128,
                            "conn_state": "RSTO : Originator aborted : Connection established, originator aborted (sent a RST).",
                            "originator_asn": "AS44477 IP Oleinichenko Denis",
                            "orig_country_code": "RU",
                            "history": "ShADdaR",
                            "start_ts": "2022-03-22T11:04:31.000Z",
                            "is_locally_responded": true,
                            "connection_state_desc": "Originator aborted",
                            "app_protocol": "ssl"
                        }
                    },
                    "dst_byte_count": 1603,
                    "src_port": 33484,
                    "dst_port": 3389,
                    "src_ref": "2",
                    "src_byte_count": 1232,
                    "dst_packets": 8,
                    "protocols": [
                        "tcp"
                    ],
                    "dst_ref": "4"
                },
                "1": {
                    "type": "x-oca-event",
                    "created": "2022-03-22T11:04:31.000Z"
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
                },
                "3": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "2",
                        "4"
                    ],
                    "extensions": {
                        "x-darktrace-connection": {
                            "identifier": "CnqTYB1K38sGXvsZ0101"
                        }
                    }
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                }
            },
            "first_observed": "2022-04-07T05:24:20.219Z",
            "last_observed": "2022-04-07T05:24:20.219Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--7075d60d-63fd-4b9b-807e-df9e655882f3",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-07T05:24:20.219Z",
            "modified": "2022-04-07T05:24:20.219Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-03-22T11:04:29.000Z"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 23545,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "dst_port": 3389,
                    "protocols": [
                        "null"
                    ],
                    "extensions": {
                        "x-darktrace-x509": {
                            "file_id": "FZ9xi5bEsRVmJP1d01",
                            "certificate_key_type": "rsa",
                            "certificate_key_length": 2048
                        }
                    }
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
                },
                "3": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "2",
                        "4"
                    ],
                    "extensions": {
                        "x-darktrace-connection": {
                            "identifier": "CdvBdF3iF8inLx6jLe01"
                        }
                    }
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "5": {
                    "type": "x509-certificate",
                    "validity_not_before": "2022-08-15T11:22:14.000Z",
                    "signature_algorithm": "sha256WithRSAEncryption",
                    "subject_public_key_algorithm": "rsaEncryption",
                    "subject": "CN=EC2AMAZ-2GNPPAQ",
                    "subject_public_key_exponent": 65537,
                    "validity_not_after": "2022-02-13T11:22:14.000Z",
                    "version": "3",
                    "serial_number": "76FDB38B8D5AA88844250EFE0EA89026",
                    "issuer": "CN=EC2AMAZ-2GNPPAQ"
                }
            },
            "first_observed": "2022-04-07T05:24:20.219Z",
            "last_observed": "2022-04-07T05:24:20.219Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```

### Multiple Observation  

####STIX Translate query
```shell
translate darktrace query '{}' "[ipv4-addr:value = '0.0.0.0' AND x-darktrace-ssl:ssl_version='TLS1.2'] START t'2022-03-21T11:00:00.000Z' STOP t'2022-03-22T11:05:00.003Z'"
```

#### STIX Translate query - output

```json
{
    "queries": [
        {
            "search": "(((@fields.version:TLS1.2) AND (@fields.source_ip:\"0.0.0.0\" OR @fields.dest_ip:\"0.0.0.0\" OR @fields.src:\"0.0.0.0\" OR @fields.dst:\"0.0.0.0\" OR @fields.ip:\"0.0.0.0\")) AND (@fields.epochdate :>1647860400.0 AND @fields.epochdate :<1647947100.003))",
            "fields": [],
            "timeframe": "custom",
            "time": {
                "from": "2022-03-21T11:00:00.000000Z",
                "to": "2022-03-22T11:05:00.003000Z"
            },
            "size": 10000
        }
    ]
}
```


#### STIX Transmit query

```shell
transmit 
darktrace 
"{\"host\":\"xx.xx.xx\"}"
"{\"auth\":{\"private_token\": \"xxxxx\", \"public_token\": \"xxxxx\"}}"
results
"{\"search\":\"(((@fields.version:TLS1.2) AND (@fields.source_ip:\\"0.0.0.0\\" OR @fields.dest_ip:\\"0.0.0.0\\" OR @fields.src:\\"0.0.0.0\\" OR @fields.dst:\\"0.0.0.0\\" OR @fields.ip:\\"0.0.0.0\\")) AND (@fields.epochdate :>1647860400.0 AND @fields.epochdate :<1647947100.003))\",\"fields\":[],\"timeframe\":\"custom\",\"time\":{\"from\":\"2022-03-21T11:00:00.000000Z\",\"to\":\"2022-03-22T11:05:00.003000Z\"},\"size\":10000}" 
0 2
```

#### STIX Transmit query - output

```json
{
    "type": "bundle",
    "id": "bundle--69e78875-840f-4a90-acd2-f727704cfca5",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "darktrace",
            "identity_class ": "events"
        },
        {
            "id": "observed-data--19eda175-c310-44ac-a8d9-1e836f301f57",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-07T05:41:54.522Z",
            "modified": "2022-04-07T05:41:54.522Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-03-22T11:04:31.000Z"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 33484,
                    "dst_port": 3389,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "protocols": [
                        "null"
                    ],
                    "extensions": {
                        "x-darktrace-ssl": {
                            "total_ciphers": 28,
                            "validation_status": "unable to get local issuer certificate",
                            "is_client_hello_seen": true,
                            "ja3_client_fingerprint": "043c543b63b895881d9abfbc320cb863",
                            "is_established": true,
                            "cipher_suite": "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
                            "cert_file_uids": "FcXA7Mkd1Wz0FwR4j01",
                            "elliptic_curve": "secp384r1",
                            "ssl_version": "TLS1.2",
                            "ja3s_server_fingerprint": "ae4edc6faf64d08308082ad26be60767"
                        }
                    }
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
                },
                "3": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "2",
                        "4"
                    ],
                    "extensions": {
                        "x-darktrace-connection": {
                            "identifier": "CnqTYB1K38sGXvsZ0101"
                        }
                    }
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "5": {
                    "type": "x509-certificate",
                    "issuer": "CN=EC2AMAZ-2GNPPAQ",
                    "subject": "CN=EC2AMAZ-2GNPPAQ"
                }
            },
            "first_observed": "2022-04-07T05:41:54.522Z",
            "last_observed": "2022-04-07T05:41:54.522Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--d32b74d6-d601-462e-a78c-054cf3607459",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-07T05:41:54.524Z",
            "modified": "2022-04-07T05:41:54.524Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-03-22T11:04:29.000Z"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 23545,
                    "dst_port": 3389,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "protocols": [
                        "null"
                    ],
                    "extensions": {
                        "x-darktrace-ssl": {
                            "total_ciphers": 28,
                            "validation_status": "unable to get local issuer certificate",
                            "is_client_hello_seen": true,
                            "ja3_client_fingerprint": "043c543b63b895881d9abfbc320cb863",
                            "is_established": true,
                            "cipher_suite": "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
                            "cert_file_uids": "FZ9xi5bEsRVmJP1d01",
                            "elliptic_curve": "secp384r1",
                            "ssl_version": "TLS1.2",
                            "ja3s_server_fingerprint": "ae4edc6faf64d08308082ad26be60767"
                        }
                    }
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
                },
                "3": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "2",
                        "4"
                    ],
                    "extensions": {
                        "x-darktrace-connection": {
                            "identifier": "CdvBdF3iF8inLx6jLe01"
                        }
                    }
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "5": {
                    "type": "x509-certificate",
                    "issuer": "CN=EC2AMAZ-2GNPPAQ",
                    "subject": "CN=EC2AMAZ-2GNPPAQ"
                }
            },
            "first_observed": "2022-04-07T05:41:54.524Z",
            "last_observed": "2022-04-07T05:41:54.524Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--19801b68-8a79-4d22-8431-1b016f17bede",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-07T05:41:54.524Z",
            "modified": "2022-04-07T05:41:54.524Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-03-22T11:04:27.000Z"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 12529,
                    "dst_port": 3389,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "protocols": [
                        "null"
                    ],
                    "extensions": {
                        "x-darktrace-ssl": {
                            "total_ciphers": 28,
                            "validation_status": "unable to get local issuer certificate",
                            "is_client_hello_seen": true,
                            "ja3_client_fingerprint": "043c543b63b895881d9abfbc320cb863",
                            "is_established": true,
                            "cipher_suite": "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
                            "cert_file_uids": "F7KkW11tCMxrFeykE301",
                            "elliptic_curve": "secp384r1",
                            "ssl_version": "TLS1.2",
                            "ja3s_server_fingerprint": "ae4edc6faf64d08308082ad26be60767"
                        }
                    }
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
                },
                "3": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "2",
                        "4"
                    ],
                    "extensions": {
                        "x-darktrace-connection": {
                            "identifier": "CPphuC1YzPi3RxWki901"
                        }
                    }
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "5": {
                    "type": "x509-certificate",
                    "issuer": "CN=EC2AMAZ-2GNPPAQ",
                    "subject": "CN=EC2AMAZ-2GNPPAQ"
                }
            },
            "first_observed": "2022-04-07T05:41:54.524Z",
            "last_observed": "2022-04-07T05:41:54.524Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--bb49f2a8-da2d-4aba-b82c-652d64a9fa88",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-07T05:41:54.524Z",
            "modified": "2022-04-07T05:41:54.524Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-03-22T11:04:25.000Z"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 2421,
                    "dst_port": 3389,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "protocols": [
                        "null"
                    ],
                    "extensions": {
                        "x-darktrace-ssl": {
                            "total_ciphers": 28,
                            "validation_status": "unable to get local issuer certificate",
                            "is_client_hello_seen": true,
                            "ja3_client_fingerprint": "043c543b63b895881d9abfbc320cb863",
                            "is_established": true,
                            "cipher_suite": "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
                            "cert_file_uids": "FTWwOv1LJIUowbcGoi01",
                            "elliptic_curve": "secp384r1",
                            "ssl_version": "TLS1.2",
                            "ja3s_server_fingerprint": "ae4edc6faf64d08308082ad26be60767"
                        }
                    }
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
                },
                "3": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "2",
                        "4"
                    ],
                    "extensions": {
                        "x-darktrace-connection": {
                            "identifier": "CeVgti48vYLBsyb11301"
                        }
                    }
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "5": {
                    "type": "x509-certificate",
                    "issuer": "CN=EC2AMAZ-2GNPPAQ",
                    "subject": "CN=EC2AMAZ-2GNPPAQ"
                }
            },
            "first_observed": "2022-04-07T05:41:54.524Z",
            "last_observed": "2022-04-07T05:41:54.524Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--08960083-7872-4014-ab42-b8278a96024d",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-07T05:41:54.524Z",
            "modified": "2022-04-07T05:41:54.524Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-03-22T11:04:23.000Z"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 50100,
                    "dst_port": 3389,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "protocols": [
                        "null"
                    ],
                    "extensions": {
                        "x-darktrace-ssl": {
                            "total_ciphers": 28,
                            "validation_status": "unable to get local issuer certificate",
                            "is_client_hello_seen": true,
                            "ja3_client_fingerprint": "043c543b63b895881d9abfbc320cb863",
                            "is_established": true,
                            "cipher_suite": "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
                            "cert_file_uids": "FGEPjd2w8gst2QUqwh01",
                            "elliptic_curve": "secp384r1",
                            "ssl_version": "TLS1.2",
                            "ja3s_server_fingerprint": "ae4edc6faf64d08308082ad26be60767"
                        }
                    }
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
                },
                "3": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "2",
                        "4"
                    ],
                    "extensions": {
                        "x-darktrace-connection": {
                            "identifier": "CrcUaT2wIylNoL0SI801"
                        }
                    }
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "5": {
                    "type": "x509-certificate",
                    "issuer": "CN=EC2AMAZ-2GNPPAQ",
                    "subject": "CN=EC2AMAZ-2GNPPAQ"
                }
            },
            "first_observed": "2022-04-07T05:41:54.524Z",
            "last_observed": "2022-04-07T05:41:54.524Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--3943381f-37e6-4eb2-9930-a55309dc50c4",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-07T05:41:54.524Z",
            "modified": "2022-04-07T05:41:54.524Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-03-22T11:04:21.000Z"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 40102,
                    "dst_port": 3389,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "protocols": [
                        "null"
                    ],
                    "extensions": {
                        "x-darktrace-ssl": {
                            "total_ciphers": 28,
                            "validation_status": "unable to get local issuer certificate",
                            "is_client_hello_seen": true,
                            "ja3_client_fingerprint": "043c543b63b895881d9abfbc320cb863",
                            "is_established": true,
                            "cipher_suite": "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
                            "cert_file_uids": "FdHj4c4bnb8duFwdtb01",
                            "elliptic_curve": "secp384r1",
                            "ssl_version": "TLS1.2",
                            "ja3s_server_fingerprint": "ae4edc6faf64d08308082ad26be60767"
                        }
                    }
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
                },
                "3": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "2",
                        "4"
                    ],
                    "extensions": {
                        "x-darktrace-connection": {
                            "identifier": "C2tIWy2pB78ziJrV8j01"
                        }
                    }
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "5": {
                    "type": "x509-certificate",
                    "issuer": "CN=EC2AMAZ-2GNPPAQ",
                    "subject": "CN=EC2AMAZ-2GNPPAQ"
                }
            },
            "first_observed": "2022-04-07T05:41:54.524Z",
            "last_observed": "2022-04-07T05:41:54.524Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--00ec74b0-1bc2-4883-a4f7-b376a60d3435",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-07T05:41:54.524Z",
            "modified": "2022-04-07T05:41:54.524Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-03-22T11:04:19.000Z"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 29869,
                    "dst_port": 3389,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "protocols": [
                        "null"
                    ],
                    "extensions": {
                        "x-darktrace-ssl": {
                            "total_ciphers": 28,
                            "validation_status": "unable to get local issuer certificate",
                            "is_client_hello_seen": true,
                            "ja3_client_fingerprint": "043c543b63b895881d9abfbc320cb863",
                            "is_established": true,
                            "cipher_suite": "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
                            "cert_file_uids": "FCO09S2H0NWYjb90Zf01",
                            "elliptic_curve": "secp384r1",
                            "ssl_version": "TLS1.2",
                            "ja3s_server_fingerprint": "ae4edc6faf64d08308082ad26be60767"
                        }
                    }
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
                },
                "3": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "2",
                        "4"
                    ],
                    "extensions": {
                        "x-darktrace-connection": {
                            "identifier": "CxkH1xtKJGRmjrja201"
                        }
                    }
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "5": {
                    "type": "x509-certificate",
                    "issuer": "CN=EC2AMAZ-2GNPPAQ",
                    "subject": "CN=EC2AMAZ-2GNPPAQ"
                }
            },
            "first_observed": "2022-04-07T05:41:54.524Z",
            "last_observed": "2022-04-07T05:41:54.524Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--f1d401a7-0940-482c-9950-46700bc23eb2",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-07T05:41:54.524Z",
            "modified": "2022-04-07T05:41:54.524Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-03-22T11:04:17.000Z"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 20285,
                    "dst_port": 3389,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "protocols": [
                        "null"
                    ],
                    "extensions": {
                        "x-darktrace-ssl": {
                            "total_ciphers": 28,
                            "validation_status": "unable to get local issuer certificate",
                            "is_client_hello_seen": true,
                            "ja3_client_fingerprint": "043c543b63b895881d9abfbc320cb863",
                            "is_established": true,
                            "cipher_suite": "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
                            "cert_file_uids": "FpUah61XH0VQVGydVc01",
                            "elliptic_curve": "secp384r1",
                            "ssl_version": "TLS1.2",
                            "ja3s_server_fingerprint": "ae4edc6faf64d08308082ad26be60767"
                        }
                    }
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
                },
                "3": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "2",
                        "4"
                    ],
                    "extensions": {
                        "x-darktrace-connection": {
                            "identifier": "CiTMLg3ZSqESsn1yk01"
                        }
                    }
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "5": {
                    "type": "x509-certificate",
                    "issuer": "CN=EC2AMAZ-2GNPPAQ",
                    "subject": "CN=EC2AMAZ-2GNPPAQ"
                }
            },
            "first_observed": "2022-04-07T05:41:54.524Z",
            "last_observed": "2022-04-07T05:41:54.524Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--a3d7049b-1221-44cd-b936-e8fef09f2dc6",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-07T05:41:54.524Z",
            "modified": "2022-04-07T05:41:54.524Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-03-22T11:04:15.000Z"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 9793,
                    "dst_port": 3389,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "protocols": [
                        "null"
                    ],
                    "extensions": {
                        "x-darktrace-ssl": {
                            "total_ciphers": 28,
                            "validation_status": "unable to get local issuer certificate",
                            "is_client_hello_seen": true,
                            "ja3_client_fingerprint": "043c543b63b895881d9abfbc320cb863",
                            "is_established": true,
                            "cipher_suite": "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
                            "cert_file_uids": "FVbiDvMg2dOKq9JK101",
                            "elliptic_curve": "secp384r1",
                            "ssl_version": "TLS1.2",
                            "ja3s_server_fingerprint": "ae4edc6faf64d08308082ad26be60767"
                        }
                    }
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
                },
                "3": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "2",
                        "4"
                    ],
                    "extensions": {
                        "x-darktrace-connection": {
                            "identifier": "Cm2RmF1W3mq1YYJck701"
                        }
                    }
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "5": {
                    "type": "x509-certificate",
                    "issuer": "CN=EC2AMAZ-2GNPPAQ",
                    "subject": "CN=EC2AMAZ-2GNPPAQ"
                }
            },
            "first_observed": "2022-04-07T05:41:54.524Z",
            "last_observed": "2022-04-07T05:41:54.524Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```

#### STIX Execute query
```shell
execute
darktrace
darktrace
"{\"type\":\"identity\",\"id\":\"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\",\"name\":\"darktrace\",\"identity_class \":\"events\"}"
"{\"host\":\"xx.xx.xx\"}"
"{\"auth\":{\"private_token\": \"xxxxx\", \"public_token\": \"xxxxx\"}}"
"[x-darktrace-ssl:ssl_version='TLS1.2'] START t'2022-03-21T11:00:00.000Z' STOP t'2022-03-22T11:05:00.003Z'"
```
#### STIX Execute query - output
```json
{
    "type": "bundle",
    "id": "bundle--c2538dec-265e-45c7-85a1-7c2206286e21",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "darktrace",
            "identity_class ": "events"
        },
        {
            "id": "observed-data--fad9e913-51a4-4882-898c-99455a8edc8e",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-07T05:38:05.840Z",
            "modified": "2022-04-07T05:38:05.840Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-03-22T11:04:31.000Z"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 33484,
                    "dst_port": 3389,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "protocols": [
                        "null"
                    ],
                    "extensions": {
                        "x-darktrace-ssl": {
                            "total_ciphers": 28,
                            "validation_status": "unable to get local issuer certificate",
                            "is_client_hello_seen": true,
                            "ja3_client_fingerprint": "043c543b63b895881d9abfbc320cb863",
                            "is_established": true,
                            "cipher_suite": "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
                            "cert_file_uids": "FcXA7Mkd1Wz0FwR4j01",
                            "elliptic_curve": "secp384r1",
                            "ssl_version": "TLS1.2",
                            "ja3s_server_fingerprint": "ae4edc6faf64d08308082ad26be60767"
                        }
                    }
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
                },
                "3": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "2",
                        "4"
                    ],
                    "extensions": {
                        "x-darktrace-connection": {
                            "identifier": "CnqTYB1K38sGXvsZ0101"
                        }
                    }
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "5": {
                    "type": "x509-certificate",
                    "issuer": "CN=EC2AMAZ-2GNPPAQ",
                    "subject": "CN=EC2AMAZ-2GNPPAQ"
                }
            },
            "first_observed": "2022-04-07T05:38:05.840Z",
            "last_observed": "2022-04-07T05:38:05.840Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--70ff51ec-4f38-463d-8d5e-a838da801220",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-07T05:38:05.840Z",
            "modified": "2022-04-07T05:38:05.840Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-03-22T11:04:29.000Z"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 23545,
                    "dst_port": 3389,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "protocols": [
                        "null"
                    ],
                    "extensions": {
                        "x-darktrace-ssl": {
                            "total_ciphers": 28,
                            "validation_status": "unable to get local issuer certificate",
                            "is_client_hello_seen": true,
                            "ja3_client_fingerprint": "043c543b63b895881d9abfbc320cb863",
                            "is_established": true,
                            "cipher_suite": "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
                            "cert_file_uids": "FZ9xi5bEsRVmJP1d01",
                            "elliptic_curve": "secp384r1",
                            "ssl_version": "TLS1.2",
                            "ja3s_server_fingerprint": "ae4edc6faf64d08308082ad26be60767"
                        }
                    }
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
                },
                "3": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "2",
                        "4"
                    ],
                    "extensions": {
                        "x-darktrace-connection": {
                            "identifier": "CdvBdF3iF8inLx6jLe01"
                        }
                    }
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "5": {
                    "type": "x509-certificate",
                    "issuer": "CN=EC2AMAZ-2GNPPAQ",
                    "subject": "CN=EC2AMAZ-2GNPPAQ"
                }
            },
            "first_observed": "2022-04-07T05:38:05.840Z",
            "last_observed": "2022-04-07T05:38:05.840Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--0e63b18a-5fd8-43a7-87b5-dee8764fa27f",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-07T05:38:05.840Z",
            "modified": "2022-04-07T05:38:05.840Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-03-22T11:04:27.000Z"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 12529,
                    "dst_port": 3389,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "protocols": [
                        "null"
                    ],
                    "extensions": {
                        "x-darktrace-ssl": {
                            "total_ciphers": 28,
                            "validation_status": "unable to get local issuer certificate",
                            "is_client_hello_seen": true,
                            "ja3_client_fingerprint": "043c543b63b895881d9abfbc320cb863",
                            "is_established": true,
                            "cipher_suite": "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
                            "cert_file_uids": "F7KkW11tCMxrFeykE301",
                            "elliptic_curve": "secp384r1",
                            "ssl_version": "TLS1.2",
                            "ja3s_server_fingerprint": "ae4edc6faf64d08308082ad26be60767"
                        }
                    }
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
                },
                "3": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "2",
                        "4"
                    ],
                    "extensions": {
                        "x-darktrace-connection": {
                            "identifier": "CPphuC1YzPi3RxWki901"
                        }
                    }
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "5": {
                    "type": "x509-certificate",
                    "issuer": "CN=EC2AMAZ-2GNPPAQ",
                    "subject": "CN=EC2AMAZ-2GNPPAQ"
                }
            },
            "first_observed": "2022-04-07T05:38:05.840Z",
            "last_observed": "2022-04-07T05:38:05.840Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--a1370e1f-b7a8-4a96-a1e2-f78eb34a5272",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-07T05:38:05.840Z",
            "modified": "2022-04-07T05:38:05.840Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-03-22T11:04:25.000Z"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 2421,
                    "dst_port": 3389,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "protocols": [
                        "null"
                    ],
                    "extensions": {
                        "x-darktrace-ssl": {
                            "total_ciphers": 28,
                            "validation_status": "unable to get local issuer certificate",
                            "is_client_hello_seen": true,
                            "ja3_client_fingerprint": "043c543b63b895881d9abfbc320cb863",
                            "is_established": true,
                            "cipher_suite": "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
                            "cert_file_uids": "FTWwOv1LJIUowbcGoi01",
                            "elliptic_curve": "secp384r1",
                            "ssl_version": "TLS1.2",
                            "ja3s_server_fingerprint": "ae4edc6faf64d08308082ad26be60767"
                        }
                    }
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
                },
                "3": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "2",
                        "4"
                    ],
                    "extensions": {
                        "x-darktrace-connection": {
                            "identifier": "CeVgti48vYLBsyb11301"
                        }
                    }
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "5": {
                    "type": "x509-certificate",
                    "issuer": "CN=EC2AMAZ-2GNPPAQ",
                    "subject": "CN=EC2AMAZ-2GNPPAQ"
                }
            },
            "first_observed": "2022-04-07T05:38:05.840Z",
            "last_observed": "2022-04-07T05:38:05.840Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--1c9d0a8b-978f-45be-8735-6361904dee64",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-07T05:38:05.840Z",
            "modified": "2022-04-07T05:38:05.840Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-03-22T11:04:23.000Z"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 50100,
                    "dst_port": 3389,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "protocols": [
                        "null"
                    ],
                    "extensions": {
                        "x-darktrace-ssl": {
                            "total_ciphers": 28,
                            "validation_status": "unable to get local issuer certificate",
                            "is_client_hello_seen": true,
                            "ja3_client_fingerprint": "043c543b63b895881d9abfbc320cb863",
                            "is_established": true,
                            "cipher_suite": "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
                            "cert_file_uids": "FGEPjd2w8gst2QUqwh01",
                            "elliptic_curve": "secp384r1",
                            "ssl_version": "TLS1.2",
                            "ja3s_server_fingerprint": "ae4edc6faf64d08308082ad26be60767"
                        }
                    }
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
                },
                "3": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "2",
                        "4"
                    ],
                    "extensions": {
                        "x-darktrace-connection": {
                            "identifier": "CrcUaT2wIylNoL0SI801"
                        }
                    }
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "5": {
                    "type": "x509-certificate",
                    "issuer": "CN=EC2AMAZ-2GNPPAQ",
                    "subject": "CN=EC2AMAZ-2GNPPAQ"
                }
            },
            "first_observed": "2022-04-07T05:38:05.840Z",
            "last_observed": "2022-04-07T05:38:05.840Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--987a70fd-5f19-4d3b-afdf-a7d47fb9c898",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-07T05:38:05.840Z",
            "modified": "2022-04-07T05:38:05.840Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-03-22T11:04:21.000Z"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 40102,
                    "dst_port": 3389,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "protocols": [
                        "null"
                    ],
                    "extensions": {
                        "x-darktrace-ssl": {
                            "total_ciphers": 28,
                            "validation_status": "unable to get local issuer certificate",
                            "is_client_hello_seen": true,
                            "ja3_client_fingerprint": "043c543b63b895881d9abfbc320cb863",
                            "is_established": true,
                            "cipher_suite": "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
                            "cert_file_uids": "FdHj4c4bnb8duFwdtb01",
                            "elliptic_curve": "secp384r1",
                            "ssl_version": "TLS1.2",
                            "ja3s_server_fingerprint": "ae4edc6faf64d08308082ad26be60767"
                        }
                    }
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
                },
                "3": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "2",
                        "4"
                    ],
                    "extensions": {
                        "x-darktrace-connection": {
                            "identifier": "C2tIWy2pB78ziJrV8j01"
                        }
                    }
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "5": {
                    "type": "x509-certificate",
                    "issuer": "CN=EC2AMAZ-2GNPPAQ",
                    "subject": "CN=EC2AMAZ-2GNPPAQ"
                }
            },
            "first_observed": "2022-04-07T05:38:05.840Z",
            "last_observed": "2022-04-07T05:38:05.840Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--cba5a71f-27ec-468a-bc11-02b2c227c4ec",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-07T05:38:05.840Z",
            "modified": "2022-04-07T05:38:05.840Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-03-22T11:04:19.000Z"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 29869,
                    "dst_port": 3389,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "protocols": [
                        "null"
                    ],
                    "extensions": {
                        "x-darktrace-ssl": {
                            "total_ciphers": 28,
                            "validation_status": "unable to get local issuer certificate",
                            "is_client_hello_seen": true,
                            "ja3_client_fingerprint": "043c543b63b895881d9abfbc320cb863",
                            "is_established": true,
                            "cipher_suite": "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
                            "cert_file_uids": "FCO09S2H0NWYjb90Zf01",
                            "elliptic_curve": "secp384r1",
                            "ssl_version": "TLS1.2",
                            "ja3s_server_fingerprint": "ae4edc6faf64d08308082ad26be60767"
                        }
                    }
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
                },
                "3": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "2",
                        "4"
                    ],
                    "extensions": {
                        "x-darktrace-connection": {
                            "identifier": "CxkH1xtKJGRmjrja201"
                        }
                    }
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "5": {
                    "type": "x509-certificate",
                    "issuer": "CN=EC2AMAZ-2GNPPAQ",
                    "subject": "CN=EC2AMAZ-2GNPPAQ"
                }
            },
            "first_observed": "2022-04-07T05:38:05.840Z",
            "last_observed": "2022-04-07T05:38:05.840Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--6fe7667e-6771-472c-b133-e832201b3d0b",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-07T05:38:05.840Z",
            "modified": "2022-04-07T05:38:05.840Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-03-22T11:04:17.000Z"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 20285,
                    "dst_port": 3389,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "protocols": [
                        "null"
                    ],
                    "extensions": {
                        "x-darktrace-ssl": {
                            "total_ciphers": 28,
                            "validation_status": "unable to get local issuer certificate",
                            "is_client_hello_seen": true,
                            "ja3_client_fingerprint": "043c543b63b895881d9abfbc320cb863",
                            "is_established": true,
                            "cipher_suite": "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
                            "cert_file_uids": "FpUah61XH0VQVGydVc01",
                            "elliptic_curve": "secp384r1",
                            "ssl_version": "TLS1.2",
                            "ja3s_server_fingerprint": "ae4edc6faf64d08308082ad26be60767"
                        }
                    }
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
                },
                "3": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "2",
                        "4"
                    ],
                    "extensions": {
                        "x-darktrace-connection": {
                            "identifier": "CiTMLg3ZSqESsn1yk01"
                        }
                    }
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "5": {
                    "type": "x509-certificate",
                    "issuer": "CN=EC2AMAZ-2GNPPAQ",
                    "subject": "CN=EC2AMAZ-2GNPPAQ"
                }
            },
            "first_observed": "2022-04-07T05:38:05.840Z",
            "last_observed": "2022-04-07T05:38:05.840Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--d036ee26-4a45-4f85-902b-cd2ff24a8513",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-07T05:38:05.840Z",
            "modified": "2022-04-07T05:38:05.840Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-03-22T11:04:15.000Z"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 9793,
                    "dst_port": 3389,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "protocols": [
                        "null"
                    ],
                    "extensions": {
                        "x-darktrace-ssl": {
                            "total_ciphers": 28,
                            "validation_status": "unable to get local issuer certificate",
                            "is_client_hello_seen": true,
                            "ja3_client_fingerprint": "043c543b63b895881d9abfbc320cb863",
                            "is_established": true,
                            "cipher_suite": "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
                            "cert_file_uids": "FVbiDvMg2dOKq9JK101",
                            "elliptic_curve": "secp384r1",
                            "ssl_version": "TLS1.2",
                            "ja3s_server_fingerprint": "ae4edc6faf64d08308082ad26be60767"
                        }
                    }
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
                },
                "3": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "2",
                        "4"
                    ],
                    "extensions": {
                        "x-darktrace-connection": {
                            "identifier": "Cm2RmF1W3mq1YYJck701"
                        }
                    }
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "5": {
                    "type": "x509-certificate",
                    "issuer": "CN=EC2AMAZ-2GNPPAQ",
                    "subject": "CN=EC2AMAZ-2GNPPAQ"
                }
            },
            "first_observed": "2022-04-07T05:38:05.840Z",
            "last_observed": "2022-04-07T05:38:05.840Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}

```

#### STIX Ping query
```shell
transmit
darktrace
"{\"host\":\"xx.xx.xx\"}"
"{\"auth\":{\"private_token\": \"xxxxx\", \"public_token\": \"xxxxx\"}}"
ping
```

#### STIX Ping query - output
```json
{
    "success": true
}
```

### Considerations
-  Advanced Search queries are Base64 encoded strings, composed of the query search terms.
-  Double quotes used in the search string must be escaped with a backslash before encoding.

### Observations
-  Darktrace does not support >= and <=, so the same is achieved by < and > operators by increasing and decreasing the corresponding values.
