# Developing a new STIX-shifter adapter

- [Introduction](../README.md)
- [Scenario](#scenario)
- [Prerequisites](#prerequisites)
- [Steps](#steps)

## Scenario

### Participants

This scenario involves a software developer (_Developer A_) and an end user (_User A_). _Developer A_ wants to implement a new adapter for the STIX-shifter project that can support a particular security product (_Product A_). _User A_ is another developer that uses the STIX-shifter library.

### Problem to solve

_User A_ performs security monitoring with _Product A_ and several other security products. The other products already have existing STIX-shifter adapters.

_User A_ would like to:

1. Submit one STIX pattern to query all the user’s security products at once. The use of a STIX pattern simplifies the search process because _User A_ does not need to know the query language or API calls for each security product.
1. See the query results from all the security products in one unified format (STIX bundle). With the assumption that the submitted pattern represents a potential security incident, the STIX bundle presents the query results in the context of the security event.

By implementing a new adapter, _Developer A_ allows _Product A_ to fit into the workflow.

## Prerequisites

- Your development environment must use Python 3.6.
- You must have access to the target data source. In the sample scenario, you must have access to Product A data source.
- You must be familiar with Product A's query language and APIs.
- You must be familiar or understand the following concepts:
  - Observable objects. See [STIX™ Version 2.0. Part 4: Cyber Observable Objects](http://docs.oasis-open.org/cti/stix/v2.0/stix-v2.0-part4-cyber-observable-objects.html)
  - Stix patterning. See [STIX™ Version 2.0. Part 5: STIX Patterning](https://docs.oasis-open.org/cti/stix/v2.0/stix-v2.0-part5-stix-patterning.html)

## Steps

To develop a STIX-shifter adapter for a data source:

1. Fork the `IBM/stix-shifter` repository from https://github.com/IBM/stix-shifter to work on your own copy of the library.
1. [Create a Translation module](#create-a-translation-module).
1. [Create a Transmission module](#create-a-transmission-module).
1. Create a pull request to merge your changes in the `IBM/stix-shifter` repository.

### Create a Translation module

1. [Create a translation module folder](#step-1-create-a-translation-module-folder)
1. [Rename the dummy_translator.py file](#step-2-rename-the-dummy-translator-file)
1. [Edit the from_stix_map.json file](#step-3-edit-the-from_stix_map-json-file)
1. [Edit the query_constructor.py file](#step-4-edit-the-query-constructor-file)
1. [Edit the to_stix_map.json file](#step-5-edit-the-to_stix_map-json-file)
1. [If required by your data source, update the transformers.py file](#step-6-if-required-by-your-data-source-update-the-transformers-file)
1. [Update the MANIFEST.in file to include the path to the json mapping folder](#step-7-update-the-manifest-file-to-include-the-path-to-the-json-mapping-folder)
1. [Verify that the translation module was created successfully](#step-8-verify-that-the-translation-module-was-created-successfully)

#### Step 1. Create a translation module folder

1. Go to `stix_shifter/stix_translation/src/modules/`.
2. Copy the `dummy` translation module folder. It is a template to help you get started quickly. It contains the necessary files that your translation module needs. You need to customize it based on your data source.

![Translation module dummy folder](./images/translation-module-dummy-folder.png)

3. Rename your `dummy` translation module folder to match the name of your data source. For example, `abc`.

   The data source name is used as an argument when either translation or transmission is called. This argument is used throughout the project so that STIX-shifter knows which modules to use.

   **Note:** The translation and transmission modules must have the same name.

4. Verify that your translation module folder contains the following folders and files.

| Folder/file             | Why is it important? Where is it used?                                                                                                                                                                                                                                                                     |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| json/from_stix_map.json | This mapping file is used to translate a STIX pattern to a data source query result.                                                                                                                                                                                                                       |
| json/to_stix_map.json   | This mapping file is used to translate a data source query result into STIX objects.                                                                                                                                                                                                                       |
| **init**.py             | This file is required by Python to properly handle library directories.                                                                                                                                                                                                                                    |
| data_mapping.py         | This file uses the mappings that are defined in the from_stix_map.json file to map the STIX objects and their properties to field names from the data source.                                                                                                                                              |
| dummy_translator.py     | This file contains the Translator class. It inherits the BaseTranslator abstract base class and is the interface to the rest of the translation logic.                                                                                                                                                     |
| query_constructor.py    | This file contains the QueryStringPatternTranslator class, which translates the ANTLR parsing of the STIX pattern to the native data source query.                                                                                                                                                         |
| stix_to_query.py        | This file contains the StixToQuery class, which inherits the BaseQueryTranslator class. <br><br>StixToQuery calls out to the ANTLR parser, which returns a parsing of the STIX pattern. The parsing is then passed onto the query_constructor.py where it is translated into the native data source query. |
| transformers.py         | This file is used to transform data formats as required by STIX and the native data source query language.                                                                                                                                                                                                 |
| MANIFEST.in             | This file is used by Python when packaging the library.                                                                                                                                                                                                                                                    |

[Back to top](#create-a-translation-module)

#### Step 2. Rename the dummy translator file

- In your `abc` translation module folder, rename the `dummy_translator.py` file to [module_name]\_translator.py.
- The [module_name] must match the name that you assigned to your module folder in step 1. For example, `abc_translator.py`.

  When STIX-shifter is used to translate to or from STIX, the data source name is passed in as an argument. This argument is used to determine which module and files to use. If the name of the translator doesn't match the name of the module, an error occurs when the new translation module is used.

  ![dummy-translator.py file](./images/dummy-translator.py.png)

[Back to top](#create-a-translation-module)

#### Step 3. Edit the from_stix_map JSON file

The `from_stix_map.json` file is where you define HOW to translate a STIX pattern to a native data source query. STIX patterns are expressions that represent Cyber Observable objects. The mapping of STIX objects and properties to data source fields determine how a STIX pattern is translated to a data source query. 


1. Identify your data source fields.
2. Refer to the following documentation [STIX™ Version 2.0. Part 4: Cyber Observable Objects](http://docs.oasis-open.org/cti/stix/v2.0/stix-v2.0-part4-cyber-observable-objects.html) for the list of STIX objects that you can map your data source fields.
3. In your `abc` translation module folder, go to your json/ subfolder and edit the `from_stix_map.json` file. The `from_stix_map.json` file contains a sample mapping of STIX objects and properties to data source fields in the following format:
   ```
   {
       "stix-object": {
           "fields": {
               "stix_object_property": ["DataSourceField", "DataSourceField"],
               "stix_object_property": ["DataSourceField"]
           }
       }
   }
   ```
4. Map your data source fields to a STIX object and property. Define the mapping based on the specified format. You can map multiple data source fields to the same STIX object property.
   - "stix-object" refer to a STIX cyber observable object type name
   - "stix_object_property" refers to a STIX cyber observable object property name

**Example mapping**

The following example illustrates the mapping of STIX objects (network-traffic, ipv4-addr, and url) to a data source with the fields – SourcePort, DestinationPort, StartTime, EndTime, NetworkProtocol, SourceIpV4, DestinationIpV4, and Url.

```
{
    "network-traffic": {
        "fields": {
          "src_port": ["SourcePort"],
          "dst_port": ["DestinationPort"],
          "start": ["StartTime"],
          "end": ["EndTime"],
          "protocols[*]": ["NetworkProtocol"]
        }
      },
      "ipv4-addr": {
        "fields": {
          "value": ["SourceIpV4", "DestinationIpV4"]
        }
      },
      "url": {
          "fields": {
              "value": ["Url"]
          }
      }
}
```

The following STIX pattern is supported in the example mapping because the STIX objects (network-traffic and ipv4-addr) and their properties are defined in the file and mapped to data source fields.

```
"[network-traffic:src_port = 12345 AND ipv4-addr:value = '00-00-5E-00-53-00']"
```

**Avoiding Custom STIX Properties**

As shown below in [Step 5](#step-5-edit-the-to_stix_map-json-file), custom objects and properties are supported by the STIX standard and can be used when converting data source results to STIX. However, ISC uses standard STIX patterns when querying data sources, so it is recommended to stick to standard objects and attributes (as outlined in the STIX [documentation](http://docs.oasis-open.org/cti/stix/v2.0/stix-v2.0-part4-cyber-observable-objects.html)) when constructing the `from_stix_map`.  

[Back to top](#create-a-translation-module)

#### Step 4. Edit the query constructor file

When a STIX pattern is translated by STIX-shifter, it is first parsed with ANTLR 4 into nested expression objects. The native data source query is constructed from these nested objects.

The following STIX pattern:

```
"[network-traffic:src_port = 37020 AND network-traffic:dst_port = 635] START '2016-06-01T00:00:00Z' STOP '2016-06-01T01:11:11Z'"
```

Translates into the following ANTLR parsing:

```
Pattern[
    ObservationExpression(
        CombinedComparisonExpression(
            ComparisonExpression(
                network-traffic:dst_port ComparisonComparators.Equal 635
            )
            ComparisonExpressionOperators.And
            ComparisonExpression(
                network-traffic:src_port ComparisonComparators.Equal 37020
            )
        )
    )
    Qualifier(
        STARTt'2016-06-01T00:00:00Z'STOPt'2016-06-01T01:11:11Z'
    )
]
```

The parsing is recursively run through QueryStringPatternTranslator.\_parse_expression, which is found in `query_constructor.py`.

The `query_constructor.py` file is where the native query is built from the ANTLR parsing.

---
#### How STIX-shifter handles unmapped STIX properties

If a STIX pattern contains an unmapped property, and any joining operators allow for it, that portion of the parsing is removed from the ANTLR objects. The modified ANTLR parsing is then transformed into one or more native queries by the query constructor. Looking at the following examples:

`[stix_object:unmapped_property OR stix_object:mapped_property]`

*The unmapped property would be removed since it is joined to a mapped property with an OR operator.*

`[stix_object:unmapped_property] OR [stix_object:mapped_property]`

*The entire observation object (square brackets) containing the unmapped property would be removed since the pattern contains at least one other observation with mapped properties.*

If the unmapped property cannot be removed, STIX-shifter produces an error. This happens because the `QueryStringPatternTranslator` class (in `query_constructor.py`) does not know what data source field the STIX object property must be converted to. The following patterns would produce such an error:

`[stix_object:unmapped_property AND stix_object:mapped_property]`

*The unmapped property cannot be removed without changing the query logic since the two properties are joined by an AND operator.*

`[stix_object:unmapped_property]`

*The pattern only contains one observation with one unmapped property; nothing would be left to the query after removing it.*

---

In your `abc` translation module folder, edit the `query_constructor.py` file. Update the following sections based on the requirements of your data source.

##### 1. Define the comparator_lookup mapping

The comparator_lookup maps the STIX pattern operators to the data source query operators. Change the comparator values to match the operators supported in your data source.

The default operators that are defined in your translation module are the ones that are used in an SQL query.

![Comparator lookup mapping](./images/comparator-lookup-mapping.png)

| STIX pattern operators                           | Data source query operators |
| ------------------------------------------------ | --------------------------- |
| ComparisonExpressionOperators.And                | And                         |
| ComparisonExpressionOperators.Or                 | OR                          |
| ComparisonExpressionOperators.GreaterThan        | >                           |
| ComparisonExpressionOperators.GreaterThanOrEqual | >=                          |
| ComparisonExpressionOperators.LessThan           | <                           |
| ComparisonComparators.LessThanOrEqual            | <=                          |
| ComparisonComparators.Equal                      | =                           |
| ComparisonComparators.NotEqual                   | !=                          |
| ComparisonComparators.Like                       | LIKE                        |
| ComparisonComparators.In                         | IN                          |
| ComparisonComparators.Matches                    | LIKE                        |

##### 2. Define the \_parse_expression method

The ANTLR parsing is recursively run through the \_parse_expression method. The type of expression is determined on each iteration. When the expression is a ComparisonExpression, a query string is added to the final data source query.

This image illustrates where the query string is constructed for the data source query.

![Parse expression method](./images/parse-expression-method.png)

The following ComparisonExpression from an ANTLR parsing:

```
ComparisonExpression(
   network-traffic:src_port ComparisonComparators.Equal 37020
)
```

Would add the following string to the native query:
`"SourcePort = 37020"`

##### 3. Define the final query that gets returned in the translate_pattern method

Depending on your data source, edit this section to:

- Add a query field selector.
- Append result limits and time windows.
- Return an array of queries or a single query string. A single query string is returned by default, but queries can be split into an array of query strings if required.

[Back to top](#create-a-translation-module)

#### Step 5. Edit the to_stix_map JSON file

The `to_stix_map.json` file is where you define HOW to translate data source query results into a bundle of STIX objects. Query results must be in JSON format; otherwise, the data source cannot be supported.

Results from unmapped data source fields are ignored during translation and are not included in the bundle.

1. Identify your data source fields.
2. Refer to the following documentation [STIX™ Version 2.0. Part 4: Cyber Observable Objects](http://docs.oasis-open.org/cti/stix/v2.0/stix-v2.0-part4-cyber-observable-objects.html) for the list of STIX objects that you can map your data source fields.
3. In your `abc` translation module folder, go to your json/ subfolder and edit the `to_stix_map.json` file. The `to_stix_map.json` file contains a sample mapping of data source fields to STIX objects and properties in the following format:

   ```
   {
       "DataSourceField": {
           "key": "stix-object.stix_object_property"
       },
       "DataSourceField": {
           "key": "x_custom_object.property",
           "cybox": false
       }
   }
   ```

4. Each JSON object in the mapping has a "key" element with a value that represents a STIX object and its property. Define the mapping based on the specified format.
   - `stix-object` refer to a STIX cyber observable object type name
   - `stix_object_property` refers to a STIX cyber observable object property name
   - `x_custom_object.property` refers to a custom object and its property that you can use for fields that don't map to any STIX objects
   - Mappings for custom properties must have a `cybox` key set to false. This setting identifies custom objects during the translation process.

**Example mapping**
Using the same data source as in step 3, the following example shows a to-STIX mapping:

```
{
    "Url": {
        "key": "url.value"
    },
    "SourcePort": {
        "key": "network-traffic.src_port",
        "object": "nt",
        "transformer": "ToInteger"
    },
    "DestinationPort": {
        "key": "network-traffic.dst_port",
        "object": "nt",
        "transformer": "ToInteger"
    },
    "SourceIpV4": [
        {
          "key": "ipv4-addr.value",
          "object": "src_ip"
        },
        {
          "key": "network-traffic.src_ref",
          "object": "nt",
          "references": "src_ip"
        }
      ],
    "DestinationIpV4": [
        {
            "key": "ipv4-addr.value",
            "object": "dst_ip"
        },
        {
            "key": "network-traffic.dst_ref",
            "object": "nt",
            "references": "dst_ip"
        }
    ],
    "NetworkProtocol": {
        "key": "network-traffic.protocols",
        "object": "nt",
        "transformer": "ToLowercaseArray"
    },
    "LogSourceId": {
        "key": "x_my_data_source.log_source",
        "cybox": false
    },
    "EventTime": [
        {
            "key": "created",
            "cybox": false
        },
        {
            "key": "modified",
            "cybox": false
        },
        {
            "key": "first_observed",
            "cybox": false
        },
        {
            "key": "last_observed",
            "cybox": false
        }
    ]
}
```

**About the example mapping**

- Url is a simple mapping.
- SourcePort and DestinationPort
  - Have matching "object" values, which cause the src_port and dst_port to be added to the same object (in this case, network-traffic).
  - Uses the ToInteger transformer. Transformers are optional mapping attributes that apply a transformation method to the data before it is written to the STIX object. The existing transform methods are in `stix_shifter/stix_translation/src/transformers.py`. Any new transformers must be added to this file.
- SourceIpV4 and DestinationIpV4 contain two objects.
  - The first object creates an ipv4-addr object for each of the values. Given the field, the "object" property is set to either src_ip or dst_ip.
  - The second object in the mapping adds references in the network-traffic object to the ipv4-addr objects. Since the second part of the mappings has the object set to "nt", the references are added to the same network-traffic object that contains the source and destination ports.
- NetworkProtocol
  - Mapped similarly to the source and destination ports.
  - Note the use of the ToLowercaseArray transformer. The example data source returns a single string in the NetworkProtocol field. However, in STIX, network-traffic protocols store an array of protocols in lowercase format.
- LogSourceId
  - An example of a custom STIX property.
  - Custom properties allow for data that would not fit in any existing STIX object type to be added to the observed-data object. Custom properties must start with an x\_. In this example, the data source name is used as the custom object name and log_source is the custom property.
- EventTime
  - Data source field indicating the time of the event.
  - Maps to the following STIX fields: created, modified, first_observed, last_observed

**Example observed-data STIX object**

**Input data**

| Url             | SourcePort | DestinationPort | SourceIpV4 | DestinationIpV4 | NetworkProtocol | LogSourceId | EventTime                |
| --------------- | ---------- | --------------- | ---------- | --------------- | --------------- | ----------- | ------------------------ |
| www.example.com | 3000       | 1000            | 192.0.2.0  | 198.51.100.0    | TCP             | 678         | 2019-04-24T12:44:00.605Z |

**Output**

The following illustrates an observed-data STIX object that is derived from the previous example mapping and sample input data.

```
{
      "id": "observed-data--6ecb744f-37d2-4950-a7bb-9dc821679c52",
      "type": "observed-data",
      "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
      "created": "2019-04-24T12:44:00.605Z",
      "first_observed": "2019-04-24T12:44:00.605Z",
      "last_observed": "2019-04-24T12:44:00.605Z",
      "modified": "2019-04-24T12:44:00.605Z",
      "number_observed": 1,
      "objects": {
        "0": {
          "type": "ipv4-addr",
          "value": "192.0.2.0"
        },
        "1": {
          "type": "network-traffic",
          "src_ref": "0",
          "src_port": 3000,
          "dst_ref": "2",
          "dst_port": 1000
        },
        "2": {
          "type": "ipv4-addr",
          "value": "198.51.100.0"
        },
        "3": {
          "type": "url",
          "value": "www.example.com"
        }
      },
      "x_my_data_source": {
        "log_source": 678
      }
    }
```

**Required fields:**

Every STIX observed-data object must include the following fields: id, type, created_by_ref, created, modified, first_observed, last_observed, and number_observed.

The code for translating data source results to STIX is found in `stix_shifter/stix_translation/src/json_to_stix/json_to_stix_translator.py`. Normally, there is no need to edit this file.

[Back to top](#create-a-translation-module)

#### Step 6. If required by your data source, update the transformers file

The `transformers.py` file contains classes that transform data formats. Each class has a method that takes in data and transforms it into the preferred format. For example, an integer value is transformed into a string. These classes can be used in cases such as:

- When converting from STIX, the data source query language requires specific data formats. For example, time stamps. In this case, the format of a value in the STIX pattern must be transformed during pattern translation if the STIX and query language data formats are different.
- When converting to STIX, the STIX object requires specific data formats. In this case, the format of a value that is returned in the data source results must be transformed during translation into a bundle of STIX objects. See [STIX™ Version 2.0. Part 4: Cyber Observable Objects](http://docs.oasis-open.org/cti/stix/v2.0/stix-v2.0-part4-cyber-observable-objects.html) for STIX data formats.

[Back to top](#create-a-translation-module)

#### Step 7. Update the MANIFEST file to include the path to the json mapping folder

The `MANIFEST.in` file is required by Python so that the new mapping files can be found when STIX-shifter is packaged.

[Back to top](#create-a-translation-module)

#### Step 8. Verify that the translation module was created successfully

You must have access to the data source either through a UI or CLI so that you can run the translated query and confirm that it works.
The translation module can be tested by calling the `main.py file` from the command line and passing in the required arguments. The order of arguments is as follows:

```
python main.py translate <data source (module) name> <"query" or "result"> <STIX identity object> <pattern or JSON results to
be translated> <options>
```

##### Test the STIX pattern to data source query translation

1. Run the translation module from the command line. For example, using abc as a data source:

```
python main.py translate abc query '{}' "[network-traffic:src_port = 37020 and network-traffic:dst_port = 635] OR [ipv4-addr:value = '333.333.333.0'] AND [url:value = 'www.example.com'] START t'2019-01-28T12:24:01.009Z' STOP t'2019-01-28T12:54:01.009Z'"
```

To run validation on the STIX pattern, add `'{"validate_pattern": "true"}'` as an option to the end of the CLI command:
```
python main.py translate abc query '{}' "[network-traffic:src_port = 37020 and network-traffic:dst_port = 635] OR [ipv4-addr:value = '333.333.333.0'] AND [url:value = 'www.example.com'] START t'2019-01-28T12:24:01.009Z' STOP t'2019-01-28T12:54:01.009Z'" '{"validate_pattern": "true"}'
```

2. Visually verify the returned query by running it against the data source.

##### Test the JSON data source results to STIX translation

1. Run the translation module from the command line. For example, using abc as a data source:

```
python main.py translate abc results '{"type": "identity","id": "identity--f431f809-377b-45e0-aa1c-
6a4751cae5ff","name": "abc","identity_class": "events"}' '[{"Url": "www.example.com", "SourcePort": 3000, "DestinationPort": 1000, "SourceIpV4": "192.0.2.0", "DestinationIpV4": "198.51.100.0", "NetworkProtocol": "TCP"}]'
```

2. Visually verify that all expected data is in the returned STIX bundle. If a data source field in your sample results is mapped in `to_stix_map.json`, the value must be in the STIX bundle under the mapped STIX property.

**Note:**

- The `<STIX identity object>` represents a data source and is the first observed-data object that gets added to the STIX bundle during results translation.
- Each observed-data object, which gets added to the bundle, references the `<STIX identity object>` to indicate which data source the result came from.
- The `<STIX identity object>` is only used when translating data source results to STIX. As such, an empty JSON object can be passed in when converting a STIX pattern to a data source query.
- For more information about identity objects, see the [STIX 2 documentation](http://docs.oasis-open.org/cti/stix/v2.0/cs01/part2-stix-objects/stix-v2.0-cs01-part2-stix-objects.html#_Toc496714310).

[Back to top](#create-a-translation-module)

### Create a Transmission module

{: #transmission-mod}

1. [Create a transmission module folder](#step-1-create-a-transmission-module-folder)
1. [Edit the apiclient.py file](#step-2-edit-the-apiclient-file)
1. [Edit the dummy_connector.py file](#step-3-edit-the-dummy-connector-file)
1. [Verify that the transmission module was created successfully](#step-4-verify-that-the-transmission-module-was-created-successfully)

#### Step 1. Create a transmission module folder

1. Go to `stix_shifter/stix_transmission/src/modules/`.
2. Copy the `async_dummy` or `synchronous_dummy` folder, whichever is appropriate for your data source, based on the data source API.

   These dummy folders are templates to help you get started quickly. They contain the necessary files that your transmission module needs. You need to customize it based on your data source.

3. Rename your `async_dummy` or `synchronous_dummy` transmission module folder to match the name of your data source. It must match the same name that you assigned for your translation module. For example, abc.

   The data source name is used as an argument when either translation or transmission is called. This argument is used throughout the project so that STIX-shifter knows which modules to use.

   **Note:** The translation and transmission modules must have the same name.

4. Verify that your transmission module folder contains the following folders and files.

   For an asynchronous transmission module, you must have the following files:

   | Folder/file              | Why is it important? Where is it used?                                  |
   | ------------------------ | ----------------------------------------------------------------------- |
   | **init**.py              | This file is required by Python to properly handle library directories. |
   | apiclient.py             |
   | async_dummy_connector.py |

   For a synchronous transmission module, you must have the following files:

   | Folder/file                    | Why is it important? Where is it used?                                  |
   | ------------------------------ | ----------------------------------------------------------------------- |
   | **init**.py                    | This file is required by Python to properly handle library directories. |
   | synchronous_dummy_connector.py |

[Back to top](#create-a-transmission-module)

#### Step 2. Edit the apiclient file

You can implement an API client for an asynchronous or a synchronous data source. If your data source has a simpler way of calling the APIs, you don’t need an API client and you can skip this step.

Edit the `apiclient.py` file's APIClient class to include the methods to call your data source' APIs. Each method calls out to the relevant API.

- At a minimum, methods must be implemented for:
  - Pinging the data source
  - Creating a search; sending a query to the data source
  - Checking the status of a search (only used for asynchronous data sources)
  - Retrieving search results (only used for asynchronous data sources)
- You can add methods for the following and others, if supported by your data source:
  - Updating a search
  - Deleting a search

[Back to top](#create-a-transmission-module)

#### Step 3. Edit the dummy connector file

1. In your abc transmission module folder, rename the `async_dummy_connector.py` file or `synchronous_dummy_connector.py` file to <module_name>\_connector.py.

   The `dummy_connector.py` file contains the Connector class, which gets instantiated when the transmission module is invoked. The Connector class contains all the methods that call out to the data source API through the API client.

   The <module_name> must match the name that you assigned to your module folder in step 1. For example, abc_connector.py.

   When STIX-shifter uses a transmission module to connect to a data source, the data source name is passed in as an argument. This argument is used to determine which module and files to use. If the argument name doesn't match the name of the module, an error occurs when the new transmission module is used.

2. Edit the `abc_connector.py` file's Connector(BaseConnector) class to include the methods to run each of the API client methods.

   - Change each method implementation as needed. Keep method names and signatures as they are.
   - You can add the methods in the same file or create individual files for each.
   - At a minimum, methods must be implemented for:

     - ping
     - create_query_connection (only used for asynchronous data sources)
     - create_status_connection (only used for asynchronous data sources)
     - create_results_connection

       **Note:** The data source results need to be in JSON format before they are converted into STIX. If the results are not returned as JSON, the create_results_connection is one place where any needed JSON conversion might take place.

   - You can add other methods, if supported by your data source. For example, delete_query_connection.

**Note on synchronous data sources**

For synchronous data sources, the query is sent to the API from the create_results_connection method. The query is sent, and the results are received in the same step. Although create_query_connection, and create_status_connection are not technically used, they still get called by UDS during the transmission execution and must be implemented as follows:

_Create Query Connection_

```
def create_query_connection(self, query):
      return { "success": True, "search_id": query }
```

_Create Status Connection_

```
def create_status_connection(self, search_id):
      return {"success": True, "status": "COMPLETED", "progress": 100}
```

For asynchronous sources, the search id that gets passed into the connection methods is a UUID. This is used to keep track of the original query, allowing the status and results to be fetched. However, in the case a synchronous data source, the query is sent and the results are returned in the same action. Therefore, the search id in this case is not a UUID but the search query itself.

[Back to top](#create-a-transmission-module)

#### Step 4. Verify that the transmission module was created successfully

1. You must have:

   - Authentication credentials to connect to the data source.
   - A private key and certificate for the cert.

   Authentication depends on the data source and can be:

   ```
   '{"auth": {"username": "<username>","password": "<password>"}}' or
   '{"auth": {"SEC":"<SEC TOKEN>"}}'
   ```

2. Test the transmission ping method.

   1. Use the following CLI command:

      ```
      python main.py transmit abc '{"host":"<IP address or URL to data source>", "port":"<port number>", "cert":
      "-----BEGIN PRIVATE KEY-----<private key>-----END PRIVATE KEY-----\n-----BEGIN CERTIFICATE-----<certificate>-----END CERTIFICATE-----\n"}' '{"auth": <authentication object>}' ping
      ```

   2. Visually confirm that a result comes back with
      ```
      {'success': True}
      ```

3. Test the transmission is_async method.

   1. Use the following CLI command:
      ```
      python main.py transmit abc '{"host":"<IP address or URL to data source>", "port":"<port number>", "cert":
      "-----BEGIN PRIVATE KEY-----<private key>-----END PRIVATE KEY-----\n-----BEGIN CERTIFICATE-----<certificate>-----END CERTIFICATE-----\n"}' '{"auth{"auth": <authentication object>}' is_async
      ```
   2. Visually confirm that it returns true if the data source is asynchronous. Otherwise, it must return false.

4. Test the transmission query method.

   1. Use the following CLI command:

      ```
      python main.py transmit abc '{"host":"<IP address or URL to data source>", "port":"<port number>", "cert":
      "-----BEGIN PRIVATE KEY-----<private key>-----END PRIVATE KEY-----\n-----BEGIN CERTIFICATE-----<certificate>-----END CERTIFICATE-----\n"}' '{"auth": <authentication object>}' query "<Native data source Query String>"
      ```

   2. Visually confirm that a result comes back with

      ```
      {'success': True, 'search_id': '<some query UUID>'}
      ```

   3. Take note of the UUID that is returned. It is the ID to use in the rest of the tests.

5. Test the transmission status method.

   1. Use the following CLI command:

      ```
      python main.py transmit abc '{"host":"<IP address or URL to data source>", "port":"<port number>", "cert":
      "-----BEGIN PRIVATE KEY-----<private key>-----END PRIVATE KEY-----\n-----BEGIN CERTIFICATE-----<certificate>-----END CERTIFICATE-----\n"}' '{"auth{"auth": <authentication object>}' status "<Query UUID from test 4>"
      ```

   2. Visually confirm that a result comes back with
      ```
      {'success': True, 'status': 'COMPLETED', 'progress': 100}
      ```

6. Test the transmission results method.

   1. Use the following CLI command:

      ```
      python main.py transmit abc '{"host":"<IP address or URL to data source>", "port":"<port number>", "cert":
      "-----BEGIN PRIVATE KEY-----<private key>-----END PRIVATE KEY-----\n-----BEGIN CERTIFICATE-----<certificate>-----END CERTIFICATE-----\n"}' '{"auth{"auth": <authentication object>}' results "<Query UUID from test 4>" <Offset Integer> <Length Integer>
      ```

   2. You can set the offset and length command line arguments to 1.
   3. Visually confirm that query results are returned as JSON objects. These results can be compared to what is returned when running the query string used in test C directly on the data source API, either through a UI or the CLI.

7. Test the transmission delete method if the data source supports it.

   1. Use the following CLI command:

      ```
      python main.py transmit abc '{"host":"<IP address or URL to data source>", "port":"<port number>", "cert":
      "-----BEGIN PRIVATE KEY-----<private key>-----END PRIVATE KEY-----\n-----BEGIN CERTIFICATE-----<certificate>-----END CERTIFICATE-----\n"}' '{"auth": <authentication object>}' delete "<Query UUID from test 4>"
      ```

   2. Visually confirm that a result comes back with
      ```
      {'success': True}
      ```
