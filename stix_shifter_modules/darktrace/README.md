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
            "conn": { "epochdate": 1647946686.995818, "source_port": 24178, "source_ip": "0.0.0.0", "dest_ip": "1.1.1.1", "uid": "CEfQ2a2ObXcyNJUvEk01", "dest_port": 3389, "proto": "null" },
            "x509": { "epochdate": 1647946686.995818, "source_port": 24178, "certificate_not_valid_after": 1660562534, "fid": "FxWXXc1uH1zQNF66T701", "certificate_key_type": "rsa", "certificate_sig_alg": "sha256WithRSAEncryption", "certificate_key_alg": "rsaEncryption", "certificate_subject": "CN=EC2AMAZ-2GNPPAQ", "source_ip": "0.0.0.0", "certificate_exponent": "65537", "certificate_key_length": 2048, "dest_ip": "1.1.1.1", "certificate_not_valid_before": 1644751334, "uid": "CEfQ2a2ObXcyNJUvEk01", "dest_port": 3389, "certificate_version": 3, "certificate_serial": "76FDB38B8D5AA88844250EFE0EA89026", "certificate_issuer": "CN=EC2AMAZ-2GNPPAQ", "proto": "null" } },
        {
            "conn": { "epochdate": 1647946686.995818, "source_port": 24178, "dest_port": 3389, "source_ip": "0.0.0.0", "dest_ip": "1.1.1.1", "uid": "CEfQ2a2ObXcyNJUvEk01", "proto": "null" },
            "ssl": { "epochdate": 1647946686.995818, "total_client_ciphers": 28, "validation_status": "unable to get local issuer certificate", "client_hello_seen": true, "ja3_client_fingerprint": "043c543b63b895881d9abfbc320cb863", "source_port": 24178, "dest_port": 3389, "established": true, "source_ip": "0.0.0.0", "issuer": "CN=EC2AMAZ-2GNPPAQ", "cipher": "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384", "dest_ip": "1.1.1.1", "cert_chain_fuids": "FxWXXc1uH1zQNF66T701", "curve": "secp384r1", "uid": "CEfQ2a2ObXcyNJUvEk01", "version": "TLS1.2", "ja3s_server_fingerprint": "ae4edc6faf64d08308082ad26be60767", "subject": "CN=EC2AMAZ-2GNPPAQ", "proto": "null" }
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
    "id": "bundle--17b8cbb6-1267-4d71-bbee-672749df19e3",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "darktrace",
            "identity_class": "events",
            "created": "2022-03-16T13:22:50.336Z",
            "modified": "2022-03-16T13:22:50.336Z"
        },
        {
            "id": "observed-data--17d5395b-592f-4cbb-9c1d-c8689b84da95",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-28T13:26:43.452Z",
            "modified": "2022-04-28T13:26:43.452Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-03-22T11:04:31.000Z",
                    "code": "CqQ5sRAFWzt7NRQmj01"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 11256,
                    "dst_port": 3389,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "protocols": [
                        "ssl"
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
                            "ja3s_server_fingerprint": "bcf3a836c82d12ee988005fb0c011445",
                            "server_certificate_ref": "5"
                        }
                    }
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
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
            "first_observed": "2022-04-28T13:26:43.452Z",
            "last_observed": "2022-04-28T13:26:43.452Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--9bcbbca4-6cbb-47d0-aeb1-b3c9b61d8395",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-28T13:26:43.460Z",
            "modified": "2022-04-28T13:26:43.460Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-03-22T11:04:31.000Z",
                    "code": "CqQ5sRAFWzt7NRQmj01"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 11256,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "dst_port": 3389,
                    "protocols": [
                        "ssl"
                    ]
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "5": {
                    "type": "x509-certificate",
                    "validity_not_before": "2022-08-15T11:22:14.000Z",
                    "extensions": {
                        "x-darktrace-x509": {
                            "file_id": "F2D8iX1YaTCWKlsoN01",
                            "certificate_key_type": "rsa",
                            "certificate_key_length": 2048
                        }
                    },
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
            "first_observed": "2022-04-28T13:26:43.460Z",
            "last_observed": "2022-04-28T13:26:43.460Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```

### Multiple Observation  

####STIX Translate query
```shell
translate darktrace query '{}' "[ipv4-addr:value = '0.0.0.0' AND network-traffic:extensions.'x-darktrace-ssl'.elliptic_curve ='secp384r1'] START t'2022-03-21T11:00:00.000Z' STOP t'2022-03-22T11:05:00.003Z'"
```

#### STIX Translate query - output

```json
{
    "queries": [
        {
            "search": "(((@fields.curve:\"secp384r1\") AND (@fields.source_ip:\"0.0.0.0\" OR @fields.dest_ip:\"0.0.0.0\" OR @fields.src:\"0.0.0.0\" OR @fields.dst:\"0.0.0.0\" OR @fields.ip:\"0.0.0.0\" OR @fields.subnet_mask:\"0.0.0.0\" OR @fields.released_ip:\"0.0.0.0\" OR @fields.requested_ip:\"0.0.0.0\" OR @fields.assigned_ip:\"0.0.0.0\")) AND (@fields.epochdate :>1647860400.0 AND @fields.epochdate :<1647947100.003))",
            "fields": [],
            "timeframe": "custom",
            "time": {
                "from": "2022-04-25T11:00:00.000000Z",
                "to": "2022-04-28T11:05:00.003000Z"
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
"{\"search\": \"(((@fields.curve:\\"secp384r1\\") AND (@fields.source_ip:\\"0.0.0.0\\" OR @fields.dest_ip:\\"0.0.0.0\\" OR @fields.src:\\"0.0.0.0\\"OR @fields.dst:\\"0.0.0.0\\" OR @fields.ip:\\"0.0.0.0\\" OR @fields.subnet_mask:\\"0.0.0.0\\" OR @fields.released_ip:\\"0.0.0.0\\" OR@fields.requested_ip:\\"0.0.0.0\\" OR @fields.assigned_ip:\\"0.0.0.0\\")) AND (@fields.epochdate :>1647860400.0 AND @fields.epochdate :<1647947100.003))\",\"fields\": [],\"timeframe\": \"custom\",\"time\": {\"from\": \"2022-04-25T11:00:00.000000Z\",\"to\":\"2022-04-28T11:05:00.003000Z\"},\"size\": 10000}"
0 2
```

#### STIX Transmit query - output

```json
{
    "success": true,
    "data": [
        {
            "conn": {
                "epochdate": 1651143658.117242,
                "source_port": 54915,
                "dest_port": 3389,
                "source_ip": "0.0.0.0",
                "dest_ip": "1.1.1.1",
                "uid": "C6TH6a1MtQEqWnyoy801",
                "proto": "ssl"
            },
            "ssl": {
                "epochdate": 1651143658.117242,
                "total_client_ciphers": 50,
                "validation_status": "unable to get local issuer certificate",
                "client_hello_seen": true,
                "ja3_client_fingerprint": "75fb48a465416d66291fb52a733d4787",
                "source_port": 54915,
                "dest_port": 3389,
                "established": true,
                "source_ip": "0.0.0.0",
                "issuer": "CN=EC2AMAZ-2GNPPAQ",
                "cipher": "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA",
                "dest_ip": "1.1.1.1",
                "cert_chain_fuids": "FmNnVq4z5RYyPGY7Ab01",
                "curve": "secp384r1",
                "uid": "C6TH6a1MtQEqWnyoy801",
                "version": "TLS1.0",
                "ja3s_server_fingerprint": "bcf3a836c82d12ee988005fb0c011445",
                "subject": "CN=EC2AMAZ-2GNPPAQ"
            }
        },
        {
            "conn": {
                "epochdate": 1651143612.952305,
                "source_port": 64959,
                "dest_port": 3389,
                "source_ip": "0.0.0.0",
                "dest_ip": "1.1.1.1",
                "uid": "C6pB5U2hSWDpf2y6h101",
                "proto": "ssl"
            },
            "ssl": {
                "epochdate": 1651143612.952305,
                "total_client_ciphers": 50,
                "validation_status": "unable to get local issuer certificate",
                "client_hello_seen": true,
                "ja3_client_fingerprint": "75fb48a465416d66291fb52a733d4787",
                "source_port": 64959,
                "dest_port": 3389,
                "established": true,
                "source_ip": "0.0.0.0",
                "issuer": "CN=EC2AMAZ-2GNPPAQ",
                "cipher": "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA",
                "dest_ip": "1.1.1.1",
                "cert_chain_fuids": "Fi6LNwSCOC85DdmGk01",
                "curve": "secp384r1",
                "uid": "C6pB5U2hSWDpf2y6h101",
                "version": "TLS1.0",
                "ja3s_server_fingerprint": "bcf3a836c82d12ee988005fb0c011445",
                "subject": "CN=EC2AMAZ-2GNPPAQ"
            }
        }
    ]
}
```

#### STIX Execute query
```shell
execute
darktrace
darktrace
"{\"type\":\"identity\",\"id\":\"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\",\"name\":\"darktrace\",\"identity_class\":\"events\", \"created\": \"2022-04-11T16:11:11.878Z\",\"modified\": \"2022-04-11T16:11:11.878Z\"}"
"{\"host\":\"xx.xx.xx\"}"
"{\"auth\":{\"private_token\": \"xxxxx\", \"public_token\": \"xxxxx\"}}"
"[network-traffic:extensions.'x-darktrace-ssl'.elliptic_curve ='secp384r1'] START t'2022-04-25T11:00:00.000Z' STOP t'2022-04-28T11:05:00.003Z'"
```
#### STIX Execute query - output
```json
{
    "type": "bundle",
    "id": "bundle--2ccf184a-da6e-43ca-a14f-d813c8f3b74c",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "darktrace",
            "identity_class": "events",
            "created": "2022-04-11T16:11:11.878Z",
            "modified": "2022-04-11T16:11:11.878Z"
        },
        {
            "id": "observed-data--4f01cfea-c96a-424a-be55-205c6e8c7ce3",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-28T13:08:42.914Z",
            "modified": "2022-04-28T13:08:42.914Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-04-28T11:04:29.000Z",
                    "code": "CyYTbd11Me5BcCwaTe01"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 62309,
                    "dst_port": 3389,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "protocols": [
                        "ssl"
                    ],
                    "extensions": {
                        "x-darktrace-ssl": {
                            "total_ciphers": 55,
                            "validation_status": "unable to get local issuer certificate",
                            "is_client_hello_seen": true,
                            "ja3_client_fingerprint": "0b63812a99e66c82a20d30c3b9ba6e06",
                            "is_established": true,
                            "cipher_suite": "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA",
                            "cert_file_uids": "Fezsmf35thStOZvLw901",
                            "elliptic_curve": "secp384r1",
                            "ssl_version": "TLS1.0",
                            "ja3s_server_fingerprint": "bcf3a836c82d12ee988005fb0c011445",
                            "server_certificate_ref": "5"
                        }
                    }
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
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
            "first_observed": "2022-04-28T13:08:42.914Z",
            "last_observed": "2022-04-28T13:08:42.914Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--0aa72643-badc-483b-b3e5-5d04350e3215",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-28T13:08:42.914Z",
            "modified": "2022-04-28T13:08:42.914Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-04-28T11:04:20.000Z",
                    "code": "CBofjX3jCG3ZFu1DB501"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 51679,
                    "dst_port": 3389,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "protocols": [
                        "ssl"
                    ],
                    "extensions": {
                        "x-darktrace-ssl": {
                            "total_ciphers": 41,
                            "validation_status": "unable to get local issuer certificate",
                            "is_client_hello_seen": true,
                            "ja3_client_fingerprint": "43e25370946f1b41b411e6d0bf378456",
                            "is_established": true,
                            "cipher_suite": "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA",
                            "cert_file_uids": "FrNUiK3CyPmwHuzKy301",
                            "elliptic_curve": "secp384r1",
                            "ssl_version": "TLS1.0",
                            "ja3s_server_fingerprint": "bcf3a836c82d12ee988005fb0c011445",
                            "server_certificate_ref": "5"
                        }
                    }
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
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
            "first_observed": "2022-04-28T13:08:42.914Z",
            "last_observed": "2022-04-28T13:08:42.914Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--6fb3e22c-8721-4d47-96eb-df942c3925be",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-28T13:08:42.914Z",
            "modified": "2022-04-28T13:08:42.914Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-04-28T11:03:44.000Z",
                    "code": "CG9Qnp1w9bi0IHg3y701"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 54279,
                    "dst_port": 3389,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "protocols": [
                        "ssl"
                    ],
                    "extensions": {
                        "x-darktrace-ssl": {
                            "total_ciphers": 41,
                            "validation_status": "unable to get local issuer certificate",
                            "is_client_hello_seen": true,
                            "ja3_client_fingerprint": "43e25370946f1b41b411e6d0bf378456",
                            "is_established": true,
                            "cipher_suite": "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA",
                            "cert_file_uids": "Fjp4gH32yIXU4SeBJ501",
                            "elliptic_curve": "secp384r1",
                            "ssl_version": "TLS1.0",
                            "ja3s_server_fingerprint": "bcf3a836c82d12ee988005fb0c011445",
                            "server_certificate_ref": "5"
                        }
                    }
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
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
            "first_observed": "2022-04-28T13:08:42.914Z",
            "last_observed": "2022-04-28T13:08:42.914Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--9f29a7e1-4b3c-43f6-ad7e-e723f783db9d",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-28T13:08:42.914Z",
            "modified": "2022-04-28T13:08:42.914Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-04-28T11:03:20.000Z",
                    "code": "ChE02THkyZAIBRqYi01"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 59976,
                    "dst_port": 3389,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "protocols": [
                        "ssl"
                    ],
                    "extensions": {
                        "x-darktrace-ssl": {
                            "total_ciphers": 41,
                            "validation_status": "unable to get local issuer certificate",
                            "is_client_hello_seen": true,
                            "ja3_client_fingerprint": "43e25370946f1b41b411e6d0bf378456",
                            "is_established": true,
                            "cipher_suite": "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA",
                            "cert_file_uids": "F6nomdQ53HGoOvfh401",
                            "elliptic_curve": "secp384r1",
                            "ssl_version": "TLS1.0",
                            "ja3s_server_fingerprint": "bcf3a836c82d12ee988005fb0c011445",
                            "server_certificate_ref": "5"
                        }
                    }
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
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
            "first_observed": "2022-04-28T13:08:42.914Z",
            "last_observed": "2022-04-28T13:08:42.914Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--d073f848-1436-4ea9-bce1-339179562a1b",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-28T13:08:42.914Z",
            "modified": "2022-04-28T13:08:42.914Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-04-28T11:03:07.000Z",
                    "code": "CnAOaZ2jYcncPVyiR01"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 5922,
                    "dst_port": 3389,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "protocols": [
                        "ssl"
                    ],
                    "extensions": {
                        "x-darktrace-ssl": {
                            "total_ciphers": 50,
                            "validation_status": "unable to get local issuer certificate",
                            "is_client_hello_seen": true,
                            "ja3_client_fingerprint": "75fb48a465416d66291fb52a733d4787",
                            "is_established": true,
                            "cipher_suite": "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA",
                            "cert_file_uids": "FJLWw6HyYpcMakddb01",
                            "elliptic_curve": "secp384r1",
                            "ssl_version": "TLS1.0",
                            "ja3s_server_fingerprint": "bcf3a836c82d12ee988005fb0c011445",
                            "server_certificate_ref": "5"
                        }
                    }
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
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
            "first_observed": "2022-04-28T13:08:42.914Z",
            "last_observed": "2022-04-28T13:08:42.914Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--d7368305-07e1-45b1-a4d2-d9f884e6feb3",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-28T13:08:42.914Z",
            "modified": "2022-04-28T13:08:42.914Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-04-28T11:03:03.000Z",
                    "code": "CHYiyQ2wN9xp5ovzId01"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 58751,
                    "dst_port": 3389,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "protocols": [
                        "ssl"
                    ],
                    "extensions": {
                        "x-darktrace-ssl": {
                            "total_ciphers": 50,
                            "validation_status": "unable to get local issuer certificate",
                            "is_client_hello_seen": true,
                            "ja3_client_fingerprint": "75fb48a465416d66291fb52a733d4787",
                            "is_established": true,
                            "cipher_suite": "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA",
                            "cert_file_uids": "FUUWZb4Z4a42mnS86801",
                            "elliptic_curve": "secp384r1",
                            "ssl_version": "TLS1.0",
                            "ja3s_server_fingerprint": "bcf3a836c82d12ee988005fb0c011445",
                            "server_certificate_ref": "5"
                        }
                    }
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
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
            "first_observed": "2022-04-28T13:08:42.914Z",
            "last_observed": "2022-04-28T13:08:42.914Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--49b46de5-f994-4a40-96f1-81fc4dad5e5e",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-28T13:08:42.914Z",
            "modified": "2022-04-28T13:08:42.914Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-04-28T11:02:49.000Z",
                    "code": "CyBGMQ1drDaoXjSK3g01"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 34867,
                    "dst_port": 3389,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "protocols": [
                        "ssl"
                    ],
                    "extensions": {
                        "x-darktrace-ssl": {
                            "total_ciphers": 55,
                            "validation_status": "unable to get local issuer certificate",
                            "is_client_hello_seen": true,
                            "ja3_client_fingerprint": "0b63812a99e66c82a20d30c3b9ba6e06",
                            "is_established": true,
                            "cipher_suite": "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA",
                            "cert_file_uids": "Fafou13BJ66JIuCLok01",
                            "elliptic_curve": "secp384r1",
                            "ssl_version": "TLS1.0",
                            "ja3s_server_fingerprint": "bcf3a836c82d12ee988005fb0c011445",
                            "server_certificate_ref": "5"
                        }
                    }
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
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
            "first_observed": "2022-04-28T13:08:42.914Z",
            "last_observed": "2022-04-28T13:08:42.914Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--ead53aeb-16ce-4bac-a233-67fbb1220d51",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-28T13:08:42.914Z",
            "modified": "2022-04-28T13:08:42.914Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-04-28T11:02:27.000Z",
                    "code": "CDR0Nv21toSvrOcpU01"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 52837,
                    "dst_port": 3389,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "protocols": [
                        "ssl"
                    ],
                    "extensions": {
                        "x-darktrace-ssl": {
                            "total_ciphers": 50,
                            "validation_status": "unable to get local issuer certificate",
                            "is_client_hello_seen": true,
                            "ja3_client_fingerprint": "75fb48a465416d66291fb52a733d4787",
                            "is_established": true,
                            "cipher_suite": "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA",
                            "cert_file_uids": "FcgYKX3Gz9akuSeD7c01",
                            "elliptic_curve": "secp384r1",
                            "ssl_version": "TLS1.0",
                            "ja3s_server_fingerprint": "bcf3a836c82d12ee988005fb0c011445",
                            "server_certificate_ref": "5"
                        }
                    }
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
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
            "first_observed": "2022-04-28T13:08:42.914Z",
            "last_observed": "2022-04-28T13:08:42.914Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--3584eaed-af03-41b1-afc1-79b7437fa8ac",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-28T13:08:42.914Z",
            "modified": "2022-04-28T13:08:42.914Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-04-28T11:02:20.000Z",
                    "code": "C3RDFn3kisVFzMRMg01"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 60052,
                    "dst_port": 3389,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "protocols": [
                        "ssl"
                    ],
                    "extensions": {
                        "x-darktrace-ssl": {
                            "total_ciphers": 50,
                            "validation_status": "unable to get local issuer certificate",
                            "is_client_hello_seen": true,
                            "ja3_client_fingerprint": "75fb48a465416d66291fb52a733d4787",
                            "is_established": true,
                            "cipher_suite": "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA",
                            "cert_file_uids": "FttvZK16zOjSrTz8X301",
                            "elliptic_curve": "secp384r1",
                            "ssl_version": "TLS1.0",
                            "ja3s_server_fingerprint": "bcf3a836c82d12ee988005fb0c011445",
                            "server_certificate_ref": "5"
                        }
                    }
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
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
            "first_observed": "2022-04-28T13:08:42.914Z",
            "last_observed": "2022-04-28T13:08:42.914Z",
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
