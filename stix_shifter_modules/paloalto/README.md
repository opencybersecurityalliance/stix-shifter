# PaloAlto Cortex XDR Connector

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
                "query": "dataset = xdr_data | filter ((action_local_ip = \"1.1.0.0\" or action_remote_ip = \"1.1.0.0\")  and (to_epoch(_time,\"millis\") >= 1646132400000 and to_epoch(_time,\"millis\") <= 1678273200003)) | alter dataset_name = \"xdr_data\" | fields dataset_name,action_local_ip,action_remote_ip,agent_ip_addresses_v6,dst_agent_ip_addresses_v6,action_local_port,action_remote_port,action_network_protocol,action_pkts_sent,action_pkts_received,action_file_name,action_process_image_name,actor_process_image_name,causality_actor_process_image_name,os_actor_process_image_name,action_file_size,action_file_md5,action_module_md5,action_process_image_md5,action_file_authenticode_sha1,action_file_authenticode_sha2,action_file_sha256,action_module_sha256,action_process_image_sha256,action_file_access_time,actor_process_file_access_time,os_actor_process_file_access_time,action_file_mod_time,actor_process_file_mod_time,os_actor_process_file_mod_time,action_file_create_time,action_file_path,action_process_image_path,action_registry_file_path,actor_process_image_path,causality_actor_process_image_path,os_actor_process_image_path,action_process_image_command_line,actor_process_command_line,causality_actor_process_command_line,os_actor_process_command_line,action_process_file_create_time,actor_process_file_create_time,causality_actor_process_file_create_time,os_actor_process_file_create_time,action_module_process_os_pid,action_process_os_pid,actor_process_os_pid,causality_actor_process_os_pid,os_actor_process_os_pid,action_process_requested_parent_pid,action_thread_parent_pid,action_thread_child_pid,action_process_username,auth_domain,dst_host_metadata_domain,host_metadata_domain,dst_action_url_category,action_registry_key_name,action_registry_value_name,mac,associated_mac,dst_associated_mac,dst_mac,actor_primary_user_sid,action_process_user_sid,actor_primary_username,actor_process_logon_id,action_file_info_company,action_file_extension,action_file_attributes,action_file_internal_zipped_files,action_file_last_writer_actor,action_file_signature_status,action_file_signature_vendor,action_file_signature_product,action_file_info_description,action_file_group,action_file_group_name,action_file_type,action_file_info_file_version,manifest_file_version,action_file_info_product_version,action_file_owner,action_file_owner_name,action_file_info_product_name,action_file_id,action_file_wildfire_verdict,action_file_hash_control_verdict,actor_process_instance_id,actor_process_causality_id,actor_process_auth_id,actor_process_container_id,actor_process_signature_vendor,actor_process_signature_status,actor_process_signature_product,actor_process_image_extension,action_process_termination_code,action_process_termination_date,action_remote_process_thread_id,action_process_instance_execution_time,actor_process_execution_time,action_process_handle_is_kernel,action_process_is_container_root,actor_process_is_native,agent_version,agent_hostname,agent_content_version,agent_session_start_time,agent_id,agent_os_type,agent_os_sub_type,agent_is_vdi,action_user_agent,http_req_user_agent_header,action_evtlog_data_fields,action_evtlog_description,action_evtlog_source,action_evtlog_event_id,action_evtlog_level,action_evtlog_tid,action_evtlog_uid,action_evtlog_pid,action_evtlog_message,action_evtlog_version,event_id,vpn_event_description,event_timestamp,event_version,event_rpc_interface_uuid,event_address_mapped_image_path,event_type,event_sub_type,action_network_creation_time,action_network_connection_id,action_network_packet_data,action_proxy,host_metadata_hostname,action_external_hostname | limit 1000 ",
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
"{ \"xdr_data\": { \"query\": \"dataset = xdr_data | filter ((action_local_ip = \\"1.1.0.0\\" or action_remote_ip = \\"1.1.0.0\\")  and (to_epoch(_time,\\"millis\\") >= 1646132400000 and to_epoch(_time,\\"millis\\") <= 1678273200003)) | alter dataset_name = \\"xdr_data\\" | fields dataset_name,action_local_ip,action_remote_ip,agent_ip_addresses_v6,dst_agent_ip_addresses_v6,action_local_port,action_remote_port,action_network_protocol,action_pkts_sent,action_pkts_received,action_file_name,action_process_image_name,actor_process_image_name,causality_actor_process_image_name,os_actor_process_image_name,action_file_size,action_file_md5,action_module_md5,action_process_image_md5,action_file_authenticode_sha1,action_file_authenticode_sha2,action_file_sha256,action_module_sha256,action_process_image_sha256,action_file_access_time,actor_process_file_access_time,os_actor_process_file_access_time,action_file_mod_time,actor_process_file_mod_time,os_actor_process_file_mod_time,action_file_create_time,action_file_path,action_process_image_path,action_registry_file_path,actor_process_image_path,causality_actor_process_image_path,os_actor_process_image_path,action_process_image_command_line,actor_process_command_line,causality_actor_process_command_line,os_actor_process_command_line,action_process_file_create_time,actor_process_file_create_time,causality_actor_process_file_create_time,os_actor_process_file_create_time,action_module_process_os_pid,action_process_os_pid,actor_process_os_pid,causality_actor_process_os_pid,os_actor_process_os_pid,action_process_requested_parent_pid,action_thread_parent_pid,action_thread_child_pid,action_process_username,auth_domain,dst_host_metadata_domain,host_metadata_domain,dst_action_url_category,action_registry_key_name,action_registry_value_name,mac,associated_mac,dst_associated_mac,dst_mac,actor_primary_user_sid,action_process_user_sid,actor_primary_username,actor_process_logon_id,action_file_info_company,action_file_extension,action_file_attributes,action_file_internal_zipped_files,action_file_last_writer_actor,action_file_signature_status,action_file_signature_vendor,action_file_signature_product,action_file_info_description,action_file_group,action_file_group_name,action_file_type,action_file_info_file_version,manifest_file_version,action_file_info_product_version,action_file_owner,action_file_owner_name,action_file_info_product_name,action_file_id,action_file_wildfire_verdict,action_file_hash_control_verdict,actor_process_instance_id,actor_process_causality_id,actor_process_auth_id,actor_process_container_id,actor_process_signature_vendor,actor_process_signature_status,actor_process_signature_product,actor_process_image_extension,action_process_termination_code,action_process_termination_date,action_remote_process_thread_id,action_process_instance_execution_time,actor_process_execution_time,action_process_handle_is_kernel,action_process_is_container_root,actor_process_is_native,agent_version,agent_hostname,agent_content_version,agent_session_start_time,agent_id,agent_os_type,agent_os_sub_type,agent_is_vdi,action_user_agent,http_req_user_agent_header,action_evtlog_data_fields,action_evtlog_description,action_evtlog_source,action_evtlog_event_id,action_evtlog_level,action_evtlog_tid,action_evtlog_uid,action_evtlog_pid,action_evtlog_message,action_evtlog_version,event_id,vpn_event_description,event_timestamp,event_version,event_rpc_interface_uuid,event_address_mapped_image_path,event_type,event_sub_type,action_network_creation_time,action_network_connection_id,action_network_packet_data,action_proxy,host_metadata_hostname,action_external_hostname | limit 1000 \", \"timeframe\": { \"from\": 1646132400000, \"to\": 1678273200003 } } }"
```

#### STIX Transmit query - output
```json
{
    "success": true,
    "search_id": "d84862b9b7254a_22989_inv"
}
```
#### STIX Transmit status 

```shell
transmit
paloalto
"{\"host\":\"xx.xx.xx\"}"
"{\"auth\":{\"api_key\": \"xxxx\", \"api_key_id\": \"xx\",\"tenant\":\"xxxx\"}}"
status
"d84862b9b7254a_22989_inv"
```

#### STIX Transmit status - output
```json
{
    "success": true,
    "status": "COMPLETED"
}
```
#### STIX Transmit results 

```shell
transmit
paloalto
"{\"host\":\"xx.xx.xx\"}"
"{\"auth\":{\"api_key\": \"xxxx\", \"api_key_id\": \"xx\",\"tenant\":\"xxxx\"}}"
results
"d84862b9b7254a_22989_inv" 0 2
```

#### STIX Transmit results - output
```json
{
    "success": true,
    "data": [
        {
            "xdr_data": {
                "action_network_protocol": "TCP",
                "action_local_ip": "193.93.62.47",
                "action_remote_ip": "1.1.0.0",
                "action_local_port": 31029,
                "action_remote_port": 3389,
                "agent_id": "193.93.62.47",
                "event_id": "MTM4NTk0MDcwNDA4NDQ0MzIwNw==",
                "event_timestamp": 1646799589433,
                "action_network_creation_time": 1646799589433,
                "action_network_connection_id": "AdgzbOqYRXkAAAAAAB+exg==",
                "action_proxy": "FALSE",
                "event_type": "STORY",
                "event_sub_type": "event_sub_type_4"
            }
        },
        {
            "xdr_data": {
                "action_network_protocol": "TCP",
                "action_local_ip": "193.93.62.6",
                "action_remote_ip": "1.1.0.0",
                "action_local_port": 47275,
                "action_remote_port": 3389,
                "agent_id": "193.93.62.6",
                "event_id": "Nzc2MzU5MjE1NjE4NTYzNDI4OA==",
                "event_timestamp": 1646799556894,
                "action_network_creation_time": 1646799556894,
                "action_network_connection_id": "AdgzbNczNawAAAAAAB+euA==",
                "action_proxy": "FALSE",
                "event_type": "STORY",
                "event_sub_type": "event_sub_type_4"
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
"{\"type\":\"identity\",\"id\":\"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\",\"name\":\"paloalto\",\"identity_class\":\"events\"}"
" [ { \"xdr_data\": { \"action_network_protocol\": \"TCP\", \"action_local_ip\": \"193.93.62.47\", \"action_remote_ip\": \"1.1.0.0\", \"action_local_port\": 31029, \"action_remote_port\": 3389, \"agent_id\": \"193.93.62.47\", \"event_id\": \"MTM4NTk0MDcwNDA4NDQ0MzIwNw==\", \"event_timestamp\": 1646799589433, \"action_network_creation_time\": 1646799589433, \"action_network_connection_id\": \"AdgzbOqYRXkAAAAAAB+exg==\", \"action_proxy\": \"FALSE\", \"event_type\": \"STORY\", \"event_sub_type\": \"event_sub_type_4\" } }, { \"xdr_data\": { \"action_network_protocol\": \"TCP\", \"action_local_ip\": \"193.93.62.6\", \"action_remote_ip\": \"1.1.0.0\", \"action_local_port\": 47275, \"action_remote_port\": 3389, \"agent_id\": \"193.93.62.6\", \"event_id\": \"Nzc2MzU5MjE1NjE4NTYzNDI4OA==\", \"event_timestamp\": 1646799556894, \"action_network_creation_time\": 1646799556894, \"action_network_connection_id\": \"AdgzbNczNawAAAAAAB+euA==\", \"action_proxy\": \"FALSE\", \"event_type\": \"STORY\", \"event_sub_type\": \"event_sub_type_4\" } } ] "
"{\"stix_validator\": true}"
```

#### STIX Translate results - output
```json
{
    "type": "bundle",
    "id": "bundle--c7d5cb7b-bfc2-4964-be1a-596a4eb37f72",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "paloalto",
            "identity_class": "events"
        },
        {
            "id": "observed-data--875927c9-575f-4410-bdf6-9bc6060b204c",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-03-09T08:08:41.394Z",
            "modified": "2022-03-09T08:08:41.394Z",
            "objects": {
                "0": {
                    "type": "network-traffic",
                    "protocols": [
                        "tcp"
                    ],
                    "src_ref": "1",
                    "dst_ref": "2",
                    "src_port": 31029,
                    "dst_port": 3389,
                    "extensions": {
                        "x-paloalto-network": {
                            "creation_time": "2022-03-09T04:19:49.433Z",
                            "connection_id": "AdgzbOqYRXkAAAAAAB+exg==",
                            "is_proxy": false
                        }
                    }
                },
                "1": {
                    "type": "ipv4-addr",
                    "value": "193.93.62.47"
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "1.1.0.0"
                },
                "3": {
                    "type": "x-oca-asset",
                    "asset_id": "193.93.62.47"
                },
                "4": {
                    "type": "x-oca-event",
                    "event_id": "MTM4NTk0MDcwNDA4NDQ0MzIwNw==",
                    "time": "2022-03-09T04:19:49.433Z",
                    "event_type": "STORY",
                    "sub_type": "event_sub_type_4"
                }
            },
            "first_observed": "2022-03-09T08:08:41.394Z",
            "last_observed": "2022-03-09T08:08:41.394Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--3b1d6e6b-95ea-406f-aafb-aa5e4056640b",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-03-09T08:08:51.467Z",
            "modified": "2022-03-09T08:08:51.467Z",
            "objects": {
                "0": {
                    "type": "network-traffic",
                    "protocols": [
                        "tcp"
                    ],
                    "src_ref": "1",
                    "dst_ref": "2",
                    "src_port": 47275,
                    "dst_port": 3389,
                    "extensions": {
                        "x-paloalto-network": {
                            "creation_time": "2022-03-09T04:19:16.894Z",
                            "connection_id": "AdgzbNczNawAAAAAAB+euA==",
                            "is_proxy": false
                        }
                    }
                },
                "1": {
                    "type": "ipv4-addr",
                    "value": "193.93.62.6"
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "1.1.0.0"
                },
                "3": {
                    "type": "x-oca-asset",
                    "asset_id": "193.93.62.6"
                },
                "4": {
                    "type": "x-oca-event",
                    "event_id": "Nzc2MzU5MjE1NjE4NTYzNDI4OA==",
                    "time": "2022-03-09T04:19:16.894Z",
                    "event_type": "STORY",
                    "sub_type": "event_sub_type_4"
                }
            },
            "first_observed": "2022-03-09T08:08:51.467Z",
            "last_observed": "2022-03-09T08:08:51.467Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```

### Multiple Observation  

#### STIX Translate query
```shell
translate paloalto query {} "([x-oca-event:event_type = 'file'] AND [file:size > 3000] OR [x-oca-asset:agent_version = '7.6.1.46600'] )START t'2022-02-10T00:00:00.000000Z' STOP t'2022-02-15T00:00:00.000000Z'"
```

#### STIX Translate query - output

```json
{
    "queries": [
        {
            "xdr_data": {
                "query": "dataset = xdr_data | filter (event_type = ENUM.FILE  and (to_epoch(_time,\"millis\") >= 1644451200000 and to_epoch(_time,\"millis\") <= 1644883200000)) or (action_file_size > 3000  and (to_epoch(_time,\"millis\") >= 1644451200000 and to_epoch(_time,\"millis\") <= 1644883200000)) or (agent_version = \"7.6.1.46600\"  and (to_epoch(_time,\"millis\") >= 1644451200000 and to_epoch(_time,\"millis\") <= 1644883200000)) | alter dataset_name = \"xdr_data\" | fields dataset_name,action_local_ip,action_remote_ip,agent_ip_addresses_v6,dst_agent_ip_addresses_v6,action_local_port,action_remote_port,action_network_protocol,action_pkts_sent,action_pkts_received,action_file_name,action_process_image_name,actor_process_image_name,causality_actor_process_image_name,os_actor_process_image_name,action_file_size,action_file_md5,action_module_md5,action_process_image_md5,action_file_authenticode_sha1,action_file_authenticode_sha2,action_file_sha256,action_module_sha256,action_process_image_sha256,action_file_access_time,actor_process_file_access_time,os_actor_process_file_access_time,action_file_mod_time,actor_process_file_mod_time,os_actor_process_file_mod_time,action_file_create_time,action_file_path,action_process_image_path,action_registry_file_path,actor_process_image_path,causality_actor_process_image_path,os_actor_process_image_path,action_process_image_command_line,actor_process_command_line,causality_actor_process_command_line,os_actor_process_command_line,action_process_file_create_time,actor_process_file_create_time,causality_actor_process_file_create_time,os_actor_process_file_create_time,action_module_process_os_pid,action_process_os_pid,actor_process_os_pid,causality_actor_process_os_pid,os_actor_process_os_pid,action_process_requested_parent_pid,action_thread_parent_pid,action_thread_child_pid,action_process_username,auth_domain,dst_host_metadata_domain,host_metadata_domain,dst_action_url_category,action_registry_key_name,action_registry_value_name,mac,associated_mac,dst_associated_mac,dst_mac,actor_primary_user_sid,action_process_user_sid,actor_primary_username,actor_process_logon_id,action_file_info_company,action_file_extension,action_file_attributes,action_file_internal_zipped_files,action_file_last_writer_actor,action_file_signature_status,action_file_signature_vendor,action_file_signature_product,action_file_info_description,action_file_group,action_file_group_name,action_file_type,action_file_info_file_version,manifest_file_version,action_file_info_product_version,action_file_owner,action_file_owner_name,action_file_info_product_name,action_file_id,action_file_wildfire_verdict,action_file_hash_control_verdict,actor_process_instance_id,actor_process_causality_id,actor_process_auth_id,actor_process_container_id,actor_process_signature_vendor,actor_process_signature_status,actor_process_signature_product,actor_process_image_extension,action_process_termination_code,action_process_termination_date,action_remote_process_thread_id,action_process_instance_execution_time,actor_process_execution_time,action_process_handle_is_kernel,action_process_is_container_root,actor_process_is_native,agent_version,agent_hostname,agent_content_version,agent_session_start_time,agent_id,agent_os_type,agent_os_sub_type,agent_is_vdi,action_user_agent,http_req_user_agent_header,action_evtlog_data_fields,action_evtlog_description,action_evtlog_source,action_evtlog_event_id,action_evtlog_level,action_evtlog_tid,action_evtlog_uid,action_evtlog_pid,action_evtlog_message,action_evtlog_version,event_id,vpn_event_description,event_timestamp,event_version,event_rpc_interface_uuid,event_address_mapped_image_path,event_type,event_sub_type,action_network_creation_time,action_network_connection_id,action_network_packet_data,action_proxy,host_metadata_hostname,action_external_hostname | limit 1000 ",
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
" { \"xdr_data\": { \"query\": \"dataset = xdr_data | filter (event_type = ENUM.FILE  and (to_epoch(_time,\\"millis\\") >= 1644451200000 and to_epoch(_time,\\"millis\\") <= 1644883200000)) or (action_file_size > 3000  and (to_epoch(_time,\\"millis\\") >= 1644451200000 and to_epoch(_time,\\"millis\\") <= 1644883200000)) or (agent_version = \\"7.6.1.46600\\"  and (to_epoch(_time,\\"millis\\") >= 1644451200000 and to_epoch(_time,\\"millis\\") <= 1644883200000)) | alter dataset_name = \\"xdr_data\\" | fields dataset_name,action_local_ip,action_remote_ip,agent_ip_addresses_v6,dst_agent_ip_addresses_v6,action_local_port,action_remote_port,action_network_protocol,action_pkts_sent,action_pkts_received,action_file_name,action_process_image_name,actor_process_image_name,causality_actor_process_image_name,os_actor_process_image_name,action_file_size,action_file_md5,action_module_md5,action_process_image_md5,action_file_authenticode_sha1,action_file_authenticode_sha2,action_file_sha256,action_module_sha256,action_process_image_sha256,action_file_access_time,actor_process_file_access_time,os_actor_process_file_access_time,action_file_mod_time,actor_process_file_mod_time,os_actor_process_file_mod_time,action_file_create_time,action_file_path,action_process_image_path,action_registry_file_path,actor_process_image_path,causality_actor_process_image_path,os_actor_process_image_path,action_process_image_command_line,actor_process_command_line,causality_actor_process_command_line,os_actor_process_command_line,action_process_file_create_time,actor_process_file_create_time,causality_actor_process_file_create_time,os_actor_process_file_create_time,action_module_process_os_pid,action_process_os_pid,actor_process_os_pid,causality_actor_process_os_pid,os_actor_process_os_pid,action_process_requested_parent_pid,action_thread_parent_pid,action_thread_child_pid,action_process_username,auth_domain,dst_host_metadata_domain,host_metadata_domain,dst_action_url_category,action_registry_key_name,action_registry_value_name,mac,associated_mac,dst_associated_mac,dst_mac,actor_primary_user_sid,action_process_user_sid,actor_primary_username,actor_process_logon_id,action_file_info_company,action_file_extension,action_file_attributes,action_file_internal_zipped_files,action_file_last_writer_actor,action_file_signature_status,action_file_signature_vendor,action_file_signature_product,action_file_info_description,action_file_group,action_file_group_name,action_file_type,action_file_info_file_version,manifest_file_version,action_file_info_product_version,action_file_owner,action_file_owner_name,action_file_info_product_name,action_file_id,action_file_wildfire_verdict,action_file_hash_control_verdict,actor_process_instance_id,actor_process_causality_id,actor_process_auth_id,actor_process_container_id,actor_process_signature_vendor,actor_process_signature_status,actor_process_signature_product,actor_process_image_extension,action_process_termination_code,action_process_termination_date,action_remote_process_thread_id,action_process_instance_execution_time,actor_process_execution_time,action_process_handle_is_kernel,action_process_is_container_root,actor_process_is_native,agent_version,agent_hostname,agent_content_version,agent_session_start_time,agent_id,agent_os_type,agent_os_sub_type,agent_is_vdi,action_user_agent,http_req_user_agent_header,action_evtlog_data_fields,action_evtlog_description,action_evtlog_source,action_evtlog_event_id,action_evtlog_level,action_evtlog_tid,action_evtlog_uid,action_evtlog_pid,action_evtlog_message,action_evtlog_version,event_id,vpn_event_description,event_timestamp,event_version,event_rpc_interface_uuid,event_address_mapped_image_path,event_type,event_sub_type,action_network_creation_time,action_network_connection_id,action_network_packet_data,action_proxy,host_metadata_hostname,action_external_hostname | limit 1000 \", \"timeframe\": { \"from\": 1644451200000, \"to\": 1644883200000 } } }"
```

#### STIX Transmit query - output

```json
{
    "success": true,
    "search_id": "8c1c048e556c4b_23040_inv"
}
```
#### STIX Transmit status 

```shell
transmit
paloalto
"{\"host\":\"xx.xx.xx\"}"
"{\"auth\":{\"api_key\": \"xxxx\", \"api_key_id\": \"xx\",\"tenant\":\"xxxx\"}}"
status
"8c1c048e556c4b_23040_inv"
```

#### STIX Transmit status - output
```json
{
    "success": true,
    "status": "COMPLETED"
}
```
#### STIX Transmit results 

```shell
transmit
paloalto
"{\"host\":\"xx.xx.xx\"}"
"{\"auth\":{\"api_key\": \"xxxx\", \"api_key_id\": \"xx\",\"tenant\":\"xxxx\"}}"
results
"8c1c048e556c4b_23040_inv" 0 2
```

#### STIX Transmit results - output
```json
{
    "success": true,
    "data": [
        {
            "xdr_data": {
                "action_file_name": "MpWppTracing-20220210-055530-00000003-ffffffff.bin",
                "actor_process_image_name": "System",
                "causality_actor_process_image_name": "System",
                "os_actor_process_image_name": "System",
                "action_file_path": "C:\\ProgramData\\Microsoft\\Windows Defender\\Support\\MpWppTracing-20220210-055530-00000003-ffffffff.bin",
                "actor_process_image_path": "System",
                "causality_actor_process_image_path": "System",
                "os_actor_process_image_path": "System",
                "actor_process_os_pid": 4,
                "causality_actor_process_os_pid": 4,
                "os_actor_process_os_pid": 4,
                "actor_primary_user_sid": "S-1-5-18",
                "actor_primary_username": "NT AUTHORITY\\SYSTEM",
                "actor_process_logon_id": "1003",
                "action_file_extension": "bin",
                "action_file_type": 18,
                "manifest_file_version": 5,
                "actor_process_instance_id": "AdgdeB26mNQAAAAEAAAAAA==",
                "actor_process_causality_id": "AdgdeB26mNQAAAAEAAAAAA==",
                "actor_process_auth_id": "999",
                "actor_process_signature_vendor": "Microsoft Corporation",
                "actor_process_signature_product": "Microsoft Windows",
                "actor_process_execution_time": 1644385473948,
                "agent_version": "7.6.1.46600",
                "agent_hostname": "EC2AMAZ-IQFSLIL",
                "agent_content_version": "380-82571",
                "agent_session_start_time": 1644385496543,
                "agent_id": "37a92aad549d41d184ec9fbdafbff55c",
                "agent_os_sub_type": "Windows Server 2016 [10.0 (Build 17763)]",
                "event_id": "AAABfvB4P2Qqn9UKABvBDw==",
                "event_timestamp": 1644711919520,
                "event_version": 25,
                "actor_process_is_native": "TRUE",
                "agent_is_vdi": "FALSE",
                "agent_os_type": "AGENT_OS_WINDOWS",
                "event_type": "FILE",
                "event_sub_type": "FILE_WRITE",
                "actor_process_signature_status": "SIGNED"
            }
        },
        {
            "xdr_data": {
                "action_file_name": "MpWppTracing-20220210-055530-00000003-ffffffff.bin",
                "actor_process_image_name": "System",
                "causality_actor_process_image_name": "System",
                "os_actor_process_image_name": "System",
                "action_file_path": "C:\\ProgramData\\Microsoft\\Windows Defender\\Support\\MpWppTracing-20220210-055530-00000003-ffffffff.bin",
                "actor_process_image_path": "System",
                "causality_actor_process_image_path": "System",
                "os_actor_process_image_path": "System",
                "actor_process_os_pid": 4,
                "causality_actor_process_os_pid": 4,
                "os_actor_process_os_pid": 4,
                "actor_primary_user_sid": "S-1-5-18",
                "actor_primary_username": "NT AUTHORITY\\SYSTEM",
                "actor_process_logon_id": "1003",
                "action_file_extension": "bin",
                "action_file_type": 18,
                "manifest_file_version": 5,
                "actor_process_instance_id": "AdgdeB26mNQAAAAEAAAAAA==",
                "actor_process_causality_id": "AdgdeB26mNQAAAAEAAAAAA==",
                "actor_process_auth_id": "999",
                "actor_process_signature_vendor": "Microsoft Corporation",
                "actor_process_signature_product": "Microsoft Windows",
                "actor_process_execution_time": 1644385473948,
                "agent_version": "7.6.1.46600",
                "agent_hostname": "EC2AMAZ-IQFSLIL",
                "agent_content_version": "380-82571",
                "agent_session_start_time": 1644385496543,
                "agent_id": "37a92aad549d41d184ec9fbdafbff55c",
                "agent_os_sub_type": "Windows Server 2016 [10.0 (Build 17763)]",
                "event_id": "AAABfvB7dS4qn9UKABvHTA==",
                "event_timestamp": 1644712129898,
                "event_version": 25,
                "actor_process_is_native": "TRUE",
                "agent_is_vdi": "FALSE",
                "agent_os_type": "AGENT_OS_WINDOWS",
                "event_type": "FILE",
                "event_sub_type": "FILE_WRITE",
                "actor_process_signature_status": "SIGNED"
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
"{\"type\":\"identity\",\"id\":\"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\",\"name\":\"paloalto\",\"identity_class\":\"events\"}"
" [ { \"xdr_data\": { \"action_file_name\": \"MpWppTracing-20220210-055530-00000003-ffffffff.bin\", \"actor_process_image_name\": \"System\", \"causality_actor_process_image_name\": \"System\", \"os_actor_process_image_name\": \"System\", \"action_file_path\": \"C:\\ProgramData\\Microsoft\\Windows Defender\\Support\\MpWppTracing-20220210-055530-00000003-ffffffff.bin\", \"actor_process_image_path\": \"System\", \"causality_actor_process_image_path\": \"System\", \"os_actor_process_image_path\": \"System\", \"actor_process_os_pid\": 4, \"causality_actor_process_os_pid\": 4, \"os_actor_process_os_pid\": 4, \"actor_primary_user_sid\": \"S-1-5-18\", \"actor_primary_username\": \"NT AUTHORITY\\SYSTEM\", \"actor_process_logon_id\": \"1003\", \"action_file_extension\": \"bin\", \"action_file_type\": 18, \"manifest_file_version\": 5, \"actor_process_instance_id\": \"AdgdeB26mNQAAAAEAAAAAA==\", \"actor_process_causality_id\": \"AdgdeB26mNQAAAAEAAAAAA==\", \"actor_process_auth_id\": \"999\", \"actor_process_signature_vendor\": \"Microsoft Corporation\", \"actor_process_signature_product\": \"Microsoft Windows\", \"actor_process_execution_time\": 1644385473948, \"agent_version\": \"7.6.1.46600\", \"agent_hostname\": \"EC2AMAZ-IQFSLIL\", \"agent_content_version\": \"380-82571\", \"agent_session_start_time\": 1644385496543, \"agent_id\": \"37a92aad549d41d184ec9fbdafbff55c\", \"agent_os_sub_type\": \"Windows Server 2016 [10.0 (Build 17763)]\", \"event_id\": \"AAABfvB4P2Qqn9UKABvBDw==\", \"event_timestamp\": 1644711919520, \"event_version\": 25, \"actor_process_is_native\": \"TRUE\", \"agent_is_vdi\": \"FALSE\", \"agent_os_type\": \"AGENT_OS_WINDOWS\", \"event_type\": \"FILE\", \"event_sub_type\": \"FILE_WRITE\", \"actor_process_signature_status\": \"SIGNED\" } }, { \"xdr_data\": { \"action_file_name\": \"MpWppTracing-20220210-055530-00000003-ffffffff.bin\", \"actor_process_image_name\": \"System\", \"causality_actor_process_image_name\": \"System\", \"os_actor_process_image_name\": \"System\", \"action_file_path\": \"C:\\ProgramData\\Microsoft\\Windows Defender\\Support\\MpWppTracing-20220210-055530-00000003-ffffffff.bin\", \"actor_process_image_path\": \"System\", \"causality_actor_process_image_path\": \"System\", \"os_actor_process_image_path\": \"System\", \"actor_process_os_pid\": 4, \"causality_actor_process_os_pid\": 4, \"os_actor_process_os_pid\": 4, \"actor_primary_user_sid\": \"S-1-5-18\", \"actor_primary_username\": \"NT AUTHORITY\\SYSTEM\", \"actor_process_logon_id\": \"1003\", \"action_file_extension\": \"bin\", \"action_file_type\": 18, \"manifest_file_version\": 5, \"actor_process_instance_id\": \"AdgdeB26mNQAAAAEAAAAAA==\", \"actor_process_causality_id\": \"AdgdeB26mNQAAAAEAAAAAA==\", \"actor_process_auth_id\": \"999\", \"actor_process_signature_vendor\": \"Microsoft Corporation\", \"actor_process_signature_product\": \"Microsoft Windows\", \"actor_process_execution_time\": 1644385473948, \"agent_version\": \"7.6.1.46600\", \"agent_hostname\": \"EC2AMAZ-IQFSLIL\", \"agent_content_version\": \"380-82571\", \"agent_session_start_time\": 1644385496543, \"agent_id\": \"37a92aad549d41d184ec9fbdafbff55c\", \"agent_os_sub_type\": \"Windows Server 2016 [10.0 (Build 17763)]\", \"event_id\": \"AAABfvB7dS4qn9UKABvHTA==\", \"event_timestamp\": 1644712129898, \"event_version\": 25, \"actor_process_is_native\": \"TRUE\", \"agent_is_vdi\": \"FALSE\", \"agent_os_type\": \"AGENT_OS_WINDOWS\", \"event_type\": \"FILE\", \"event_sub_type\": \"FILE_WRITE\", \"actor_process_signature_status\": \"SIGNED\" } } ] "
"{\"stix_validator\": true}"
```

#### STIX Translate results - output
```json
{
    "type": "bundle",
    "id": "bundle--a1d2533a-11e1-4ee8-9c96-4c298f87a823",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "paloalto",
            "identity_class": "events"
        },
        {
            "id": "observed-data--734f2fdb-7777-4a8f-8fb1-c08dceec94fa",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-03-09T08:56:29.407Z",
            "modified": "2022-03-09T08:56:29.407Z",
            "objects": {
                "0": {
                    "type": "file",
                    "name": "MpWppTracing-20220210-055530-00000003-ffffffff.bin",
                    "parent_directory_ref": "9",
                    "extensions": {
                        "x-paloalto-file": {
                            "extension": "bin",
                            "type": 18,
                            "manifest_version": 5
                        }
                    }
                },
                "1": {
                    "type": "file",
                    "name": "System"
                },
                "2": {
                    "type": "process",
                    "name": "System",
                    "binary_ref": "1",
                    "pid": 4,
                    "extensions": {
                        "x-paloalto-process": {
                            "instance_id": "AdgdeB26mNQAAAAEAAAAAA==",
                            "causality_id": "AdgdeB26mNQAAAAEAAAAAA==",
                            "auth_id": "999",
                            "signature_vendor": "Microsoft Corporation",
                            "signature_product": "Microsoft Windows",
                            "execution_time": "2022-02-09T05:44:33.948Z",
                            "is_native": true,
                            "signature_status": "SIGNED"
                        }
                    }
                },
                "3": {
                    "type": "file",
                    "name": "System"
                },
                "4": {
                    "type": "process",
                    "name": "System"
                },
                "5": {
                    "type": "process",
                    "parent_ref": "4",
                    "binary_ref": "3",
                    "pid": 4
                },
                "6": {
                    "type": "file",
                    "name": "System"
                },
                "7": {
                    "type": "process",
                    "name": "System"
                },
                "8": {
                    "type": "process",
                    "parent_ref": "7",
                    "binary_ref": "6",
                    "pid": 4
                },
                "9": {
                    "type": "directory",
                    "path": "C:\\ProgramData\\Microsoft\\Windows Defender\\Support"
                },
                "10": {
                    "type": "user-account",
                    "user_id": "S-1-5-18",
                    "display_name": "NT AUTHORITY\\SYSTEM",
                    "account_login": "1003"
                },
                "11": {
                    "type": "x-oca-asset",
                    "agent_version": "7.6.1.46600",
                    "hostname": "EC2AMAZ-IQFSLIL",
                    "content_version": "380-82571",
                    "start_time": "2022-02-09T05:44:56.543Z",
                    "asset_id": "37a92aad549d41d184ec9fbdafbff55c",
                    "os_sub_type": "Windows Server 2016 [10.0 (Build 17763)]",
                    "is_vdi": false,
                    "os_type": "AGENT_OS_WINDOWS"
                },
                "12": {
                    "type": "x-oca-event",
                    "event_id": "AAABfvB4P2Qqn9UKABvBDw==",
                    "time": "2022-02-13T00:25:19.520Z",
                    "version": 25,
                    "event_type": "FILE",
                    "sub_type": "FILE_WRITE"
                }
            },
            "first_observed": "2022-03-09T08:56:29.407Z",
            "last_observed": "2022-03-09T08:56:29.407Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--65f9e698-ecd2-41f9-b370-cf9dae876eeb",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-03-09T08:56:29.746Z",
            "modified": "2022-03-09T08:56:29.746Z",
            "objects": {
                "0": {
                    "type": "file",
                    "name": "MpWppTracing-20220210-055530-00000003-ffffffff.bin",
                    "parent_directory_ref": "9",
                    "extensions": {
                        "x-paloalto-file": {
                            "extension": "bin",
                            "type": 18,
                            "manifest_version": 5
                        }
                    }
                },
                "1": {
                    "type": "file",
                    "name": "System"
                },
                "2": {
                    "type": "process",
                    "name": "System",
                    "binary_ref": "1",
                    "pid": 4,
                    "extensions": {
                        "x-paloalto-process": {
                            "instance_id": "AdgdeB26mNQAAAAEAAAAAA==",
                            "causality_id": "AdgdeB26mNQAAAAEAAAAAA==",
                            "auth_id": "999",
                            "signature_vendor": "Microsoft Corporation",
                            "signature_product": "Microsoft Windows",
                            "execution_time": "2022-02-09T05:44:33.948Z",
                            "is_native": true,
                            "signature_status": "SIGNED"
                        }
                    }
                },
                "3": {
                    "type": "file",
                    "name": "System"
                },
                "4": {
                    "type": "process",
                    "name": "System"
                },
                "5": {
                    "type": "process",
                    "parent_ref": "4",
                    "binary_ref": "3",
                    "pid": 4
                },
                "6": {
                    "type": "file",
                    "name": "System"
                },
                "7": {
                    "type": "process",
                    "name": "System"
                },
                "8": {
                    "type": "process",
                    "parent_ref": "7",
                    "binary_ref": "6",
                    "pid": 4
                },
                "9": {
                    "type": "directory",
                    "path": "C:\\ProgramData\\Microsoft\\Windows Defender\\Support"
                },
                "10": {
                    "type": "user-account",
                    "user_id": "S-1-5-18",
                    "display_name": "NT AUTHORITY\\SYSTEM",
                    "account_login": "1003"
                },
                "11": {
                    "type": "x-oca-asset",
                    "agent_version": "7.6.1.46600",
                    "hostname": "EC2AMAZ-IQFSLIL",
                    "content_version": "380-82571",
                    "start_time": "2022-02-09T05:44:56.543Z",
                    "asset_id": "37a92aad549d41d184ec9fbdafbff55c",
                    "os_sub_type": "Windows Server 2016 [10.0 (Build 17763)]",
                    "is_vdi": false,
                    "os_type": "AGENT_OS_WINDOWS"
                },
                "12": {
                    "type": "x-oca-event",
                    "event_id": "AAABfvB7dS4qn9UKABvHTA==",
                    "time": "2022-02-13T00:28:49.898Z",
                    "version": 25,
                    "event_type": "FILE",
                    "sub_type": "FILE_WRITE"
                }
            },
            "first_observed": "2022-03-09T08:56:29.746Z",
            "last_observed": "2022-03-09T08:56:29.746Z",
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
"{\"type\":\"identity\",\"id\":\"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\",\"name\":\"paloalto\",\"identity_class \":\"events\"}"
"{\"host\":\"xx.xx.xx\"}"
"{\"auth\":{\"api_key\": \"xxxx\", \"api_key_id\": \"xx\",\"tenant\":\"xxxx\"}}"
"[file:name = 'chrome.exe' ] START t'2022-01-16T11:00:00.000Z' STOP t'2022-01-20T11:00:00.003Z'"
```
#### STIX Execute query - output
```json
{
    "type": "bundle",
    "id": "bundle--899d573b-3fcb-4561-bedd-6038fd4da192",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "paloalto",
            "identity_class ": "events"
        },
        {
            "id": "observed-data--59220f58-f8ee-4d2b-a2df-367958e132b7",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-03-09T09:04:32.272Z",
            "modified": "2022-03-09T09:04:32.272Z",
            "objects": {
                "0": {
                    "type": "file",
                    "name": "LICENSE",
                    "parent_directory_ref": "9",
                    "extensions": {
                        "x-paloalto-file": {
                            "type": 18,
                            "manifest_version": 5
                        }
                    }
                },
                "1": {
                    "type": "file",
                    "name": "chrome.exe",
                    "accessed": "2021-12-15T22:05:27.664Z",
                    "modified": "2021-12-12T08:19:30.068Z",
                    "parent_directory_ref": "10"
                },
                "2": {
                    "type": "process",
                    "name": "chrome.exe",
                    "binary_ref": "1",
                    "command_line": "\"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\" --flag-switches-begin --flag-switches-end --origin-trial-disabled-features=CaptureHandle",
                    "created": "2021-11-10T06:59:32.948Z",
                    "pid": 4572,
                    "extensions": {
                        "x-paloalto-process": {
                            "instance_id": "AdgAs0qzIE0AABHcAAAAAA==",
                            "causality_id": "AdgAs0qzIE0AABHcAAAAAA==",
                            "auth_id": "999",
                            "signature_vendor": "Google LLC",
                            "signature_product": "Google LLC",
                            "extension": "exe",
                            "execution_time": "2022-01-03T15:05:05.983Z",
                            "is_native": true,
                            "signature_status": "SIGNED"
                        }
                    }
                },
                "3": {
                    "type": "file",
                    "name": "chrome.exe",
                    "parent_directory_ref": "11"
                },
                "4": {
                    "type": "process",
                    "name": "chrome.exe"
                },
                "5": {
                    "type": "process",
                    "parent_ref": "4",
                    "binary_ref": "3",
                    "command_line": "\"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\" --flag-switches-begin --flag-switches-end --origin-trial-disabled-features=CaptureHandle",
                    "created": "2021-11-10T06:59:32.948Z",
                    "pid": 4572
                },
                "6": {
                    "type": "file",
                    "name": "chrome.exe",
                    "accessed": "2021-12-15T22:05:27.664Z",
                    "modified": "2021-12-12T08:19:30.068Z",
                    "parent_directory_ref": "12"
                },
                "7": {
                    "type": "process",
                    "name": "chrome.exe"
                },
                "8": {
                    "type": "process",
                    "parent_ref": "7",
                    "binary_ref": "6",
                    "command_line": "\"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\" --flag-switches-begin --flag-switches-end --origin-trial-disabled-features=CaptureHandle",
                    "created": "2021-11-10T06:59:32.948Z",
                    "pid": 4572
                },
                "9": {
                    "type": "directory",
                    "path": "C:\\Users\\Administrator\\AppData\\Local\\Temp\\2\\4572_137263248"
                },
                "10": {
                    "type": "directory",
                    "path": "C:\\Program Files\\Google\\Chrome\\Application"
                },
                "11": {
                    "type": "directory",
                    "path": "C:\\Program Files\\Google\\Chrome\\Application"
                },
                "12": {
                    "type": "directory",
                    "path": "C:\\Program Files\\Google\\Chrome\\Application"
                },
                "13": {
                    "type": "user-account",
                    "user_id": "S-1-5-21-3039464837-300237904-2407637926-500",
                    "display_name": "EC2AMAZ-65BN1IK\\Administrator",
                    "account_login": "1003"
                },
                "14": {
                    "type": "x-oca-asset",
                    "agent_version": "7.6.1.46600",
                    "hostname": "EC2AMAZ-65BN1IK",
                    "content_version": "350-80787",
                    "start_time": "2022-01-19T10:02:28.366Z",
                    "asset_id": "f344796340f84d0ca7e0fdaedbcbd594",
                    "os_sub_type": "Windows Server 2016 [10.0 (Build 14393)]",
                    "is_vdi": false,
                    "os_type": "AGENT_OS_WINDOWS"
                },
                "15": {
                    "type": "x-oca-event",
                    "event_id": "AAABfnQpgUfunpI7AANI6Q==",
                    "time": "2022-01-19T21:06:24.409Z",
                    "version": 25,
                    "event_type": "FILE",
                    "sub_type": "FILE_WRITE"
                }
            },
            "x_actor_process_last_observed": "2021-12-15T22:05:27.664Z",
            "x_os_actor_process_last_observed": "2021-12-15T22:05:27.664Z",
            "x_process_actor_first_observed": "2021-11-10T06:59:32.948Z",
            "x_process_causality_actor_first_observed": "2021-11-10T06:59:32.948Z",
            "x_process_os_actor_first_observed": "2021-11-10T06:59:32.948Z",
            "first_observed": "2022-03-09T09:04:32.272Z",
            "last_observed": "2022-03-09T09:04:32.272Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--1bd94f55-3b0d-4057-b281-f8c17cdc6cfa",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-03-09T09:04:32.272Z",
            "modified": "2022-03-09T09:04:32.272Z",
            "objects": {
                "0": {
                    "type": "file",
                    "name": "22c34728-a90d-4fe4-8774-21563d2be0f3.tmp",
                    "size": 117576,
                    "parent_directory_ref": "9",
                    "extensions": {
                        "x-paloalto-file": {
                            "extension": "tmp",
                            "writer": "AdgAs0qzIE0AABHcAAAAAA==",
                            "type": 0,
                            "manifest_version": 5
                        }
                    }
                },
                "1": {
                    "type": "file",
                    "name": "chrome.exe",
                    "accessed": "2021-12-15T22:05:27.664Z",
                    "modified": "2021-12-12T08:19:30.068Z",
                    "parent_directory_ref": "10"
                },
                "2": {
                    "type": "process",
                    "name": "chrome.exe",
                    "binary_ref": "1",
                    "command_line": "\"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\" --flag-switches-begin --flag-switches-end --origin-trial-disabled-features=CaptureHandle",
                    "created": "2021-11-10T06:59:32.948Z",
                    "pid": 4572,
                    "extensions": {
                        "x-paloalto-process": {
                            "instance_id": "AdgAs0qzIE0AABHcAAAAAA==",
                            "causality_id": "AdgAs0qzIE0AABHcAAAAAA==",
                            "auth_id": "999",
                            "signature_vendor": "Google LLC",
                            "signature_product": "Google LLC",
                            "extension": "exe",
                            "execution_time": "2022-01-03T15:05:05.983Z",
                            "is_native": true,
                            "signature_status": "SIGNED"
                        }
                    }
                },
                "3": {
                    "type": "file",
                    "name": "chrome.exe",
                    "parent_directory_ref": "11"
                },
                "4": {
                    "type": "process",
                    "name": "chrome.exe"
                },
                "5": {
                    "type": "process",
                    "parent_ref": "4",
                    "binary_ref": "3",
                    "command_line": "\"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\" --flag-switches-begin --flag-switches-end --origin-trial-disabled-features=CaptureHandle",
                    "created": "2021-11-10T06:59:32.948Z",
                    "pid": 4572
                },
                "6": {
                    "type": "file",
                    "name": "chrome.exe",
                    "accessed": "2021-12-15T22:05:27.664Z",
                    "modified": "2021-12-12T08:19:30.068Z",
                    "parent_directory_ref": "12"
                },
                "7": {
                    "type": "process",
                    "name": "chrome.exe"
                },
                "8": {
                    "type": "process",
                    "parent_ref": "7",
                    "binary_ref": "6",
                    "command_line": "\"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\" --flag-switches-begin --flag-switches-end --origin-trial-disabled-features=CaptureHandle",
                    "created": "2021-11-10T06:59:32.948Z",
                    "pid": 4572
                },
                "9": {
                    "type": "directory",
                    "path": "C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data"
                },
                "10": {
                    "type": "directory",
                    "path": "C:\\Program Files\\Google\\Chrome\\Application"
                },
                "11": {
                    "type": "directory",
                    "path": "C:\\Program Files\\Google\\Chrome\\Application"
                },
                "12": {
                    "type": "directory",
                    "path": "C:\\Program Files\\Google\\Chrome\\Application"
                },
                "13": {
                    "type": "user-account",
                    "user_id": "S-1-5-21-3039464837-300237904-2407637926-500",
                    "display_name": "EC2AMAZ-65BN1IK\\Administrator",
                    "account_login": "1003"
                },
                "14": {
                    "type": "x-oca-asset",
                    "agent_version": "7.6.1.46600",
                    "hostname": "EC2AMAZ-65BN1IK",
                    "content_version": "350-80787",
                    "start_time": "2022-01-19T10:02:28.366Z",
                    "asset_id": "f344796340f84d0ca7e0fdaedbcbd594",
                    "os_sub_type": "Windows Server 2016 [10.0 (Build 14393)]",
                    "is_vdi": false,
                    "os_type": "AGENT_OS_WINDOWS"
                },
                "15": {
                    "type": "x-oca-event",
                    "event_id": "AAABfnRfbAPunpI7AANyKA==",
                    "time": "2022-01-19T22:05:17.974Z",
                    "version": 25,
                    "event_type": "FILE",
                    "sub_type": "FILE_WRITE"
                }
            },
            "x_actor_process_last_observed": "2021-12-15T22:05:27.664Z",
            "x_os_actor_process_last_observed": "2021-12-15T22:05:27.664Z",
            "x_process_actor_first_observed": "2021-11-10T06:59:32.948Z",
            "x_process_causality_actor_first_observed": "2021-11-10T06:59:32.948Z",
            "x_process_os_actor_first_observed": "2021-11-10T06:59:32.948Z",
            "first_observed": "2022-03-09T09:04:32.272Z",
            "last_observed": "2022-03-09T09:04:32.272Z",
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
- The quota limit range for the API call would be from 1 to 4 units for the Standard license, and it will be from 6 to 12  
  if additional units are purchased.

### References
- [Cortex XDR](https://docs.paloaltonetworks.com/cortex/cortex-xdr.html)
- [Get Started with XQL](https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-xql-language-reference/get-started-with-xql.html)
- [Cortex XDR™ XQL Schema Reference](https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-xql-schema-reference.html)
- [Cortex XDR API Overview](https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-api/cortex-xdr-api-overview.html)
