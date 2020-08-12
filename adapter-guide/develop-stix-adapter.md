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


#### Entry points for synchronous connections

If the data source is synchronous, you must include `set_async(False)` in the connector's entry point initialization, otherwise the data source will be treated as asynchronous by default. Even though a synchronous connector omits the `query_connector.py` and `status_connector.py` files from its transmission directory, those connectors are still called in every module's entry point. For synchronous data sources, those connectors call the `BaseSyncConnector()` methods which return `{"success": True, "status": "COMPLETED", "progress": 100}`. 

```
  class EntryPoint(EntryPointBase):
    def __init__(self, connection={}, configuration={}, options={}):
      super().__init__(connection, configuration, options)
      self.set_async(False)
      if connection:
        api_client = APIClient(connection, configuration)
        base_sync_connector = BaseSyncConnector()
        ping_connector = PingConnector(api_client)
        query_connector = base_sync_connector
        status_connector = base_sync_connector
        ...
        self.set_query_connector(query_connector)
        self.set_ping_connector(ping_connector)
        self.set_status_connector(status_connector)
        self.set_delete_connector(delete_connector)
        self.set_results_connector(results_connector)
      else:
        ...
```


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

### Packaging individual connectors

Stix-shifter can be broken into several python whl packages by using the `setup.py` script found in the root of the project. This packaging script can be called from the CLI:

```
MODE='<module name>' VERSION='<connector version>' python3 setup.py bdist_wheel
```

`MODE` is a required argument that is used to determine how the project is packaged. Mode options include:

`'1'` = Include everything in one whl package

`'3'` - 3 whl packages respectively for stix-shifter, stix-shifter-utils and stix-shifter-modules

`'N'` - `stix-shifter`, `stix-shifter-utils`, and each connector is packaged separately

`<module name>` - package only the specified connector

The `VERSION` argument is optional. If missing, version 1.0.0 is attached to the package name.

When the script is executed, a new `dist` directory is created at the root of the stix-shifter project; this contains the generated whl packages.

A packaged connector follows the naming convention of: 

`stix_shifter_modules_<module name>-<version>-py2.py3-none-any.whl`

The contents of the package has the same directory structure as the module in the project:

```
stix_shifter_modules => 
    <module name> =>
        configuration
        stix_translation
        stix_transmission
        entry_point
```

### Building images of the connectors

You can build the docker image your developed connector locally and publish it to your desired repository. In order to do that, follow the below steps-

1. Make sure you have built the wheel distribution of the connector module by following the steps in [Packaging individual connectors section](#Packaging-individual-connectors).
2. `image_builder` directory in your stix-shifter project contains the required scripts that will automatically build the connector image. You can copy the directory in a separate location or keep it inside stix-shifter project.
3. Create a folder named `bundle` inside `image_builder/` directory.
4. Move your desired connector wheel file (`stix_shifter_modules_<module name>-<version>-py2.py3-none-any.whl`) to the bundle folder created in step 3.
5. Run `build_local.sh` script.
6. Image should be automatically built in your running docker client.