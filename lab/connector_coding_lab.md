# Connector Coding Lab

This is a hands on lab to start implementing a connector module in STIX-shifter from scratch. The main purpose of this lab is to give developers experience developing a functional connector. You will basically recreate an already existing connector. We will mostly copy and paste required code blocks and functions. We chose the MySQL connector since its coding complexity is simpler than most of the existing connectors. 


## Prerequisites

1. Github account
2. Basic knowledge of Git such as forking, committing, branching, pulling, and merging
3. Working knowledge of the Python programming language. This lab will use Python 3.6
4. An IDE to write Python code, such as VS Code.

## Steps

1. Open stix-shifter folder in VS Code IDE
2. Open a terminal in VS code
3. Make sure you are in `stix-shifter/` parent directory
4. Create a python virtual environment
```
virtualenv -p python3 virtualenv && source virtualenv/bin/activate
INSTALL_REQUIREMENTS_ONLY=1 python3 setup.py install
```
5. Make a copy of `stix_shifter_modules/synchronous_template` module
6. Change the name to `lab_connector`   
    You should have connector module skeleton for the new connector name lab_connector
7. Implement `EntryPoint()` class in `stix_shifter_modules/lab_connector/entry_point.py`. 

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

8. Implement input configuration of the connector in `stix_shifter_modules/lab_connector/configuration`

    * Implement connection and configuration of the connector in config.json file. you can copy the content from https://raw.githubusercontent.com/opencybersecurityalliance/stix-shifter/develop/stix_shifter_modules/mysql/configuration/config.json for this lab
    
    * You can also implement the language definition of the input configuration for the UI label and description in lang_en.json(for English) file. you can copy the content from https://raw.githubusercontent.com/opencybersecurityalliance/stix-shifter/develop/stix_shifter_modules/mysql/configuration/lang_en.json for this lab.

9. Implement stix to query translation

    * Go to `stix_shifter_modules/lab_connector/stix_translation`

    * Update `stix_shifter_modules/lab_connector/stix_translation/json/from_stix_map.json` file with the content of https://raw.githubusercontent.com/opencybersecurityalliance/stix-shifter/develop/stix_shifter_modules/mysql/stix_translation/json/from_stix_map.json

    * If data source API offers one schema type the dialect prefix can be removed

    * Update `stix_shifter_modules/lab_connector/stix_translation/json/operators.json` with the content of https://raw.githubusercontent.com/opencybersecurityalliance/stix-shifter/develop/stix_shifter_modules/mysql/stix_translation/json/operators.json

    * QueryTranslator() class can be left as it `stix_shifter_modules/mysql/stix_translation/query_translator.py`
    * Update `stix_shifter_modules/lab_connector/stix_translation/query_constructor.py` with the content of https://raw.githubusercontent.com/opencybersecurityalliance/stix-shifter/develop/stix_shifter_modules/mysql/stix_translation/query_constructor.py

    * You can now run the basic query translation CLI command from your workspace to tests

10. Implement stix transmission module. 

    * You need to implement four functionalities of the transmission module which are `ping`, `query`, `status` and `results`. 
    * First step, create a class called `APIClient()` in `stix_shifter_modules/lab_connector/stix_transmission/api_client.py` where you initialize the connection and configurations needed for data source API requests. This class also includes the utility functions needed for the major functionalities of the connector.

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

    * Define and implement `ping_data_source()` function inside `APIClient()`:

    ```
    def ping_data_source(self):
            # Pings the data source
            response = {"code": 200, "message": "All Good!"}
            try:
                cnx = lab_connector.connector.connect(user=self.user, password=self.password, 
                                              host=self.host, database=self.database, 
                                              port=self.port, auth_plugin=self.auth_plugin)  


            except lab_connector.connector.Error as err:
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

    ### Query 

    * As a synchronous connector, it doesn't require any API request to start or create the query. Therefore no need to define and implement the functions of the query function. `self.setup_transmission_basic(connection, configuration)` statement inside entry point class `EntryPoint()` takes care of that automatically.

    ### Status

    * Same as query, synchronous connector doesn't return any status from the data source hence no action needed.

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

    * Define and implement a function named `run_search(self, query, offset, length)`  in `APIClient()` class.

    * Copy the code block https://github.com/opencybersecurityalliance/stix-shifter/blob/8ae2cf2a0196531b8e0daf8f5ff141b4251ec201/stix_shifter_modules/mysql/stix_transmission/api_client.py#L40

    * You can now run all the transmission CLI command from your workspace to tests

11. Implement Datasource results to STIX translation
    
    * Make sure datasource returns the results in JSON format
    * Implement ResultsTranslator(JSONToStix) class
    ```
    from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import JSONToStix

    class ResultsTranslator(JSONToStix):
        pass    
    ```
    * There's no pre-processing needed fo the results 
    * The parent utility class JSONToStix automatically translates the results into STIX. 

12. Implement `ErrorMapper()` class in `stix_shifter_modules/lab_connector/stix_transmission/error_mapper.py` for mapping any API specific error code message for the return object. This same content can be used: https://raw.githubusercontent.com/opencybersecurityalliance/stix-shifter/develop/stix_shifter_modules/mysql/stix_transmission/error_mapper.py

13. Add any data source specific dependency to the stix_shifter_modules/lab_connector/requirements.txt.  In this case add `mysql-connector-python==8.0.25`

14. You also need to create a `README.md` for the connector which includes the details of the API or SDK used in the connector and also some sample commands and the results `stix_shifter_modules/lab_connector/README.md`