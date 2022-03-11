# Cybereason Connector

**Table of Contents**

- [Cybereason API Endpoints](#cybereason-api-endpoints)
- [Pattern expression with STIX attributes - Single Observation](#single-observation)
- [Pattern expression with STIX attributes - Multiple Observation](#multiple-observation)
- [Pattern expression with STIX attributes - Execute Query](#stix-execute-query)
- [Pattern expression with STIX attributes - Ping Query](#stix-ping-query)
- [Limitations](#limitations)
- [Observations](#observations)

### Cybereason API Endpoints

   |Connector Method|Cybereason API Endpoint| Method
   | ----           |   ------              | -----|
   |Login Endpoint  |https://\<your server\>/login.html|POST
   |Query Endpoint|https://\<your server\>/rest/visualsearch/query/simple|POST
   |Logout Endpoint|https://\<your server\>/logout|GET
###Format for calling stix-shifter from the command line
python main.py `<translator_module>` `<query or result>` `<STIX identity object>` `<data>`

### Pattern expression with STIX attributes

### Single Observation

####STIX Translate query
```shell
translate cybereason query '{}' "[ipv4-addr:value = '1.1.0.0'] START t'2021-10-01T11:00:00.000Z' STOP t'2021-10-07T11:00:00.003Z'"
```
#### STIX Translate query - output
```json
{
    "queries": [
        {
            "queryPath": [
                {
                    "requestedType": "Connection",
                    "filters": [
                        {
                            "facetName": "localAddress",
                            "filterType": "Equals",
                            "values": [
                                "1.1.0.0"
                            ]
                        },
                        {
                            "facetName": "creationTime",
                            "filterType": "Between",
                            "values": [
                                1633086000000,
                                1633604400003
                            ]
                        }
                    ],
                    "isResult": true
                }
            ],
            "queryLimits": {
                "groupingFeature": {
                    "elementInstanceType": "Connection",
                    "featureName": "elementDisplayName"
                }
            },
            "perFeatureLimit": 1,
            "totalResultLimit": 9999,
            "perGroupLimit": 1,
            "templateContext": "CUSTOM",
            "customFields": [
                "elementDisplayName",
                "direction",
                "ownerMachine",
                "ownerProcess",
                "serverPort",
                "serverAddress",
                "portType",
                "aggregatedReceivedBytesCount",
                "aggregatedTransmittedBytesCount",
                "remoteAddressCountryName",
                "dnsQuery",
                "calculatedCreationTime",
                "domainName",
                "endTime",
                "localPort",
                "portDescription",
                "remotePort",
                "state",
                "isExternalConnection",
                "isIncoming",
                "remoteAddressInternalExternalLocal",
                "transportProtocol",
                "hasMalops",
                "hasSuspicions",
                "relatedToMalop",
                "isWellKnownPort",
                "isProcessLegit",
                "isProcessMalware",
                "localAddress",
                "remoteAddress",
                "urlDomains"
            ]
        },
        {
            "queryPath": [
                {
                    "requestedType": "Connection",
                    "filters": [
                        {
                            "facetName": "remoteAddress",
                            "filterType": "Equals",
                            "values": [
                                "127.0.0.1"
                            ]
                        },
                        {
                            "facetName": "creationTime",
                            "filterType": "Between",
                            "values": [
                                1633086000000,
                                1633604400003
                            ]
                        }
                    ],
                    "isResult": true
                }
            ],
            "queryLimits": {
                "groupingFeature": {
                    "elementInstanceType": "Connection",
                    "featureName": "elementDisplayName"
                }
            },
            "perFeatureLimit": 1,
            "totalResultLimit": 9999,
            "perGroupLimit": 1,
            "templateContext": "CUSTOM",
            "customFields": [
                "elementDisplayName",
                "direction",
                "ownerMachine",
                "ownerProcess",
                "serverPort",
                "serverAddress",
                "portType",
                "aggregatedReceivedBytesCount",
                "aggregatedTransmittedBytesCount",
                "remoteAddressCountryName",
                "dnsQuery",
                "calculatedCreationTime",
                "domainName",
                "endTime",
                "localPort",
                "portDescription",
                "remotePort",
                "state",
                "isExternalConnection",
                "isIncoming",
                "remoteAddressInternalExternalLocal",
                "transportProtocol",
                "hasMalops",
                "hasSuspicions",
                "relatedToMalop",
                "isWellKnownPort",
                "isProcessLegit",
                "isProcessMalware",
                "localAddress",
                "remoteAddress",
                "urlDomains"
            ]
        }
    ]
}
```
#### STIX Transmit query

```shell
transmit
cybereason
"{\"host\":\"xx.xx.xx\",\"port\": xxxx}"
"{\"auth\":{\"username\": \"xxxxx\", \"password\": \"xxxx\"}}"
results
"{ \"queryPath\": [ { \"requestedType\": \"Connection\", \"filters\": [ { \"facetName\": \"localAddress\", \"filterType\": \"Equals\", \"values\": [ \"1.1.0.0\" ] }, { \"facetName\": \"creationTime\", \"filterType\": \"Between\", \"values\": [ 1633086000000, 1633604400003 ] } ], \"isResult\": true } ], \"queryLimits\": { \"groupingFeature\": { \"elementInstanceType\": \"Connection\", \"featureName\": \"elementDisplayName\" } }, \"perFeatureLimit\": 1, \"totalResultLimit\": 9999, \"perGroupLimit\": 1, \"templateContext\": \"CUSTOM\", \"customFields\": [ \"elementDisplayName\", \"direction\", \"ownerMachine\", \"ownerProcess\", \"serverPort\", \"serverAddress\", \"portType\", \"aggregatedReceivedBytesCount\", \"aggregatedTransmittedBytesCount\", \"remoteAddressCountryName\", \"dnsQuery\", \"calculatedCreationTime\", \"domainName\", \"endTime\", \"localPort\", \"portDescription\", \"remotePort\", \"state\", \"isExternalConnection\", \"isIncoming\", \"remoteAddressInternalExternalLocal\", \"transportProtocol\", \"hasMalops\", \"hasSuspicions\", \"relatedToMalop\", \"isWellKnownPort\", \"isProcessLegit\", \"isProcessMalware\", \"localAddress\", \"remoteAddress\", \"urlDomains\" ] }, { \"queryPath\": [ { \"requestedType\": \"Connection\", \"filters\": [ { \"facetName\": \"remoteAddress\", \"filterType\": \"Equals\", \"values\": [ \"127.0.0.1\" ] }, { \"facetName\": \"creationTime\", \"filterType\": \"Between\", \"values\": [ 1633086000000, 1633604400003 ] } ], \"isResult\": true } ], \"queryLimits\": { \"groupingFeature\": { \"elementInstanceType\": \"Connection\", \"featureName\": \"elementDisplayName\" } }, \"perFeatureLimit\": 1, \"totalResultLimit\": 9999, \"perGroupLimit\": 1, \"templateContext\": \"CUSTOM\", \"customFields\": [ \"elementDisplayName\", \"direction\", \"ownerMachine\", \"ownerProcess\", \"serverPort\", \"serverAddress\", \"portType\", \"aggregatedReceivedBytesCount\", \"aggregatedTransmittedBytesCount\", \"remoteAddressCountryName\", \"dnsQuery\", \"calculatedCreationTime\", \"domainName\", \"endTime\", \"localPort\", \"portDescription\", \"remotePort\", \"state\", \"isExternalConnection\", \"isIncoming\", \"remoteAddressInternalExternalLocal\", \"transportProtocol\", \"hasMalops\", \"hasSuspicions\", \"relatedToMalop\", \"isWellKnownPort\", \"isProcessLegit\", \"isProcessMalware\", \"localAddress\", \"remoteAddress\", \"urlDomains\" ] }" 
0 2
```

#### STIX Transmit query - output
```json
{"success":true,
"data":[
	{"Connection":{"hasSuspicions":"false","isProcessLegit":"true","aggregatedReceivedBytesCount":"1225449","remotePort":"443","state":"CONNECTION_OPEN","portType":"SERVICE_HTTP","transportProtocol":"TCP","elementDisplayName":"1.1.0.0:50799 > 52.226.139.180:443","aggregatedTransmittedBytesCount":"724812","isWellKnownPort":"true","isExternalConnection":"true","localPort":"50799","remoteAddressInternalExternalLocal":"EXTERNAL","endTime":"1635034091852","serverAddress":"52.226.139.180","portDescription":"Hypertext Transfer Protocol over TLS\/SSL (HTTPS)","serverPort":"443","isIncoming":"false","calculatedCreationTime":"1633093769591","hasMalops":"false","direction":"OUTGOING","isProcessMalware":"false","localAddress":"1.1.0.0","domainName":"client.wns.windows.com","remoteAddress":"52.226.139.180","ownerMachine":"d3cyber-win10-1","ownerProcess":"svchost.exe","dnsQuery":"client.wns.windows.com > 52.226.139.180","urlDomains":["wns2-bl2p.wns.windows.com","client.wns.windows.com"]}},
	{"Connection":{"hasSuspicions":"false","isProcessLegit":"true","aggregatedReceivedBytesCount":"183141","remotePort":"443","state":"CONNECTION_OPEN","portType":"SERVICE_HTTP","transportProtocol":"TCP","elementDisplayName":"1.1.0.0:57412 > 40.83.240.146:443","aggregatedTransmittedBytesCount":"106995","isWellKnownPort":"true","isExternalConnection":"true","localPort":"57412","remoteAddressInternalExternalLocal":"EXTERNAL","endTime":"1634996831727","serverAddress":"40.83.240.146","portDescription":"Hypertext Transfer Protocol over TLS\/SSL (HTTPS)","serverPort":"443","isIncoming":"false","calculatedCreationTime":"1633417907599","hasMalops":"false","direction":"OUTGOING","isProcessMalware":"false","localAddress":"1.1.0.0","domainName":"client.wns.windows.com","remoteAddress":"40.83.240.146","ownerMachine":"d3cyber-win10-1","ownerProcess":"svchost.exe","dnsQuery":"client.wns.windows.com > 40.83.240.146","urlDomains":"client.wns.windows.com"}}
    ]
}

```
#### STIX Translate results

```shell
translate cybereason results 
"{\"type\":\"identity\",\"id\":\"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\",\"name\":\"cybereason\",\"identity_class\":\"events\"}" 
"[ { \"Connection\": { \"hasSuspicions\": \"false\", \"isProcessLegit\": \"true\", \"aggregatedReceivedBytesCount\": \"1225449\", \"remotePort\": \"443\", \"state\": \"CONNECTION_OPEN\", \"portType\": \"SERVICE_HTTP\", \"transportProtocol\": \"TCP\", \"elementDisplayName\": \"1.1.0.0:50799 > 52.226.139.180:443\", \"aggregatedTransmittedBytesCount\": \"724812\", \"isWellKnownPort\": \"true\", \"isExternalConnection\": \"true\", \"localPort\": \"50799\", \"remoteAddressInternalExternalLocal\": \"EXTERNAL\", \"endTime\": \"1635034091852\", \"serverAddress\": \"52.226.139.180\", \"portDescription\": \"Hypertext Transfer Protocol over TLS/SSL (HTTPS)\", \"serverPort\": \"443\", \"isIncoming\": \"false\", \"calculatedCreationTime\": \"1633093769591\", \"hasMalops\": \"false\", \"direction\": \"OUTGOING\", \"isProcessMalware\": \"false\", \"localAddress\": \"1.1.0.0\", \"domainName\": \"client.wns.windows.com\", \"remoteAddress\": \"52.226.139.180\", \"ownerMachine\": \"d3cyber-win10-1\", \"ownerProcess\": \"svchost.exe\", \"dnsQuery\": \"client.wns.windows.com > 52.226.139.180\", \"urlDomains\": [ \"wns2-bl2p.wns.windows.com\", \"client.wns.windows.com\" ] } }, { \"Connection\": { \"hasSuspicions\": \"false\", \"isProcessLegit\": \"true\", \"aggregatedReceivedBytesCount\": \"183141\", \"remotePort\": \"443\", \"state\": \"CONNECTION_OPEN\", \"portType\": \"SERVICE_HTTP\", \"transportProtocol\": \"TCP\", \"elementDisplayName\": \"1.1.0.0:57412 > 40.83.240.146:443\", \"aggregatedTransmittedBytesCount\": \"106995\", \"isWellKnownPort\": \"true\", \"isExternalConnection\": \"true\", \"localPort\": \"57412\", \"remoteAddressInternalExternalLocal\": \"EXTERNAL\", \"endTime\": \"1634996831727\", \"serverAddress\": \"40.83.240.146\", \"portDescription\": \"Hypertext Transfer Protocol over TLS/SSL (HTTPS)\", \"serverPort\": \"443\", \"isIncoming\": \"false\", \"calculatedCreationTime\": \"1633417907599\", \"hasMalops\": \"false\", \"direction\": \"OUTGOING\", \"isProcessMalware\": \"false\", \"localAddress\": \"1.1.0.0\", \"domainName\": \"client.wns.windows.com\", \"remoteAddress\": \"40.83.240.146\", \"ownerMachine\": \"d3cyber-win10-1\", \"ownerProcess\": \"svchost.exe\", \"dnsQuery\": \"client.wns.windows.com > 40.83.240.146\", \"urlDomains\": \"client.wns.windows.com\" } } ]" 
```

#### STIX Translate results - output
```json
{
    "type": "bundle",
    "id": "bundle--8a2847d1-6eb6-4e8b-8d74-a190648449ef",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "cybereason",
            "identity_class": "events"
        },
        {
            "id": "observed-data--8e8500d7-c46b-46eb-a414-2610e5e5b4d3",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2021-12-27T10:26:17.736Z",
            "modified": "2021-12-27T10:26:17.736Z",
            "objects": {
                "0": {
                    "type": "x-cybereason-malops",
                    "suspicions": "false",
                    "malops": "false",
                    "malware_process": "false"
                },
                "1": {
                    "type": "network-traffic",
                    "extensions": {
                        "x-cybereason-connection": {
                            "legit_process": "true",
                            "state": "CONNECTION_OPEN",
                            "port_type": "SERVICE_HTTP",
                            "well_known_port": "true",
                            "external_connection": "true",
                            "remote_address_type": "EXTERNAL",
                            "port_description": "Hypertext Transfer Protocol over TLS/SSL (HTTPS)",
                            "incoming": "false",
                            "direction": "OUTGOING",
                            "dns_query": "client.wns.windows.com > 52.226.139.180",
                            "url_domain": [
                                "wns2-bl2p.wns.windows.com",
                                "client.wns.windows.com"
                            ]
                        }
                    },
                    "dst_byte_count": 1225449,
                    "dst_port": 443,
                    "protocols": [
                        "tcp"
                    ],
                    "src_byte_count": 724812,
                    "src_port": 50799,
                    "end": "2021-10-24T00:08:11.852Z",
                    "start": "2021-10-01T13:09:29.591Z",
                    "src_ref": "3",
                    "dst_ref": "5"
                },
                "2": {
                    "type": "x-oca-event",
                    "network_ref": "1",
                    "machine": "d3cyber-win10-1",
                    "process_ref": "7",
                    "domain_ref": "4"
                },
                "3": {
                    "type": "ipv4-addr",
                    "value": "1.1.0.0"
                },
                "4": {
                    "type": "domain-name",
                    "value": "client.wns.windows.com"
                },
                "5": {
                    "type": "ipv4-addr",
                    "value": "52.226.139.180"
                },
                "6": {
                    "type": "file",
                    "name": "svchost.exe"
                },
                "7": {
                    "type": "process",
                    "name": "svchost.exe",
                    "binary_ref": "6"
                }
            },
            "last_observed": "2021-10-24T00:08:11.852Z",
            "first_observed": "2021-10-01T13:09:29.591Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--0fdb6b35-17ae-47bf-a0c4-8cdc271cb77d",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2021-12-27T10:26:21.517Z",
            "modified": "2021-12-27T10:26:21.517Z",
            "objects": {
                "0": {
                    "type": "x-cybereason-malops",
                    "suspicions": "false",
                    "malops": "false",
                    "malware_process": "false"
                },
                "1": {
                    "type": "network-traffic",
                    "extensions": {
                        "x-cybereason-connection": {
                            "legit_process": "true",
                            "state": "CONNECTION_OPEN",
                            "port_type": "SERVICE_HTTP",
                            "well_known_port": "true",
                            "external_connection": "true",
                            "remote_address_type": "EXTERNAL",
                            "port_description": "Hypertext Transfer Protocol over TLS/SSL (HTTPS)",
                            "incoming": "false",
                            "direction": "OUTGOING",
                            "dns_query": "client.wns.windows.com > 40.83.240.146",
                            "url_domain": "client.wns.windows.com"
                        }
                    },
                    "dst_byte_count": 183141,
                    "dst_port": 443,
                    "protocols": [
                        "tcp"
                    ],
                    "src_byte_count": 106995,
                    "src_port": 57412,
                    "end": "2021-10-23T13:47:11.727Z",
                    "start": "2021-10-05T07:11:47.599Z",
                    "src_ref": "3",
                    "dst_ref": "5"
                },
                "2": {
                    "type": "x-oca-event",
                    "network_ref": "1",
                    "machine": "d3cyber-win10-1",
                    "process_ref": "7",
                    "domain_ref": "4"
                },
                "3": {
                    "type": "ipv4-addr",
                    "value": "1.1.0.0"
                },
                "4": {
                    "type": "domain-name",
                    "value": "client.wns.windows.com"
                },
                "5": {
                    "type": "ipv4-addr",
                    "value": "40.83.240.146"
                },
                "6": {
                    "type": "file",
                    "name": "svchost.exe"
                },
                "7": {
                    "type": "process",
                    "name": "svchost.exe",
                    "binary_ref": "6"
                }
            },
            "last_observed": "2021-10-23T13:47:11.727Z",
            "first_observed": "2021-10-05T07:11:47.599Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```

### Multiple Observation  

####STIX Translate query
```shell
translate cybereason query '{}' "([x-cybereason-process:integrity != 'trusted'] AND [x-cybereason-file:product_type IN ('Adobe')] AND [process:command_line LIKE 'Adobe\\Acrobat Reader DC']) START t'2021-02-10T11:43:08.000Z' STOP t'2021-11-12T11:00:00.003Z'"
```

#### STIX Translate query - output

```json
{
    "queries": [
        {
            "queryPath": [
                {
                    "requestedType": "Process",
                    "filters": [
                        {
                            "facetName": "integrity",
                            "filterType": "NotEquals",
                            "values": [
                                "trusted"
                            ]
                        },
                        {
                            "facetName": "creationTime",
                            "filterType": "Between",
                            "values": [
                                1612957388000,
                                1636714800003
                            ]
                        }
                    ],
                    "connectionFeature": {
                        "elementInstanceType": "Process",
                        "featureName": "imageFile"
                    }
                },
                {
                    "requestedType": "File",
                    "filters": [
                        {
                            "facetName": "productType",
                            "filterType": "Equals",
                            "values": [
                                "Adobe"
                            ]
                        },
                        {
                            "facetName": "createdTime",
                            "filterType": "Between",
                            "values": [
                                1612957388000,
                                1636714800003
                            ]
                        }
                    ],
                    "connectionFeature": {
                        "elementInstanceType": "Process",
                        "featureName": "imageFile"
                    },
                    "isReversed": true
                },
                {
                    "requestedType": "Process",
                    "filters": [
                        {
                            "facetName": "commandLine",
                            "filterType": "ContainsIgnoreCase",
                            "values": [
                                "Adobe\\Acrobat Reader DC"
                            ]
                        },
                        {
                            "facetName": "creationTime",
                            "filterType": "Between",
                            "values": [
                                1612957388000,
                                1636714800003
                            ]
                        }
                    ],
                    "isResult": true
                }
            ],
            "queryLimits": {
                "groupingFeature": {
                    "elementInstanceType": "Process",
                    "featureName": "elementDisplayName"
                }
            },
            "perFeatureLimit": 1,
            "totalResultLimit": 9999,
            "perGroupLimit": 1,
            "templateContext": "CUSTOM",
            "customFields": [
                "elementDisplayName",
                "creationTime",
                "endTime",
                "commandLine",
                "imageFile.maliciousClassificationType",
                "productType",
                "children",
                "parentProcess",
                "ownerMachine",
                "calculatedUser",
                "imageFile",
                "imageFile.sha1String",
                "imageFile.md5String",
                "imageFile.sha256String",
                "imageFile.companyName",
                "imageFile.productName",
                "applicablePid",
                "imageFileExtensionType",
                "integrity",
                "tid",
                "isAggregate",
                "isDotNetProtected",
                "hasMalops",
                "hasSuspicions",
                "relatedToMalop",
                "multipleSizeForHashEvidence",
                "isImageFileVerified",
                "knownMaliciousToolSuspicion",
                "knownMalwareSuspicion",
                "knownUnwantedSuspicion",
                "isMaliciousByHashEvidence",
                "imageFileMultipleCompanyNamesEvidence",
                "multipleHashForUnsignedPeInfoEvidence",
                "multipleNameForHashEvidence",
                "unknownEvidence",
                "rareHasPeMismatchEvidence",
                "imageFile.signedInternalOrExternal",
                "unknownUnsignedBySigningCompany",
                "imageFileUnsignedEvidence",
                "imageFileUnsignedHasSignedVersionEvidence",
                "unwantedModuleSuspicion",
                "imageFile.signerInternalOrExternal",
                "architecture",
                "commandLineContainsTempEvidence",
                "hasChildren",
                "hasClassification",
                "hasVisibleWindows",
                "hasWindows",
                "isInstaller",
                "isIdentifiedProduct",
                "hasModuleFromTempEvidence",
                "nonExecutableExtensionEvidence",
                "isNotShellRunner",
                "runningFromTempEvidence",
                "shellOfNonShellRunnerSuspicion",
                "shellWithElevatedPrivilegesEvidence",
                "systemUserEvidence",
                "hasExternalConnection",
                "hasExternalConnectionToWellKnownPortEvidence",
                "hasIncomingConnection",
                "hasInternalConnection",
                "hasMailConnectionForNonMailProcessEvidence",
                "hasListeningConnection",
                "hasOutgoingConnection",
                "hasUnresolvedDnsQueriesFromDomain",
                "multipleUnresolvedRecordNotExistsEvidence",
                "hasNonDefaultResolverEvidence",
                "parentProcessNotMatchHierarchySuspicion",
                "parentProcessNotAdminUserEvidence",
                "parentProcessFromRemovableDeviceEvidence",
                "autorun",
                "childrenCreatedByThread",
                "connections",
                "elevatedPrivilegeChildren",
                "hackerToolChildren",
                "hostProcess",
                "hostUser",
                "hostedChildren",
                "injectedChildren",
                "loadedModules",
                "logonSession",
                "remoteSession",
                "service",
                "execedBy",
                "connectionsToMaliciousDomain",
                "connectionsToMalwareAddresses",
                "externalConnections",
                "absoluteHighVolumeMaliciousAddressConnections",
                "absoluteHighVolumeExternalConnections",
                "incomingConnections",
                "incomingExternalConnections",
                "incomingInternalConnections",
                "internalConnections",
                "listeningConnections",
                "localConnections",
                "mailConnections",
                "outgoingConnections",
                "outgoingExternalConnections",
                "outgoingInternalConnections",
                "suspiciousExternalConnections",
                "suspiciousInternalConnections",
                "wellKnownPortConnections",
                "lowTtlDnsQueries",
                "nonDefaultResolverQueries",
                "resolvedDnsQueriesDomainToDomain",
                "resolvedDnsQueriesDomainToIp",
                "resolvedDnsQueriesIpToDomain",
                "suspiciousDnsQueryDomainToDomain",
                "unresolvedQueryFromSuspiciousDomain",
                "dnsQueryFromSuspiciousDomain",
                "dnsQueryToSuspiciousDomain",
                "unresolvedRecordNotExist",
                "unresolvedDnsQueriesFromDomain",
                "unresolvedDnsQueriesFromIp",
                "maliciousToolClassificationModules",
                "malwareClassificationModules",
                "modulesNotInLoaderDbList",
                "modulesFromTemp",
                "unsignedWithSignedVersionModules",
                "unwantedClassificationModules",
                "accessToMalwareAddressInfectedProcess",
                "connectingToBadReputationAddressSuspicion",
                "hasMaliciousConnectionEvidence",
                "hasSuspiciousExternalConnectionSuspicion",
                "highNumberOfExternalConnectionsSuspicion",
                "nonDefaultResolverSuspicion",
                "hasRareExternalConnectionEvidence",
                "hasRareRemoteAddressEvidence",
                "suspiciousMailConnections",
                "accessToMalwareAddressByUnknownProcess",
                "hasAbsoluteHighVolumeConnectionToMaliciousAddressEvidence",
                "hasAbsoluteHighVolumeExternalOutgoingConnectionEvidence",
                "highDataTransmittedSuspicion",
                "highDataVolumeTransmittedToMaliciousAddressSuspicion",
                "highDataVolumeTransmittedByUnknownProcess",
                "absoluteHighNumberOfInternalOutgoingEmbryonicConnectionsEvidence",
                "dgaSuspicion",
                "hasLowTtlDnsQueryEvidence",
                "highUnresolvedToResolvedRateEvidence",
                "manyUnresolvedRecordNotExistsEvidence",
                "hasChildKnownHackerToolEvidence",
                "hackingToolOfNonToolRunnerEvidence",
                "hackingToolOfNonToolRunnerSuspicion",
                "hasRareChildProcessKnownHackerToolEvidence",
                "maliciousToolModuleSuspicion",
                "deletedParentProcessEvidence",
                "malwareModuleSuspicion",
                "dualExtensionNameEvidence",
                "hiddenFileExtensionEvidence",
                "rightToLeftFileExtensionEvidence",
                "screenSaverWithChildrenEvidence",
                "suspicionsScreenSaverEvidence",
                "hasPeFloatingCodeEvidence",
                "hasSectionMismatchEvidence",
                "detectedInjectedEvidence",
                "detectedInjectingEvidence",
                "detectedInjectingToProtectedProcessEvidence",
                "hasInjectedChildren",
                "hostingInjectedThreadEvidence",
                "injectedProtectedProcessEvidence",
                "maliciousInjectingCodeSuspicion",
                "injectionMethod",
                "isHostingInjectedThread",
                "maliciousInjectedCodeSuspicion",
                "maliciousPeExecutionSuspicion",
                "hasSuspiciousInternalConnectionEvidence",
                "highInternalOutgoingEmbryonicConnectionRateEvidence",
                "highNumberOfInternalConnectionsEvidence",
                "newProcessesAboveThresholdEvidence",
                "hasRareInternalConnectionEvidence",
                "elevatingPrivilegesToChildEvidence",
                "parentProcessNotSystemUserEvidence",
                "privilegeEscalationEvidence",
                "firstExecutionOfDownloadedProcessEvidence",
                "hasAutorun",
                "newProcessEvidence",
                "markedForPrevention",
                "ransomwareAutoRemediationSuspended",
                "totalNumOfInstances",
                "lastMinuteNumOfInstances",
                "lastSeenTimeStamp",
                "wmiQueryStrings",
                "isExectuedByWmi",
                "absoluteHighNumberOfInternalConnectionsEvidence",
                "scanningProcessSuspicion",
                "imageFile.isDownloadedFromInternet",
                "imageFile.downloadedFromDomain",
                "imageFile.downloadedFromIpAddress",
                "imageFile.downloadedFromUrl",
                "imageFile.downloadedFromUrlReferrer",
                "imageFile.downloadedFromEmailFrom",
                "imageFile.downloadedFromEmailMessageId",
                "imageFile.downloadedFromEmailSubject",
                "rpcRequests",
                "iconBase64",
                "executionPrevented",
                "isWhiteListClassification",
                "matchedWhiteListRuleIds"
            ]
        },
        {
            "queryPath": [
                {
                    "requestedType": "Process",
                    "filters": [
                        {
                            "facetName": "integrity",
                            "filterType": "NotEquals",
                            "values": [
                                "trusted"
                            ]
                        },
                        {
                            "facetName": "creationTime",
                            "filterType": "Between",
                            "values": [
                                1612957388000,
                                1636714800003
                            ]
                        }
                    ],
                    "connectionFeature": {
                        "elementInstanceType": "Process",
                        "featureName": "imageFile"
                    }
                },
                {
                    "requestedType": "File",
                    "filters": [
                        {
                            "facetName": "productType",
                            "filterType": "Equals",
                            "values": [
                                "Adobe"
                            ]
                        },
                        {
                            "facetName": "createdTime",
                            "filterType": "Between",
                            "values": [
                                1612957388000,
                                1636714800003
                            ]
                        }
                    ],
                    "connectionFeature": {
                        "elementInstanceType": "Process",
                        "featureName": "imageFile"
                    },
                    "isReversed": true
                },
                {
                    "requestedType": "Process",
                    "filters": [
                        {
                            "facetName": "decodedCommandLine",
                            "filterType": "ContainsIgnoreCase",
                            "values": [
                                "Adobe\\Acrobat Reader DC"
                            ]
                        },
                        {
                            "facetName": "creationTime",
                            "filterType": "Between",
                            "values": [
                                1612957388000,
                                1636714800003
                            ]
                        }
                    ],
                    "isResult": true
                }
            ],
            "queryLimits": {
                "groupingFeature": {
                    "elementInstanceType": "Process",
                    "featureName": "elementDisplayName"
                }
            },
            "perFeatureLimit": 1,
            "totalResultLimit": 9999,
            "perGroupLimit": 1,
            "templateContext": "CUSTOM",
            "customFields": [
                "elementDisplayName",
                "creationTime",
                "endTime",
                "commandLine",
                "imageFile.maliciousClassificationType",
                "productType",
                "children",
                "parentProcess",
                "ownerMachine",
                "calculatedUser",
                "imageFile",
                "imageFile.sha1String",
                "imageFile.md5String",
                "imageFile.sha256String",
                "imageFile.companyName",
                "imageFile.productName",
                "applicablePid",
                "imageFileExtensionType",
                "integrity",
                "tid",
                "isAggregate",
                "isDotNetProtected",
                "hasMalops",
                "hasSuspicions",
                "relatedToMalop",
                "multipleSizeForHashEvidence",
                "isImageFileVerified",
                "knownMaliciousToolSuspicion",
                "knownMalwareSuspicion",
                "knownUnwantedSuspicion",
                "isMaliciousByHashEvidence",
                "imageFileMultipleCompanyNamesEvidence",
                "multipleHashForUnsignedPeInfoEvidence",
                "multipleNameForHashEvidence",
                "unknownEvidence",
                "rareHasPeMismatchEvidence",
                "imageFile.signedInternalOrExternal",
                "unknownUnsignedBySigningCompany",
                "imageFileUnsignedEvidence",
                "imageFileUnsignedHasSignedVersionEvidence",
                "unwantedModuleSuspicion",
                "imageFile.signerInternalOrExternal",
                "architecture",
                "commandLineContainsTempEvidence",
                "hasChildren",
                "hasClassification",
                "hasVisibleWindows",
                "hasWindows",
                "isInstaller",
                "isIdentifiedProduct",
                "hasModuleFromTempEvidence",
                "nonExecutableExtensionEvidence",
                "isNotShellRunner",
                "runningFromTempEvidence",
                "shellOfNonShellRunnerSuspicion",
                "shellWithElevatedPrivilegesEvidence",
                "systemUserEvidence",
                "hasExternalConnection",
                "hasExternalConnectionToWellKnownPortEvidence",
                "hasIncomingConnection",
                "hasInternalConnection",
                "hasMailConnectionForNonMailProcessEvidence",
                "hasListeningConnection",
                "hasOutgoingConnection",
                "hasUnresolvedDnsQueriesFromDomain",
                "multipleUnresolvedRecordNotExistsEvidence",
                "hasNonDefaultResolverEvidence",
                "parentProcessNotMatchHierarchySuspicion",
                "parentProcessNotAdminUserEvidence",
                "parentProcessFromRemovableDeviceEvidence",
                "autorun",
                "childrenCreatedByThread",
                "connections",
                "elevatedPrivilegeChildren",
                "hackerToolChildren",
                "hostProcess",
                "hostUser",
                "hostedChildren",
                "injectedChildren",
                "loadedModules",
                "logonSession",
                "remoteSession",
                "service",
                "execedBy",
                "connectionsToMaliciousDomain",
                "connectionsToMalwareAddresses",
                "externalConnections",
                "absoluteHighVolumeMaliciousAddressConnections",
                "absoluteHighVolumeExternalConnections",
                "incomingConnections",
                "incomingExternalConnections",
                "incomingInternalConnections",
                "internalConnections",
                "listeningConnections",
                "localConnections",
                "mailConnections",
                "outgoingConnections",
                "outgoingExternalConnections",
                "outgoingInternalConnections",
                "suspiciousExternalConnections",
                "suspiciousInternalConnections",
                "wellKnownPortConnections",
                "lowTtlDnsQueries",
                "nonDefaultResolverQueries",
                "resolvedDnsQueriesDomainToDomain",
                "resolvedDnsQueriesDomainToIp",
                "resolvedDnsQueriesIpToDomain",
                "suspiciousDnsQueryDomainToDomain",
                "unresolvedQueryFromSuspiciousDomain",
                "dnsQueryFromSuspiciousDomain",
                "dnsQueryToSuspiciousDomain",
                "unresolvedRecordNotExist",
                "unresolvedDnsQueriesFromDomain",
                "unresolvedDnsQueriesFromIp",
                "maliciousToolClassificationModules",
                "malwareClassificationModules",
                "modulesNotInLoaderDbList",
                "modulesFromTemp",
                "unsignedWithSignedVersionModules",
                "unwantedClassificationModules",
                "accessToMalwareAddressInfectedProcess",
                "connectingToBadReputationAddressSuspicion",
                "hasMaliciousConnectionEvidence",
                "hasSuspiciousExternalConnectionSuspicion",
                "highNumberOfExternalConnectionsSuspicion",
                "nonDefaultResolverSuspicion",
                "hasRareExternalConnectionEvidence",
                "hasRareRemoteAddressEvidence",
                "suspiciousMailConnections",
                "accessToMalwareAddressByUnknownProcess",
                "hasAbsoluteHighVolumeConnectionToMaliciousAddressEvidence",
                "hasAbsoluteHighVolumeExternalOutgoingConnectionEvidence",
                "highDataTransmittedSuspicion",
                "highDataVolumeTransmittedToMaliciousAddressSuspicion",
                "highDataVolumeTransmittedByUnknownProcess",
                "absoluteHighNumberOfInternalOutgoingEmbryonicConnectionsEvidence",
                "dgaSuspicion",
                "hasLowTtlDnsQueryEvidence",
                "highUnresolvedToResolvedRateEvidence",
                "manyUnresolvedRecordNotExistsEvidence",
                "hasChildKnownHackerToolEvidence",
                "hackingToolOfNonToolRunnerEvidence",
                "hackingToolOfNonToolRunnerSuspicion",
                "hasRareChildProcessKnownHackerToolEvidence",
                "maliciousToolModuleSuspicion",
                "deletedParentProcessEvidence",
                "malwareModuleSuspicion",
                "dualExtensionNameEvidence",
                "hiddenFileExtensionEvidence",
                "rightToLeftFileExtensionEvidence",
                "screenSaverWithChildrenEvidence",
                "suspicionsScreenSaverEvidence",
                "hasPeFloatingCodeEvidence",
                "hasSectionMismatchEvidence",
                "detectedInjectedEvidence",
                "detectedInjectingEvidence",
                "detectedInjectingToProtectedProcessEvidence",
                "hasInjectedChildren",
                "hostingInjectedThreadEvidence",
                "injectedProtectedProcessEvidence",
                "maliciousInjectingCodeSuspicion",
                "injectionMethod",
                "isHostingInjectedThread",
                "maliciousInjectedCodeSuspicion",
                "maliciousPeExecutionSuspicion",
                "hasSuspiciousInternalConnectionEvidence",
                "highInternalOutgoingEmbryonicConnectionRateEvidence",
                "highNumberOfInternalConnectionsEvidence",
                "newProcessesAboveThresholdEvidence",
                "hasRareInternalConnectionEvidence",
                "elevatingPrivilegesToChildEvidence",
                "parentProcessNotSystemUserEvidence",
                "privilegeEscalationEvidence",
                "firstExecutionOfDownloadedProcessEvidence",
                "hasAutorun",
                "newProcessEvidence",
                "markedForPrevention",
                "ransomwareAutoRemediationSuspended",
                "totalNumOfInstances",
                "lastMinuteNumOfInstances",
                "lastSeenTimeStamp",
                "wmiQueryStrings",
                "isExectuedByWmi",
                "absoluteHighNumberOfInternalConnectionsEvidence",
                "scanningProcessSuspicion",
                "imageFile.isDownloadedFromInternet",
                "imageFile.downloadedFromDomain",
                "imageFile.downloadedFromIpAddress",
                "imageFile.downloadedFromUrl",
                "imageFile.downloadedFromUrlReferrer",
                "imageFile.downloadedFromEmailFrom",
                "imageFile.downloadedFromEmailMessageId",
                "imageFile.downloadedFromEmailSubject",
                "rpcRequests",
                "iconBase64",
                "executionPrevented",
                "isWhiteListClassification",
                "matchedWhiteListRuleIds"
            ]
        }
    ]
}
```


#### STIX Transmit query

```shell
transmit 
cybereason 
"{\"host\":\"xx.xx.xx\",\"port\": xxxx}" 
"{\"auth\":{\"username\": \"xxxxx\", \"password\": \"xxxx\"}}" 
results 
"{ \"queryPath\": [ { \"requestedType\": \"Process\", \"filters\": [ { \"facetName\": \"integrity\", \"filterType\": \"NotEquals\", \"values\": [ \"trusted\" ] }, { \"facetName\": \"creationTime\", \"filterType\": \"Between\", \"values\": [ 1612957388000, 1636714800003 ] } ], \"connectionFeature\": { \"elementInstanceType\": \"Process\", \"featureName\": \"imageFile\" } }, { \"requestedType\": \"File\", \"filters\": [ { \"facetName\": \"productType\", \"filterType\": \"Equals\", \"values\": [ \"Adobe\" ] }, { \"facetName\": \"createdTime\", \"filterType\": \"Between\", \"values\": [ 1612957388000, 1636714800003 ] } ], \"connectionFeature\": { \"elementInstanceType\": \"Process\", \"featureName\": \"imageFile\" }, \"isReversed\": true }, { \"requestedType\": \"Process\", \"filters\": [ { \"facetName\": \"commandLine\", \"filterType\": \"ContainsIgnoreCase\", \"values\": [ \"Adobe\\Acrobat Reader DC\" ] }, { \"facetName\": \"creationTime\", \"filterType\": \"Between\", \"values\": [ 1612957388000, 1636714800003 ] } ], \"isResult\": true } ], \"queryLimits\": { \"groupingFeature\": { \"elementInstanceType\": \"Process\", \"featureName\": \"elementDisplayName\" } }, \"perFeatureLimit\": 1, \"totalResultLimit\": 9999, \"perGroupLimit\": 1, \"templateContext\": \"CUSTOM\", \"customFields\": [ \"elementDisplayName\", \"creationTime\", \"endTime\", \"commandLine\", \"imageFile.maliciousClassificationType\", \"productType\", \"children\", \"parentProcess\", \"ownerMachine\", \"calculatedUser\", \"imageFile\", \"imageFile.sha1String\", \"imageFile.md5String\", \"imageFile.sha256String\", \"imageFile.companyName\", \"imageFile.productName\", \"applicablePid\", \"imageFileExtensionType\", \"integrity\", \"tid\", \"isAggregate\", \"isDotNetProtected\", \"hasMalops\", \"hasSuspicions\", \"relatedToMalop\", \"multipleSizeForHashEvidence\", \"isImageFileVerified\", \"knownMaliciousToolSuspicion\", \"knownMalwareSuspicion\", \"knownUnwantedSuspicion\", \"isMaliciousByHashEvidence\", \"imageFileMultipleCompanyNamesEvidence\", \"multipleHashForUnsignedPeInfoEvidence\", \"multipleNameForHashEvidence\", \"unknownEvidence\", \"rareHasPeMismatchEvidence\", \"imageFile.signedInternalOrExternal\", \"unknownUnsignedBySigningCompany\", \"imageFileUnsignedEvidence\", \"imageFileUnsignedHasSignedVersionEvidence\", \"unwantedModuleSuspicion\", \"imageFile.signerInternalOrExternal\", \"architecture\", \"commandLineContainsTempEvidence\", \"hasChildren\", \"hasClassification\", \"hasVisibleWindows\", \"hasWindows\", \"isInstaller\", \"isIdentifiedProduct\", \"hasModuleFromTempEvidence\", \"nonExecutableExtensionEvidence\", \"isNotShellRunner\", \"runningFromTempEvidence\", \"shellOfNonShellRunnerSuspicion\", \"shellWithElevatedPrivilegesEvidence\", \"systemUserEvidence\", \"hasExternalConnection\", \"hasExternalConnectionToWellKnownPortEvidence\", \"hasIncomingConnection\", \"hasInternalConnection\", \"hasMailConnectionForNonMailProcessEvidence\", \"hasListeningConnection\", \"hasOutgoingConnection\", \"hasUnresolvedDnsQueriesFromDomain\", \"multipleUnresolvedRecordNotExistsEvidence\", \"hasNonDefaultResolverEvidence\", \"parentProcessNotMatchHierarchySuspicion\", \"parentProcessNotAdminUserEvidence\", \"parentProcessFromRemovableDeviceEvidence\", \"autorun\", \"childrenCreatedByThread\", \"connections\", \"elevatedPrivilegeChildren\", \"hackerToolChildren\", \"hostProcess\", \"hostUser\", \"hostedChildren\", \"injectedChildren\", \"loadedModules\", \"logonSession\", \"remoteSession\", \"service\", \"execedBy\", \"connectionsToMaliciousDomain\", \"connectionsToMalwareAddresses\", \"externalConnections\", \"absoluteHighVolumeMaliciousAddressConnections\", \"absoluteHighVolumeExternalConnections\", \"incomingConnections\", \"incomingExternalConnections\", \"incomingInternalConnections\", \"internalConnections\", \"listeningConnections\", \"localConnections\", \"mailConnections\", \"outgoingConnections\", \"outgoingExternalConnections\", \"outgoingInternalConnections\", \"suspiciousExternalConnections\", \"suspiciousInternalConnections\", \"wellKnownPortConnections\", \"lowTtlDnsQueries\", \"nonDefaultResolverQueries\", \"resolvedDnsQueriesDomainToDomain\", \"resolvedDnsQueriesDomainToIp\", \"resolvedDnsQueriesIpToDomain\", \"suspiciousDnsQueryDomainToDomain\", \"unresolvedQueryFromSuspiciousDomain\", \"dnsQueryFromSuspiciousDomain\", \"dnsQueryToSuspiciousDomain\", \"unresolvedRecordNotExist\", \"unresolvedDnsQueriesFromDomain\", \"unresolvedDnsQueriesFromIp\", \"maliciousToolClassificationModules\", \"malwareClassificationModules\", \"modulesNotInLoaderDbList\", \"modulesFromTemp\", \"unsignedWithSignedVersionModules\", \"unwantedClassificationModules\", \"accessToMalwareAddressInfectedProcess\", \"connectingToBadReputationAddressSuspicion\", \"hasMaliciousConnectionEvidence\", \"hasSuspiciousExternalConnectionSuspicion\", \"highNumberOfExternalConnectionsSuspicion\", \"nonDefaultResolverSuspicion\", \"hasRareExternalConnectionEvidence\", \"hasRareRemoteAddressEvidence\", \"suspiciousMailConnections\", \"accessToMalwareAddressByUnknownProcess\", \"hasAbsoluteHighVolumeConnectionToMaliciousAddressEvidence\", \"hasAbsoluteHighVolumeExternalOutgoingConnectionEvidence\", \"highDataTransmittedSuspicion\", \"highDataVolumeTransmittedToMaliciousAddressSuspicion\", \"highDataVolumeTransmittedByUnknownProcess\", \"absoluteHighNumberOfInternalOutgoingEmbryonicConnectionsEvidence\", \"dgaSuspicion\", \"hasLowTtlDnsQueryEvidence\", \"highUnresolvedToResolvedRateEvidence\", \"manyUnresolvedRecordNotExistsEvidence\", \"hasChildKnownHackerToolEvidence\", \"hackingToolOfNonToolRunnerEvidence\", \"hackingToolOfNonToolRunnerSuspicion\", \"hasRareChildProcessKnownHackerToolEvidence\", \"maliciousToolModuleSuspicion\", \"deletedParentProcessEvidence\", \"malwareModuleSuspicion\", \"dualExtensionNameEvidence\", \"hiddenFileExtensionEvidence\", \"rightToLeftFileExtensionEvidence\", \"screenSaverWithChildrenEvidence\", \"suspicionsScreenSaverEvidence\", \"hasPeFloatingCodeEvidence\", \"hasSectionMismatchEvidence\", \"detectedInjectedEvidence\", \"detectedInjectingEvidence\", \"detectedInjectingToProtectedProcessEvidence\", \"hasInjectedChildren\", \"hostingInjectedThreadEvidence\", \"injectedProtectedProcessEvidence\", \"maliciousInjectingCodeSuspicion\", \"injectionMethod\", \"isHostingInjectedThread\", \"maliciousInjectedCodeSuspicion\", \"maliciousPeExecutionSuspicion\", \"hasSuspiciousInternalConnectionEvidence\", \"highInternalOutgoingEmbryonicConnectionRateEvidence\", \"highNumberOfInternalConnectionsEvidence\", \"newProcessesAboveThresholdEvidence\", \"hasRareInternalConnectionEvidence\", \"elevatingPrivilegesToChildEvidence\", \"parentProcessNotSystemUserEvidence\", \"privilegeEscalationEvidence\", \"firstExecutionOfDownloadedProcessEvidence\", \"hasAutorun\", \"newProcessEvidence\", \"markedForPrevention\", \"ransomwareAutoRemediationSuspended\", \"totalNumOfInstances\", \"lastMinuteNumOfInstances\", \"lastSeenTimeStamp\", \"wmiQueryStrings\", \"isExectuedByWmi\", \"absoluteHighNumberOfInternalConnectionsEvidence\", \"scanningProcessSuspicion\", \"imageFile.isDownloadedFromInternet\", \"imageFile.downloadedFromDomain\", \"imageFile.downloadedFromIpAddress\", \"imageFile.downloadedFromUrl\", \"imageFile.downloadedFromUrlReferrer\", \"imageFile.downloadedFromEmailFrom\", \"imageFile.downloadedFromEmailMessageId\", \"imageFile.downloadedFromEmailSubject\", \"rpcRequests\", \"iconBase64\", \"executionPrevented\", \"isWhiteListClassification\", \"matchedWhiteListRuleIds\" ] }, { \"queryPath\": [ { \"requestedType\": \"Process\", \"filters\": [ { \"facetName\": \"integrity\", \"filterType\": \"NotEquals\", \"values\": [ \"trusted\" ] }, { \"facetName\": \"creationTime\", \"filterType\": \"Between\", \"values\": [ 1612957388000, 1636714800003 ] } ], \"connectionFeature\": { \"elementInstanceType\": \"Process\", \"featureName\": \"imageFile\" } }, { \"requestedType\": \"File\", \"filters\": [ { \"facetName\": \"productType\", \"filterType\": \"Equals\", \"values\": [ \"Adobe\" ] }, { \"facetName\": \"createdTime\", \"filterType\": \"Between\", \"values\": [ 1612957388000, 1636714800003 ] } ], \"connectionFeature\": { \"elementInstanceType\": \"Process\", \"featureName\": \"imageFile\" }, \"isReversed\": true }, { \"requestedType\": \"Process\", \"filters\": [ { \"facetName\": \"decodedCommandLine\", \"filterType\": \"ContainsIgnoreCase\", \"values\": [ \"Adobe\\Acrobat Reader DC\" ] }, { \"facetName\": \"creationTime\", \"filterType\": \"Between\", \"values\": [ 1612957388000, 1636714800003 ] } ], \"isResult\": true } ], \"queryLimits\": { \"groupingFeature\": { \"elementInstanceType\": \"Process\", \"featureName\": \"elementDisplayName\" } }, \"perFeatureLimit\": 1, \"totalResultLimit\": 9999, \"perGroupLimit\": 1, \"templateContext\": \"CUSTOM\", \"customFields\": [ \"elementDisplayName\", \"creationTime\", \"endTime\", \"commandLine\", \"imageFile.maliciousClassificationType\", \"productType\", \"children\", \"parentProcess\", \"ownerMachine\", \"calculatedUser\", \"imageFile\", \"imageFile.sha1String\", \"imageFile.md5String\", \"imageFile.sha256String\", \"imageFile.companyName\", \"imageFile.productName\", \"applicablePid\", \"imageFileExtensionType\", \"integrity\", \"tid\", \"isAggregate\", \"isDotNetProtected\", \"hasMalops\", \"hasSuspicions\", \"relatedToMalop\", \"multipleSizeForHashEvidence\", \"isImageFileVerified\", \"knownMaliciousToolSuspicion\", \"knownMalwareSuspicion\", \"knownUnwantedSuspicion\", \"isMaliciousByHashEvidence\", \"imageFileMultipleCompanyNamesEvidence\", \"multipleHashForUnsignedPeInfoEvidence\", \"multipleNameForHashEvidence\", \"unknownEvidence\", \"rareHasPeMismatchEvidence\", \"imageFile.signedInternalOrExternal\", \"unknownUnsignedBySigningCompany\", \"imageFileUnsignedEvidence\", \"imageFileUnsignedHasSignedVersionEvidence\", \"unwantedModuleSuspicion\", \"imageFile.signerInternalOrExternal\", \"architecture\", \"commandLineContainsTempEvidence\", \"hasChildren\", \"hasClassification\", \"hasVisibleWindows\", \"hasWindows\", \"isInstaller\", \"isIdentifiedProduct\", \"hasModuleFromTempEvidence\", \"nonExecutableExtensionEvidence\", \"isNotShellRunner\", \"runningFromTempEvidence\", \"shellOfNonShellRunnerSuspicion\", \"shellWithElevatedPrivilegesEvidence\", \"systemUserEvidence\", \"hasExternalConnection\", \"hasExternalConnectionToWellKnownPortEvidence\", \"hasIncomingConnection\", \"hasInternalConnection\", \"hasMailConnectionForNonMailProcessEvidence\", \"hasListeningConnection\", \"hasOutgoingConnection\", \"hasUnresolvedDnsQueriesFromDomain\", \"multipleUnresolvedRecordNotExistsEvidence\", \"hasNonDefaultResolverEvidence\", \"parentProcessNotMatchHierarchySuspicion\", \"parentProcessNotAdminUserEvidence\", \"parentProcessFromRemovableDeviceEvidence\", \"autorun\", \"childrenCreatedByThread\", \"connections\", \"elevatedPrivilegeChildren\", \"hackerToolChildren\", \"hostProcess\", \"hostUser\", \"hostedChildren\", \"injectedChildren\", \"loadedModules\", \"logonSession\", \"remoteSession\", \"service\", \"execedBy\", \"connectionsToMaliciousDomain\", \"connectionsToMalwareAddresses\", \"externalConnections\", \"absoluteHighVolumeMaliciousAddressConnections\", \"absoluteHighVolumeExternalConnections\", \"incomingConnections\", \"incomingExternalConnections\", \"incomingInternalConnections\", \"internalConnections\", \"listeningConnections\", \"localConnections\", \"mailConnections\", \"outgoingConnections\", \"outgoingExternalConnections\", \"outgoingInternalConnections\", \"suspiciousExternalConnections\", \"suspiciousInternalConnections\", \"wellKnownPortConnections\", \"lowTtlDnsQueries\", \"nonDefaultResolverQueries\", \"resolvedDnsQueriesDomainToDomain\", \"resolvedDnsQueriesDomainToIp\", \"resolvedDnsQueriesIpToDomain\", \"suspiciousDnsQueryDomainToDomain\", \"unresolvedQueryFromSuspiciousDomain\", \"dnsQueryFromSuspiciousDomain\", \"dnsQueryToSuspiciousDomain\", \"unresolvedRecordNotExist\", \"unresolvedDnsQueriesFromDomain\", \"unresolvedDnsQueriesFromIp\", \"maliciousToolClassificationModules\", \"malwareClassificationModules\", \"modulesNotInLoaderDbList\", \"modulesFromTemp\", \"unsignedWithSignedVersionModules\", \"unwantedClassificationModules\", \"accessToMalwareAddressInfectedProcess\", \"connectingToBadReputationAddressSuspicion\", \"hasMaliciousConnectionEvidence\", \"hasSuspiciousExternalConnectionSuspicion\", \"highNumberOfExternalConnectionsSuspicion\", \"nonDefaultResolverSuspicion\", \"hasRareExternalConnectionEvidence\", \"hasRareRemoteAddressEvidence\", \"suspiciousMailConnections\", \"accessToMalwareAddressByUnknownProcess\", \"hasAbsoluteHighVolumeConnectionToMaliciousAddressEvidence\", \"hasAbsoluteHighVolumeExternalOutgoingConnectionEvidence\", \"highDataTransmittedSuspicion\", \"highDataVolumeTransmittedToMaliciousAddressSuspicion\", \"highDataVolumeTransmittedByUnknownProcess\", \"absoluteHighNumberOfInternalOutgoingEmbryonicConnectionsEvidence\", \"dgaSuspicion\", \"hasLowTtlDnsQueryEvidence\", \"highUnresolvedToResolvedRateEvidence\", \"manyUnresolvedRecordNotExistsEvidence\", \"hasChildKnownHackerToolEvidence\", \"hackingToolOfNonToolRunnerEvidence\", \"hackingToolOfNonToolRunnerSuspicion\", \"hasRareChildProcessKnownHackerToolEvidence\", \"maliciousToolModuleSuspicion\", \"deletedParentProcessEvidence\", \"malwareModuleSuspicion\", \"dualExtensionNameEvidence\", \"hiddenFileExtensionEvidence\", \"rightToLeftFileExtensionEvidence\", \"screenSaverWithChildrenEvidence\", \"suspicionsScreenSaverEvidence\", \"hasPeFloatingCodeEvidence\", \"hasSectionMismatchEvidence\", \"detectedInjectedEvidence\", \"detectedInjectingEvidence\", \"detectedInjectingToProtectedProcessEvidence\", \"hasInjectedChildren\", \"hostingInjectedThreadEvidence\", \"injectedProtectedProcessEvidence\", \"maliciousInjectingCodeSuspicion\", \"injectionMethod\", \"isHostingInjectedThread\", \"maliciousInjectedCodeSuspicion\", \"maliciousPeExecutionSuspicion\", \"hasSuspiciousInternalConnectionEvidence\", \"highInternalOutgoingEmbryonicConnectionRateEvidence\", \"highNumberOfInternalConnectionsEvidence\", \"newProcessesAboveThresholdEvidence\", \"hasRareInternalConnectionEvidence\", \"elevatingPrivilegesToChildEvidence\", \"parentProcessNotSystemUserEvidence\", \"privilegeEscalationEvidence\", \"firstExecutionOfDownloadedProcessEvidence\", \"hasAutorun\", \"newProcessEvidence\", \"markedForPrevention\", \"ransomwareAutoRemediationSuspended\", \"totalNumOfInstances\", \"lastMinuteNumOfInstances\", \"lastSeenTimeStamp\", \"wmiQueryStrings\", \"isExectuedByWmi\", \"absoluteHighNumberOfInternalConnectionsEvidence\", \"scanningProcessSuspicion\", \"imageFile.isDownloadedFromInternet\", \"imageFile.downloadedFromDomain\", \"imageFile.downloadedFromIpAddress\", \"imageFile.downloadedFromUrl\", \"imageFile.downloadedFromUrlReferrer\", \"imageFile.downloadedFromEmailFrom\", \"imageFile.downloadedFromEmailMessageId\", \"imageFile.downloadedFromEmailSubject\", \"rpcRequests\", \"iconBase64\", \"executionPrevented\", \"isWhiteListClassification\", \"matchedWhiteListRuleIds\" ] } " 
0 2
```

#### STIX Transmit query - output

```json
{"success":true,
  "data":[
    {"Process":{"imageFile.maliciousClassificationType":"indifferent","isImageFileVerified":"true","imageFile.companyName":"Adobe Systems Incorporated","productType":"ADOBE","imageFileExtensionType":"EXECUTABLE_WINDOWS","isAggregate":"false","hasAutorun":"false","hasClassification":"true","imageFile.productName":"Adobe Acrobat Reader DC","imageFile.signerInternalOrExternal":"Adobe Inc.","imageFile.signedInternalOrExternal":"true","hasInjectedChildren":"false","creationTime":"1625048289019","imageFile.sha256String":"cf40670e0eb0629a0d51f65325c692788d0a5503dea3f13db643b916701ab1da","imageFile.md5String":"3c9b885b579ebadaae15e391ac8313af","iconBase64":"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAKGSURBVFhHxZc\/aBNRHMd\/TZMmFy0pIhVdLCIOXZKaxQoSB1FRahwcXDTqELemBKqDYLrUTRBUsKJExMFR6CKo4B9wUbSIi4soDi4OdnFxeH6\/T96RhF9ySe6O\/uDT67v3u\/f93u9+d+SJMWZDUU\/W6\/VEsVhMghQYC0mqVCqNNhqNEU2rbZDP50eve3LgcVaer24SEyVY89ktT\/ZXKpU2I\/4\/uVwuddOTRe3iKLmflXmYSLQZ4J3X03JcuyAOrmXkYK1Ws5X470JkopmVt1pyHDzMymtoZqw2Gm4Eg91aYpxAc9IaqFarCQxmtKRevDt90vz5\/s18vX1DnQ8CmlN8M5yBopbUC8avNy\/tUZsPApq7Qht4umPCHrX5ICIx8PnSgj1q80GENrD+ac38Xf+9cQa+LC9ZcYY2H0RoA3wLGKyCNh9EaAM\/Hj2wBhivZgtqTi9CGXDdz2AF2A88p+V2I5QB9\/z5IeLd08TP1SdqbjeGNsA7dd1PUZpx487gec5r6wxtoLX7GawCjfCTTEGO1y6eMy+mp+yYaOsMbICL8lm7oGhn81GUzdlaERpqzXH0bYAl5zefizoD3RYdhL4NUJQGXLMxhnntOunbAEVdFRh8FFreoLQZOJaSOS2JsLkYNBKVOOm7AnHRaSC\/4skHLTEO7nryHpo7rQH7B4OjSbmsJcfBXEpq0NyCJ+v\/Kt4MSvNpuaddECULaVmBVgH7kDHfAHcrOLkNHDmUlKt3PPmoXRwGrnk4KVegsQ+MU9c3QLA5YS9MgllwCpwFFyLgPDgDToACGG82m\/72zDdAuFtBQgZsB9NgLyiGZAbsAVtd2VtpG7SCHW2Cu9ooKJfL6s7YGCP\/ABNgFQCEfBgYAAAAAElFTkSuQmCC","hasSuspicions":"false","hasUnresolvedDnsQueriesFromDomain":"false","hasMalops":"false","imageFile.sha1String":"d75dea803685620b22514689e32c2287206dcc63","architecture":"wow64","markedForPrevention":"false","applicablePid":"10148","endTime":"1625048301349","integrity":"MEDIUM","isExectuedByWmi":"false","commandLine":"\"C:\\Program Files (x86)\\Adobe\\Acrobat Reader DC\\Reader\\AcroRd32.exe\" \/l \/slMode","isWhiteListClassification":"false","executionPrevented":"false","isNotShellRunner":"true","elementDisplayName":"acrord32.exe","isIdentifiedProduct":"true","hasChildren":"false","calculatedUser":"desktop-trs61af\\kj","ownerMachine":"desktop-trs61af","logonSession":"desktop-trs61af > desktop-trs61af","loadedModules":["cryptbase.dll","ole32.dll","rpcrt4.dll","propsys.dll","bcrypt.dll","combase.dll","oleaut32.dll","samcli.dll","libeay32.dll","comctl32.dll","dwmapi.dll","shlwapi.dll","urlmon.dll","mpr.dll","msvcrt.dll","wow64win.dll","sspicli.dll","gdi32.dll","winmmbase.dll","firewallapi.dll","windows.storage.dll","user32.dll","acrord32.exe","wow64.dll","uxtheme.dll","sechost.dll","msctf.dll","fwbase.dll","iphlpapi.dll","version.dll","bcryptprimitives.dll","agm.dll","profext.dll","ntmarta.dll","winmm.dll","kernelbase.dll","powrprof.dll","user32.dll","msvcp_win.dll","kernel.appcore.dll","ntdll.dll","ntdll.dll","ucrtbase.dll","imm32.dll","cfgmgr32.dll","userenv.dll","wow64cpu.dll","win32u.dll","kernel32.dll","{FLOATING}","profapi.dll","acrord32.dll","kernel32.dll","ws2_32.dll","ninput.dll","iertutil.dll","apphelp.dll","winspool.drv","shell32.dll","fltlib.dll","advapi32.dll","shcore.dll","gdi32full.dll"],"modulesNotInLoaderDbList":["samcli.dll","comctl32.dll","dwmapi.dll","winmmbase.dll","firewallapi.dll","user32.dll","uxtheme.dll","fwbase.dll","winmm.dll","apphelp.dll"],"unsignedWithSignedVersionModules":"libeay32.dll","imageFile":"acrord32.exe"}}
  ]
}

```
#### STIX Translate results
```shell
translate cybereason results 
"{\"type\":\"identity\",\"id\":\"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\",\"name\":\"cybereason\",\"identity_class\":\"events\"}" 
"[ { \"Process\": { \"imageFile.maliciousClassificationType\": \"indifferent\", \"isImageFileVerified\": \"true\", \"imageFile.companyName\": \"Adobe Systems Incorporated\", \"productType\": \"ADOBE\", \"imageFileExtensionType\": \"EXECUTABLE_WINDOWS\", \"isAggregate\": \"false\", \"hasAutorun\": \"false\", \"hasClassification\": \"true\", \"imageFile.productName\": \"Adobe Acrobat Reader DC\", \"imageFile.signerInternalOrExternal\": \"Adobe Inc.\", \"imageFile.signedInternalOrExternal\": \"true\", \"hasInjectedChildren\": \"false\", \"creationTime\": \"1625048289019\", \"imageFile.sha256String\": \"cf40670e0eb0629a0d51f65325c692788d0a5503dea3f13db643b916701ab1da\", \"imageFile.md5String\": \"3c9b885b579ebadaae15e391ac8313af\", \"iconBase64\": \"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAKGSURBVFhHxZc/aBNRHMd/TZMmFy0pIhVdLCIOXZKaxQoSB1FRahwcXDTqELemBKqDYLrUTRBUsKJExMFR6CKo4B9wUbSIi4soDi4OdnFxeH6/T96RhF9ySe6O/uDT67v3u/f93u9+d+SJMWZDUU/W6/VEsVhMghQYC0mqVCqNNhqNEU2rbZDP50eve3LgcVaer24SEyVY89ktT/ZXKpU2I/4/uVwuddOTRe3iKLmflXmYSLQZ4J3X03JcuyAOrmXkYK1Ws5X470JkopmVt1pyHDzMymtoZqw2Gm4Eg91aYpxAc9IaqFarCQxmtKRevDt90vz5/s18vX1DnQ8CmlN8M5yBopbUC8avNy/tUZsPApq7Qht4umPCHrX5ICIx8PnSgj1q80GENrD+ac38Xf+9cQa+LC9ZcYY2H0RoA3wLGKyCNh9EaAM/Hj2wBhivZgtqTi9CGXDdz2AF2A88p+V2I5QB9/z5IeLd08TP1SdqbjeGNsA7dd1PUZpx487gec5r6wxtoLX7GawCjfCTTEGO1y6eMy+mp+yYaOsMbICL8lm7oGhn81GUzdlaERpqzXH0bYAl5zefizoD3RYdhL4NUJQGXLMxhnntOunbAEVdFRh8FFreoLQZOJaSOS2JsLkYNBKVOOm7AnHRaSC/4skHLTEO7nryHpo7rQH7B4OjSbmsJcfBXEpq0NyCJ+v/Kt4MSvNpuaddECULaVmBVgH7kDHfAHcrOLkNHDmUlKt3PPmoXRwGrnk4KVegsQ+MU9c3QLA5YS9MgllwCpwFFyLgPDgDToACGG82m/72zDdAuFtBQgZsB9NgLyiGZAbsAVtd2VtpG7SCHW2Cu9ooKJfL6s7YGCP/ABNgFQCEfBgYAAAAAElFTkSuQmCC\", \"hasSuspicions\": \"false\", \"hasUnresolvedDnsQueriesFromDomain\": \"false\", \"hasMalops\": \"false\", \"imageFile.sha1String\": \"d75dea803685620b22514689e32c2287206dcc63\", \"architecture\": \"wow64\", \"markedForPrevention\": \"false\", \"applicablePid\": \"10148\", \"endTime\": \"1625048301349\", \"integrity\": \"MEDIUM\", \"isExectuedByWmi\": \"false\", \"commandLine\": \"\\"C:\\Program Files (x86)\\Adobe\\Acrobat Reader DC\\Reader\\AcroRd32.exe\\" /l /slMode\", \"isWhiteListClassification\": \"false\", \"executionPrevented\": \"false\", \"isNotShellRunner\": \"true\", \"elementDisplayName\": \"acrord32.exe\", \"isIdentifiedProduct\": \"true\", \"hasChildren\": \"false\", \"calculatedUser\": \"desktop-trs61af\\kj\", \"ownerMachine\": \"desktop-trs61af\", \"logonSession\": \"desktop-trs61af > desktop-trs61af\", \"loadedModules\": [ \"cryptbase.dll\", \"ole32.dll\", \"rpcrt4.dll\", \"propsys.dll\", \"bcrypt.dll\", \"combase.dll\", \"oleaut32.dll\", \"samcli.dll\", \"libeay32.dll\", \"comctl32.dll\", \"dwmapi.dll\", \"shlwapi.dll\", \"urlmon.dll\", \"mpr.dll\", \"msvcrt.dll\", \"wow64win.dll\", \"sspicli.dll\", \"gdi32.dll\", \"winmmbase.dll\", \"firewallapi.dll\", \"windows.storage.dll\", \"user32.dll\", \"acrord32.exe\", \"wow64.dll\", \"uxtheme.dll\", \"sechost.dll\", \"msctf.dll\", \"fwbase.dll\", \"iphlpapi.dll\", \"version.dll\", \"bcryptprimitives.dll\", \"agm.dll\", \"profext.dll\", \"ntmarta.dll\", \"winmm.dll\", \"kernelbase.dll\", \"powrprof.dll\", \"user32.dll\", \"msvcp_win.dll\", \"kernel.appcore.dll\", \"ntdll.dll\", \"ntdll.dll\", \"ucrtbase.dll\", \"imm32.dll\", \"cfgmgr32.dll\", \"userenv.dll\", \"wow64cpu.dll\", \"win32u.dll\", \"kernel32.dll\", \"{FLOATING}\", \"profapi.dll\", \"acrord32.dll\", \"kernel32.dll\", \"ws2_32.dll\", \"ninput.dll\", \"iertutil.dll\", \"apphelp.dll\", \"winspool.drv\", \"shell32.dll\", \"fltlib.dll\", \"advapi32.dll\", \"shcore.dll\", \"gdi32full.dll\" ], \"modulesNotInLoaderDbList\": [ \"samcli.dll\", \"comctl32.dll\", \"dwmapi.dll\", \"winmmbase.dll\", \"firewallapi.dll\", \"user32.dll\", \"uxtheme.dll\", \"fwbase.dll\", \"winmm.dll\", \"apphelp.dll\" ], \"unsignedWithSignedVersionModules\": \"libeay32.dll\", \"imageFile\": \"acrord32.exe\" } } ] "
```
#### STIX Translate results - output

```json
{
    "type": "bundle",
    "id": "bundle--37c60ebf-b03d-4bf1-8f95-96dbfac091b4",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "cybereason",
            "identity_class": "events"
        },
        {
            "id": "observed-data--74c4ff5d-63f7-4236-896f-2c433e711e89",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2021-12-27T12:48:41.720Z",
            "modified": "2021-12-27T12:48:41.720Z",
            "objects": {
                "0": {
                    "type": "x-cybereason-malops",
                    "malicious_classification_type": "indifferent",
                    "has_classification": "true",
                    "has_suspicions": "false",
                    "has_malops": "false",
                    "marked_for_prevention": "false",
                    "is_white_list_classification": "false",
                    "execution_prevented": "false"
                },
                "1": {
                    "type": "process",
                    "extensions": {
                        "x-cybereason-process": {
                            "is_verified": "true",
                            "company_name": "Adobe Systems Incorporated",
                            "extension_type": "EXECUTABLE_WINDOWS",
                            "is_aggregate": "false",
                            "has_autorun": "false",
                            "product_name": "Adobe Acrobat Reader DC",
                            "signer_internal_or_external": "Adobe Inc.",
                            "signed_internal_or_external": "true",
                            "has_injected_children": "false",
                            "icon_base64": "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAKGSURBVFhHxZc/aBNRHMd/TZMmFy0pIhVdLCIOXZKaxQoSB1FRahwcXDTqELemBKqDYLrUTRBUsKJExMFR6CKo4B9wUbSIi4soDi4OdnFxeH6/T96RhF9ySe6O/uDT67v3u/f93u9+d+SJMWZDUU/W6/VEsVhMghQYC0mqVCqNNhqNEU2rbZDP50eve3LgcVaer24SEyVY89ktT/ZXKpU2I/4/uVwuddOTRe3iKLmflXmYSLQZ4J3X03JcuyAOrmXkYK1Ws5X470JkopmVt1pyHDzMymtoZqw2Gm4Eg91aYpxAc9IaqFarCQxmtKRevDt90vz5/s18vX1DnQ8CmlN8M5yBopbUC8avNy/tUZsPApq7Qht4umPCHrX5ICIx8PnSgj1q80GENrD+ac38Xf+9cQa+LC9ZcYY2H0RoA3wLGKyCNh9EaAM/Hj2wBhivZgtqTi9CGXDdz2AF2A88p+V2I5QB9/z5IeLd08TP1SdqbjeGNsA7dd1PUZpx487gec5r6wxtoLX7GawCjfCTTEGO1y6eMy+mp+yYaOsMbICL8lm7oGhn81GUzdlaERpqzXH0bYAl5zefizoD3RYdhL4NUJQGXLMxhnntOunbAEVdFRh8FFreoLQZOJaSOS2JsLkYNBKVOOm7AnHRaSC/4skHLTEO7nryHpo7rQH7B4OjSbmsJcfBXEpq0NyCJ+v/Kt4MSvNpuaddECULaVmBVgH7kDHfAHcrOLkNHDmUlKt3PPmoXRwGrnk4KVegsQ+MU9c3QLA5YS9MgllwCpwFFyLgPDgDToACGG82m/72zDdAuFtBQgZsB9NgLyiGZAbsAVtd2VtpG7SCHW2Cu9ooKJfL6s7YGCP/ABNgFQCEfBgYAAAAAElFTkSuQmCC",
                            "architecture": "wow64",
                            "integrity": "MEDIUM",
                            "is_executed_by_wmi": "false",
                            "is_not_shell_runner": "true",
                            "is_identified_product": "true",
                            "has_children": "false",
                            "logon_session": "desktop-trs61af > desktop-trs61af",
                            "loaded_modules": [
                                "cryptbase.dll",
                                "ole32.dll",
                                "rpcrt4.dll",
                                "propsys.dll",
                                "bcrypt.dll",
                                "combase.dll",
                                "oleaut32.dll",
                                "samcli.dll",
                                "libeay32.dll",
                                "comctl32.dll",
                                "dwmapi.dll",
                                "shlwapi.dll",
                                "urlmon.dll",
                                "mpr.dll",
                                "msvcrt.dll",
                                "wow64win.dll",
                                "sspicli.dll",
                                "gdi32.dll",
                                "winmmbase.dll",
                                "firewallapi.dll",
                                "windows.storage.dll",
                                "user32.dll",
                                "acrord32.exe",
                                "wow64.dll",
                                "uxtheme.dll",
                                "sechost.dll",
                                "msctf.dll",
                                "fwbase.dll",
                                "iphlpapi.dll",
                                "version.dll",
                                "bcryptprimitives.dll",
                                "agm.dll",
                                "profext.dll",
                                "ntmarta.dll",
                                "winmm.dll",
                                "kernelbase.dll",
                                "powrprof.dll",
                                "user32.dll",
                                "msvcp_win.dll",
                                "kernel.appcore.dll",
                                "ntdll.dll",
                                "ntdll.dll",
                                "ucrtbase.dll",
                                "imm32.dll",
                                "cfgmgr32.dll",
                                "userenv.dll",
                                "wow64cpu.dll",
                                "win32u.dll",
                                "kernel32.dll",
                                "{FLOATING}",
                                "profapi.dll",
                                "acrord32.dll",
                                "kernel32.dll",
                                "ws2_32.dll",
                                "ninput.dll",
                                "iertutil.dll",
                                "apphelp.dll",
                                "winspool.drv",
                                "shell32.dll",
                                "fltlib.dll",
                                "advapi32.dll",
                                "shcore.dll",
                                "gdi32full.dll"
                            ],
                            "modules_not_db_list": [
                                "samcli.dll",
                                "comctl32.dll",
                                "dwmapi.dll",
                                "winmmbase.dll",
                                "firewallapi.dll",
                                "user32.dll",
                                "uxtheme.dll",
                                "fwbase.dll",
                                "winmm.dll",
                                "apphelp.dll"
                            ],
                            "unsigned_with_signed_version_modules": "libeay32.dll"
                        }
                    },
                    "created": "2021-06-30T10:18:09.019Z",
                    "pid": 10148,
                    "command_line": "\"C:\\Program Files (x86)\\Adobe\\Acrobat Reader DC\\Reader\\AcroRd32.exe\" /l /slMode",
                    "name": "acrord32.exe",
                    "binary_ref": "3",
                    "creator_user_ref": "5"
                },
                "2": {
                    "type": "x-oca-event",
                    "created": "2021-06-30T10:18:09.019Z",
                    "process_ref": "1",
                    "user_ref": "5"
                },
                "3": {
                    "type": "file",
                    "hashes": {
                        "SHA-256": "cf40670e0eb0629a0d51f65325c692788d0a5503dea3f13db643b916701ab1da",
                        "MD5": "3c9b885b579ebadaae15e391ac8313af",
                        "SHA-1": "d75dea803685620b22514689e32c2287206dcc63"
                    },
                    "name": "acrord32.exe"
                },
                "4": {
                    "type": "x-cybereason-connection",
                    "has_unresolved_dns_query": "false"
                },
                "5": {
                    "type": "user-account",
                    "user_id": "desktop-trs61af\\kj"
                },
                "6": {
                    "type": "file",
                    "name": "acrord32.exe"
                }
            },
            "first_observed": "2021-06-30T10:18:09.019Z",
            "last_observed": "2021-06-30T10:18:21.349Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}


```

#### STIX Execute query
```shell
execute
cybereason
cybereason
"{\"type\":\"identity\",\"id\":\"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\",\"name\":\"cybereason\",\"identity_class \":\"events\"}"
"{\"host\":\"xx.xx.xx\",\"port\": xxxx}"
"{\"auth\":{\"username\": \"xxxxx\", \"password\": \"xxxx\"}}"
" ( [ email-addr:value = 'Administrator@exlab1.local' ] )START t'2019-10-26T00:00:00.003Z' STOP t'2021-10-27T00:00:00.003Z'"
```
#### STIX Execute query - output
```json
{
    "type": "bundle",
    "id": "bundle--ff96ba28-4cd0-450b-9426-1689e9abff68",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "cybereason",
            "identity_class ": "events"
        },
        {
            "id": "observed-data--7c94d37a-0840-4e0f-a1b3-8ceeb6441cbe",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2021-12-27T14:06:49.083Z",
            "modified": "2021-12-27T14:06:49.083Z",
            "objects": {
                "0": {
                    "type": "user-account",
                    "extensions": {
                        "x-cybereason-user": {
                            "comment": "Built-in account for administering the computer/domain",
                            "password_age_days": "12",
                            "mail": "Administrator@exlab1.local",
                            "sam_account_name": "Administrator",
                            "member_of": "CN=400,CN=Users,DC=exlab1,DC=local, CN=100,CN=Users,DC=exlab1,DC=local, CN=Security Administrator,OU=Microsoft Exchange Security Groups,DC=exlab1,DC=local, CN=Security Reader,OU=Microsoft Exchange Security Groups,DC=exlab1,DC=local, CN=Compliance Management,OU=Microsoft Exchange Security Groups,DC=exlab1,DC=local, CN=Hygiene Management,OU=Microsoft Exchange Security Groups,DC=exlab1,DC=local, CN=Delegated Setup,OU=Microsoft Exchange Security Groups,DC=exlab1,DC=local, CN=Server Management,OU=Microsoft Exchange Security Groups,DC=exlab1,DC=local, CN=Discovery Management,OU=Microsoft Exchange Security Groups,DC=exlab1,DC=local, CN=Records Management,OU=Microsoft Exchange Security Groups,DC=exlab1,DC=local, CN=Help Desk,OU=Microsoft Exchange Security Groups,DC=exlab1,DC=local, CN=UM Management,OU=Microsoft Exchange Security Groups,DC=exlab1,DC=local, CN=Public Folder Management,OU=Microsoft Exchange Security Groups,DC=exlab1,DC=local, CN=Recipient Management,OU=Microsoft Exchange Security Groups,DC=exlab1,DC=local, CN=Organization Management,OU=Microsoft Exchange Security Groups,DC=exlab1,DC=local, CN=Group Policy Creator Owners,CN=Users,DC=exlab1,DC=local, CN=Domain Admins,CN=Users,DC=exlab1,DC=local, CN=Enterprise Admins,CN=Users,DC=exlab1,DC=local, CN=Schema Admins,CN=Users,DC=exlab1,DC=local, CN=Administrators,CN=Builtin,DC=exlab1,DC=local",
                            "privileges": "UserPrivAdmin",
                            "has_power_tool": "false",
                            "total_machines": "1",
                            "is_admin": "true",
                            "unusual_process_ext_connection": "false",
                            "is_local_system": "false",
                            "organizational_unit": "INTEGRATION",
                            "group_id": "513",
                            "domain": "exlab1",
                            "email_address": "Administrator@exlab1.local",
                            "last_logged_machine": "siemplify-cyber"
                        }
                    },
                    "user_id": "administrator",
                    "account_created": "2021-04-08T14:22:08.000Z"
                },
                "1": {
                    "type": "x-cybereason-malops",
                    "has_suspicions": "false",
                    "has_suspicious_process": "true",
                    "has_malicious_process": "false"
                },
                "2": {
                    "type": "email-addr",
                    "value": "Administrator@exlab1.local",
                    "belongs_to_ref": "0"
                },
                "3": {
                    "type": "x-oca-asset",
                    "host_name": "exlab1.local/Users/Administrator",
                    "user_ref": "0"
                }
            },
            "first_observed": "2021-04-08T14:22:08.000Z",
            "last_observed": "2021-04-08T14:22:08.000Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--750ab5cb-b150-4051-9f0a-cb1d86fbd2b1",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2021-12-27T14:06:49.083Z",
            "modified": "2021-12-27T14:06:49.083Z",
            "objects": {
                "0": {
                    "type": "user-account",
                    "extensions": {
                        "x-cybereason-user": {
                            "comment": "Built-in account for administering the computer/domain",
                            "password_age_days": "12",
                            "mail": "Administrator@exlab1.local",
                            "sam_account_name": "Administrator",
                            "member_of": "CN=400,CN=Users,DC=exlab1,DC=local, CN=100,CN=Users,DC=exlab1,DC=local, CN=Security Administrator,OU=Microsoft Exchange Security Groups,DC=exlab1,DC=local, CN=Security Reader,OU=Microsoft Exchange Security Groups,DC=exlab1,DC=local, CN=Compliance Management,OU=Microsoft Exchange Security Groups,DC=exlab1,DC=local, CN=Hygiene Management,OU=Microsoft Exchange Security Groups,DC=exlab1,DC=local, CN=Delegated Setup,OU=Microsoft Exchange Security Groups,DC=exlab1,DC=local, CN=Server Management,OU=Microsoft Exchange Security Groups,DC=exlab1,DC=local, CN=Discovery Management,OU=Microsoft Exchange Security Groups,DC=exlab1,DC=local, CN=Records Management,OU=Microsoft Exchange Security Groups,DC=exlab1,DC=local, CN=Help Desk,OU=Microsoft Exchange Security Groups,DC=exlab1,DC=local, CN=UM Management,OU=Microsoft Exchange Security Groups,DC=exlab1,DC=local, CN=Public Folder Management,OU=Microsoft Exchange Security Groups,DC=exlab1,DC=local, CN=Recipient Management,OU=Microsoft Exchange Security Groups,DC=exlab1,DC=local, CN=Organization Management,OU=Microsoft Exchange Security Groups,DC=exlab1,DC=local, CN=Group Policy Creator Owners,CN=Users,DC=exlab1,DC=local, CN=Domain Admins,CN=Users,DC=exlab1,DC=local, CN=Enterprise Admins,CN=Users,DC=exlab1,DC=local, CN=Schema Admins,CN=Users,DC=exlab1,DC=local, CN=Administrators,CN=Builtin,DC=exlab1,DC=local",
                            "privileges": "UserPrivAdmin",
                            "has_power_tool": "false",
                            "total_machines": "1",
                            "is_admin": "true",
                            "unusual_process_ext_connection": "false",
                            "is_local_system": "false",
                            "organizational_unit": "INTEGRATION",
                            "group_id": "513",
                            "domain": "exlab1",
                            "email_address": "Administrator@exlab1.local",
                            "last_logged_machine": "siemplify-cyber"
                        }
                    },
                    "user_id": "administrator",
                    "account_created": "2021-04-08T14:22:08.000Z"
                },
                "1": {
                    "type": "x-cybereason-malops",
                    "has_suspicions": "false",
                    "has_suspicious_process": "true",
                    "has_malicious_process": "false"
                },
                "2": {
                    "type": "email-addr",
                    "value": "Administrator@exlab1.local",
                    "belongs_to_ref": "0"
                },
                "3": {
                    "type": "x-oca-asset",
                    "host_name": "exlab1.local/Users/Administrator",
                    "user_ref": "0"
                }
            },
            "first_observed": "2021-04-08T14:22:08.000Z",
            "last_observed": "2021-04-08T14:22:08.000Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}

```

#### STIX Ping query
```shell
transmit
cybereason
"{\"host\":\"xx.xx.xx\",\"port\": xxxx}"
"{\"auth\":{\"username\": \"xxxxx\", \"password\": \"xxxx\"}}"
ping
```

#### STIX Ping query - output
```json
{
    "success": true
}
```

### Limitations
- Cybereason does not support “OR” operator between the elements and features. It supports only "AND" operator through "connectionFeature" and "Filters".

### Observations
- Cybereason doesnt support regex based search. It supports only substring based search . Hence wildcard characters cannot be used for searches using  LIKE or MATCHES operator


