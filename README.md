# stix-shifter

#### Table of Contents

[Introduction](#introduction)<br/>
[How to use](#How-to-use)<br/>
[Translation](#translation)<br/>
[Transmission](#transmission)<br/>
[Contributing](#contributing)<br/>
[Creating new modules](#creating-new-modules)<br/>
[Licensing](#licensing)

# Introduction

This project consists of an open source library allowing software to connect to products that house data repositories using STIX Patterning, and return results as STIX Observations.

Requires Python 3.6

## It is a who that does what now? What is STIX Patterning? What are STIX Observations?

[Structured Threat Information Expression (STIX™)](https://oasis-open.github.io/cti-documentation/) is a language and serialization format used to exchange cyber threat intelligence (CTI). STIX 2 Patterning is a part of STIX that deals with the "matching things" part of STIX, which is an integral component of STIX Indicators.

This library takes in STIX 2 Patterns as input, and "finds" data that matches the patterns inside various products that house repositories of cybersecurity data. Examples of such products include SIEM systems, endpoint management systems, threat intelligence platforms, orchestration platforms, network control points, data lakes, and more.

In addition to "finding" the data using these patterns, STIX-Shifter uniquely also _transforms the output_ into STIX 2 Observations. Why would we do that you ask? To put it simply - so that all of the security data, regardless of the source, mostly looks and behaves the same. As anyone with experience in data science will tell you, the cleansing and normalizing of the data across domains, is one of the largest hurdles to overcome with attempting to build cross-platform security analytics. This is one of the barriers we are attempting to break down with STIX Shifter.

## This sounds like Sigma, I already have that

[Sigma](https://github.com/Neo23x0/sigma) and STIX Patterning have goals that are related, but at the end of the day have slightly different scopes. While Sigma seeks to be "for log files what Snort is for network traffic and YARA is for files", STIX Patterning's goal is to encompass _all three_ fundamental security data source types - network, file, and log - and do so simultaneously, allowing you to create complex queries and analytics that span domains. As such, so does STIX Shifter. We feel it is critical to be able to create search patterns that span SIEM, Endpoint, Network, and File levels, in order to detect the complex patterns used in modern campaigns.

## Why would I want to use this?

You may want to use this library and/or contribute to development, if any of the follwing are true:

- You are a vendor or project owner who wants to add some form of query or enrichment functionality to your product capabilities
- You are an end user and want to have a way to script searches and/or queries as part of your orchestration flow
- You are a vendor or project owner who has data that could be made available, and you want to contribute an adapter
- You just want to help make the world a safer place!

# How to use

Stix-shifter handles two primary functions:

1. **Translation:** Stix-shifter translates STIX patterns into data source queries (in whatever query language the data source may use) and from data source results into bundled STIX observation objects (very similar to JSON).
2. **Transmission:** Passes in authentication credentials to connect to a data source where stix-shifter can then ping or query the data source or fetch the query status and results.

## Translation

### Converting from STIX Patterns to data source queries (query) or from data source results to STIX cyber observables (results)

#### Call the stix_translation in the format of

```
usage: stix_translation.py translate [-h]
                                 {'qradar', 'dummy', 'car', 'cim', 'splunk', 'elastic', 'bigfix', 'csa', 'csa:at', 'csa:nf'}
                                 {results, query} data

positional arguments:
{qradar, dummy}                        What translation module to use
{results, query}                       What translation action to perform
data source                            A STIX identity object
data                                   STIX pattern or data to be translated

optional arguments:
  -h, --help            show this help message and exit
  -x                    run STIX validation on each observable as it's written to the output JSON
```

### Translation is called with the following ordered parameters:

```
<data source (ie. "qradar")> <"query" or "results"> <{} or STIX identity object> <STIX pattern or data source results> <options>
```

**Data source:** This will be the name of the module used for translation. Currently stix-shifter supports QRadar, Splunk, and Elastic.

**Query or Results:** This argument controls if stix-shifter is translating from a STIX pattern to the data source query, or it it’s translating from the data source results to a STIX bundle of observation objects

**STIX Identity object:** An Identity object is used by stix-shifter to represent a data source and is inserted at the top of a returned observation bundle. Each observation in the bundle gets referenced to this identity. This parameter is only needed when converting from the data source results to the STIX bundle. When converting from a pattern to a query, pass this in as an empty hash.

**STIX Pattern or data source results:** The input getting translated by stix-shifter.

**Options:** Options arguments come in as:

- **"select_fields":** string array of fields in the data source select statement
- **"mapping":** mapping hash for either stix pattern to data source or data results to STIX observation objects
- **"result_limit":** integer to limit number or results in the data source query
- **"time_range":** time window (ie. last 5 minutes) used in the data source query when START STOP qualifiers are absent

## Example of converting a STIX pattern to (AQL) query

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
  ],
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
  ]
}
```

## Example of converting (QRadar) data to a STIX bundle

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

## Transmission

#### Call the stix_transmission in the format of

```
usage: stix_transmission.py transmit [-h]
                      {'async_dummy', 'synchronous_dummy', 'qradar', 'splunk', 'bigfix', 'csa'}

positional arguments:
{<async_dummy, synchronous_dummy, qradar, splunk, bigfix>}         Transmission module to use
  {"host": <host IP>, "port": <port>, "cert": <certificate>} Data source connection
  {"auth": <authentication>} Data source authentication
  {
    "type": <ping, query, results, is_async, status>,   Translation method to be used
    "search_id": <uuid> (for results and status),
    "query": <native datasource query string> (for query),
    "offset": <offset> (for results),
    "length": <length> (for results)
  }

optional arguments:
  -h, --help            show this help message and exit
```

### Transmission is called with the following ordered parameters:

```
<Data Source (ie. "qradar")> <Connection Params: '{"host":"host ip address", "port":"port number", "cert":"certificate"}'> <'{"auth": {authentication}}'> <Transmission Operation: ping, query, status, results or is_async> <Operation input>
```

**Data source:** This will be the name of the module used for transmission. Currently stix-shifter supports QRadar, Splunk, and Bigfix.

**Connection Parameters:** Data source IP, port, and certificate

**Data source authentication:** Authentication hash

**Transmission Operation:** The transmission function being called. Transmission functions include:

- **Ping:** ping the data source
- **Query:** Execute a query on the data source. The input is the native data source query (after it has been translated from the STIX pattern).
- **Status:** Check the status of the executed query. The input is the query UUID.
- **Results:** Fetch the results from the query. The input is the query UUID, offset, and length
- **Is Async**

### Examples of using transmission from the CLI

#### Ping

```
python main.py transmit qradar '{"host":"<ip address>", "port":"<port>", "cert":"-----BEGIN CERTIFICATE-----\ncErTificateGoesHere=\n-----END CERTIFICATE-----"}' '{"auth": {"SEC":"1234..sec uid..5678"}}' ping
```

#### Query (AQL)

```
python main.py transmit qradar '{"host":"<ip address>", "port":"<port>", "cert":"-----BEGIN CERTIFICATE-----\ncErTificateGoesHere=\n-----END CERTIFICATE-----"}' '{"auth": {"SEC":"1234..sec..uid..5678"}}' query "select * from events limit 100"
```

#### Status

```
python main.py transmit qradar '{"host":"<ip address>", "port":"<port>", "cert":"-----BEGIN CERTIFICATE-----\ncErTificateGoesHere=\n----END CERTIFICATE-----"}' '{"auth": {"SEC":"1234..sec..uid..5678"}}' status "uuid-12345"
```

#### Results

```
python main.py transmit qradar '{"host":"<ip address>", "port":"<port>", "cert":"-----BEGIN CERTIFICATE-----\ncErTificateGoesHere=\n-----END CERTIFICATE-----"}' '{"auth": {"SEC":"1234..sec..uid..5678"}}' results "uuid-12345" <offset> <length>
```

#### Is Async

```
python main.py transmit qradar '{"host":"<ip address>", "port":"<port>", "cert":"-----BEGIN CERTIFICATE-----\ncErTificateGoesHere=\n-----END CERTIFICATE-----"}' '{"auth": {"SEC":"1234..sec..uid..5678"}}' is_async
```

### Example of converting a STIX pattern to an IBM QRadar AQL query:

[See the QRadar module documentation](stix_shifter/stix_translation/src/modules/qradar/README.md)

### Example of converting IBM QRadar events to STIX:

[See the QRadar module documentation](stix_shifter/stix_translation/src/modules/qradar/README.md)

# Contributing

We are thrilled you are considering contributing! We welcome all contributors.

Please read our [guidelines for contributing](CONTRIBUTING.md).

# Creating new modules

To create a new module that can be used when importing stix-shifter, follow these steps:

- Create a directory with the name of your module in the `stix-shifter/src/modules/` directory
- In `stix-shifter.py`, add `<module-name>` to the `MODULES` array at the top of the file
- In your module directory, create a new python code file named `<module-name>_translator.py`. This is where you'll be defining your concrete translator class
  - In `<module-name>_translator.py`, define a class named `Translator` and have it extend `BaseTranslator` from `stix-shifter/src/modules/base/base_translator.py`. (You can use `stix-shifter/src/modules/dummy/dummy_translator.py` as an example)
  - In `__init__` you need to assign `self.result_translator` and `self.query_translator` to the appropriate query and result translator you want your module to use. For example the QRadar translator uses `JSONToStix` as its result translator and `StixToAQL` as its query translator
  - You can write your own query and result translators as well, they must be based off of `BaseQueryTranslator` and `BaseResultTranslator` found in `stix-shifter/src/modules/base/`. Again, you can use the dummy module as a decent example on how to setup the concrete classes found in `stix-shifter/src/modules/dummy/`
- Once you have this all set up you can invoke your module by running `stix_shifter.py` and passing in your translator module name as the first parameter. The second parameter `query or result` determines if your module runs the query or result translator. The third parameter `data` is passed into your translator as the data that will be translated. If you've imported `stix_shifter.py` into other python code, you can invoke it by running the `translate(module, translation_type, data)` function
- IMPORTANT: If you're including any json data files in your module, be sure to include the path in `MANIFEST.in` so that it's included in the packaging

# Licensing

:copyright: Copyright IBM Corp. 2018

All code contained within this project repository or any
subdirectories is licensed according to the terms of the Apache v2.0 license,
which can be viewed in the file [LICENSE](LICENSE).

# Open Source @ IBM

[Find more open source projects on the IBM Github Page](http://ibm.github.io/)
