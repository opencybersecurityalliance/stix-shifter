# SentinelOne

## Supported STIX Mappings

See the [table of mappings](sentinelone_supported_stix.md) for the STIX objects and operators supported by this connector.

**Table of Contents**

- [SentinelOne API Endpoints](#SentinelOne-api-endpoints)
- [Pattern expression with STIX attributes - Single Observation](#single-observation)
- [Pattern expression with STIX attributes - Multiple Observation](#multiple-observation)
- [Pattern expression with STIX attributes - Execute Query](#stix-execute-query)
- [Limitations](#limitations)
- [References](#references)

### SentinelOne API Endpoints

   |Connector Method|SentinelOne API Endpoint| Method
   | ----           |   ------              | -----|
   |Query Endpoint  |https://<{fqdn}>/web/api/v2.1/dv/init-query/|POST
   |Result Endpoint|https://<{fqdn}>/web/api/v2.1/dv/events/|GET
   
### Format for calling stix-shifter from the command line
```
python main.py `<translate or transmit>` `<translator_module>` `<query or result>` `<STIX identity object>` `<data>`
```
### Pattern expression with STIX attributes

### Single Observation

#### STIX Translate query
```shell
translate sentinelone query '{}' "[ipv4-addr:value = '1.1.0.0'] START t'2022-03-01T11:00:00.000Z' STOP t'2023-03-08T11:00:00.003Z'"
```
#### STIX Translate query - output
```json
{
    "queries": [
        "{\"query\": \"(srcIp = \\\"1.1.0.0\\\" OR dstIp = \\\"1.1.0.0\\\" OR srcMachineIP = \\\"1.1.0.0\\\") AND EventTime  BETWEEN \\\"2022-03-01T11:00:00.000Z\\\" AND \\\"2023-03-08T11:00:00.003Z\\\"\", \"fromDate\": \"2022-03-01T11:00:00.000Z\", \"toDate\": \"2023-03-08T11:00:00.003Z\", \"limit\": 10000}"
    ]
}
```
#### STIX Transmit ping 

```shell
transmit
sentinelone
"{\"host\":\"xx.xx.xx\"}"
"{\"auth\":{\"apitoken\": \"xxxxx\"}}"
ping
```

#### STIX Transmit ping - output
```json
{
    "success": true,
    "code": 200
}
```
#### STIX Transmit query 

```shell
transmit
sentinelone
"{\"host\":\"xx.xx.xx\"}"
"{\"auth\":{\"apitoken\": \"xxxxx\"}}"
query
"{\"query\": \"(srcIp = \\"1.1.0.0\\" OR dstIp = \\"1.1.0.0\\" OR srcMachineIP = \\"1.1.0.0\\") AND EventTime  BETWEEN \\"2022-03-01T11:00:00.000Z\\" AND \\"2023-03-08T11:00:00.003Z\\"\", \"fromDate\": \"2022-03-01T11:00:00.000Z\", \"toDate\": \"2023-03-08T11:00:00.003Z\", \"limit\": 10000}"
```

#### STIX Transmit query - output
```json
{
    "success": true,
    "search_id": "xxxx"
}
```
#### STIX Transmit status 

```shell
transmit
sentinelone
"{\"host\":\"xx.xx.xx\"}"
"{\"auth\":{\"apitoken\": \"xxxxx\"}}"
status
"xxxxxx"
```

#### STIX Transmit status - output
```json
{
    "success": true,
    "status": "COMPLETED",
    "progress": 100
}
```
#### STIX Transmit results 

```shell
transmit
sentinelone
"{\"host\":\"xx.xx.xx\"}"
"{\"auth\":{\"apitoken\": \"xxxxx\"}}"
results
"xxxxxx"
0
1
```

#### STIX Transmit results - output
```json
{
    "success": true,
    "data": [
        {
            "agentDomain": "xx",
            "agentGroupId": "xx",
            "agentId": "xx",
            "agentInfected": false,
            "agentIp": "xx",
            "agentIsActive": true,
            "agentIsDecommissioned": false,
            "agentMachineType": "xx",
            "agentName": "xx",
            "agentNetworkStatus": "connected",
            "agentOs": "windows",
            "agentTimestamp": "2022-04-19T19:19:09.177Z",
            "agentUuid": "xx",
            "createdAt": "2022-04-19T19:19:09.177000Z",
            "endpointMachineType": "xx",
            "endpointName": "xx",
            "endpointOs": "windows",
            "eventIndex": "55",
            "eventTime": "2022-04-19T19:19:09.177Z",
            "eventType": "Login",
            "id": "xx",
            "loginAccountDomain": "-",
            "loginAccountName": "-",
            "loginAccountSid": "S-1-0-0",
            "loginFailureReason": "Unknown user name or bad password.",
            "loginIsSuccessful": "False",
            "loginType": "NETWORK",
            "loginsUserName": "ARLENE",
            "metaEventName": "WINLOGONATTEMPT",
            "objectType": "logins",
            "osSrcProcRelatedToThreat": "False",
            "parentProcessName": "xx",
            "parentProcessStartTime": "2022-02-18T11:13:25.373Z",
            "parentProcessUniqueKey": "xx",
            "pid": "xx",
            "processCmd": "C:\\Windows\\System32\\xx -k termsvcs",
            "processGroupId": "xx",
            "processImagePath": "C:\\Windows\\system32\\xx",
            "processImageSha1Hash": "a1385ce20ad79f55df235effd9780c31442aa234",
            "processIntegrityLevel": "SYSTEM",
            "processName": "xx",
            "processStartTime": "2022-02-18T11:13:26.812Z",
            "processUniqueKey": "F7562BB2C0064892",
            "publisher": "MICROSOFT WINDOWS PUBLISHER",
            "relatedToThreat": "False",
            "signedStatus": "signed",
            "siteId": "xx",
            "siteName": "Default site",
            "srcMachineIp": "xx",
            "srcProcCmdLine": "C:\\Windows\\System32\\xx -k termsvcs",
            "srcProcImagePath": "C:\\Windows\\system32\\xx",
            "srcProcImageSha1": "a1385ce20ad79f55df235effd9780c31442aa234",
            "srcProcIntegrityLevel": "SYSTEM",
            "srcProcName": "xx",
            "srcProcParentImagePath": "C:\\Windows\\system32\\xx",
            "srcProcParentImageSha1": "106a001c4c9820a6aec6a8ba17d3836525faf80e",
            "srcProcParentName": "xx",
            "srcProcParentProcUid": "27717F70F7FD180D",
            "srcProcParentStartTime": "2022-02-18T11:13:25.373Z",
            "srcProcParentStorylineId": "0917681AF353A269",
            "srcProcParentUid": "27717F70F7FD180D",
            "srcProcPid": "xx",
            "srcProcPublisher": "MICROSOFT WINDOWS PUBLISHER",
            "srcProcRelatedToThreat": "False",
            "srcProcSignedStatus": "signed",
            "srcProcStartTime": "2022-02-18T11:13:26.812Z",
            "srcProcStorylineId": "FE6925F54601DFEE",
            "srcProcUid": "xx",
            "srcProcUser": "NT AUTHORITY\\xx",
            "srcProcVerifiedStatus": "verified",
            "storyline": "FE6925F54601DFEE",
            "traceId": "01G11M7QQBAPEYMCVTEY288JN0",
            "trueContext": "FE6925F54601DFEE",
            "user": "NT AUTHORITY\\xx",
            "verifiedStatus": "verified"
        }
    ]
}

```


#### STIX Translate results

```shell
translate
sentinelone
results
"{\"type\":\"identity\",\"id\":\"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\",\"name\":\"sentinelone\",\"identity_class\":\"events\",\"created\":\"2022-03-22T13:22:50.336Z\",\"modified\":\"2022-03-22T13:22:50.336Z\"}"
" [{ \"agentDomain\": \"xx\", \"agentGroupId\": \"xx\", \"agentId\": \"xx\", \"agentInfected\": false, \"agentIp\": \"xx\", \"agentIsActive\": true, \"agentIsDecommissioned\": false, \"agentMachineType\": \"xx\", \"agentName\": \"xx\", \"agentNetworkStatus\": \"connected\", \"agentOs\": \"windows\", \"agentTimestamp\": \"2022-04-19T19:19:09.177Z\", \"agentUuid\": \"xx\", \"createdAt\": \"2022-04-19T19:19:09.177000Z\", \"endpointMachineType\": \"xx\", \"endpointName\": \"xx\", \"endpointOs\": \"windows\", \"eventIndex\": \"55\", \"eventTime\": \"2022-04-19T19:19:09.177Z\", \"eventType\": \"Login\", \"id\": \"xx\", \"loginAccountDomain\": \"-\", \"loginAccountName\": \"-\", \"loginAccountSid\": \"S-1-0-0\", \"loginFailureReason\": \"Unknown user name or bad password.\", \"loginIsSuccessful\": \"False\", \"loginType\": \"NETWORK\", \"loginsUserName\": \"ARLENE\", \"metaEventName\": \"WINLOGONATTEMPT\", \"objectType\": \"logins\", \"osSrcProcRelatedToThreat\": \"False\", \"parentProcessName\": \"xx\", \"parentProcessStartTime\": \"2022-02-18T11:13:25.373Z\", \"parentProcessUniqueKey\": \"xx\", \"pid\": \"xx\", \"processCmd\": \"C:\\Windows\\System32\\xx -k termsvcs\", \"processGroupId\": \"xx\", \"processImagePath\": \"C:\\Windows\\system32\\xx\", \"processImageSha1Hash\": \"a1385ce20ad79f55df235effd9780c31442aa234\", \"processIntegrityLevel\": \"SYSTEM\", \"processName\": \"xx\", \"processStartTime\": \"2022-02-18T11:13:26.812Z\", \"processUniqueKey\": \"F7562BB2C0064892\", \"publisher\": \"MICROSOFT WINDOWS PUBLISHER\", \"relatedToThreat\": \"False\", \"signedStatus\": \"signed\", \"siteId\": \"1336793312849490611\", \"siteName\": \"Default site\", \"srcMachineIp\": \"1.1.1.1\", \"srcProcCmdLine\": \"C:\\Windows\\System32\\xx -k termsvcs\", \"srcProcImagePath\": \"C:\\Windows\\system32\\xx\", \"srcProcImageSha1\": \"a1385ce20ad79f55df235effd9780c31442aa234\", \"srcProcIntegrityLevel\": \"SYSTEM\", \"srcProcName\": \"xx\", \"srcProcParentImagePath\": \"C:\\Windows\\system32\\xx\", \"srcProcParentImageSha1\": \"106a001c4c9820a6aec6a8ba17d3836525faf80e\", \"srcProcParentName\": \"xx\", \"srcProcParentProcUid\": \"27717F70F7FD180D\", \"srcProcParentStartTime\": \"2022-02-18T11:13:25.373Z\", \"srcProcParentStorylineId\": \"0917681AF353A269\", \"srcProcParentUid\": \"27717F70F7FD180D\", \"srcProcPid\": \"xx\", \"srcProcPublisher\": \"MICROSOFT WINDOWS PUBLISHER\", \"srcProcRelatedToThreat\": \"False\", \"srcProcSignedStatus\": \"signed\", \"srcProcStartTime\": \"2022-02-18T11:13:26.812Z\", \"srcProcStorylineId\": \"FE6925F54601DFEE\", \"srcProcUid\": \"F7562BB2C0064892\", \"srcProcUser\": \"NT AUTHORITY\\NETWORK SERVICE\", \"srcProcVerifiedStatus\": \"verified\", \"storyline\": \"FE6925F54601DFEE\", \"traceId\": \"01G11M7QQBAPEYMCVTEY288JN0\", \"trueContext\": \"FE6925F54601DFEE\", \"user\": \"NT AUTHORITY\\xx\", \"verifiedStatus\": \"verified\" } ]"
```

#### STIX Translate results - output
```json
{
    "type": "bundle",
    "id": "bundle--aeb0a89c-5822-4afb-933f-0ad7faf120d5",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "sentinelone",
            "identity_class": "events",
            "created": "2022-03-22T13:22:50.336Z",
            "modified": "2022-03-22T13:22:50.336Z"
        },
        {
            "id": "observed-data--4fc65e04-ec66-4a1e-8ae0-7766a0b5e483",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-20T11:23:52.886Z",
            "modified": "2022-04-20T11:23:52.886Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "agent": "xx",
                    "host_ref": "1",
                    "created": "2022-04-19T19:19:09.177Z",
                    "action": "Login",
                    "category": [
                        "logins"
                    ],
                    "process_ref": "3",
                    "user_ref": "8"
                },
                "1": {
                    "type": "x-oca-asset",
                    "extensions": {
                        "x-sentinelone-endpoint": {
                            "agent_uuid": "xx",
                            "machine_type": "xx",
                            "endpoint_os": "windows"
                        }
                    },
                    "hostname": "xx"
                },
                "2": {
                    "type": "user-account",
                    "display_name": "-",
                    "user_id": "S-1-0-0",
                    "extensions": {
                        "x-sentinelone-login": {
                            "login_failure_reason": "Unknown user name or bad password.",
                            "login_type": "NETWORK"
                        }
                    },
                    "account_login": "ARLENE"
                },
                "3": {
                    "type": "process",
                    "command_line": "C:\\Windows\\System32\\xx -k termsvcs",
                    "binary_ref": "6",
                    "x_unique_id": "xx",
                    "extensions": {
                        "x-sentinelone-process": {
                            "integrity_level": "SYSTEM",
                            "publisher": "MICROSOFT WINDOWS PUBLISHER",
                            "signed_status": "signed",
                            "story_line_id": "xx",
                            "verified_status": "verified"
                        }
                    },
                    "name": "xx",
                    "parent_ref": "7",
                    "pid": 11111,
                    "created": "2022-02-18T11:13:26.812Z",
                    "creator_user_ref": "8"
                },
                "4": {
                    "type": "directory",
                    "path": "C:\\Windows\\xx"
                },
                "6": {
                    "type": "file",
                    "hashes": {
                        "SHA-1": "a1385ce20ad79f55df235effd9780c31442aa234"
                    }
                },
                "7": {
                    "type": "process",
                    "name": "xxxx",
                    "created": "2022-02-18T11:13:25.373Z"
                },
                "8": {
                    "type": "user-account",
                    "user_id": "NT AUTHORITY\\xx"
                }
            },
            "first_observed": "2022-02-18T11:13:26.812Z",
            "last_observed": "2022-04-20T11:23:52.886Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```

### Multiple Observation  

#### STIX Translate query
```shell
translate sentinelone query {} "([x-oca-event:action = 'Process Creation'] AND [file:size > 1000] OR [x-oca-asset:extensions.'x-sentinelone-endpoint'.endpoint_os = 'windows'] ) START t'2022-04-16T00:00:00.000000Z' STOP t'2023-04-17T00:00:00.000000Z'"
```

#### STIX Translate query - output

```json
{
    "queries": [
        "{\"query\": \"(eventType = \\\"PROCESS CREATION\\\" AND EventTime  BETWEEN \\\"2022-04-16T00:00:00.000000Z\\\" AND \\\"2023-04-17T00:00:00.000000Z\\\") OR (tgtFileSize > \\\"1000\\\" AND EventTime  BETWEEN \\\"2022-04-16T00:00:00.000000Z\\\" AND \\\"2023-04-17T00:00:00.000000Z\\\") OR (endpointOs = \\\"WINDOWS\\\" AND EventTime  BETWEEN \\\"2022-04-16T00:00:00.000000Z\\\" AND \\\"2023-04-17T00:00:00.000000Z\\\")\", \"fromDate\": \"2022-04-16T00:00:00.000000Z\", \"toDate\": \"2023-04-17T00:00:00.000000Z\", \"limit\": 10000}"
    ]
}
```


#### STIX Transmit query

```shell
transmit
sentinelone
"{\"host\":\"xx.xx.xx\"}"
"{\"auth\":{\"apitoken\": \"xxxxx\"}}"
query
"{\"query\": \"(eventType = \\"PROCESS CREATION\\" AND EventTime  BETWEEN \\"2022-04-16T00:00:00.000000Z\\" AND \\"2023-04-17T00:00:00.000000Z\\") OR (tgtFileSize > \\"1000\\" AND EventTime  BETWEEN \\"2022-04-16T00:00:00.000000Z\\" AND \\"2023-04-17T00:00:00.000000Z\\") OR (endpointOs = \\"WINDOWS\\" AND EventTime  BETWEEN \\"2022-04-16T00:00:00.000000Z\\" AND \\"2023-04-17T00:00:00.000000Z\\")\", \"fromDate\": \"2022-04-16T00:00:00.000000Z\", \"toDate\": \"2023-04-17T00:00:00.000000Z\", \"limit\": 10000}"
```

#### STIX Transmit query - output

```json
{
    "success": true,
    "search_id": "xxxxx"
}
```
#### STIX Transmit status 

```shell
transmit
sentinelone
"{\"host\":\"xx.xx.xx\"}"
"{\"auth\":{\"apitoken\": \"xxxxx\"}}"
status
"xxxxxx"
```

#### STIX Transmit status - output
```json
{
    "success": true,
    "status": "COMPLETED",
    "progress": 100
}
```
#### STIX Transmit results 

```shell
transmit
sentinelone
"{\"host\":\"xx.xx.xx\"}"
"{\"auth\":{\"apitoken\": \"xxxxx\"}}"
results
"xxxxxx"
0
1
```

#### STIX Transmit results - output
```json
{
    "success": true,
    "data": [
        {
            "agentDomain": "WORKGROUP",
            "agentGroupId": "xx",
            "agentId": "xx",
            "agentInfected": false,
            "agentIp": "xx",
            "agentIsActive": true,
            "agentIsDecommissioned": false,
            "agentMachineType": "server",
            "agentName": "xx",
            "agentNetworkStatus": "connected",
            "agentOs": "windows",
            "agentTimestamp": "2022-04-17T07:20:10.796Z",
            "agentUuid": "xx",
            "connectionStatus": "SUCCESS",
            "createdAt": "2022-04-17T07:20:10.796000Z",
            "direction": "OUTGOING",
            "dstIp": "xx",
            "dstPort": 11111,
            "endpointMachineType": "xx",
            "endpointName": "xxxxxxx",
            "endpointOs": "windows",
            "eventIndex": "19",
            "eventTime": "2022-04-17T07:20:10.796Z",
            "eventType": "IP Connect",
            "id": "xx",
            "metaEventName": "TCPV4",
            "netConnStatus": "SUCCESS",
            "netEventDirection": "OUTGOING",
            "netProtocolName": "null",
            "objectType": "ip",
            "osSrcProcRelatedToThreat": "False",
            "parentProcessName": "xxxx",
            "parentProcessStartTime": "2022-04-13T10:25:21.517Z",
            "parentProcessUniqueKey": "B5DBD2638D99E654",
            "pid": "xxxx",
            "processCmd": "C:\\Program Files\\Palo Alto Networks\\Traps\\xxxx",
            "processGroupId": "EF4338FE0431ABCC",
            "processImagePath": "C:\\Program Files\\Palo Alto Networks\\Traps\\xxxx",
            "processImageSha1Hash": "1627eeb843c764f25c5f8d9aac687dea539f4a9b",
            "processIntegrityLevel": "SYSTEM",
            "processName": "xxxx",
            "processStartTime": "2022-04-13T10:25:26.383Z",
            "processUniqueKey": "B5DBD2638D99E654",
            "publisher": "PALO ALTO NETWORKS",
            "relatedToThreat": "False",
            "signedStatus": "signed",
            "siteId": "1336793312849490611",
            "siteName": "Default site",
            "srcIp": "xxxx",
            "srcPort": 1111111,
            "srcProcCmdLine": "C:\\Program Files\\Palo Alto Networks\\Traps\\xxxx",
            "srcProcImagePath": "C:\\Program Files\\Palo Alto Networks\\Traps\\xxxx",
            "srcProcImageSha1": "1627eeb843c764f25c5f8d9aac687dea539f4a9b",
            "srcProcIntegrityLevel": "SYSTEM",
            "srcProcName": "xxxx",
            "srcProcParentImagePath": "C:\\Windows\\System32\\xxxx",
            "srcProcParentImageSha1": "106a001c4c9820a6aec6a8ba17d3836525faf80e",
            "srcProcParentName": "xxxx",
            "srcProcParentProcUid": "17AE1B8C02AC084F",
            "srcProcParentStartTime": "2022-04-13T10:25:21.517Z",
            "srcProcParentStorylineId": "9FB6E0E3103901BC",
            "srcProcParentUid": "17AE1B8C02AC084F",
            "srcProcPid": "xxxx",
            "srcProcPublisher": "PALO ALTO NETWORKS",
            "srcProcRelatedToThreat": "False",
            "srcProcSignedStatus": "signed",
            "srcProcStartTime": "2022-04-13T10:25:26.383Z",
            "srcProcStorylineId": "EF4338FE0431ABCC",
            "srcProcUid": "B5DBD2638D99E654",
            "srcProcUser": "NT AUTHORITY\\xx",
            "srcProcVerifiedStatus": "verified",
            "storyline": "EF4338FE0431ABCC",
            "traceId": "01G0V6A46VQ4HJA5KH147CFKWY",
            "trueContext": "EF4338FE0431ABCC",
            "user": "NT AUTHORITY\\SYSTEM",
            "verifiedStatus": "verified"
        }
    ]
}
```


#### STIX Translate results

```shell
translate
sentinelone
results
"{\"type\":\"identity\",\"id\":\"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\",\"name\":\"sentinelone\",\"identity_class\":\"events\",\"created\":\"2022-03-22T13:22:50.336Z\",\"modified\":\"2022-03-22T13:22:50.336Z\"}"
"[{ \"agentDomain\": \"xx\", \"agentGroupId\": \"xx\", \"agentId\": \"xx\", \"agentInfected\": false, \"agentIp\": \"1.1.1.1\", \"agentIsActive\": true, \"agentIsDecommissioned\": false, \"agentMachineType\": \"xx\", \"agentName\": \"xx\", \"agentNetworkStatus\": \"connected\", \"agentOs\": \"windows\", \"agentTimestamp\": \"2022-04-20T01:01:46.324Z\", \"agentUuid\": \"xx\", \"createdAt\": \"2022-04-20T01:01:46.324000Z\", \"endpointMachineType\": \"xx\", \"endpointName\": \"xx\", \"endpointOs\": \"windows\", \"eventIndex\": \"54\", \"eventTime\": \"2022-04-20T01:01:46.324Z\", \"eventType\": \"Login\", \"id\": \"677881012878508059\", \"loginAccountDomain\": \"-\", \"loginAccountName\": \"-\", \"loginAccountSid\": \"S-1-0-0\", \"loginFailureReason\": \"Unknown user name or bad password.\", \"loginIsSuccessful\": \"False\", \"loginType\": \"NETWORK\", \"loginsUserName\": \"ADMIN\", \"metaEventName\": \"WINLOGONATTEMPT\", \"objectType\": \"logins\", \"osSrcProcRelatedToThreat\": \"False\", \"parentProcessName\": \"xx\", \"parentProcessStartTime\": \"2022-02-18T11:13:25.373Z\", \"parentProcessUniqueKey\": \"xx\", \"pid\": \"xx\", \"processCmd\": \"C:\\Windows\\System32\\xx -k termsvcs\", \"processGroupId\": \"xx\", \"processImagePath\": \"C:\\Windows\\system32\\xx\", \"processImageSha1Hash\": \"a1385ce20ad79f55df235effd9780c31442aa234\", \"processIntegrityLevel\": \"SYSTEM\", \"processName\": \"xx\", \"processStartTime\": \"2022-02-18T11:13:26.812Z\", \"processUniqueKey\": \"xx\", \"publisher\": \"MICROSOFT WINDOWS PUBLISHER\", \"relatedToThreat\": \"False\", \"signedStatus\": \"signed\", \"siteId\": \"1336793312849490611\", \"siteName\": \"Default site\", \"srcMachineIp\": \"1.1.1.1\", \"srcProcCmdLine\": \"C:\\Windows\\System32\\xx -k termsvcs\", \"srcProcImagePath\": \"C:\\Windows\\system32\\xx\", \"srcProcImageSha1\": \"a1385ce20ad79f55df235effd9780c31442aa234\", \"srcProcIntegrityLevel\": \"SYSTEM\", \"srcProcName\": \"xx\", \"srcProcParentImagePath\": \"C:\\Windows\\system32\\services.exe\", \"srcProcParentImageSha1\": \"106a001c4c9820a6aec6a8ba17d3836525faf80e\", \"srcProcParentName\": \"services.exe\", \"srcProcParentProcUid\": \"xx\", \"srcProcParentStartTime\": \"2022-02-18T11:13:25.373Z\", \"srcProcParentStorylineId\": \"0917681AF353A269\", \"srcProcParentUid\": \"27717F70F7FD180D\", \"srcProcPid\": \"724\", \"srcProcPublisher\": \"MICROSOFT WINDOWS PUBLISHER\", \"srcProcRelatedToThreat\": \"False\", \"srcProcSignedStatus\": \"signed\", \"srcProcStartTime\": \"2022-02-18T11:13:26.812Z\", \"srcProcStorylineId\": \"FE6925F54601DFEE\", \"srcProcUid\": \"F7562BB2C0064892\", \"srcProcUser\": \"NT AUTHORITY\\NETWORK SERVICE\", \"srcProcVerifiedStatus\": \"verified\", \"storyline\": \"FE6925F54601DFEE\", \"traceId\": \"01G127VVYKGDE639TA8JHGGAW4\", \"trueContext\": \"FE6925F54601DFEE\", \"user\": \"NT AUTHORITY\\xx\", \"verifiedStatus\": \"verified\" }]"

```

#### STIX Translate results - output
```json
{
    "type": "bundle",
    "id": "bundle--50ff31f7-bae6-4889-a021-e76b722c3cd5",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "sentinelone",
            "identity_class": "events",
            "created": "2022-03-22T13:22:50.336Z",
            "modified": "2022-03-22T13:22:50.336Z"
        },
        {
            "id": "observed-data--18832926-d2ff-432c-84d2-1e48bf13a3c0",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-20T11:42:13.786Z",
            "modified": "2022-04-20T11:42:13.786Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "agent": "xx",
                    "host_ref": "1",
                    "created": "2022-04-20T01:01:46.324Z",
                    "action": "Login",
                    "category": [
                        "logins"
                    ],
                    "process_ref": "3",
                    "user_ref": "8"
                },
                "1": {
                    "type": "x-oca-asset",
                    "extensions": {
                        "x-sentinelone-endpoint": {
                            "agent_uuid": "xx",
                            "machine_type": "xx",
                            "endpoint_os": "windows"
                        }
                    },
                    "hostname": "xx"
                },
                "2": {
                    "type": "user-account",
                    "display_name": "-",
                    "user_id": "S-1-0-0",
                    "extensions": {
                        "x-sentinelone-login": {
                            "login_failure_reason": "Unknown user name or bad password.",
                            "login_type": "NETWORK"
                        }
                    },
                    "account_login": "ADMIN"
                },
                "3": {
                    "type": "process",
                    "command_line": "C:\\Windows\\System32\\xx -k termsvcs",
                    "binary_ref": "6",
                    "x_unique_id": "xx",
                    "extensions": {
                        "x-sentinelone-process": {
                            "integrity_level": "SYSTEM",
                            "publisher": "MICROSOFT WINDOWS PUBLISHER",
                            "signed_status": "signed",
                            "story_line_id": "xx",
                            "verified_status": "verified"
                        }
                    },
                    "name": "xx",
                    "parent_ref": "7",
                    "pid": 11111111,
                    "created": "2022-02-18T11:13:26.812Z",
                    "creator_user_ref": "8"
                },
                "4": {
                    "type": "directory",
                    "path": "C:\\Windows\\xx"
                },
                "6": {
                    "type": "file",
                    "hashes": {
                        "SHA-1": "a1385ce20ad79f55df235effd9780c31442aa234"
                    }
                },
                "7": {
                    "type": "process",
                    "name": "xx",
                    "created": "2022-02-18T11:13:25.373Z"
                },
                "8": {
                    "type": "user-account",
                    "user_id": "NT AUTHORITY\\xx"
                }
            },
            "first_observed": "2022-02-18T11:13:26.812Z",
            "last_observed": "2022-04-20T11:42:13.786Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```
#### STIX Execute query
```shell
execute
sentinelone
sentinelone
"{\"type\":\"identity\",\"id\":\"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\",\"name\":\"sentinelone\",\"identity_class \":\"events\"}"
"{\"host\":\"xx.xx.xx.xx\"}"
"{\"auth\":{\"apitoken\": \"xxxxx\"}}"
"[process:name LIKE 'exe' AND x-oca-event:action = 'Process Creation'] START t'2022-04-03T08:43:10.003Z' STOP t'2022-04-04T05:35:10.003Z'"
```
#### STIX Execute query - output
```json
{
   "type": "bundle",
   "id": "bundle--5a8647f3-d72e-455f-aa90-1e99c3dda2db",
   "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "sentinelone",
            "identity_class ": "events"
        },
        {
            "id": "observed-data--4458cf67-2a8d-438f-b222-694e39b090ad",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-20T11:52:32.202Z",
            "modified": "2022-04-20T11:52:32.202Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "agent": "xx",
                    "host_ref": "1",
                    "created": "2022-04-20T05:31:03.739Z",
                    "action": "Process Creation",
                    "category": [
                        "process"
                    ],
                    "process_ref": "2",
                    "user_ref": "7"
                },
                "1": {
                    "type": "x-oca-asset",
                    "extensions": {
                        "x-sentinelone-endpoint": {
                            "agent_uuid": "xx",
                            "machine_type": "xx",
                            "endpoint_os": "windows"
                        }
                    },
                    "hostname": "xx"
                },
                "2": {
                    "type": "process",
                    "command_line": "C:\\Program Files (x86)\\Google\\Temp\\GUM10C0.tmp\\xx /update /sessionid {A621AB5C-61F8-473C-91D7-6C91A9F50036}",
                    "binary_ref": "5",
                    "x_unique_id": "xx",
                    "extensions": {
                        "x-sentinelone-process": {
                            "integrity_level": "SYSTEM",
                            "publisher": "GOOGLE LLC",
                            "signed_status": "signed",
                            "story_line_id": "xx",
                            "verified_status": "verified"
                        }
                    },
                    "name": "xx",
                    "parent_ref": "6",
                    "pid": 228,
                    "created": "2022-04-20T05:31:33.088Z",
                    "creator_user_ref": "7"
                },
                "3": {
                    "type": "directory",
                    "path": "C:\\Program Files (x86)\\Google\\Temp\\xx"
                },
                "5": {
                    "type": "file",
                    "hashes": {
                        "SHA-1": "c0a98fd8c74d031f54fda658a1c67d8886b5e076"
                    }
                },
                "6": {
                    "type": "process",
                    "name": "xx",
                    "created": "2022-04-20T05:31:31.715Z"
                },
                "7": {
                    "type": "user-account",
                    "user_id": "NT AUTHORITY\\xx"
                }
            },
            "first_observed": "2022-04-20T05:31:42.446Z",
            "last_observed": "2022-04-20T11:52:32.202Z",
            "number_observed": 1
      }
   ]
}
```

### Limitations
- Default data retention in sentinelone deep visibility is 14 days.

### References
- [SentinelOne](https://www.sentinelone.com/)