#  Elastic ECS Connector

Elastic ECS Connector can be used to search events such as logs and metrics stored Elasticsearch. The connector can search Elastic Common Schema (ECS) formatted events.

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

Beats dialect can be used if any [beats](https://www.elastic.co/guide/en/beats/libbeat/current/beats-reference.html) agents is installed Elasticsearch datasource. The mapping of this dialect can be found in [beats_from_stix_map.json](https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/stix_shifter_modules/elastic_ecs/stix_translation/json/beats_from_stix_map.json)


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
python main.py transmit elastic_ecs '{"host":"<elasticsearch host>", "port": <port number>, "selfSignedCert": "<certificate>", "indices": "<index1, index2>"}' '{"auth":{"username":"<user>","password":"<pass>"}}' results '((source.port : "443" OR client.port : "443") OR (source.ip : "192.168.1.2" OR destination.ip : "192.168.1.2" OR client.ip : "192.168.1.2" OR server.ip : "192.168.1.2" OR host.ip : "192.168.1.2" OR dns.resolved_ip : "192.168.1.2")) AND (@timestamp:["2022-04-06T00:00:00.000Z" TO "2022-04-06T00:05:00.000Z"])' 0 1
```

**Note** "indices" parameter is optional. If it is not specified all the indices will be queried. If the connector supports key and token based authentication then specify them inside "auth" object.

### Transmit Results Output
.....


##  Elasticsearch response results to STIX objects

### Translate command
``` 
python main.py translate elastic_ecs results '{"type":"identity","id":"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff","name":"elastic_ecs","identity_class":"events", "created": "2022-04-07T20:35:41.042Z", "modified": "2022-04-07T20:35:41.042Z"}' '[<Elasticsearch JSON response>]'
```
### STIX 2.0 Output

.....
