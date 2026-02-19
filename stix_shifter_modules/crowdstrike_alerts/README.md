# CrowdStrike Falcon Alerts

## About this connector

This connector replaces the now deprecated crowdstrike connector for collecting CrowdStrike Falcon detection and alert data.

## Supported STIX Mappings

See the [table of mappings](crowdstrike_alerts_supported_stix.md) for the STIX objects and operators supported by this connector.

## CrowdStrike Alerts Requirements

The CrowdStrike Alerts API requires the following to work.

1. A CrowdStrike environment with Endpoint Security set-up.
2. An OAuth2 API Client created with Alerts Scope enabled for read and the Detections Scope enabled for read.
3. Both the Client ID and Secret.

## CrowdStrike Alerts Sample Curl Commands

The Crowdstrike alerts API works via the following mechanisms.

1. Use the OAuth2 API Client Credentials to obtain a bearer token (this token expires after a set amount of time).
2. Using the bearer token, create a request for a list of ID's that match the query with a set limit.
3. Create a query for the data results using the list of ID's. 

Curl command to get a bearer token.

```curl --location 'https://[host]/oauth2/token' \
--header 'accept: application/json' \
--header 'user-agent: oca_stixshifter_1.0' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'client_id=[id]' \
--data-urlencode 'client_secret=[secret]'
```

Curl command to get a list of ID's.

```curl --location 'https://[host]/alerts/queries/alerts/v2' \
--header 'accept: application/json' \
--header 'user-agent: oca_stixshifter_1.0' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer [bearer token]'
```

Curl command to get the ID details

```curl --location 'https://[host]/alerts/queries/alerts/v2' \
--header 'accept: application/json' \
--header 'user-agent: oca_stixshifter_1.0' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer [bearer token]' \
--data '{"composite_ids":[ID List]}'
```

## CrowdStrike Supported STIX Pattern values (Querying):

The supported query values are defined in the mapping file from_stix_map.json. For detailed list of supported STIX Pattern values refer to the crowdstrike_alerts_supported_stix.md.

### Execute a STIX pattern on a CrowdStrike instance

```bash
$ python3 main.py execute crowdstrike_alerts crowdstrike_alerts "<data_source>" "<connection>" "<configuration>" "<query>"
```


```bash
$ python3 main.py execute crowdstrike_alerts crowdstrike_alerts "{\"type\":\"identity\",\"id\":\"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\",\"name\":\"Crowdstrike\",\"identity_class\":\"events\", \"created\":\"2022-05-22T13:22:50.336Z\",\"modified\":\"2022-05-25T13:22:50.336Z\"}" "{\"host\":\"[host\"}" "{\"auth\":{\"client_id\":\"[id]\", \"client_secret\":\"[secret]\"}}" "[ipv4-addr:value != '1.1.1.1'] START t'2024-03-01T11:00:00.000Z' STOP t'2024-07-03T11:54:00.000Z'" -r 100
```

Note in this example some logging is omitted.

Translated CrowdStrike query and parsed STIX expression:

```bash
$ python3 main.py translate crowdstrike_alerts query '{}' "[process:name = 'cmd.exe']"

    "queries": [
        "(((filename: 'cmd.exe',grandparent_details.filename: 'cmd.exe',parent_details.filename: 'cmd.exe')) %2B timestamp:> '2024-07-19T14:53:37.560762')"
    ]
```

## Example I - Converting from STIX patterns to FQL queries (STIX attributes)

STIX to sentinel field mapping is defined in from_stix_map.json

This example input pattern:

```bash
$ python3 main.py translate crowdstrike_alerts query '{}' "[process:name = 'cmd.exe']"
```

Returns the following native query:

```bash
    "queries": [
        "(((filename: 'cmd.exe',grandparent_details.filename: 'cmd.exe',parent_details.filename: 'cmd.exe')) %2B timestamp:> '2024-07-19T14:53:37.560762')"
    ]
```


## Example - Converting from CrowdStrike alerts to STIX (STIX attributes)

Sentinel data to STIX mapping is defined in to_stix_map.json

Sample data:

CrowdStrike data to Stix mapping is defined in to_stix_map.json which is located in the crowdstrike module.

For an example of an untranslated result see the file under crowdstrike_alerts/tests/stix_translation/sample_results_data.json.
For an example of a translated result see the file under crowdstrike_alerts/tests/stix_translation/sample_results_transformed.json.

## Operator Support (Data Source)
AND (Comparison)
OR (Comparison)
=
!=
>
>=
<
<= 
IN 

## Exclusions

FQL does not supports the following operators:
* LIKE 
* Matches

## Limitations

Not all fields may be supported. The Alerts endpoint can pull results from multiple products. The current implementation will only support detection alerts.