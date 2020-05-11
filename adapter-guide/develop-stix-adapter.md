# Developing a new STIX-shifter connector

- [Introduction](../README.md)
- [Scenario](#scenario)
- [Prerequisites](#prerequisites)
- [Steps](#steps)

## Scenario

### Participants

This scenario involves a software developer (_Developer A_) and an end user (_User A_). _Developer A_ wants to implement a new connector for the STIX-shifter project that can support a particular security product (_Product A_). _User A_ is another developer that uses the STIX-shifter library.

### Problem to solve

_User A_ performs security monitoring with _Product A_ and several other security products. The other products already have existing STIX-shifter connectors.

_User A_ would like to:

1. Submit one STIX pattern to query all the user’s security products at once. The use of a STIX pattern simplifies the search process because _User A_ does not need to know the query language or API calls for each security product.
1. See the query results from all the security products in one unified format (STIX bundle). With the assumption that the submitted pattern represents a potential security incident, the STIX bundle presents the query results in the context of the security event.

By implementing a new connector, _Developer A_ allows _Product A_ to fit into the workflow.

## Prerequisites

- Your development environment must use Python 3.6.
- You must have access to the target data source. In the sample scenario, you must have access to Product A data source.
- You must be familiar with Product A's query language and APIs.
- You must be familiar or understand the following concepts:
  - Observable objects. See [STIX™ Version 2.0. Part 4: Cyber Observable Objects](http://docs.oasis-open.org/cti/stix/v2.0/stix-v2.0-part4-cyber-observable-objects.html)
  - Stix patterning. See [STIX™ Version 2.0. Part 5: STIX Patterning](https://docs.oasis-open.org/cti/stix/v2.0/stix-v2.0-part5-stix-patterning.html)

## Steps

To develop a STIX-shifter connector for a data source:

1. Fork the `opencybersecurityalliance/stix-shifter` repository from https://github.com/opencybersecurityalliance/stix-shifter to work on your own copy of the library.
1. [Create a module folder](#create-a-module-folder).
1. [Create a Translation module](develop-translation-module.md).
1. [Create a Transmission module](develop-transmission-module.md).
1. [Create Configuration JSONs](develop-configuration-json.md).
1. [Create the module entry points](#create-module-entry-points).
1. Create a pull request to merge your changes in the `opencybersecurityalliance/stix-shifter` repository.

### Create a module folder

Connector modules are stored under the `stix_shifter_modules` directory. To help you get started with creating a new connector, two module templates are available. If your data source executes queries synchronously (there is no API call to check the status of the query), make a copy of the `synchronous_dummy` folder in the `stix_shifter_modules` directory. If your data source executes queries asynchronously, make a copy of the `async_dummy` folder. The instructions that follow use the async template as an example.

Rename the copied folder to match the data source your new connector is being developed for. For example, `abc_security_monitor`.

<!-- Todo: reword this, it sounds awkward -->
The module name is used as an argument when either translation or transmission is called. This argument is used throughout the project so that STIX-shifter knows which modules to use.

Each module contains the following directories and files: 

[stix_translation](develop-translation-module.md): Directory containing files needed for STIX translation. 

[stix_transmission](develop-transmission-module.md): Directory containing files for executing API calls to run data source queries.   

[configuration](develop-configuration-json.md): Directory containing configuration files.

entry_point.py: Initializes classes and paths used by the connector. 

### Create the module entry points

The `EntryPoint` class acts as a gateway to the various methods used by the translation and transmission classes. In most instances, it's fine to use the `setup_transmission_simple` and `setup_translation_simple(dialect_default='default')` methods. In cases where multiple dialects are used by the connector, the `dialect_default` argument is the dialect you wish to use as the default when the entire collection isn't passed in. See [Create a Translation module](develop-translation-module.md) to learn about dialects.


### Testing a new connector using the proxy host

Work on a new stix-shifter connector occurs after the project has been forked and cloned into a local development environment. Stix-shifter contains a **proxy** connector that facilitates a remote instance of the project calling out to a local instance. While in development, a new connector's working branch can be tested in any project using the stix-shifter library without first merging into the master branch on Github. A host is run on the local instance from the CLI. When a `proxy` data source is passed to the remote instance of stix-shifter, the real connection attributes (data source type, host, and port contained in the options) are passed onto the local instance of stix-shifter running the proxy host. The host will then use the new connector and return results back to the remote stix-shifter instance.

Open a terminal and navigate to your local stix-shifter directory. Run the host with the following command:

```
python main.py host "<STIX Identity Object>" "<Host IP address>:<Host Port>"
```

As an example:

```
python main.py host '{"type": "identity","id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff","name": "Bundle","identity_class": "events"}' "192.168.122.83:5000"
```
