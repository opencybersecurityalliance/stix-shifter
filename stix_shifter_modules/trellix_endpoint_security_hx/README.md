# Trellix Endpoint Security HX

## Supported STIX Mappings

See the [table of mappings](trellix_endpoint_security_hx_supported_stix.md) for the STIX objects and operators supported by this connector.

**Table of Contents**
- [Trellix Endpoint Security HX API Endpoints](#trellix-endpoint-security-hx-api-endpoints)
- [Curl Command to test the API Endpoints](#curl-command-to-test-api-endpoints)
- [Format of calling Stix shifter from Command Line](#format-for-calling-stix-shifter-from-the-command-line)
- [Pattern expression with STIX attributes and CUSTOM attributes - Single Observation](#single-observation)
- [Pattern expression with STIX and CUSTOM attributes - Multiple Observation](#multiple-observation)
- [STIX Execute Query](#stix-execute-query)
- [Usage of Host Sets in Command Line](#usage-of-host-sets-in-command-line)
- [Recommendations](#recommendations)
- [Limitations](#limitations)
- [References](#references)

### Trellix Endpoint Security HX API Endpoints

   | Connector Method | Trellix Endpoint Security HX API Endpoint                | Method |
   |------------------|----------------------------------------------------------|--------|
   | Ping Endpoint    | Agents System Information API - hx/api/v3/agents/sysinfo | GET    |
   | Query Endpoint   | Enterprise Search API - hx/api/v3/searches               | POST   |
   | Status Endpoint  | Enterprise Search API details - hx/api/v3/searches/{id}  | GET    |
   | Results Endpoint | Search Results API - hx/api/v3/searches/{id}/results     | GET    |
   | Delete Endpoint  | Delete Search API - hx/api/v3/searches/{id}              | DELETE |


### CURL command to test API Endpoints
#### Ping 
```
curl --location --request GET 'https://{host}:{port}/hx/api/v3/agents/sysinfo' \
--cacert {PEM file} \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic {base 64 encoded token of user name and password}'
```
#### Query
```
curl --location --request POST 'https://{host}:{port}/hx/api/v3/searches' \
--cacert {PEM file} \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic {base 64 encoded token of user name and password}' \
--data '{
    "host_set": {
    "_id": 1002
    },
    "query": [
        {
     "field": "Local IP Address",
     "operator": "not equals",
     "value": "1.1.1.1"
      }
    ]
}'
```

#### Results
```
curl --location --request GET 'https://{host}:{port}/hx/api/v3/searches/{search id}/results' \
--cacert {PEM file} \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic {base 64 encoded token of user name and password}'
```

### Format for calling stix-shifter from the command line
```
python main.py `<translator_module>` `<query or result>` `<STIX identity object>` `<data>`

```

### Pattern expression with STIX and CUSTOM attributes

#### Single Observation

#### STIX Translate query using OR operator
```shell
translate trellix_endpoint_security_hx query "{}" "[domain-name:value LIKE 'download' OR ipv4-addr:value ='1.1.1.1'] START t'2024-05-01T00:00:00.000Z' STOP t'2024-05-29T00:00:00.000Z'"
"{\"host_sets\": \"host_set1,host_set2\"}"
```
#### STIX Translate query - Output
```json
{
    "queries": [
        {
            "host_set": {
                "_id": "host_set1"
            },
            "query": [
                {
                    "field": "Local IP Address",
                    "value": "1.1.1.1",
                    "operator": "equals"
                },
                {
                    "field": "Timestamp - Event",
                    "operator": "between",
                    "value": [
                        "2024-05-01T00:00:00.000Z",
                        "2024-05-29T00:00:00.000Z"
                    ]
                }
            ]
        },
        {
            "host_set": {
                "_id": "host_set2"
            },
            "query": [
                {
                    "field": "Local IP Address",
                    "value": "1.1.1.1",
                    "operator": "equals"
                },
                {
                    "field": "Timestamp - Event",
                    "operator": "between",
                    "value": [
                        "2024-05-01T00:00:00.000Z",
                        "2024-05-29T00:00:00.000Z"
                    ]
                }
            ]
        },
        {
            "host_set": {
                "_id": "host_set1"
            },
            "query": [
                {
                    "field": "DNS Hostname",
                    "value": "download",
                    "operator": "contains"
                },
                {
                    "field": "Timestamp - Event",
                    "operator": "between",
                    "value": [
                        "2024-05-01T00:00:00.000Z",
                        "2024-05-29T00:00:00.000Z"
                    ]
                }
            ]
        },
        {
            "host_set": {
                "_id": "host_set2"
            },
            "query": [
                {
                    "field": "DNS Hostname",
                    "value": "download",
                    "operator": "contains"
                },
                {
                    "field": "Timestamp - Event",
                    "operator": "between",
                    "value": [
                        "2024-05-01T00:00:00.000Z",
                        "2024-05-29T00:00:00.000Z"
                    ]
                }
            ]
        },
        {
            "host_set": {
                "_id": "host_set1"
            },
            "query": [
                {
                    "field": "Remote IP Address",
                    "value": "1.1.1.1",
                    "operator": "equals"
                },
                {
                    "field": "Timestamp - Event",
                    "operator": "between",
                    "value": [
                        "2024-05-01T00:00:00.000Z",
                        "2024-05-29T00:00:00.000Z"
                    ]
                }
            ]
        },
        {
            "host_set": {
                "_id": "host_set2"
            },
            "query": [
                {
                    "field": "Remote IP Address",
                    "value": "1.1.1.1",
                    "operator": "equals"
                },
                {
                    "field": "Timestamp - Event",
                    "operator": "between",
                    "value": [
                        "2024-05-01T00:00:00.000Z",
                        "2024-05-29T00:00:00.000Z"
                    ]
                }
            ]
        }
    ]
}
```
#### STIX Transmit Query
```shell
transmit
trellix_endpoint_security_hx
"{\"host\":\"1.2.3.4\",\"port\":123,\"selfSignedCert\":\"cert\",\"options\":{\"host_sets\":\"host_set1,host_set2\"}}"
"{\"auth\":{\"username\":\"xxx\",\"password\":  \"yyyy\"}}"
query
"{ \"host_set\": { \"_id\": \"host_set1\" }, \"query\": [ { \"field\": \"DNS Hostname\", \"value\": \"download\", 
\"operator\": \"contains\" }, { \"field\": \"Timestamp - Event\", \"operator\": \"between\", \"value\": 
[ \"2024-05-01T00:00:00.000Z\", \"2024-05-29T00:00:00.000Z\" ] } ] }
```
#### STIX Transmit Query - Output

```json
{
    "success": true,
    "search_id": "2493:host_set1"
}
```
#### STIX Transmit Status
```shell
transmit
trellix_endpoint_security_hx
"{\"host\":\"1.2.3.4\",\"port\":123,\"selfSignedCert\":\"cert\",\"options\":{\"host_sets\":\"host_set1,host_set2\"}}"
"{\"auth\":{\"username\":\"xxx\",\"password\":  \"yyyy\"}}"
status  "2493:host_set1"
```

#### STIX Transmit Status - Output
```json
{
    "success": true,
    "status": "COMPLETED",
    "progress": 100
}
```
#### STIX Transmit Results
```shell
transmit
trellix_endpoint_security_hx
"{\"host\":\"1.2.3.4\",\"port\":123,\"selfSignedCert\":\"cert\",\"options\":{\"host_sets\":\"host_set1,host_set2\"}}"
"{\"auth\":{\"username\":\"xxx\",\"password\":  \"yyyy\"}}"
results  "2493:host_set1" 0 1
```

#### STIX Transmit Results - Output
```json
{
    "success": true,
    "data": [
        {
            "Process Name": "svchost.exe",
            "Process ID": "7996",
            "Username": "NT AUTHORITY\\SYSTEM",
            "Remote IP Address": "2.2.2.2",
            "IP Address": "2.2.2.2",
            "Port": "80",
            "Local Port": "49985",
            "Remote Port": "80",
            "DNS Hostname": "download.windowsupdate.com",
            "URL": "/c/msdownload.cab",
            "HTTP Header": {
                "User-Agent": "Windows-Update-Agent/10.0.10011.16384 Client-Protocol/2.0",
                "Host": "download.windowsupdate.com"
            },
            "HTTP Method": "GET",
            "Timestamp - Event": "2024-05-02T04:57:11.644Z",
            "Timestamp - Modified": "2024-05-02T04:57:11.644Z",
            "Timestamp - Accessed": "2024-05-02T04:57:11.644Z",
            "Host ID": "host1",
            "Hostname": "EC2",
            "Event Type": "URL Event",
            "Host Set": "host_set1",
            "Port Protocol": "http",
            "File Name": "svchost.exe"
        }
    ],
    "metadata": {
        "host_offset": 0,
        "host_record_index": 2
    }
}
```

#### STIX Translate results
```json
{
    "type": "bundle",
    "id": "bundle--294ab994-fbd4-46cb-bcdc-77d50747f617",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "trellix_endpoint_security_hx",
            "identity_class": "events",
            "created": "2023-05-30T00:00:50.336Z",
            "modified": "2024-05-30T00:01:50.336Z"
        },
        {
            "id": "observed-data--53bc6881-ba03-4cad-8235-2f9695e4695f",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2024-05-30T01:07:30.991Z",
            "modified": "2024-05-30T01:07:30.991Z",
            "objects": {
                "0": {
                    "type": "process",
                    "name": "svchost.exe",
                    "pid": 7996,
                    "creator_user_ref": "2",
                    "binary_ref": "7"
                },
                "1": {
                    "type": "x-oca-event",
                    "process_ref": "0",
                    "user_ref": "2",
                    "ip_refs": [
                        "3"
                    ],
                    "network_ref": "4",
                    "domain_ref": "5",
                    "created": "2024-05-02T04:57:11.644Z",
                    "modified": "2024-05-02T04:57:11.644Z",
                    "x_accessed_time": "2024-05-02T04:57:11.644Z",
                    "host_ref": "6",
                    "action": "URL Event"
                },
                "2": {
                    "type": "user-account",
                    "user_id": "NT AUTHORITY\\SYSTEM"
                },
                "3": {
                    "type": "ipv4-addr",
                    "value": "2.2.2.2"
                },
                "4": {
                    "type": "network-traffic",
                    "dst_ref": "3",
                    "src_port": 49985,
                    "dst_port": 80,
                    "extensions": {
                        "http-request-ext": {
                            "request_value": "/c/msdownload.cab",
                            "request_header": {
                                "User-Agent": "Windows-Update-Agent/10.0.10011.16384 Client-Protocol/2.0",
                                "Host": "download.windowsupdate.com"
                            },
                            "request_method": "GET"
                        }
                    },
                    "protocols": [
                        "http"
                    ]
                },
                "5": {
                    "type": "domain-name",
                    "value": "download.windowsupdate.com"
                },
                "6": {
                    "type": "x-oca-asset",
                    "device_id": "host1",
                    "hostname": "EC2",
                    "x_host_set": "host_set1"
                },
                "7": {
                    "type": "file",
                    "name": "svchost.exe"
                }
            },
            "first_observed": "2024-05-02T04:57:11.644Z",
            "last_observed": "2024-05-02T04:57:11.644Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```
#### Multiple Observation
```shell
translate trellix_endpoint_security_hx query "{}" "[x-oca-event:file_ref.name IN ('conhost.exe','Svc.log') AND user-account:user_id = 'NT AUTHORITY\\SYSTEM'] OR [network-traffic: src_port < 100 AND ipv4-addr:value != '1.1.1.1']START t'2024-05-01T00:00:00.000Z' STOP t'2024-05-29T00:00:00.000Z'" "{\"host_sets\": \"host_set1\"}"
```
#### STIX Multiple observation - Output
```json
{
    "queries": [
        {
            "host_set": {
                "_id": "host_set1"
            },
            "query": [
                {
                    "field": "Username",
                    "value": "NT AUTHORITY\\SYSTEM",
                    "operator": "equals"
                },
                {
                    "field": "Timestamp - Event",
                    "operator": "between",
                    "value": [
                        "2024-05-31T13:12:49.751Z",
                        "2024-05-31T13:17:49.751Z"
                    ]
                },
                {
                    "field": "File Name",
                    "value": "conhost.exe",
                    "operator": "equals"
                },
                {
                    "field": "File Name",
                    "value": "Svc.log",
                    "operator": "equals"
                }
            ]
        },
        {
            "host_set": {
                "_id": "host_set1"
            },
            "query": [
                {
                    "field": "Local IP Address",
                    "value": "1.1.1.1",
                    "operator": "not equals"
                },
                {
                    "field": "Timestamp - Event",
                    "operator": "between",
                    "value": [
                        "2024-05-01T00:00:00.000Z",
                        "2024-05-29T00:00:00.000Z"
                    ]
                },
                {
                    "field": "Local Port",
                    "value": 100,
                    "operator": "less than"
                }
            ]
        },
        {
            "host_set": {
                "_id": "host_set1"
            },
            "query": [
                {
                    "field": "Remote IP Address",
                    "value": "1.1.1.1",
                    "operator": "not equals"
                },
                {
                    "field": "Timestamp - Event",
                    "operator": "between",
                    "value": [
                        "2024-05-01T00:00:00.000Z",
                        "2024-05-29T00:00:00.000Z"
                    ]
                },
                {
                    "field": "Local Port",
                    "value": 100,
                    "operator": "less than"
                }
            ]
        }
    ]
}
```
#### STIX Translate query using AND operator
```shell
translate trellix_endpoint_security_hx query "{}" "[network-traffic:src_port > 30 AND domain-name:value LIKE 'dns']
START t'2024-05-01T00:00:00.000Z' STOP t'2024-05-29T00:00:00.000Z'" 
"{\"host_sets\": \"host_set1,host_set2\"}" 
```
#### STIX Translate query - Output
```json
{
    "queries": [
        {
            "host_set": {
                "_id": "host_set1"
            },
            "query": [
                {
                    "field": "DNS Hostname",
                    "value": "dns",
                    "operator": "contains"
                },
                {
                    "field": "Timestamp - Event",
                    "operator": "between",
                    "value": [
                        "2024-05-01T00:00:00.000Z",
                        "2024-05-29T00:00:00.000Z"
                    ]
                },
                {
                    "field": "Local Port",
                    "value": 30,
                    "operator": "greater than"
                }
            ]
        },
        {
            "host_set": {
                "_id": "host_set2"
            },
            "query": [
                {
                    "field": "DNS Hostname",
                    "value": "dns",
                    "operator": "contains"
                },
                {
                    "field": "Timestamp - Event",
                    "operator": "between",
                    "value": [
                        "2024-05-01T00:00:00.000Z",
                        "2024-05-29T00:00:00.000Z"
                    ]
                },
                {
                    "field": "Local Port",
                    "value": 30,
                    "operator": "greater than"
                }
            ]
        }
    ]
}
```

### STIX Execute query
```shell
execute
trellix_endpoint_security_hx
trellix_endpoint_security_hx
"{\"type\":\"identity\",\"id\":\"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\",\"name\":\"trellix_endpoint_security_hx\",\"identity_class\":\"system\",\"created\":\"2024-04-29T00:22:50.336Z\",\"modified\":\"2024-04-29T06:22:50.336Z\"}" 
"{\"host\":\"1.2.3.4\",\"port\":123,\"selfSignedCert\":\"cert\",\"options\":{\"host_sets\":\"host_set1,host_set2\"}}"
"{\"auth\":{\"username\":\"xxx\",\"password\":  \"yyyy\"}}"
"[process:name NOT MATCHES 'explorer' AND windows-registry-key:key LIKE 'HKEY_USERS\\Microsoft\\Internet Explorer\\Toolbar\\ShellBrowser\\ITBar7Layout' OR file:size > 10]START t'2024-05-01T00:00:00.000Z' STOP t'2024-05-30T00:00:00.000Z'"
```

#### STIX Execute query - Output
```json
{
    "type": "bundle",
    "id": "bundle--ebddf348-de7e-4913-80e9-9fd1021abf8e",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "trellix_endpoint_security_hx",
            "identity_class": "system",
            "created": "2024-04-29T00:22:50.336Z",
            "modified": "2024-04-29T06:22:50.336Z"
        },
	    {
            "id": "observed-data--a782a1e9-b853-44f5-916b-c159e4e00bdf",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2024-05-30T02:36:03.353Z",
            "modified": "2024-05-30T02:36:03.353Z",
            "objects": {
                "0": {
                    "type": "process",
                    "name": "explorer.exe",
                    "pid": 3816,
                    "creator_user_ref": "2",
                    "binary_ref": "5"
                },
                "1": {
                    "type": "x-oca-event",
                    "process_ref": "0",
                    "user_ref": "2",
                    "registry_ref": "3",
                    "created": "2024-05-29T15:54:50.795Z",
                    "modified": "2024-05-29T15:54:50.795Z",
                    "x_modified_time": "2024-05-29T15:54:50.795Z",
                    "host_ref": "4",
                    "action": "Registry Event"
                },
                "2": {
                    "type": "user-account",
                    "user_id": "USER1"
                },
                "3": {
                    "type": "windows-registry-key",
                    "key": "HKEY_USERS\\Microsoft\\Internet Explorer\\Toolbar\\ShellBrowser\\ITBar7Layout",
                    "values": [
                        {
                            "name": "ITBar7Layout",
                            "data_type": "REG_BINARY",
                            "data": "............ ...................^....."
                        }
                    ]
                },
                "4": {
                    "type": "x-oca-asset",
                    "device_id": "device1",
                    "hostname": "host1",
                    "x_host_set": "host_set1"
                },
                "5": {
                    "type": "file",
                    "name": "explorer.exe"
                }
            },
            "first_observed": "2024-05-29T15:54:50.795Z",
            "last_observed": "2024-05-29T15:54:50.795Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```

### Usage of host sets in Command Line

- The host set name should be passed as comma\(,\) separated values in options parameter under connections 
  while running the queries in command line.

#### STIX Translate query

translate trellix_endpoint_security_hx query "{}" "[domain-name:value LIKE 'download'] START t'2024-05-01T00:00:00.000Z' STOP t'2024-05-29T00:00:00.000Z'"
"{\"host_sets\": \"host_set1,host_set2\"}"

#### STIX Transmit Query

transmit
trellix_endpoint_security_hx
"{\"host\":\"1.2.3.4\",\"port\":123,\"selfSignedCert\":\"cert\",\"options\":{\"host_sets\":\"host_set1,host_set2\"}}"
"{\"auth\":{\"username\":\"xxx\",\"password\":  \"yyyy\"}}"
query
{input query}

#### STIX Transmit Status

transmit
trellix_endpoint_security_hx
"{\"host\":\"1.2.3.4\",\"port\":123,\"selfSignedCert\":\"cert\",\"options\":{\"host_sets\":\"host_set1,host_set2\"}}"
"{\"auth\":{\"username\":\"xxx\",\"password\":  \"yyyy\"}}"
status  {search id}

#### STIX Transmit Results

transmit
trellix_endpoint_security_hx
"{\"host\":\"1.2.3.4\",\"port\":123,\"selfSignedCert\":\"cert\",\"options\":{\"host_sets\":\"host_set1,host_set2\"}}"
"{\"auth\":{\"username\":\"xxx\",\"password\":  \"yyyy\"}}"
results  {search id} offset length

#### STIX Translate Results

translate
trellix_endpoint_security_hx
results
"{\"type\": \"identity\", \"id\": \"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\", 
\"name\": \"trellix_endpoint_security_hx\", \"identity_class\": \"events\", \"created\": \"2023-05-30T00:00:50.336Z\", 
\"modified\": \"2024-05-30T00:01:50.336Z\"}"
"{transmit result response}" "{\"host_sets\": \"host_set1,host_set2\"}"


### Recommendations

- Use multiple host sets in the input to fetch records from more than 1000 hosts.
- Progress threshold input parameter depends on the number of hosts in the host set that responds to the server. 
  The default value of this parameter in the connector is set to 50. This value can be updated based on the number 
  of hosts that responds.

### Limitations

- A maximum of 25 conditions using AND operator can be specified. Exception will be raised if more than 25 conditions 
  are specified
- Based on the concurrent search limit of the data source, the concurrent search limit of the connector should be 
  less than or equal to the data source. 
- A maximum of 15 searches only can be created in data source. In order to create more searches, the existing 
  search ids created needs to be deleted.
- As per the Trellix data source limitation, if a host set contains more than 1000 hosts, the 1000 hosts that respond
  first will be returned in the response. To avoid this scenario, configure multiple host sets in the data source 
  to fetch the records from more than 1000 hosts.
- Supported operators for IP address fields and File hash fields are =, !=, IN, NOT IN.
- Supported operators for Directory, file:parent_directory_ref.path, process:parent_ref.cwd are LIKE, MATCHES, NOT LIKE, NOT MATCHES.
- Supported operators for network traffic : extensions.'http-request-ext'.request_header fields are LIKE, MATCHES, NOT LIKE, NOT MATCHES.
- LIKE/MATCHES operator supports only substring search. Wild card character search is not supported.

### References
- [Authentication | Developer Hub](https://fireeye.dev/docs/endpoint/authentication/)
- [Search limits](https://docs.trellix.com/bundle/hx_5.3.0_ug/page/UUID-bb2cc194-22e0-4501-95d8-6a73458db012.html)
- [API Documentation](https://fireeye.dev/apis/lighthouse/)
- [Enterprise Search](https://docs.trellix.com/bundle/hx_5.3.0_ug/page/UUID-e81232c3-a871-c015-f191-9fbd431bdb59.html)