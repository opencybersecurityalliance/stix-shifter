# STIX-SHIFTER

**Table of Contents**

- [Introduction](#introduction)
  - [What is STIX?](#what-is-stix)
  - [What is STIX-SHIFTER?](#what-is-stix-shifter)
  - [What is STIX Patterning? What are STIX Observations?](#what-is-stix-patterning-what-are-stix-observations)
  - [This sounds like Sigma, I already have that](#this-sounds-like-sigma-i-already-have-that)
  - [What is a STIX-SHIFTER adapter?](#what-is-a-stix-shifter-adapter)
  - [Why would I want to use this?](#why-would-i-want-to-use-this)
- [Available Connectors](#available-connectors)
- [How to use](#How-to-use)
  - [Translation](#translation)
  - [Transmission](#transmission)
- [Glossary](#glossary)
- [Architecture Context](#architecture-context)
- [Contributing](#contributing)
- [Guide for creating new adapters](adapter-guide/develop-stix-adapter.md)
- [Licensing](#licensing)

## Introduction

### What is STIX?

Structured Threat Information eXpression (STIX™) is a language and serialization format that organizations can use to exchange cyber threat intelligence (CTI). CTI is represented with objects and descriptive relationships and stored as JSON for machine readability.

STIX delivers a consistent and machine-readable way to enable collaborative threat analysis, automated threat exchange, automated detection and response, and more.

To learn more about STIX, see the following references:

- [Introduction to STIX](https://oasis-open.github.io/cti-documentation/stix/intro)
- [STIX and TAXII](https://docs.google.com/document/d/1yvqWaPPnPW-2NiVCLqzRszcx91ffMowfT5MmE9Nsy_w/edit?usp=sharing)

### What is STIX-SHIFTER?

STIX-shifter is an open source python library allowing software to connect to products that house data repositories by using `STIX Patterning`, and return results as `STIX Observations`.

STIX-Shifter is the heart of the **Universal Data Service** (UDS) that is provided as part of [IBM Security Connect](https://www.ibm.com/security/connect/).

### What is STIX Patterning? What are STIX Observations?

STIX 2 Patterning is a part of STIX that deals with the "matching things" part of STIX, which is an integral component of STIX Indicators.

This library takes in STIX 2 Patterns as input, and "finds" data that matches the patterns inside various products that house repositories of cybersecurity data. Examples of such products include SIEM systems, endpoint management systems, threat intelligence platforms, orchestration platforms, network control points, data lakes, and more.

In addition to "finding" the data by using these patterns, STIX-Shifter uniquely also _transforms the output_ into STIX 2 Observations. Why would we do that you ask? To put it simply - so that all of the security data, regardless of the source, mostly looks and behaves the same.

As anyone with experience in data science will tell you, the cleansing and normalizing of the data across domains, is one of the largest hurdles to overcome with attempting to build cross-platform security analytics. This is one of the barriers we are attempting to break down with STIX Shifter.

### This sounds like Sigma, I already have that

[Sigma](https://github.com/Neo23x0/sigma) and STIX Patterning have goals that are related, but at the end of the day has slightly different scopes. While Sigma seeks to be "for log files what Snort is for network traffic and YARA is for files", STIX Patterning's goal is to encompass _all three_ fundamental security data source types - network, file, and log - and do so simultaneously, allowing you to create complex queries and analytics that span domains. As such, so does STIX Shifter. It is critical to be able to create search patterns that span SIEM, Endpoint, Network, and File levels, in order to detect the complex patterns used in modern campaigns.

### What is a STIX-SHIFTER adapter?

A STIX-shifter adapter is the bridge that connects IBM Security Connect to a data source. Developing a new adapter expands on the data sources that STIX-shifter can support.

The combination of translation and transmission functions allows for a single STIX pattern to generate a native query for each supported data source. Each query is run, and the results are translated back into STIX objects; allowing for a uniform presentation of data.

The objective is to have all the security data, regardless of the data source to look and behave the same.

### Why would I want to use this?

You might want to use this library and contribute to development, if any of the following are true:

- You are a vendor or project owner who wants to add some form of query or enrichment functions to your product capabilities
- You are an end user and want to have a way to script searches and/or queries as part of your orchestration flow
- You are a vendor or project owner who has data that can be made available, and you want to contribute an adapter
- You just want to help make the world a safer place!

## Available Connectors

List updated: March 22, 2019

|         Connector          | Data Model |  Developer   | Translation | Connection | Availability |           Observables            |     Unsupported      |
| :------------------------: | :--------: | :----------: | :---------: | :--------: | :----------: | :------------------------------: | :------------------: |
|         IBM QRadar         |  Default   | IBM Security |     Yes     |    Yes     |   Release    | network-traffic, file, url, host |      ISSUPERSET      |
|         IBM BigFix         |  Default   | IBM Security |     Yes     |    Yes     | Pre-release  |                                  |                      |
|  Carbon Black CB Response  |  Default   | IBM Security |     Yes     |    Yes     |   Release    |          process, file           | ISSUPERSET, ISSUBSET |
|       Elastic Search       | MITRE CAR  |    MITRE     |     Yes     |     No     | Pre-release  |                                  |                      |
|       Elastic Search       |    ECS     | IBM Security |     No      |     No     |   Planned    |                                  |                      |
|      AWS SecurityHub       |  Default   | IBM Security |     Yes     |    Yes     | Pre-release  |                                  |                      |
| IBM Cloud Security Advisor |  Default   |  IBM Cloud   |     Yes     |     No     | Pre-release  |                                  |                      |
|           Splunk           | Splunk CIM | IBM Security |     Yes     |    Yes     |   Release    |                                  | ISSUPERSET, ISSUBSET |
|           Splunk           | MITRE CAR  |    MITRE     |     Yes     |    Yes     | Pre-release  |                                  |                      |

## How to use

Stix-shifter handles two primary functions:

1. **Translation**
   Stix-shifter translates STIX patterns into data source queries (in whatever query language the data source might use) and from data source results into bundled STIX observation objects (very similar to JSON).
2. **Transmission**
   Passes in authentication credentials to connect to a data source where stix-shifter can then ping or query the data source or fetch the query status and results.

Python 3.6 is required to use stix-shifter.

### Translation

#### Translate a STIX 2 pattern to a native data source query

##### INPUT: STIX 2 pattern

```
# STIX Pattern:
"[url:value = 'http://www.testaddress.com'] OR [ipv4-addr:value = '192.168.122.84']"
```

##### OUTPUT: Native data source query

```
# Translated Query:
"SELECT * FROM tableName WHERE (Url = 'http://www.testaddress.com')
OR
((SourceIpV4 = '192.168.122.84' OR DestinationIpV4 = '192.168.122.84'))"
```

#### Translate a JSON data source query result to a STIX bundle of observable objects

##### INPUT: JSON data source query result

```
# Datasource results:
[
    {
        "SourcePort": 567,
        "DestinationPort": 102,
        "SourceIpV4": "192.168.122.84",
        "DestinationIpV4": "127.0.0.1",
        "Url": "www.testaddress.com"
    }
]
```

##### OUTPUT: STIX bundle of observable objects

```
# STIX Observables
{
    "type": "bundle",
    "id": "bundle--2042a6e9-7f34-4a03-a745-502e358594c3",
    "objects": [
        {
            "type": "identity",
            "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d8",
            "name": "YourDataSource",
            "identity_class": "events"
        },
        {
            "id": "observed-data--cf2c58dc-200e-49e0-b6f7-e1997cccf707",
            "type": "observed-data",
            "created_by_ref": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d8",
            "objects": {
                "0": {
                    "type": "network-traffic",
                    "src_port": 567,
                    "dst_port": 102,
                    "src_ref": "1",
                    "dst_ref": "2"
                },
                "1": {
                    "type": "ipv4-addr",
                    "value": "192.168.122.84"
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "127.0.0.1"
                },
                "3": {
                    "type": "url",
                    "value": "www.testaddress.com"
                }
            }
        }
    ]
}
```

#### CLI help message for translation

```
usage: main.py translate [-h] [-x] [-m DATA_MAPPER]
                         {qradar,dummy,car,cim,splunk,elastic,bigfix,csa,csa:at,csa:nf,aws_security_hub,carbonblack}
                         {results,query} data_source data [options]

positional arguments:
  {qradar,dummy,car,cim,splunk,elastic,bigfix,csa,csa:at,csa:nf,aws_security_hub,carbonblack}
                        The translation module to use
  {results,query,parse} The translation action to perform
  data_source           STIX identity object representing a datasource
  data                  The STIX pattern or JSON results to be translated
  options               Options dictionary

optional arguments:
  -h, --help            show this help message and exit
  -x, --stix-validator  Run the STIX 2 validator against the translated results
  -m DATA_MAPPER, --data-mapper DATA_MAPPER
                        optional module to use for Splunk or Elastic STIX-to-query mapping
```

#### Translation is called with the following ordered parameters

```
<data source (ie. "qradar")> <"query", "results", "parse"> <{} or STIX identity object> <STIX pattern or data source results> <options>
```

**Data source:** This is the name of the module used for translation.

**Query, Results, or Parse:** This argument controls if stix-shifter is translating from a STIX pattern to the data source query, translating from the data source results to a STIX bundle of observation objects, or parsing the STIX pattern into it's components and time range.

**STIX Identity object:** An Identity object is used by stix-shifter to represent a data source and is inserted at the top of a returned observation bundle. Each observation in the bundle gets referenced to this identity. This parameter is only needed when converting from the data source results to the STIX bundle. When converting from a STIX pattern to a query, pass this in as an empty hash.

**STIX Pattern or data source results:** The input getting translated by stix-shifter.

**Options:** Options arguments come in as:

- **"select_fields":** string array of fields in the data source select statement
- **"mapping":** mapping hash for either STIX pattern to data source or data results to STIX observation objects
- **"resultSizeLimit":** integer to limit number or results in the data source query
- **"timeRange":** time window (ie. last 5 minutes) used in the data source query when START STOP qualifiers are absent

#### Example of converting a STIX pattern to (AQL) query

**Running the following:**

```
python main.py translate qradar query \
'{}' \
"[network-traffic:src_port = 37020 AND network-traffic:dst_port = 635] START t'2016-06-01T00:00:00.123Z' STOP t'2016-06-01T01:11:11.123Z'"
```

**Will return:**

```
{
  "queries": [
    "SELECT QIDNAME(qid) as qidname, qid as qid, CATEGORYNAME(category) as categoryname, category as categoryid, CATEGORYNAME(highlevelcategory) as high_level_category_name, highlevelcategory as high_level_category_id, logsourceid as logsourceid, LOGSOURCETYPENAME(logsourceid) as logsourcename, starttime as starttime, endtime as endtime, devicetime as devicetime, sourceaddress as sourceip, sourceport as sourceport, sourcemac as sourcemac, destinationaddress as destinationip, destinationport as destinationport, destinationmac as destinationmac, username as username, eventdirection as direction, identityip as identityip, identityhostname as identity_host_name, eventcount as eventcount, PROTOCOLNAME(protocolid) as protocol, BASE64(payload) as payload, URL as url, magnitude as magnitude, Filename as filename, URL as domainname FROM events WHERE destinationport = '635' AND sourceport = '37020' limit 10000 START 1464739200123 STOP 1464743471123"
  ]
}
```

#### Example of converting (QRadar) data to a STIX bundle

**Running the following:**

```
python main.py translate qradar results \
'{"type": "identity", "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3", "name": "QRadar", "identity_class": "events"}' \
'[{"sourceip": "192.0.2.0", "filename": "someFile.exe", "sourceport": "0123", "username": "root"}]' \
```

**Will return:**

```
{
    "type": "bundle",
    "id": "bundle--db4e0730-c5e3-4b72-9339-87ed7b1cf415",
    "objects": [
        {
            "type": "identity",
            "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
            "name": "QRadar",
            "identity_class": "events"
        },
        {
            "id": "observed-data--4eec7558-2016-464a-9ab7-5f7e263f2942",
            "type": "observed-data",
            "created_by_ref": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
            "objects": {
                "0": {
                    "type": "ipv4-addr",
                    "value": "192.0.2.0"
                },
                "1": {
                    "type": "network-traffic",
                    "src_ref": "0",
                    "src_port": "0123"
                },
                "2": {
                    "type": "file",
                    "name": "someFile.exe"
                },
                "3": {
                    "type": "user-account",
                    "user_id": "root"
                }
            }
        }
    ]
}
```

### Example of parsing the components and time range from a STIX pattern

**Running the following:**

```
python main.py translate qradar parse \
'{}' \
"[network-traffic:src_port = 37020 AND network-traffic:dst_port = 635] START t'2016-06-01T00:00:00.123Z' STOP t'2016-06-01T01:11:11.123Z'"
```

**Will return:**

```
{
  "parsed_stix": [
    {
      "attribute": "network-traffic:dst_port",
      "comparison_operator": "=",
      "value": 635
    },
    {
      "attribute": "network-traffic:src_port",
      "comparison_operator": "=",
      "value": 37020
    }
  ],
  "start_time": 1464739200123,
  "end_time": 1464743471123
}
```

The `start_time` represents the earliest of either the START qualifier or the default time range. The default time range is last 5 minutes unless overridden in the `time_range` options param. The `end_time` represents the latest of either the STOP qualifier or the current UTC time.

### Transmission

With the transmission module, you can connect to any products that house repositories of cybersecurity data.

The module uses the data source APIs to:

- Ping the data source
- Send queries in the native language of the data source
- Fetch query status (if supported by the APIs)
- Fetch query results
- Delete the query (if supported by the APIs)

#### CLI help message for transmission

```
usage: main.py transmit [-h]
                        {async_dummy,synchronous_dummy,qradar,splunk,bigfix,csa,aws_security_hub,carbonblack}
                        connection configuration
                        {ping,query,results,status,delete,is_async} ...

positional arguments:
  {async_dummy,synchronous_dummy,qradar,splunk,bigfix,csa,aws_security_hub,carbonblack}
                        Choose which connection module to use
  connection            Data source connection with host, port, and
                        certificate
  configuration         Data source authentication

optional arguments:
  -h, --help            show this help message and exit

operation:
  {ping,query,results,status,delete,is_async}
    ping                Pings the data source
    query               Executes a query on the data source
    results             Fetches the results of the data source query
    status              Gets the current status of the query
    delete              Delete a running query on the data source
    is_async            Checks if the query operation is asynchronous
```

#### Transmission is called with the following ordered parameters

```
<Data Source (ie. "qradar")> <Connection Params: '{"host":"host ip address", "port":"port number", "cert":"certificate"}'> <'{"auth": {authentication}}'> <Transmission Operation: ping, query, status, results or is_async> <Operation input>
```

**Data source:** This is the name of the module used for transmission.

**Connection Parameters:** Data source IP, port, and certificate

**Data source authentication:** Authentication hash

**Transmission Operation:** The transmission function being called. Transmission functions include:

- **Ping:** ping the data source
- **Query:** Execute a query on the data source. The input is the native data source query (after it has been translated from the STIX pattern).
- **Status:** Check the status of the executed query on an asynchronous data source. The input is the query UUID.
- **Results:** Fetch the results from the query. The input is the query UUID, offset, and length
- **Is Async** Returns a boolean indicating if the data source is asynchronous

#### Examples of using transmission from the CLI to connect to a (QRadar) data source.

##### Ping

```
python main.py transmit qradar '{"host":"<ip address>", "port":"<port>", "cert":"-----BEGIN CERTIFICATE-----\ncErTificateGoesHere=\n-----END CERTIFICATE-----"}' '{"auth": {"SEC":"1234..sec uid..5678"}}' ping
```

##### Query

```
python main.py transmit qradar '{"host":"<ip address>", "port":"<port>", "cert":"-----BEGIN CERTIFICATE-----\ncErTificateGoesHere=\n-----END CERTIFICATE-----"}' '{"auth": {"SEC":"1234..sec..uid..5678"}}' query "select * from events limit 100"
```

##### Status

```
python main.py transmit qradar '{"host":"<ip address>", "port":"<port>", "cert":"-----BEGIN CERTIFICATE-----\ncErTificateGoesHere=\n----END CERTIFICATE-----"}' '{"auth": {"SEC":"1234..sec..uid..5678"}}' status "uuid-12345"
```

##### Results

```
python main.py transmit qradar '{"host":"<ip address>", "port":"<port>", "cert":"-----BEGIN CERTIFICATE-----\ncErTificateGoesHere=\n-----END CERTIFICATE-----"}' '{"auth": {"SEC":"1234..sec..uid..5678"}}' results "uuid-12345" <offset> <length>
```

##### Is Async

```
python main.py transmit qradar '{"host":"<ip address>", "port":"<port>", "cert":"-----BEGIN CERTIFICATE-----\ncErTificateGoesHere=\n-----END CERTIFICATE-----"}' '{"auth": {"SEC":"1234..sec..uid..5678"}}' is_async
```

#### How UDS uses STIX-shifter

IBM's Universal Data Service first uses the translation modules to convert a STIX pattern into one or more native queries; this happens for each data source connected to IBM Security Connect.

Each translated query is sent to its respective data source, query status is polled, and query results are returned, all via the transmission modules.

The translation modules are again used to convert the JSON results into STIX observed-data objects. These objects get wrapped in STIX bundles to be used by the IBM Security Connect service.

Throughout this process, all data is stateless. The pattern, translated query, JSON results, and STIX objects do not get stored anywhere. UDS simply submits a pattern and fetches the resulting STIX as needed.

## Glossary

| Terms                     | Definition                                                                                                                                                                                              |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Modules                   | Folders in the stix-shifter project that contains code that is specific to a data source.                                                                                                               |
| STIX 2 patterns           | STIX patterns are expressions that represent Cyber Observable objects within a STIX Indicator STIX Domain Objects (SDOs). <br>They are helpful for modeling intelligence that indicates cyber activity. |
| STIX 2 objects            | JSON objects that contain CTI data. In STIX, these objects are referred to as Cyber Observable Objects.                                                                                                 |
| Data sources              | Security products that house data repositories.                                                                                                                                                         |
| Data source queries       | Queries written in the data source's native query language.                                                                                                                                             |
| Data source query results | Data returned from a data source query.                                                                                                                                                                 |

## Architecture Context

![STIX SHIFTER CLASS DIAGRAM](./adapter-guide/images/architecture.png)

## Contributing

We are thrilled you are considering contributing! We welcome all contributors.

Please read our [guidelines for contributing](CONTRIBUTING.md).

## Guide for creating new adapters

If you want to create a new adapter for STIX-shifter, see the [developer guide](adapter-guide/develop-stix-adapter.md)

## Licensing

Copyright 2019 IBM

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
