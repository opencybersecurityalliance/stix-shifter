#  Elastic ECS

Elastic ECS Connector can be used to search events such as logs and metrics stored Elasticsearch. The connector can search Elastic Common Schema (ECS) formatted events.

## Supported STIX Mappings

See the [table of mappings](elastic_ecs_supported_stix.md) for the STIX objects and operators supported by this connector.

## Supported version

The connector supports Elasticsearch version 8.6

## API and Query Language

Connector uses Elasticsearch [search REST API](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html) to fetch events stored in Elasticsearch indices. API Endpoint: `GET /<indices>/_search`

For search, the connector uses Elasticsearch [Query DSL](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html) (Domain Specific Language). The query syntax is based on JSON.

## Dialects

The connector supports two dialects. 

### Elastic Common Schema (ECS)

The default dialects contains [Elastic Common Schema](https://www.elastic.co/guide/en/ecs/8.6/ecs-reference.html). All the available ECS fields can be searched using the default dialect. The default dialect mapping is specified in [from_stix_map.json](https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/stix_shifter_modules/elastic_ecs/stix_translation/json/from_stix_map.json)

### Beats

Beats dialect can be used if any [beats](https://www.elastic.co/guide/en/beats/libbeat/current/beats-reference.html) agents is installed in Elasticsearch datasource. The mapping of this dialect can be found in [beats_from_stix_map.json](https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/stix_shifter_modules/elastic_ecs/stix_translation/json/beats_from_stix_map.json)


### Format for making STIX translation calls via the CLI

`python main.py <translator_module> <query or result> <STIX identity object> <data>`

Note the identity object is only used when converting from Elasticsearch JSON response to STIX, but due to positional arguments, an empty hash will need to be passed in when converting from STIX patterns to datasource query.


## Converting from STIX patterns to DSL queries

This example input stix pattern for default dialect:

`python main.py translate elastic_ecs query {} "[ipv4-addr:value = '192.168.1.2' OR network-traffic:src_port = 443] START t'2022-04-06T00:00:00.000Z' STOP t'2022-04-06T00:05:00.000Z'"`

Returns the following DSL query string:

`((source.port : \"443\" OR client.port : \"443\") OR (source.ip : \"192.168.1.2\" OR destination.ip : \"192.168.1.2\" OR client.ip : \"192.168.1.2\" OR server.ip : \"192.168.1.2\" OR host.ip : \"192.168.1.2\" OR dns.resolved_ip : \"192.168.1.2\")) AND (@timestamp:[\"2022-04-06T00:00:00.000Z\" TO \"2022-04-06T00:05:00.000Z\"])`

This example input stix pattern for beats dialect:

`python main.py translate elastic_ecs:beats query {} "[ipv4-addr:value = '192.168.1.2' OR network-traffic:src_port = 443] START t'2022-04-06T00:00:00.000Z' STOP t'2022-04-06T00:05:00.000Z'"`

Returns the following DSL query string:

`((source.port : \"443\" OR client.port : \"443\") OR (source.ip.keyword : \"192.168.1.2\" OR destination.ip.keyword : \"192.168.1.2\" OR client.ip : \"192.168.1.2\" OR server.ip : \"192.168.1.2\" OR host.ip.keyword : \"192.168.1.2\" OR dns.resolved_ip : \"192.168.1.2\")) AND (@timestamp:[\"2022-04-06T00:00:00.000Z\" TO \"2022-04-06T00:05:00.000Z\"])`

## Sending Query to Search API

This is a synchronous connector. Therefore, the connector can only uses results transmission call to send query to the API. Example results call:

```
python main.py transmit elastic_ecs '{"host":"<elasticsearch host>", "port": <port number>, "selfSignedCert": "<certificate>", "indices": "index1, index2"}' '{"auth":{"username":"<user>","password":"<pass>"}}' results '((source.port : "443" OR client.port : "443") OR (source.ip : "192.168.1.2" OR destination.ip : "192.168.1.2" OR client.ip : "192.168.1.2" OR server.ip : "192.168.1.2" OR host.ip : "192.168.1.2" OR dns.resolved_ip : "192.168.1.2")) AND (@timestamp:["2022-04-06T00:00:00.000Z" TO "2022-04-06T00:05:00.000Z"])' 0 1
```

**Note** 
   1. "indices" parameter is optional. If it is not specified all the indices will be queried. Multiple indices can be set for the search. 
   2. If the connector supports key and token based authentication then specify them inside "auth" object.

### Transmit Results Output

```
{
    "success": true,
    "data": [
        {
            "process": {
                "args": "-D -e -f /etc/ssh/sshd_config -R",
                "parent": {
                    "args": "-D -e -f /etc/ssh/sshd_config",
                    "name": "sshd",
                    "start": "2021-10-16T01:54:25.664830275Z",
                    "pid": 820693,
                    "command_line": "/path/sbin/sshd -D",
                    "executable": "/path/sbin/sshd"
                },
                "name": "sshd",
                "start": "2021-10-17T14:33:05.446908698Z",
                "pid": 899531,
                "thread": {
                    "id": 899531
                },
                "command_line": "/path/sbin/sshd -D",
                "executable": "/path/sbin/sshd"
            },
            "@timestamp": "2021-10-17T14:33:05.452045076Z",
            "destination": {
                "address": "0.0.0.0",
                "port": 655,
                "bytes": 0,
                "ip": "0.0.0.0",
                "packets": 0
            },
            "source": {
                "address": "127.0.0.1",
                "port": 422,
                "bytes": 0,
                "ip": "127.0.0.1",
                "packets": 0
            },
            "event": {
                "duration": 5354,
                "kind": "event",
                "start": "2021-10-17T14:33:05.452045076Z",
                "action": "network-connection-traffic",
                "end": "2021-10-17T14:33:05.45205043Z",
                "sf_type": "NF",
                "category": "network",
                "type": "connection"
            },
            "user": {
                "name": "root",
                "id": 0,
                "group": {
                    "name": "root",
                    "id": 0
                }
            },
            "network": {
                "community_id": "1233242",
                "protocol": "udp",
                "bytes": 0,
                "iana_number": "17"
            }
        }
    ],
    "metadata": [
        1634481185452
    ]
}
```

***Note** "metadata" parameter is returned for pagination. The value of the metadata is used to fetch next batch of results.

##  Elasticsearch response results to STIX objects

### Translate command
``` 
python main.py translate elastic_ecs results '{"type":"identity","id":"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff","name":"elastic_ecs","identity_class":"events", "created": "2022-04-07T20:35:41.042Z", "modified": "2022-04-07T20:35:41.042Z"}' '[<Elasticsearch JSON response>]'
```
### STIX 2.0 Output

```
{
    "type": "bundle",
    "id": "bundle--d0c6c6ce-69a2-45bb-82f3-a5e96a9af95e",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "elastic",
            "identity_class": "events"
        },
        {
            "id": "observed-data--a0b6e2fa-1f8b-47de-9777-383646ad304e",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2023-03-23T18:47:27.536Z",
            "modified": "2023-03-23T18:47:27.536Z",
            "objects": {
                "0": {
                    "type": "process",
                    "name": "sshd",
                    "created": "2021-10-16T01:54:25.664830275Z",
                    "pid": 820693,
                    "command_line": "/usr/sbin/sshd -D",
                    "binary_ref": "3"
                },
                "1": {
                    "type": "process",
                    "parent_ref": "0",
                    "name": "sshd",
                    "created": "2021-10-17T14:33:05.446908698Z",
                    "pid": 899531,
                    "x_thread_id": 899531,
                    "command_line": "/path/sbin/sshd -D -e",
                    "binary_ref": "5",
                    "creator_user_ref": "12",
                    "opened_connection_refs": [
                        "8"
                    ]
                },
                "2": {
                    "type": "x-oca-event",
                    "parent_process_ref": "0",
                    "process_ref": "1",
                    "duration": 5354,
                    "kind": "event",
                    "start": "2021-10-17T14:33:05.452045076Z",
                    "action": "network-connection-traffic",
                    "end": "2021-10-17T14:33:05.45205043Z",
                    "category": "network",
                    "event_type": "connection",
                    "user_ref": "12",
                    "network_ref": "8"
                },
                "3": {
                    "type": "file",
                    "name": "sshd",
                    "parent_directory_ref": "4"
                },
                "4": {
                    "type": "directory",
                    "path": "/path/sbin"
                },
                "5": {
                    "type": "file",
                    "name": "sshd",
                    "parent_directory_ref": "6",
                    "x_owner_ref": "12"
                },
                "6": {
                    "type": "directory",
                    "path": "/path/sbin"
                },
                "7": {
                    "type": "x-ecs-destination",
                    "address": "0.0.0.0"
                },
                "8": {
                    "type": "network-traffic",
                    "dst_port": 655,
                    "dst_byte_count": 0,
                    "dst_ref": "9",
                    "dst_packets": 0,
                    "src_port": 42001,
                    "src_byte_count": 0,
                    "src_ref": "11",
                    "src_packets": 0,
                    "x_community_id": "123456",
                    "protocols": [
                        "udp"
                    ]
                },
                "9": {
                    "type": "ipv4-addr",
                    "value": "0.0.0.0"
                },
                "10": {
                    "type": "x-ecs-source",
                    "address": "127.0.0.1"
                },
                "11": {
                    "type": "ipv4-addr",
                    "value": "127.0.0.1"
                },
                "12": {
                    "type": "user-account",
                    "user_id": "root",
                    "account_login": "root",
                    "x_group": {
                        "name": "root",
                        "id": 0
                    }
                }
            },
            "first_observed": "2021-10-17T14:33:05.452045076Z",
            "last_observed": "2021-10-17T14:33:05.452045076Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```
