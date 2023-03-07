from unittest.mock import patch
import unittest
import json
from stix_shifter_modules.cybereason.entry_point import EntryPoint
from stix_shifter.stix_transmission import stix_transmission
from stix_shifter.stix_transmission.stix_transmission import run_in_thread
from tests.utils.async_utils import get_mock_response


class HistoryMockResponse:
    def __init__(self):
        self.history = []


class CybereasonMockError:
    """ class for cybereason mock error"""

    def __init__(self, response_code, obj):
        self.code = response_code
        self.response = obj

    def read(self):
        return self.response.read()


class ErrorText:
    """ class for error text"""

    def __init__(self, txt):
        self.text = txt

    def read(self):
        return bytearray(self.text, 'utf-8')


class ErrorTextInvalidRequest:
    """ class for error text"""

    def __init__(self, txt):
        self.text = txt
        self.history = []


class ErrorTextInvalid:
    """ class for error text"""

    def __init__(self, txt, obj):
        self.text = txt
        self.history = [obj]
        self.status_code = 302

    def read(self):
        return bytearray(self.text, 'utf-8')


class ErrorTextA:
    def __init__(self):
        self.status_code = 302


@patch('stix_shifter_modules.cybereason.stix_transmission.api_client'
       '.APIClient.__init__')
class TestCybereasonConnection(unittest.TestCase):
    """ class for test cybereason connection"""

    @staticmethod
    def config():
        """format for configuration"""
        return {
            "auth": {
                "username": "bla",
                "password": "bla"
            }
        }

    @staticmethod
    def connection():
        """format for connection"""
        return {
            "host": "hostbla",
            "port": 8080
        }

    def test_is_async(self, mock_api_client):
        """check for synchronous or asynchronous"""
        mock_api_client.return_value = None
        entry_point = EntryPoint(self.connection(), self.config())
        check_async = entry_point.is_async()
        assert check_async is False

    @patch('stix_shifter_modules.cybereason.stix_transmission.api_client'
           '.APIClient.session_log_out')
    @patch('stix_shifter_modules.cybereason.stix_transmission.api_client'
           '.APIClient.session_log_in')
    @patch('stix_shifter_modules.cybereason.stix_transmission.api_client'
           '.APIClient.ping_box')
    def test_ping_endpoint(self, mock_ping_source, mock_cookie,
                           mock_logout, mock_api_client):
        """ test to check ping_data_source function"""
        pingmock = """{"pendingProbesPerServer":{"637b4d77e4b01c68baf5b572":0},"unassignedProbes":0,"online":true,"readyToServe":true}"""
        histobj = HistoryMockResponse()
        pingresponse = get_mock_response(200, pingmock, 'byte', response=histobj)
        mock_ping_source.return_value = pingresponse

        mock_logout.return_value = """{"response_code":200}"""
        mock_cookie.return_value = "JSESSIONID=52DCF6DF6CE150C27D2C7B96CCE66D7D"

        mock_api_client.return_value = None

        transmission = stix_transmission.StixTransmission('cybereason',
                                                          self.connection(),
                                                          self.config())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is True

    def test_process_query(self, mock_api_client):
        """ test to check query of process element """
        mock_api_client.return_value = None
        query = json.dumps({
            "queryPath": [{
                "requestedType": "Process",
                "filters": [{
                    "facetName": "elementDisplayName",
                    "filterType": "ContainsIgnoreCase",
                    "values": ["wmic.exe"]
                }],
                "isResult": True
            }],
            "totalResultLimit": 1000,
            "perGroupLimit": 100,
            "templateContext": "SPECIFIC",
            "customFields": ["elementDisplayName", "creationTime", "endTime",
                             "commandLine", "imageFile.maliciousClassificationType",
                             "productType", "children", "parentProcess",
                             "ownerMachine", "calculatedUser", "imageFile",
                             "imageFile.sha1String", "imageFile.md5String",
                             "imageFile.sha256String", "imageFile.companyName",
                             "imageFile.productName", "applicablePid",
                             "imageFileExtensionType", "integrity", "tid",
                             "isAggregate", "isDotNetProtected", "hasMalops",
                             "hasSuspicions", "relatedToMalop",
                             "multipleSizeForHashEvidence", "isImageFileVerified",
                             "knownMaliciousToolSuspicion", "knownMalwareSuspicion",
                             "knownUnwantedSuspicion", "isMaliciousByHashEvidence",
                             "imageFileMultipleCompanyNamesEvidence",
                             "multipleHashForUnsignedPeInfoEvidence",
                             "multipleNameForHashEvidence",
                             "unknownEvidence", "rareHasPeMismatchEvidence",
                             "imageFile.signedInternalOrExternal",
                             "unknownUnsignedBySigningCompany",
                             "imageFileUnsignedEvidence",
                             "imageFileUnsignedHasSignedVersionEvidence",
                             "unwantedModuleSuspicion",
                             "imageFile.signerInternalOrExternal",
                             "architecture",
                             "commandLineContainsTempEvidence", "hasChildren",
                             "hasClassification", "hasVisibleWindows",
                             "hasWindows", "isInstaller", "isIdentifiedProduct",
                             "hasModuleFromTempEvidence", "nonExecutableExtensionEvidence",
                             "isNotShellRunner", "runningFromTempEvidence",
                             "shellOfNonShellRunnerSuspicion",
                             "shellWithElevatedPrivilegesEvidence",
                             "systemUserEvidence", "hasExternalConnection",
                             "hasExternalConnectionToWellKnownPortEvidence",
                             "hasIncomingConnection", "hasInternalConnection",
                             "hasMailConnectionForNonMailProcessEvidence",
                             "hasListeningConnection", "hasOutgoingConnection",
                             "hasUnresolvedDnsQueriesFromDomain",
                             "multipleUnresolvedRecordNotExistsEvidence",
                             "hasNonDefaultResolverEvidence",
                             "parentProcessNotMatchHierarchySuspicion",
                             "parentProcessNotAdminUserEvidence",
                             "parentProcessFromRemovableDeviceEvidence",
                             "autorun", "childrenCreatedByThread",
                             "connections", "elevatedPrivilegeChildren",
                             "hackerToolChildren", "hostProcess", "hostUser",
                             "hostedChildren", "injectedChildren",
                             "loadedModules", "logonSession", "remoteSession",
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
                             "dgaSuspicion", "hasLowTtlDnsQueryEvidence",
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

        })

        transmission = stix_transmission.StixTransmission('cybereason',
                                                          self.connection(),
                                                          self.config())
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert query_response['search_id'] is not None
        assert query_response['search_id'] == query

    @patch('stix_shifter_modules.cybereason.stix_transmission.api_client'
           '.APIClient.session_log_out')
    @patch('stix_shifter_modules.cybereason.stix_transmission.api_client'
           '.APIClient.session_log_in')
    @patch('stix_shifter_modules.cybereason.stix_transmission.api_client'
           '.APIClient.get_search_results')
    def test_process_result(self, mock_results_response, mock_session,
                            mock_session_logout, mock_api_client):
        """ test to check result of process element"""
        mock_session_logout.return_value = get_mock_response(200)
        mock_session.return_value = "JSESSIONID=52DCF6DF6CE150C27D2C7B96CCE66D7D"
        mocked_return_value = """{
            "data": {
                "resultIdToElementDataMap": {
                    "-1837391212.1746789123229245971": {
                        "simpleValues": {
                            "applicablePid": {
                                "totalValues": 1,
                                "values": ["624"]
                            },
                            "commandLine": {
                                "totalValues": 1,
                                "values": ["C:\\\\WINDOWS\\\\System32\\\\svchost.exe \
                                -k NetworkService -p"]
                            },
                            "imageFile.md5String": {
                                "totalValues": 1,
                                "values": ["9520a99e77d6196d0d09833146424113"]
                            },
                            "creationTime": {
                                "totalValues": 1,
                                "values": ["1596848617500"]
                            },
                            "endTime": {
                                "totalValues": 1,
                                "values": ["1597955913267"]
                            },
                            "imageFile.sha256String": {
                                "totalValues": 1,
                                "values": ["dd191a5b23df92e12a8852291f9fb5ed594b76\
                                a28a5a464418442584afd1e048"]
                            },
                            "imageFile.sha1String": {
                                "totalValues": 1,
                                "values": ["75c5a97f521f760e32a4a9639a653eed862e9c61"]
                            },
                            "elementDisplayName": {
                                "totalValues": 1,
                                "values": ["svchost.exe"]
                            }
                        },
                        "elementValues": {
                            "parentProcess": {
                                "totalValues": 1,
                                "elementValues": [{
                                    "elementType": "Process",
                                    "guid": "-1837391212.4247194264269145540",
                                    "name": "services.exe",
                                    "hasSuspicions": false,
                                    "hasMalops": false
                                }],
                                "totalSuspicious": 0,
                                "totalMalicious": 0,
                                "guessedTotal": 0
                            },
                            "imageFile": {
                                "totalValues": 1,
                                "elementValues": [{
                                    "elementType": "File",
                                    "guid": "-1837391212.1251190729327068266",
                                    "name": "svchost.exe",
                                    "hasSuspicions": false,
                                    "hasMalops": false
                                }],
                                "totalSuspicious": 0,
                                "totalMalicious": 0,
                                "guessedTotal": 0
                            }
                        },
                        "suspicions": {
                            "blackListModuleSuspicion": 1602172848998,
                            "connectingToBlackListAddressSuspicion": 1611540009703
                        },
                        "filterData": {
                            "sortInGroupValue": "-1837391212.1746789123229245971",
                            "groupByValue": "svchost.exe"
                        },
                        "isMalicious": true,
                        "suspicionCount": 2,
                        "guidString": "-1837391212.1746789123229245971",
                        "labelsIds": null,
                        "malopPriority": null,
                        "suspect": true,
                        "malicious": true
                    }
                },
                "suspicionsMap": {
                    "blackListModuleSuspicion": {
                        "potentialEvidence": ["blackListModuleEvidence"],
                        "firstTimestamp": 1602172848998,
                        "totalSuspicions": 1
                    },
                    "connectingToBlackListAddressSuspicion": {
                        "potentialEvidence": ["hasBlackListConnectionEvidence"],
                        "firstTimestamp": 1611540009703,
                        "totalSuspicions": 1
                    }
                },
                "evidenceMap": {},
                "totalPossibleResults": 158260,
                "guessedPossibleResults": 0,
                "queryLimits": {
                    "totalResultLimit": 1,
                    "perGroupLimit": 1,
                    "perFeatureLimit": 1,
                    "groupingFeature": {
                        "elementInstanceType": "Process",
                        "featureName": "elementDisplayName"
                    },
                    "sortInGroupFeature": null
                },
                "queryTerminated": false,
                "pathResultCounts": [{
                    "featureDescriptor": {
                        "elementInstanceType": "Process",
                        "featureName": null
                    },
                    "count": 158260
                }],
                "guids": []
            },
            "status": "SUCCESS",
            "hidePartialSuccess": false,
            "message": "",
            "expectedResults": 1,
            "failures": 0
        }"""
        histobj = HistoryMockResponse()
        mock_results_response.return_value = get_mock_response(200, mocked_return_value, 'byte', histobj)
        mock_api_client.return_value = None

        query = json.dumps({
            "queryPath": [{
                "requestedType": "Process",
                "filters": [{
                    "facetName": "elementDisplayName",
                    "filterType": "ContainsIgnoreCase",
                    "values": ["wmic.exe"]
                }],
                "isResult": True
            }],
            "totalResultLimit": 1000,
            "perGroupLimit": 100,
            "templateContext": "SPECIFIC",
            "customFields": ["elementDisplayName",
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
                             "dgaSuspicion", "hasLowTtlDnsQueryEvidence",
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

        })

        transmission = stix_transmission.StixTransmission('cybereason',
                                                          self.connection(),
                                                          self.config())
        offset = 0
        length = 1
        results_response = transmission.results(query, offset, length)

        assert results_response is not None
        assert results_response['success'] is True
        assert 'data' in results_response
        assert results_response['data'] is not None

    def test_file_query(self, mock_api_client):
        """ test to check query of file element """
        mock_api_client.return_value = None
        query = json.dumps({
            "queryPath": [{
                "requestedType": "File",
                "filters": [{
                    "facetName": "elementDisplayName",
                    "filterType": "ContainsIgnoreCase",
                    "values": ["sbsimulation_sb_265540_bs_254977.exe"]
                }],
                "isResult": True
            }],
            "totalResultLimit": 1000,
            "perGroupLimit": 100,
            "templateContext": "SPECIFIC",
            "customFields": ["elementDisplayName", "maliciousClassificationType",
                             "ownerMachine", "avRemediationStatus",
                             "signerInternalOrExternal", "signedInternalOrExternal",
                             "signatureVerifiedInternalOrExternal", "sha1String",
                             "createdTime", "modifiedTime", "size",
                             "correctedPath", "productName"
                             ]
        })

        transmission = stix_transmission.StixTransmission('cybereason',
                                                          self.connection(),
                                                          self.config())
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert query_response['search_id'] is not None
        assert query_response['search_id'] == query

    @patch('stix_shifter_modules.cybereason.stix_transmission.api_client'
           '.APIClient.session_log_out')
    @patch('stix_shifter_modules.cybereason.stix_transmission.api_client'
           '.APIClient.session_log_in')
    @patch('stix_shifter_modules.cybereason.stix_transmission.api_client'
           '.APIClient.get_search_results')
    def test_file_result(self, mock_results_response, mock_session,
                         mock_session_logout, mock_api_client):
        """ test to check result of file element"""
        mock_session_logout.return_value = get_mock_response(200)
        mock_session.return_value = "JSESSIONID=52DCF6DF6CE150C27D2C7B96CCE66D7D"
        mocked_return_value = """{
            "data": {
                "resultIdToElementDataMap": {
                    "-1837391212.1746789123229245971": {
                        "simpleValues": {
                            "applicablePid": {
                                "totalValues": 1,
                                "values": ["624"]
                            },
                            "commandLine": {
                                "totalValues": 1,
                                "values": ["C:\\\\WINDOWS\\\\System32\\\\svchost.exe \
                                -k NetworkService -p"]
                            },
                            "imageFile.md5String": {
                                "totalValues": 1,
                                "values": ["9520a99e77d6196d0d09833146424113"]
                            },
                            "creationTime": {
                                "totalValues": 1,
                                "values": ["1596848617500"]
                            },
                            "endTime": {
                                "totalValues": 1,
                                "values": ["1597955913267"]
                            },
                            "imageFile.sha256String": {
                                "totalValues": 1,
                                "values": ["dd191a5b23df92e12a8852291f\
                                9fb5ed594b76a28a5a464418442584afd1e048"]
                            },
                            "imageFile.sha1String": {
                                "totalValues": 1,
                                "values": ["75c5a97f521f760e32a4a9639a653eed862e9c61"]
                            },
                            "elementDisplayName": {
                                "totalValues": 1,
                                "values": ["svchost.exe"]
                            }
                        },
                        "elementValues": {
                            "parentProcess": {
                                "totalValues": 1,
                                "elementValues": [{
                                    "elementType": "Process",
                                    "guid": "-1837391212.4247194264269145540",
                                    "name": "services.exe",
                                    "hasSuspicions": false,
                                    "hasMalops": false
                                }],
                                "totalSuspicious": 0,
                                "totalMalicious": 0,
                                "guessedTotal": 0
                            },
                            "imageFile": {
                                "totalValues": 1,
                                "elementValues": [{
                                    "elementType": "File",
                                    "guid": "-1837391212.1251190729327068266",
                                    "name": "svchost.exe",
                                    "hasSuspicions": false,
                                    "hasMalops": false
                                }],
                                "totalSuspicious": 0,
                                "totalMalicious": 0,
                                "guessedTotal": 0
                            }
                        },
                        "suspicions": {
                            "blackListModuleSuspicion": 1602172848998,
                            "connectingToBlackListAddressSuspicion": 1611540009703
                        },
                        "filterData": {
                            "sortInGroupValue": "-1837391212.1746789123229245971",
                            "groupByValue": "svchost.exe"
                        },
                        "isMalicious": true,
                        "suspicionCount": 2,
                        "guidString": "-1837391212.1746789123229245971",
                        "labelsIds": null,
                        "malopPriority": null,
                        "suspect": true,
                        "malicious": true
                    }
                },
                "suspicionsMap": {
                    "blackListModuleSuspicion": {
                        "potentialEvidence": ["blackListModuleEvidence"],
                        "firstTimestamp": 1602172848998,
                        "totalSuspicions": 1
                    },
                    "connectingToBlackListAddressSuspicion": {
                        "potentialEvidence": ["hasBlackListConnectionEvidence"],
                        "firstTimestamp": 1611540009703,
                        "totalSuspicions": 1
                    }
                },
                "evidenceMap": {},
                "totalPossibleResults": 158260,
                "guessedPossibleResults": 0,
                "queryLimits": {
                    "totalResultLimit": 1,
                    "perGroupLimit": 1,
                    "perFeatureLimit": 1,
                    "groupingFeature": {
                        "elementInstanceType": "Process",
                        "featureName": "elementDisplayName"
                    },
                    "sortInGroupFeature": null
                },
                "queryTerminated": false,
                "pathResultCounts": [{
                    "featureDescriptor": {
                        "elementInstanceType": "Process",
                        "featureName": null
                    },
                    "count": 158260
                }],
                "guids": []
            },
            "status": "SUCCESS",
            "hidePartialSuccess": false,
            "message": "",
            "expectedResults": 1,
            "failures": 0
        }"""
        histobj = HistoryMockResponse()
        mock_results_response.return_value = get_mock_response(200, mocked_return_value, 'byte', histobj)
        mock_api_client.return_value = None

        query = json.dumps({
            "queryPath": [{
                "requestedType": "File",
                "filters": [{
                    "facetName": "elementDisplayName",
                    "filterType": "ContainsIgnoreCase",
                    "values": ["sbsimulation_sb_265540_bs_254977.exe"]
                }],
                "isResult": True
            }],
            "totalResultLimit": 1000,
            "perGroupLimit": 100,
            "templateContext": "SPECIFIC",
            "customFields": ["elementDisplayName", "maliciousClassificationType",
                             "ownerMachine", "avRemediationStatus",
                             "signerInternalOrExternal", "signedInternalOrExternal",
                             "signatureVerifiedInternalOrExternal", "sha1String",
                             "createdTime", "modifiedTime", "size",
                             "correctedPath", "productName"
                             ]
        })

        transmission = stix_transmission.StixTransmission('cybereason',
                                                          self.connection(),
                                                          self.config())
        offset = 0
        length = 1
        results_response = transmission.results(query, offset, length)

        assert results_response is not None
        assert results_response['success'] is True
        assert 'data' in results_response
        assert results_response['data'] is not None

    @patch('stix_shifter_modules.cybereason.stix_transmission.api_client'
           '.APIClient.session_log_out')
    @patch('stix_shifter_modules.cybereason.stix_transmission.api_client'
           '.APIClient.session_log_in')
    @patch('stix_shifter_modules.cybereason.stix_transmission.api_client'
           '.APIClient.get_search_results')
    def test_machine_result(self, mock_results_response, mock_session,
                            mock_session_logout, mock_api_client):
        """ test to check result of machine element"""
        mock_session_logout.return_value = get_mock_response(200)
        mock_session.return_value = "JSESSIONID=52DCF6DF6CE150C27D2C7B96CCE66D7D"

        mocked_return_value = """{
            "data": {
                "resultIdToElementDataMap": {
                    "-1682067831.1198775089551518743": {
                        "simpleValues": {
                            "elementDisplayName": {
                                "totalValues": 1,
                                "values": ["w7-cbr-se2"]
                            }
                        },
                        "elementValues": {
                            "ownerOrganization": {
                                "totalValues": 1,
                                "elementValues": [{
                                    "elementType": "Organization",
                                    "guid": "0.7172824620821059429",
                                    "name": "INTEGRATION",
                                    "hasSuspicions": false,
                                    "hasMalops": false
                                }],
                                "totalSuspicious": 0,
                                "totalMalicious": 0,
                                "guessedTotal": 0
                            }
                        },
                        "suspicions": {},
                        "filterData": {
                            "sortInGroupValue": "-1682067831.1198775089551518743",
                            "groupByValue": "MachineRuntime:-1682067831.1198775089551518743 \
                            adCanonicalName=cyberrange.attackiq.com/Computers/W7-CBR-SE2 , \
                            adCompany=null , adDNSHostName=W7-CBR-SE2.cyberrange.attackiq.com , \
                            adDepartment=null , adDescription=null , adDisplayName=null , \
                            adLocation=null , adMachineRole=null , adOU=null , \
                            adOrganization=null , \
                            adSid=S-1-5-21-925260173-1387230621-1164276501-2222 , \
                            computerName=w7-cbr-se2 , "
                        },
                        "isMalicious": false,
                        "suspicionCount": 0,
                        "guidString": "-1682067831.1198775089551518743",
                        "labelsIds": null,
                        "malopPriority": null,
                        "suspect": false,
                        "malicious": false
                    },
                    "-1252318094.1198775089551518743": {
                        "simpleValues": {
                            "elementDisplayName": {
                                "totalValues": 1,
                                "values": ["w7-cbr-se"]
                            }
                        },
                        "elementValues": {
                            "ownerOrganization": {
                                "totalValues": 1,
                                "elementValues": [{
                                    "elementType": "Organization",
                                    "guid": "0.7172824620821059429",
                                    "name": "INTEGRATION",
                                    "hasSuspicions": false,
                                    "hasMalops": false
                                }],
                                "totalSuspicious": 0,
                                "totalMalicious": 0,
                                "guessedTotal": 0
                            }
                        },
                        "suspicions": {},
                        "filterData": {
                            "sortInGroupValue": "-1252318094.1198775089551518743",
                            "groupByValue": "MachineRuntime:-1252318094.1198775089551518743 \
                            adCanonicalName=cyberrange.attackiq.com/Computers/W7-CBR-SE , \
                            adCompany=null , adDNSHostName=W7-CBR-SE.cyberrange.attackiq.com , \
                            adDepartment=null , adDescription=null , adDisplayName=null , \
                            adLocation=null , adMachineRole=null , adOU=null , \
                            adOrganization=null , \
                            adSid=S-1-5-21-925260173-1387230621-1164276501-2223 , \
                            computerName=w7-cbr-se , "
                        },
                        "isMalicious": false,
                        "suspicionCount": 0,
                        "guidString": "-1252318094.1198775089551518743",
                        "labelsIds": null,
                        "malopPriority": null,
                        "suspect": false,
                        "malicious": false
                    }
                },
                "suspicionsMap": {},
                "evidenceMap": {},
                "totalPossibleResults": 2,
                "guessedPossibleResults": 0,
                "queryLimits": {
                    "totalResultLimit": 1000,
                    "perGroupLimit": 100,
                    "perFeatureLimit": 100,
                    "groupingFeature": {
                        "elementInstanceType": "Machine",
                        "featureName": "self"
                    },
                    "sortInGroupFeature": null
                },
                "queryTerminated": false,
                "pathResultCounts": [{
                    "featureDescriptor": {
                        "elementInstanceType": "Machine",
                        "featureName": null
                    },
                    "count": 2
                }],
                "guids": []
            },
            "status": "SUCCESS",
            "hidePartialSuccess": false,
            "message": "",
            "expectedResults": 1,
            "failures": 0
        }"""
        histobj = HistoryMockResponse()
        mock_results_response.return_value = get_mock_response(200, mocked_return_value, 'byte', histobj)
        mock_api_client.return_value = None

        query = json.dumps({
            "queryPath": [{
                "requestedType": "Machine",
                "filters": [{
                    "facetName": "elementDisplayName",
                    "filterType": "ContainsIgnoreCase",
                    "values": ["w7-cbr-se"]
                }],
                "isResult": True
            }],
            "totalResultLimit": 1000,
            "perGroupLimit": 100,
            "templateContext": "SPECIFIC",
            "customFields": ["elementDisplayName", "mountPoints",
                             "processes", "services", "logonSessions",
                             "hasRemovableDevice", "timezoneUTCOffsetMinutes",
                             "osVersionType", "platformArchitecture",
                             "mbrHashString", "osType", "domainFqdn",
                             "ownerOrganization", "pylumId", "adSid", "adOU",
                             "adOrganization", "adCanonicalName", "adCompany",
                             "adDNSHostName", "adDepartment", "adDisplayName",
                             "adLocation", "adMachineRole", "adDescription",
                             "freeDiskSpace", "totalDiskSpace", "freeMemory",
                             "totalMemory", "cpuCount", "isLaptop", "deviceModel",
                             "isActiveProbeConnected", "uptime", "isIsolated",
                             "lastSeenTimeStamp", "timeStampSinceLastConnectionTime",
                             "hasMalops", "hasSuspicions",
                             "isSuspiciousOrHasSuspiciousProcessOrFile", "maliciousTools",
                             "maliciousProcesses", "suspiciousProcesses"
                             ]
        })

        transmission = stix_transmission.StixTransmission('cybereason',
                                                          self.connection(),
                                                          self.config())
        offset = 0
        length = 1
        results_response = transmission.results(query, offset, length)

        assert results_response is not None
        assert results_response['success'] is True
        assert 'data' in results_response
        assert results_response['data'] is not None

    def test_connection_query(self, mock_api_client):
        """ test to check query of connection element"""
        mock_api_client.return_value = None
        query = json.dumps({
            "queryPath": [{
                "requestedType": "Connection",
                "filters": [{
                    "facetName": "elementDisplayName",
                    "filterType": "ContainsIgnoreCase",
                    "values": ["192.168.87.72:53235"]
                }],
                "isResult": True
            }],
            "totalResultLimit": 1000,
            "perGroupLimit": 100,
            "templateContext": "SPECIFIC",
            "customFields": ["elementDisplayName", "direction",
                             "ownerMachine", "ownerProcess",
                             "serverPort", "serverAddress",
                             "portType", "aggregatedReceivedBytesCount",
                             "aggregatedTransmittedBytesCount",
                             "remoteAddressCountryName", "dnsQuery",
                             "calculatedCreationTime", "domainName",
                             "endTime", "localPort", "portDescription",
                             "remotePort", "state", "isExternalConnection",
                             "isIncoming", "remoteAddressInternalExternalLocal",
                             "transportProtocol", "hasMalops", "hasSuspicions",
                             "relatedToMalop", "isWellKnownPort",
                             "isProcessLegit", "isProcessMalware", "localAddress",
                             "remoteAddress", "urlDomains"
                             ]
        })
        transmission = stix_transmission.StixTransmission('cybereason',
                                                          self.connection(),
                                                          self.config())
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert 'search_id' in query_response
        assert query_response['search_id'] == query

    def test_multielement_query(self, mock_api_client):
        """ test to check multielement query"""
        mock_api_client.return_value = None
        query = json.dumps({
            "queryPath": [{
                "requestedType": "Machine",
                "filters": [],
                "connectionFeature": {
                    "elementInstanceType": "Machine",
                    "featureName": "processes"
                }
            },
                {
                    "requestedType": "Process",
                    "filters": [{
                        "facetName": "elementDisplayName",
                        "filterType": "ContainsIgnoreCase",
                        "values": ["lazagne_windows_x64.exe"]
                    }],
                    "isResult": True
                }
            ],
            "totalResultLimit": 1000,
            "perGroupLimit": 100,
            "templateContext": "SPECIFIC",
            "customFields": ["elementDisplayName", "creationTime", "endTime",
                             "commandLine", "imageFile.maliciousClassificationType",
                             "productType", "children", "parentProcess",
                             "ownerMachine", "calculatedUser", "imageFile",
                             "imageFile.sha1String", "imageFile.md5String",
                             "imageFile.sha256String", "imageFile.companyName",
                             "imageFile.productName", "applicablePid",
                             "imageFileExtensionType", "integrity", "tid",
                             "isAggregate", "isDotNetProtected", "hasMalops",
                             "hasSuspicions", "relatedToMalop",
                             "multipleSizeForHashEvidence", "isImageFileVerified",
                             "knownMaliciousToolSuspicion", "knownMalwareSuspicion",
                             "knownUnwantedSuspicion", "isMaliciousByHashEvidence",
                             "imageFileMultipleCompanyNamesEvidence",
                             "multipleHashForUnsignedPeInfoEvidence",
                             "multipleNameForHashEvidence",
                             "unknownEvidence", "rareHasPeMismatchEvidence",
                             "imageFile.signedInternalOrExternal",
                             "unknownUnsignedBySigningCompany",
                             "imageFileUnsignedEvidence",
                             "imageFileUnsignedHasSignedVersionEvidence",
                             "unwantedModuleSuspicion",
                             "imageFile.signerInternalOrExternal",
                             "architecture",
                             "commandLineContainsTempEvidence", "hasChildren",
                             "hasClassification", "hasVisibleWindows",
                             "hasWindows", "isInstaller", "isIdentifiedProduct",
                             "hasModuleFromTempEvidence", "nonExecutableExtensionEvidence",
                             "isNotShellRunner", "runningFromTempEvidence",
                             "shellOfNonShellRunnerSuspicion",
                             "shellWithElevatedPrivilegesEvidence",
                             "systemUserEvidence", "hasExternalConnection",
                             "hasExternalConnectionToWellKnownPortEvidence",
                             "hasIncomingConnection", "hasInternalConnection",
                             "hasMailConnectionForNonMailProcessEvidence",
                             "hasListeningConnection", "hasOutgoingConnection",
                             "hasUnresolvedDnsQueriesFromDomain",
                             "multipleUnresolvedRecordNotExistsEvidence",
                             "hasNonDefaultResolverEvidence",
                             "parentProcessNotMatchHierarchySuspicion",
                             "parentProcessNotAdminUserEvidence",
                             "parentProcessFromRemovableDeviceEvidence",
                             "autorun", "childrenCreatedByThread",
                             "connections", "elevatedPrivilegeChildren",
                             "hackerToolChildren", "hostProcess", "hostUser",
                             "hostedChildren", "injectedChildren",
                             "loadedModules", "logonSession", "remoteSession",
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
                             "dgaSuspicion", "hasLowTtlDnsQueryEvidence",
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

        })
        transmission = stix_transmission.StixTransmission('cybereason',
                                                          self.connection(),
                                                          self.config())
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert 'search_id' in query_response
        assert query_response['search_id'] == query

    @patch('stix_shifter_modules.cybereason.stix_transmission.api_client'
           '.APIClient.session_log_out')
    @patch('stix_shifter_modules.cybereason.stix_transmission.api_client'
           '.APIClient.session_log_in')
    @patch('stix_shifter_modules.cybereason.stix_transmission.api_client'
           '.APIClient.get_search_results')
    def test_multielement_result(self, mock_results_response, mock_session,
                                 mock_session_logout, mock_api_client):
        """ test to check multielement result"""
        mock_session_logout.return_value = get_mock_response(200)
        mock_session.return_value = "JSESSIONID=52DCF6DF6CE150C27D2C7B96CCE66D7D"
        mocked_return_value = """{"data":{"resultIdToElementDataMap":{
            "92938357.6664466136019493057":{
            "simpleValues":{"elementDisplayName":{"totalValues":1,
            "values":["lazagne_windows_x64.exe"]},
            "endTime":{"totalValues":1,"values":["1603502037441"]},
            "imageFile.md5String":{"totalValues":1,
            "values":["e698cc182af5c9943475157626a338e8"]},
            "isWhiteListClassification":{"totalValues":1,
            "values":["false"]},"productType":{"totalValues":1,
            "values":["NONE"]},"commandLine":{
            "totalValues":1,"values":["\\"C:\\\\Program Files\\\\AttackIQ\\\\Firedrill\
            Agent\\\\scenarios\\\\f60\
            1a3b6-2587-436d-a635-e8589d69d6b8\\\\files\\\\ee61cb79-a4af-493d-b8\
            d2-a974411b6829\\\\laZagne_windows_x64.exe\\" \
            all -oJ -output C:\\\\WINDOWS\\\\TEMP"]},
            "creationTime":{"totalValues":1,"values":["1603502022981"]},
            "iconBase64":{
            "totalValues":1,"values":["iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6\
                                        QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAgbSURBVFhH\
                                        nVcLUBRXFm0gfE1EUEGQj/IR8AM6/CUggiAMAwgxIiCuFRzlj24sxogCAkIwKiw\
                                        wfgigQpQQFHCDKB/RxVKiZSQiIboxxERjsNxK3MKq7LJrn73dMw4zOGaJp+pU9e\
                                        3peee8++59r5tRRn2G1uIvK2Yc/bbe6ruHLfP+9X2zwy/fNNj2dpUYZx4WM3ryx\
                                        /4YBGJtogXRXWtphpCP1aElSyf4lyaLMbZ3IdgvvcB+HQj27yHElWBv++HWMasv\
                                        yISO/HFuYD3iHGZJojfjEBHNzPFPZWZ7FDKmzjXMDMdzjJHNV4yh9WNmislzRud\
                                        NaBoYwjbnAgzXlLbKR1DFYLnhObbLDrjmBvabILD3o8A+eBf4IRrst6F4/pUPfD\
                                        0trjPTbG7TwP9gDGayjPYUMBqaoL9PivY7z2NWUv2vdK0EmoldTHFjd+nCZ+hxA\
                                        Pq9wQ6Hg/05DhhZBzxaS2ZWkalA+LvoqB14srTbcgLWW5pAmvoUy2ASuiNZtPsU\
                                        LkrdgUtOwC1fsD/Q7B8nABzJCPtgNZ8FfxddtQNPljYby2G/vY0zYEOxDMZBWXG\
                                        ivCb0HHQH+zcnsAOcAUo7ifMciQf7cA1GB4IR7aMD65kMzIwY6OuoF/k9Wq/Nxc\
                                        K8bmi4bfahWAYtj+TlwtxG9FAGOANQMvDs3mo8uBqIR30r8M/bQozdDcN/7qzEb\
                                        /1+eHLRlUzbIjbAAJoa6gUn0iIsDYsLLkA/ULKaYjkEYsfA7fW8ASgZGHsQi4d9\
                                        Qfwy8Fl4FAtQJvDjO7KaoDoBdcjzW28jO2GaWsGJNPOLhYAMGK/ak0GxHAKxoU/\
                                        mx2TATcXAo+vUflwNKJaCCvLneFlNkBlpkQAxInM8vroMw63z1QpO5IwlwXAv7I\
                                        ZpzL5iisfhmlT5jDOgXAMvDKhyHW+EJSPGRrKOqClagJFO50ktwzQ7N3iRAYuEi\
                                        mMUj8MlsezeCwOvzABHPguxfFGerHBHyjor/HrNDyPnF0zKgIHpXCzd00XdUNVB\
                                        8Tic1n/Ue6Hy5SXg21DJAJd+rg7Y+5HUliHA18tp3/DCyOd2CgOmpqbYv38/kpK\
                                        SXjKgTbuh755OzEuqGaB4HPZxHzb+fwOyTQm0RzSW2GGeGaOgPZGGUTAqKgqjo6\
                                        Oora2Fjo7q5uWb3w6nlKNP6Hocc94tLOuudFWpgZEboYqZ8+TW/qcYvvpr8+aoD\
                                        KqOzs7OGB4expUrV/isvLjvnfUJFr/fwDKum3QplsE8MkfSXSEAe9GRdsK3ZW3G\
                                        FRwJKzLAtSJ3NtwTojbHSkXsVczNzcXTp0/h5OSkuOeW/Bd4Z7dwu6E1xTIYBWW\
                                        tP1dG+8AFe4A7Cb8Tyc4CZQNcTJnB3WAckpirCKmjUEgb19gYRCKRyn3ndTnwL2\
                                        gHZcCLYhne8EwOKi2IADrmAn1LwA7RUcyJcWsu73t+9sMiYHAZxKK3VAadSEdHR\
                                        37mEonkpd+cItOwoug83gzYFkWxHK6bFgZlFOGnE9Zg6UBib3jKjmQuE9xycEcz\
                                        dz0UgLunnWBooDroRAYEBCAkJETtby6xOxBMBkwjdqdQLIdAbOyyuRIxmZnol5p\
                                        SMS4Ae53OBqoHDPrzwuxtX3xRS9U/W/35r6mlDf1pJjCydIDZfG/M8QyDY1ACXK\
                                        Iz4bFhN3zTK7AiuwGhReewkmi9dm8B/U8OgVjDYcOB39zTpNDT1UKYuzZKk43QU\
                                        mCG1hIbSHcuREyUMywXecHaIxQOgXFwWZUKz4RdWJZaipXbjyM8/zQiCloQUdiK\
                                        cGJE4RlE7Pkrwvd8DlERxzaEFZ2FkMiZsF9fVi1Xl8Emfu/3HltrsGgdHZlrJHB\
                                        NLIbPlsNYvr0OgR98gqDsEwjOPomQXTSLnE8hzCVm10GYVYXwbRVY+4EUG/MOYU\
                                        txFXYeqEHJwWNIKqh6hYl2zE+sPCuXlsEqpuiqa2Y1OBNe79fCZ9sx+GYdR8BWK\
                                        eKy9mHTzgPYml+GXSXlKCmTQnroMOrq6tDa2oquri709PTg0qVLuHz5Mt/7fX19\
                                        qD5+8pWZcEk60i+XlsF8dcHpJRkfQ9XEUaTlfITGxkacOnUKzc3NOHPmDNra2tD\
                                        e3o6Ojg50d3crxHt7exXi165dw2dNTQjnl+VlE4KUqhG5tAwmkbmVi9KrMNHE5p\
                                        37Xkv8xo0b6OzsRPiuE2prwvvPx/9LtfeGXJ42o9Ad2fNTD2OiiXjJvtcSv3nzJ\
                                        n8dJjmitjADdnzK7Yaz5fIMYxCw7T2H5EPgTaSNm4jcuvd3xZXXXFm8v78fAwMD\
                                        iJYcVHSHjDITwvxWzoCbXJ7eDb1SQuw2H8REE8tTPvzDM38hPjg4iD/lHqE6aFb\
                                        bolOWbQ2XyxMEYhfr98oxbuIIvxzu4mLewOuIDw0NIb24ht8j1JkwEWZvkqsTBG\
                                        KTWfH7MFdcqWTiMBZvPsAX4euI37lzB9lldeC+O16YCMn5DMuz6uGSWPGjhtumW\
                                        XJ1gkCsafxO4ahlYgWZkCpMLEiW8v0+2TXnrjmDZ8+efd7Q0PA4dXtBj3V0/g76\
                                        ANqguzRtJek4E2dyenLlcWi8ZRZlJJI8k5mohC2ZsN1YgYNHqvklaGlpQX19PVt\
                                        eXv7vvLy80fT09CdxcXH3g4OD+wUCwXlLS8vqqVOn5ujp6SVoamr60ZACohNxLt\
                                        GMOI04/oGrBvr0JeumPdcrW8vcOZUxtIpn9IzCp0+fsdrQ0DBMV1fXT0NDw5Wec\
                                        ybOJzoQbYncy4UF0ZxoQpxONCJOJU4hct+C3BsQ1/dKM2eY/wFOha+/qX5m8AAA\
                                        AABJRU5ErkJggg=="]},

            "executionPrevented":{"totalValues":1,
            "values":["false"]},
            "imageFile.maliciousClassificationType":{"totalValues":1,
            "values":["unwanted"]},
            "applicablePid":{"totalValues":1,"values":["14204"]},
            "imageFile.sha1String":{
            "totalValues":1,"values":["62fa972f6113fdbf54ed4988a59a5c8c2c953ec7"]}},
            "elementValues":{
            "calculatedUser":{"totalValues":1,"elementValues":[{"elementType":"User",
            "guid":"0.-5690956990971252393","name":"cyb10-110\\\\system",
            "hasSuspicions":false,
            "hasMalops":false}],"totalSuspicious":0,"totalMalicious":0,
            "guessedTotal":0},
            "ownerMachine":{"totalValues":1,"elementValues":[{
            "elementType":"Machine",
            "guid":"92938357.1198775089551518743","name":"cyb10-110",
            "hasSuspicions":false,
            "hasMalops":false}],"totalSuspicious":0,"totalMalicious":0,
            "guessedTotal":0},
            "parentProcess":{"totalValues":1,"elementValues":[{
            "elementType":"Process",
            "guid":"92938357.-3378925745757371080","name":"lazagne_windows_x64.exe",
            "hasSuspicions":true,
            "hasMalops":true}],"totalSuspicious":1,"totalMalicious":1,
            "guessedTotal":0},
            "imageFile":{"totalValues":1,"elementValues":[{
            "elementType":"File",
            "guid":"92938357.467292301145861176","name":"lazagne_windows_x64.exe",
            "hasSuspicions":true,
            "hasMalops":false}],"totalSuspicious":1,"totalMalicious":0,
            "guessedTotal":0}},
            "suspicions":{"blackListModuleSuspicion":1619649864414,
            "lsassEncryptionKeysReadSuspicion":1603502037125,
            "lsassMainAuthenticationPackageReadSuspicion":1603502037125,
            "blackListFileSuspicion":1606841501449,
            "lsassSupplementalAuthenticationPackageReadSuspicion":1603502037125,
            "knownUnwantedSuspicion":1619822664080},"filterData":{
            "sortInGroupValue":"92938357.6664466136019493057",
            "groupByValue":"lazagne_windows_x64.exe"},
            "isMalicious":true,"suspicionCount":6,
            "guidString":"92938357.6664466136019493057",
            "labelsIds":null,"malopPriority":null,"suspect":true,
            "malicious":true}},
            "suspicionsMap":{"blackListModuleSuspicion":{
            "potentialEvidence":["blackListModuleEvidence"],
            "firstTimestamp":1619649864414,"totalSuspicions":100},
            "lsassEncryptionKeysReadSuspicion":{
            "potentialEvidence":["lsassVMReadEvidence"],
            "firstTimestamp":1600995627181,"totalSuspicions":100},
            "lsassMainAuthenticationPackageReadSuspicion":{
            "potentialEvidence":["lsassVMReadEvidence"],
            "firstTimestamp":1600995627181,"totalSuspicions":100},
            "blackListFileSuspicion":{"potentialEvidence":["fileBlackListEvidence"],
            "firstTimestamp":1606841501449,"totalSuspicions":100},
            "lsassSupplementalAuthenticationPackageReadSuspicion":{
            "potentialEvidence":["lsassVMReadEvidence"],
            "firstTimestamp":1600995627181,"totalSuspicions":100},
            "knownUnwantedSuspicion":{"potentialEvidence":["unwantedEvidence"],
            "firstTimestamp":1619822664080,"totalSuspicions":100}},"evidenceMap":{},
            "totalPossibleResults":1543,"guessedPossibleResults":0,
            "queryLimits":{"totalResultLimit":1000,
            "perGroupLimit":100,"perFeatureLimit":100,"groupingFeature":{
            "elementInstanceType":"Process",
            "featureName":"imageFileHash"},"sortInGroupFeature":null},
            "queryTerminated":false,
            "pathResultCounts":[{"featureDescriptor":{
            "elementInstanceType":"Machine","featureName":null},
            "count":17},{"featureDescriptor":{"elementInstanceType":"Machine",
            "featureName":"processes"},
            "count":1543}],"guids":[]},"status":"SUCCESS",
            "hidePartialSuccess":false,
            "message":"","expectedResults":1,"failures":0}"""
        histobj = HistoryMockResponse()
        mock_results_response.return_value = get_mock_response(200, mocked_return_value, 'byte', histobj)
        mock_api_client.return_value = None

        query = json.dumps({
            "queryPath": [{
                "requestedType": "Machine",
                "filters": [],
                "connectionFeature": {
                    "elementInstanceType": "Machine",
                    "featureName": "processes"
                }
            },
                {
                    "requestedType": "Process",
                    "filters": [{
                        "facetName": "elementDisplayName",
                        "filterType": "ContainsIgnoreCase",
                        "values": ["lazagne_windows_x64.exe"]
                    }],
                    "isResult": True
                }
            ],
            "totalResultLimit": 1000,
            "perGroupLimit": 100,
            "templateContext": "SPECIFIC",
            "customFields": ["elementDisplayName", "creationTime", "endTime",
                             "commandLine", "imageFile.maliciousClassificationType",
                             "productType", "children", "parentProcess",
                             "ownerMachine", "calculatedUser", "imageFile",
                             "imageFile.sha1String", "imageFile.md5String",
                             "imageFile.sha256String", "imageFile.companyName",
                             "imageFile.productName", "applicablePid",
                             "imageFileExtensionType", "integrity", "tid",
                             "isAggregate", "isDotNetProtected", "hasMalops",
                             "hasSuspicions", "relatedToMalop",
                             "multipleSizeForHashEvidence", "isImageFileVerified",
                             "knownMaliciousToolSuspicion", "knownMalwareSuspicion",
                             "knownUnwantedSuspicion", "isMaliciousByHashEvidence",
                             "imageFileMultipleCompanyNamesEvidence",
                             "multipleHashForUnsignedPeInfoEvidence",
                             "multipleNameForHashEvidence",
                             "unknownEvidence", "rareHasPeMismatchEvidence",
                             "imageFile.signedInternalOrExternal",
                             "unknownUnsignedBySigningCompany",
                             "imageFileUnsignedEvidence",
                             "imageFileUnsignedHasSignedVersionEvidence",
                             "unwantedModuleSuspicion",
                             "imageFile.signerInternalOrExternal",
                             "architecture",
                             "commandLineContainsTempEvidence", "hasChildren",
                             "hasClassification", "hasVisibleWindows",
                             "hasWindows", "isInstaller", "isIdentifiedProduct",
                             "hasModuleFromTempEvidence", "nonExecutableExtensionEvidence",
                             "isNotShellRunner", "runningFromTempEvidence",
                             "shellOfNonShellRunnerSuspicion",
                             "shellWithElevatedPrivilegesEvidence",
                             "systemUserEvidence", "hasExternalConnection",
                             "hasExternalConnectionToWellKnownPortEvidence",
                             "hasIncomingConnection", "hasInternalConnection",
                             "hasMailConnectionForNonMailProcessEvidence",
                             "hasListeningConnection", "hasOutgoingConnection",
                             "hasUnresolvedDnsQueriesFromDomain",
                             "multipleUnresolvedRecordNotExistsEvidence",
                             "hasNonDefaultResolverEvidence",
                             "parentProcessNotMatchHierarchySuspicion",
                             "parentProcessNotAdminUserEvidence",
                             "parentProcessFromRemovableDeviceEvidence",
                             "autorun", "childrenCreatedByThread",
                             "connections", "elevatedPrivilegeChildren",
                             "hackerToolChildren", "hostProcess", "hostUser",
                             "hostedChildren", "injectedChildren",
                             "loadedModules", "logonSession", "remoteSession",
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
                             "dgaSuspicion", "hasLowTtlDnsQueryEvidence",
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

        })
        transmission = stix_transmission.StixTransmission('cybereason',
                                                          self.connection(),
                                                          self.config())
        offset = 0
        length = 1
        results_response = transmission.results(query, offset, length)

        assert results_response is not None
        assert results_response['success'] is True
        assert 'data' in results_response
        assert results_response['data'] is not None

    def test_registry_events_query(self, mock_api_client):
        """ test to check query of registry event element"""
        mock_api_client.return_value = None

        query = json.dumps({
            "queryPath": [{
                "requestedType": "RegistryEvent",
                "filters": [{
                    "facetName": "registryProcess",
                    "filterType": "ContainsIgnoreCase",
                    "values": ["msiexec.exe"]
                }],
                "isResult": True
            }],
            "totalResultLimit": 1000,
            "perGroupLimit": 100,
            "templateContext": "SPECIFIC",
            "customFields": ["elementDisplayName", "self", "registryDataType",
                             "registryOperationType", "timestamp", "firstTime",
                             "detectionTimesNumber", "registryProcess",
                             "registryEntry", "data", "ownerMachine"
                             ]
        })

        transmission = stix_transmission.StixTransmission('cybereason',
                                                          self.connection(),
                                                          self.config())
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert 'search_id' in query_response
        assert query_response['search_id'] == query

    @patch('stix_shifter_modules.cybereason.stix_transmission.api_client'
           '.APIClient.session_log_out')
    @patch('stix_shifter_modules.cybereason.stix_transmission.api_client'
           '.APIClient.session_log_in')
    @patch('stix_shifter_modules.cybereason.stix_transmission.api_client'
           '.APIClient.get_search_results')
    def test_registry_events_result(self, mock_results_response, mock_session,
                                    mock_session_logout, mock_api_client):
        """ test to check result of registry event element"""
        mock_session_logout.return_value = get_mock_response(200)
        mock_session.return_value = "JSESSIONID=52DCF6DF6CE150C27D2C7B96CCE66D7D"
        mocked_return_value = """{
            "data": {
                "resultIdToElementDataMap": {
                    "-1595658254.6071472875411682107": {
                        "simpleValues": {
                            "firstTime": {
                                "totalValues": 1,
                                "values": ["1627221203465"]
                            },
                            "registryOperationType": {
                                "totalValues": 1,
                                "values": ["REG_MODIFY"]
                            },
                            "detectionTimesNumber": {
                                "totalValues": 1,
                                "values": ["1"]
                            },
                            "data": {
                                "totalValues": 1,
                                "values": ["C:\\\\Program Files\\\\Hysolate\\\\Work\
                                space\\\\hywsint.exe"]
                            },
                            "timestamp": {
                                "totalValues": 1,
                                "values": ["1627221203465"]
                            },
                            "registryDataType": {
                                "totalValues": 1,
                                "values": ["REG_DATATYPE_SZ"]
                            },
                            "elementDisplayName": {
                                "totalValues": 1,
                                "values": [
                                    "hklm\\\\software\\\\microsoft\\\\windows\\\\curren\
                                    tversion\\\\run\\\\hywsint"]
                            }
                        },
                        "elementValues": {
                            "registryProcess": {
                                "totalValues": 1,
                                "elementValues": [{
                                    "elementType": "Process",
                                    "guid": "-1595658254.7874497552221052881",
                                    "name": "msiexec.exe",
                                    "hasSuspicions": false,
                                    "hasMalops": false
                                }],
                                "totalSuspicious": 0,
                                "totalMalicious": 0,
                                "guessedTotal": 0
                            },
                            "ownerMachine": {
                                "totalValues": 1,
                                "elementValues": [{
                                    "elementType": "Machine",
                                    "guid": "-1595658254.1198775089551518743",
                                    "name": "hy01-yak",
                                    "hasSuspicions": false,
                                    "hasMalops": false
                                }],
                                "totalSuspicious": 0,
                                "totalMalicious": 0,
                                "guessedTotal": 0
                            },
                            "self": {
                                "totalValues": 1,
                                "elementValues": [{
                                    "elementType": "RegistryEvent",
                                    "guid": "-1595658254.6071472875411682107",
                                    "name": "hklm\\\\software\\\\microsoft\\\\win\
                                    dows\\\\currentversion\\\\run\\\\hywsint",
                                    "hasSuspicions": false,
                                    "hasMalops": false
                                }],
                                "totalSuspicious": 0,
                                "totalMalicious": 0,
                                "guessedTotal": 0
                            }
                        },
                        "filterData": {
                            "sortInGroupValue": "-1595658254.6071472875411682107",
                            "groupByValue": "1627221203465"
                        },
                        "isMalicious": false,
                        "suspicionCount": 0,
                        "guidString": "-1595658254.6071472875411682107",
                        "labelsIds": "None",
                        "malopPriority": "None",
                        "suspect": false,
                        "malicious": false
                    }
                },
                "suspicionsMap": {},
                "evidenceMap": {},
                "totalPossibleResults": 71,
                "guessedPossibleResults": 0,
                "queryLimits": {
                    "totalResultLimit": 1000,
                    "perGroupLimit": 100,
                    "perFeatureLimit": 100,
                    "groupingFeature": {
                        "elementInstanceType": "RegistryEvent",
                        "featureName": "timestamp"
                    },
                    "sortInGroupFeature": "None"
                },
                "queryTerminated": false,
                "pathResultCounts": [{
                    "featureDescriptor": {
                        "elementInstanceType": "RegistryEvent",
                        "featureName": "None"
                    },
                    "count": 71
                }],
                "guids": []
            },
            "status": "SUCCESS"
        }"""
        histobj = HistoryMockResponse()
        mock_results_response.return_value = get_mock_response(200, mocked_return_value, 'byte', histobj)
        mock_api_client.return_value = None

        query = json.dumps({
            "queryPath": [{
                "requestedType": "RegistryEvent",
                "filters": [{
                    "facetName": "registryProcess",
                    "filterType": "ContainsIgnoreCase",
                    "values": ["msiexec.exe"]
                }],
                "isResult": True
            }],
            "totalResultLimit": 1000,
            "perGroupLimit": 100,
            "templateContext": "SPECIFIC",
            "customFields": ["elementDisplayName", "self", "registryDataType",
                             "registryOperationType", "timestamp", "firstTime",
                             "detectionTimesNumber", "registryProcess",
                             "registryEntry", "data", "ownerMachine"
                             ]
        })

        transmission = stix_transmission.StixTransmission('cybereason',
                                                          self.connection(),
                                                          self.config())
        offset = 0
        length = 1
        results_response = transmission.results(query, offset, length)

        assert results_response is not None
        assert results_response['success'] is True
        assert 'data' in results_response
        assert results_response['data'] is not None

    def test_delete_query(self, mock_api_client):
        """ test for checking delete query"""
        mock_api_client.return_value = None
        search_id = json.dumps({
            "queryPath": [{
                "requestedType": "Connection",
                "filters": [{
                    "facetName": "elementDisplayName",
                    "filterType": "ContainsIgnoreCase",
                    "values": ["192.168.87.72:53235"]
                }],
                "isResult": True
            }],
            "totalResultLimit": 1000,
            "perGroupLimit": 100,
            "templateContext": "SPECIFIC",
            "customFields": ["elementDisplayName", "direction",
                             "ownerMachine", "ownerProcess",
                             "serverPort", "serverAddress",
                             "portType", "aggregatedReceivedBytesCount",
                             "aggregatedTransmittedBytesCount",
                             "remoteAddressCountryName", "dnsQuery",
                             "calculatedCreationTime", "domainName",
                             "endTime", "localPort", "portDescription",
                             "remotePort", "state", "isExternalConnection",
                             "isIncoming", "remoteAddressInternalExternalLocal",
                             "transportProtocol", "hasMalops", "hasSuspicions",
                             "relatedToMalop", "isWellKnownPort",
                             "isProcessLegit", "isProcessMalware", "localAddress",
                             "remoteAddress", "urlDomains"
                             ]
        })

        entry_point = EntryPoint(self.connection(), self.config())
        status_response = run_in_thread(entry_point.delete_query_connection, search_id)

        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is True

    def test_ping_exception(self, m_api_client):
        """ test to check ping box exception"""

        m_api_client.return_value = None
        transmission = stix_transmission.StixTransmission('cybereason',
                                                          self.connection(),
                                                          self.config()
                                                          )

        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False

    def test_file_result_exception(self, m_api_client):
        """ test to check result exception of file element"""

        m_api_client.return_value = None

        query = json.dumps({
            "queryPath": [{
                "requestedType": "File",
                "filters": [{
                    "facetName": "elementDisplayName",
                    "filterType": "ContainsIgnoreCase",
                    "values": ["sbsimulation_sb_265540_bs_254977.exe"]
                }],
                "isResult": True
            }],
            "totalResultLimit": 1000,
            "perGroupLimit": 100,
            "templateContext": "SPECIFIC",
            "customFields": ["elementDisplayName", "maliciousClassificationType",
                             "ownerMachine", "avRemediationStatus",
                             "signerInternalOrExternal", "signedInternalOrExternal",
                             "signatureVerifiedInternalOrExternal", "sha1String",
                             "createdTime", "modifiedTime", "size",
                             "correctedPath", "productName"
                             ]
        })

        transmission = stix_transmission.StixTransmission('cybereason',
                                                          self.connection(),
                                                          self.config())
        offset = 0
        length = 1
        results_response = transmission.results(query, offset, length)

        assert results_response is not None
        assert results_response['success'] is False
        assert 'error' in results_response
        assert results_response['error'] is not None

    @patch('stix_shifter_modules.cybereason.stix_transmission.api_client'
           '.APIClient.get_search_results')
    def test_result_invalidrequesterror(self, mock_results_response, mock_api_client):
        """ test for checking invalid request error"""
        invalidtext =ErrorTextInvalidRequest("InvalidRequest")
        mock_results_response.return_value = CybereasonMockError(402, invalidtext)
        mock_api_client.return_value = None

        query = json.dumps({
            "queryPath": [{
                "requestedType": "RegistryEvent",
                "filters": [{
                    "facetName": "registryProcess",
                    "filterType": "ContainsIgnoreCase",
                    "values": ["msiexec.exe"]
                }],
                "isResult": True
            }],
            "totalResultLimit": 1000,
            "perGroupLimit": 100,
            "templateContext": "TEMPLATE",
            "customFields": ["elementDisplayName", "self", "registryDataType",
                             "registryOperationType", "timestamp", "firstTime",
                             "detectionTimesNumber", "registryProcess",
                             "registryEntry", "data", "ownerMachine"
                             ]
        })

        transmission = stix_transmission.StixTransmission('cybereason',
                                                          self.connection(),
                                                          self.config())
        offset = 0
        length = 1
        results_response = transmission.results(query, offset, length)

        assert results_response is not None
        assert 'success' in results_response
        assert results_response['success'] is False
        assert 'error' in results_response

    @patch('stix_shifter_modules.cybereason.stix_transmission.api_client'
           '.APIClient.get_search_results')
    def test_result_internalservererror(self, mock_results_response, mock_api_client):
        """ test for checking internal server error"""
        errortext = ErrorTextInvalidRequest("InternalServerError")
        mock_results_response.return_value = CybereasonMockError(500, errortext)
        mock_api_client.return_value = None

        query = json.dumps({
            "QueryPath": [{
                "requestedType": "RegistryEvent",
                "filters": [{
                    "facetName": "registryProcess",
                    "filterType": "ContainsIgnoreCase",
                    "values": ["msiexec.exe"]
                }],
                "isResult": True
            }],
            "totalResultLimit": 1000,
            "perGroupLimit": 100,
            "templateContext": "TEMPLATE",
            "customFields": ["elementDisplayName", "self", "registryDataType",
                             "registryOperationType", "timestamp", "firstTime",
                             "detectionTimesNumber", "registryProcess",
                             "registryEntry", "data", "ownerMachine"
                             ]
        })

        transmission = stix_transmission.StixTransmission('cybereason',
                                                          self.connection(),
                                                          self.config())
        offset = 0
        length = 1
        results_response = transmission.results(query, offset, length)

        assert results_response is not None
        assert 'success' in results_response
        assert results_response['success'] is False
        assert 'error' in results_response

    @patch('stix_shifter_modules.cybereason.stix_transmission.api_client'
           '.APIClient.get_search_results')
    def test_result_invalidauthenticationerror(self, mock_results_response, mock_api_client):
        """ test for checking invalid request error"""
        obj = ErrorTextA()
        invalidtext = ErrorTextInvalid("AuthenticationError", obj)
        mock_results_response.return_value = CybereasonMockError(302, invalidtext)
        mock_api_client.return_value = None
        query = json.dumps({
            "queryPath": [{
                "requestedType": "RegistryEvent",
                "filters": [{
                    "facetName": "registryProcess",
                    "filterType": "ContainsIgnoreCase",
                    "values": ["msiexec.exe"]
                }],
                "isResult": True
            }],
            "totalResultLimit": 1000,
            "perGroupLimit": 100,
            "templateContext": "TEMPLATE",
            "customFields": ["elementDisplayName", "self", "registryDataType",
                             "registryOperationType", "timestamp", "firstTime",
                             "detectionTimesNumber", "registryProcess",
                             "registryEntry", "data", "ownerMachine"
                             ]
        })

        transmission = stix_transmission.StixTransmission('cybereason',
                                                          self.connection(),
                                                          self.config())
        offset = 0
        length = 1
        results_response = transmission.results(query, offset, length)

        assert results_response is not None
        assert 'success' in results_response
        assert results_response['success'] is False
        assert 'error' in results_response

    @patch('stix_shifter_modules.cybereason.stix_transmission.api_client'
           '.APIClient.session_log_out')
    @patch('stix_shifter_modules.cybereason.stix_transmission.api_client'
           '.APIClient.session_log_in')
    @patch('stix_shifter_modules.cybereason.stix_transmission.api_client'
           '.APIClient.ping_box')
    def test_ping_endpoint_invaliderror(self, mock_ping_source, mock_cookie,
                                        mock_logout, mock_api_client):
        """ test to check ping_data_source function"""
        obj = ErrorTextA()
        invalidtext = ErrorTextInvalid("""{"status":"authenticationerror"}""", obj)
        pingresponse = CybereasonMockError(302, invalidtext)
        mock_ping_source.return_value = pingresponse

        mock_logout.return_value = """{"response_code":200}"""
        mock_cookie.return_value = "JSESSIONID=52DCF6DF6CE150C27D2C7B96CCE66D7D"

        mock_api_client.return_value = None

        transmission = stix_transmission.StixTransmission('cybereason',
                                                          self.connection(),
                                                          self.config())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert 'error' in ping_response

    @patch('stix_shifter_modules.cybereason.stix_transmission.api_client'
           '.APIClient.session_log_out')
    @patch('stix_shifter_modules.cybereason.stix_transmission.api_client'
           '.APIClient.session_log_in')
    @patch('stix_shifter_modules.cybereason.stix_transmission.api_client'
           '.APIClient.get_search_results')
    def test_file_list_result(self, mock_results_response, mock_session,
                         mock_session_logout, mock_api_client):
        """ test to check result of file element"""
        mock_session_logout.return_value = get_mock_response(200)
        mock_session.return_value = "JSESSIONID=52DCF6DF6CE150C27D2C7B96CCE66D7D"
        mocked_return_value = """{
            "data": {
                "resultIdToElementDataMap": {
                    "-1837391212.1746789123229245971": {
                        "simpleValues": {
                            "applicablePid": {
                                "totalValues": 1,
                                "values": ["624"]
                            },
                            "commandLine": {
                                "totalValues": 1,
                                "values": ["C:\\\\WINDOWS\\\\System32\\\\svchost.exe \
                                -k NetworkService -p"]
                            },
                            "imageFile.md5String": {
                                "totalValues": 1,
                                "values": ["9520a99e77d6196d0d09833146424113"]
                            },
                            "creationTime": {
                                "totalValues": 1,
                                "values": ["1596848617500"]
                            },
                            "endTime": {
                                "totalValues": 1,
                                "values": ["1597955913267"]
                            },
                            "imageFile.sha256String": {
                                "totalValues": 1,
                                "values": ["dd191a5b23df92e12a8852291f\
                                9fb5ed594b76a28a5a464418442584afd1e048"]
                            },
                            "imageFile.sha1String": {
                                "totalValues": 1,
                                "values": ["75c5a97f521f760e32a4a9639a653eed862e9c61"]
                            },
                            "elementDisplayName": {
                                "totalValues": 1,
                                "values": ["svchost.exe"]
                            }
                        },
                        "elementValues": {
                            "parentProcess": {
                                "totalValues": 2,
                                "elementValues": [{
                                    "elementType": "Process",
                                    "guid": "-1837391212.4247194264269145540",
                                    "name": "services.exe",
                                    "hasSuspicions": false,
                                    "hasMalops": false
                                },
                                {
                                    "elementType": "Process",
                                    "guid": "-1837391213.4247194264269145540",
                                    "name": "svchost.exe",
                                    "hasSuspicions": false,
                                    "hasMalops": false
                                }],
                                "totalSuspicious": 0,
                                "totalMalicious": 0,
                                "guessedTotal": 0
                            },
                            "imageFile": {
                                "totalValues": 1,
                                "elementValues": [{
                                    "elementType": "File",
                                    "guid": "-1837391212.1251190729327068266",
                                    "name": "svchost.exe",
                                    "hasSuspicions": false,
                                    "hasMalops": false
                                }],
                                "totalSuspicious": 0,
                                "totalMalicious": 0,
                                "guessedTotal": 0
                            }
                        },
                        "suspicions": {
                            "blackListModuleSuspicion": 1602172848998,
                            "connectingToBlackListAddressSuspicion": 1611540009703
                        },
                        "filterData": {
                            "sortInGroupValue": "-1837391212.1746789123229245971",
                            "groupByValue": "svchost.exe"
                        },
                        "isMalicious": true,
                        "suspicionCount": 2,
                        "guidString": "-1837391212.1746789123229245971",
                        "labelsIds": null,
                        "malopPriority": null,
                        "suspect": true,
                        "malicious": true
                    }
                },
                "suspicionsMap": {
                    "blackListModuleSuspicion": {
                        "potentialEvidence": ["blackListModuleEvidence"],
                        "firstTimestamp": 1602172848998,
                        "totalSuspicions": 1
                    },
                    "connectingToBlackListAddressSuspicion": {
                        "potentialEvidence": ["hasBlackListConnectionEvidence"],
                        "firstTimestamp": 1611540009703,
                        "totalSuspicions": 1
                    }
                },
                "evidenceMap": {},
                "totalPossibleResults": 158260,
                "guessedPossibleResults": 0,
                "queryLimits": {
                    "totalResultLimit": 1,
                    "perGroupLimit": 1,
                    "perFeatureLimit": 1,
                    "groupingFeature": {
                        "elementInstanceType": "Process",
                        "featureName": "elementDisplayName"
                    },
                    "sortInGroupFeature": null
                },
                "queryTerminated": false,
                "pathResultCounts": [{
                    "featureDescriptor": {
                        "elementInstanceType": "Process",
                        "featureName": null
                    },
                    "count": 158260
                }],
                "guids": []
            },
            "status": "SUCCESS",
            "hidePartialSuccess": false,
            "message": "",
            "expectedResults": 1,
            "failures": 0
        }"""
        histobj = HistoryMockResponse()
        mock_results_response.return_value = get_mock_response(200, mocked_return_value, 'byte', histobj)
        mock_api_client.return_value = None

        query = json.dumps({
            "queryPath": [{
                "requestedType": "File",
                "filters": [{
                    "facetName": "elementDisplayName",
                    "filterType": "ContainsIgnoreCase",
                    "values": ["sbsimulation_sb_265540_bs_254977.exe"]
                }],
                "isResult": True
            }],
            "totalResultLimit": 1000,
            "perGroupLimit": 100,
            "templateContext": "SPECIFIC",
            "customFields": ["elementDisplayName", "maliciousClassificationType",
                             "ownerMachine", "avRemediationStatus",
                             "signerInternalOrExternal", "signedInternalOrExternal",
                             "signatureVerifiedInternalOrExternal", "sha1String",
                             "createdTime", "modifiedTime", "size",
                             "correctedPath", "productName"
                             ]
        })

        transmission = stix_transmission.StixTransmission('cybereason',
                                                          self.connection(),
                                                          self.config())
        offset = 0
        length = 1
        results_response = transmission.results(query, offset, length)

        assert results_response is not None
        assert results_response['success'] is True
        assert 'data' in results_response
        assert results_response['data'] is not None
