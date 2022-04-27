# STIX-Shifter CLI Quick Lab

## Overview

STIX (Structured Threat Information eXpression) is a JSON structure used to share cybersecurity threat intelligence. STIX-shifter is an open-source python library that is part of the Open Cybersecurity Alliance. It allows data repositories to be queried using STIX patterning and return the results as STIX cyber observable objects. This lab will allow users to test out the various stix-shifter CLI commands.

## Setup

### 1. Open a terminal and install the required stix-shifter libraries

This installs the core stix-shifter and utils library along with the STIX-bundle and QRadar connectors.

```
pip install stix-shifter stix-shifter-utils stix-shifter-modules-stix_bundle stix-shifter-modules-qradar
```

### 2. Store the STIX bundle URL in a bash variable

This is a bundle of sample STIX data that will be used to demonstrate the `stix_bundle` connector.

```
BUNDLE_URL=https://raw.githubusercontent.com/opencybersecurityalliance/stix-shifter/develop/data/cybox/crowdstrike/crowdstrike_detections_20210723.json
```

### 3. Store the sample result JSON in a bash variable

This is a list of JSON objects containing sample data that will be used to demonstrate STIX translation.

```
JSON_RESULTS=$(cat <<EOF 
[
    {
        "qidname": "Logon Failure - Unknown user name or bad password",
        "qid": 5000012,
        "categoryname": "Host Login Failed",
        "categoryid": 3003,
        "high_level_category_name": "Authentication",
        "high_level_category_id": 3000,
        "logsourceid": 1864,
        "devicetype": 12,
        "logsourcetypename": "Microsoft Windows Security Event Log",
        "logsourcename": "WindowsAuthServer @ microsoft.windows.test.com",
        "starttime": 1624908958652,
        "endtime": 1624909018652,
        "devicetime": 1624908958000,
        "sourceip": "109.0.216.203",
        "sourceport": 0,
        "sourcemac": "00:00:00:00:00:00",
        "destinationip": "192.168.1.11",
        "destinationport": 0,
        "destinationmac": "00:00:00:00:00:00",
        "username": "bill_holland",
        "direction": "R2L",
        "identityip": "0.0.0.0",
        "identityhostname": null,
        "eventcount": 31,
        "protocol": "Reserved",
        "eventpayload": "<13>Mar 21 01:42:50 microsoft.windows.test.com",
        "url": null,
        "magnitude": 8,
        "filename": null,
        "filehash": null,
        "sha1hash": null,
        "sha256hash": null,
        "md5hash": null,
        "filepath": null,
        "eventseverity": 7,
        "credibility": 10,
        "relevance": 8,
        "sourcegeographic": "Europe.France",
        "destinationgeographic": "other",
        "domainname": "Default Domain",
        "EventID": "529",
        "Image": "null",
        "ParentImage": "null",
        "ProcessCommandLine": "null",
        "ParentCommandLine": "null",
        "TargetImage": "null",
        "GrantedAccess": null,
        "CallTrace": null,
        "SourceImage": "null",
        "PipeName": "null",
        "StartModule": "null",
        "StartFunction": "null",
        "Signed": null,
        "Message": null,
        "RegistryValueName": null,
        "IMPHash": null,
        "ServiceFileName": "null",
        "RegistryKey": null,
        "ObjectName": "null",
        "UrlHost": "null",
        "ProcessName": null,
        "ProcessId": null,
        "ParentProcessId": null
    }
]
EOF
)
```

## Lab Steps

### 1. Examine the STIX Bundle

This is a bundle of STIX observed-data objects containing sanitized data from a CrowdStrike instance.

https://raw.githubusercontent.com/opencybersecurityalliance/stix-shifter/develop/data/cybox/crowdstrike/crowdstrike_detections_20210723.json

The stix_bundle connector will query the sample STIX bundle and return a subset of data based on the query pattern.

### 2. Run the execute command

The execute command runs through the entire stix-shifter flow:

-	Translates a STIX pattern into a native data source query
-	Sends the query to the data source via the data source APIs
-	Checks the status of the query via the data source APIs
-	Fetches the query results via the APIs and, if needed, converts them to JSON
-	Translates the JSON results into STIX objects

```
stix-shifter execute stix_bundle stix_bundle '{"type": "identity","id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff","name": "stix-bundle","identity_class": "system"}' '{"url": "'"$BUNDLE_URL"'"}' '{"auth": {}}' "[ipv4-addr:value = '12.111.222.0']"
```

Note the bundle of observed-data objects that are returned. Each of these objects contains a numbered set of cyber observable objects (url, network-traffic, ipv4-addr…) which contain the data from the target data source. Given the above CLI example, the ipv4-addr object should contain a value property with 12.111.222.0


## STIX Transmission CLI commands

The transmission commands use the data source APIs to send a query, check the status, fetch the results, and ping the connection.

### 3. Run the ping command

This command checks that the data source can be reached by the stix-shifter connector.

```
stix-shifter transmit stix_bundle '{"url": "'"$BUNDLE_URL"'"}' '{"auth": {}}' ping
```

### 4. Run the query command

This command sends the native query to the data source.

```
stix-shifter transmit stix_bundle '{"url": "'"$BUNDLE_URL"'"}' '{"auth": {}}' query "[ipv4-addr:value = '192.168.0.8']"
```

### 5. Run the status command 

This command checks the status of the query.


```
stix-shifter transmit stix_bundle '{"url": "'"$BUNDLE_URL"'"}' '{"auth": {}}' status "[ipv4-addr:value = '192.168.0.8']"
```

### 6. Run the results command

This command fetches the query results


```
stix-shifter transmit stix_bundle '{"url": "'"$BUNDLE_URL"'"}' '{"auth": {}}' results "[ipv4-addr:value = '192.168.0.8']" 0 2
```

## Translation mapping for QRadar


### 7. Examine the STIX pattern to AQL mapping file for the QRadar connector

https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/stix_shifter_modules/qradar/stix_translation/json/events_from_stix_map.json

This file determines how STIX objects and their properties are mapped to the target data source fields. 

### 8. Run the STIX query translation CLI command for the QRadar connector

This command passing in a STIX pattern and returns a list of native data source queries that can later be passed to a query transmission call.

```
stix-shifter translate qradar:events query '{}' "[ipv4-addr:value = '109.0.216.203' AND file:name = 'photos.exe'] OR [url:value = 'blah.com' OR url:value = 'path.com' OR url:value = 'crhs.ca']"
```


### 9. Examine the JSON to STIX mapping file for the QRadar connector

https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/stix_shifter_modules/qradar/stix_translation/json/to_stix_map.json


### 10. Run the JSON results translation CLI command for the QRadar connector

This command passes in a STIX identity object and a list of JSON results (each element in the list represents a row of data). A bundle of STIX objects is returned. The bundle contains the identity object, which represents the data source the data comes from, and an observed-data object for each of the rows that were translated.
```
stix-shifter translate qradar results '{"type": "identity","id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff","name": "QRadar","identity_class": "system"}' "$JSON_RESULTS"
```


