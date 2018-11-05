# stix-shifter

This project consists of an open source library allowing software to connect to products that house data repositories using STIX Patterning, and return results as STIX Observations.

Requires Python 3.6

## It is a who that does what now? What is STIX Patterning? What are STIX Observations?

[Structured Threat Information Expression (STIX™)](https://oasis-open.github.io/cti-documentation/) is a language and serialization format used to exchange cyber threat intelligence (CTI). STIX 2 Patterning is a part of STIX that deals with the "matching things" part of STIX, which is an integral component of STIX Indicators.

This library takes in STIX 2 Patterns as input, and "finds" data that matches the patterns inside various products that house repositories of cybersecurity data. Examples of such products include SIEM systems, endpoint management systems, threat intelligence platforms, orchestration platforms, network control points, data lakes, and more.

In addition to "finding" the data using these patterns, STIX-Shifter uniquely also _transforms the output_ into STIX 2 Observations. Why would we do that you ask? To put it simply - so that all of the security data, regardless of the source, mostly looks and behaves the same. As anyone with experience in data science will tell you, the cleansing and normalizing of the data accross domains, is one of the largest hurdles to overcome with attempting to build cross-platform security analytics. This is one of the barriers we are attempting to break down with STIX Shifter.

## This sounds like Sigma, I already have that

[Sigma](https://github.com/Neo23x0/sigma) and STIX Patterning have goals that are related, but at the end of the day have slightly different scopes. While Sigma seeks to be "for log files what Snort is for network traffic and YARA is for files", STIX Patterning's goal is to encompass _all three_ fundamental security data source types - network, file, and log - and do so simultaneously, allowing you to create complex queries and analytics that span domains. As such, so does STIX Shifter. We feel it is critical to be able to create search patterns that span SIEM, Endpoint, Network, and File levels, in order to detect the complex patterns used in modern campaigns.

## Why would I want to use this?

You may want to use this library and/or contribute to development, if any of the follwing are true:

- You are a vendor or project owner who wants to add some form of query or enrichment functionality to your product capabilities
- You are an end user and want to have a way to script searches and/or queries as part of your orchestrsation flow
- You are a vendor or project owner who has data that could be made available, and you want to contribute an adapter
- You just want to help make the world a safer place!

# How to use

## Converting from STIX Patterns to data source queries (query) or from data source results to STIX cyber observables (results)

### Call the stix_shifter in the format of

```
usage: stix_shifter.py translate [-h]
                                 {qradar, dummy, splunk}
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

## Connecting to a data source

### Call the stix_shifter in the format of

```
usage: stix_shifter.py transmit [-h]
                      {async_dummy, synchronous_dummy, qradar, splunk, bigfix}

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

### Example of converting a STIX pattern to an IBM QRadar AQL query:

[See the QRadar module documentation](stix_shifter/src/modules/qradar/README.md)

### Example of converting IBM QRadar events to STIX:

[See the QRadar module documentation](stix_shifter/src/modules/qradar/README.md)

# Contributing

We are thrilled you are considering contributing! We welcome all contributors.

Please read our [guidelines for contributing](CONTRIBUTING.md).

## Creating new translator modules

To create a new module that can be used when importing stix-shifter, follow these steps:

- Create a directory with the name of your module in the `stix-shifter/src/modules/` directory
- In `stix-shifter.py`, add `<module-name>` to the `MODULES` array at the top of the file
- In your module directory, create a new python code file named `<module-name>_translator.py`. This is where you'll be defining your concrete translator class
  - In `<module-name>_translator.py`, define a class named `Translator` and have it extend `BaseTranslator` from `stix-shifter/src/modules/base/base_translator.py`. (You can use `stix-shifter/src/modules/dummy/dummy_translator.py` as an example)
  - In `__init__` you need to assign `self.result_translator` and `self.query_translator` to the appropriate query and result translator you want your module to use. For example the QRadar translator uses `JSONToStix` as its result translator and `StixToAQL` as its query translator
  - You can write your own query and result translators as well, they must be based off of `BaseQueryTranslator` and `BaseResultTranslator` found in `stix-shifter/src/modules/base/`. Again, you can use the dummy module as a decent example on how to setup the concrete classes found in `stix-shifter/src/modules/dummy/`
- Once you have this all set up you can invoke your module by running `stix_shifter.py` and passing in your translator module name as the first parameter. The second parameter `query or result` determines if your module runs the query or result translator. The third parameter `data` is passed into your translator as the data that will be translated. If you've imported `stix_shifter.py` into other python code, you can invoke it by running the `translate(module, translation_type, data)` method
- IMPORTANT: If you're including any json data files in your module, be sure to include the path in `MANIFEST.in` so that it's included in the packaging

# Licensing

:copyright: Copyright IBM Corp. 2018

All code contained within this project repository or any
subdirectories is licensed according to the terms of the Apache v2.0 license,
which can be viewed in the file [LICENSE](LICENSE).

# Open Source @ IBM

[Find more open source projects on the IBM Github Page](http://ibm.github.io/)
