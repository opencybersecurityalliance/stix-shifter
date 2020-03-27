# Configuration paramaters

A json file needs to be created that contains configuration paramters for each module. Configuration json file is required in order to validate the module specific parameters for a successful translation and tranmission call. Please follow this naming convention when you create the file: `<module name>_config.json`

A second json file is required to translate the parameters mention in `<module name>_lang.json` for the UI. This file is necessary in order to help the UI framework to show the parameters in human readable format.

## File Location

Create a directory named `configuration` in your module folder. The json files mentioned above needs to be created inside `configuration`. Make sure json files saved in the following location for your new module-

```
/stix_shifter_modules/<module name>/configuration
```

## JSON File description

### config json file

Two top level json object needs to be preset in the file `connection` and `configuration`. The child attributes of `connection` object should be the parameters required for making api call which can be used by multiple user and role level. `configuration` object should contain the parameters that are required for api authentication for individual user and role. 

Following example json contains the appropriate parameters that each module requires-

```
{
    "connection": {
        "type": {
            "default": "QRadar"
        },
        "host": {
            "type": "text"
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

Each parameter in both connection and configuration object can also have few different child attribute to define the paramatere functionality. Below are the attributes that can be specified at least one or more based on the parameter funciton-

1. type
    - Following types can be specified for the parameters(more can be added based on module requirements):
        - text
        - number
        - password
2. default
    - Any value that needs to be default for the parameter
3. min
    - Minmum value for the parameter. If the type is text than it is the minimum number of character in the value.
4. max
    - Maximum value for the parameter. If the type is text than it is the maximum number of character in the value.
5. optional
    - Set this value to "true" if the parameter is optional. By default the value is "false" if not mentioned
6. hidden
    - Set this value to "true" if the parameter needs to be hidden by the UI. By default the value is "false" if not mentioned

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

Both connection and configuration object may contain more or different parameters than that are mentioned in the example above based on the individual module. 

### lang json file

The `<module name>_lang.json` file has the similar format like `<module name>_config.json`. It has different child attributes to translate the files for UI framework.

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
            "description": "Specify the IP address or  hostname of the data source so that IBM Cloud Pak for Security can communicate with it"
        },
        "port": {
            "label": "Host Port",
            "description": "Set the port number that is associated with the Host name or IP"
        },
        "help": {
            "label": "Help",
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

For easier implementation, you can copy the json files from dummy modules (async_dummy or synchornous_dummy) and modify according the module requirements. You can also review the existing module configuration json files to reference. 