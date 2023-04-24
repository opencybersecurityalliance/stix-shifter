# Configuration Parameters

A json file needs to be created that contains configuration parameters for each module. The configuration json file is required in order to validate the module specific parameters for a successful translation and transmission call. Please follow this naming convention when you create the file: `config.json`

A second json file is required to translate the parameters defined in `lang_en.json` for the UI. This file is necessary in order to help the UI framework show the parameters in human readable format.

## File Location

Create a directory named `configuration` in your module folder. The json files mentioned above needs to be created inside `configuration`. Make sure json files saved in the following location for your new module-

```
/stix_shifter_modules/<module name>/configuration
```

## JSON File Description

### config json file

Two top level json objects needs to be preset in the file: `connection` and `configuration`. The child attributes of the `connection` object should be the parameters required for making API calls which can be used by multiple users and role levels. The `configuration` object should contain the parameters that are required for API authentication for individual users and roles. 

The following example JSON contains the appropriate parameters that each module requires:

```
{
    "connection": {
        "type": {
            "default": "QRadar",
            "group": "qradar"
        },
        "host": {
            "type": "text",
            "regex": "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\\-]*[a-zA-Z0-9])\\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\\-]*[A-Za-z0-9])$"
        },
        "port": {
            "default": 443,
            "type": "number"
        },
        "help": {
            "default": "<Help URL to configure datasource to make api call>",
            "type": "link"
        },
        "limit": {
            "default": 1000,
            "max": 10000,
            "type": "number"
        },
        "timeout": {
            "default": 1,
            "max": 60,
            "type": "number"
        },
        "cert": {
            "type": "password",
            "optional": true
        },
        "sni": {
            "type": "text",
            "optional": true
        },
        "selfSignedCert": {
            "type": "password",
            "optional": true
        }
    },
    "configuration": {
        "auth": {
            "sec": {
                "type": "password"
            }
        }
    }
}
```

Each parameter in both the connection and configuration object can also have few different child attributes to define the parameter functionality. Below are the attributes that can be specified at least one or more based on the parameter function:

1. type
    - The following types can be specified for the parameters (more can be added based on data source requirements):
        - text
        - number
        - password
        - boolean
2. default
    - The default value for the parameter
3. min
    - Minimum value for the parameter. If the type is text, then the value is the minimum number of characters in the value.
4. max
    - Maximum value for the parameter. If the type is text, then the value is the maximum number of characters in the value.
5. optional
    - Set this value to "true" if the parameter is optional. By default the value is "false" if not defined
6. hidden
    - Set this value to "true" if the parameter needs to be hidden by the UI. By default the value is "false" if not defined
7. regex
    - Regular expression pattern that defines what characters are permitted in the value.

Configuration object needs to have `auth` child object. `auth` object should contain the parameters that are needed for api authentication. We have put an example of qradar api authentication paramter in the above example. Here's another example of `auth` object-

```
"auth": {
    "username": {
        "type": "password"
    },
    "password": {
        "type": "password"
    }
}
```

Both connection and configuration object may contain more or different parameters than that are defined in the example above based on the individual module. 

### lang json file

The `lang_en.json` file has the similar format like `config.json`. It has different child attributes to translate the files for UI framework.

1. label
    - Label of the parameter that is visiable in the UI
2. placeholder
    - Any placeholder value that can be present in the user input field
3. description
    - Description of the parameter

Below example json is the language translation file of the above QRadar config json file:

```
{
    "connection": {
        "host": {
            "label": "Management IP address or Hostname",
            "placeholder": "192.168.1.10",
            "description": "Specify the IP address or hostname of the data source"
        },
        "port": {
            "label": "Host Port",
            "description": "Set the port number that is associated with the host name or IP address"
        },
        "help": {
            "label": "Need additional help?",
            "description": "More details on the datasource setting can be found in the specified link"
        },
        "limit": {
            "label": "Result Size Limit",
            "description": "The maximum number of entries or objects that are returned by search query.The default result size limit is 1000. The value must not be less than 1 and must not be greater than 10,000."
        },
        "timeout": {
            "label": "Query Timeout Limit",
            "description": "The time limit in minutes for how long the query is run on the data source. The default time limit is 1. When the value is set to zero, there is no timeout. If the query takes longer than 1 min, it is likely to indicate a problem."
        },
        "cert": {
            "label": "IBM QRadar Certificate",
            "description": "Use self-signed SSL certificate for QRadar V7.3.1 and CA content(root and intermediate) for QRadar V7.3.2"
        },
        "sni": {
            "label": "Server Name Indicator",
            "description": "The Server Name Indicator (SNI) enables a separate hostname to be provided for SSL authentication"
        }
    },
    "configuration": {
        "auth": {
            "sec": {
                "label": "Authentication Token",
                "description": "The Authentication Token is the unique identifier of the data source that you want to establish the connection with. It is required to authenticate the connection request."
            }
        }
    }
}
```

For easier implementation, you can copy the json files from template modules (async_template or synchronous_template) and modify according the module requirements. You can also review the configuration json files of existing modules for reference. 