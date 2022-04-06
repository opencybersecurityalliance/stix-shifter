# SentinelOne Connector

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
        "{\"query\": \"(srcIp = \\\"1.1.0.0\\\" OR dstIp = \\\"1.1.0.0\\\") AND EventTime  BETWEEN \\\"2022-03-01T11:00:00.000Z\\\" AND \\\"2023-03-08T11:00:00.003Z\\\"\", \"fromDate\": \"2022-03-01T11:00:00.000Z\", \"toDate\": \"2023-03-08T11:00:00.003Z\", \"limit\": 10000}"
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
"{\"query\": \"(srcIp = \\"1.1.0.0\\" OR dstIp = \\"1.1.0.0\\") AND EventTime  BETWEEN \\"2022-03-01T11:00:00.000Z\\" AND \\"2023-03-08T11:00:00.003Z\\"\", \"fromDate\": \"2022-03-01T11:00:00.000Z\", \"toDate\": \"2023-03-08T11:00:00.003Z\"}"
```

#### STIX Transmit query - output
```json
{
    "success": true,
    "search_id": "xxxxxx"
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
    "status": "FINISHED",
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
3
```

#### STIX Transmit results - output
```json
{
"success": true,
"data": [
{
	"agentDomain": "WORKGROUP",
	"agentGroupId": "1336793312883045044",
	"agentId": "xxxx",
	"agentInfected": false,
	"agentIp": "xx",
	"agentIsActive": true,
	"agentIsDecommissioned": false,
	"agentMachineType": "xx",
	"agentName": "xx",
	"agentNetworkStatus": "connected",
	"agentOs": "windows",
	"agentTimestamp": "2022-04-03T08:32:05.605Z",
	"agentUuid": "xx",
	"connectionStatus": "SUCCESS",
	"createdAt": "2022-04-03T08:32:05.605000Z",
	"direction": "INCOMING",
	"dstIp": "xx",
	"dstPort": xx,
	"endpointMachineType": "xx",
	"endpointName": "xx",
	"endpointOs": "xx",
	"eventIndex": "15",
	"eventTime": "2022-04-03T08:32:05.605Z",
	"eventType": "IP Connect",
	"id": "xx",
	"metaEventName": "TCPV4",
	"netConnStatus": "SUCCESS",
	"netEventDirection": "INCOMING",
	"netProtocolName": "null",
	"objectType": "ip",
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
	"siteId": "1336793312849490611",
	"siteName": "Default site",
	"srcIp": "xx",
	"srcPort": xx,
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
	"srcProcUid": "F7562BB2C0064892",
	"srcProcUser": "NT AUTHORITY\\xx",
	"srcProcVerifiedStatus": "verified",
	"storyline": "FE6925F54601DFEE",
	"traceId": "01FZQ8VCZBGJ0M5ZSFGP4M6X2P",
	"trueContext": "FE6925F54601DFEE",
	"user": "NT AUTHORITY\\xx",
	"verifiedStatus": "verified"
}
```


#### STIX Translate results

```shell
translate
sentinelone
results
{\"type\":\"identity\",\"id\":\"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\",\"name\":\"sentinelone\",\"identity_class\":\"events\"}
"[{ \"accountId\": null, \"activeContentFileId\": null, \"activeContentHash\": null, \"activeContentPath\": null, \"activeContentSignedStatus\": null, \"activeContentType\": null, \"agentDomain\": \"WORKGROUP\", \"agentGroupId\": \"xx\", \"agentId\": \"xx\", \"agentInfected\": false, \"agentIp\": \"xx\", \"agentIsActive\": true, \"agentIsDecommissioned\": false, \"agentMachineType\": \"server\", \"agentName\": \"xxxx\", \"agentNetworkStatus\": \"connected\", \"agentOs\": \"windows\", \"agentTimestamp\": \"2022-03-03T10:44:02.276Z\", \"agentUuid\": \"xxxx\", \"agentVersion\": null, \"childProcCount\": null, \"connectionStatus\": \"SUCCESS\", \"containerId\": null, \"containerImage\": null, \"containerLabels\": null, \"containerName\": null, \"createdAt\": \"2022-03-03T10:44:02.276000Z\", \"crossProcCount\": null, \"crossProcDupRemoteProcHandleCount\": null, \"crossProcDupThreadHandleCount\": null, \"crossProcOpenProcCount\": null, \"crossProcOutOfStorylineCount\": null, \"crossProcThreadCreateCount\": null, \"direction\": \"INCOMING\", \"dnsCount\": null, \"dstIp\": \"1.1.0.0\", \"dstPort\": xx, \"endpointMachineType\": \"server\", \"endpointName\": \"xxxxx\", \"endpointOs\": \"windows\", \"eventIndex\": \"xxx\", \"eventTime\": \"2022-03-03T10:44:02.276Z\", \"eventType\": \"IP Connect\", \"fileIsExecutable\": null, \"fileMd5\": null, \"fileSha256\": null, \"id\": \"xxxx\", \"indicatorBootConfigurationUpdateCount\": null, \"indicatorEvasionCount\": null, \"indicatorExploitationCount\": null, \"indicatorGeneralCount\": null, \"indicatorInfostealerCount\": null, \"indicatorInjectionCount\": null, \"indicatorPersistenceCount\": null, \"indicatorPostExploitationCount\": null, \"indicatorRansomwareCount\": null, \"indicatorReconnaissanceCount\": null, \"k8sClusterName\": null, \"k8sControllerLabels\": null, \"k8sControllerName\": null, \"k8sControllerType\": null, \"k8sNamespace\": null, \"k8sNamespaceLabels\": null, \"k8sNode\": null, \"k8sPodLabels\": null, \"k8sPodName\": null, \"lastActivatedAt\": null, \"metaEventName\": \"TCPV4\", \"moduleCount\": null, \"netConnCount\": null, \"netConnInCount\": null, \"netConnOutCount\": null, \"netConnStatus\": \"SUCCESS\", \"netEventDirection\": \"INCOMING\", \"netProtocolName\": null, \"objectType\": \"ip\", \"osSrcChildProcCount\": null, \"osSrcCrossProcCount\": null, \"osSrcCrossProcDupRemoteProcHandleCount\": null, \"osSrcCrossProcDupThreadHandleCount\": null, \"osSrcCrossProcOpenProcCount\": null, \"osSrcCrossProcOutOfStorylineCount\": null, \"osSrcCrossProcThreadCreateCount\": null, \"osSrcDnsCount\": null, \"osSrcIndicatorBootConfigurationUpdateCount\": null, \"osSrcIndicatorEvasionCount\": null, \"osSrcIndicatorExploitationCount\": null, \"osSrcIndicatorGeneralCount\": null, \"osSrcIndicatorInfostealerCount\": null, \"osSrcIndicatorInjectionCount\": null, \"osSrcIndicatorPersistenceCount\": null, \"osSrcIndicatorPostExploitationCount\": null, \"osSrcIndicatorRansomwareCount\": null, \"osSrcIndicatorReconnaissanceCount\": null, \"osSrcModuleCount\": null, \"osSrcNetConnCount\": null, \"osSrcNetConnInCount\": null, \"osSrcNetConnOutCount\": null, \"osSrcProcActiveContentFileId\": null, \"osSrcProcActiveContentHash\": null, \"osSrcProcActiveContentPath\": null, \"osSrcProcActiveContentSignedStatus\": null, \"osSrcProcActiveContentType\": null, \"osSrcProcBinaryisExecutable\": null, \"osSrcProcCmdLine\": null, \"osSrcProcDisplayName\": null, \"osSrcProcImageMd5\": null, \"osSrcProcImagePath\": null, \"osSrcProcImageSha1\": null, \"osSrcProcImageSha256\": null, \"osSrcProcIntegrityLevel\": null, \"osSrcProcIsNative64Bit\": null, \"osSrcProcIsRedirectCmdProcessor\": null, \"osSrcProcIsStorylineRoot\": null, \"osSrcProcName\": null, \"osSrcProcParentActiveContentFileId\": null, \"osSrcProcParentActiveContentHash\": null, \"osSrcProcParentActiveContentPath\": null, \"osSrcProcParentActiveContentSignedStatus\": null, \"osSrcProcParentActiveContentType\": null, \"osSrcProcParentCmdLine\": null, \"osSrcProcParentDisplayName\": null, \"osSrcProcParentImageMd5\": null, \"osSrcProcParentImagePath\": null, \"osSrcProcParentImageSha1\": null, \"osSrcProcParentImageSha256\": null, \"osSrcProcParentIntegrityLevel\": null, \"osSrcProcParentIsNative64Bit\": null, \"osSrcProcParentIsRedirectCmdProcessor\": null, \"osSrcProcParentIsStorylineRoot\": null, \"osSrcProcParentName\": null, \"osSrcProcParentPid\": null, \"osSrcProcParentPublisher\": null, \"osSrcProcParentReasonSignatureInvalid\": null, \"osSrcProcParentSessionId\": null, \"osSrcProcParentSignedStatus\": null, \"osSrcProcParentStartTime\": null, \"osSrcProcParentStorylineId\": null, \"osSrcProcParentUid\": null, \"osSrcProcParentUser\": null, \"osSrcProcPid\": null, \"osSrcProcPublisher\": null, \"osSrcProcReasonSignatureInvalid\": null, \"osSrcProcRelatedToThreat\": \"False\", \"osSrcProcSessionId\": null, \"osSrcProcSignedStatus\": null, \"osSrcProcStartTime\": null, \"osSrcProcStorylineId\": null, \"osSrcProcSubsystem\": null, \"osSrcProcUid\": null, \"osSrcProcUser\": null, \"osSrcProcVerifiedStatus\": null, \"osSrcRegistryChangeCount\": null, \"osSrcTgtFileCreationCount\": null, \"osSrcTgtFileDeletionCount\": null, \"osSrcTgtFileModificationCount\": null, \"parentPid\": null, \"parentProcessName\": \"xxxx.exe\", \"parentProcessStartTime\": \"2022-02-18T11:13:25.373Z\", \"parentProcessUniqueKey\": \"xxxx\", \"pid\": \"xx\", \"processCmd\": \"C:\\xx\\xx\\xxxx.exe -k termsvcs\", \"processDisplayName\": null, \"processGroupId\": \"xxxx\", \"processImagePath\": \"C:\\xx\\xx\\xxxx.exe\", \"processImageSha1Hash\": \"xx\", \"processIntegrityLevel\": \"SYSTEM\", \"processIsRedirectedCommandProcessor\": null, \"processIsWow64\": null, \"processName\": \"xxxx.exe\", \"processRoot\": null, \"processSessionId\": null, \"processStartTime\": \"2022-02-18T11:13:26.812Z\", \"processSubSystem\": null, \"processUniqueKey\": \"xxxx\", \"publisher\": \"MICROSOFT WINDOWS PUBLISHER\", \"registryChangeCount\": null, \"relatedToThreat\": \"False\", \"rpid\": null, \"signatureSignedInvalidReason\": null, \"signedStatus\": \"signed\", \"siteId\": \"xxxx\", \"siteName\": \"Default site\", \"srcIp\": \"1.1.0.0\", \"srcPort\": xx, \"srcProcActiveContentFileId\": null, \"srcProcActiveContentHash\": null, \"srcProcActiveContentPath\": null, \"srcProcActiveContentSignedStatus\": null, \"srcProcActiveContentType\": null, \"srcProcBinaryisExecutable\": null, \"srcProcCmdLine\": \"C:\\xx\\xx\\xxxx.exe -k termsvcs\", \"srcProcDisplayName\": null, \"srcProcImageMd5\": null, \"srcProcImagePath\": \"C:\\xx\\xx\\xxxx.exe\", \"srcProcImageSha1\": \"xxxx\", \"srcProcImageSha256\": null, \"srcProcIntegrityLevel\": \"SYSTEM\", \"srcProcIsNative64Bit\": null, \"srcProcIsRedirectCmdProcessor\": null, \"srcProcIsStorylineRoot\": null, \"srcProcName\": \"xxxx.exe\", \"srcProcParentActiveContentFileId\": null, \"srcProcParentActiveContentHash\": null, \"srcProcParentActiveContentPath\": null, \"srcProcParentActiveContentSignedStatus\": null, \"srcProcParentActiveContentType\": null, \"srcProcParentCmdLine\": null, \"srcProcParentDisplayName\": null, \"srcProcParentImageMd5\": null, \"srcProcParentImagePath\": \"C:\\xx\\xx\\xxxx.exe\", \"srcProcParentImageSha1\": \"xx\", \"srcProcParentImageSha256\": null, \"srcProcParentIntegrityLevel\": null, \"srcProcParentIsNative64Bit\": null, \"srcProcParentIsRedirectCmdProcessor\": null, \"srcProcParentIsStorylineRoot\": null, \"srcProcParentName\": \"xxxx.exe\", \"srcProcParentPid\": null, \"srcProcParentProcUid\": \"xxxx\", \"srcProcParentPublisher\": null, \"srcProcParentReasonSignatureInvalid\": null, \"srcProcParentSessionId\": null, \"srcProcParentSignedStatus\": null, \"srcProcParentStartTime\": \"2022-02-18T11:13:25.373Z\", \"srcProcParentStorylineId\": null, \"srcProcParentUid\": \"xxxx\", \"srcProcParentUser\": null, \"srcProcPid\": \"xx\", \"srcProcPublisher\": \"MICROSOFT WINDOWS PUBLISHER\", \"srcProcReasonSignatureInvalid\": null, \"srcProcRelatedToThreat\": \"False\", \"srcProcRpid\": null, \"srcProcSessionId\": null, \"srcProcSignedStatus\": \"signed\", \"srcProcStartTime\": \"2022-02-18T11:13:26.812Z\", \"srcProcStorylineId\": \"xx\", \"srcProcSubsystem\": null, \"srcProcTid\": null, \"srcProcUid\": \"xx\", \"srcProcUser\": \"NT AUTHORITY\\xxxx\", \"srcProcVerifiedStatus\": \"verified\", \"storyline\": \"xxxx\", \"tgtFileCreationCount\": null, \"tgtFileDeletionCount\": null, \"tgtFileModificationCount\": null, \"tiOriginalEventId\": null, \"tiOriginalEventIndex\": null, \"tiOriginalEventTraceId\": null, \"tid\": null, \"tiindicatorRelatedEventTime\": null, \"traceId\": \"xxxx\", \"trueContext\": \"xxxx\", \"user\": \"NT AUTHORITY\\xxxx\", \"verifiedStatus\": \"verified\" }]"
```

#### STIX Translate results - output
```json
{
    "type": "bundle",
    "id": "bundle--9c4c780d-2237-489a-afbf-18ab4bdf02ab",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "sentinelone",
            "identity_class": "events"
        },
        {
            "id": "observed-data--5bd8f7b5-205d-4855-a5fc-044300ca5c78",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-05T07:35:35.727Z",
            "modified": "2022-04-05T07:35:35.727Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "agent": "xx",
                    "host_ref": "1",
                    "created": "2022-04-03T08:32:05.605Z",
                    "action": "IP Connect",
                    "object_type": "ip",
                    "process_ref": "5",
                    "user_ref": "7"
                },
                "1": {
                    "type": "x-oca-asset",
                    "extensions": {
                        "x-oca-endpoint": {
                            "agent_uuid": "xx",
                            "machine_type": "xx",
                            "endpoint_os": "windows"
                        }
                    },
                    "ip_refs": ["2","4"],
                    "hostname": "xx"
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "xx"
                },
                "3": {
                    "type": "network-traffic",
                    "dst_ref": "2",
                    "dst_port": xx,
                    "extensions": {
                        "x-sentinelone-network-action": {
                            "connection_status": "SUCCESS",
                            "event_direction": "INCOMING"
                        }
                    },
                    "protocols": [
                        "null"
                    ],
                    "src_ref": "4",
                    "src_port": xx
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "xx"
                },
                "5": {
                    "type": "process",
                    "command_line": "C:\\Windows\\System32\\xx -k termsvcs",
                    "extensions": {
                        "x-sentinelone-process": {
                            "image_path": "C:\\Windows\\system32\\xx",
                            "sha1_image": "a1385ce20ad79f55df235effd9780c31442aa234",
                            "integrity_level": "SYSTEM",
                            "parent_image_path": "C:\\Windows\\system32\\xx",
                            "parent_sha1_image": "106a001c4c9820a6aec6a8ba17d3836525faf80e",
                            "parent_process_start_time": "2022-02-18T11:13:25.373Z",
                            "parent_uid": "27717F70F7FD180D",
                            "publisher": "MICROSOFT WINDOWS PUBLISHER",
                            "signed_status": "signed",
                            "story_line_id": "FE6925F54601DFEE",
                            "process_unique_id": "F7562BB2C0064892",
                            "verified_status": "verified"
                        }
                    },
                    "name": "xx",
                    "parent_ref": "6",
                    "pid": xx,
                    "created": "2022-02-18T11:13:26.812Z",
                    "creator_user_ref": "7"
                },
                "6": {
                    "type": "process",
                    "name": "xx"
                },
                "7": {
                    "type": "user-account",
                    "user_id": "NT AUTHORITY\\xx"
                }
            },
            "first_observed": "2022-02-18T11:13:26.812Z",
            "last_observed": "2022-04-05T07:35:35.727Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```

### Multiple Observation  

#### STIX Translate query
```shell
translate sentinelone query {} "([x-oca-event:action = 'Process Creation'] AND [file:size > 1000] OR [x-oca-endpoint:endpoint_os = 'windows'] ) START t'2022-01-01T00:00:00.000000Z' STOP t'2023-02-15T00:00:00.000000Z'"
```

#### STIX Translate query - output

```json
{
    "queries": [
        "{\"query\": \"(eventType = \\\"PROCESS CREATION\\\" AND EventTime  BETWEEN \\\"2022-01-01T00:00:00.000000Z\\\" AND \\\"2023-02-15T00:00:00.000000Z\\\") OR (tgtFileSize > \\\"1000\\\" AND EventTime  BETWEEN \\\"2022-01-01T00:00:00.000000Z\\\" AND \\\"2023-02-15T00:00:00.000000Z\\\") OR (endpointOs = \\\"WINDOWS\\\" AND EventTime  BETWEEN \\\"2022-01-01T00:00:00.000000Z\\\" AND \\\"2023-02-15T00:00:00.000000Z\\\")\", \"fromDate\": \"2022-01-01T00:00:00.000000Z\", \"toDate\": \"2023-02-15T00:00:00.000000Z\", \"limit\": 10000}"
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
"{\"query\": \"(eventType = \\\"PROCESS CREATION\\\" AND EventTime  BETWEEN \\\"2022-01-01T00:00:00.000000Z\\\" AND \\\"2023-02-15T00:00:00.000000Z\\\") OR (tgtFileSize > \\\"1000\\\" AND EventTime  BETWEEN \\\"2022-01-01T00:00:00.000000Z\\\" AND \\\"2023-02-15T00:00:00.000000Z\\\") OR (endpointOs = \\\"WINDOWS\\\" AND EventTime  BETWEEN \\\"2022-01-01T00:00:00.000000Z\\\" AND \\\"2023-02-15T00:00:00.000000Z\\\")\", \"fromDate\": \"2022-01-01T00:00:00.000000Z\", \"toDate\": \"2023-02-15T00:00:00.000000Z\", \"limit\": 10000}"
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
    "status": "FINISHED",
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
3
```

#### STIX Transmit results - output
```json
{
    "success": true,
    "data": [
        {
            "agentDomain": "WORKGROUP",
            "agentGroupId": "1336793312883045044",
            "agentId": "xx",
            "agentInfected": false,
            "agentIp": "xx",
            "agentIsActive": true,
            "agentIsDecommissioned": false,
            "agentMachineType": "xx",
            "agentName": "xx",
            "agentNetworkStatus": "connected",
            "agentOs": "windows",
            "agentTimestamp": "2022-04-05T07:52:02.051Z",
            "agentUuid": "209e5033aedc4d50b3c056e0a01a9841",
            "connectionStatus": "SUCCESS",
            "createdAt": "2022-04-05T07:52:02.051000Z",
            "direction": "INCOMING",
            "dstIp": "xx",
            "dstPort": xx,
            "endpointMachineType": "server",
            "endpointName": "xx",
            "endpointOs": "windows",
            "eventIndex": "xx",
            "eventTime": "2022-04-05T07:52:02.051Z",
            "eventType": "IP Connect",
            "id": "xx",
            "metaEventName": "TCPV4",
            "netConnStatus": "SUCCESS",
            "netEventDirection": "INCOMING",
            "netProtocolName": "null",
            "objectType": "ip",
            "osSrcProcRelatedToThreat": "False",
            "parentProcessName": "xx",
            "parentProcessStartTime": "2022-02-18T11:13:25.373Z",
            "parentProcessUniqueKey": "F7562BB2C0064892",
            "pid": "xx",
            "processCmd": "C:\\Windows\\System32\\xx -k termsvcs",
            "processGroupId": "FE6925F54601DFEE",
            "processImagePath": "C:\\Windows\\system32\\xx",
            "processImageSha1Hash": "a1385ce20ad79f55df235effd9780c31442aa234",
            "processIntegrityLevel": "SYSTEM",
            "processName": "xx",
            "processStartTime": "2022-02-18T11:13:26.812Z",
            "processUniqueKey": "F7562BB2C0064892",
            "publisher": "MICROSOFT WINDOWS PUBLISHER",
            "relatedToThreat": "False",
            "signedStatus": "signed",
            "siteId": "1336793312849490611",
            "siteName": "Default site",
            "srcIp": "xx",
            "srcPort": xx,
            "srcProcCmdLine": "C:\\Windows\\System32\\xx -k termsvcs",
            "srcProcImagePath": "C:\\Windows\\system32\\xx",
            "srcProcImageSha1": "a1385ce20ad79f55df235effd9780c31442aa234",
            "srcProcIntegrityLevel": "SYSTEM",
            "srcProcName": "svchost.exe",
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
            "srcProcUid": "F7562BB2C0064892",
            "srcProcUser": "NT AUTHORITY\\xx",
            "srcProcVerifiedStatus": "verified",
            "storyline": "FE6925F54601DFEE",
            "traceId": "01FZWBAGRDMGQ2P37MEGJSW1FY",
            "trueContext": "FE6925F54601DFEE",
            "user": "NT AUTHORITY\\NETWORK SERVICE",
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
{\"type\":\"identity\",\"id\":\"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\",\"name\":\"sentinelone\",\"identity_class\":\"events\"}
"[{ \"accountId\": null, \"activeContentFileId\": null, \"activeContentHash\": null, \"activeContentPath\": null, \"activeContentSignedStatus\": null, \"activeContentType\": null, \"agentDomain\": \"WORKGROUP\", \"agentGroupId\": \"xxxx\", \"agentId\": \"xxxx\", \"agentInfected\": false, \"agentIp\": \"1.1.0.0\", \"agentIsActive\": true, \"agentIsDecommissioned\": false, \"agentMachineType\": \"server\", \"agentName\": \"xxxx\", \"agentNetworkStatus\": \"connected\", \"agentOs\": \"windows\", \"agentTimestamp\": \"2022-03-06T22:16:26.998Z\", \"agentUuid\": \"xxxx\", \"agentVersion\": null, \"childProcCount\": null, \"createdAt\": \"2022-03-06T22:16:26.998000Z\", \"crossProcCount\": null, \"crossProcDupRemoteProcHandleCount\": null, \"crossProcDupThreadHandleCount\": null, \"crossProcOpenProcCount\": null, \"crossProcOutOfStorylineCount\": null, \"crossProcThreadCreateCount\": null, \"dnsCount\": null, \"endpointMachineType\": \"server\", \"endpointName\": \"xxxx\", \"endpointOs\": \"windows\", \"eventIndex\": \"xxxx\", \"eventTime\": \"2022-03-06T22:16:26.998Z\", \"eventType\": \"Process Creation\", \"fileIsExecutable\": null, \"fileMd5\": null, \"fileSha256\": null, \"id\": \"xxxxx\", \"indicatorBootConfigurationUpdateCount\": null, \"indicatorEvasionCount\": null, \"indicatorExploitationCount\": null, \"indicatorGeneralCount\": null, \"indicatorInfostealerCount\": null, \"indicatorInjectionCount\": null, \"indicatorPersistenceCount\": null, \"indicatorPostExploitationCount\": null, \"indicatorRansomwareCount\": null, \"indicatorReconnaissanceCount\": null, \"lastActivatedAt\": null, \"loginAccountDomain\": \"-\", \"loginAccountName\": \"-\", \"loginAccountSid\": \"S-1-0-0\", \"loginFailureReason\": \"Unknown user name or bad password.\", \"loginIsAdministratorEquivalent\": null, \"loginIsSuccessful\": \"False\", \"loginSessionId\": null, \"loginType\": \"NETWORK\", \"loginsBaseType\": null, \"loginsUserName\": \"xxxx\", \"metaEventName\": \"WINLOGONATTEMPT\", \"moduleCount\": null, \"netConnCount\": null, \"netConnInCount\": null, \"netConnOutCount\": null, \"objectType\": \"logins\", \"osSrcChildProcCount\": null, \"osSrcCrossProcCount\": null, \"osSrcCrossProcDupRemoteProcHandleCount\": null, \"osSrcCrossProcDupThreadHandleCount\": null, \"osSrcCrossProcOpenProcCount\": null, \"osSrcCrossProcOutOfStorylineCount\": null, \"osSrcCrossProcThreadCreateCount\": null, \"osSrcDnsCount\": null, \"osSrcIndicatorBootConfigurationUpdateCount\": null, \"osSrcIndicatorEvasionCount\": null, \"osSrcIndicatorExploitationCount\": null, \"osSrcIndicatorGeneralCount\": null, \"osSrcIndicatorInfostealerCount\": null, \"osSrcIndicatorInjectionCount\": null, \"osSrcIndicatorPersistenceCount\": null, \"osSrcIndicatorPostExploitationCount\": null, \"osSrcIndicatorRansomwareCount\": null, \"osSrcIndicatorReconnaissanceCount\": null, \"osSrcModuleCount\": null, \"osSrcNetConnCount\": null, \"osSrcNetConnInCount\": null, \"osSrcNetConnOutCount\": null, \"osSrcProcActiveContentFileId\": null, \"osSrcProcActiveContentHash\": null, \"osSrcProcActiveContentPath\": null, \"osSrcProcActiveContentSignedStatus\": null, \"osSrcProcActiveContentType\": null, \"osSrcProcBinaryisExecutable\": null, \"osSrcProcCmdLine\": null, \"osSrcProcDisplayName\": null, \"osSrcProcImageMd5\": null, \"osSrcProcImagePath\": null, \"osSrcProcImageSha1\": null, \"osSrcProcImageSha256\": null, \"osSrcProcIntegrityLevel\": null, \"osSrcProcIsNative64Bit\": null, \"osSrcProcIsRedirectCmdProcessor\": null, \"osSrcProcIsStorylineRoot\": null, \"osSrcProcName\": null, \"osSrcProcParentActiveContentFileId\": null, \"osSrcProcParentActiveContentHash\": null, \"osSrcProcParentActiveContentPath\": null, \"osSrcProcParentActiveContentSignedStatus\": null, \"osSrcProcParentActiveContentType\": null, \"osSrcProcParentCmdLine\": null, \"osSrcProcParentDisplayName\": null, \"osSrcProcParentImageMd5\": null, \"osSrcProcParentImagePath\": null, \"osSrcProcParentImageSha1\": null, \"osSrcProcParentImageSha256\": null, \"osSrcProcParentIntegrityLevel\": null, \"osSrcProcParentIsNative64Bit\": null, \"osSrcProcParentIsRedirectCmdProcessor\": null, \"osSrcProcParentIsStorylineRoot\": null, \"osSrcProcParentName\": null, \"osSrcProcParentPid\": null, \"osSrcProcParentPublisher\": null, \"osSrcProcParentReasonSignatureInvalid\": null, \"osSrcProcParentSessionId\": null, \"osSrcProcParentSignedStatus\": null, \"osSrcProcParentStartTime\": null, \"osSrcProcParentStorylineId\": null, \"osSrcProcParentUid\": null, \"osSrcProcParentUser\": null, \"osSrcProcPid\": null, \"osSrcProcPublisher\": null, \"osSrcProcReasonSignatureInvalid\": null, \"osSrcProcRelatedToThreat\": \"False\", \"osSrcProcSessionId\": null, \"osSrcProcSignedStatus\": null, \"osSrcProcStartTime\": null, \"osSrcProcStorylineId\": null, \"osSrcProcSubsystem\": null, \"osSrcProcUid\": null, \"osSrcProcUser\": null, \"osSrcProcVerifiedStatus\": null, \"osSrcRegistryChangeCount\": null, \"osSrcTgtFileCreationCount\": null, \"osSrcTgtFileDeletionCount\": null, \"osSrcTgtFileModificationCount\": null, \"parentPid\": null, \"parentProcessName\": \"xxxx.exe\", \"parentProcessStartTime\": \"2022-02-18T11:13:25.373Z\", \"parentProcessUniqueKey\": \"xxxx\", \"pid\": \"xx\", \"processCmd\": \"C:\\xx\\xx\\xxxx.exe -k termsvcs\", \"processDisplayName\": null, \"processGroupId\": \"xxxx\", \"processImagePath\": \"C:\\xx\\xx\\xxxx.exe\", \"processImageSha1Hash\": \"xxxx\", \"processIntegrityLevel\": \"SYSTEM\", \"processIsRedirectedCommandProcessor\": null, \"processIsWow64\": null, \"processName\": \"xxxx.exe\", \"processRoot\": null, \"processSessionId\": null, \"processStartTime\": \"2022-02-18T11:13:26.812Z\", \"processSubSystem\": null, \"processUniqueKey\": \"xxxx\", \"publisher\": \"MICROSOFT WINDOWS PUBLISHER\", \"registryChangeCount\": null, \"relatedToThreat\": \"False\", \"rpid\": null, \"signatureSignedInvalidReason\": null, \"signedStatus\": \"signed\", \"siteId\": \"xxxx\", \"siteName\": \"Default site\", \"srcMachineIp\": \"1.1.0.0\", \"srcProcActiveContentFileId\": null, \"srcProcActiveContentHash\": null, \"srcProcActiveContentPath\": null, \"srcProcActiveContentSignedStatus\": null, \"srcProcActiveContentType\": null, \"srcProcBinaryisExecutable\": null, \"srcProcCmdLine\": \"C:\\xx\\xx\\xxxx.exe -k termsvcs\", \"srcProcDisplayName\": null, \"srcProcImageMd5\": null, \"srcProcImagePath\": \"C:\\xx\\xx\\xxxx.exe\", \"srcProcImageSha1\": \"xxxx\", \"srcProcImageSha256\": null, \"srcProcIntegrityLevel\": \"SYSTEM\", \"srcProcIsNative64Bit\": null, \"srcProcIsRedirectCmdProcessor\": null, \"srcProcIsStorylineRoot\": null, \"srcProcName\": \"xxxx.exe\", \"srcProcParentActiveContentFileId\": null, \"srcProcParentActiveContentHash\": null, \"srcProcParentActiveContentPath\": null, \"srcProcParentActiveContentSignedStatus\": null, \"srcProcParentActiveContentType\": null, \"srcProcParentCmdLine\": null, \"srcProcParentDisplayName\": null, \"srcProcParentImageMd5\": null, \"srcProcParentImagePath\": \"C:\\xx\\xx\\xxxx.exe\", \"srcProcParentImageSha1\": \"xxxx\", \"srcProcParentImageSha256\": null, \"srcProcParentIntegrityLevel\": null, \"srcProcParentIsNative64Bit\": null, \"srcProcParentIsRedirectCmdProcessor\": null, \"srcProcParentIsStorylineRoot\": null, \"srcProcParentName\": \"xxxx.exe\", \"srcProcParentPid\": null, \"srcProcParentProcUid\": \"xxxx\", \"srcProcParentPublisher\": null, \"srcProcParentReasonSignatureInvalid\": null, \"srcProcParentSessionId\": null, \"srcProcParentSignedStatus\": null, \"srcProcParentStartTime\": \"2022-02-18T11:13:25.373Z\", \"srcProcParentStorylineId\": null, \"srcProcParentUid\": \"xxxx\", \"srcProcParentUser\": null, \"srcProcPid\": \"xx\", \"srcProcPublisher\": \"MICROSOFT WINDOWS PUBLISHER\", \"srcProcReasonSignatureInvalid\": null, \"srcProcRelatedToThreat\": \"False\", \"srcProcRpid\": null, \"srcProcSessionId\": null, \"srcProcSignedStatus\": \"signed\", \"srcProcStartTime\": \"2022-02-18T11:13:26.812Z\", \"srcProcStorylineId\": \"xxxx\", \"srcProcSubsystem\": null, \"srcProcTid\": null, \"srcProcUid\": \"F7562BB2C0064892\", \"srcProcUser\": \"NT AUTHORITY\\xxxx\", \"srcProcVerifiedStatus\": \"verified\", \"storyline\": \"xxxx\", \"tgtFileCreationCount\": null, \"tgtFileDeletionCount\": null, \"tgtFileModificationCount\": null, \"tiOriginalEventId\": null, \"tiOriginalEventIndex\": null, \"tiOriginalEventTraceId\": null, \"tid\": null, \"tiindicatorRelatedEventTime\": null, \"traceId\": \"xxxx\", \"trueContext\": \"xxxx\", \"user\": \"NT AUTHORITY\\xxxx\", \"verifiedStatus\": \"verified\" }  ]"
```

#### STIX Translate results - output
```json
{
    "type": "bundle",
    "id": "bundle--245724b9-0860-4099-b24c-0dd298eeff4a",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "sentinelone",
            "identity_class": "events"
        },
        {
            "id": "observed-data--08187b26-000a-4ce5-8da6-37b388bdbbf2",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-05T08:10:53.159Z",
            "modified": "2022-04-05T08:10:53.159Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "agent": "xx",
                    "host_ref": "1",
                    "created": "2022-04-05T07:52:02.051Z",
                    "action": "IP Connect",
                    "object_type": "ip",
                    "process_ref": "5",
                    "user_ref": "7"
                },
                "1": {
                    "type": "x-oca-asset",
                    "extensions": {
                        "x-oca-endpoint": {
                            "agent_uuid": "209e5033aedc4d50b3c056e0a01a9841",
                            "machine_type": "xx",
                            "endpoint_os": "windows"
                        }
                    },
                    "ip_refs": ["2","4"],
                    "hostname": "xx"
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "xx"
                },
                "3": {
                    "type": "network-traffic",
                    "dst_ref": "2",
                    "dst_port": xx,
                    "extensions": {
                        "x-sentinelone-network-action": {
                            "connection_status": "SUCCESS",
                            "event_direction": "INCOMING"
                        }
                    },
                    "protocols": [
                        "null"
                    ],
                    "src_ref": "4",
                    "src_port": xx
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "xx"
                },
                "5": {
                    "type": "process",
                    "command_line": "C:\\Windows\\System32\\xx -k termsvcs",
                    "extensions": {
                        "x-sentinelone-process": {
                            "image_path": "C:\\Windows\\system32\\xx",
                            "sha1_image": "a1385ce20ad79f55df235effd9780c31442aa234",
                            "integrity_level": "SYSTEM",
                            "parent_image_path": "C:\\Windows\\system32\\xx",
                            "parent_sha1_image": "106a001c4c9820a6aec6a8ba17d3836525faf80e",
                            "parent_process_start_time": "2022-02-18T11:13:25.373Z",
                            "parent_uid": "27717F70F7FD180D",
                            "publisher": "MICROSOFT WINDOWS PUBLISHER",
                            "signed_status": "signed",
                            "story_line_id": "FE6925F54601DFEE",
                            "process_unique_id": "F7562BB2C0064892",
                            "verified_status": "verified"
                        }
                    },
                    "name": "xx",
                    "parent_ref": "6",
                    "pid": xx,
                    "created": "2022-02-18T11:13:26.812Z",
                    "creator_user_ref": "7"
                },
                "6": {
                    "type": "process",
                    "name": "xx"
                },
                "7": {
                    "type": "user-account",
                    "user_id": "NT AUTHORITY\\xx"
                }
            },
            "first_observed": "2022-02-18T11:13:26.812Z",
            "last_observed": "2022-04-05T08:10:53.159Z",
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
    "id": "bundle--7c5100bb-12cb-44c8-b5ed-48a37b58b385",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "sentinelone",
            "identity_class ": "events"
        },
        {
            "id": "observed-data--c76c61f3-720d-4856-a27e-2c61bf6ee229",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-04-05T08:32:42.894Z",
            "modified": "2022-04-05T08:32:42.894Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "agent": "xx",
                    "host_ref": "1",
                    "created": "2022-04-04T04:55:40.896Z",
                    "action": "Process Creation",
                    "object_type": "process",
                    "process_ref": "2",
                    "user_ref": "4"
                },
                "1": {
                    "type": "x-oca-asset",
                    "extensions": {
                        "x-oca-endpoint": {
                            "agent_uuid": "209e5033aedc4d50b3c056e0a01a9841",
                            "machine_type": "xx",
                            "endpoint_os": "windows"
                        }
                    },
                    "hostname": "xx"
                },
                "2": {
                    "type": "process",
                    "command_line": "C:\\Windows\\system32\\xx -k netsvcs -p",
                    "extensions": {
                        "x-sentinelone-process": {
                            "image_path": "C:\\Program Files (x86)\\Google\\Update\\xx",
                            "sha1_image": "a1385ce20ad79f55df235effd9780c31442aa234",
                            "integrity_level": "SYSTEM",
                            "parent_image_path": "C:\\Windows\\system32\\xx",
                            "parent_sha1_image": "106a001c4c9820a6aec6a8ba17d3836525faf80e",
                            "parent_process_start_time": "2022-02-18T11:13:25.373Z",
                            "parent_uid": "27717F70F7FD180D",
                            "publisher": "MICROSOFT WINDOWS PUBLISHER",
                            "signed_status": "signed",
                            "story_line_id": "456BE601CF03E0AF",
                            "process_unique_id": "337BF507ABE4D3BC",
                            "verified_status": "verified"
                        }
                    },
                    "name": "xx",
                    "parent_ref": "3",
                    "pid": xx,
                    "created": "2022-02-18T11:13:27.453Z",
                    "creator_user_ref": "4"
                },
                "3": {
                    "type": "process",
                    "name": "xx"
                },
                "4": {
                    "type": "user-account",
                    "user_id": "NT AUTHORITY\\xx"
                }
            },
            "first_observed": "2022-04-04T04:55:21.942Z",
            "last_observed": "2022-04-05T08:32:42.894Z",
            "number_observed": 1
}
```

### Limitations
- Default data retention in sentinelone deep visibility is 14 days.

### References
- [SentinelOne](#https://www.sentinelone.com/)