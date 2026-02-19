# Darktrace

## Supported STIX Mappings

See the [table of mappings](darktrace_supported_stix.md) for the STIX objects and operators supported by this connector.

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
    "id": "bundle--9c117c3b-a4d8-4f52-8c3d-8381a6512112",
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
            "id": "observed-data--3e83dba4-2125-495f-af23-48f323530069",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-05-09T07:30:14.830Z",
            "modified": "2022-05-09T07:30:14.830Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-03-22T10:58:06.000Z",
                    "code": "CEfQ2a2ObXcyNJUvEk01"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 24178,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "dst_port": 3389,
                    "protocols": [
                        "null"
                    ]
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
                },
                "5": {
                    "type": "x509-certificate",
                    "validity_not_before": "2022-08-15T11:22:14.000Z",
                    "extensions": {
                        "x-darktrace-x509": {
                            "file_id": "FxWXXc1uH1zQNF66T701",
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
            "first_observed": "2022-05-09T07:30:14.830Z",
            "last_observed": "2022-05-09T07:30:14.830Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--3a0b3a54-b6fe-4a67-b114-0be8a5fa494b",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-05-09T07:30:14.833Z",
            "modified": "2022-05-09T07:30:14.833Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "created": "2022-03-22T10:58:06.000Z",
                    "code": "CEfQ2a2ObXcyNJUvEk01"
                },
                "1": {
                    "type": "network-traffic",
                    "src_port": 24178,
                    "dst_port": 3389,
                    "src_ref": "2",
                    "dst_ref": "4",
                    "protocols": [
                        "null"
                    ]
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
                },
                "5": {
                    "type": "x509-certificate",
                    "extensions": {
                        "x-darktrace-ssl": {
                            "total_ciphers": 28,
                            "validation_status": "unable to get local issuer certificate",
                            "is_client_hello_seen": true,
                            "ja3_client_fingerprint": "043c543b63b895881d9abfbc320cb863",
                            "is_established": true,
                            "cipher_suite": "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
                            "cert_file_uids": "FxWXXc1uH1zQNF66T701",
                            "elliptic_curve": "secp384r1",
                            "ja3s_server_fingerprint": "ae4edc6faf64d08308082ad26be60767"
                        }
                    },
                    "issuer": "CN=EC2AMAZ-2GNPPAQ",
                    "version": "TLS1.2",
                    "subject": "CN=EC2AMAZ-2GNPPAQ"
                }
            },
            "first_observed": "2022-05-09T07:30:14.833Z",
            "last_observed": "2022-05-09T07:30:14.833Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```

### Multiple Observation  

####STIX Translate query
```shell
translate darktrace query '{}' "[ipv4-addr:value = '0.0.0.0' AND x509-certificate:extensions.'x-darktrace-ssl'.elliptic_curve ='secp384r1'] START t'2022-03-21T11:00:00.000Z' STOP t'2022-03-22T11:05:00.003Z'"
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
"[x509-certificate:extensions.'x-darktrace-ssl'.elliptic_curve ='secp384r1'] START t'2022-04-25T11:00:00.000Z' STOP t'2022-04-28T11:05:00.003Z'"
```
#### STIX Execute query - output
```json
{
    "type": "bundle",
    "id": "bundle--6c59781b-4f5c-40bd-9605-2d8ded54ec63",
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
            "id": "observed-data--940b44a6-9258-40fc-8fe8-0062076fc701",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-05-09T07:51:09.876Z",
            "modified": "2022-05-09T07:51:09.876Z",
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
                    ]
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "123.253.14.12"
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "172.31.81.98"
                },
                "5": {
                    "type": "x509-certificate",
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
                            "ja3s_server_fingerprint": "bcf3a836c82d12ee988005fb0c011445",
                            "is_resumed": false
                        }
                    },
                    "issuer": "CN=EC2AMAZ-2GNPPAQ",
                    "version": "TLS1.0",
                    "subject": "CN=EC2AMAZ-2GNPPAQ"
                }
            },
            "first_observed": "2022-05-09T07:51:09.876Z",
            "last_observed": "2022-05-09T07:51:09.876Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--976158ba-217d-436b-a2c7-352f80e0592f",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-05-09T07:51:09.876Z",
            "modified": "2022-05-09T07:51:09.876Z",
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
                    ]
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "149.56.29.150"
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "172.31.81.98"
                },
                "5": {
                    "type": "x509-certificate",
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
                            "ja3s_server_fingerprint": "bcf3a836c82d12ee988005fb0c011445",
                            "is_resumed": false
                        }
                    },
                    "issuer": "CN=EC2AMAZ-2GNPPAQ",
                    "version": "TLS1.0",
                    "subject": "CN=EC2AMAZ-2GNPPAQ"
                }
            },
            "first_observed": "2022-05-09T07:51:09.876Z",
            "last_observed": "2022-05-09T07:51:09.876Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--ac6ef37d-773d-4e9f-9559-c13ed45288ef",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-05-09T07:51:09.876Z",
            "modified": "2022-05-09T07:51:09.876Z",
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
                    ]
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "181.48.90.197"
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "172.31.81.98"
                },
                "5": {
                    "type": "x509-certificate",
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
                            "ja3s_server_fingerprint": "bcf3a836c82d12ee988005fb0c011445",
                            "is_resumed": false
                        }
                    },
                    "issuer": "CN=EC2AMAZ-2GNPPAQ",
                    "version": "TLS1.0",
                    "subject": "CN=EC2AMAZ-2GNPPAQ"
                }
            },
            "first_observed": "2022-05-09T07:51:09.876Z",
            "last_observed": "2022-05-09T07:51:09.876Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--5e5c42c2-6e6f-4f75-ab17-784deb448b43",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-05-09T07:51:09.876Z",
            "modified": "2022-05-09T07:51:09.876Z",
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
                    ]
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "129.153.22.227"
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "172.31.81.98"
                },
                "5": {
                    "type": "x509-certificate",
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
                            "ja3s_server_fingerprint": "bcf3a836c82d12ee988005fb0c011445",
                            "is_resumed": false
                        }
                    },
                    "issuer": "CN=EC2AMAZ-2GNPPAQ",
                    "version": "TLS1.0",
                    "subject": "CN=EC2AMAZ-2GNPPAQ"
                }
            },
            "first_observed": "2022-05-09T07:51:09.876Z",
            "last_observed": "2022-05-09T07:51:09.876Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--d1fdd9b7-cea9-4d6f-ad16-bb20abbe9522",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-05-09T07:51:09.876Z",
            "modified": "2022-05-09T07:51:09.876Z",
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
                    ]
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "193.142.146.135"
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "172.31.81.98"
                },
                "5": {
                    "type": "x509-certificate",
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
                            "ja3s_server_fingerprint": "bcf3a836c82d12ee988005fb0c011445",
                            "is_resumed": false
                        }
                    },
                    "issuer": "CN=EC2AMAZ-2GNPPAQ",
                    "version": "TLS1.0",
                    "subject": "CN=EC2AMAZ-2GNPPAQ"
                }
            },
            "first_observed": "2022-05-09T07:51:09.876Z",
            "last_observed": "2022-05-09T07:51:09.876Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--e46d6472-f224-4e03-b4a3-952c5116dda8",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-05-09T07:51:09.876Z",
            "modified": "2022-05-09T07:51:09.876Z",
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
                    ]
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "92.255.85.123"
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "172.31.81.98"
                },
                "5": {
                    "type": "x509-certificate",
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
                            "ja3s_server_fingerprint": "bcf3a836c82d12ee988005fb0c011445",
                            "is_resumed": false
                        }
                    },
                    "issuer": "CN=EC2AMAZ-2GNPPAQ",
                    "version": "TLS1.0",
                    "subject": "CN=EC2AMAZ-2GNPPAQ"
                }
            },
            "first_observed": "2022-05-09T07:51:09.876Z",
            "last_observed": "2022-05-09T07:51:09.876Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--9218111a-afb7-41bd-b2fa-a8638ac20645",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-05-09T07:51:09.876Z",
            "modified": "2022-05-09T07:51:09.876Z",
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
                    ]
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "77.83.36.225"
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "172.31.81.98"
                },
                "5": {
                    "type": "x509-certificate",
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
                            "ja3s_server_fingerprint": "bcf3a836c82d12ee988005fb0c011445",
                            "is_resumed": false
                        }
                    },
                    "issuer": "CN=EC2AMAZ-2GNPPAQ",
                    "version": "TLS1.0",
                    "subject": "CN=EC2AMAZ-2GNPPAQ"
                }
            },
            "first_observed": "2022-05-09T07:51:09.876Z",
            "last_observed": "2022-05-09T07:51:09.876Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--5f64d451-7e7d-4f3b-8afd-bbb9e65ab2e6",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-05-09T07:51:09.876Z",
            "modified": "2022-05-09T07:51:09.876Z",
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
                    ]
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "92.255.85.200"
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "172.31.81.98"
                },
                "5": {
                    "type": "x509-certificate",
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
                            "ja3s_server_fingerprint": "bcf3a836c82d12ee988005fb0c011445",
                            "is_resumed": false
                        }
                    },
                    "issuer": "CN=EC2AMAZ-2GNPPAQ",
                    "version": "TLS1.0",
                    "subject": "CN=EC2AMAZ-2GNPPAQ"
                }
            },
            "first_observed": "2022-05-09T07:51:09.876Z",
            "last_observed": "2022-05-09T07:51:09.876Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--c03eb790-fbe8-4a20-bb59-660a6cb900a5",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-05-09T07:51:09.876Z",
            "modified": "2022-05-09T07:51:09.876Z",
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
                    ]
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "92.255.85.118"
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "172.31.81.98"
                },
                "5": {
                    "type": "x509-certificate",
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
                            "ja3s_server_fingerprint": "bcf3a836c82d12ee988005fb0c011445",
                            "is_resumed": false
                        }
                    },
                    "issuer": "CN=EC2AMAZ-2GNPPAQ",
                    "version": "TLS1.0",
                    "subject": "CN=EC2AMAZ-2GNPPAQ"
                }
            },
            "first_observed": "2022-05-09T07:51:09.876Z",
            "last_observed": "2022-05-09T07:51:09.876Z",
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
-  Query will return those records in the specified timeframe which satisfy the applied search filters. If there are no records in the given timeframe, search filter won't be applied and "Invalid parameter" error will be returned.
-  It is observed that Darktrace API returns 'timed out' error if translated query string length is more than MAX_QUERY_LENGTH. To avoid this error, query is split at 'OR' conditions and multiple requests are made to darktrace to get the result. However, the part of query joined by 'AND' operator won't be split and 'timed out' error is returned if the length of that part is beyond MAX_QUERY_LENGTH.