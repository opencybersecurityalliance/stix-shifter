# PaloAlto Cortex XDR

## Supported STIX Mappings

See the [table of mappings](paloalto_supported_stix.md) for the STIX objects and operators supported by this connector.

**Table of Contents**

- [PaloAlto Cortex XDR API Endpoints](#paloalto-cortex-xdr-api-endpoints)
- [Pattern expression with STIX attributes - Single Observation](#single-observation)
- [Pattern expression with STIX attributes - Multiple Observation](#multiple-observation)
- [Pattern expression with STIX attributes - Execute Query](#stix-execute-query)
- [Limitations](#limitations)
- [References](#references)

### PaloAlto Cortex XDR API Endpoints

   |Connector Method|PaloAlto Cortex XDR API Endpoint| Method
   | ----           |   ------              | -----|
   |Query Endpoint  |https://<api-{fqdn}>/public_api/v1/xql/start_xql_query/|POST
   |Result Endpoint |https://<api-{fqdn}>/public_api/v1/xql/get_query_results/|POST
   |Stream Endpoint |https://<api-{fqdn}>/public_api/v1/xql/get_query_results_stream/|POST
   |Quota Endpoint  |https://<api-{fqdn}>/public_api/v1/xql/get_quota/|POST

### Format for calling stix-shifter from the command line
```
$ stix-shifter translate <MODULE NAME> query "<STIX IDENTITY OBJECT>" "<STIX PATTERN>" "<OPTIONS>"
```
### Pattern expression with STIX attributes

### Single Observation

#### STIX Translate query
```shell
translate paloalto query '{}' "[ipv4-addr:value = '1.1.0.0'] START t'2022-03-01T11:00:00.000Z' STOP t'2023-03-08T11:00:00.003Z'"
```
#### STIX Translate query - output
```json
{
    "queries": [
        {
            "xdr_data": {
                "query": "dataset = xdr_data | filter ((action_local_ip = \"1.1.0.0\" or action_remote_ip = \"1.1.0.0\" or agent_ip_addresses = \"1.1.0.0\")  and (to_epoch(_time,\"millis\") >= 1646132400000 and to_epoch(_time,\"millis\") <= 1678273200003)) | alter dataset_name = \"xdr_data\" | fields dataset_name,action_local_ip,action_remote_ip,agent_ip_addresses,agent_ip_addresses_v6,dst_agent_ip_addresses_v6,action_local_port,action_remote_port,action_network_protocol,action_pkts_sent,action_pkts_received,action_file_name,action_process_image_name,actor_process_image_name,causality_actor_process_image_name,os_actor_process_image_name,action_file_size,action_file_md5,action_module_md5,action_process_image_md5,action_file_authenticode_sha1,action_file_authenticode_sha2,action_file_sha256,action_module_sha256,action_process_image_sha256,action_file_access_time,actor_process_file_access_time,os_actor_process_file_access_time,action_file_mod_time,actor_process_file_mod_time,os_actor_process_file_mod_time,action_file_create_time,action_file_path,action_process_image_path,action_registry_file_path,actor_process_image_path,causality_actor_process_image_path,os_actor_process_image_path,action_process_image_command_line,actor_process_command_line,causality_actor_process_command_line,os_actor_process_command_line,action_process_file_create_time,actor_process_file_create_time,causality_actor_process_file_create_time,os_actor_process_file_create_time,action_module_process_os_pid,action_process_os_pid,actor_process_os_pid,causality_actor_process_os_pid,os_actor_process_os_pid,action_process_requested_parent_pid,action_thread_parent_pid,action_thread_child_pid,action_process_username,auth_domain,dst_host_metadata_domain,host_metadata_domain,dst_action_url_category,action_registry_key_name,action_registry_value_name,mac,associated_mac,dst_associated_mac,dst_mac,actor_primary_user_sid,action_process_user_sid,actor_primary_username,actor_process_logon_id,action_file_info_company,action_file_extension,action_file_attributes,action_file_internal_zipped_files,action_file_last_writer_actor,action_file_signature_status,action_file_signature_vendor,action_file_signature_product,action_file_info_description,action_file_group,action_file_group_name,action_file_type,action_file_info_file_version,manifest_file_version,action_file_info_product_version,action_file_owner,action_file_owner_name,action_file_info_product_name,action_file_id,action_file_wildfire_verdict,action_file_hash_control_verdict,actor_process_instance_id,actor_process_causality_id,actor_process_auth_id,actor_process_container_id,actor_process_signature_vendor,actor_process_signature_status,actor_process_signature_product,actor_process_image_extension,action_process_termination_code,action_process_termination_date,action_remote_process_thread_id,action_process_instance_execution_time,actor_process_execution_time,action_process_handle_is_kernel,action_process_is_container_root,actor_process_is_native,agent_version,agent_hostname,agent_content_version,agent_session_start_time,agent_id,agent_os_type,agent_os_sub_type,agent_is_vdi,action_user_agent,http_req_user_agent_header,action_evtlog_data_fields,action_evtlog_description,action_evtlog_source,action_evtlog_event_id,action_evtlog_level,action_evtlog_tid,action_evtlog_uid,action_evtlog_pid,action_evtlog_message,action_evtlog_version,event_id,vpn_event_description,event_timestamp,event_version,event_rpc_interface_uuid,event_address_mapped_image_path,event_type,event_sub_type,action_network_creation_time,action_network_connection_id,action_network_packet_data,action_proxy,host_metadata_hostname,action_external_hostname | limit 10000 ",
                "timeframe": {
                    "from": 1646132400000,
                    "to": 1678273200003
                }
            }
        }
    ]
}

```
#### STIX Transmit ping 

```shell
transmit
paloalto
"{\"host\":\"xx.xx.xx\"}"
"{\"auth\":{\"api_key\": \"xxxx\", \"api_key_id\": \"xx\",\"tenant\":\"xxxx\"}}"
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
paloalto
"{\"host\":\"xx.xx.xx\"}"
"{\"auth\":{\"api_key\": \"xxxx\", \"api_key_id\": \"xx\",\"tenant\":\"xxxx\"}}"
query
"{\"xdr_data\": {\"query\": \"dataset = xdr_data | filter ((action_local_ip = \\"1.1.0.0\\" or action_remote_ip = \\"1.1.0.0\\" or agent_ip_addresses = \\"1.1.0.0\\")  and (to_epoch(_time,\\"millis\\") >= 1646132400000 and to_epoch(_time,\\"millis\\") <= 1678273200003)) | alter dataset_name = \\"xdr_data\\" | fields dataset_name,action_local_ip,action_remote_ip,agent_ip_addresses,agent_ip_addresses_v6,dst_agent_ip_addresses_v6,action_local_port,action_remote_port,action_network_protocol,action_pkts_sent,action_pkts_received,action_file_name,action_process_image_name,actor_process_image_name,causality_actor_process_image_name,os_actor_process_image_name,action_file_size,action_file_md5,action_module_md5,action_process_image_md5,action_file_authenticode_sha1,action_file_authenticode_sha2,action_file_sha256,action_module_sha256,action_process_image_sha256,action_file_access_time,actor_process_file_access_time,os_actor_process_file_access_time,action_file_mod_time,actor_process_file_mod_time,os_actor_process_file_mod_time,action_file_create_time,action_file_path,action_process_image_path,action_registry_file_path,actor_process_image_path,causality_actor_process_image_path,os_actor_process_image_path,action_process_image_command_line,actor_process_command_line,causality_actor_process_command_line,os_actor_process_command_line,action_process_file_create_time,actor_process_file_create_time,causality_actor_process_file_create_time,os_actor_process_file_create_time,action_module_process_os_pid,action_process_os_pid,actor_process_os_pid,causality_actor_process_os_pid,os_actor_process_os_pid,action_process_requested_parent_pid,action_thread_parent_pid,action_thread_child_pid,action_process_username,auth_domain,dst_host_metadata_domain,host_metadata_domain,dst_action_url_category,action_registry_key_name,action_registry_value_name,mac,associated_mac,dst_associated_mac,dst_mac,actor_primary_user_sid,action_process_user_sid,actor_primary_username,actor_process_logon_id,action_file_info_company,action_file_extension,action_file_attributes,action_file_internal_zipped_files,action_file_last_writer_actor,action_file_signature_status,action_file_signature_vendor,action_file_signature_product,action_file_info_description,action_file_group,action_file_group_name,action_file_type,action_file_info_file_version,manifest_file_version,action_file_info_product_version,action_file_owner,action_file_owner_name,action_file_info_product_name,action_file_id,action_file_wildfire_verdict,action_file_hash_control_verdict,actor_process_instance_id,actor_process_causality_id,actor_process_auth_id,actor_process_container_id,actor_process_signature_vendor,actor_process_signature_status,actor_process_signature_product,actor_process_image_extension,action_process_termination_code,action_process_termination_date,action_remote_process_thread_id,action_process_instance_execution_time,actor_process_execution_time,action_process_handle_is_kernel,action_process_is_container_root,actor_process_is_native,agent_version,agent_hostname,agent_content_version,agent_session_start_time,agent_id,agent_os_type,agent_os_sub_type,agent_is_vdi,action_user_agent,http_req_user_agent_header,action_evtlog_data_fields,action_evtlog_description,action_evtlog_source,action_evtlog_event_id,action_evtlog_level,action_evtlog_tid,action_evtlog_uid,action_evtlog_pid,action_evtlog_message,action_evtlog_version,event_id,vpn_event_description,event_timestamp,event_version,event_rpc_interface_uuid,event_address_mapped_image_path,event_type,event_sub_type,action_network_creation_time,action_network_connection_id,action_network_packet_data,action_proxy,host_metadata_hostname,action_external_hostname | limit 10000 \", \"timeframe\": {\"from\": 1646132400000, \"to\": 1678273200003}}}"
```

#### STIX Transmit query - output
```json
{
    "success": true,
    "search_id": "a106f2f4614f40_34940_inv"
}
```
#### STIX Transmit status 

```shell
transmit
paloalto
"{\"host\":\"xx.xx.xx\"}"
"{\"auth\":{\"api_key\": \"xxxx\", \"api_key_id\": \"xx\",\"tenant\":\"xxxx\"}}"
status
"a106f2f4614f40_34940_inv"
```

#### STIX Transmit status - output
```json
{
    "success": true,
    "status": "COMPLETED",
    "progress": 100
}
```
#### STIX Transmit results 

```shell
transmit
paloalto
"{\"host\":\"xx.xx.xx\"}"
"{\"auth\":{\"api_key\": \"xxxx\", \"api_key_id\": \"xx\",\"tenant\":\"xxxx\"}}"
results
"a106f2f4614f40_34940_inv" 0 2
```

#### STIX Transmit results - output
```json
{
    "success": true,
    "data": [
        {
            "xdr_data": {
                "action_local_ip": "94.232.41.158",
                "action_network_protocol": "TCP",
                "action_remote_ip": "172.31.90.48",
                "action_local_port": "31545",
                "action_remote_port": "3389",
                "agent_id": "94.232.41.158",
                "event_id": "NDQ3NzY1MTgzNjU1MjQxNTg0Ng==",
                "event_timestamp": "1648884264296",
                "event_type": "STORY",
                "event_sub_type": "event_sub_type_4",
                "action_network_creation_time": "1648884264296",
                "action_network_connection_id": "AdhGYq2dw14AAAAAAAEOxg==",
                "action_proxy": "FALSE"
            }
        },
        {
            "xdr_data": {
                "action_local_ip": "94.232.41.158",
                "action_network_protocol": "TCP",
                "action_remote_ip": "172.31.90.48",
                "action_local_port": "6142",
                "action_remote_port": "3389",
                "agent_id": "94.232.41.158",
                "event_id": "MjAyOTYyMzMyMTg3Njc5MDY4NA==",
                "event_timestamp": "1648884468933",
                "event_type": "STORY",
                "event_sub_type": "event_sub_type_4",
                "action_network_creation_time": "1648884468933",
                "action_network_connection_id": "AdhGYyeW9LcAAAAAAAEO5g==",
                "action_proxy": "FALSE"
            }
        }
    ]
}
```


#### STIX Translate results

```shell
translate 
paloalto 
results 
"{\"type\":\"identity\",\"id\":\"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\",\"name\":\"paloalto\",\"identity_class\":\"system\",\"created\":\"2022-03-16T13:22:50.336Z\",\"modified\":\"2022-03-16T13:22:50.336Z\"}" 
"[ { \"xdr_data\": { \"action_local_ip\": \"94.232.41.158\", \"action_network_protocol\": \"TCP\", \"action_remote_ip\": \"1.1.0.0\", \"action_local_port\": \"31545\", \"action_remote_port\": \"3389\", \"agent_id\": \"94.232.41.158\", \"event_id\": \"NDQ3NzY1MTgzNjU1MjQxNTg0Ng==\", \"event_timestamp\": \"1648884264296\", \"event_type\": \"STORY\", \"event_sub_type\": \"event_sub_type_4\", \"action_network_creation_time\": \"1648884264296\", \"action_network_connection_id\": \"AdhGYq2dw14AAAAAAAEOxg==\", \"action_proxy\": \"FALSE\" } }, { \"xdr_data\": { \"action_local_ip\": \"94.232.41.158\", \"action_network_protocol\": \"TCP\", \"action_remote_ip\": \"1.1.0.0\", \"action_local_port\": \"6142\", \"action_remote_port\": \"3389\", \"agent_id\": \"94.232.41.158\", \"event_id\": \"MjAyOTYyMzMyMTg3Njc5MDY4NA==\", \"event_timestamp\": \"1648884468933\", \"event_type\": \"STORY\", \"event_sub_type\": \"event_sub_type_4\", \"action_network_creation_time\": \"1648884468933\", \"action_network_connection_id\": \"AdhGYyeW9LcAAAAAAAEO5g==\", \"action_proxy\": \"FALSE\" } } ] " 
"{\"stix_validator\": true}"
```

#### STIX Translate results - output
```json
{
    "type": "bundle",
    "id": "bundle--318a05c9-47e5-4146-80ce-e6b95c71c8bd",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "paloalto",
            "identity_class": "system",
            "created": "2022-03-16T13:22:50.336Z",
            "modified": "2022-03-16T13:22:50.336Z"
        },
        {
            "id": "observed-data--713d4380-de85-40f7-a6c1-c893331e9c99",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-05T12:43:28.560Z",
            "modified": "2022-04-05T12:43:28.560Z",
            "objects": {
                "0": {
                    "type": "ipv4-addr",
                    "value": "94.232.41.158"
                },
                "1": {
                    "type": "network-traffic",
                    "src_ref": "0",
                    "protocols": [
                        "tcp"
                    ],
                    "dst_ref": "4",
                    "src_port": 31545,
                    "dst_port": 3389,
                    "extensions": {
                        "x-paloalto-network": {
                            "creation_time": "2022-04-02T07:24:24.296Z",
                            "connection_id": "AdhGYq2dw14AAAAAAAEOxg==",
                            "is_proxy": false
                        }
                    }
                },
                "2": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "0"
                    ],
                    "extensions": {
                        "x-paloalto-agent": {
                            "asset_id": "94.232.41.158"
                        }
                    }
                },
                "3": {
                    "type": "x-oca-event",
                    "network_ref": "1",
                    "code": "NDQ3NzY1MTgzNjU1MjQxNTg0Ng==",
                    "created": "2022-04-02T07:24:24.296Z",
                    "category": ["story"],
                    "action": "event_sub_type_4"
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "1.1.0.0"
                }
            },
            "first_observed": "2022-04-05T12:43:28.560Z",
            "last_observed": "2022-04-05T12:43:28.560Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--d05e4f7d-0866-4f4d-be32-a39832ad27c1",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-05T12:43:28.565Z",
            "modified": "2022-04-05T12:43:28.565Z",
            "objects": {
                "0": {
                    "type": "ipv4-addr",
                    "value": "94.232.41.158"
                },
                "1": {
                    "type": "network-traffic",
                    "src_ref": "0",
                    "protocols": [
                        "tcp"
                    ],
                    "dst_ref": "4",
                    "src_port": 6142,
                    "dst_port": 3389,
                    "extensions": {
                        "x-paloalto-network": {
                            "creation_time": "2022-04-02T07:27:48.933Z",
                            "connection_id": "AdhGYyeW9LcAAAAAAAEO5g==",
                            "is_proxy": false
                        }
                    }
                },
                "2": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "0"
                    ],
                    "extensions": {
                        "x-paloalto-agent": {
                            "asset_id": "94.232.41.158"
                        }
                    }
                },
                "3": {
                    "type": "x-oca-event",
                    "network_ref": "1",
                    "code": "MjAyOTYyMzMyMTg3Njc5MDY4NA==",
                    "created": "2022-04-02T07:27:48.933Z",
                    "category": ["story"],
                    "action": "event_sub_type_4"
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "1.1.0.0"
                }
            },
            "first_observed": "2022-04-05T12:43:28.565Z",
            "last_observed": "2022-04-05T12:43:28.565Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```

### Multiple Observation  

#### STIX Translate query
```shell
translate paloalto query {} "([x-oca-event:category[*] = 'file'] AND [file:size > 3000] OR [x-oca-asset:agent_version = '7.6.1.46600'] )START t'2022-02-10T00:00:00.000000Z' STOP t'2022-02-15T00:00:00.000000Z'"
```

#### STIX Translate query - output

```json
{
    "queries": [
        {
            "xdr_data": {
                "query": "dataset = xdr_data | filter (event_type = ENUM.FILE  and (to_epoch(_time,\"millis\") >= 1644451200000 and to_epoch(_time,\"millis\") <= 1644883200000)) or (action_file_size > 3000  and (to_epoch(_time,\"millis\") >= 1644451200000 and to_epoch(_time,\"millis\") <= 1644883200000)) | alter dataset_name = \"xdr_data\" | fields dataset_name,action_local_ip,action_remote_ip,agent_ip_addresses,agent_ip_addresses_v6,dst_agent_ip_addresses_v6,action_local_port,action_remote_port,action_network_protocol,action_pkts_sent,action_pkts_received,action_file_name,action_process_image_name,actor_process_image_name,causality_actor_process_image_name,os_actor_process_image_name,action_file_size,action_file_md5,action_module_md5,action_process_image_md5,action_file_authenticode_sha1,action_file_authenticode_sha2,action_file_sha256,action_module_sha256,action_process_image_sha256,action_file_access_time,actor_process_file_access_time,os_actor_process_file_access_time,action_file_mod_time,actor_process_file_mod_time,os_actor_process_file_mod_time,action_file_create_time,action_file_path,action_process_image_path,action_registry_file_path,actor_process_image_path,causality_actor_process_image_path,os_actor_process_image_path,action_process_image_command_line,actor_process_command_line,causality_actor_process_command_line,os_actor_process_command_line,action_process_file_create_time,actor_process_file_create_time,causality_actor_process_file_create_time,os_actor_process_file_create_time,action_module_process_os_pid,action_process_os_pid,actor_process_os_pid,causality_actor_process_os_pid,os_actor_process_os_pid,action_process_requested_parent_pid,action_thread_parent_pid,action_thread_child_pid,action_process_username,auth_domain,dst_host_metadata_domain,host_metadata_domain,dst_action_url_category,action_registry_key_name,action_registry_value_name,mac,associated_mac,dst_associated_mac,dst_mac,actor_primary_user_sid,action_process_user_sid,actor_primary_username,actor_process_logon_id,action_file_info_company,action_file_extension,action_file_attributes,action_file_internal_zipped_files,action_file_last_writer_actor,action_file_signature_status,action_file_signature_vendor,action_file_signature_product,action_file_info_description,action_file_group,action_file_group_name,action_file_type,action_file_info_file_version,manifest_file_version,action_file_info_product_version,action_file_owner,action_file_owner_name,action_file_info_product_name,action_file_id,action_file_wildfire_verdict,action_file_hash_control_verdict,actor_process_instance_id,actor_process_causality_id,actor_process_auth_id,actor_process_container_id,actor_process_signature_vendor,actor_process_signature_status,actor_process_signature_product,actor_process_image_extension,action_process_termination_code,action_process_termination_date,action_remote_process_thread_id,action_process_instance_execution_time,actor_process_execution_time,action_process_handle_is_kernel,action_process_is_container_root,actor_process_is_native,agent_version,agent_hostname,agent_content_version,agent_session_start_time,agent_id,agent_os_type,agent_os_sub_type,agent_is_vdi,action_user_agent,http_req_user_agent_header,action_evtlog_data_fields,action_evtlog_description,action_evtlog_source,action_evtlog_event_id,action_evtlog_level,action_evtlog_tid,action_evtlog_uid,action_evtlog_pid,action_evtlog_message,action_evtlog_version,event_id,vpn_event_description,event_timestamp,event_version,event_rpc_interface_uuid,event_address_mapped_image_path,event_type,event_sub_type,action_network_creation_time,action_network_connection_id,action_network_packet_data,action_proxy,host_metadata_hostname,action_external_hostname | limit 10000 ",
                "timeframe": {
                    "from": 1644451200000,
                    "to": 1644883200000
                }
            }
        }
    ]
}
```


#### STIX Transmit query

```shell
transmit
paloalto
"{\"host\":\"xx.xx.xx\"}"
"{\"auth\":{\"api_key\": \"xxxx\", \"api_key_id\": \"xx\",\"tenant\":\"xxxx\"}}"
query
"{ \"xdr_data\": { \"query\": \"dataset = xdr_data | filter (event_type = ENUM.FILE and (to_epoch(_time,\\"millis\\") >= 1644451200000 and to_epoch(_time,\\"millis\\") <= 1644883200000)) or (action_file_size > 3000 and (to_epoch(_time,\\"millis\\") >= 1644451200000 and to_epoch(_time,\\"millis\\") <= 1644883200000)) | alter dataset_name = \\"xdr_data\\" | fields dataset_name,action_local_ip,action_remote_ip,agent_ip_addresses,agent_ip_addresses_v6,dst_agent_ip_addresses_v6,action_local_port,action_remote_port,action_network_protocol,action_pkts_sent,action_pkts_received,action_file_name,action_process_image_name,actor_process_image_name,causality_actor_process_image_name,os_actor_process_image_name,action_file_size,action_file_md5,action_module_md5,action_process_image_md5,action_file_authenticode_sha1,action_file_authenticode_sha2,action_file_sha256,action_module_sha256,action_process_image_sha256,action_file_access_time,actor_process_file_access_time,os_actor_process_file_access_time,action_file_mod_time,actor_process_file_mod_time,os_actor_process_file_mod_time,action_file_create_time,action_file_path,action_process_image_path,action_registry_file_path,actor_process_image_path,causality_actor_process_image_path,os_actor_process_image_path,action_process_image_command_line,actor_process_command_line,causality_actor_process_command_line,os_actor_process_command_line,action_process_file_create_time,actor_process_file_create_time,causality_actor_process_file_create_time,os_actor_process_file_create_time,action_module_process_os_pid,action_process_os_pid,actor_process_os_pid,causality_actor_process_os_pid,os_actor_process_os_pid,action_process_requested_parent_pid,action_thread_parent_pid,action_thread_child_pid,action_process_username,auth_domain,dst_host_metadata_domain,host_metadata_domain,dst_action_url_category,action_registry_key_name,action_registry_value_name,mac,associated_mac,dst_associated_mac,dst_mac,actor_primary_user_sid,action_process_user_sid,actor_primary_username,actor_process_logon_id,action_file_info_company,action_file_extension,action_file_attributes,action_file_internal_zipped_files,action_file_last_writer_actor,action_file_signature_status,action_file_signature_vendor,action_file_signature_product,action_file_info_description,action_file_group,action_file_group_name,action_file_type,action_file_info_file_version,manifest_file_version,action_file_info_product_version,action_file_owner,action_file_owner_name,action_file_info_product_name,action_file_id,action_file_wildfire_verdict,action_file_hash_control_verdict,actor_process_instance_id,actor_process_causality_id,actor_process_auth_id,actor_process_container_id,actor_process_signature_vendor,actor_process_signature_status,actor_process_signature_product,actor_process_image_extension,action_process_termination_code,action_process_termination_date,action_remote_process_thread_id,action_process_instance_execution_time,actor_process_execution_time,action_process_handle_is_kernel,action_process_is_container_root,actor_process_is_native,agent_version,agent_hostname,agent_content_version,agent_session_start_time,agent_id,agent_os_type,agent_os_sub_type,agent_is_vdi,action_user_agent,http_req_user_agent_header,action_evtlog_data_fields,action_evtlog_description,action_evtlog_source,action_evtlog_event_id,action_evtlog_level,action_evtlog_tid,action_evtlog_uid,action_evtlog_pid,action_evtlog_message,action_evtlog_version,event_id,vpn_event_description,event_timestamp,event_version,event_rpc_interface_uuid,event_address_mapped_image_path,event_type,event_sub_type,action_network_creation_time,action_network_connection_id,action_network_packet_data,action_proxy,host_metadata_hostname,action_external_hostname | limit 10000 \", \"timeframe\": { \"from\": 1644451200000, \"to\": 1644883200000 } } }"
```

#### STIX Transmit query - output

```json
{
    "success": true,
    "search_id": "3dc7d55520fe41_35090_inv"
}
```
#### STIX Transmit status 

```shell
transmit
paloalto
"{\"host\":\"xx.xx.xx\"}"
"{\"auth\":{\"api_key\": \"xxxx\", \"api_key_id\": \"xx\",\"tenant\":\"xxxx\"}}"
status
"3dc7d55520fe41_35090_inv"
```

#### STIX Transmit status - output
```json
{
    "success": true,
    "status": "COMPLETED",
    "progress": 100
}

```
#### STIX Transmit results 

```shell
transmit
paloalto
"{\"host\":\"xx.xx.xx\"}"
"{\"auth\":{\"api_key\": \"xxxx\", \"api_key_id\": \"xx\",\"tenant\":\"xxxx\"}}"
results
"3dc7d55520fe41_35090_inv" 0 2
```

#### STIX Transmit results - output
```json
{
    "success": true,
    "data": [
        {
            "xdr_data": {
                "agent_ip_addresses": [
                    "172.31.31.67"
                ],
                "action_file_name": "DRIVERS",
                "actor_process_image_name": "System",
                "causality_actor_process_image_name": "System",
                "os_actor_process_image_name": "System",
                "action_file_size": "4255744",
                "action_file_path": "C:\\Windows\\System32\\config\\DRIVERS",
                "actor_process_image_path": "System",
                "causality_actor_process_image_path": "System",
                "os_actor_process_image_path": "System",
                "actor_process_os_pid": "4",
                "causality_actor_process_os_pid": "4",
                "os_actor_process_os_pid": "4",
                "actor_primary_user_sid": "S-1-5-18",
                "actor_primary_username": "NT AUTHORITY\\SYSTEM",
                "actor_process_logon_id": "1003",
                "action_file_attributes": "128",
                "action_file_type": "18",
                "manifest_file_version": "5",
                "actor_process_instance_id": "AdgdeB26mNQAAAAEAAAAAA==",
                "actor_process_causality_id": "AdgdeB26mNQAAAAEAAAAAA==",
                "actor_process_auth_id": "999",
                "actor_process_signature_vendor": "Microsoft Corporation",
                "actor_process_signature_status": "SIGNED",
                "actor_process_signature_product": "Microsoft Windows",
                "actor_process_execution_time": "1644385473948",
                "actor_process_is_native": "TRUE",
                "agent_version": "7.6.1.46600",
                "agent_hostname": "EC2AMAZ-IQFSLIL",
                "agent_content_version": "380-82571",
                "agent_session_start_time": "1644385496543",
                "agent_id": "37a92aad549d41d184ec9fbdafbff55c",
                "agent_os_type": "AGENT_OS_WINDOWS",
                "agent_os_sub_type": "Windows Server 2016 [10.0 (Build 17763)]",
                "agent_is_vdi": "FALSE",
                "event_id": "AAABfvQtkk8qn9UKACE2JA==",
                "event_timestamp": "1644774134407",
                "event_version": "25",
                "event_type": "FILE",
                "event_sub_type": "FILE_OPEN"
            }
        },
        {
            "xdr_data": {
                "agent_ip_addresses": [
                    "172.31.31.67"
                ],
                "action_file_name": "DRIVERS",
                "actor_process_image_name": "System",
                "causality_actor_process_image_name": "System",
                "os_actor_process_image_name": "System",
                "action_file_size": "4255744",
                "action_file_path": "C:\\Windows\\System32\\config\\DRIVERS",
                "actor_process_image_path": "System",
                "causality_actor_process_image_path": "System",
                "os_actor_process_image_path": "System",
                "actor_process_os_pid": "4",
                "causality_actor_process_os_pid": "4",
                "os_actor_process_os_pid": "4",
                "actor_primary_user_sid": "S-1-5-18",
                "actor_primary_username": "NT AUTHORITY\\SYSTEM",
                "actor_process_logon_id": "1003",
                "action_file_type": "0",
                "manifest_file_version": "5",
                "actor_process_instance_id": "AdgdeB26mNQAAAAEAAAAAA==",
                "actor_process_causality_id": "AdgdeB26mNQAAAAEAAAAAA==",
                "actor_process_auth_id": "999",
                "actor_process_signature_vendor": "Microsoft Corporation",
                "actor_process_signature_status": "SIGNED",
                "actor_process_signature_product": "Microsoft Windows",
                "actor_process_execution_time": "1644385473948",
                "actor_process_is_native": "TRUE",
                "agent_version": "7.6.1.46600",
                "agent_hostname": "EC2AMAZ-IQFSLIL",
                "agent_content_version": "380-82571",
                "agent_session_start_time": "1644385496543",
                "agent_id": "37a92aad549d41d184ec9fbdafbff55c",
                "agent_os_type": "AGENT_OS_WINDOWS",
                "agent_os_sub_type": "Windows Server 2016 [10.0 (Build 17763)]",
                "agent_is_vdi": "FALSE",
                "event_id": "AAABfvWCZpMqn9UKACRWUw==",
                "event_timestamp": "1644796471001",
                "event_version": "25",
                "event_type": "FILE",
                "event_sub_type": "FILE_WRITE"
            }
        }
    ]
}
```


#### STIX Translate results

```shell
translate 
paloalto 
results 
"{\"type\":\"identity\",\"id\":\"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\",\"name\":\"paloalto\",\"identity_class\":\"system\",\"created\":\"2022-03-16T13:22:50.336Z\",\"modified\":\"2022-03-16T13:22:50.336Z\"}" 
" [ { \"xdr_data\": { \"agent_ip_addresses\": [ \"172.31.31.67\" ], \"action_file_name\": \"DRIVERS\", \"actor_process_image_name\": \"System\", \"causality_actor_process_image_name\": \"System\", \"os_actor_process_image_name\": \"System\", \"action_file_size\": \"4255744\", \"action_file_path\": \"C:\\Windows\\System32\\config\\DRIVERS\", \"actor_process_image_path\": \"System\", \"causality_actor_process_image_path\": \"System\", \"os_actor_process_image_path\": \"System\", \"actor_process_os_pid\": \"4\", \"causality_actor_process_os_pid\": \"4\", \"os_actor_process_os_pid\": \"4\", \"actor_primary_user_sid\": \"S-1-5-18\", \"actor_primary_username\": \"NT AUTHORITY\\SYSTEM\", \"actor_process_logon_id\": \"1003\", \"action_file_attributes\": \"128\", \"action_file_type\": \"18\", \"manifest_file_version\": \"5\", \"actor_process_instance_id\": \"AdgdeB26mNQAAAAEAAAAAA==\", \"actor_process_causality_id\": \"AdgdeB26mNQAAAAEAAAAAA==\", \"actor_process_auth_id\": \"999\", \"actor_process_signature_vendor\": \"Microsoft Corporation\", \"actor_process_signature_status\": \"SIGNED\", \"actor_process_signature_product\": \"Microsoft Windows\", \"actor_process_execution_time\": \"1644385473948\", \"actor_process_is_native\": \"TRUE\", \"agent_version\": \"7.6.1.46600\", \"agent_hostname\": \"EC2AMAZ-IQFSLIL\", \"agent_content_version\": \"380-82571\", \"agent_session_start_time\": \"1644385496543\", \"agent_id\": \"37a92aad549d41d184ec9fbdafbff55c\", \"agent_os_type\": \"AGENT_OS_WINDOWS\", \"agent_os_sub_type\": \"Windows Server 2016 [10.0 (Build 17763)]\", \"agent_is_vdi\": \"FALSE\", \"event_id\": \"AAABfvQtkk8qn9UKACE2JA==\", \"event_timestamp\": \"1644774134407\", \"event_version\": \"25\", \"event_type\": \"FILE\", \"event_sub_type\": \"FILE_OPEN\" } }, { \"xdr_data\": { \"agent_ip_addresses\": [ \"172.31.31.67\" ], \"action_file_name\": \"DRIVERS\", \"actor_process_image_name\": \"System\", \"causality_actor_process_image_name\": \"System\", \"os_actor_process_image_name\": \"System\", \"action_file_size\": \"4255744\", \"action_file_path\": \"C:\\Windows\\System32\\config\\DRIVERS\", \"actor_process_image_path\": \"System\", \"causality_actor_process_image_path\": \"System\", \"os_actor_process_image_path\": \"System\", \"actor_process_os_pid\": \"4\", \"causality_actor_process_os_pid\": \"4\", \"os_actor_process_os_pid\": \"4\", \"actor_primary_user_sid\": \"S-1-5-18\", \"actor_primary_username\": \"NT AUTHORITY\\SYSTEM\", \"actor_process_logon_id\": \"1003\", \"action_file_type\": \"0\", \"manifest_file_version\": \"5\", \"actor_process_instance_id\": \"AdgdeB26mNQAAAAEAAAAAA==\", \"actor_process_causality_id\": \"AdgdeB26mNQAAAAEAAAAAA==\", \"actor_process_auth_id\": \"999\", \"actor_process_signature_vendor\": \"Microsoft Corporation\", \"actor_process_signature_status\": \"SIGNED\", \"actor_process_signature_product\": \"Microsoft Windows\", \"actor_process_execution_time\": \"1644385473948\", \"actor_process_is_native\": \"TRUE\", \"agent_version\": \"7.6.1.46600\", \"agent_hostname\": \"EC2AMAZ-IQFSLIL\", \"agent_content_version\": \"380-82571\", \"agent_session_start_time\": \"1644385496543\", \"agent_id\": \"37a92aad549d41d184ec9fbdafbff55c\", \"agent_os_type\": \"AGENT_OS_WINDOWS\", \"agent_os_sub_type\": \"Windows Server 2016 [10.0 (Build 17763)]\", \"agent_is_vdi\": \"FALSE\", \"event_id\": \"AAABfvWCZpMqn9UKACRWUw==\", \"event_timestamp\": \"1644796471001\", \"event_version\": \"25\", \"event_type\": \"FILE\", \"event_sub_type\": \"FILE_WRITE\" } } ]" 
"{\"stix_validator\": true}"
```

#### STIX Translate results - output
```json
{
    "type": "bundle",
    "id": "bundle--de01a54d-dd8d-4005-b640-29e68c24d976",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "paloalto",
            "identity_class": "system",
            "created": "2022-03-16T13:22:50.336Z",
            "modified": "2022-03-16T13:22:50.336Z"
        },
        {
            "id": "observed-data--ce1c1768-d2ad-41bd-a3d3-d11bf2ae3d94",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-05T13:01:57.723Z",
            "modified": "2022-04-05T13:01:57.723Z",
            "objects": {
                "0": {
                    "type": "ipv4-addr",
                    "value": "172.31.31.67"
                },
                "2": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "0"
                    ],
                    "extensions": {
                        "x-paloalto-agent": {
                            "agent_version": "7.6.1.46600",
                            "content_version": "380-82571",
                            "start_time": "2022-02-09T05:44:56.543Z",
                            "asset_id": "37a92aad549d41d184ec9fbdafbff55c",
                            "os_type": "AGENT_OS_WINDOWS",
                            "os_sub_type": "Windows Server 2016 [10.0 (Build 17763)]",
                            "is_vdi": false
                        }
                    },
                    "hostname": "EC2AMAZ-IQFSLIL"
                },
                "3": {
                    "type": "file",
                    "name": "DRIVERS",
                    "size": 4255744,
                    "parent_directory_ref": "13",
                    "extensions": {
                        "x-paloalto-file": {
                            "attributes": 128,
                            "type": 18,
                            "manifest_version": 5
                        }
                    }
                },
                "4": {
                    "type": "x-oca-event",
                    "file_ref": "3",
                    "process_ref": "6",
                    "parent_process_ref": "8",
                    "agent": "EC2AMAZ-IQFSLIL",
                    "code": "AAABfvQtkk8qn9UKACE2JA==",
                    "created": "2022-02-13T17:42:14.407Z",
                    "extensions": {
                        "x-paloalto-event": {
                            "version": 25
                        }
                    },
                    "category": [
                        "file"
                    ],
                    "action": "FILE_OPEN"
                },
                "5": {
                    "type": "file",
                    "name": "System"
                },
                "6": {
                    "type": "process",
                    "name": "System",
                    "binary_ref": "5",
                    "pid": 4,
                    "x_unique_id": "AdgdeB26mNQAAAAEAAAAAA==",
                    "extensions": {
                        "x-paloalto-process": {
                            "causality_id": "AdgdeB26mNQAAAAEAAAAAA==",
                            "auth_id": "999",
                            "signature_vendor": "Microsoft Corporation",
                            "signature_status": "SIGNED",
                            "signature_product": "Microsoft Windows",
                            "execution_time": "2022-02-09T05:44:33.948Z",
                            "is_native": true
                        }
                    }
                },
                "7": {
                    "type": "file",
                    "name": "System"
                },
                "8": {
                    "type": "process",
                    "name": "System"
                },
                "9": {
                    "type": "process",
                    "parent_ref": "8",
                    "binary_ref": "7",
                    "pid": 4
                },
                "10": {
                    "type": "file",
                    "name": "System"
                },
                "11": {
                    "type": "process",
                    "name": "System"
                },
                "12": {
                    "type": "process",
                    "parent_ref": "11",
                    "binary_ref": "10",
                    "pid": 4
                },
                "13": {
                    "type": "directory",
                    "path": "C:\\Windows\\System32\\config"
                },
                "14": {
                    "type": "user-account",
                    "user_id": "S-1-5-18",
                    "display_name": "NT AUTHORITY\\SYSTEM",
                    "account_login": "1003"
                }
            },
            "first_observed": "2022-04-05T16:17:58.820Z",
            "last_observed": "2022-04-05T16:17:58.820Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--f3a29cc9-e4e1-431f-943c-edf91e42edc5",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-05T13:01:57.731Z",
            "modified": "2022-04-05T13:01:57.731Z",
            "objects": {
                "0": {
                    "type": "ipv4-addr",
                    "value": "172.31.31.67"
                },
                "2": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "0"
                    ],
                    "extensions": {
                        "x-paloalto-agent": {
                            "agent_version": "7.6.1.46600",
                            "content_version": "380-82571",
                            "start_time": "2022-02-09T05:44:56.543Z",
                            "asset_id": "37a92aad549d41d184ec9fbdafbff55c",
                            "os_type": "AGENT_OS_WINDOWS",
                            "os_sub_type": "Windows Server 2016 [10.0 (Build 17763)]",
                            "is_vdi": false
                        }
                    },
                    "hostname": "EC2AMAZ-IQFSLIL"
                },
                "3": {
                    "type": "file",
                    "name": "DRIVERS",
                    "size": 4255744,
                    "parent_directory_ref": "13",
                    "extensions": {
                        "x-paloalto-file": {
                            "type": 0,
                            "manifest_version": 5
                        }
                    }
                },
                "4": {
                    "type": "x-oca-event",
                    "file_ref": "3",
                    "process_ref": "6",
                    "parent_process_ref": "8",
                    "agent": "EC2AMAZ-IQFSLIL",
                    "code": "AAABfvWCZpMqn9UKACRWUw==",
                    "created": "2022-02-13T23:54:31.001Z",
                    "extensions": {
                        "x-paloalto-event": {
                            "version": 25
                        }
                    },
                    "category": [
                        "file"
                    ],
                    "action": "FILE_WRITE"
                },
                "5": {
                    "type": "file",
                    "name": "System"
                },
                "6": {
                    "type": "process",
                    "name": "System",
                    "binary_ref": "5",
                    "pid": 4,
                    "x_unique_id": "AdgdeB26mNQAAAAEAAAAAA==",
                    "extensions": {
                        "x-paloalto-process": {
                            "causality_id": "AdgdeB26mNQAAAAEAAAAAA==",
                            "auth_id": "999",
                            "signature_vendor": "Microsoft Corporation",
                            "signature_status": "SIGNED",
                            "signature_product": "Microsoft Windows",
                            "execution_time": "2022-02-09T05:44:33.948Z",
                            "is_native": true
                        }
                    }
                },
                "7": {
                    "type": "file",
                    "name": "System"
                },
                "8": {
                    "type": "process",
                    "name": "System"
                },
                "9": {
                    "type": "process",
                    "parent_ref": "8",
                    "binary_ref": "7",
                    "pid": 4
                },
                "10": {
                    "type": "file",
                    "name": "System"
                },
                "11": {
                    "type": "process",
                    "name": "System"
                },
                "12": {
                    "type": "process",
                    "parent_ref": "11",
                    "binary_ref": "10",
                    "pid": 4
                },
                "13": {
                    "type": "directory",
                    "path": "C:\\Windows\\System32\\config"
                },
                "14": {
                    "type": "user-account",
                    "user_id": "S-1-5-18",
                    "display_name": "NT AUTHORITY\\SYSTEM",
                    "account_login": "1003"
                }
            },
            "first_observed": "2022-04-05T13:01:57.731Z",
            "last_observed": "2022-04-05T13:01:57.731Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```
#### STIX Execute query
```shell
execute
paloalto
paloalto
"{\"type\":\"identity\",\"id\":\"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\",\"name\":\"paloalto\",\"identity_class\":\"system\",\"created\":\"2022-03-16T13:22:50.336Z\",\"modified\":\"2022-03-16T13:22:50.336Z\"}"
"{\"host\":\"xx.xx.xx\"}"
"{\"auth\":{\"api_key\": \"xxxx\", \"api_key_id\": \"xx\",\"tenant\":\"xxxx\"}}"
"[file:name = 'chrome.exe' ] START t'2022-01-16T11:00:00.000Z' STOP t'2022-01-20T11:00:00.003Z'"
```
#### STIX Execute query - output
```json
{
    "type": "bundle",
    "id": "bundle--1683947d-9c7e-4d35-b70b-a0ccc90d5cba",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "paloalto",
            "identity_class": "system",
            "created": "2022-03-16T13:22:50.336Z",
            "modified": "2022-03-16T13:22:50.336Z"
        },
        {
            "id": "observed-data--34da8902-db25-4388-8312-526347de345d",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-05T13:05:20.377Z",
            "modified": "2022-04-05T13:05:20.377Z",
            "objects": {
                "0": {
                    "type": "ipv4-addr",
                    "value": "172.31.31.236"
                },
                "2": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "0"
                    ],
                    "extensions": {
                        "x-paloalto-agent": {
                            "agent_version": "7.6.1.46600",
                            "content_version": "350-80787",
                            "start_time": "2022-01-19T10:02:28.366Z",
                            "asset_id": "f344796340f84d0ca7e0fdaedbcbd594",
                            "os_type": "AGENT_OS_WINDOWS",
                            "os_sub_type": "Windows Server 2016 [10.0 (Build 14393)]",
                            "is_vdi": false
                        }
                    },
                    "hostname": "EC2AMAZ-65BN1IK"
                },
                "3": {
                    "type": "file",
                    "name": "Network Persistent State",
                    "size": 4595,
                    "parent_directory_ref": "13",
                    "extensions": {
                        "x-paloalto-file": {
                            "attributes": 0,
                            "type": 18,
                            "manifest_version": 5
                        }
                    }
                },
                "4": {
                    "type": "x-oca-event",
                    "file_ref": "3",
                    "process_ref": "6",
                    "parent_process_ref": "8",
                    "agent": "EC2AMAZ-65BN1IK",
                    "code": "AAABfnYIxcPunpI7AATXuQ==",
                    "created": "2022-01-20T05:49:53.598Z",
                    "extensions": {
                        "x-paloalto-event": {
                            "version": 25
                        }
                    },
                    "category": ["file"],
                    "action": "FILE_OPEN"
                },
                "5": {
                    "type": "file",
                    "name": "chrome.exe",
                    "accessed": "2021-12-15T22:05:27.664Z",
                    "modified": "2021-12-12T08:19:30.068Z",
                    "parent_directory_ref": "14"
                },
                "6": {
                    "type": "process",
                    "name": "chrome.exe",
                    "binary_ref": "5",
                    "command_line": "\"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\" --type=utility --utility-sub-type=network.mojom.NetworkService --field-trial-handle=1456,2805956566820005361,12799224617572967118,131072 --lang=en-US --service-sandbox-type=none --mojo-platform-channel-handle=1772 /prefetch:8",
                    "created": "2021-11-10T06:59:32.948Z",
                    "pid": 4724,
                    "extensions": {
                        "x-paloalto-process": {
                            "instance_id": "AdgAs0xnjjUAABJ0AAAAAA==",
                            "causality_id": "AdgAs0qzIE0AABHcAAAAAA==",
                            "auth_id": "999",
                            "signature_vendor": "Google LLC",
                            "signature_status": "SIGNED",
                            "signature_product": "Google LLC",
                            "extension": "exe",
                            "execution_time": "2022-01-03T15:05:08.844Z",
                            "is_native": true
                        }
                    }
                },
                "7": {
                    "type": "file",
                    "name": "chrome.exe",
                    "parent_directory_ref": "15"
                },
                "8": {
                    "type": "process",
                    "name": "chrome.exe"
                },
                "9": {
                    "type": "process",
                    "parent_ref": "8",
                    "binary_ref": "7",
                    "command_line": "\"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\" --flag-switches-begin --flag-switches-end --origin-trial-disabled-features=CaptureHandle",
                    "created": "2021-11-10T06:59:32.948Z",
                    "pid": 4572
                },
                "10": {
                    "type": "file",
                    "name": "chrome.exe",
                    "accessed": "2021-12-15T22:05:27.664Z",
                    "modified": "2021-12-12T08:19:30.068Z",
                    "parent_directory_ref": "16"
                },
                "11": {
                    "type": "process",
                    "name": "chrome.exe"
                },
                "12": {
                    "type": "process",
                    "parent_ref": "11",
                    "binary_ref": "10",
                    "command_line": "\"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\" --type=utility --utility-sub-type=network.mojom.NetworkService --field-trial-handle=1456,2805956566820005361,12799224617572967118,131072 --lang=en-US --service-sandbox-type=none --mojo-platform-channel-handle=1772 /prefetch:8",
                    "created": "2021-11-10T06:59:32.948Z",
                    "pid": 4724
                },
                "13": {
                    "type": "directory",
                    "path": "C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Network"
                },
                "14": {
                    "type": "directory",
                    "path": "C:\\Program Files\\Google\\Chrome\\Application"
                },
                "15": {
                    "type": "directory",
                    "path": "C:\\Program Files\\Google\\Chrome\\Application"
                },
                "16": {
                    "type": "directory",
                    "path": "C:\\Program Files\\Google\\Chrome\\Application"
                },
                "17": {
                    "type": "user-account",
                    "user_id": "S-1-5-21-3039464837-300237904-2407637926-500",
                    "display_name": "EC2AMAZ-65BN1IK\\Administrator",
                    "account_login": "1003"
                }
            },
            "x_actor_process_last_observed": "2021-12-15T22:05:27.664Z",
            "x_os_actor_process_last_observed": "2021-12-15T22:05:27.664Z",
            "x_process_actor_first_observed": "2021-11-10T06:59:32.948Z",
            "x_process_causality_actor_first_observed": "2021-11-10T06:59:32.948Z",
            "x_process_os_actor_first_observed": "2021-11-10T06:59:32.948Z",
            "first_observed": "2022-04-05T13:05:20.377Z",
            "last_observed": "2022-04-05T13:05:20.377Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```

### Limitations
- Each XQL API query entails a cost of query units calculated according to the complexity and number of search results.
- Queries called without enough quota will fail.

### Observations
- The quota limit range for the API call would be from 1 to 15 (Standard 5 + 10 Additional ) units. 
  The default value of quota thershold limit in CP4S UI is 5. 
- If the user purchases standard license only(5 units), and configures the threshold value more than 5, 
  the usage limit will be checked only for 5 units. Otherwise, usage will be checked for the configured value.
- If the user purchases Additional 10 units along with standard license, the usage limit will be checked for configured value.   

### References
- [Cortex XDR](https://docs.paloaltonetworks.com/cortex/cortex-xdr.html)
- [Get Started with XQL](https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-xql-language-reference/get-started-with-xql.html)
- [Cortex XDR™ XQL Schema Reference](https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-xql-schema-reference.html)
- [Cortex XDR API Overview](https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-api/cortex-xdr-api-overview.html)
