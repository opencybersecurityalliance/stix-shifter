# Splunk Enterprise

## Supported STIX Mappings

See the [table of mappings](splunk_supported_stix.md) for the STIX objects and operators supported by this connector.

**Table of Contents**

- [Splunk API Endpoints](#splunk-api-endpoints)
- [Pattern expression with STIX attributes - Single Observation](#single-observation)
- [Pattern expression with STIX attributes - Multiple Observation](#multiple-observation)
- [Pattern expression with STIX attributes - Execute Query](#stix-execute-query)
- [References](#references)

### Splunk API Endpoints

   |Connector Method|Splunk API Endpoint| Method
   | ----           |   ------              | -----|
   |Ping Endpoint   |https://<server_ip>:<port>/services/|GET
   |Query Endpoint  |https://<server_ip>:<port>/services/search/jobs|POST
   |Result Endpoint|https://<server_ip>:<port>/services/search/v2/jobs/<search_id>/results|GET
   
### Format for calling stix-shifter from the command line
```
python main.py `<translate or transmit>` `<translator_module>` `<query or result>` `<STIX identity object>` `<data>`
```
### Pattern expression with STIX attributes

### Single Observation

#### STIX Translate query
```shell
translate splunk query "{}" "[ipv4-addr:value = '1.1.1.1'] START t'2023-01-01T11:00:00.000Z' STOP t'2023-03-08T11:00:00.003Z'"
```
#### STIX Translate query - output
```json
{
    "queries": [
        "search ((src_ip = \"1.1.1.1\") OR (dest_ip = \"1.1.1.1\")) earliest=\"01/01/2023:11:00:00\" latest=\"03/08/2023:11:00:00\" | head 10000 | fields src_ip, src_port, src_mac, dest_ip, dest_port, dest_mac, file_hash, user, url, protocol, host, source, severity, process, process_id, process_name, process_exec, process_path, process_hash, process_guid, parent_process, parent_process_id, parent_process_name, parent_process_exec, description, signature, signature_id, query, answer, transport, bytes_in, bytes_out, packets_in, packets_out, direction, name, message_type, query_count, query_type, record_type, reply_code, reply_code_id, vendor_product, duration, transaction_id, action, file_access_time, file_acl, registry_hive, registry_path, registry_key_name, registry_value_data, registry_value_name, registry_value_text, registry_value_type, status, ssl_version, ssl_serial, ssl_issuer, ssl_subject, ssl_signature_algorithm, ssl_publickey_algorithm, ssl_start_time, ssl_end_time, ssl_is_valid, ssl_issuer_common_name, ssl_subject_common_name, ssl_name, ssl_publickey, ssl_issuer_email, ssl_subject_email, ssl_issuer_email_domain, ssl_subject_email_domain, ssl_issuer_organization, ssl_subject_organization, recipient, subject, file_hash, file_name, file_size, recipient_domain, src_user_domain, internal_message_id, message_id, message_info, app, authentication_method, authentication_service, dest, src, src_user, user_name, user_id, user_type, user_agent, http_method, http_referrer, http_user_agent, uri_path, uri_query, os, dvc, id, msft, cve, cvss, mskb, type, eventtype, event_id, mitre_technique_id, mem_used, original_file_name, file_create_time, file_modify_time"
    ]
}
```
#### STIX Transmit ping 

```shell
transmit
splunk
"{\"host\":\"xxxx\",\"port\": xxxx,\"selfSignedCert\": \"-----BEGIN PRIVATE KEY-----\n\n-----END PRIVATE KEY-----\n-----BEGIN CERTIFICATE-----\n\n-----END CERTIFICATE-----\"}"
"{\"auth\":{\"username\": \"xxxx\", \"password\": \"xxxx\"}}"
ping
```

#### STIX Transmit ping - output
```json
{
    "success": true
}
```
#### STIX Transmit query 

```shell
transmit
splunk
"{\"host\":\"xxxx\",\"port\": xxxx,\"selfSignedCert\": \"-----BEGIN PRIVATE KEY-----\n\n-----END PRIVATE KEY-----\n-----BEGIN CERTIFICATE-----\n\n-----END CERTIFICATE-----\"}"
"{\"auth\":{\"username\": \"xxxx\", \"password\": \"xxxx\"}}"
query
"search ((src_ip = \"1.1.1.1\") OR (dest_ip = \"1.1.1.1\")) earliest=\"01/01/2023:11:00:00\" latest=\"03/08/2023:11:00:00\" | head 10000 | fields src_ip, src_port, src_mac, dest_ip, dest_port, dest_mac, file_hash, user, url, protocol, host, source, severity, process, process_id, process_name, process_exec, process_path, process_hash, process_guid, parent_process, parent_process_id, parent_process_name, parent_process_exec, description, signature, signature_id, query, answer, transport, bytes_in, bytes_out, packets_in, packets_out, direction, name, message_type, query_count, query_type, record_type, reply_code, reply_codeid, vendor_product, duration, transaction_id, action, file_access_time, file_acl, registry_hive, registry_path, registry_key_name, registry_value_data, registry_value_name, registry_value_text, registry_value_type, status, ssl_version, ssl_serial, ssl_issuer, ssl_subject, ssl_signature_algorithm, ssl_publickey_algorithm, ssl_start_time, ssl_end_time, ssl_is_valid, ssl_issuer_common_name, ssl_subject_common_name, ssl_name, ssl_publickey, ssl_issuer_email, ssl_subject_email, ssl_issuer_email_domain, ssl_subject_email_domain, ssl_issuer_organization, ssl_subject_organization, recipient, subject, file_hash, file_name, file_size, recipient_domain, src_user_domain, internal_message_id, message_id, message_info, app, authentication_method, authentication_service, dest, src, src_user, user_name, user_id, user_type, user_agent, http_method, http_referrer, http_user_agent, uri_path, uri_query, os, dvc, id, msft, cve, cvss, mskb, type, eventtype, event_id, mitre_technique_id, mem_used, original_file_name, original_file_name, file_create_time, file_modify_time"
```

#### STIX Transmit query - output
```json
{
    "success": true,
    "search_id": "xxxxx"
}
```
#### STIX Transmit status 

```shell
transmit
splunk
"{\"host\":\"xxxx\",\"port\": xxxx,\"selfSignedCert\": \"-----BEGIN PRIVATE KEY-----\n\n-----END PRIVATE KEY-----\n-----BEGIN CERTIFICATE-----\n\n-----END CERTIFICATE-----\"}"
"{\"auth\":{\"username\": \"xxxx\", \"password\": \"xxxx\"}}"
status
"xxxxxx"
```

#### STIX Transmit status - output
```json
{
    "success": true,
    "status": "RUNNING",
    "progress": 3
}
```
#### STIX Transmit results 

```shell
transmit
splunk
"{\"host\":\"xxxx\",\"port\": xxxx,\"selfSignedCert\": \"-----BEGIN PRIVATE KEY-----\n\n-----END PRIVATE KEY-----\n-----BEGIN CERTIFICATE-----\n\n-----END CERTIFICATE-----\"}"
"{\"auth\":{\"username\": \"xxxx\", \"password\": \"xxxx\"}}"
results
"xxxxxx"
0
1
```

#### STIX Transmit results - output
```json
{
    "success": true,
    "data": [
        {
            "src_ip": "1.1.1.1",
            "src_port": null,
            "dest_ip": "1.1.1.1",
            "dest_port": null,
            "user": "xxxx",
            "protocol": "ip",
            "host": "xxxx",
            "source": "xxxx",
            "process_id": "532",
            "process_name": "xxxx",
            "process_exec": null,
            "process_guid": "xxxxx",
            "signature": "Network connection",
            "signature_id": "3",
            "transport": "tcp",
            "direction": "inbound",
            "vendor_product": "Microsoft Sysmon",
            "action": "allowed",
            "app": "C:\\Windows\\System32\\svchost.exe",
            "dest": null,
            "src": null,
            "user_id": "'S-1-5-18'",
            "dvc": "xxxxx",
            "id": "9383",
            "eventtype": [
                "corelight_idx",
                "endpoint_services_processes",
                "ms-sysmon-network",
                "windows_event_signature"
            ],
            "event_id": "9383",
            "_bkt": "main~9~FF7D676A-5C1A-492E-9A6D-4653BFD400A6",
            "_cd": "9:31677",
            "_eventtype_color": "none",
            "_indextime": "1676460270",
            "_raw": "xxxx",
            "_serial": "0",
            "_si": [
                "xxxxxx",
                "main"
            ],
            "_sourcetype": "XmlWinEventLog",
            "_time": "2023-01-11T15:29:45.000+00:00",
            "name": null,
            "query_count": null,
            "query_type": null,
            "networkdata": {
                "src_port": "60318",
                "dest_port": "3389",
                "protocol": "ip",
                "transport": "tcp",
                "direction": "inbound"
            },
            "file_hash": null,
            "file_hashes": {}
        }
    ]
}
```


#### STIX Translate results

```shell
translate
splunk
results
"{\"type\": \"identity\", \"id\": \"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\", \"name\": \"splunk\", \"identity_class\": \"events\", \"created\": \"2022-03-22T13:22:50.336Z\", \"modified\": \"2022-03-22T13:22:50.336Z\"}"
"[ { \"src_ip\": \"1.1.1.1\", \"src_port\": null, \"dest_ip\": \"1.1.1.1\", \"dest_port\": null, \"user\": \"NETWORK SERVICE\", \"protocol\": \"ip\", \"host\": \"xxxxx\", \"source\": \"XmlWinEventLog:Microsoft-Windows-Sysmon/Operational\", \"process_id\": \"532\", \"process_name\": \"svchost.exe\", \"process_exec\": null, \"process_guid\": \"xxxxx\", \"signature\": \"Network connection\", \"signature_id\": \"3\", \"transport\": \"tcp\", \"direction\": \"inbound\", \"vendor_product\": \"Microsoft Sysmon\", \"action\": \"allowed\", \"app\": \"C:\\Windows\\System32\\svchost.exe\", \"dest\": null, \"src\": null, \"user_id\": \"'S-1-5-18'\", \"dvc\": \"xxxxx\", \"id\": \"9383\", \"eventtype\": [ \"corelight_idx\", \"endpoint_services_processes\", \"ms-sysmon-network\", \"windows_event_signature\" ], \"event_id\": \"9383\", \"_bkt\": \"main~9~FF7D676A-5C1A-492E-9A6D-4653BFD400A6\", \"_cd\": \"9:31677\", \"_eventtype_color\": \"none\", \"_indextime\": \"1676460270\", \"_raw\": \"<Event xmlns='http://schemas.microsoft.com/win/2004/08/events/event'><System><Provider Name='Microsoft-Windows-Sysmon' Guid='{5770385f-c22a-43e0-bf4c-06f5698ffbd9}'/><EventID>3</EventID><Version>5</Version><Level>4</Level><Task>3</Task><Opcode>0</Opcode><Keywords>0x8000000000000000</Keywords><TimeCreated SystemTime='2023-01-11T15:29:45.8322874Z'/><EventRecordID>9383</EventRecordID><Correlation/><Execution ProcessID='1888' ThreadID='2956'/><Channel>Microsoft-Windows-Sysmon/Operational</Channel><Computer>xxxxx</Computer><Security UserID='S-1-5-18'/></System><EventData><Data Name='RuleName'>technique_id=T1021,technique_name=Remote Services</Data><Data Name='UtcTime'>2023-01-11 15:29:43.732</Data><Data Name='ProcessGuid'>xxxxxx</Data><Data Name='ProcessId'>532</Data><Data Name='Image'>C:\\Windows\\System32\\svchost.exe</Data><Data Name='User'>NT AUTHORITY\\NETWORK SERVICE</Data><Data Name='Protocol'>tcp</Data><Data Name='Initiated'>false</Data><Data Name='SourceIsIpv6'>false</Data><Data Name='SourceIp'>198.235.24.155</Data><Data Name='SourceHostname'>-</Data><Data Name='SourcePort'>60318</Data><Data Name='SourcePortName'>-</Data><Data Name='DestinationIsIpv6'>false</Data><Data Name='DestinationIp'>172.31.29.79</Data><Data Name='DestinationHostname'>-</Data><Data Name='DestinationPort'>3389</Data><Data Name='DestinationPortName'>-</Data></EventData></Event>\", \"_serial\": \"0\", \"_si\": [ \"xxxxx\", \"main\" ], \"_sourcetype\": \"XmlWinEventLog\", \"_time\": \"2023-01-11T15:29:45.000+00:00\", \"name\": null, \"query_count\": null, \"query_type\": null, \"networkdata\": { \"src_port\": \"60318\", \"dest_port\": \"3389\", \"protocol\": \"ip\", \"transport\": \"tcp\", \"direction\": \"inbound\" }, \"file_hash\": null, \"file_hashes\": {} } ]"
```

#### STIX Translate results - output
```json
{
    "type": "bundle",
    "id": "bundle--e41614dc-a4c3-49b7-a95b-467cf75ef2d9",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "splunk",
            "identity_class": "events",
            "created": "2022-03-22T13:22:50.336Z",
            "modified": "2022-03-22T13:22:50.336Z"
        },
        {
            "id": "observed-data--4d3a2d6c-c8f2-4f83-a36e-cbf0565968aa",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2023-05-08T13:12:54.984Z",
            "modified": "2023-05-08T13:12:54.984Z",
            "objects": {
                "0": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "1": {
                    "type": "network-traffic",
                    "src_ref": "0",
                    "dst_ref": "4",
                    "src_port": 60318,
                    "dst_port": 3389,
                    "protocols": [
                        "ip",
                        "tcp"
                    ],
                    "x_direction": "inbound"
                },
                "2": {
                    "type": "x-oca-event",
                    "ip_refs": [
                        "0",
                        "4"
                    ],
                    "user_ref": "5",
                    "host_ref": "6",
                    "module": "XmlWinEventLog:Microsoft-Windows-Sysmon/Operational",
                    "process_ref": "8",
                    "action": "Network connection",
                    "code": "3",
                    "provider": "Microsoft Sysmon",
                    "outcome": "allowed",
                    "x_application": "C:\\Windows\\System32\\svchost.exe",
                    "x_event_id": "9383",
                    "original_ref": "10",
                    "created": "2023-01-11T15:29:45.000Z",
                    "network_ref": "1"
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "5": {
                    "type": "user-account",
                    "user_id": "NETWORK SERVICE",
                    "account_login": "'S-1-5-18'"
                },
                "6": {
                    "type": "x-oca-asset",
                    "hostname": "xxxxx"
                },
                "7": {
                    "type": "x-splunk-data",
                    "log_source": "XmlWinEventLog:Microsoft-Windows-Sysmon/Operational",
                    "event_type": [
                        "corelight_idx",
                        "endpoint_services_processes",
                        "ms-sysmon-network",
                        "windows_event_signature"
                    ],
                    "log_source_type": "XmlWinEventLog"
                },
                "8": {
                    "type": "process",
                    "pid": 532,
                    "name": "svchost.exe",
                    "binary_ref": "9",
                    "x_unique_id": "xxxxx",
                    "opened_connection_refs": [
                        "1"
                    ]
                },
                "9": {
                    "type": "file",
                    "name": "svchost.exe"
                },
                "10": {
                    "type": "artifact",
                    "payload_bin": "PEV2ZW50IHhtbG5zPSdodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dpbi8yMDA0LzA4L2V2ZW50cy9ldmVudCc+PFN5c3RlbT48UHJvdmlkZXIgTmFtZT0nTWljcm9zb2Z0LVdpbmRvd3MtU3lzbW9uJyBHdWlkPSd7NTc3MDM4NWYtYzIyYS00M2UwLWJmNGMtMDZmNTY5OGZmYmQ5fScvPjxFdmVudElEPjM8L0V2ZW50SUQ+PFZlcnNpb24+NTwvVmVyc2lvbj48TGV2ZWw+NDwvTGV2ZWw+PFRhc2s+MzwvVGFzaz48T3Bjb2RlPjA8L09wY29kZT48S2V5d29yZHM+MHg4MDAwMDAwMDAwMDAwMDAwPC9LZXl3b3Jkcz48VGltZUNyZWF0ZWQgU3lzdGVtVGltZT0nMjAyMy0wMS0xMVQxNToyOTo0NS44MzIyODc0WicvPjxFdmVudFJlY29yZElEPjkzODM8L0V2ZW50UmVjb3JkSUQ+PENvcnJlbGF0aW9uLz48RXhlY3V0aW9uIFByb2Nlc3NJRD0nMTg4OCcgVGhyZWFkSUQ9JzI5NTYnLz48Q2hhbm5lbD5NaWNyb3NvZnQtV2luZG93cy1TeXNtb24vT3BlcmF0aW9uYWw8L0NoYW5uZWw+PENvbXB1dGVyPkVDMkFNQVotTzRLQ1VLMzwvQ29tcHV0ZXI+PFNlY3VyaXR5IFVzZXJJRD0nUy0xLTUtMTgnLz48L1N5c3RlbT48RXZlbnREYXRhPjxEYXRhIE5hbWU9J1J1bGVOYW1lJz50ZWNobmlxdWVfaWQ9VDEwMjEsdGVjaG5pcXVlX25hbWU9UmVtb3RlIFNlcnZpY2VzPC9EYXRhPjxEYXRhIE5hbWU9J1V0Y1RpbWUnPjIwMjMtMDEtMTEgMTU6Mjk6NDMuNzMyPC9EYXRhPjxEYXRhIE5hbWU9J1Byb2Nlc3NHdWlkJz57N2E5N2I4NWYtNDU1MC02M2JlLTEzMDAtMDAwMDAwMDA3ZDAwfTwvRGF0YT48RGF0YSBOYW1lPSdQcm9jZXNzSWQnPjUzMjwvRGF0YT48RGF0YSBOYW1lPSdJbWFnZSc+QzpcV2luZG93c1xTeXN0ZW0zMlxzdmNob3N0LmV4ZTwvRGF0YT48RGF0YSBOYW1lPSdVc2VyJz5OVCBBVVRIT1JJVFlcTkVUV09SSyBTRVJWSUNFPC9EYXRhPjxEYXRhIE5hbWU9J1Byb3RvY29sJz50Y3A8L0RhdGE+PERhdGEgTmFtZT0nSW5pdGlhdGVkJz5mYWxzZTwvRGF0YT48RGF0YSBOYW1lPSdTb3VyY2VJc0lwdjYnPmZhbHNlPC9EYXRhPjxEYXRhIE5hbWU9J1NvdXJjZUlwJz4xOTguMjM1LjI0LjE1NTwvRGF0YT48RGF0YSBOYW1lPSdTb3VyY2VIb3N0bmFtZSc+LTwvRGF0YT48RGF0YSBOYW1lPSdTb3VyY2VQb3J0Jz42MDMxODwvRGF0YT48RGF0YSBOYW1lPSdTb3VyY2VQb3J0TmFtZSc+LTwvRGF0YT48RGF0YSBOYW1lPSdEZXN0aW5hdGlvbklzSXB2Nic+ZmFsc2U8L0RhdGE+PERhdGEgTmFtZT0nRGVzdGluYXRpb25JcCc+MTcyLjMxLjI5Ljc5PC9EYXRhPjxEYXRhIE5hbWU9J0Rlc3RpbmF0aW9uSG9zdG5hbWUnPi08L0RhdGE+PERhdGEgTmFtZT0nRGVzdGluYXRpb25Qb3J0Jz4zMzg5PC9EYXRhPjxEYXRhIE5hbWU9J0Rlc3RpbmF0aW9uUG9ydE5hbWUnPi08L0RhdGE+PC9FdmVudERhdGE+PC9FdmVudD4=",
                    "mime_type": "text/plain"
                }
            },
            "first_observed": "2023-01-11T15:29:45.000Z",
            "last_observed": "2023-01-11T15:29:45.000Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```

### Multiple Observation  

#### STIX Translate query
```shell
translate
splunk
query
"{}"
"[network-traffic:src_ref.value = '1.1.1.1'] AND [network-traffic:dst_ref.value ='2.2.2.2'] START t'2023-01-01T11:00:00.000Z' STOP t'2023-02-28T11:00:00.003Z'"
```

#### STIX Translate query - output

```json
{
    "queries": [
        "search (src_ip = \"1.1.1.1\") OR (dest_ip = \"2.2.2.2\") earliest=\"01/01/2023:11:00:00\" latest=\"02/28/2023:11:00:00\" | head 10000 | fields src_ip, src_port, src_mac, dest_ip, dest_port, dest_mac, file_hash, user, url, protocol, host, source, severity, process, process_id, process_name, process_exec, process_path, process_hash, process_guid, parent_process, parent_process_id, parent_process_name, parent_process_exec, description, signature, signature_id, query, answer, transport, bytes_in, bytes_out, packets_in, packets_out, direction, name, message_type, query_count, query_type, record_type, reply_code, reply_codeid, vendor_product, duration, transaction_id, action, file_access_time, file_acl, registry_hive, registry_path, registry_key_name, registry_value_data, registry_value_name, registry_value_text, registry_value_type, status, ssl_version, ssl_serial, ssl_issuer, ssl_subject, ssl_signature_algorithm, ssl_publickey_algorithm, ssl_start_time, ssl_end_time, ssl_is_valid, ssl_issuer_common_name, ssl_subject_common_name, ssl_name, ssl_publickey, ssl_issuer_email, ssl_subject_email, ssl_issuer_email_domain, ssl_subject_email_domain, ssl_issuer_organization, ssl_subject_organization, recipient, subject, file_hash, file_name, file_size, recipient_domain, src_user_domain, internal_message_id, message_id, message_info, app, authentication_method, authentication_service, dest, src, src_user, user_name, user_id, user_type, user_agent, http_method, http_referrer, http_user_agent, uri_path, uri_query, os, dvc, id, msft, cve, cvss, mskb, type, eventtype, event_id, mitre_technique_id, mem_used, original_file_name, original_file_name, file_create_time, file_modify_time"
    ]
}
```

#### STIX Transmit query

```shell
transmit
splunk
"{\"host\":\"xxxx\",\"port\": xxxx,\"selfSignedCert\": \"-----BEGIN PRIVATE KEY-----\n\n-----END PRIVATE KEY-----\n-----BEGIN CERTIFICATE-----\n\n-----END CERTIFICATE-----\"}"
"{\"auth\":{\"username\": \"xxxx\", \"password\": \"xxxx\"}}"
query
"search (src_ip = \"1.1.1.1\") OR (dest_ip = \"2.2.2.2\") earliest=\"01/01/2023:11:00:00\" latest=\"02/28/2023:11:00:00\" | head 10000 | fields src_ip, src_port, src_mac, dest_ip, dest_port, dest_mac, file_hash, user, url, protocol, host, source, severity, process, process_id, process_name, process_exec, process_path, process_hash, process_guid, parent_process, parent_process_id, parent_process_name, parent_process_exec, description, signature, signature_id, query, answer, transport, bytes_in, bytes_out, packets_in, packets_out, direction, name, message_type, query_count, query_type, record_type, reply_code, reply_codeid, vendor_product, duration, transaction_id, action, file_access_time, file_acl, registry_hive, registry_path, registry_key_name, registry_value_data, registry_value_name, registry_value_text, registry_value_type, status, ssl_version, ssl_serial, ssl_issuer, ssl_subject, ssl_signature_algorithm, ssl_publickey_algorithm, ssl_start_time, ssl_end_time, ssl_is_valid, ssl_issuer_common_name, ssl_subject_common_name, ssl_name, ssl_publickey, ssl_issuer_email, ssl_subject_email, ssl_issuer_email_domain, ssl_subject_email_domain, ssl_issuer_organization, ssl_subject_organization, recipient, subject, file_hash, file_name, file_size, recipient_domain, src_user_domain, internal_message_id, message_id, message_info, app, authentication_method, authentication_service, dest, src, src_user, user_name, user_id, user_type, user_agent, http_method, http_referrer, http_user_agent, uri_path, uri_query, os, dvc, id, msft, cve, cvss, mskb, type, eventtype, event_id, mitre_technique_id, mem_used, original_file_name, original_file_name, file_create_time, file_modify_time"
```

#### STIX Transmit query - output

```json
{
    "success": true,
    "search_id": "xxxxx"
}
```
#### STIX Transmit status 

```shell
transmit
splunk
"{\"host\":\"xxxx\",\"port\": xxxx,\"selfSignedCert\": \"-----BEGIN PRIVATE KEY-----\n\n-----END PRIVATE KEY-----\n-----BEGIN CERTIFICATE-----\n\n-----END CERTIFICATE-----\"}"
"{\"auth\":{\"username\": \"xxxx\", \"password\": \"xxxx\"}}"
status
"xxxxxx"
```

#### STIX Transmit status - output
```json
{
    "success": true,
    "status": "RUNNING",
    "progress": 3
}
```
#### STIX Transmit results 

```shell
transmit
splunk
"{\"host\":\"xxxx\",\"port\": xxxx,\"selfSignedCert\": \"-----BEGIN PRIVATE KEY-----\n\n-----END PRIVATE KEY-----\n-----BEGIN CERTIFICATE-----\n\n-----END CERTIFICATE-----\"}"
"{\"auth\":{\"username\": \"xxxx\", \"password\": \"xxxx\"}}"
results
"xxxxxx"
0
1
```

#### STIX Transmit results - output
```json
{
    "success": true,
    "data": [
        {
            "src_ip": "xxxx",
            "src_port": null,
            "dest_ip": "xxxx",
            "dest_port": null,
            "user": "NETWORK SERVICE",
            "protocol": "ip",
            "host": "xxxxx",
            "source": "XmlWinEventLog:Microsoft-Windows-Sysmon/Operational",
            "process_id": "1028",
            "process_name": "svchost.exe",
            "process_exec": null,
            "process_guid": "xxxx",
            "signature": "Network connection",
            "signature_id": "3",
            "transport": "tcp",
            "direction": "inbound",
            "vendor_product": "Microsoft Sysmon",
            "action": "allowed",
            "app": "C:\\Windows\\System32\\svchost.exe",
            "dest": null,
            "src": null,
            "user_id": "'S-1-5-18'",
            "dvc": "xxxxx",
            "id": "13220",
            "eventtype": [
                "corelight_idx",
                "endpoint_services_processes",
                "ms-sysmon-network",
                "windows_event_signature"
            ],
            "event_id": "13220",
            "_bkt": "main~9~FF7D676A-5C1A-492E-9A6D-4653BFD400A6",
            "_cd": "9:193619",
            "_eventtype_color": "none",
            "_indextime": "1676461141",
            "_raw": "xxxx",
            "_serial": "0",
            "_si": [
                "xxxxxx",
                "main"
            ],
            "_sourcetype": "XmlWinEventLog",
            "_time": "2023-02-15T11:38:26.000+00:00",
            "name": null,
            "query_count": null,
            "query_type": null,
            "networkdata": {
                "src_port": "61111",
                "dest_port": "3389",
                "protocol": "ip",
                "transport": "tcp",
                "direction": "inbound"
            },
            "file_hash": null,
            "file_hashes": {}
        }
    ]
}
```


#### STIX Translate results

```shell
translate
splunk
results
"{\"type\": \"identity\", \"id\": \"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\", \"name\": \"splunk\", \"identity_class\": \"events\", \"created\": \"2022-03-22T13:22:50.336Z\", \"modified\": \"2022-03-22T13:22:50.336Z\"}"
"[{ \"src_ip\": \"1.1.1.1\", \"src_port\": null, \"dest_ip\": \"2.2.2.2\", \"dest_port\": null, \"user\": \"NETWORK SERVICE\", \"protocol\": \"ip\", \"host\": \"xxxxx\", \"source\": \"XmlWinEventLog:Microsoft-Windows-Sysmon/Operational\", \"process_id\": \"1028\", \"process_name\": \"svchost.exe\", \"process_exec\": null, \"process_guid\": \"{7a97b85f-7dba-63ec-1300-000000007e00}\", \"signature\": \"Network connection\", \"signature_id\": \"3\", \"transport\": \"tcp\", \"direction\": \"inbound\", \"vendor_product\": \"Microsoft Sysmon\", \"action\": \"allowed\", \"app\": \"C:\\Windows\\System32\\svchost.exe\", \"dest\": null, \"src\": null, \"user_id\": \"'S-1-5-18'\", \"dvc\": \"xxxxx\", \"id\": \"13220\", \"eventtype\": [ \"corelight_idx\", \"endpoint_services_processes\", \"ms-sysmon-network\", \"windows_event_signature\" ], \"event_id\": \"13220\", \"_bkt\": \"main~9~FF7D676A-5C1A-492E-9A6D-4653BFD400A6\", \"_cd\": \"9:193619\", \"_eventtype_color\": \"none\", \"_indextime\": \"1676461141\", \"_raw\": \"<Event xmlns='http://schemas.microsoft.com/win/2004/08/events/event'><System><Provider Name='Microsoft-Windows-Sysmon' Guid='{5770385f-c22a-43e0-bf4c-06f5698ffbd9}'/><EventID>3</EventID><Version>5</Version><Level>4</Level><Task>3</Task><Opcode>0</Opcode><Keywords>0x8000000000000000</Keywords><TimeCreated SystemTime='2023-02-15T11:38:26.4054216Z'/><EventRecordID>13220</EventRecordID><Correlation/><Execution ProcessID='1528' ThreadID='3032'/><Channel>Microsoft-Windows-Sysmon/Operational</Channel><Computer>xxxxx</Computer><Security UserID='S-1-5-18'/></System><EventData><Data Name='RuleName'>technique_id=T1021,technique_name=Remote Services</Data><Data Name='UtcTime'>2023-02-15 11:38:24.751</Data><Data Name='ProcessGuid'>xxxxx</Data><Data Name='ProcessId'>1028</Data><Data Name='Image'>C:\\Windows\\System32\\svchost.exe</Data><Data Name='User'>NT AUTHORITY\\NETWORK SERVICE</Data><Data Name='Protocol'>tcp</Data><Data Name='Initiated'>false</Data><Data Name='SourceIsIpv6'>false</Data><Data Name='SourceIp'>xxxxx</Data><Data Name='SourceHostname'>-</Data><Data Name='SourcePort'>61111</Data><Data Name='SourcePortName'>-</Data><Data Name='DestinationIsIpv6'>false</Data><Data Name='DestinationIp'>xxxxx</Data><Data Name='DestinationHostname'>-</Data><Data Name='DestinationPort'>3389</Data><Data Name='DestinationPortName'>-</Data></EventData></Event>\", \"_serial\": \"0\", \"_si\": [ \"xxxxx\", \"main\" ], \"_sourcetype\": \"XmlWinEventLog\", \"_time\": \"2023-02-15T11:38:26.000+00:00\", \"name\": null, \"query_count\": null, \"query_type\": null, \"networkdata\": { \"src_port\": \"61111\", \"dest_port\": \"3389\", \"protocol\": \"ip\", \"transport\": \"tcp\", \"direction\": \"inbound\" }, \"file_hash\": null, \"file_hashes\": {} }]"
```

#### STIX Translate results - output
```json
{
    "type": "bundle",
    "id": "bundle--e8d34045-57ea-498c-b1fd-1644ce5c387c",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "splunk",
            "identity_class": "events",
            "created": "2022-03-22T13:22:50.336Z",
            "modified": "2022-03-22T13:22:50.336Z"
        },
        {
            "id": "observed-data--0c6e731b-38fe-4b76-a8a4-583fcd92535b",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2023-05-08T13:37:00.218Z",
            "modified": "2023-05-08T13:37:00.218Z",
            "objects": {
                "0": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "1": {
                    "type": "network-traffic",
                    "src_ref": "0",
                    "dst_ref": "4",
                    "src_port": 61111,
                    "dst_port": 3389,
                    "protocols": [
                        "ip",
                        "tcp"
                    ],
                    "x_direction": "inbound"
                },
                "2": {
                    "type": "x-oca-event",
                    "ip_refs": [
                        "0",
                        "4"
                    ],
                    "user_ref": "5",
                    "host_ref": "6",
                    "module": "XmlWinEventLog:Microsoft-Windows-Sysmon/Operational",
                    "process_ref": "8",
                    "action": "Network connection",
                    "code": "3",
                    "provider": "Microsoft Sysmon",
                    "outcome": "allowed",
                    "x_application": "C:\\Windows\\System32\\svchost.exe",
                    "x_event_id": "13220",
                    "original_ref": "10",
                    "created": "2023-02-15T11:38:26.000Z",
                    "network_ref": "1"
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "2.2.2.2"
                },
                "5": {
                    "type": "user-account",
                    "user_id": "NETWORK SERVICE",
                    "account_login": "'S-1-5-18'"
                },
                "6": {
                    "type": "x-oca-asset",
                    "hostname": "1.1.1.1"
                },
                "7": {
                    "type": "x-splunk-data",
                    "log_source": "XmlWinEventLog:Microsoft-Windows-Sysmon/Operational",
                    "event_type": [
                        "corelight_idx",
                        "endpoint_services_processes",
                        "ms-sysmon-network",
                        "windows_event_signature"
                    ],
                    "log_source_type": "XmlWinEventLog"
                },
                "8": {
                    "type": "process",
                    "pid": 1028,
                    "name": "svchost.exe",
                    "binary_ref": "9",
                    "x_unique_id": "xxxxxx",
                    "opened_connection_refs": [
                        "1"
                    ]
                },
                "9": {
                    "type": "file",
                    "name": "svchost.exe"
                },
                "10": {
                    "type": "artifact",
                    "payload_bin": "PEV2ZW50IHhtbG5zPSdodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dpbi8yMDA0LzA4L2V2ZW50cy9ldmVudCc+PFN5c3RlbT48UHJvdmlkZXIgTmFtZT0nTWljcm9zb2Z0LVdpbmRvd3MtU3lzbW9uJyBHdWlkPSd7NTc3MDM4NWYtYzIyYS00M2UwLWJmNGMtMDZmNTY5OGZmYmQ5fScvPjxFdmVudElEPjM8L0V2ZW50SUQ+PFZlcnNpb24+NTwvVmVyc2lvbj48TGV2ZWw+NDwvTGV2ZWw+PFRhc2s+MzwvVGFzaz48T3Bjb2RlPjA8L09wY29kZT48S2V5d29yZHM+MHg4MDAwMDAwMDAwMDAwMDAwPC9LZXl3b3Jkcz48VGltZUNyZWF0ZWQgU3lzdGVtVGltZT0nMjAyMy0wMi0xNVQxMTozODoyNi40MDU0MjE2WicvPjxFdmVudFJlY29yZElEPjEzMjIwPC9FdmVudFJlY29yZElEPjxDb3JyZWxhdGlvbi8+PEV4ZWN1dGlvbiBQcm9jZXNzSUQ9JzE1MjgnIFRocmVhZElEPSczMDMyJy8+PENoYW5uZWw+TWljcm9zb2Z0LVdpbmRvd3MtU3lzbW9uL09wZXJhdGlvbmFsPC9DaGFubmVsPjxDb21wdXRlcj5FQzJBTUFaLU80S0NVSzM8L0NvbXB1dGVyPjxTZWN1cml0eSBVc2VySUQ9J1MtMS01LTE4Jy8+PC9TeXN0ZW0+PEV2ZW50RGF0YT48RGF0YSBOYW1lPSdSdWxlTmFtZSc+dGVjaG5pcXVlX2lkPVQxMDIxLHRlY2huaXF1ZV9uYW1lPVJlbW90ZSBTZXJ2aWNlczwvRGF0YT48RGF0YSBOYW1lPSdVdGNUaW1lJz4yMDIzLTAyLTE1IDExOjM4OjI0Ljc1MTwvRGF0YT48RGF0YSBOYW1lPSdQcm9jZXNzR3VpZCc+ezdhOTdiODVmLTdkYmEtNjNlYy0xMzAwLTAwMDAwMDAwN2UwMH08L0RhdGE+PERhdGEgTmFtZT0nUHJvY2Vzc0lkJz4xMDI4PC9EYXRhPjxEYXRhIE5hbWU9J0ltYWdlJz5DOlxXaW5kb3dzXFN5c3RlbTMyXHN2Y2hvc3QuZXhlPC9EYXRhPjxEYXRhIE5hbWU9J1VzZXInPk5UIEFVVEhPUklUWVxORVRXT1JLIFNFUlZJQ0U8L0RhdGE+PERhdGEgTmFtZT0nUHJvdG9jb2wnPnRjcDwvRGF0YT48RGF0YSBOYW1lPSdJbml0aWF0ZWQnPmZhbHNlPC9EYXRhPjxEYXRhIE5hbWU9J1NvdXJjZUlzSXB2Nic+ZmFsc2U8L0RhdGE+PERhdGEgTmFtZT0nU291cmNlSXAnPjU5LjIuNTIuMTIyPC9EYXRhPjxEYXRhIE5hbWU9J1NvdXJjZUhvc3RuYW1lJz4tPC9EYXRhPjxEYXRhIE5hbWU9J1NvdXJjZVBvcnQnPjYxMTExPC9EYXRhPjxEYXRhIE5hbWU9J1NvdXJjZVBvcnROYW1lJz4tPC9EYXRhPjxEYXRhIE5hbWU9J0Rlc3RpbmF0aW9uSXNJcHY2Jz5mYWxzZTwvRGF0YT48RGF0YSBOYW1lPSdEZXN0aW5hdGlvbklwJz4xNzIuMzEuMjkuNzk8L0RhdGE+PERhdGEgTmFtZT0nRGVzdGluYXRpb25Ib3N0bmFtZSc+LTwvRGF0YT48RGF0YSBOYW1lPSdEZXN0aW5hdGlvblBvcnQnPjMzODk8L0RhdGE+PERhdGEgTmFtZT0nRGVzdGluYXRpb25Qb3J0TmFtZSc+LTwvRGF0YT48L0V2ZW50RGF0YT48L0V2ZW50Pg==",
                    "mime_type": "text/plain"
                }
            },
            "first_observed": "2023-02-15T11:38:26.000Z",
            "last_observed": "2023-02-15T11:38:26.000Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```
#### STIX Execute query
```shell
execute
splunk
splunk
"{\"type\":\"identity\",\"id\":\"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\", \"name\":\"splunk\",\"identity_class\":\"events\", \"created\": \"2022-01-22T13:22:50.336Z\", \"modified\": \"2023-03-22T13:22:50.336Z\"}"
"{\"host\":\"xxxx\",\"port\": xxxx,\"selfSignedCert\": \"-----BEGIN PRIVATE KEY-----\n\n-----END PRIVATE KEY-----\n-----BEGIN CERTIFICATE-----\n\n-----END CERTIFICATE-----\"}"
"{\"auth\":{\"username\": \"xxxx\", \"password\": \"xxxx\"}}"
"[process:name = 'cmd.exe' AND process:pid = 100] START t'2023-01-01T11:00:00.000Z' STOP t'2023-02-28T11:00:00.003Z'"
```
#### STIX Execute query - output
```json
{
    "type": "bundle",
    "id": "bundle--6afd74ac-8ea5-4989-9b5d-5a8c8f4fd955",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "splunk",
            "identity_class": "events",
            "created": "2022-01-22T13:22:50.336Z",
            "modified": "2023-03-22T13:22:50.336Z"
        },
        {
            "id": "observed-data--1dca7286-c0f3-496b-9474-0c803fd02aa3",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2023-05-09T07:33:49.320Z",
            "modified": "2023-05-09T07:33:49.320Z",
            "objects": {
                "0": {
                    "type": "user-account",
                    "user_id": "SYSTEM",
                    "account_login": "'S-1-5-18'"
                },
                "1": {
                    "type": "x-oca-event",
                    "user_ref": "0",
                    "host_ref": "2",
                    "module": "XmlWinEventLog:Microsoft-Windows-Sysmon/Operational",
                    "process_ref": "4",
                    "parent_process_ref": "8",
                    "action": "Process creation",
                    "code": "1",
                    "provider": "Microsoft Sysmon",
                    "outcome": "allowed",
                    "x_dest": "xxxxx",
                    "x_event_id": "13153",
                    "original_ref": "10",
                    "created": "2023-02-15T11:25:49.000Z"
                },
                "2": {
                    "type": "x-oca-asset",
                    "hostname": "xxxxx",
                    "x_operating_system": "Microsoft Windows"
                },
                "3": {
                    "type": "x-splunk-data",
                    "log_source": "XmlWinEventLog:Microsoft-Windows-Sysmon/Operational",
                    "event_type": [
                        "corelight_idx",
                        "endpoint_services_processes",
                        "ms-sysmon-process",
                        "windows_event_signature"
                    ],
                    "log_source_type": "XmlWinEventLog"
                },
                "4": {
                    "type": "process",
                    "command_line": "btool  server list general --no-log",
                    "pid": 5248,
                    "name": "btool.exe",
                    "binary_ref": "5",
                    "x_unique_id": "{7a97b85f-c13d-63ec-1103-000000007e00}",
                    "parent_ref": "8",
                    "x_original_file_name": "btool.exe"
                },
                "5": {
                    "type": "file",
                    "name": "btool.exe",
                    "parent_directory_ref": "6"
                },
                "6": {
                    "type": "directory",
                    "path": "C:\\SplunkForwarder\\bin"
                },
                "7": {
                    "type": "file",
                    "hashes": {
                        "SHA-1": "6C0F0DBCBC1442960CFEE43105BDF2CED4A7133E",
                        "MD5": "95439F1985B1CE750FF6693E7FB0F4BA",
                        "SHA-256": "303113F43A6187007B250230D34499082CCB42BB7920754DDC4E5302294A0D2D",
                        "x_IMPHASH": "D7E7C7FB1023AE6F5D81B244992E7451"
                    }
                },
                "8": {
                    "type": "process",
                    "pid": 100,
                    "name": "cmd.exe",
                    "binary_ref": "9"
                },
                "9": {
                    "type": "file",
                    "name": "cmd.exe"
                },
                "10": {
                    "type": "artifact",
                    "payload_bin": "PEV2ZW50IHhtbG5zPSdodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dpbi8yMDA0LzA4L2V2ZW50cy9ldmVudCc+PFN5c3RlbT48UHJvdmlkZXIgTmFtZT0nTWljcm9zb2Z0LVdpbmRvd3MtU3lzbW9uJyBHdWlkPSd7NTc3MDM4NWYtYzIyYS00M2UwLWJmNGMtMDZmNTY5OGZmYmQ5fScvPjxFdmVudElEPjE8L0V2ZW50SUQ+PFZlcnNpb24+NTwvVmVyc2lvbj48TGV2ZWw+NDwvTGV2ZWw+PFRhc2s+MTwvVGFzaz48T3Bjb2RlPjA8L09wY29kZT48S2V5d29yZHM+MHg4MDAwMDAwMDAwMDAwMDAwPC9LZXl3b3Jkcz48VGltZUNyZWF0ZWQgU3lzdGVtVGltZT0nMjAyMy0wMi0xNVQxMToyNTo0OS42NDQ0NzMxWicvPjxFdmVudFJlY29yZElEPjEzMTUzPC9FdmVudFJlY29yZElEPjxDb3JyZWxhdGlvbi8+PEV4ZWN1dGlvbiBQcm9jZXNzSUQ9JzE1MjgnIFRocmVhZElEPSczMDI0Jy8+PENoYW5uZWw+TWljcm9zb2Z0LVdpbmRvd3MtU3lzbW9uL09wZXJhdGlvbmFsPC9DaGFubmVsPjxDb21wdXRlcj5FQzJBTUFaLU80S0NVSzM8L0NvbXB1dGVyPjxTZWN1cml0eSBVc2VySUQ9J1MtMS01LTE4Jy8+PC9TeXN0ZW0+PEV2ZW50RGF0YT48RGF0YSBOYW1lPSdSdWxlTmFtZSc+dGVjaG5pcXVlX2lkPVQxMDU5LHRlY2huaXF1ZV9uYW1lPUNvbW1hbmQtTGluZSBJbnRlcmZhY2U8L0RhdGE+PERhdGEgTmFtZT0nVXRjVGltZSc+MjAyMy0wMi0xNSAxMToyNTo0OS42NDA8L0RhdGE+PERhdGEgTmFtZT0nUHJvY2Vzc0d1aWQnPns3YTk3Yjg1Zi1jMTNkLTYzZWMtMTEwMy0wMDAwMDAwMDdlMDB9PC9EYXRhPjxEYXRhIE5hbWU9J1Byb2Nlc3NJZCc+NTI0ODwvRGF0YT48RGF0YSBOYW1lPSdJbWFnZSc+QzpcU3BsdW5rRm9yd2FyZGVyXGJpblxidG9vbC5leGU8L0RhdGE+PERhdGEgTmFtZT0nRmlsZVZlcnNpb24nPjkuMC4zPC9EYXRhPjxEYXRhIE5hbWU9J0Rlc2NyaXB0aW9uJz5idG9vbDwvRGF0YT48RGF0YSBOYW1lPSdQcm9kdWN0Jz5zcGx1bmsgQXBwbGljYXRpb248L0RhdGE+PERhdGEgTmFtZT0nQ29tcGFueSc+U3BsdW5rIEluYy48L0RhdGE+PERhdGEgTmFtZT0nT3JpZ2luYWxGaWxlTmFtZSc+YnRvb2wuZXhlPC9EYXRhPjxEYXRhIE5hbWU9J0NvbW1hbmRMaW5lJz5idG9vbCAgc2VydmVyIGxpc3QgZ2VuZXJhbCAtLW5vLWxvZzwvRGF0YT48RGF0YSBOYW1lPSdDdXJyZW50RGlyZWN0b3J5Jz5DOlxXaW5kb3dzXHN5c3RlbTMyXDwvRGF0YT48RGF0YSBOYW1lPSdVc2VyJz5OVCBBVVRIT1JJVFlcU1lTVEVNPC9EYXRhPjxEYXRhIE5hbWU9J0xvZ29uR3VpZCc+ezdhOTdiODVmLTdkYjgtNjNlYy1lNzAzLTAwMDAwMDAwMDAwMH08L0RhdGE+PERhdGEgTmFtZT0nTG9nb25JZCc+MHgzZTc8L0RhdGE+PERhdGEgTmFtZT0nVGVybWluYWxTZXNzaW9uSWQnPjA8L0RhdGE+PERhdGEgTmFtZT0nSW50ZWdyaXR5TGV2ZWwnPlN5c3RlbTwvRGF0YT48RGF0YSBOYW1lPSdIYXNoZXMnPlNIQTE9NkMwRjBEQkNCQzE0NDI5NjBDRkVFNDMxMDVCREYyQ0VENEE3MTMzRSxNRDU9OTU0MzlGMTk4NUIxQ0U3NTBGRjY2OTNFN0ZCMEY0QkEsU0hBMjU2PTMwMzExM0Y0M0E2MTg3MDA3QjI1MDIzMEQzNDQ5OTA4MkNDQjQyQkI3OTIwNzU0RERDNEU1MzAyMjk0QTBEMkQsSU1QSEFTSD1EN0U3QzdGQjEwMjNBRTZGNUQ4MUIyNDQ5OTJFNzQ1MTwvRGF0YT48RGF0YSBOYW1lPSdQYXJlbnRQcm9jZXNzR3VpZCc+ezdhOTdiODVmLWMxM2QtNjNlYy0xMDAzLTAwMDAwMDAwN2UwMH08L0RhdGE+PERhdGEgTmFtZT0nUGFyZW50UHJvY2Vzc0lkJz4xMDA8L0RhdGE+PERhdGEgTmFtZT0nUGFyZW50SW1hZ2UnPkM6XFdpbmRvd3NcU3lzdGVtMzJcY21kLmV4ZTwvRGF0YT48RGF0YSBOYW1lPSdQYXJlbnRDb21tYW5kTGluZSc+QzpcV2luZG93c1xzeXN0ZW0zMlxjbWQuZXhlIC9jIGJ0b29sIHNlcnZlciBsaXN0IGdlbmVyYWwgLS1uby1sb2c8L0RhdGE+PERhdGEgTmFtZT0nUGFyZW50VXNlcic+TlQgQVVUSE9SSVRZXFNZU1RFTTwvRGF0YT48L0V2ZW50RGF0YT48L0V2ZW50Pg==",
                    "mime_type": "text/plain"
                }
            },
            "first_observed": "2023-01-11T15:29:45.000Z",
            "last_observed": "2023-01-11T15:29:45.000Z",
            "number_observed": 1
        }
	],
"spec_version": "2.0"
}
```

### References
- [Splunk](https://docs.splunk.com/Documentation/Splunk)