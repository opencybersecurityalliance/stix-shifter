# Connector Coding Lab

This is a hands-on lab to start implementing a connector module in STIX-shifter from scratch. The main purpose of this lab is to get an experience of developing a functional connector. You will basically recreate an already existing connector. We will mostly copy and paste required code blocks and functions. We chose the MySQL connector since its coding complexity is simpler than most of the existing connectors. 


## Prerequisites

* Github account
* Basic knowledge of Git such as forking, committing, branching, pulling, and merging
* Working knowledge of the Python programming language. This lab will work with Python 3.8 or greater.
* An IDE to write Python code, such as VS Code.
* Knowledge of the data source API that includes API request, response, datatype and schema.
* Knowledge of STIX 2.0. To learn about STIX Cyber Observable Objects, see the [STIX 2.0](https://docs.oasis-open.org/cti/stix/v2.0/stix-v2.0-part4-cyber-observable-objects.html) specification.
## Steps

### 1. Open stix-shifter folder in the VS Code IDE
### 2. Open a terminal in VS code
### 3. Make sure you are in the `stix-shifter/` parent directory
### 4. Create a python virtual environment

```
virtualenv -p python3 virtualenv && source virtualenv/bin/activate
python3 -m pip install --upgrade pip
INSTALL_REQUIREMENTS_ONLY=1 python3 setup.py install
```

### 5. Make a copy of the `stix_shifter_modules/demo_template` module
### 6. Change the name to `lab_connector`   
    
* You should now have a connector module skeleton for the new connector named `lab_connector`

### 7. Create the module entry points

* Implement the `EntryPoint()` class in `stix_shifter_modules/lab_connector/entry_point.py`. 
* The EntryPoint class acts as a gateway to the various methods used by the translation and transmission classes.

```
from stix_shifter_utils.utils.base_entry_point import BaseEntryPoint

class EntryPoint(BaseEntryPoint):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(connection, configuration, options)
        self.set_async(False)
        if connection:
            self.setup_transmission_basic(connection, configuration)
        self.setup_translation_simple(dialect_default='default')
```

### 8. Implement input configuration of the connector in `stix_shifter_modules/lab_connector/configuration`

* A json file needs to be created that contains configuration parameters for each module. The configuration json file is required in order to validate the module specific parameters for a successful translation and transmission call. Please follow this naming convention when you create the file: config.json. 
* Two top level json objects needs to be preset in the file: `connection` and `configuration`.
* The child attributes of the connection object should be the parameters required for making API calls which can be used by multiple users and role levels.
* Here's an example of the connection object:

```
"connection": {
        "type": {
            "displayName": "Lab Connector"
        },
        "host": {
            "type": "text",
            "regex": "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\\-]*[a-zA-Z0-9])\\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\\-]*[A-Za-z0-9])$"
        },
        "port": {
            "type": "number",
            "default": 3306,
            "min": 1,
            "max": 65535
        },
        "database": {
            "type": "text"
        },
        "help": {
            "type": "link",
        },
        "options": {
            "table": {
                "type": "text",
                "optional": false
            }
        }
    }
```

* The configuration object should contain the parameters that are required for API authentication for individual users and roles.
* Here's an example of the configuration object:

```
"configuration": {
        "auth": {
            "type" : "fields",
            "username": {
                "type": "password"
            },
            "password": {
                "type": "password"
            }
        }
    }
```

* For this lab, copy the entire content from https://raw.githubusercontent.com/opencybersecurityalliance/stix-shifter/develop/stix_shifter_modules/mysql/configuration/config.json.

* A second JSON file is required to translate the parameters defined in `config.json` for the UI. This file is necessary in order to help the UI framework show the parameters in human-readable format. For english language, create a file named `lang_en.json`. 

Here's an example of the content of a `lang_en.json` file:

```
"configuration": {
        "auth": {
            "username": {
                "label": "Username",
                "description": "Username with access to the database"
            },
            "password": {
                "label": "Password",
                "description": "Password of the user with access to the database"
            }
        }
    }
```

* For this lab, copy the entire content from https://raw.githubusercontent.com/opencybersecurityalliance/stix-shifter/develop/stix_shifter_modules/mysql/configuration/lang_en.json.

**Note** For more details about the configuration JSON, go to [Configuration JSON](https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/adapter-guide/develop-configuration-json.md)

### 9. Implement stix to query translation

* Go to `stix_shifter_modules/lab_connector/stix_translation`

* Edit the from_stix_map(`from_stix_map.json`) JSON files
    * `from_stix_map.json` file contains STIX Objects to datasource fields  mapping.
    * The mapping of STIX objects and properties to data source fields determine how a STIX pattern is translated to a data source query.
    * Update `stix_shifter_modules/lab_connector/stix_translation/json/from_stix_map.json` file with the content of https://raw.githubusercontent.com/opencybersecurityalliance/stix-shifter/develop/stix_shifter_modules/mysql/stix_translation/json/from_stix_map.json

    ***Note:*** If the data source API offers more than one schema type then the dialect prefix can be added. For example: `dialect1_from_stix_map.json`

* Edit the `operators.json` file:
    * The operators.json file maps the STIX pattern operators to the data source query operators. Change the comparator values to match the operators supported in your data source.
    * Update `stix_shifter_modules/lab_connector/stix_translation/json/operators.json` with the content of https://raw.githubusercontent.com/opencybersecurityalliance/stix-shifter/develop/stix_shifter_modules/mysql/stix_translation/json/operators.json

* The `QueryTranslator()` class can be left as is `stix_shifter_modules/mysql/stix_translation/query_translator.py`
* Edit the query constructor file:
    * When a STIX pattern is translated by STIX-shifter, it is first parsed with ANTLR 4 into nested expression objects. The native data source query is constructed from these nested objects.
    * The parsing is recursively run through `QueryStringPatternTranslator._parse_expression`, which is found in `query_constructor.py`.
    * The `query_constructor.py` file is where the native query is built from the ANTLR parsing.
    * Update `stix_shifter_modules/lab_connector/stix_translation/query_constructor.py` with the content of https://raw.githubusercontent.com/opencybersecurityalliance/stix-shifter/develop/stix_shifter_modules/mysql/stix_translation/query_constructor.py

**Test the query translation command using the CLI tool**

```
python main.py translate lab_connector query {} "[ipv4-addr:value = '127.0.0.1'] START t'2022-07-01T00:00:00.000Z' STOP t'2022-07-27T00:05:00.000Z'" '{"table":"demo_db"}'
```

### 10. Implement stix transmission module. 

* You need to implement four functionalities of the transmission module which are `ping`, `query`, `status` and `results`. 
* First create a class called `APIClient()` in `stix_shifter_modules/lab_connector/stix_transmission/api_client.py`. This is where you initialize the connection and configurations needed for the data source API requests. This class also includes the utility functions needed for the major functionalities of the connector. Add the following code to the top of the API client:

```
import mysql.connector
from mysql.connector import errorcode


class APIClient():

    def __init__(self, connection, configuration):
        auth = configuration.get('auth')
        self.user = auth.get('username')
        self.password = auth.get('password')
        self.timeout = connection['options'].get('timeout')
        self.result_limit = connection['options'].get('result_limit')
        self.host = connection.get("host")
        self.database = connection.get("database")
        self.table = connection['options'].get("table")
        self.port = connection.get("port")
        self.auth_plugin = 'mysql_native_password'
```

* Create a file called `connector.py` if it doesn't yet exist, and add the following code to the top of the file:

```
import datetime
import json
from stix_shifter_utils.modules.base.stix_transmission.base_json_sync_connector import BaseJsonSyncConnector
from .api_client import APIClient
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger


class Connector(BaseJsonSyncConnector):

    def __init__(self, connection, configuration):
        self.api_client = APIClient(connection, configuration)
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]
```
* Now we can add the required transmission functions

### Ping

* Define and implement a function named `ping_connection(self)` inside `stix_shifter_modules/lab_connector/stix_transmission/connector.py` 

```
def ping_connection(self):
    response = self.api_client.ping_data_source()
    response_code = response.get('code')
    response_txt = response.get('message')
    return_obj = dict()
    return_obj['success'] = False

    if len(response) > 0 and response_code == 200:
        return_obj['success'] = True
    else:
        ErrorResponder.fill_error(return_obj, response, ['message'], error=response_txt, connector=self.connector)
    return return_obj
```

* Define and implement the `ping_data_source()` function inside `APIClient()`:

```
def ping_data_source(self):
    # Pings the data source
    response = {"code": 200, "message": "All Good!"}
    try:
        cnx = mysql.connector.connect(user=self.user, password=self.password, 
                                        host=self.host, database=self.database, 
                                        port=self.port, auth_plugin=self.auth_plugin)  

    except mysql.connector.Error as err:
        response["code"] = err.errno

        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            response["message"] = "Something is wrong with your user name or password"
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            response["message"] = "Database does not exist"
        else:
            response["message"] = err
    else:
        cnx.close()
    return response
```

**Test the Ping command using the CLI tool**

```
python main.py transmit lab_connector '{"host": "localhost", "database":"demo_db", "options": {"table":"demo_table"}}' '{"auth": {"username":"root", "password":"Giv3@m@n@fish"}}' ping
```

### Query 

* As a synchronous connector, it doesn't require any API request to start or create the query. Therefore no need to define and implement the functions of the query function. The `self.setup_transmission_basic(connection, configuration)` statement inside entry point class `EntryPoint()` takes care of that automatically.

**Test the Query command using the CLI tool**

```
python main.py transmit lab_connector '{"host": "localhost", "database":"demo_db", "options": {"table":"demo_table"}}' '{"auth": {"username":"root", "password":"Giv3@m@n@fish"}}' query "SELECT * FROM demo_table WHERE source_ipaddr = '10.0.0.9'" 
```

### Status

* Same as query, a synchronous connector doesn't return any status from the data source so no action is needed.

**Test the Status command with the CLI tool**

```
python main.py transmit lab_connector '{"host": "localhost", "database":"demo_db", "options": {"table":"demo_table"}}' '{"auth": {"username":"root", "password":"Giv3@m@n@fish"}}' status "SELECT * FROM demo_table WHERE source_ipaddr = '10.0.0.9'" 
```

### Results

* Define and implement a function named `create_results_connection(self, query, offset, length)` inside `stix_shifter_modules/lab_connector/stix_transmission/connector.py`

```
def create_results_connection(self, query, offset, length):
    return_obj = dict()
    response = self.api_client.run_search(query, start=offset, rows=length)
    response_code = response.get('code')
    response_txt = response.get('message')
    if response_code == 200:
        return_obj['success'] = True
        return_obj['data'] = response.get('result')
    else:
        ErrorResponder.fill_error(return_obj, response, ['message'], error=response_txt, connector=self.connector)
    return return_obj
```

* Define and implement a function named `run_search(self, query, offset, length)`  in the `APIClient()` class.

* Copy the code block for the MySQL connector's `run_search` function https://github.com/opencybersecurityalliance/stix-shifter/blob/8ae2cf2a0196531b8e0daf8f5ff141b4251ec201/stix_shifter_modules/mysql/stix_transmission/api_client.py#L40

**Test the Results command using the CLI tool**

```
python main.py transmit lab_connector '{"host": "localhost", "database":"demo_db", "options": {"table":"demo_table"}}' '{"auth": {"username":"root", "password":"Giv3@m@n@fish"}}' results "SELECT * FROM demo_table WHERE source_ipaddr = '10.0.0.9'" 0 100
```

## Results Translation

### 11. Implement data source results to STIX translation
    
* Make sure the data source returns the results in JSON format
* Go to `stix_shifter_modules/lab_connector/stix_translation`
* Create a JSON file named `to_stix_map.json` that maps data source fields to STIX objects. 
* For this lab, update `stix_shifter_modules/lab_connector/stix_translation/json/to_stix_map.json` file with the content of https://raw.githubusercontent.com/opencybersecurityalliance/stix-shifter/develop/stix_shifter_modules/mysql/stix_translation/json/to_stix_map.json
* Implement the `ResultsTranslator(JSONToStix)` class in `results_translator.py`

```
from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import JSONToStix

class ResultsTranslator(JSONToStix):
    pass    
```
     
* The parent utility class `JSONToStix` automatically translates the results into STIX.

**Test the results translation command using the CLI tool**

```
python main.py translate mysql results '{ "type":"identity","id":"identity--20a77a37-911e-468f-a165-28da7d02985b", "name":"MySQL Database", "identity_class":"system", "created": "2022-04-07T20:35:41.042Z", "modified": "2022-04-07T20:35:41.042Z" }' '[ { "source_ipaddr": "10.0.0.9",  "dest_ipaddr": "10.0.0.9",  "url": "www.example.org",  "filename": "spreadsheet.doc",  "sha256hash": "b0795d1f264efa26bf464612a95bba710c10d3de594d888b6282c48f15690459",  "md5hash": "0a556fbb7d3c184fad0a625afccd2b62",  "file_path": "C:/PHOTOS",  "username": "root", "source_port": 143,  "dest_port": 8080,  "protocol": "udp",  "entry_time": 1617123877.0,  "system_name": "demo_system",  "severity": 2,  "magnitude": 1 } ]' '{"table":"demo_table"}'
```

### 12. Implement the `ErrorMapper()` class in `stix_shifter_modules/lab_connector/stix_transmission/error_mapper.py` 

* This is where you map any API specific error code messages for the return object. You can use the same error mapper content that is used in the MySQL connector: https://raw.githubusercontent.com/opencybersecurityalliance/stix-shifter/develop/stix_shifter_modules/mysql/stix_transmission/error_mapper.py

### 13. Add any data source specific dependency to the `stix_shifter_modules/lab_connector/requirements.txt`.  
* In this case add `mysql-connector-python==8.0.25`

### 14. The entire end-to-end query flow can now be tested with the CLI `execute` command:

```
python main.py execute lab_connector lab_connector '{"type": "identity","id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff","name": "mysql","identity_class": "system"}' '{"host": "localhost", "database":"demo_db", "options": {"table":"demo_table"}}' '{"auth": {"username":"root", "password":"Giv3@m@n@fish"}}' "[ipv4-addr:value = '10.0.0.9']"
```
