In this STIX Shifter Utility, we are creating and returning a STIX Bundle with the following STIX Domain Objects (SDO's):
  1. Identity
  2. Extension-Definition
  3. Indicator
  4. Malware
  5. Infrastructure
  6. Sighting

We are going to be using `stix_shifter_utils/normalization/BaseNormalization.py` in our `results_translator.py` file, by creating a `sdo_translator.py` file which calls the BaseNormalization , and depending on your use case, you can modify the returned bundle fields further

A sample `sdo_translator.py` file:
```python
from stix_shifter_utils.normalization.BaseNormalization import BaseNormalization

class SdoTranslator(BaseNormalization):
    pass
```
In `results_translator.py`:
```python
from . import sdo_translator

class ResultsTranslator(BaseResultTranslator):
  def translate_results(self, data_source, data):
    sdo_translator_object = sdo_translator.SdoTranslator(data_source, self.options)
    stix_bundle = sdo_translator_object.create_stix_bundle()

```

We can pass the optional CLI argument `stix_validator=True` to run the stix validator to assert if our STIX Bundle output is a valid STIX 2.1 bundle that is passed as part of the `self.options` param

The following piece of code above does the following:

```json
{
    "type": "bundle",
    "id": "bundle--b461f6cd-6bfb-43a5-ae5a-e7020cef25dd",
    "spec_version": "2.1",
    "objects": []
}
```

# All SDO creation methods include the required common properties for each SDO, and its type

It creates an empty STIX 2.1 bundle with no STIX Domain Objects (SDOs), we can then add SDOs of our choosing (identity, extension-definition, indicator, malware, infrastructure) based on our use cases for each threat feed. In our example, we will be creating an identity, extension-definition, and indicator SDO on our stix bundle

First, we'll add the identity SDO, using the following snippet:

```python
    identity = {'name': 'SampleConnector'}
    NAMESPACE = '00abedb4-aa42-466c-9c01-fed23315a9b7' # Example namespace but cannot be used per STIX 2.1 documentation
    identity_object = sdo_translator_object.create_identity_sdo(identity, NAMESPACE)
    stix_bundle['objects'] += identity_object
```

The SDO creation takes two arguments, the data_source, and NAMESPACE, a UUID value that you can choose to use for your connector

For more information: https://docs.oasis-open.org/cti/stix/v2.1/cs01/stix-v2.1-cs01.html#_64yvzeku5a5c

The first argument, is the identity object, defined by STIX 2.1 documentation:

https://docs.oasis-open.org/cti/stix/v2.1/cs01/stix-v2.1-cs01.html#_wh296fiwpklp

You only need to pass the minimum required property in the first parameter for it to be a valid. You can choose to include optional fields if you want to enrich your identity object with more information

The namespace ensures that our identity SDO's `id` will always be unique for and same for each bundle (deterministic)

You can add optional properties to the identity dictionary as specified in the STIX 2.1 documentation to include those fields (example in indicator SDO below)

Our bundle will now be as following:

```json
{
    "type": "bundle",
    "id": "bundle--b461f6cd-6bfb-43a5-ae5a-e7020cef25dd",
    "spec_version": "2.1",
    "objects": [
      {
        "type": "identity",
        "name": "SampleConnector",
        "spec_version": "2.1",
        "id": "identity--f67e2e66-6da9-5c78-9d90-e3518a1256e5",
        "created": "2022-02-28T15:39:24.189Z",
        "modified": "2022-02-28T15:39:24.189Z",
        "identity_class": "system"
      }
    ]
}
```

Next, we will add an Extension-Definition object since we plan on adding custom stix properties to our indicator SDO, such as `threat_score` that will inform us how malicious the indicator is:

```python
    toplevel_properties = ['threat_score']
    nested_properties = []
    extension_object = sdo_translator_object.create_extension_sdo(identity_object[0], NAMESPACE, nested_properties, toplevel_properties=toplevel_properties)
    stix_bundle['objects'] += extension_object
```

The first argument is the identity SDO that we created earlier, all create_sdo's return the SDO as a type `list` so that we can append it to our stix_bundle['objects'] so we pass identity_object[0] as the first argument, and namespace as the second. The two optional arguments are `nested_properties` and `toplevel_properties` that determine which properties we want to include in our sdo as toplevel or nested

Our bundle will now be as following:

```json
{
    "type": "bundle",
    "id": "bundle--b461f6cd-6bfb-43a5-ae5a-e7020cef25dd",
    "spec_version": "2.1",
    "objects": [
      {
        "type": "identity",
        "name": "SampleConnector",
        "spec_version": "2.1",
        "id": "identity--f67e2e66-6da9-5c78-9d90-e3518a1256e5",
        "created": "2022-02-28T15:39:24.189Z",
        "modified": "2022-02-28T15:39:24.189Z",
        "identity_class": "system"
      },
      {
        "id": "extension-definition--3bb57c17-477e-5bd4-bdbd-f588899678cf",
        "type": "extension-definition",
        "spec_version": "2.1",
        "name": "SampleConnector extension",
        "created": "2022-02-28T15:39:24.189Z",
        "modified": "2022-02-28T15:39:24.189Z",
        "created_by_ref": "identity--f67e2e66-6da9-5c78-9d90-e3518a1256e5",
        "schema": "https://www.ibm.com/cp4s",
        "version": "1.2.1",
        "extension_types": [
          "toplevel-property-extension"
        ],
        "extension_properties": [
          "threat_score"
        ]
      },
    ]
}
```

Finally, we will now add the indicator SDO to our STIX Bundle, according to the documentation:

https://docs.oasis-open.org/cti/stix/v2.1/cs01/stix-v2.1-cs01.html#_muftrcpnf89v

The required fields for an indcator SDO are: 
1. pattern

the other two required fields, pattern_type and valid_from are generated as part of the method call

So we can pass a dict object as such:

```python
    indicator = {"pattern": "[ipv4-addr:value='0.0.0.0']"}
    threat_score = {"threat_score": 10}
    extension_id = extension_object[0]['id']
    identity_id = identity_object[0]['id']
    nested_indicator = []
    top_indicator = [threat_score]

    indicator_stix_object = sdo_translator_object.create_indicator_sdo(indicator_object, identity_id, extension_id, nested_indicator, top_indicator)
    stix_bundle['objects'] += indicator_stix_object

```

This will result in the following STIX Indicator SDO:

```json
{
  "type": "indicator",
  "spec_version": "2.1",
  "id": "indicator--05b574d2-e753-445f-851f-c06acf23bc7c",
  "pattern": "[ipv4-addr:value='0.0.0.0']",
  "pattern_type": "stix",
  "created_by_ref": "identity--f67e2e66-6da9-5c78-9d90-e3518a1256e5",
  "created": "2022-02-28T15:39:24.189Z",
  "modified": "2022-02-28T15:39:24.189Z",
  "valid_from": "2022-02-28T15:39:24.189Z",
}
```

`def create_indicator_sdo(self, indicator_object: dict, identity_id: str, extension_id:str=None, nested_properties:list=None, top_properties:list=None):`

For an indicator SDO, you can add custom properties as optional params (extension_id, nested_properties, toplevel_properties)

it requires an indicator_object as a dictionary, but for now we will try to see what happens if we want to create an indicator SDO with optional properties in STIX 2.1 documentation such as name, description, indicator_types:

```python
    indicator = {
      "pattern": "[ipv4-addr:value='0.0.0.0']",
      "name": "0.0.0.0",
      "description": "Not Available",
      "indicator_types": ["unknown"]
    }
    threat_score = {"threat_score": 10}
    extension_id = extension_object[0]['id']
    identity_id = identity_object[0]['id']
    nested_indicator = []
    top_indicator = [threat_score]

    indicator_stix_object = sdo_translator_object.create_indicator_sdo(indicator_object, identity_id, extension_id, nested_indicator, top_indicator)
    stix_bundle['objects'] += indicator_stix_object

```

This STIX Shifter connector returns a STIX Bundle in the following format using BaseNormalization from `stix_shifter_utils/normalization/BaseNormalization.py`:

##### An example of a STIX Normalization Bundle:

```json
{
    "type": "bundle",
    "id": "bundle--b461f6cd-6bfb-43a5-ae5a-e7020cef25dd",
    "spec_version": "2.1",
    "objects": [
        {
            "type": "identity",
            "name": "SampleConnector",
            "spec_version": "2.1",
            "id": "identity--f67e2e66-6da9-5c78-9d90-e3518a1256e5",
            "created": "2022-02-28T15:39:24.189Z",
            "modified": "2022-02-28T15:39:24.189Z",
            "identity_class": "system"
        },
        {
            "id": "extension-definition--3bb57c17-477e-5bd4-bdbd-f588899678cf",
            "type": "extension-definition",
            "spec_version": "2.1",
            "name": "SampleConnector extension",
            "created": "2022-02-28T15:39:24.189Z",
            "modified": "2022-02-28T15:39:24.189Z",
            "created_by_ref": "identity--f67e2e66-6da9-5c78-9d90-e3518a1256e5",
            "schema": "https://www.ibm.com/cp4s",
            "version": "1.2.1",
            "extension_types": [
                "toplevel-property-extension"
            ],
            "extension_properties": [
                "x_ibm_original_threat_feed_data",
                "threat_score"
            ]
        },
        {
            "type": "indicator",
            "spec_version": "2.1",
            "id": "indicator--05b574d2-e753-445f-851f-c06acf23bc7c",
            "pattern": "[ipv4-addr:value='0.0.0.0']",
            "pattern_type": "stix",
            "created_by_ref": "identity--f67e2e66-6da9-5c78-9d90-e3518a1256e5",
            "created": "2022-02-28T15:39:24.189Z",
            "modified": "2022-02-28T15:39:24.189Z",
            "valid_from": "2022-02-28T15:39:24.189Z",
            "name": "0.0.0.0",
            "description": "Not Available",
            "indicator_types": [
                "unknown"
            ],
            "threat_score": 10,
        }
    ]
}
```

