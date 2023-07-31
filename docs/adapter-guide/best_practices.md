# Best practices when developing a new connector

An assessment of the data source APIs should be made before beginning implementation of a connector. The APIs should return a good coverage of [cyber observable](https://docs.oasis-open.org/cti/stix/v2.0/stix-v2.0-part4-cyber-observable-objects.html) data that fits within the standard STIX `observed-data` objects. If most of the data returned is getting mapped to custom STIX objects or properties, it may be an indication that the data source is not a good fit for a connector. The APIs should also allow for robust filtering of the data, or support a query language; this is essential for executing federated searches against multiple connectors using STIX patterning.

Verify the data returned by the connector is stored in cyber observable objects as defined in the [STIX 2.0 standard](https://docs.oasis-open.org/cti/stix/v2.0/stix-v2.0-part4-cyber-observable-objects.html). Data that doesn’t fit into standard cyber observable objects may be added as custom STIX objects with the following preferences:

<!-- TODO: Make note of community-defined custom extensions -->

### Custom Extensions on standard STIX objects

Custom STIX may be added in user-defined custom extensions to the standard STIX objects. For example, if the data source returns fields that should be grouped together and could enrich the data presented in the file object, it could be added to the object like so:

```JSON
"extensions": {
    "x-datasource-custom-file-extension": {
        "foo_val": "foo",
        "bar_val": "bar"
    }
}
```
See [section 5.2 Custom Object Extensions](https://docs.oasis-open.org/cti/stix/v2.0/stix-v2.0-part3-cyber-observable-core.html) in the STIX standard for more details.

### Custom properties on standard STIX objects

Custom STIX can be added as a custom object property on standard STIX objects. For example if the data source returns data related to the file object but not captured in one of the file object’s standard properties, it could be added like so:

```JSON
{

    "0": {
        "type": "file",
        "name": "myfile.exe",
        "x_datasource_custom_property": "bar"
    }
}
```

### Custom STIX objects

Custom STIX can be added in a custom object with the type following the naming convention of `x-datasource-object-type`

### Other considerations

Data should not be repeated in the same observed-data object. That is, if a data element is represented as a property on a standard STIX object, it should not also be included as a custom property. If a custom STIX object needs to refer to an existing property on another object, it should do so using referencing rather than repeating the data.

Ensure blank data values are not written to the STIX results. This should happen automatically via the json-to-STIX flow but this may need to be improved to prevent bad data from slipping through (ie. certain IP values and mac addresses that we wish to strip out).

When a connector is close to completion, generate a sample STIX bundle with the [execute command](https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/OVERVIEW.md#execute) and run it through the [validator script](https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/bundle_validator) to catch errors.
