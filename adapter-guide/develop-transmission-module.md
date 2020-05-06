# STIX Transmission

The steps below assume you have renamed the `async_dummy` module directory to our example connector name, `abc_security_monitor`.

{: #transmission-mod}

1. [Exploring the stix_transmission directory](#step-1-exploring-the-stix_transmission-directory)
1. [Edit the apiclient.py file](#step-2-edit-the-apiclient-file)
1. [Edit the dummy_connector.py file](#step-3-edit-the-dummy-connector-file)
1. [Edit the dummy_error_mapper.py file](#step-4-edit-the-dummy-error-mapper-file)
1. [Add the module name to the stix transmission file](#step-5-add-the-module-name-to-stix_transmission.py)
1. [Verify that the transmission module was created successfully](#step-6-verify-that-the-transmission-module-was-created-successfully)

## Step 1. Exploring the stix_transmission directory

Verify that your `stix_transmission` directory contains the following folders and files.

For an asynchronous transmission module, you must have the following files:

| Folder/file        | Why is it important? Where is it used?                                  |
| -------------------| ----------------------------------------------------------------------- |
| \_\_init\_\_.py    | This file is required by Python to properly handle library directories. |
| api_client.py       | Contains methods that make the data source API calls, used by the individual connector classes
| query_connector.py | Contains class for executing a search on the data source
| status_connector.py | Contains class for checking the status an active search on the data source
| delete_connector.py | Contains class for deleting an active search on the data source
| results_connector.py | Contains class for fetching the search results from the data source
| ping_connector.py | Contains class to ping the data source
| error_mapper.py |

The synchronous transmission module has no need to make status or query calls since the query is handled directly in the results API call. Therefore, the synchronous transmission module will not include  `query_connector.py` or `status_connector.py`. 


[Back to top](#create-a-transmission-module)

## Step 2. Edit the API Client

Edit the `api_client.py` APIClient class methods to make the relevant API calls to the data source. 

- For a asynchronous connector, the data source API must support:
  - Pinging the data source
  - Sending a search query to the data source
  - Checking the status of a search
  - Retrieving the search results

If supported by the data source, edit the `delete_search` method, otherwise leave it as it appears in the async_dummy connector.

[Back to top](#create-a-transmission-module)

## Step 3. Edit the connector class methods

Each of the stix transmission connector classes (found in the `stix_transmission/*_connector.py` files) use `api_client.py` to make the relevant calls to the data source. Edit the class methods if required by the data source. **It is important to keep the method names and signatures as they are.** Changing them will prevent the transmission methods from working properly. You are free to add new class methods as needed.

### Returning results in JSON format

Results from the data source need to be returned as an array of JSON objects before they can be converted into STIX. If the data source does not natively return results in this way, the `ResultsConnector.create_results_connection` method should handle any needed conversion. The results array needs to be wrapped in a string. A simple example of returned data:

```
'[{"ipaddress": "0.0.0.0", "url": "www.example.com"}, {"ipaddress": "1.1.1.1", "url": "www.another.example.net"}]'
```

**Note on search IDs**

For asynchronous sources, the search id that gets passed into the status, delete, and results methods is the ID returned by the data source when making the query API call. This is used to keep track of the original query, allowing the status and results to be fetched. However, in the case a synchronous data source, the search id is the entire query string; this is what gets passed into the results and delete methods.

[Back to top](#create-a-transmission-module)

## Step 4. Edit the error mapper file

The error mapper associates data source error codes, returned by the API, with error messages defined in the `ErrorCode` class (found in `stix_shifter_utils/utils/error_response.py`). Update the keys in the `error_mapping` dictionary to match any error codes returned by the API.

As an example, `1002: ErrorCode.TRANSMISSION_SEARCH_DOES_NOT_EXISTS` would return an error code of 'no_results' if the API returned a 1002 code. Stix-shifter returns errors in the following format:

`{'success': False, 'error': <Error message reported by API>, 'code': <Error code>}`

[Back to top](#create-a-transmission-module)


## Step 5. Verify that the transmission module was created successfully

The stix-shifter CLI can be used to test each of the transmission methods. Open a terminal on your local machine, and navigate to the root of the stix-shifter project. The format for calling a method is:

`python main.py <connector name> '<CONNECTION OBJECT>' '<CONFIGURATION OBJECT>' <METHOD NAME> '<METHOD ARGUMENTS>'`

1. You must have:

   - Authentication credentials to connect to the data source, (ex. username and password).
   - A self-signed certificate if required by your data source.

   Authentication depends on the data source and can be:

   ```
   '{"auth": {"username": "<username>","password": "<password>"}}' or
   '{"auth": {"SEC":"<SEC TOKEN>"}}'
   ```

2. Test the transmission ping method.

   1. Use the following CLI command:

      ```
      python main.py transmit abc '{"host":"<IP address or URL to data source>", "port":"<port number>", "cert":
      "-----BEGIN CERTIFICATE-----<certificate>-----END CERTIFICATE-----\n"}' '{"auth": <authentication object>}' ping
      ```

   2. Visually confirm that a result comes back with
      ```
      {'success': True}
      ```

3. Test the transmission is_async method.

   1. Use the following CLI command:
      ```
      python main.py transmit abc '{"host":"<IP address or URL to data source>", "port":"<port number>", "cert":
      "-----BEGIN CERTIFICATE-----<certificate>-----END CERTIFICATE-----\n"}' '{"auth{"auth": <authentication object>}' is_async
      ```
   2. Visually confirm that it returns true if the data source is asynchronous. Otherwise, it must return false.

4. Test the transmission query method.

   1. Use the following CLI command:

      ```
      python main.py transmit abc '{"host":"<IP address or URL to data source>", "port":"<port number>", "cert":
      "-----BEGIN CERTIFICATE-----<certificate>-----END CERTIFICATE-----\n"}' '{"auth": <authentication object>}' query "<Native data source Query String>"
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
      "-----BEGIN CERTIFICATE-----<certificate>-----END CERTIFICATE-----\n"}' '{"auth{"auth": <authentication object>}' status "<Query UUID from test 4>"
      ```

   2. Visually confirm that a result comes back with
      ```
      {'success': True, 'status': 'COMPLETED', 'progress': 100}
      ```

6. Test the transmission results method.

   1. Use the following CLI command:

      ```
      python main.py transmit abc '{"host":"<IP address or URL to data source>", "port":"<port number>", "cert":
      "-----BEGIN CERTIFICATE-----<certificate>-----END CERTIFICATE-----\n"}' '{"auth{"auth": <authentication object>}' results "<Query UUID from test 4>" <Offset Integer> <Length Integer>
      ```

   2. You can set the offset and length command line arguments to 1.
   3. Visually confirm that query results are returned as JSON objects. These results can be compared to what is returned when running the query string used in test C directly on the data source API, either through a UI or the CLI.

7. Test the transmission delete method if the data source supports it.

   1. Use the following CLI command:

      ```
      python main.py transmit abc '{"host":"<IP address or URL to data source>", "port":"<port number>", "cert":
      "-----BEGIN CERTIFICATE-----<certificate>-----END CERTIFICATE-----\n"}' '{"auth": <authentication object>}' delete "<Query UUID from test 4>"
      ```

   2. Visually confirm that a result comes back with
      ```
      {'success': True}
      ```

# Testing a new connector using the proxy host

Work on a new stix-shifter connector occurs after the project has been forked and cloned into a local development environment. Stix-shifter contains a **proxy** connector that facilitates a remote instance of the project calling out to a local instance. While in development, a new connector's working branch can be tested in any project using the stix-shifter library without first merging into the master branch on Github. A host is run on the local instance from the CLI. When a `proxy` data source is passed to the remote instance of stix-shifter, the real connection attributes (data source type, host, and port contained in the options) are passed onto the local instance of stix-shifter running the proxy host. The host will then use the new connector and return results back to the remote stix-shifter instance.

Open a terminal and navigate to your local stix-shifter directory. Run the host with the following command:

```
python main.py host "<STIX Identity Object>" "<Host IP address>:<Host Port>"
```

As an example:

```
python main.py host '{"type": "identity","id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff","name": "Bundle","identity_class": "events"}' "192.168.122.83:5000"
```
