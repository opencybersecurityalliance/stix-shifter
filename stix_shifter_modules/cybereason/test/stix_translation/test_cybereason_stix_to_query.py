from stix_shifter.stix_translation import stix_translation
from stix_shifter_utils.utils.error_response import ErrorCode
import unittest
import re

translation = stix_translation.StixTranslation()


def _remove_timestamp_from_query(queries):
    pattern = r"'filterType':\s*'Between',\s*'values':\s*\[\d{0,13},\s*\d{0,13}\]"

    if isinstance(queries, list):
        return [re.sub(pattern, '', str(query)) for query in queries]
    elif isinstance(queries, str):
        return re.sub(pattern, '', queries)


class TestQueryTranslator(unittest.TestCase):
    """
    class to perform unit test case cybereason translate query
    """
    if __name__ == "__main__":
        unittest.main()

    def _test_query_assertions(self, query, queries):
        """
        to assert the each query in the list against expected result
        """
        self.assertIsInstance(queries, list)
        self.assertIsInstance(query, dict)
        self.assertIsInstance(query['queries'], list)
        for index, each_query in enumerate(query.get('queries'), start=0):
            self.assertEqual(each_query, queries[index])

    def test_ipv4_query(self):
        stix_pattern = "[ipv4-addr:value = '172.16.2.22']"
        query = translation.translate('cybereason', 'query', '{}', stix_pattern)

        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'queryPath': [{'requestedType': 'Connection', 'filters': [{'facetName': 'localAddress',"
                   " 'filterType': 'Equals', 'values': ['172.16.2.22']}, {'facetName': 'creationTime',"
                   " 'filterType': 'Between', 'values': [1638249307604, 1638249607604]}], 'isResult': True}],"
                   " 'queryLimits': {'groupingFeature': {'elementInstanceType': 'Connection', 'featureName': "
                   "'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, "
                   "'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', 'direction', "
                   "'ownerMachine', 'ownerProcess', 'serverPort', 'serverAddress', 'portType', "
                   "'aggregatedReceivedBytesCount', 'aggregatedTransmittedBytesCount', 'remoteAddressCountryName', "
                   "'dnsQuery', 'calculatedCreationTime', 'domainName', 'endTime', 'localPort', 'portDescription', "
                   "'remotePort', 'state', 'isExternalConnection', 'isIncoming', "
                   "'remoteAddressInternalExternalLocal', 'transportProtocol', 'hasMalops', 'hasSuspicions', "
                   "'relatedToMalop', 'isWellKnownPort', 'isProcessLegit', 'isProcessMalware', 'localAddress', "
                   "'remoteAddress', 'urlDomains']}",
                   "{'queryPath': [{'requestedType': 'Connection', 'filters': [{"
                   "'facetName': 'remoteAddress', 'filterType': 'Equals', 'values': ['172.16.2.22']}, {'facetName': "
                   "'creationTime', 'filterType': 'Between', 'values': [1638249307604, 1638249607604]}], 'isResult': "
                   "True}], 'queryLimits': {'groupingFeature': {'elementInstanceType': 'Connection', 'featureName': "
                   "'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, "
                   "'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', 'direction', "
                   "'ownerMachine', 'ownerProcess', 'serverPort', 'serverAddress', 'portType', "
                   "'aggregatedReceivedBytesCount', 'aggregatedTransmittedBytesCount', 'remoteAddressCountryName', "
                   "'dnsQuery', 'calculatedCreationTime', 'domainName', 'endTime', 'localPort', 'portDescription', "
                   "'remotePort', 'state', 'isExternalConnection', 'isIncoming', "
                   "'remoteAddressInternalExternalLocal', 'transportProtocol', 'hasMalops', 'hasSuspicions', "
                   "'relatedToMalop', 'isWellKnownPort', 'isProcessLegit', 'isProcessMalware', 'localAddress', "
                   "'remoteAddress', 'urlDomains']}"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_network_traffic_query(self):
        stix_pattern = "[network-traffic:dst_port=22]"
        query = translation.translate('cybereason', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'queryPath': [{'requestedType': 'Connection', 'filters': [{'facetName': 'remotePort',"
                   " 'filterType': 'Equals', 'values': [22]}, {'facetName': 'creationTime',"
                   " 'filterType': 'Between', 'values': [1638249439425, 1638249739425]}], 'isResult': True}],"
                   " 'queryLimits': {'groupingFeature': {'elementInstanceType': 'Connection', 'featureName': "
                   "'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, "
                   "'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', 'direction', "
                   "'ownerMachine', 'ownerProcess', 'serverPort', 'serverAddress', 'portType', "
                   "'aggregatedReceivedBytesCount', 'aggregatedTransmittedBytesCount', 'remoteAddressCountryName', "
                   "'dnsQuery', 'calculatedCreationTime', 'domainName', 'endTime', 'localPort', 'portDescription', "
                   "'remotePort', 'state', 'isExternalConnection', 'isIncoming', "
                   "'remoteAddressInternalExternalLocal', 'transportProtocol', 'hasMalops', 'hasSuspicions', "
                   "'relatedToMalop', 'isWellKnownPort', 'isProcessLegit', 'isProcessMalware', 'localAddress', "
                   "'remoteAddress', 'urlDomains']}"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_network_queries_greater_than(self):
        stix_pattern = "[network-traffic:dst_port>22]"
        query = translation.translate('cybereason', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'queryPath': [{'requestedType': 'Connection', 'filters': [{'facetName': 'remotePort', "
                   "'filterType': 'GreaterThan', 'values': [22]}, {'facetName': 'creationTime', "
                   "'filterType': 'Between', 'values': [1638249543967, 1638249843967]}], 'isResult': True}],"
                   " 'queryLimits': {"
                   "'groupingFeature': {'elementInstanceType': 'Connection', 'featureName': 'elementDisplayName'}}, "
                   "'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, 'templateContext': "
                   "'CUSTOM', 'customFields': ['elementDisplayName', 'direction', 'ownerMachine', 'ownerProcess', "
                   "'serverPort', 'serverAddress', 'portType', 'aggregatedReceivedBytesCount', "
                   "'aggregatedTransmittedBytesCount', 'remoteAddressCountryName', 'dnsQuery', "
                   "'calculatedCreationTime', 'domainName', 'endTime', 'localPort', 'portDescription', 'remotePort', "
                   "'state', 'isExternalConnection', 'isIncoming', 'remoteAddressInternalExternalLocal', "
                   "'transportProtocol', 'hasMalops', 'hasSuspicions', 'relatedToMalop', 'isWellKnownPort', "
                   "'isProcessLegit', 'isProcessMalware', 'localAddress', 'remoteAddress', 'urlDomains']}"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_network_queries_not_equals(self):
        stix_pattern = "[network-traffic:dst_port!=22]"
        query = translation.translate('cybereason', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'queryPath': [{'requestedType': 'Connection', 'filters': [{'facetName': 'remotePort', "
                   "'filterType': 'NotEquals', 'values': [22]}, {'facetName': 'creationTime',"
                   " 'filterType': 'Between', 'values': [1638249618181, 1638249918181]}], 'isResult': True}],"
                   " 'queryLimits': {"
                   "'groupingFeature': {'elementInstanceType': 'Connection', 'featureName': 'elementDisplayName'}}, "
                   "'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, 'templateContext': "
                   "'CUSTOM', 'customFields': ['elementDisplayName', 'direction', 'ownerMachine', 'ownerProcess', "
                   "'serverPort', 'serverAddress', 'portType', 'aggregatedReceivedBytesCount', "
                   "'aggregatedTransmittedBytesCount', 'remoteAddressCountryName', 'dnsQuery', "
                   "'calculatedCreationTime', 'domainName', 'endTime', 'localPort', 'portDescription', 'remotePort', "
                   "'state', 'isExternalConnection', 'isIncoming', 'remoteAddressInternalExternalLocal', "
                   "'transportProtocol', 'hasMalops', 'hasSuspicions', 'relatedToMalop', 'isWellKnownPort', "
                   "'isProcessLegit', 'isProcessMalware', 'localAddress', 'remoteAddress', 'urlDomains']}"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_network_queries_less_than(self):
        stix_pattern = "[network-traffic:dst_port<22]"
        query = translation.translate('cybereason', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'queryPath': [{'requestedType': 'Connection', 'filters': [{'facetName': 'remotePort', "
                   "'filterType': 'LessThan', 'values': [22]}, {'facetName': 'creationTime', "
                   "'filterType': 'Between', 'values': [1638249727494, 1638250027494]}], 'isResult': True}],"
                   " 'queryLimits': {"
                   "'groupingFeature': {'elementInstanceType': 'Connection', 'featureName': 'elementDisplayName'}}, "
                   "'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, 'templateContext': "
                   "'CUSTOM', 'customFields': ['elementDisplayName', 'direction', 'ownerMachine', 'ownerProcess', "
                   "'serverPort', 'serverAddress', 'portType', 'aggregatedReceivedBytesCount', "
                   "'aggregatedTransmittedBytesCount', 'remoteAddressCountryName', 'dnsQuery', "
                   "'calculatedCreationTime', 'domainName', 'endTime', 'localPort', 'portDescription', 'remotePort', "
                   "'state', 'isExternalConnection', 'isIncoming', 'remoteAddressInternalExternalLocal', "
                   "'transportProtocol', 'hasMalops', 'hasSuspicions', 'relatedToMalop', 'isWellKnownPort', "
                   "'isProcessLegit', 'isProcessMalware', 'localAddress', 'remoteAddress', 'urlDomains']}"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_network_queries_lessthan_or_equals(self):
        stix_pattern = "[network-traffic:dst_port<=22]"

        query = translation.translate('cybereason', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'queryPath': [{'requestedType': 'Connection', 'filters': [{'facetName': 'remotePort', "
                   "'filterType': 'LessOrEqualsTo', 'values': [22]}, {'facetName': 'creationTime',"
                   " 'filterType': 'Between', 'values': [1638249854906, 1638250154906]}], 'isResult': True}],"
                   " 'queryLimits': {"
                   "'groupingFeature': {'elementInstanceType': 'Connection', 'featureName': 'elementDisplayName'}}, "
                   "'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, 'templateContext': "
                   "'CUSTOM', 'customFields': ['elementDisplayName', 'direction', 'ownerMachine', 'ownerProcess', "
                   "'serverPort', 'serverAddress', 'portType', 'aggregatedReceivedBytesCount', "
                   "'aggregatedTransmittedBytesCount', 'remoteAddressCountryName', 'dnsQuery', "
                   "'calculatedCreationTime', 'domainName', 'endTime', 'localPort', 'portDescription', 'remotePort', "
                   "'state', 'isExternalConnection', 'isIncoming', 'remoteAddressInternalExternalLocal', "
                   "'transportProtocol', 'hasMalops', 'hasSuspicions', 'relatedToMalop', 'isWellKnownPort', "
                   "'isProcessLegit', 'isProcessMalware', 'localAddress', 'remoteAddress', 'urlDomains']}"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_network_queries_greaterthan_or_equals(self):
        stix_pattern = "[network-traffic:dst_port>=22]"
        query = translation.translate('cybereason', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'queryPath': [{'requestedType': 'Connection', 'filters':"
                   " [{'facetName': 'remotePort', 'filterType': 'GreaterOrEqualsTo', 'values': [22]},"
                   " {'facetName': 'creationTime', 'filterType': 'Between', 'values': [1638251439992, 1638251739992]}],"
                   " 'isResult': True}], 'queryLimits': {'groupingFeature': {'elementInstanceType': 'Connection', "
                   "'featureName': 'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, "
                   "'perGroupLimit': 1, 'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', "
                   "'direction', 'ownerMachine', 'ownerProcess', 'serverPort', 'serverAddress', 'portType', "
                   "'aggregatedReceivedBytesCount', 'aggregatedTransmittedBytesCount', 'remoteAddressCountryName', "
                   "'dnsQuery', 'calculatedCreationTime', 'domainName', 'endTime', 'localPort', 'portDescription', "
                   "'remotePort', 'state', 'isExternalConnection', 'isIncoming', "
                   "'remoteAddressInternalExternalLocal', 'transportProtocol', 'hasMalops', 'hasSuspicions', "
                   "'relatedToMalop', 'isWellKnownPort', 'isProcessLegit', 'isProcessMalware', 'localAddress', "
                   "'remoteAddress', 'urlDomains']}"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_network_queries_in_operator(self):
        stix_pattern = "[network-traffic:dst_port IN (80,443)]"
        query = translation.translate('cybereason', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'queryPath': [{'requestedType': 'Connection', 'filters':"
                   " [{'facetName': 'remotePort', 'filterType': 'Equals', 'values': [80, 443]},"
                   " {'facetName': 'creationTime', 'filterType': 'Between', 'values': [1638251545589, 1638251845589]}],"
                   " 'isResult': True}], 'queryLimits': {'groupingFeature': {'elementInstanceType': 'Connection', "
                   "'featureName': 'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, "
                   "'perGroupLimit': 1, 'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', "
                   "'direction', 'ownerMachine', 'ownerProcess', 'serverPort', 'serverAddress', 'portType', "
                   "'aggregatedReceivedBytesCount', 'aggregatedTransmittedBytesCount', 'remoteAddressCountryName', "
                   "'dnsQuery', 'calculatedCreationTime', 'domainName', 'endTime', 'localPort', 'portDescription', "
                   "'remotePort', 'state', 'isExternalConnection', 'isIncoming', "
                   "'remoteAddressInternalExternalLocal', 'transportProtocol', 'hasMalops', 'hasSuspicions', "
                   "'relatedToMalop', 'isWellKnownPort', 'isProcessLegit', 'isProcessMalware', 'localAddress', "
                   "'remoteAddress', 'urlDomains']}"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_process_like_operator(self):
        stix_pattern = "[process:name LIKE 'update.exe']"

        query = translation.translate('cybereason', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'queryPath': [{'requestedType': 'Process', 'filters': [{'facetName': 'elementDisplayName', "
                   "'filterType': 'ContainsIgnoreCase', 'values': ['update.exe']}, {'facetName': 'creationTime', "
                   "'filterType': 'Between', 'values': [1638251656373, 1638251956373]}], 'isResult': True}], "
                   "'queryLimits': {'groupingFeature': {'elementInstanceType': 'Process', 'featureName': "
                   "'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, "
                   "'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', 'creationTime', 'endTime', "
                   "'commandLine', 'imageFile.maliciousClassificationType', 'productType', 'children', "
                   "'parentProcess', 'ownerMachine', 'calculatedUser', 'imageFile', 'imageFile.sha1String', "
                   "'imageFile.md5String', 'imageFile.sha256String', 'imageFile.companyName', "
                   "'imageFile.productName', 'applicablePid', 'imageFileExtensionType', 'integrity', 'tid', "
                   "'isAggregate', 'isDotNetProtected', 'hasMalops', 'hasSuspicions', 'relatedToMalop', "
                   "'multipleSizeForHashEvidence', 'isImageFileVerified', 'knownMaliciousToolSuspicion', "
                   "'knownMalwareSuspicion', 'knownUnwantedSuspicion', 'isMaliciousByHashEvidence', "
                   "'imageFileMultipleCompanyNamesEvidence', 'multipleHashForUnsignedPeInfoEvidence', "
                   "'multipleNameForHashEvidence', 'unknownEvidence', 'rareHasPeMismatchEvidence', "
                   "'imageFile.signedInternalOrExternal', 'unknownUnsignedBySigningCompany', "
                   "'imageFileUnsignedEvidence', 'imageFileUnsignedHasSignedVersionEvidence', "
                   "'unwantedModuleSuspicion', 'imageFile.signerInternalOrExternal', 'architecture', "
                   "'commandLineContainsTempEvidence', 'hasChildren', 'hasClassification', 'hasVisibleWindows', "
                   "'hasWindows', 'isInstaller', 'isIdentifiedProduct', 'hasModuleFromTempEvidence', "
                   "'nonExecutableExtensionEvidence', 'isNotShellRunner', 'runningFromTempEvidence', "
                   "'shellOfNonShellRunnerSuspicion', 'shellWithElevatedPrivilegesEvidence', 'systemUserEvidence', "
                   "'hasExternalConnection', 'hasExternalConnectionToWellKnownPortEvidence', 'hasIncomingConnection', "
                   "'hasInternalConnection', 'hasMailConnectionForNonMailProcessEvidence', 'hasListeningConnection', "
                   "'hasOutgoingConnection', 'hasUnresolvedDnsQueriesFromDomain', "
                   "'multipleUnresolvedRecordNotExistsEvidence', 'hasNonDefaultResolverEvidence', "
                   "'parentProcessNotMatchHierarchySuspicion', 'parentProcessNotAdminUserEvidence', "
                   "'parentProcessFromRemovableDeviceEvidence', 'autorun', 'childrenCreatedByThread', 'connections', "
                   "'elevatedPrivilegeChildren', 'hackerToolChildren', 'hostProcess', 'hostUser', 'hostedChildren', "
                   "'injectedChildren', 'loadedModules', 'logonSession', 'remoteSession', 'service', 'execedBy', "
                   "'connectionsToMaliciousDomain', 'connectionsToMalwareAddresses', 'externalConnections', "
                   "'absoluteHighVolumeMaliciousAddressConnections', 'absoluteHighVolumeExternalConnections', "
                   "'incomingConnections', 'incomingExternalConnections', 'incomingInternalConnections', "
                   "'internalConnections', 'listeningConnections', 'localConnections', 'mailConnections', "
                   "'outgoingConnections', 'outgoingExternalConnections', 'outgoingInternalConnections', "
                   "'suspiciousExternalConnections', 'suspiciousInternalConnections', 'wellKnownPortConnections', "
                   "'lowTtlDnsQueries', 'nonDefaultResolverQueries', 'resolvedDnsQueriesDomainToDomain', "
                   "'resolvedDnsQueriesDomainToIp', 'resolvedDnsQueriesIpToDomain', "
                   "'suspiciousDnsQueryDomainToDomain', 'unresolvedQueryFromSuspiciousDomain', "
                   "'dnsQueryFromSuspiciousDomain', 'dnsQueryToSuspiciousDomain', 'unresolvedRecordNotExist', "
                   "'unresolvedDnsQueriesFromDomain', 'unresolvedDnsQueriesFromIp', "
                   "'maliciousToolClassificationModules', 'malwareClassificationModules', 'modulesNotInLoaderDbList', "
                   "'modulesFromTemp', 'unsignedWithSignedVersionModules', 'unwantedClassificationModules', "
                   "'accessToMalwareAddressInfectedProcess', 'connectingToBadReputationAddressSuspicion', "
                   "'hasMaliciousConnectionEvidence', 'hasSuspiciousExternalConnectionSuspicion', "
                   "'highNumberOfExternalConnectionsSuspicion', 'nonDefaultResolverSuspicion', "
                   "'hasRareExternalConnectionEvidence', 'hasRareRemoteAddressEvidence', 'suspiciousMailConnections', "
                   "'accessToMalwareAddressByUnknownProcess', "
                   "'hasAbsoluteHighVolumeConnectionToMaliciousAddressEvidence', "
                   "'hasAbsoluteHighVolumeExternalOutgoingConnectionEvidence', 'highDataTransmittedSuspicion', "
                   "'highDataVolumeTransmittedToMaliciousAddressSuspicion', "
                   "'highDataVolumeTransmittedByUnknownProcess', "
                   "'absoluteHighNumberOfInternalOutgoingEmbryonicConnectionsEvidence', 'dgaSuspicion', "
                   "'hasLowTtlDnsQueryEvidence', 'highUnresolvedToResolvedRateEvidence', "
                   "'manyUnresolvedRecordNotExistsEvidence', 'hasChildKnownHackerToolEvidence', "
                   "'hackingToolOfNonToolRunnerEvidence', 'hackingToolOfNonToolRunnerSuspicion', "
                   "'hasRareChildProcessKnownHackerToolEvidence', 'maliciousToolModuleSuspicion', "
                   "'deletedParentProcessEvidence', 'malwareModuleSuspicion', 'dualExtensionNameEvidence', "
                   "'hiddenFileExtensionEvidence', 'rightToLeftFileExtensionEvidence', "
                   "'screenSaverWithChildrenEvidence', 'suspicionsScreenSaverEvidence', 'hasPeFloatingCodeEvidence', "
                   "'hasSectionMismatchEvidence', 'detectedInjectedEvidence', 'detectedInjectingEvidence', "
                   "'detectedInjectingToProtectedProcessEvidence', 'hasInjectedChildren', "
                   "'hostingInjectedThreadEvidence', 'injectedProtectedProcessEvidence', "
                   "'maliciousInjectingCodeSuspicion', 'injectionMethod', 'isHostingInjectedThread', "
                   "'maliciousInjectedCodeSuspicion', 'maliciousPeExecutionSuspicion', "
                   "'hasSuspiciousInternalConnectionEvidence', 'highInternalOutgoingEmbryonicConnectionRateEvidence', "
                   "'highNumberOfInternalConnectionsEvidence', 'newProcessesAboveThresholdEvidence', "
                   "'hasRareInternalConnectionEvidence', 'elevatingPrivilegesToChildEvidence', "
                   "'parentProcessNotSystemUserEvidence', 'privilegeEscalationEvidence', "
                   "'firstExecutionOfDownloadedProcessEvidence', 'hasAutorun', 'newProcessEvidence', "
                   "'markedForPrevention', 'ransomwareAutoRemediationSuspended', 'totalNumOfInstances', "
                   "'lastMinuteNumOfInstances', 'lastSeenTimeStamp', 'wmiQueryStrings', 'isExectuedByWmi', "
                   "'absoluteHighNumberOfInternalConnectionsEvidence', 'scanningProcessSuspicion', "
                   "'imageFile.isDownloadedFromInternet', 'imageFile.downloadedFromDomain', "
                   "'imageFile.downloadedFromIpAddress', 'imageFile.downloadedFromUrl', "
                   "'imageFile.downloadedFromUrlReferrer', 'imageFile.downloadedFromEmailFrom', "
                   "'imageFile.downloadedFromEmailMessageId', 'imageFile.downloadedFromEmailSubject', 'rpcRequests', "
                   "'iconBase64', 'executionPrevented', 'isWhiteListClassification', 'matchedWhiteListRuleIds']}",
                   "{'queryPath': [{'requestedType': 'Process', 'filters': [{'facetName': 'parentProcess', "
                   "'filterType': 'ContainsIgnoreCase', 'values': ['update.exe']}, {'facetName': 'creationTime', "
                   "'filterType': 'Between', 'values': [1638251656373, 1638251956373]}], 'isResult': True}], "
                   "'queryLimits': {'groupingFeature': {'elementInstanceType': 'Process', 'featureName': "
                   "'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, "
                   "'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', 'creationTime', 'endTime', "
                   "'commandLine', 'imageFile.maliciousClassificationType', 'productType', 'children', "
                   "'parentProcess', 'ownerMachine', 'calculatedUser', 'imageFile', 'imageFile.sha1String', "
                   "'imageFile.md5String', 'imageFile.sha256String', 'imageFile.companyName', "
                   "'imageFile.productName', 'applicablePid', 'imageFileExtensionType', 'integrity', 'tid', "
                   "'isAggregate', 'isDotNetProtected', 'hasMalops', 'hasSuspicions', 'relatedToMalop', "
                   "'multipleSizeForHashEvidence', 'isImageFileVerified', 'knownMaliciousToolSuspicion', "
                   "'knownMalwareSuspicion', 'knownUnwantedSuspicion', 'isMaliciousByHashEvidence', "
                   "'imageFileMultipleCompanyNamesEvidence', 'multipleHashForUnsignedPeInfoEvidence', "
                   "'multipleNameForHashEvidence', 'unknownEvidence', 'rareHasPeMismatchEvidence', "
                   "'imageFile.signedInternalOrExternal', 'unknownUnsignedBySigningCompany', "
                   "'imageFileUnsignedEvidence', 'imageFileUnsignedHasSignedVersionEvidence', "
                   "'unwantedModuleSuspicion', 'imageFile.signerInternalOrExternal', 'architecture', "
                   "'commandLineContainsTempEvidence', 'hasChildren', 'hasClassification', 'hasVisibleWindows', "
                   "'hasWindows', 'isInstaller', 'isIdentifiedProduct', 'hasModuleFromTempEvidence', "
                   "'nonExecutableExtensionEvidence', 'isNotShellRunner', 'runningFromTempEvidence', "
                   "'shellOfNonShellRunnerSuspicion', 'shellWithElevatedPrivilegesEvidence', 'systemUserEvidence', "
                   "'hasExternalConnection', 'hasExternalConnectionToWellKnownPortEvidence', 'hasIncomingConnection', "
                   "'hasInternalConnection', 'hasMailConnectionForNonMailProcessEvidence', 'hasListeningConnection', "
                   "'hasOutgoingConnection', 'hasUnresolvedDnsQueriesFromDomain', "
                   "'multipleUnresolvedRecordNotExistsEvidence', 'hasNonDefaultResolverEvidence', "
                   "'parentProcessNotMatchHierarchySuspicion', 'parentProcessNotAdminUserEvidence', "
                   "'parentProcessFromRemovableDeviceEvidence', 'autorun', 'childrenCreatedByThread', 'connections', "
                   "'elevatedPrivilegeChildren', 'hackerToolChildren', 'hostProcess', 'hostUser', 'hostedChildren', "
                   "'injectedChildren', 'loadedModules', 'logonSession', 'remoteSession', 'service', 'execedBy', "
                   "'connectionsToMaliciousDomain', 'connectionsToMalwareAddresses', 'externalConnections', "
                   "'absoluteHighVolumeMaliciousAddressConnections', 'absoluteHighVolumeExternalConnections', "
                   "'incomingConnections', 'incomingExternalConnections', 'incomingInternalConnections', "
                   "'internalConnections', 'listeningConnections', 'localConnections', 'mailConnections', "
                   "'outgoingConnections', 'outgoingExternalConnections', 'outgoingInternalConnections', "
                   "'suspiciousExternalConnections', 'suspiciousInternalConnections', 'wellKnownPortConnections', "
                   "'lowTtlDnsQueries', 'nonDefaultResolverQueries', 'resolvedDnsQueriesDomainToDomain', "
                   "'resolvedDnsQueriesDomainToIp', 'resolvedDnsQueriesIpToDomain', "
                   "'suspiciousDnsQueryDomainToDomain', 'unresolvedQueryFromSuspiciousDomain', "
                   "'dnsQueryFromSuspiciousDomain', 'dnsQueryToSuspiciousDomain', 'unresolvedRecordNotExist', "
                   "'unresolvedDnsQueriesFromDomain', 'unresolvedDnsQueriesFromIp', "
                   "'maliciousToolClassificationModules', 'malwareClassificationModules', 'modulesNotInLoaderDbList', "
                   "'modulesFromTemp', 'unsignedWithSignedVersionModules', 'unwantedClassificationModules', "
                   "'accessToMalwareAddressInfectedProcess', 'connectingToBadReputationAddressSuspicion', "
                   "'hasMaliciousConnectionEvidence', 'hasSuspiciousExternalConnectionSuspicion', "
                   "'highNumberOfExternalConnectionsSuspicion', 'nonDefaultResolverSuspicion', "
                   "'hasRareExternalConnectionEvidence', 'hasRareRemoteAddressEvidence', 'suspiciousMailConnections', "
                   "'accessToMalwareAddressByUnknownProcess', "
                   "'hasAbsoluteHighVolumeConnectionToMaliciousAddressEvidence', "
                   "'hasAbsoluteHighVolumeExternalOutgoingConnectionEvidence', 'highDataTransmittedSuspicion', "
                   "'highDataVolumeTransmittedToMaliciousAddressSuspicion', "
                   "'highDataVolumeTransmittedByUnknownProcess', "
                   "'absoluteHighNumberOfInternalOutgoingEmbryonicConnectionsEvidence', 'dgaSuspicion', "
                   "'hasLowTtlDnsQueryEvidence', 'highUnresolvedToResolvedRateEvidence', "
                   "'manyUnresolvedRecordNotExistsEvidence', 'hasChildKnownHackerToolEvidence', "
                   "'hackingToolOfNonToolRunnerEvidence', 'hackingToolOfNonToolRunnerSuspicion', "
                   "'hasRareChildProcessKnownHackerToolEvidence', 'maliciousToolModuleSuspicion', "
                   "'deletedParentProcessEvidence', 'malwareModuleSuspicion', 'dualExtensionNameEvidence', "
                   "'hiddenFileExtensionEvidence', 'rightToLeftFileExtensionEvidence', "
                   "'screenSaverWithChildrenEvidence', 'suspicionsScreenSaverEvidence', 'hasPeFloatingCodeEvidence', "
                   "'hasSectionMismatchEvidence', 'detectedInjectedEvidence', 'detectedInjectingEvidence', "
                   "'detectedInjectingToProtectedProcessEvidence', 'hasInjectedChildren', "
                   "'hostingInjectedThreadEvidence', 'injectedProtectedProcessEvidence', "
                   "'maliciousInjectingCodeSuspicion', 'injectionMethod', 'isHostingInjectedThread', "
                   "'maliciousInjectedCodeSuspicion', 'maliciousPeExecutionSuspicion', "
                   "'hasSuspiciousInternalConnectionEvidence', 'highInternalOutgoingEmbryonicConnectionRateEvidence', "
                   "'highNumberOfInternalConnectionsEvidence', 'newProcessesAboveThresholdEvidence', "
                   "'hasRareInternalConnectionEvidence', 'elevatingPrivilegesToChildEvidence', "
                   "'parentProcessNotSystemUserEvidence', 'privilegeEscalationEvidence', "
                   "'firstExecutionOfDownloadedProcessEvidence', 'hasAutorun', 'newProcessEvidence', "
                   "'markedForPrevention', 'ransomwareAutoRemediationSuspended', 'totalNumOfInstances', "
                   "'lastMinuteNumOfInstances', 'lastSeenTimeStamp', 'wmiQueryStrings', 'isExectuedByWmi', "
                   "'absoluteHighNumberOfInternalConnectionsEvidence', 'scanningProcessSuspicion', "
                   "'imageFile.isDownloadedFromInternet', 'imageFile.downloadedFromDomain', "
                   "'imageFile.downloadedFromIpAddress', 'imageFile.downloadedFromUrl', "
                   "'imageFile.downloadedFromUrlReferrer', 'imageFile.downloadedFromEmailFrom', "
                   "'imageFile.downloadedFromEmailMessageId', 'imageFile.downloadedFromEmailSubject', 'rpcRequests', "
                   "'iconBase64', 'executionPrevented', 'isWhiteListClassification', 'matchedWhiteListRuleIds']}",
                   "{'queryPath': [{'requestedType': 'Process', 'filters': [{'facetName': 'execedBy', "
                   "'filterType': 'ContainsIgnoreCase', 'values': ['update.exe']}, {'facetName': 'creationTime', "
                   "'filterType': 'Between', 'values': [1638251656373, 1638251956373]}], 'isResult': True}], "
                   "'queryLimits': {'groupingFeature': {'elementInstanceType': 'Process', 'featureName': "
                   "'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, "
                   "'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', 'creationTime', 'endTime', "
                   "'commandLine', 'imageFile.maliciousClassificationType', 'productType', 'children', "
                   "'parentProcess', 'ownerMachine', 'calculatedUser', 'imageFile', 'imageFile.sha1String', "
                   "'imageFile.md5String', 'imageFile.sha256String', 'imageFile.companyName', "
                   "'imageFile.productName', 'applicablePid', 'imageFileExtensionType', 'integrity', 'tid', "
                   "'isAggregate', 'isDotNetProtected', 'hasMalops', 'hasSuspicions', 'relatedToMalop', "
                   "'multipleSizeForHashEvidence', 'isImageFileVerified', 'knownMaliciousToolSuspicion', "
                   "'knownMalwareSuspicion', 'knownUnwantedSuspicion', 'isMaliciousByHashEvidence', "
                   "'imageFileMultipleCompanyNamesEvidence', 'multipleHashForUnsignedPeInfoEvidence', "
                   "'multipleNameForHashEvidence', 'unknownEvidence', 'rareHasPeMismatchEvidence', "
                   "'imageFile.signedInternalOrExternal', 'unknownUnsignedBySigningCompany', "
                   "'imageFileUnsignedEvidence', 'imageFileUnsignedHasSignedVersionEvidence', "
                   "'unwantedModuleSuspicion', 'imageFile.signerInternalOrExternal', 'architecture', "
                   "'commandLineContainsTempEvidence', 'hasChildren', 'hasClassification', 'hasVisibleWindows', "
                   "'hasWindows', 'isInstaller', 'isIdentifiedProduct', 'hasModuleFromTempEvidence', "
                   "'nonExecutableExtensionEvidence', 'isNotShellRunner', 'runningFromTempEvidence', "
                   "'shellOfNonShellRunnerSuspicion', 'shellWithElevatedPrivilegesEvidence', 'systemUserEvidence', "
                   "'hasExternalConnection', 'hasExternalConnectionToWellKnownPortEvidence', 'hasIncomingConnection', "
                   "'hasInternalConnection', 'hasMailConnectionForNonMailProcessEvidence', 'hasListeningConnection', "
                   "'hasOutgoingConnection', 'hasUnresolvedDnsQueriesFromDomain', "
                   "'multipleUnresolvedRecordNotExistsEvidence', 'hasNonDefaultResolverEvidence', "
                   "'parentProcessNotMatchHierarchySuspicion', 'parentProcessNotAdminUserEvidence', "
                   "'parentProcessFromRemovableDeviceEvidence', 'autorun', 'childrenCreatedByThread', 'connections', "
                   "'elevatedPrivilegeChildren', 'hackerToolChildren', 'hostProcess', 'hostUser', 'hostedChildren', "
                   "'injectedChildren', 'loadedModules', 'logonSession', 'remoteSession', 'service', 'execedBy', "
                   "'connectionsToMaliciousDomain', 'connectionsToMalwareAddresses', 'externalConnections', "
                   "'absoluteHighVolumeMaliciousAddressConnections', 'absoluteHighVolumeExternalConnections', "
                   "'incomingConnections', 'incomingExternalConnections', 'incomingInternalConnections', "
                   "'internalConnections', 'listeningConnections', 'localConnections', 'mailConnections', "
                   "'outgoingConnections', 'outgoingExternalConnections', 'outgoingInternalConnections', "
                   "'suspiciousExternalConnections', 'suspiciousInternalConnections', 'wellKnownPortConnections', "
                   "'lowTtlDnsQueries', 'nonDefaultResolverQueries', 'resolvedDnsQueriesDomainToDomain', "
                   "'resolvedDnsQueriesDomainToIp', 'resolvedDnsQueriesIpToDomain', "
                   "'suspiciousDnsQueryDomainToDomain', 'unresolvedQueryFromSuspiciousDomain', "
                   "'dnsQueryFromSuspiciousDomain', 'dnsQueryToSuspiciousDomain', 'unresolvedRecordNotExist', "
                   "'unresolvedDnsQueriesFromDomain', 'unresolvedDnsQueriesFromIp', "
                   "'maliciousToolClassificationModules', 'malwareClassificationModules', 'modulesNotInLoaderDbList', "
                   "'modulesFromTemp', 'unsignedWithSignedVersionModules', 'unwantedClassificationModules', "
                   "'accessToMalwareAddressInfectedProcess', 'connectingToBadReputationAddressSuspicion', "
                   "'hasMaliciousConnectionEvidence', 'hasSuspiciousExternalConnectionSuspicion', "
                   "'highNumberOfExternalConnectionsSuspicion', 'nonDefaultResolverSuspicion', "
                   "'hasRareExternalConnectionEvidence', 'hasRareRemoteAddressEvidence', 'suspiciousMailConnections', "
                   "'accessToMalwareAddressByUnknownProcess', "
                   "'hasAbsoluteHighVolumeConnectionToMaliciousAddressEvidence', "
                   "'hasAbsoluteHighVolumeExternalOutgoingConnectionEvidence', 'highDataTransmittedSuspicion', "
                   "'highDataVolumeTransmittedToMaliciousAddressSuspicion', "
                   "'highDataVolumeTransmittedByUnknownProcess', "
                   "'absoluteHighNumberOfInternalOutgoingEmbryonicConnectionsEvidence', 'dgaSuspicion', "
                   "'hasLowTtlDnsQueryEvidence', 'highUnresolvedToResolvedRateEvidence', "
                   "'manyUnresolvedRecordNotExistsEvidence', 'hasChildKnownHackerToolEvidence', "
                   "'hackingToolOfNonToolRunnerEvidence', 'hackingToolOfNonToolRunnerSuspicion', "
                   "'hasRareChildProcessKnownHackerToolEvidence', 'maliciousToolModuleSuspicion', "
                   "'deletedParentProcessEvidence', 'malwareModuleSuspicion', 'dualExtensionNameEvidence', "
                   "'hiddenFileExtensionEvidence', 'rightToLeftFileExtensionEvidence', "
                   "'screenSaverWithChildrenEvidence', 'suspicionsScreenSaverEvidence', 'hasPeFloatingCodeEvidence', "
                   "'hasSectionMismatchEvidence', 'detectedInjectedEvidence', 'detectedInjectingEvidence', "
                   "'detectedInjectingToProtectedProcessEvidence', 'hasInjectedChildren', "
                   "'hostingInjectedThreadEvidence', 'injectedProtectedProcessEvidence', "
                   "'maliciousInjectingCodeSuspicion', 'injectionMethod', 'isHostingInjectedThread', "
                   "'maliciousInjectedCodeSuspicion', 'maliciousPeExecutionSuspicion', "
                   "'hasSuspiciousInternalConnectionEvidence', 'highInternalOutgoingEmbryonicConnectionRateEvidence', "
                   "'highNumberOfInternalConnectionsEvidence', 'newProcessesAboveThresholdEvidence', "
                   "'hasRareInternalConnectionEvidence', 'elevatingPrivilegesToChildEvidence', "
                   "'parentProcessNotSystemUserEvidence', 'privilegeEscalationEvidence', "
                   "'firstExecutionOfDownloadedProcessEvidence', 'hasAutorun', 'newProcessEvidence', "
                   "'markedForPrevention', 'ransomwareAutoRemediationSuspended', 'totalNumOfInstances', "
                   "'lastMinuteNumOfInstances', 'lastSeenTimeStamp', 'wmiQueryStrings', 'isExectuedByWmi', "
                   "'absoluteHighNumberOfInternalConnectionsEvidence', 'scanningProcessSuspicion', "
                   "'imageFile.isDownloadedFromInternet', 'imageFile.downloadedFromDomain', "
                   "'imageFile.downloadedFromIpAddress', 'imageFile.downloadedFromUrl', "
                   "'imageFile.downloadedFromUrlReferrer', 'imageFile.downloadedFromEmailFrom', "
                   "'imageFile.downloadedFromEmailMessageId', 'imageFile.downloadedFromEmailSubject', 'rpcRequests', "
                   "'iconBase64', 'executionPrevented', 'isWhiteListClassification', 'matchedWhiteListRuleIds']}"
                   ]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_process_matches_operator(self):
        stix_pattern = "[process:name MATCHES 'update.exe']"
        query = translation.translate('cybereason', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'queryPath': [{'requestedType': 'Process', 'filters': [{'facetName': 'elementDisplayName', "
                   "'filterType': 'ContainsIgnoreCase', 'values': ['update.exe']}, {'facetName': 'creationTime', "
                   "'filterType': 'Between', 'values': [1638267965704, 1638268265704]}], 'isResult': True}], "
                   "'queryLimits': {'groupingFeature': {'elementInstanceType': 'Process', 'featureName': "
                   "'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, "
                   "'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', 'creationTime', 'endTime', "
                   "'commandLine', 'imageFile.maliciousClassificationType', 'productType', 'children', "
                   "'parentProcess', 'ownerMachine', 'calculatedUser', 'imageFile', 'imageFile.sha1String', "
                   "'imageFile.md5String', 'imageFile.sha256String', 'imageFile.companyName', "
                   "'imageFile.productName', 'applicablePid', 'imageFileExtensionType', 'integrity', 'tid', "
                   "'isAggregate', 'isDotNetProtected', 'hasMalops', 'hasSuspicions', 'relatedToMalop', "
                   "'multipleSizeForHashEvidence', 'isImageFileVerified', 'knownMaliciousToolSuspicion', "
                   "'knownMalwareSuspicion', 'knownUnwantedSuspicion', 'isMaliciousByHashEvidence', "
                   "'imageFileMultipleCompanyNamesEvidence', 'multipleHashForUnsignedPeInfoEvidence', "
                   "'multipleNameForHashEvidence', 'unknownEvidence', 'rareHasPeMismatchEvidence', "
                   "'imageFile.signedInternalOrExternal', 'unknownUnsignedBySigningCompany', "
                   "'imageFileUnsignedEvidence', 'imageFileUnsignedHasSignedVersionEvidence', "
                   "'unwantedModuleSuspicion', 'imageFile.signerInternalOrExternal', 'architecture', "
                   "'commandLineContainsTempEvidence', 'hasChildren', 'hasClassification', 'hasVisibleWindows', "
                   "'hasWindows', 'isInstaller', 'isIdentifiedProduct', 'hasModuleFromTempEvidence', "
                   "'nonExecutableExtensionEvidence', 'isNotShellRunner', 'runningFromTempEvidence', "
                   "'shellOfNonShellRunnerSuspicion', 'shellWithElevatedPrivilegesEvidence', 'systemUserEvidence', "
                   "'hasExternalConnection', 'hasExternalConnectionToWellKnownPortEvidence', 'hasIncomingConnection', "
                   "'hasInternalConnection', 'hasMailConnectionForNonMailProcessEvidence', 'hasListeningConnection', "
                   "'hasOutgoingConnection', 'hasUnresolvedDnsQueriesFromDomain', "
                   "'multipleUnresolvedRecordNotExistsEvidence', 'hasNonDefaultResolverEvidence', "
                   "'parentProcessNotMatchHierarchySuspicion', 'parentProcessNotAdminUserEvidence', "
                   "'parentProcessFromRemovableDeviceEvidence', 'autorun', 'childrenCreatedByThread', 'connections', "
                   "'elevatedPrivilegeChildren', 'hackerToolChildren', 'hostProcess', 'hostUser', 'hostedChildren', "
                   "'injectedChildren', 'loadedModules', 'logonSession', 'remoteSession', 'service', 'execedBy', "
                   "'connectionsToMaliciousDomain', 'connectionsToMalwareAddresses', 'externalConnections', "
                   "'absoluteHighVolumeMaliciousAddressConnections', 'absoluteHighVolumeExternalConnections', "
                   "'incomingConnections', 'incomingExternalConnections', 'incomingInternalConnections', "
                   "'internalConnections', 'listeningConnections', 'localConnections', 'mailConnections', "
                   "'outgoingConnections', 'outgoingExternalConnections', 'outgoingInternalConnections', "
                   "'suspiciousExternalConnections', 'suspiciousInternalConnections', 'wellKnownPortConnections', "
                   "'lowTtlDnsQueries', 'nonDefaultResolverQueries', 'resolvedDnsQueriesDomainToDomain', "
                   "'resolvedDnsQueriesDomainToIp', 'resolvedDnsQueriesIpToDomain', "
                   "'suspiciousDnsQueryDomainToDomain', 'unresolvedQueryFromSuspiciousDomain', "
                   "'dnsQueryFromSuspiciousDomain', 'dnsQueryToSuspiciousDomain', 'unresolvedRecordNotExist', "
                   "'unresolvedDnsQueriesFromDomain', 'unresolvedDnsQueriesFromIp', "
                   "'maliciousToolClassificationModules', 'malwareClassificationModules', 'modulesNotInLoaderDbList', "
                   "'modulesFromTemp', 'unsignedWithSignedVersionModules', 'unwantedClassificationModules', "
                   "'accessToMalwareAddressInfectedProcess', 'connectingToBadReputationAddressSuspicion', "
                   "'hasMaliciousConnectionEvidence', 'hasSuspiciousExternalConnectionSuspicion', "
                   "'highNumberOfExternalConnectionsSuspicion', 'nonDefaultResolverSuspicion', "
                   "'hasRareExternalConnectionEvidence', 'hasRareRemoteAddressEvidence', 'suspiciousMailConnections', "
                   "'accessToMalwareAddressByUnknownProcess', "
                   "'hasAbsoluteHighVolumeConnectionToMaliciousAddressEvidence', "
                   "'hasAbsoluteHighVolumeExternalOutgoingConnectionEvidence', 'highDataTransmittedSuspicion', "
                   "'highDataVolumeTransmittedToMaliciousAddressSuspicion', "
                   "'highDataVolumeTransmittedByUnknownProcess', "
                   "'absoluteHighNumberOfInternalOutgoingEmbryonicConnectionsEvidence', 'dgaSuspicion', "
                   "'hasLowTtlDnsQueryEvidence', 'highUnresolvedToResolvedRateEvidence', "
                   "'manyUnresolvedRecordNotExistsEvidence', 'hasChildKnownHackerToolEvidence', "
                   "'hackingToolOfNonToolRunnerEvidence', 'hackingToolOfNonToolRunnerSuspicion', "
                   "'hasRareChildProcessKnownHackerToolEvidence', 'maliciousToolModuleSuspicion', "
                   "'deletedParentProcessEvidence', 'malwareModuleSuspicion', 'dualExtensionNameEvidence', "
                   "'hiddenFileExtensionEvidence', 'rightToLeftFileExtensionEvidence', "
                   "'screenSaverWithChildrenEvidence', 'suspicionsScreenSaverEvidence', 'hasPeFloatingCodeEvidence', "
                   "'hasSectionMismatchEvidence', 'detectedInjectedEvidence', 'detectedInjectingEvidence', "
                   "'detectedInjectingToProtectedProcessEvidence', 'hasInjectedChildren', "
                   "'hostingInjectedThreadEvidence', 'injectedProtectedProcessEvidence', "
                   "'maliciousInjectingCodeSuspicion', 'injectionMethod', 'isHostingInjectedThread', "
                   "'maliciousInjectedCodeSuspicion', 'maliciousPeExecutionSuspicion', "
                   "'hasSuspiciousInternalConnectionEvidence', 'highInternalOutgoingEmbryonicConnectionRateEvidence', "
                   "'highNumberOfInternalConnectionsEvidence', 'newProcessesAboveThresholdEvidence', "
                   "'hasRareInternalConnectionEvidence', 'elevatingPrivilegesToChildEvidence', "
                   "'parentProcessNotSystemUserEvidence', 'privilegeEscalationEvidence', "
                   "'firstExecutionOfDownloadedProcessEvidence', 'hasAutorun', 'newProcessEvidence', "
                   "'markedForPrevention', 'ransomwareAutoRemediationSuspended', 'totalNumOfInstances', "
                   "'lastMinuteNumOfInstances', 'lastSeenTimeStamp', 'wmiQueryStrings', 'isExectuedByWmi', "
                   "'absoluteHighNumberOfInternalConnectionsEvidence', 'scanningProcessSuspicion', "
                   "'imageFile.isDownloadedFromInternet', 'imageFile.downloadedFromDomain', "
                   "'imageFile.downloadedFromIpAddress', 'imageFile.downloadedFromUrl', "
                   "'imageFile.downloadedFromUrlReferrer', 'imageFile.downloadedFromEmailFrom', "
                   "'imageFile.downloadedFromEmailMessageId', 'imageFile.downloadedFromEmailSubject', 'rpcRequests', "
                   "'iconBase64', 'executionPrevented', 'isWhiteListClassification', 'matchedWhiteListRuleIds']}",
                   "{'queryPath': [{'requestedType': 'Process', 'filters': [{'facetName': 'parentProcess', "
                   "'filterType': 'ContainsIgnoreCase', 'values': ['update.exe']}, {'facetName': 'creationTime', "
                   "'filterType': 'Between', 'values': [1638267965704, 1638268265704]}], 'isResult': True}], "
                   "'queryLimits': {'groupingFeature': {'elementInstanceType': 'Process', 'featureName': "
                   "'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, "
                   "'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', 'creationTime', 'endTime', "
                   "'commandLine', 'imageFile.maliciousClassificationType', 'productType', 'children', "
                   "'parentProcess', 'ownerMachine', 'calculatedUser', 'imageFile', 'imageFile.sha1String', "
                   "'imageFile.md5String', 'imageFile.sha256String', 'imageFile.companyName', "
                   "'imageFile.productName', 'applicablePid', 'imageFileExtensionType', 'integrity', 'tid', "
                   "'isAggregate', 'isDotNetProtected', 'hasMalops', 'hasSuspicions', 'relatedToMalop', "
                   "'multipleSizeForHashEvidence', 'isImageFileVerified', 'knownMaliciousToolSuspicion', "
                   "'knownMalwareSuspicion', 'knownUnwantedSuspicion', 'isMaliciousByHashEvidence', "
                   "'imageFileMultipleCompanyNamesEvidence', 'multipleHashForUnsignedPeInfoEvidence', "
                   "'multipleNameForHashEvidence', 'unknownEvidence', 'rareHasPeMismatchEvidence', "
                   "'imageFile.signedInternalOrExternal', 'unknownUnsignedBySigningCompany', "
                   "'imageFileUnsignedEvidence', 'imageFileUnsignedHasSignedVersionEvidence', "
                   "'unwantedModuleSuspicion', 'imageFile.signerInternalOrExternal', 'architecture', "
                   "'commandLineContainsTempEvidence', 'hasChildren', 'hasClassification', 'hasVisibleWindows', "
                   "'hasWindows', 'isInstaller', 'isIdentifiedProduct', 'hasModuleFromTempEvidence', "
                   "'nonExecutableExtensionEvidence', 'isNotShellRunner', 'runningFromTempEvidence', "
                   "'shellOfNonShellRunnerSuspicion', 'shellWithElevatedPrivilegesEvidence', 'systemUserEvidence', "
                   "'hasExternalConnection', 'hasExternalConnectionToWellKnownPortEvidence', 'hasIncomingConnection', "
                   "'hasInternalConnection', 'hasMailConnectionForNonMailProcessEvidence', 'hasListeningConnection', "
                   "'hasOutgoingConnection', 'hasUnresolvedDnsQueriesFromDomain', "
                   "'multipleUnresolvedRecordNotExistsEvidence', 'hasNonDefaultResolverEvidence', "
                   "'parentProcessNotMatchHierarchySuspicion', 'parentProcessNotAdminUserEvidence', "
                   "'parentProcessFromRemovableDeviceEvidence', 'autorun', 'childrenCreatedByThread', 'connections', "
                   "'elevatedPrivilegeChildren', 'hackerToolChildren', 'hostProcess', 'hostUser', 'hostedChildren', "
                   "'injectedChildren', 'loadedModules', 'logonSession', 'remoteSession', 'service', 'execedBy', "
                   "'connectionsToMaliciousDomain', 'connectionsToMalwareAddresses', 'externalConnections', "
                   "'absoluteHighVolumeMaliciousAddressConnections', 'absoluteHighVolumeExternalConnections', "
                   "'incomingConnections', 'incomingExternalConnections', 'incomingInternalConnections', "
                   "'internalConnections', 'listeningConnections', 'localConnections', 'mailConnections', "
                   "'outgoingConnections', 'outgoingExternalConnections', 'outgoingInternalConnections', "
                   "'suspiciousExternalConnections', 'suspiciousInternalConnections', 'wellKnownPortConnections', "
                   "'lowTtlDnsQueries', 'nonDefaultResolverQueries', 'resolvedDnsQueriesDomainToDomain', "
                   "'resolvedDnsQueriesDomainToIp', 'resolvedDnsQueriesIpToDomain', "
                   "'suspiciousDnsQueryDomainToDomain', 'unresolvedQueryFromSuspiciousDomain', "
                   "'dnsQueryFromSuspiciousDomain', 'dnsQueryToSuspiciousDomain', 'unresolvedRecordNotExist', "
                   "'unresolvedDnsQueriesFromDomain', 'unresolvedDnsQueriesFromIp', "
                   "'maliciousToolClassificationModules', 'malwareClassificationModules', 'modulesNotInLoaderDbList', "
                   "'modulesFromTemp', 'unsignedWithSignedVersionModules', 'unwantedClassificationModules', "
                   "'accessToMalwareAddressInfectedProcess', 'connectingToBadReputationAddressSuspicion', "
                   "'hasMaliciousConnectionEvidence', 'hasSuspiciousExternalConnectionSuspicion', "
                   "'highNumberOfExternalConnectionsSuspicion', 'nonDefaultResolverSuspicion', "
                   "'hasRareExternalConnectionEvidence', 'hasRareRemoteAddressEvidence', 'suspiciousMailConnections', "
                   "'accessToMalwareAddressByUnknownProcess', "
                   "'hasAbsoluteHighVolumeConnectionToMaliciousAddressEvidence', "
                   "'hasAbsoluteHighVolumeExternalOutgoingConnectionEvidence', 'highDataTransmittedSuspicion', "
                   "'highDataVolumeTransmittedToMaliciousAddressSuspicion', "
                   "'highDataVolumeTransmittedByUnknownProcess', "
                   "'absoluteHighNumberOfInternalOutgoingEmbryonicConnectionsEvidence', 'dgaSuspicion', "
                   "'hasLowTtlDnsQueryEvidence', 'highUnresolvedToResolvedRateEvidence', "
                   "'manyUnresolvedRecordNotExistsEvidence', 'hasChildKnownHackerToolEvidence', "
                   "'hackingToolOfNonToolRunnerEvidence', 'hackingToolOfNonToolRunnerSuspicion', "
                   "'hasRareChildProcessKnownHackerToolEvidence', 'maliciousToolModuleSuspicion', "
                   "'deletedParentProcessEvidence', 'malwareModuleSuspicion', 'dualExtensionNameEvidence', "
                   "'hiddenFileExtensionEvidence', 'rightToLeftFileExtensionEvidence', "
                   "'screenSaverWithChildrenEvidence', 'suspicionsScreenSaverEvidence', 'hasPeFloatingCodeEvidence', "
                   "'hasSectionMismatchEvidence', 'detectedInjectedEvidence', 'detectedInjectingEvidence', "
                   "'detectedInjectingToProtectedProcessEvidence', 'hasInjectedChildren', "
                   "'hostingInjectedThreadEvidence', 'injectedProtectedProcessEvidence', "
                   "'maliciousInjectingCodeSuspicion', 'injectionMethod', 'isHostingInjectedThread', "
                   "'maliciousInjectedCodeSuspicion', 'maliciousPeExecutionSuspicion', "
                   "'hasSuspiciousInternalConnectionEvidence', 'highInternalOutgoingEmbryonicConnectionRateEvidence', "
                   "'highNumberOfInternalConnectionsEvidence', 'newProcessesAboveThresholdEvidence', "
                   "'hasRareInternalConnectionEvidence', 'elevatingPrivilegesToChildEvidence', "
                   "'parentProcessNotSystemUserEvidence', 'privilegeEscalationEvidence', "
                   "'firstExecutionOfDownloadedProcessEvidence', 'hasAutorun', 'newProcessEvidence', "
                   "'markedForPrevention', 'ransomwareAutoRemediationSuspended', 'totalNumOfInstances', "
                   "'lastMinuteNumOfInstances', 'lastSeenTimeStamp', 'wmiQueryStrings', 'isExectuedByWmi', "
                   "'absoluteHighNumberOfInternalConnectionsEvidence', 'scanningProcessSuspicion', "
                   "'imageFile.isDownloadedFromInternet', 'imageFile.downloadedFromDomain', "
                   "'imageFile.downloadedFromIpAddress', 'imageFile.downloadedFromUrl', "
                   "'imageFile.downloadedFromUrlReferrer', 'imageFile.downloadedFromEmailFrom', "
                   "'imageFile.downloadedFromEmailMessageId', 'imageFile.downloadedFromEmailSubject', 'rpcRequests', "
                   "'iconBase64', 'executionPrevented', 'isWhiteListClassification', 'matchedWhiteListRuleIds']}",
                   "{'queryPath': [{'requestedType': 'Process', 'filters': [{'facetName': 'execedBy', "
                   "'filterType': 'ContainsIgnoreCase', 'values': ['update.exe']}, {'facetName': 'creationTime', "
                   "'filterType': 'Between', 'values': [1638267965704, 1638268265704]}], 'isResult': True}], "
                   "'queryLimits': {'groupingFeature': {'elementInstanceType': 'Process', 'featureName': "
                   "'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, "
                   "'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', 'creationTime', 'endTime', "
                   "'commandLine', 'imageFile.maliciousClassificationType', 'productType', 'children', "
                   "'parentProcess', 'ownerMachine', 'calculatedUser', 'imageFile', 'imageFile.sha1String', "
                   "'imageFile.md5String', 'imageFile.sha256String', 'imageFile.companyName', "
                   "'imageFile.productName', 'applicablePid', 'imageFileExtensionType', 'integrity', 'tid', "
                   "'isAggregate', 'isDotNetProtected', 'hasMalops', 'hasSuspicions', 'relatedToMalop', "
                   "'multipleSizeForHashEvidence', 'isImageFileVerified', 'knownMaliciousToolSuspicion', "
                   "'knownMalwareSuspicion', 'knownUnwantedSuspicion', 'isMaliciousByHashEvidence', "
                   "'imageFileMultipleCompanyNamesEvidence', 'multipleHashForUnsignedPeInfoEvidence', "
                   "'multipleNameForHashEvidence', 'unknownEvidence', 'rareHasPeMismatchEvidence', "
                   "'imageFile.signedInternalOrExternal', 'unknownUnsignedBySigningCompany', "
                   "'imageFileUnsignedEvidence', 'imageFileUnsignedHasSignedVersionEvidence', "
                   "'unwantedModuleSuspicion', 'imageFile.signerInternalOrExternal', 'architecture', "
                   "'commandLineContainsTempEvidence', 'hasChildren', 'hasClassification', 'hasVisibleWindows', "
                   "'hasWindows', 'isInstaller', 'isIdentifiedProduct', 'hasModuleFromTempEvidence', "
                   "'nonExecutableExtensionEvidence', 'isNotShellRunner', 'runningFromTempEvidence', "
                   "'shellOfNonShellRunnerSuspicion', 'shellWithElevatedPrivilegesEvidence', 'systemUserEvidence', "
                   "'hasExternalConnection', 'hasExternalConnectionToWellKnownPortEvidence', 'hasIncomingConnection', "
                   "'hasInternalConnection', 'hasMailConnectionForNonMailProcessEvidence', 'hasListeningConnection', "
                   "'hasOutgoingConnection', 'hasUnresolvedDnsQueriesFromDomain', "
                   "'multipleUnresolvedRecordNotExistsEvidence', 'hasNonDefaultResolverEvidence', "
                   "'parentProcessNotMatchHierarchySuspicion', 'parentProcessNotAdminUserEvidence', "
                   "'parentProcessFromRemovableDeviceEvidence', 'autorun', 'childrenCreatedByThread', 'connections', "
                   "'elevatedPrivilegeChildren', 'hackerToolChildren', 'hostProcess', 'hostUser', 'hostedChildren', "
                   "'injectedChildren', 'loadedModules', 'logonSession', 'remoteSession', 'service', 'execedBy', "
                   "'connectionsToMaliciousDomain', 'connectionsToMalwareAddresses', 'externalConnections', "
                   "'absoluteHighVolumeMaliciousAddressConnections', 'absoluteHighVolumeExternalConnections', "
                   "'incomingConnections', 'incomingExternalConnections', 'incomingInternalConnections', "
                   "'internalConnections', 'listeningConnections', 'localConnections', 'mailConnections', "
                   "'outgoingConnections', 'outgoingExternalConnections', 'outgoingInternalConnections', "
                   "'suspiciousExternalConnections', 'suspiciousInternalConnections', 'wellKnownPortConnections', "
                   "'lowTtlDnsQueries', 'nonDefaultResolverQueries', 'resolvedDnsQueriesDomainToDomain', "
                   "'resolvedDnsQueriesDomainToIp', 'resolvedDnsQueriesIpToDomain', "
                   "'suspiciousDnsQueryDomainToDomain', 'unresolvedQueryFromSuspiciousDomain', "
                   "'dnsQueryFromSuspiciousDomain', 'dnsQueryToSuspiciousDomain', 'unresolvedRecordNotExist', "
                   "'unresolvedDnsQueriesFromDomain', 'unresolvedDnsQueriesFromIp', "
                   "'maliciousToolClassificationModules', 'malwareClassificationModules', 'modulesNotInLoaderDbList', "
                   "'modulesFromTemp', 'unsignedWithSignedVersionModules', 'unwantedClassificationModules', "
                   "'accessToMalwareAddressInfectedProcess', 'connectingToBadReputationAddressSuspicion', "
                   "'hasMaliciousConnectionEvidence', 'hasSuspiciousExternalConnectionSuspicion', "
                   "'highNumberOfExternalConnectionsSuspicion', 'nonDefaultResolverSuspicion', "
                   "'hasRareExternalConnectionEvidence', 'hasRareRemoteAddressEvidence', 'suspiciousMailConnections', "
                   "'accessToMalwareAddressByUnknownProcess', "
                   "'hasAbsoluteHighVolumeConnectionToMaliciousAddressEvidence', "
                   "'hasAbsoluteHighVolumeExternalOutgoingConnectionEvidence', 'highDataTransmittedSuspicion', "
                   "'highDataVolumeTransmittedToMaliciousAddressSuspicion', "
                   "'highDataVolumeTransmittedByUnknownProcess', "
                   "'absoluteHighNumberOfInternalOutgoingEmbryonicConnectionsEvidence', 'dgaSuspicion', "
                   "'hasLowTtlDnsQueryEvidence', 'highUnresolvedToResolvedRateEvidence', "
                   "'manyUnresolvedRecordNotExistsEvidence', 'hasChildKnownHackerToolEvidence', "
                   "'hackingToolOfNonToolRunnerEvidence', 'hackingToolOfNonToolRunnerSuspicion', "
                   "'hasRareChildProcessKnownHackerToolEvidence', 'maliciousToolModuleSuspicion', "
                   "'deletedParentProcessEvidence', 'malwareModuleSuspicion', 'dualExtensionNameEvidence', "
                   "'hiddenFileExtensionEvidence', 'rightToLeftFileExtensionEvidence', "
                   "'screenSaverWithChildrenEvidence', 'suspicionsScreenSaverEvidence', 'hasPeFloatingCodeEvidence', "
                   "'hasSectionMismatchEvidence', 'detectedInjectedEvidence', 'detectedInjectingEvidence', "
                   "'detectedInjectingToProtectedProcessEvidence', 'hasInjectedChildren', "
                   "'hostingInjectedThreadEvidence', 'injectedProtectedProcessEvidence', "
                   "'maliciousInjectingCodeSuspicion', 'injectionMethod', 'isHostingInjectedThread', "
                   "'maliciousInjectedCodeSuspicion', 'maliciousPeExecutionSuspicion', "
                   "'hasSuspiciousInternalConnectionEvidence', 'highInternalOutgoingEmbryonicConnectionRateEvidence', "
                   "'highNumberOfInternalConnectionsEvidence', 'newProcessesAboveThresholdEvidence', "
                   "'hasRareInternalConnectionEvidence', 'elevatingPrivilegesToChildEvidence', "
                   "'parentProcessNotSystemUserEvidence', 'privilegeEscalationEvidence', "
                   "'firstExecutionOfDownloadedProcessEvidence', 'hasAutorun', 'newProcessEvidence', "
                   "'markedForPrevention', 'ransomwareAutoRemediationSuspended', 'totalNumOfInstances', "
                   "'lastMinuteNumOfInstances', 'lastSeenTimeStamp', 'wmiQueryStrings', 'isExectuedByWmi', "
                   "'absoluteHighNumberOfInternalConnectionsEvidence', 'scanningProcessSuspicion', "
                   "'imageFile.isDownloadedFromInternet', 'imageFile.downloadedFromDomain', "
                   "'imageFile.downloadedFromIpAddress', 'imageFile.downloadedFromUrl', "
                   "'imageFile.downloadedFromUrlReferrer', 'imageFile.downloadedFromEmailFrom', "
                   "'imageFile.downloadedFromEmailMessageId', 'imageFile.downloadedFromEmailSubject', 'rpcRequests', "
                   "'iconBase64', 'executionPrevented', 'isWhiteListClassification', 'matchedWhiteListRuleIds']}"
                   ]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_process_created_query(self):
        stix_pattern = "[process:created >= '2019-09-04T09:29:29.0882Z']"
        query = translation.translate('cybereason', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'queryPath': [{'requestedType': 'Process', 'filters': [{'facetName': 'creationTime', "
                   "'filterType': 'GreaterOrEqualsTo', 'values': [1567589369088]}, {'facetName': 'creationTime', "
                   "'filterType': 'Between', 'values': [1640861056918, 1640861356918]}], 'isResult': True}], "
                   "'queryLimits': {'groupingFeature': {'elementInstanceType': 'Process', 'featureName': "
                   "'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, "
                   "'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', 'creationTime', 'endTime', "
                   "'commandLine', 'imageFile.maliciousClassificationType', 'productType', 'children', "
                   "'parentProcess', 'ownerMachine', 'calculatedUser', 'imageFile', 'imageFile.sha1String', "
                   "'imageFile.md5String', 'imageFile.sha256String', 'imageFile.companyName', "
                   "'imageFile.productName', 'applicablePid', 'imageFileExtensionType', 'integrity', 'tid', "
                   "'isAggregate', 'isDotNetProtected', 'hasMalops', 'hasSuspicions', 'relatedToMalop', "
                   "'multipleSizeForHashEvidence', 'isImageFileVerified', 'knownMaliciousToolSuspicion', "
                   "'knownMalwareSuspicion', 'knownUnwantedSuspicion', 'isMaliciousByHashEvidence', "
                   "'imageFileMultipleCompanyNamesEvidence', 'multipleHashForUnsignedPeInfoEvidence', "
                   "'multipleNameForHashEvidence', 'unknownEvidence', 'rareHasPeMismatchEvidence', "
                   "'imageFile.signedInternalOrExternal', 'unknownUnsignedBySigningCompany', "
                   "'imageFileUnsignedEvidence', 'imageFileUnsignedHasSignedVersionEvidence', "
                   "'unwantedModuleSuspicion', 'imageFile.signerInternalOrExternal', 'architecture', "
                   "'commandLineContainsTempEvidence', 'hasChildren', 'hasClassification', 'hasVisibleWindows', "
                   "'hasWindows', 'isInstaller', 'isIdentifiedProduct', 'hasModuleFromTempEvidence', "
                   "'nonExecutableExtensionEvidence', 'isNotShellRunner', 'runningFromTempEvidence', "
                   "'shellOfNonShellRunnerSuspicion', 'shellWithElevatedPrivilegesEvidence', 'systemUserEvidence', "
                   "'hasExternalConnection', 'hasExternalConnectionToWellKnownPortEvidence', 'hasIncomingConnection', "
                   "'hasInternalConnection', 'hasMailConnectionForNonMailProcessEvidence', 'hasListeningConnection', "
                   "'hasOutgoingConnection', 'hasUnresolvedDnsQueriesFromDomain', "
                   "'multipleUnresolvedRecordNotExistsEvidence', 'hasNonDefaultResolverEvidence', "
                   "'parentProcessNotMatchHierarchySuspicion', 'parentProcessNotAdminUserEvidence', "
                   "'parentProcessFromRemovableDeviceEvidence', 'autorun', 'childrenCreatedByThread', 'connections', "
                   "'elevatedPrivilegeChildren', 'hackerToolChildren', 'hostProcess', 'hostUser', 'hostedChildren', "
                   "'injectedChildren', 'loadedModules', 'logonSession', 'remoteSession', 'service', 'execedBy', "
                   "'connectionsToMaliciousDomain', 'connectionsToMalwareAddresses', 'externalConnections', "
                   "'absoluteHighVolumeMaliciousAddressConnections', 'absoluteHighVolumeExternalConnections', "
                   "'incomingConnections', 'incomingExternalConnections', 'incomingInternalConnections', "
                   "'internalConnections', 'listeningConnections', 'localConnections', 'mailConnections', "
                   "'outgoingConnections', 'outgoingExternalConnections', 'outgoingInternalConnections', "
                   "'suspiciousExternalConnections', 'suspiciousInternalConnections', 'wellKnownPortConnections', "
                   "'lowTtlDnsQueries', 'nonDefaultResolverQueries', 'resolvedDnsQueriesDomainToDomain', "
                   "'resolvedDnsQueriesDomainToIp', 'resolvedDnsQueriesIpToDomain', "
                   "'suspiciousDnsQueryDomainToDomain', 'unresolvedQueryFromSuspiciousDomain', "
                   "'dnsQueryFromSuspiciousDomain', 'dnsQueryToSuspiciousDomain', 'unresolvedRecordNotExist', "
                   "'unresolvedDnsQueriesFromDomain', 'unresolvedDnsQueriesFromIp', "
                   "'maliciousToolClassificationModules', 'malwareClassificationModules', 'modulesNotInLoaderDbList', "
                   "'modulesFromTemp', 'unsignedWithSignedVersionModules', 'unwantedClassificationModules', "
                   "'accessToMalwareAddressInfectedProcess', 'connectingToBadReputationAddressSuspicion', "
                   "'hasMaliciousConnectionEvidence', 'hasSuspiciousExternalConnectionSuspicion', "
                   "'highNumberOfExternalConnectionsSuspicion', 'nonDefaultResolverSuspicion', "
                   "'hasRareExternalConnectionEvidence', 'hasRareRemoteAddressEvidence', 'suspiciousMailConnections', "
                   "'accessToMalwareAddressByUnknownProcess', "
                   "'hasAbsoluteHighVolumeConnectionToMaliciousAddressEvidence', "
                   "'hasAbsoluteHighVolumeExternalOutgoingConnectionEvidence', 'highDataTransmittedSuspicion', "
                   "'highDataVolumeTransmittedToMaliciousAddressSuspicion', "
                   "'highDataVolumeTransmittedByUnknownProcess', "
                   "'absoluteHighNumberOfInternalOutgoingEmbryonicConnectionsEvidence', 'dgaSuspicion', "
                   "'hasLowTtlDnsQueryEvidence', 'highUnresolvedToResolvedRateEvidence', "
                   "'manyUnresolvedRecordNotExistsEvidence', 'hasChildKnownHackerToolEvidence', "
                   "'hackingToolOfNonToolRunnerEvidence', 'hackingToolOfNonToolRunnerSuspicion', "
                   "'hasRareChildProcessKnownHackerToolEvidence', 'maliciousToolModuleSuspicion', "
                   "'deletedParentProcessEvidence', 'malwareModuleSuspicion', 'dualExtensionNameEvidence', "
                   "'hiddenFileExtensionEvidence', 'rightToLeftFileExtensionEvidence', "
                   "'screenSaverWithChildrenEvidence', 'suspicionsScreenSaverEvidence', 'hasPeFloatingCodeEvidence', "
                   "'hasSectionMismatchEvidence', 'detectedInjectedEvidence', 'detectedInjectingEvidence', "
                   "'detectedInjectingToProtectedProcessEvidence', 'hasInjectedChildren', "
                   "'hostingInjectedThreadEvidence', 'injectedProtectedProcessEvidence', "
                   "'maliciousInjectingCodeSuspicion', 'injectionMethod', 'isHostingInjectedThread', "
                   "'maliciousInjectedCodeSuspicion', 'maliciousPeExecutionSuspicion', "
                   "'hasSuspiciousInternalConnectionEvidence', 'highInternalOutgoingEmbryonicConnectionRateEvidence', "
                   "'highNumberOfInternalConnectionsEvidence', 'newProcessesAboveThresholdEvidence', "
                   "'hasRareInternalConnectionEvidence', 'elevatingPrivilegesToChildEvidence', "
                   "'parentProcessNotSystemUserEvidence', 'privilegeEscalationEvidence', "
                   "'firstExecutionOfDownloadedProcessEvidence', 'hasAutorun', 'newProcessEvidence', "
                   "'markedForPrevention', 'ransomwareAutoRemediationSuspended', 'totalNumOfInstances', "
                   "'lastMinuteNumOfInstances', 'lastSeenTimeStamp', 'wmiQueryStrings', 'isExectuedByWmi', "
                   "'absoluteHighNumberOfInternalConnectionsEvidence', 'scanningProcessSuspicion', "
                   "'imageFile.isDownloadedFromInternet', 'imageFile.downloadedFromDomain', "
                   "'imageFile.downloadedFromIpAddress', 'imageFile.downloadedFromUrl', "
                   "'imageFile.downloadedFromUrlReferrer', 'imageFile.downloadedFromEmailFrom', "
                   "'imageFile.downloadedFromEmailMessageId', 'imageFile.downloadedFromEmailSubject', 'rpcRequests', "
                   "'iconBase64', 'executionPrevented', 'isWhiteListClassification', 'matchedWhiteListRuleIds']}",
                   "{'queryPath': [{'requestedType': 'DetectionEvents', 'filters': [{'facetName': 'firstSeen', "
                   "'filterType': 'GreaterOrEqualsTo', 'values': [1567589369088]}, {'facetName': 'firstSeen', "
                   "'filterType': 'Between', 'values': [1640861056918, 1640861356918]}], 'isResult': True}], "
                   "'queryLimits': {'groupingFeature': {'elementInstanceType': 'DetectionEvents', 'featureName': "
                   "'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, "
                   "'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', 'detectionEngine', "
                   "'decisionStatus', 'detectionValue', 'firstSeen', 'process', 'user', 'ownerMachine', "
                   "'detectionValueType', 'ownerMachine.isActiveProbeConnected', 'ownerMachine.osVersionType', "
                   "'process.calculatedName', 'process.calculatedUser', 'process.creationTime', 'process.endTime', "
                   "'process.imageFile.maliciousClassificationType']}"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_mac_address_query(self):
        stix_pattern = "[mac-addr:value = '00:15:5D:96:00:01']"
        query = translation.translate('cybereason', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'queryPath': [{'requestedType': 'NetworkInterface', 'filters': [{'facetName': "
                   "'macAddressFormat', 'filterType': 'Equals', 'values': ['00:15:5D:96:00:01']}], 'isResult': "
                   "True}], 'queryLimits': {'groupingFeature': {'elementInstanceType': 'NetworkInterface', "
                   "'featureName': 'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, "
                   "'perGroupLimit': 1, 'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', "
                   "'ipAddress', 'ownerMachine', 'gateway', 'dnsServer', 'dhcpServer', 'macAddressFormat', 'id', "
                   "'proxies']}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_email_address_query(self):
        stix_pattern = "[email-addr:value IN ('Administrator@gmail.com')]"
        query = translation.translate('cybereason', 'query', '{}', stix_pattern)

        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'queryPath': [{'requestedType': 'User', 'filters': [{'facetName': 'emailAddress', 'filterType': "
                   "'Equals', 'values': ['Administrator@gmail.com']}, {'facetName': 'adCreated', "
                   "'filterType': 'Between', 'values': [1642698025730, 1642698325730]}], 'isResult': True}],"
                   " 'queryLimits': {"
                   "'groupingFeature': {'elementInstanceType': 'User', 'featureName': 'elementDisplayName'}}, "
                   "'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, 'templateContext': 'CUSTOM', "
                   "'customFields': ['elementDisplayName', 'domain', 'ownerOrganization.name', 'ownerMachine', "
                   "'isLocalSystem', 'isAdmin', 'username', 'emailAddress', 'numberOfMachines', 'passwordAgeDays', "
                   "'privileges', 'comment', 'adCanonicalName', 'adCreated', 'adDisplayName', 'adLogonName', "
                   "'adMail', 'adMemberOf', 'adOU', 'adPrimaryGroupID', 'adSamAccountName', 'adTitle', "
                   "'hasPowerTool', 'hasMaliciousProcess', 'hasSuspicions', 'hasSuspiciousProcess', "
                   "'runningMaliciousProcessEvidence', 'hasRareProcessWithExternalConnections']}",
                   "{'queryPath': [{"
                   "'requestedType': 'User', 'filters': [{'facetName': 'adMail', 'filterType': 'Equals', 'values': ["
                   "'Administrator@gmail.com']}, {'facetName': 'adCreated', "
                   "'filterType': 'Between', 'values': [1642698025730, 1642698325730]}], "
                   "'isResult': True}], 'queryLimits': {'groupingFeature': {"
                   "'elementInstanceType': 'User', 'featureName': 'elementDisplayName'}}, 'perFeatureLimit': 1, "
                   "'totalResultLimit': 9999, 'perGroupLimit': 1, 'templateContext': 'CUSTOM', 'customFields': ["
                   "'elementDisplayName', 'domain', 'ownerOrganization.name', 'ownerMachine', 'isLocalSystem', "
                   "'isAdmin', 'username', 'emailAddress', 'numberOfMachines', 'passwordAgeDays', 'privileges', "
                   "'comment', 'adCanonicalName', 'adCreated', 'adDisplayName', 'adLogonName', 'adMail', "
                   "'adMemberOf', 'adOU', 'adPrimaryGroupID', 'adSamAccountName', 'adTitle', 'hasPowerTool', "
                   "'hasMaliciousProcess', 'hasSuspicions', 'hasSuspiciousProcess', "
                   "'runningMaliciousProcessEvidence', 'hasRareProcessWithExternalConnections']}",
                   "{'queryPath': [{"
                   "'requestedType': 'User', 'filters': [{'facetName': 'adLogonName', 'filterType': 'Equals', "
                   "'values': ['Administrator@gmail.com']}, {'facetName': 'adCreated', "
                   "'filterType': 'Between', 'values': [1642698025730, 1642698325730]}],"
                   " 'isResult': True}], 'queryLimits': {"
                   "'groupingFeature': {'elementInstanceType': 'User', 'featureName': 'elementDisplayName'}}, "
                   "'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, 'templateContext': 'CUSTOM', "
                   "'customFields': ['elementDisplayName', 'domain', 'ownerOrganization.name', 'ownerMachine', "
                   "'isLocalSystem', 'isAdmin', 'username', 'emailAddress', 'numberOfMachines', 'passwordAgeDays', "
                   "'privileges', 'comment', 'adCanonicalName', 'adCreated', 'adDisplayName', 'adLogonName', "
                   "'adMail', 'adMemberOf', 'adOU', 'adPrimaryGroupID', 'adSamAccountName', 'adTitle', "
                   "'hasPowerTool', 'hasMaliciousProcess', 'hasSuspicions', 'hasSuspiciousProcess', "
                   "'runningMaliciousProcessEvidence', 'hasRareProcessWithExternalConnections']}"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_query_from_multiple_comparison_expressions_joined_by_AND(self):
        stix_pattern = "[  x-oca-asset:name = 'bcybdw8888w10e2' AND x-cybereason-file:internal_name LIKE 'ping.exe']"
        query = translation.translate('cybereason', 'query', '{}', stix_pattern)

        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ["{'queryPath': [{'requestedType': 'File', 'filters': [{'facetName': 'internalName', 'filterType': "
                   "'ContainsIgnoreCase', 'values': ['ping.exe']}, {'facetName': 'createdTime', "
                   "'filterType': 'Between', 'values': [1643109411494, 1643109711494]}], 'connectionFeature': {"
                   "'elementInstanceType': 'File', 'featureName': 'ownerMachine'}}, {'requestedType': 'Machine', "
                   "'filters': [{'facetName': 'elementDisplayName', 'filterType': 'Equals', 'values': ["
                   "'bcybdw8888w10e2']}, {'facetName': 'lastSeenTimeStamp', "
                   "'filterType': 'Between', 'values': [1643109411494, 1643109711494]}], "
                   "'isResult': True}], 'queryLimits': {'groupingFeature': {"
                   "'elementInstanceType': 'Machine', 'featureName': 'elementDisplayName'}}, 'perFeatureLimit': 1, "
                   "'totalResultLimit': 9999, 'perGroupLimit': 1, 'templateContext': 'CUSTOM', 'customFields': ["
                   "'elementDisplayName', 'mountPoints', 'processes', 'services', 'logonSessions', "
                   "'hasRemovableDevice', 'timezoneUTCOffsetMinutes', 'osVersionType', 'platformArchitecture', "
                   "'mbrHashString', 'osType', 'domainFqdn', 'ownerOrganization', 'pylumId', 'adSid', 'adOU', "
                   "'adOrganization', 'adCanonicalName', 'adCompany', 'adDNSHostName', 'adDepartment', "
                   "'adDisplayName', 'adLocation', 'adMachineRole', 'adDescription', 'freeDiskSpace', "
                   "'totalDiskSpace', 'freeMemory', 'totalMemory', 'cpuCount', 'isLaptop', 'deviceModel', "
                   "'isActiveProbeConnected', 'uptime', 'isIsolated', 'lastSeenTimeStamp', "
                   "'timeStampSinceLastConnectionTime', 'hasMalops', 'hasSuspicions', "
                   "'isSuspiciousOrHasSuspiciousProcessOrFile', 'maliciousTools', 'maliciousProcesses', "
                   "'suspiciousProcesses']}",
                   "{'queryPath': [{'requestedType': 'File', 'filters': [{'facetName': "
                   "'internalName', 'filterType': 'ContainsIgnoreCase', 'values': ['ping.exe']}, {'facetName': "
                   "'createdTime', 'filterType': 'Between', 'values': [1643109411494, 1643109711494]}], "
                   "'connectionFeature': {'elementInstanceType': 'File', 'featureName': 'ownerMachine'}}, "
                   "{'requestedType': 'Machine', 'filters': [{'facetName': 'adDisplayName', 'filterType': 'Equals', "
                   "'values': ['bcybdw8888w10e2']}, {'facetName': 'lastSeenTimeStamp', "
                   "'filterType': 'Between', 'values': [1643109411494, 1643109711494]}], 'isResult': True}],"
                   " 'queryLimits': {"
                   "'groupingFeature': {'elementInstanceType': 'Machine', 'featureName': 'elementDisplayName'}}, "
                   "'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, 'templateContext': 'CUSTOM', "
                   "'customFields': ['elementDisplayName', 'mountPoints', 'processes', 'services', 'logonSessions', "
                   "'hasRemovableDevice', 'timezoneUTCOffsetMinutes', 'osVersionType', 'platformArchitecture', "
                   "'mbrHashString', 'osType', 'domainFqdn', 'ownerOrganization', 'pylumId', 'adSid', 'adOU', "
                   "'adOrganization', 'adCanonicalName', 'adCompany', 'adDNSHostName', 'adDepartment', "
                   "'adDisplayName', 'adLocation', 'adMachineRole', 'adDescription', 'freeDiskSpace', "
                   "'totalDiskSpace', 'freeMemory', 'totalMemory', 'cpuCount', 'isLaptop', 'deviceModel', "
                   "'isActiveProbeConnected', 'uptime', 'isIsolated', 'lastSeenTimeStamp', "
                   "'timeStampSinceLastConnectionTime', 'hasMalops', 'hasSuspicions', "
                   "'isSuspiciousOrHasSuspiciousProcessOrFile', 'maliciousTools', 'maliciousProcesses', "
                   "'suspiciousProcesses']}",
                   "{'queryPath': [{'requestedType': 'File', 'filters': [{'facetName': "
                   "'internalName', 'filterType': 'ContainsIgnoreCase', 'values': ['ping.exe']}, {'facetName': "
                   "'createdTime', 'filterType': 'Between', 'values': [1643109411494, 1643109711494]}], "
                   "'connectionFeature': {'elementInstanceType': 'File', 'featureName': 'ownerMachine'}}, "
                   "{'requestedType': 'Machine', 'filters': [{'facetName': 'adCanonicalName', 'filterType': 'Equals', "
                   "'values': ['bcybdw8888w10e2']}, {'facetName': 'lastSeenTimeStamp', "
                   "'filterType': 'Between', 'values': [1643109411494, 1643109711494]}], 'isResult': True}],"
                   " 'queryLimits': {"
                   "'groupingFeature': {'elementInstanceType': 'Machine', 'featureName': 'elementDisplayName'}}, "
                   "'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, 'templateContext': 'CUSTOM', "
                   "'customFields': ['elementDisplayName', 'mountPoints', 'processes', 'services', 'logonSessions', "
                   "'hasRemovableDevice', 'timezoneUTCOffsetMinutes', 'osVersionType', 'platformArchitecture', "
                   "'mbrHashString', 'osType', 'domainFqdn', 'ownerOrganization', 'pylumId', 'adSid', 'adOU', "
                   "'adOrganization', 'adCanonicalName', 'adCompany', 'adDNSHostName', 'adDepartment', "
                   "'adDisplayName', 'adLocation', 'adMachineRole', 'adDescription', 'freeDiskSpace', "
                   "'totalDiskSpace', 'freeMemory', 'totalMemory', 'cpuCount', 'isLaptop', 'deviceModel', "
                   "'isActiveProbeConnected', 'uptime', 'isIsolated', 'lastSeenTimeStamp', "
                   "'timeStampSinceLastConnectionTime', 'hasMalops', 'hasSuspicions', "
                   "'isSuspiciousOrHasSuspiciousProcessOrFile', 'maliciousTools', 'maliciousProcesses', "
                   "'suspiciousProcesses']}"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_file_query(self):
        stix_pattern = "[file:name LIKE 'wim.exe']"
        query = translation.translate('cybereason', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'queryPath': [{'requestedType': 'File', 'filters': [{'facetName': 'elementDisplayName', "
                   "'filterType': 'ContainsIgnoreCase', 'values': ['wim.exe']}, {'facetName': 'createdTime', "
                   "'filterType': 'Between', 'values': [1638268938121, 1638269238121]}], 'isResult': True}], "
                   "'queryLimits': {'groupingFeature': {'elementInstanceType': 'File', 'featureName': "
                   "'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, "
                   "'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', 'avRemediationStatus', "
                   "'signerInternalOrExternal', 'fileHash', 'autoruns', 'ownerMachine', 'mount', 'autorun', "
                   "'dualExtensionEvidence', 'hiddenFileExtensionEvidence', 'rightToLeftFileExtensionEvidence', "
                   "'hasMalops', 'hasSuspicions', 'maliciousClassificationType', 'hackingToolClassificationEvidence', "
                   "'classificationLink', 'isPEFile', 'executedByProcessEvidence', 'hasAutorun', "
                   "'isInstallerProperties', 'isFromRemovableDevice', 'productType', 'secondExtensionType', "
                   "'temporaryFolderEvidence', 'multipleCompanyNamesEvidence', "
                   "'multipleHashForUnsignedPeInfoEvidence', 'unsignedHasSignedVersionEvidence', "
                   "'classificationComment', 'signedInternalOrExternal', 'signatureVerifiedInternalOrExternal', "
                   "'classificationBlocking', 'isDownloadedFromInternet', 'downloadedFromDomain', "
                   "'downloadedFromIpAddress', 'downloadedFromUrl', 'downloadedFromUrlReferrer', "
                   "'downloadedFromEmailFrom', 'downloadedFromEmailMessageId', 'downloadedFromEmailSubject', "
                   "'legalCopyright', 'legalTrademarks', 'privateBuild', 'specialBuild', 'companyName', "
                   "'createdTime', 'extensionType', 'fileDescription', 'internalName', 'md5String', 'modifiedTime', "
                   "'originalFileName', 'correctedPath', 'productName', 'productVersion', 'sha1String', 'size', "
                   "'comments', 'fileVersion', 'applicationIdentifier', 'sha256String']}",
                   "{'queryPath': [{"
                   "'requestedType': 'File', 'filters': [{'facetName': 'originalFileName', 'filterType': "
                   "'ContainsIgnoreCase', 'values': ['wim.exe']}, {'facetName': 'createdTime', "
                   "'filterType': 'Between', 'values': [1638268938121, 1638269238121]}], "
                   "'isResult': True}], 'queryLimits': {"
                   "'groupingFeature': {'elementInstanceType': 'File', 'featureName': 'elementDisplayName'}}, "
                   "'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, 'templateContext': "
                   "'CUSTOM', 'customFields': ['elementDisplayName', 'avRemediationStatus', "
                   "'signerInternalOrExternal', 'fileHash', 'autoruns', 'ownerMachine', 'mount', 'autorun', "
                   "'dualExtensionEvidence', 'hiddenFileExtensionEvidence', 'rightToLeftFileExtensionEvidence', "
                   "'hasMalops', 'hasSuspicions', 'maliciousClassificationType', 'hackingToolClassificationEvidence', "
                   "'classificationLink', 'isPEFile', 'executedByProcessEvidence', 'hasAutorun', "
                   "'isInstallerProperties', 'isFromRemovableDevice', 'productType', 'secondExtensionType', "
                   "'temporaryFolderEvidence', 'multipleCompanyNamesEvidence', "
                   "'multipleHashForUnsignedPeInfoEvidence', 'unsignedHasSignedVersionEvidence', "
                   "'classificationComment', 'signedInternalOrExternal', 'signatureVerifiedInternalOrExternal', "
                   "'classificationBlocking', 'isDownloadedFromInternet', 'downloadedFromDomain', "
                   "'downloadedFromIpAddress', 'downloadedFromUrl', 'downloadedFromUrlReferrer', "
                   "'downloadedFromEmailFrom', 'downloadedFromEmailMessageId', 'downloadedFromEmailSubject', "
                   "'legalCopyright', 'legalTrademarks', 'privateBuild', 'specialBuild', 'companyName', "
                   "'createdTime', 'extensionType', 'fileDescription', 'internalName', 'md5String', 'modifiedTime', "
                   "'originalFileName', 'correctedPath', 'productName', 'productVersion', 'sha1String', 'size', "
                   "'comments', 'fileVersion', 'applicationIdentifier', 'sha256String']}",
                   "{'queryPath': [{"
                   "'requestedType': 'DetectionEvents', 'filters': [{'facetName': 'file', 'filterType': "
                   "'ContainsIgnoreCase', 'values': ['wim.exe']}, {'facetName': 'firstSeen', "
                   "'filterType': 'Between', 'values': [1638268938121, 1638269238121]}], 'isResult': True}],"
                   " 'queryLimits': {"
                   "'groupingFeature': {'elementInstanceType': 'DetectionEvents', 'featureName': "
                   "'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, "
                   "'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', 'detectionEngine', "
                   "'decisionStatus', 'detectionValue', 'firstSeen', 'process', 'user', 'ownerMachine', "
                   "'detectionValueType', 'ownerMachine.isActiveProbeConnected', 'ownerMachine.osVersionType', "
                   "'process.calculatedName', 'process.calculatedUser', 'process.creationTime', 'process.endTime', "
                   "'process.imageFile.maliciousClassificationType']}",
                   "{'queryPath': [{'requestedType': 'Driver', "
                   "'filters': [{'facetName': 'file', 'filterType': 'ContainsIgnoreCase', 'values': ['wim.exe']}, "
                   "{'facetName': 'endTime', 'filterType': 'Between', 'values': [1638268938121, 1638269238121]}], "
                   "'isResult': True}], 'queryLimits': {'groupingFeature': {'elementInstanceType': 'Driver', "
                   "'featureName': 'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, "
                   "'perGroupLimit': 1, 'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', "
                   "'creationTime', 'file', 'ownerMachine', 'service', 'endTime', 'newDriverEvidence', "
                   "'hasSuspicions']}",
                   "{'queryPath': [{'requestedType': 'Service', 'filters': [{'facetName': "
                   "'binaryFile', 'filterType': 'ContainsIgnoreCase', 'values': ['wim.exe']}, {'facetName': "
                   "'endTime', 'filterType': 'Between', 'values': [1638268938121, 1638269238121]}], 'isResult': "
                   "True}], 'queryLimits': {'groupingFeature': {'elementInstanceType': 'Service', 'featureName': "
                   "'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, "
                   "'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', 'binaryFile', "
                   "'ownerMachine', 'process', 'serviceStartName', 'commandLineArguments', 'description', "
                   "'displayName', 'endTime', 'isActive', 'startType', 'unitFilePath', 'serviceState', "
                   "'serviceSubState', 'isAutoRestartService', 'hasSuspicions', 'newServiceEvidence', "
                   "'rareServiceEvidence', 'serviceType', 'driver']}",
                   "{'queryPath': [{'requestedType': 'Service', "
                   "'filters': [{'facetName': 'oldBinaryFile', 'filterType': 'ContainsIgnoreCase', 'values': ["
                   "'wim.exe']}, {'facetName': 'endTime', "
                   "'filterType': 'Between', 'values': [1638268938121, 1638269238121]}], 'isResult': True}],"
                   " 'queryLimits': {'groupingFeature': {'elementInstanceType': "
                   "'Service', 'featureName': 'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, "
                   "'perGroupLimit': 1, 'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', "
                   "'binaryFile', 'ownerMachine', 'process', 'serviceStartName', 'commandLineArguments', "
                   "'description', 'displayName', 'endTime', 'isActive', 'startType', 'unitFilePath', 'serviceState', "
                   "'serviceSubState', 'isAutoRestartService', 'hasSuspicions', 'newServiceEvidence', "
                   "'rareServiceEvidence', 'serviceType', 'driver']}"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_query_from_morethan_two_comparison_expressions_joined_by_AND(self):
        stix_pattern = "[user-account:display_name LIKE 'window' AND x-oca-asset:os_type = 'Windows' AND " \
                       "x-cybereason-logonsession:type = 'Interactive']"

        query = translation.translate('cybereason', 'query', '{}', stix_pattern)

        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ["{'queryPath': [{'requestedType': 'LogonSession', 'filters': [{'facetName': 'logonType', "
                   "'filterType': 'Equals', 'values': ['Interactive']}, {'facetName': 'creationTime',"
                   " 'filterType': 'Between', 'values': [1638269189884, 1638269489884]}], 'connectionFeature': {"
                   "'elementInstanceType': 'LogonSession', 'featureName': 'ownerMachine'}}, {'requestedType': "
                   "'Machine', 'filters': [{'facetName': 'osType', 'filterType': 'Equals', 'values': ['Windows']}, "
                   "{'facetName': 'lastSeenTimeStamp', 'filterType': 'Between', 'values': [1638269189884, "
                   "1638269489884]}], 'connectionFeature': {'elementInstanceType': 'Machine', 'featureName': "
                   "'users'}}, {'requestedType': 'User', 'filters': [{'facetName': 'elementDisplayName', "
                   "'filterType': 'ContainsIgnoreCase', 'values': ['window']}, {'facetName': 'adCreated', "
                   "'filterType': 'Between', 'values': [1638269189884, 1638269489884]}], 'isResult': True}], "
                   "'queryLimits': {'groupingFeature': {'elementInstanceType': 'User', 'featureName': "
                   "'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, "
                   "'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', 'domain', "
                   "'ownerOrganization.name', 'ownerMachine', 'isLocalSystem', 'isAdmin', 'username', 'emailAddress', "
                   "'numberOfMachines', 'passwordAgeDays', 'privileges', 'comment', 'adCanonicalName', 'adCreated', "
                   "'adDisplayName', 'adLogonName', 'adMail', 'adMemberOf', 'adOU', 'adPrimaryGroupID', "
                   "'adSamAccountName', 'adTitle', 'hasPowerTool', 'hasMaliciousProcess', 'hasSuspicions', "
                   "'hasSuspiciousProcess', 'runningMaliciousProcessEvidence', "
                   "'hasRareProcessWithExternalConnections']}",
                   "{'queryPath': [{'requestedType': 'LogonSession', "
                   "'filters': [{'facetName': 'logonType', 'filterType': 'Equals', 'values': ['Interactive']}, "
                   "{'facetName': 'creationTime', "
                   "'filterType': 'Between', 'values': [1638269189884, 1638269489884]}],"
                   " 'connectionFeature': {'elementInstanceType': 'LogonSession', 'featureName': "
                   "'ownerMachine'}}, {'requestedType': 'Machine', 'filters': [{'facetName': 'osType', 'filterType': "
                   "'Equals', 'values': ['Windows']}, {'facetName': 'lastSeenTimeStamp', 'filterType': 'Between', "
                   "'values': [1638269189884, 1638269489884]}], 'connectionFeature': {'elementInstanceType': "
                   "'Machine', 'featureName': 'users'}}, {'requestedType': 'User', 'filters': [{'facetName': "
                   "'adDisplayName', 'filterType': 'ContainsIgnoreCase', 'values': ['window']}, {'facetName': "
                   "'adCreated', 'filterType': 'Between', 'values': [1638269189884, 1638269489884]}], 'isResult': "
                   "True}], 'queryLimits': {'groupingFeature': {'elementInstanceType': 'User', 'featureName': "
                   "'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, "
                   "'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', 'domain', "
                   "'ownerOrganization.name', 'ownerMachine', 'isLocalSystem', 'isAdmin', 'username', 'emailAddress', "
                   "'numberOfMachines', 'passwordAgeDays', 'privileges', 'comment', 'adCanonicalName', 'adCreated', "
                   "'adDisplayName', 'adLogonName', 'adMail', 'adMemberOf', 'adOU', 'adPrimaryGroupID', "
                   "'adSamAccountName', 'adTitle', 'hasPowerTool', 'hasMaliciousProcess', 'hasSuspicions', "
                   "'hasSuspiciousProcess', 'runningMaliciousProcessEvidence', "
                   "'hasRareProcessWithExternalConnections']}",
                   "{'queryPath': [{'requestedType': 'LogonSession', "
                   "'filters': [{'facetName': 'logonType', 'filterType': 'Equals', 'values': ['Interactive']}, "
                   "{'facetName': 'creationTime', "
                   "'filterType': 'Between', 'values': [1638269189884, 1638269489884]}],"
                   " 'connectionFeature': {'elementInstanceType': 'LogonSession', 'featureName': "
                   "'ownerMachine'}}, {'requestedType': 'Machine', 'filters': [{'facetName': 'osType', 'filterType': "
                   "'Equals', 'values': ['Windows']}, {'facetName': 'lastSeenTimeStamp', 'filterType': 'Between', "
                   "'values': [1638269189884, 1638269489884]}], 'connectionFeature': {'elementInstanceType': "
                   "'Machine', 'featureName': 'users'}}, {'requestedType': 'User', 'filters': [{'facetName': "
                   "'adCanonicalName', 'filterType': 'ContainsIgnoreCase', 'values': ['window']}, {'facetName': "
                   "'adCreated', 'filterType': 'Between', 'values': [1638269189884, 1638269489884]}], 'isResult': "
                   "True}], 'queryLimits': {'groupingFeature': {'elementInstanceType': 'User', 'featureName': "
                   "'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, "
                   "'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', 'domain', "
                   "'ownerOrganization.name', 'ownerMachine', 'isLocalSystem', 'isAdmin', 'username', 'emailAddress', "
                   "'numberOfMachines', 'passwordAgeDays', 'privileges', 'comment', 'adCanonicalName', 'adCreated', "
                   "'adDisplayName', 'adLogonName', 'adMail', 'adMemberOf', 'adOU', 'adPrimaryGroupID', "
                   "'adSamAccountName', 'adTitle', 'hasPowerTool', 'hasMaliciousProcess', 'hasSuspicions', "
                   "'hasSuspiciousProcess', 'runningMaliciousProcessEvidence', "
                   "'hasRareProcessWithExternalConnections']}",
                   "{'queryPath': [{'requestedType': 'LogonSession', "
                   "'filters': [{'facetName': 'logonType', 'filterType': 'Equals', 'values': ['Interactive']}, "
                   "{'facetName': 'creationTime', "
                   "'filterType': 'Between', 'values': [1638269189884, 1638269489884]}], "
                   "'connectionFeature': {'elementInstanceType': 'LogonSession', 'featureName': "
                   "'remoteMachine'}}, {'requestedType': 'Machine', 'filters': [{'facetName': 'osType', 'filterType': "
                   "'Equals', 'values': ['Windows']}, {'facetName': 'lastSeenTimeStamp', 'filterType': 'Between', "
                   "'values': [1638269189884, 1638269489884]}], 'connectionFeature': {'elementInstanceType': "
                   "'Machine', 'featureName': 'users'}}, {'requestedType': 'User', 'filters': [{'facetName': "
                   "'elementDisplayName', 'filterType': 'ContainsIgnoreCase', 'values': ['window']}, {'facetName': "
                   "'adCreated', 'filterType': 'Between', 'values': [1638269189884, 1638269489884]}], 'isResult': "
                   "True}], 'queryLimits': {'groupingFeature': {'elementInstanceType': 'User', 'featureName': "
                   "'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, "
                   "'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', 'domain', "
                   "'ownerOrganization.name', 'ownerMachine', 'isLocalSystem', 'isAdmin', 'username', 'emailAddress', "
                   "'numberOfMachines', 'passwordAgeDays', 'privileges', 'comment', 'adCanonicalName', 'adCreated', "
                   "'adDisplayName', 'adLogonName', 'adMail', 'adMemberOf', 'adOU', 'adPrimaryGroupID', "
                   "'adSamAccountName', 'adTitle', 'hasPowerTool', 'hasMaliciousProcess', 'hasSuspicions', "
                   "'hasSuspiciousProcess', 'runningMaliciousProcessEvidence', "
                   "'hasRareProcessWithExternalConnections']}",
                   "{'queryPath': [{'requestedType': 'LogonSession', "
                   "'filters': [{'facetName': 'logonType', 'filterType': 'Equals', 'values': ['Interactive']}, "
                   "{'facetName': 'creationTime',"
                   " 'filterType': 'Between', 'values': [1638269189884, 1638269489884]}], "
                   "'connectionFeature': {'elementInstanceType': 'LogonSession', 'featureName': "
                   "'remoteMachine'}}, {'requestedType': 'Machine', 'filters': [{'facetName': 'osType', 'filterType': "
                   "'Equals', 'values': ['Windows']}, {'facetName': 'lastSeenTimeStamp', 'filterType': 'Between', "
                   "'values': [1638269189884, 1638269489884]}], 'connectionFeature': {'elementInstanceType': "
                   "'Machine', 'featureName': 'users'}}, {'requestedType': 'User', 'filters': [{'facetName': "
                   "'adDisplayName', 'filterType': 'ContainsIgnoreCase', 'values': ['window']}, {'facetName': "
                   "'adCreated', 'filterType': 'Between', 'values': [1638269189884, 1638269489884]}], 'isResult': "
                   "True}], 'queryLimits': {'groupingFeature': {'elementInstanceType': 'User', 'featureName': "
                   "'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, "
                   "'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', 'domain', "
                   "'ownerOrganization.name', 'ownerMachine', 'isLocalSystem', 'isAdmin', 'username', 'emailAddress', "
                   "'numberOfMachines', 'passwordAgeDays', 'privileges', 'comment', 'adCanonicalName', 'adCreated', "
                   "'adDisplayName', 'adLogonName', 'adMail', 'adMemberOf', 'adOU', 'adPrimaryGroupID', "
                   "'adSamAccountName', 'adTitle', 'hasPowerTool', 'hasMaliciousProcess', 'hasSuspicions', "
                   "'hasSuspiciousProcess', 'runningMaliciousProcessEvidence', "
                   "'hasRareProcessWithExternalConnections']}",
                   "{'queryPath': [{'requestedType': 'LogonSession', "
                   "'filters': [{'facetName': 'logonType', 'filterType': 'Equals', 'values': ['Interactive']}, "
                   "{'facetName': 'creationTime', "
                   "'filterType': 'Between', 'values': [1638269189884, 1638269489884]}], "
                   "'connectionFeature': {'elementInstanceType': 'LogonSession', 'featureName': "
                   "'remoteMachine'}}, {'requestedType': 'Machine', 'filters': [{'facetName': 'osType', 'filterType': "
                   "'Equals', 'values': ['Windows']}, {'facetName': 'lastSeenTimeStamp', 'filterType': 'Between', "
                   "'values': [1638269189884, 1638269489884]}], 'connectionFeature': {'elementInstanceType': "
                   "'Machine', 'featureName': 'users'}}, {'requestedType': 'User', 'filters': [{'facetName': "
                   "'adCanonicalName', 'filterType': 'ContainsIgnoreCase', 'values': ['window']}, {'facetName': "
                   "'adCreated', 'filterType': 'Between', 'values': [1638269189884, 1638269489884]}], 'isResult': "
                   "True}], 'queryLimits': {'groupingFeature': {'elementInstanceType': 'User', 'featureName': "
                   "'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, "
                   "'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', 'domain', "
                   "'ownerOrganization.name', 'ownerMachine', 'isLocalSystem', 'isAdmin', 'username', 'emailAddress', "
                   "'numberOfMachines', 'passwordAgeDays', 'privileges', 'comment', 'adCanonicalName', 'adCreated', "
                   "'adDisplayName', 'adLogonName', 'adMail', 'adMemberOf', 'adOU', 'adPrimaryGroupID', "
                   "'adSamAccountName', 'adTitle', 'hasPowerTool', 'hasMaliciousProcess', 'hasSuspicions', "
                   "'hasSuspiciousProcess', 'runningMaliciousProcessEvidence', "
                   "'hasRareProcessWithExternalConnections']}"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_observation_query(self):
        stix_pattern = "([file: hashes.MD5 = 'MD5' AND windows-registry-key:key = 'name' AND " \
                       "x-oca-event:detection_time = 1] AND [x-cybereason-service:file = 'sfile' AND " \
                       "x-cybereason-service:arguments = 'arg'] AND [ x-oca-asset: timezone = 4 AND " \
                       "x-cybereason-driver:machine ='username' ])START " \
                       "t'2019-10-01T00:00:00.030Z' STOP t'2021-10-07T00:00:00.030Z' "

        query = translation.translate('cybereason', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'queryPath': [{'requestedType': 'RegistryEvent', 'filters': [{'facetName': "
                   "'detectionTimesNumber', 'filterType': 'Equals', 'values': [1]}, {'facetName': 'firstTime', "
                   "'filterType': 'Between', 'values': [1569888000030, 1633564800030]}], 'connectionFeature': {"
                   "'elementInstanceType': 'RegistryEvent', 'featureName': 'registryEntry'}}, {'requestedType': "
                   "'Autorun', 'filters': [{'facetName': 'elementDisplayName', 'filterType': 'Equals', 'values': ["
                   "'name']}, {'facetName': 'endTime', 'filterType': 'Between', 'values': [1569888000030, "
                   "1633564800030]}], 'connectionFeature': {'elementInstanceType': 'Autorun', 'featureName': "
                   "'dependInFile'}}, {'requestedType': 'File', 'filters': [{'facetName': 'md5String', 'filterType': "
                   "'Equals', 'values': ['MD5']}, {'facetName': 'createdTime', 'filterType': 'Between', 'values': ["
                   "1569888000030, 1633564800030]}], 'isResult': True}], 'queryLimits': {'groupingFeature': {"
                   "'elementInstanceType': 'File', 'featureName': 'elementDisplayName'}}, 'perFeatureLimit': 1, "
                   "'totalResultLimit': 9999, 'perGroupLimit': 1, 'templateContext': 'CUSTOM', 'customFields': ["
                   "'elementDisplayName', 'avRemediationStatus', 'signerInternalOrExternal', 'fileHash', 'autoruns', "
                   "'ownerMachine', 'mount', 'autorun', 'dualExtensionEvidence', 'hiddenFileExtensionEvidence', "
                   "'rightToLeftFileExtensionEvidence', 'hasMalops', 'hasSuspicions', 'maliciousClassificationType', "
                   "'hackingToolClassificationEvidence', 'classificationLink', 'isPEFile', "
                   "'executedByProcessEvidence', 'hasAutorun', 'isInstallerProperties', 'isFromRemovableDevice', "
                   "'productType', 'secondExtensionType', 'temporaryFolderEvidence', 'multipleCompanyNamesEvidence', "
                   "'multipleHashForUnsignedPeInfoEvidence', 'unsignedHasSignedVersionEvidence', "
                   "'classificationComment', 'signedInternalOrExternal', 'signatureVerifiedInternalOrExternal', "
                   "'classificationBlocking', 'isDownloadedFromInternet', 'downloadedFromDomain', "
                   "'downloadedFromIpAddress', 'downloadedFromUrl', 'downloadedFromUrlReferrer', "
                   "'downloadedFromEmailFrom', 'downloadedFromEmailMessageId', 'downloadedFromEmailSubject', "
                   "'legalCopyright', 'legalTrademarks', 'privateBuild', 'specialBuild', 'companyName', "
                   "'createdTime', 'extensionType', 'fileDescription', 'internalName', 'md5String', 'modifiedTime', "
                   "'originalFileName', 'correctedPath', 'productName', 'productVersion', 'sha1String', 'size', "
                   "'comments', 'fileVersion', 'applicationIdentifier', 'sha256String']}",
                   "{'queryPath': [{"
                   "'requestedType': 'Driver', 'filters': [{'facetName': 'ownerMachine', 'filterType': 'Equals', "
                   "'values': ['username']}, {'facetName': 'endTime', 'filterType': 'Between', 'values': ["
                   "1569888000030, 1633564800030]}], 'connectionFeature': {'elementInstanceType': 'Driver', "
                   "'featureName': 'ownerMachine'}}, {'requestedType': 'Machine', 'filters': [{'facetName': "
                   "'timezoneUTCOffsetMinutes', 'filterType': 'Equals', 'values': [4]}, {'facetName': "
                   "'lastSeenTimeStamp', 'filterType': 'Between', 'values': [1569888000030, 1633564800030]}], "
                   "'isResult': True}], 'queryLimits': {'groupingFeature': {'elementInstanceType': 'Machine', "
                   "'featureName': 'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, "
                   "'perGroupLimit': 1, 'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', "
                   "'mountPoints', 'processes', 'services', 'logonSessions', 'hasRemovableDevice', "
                   "'timezoneUTCOffsetMinutes', 'osVersionType', 'platformArchitecture', 'mbrHashString', 'osType', "
                   "'domainFqdn', 'ownerOrganization', 'pylumId', 'adSid', 'adOU', 'adOrganization', "
                   "'adCanonicalName', 'adCompany', 'adDNSHostName', 'adDepartment', 'adDisplayName', 'adLocation', "
                   "'adMachineRole', 'adDescription', 'freeDiskSpace', 'totalDiskSpace', 'freeMemory', 'totalMemory', "
                   "'cpuCount', 'isLaptop', 'deviceModel', 'isActiveProbeConnected', 'uptime', 'isIsolated', "
                   "'lastSeenTimeStamp', 'timeStampSinceLastConnectionTime', 'hasMalops', 'hasSuspicions', "
                   "'isSuspiciousOrHasSuspiciousProcessOrFile', 'maliciousTools', 'maliciousProcesses', "
                   "'suspiciousProcesses']}"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_unmapped_attribute_handling_with_AND(self):

        stix_pattern = "[url:value = 'http://www.testaddress.com' AND unmapped:attribute = 'something']"
        result = translation.translate('cybereason', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_MAPPING_ERROR.value == result['code']
        assert 'Unable to map the following STIX objects and properties' in result['error']

    def test_invalid_boolean_value(self):
        stix_pattern = "[user-account:is_privileged = '2']"
        result = translation.translate('cybereason', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert 'Invalid boolean type input' in result['error']

    def test_invalid_stix_pattern(self):
        stix_pattern = "[not_a_valid_pattern]"
        result = translation.translate('cybereason', 'query', '{}', stix_pattern, {'validate_pattern': 'true'})
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_STIX_VALIDATION.value == result['code']
        assert stix_pattern[1:-1] in result['error']

    def test_with_OR_operator_pattern(self):
        stix_pattern = "[ipv4-addr:value = '8.8.8.8' OR network-traffic:src_port > 22]"
        result = translation.translate('cybereason', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert 'OR operator is not supported' in result['error']

    def test_service_negate_query(self):
        stix_pattern = "[x-cybereason-service:name NOT = 'Windows Push Notifications UserService_2d02eb']"
        query = translation.translate('cybereason', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'queryPath': [{'requestedType': 'Service', 'filters': [{'facetName': 'displayName', 'filterType': "
                   "'NotEquals', 'values': ['Windows Push Notifications UserService_2d02eb']}, {'facetName': "
                   "'endTime', 'filterType': 'Between', 'values': [1638160959907, 1638161259907]}], 'isResult': "
                   "True}], 'queryLimits': {'groupingFeature': {'elementInstanceType': 'Service', 'featureName': "
                   "'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, "
                   "'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', 'binaryFile', "
                   "'ownerMachine', 'process', 'serviceStartName', 'commandLineArguments', 'description', "
                   "'displayName', 'endTime', 'isActive', 'startType', 'unitFilePath', 'serviceState', "
                   "'serviceSubState', 'isAutoRestartService', 'hasSuspicions', 'newServiceEvidence', "
                   "'rareServiceEvidence', 'serviceType', 'driver']}",
                   "{'queryPath': [{'requestedType': 'Service', "
                   "'filters': [{'facetName': 'oldServiceStartName', 'filterType': 'NotEquals', 'values': ['Windows "
                   "Push Notifications UserService_2d02eb']}, {'facetName': 'endTime', "
                   "'filterType': 'Between','values': [1638160959907, 1638161259907]}], 'isResult': True}],"
                   " 'queryLimits': {'groupingFeature': "
                   "{'elementInstanceType': 'Service', 'featureName': 'elementDisplayName'}}, 'perFeatureLimit': 1, "
                   "'totalResultLimit': 9999, 'perGroupLimit': 1, 'templateContext': 'CUSTOM', 'customFields': ["
                   "'elementDisplayName', 'binaryFile', 'ownerMachine', 'process', 'serviceStartName', "
                   "'commandLineArguments', 'description', 'displayName', 'endTime', 'isActive', 'startType', "
                   "'unitFilePath', 'serviceState', 'serviceSubState', 'isAutoRestartService', 'hasSuspicions', "
                   "'newServiceEvidence', 'rareServiceEvidence', 'serviceType', 'driver']}",
                   "{'queryPath': [{"
                   "'requestedType': 'Service', 'filters': [{'facetName': 'elementDisplayName', 'filterType': "
                   "'NotEquals', 'values': ['Windows Push Notifications UserService_2d02eb']}, {'facetName': "
                   "'endTime', 'filterType': 'Between', 'values': [1638160959907, 1638161259907]}], 'isResult': "
                   "True}], 'queryLimits': {'groupingFeature': {'elementInstanceType': 'Service', 'featureName': "
                   "'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, "
                   "'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', 'binaryFile', "
                   "'ownerMachine', 'process', 'serviceStartName', 'commandLineArguments', 'description', "
                   "'displayName', 'endTime', 'isActive', 'startType', 'unitFilePath', 'serviceState', "
                   "'serviceSubState', 'isAutoRestartService', 'hasSuspicions', 'newServiceEvidence', "
                   "'rareServiceEvidence', 'serviceType', 'driver']}",
                   "{'queryPath': [{'requestedType': 'Service', "
                   "'filters': [{'facetName': 'serviceStartName', 'filterType': 'NotEquals', 'values': ['Windows Push "
                   "Notifications UserService_2d02eb']}, {'facetName': 'endTime',"
                   " 'filterType': 'Between', 'values': [1638160959907, 1638161259907]}], 'isResult': True}], "
                   "'queryLimits': {'groupingFeature': {"
                   "'elementInstanceType': 'Service', 'featureName': 'elementDisplayName'}}, 'perFeatureLimit': 1, "
                   "'totalResultLimit': 9999, 'perGroupLimit': 1, 'templateContext': 'CUSTOM', 'customFields': ["
                   "'elementDisplayName', 'binaryFile', 'ownerMachine', 'process', 'serviceStartName', "
                   "'commandLineArguments', 'description', 'displayName', 'endTime', 'isActive', 'startType', "
                   "'unitFilePath', 'serviceState', 'serviceSubState', 'isAutoRestartService', 'hasSuspicions', "
                   "'newServiceEvidence', 'rareServiceEvidence', 'serviceType', 'driver']}",
                   "{'queryPath': [{"
                   "'requestedType': 'Driver', 'filters': [{'facetName': 'service', 'filterType': 'NotEquals', "
                   "'values': ['Windows Push Notifications UserService_2d02eb']}, {'facetName': 'endTime', "
                   "'filterType': 'Between', 'values': [1638160959907, 1638161259907]}], 'isResult': True}], "
                   "'queryLimits': {'groupingFeature': {'elementInstanceType': 'Driver', 'featureName': "
                   "'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, "
                   "'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', 'creationTime', 'file', "
                   "'ownerMachine', 'service', 'endTime', 'newDriverEvidence', 'hasSuspicions']}",
                   "{'queryPath': [{"
                   "'requestedType': 'Process', 'filters': [{'facetName': 'service', 'filterType': 'NotEquals', "
                   "'values': ['Windows Push Notifications UserService_2d02eb']}, {'facetName': 'creationTime', "
                   "'filterType': 'Between', 'values': [1638160959907, 1638161259907]}], 'isResult': True}], "
                   "'queryLimits': {'groupingFeature': {'elementInstanceType': 'Process', 'featureName': "
                   "'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, "
                   "'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', 'creationTime', 'endTime', "
                   "'commandLine', 'imageFile.maliciousClassificationType', 'productType', 'children', "
                   "'parentProcess', 'ownerMachine', 'calculatedUser', 'imageFile', 'imageFile.sha1String', "
                   "'imageFile.md5String', 'imageFile.sha256String', 'imageFile.companyName', 'imageFile.productName', "
                   "'applicablePid', 'imageFileExtensionType', 'integrity', 'tid', 'isAggregate', 'isDotNetProtected', "
                   "'hasMalops', 'hasSuspicions', 'relatedToMalop', 'multipleSizeForHashEvidence', "
                   "'isImageFileVerified', 'knownMaliciousToolSuspicion', 'knownMalwareSuspicion', "
                   "'knownUnwantedSuspicion', 'isMaliciousByHashEvidence', 'imageFileMultipleCompanyNamesEvidence', "
                   "'multipleHashForUnsignedPeInfoEvidence', 'multipleNameForHashEvidence', 'unknownEvidence', "
                   "'rareHasPeMismatchEvidence', 'imageFile.signedInternalOrExternal', "
                   "'unknownUnsignedBySigningCompany', 'imageFileUnsignedEvidence', "
                   "'imageFileUnsignedHasSignedVersionEvidence', 'unwantedModuleSuspicion', "
                   "'imageFile.signerInternalOrExternal', 'architecture', 'commandLineContainsTempEvidence', "
                   "'hasChildren', 'hasClassification', 'hasVisibleWindows', 'hasWindows', 'isInstaller', "
                   "'isIdentifiedProduct', 'hasModuleFromTempEvidence', 'nonExecutableExtensionEvidence', "
                   "'isNotShellRunner', 'runningFromTempEvidence', 'shellOfNonShellRunnerSuspicion', "
                   "'shellWithElevatedPrivilegesEvidence', 'systemUserEvidence', 'hasExternalConnection', "
                   "'hasExternalConnectionToWellKnownPortEvidence', 'hasIncomingConnection', 'hasInternalConnection', "
                   "'hasMailConnectionForNonMailProcessEvidence', 'hasListeningConnection', 'hasOutgoingConnection', "
                   "'hasUnresolvedDnsQueriesFromDomain', 'multipleUnresolvedRecordNotExistsEvidence', "
                   "'hasNonDefaultResolverEvidence', 'parentProcessNotMatchHierarchySuspicion', "
                   "'parentProcessNotAdminUserEvidence', 'parentProcessFromRemovableDeviceEvidence', 'autorun', "
                   "'childrenCreatedByThread', 'connections', 'elevatedPrivilegeChildren', 'hackerToolChildren', "
                   "'hostProcess', 'hostUser', 'hostedChildren', 'injectedChildren', 'loadedModules', 'logonSession', "
                   "'remoteSession', 'service', 'execedBy', 'connectionsToMaliciousDomain', "
                   "'connectionsToMalwareAddresses', 'externalConnections', "
                   "'absoluteHighVolumeMaliciousAddressConnections', 'absoluteHighVolumeExternalConnections', "
                   "'incomingConnections', 'incomingExternalConnections', 'incomingInternalConnections', "
                   "'internalConnections', 'listeningConnections', 'localConnections', 'mailConnections', "
                   "'outgoingConnections', 'outgoingExternalConnections', 'outgoingInternalConnections', "
                   "'suspiciousExternalConnections', 'suspiciousInternalConnections', 'wellKnownPortConnections', "
                   "'lowTtlDnsQueries', 'nonDefaultResolverQueries', 'resolvedDnsQueriesDomainToDomain', "
                   "'resolvedDnsQueriesDomainToIp', 'resolvedDnsQueriesIpToDomain', "
                   "'suspiciousDnsQueryDomainToDomain', 'unresolvedQueryFromSuspiciousDomain', "
                   "'dnsQueryFromSuspiciousDomain', 'dnsQueryToSuspiciousDomain', 'unresolvedRecordNotExist', "
                   "'unresolvedDnsQueriesFromDomain', 'unresolvedDnsQueriesFromIp', "
                   "'maliciousToolClassificationModules', 'malwareClassificationModules', 'modulesNotInLoaderDbList', "
                   "'modulesFromTemp', 'unsignedWithSignedVersionModules', 'unwantedClassificationModules', "
                   "'accessToMalwareAddressInfectedProcess', 'connectingToBadReputationAddressSuspicion', "
                   "'hasMaliciousConnectionEvidence', 'hasSuspiciousExternalConnectionSuspicion', "
                   "'highNumberOfExternalConnectionsSuspicion', 'nonDefaultResolverSuspicion', "
                   "'hasRareExternalConnectionEvidence', 'hasRareRemoteAddressEvidence', 'suspiciousMailConnections', "
                   "'accessToMalwareAddressByUnknownProcess', "
                   "'hasAbsoluteHighVolumeConnectionToMaliciousAddressEvidence', "
                   "'hasAbsoluteHighVolumeExternalOutgoingConnectionEvidence', 'highDataTransmittedSuspicion', "
                   "'highDataVolumeTransmittedToMaliciousAddressSuspicion', "
                   "'highDataVolumeTransmittedByUnknownProcess', "
                   "'absoluteHighNumberOfInternalOutgoingEmbryonicConnectionsEvidence', 'dgaSuspicion', "
                   "'hasLowTtlDnsQueryEvidence', 'highUnresolvedToResolvedRateEvidence', "
                   "'manyUnresolvedRecordNotExistsEvidence', 'hasChildKnownHackerToolEvidence', "
                   "'hackingToolOfNonToolRunnerEvidence', 'hackingToolOfNonToolRunnerSuspicion', "
                   "'hasRareChildProcessKnownHackerToolEvidence', 'maliciousToolModuleSuspicion', "
                   "'deletedParentProcessEvidence', 'malwareModuleSuspicion', 'dualExtensionNameEvidence', "
                   "'hiddenFileExtensionEvidence', 'rightToLeftFileExtensionEvidence', "
                   "'screenSaverWithChildrenEvidence', 'suspicionsScreenSaverEvidence', 'hasPeFloatingCodeEvidence', "
                   "'hasSectionMismatchEvidence', 'detectedInjectedEvidence', 'detectedInjectingEvidence', "
                   "'detectedInjectingToProtectedProcessEvidence', 'hasInjectedChildren', "
                   "'hostingInjectedThreadEvidence', 'injectedProtectedProcessEvidence', "
                   "'maliciousInjectingCodeSuspicion', 'injectionMethod', 'isHostingInjectedThread', "
                   "'maliciousInjectedCodeSuspicion', 'maliciousPeExecutionSuspicion', "
                   "'hasSuspiciousInternalConnectionEvidence', 'highInternalOutgoingEmbryonicConnectionRateEvidence', "
                   "'highNumberOfInternalConnectionsEvidence', 'newProcessesAboveThresholdEvidence', "
                   "'hasRareInternalConnectionEvidence', 'elevatingPrivilegesToChildEvidence', "
                   "'parentProcessNotSystemUserEvidence', 'privilegeEscalationEvidence', "
                   "'firstExecutionOfDownloadedProcessEvidence', 'hasAutorun', 'newProcessEvidence', "
                   "'markedForPrevention', 'ransomwareAutoRemediationSuspended', 'totalNumOfInstances', "
                   "'lastMinuteNumOfInstances', 'lastSeenTimeStamp', 'wmiQueryStrings', 'isExectuedByWmi', "
                   "'absoluteHighNumberOfInternalConnectionsEvidence', 'scanningProcessSuspicion', "
                   "'imageFile.isDownloadedFromInternet', 'imageFile.downloadedFromDomain', "
                   "'imageFile.downloadedFromIpAddress', 'imageFile.downloadedFromUrl', "
                   "'imageFile.downloadedFromUrlReferrer', 'imageFile.downloadedFromEmailFrom', "
                   "'imageFile.downloadedFromEmailMessageId', 'imageFile.downloadedFromEmailSubject', 'rpcRequests', "
                   "'iconBase64', 'executionPrevented', 'isWhiteListClassification', 'matchedWhiteListRuleIds']}"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_boolean_true_value_query(self):
        stix_pattern = "[user-account:is_privileged = 'TRUE']"
        query = translation.translate('cybereason', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'queryPath': [{'requestedType': 'User', 'filters': [{'facetName': 'isAdmin', 'filterType': "
                   "'Equals', 'values': [True]}, {'facetName': 'adCreated', 'filterType': 'Between', 'values': ["
                   "1638162578613, 1638162878613]}], 'isResult': True}], 'queryLimits': {'groupingFeature': {"
                   "'elementInstanceType': 'User', 'featureName': 'elementDisplayName'}}, 'perFeatureLimit': 1, "
                   "'totalResultLimit': 9999, 'perGroupLimit': 1, 'templateContext': 'CUSTOM', 'customFields': ["
                   "'elementDisplayName', 'domain', 'ownerOrganization.name', 'ownerMachine', 'isLocalSystem', "
                   "'isAdmin', 'username', 'emailAddress', 'numberOfMachines', 'passwordAgeDays', 'privileges', "
                   "'comment', 'adCanonicalName', 'adCreated', 'adDisplayName', 'adLogonName', 'adMail', 'adMemberOf', "
                   "'adOU', 'adPrimaryGroupID', 'adSamAccountName', 'adTitle', 'hasPowerTool', 'hasMaliciousProcess', "
                   "'hasSuspicions', 'hasSuspiciousProcess', 'runningMaliciousProcessEvidence', "
                   "'hasRareProcessWithExternalConnections']}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_boolean_false_value_query(self):
        stix_pattern = "[user-account:is_privileged = '0']"
        query = translation.translate('cybereason', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'queryPath': [{'requestedType': 'User', 'filters': [{'facetName': 'isAdmin', 'filterType': "
                   "'Equals', 'values': [False]}, {'facetName': 'adCreated', 'filterType': 'Between', 'values': ["
                   "1638162578613, 1638162878613]}], 'isResult': True}], 'queryLimits': {'groupingFeature': {"
                   "'elementInstanceType': 'User', 'featureName': 'elementDisplayName'}}, 'perFeatureLimit': 1, "
                   "'totalResultLimit': 9999, 'perGroupLimit': 1, 'templateContext': 'CUSTOM', 'customFields': ["
                   "'elementDisplayName', 'domain', 'ownerOrganization.name', 'ownerMachine', 'isLocalSystem', "
                   "'isAdmin', 'username', 'emailAddress', 'numberOfMachines', 'passwordAgeDays', 'privileges', "
                   "'comment', 'adCanonicalName', 'adCreated', 'adDisplayName', 'adLogonName', 'adMail', 'adMemberOf', "
                   "'adOU', 'adPrimaryGroupID', 'adSamAccountName', 'adTitle', 'hasPowerTool', 'hasMaliciousProcess', "
                   "'hasSuspicions', 'hasSuspiciousProcess', 'runningMaliciousProcessEvidence', "
                   "'hasRareProcessWithExternalConnections']}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_merge_similar_element_timestamp_query(self):
        stix_pattern = "[network-traffic:src_port = 23 AND network-traffic:protocols[*] = 'tcp'] START " \
                       "t'2019-10-01T08:43:10.003Z' STOP t'2019-11-30T10:43:10.005Z' "

        query = translation.translate('cybereason', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [
            "{'queryPath': [{'requestedType': 'Connection', 'filters': [{'facetName': 'localPort', 'filterType': "
            "'Equals', 'values': [23]}, {'facetName': 'transportProtocol', 'filterType': 'Equals', 'values': ["
            "'tcp']}, {'facetName': 'creationTime', 'filterType': 'Between', 'values': [1569919390003, "
            "1575110590005]}], 'isResult': True}], 'queryLimits': {'groupingFeature': {'elementInstanceType': "
            "'Connection', 'featureName': 'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': "
            "9999, 'perGroupLimit': 1, 'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', "
            "'direction', 'ownerMachine', 'ownerProcess', 'serverPort', 'serverAddress', 'portType', "
            "'aggregatedReceivedBytesCount', 'aggregatedTransmittedBytesCount', 'remoteAddressCountryName', "
            "'dnsQuery', 'calculatedCreationTime', 'domainName', 'endTime', 'localPort', 'portDescription', "
            "'remotePort', 'state', 'isExternalConnection', 'isIncoming', 'remoteAddressInternalExternalLocal', "
            "'transportProtocol', 'hasMalops', 'hasSuspicions', 'relatedToMalop', 'isWellKnownPort', "
            "'isProcessLegit', 'isProcessMalware', 'localAddress', 'remoteAddress', 'urlDomains']}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_is_reversed_parm_query(self):
        stix_pattern = "[x-cybereason-process:architecture = '64 bit' AND network-traffic:src_port = 23 ] START " \
                       "t'2019-10-01T08:43:10.003Z' STOP t'2019-11-30T10:43:10.005Z' "
        query = translation.translate('cybereason', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [
            "{'queryPath': [{'requestedType': 'Connection', 'filters': [{'facetName': 'localPort', 'filterType': "
            "'Equals', 'values': [23]}, {'facetName': 'creationTime', "
            "'filterType': 'Between', 'values': [1569919390003, 1575110590005]}], "
            "'connectionFeature': {'elementInstanceType': 'Process', "
            "'featureName': 'connections'}, 'isReversed': True}, {'requestedType': 'Process', 'filters': [{"
            "'facetName': 'architecture', 'filterType': 'Equals', 'values': ['64 bit']}, {'facetName': "
            "'creationTime', 'filterType': 'Between', 'values': [1569919390003, 1575110590005]}], 'isResult': "
            "True}], 'queryLimits': {'groupingFeature': {'elementInstanceType': 'Process', 'featureName': "
            "'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, "
            "'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', 'creationTime', 'endTime', "
            "'commandLine', 'imageFile.maliciousClassificationType', 'productType', 'children', 'parentProcess', "
            "'ownerMachine', 'calculatedUser', 'imageFile', 'imageFile.sha1String', 'imageFile.md5String', "
            "'imageFile.sha256String', 'imageFile.companyName', 'imageFile.productName', 'applicablePid', "
            "'imageFileExtensionType', 'integrity', 'tid', 'isAggregate', 'isDotNetProtected', 'hasMalops', "
            "'hasSuspicions', 'relatedToMalop', 'multipleSizeForHashEvidence', 'isImageFileVerified', "
            "'knownMaliciousToolSuspicion', 'knownMalwareSuspicion', 'knownUnwantedSuspicion', "
            "'isMaliciousByHashEvidence', 'imageFileMultipleCompanyNamesEvidence', "
            "'multipleHashForUnsignedPeInfoEvidence', 'multipleNameForHashEvidence', 'unknownEvidence', "
            "'rareHasPeMismatchEvidence', 'imageFile.signedInternalOrExternal', "
            "'unknownUnsignedBySigningCompany', 'imageFileUnsignedEvidence', "
            "'imageFileUnsignedHasSignedVersionEvidence', 'unwantedModuleSuspicion', "
            "'imageFile.signerInternalOrExternal', 'architecture', 'commandLineContainsTempEvidence', "
            "'hasChildren', 'hasClassification', 'hasVisibleWindows', 'hasWindows', 'isInstaller', "
            "'isIdentifiedProduct', 'hasModuleFromTempEvidence', 'nonExecutableExtensionEvidence', "
            "'isNotShellRunner', 'runningFromTempEvidence', 'shellOfNonShellRunnerSuspicion', "
            "'shellWithElevatedPrivilegesEvidence', 'systemUserEvidence', 'hasExternalConnection', "
            "'hasExternalConnectionToWellKnownPortEvidence', 'hasIncomingConnection', 'hasInternalConnection', "
            "'hasMailConnectionForNonMailProcessEvidence', 'hasListeningConnection', 'hasOutgoingConnection', "
            "'hasUnresolvedDnsQueriesFromDomain', 'multipleUnresolvedRecordNotExistsEvidence', "
            "'hasNonDefaultResolverEvidence', 'parentProcessNotMatchHierarchySuspicion', "
            "'parentProcessNotAdminUserEvidence', 'parentProcessFromRemovableDeviceEvidence', 'autorun', "
            "'childrenCreatedByThread', 'connections', 'elevatedPrivilegeChildren', 'hackerToolChildren', "
            "'hostProcess', 'hostUser', 'hostedChildren', 'injectedChildren', 'loadedModules', 'logonSession', "
            "'remoteSession', 'service', 'execedBy', 'connectionsToMaliciousDomain', "
            "'connectionsToMalwareAddresses', 'externalConnections', "
            "'absoluteHighVolumeMaliciousAddressConnections', 'absoluteHighVolumeExternalConnections', "
            "'incomingConnections', 'incomingExternalConnections', 'incomingInternalConnections', "
            "'internalConnections', 'listeningConnections', 'localConnections', 'mailConnections', "
            "'outgoingConnections', 'outgoingExternalConnections', 'outgoingInternalConnections', "
            "'suspiciousExternalConnections', 'suspiciousInternalConnections', 'wellKnownPortConnections', "
            "'lowTtlDnsQueries', 'nonDefaultResolverQueries', 'resolvedDnsQueriesDomainToDomain', "
            "'resolvedDnsQueriesDomainToIp', 'resolvedDnsQueriesIpToDomain', 'suspiciousDnsQueryDomainToDomain', "
            "'unresolvedQueryFromSuspiciousDomain', 'dnsQueryFromSuspiciousDomain', "
            "'dnsQueryToSuspiciousDomain', 'unresolvedRecordNotExist', 'unresolvedDnsQueriesFromDomain', "
            "'unresolvedDnsQueriesFromIp', 'maliciousToolClassificationModules', 'malwareClassificationModules', "
            "'modulesNotInLoaderDbList', 'modulesFromTemp', 'unsignedWithSignedVersionModules', "
            "'unwantedClassificationModules', 'accessToMalwareAddressInfectedProcess', "
            "'connectingToBadReputationAddressSuspicion', 'hasMaliciousConnectionEvidence', "
            "'hasSuspiciousExternalConnectionSuspicion', 'highNumberOfExternalConnectionsSuspicion', "
            "'nonDefaultResolverSuspicion', 'hasRareExternalConnectionEvidence', 'hasRareRemoteAddressEvidence', "
            "'suspiciousMailConnections', 'accessToMalwareAddressByUnknownProcess', "
            "'hasAbsoluteHighVolumeConnectionToMaliciousAddressEvidence', "
            "'hasAbsoluteHighVolumeExternalOutgoingConnectionEvidence', 'highDataTransmittedSuspicion', "
            "'highDataVolumeTransmittedToMaliciousAddressSuspicion', "
            "'highDataVolumeTransmittedByUnknownProcess', "
            "'absoluteHighNumberOfInternalOutgoingEmbryonicConnectionsEvidence', 'dgaSuspicion', "
            "'hasLowTtlDnsQueryEvidence', 'highUnresolvedToResolvedRateEvidence', "
            "'manyUnresolvedRecordNotExistsEvidence', 'hasChildKnownHackerToolEvidence', "
            "'hackingToolOfNonToolRunnerEvidence', 'hackingToolOfNonToolRunnerSuspicion', "
            "'hasRareChildProcessKnownHackerToolEvidence', 'maliciousToolModuleSuspicion', "
            "'deletedParentProcessEvidence', 'malwareModuleSuspicion', 'dualExtensionNameEvidence', "
            "'hiddenFileExtensionEvidence', 'rightToLeftFileExtensionEvidence', "
            "'screenSaverWithChildrenEvidence', 'suspicionsScreenSaverEvidence', 'hasPeFloatingCodeEvidence', "
            "'hasSectionMismatchEvidence', 'detectedInjectedEvidence', 'detectedInjectingEvidence', "
            "'detectedInjectingToProtectedProcessEvidence', 'hasInjectedChildren', "
            "'hostingInjectedThreadEvidence', 'injectedProtectedProcessEvidence', "
            "'maliciousInjectingCodeSuspicion', 'injectionMethod', 'isHostingInjectedThread', "
            "'maliciousInjectedCodeSuspicion', 'maliciousPeExecutionSuspicion', "
            "'hasSuspiciousInternalConnectionEvidence', 'highInternalOutgoingEmbryonicConnectionRateEvidence', "
            "'highNumberOfInternalConnectionsEvidence', 'newProcessesAboveThresholdEvidence', "
            "'hasRareInternalConnectionEvidence', 'elevatingPrivilegesToChildEvidence', "
            "'parentProcessNotSystemUserEvidence', 'privilegeEscalationEvidence', "
            "'firstExecutionOfDownloadedProcessEvidence', 'hasAutorun', 'newProcessEvidence', "
            "'markedForPrevention', 'ransomwareAutoRemediationSuspended', 'totalNumOfInstances', "
            "'lastMinuteNumOfInstances', 'lastSeenTimeStamp', 'wmiQueryStrings', 'isExectuedByWmi', "
            "'absoluteHighNumberOfInternalConnectionsEvidence', 'scanningProcessSuspicion', "
            "'imageFile.isDownloadedFromInternet', 'imageFile.downloadedFromDomain', "
            "'imageFile.downloadedFromIpAddress', 'imageFile.downloadedFromUrl', "
            "'imageFile.downloadedFromUrlReferrer', 'imageFile.downloadedFromEmailFrom', "
            "'imageFile.downloadedFromEmailMessageId', 'imageFile.downloadedFromEmailSubject', 'rpcRequests', "
            "'iconBase64', 'executionPrevented', 'isWhiteListClassification', 'matchedWhiteListRuleIds']}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_observation_with_qualifier_query(self):
        stix_pattern = "[file:size > 10 ] START t'2020-10-01T00:00:00.030Z' STOP t'2021-10-07T00:00:00.030Z' AND [ " \
                       "x-cybereason-service:name = 'Windows Push Notifications User Service_2d02eb' AND " \
                       "x-oca-asset:os_version = 'Windows_Server_2016'] "
        query = translation.translate('cybereason', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'queryPath': [{'requestedType': 'File', 'filters': [{'facetName': 'size', 'filterType': "
                   "'GreaterThan', 'values': [10]}, {'facetName': 'createdTime', 'filterType': 'Between', 'values': ["
                   "1601510400030, 1633564800030]}], 'isResult': True}], 'queryLimits': {'groupingFeature': {"
                   "'elementInstanceType': 'File', 'featureName': 'elementDisplayName'}}, 'perFeatureLimit': 1, "
                   "'totalResultLimit': 9999, 'perGroupLimit': 1, 'templateContext': 'CUSTOM', 'customFields': ["
                   "'elementDisplayName', 'avRemediationStatus', 'signerInternalOrExternal', 'fileHash', 'autoruns', "
                   "'ownerMachine', 'mount', 'autorun', 'dualExtensionEvidence', 'hiddenFileExtensionEvidence', "
                   "'rightToLeftFileExtensionEvidence', 'hasMalops', 'hasSuspicions', 'maliciousClassificationType', "
                   "'hackingToolClassificationEvidence', 'classificationLink', 'isPEFile', "
                   "'executedByProcessEvidence', 'hasAutorun', 'isInstallerProperties', 'isFromRemovableDevice', "
                   "'productType', 'secondExtensionType', 'temporaryFolderEvidence', 'multipleCompanyNamesEvidence', "
                   "'multipleHashForUnsignedPeInfoEvidence', 'unsignedHasSignedVersionEvidence', "
                   "'classificationComment', 'signedInternalOrExternal', 'signatureVerifiedInternalOrExternal', "
                   "'classificationBlocking', 'isDownloadedFromInternet', 'downloadedFromDomain', "
                   "'downloadedFromIpAddress', 'downloadedFromUrl', 'downloadedFromUrlReferrer', "
                   "'downloadedFromEmailFrom', 'downloadedFromEmailMessageId', 'downloadedFromEmailSubject', "
                   "'legalCopyright', 'legalTrademarks', 'privateBuild', 'specialBuild', 'companyName', "
                   "'createdTime', 'extensionType', 'fileDescription', 'internalName', 'md5String', 'modifiedTime', "
                   "'originalFileName', 'correctedPath', 'productName', 'productVersion', 'sha1String', 'size', "
                   "'comments', 'fileVersion', 'applicationIdentifier', 'sha256String']}",
                   "{'queryPath': [{"
                   "'requestedType': 'Machine', 'filters': [{'facetName': 'osVersionType', 'filterType': 'Equals', "
                   "'values': ['Windows_Server_2016']}, {'facetName': 'lastSeenTimeStamp', 'filterType': 'Between', "
                   "'values': [1669869087615, 1669869387615]}], 'connectionFeature': {'elementInstanceType': "
                   "'Machine', 'featureName': 'services'}}, {'requestedType': 'Service', 'filters': [{'facetName': "
                   "'displayName', 'filterType': 'Equals', 'values': ['Windows Push Notifications User "
                   "Service_2d02eb']}, {'facetName': 'endTime', 'filterType': 'Between', 'values': [1669869087615, "
                   "1669869387615]}], 'isResult': True}], 'queryLimits': {'groupingFeature': {'elementInstanceType': "
                   "'Service', 'featureName': 'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, "
                   "'perGroupLimit': 1, 'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', "
                   "'binaryFile', 'ownerMachine', 'process', 'serviceStartName', 'commandLineArguments', "
                   "'description', 'displayName', 'endTime', 'isActive', 'startType', 'unitFilePath', 'serviceState', "
                   "'serviceSubState', 'isAutoRestartService', 'hasSuspicions', 'newServiceEvidence', "
                   "'rareServiceEvidence', 'serviceType', 'driver']}",
                   "{'queryPath': [{'requestedType': 'Machine', "
                   "'filters': [{'facetName': 'osVersionType', 'filterType': 'Equals', 'values': ["
                   "'Windows_Server_2016']}, {'facetName': 'lastSeenTimeStamp', 'filterType': 'Between', 'values': ["
                   "1669869087615, 1669869387615]}], 'connectionFeature': {'elementInstanceType': 'Machine', "
                   "'featureName': 'services'}}, {'requestedType': 'Service', 'filters': [{'facetName': "
                   "'oldServiceStartName', 'filterType': 'Equals', 'values': ['Windows Push Notifications User "
                   "Service_2d02eb']}, {'facetName': 'endTime', 'filterType': 'Between', 'values': [1669869087615, "
                   "1669869387615]}], 'isResult': True}], 'queryLimits': {'groupingFeature': {'elementInstanceType': "
                   "'Service', 'featureName': 'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, "
                   "'perGroupLimit': 1, 'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', "
                   "'binaryFile', 'ownerMachine', 'process', 'serviceStartName', 'commandLineArguments', "
                   "'description', 'displayName', 'endTime', 'isActive', 'startType', 'unitFilePath', 'serviceState', "
                   "'serviceSubState', 'isAutoRestartService', 'hasSuspicions', 'newServiceEvidence', "
                   "'rareServiceEvidence', 'serviceType', 'driver']}",
                   "{'queryPath': [{'requestedType': 'Machine', "
                   "'filters': [{'facetName': 'osVersionType', 'filterType': 'Equals', 'values': ["
                   "'Windows_Server_2016']}, {'facetName': 'lastSeenTimeStamp', 'filterType': 'Between', 'values': ["
                   "1669869087615, 1669869387615]}], 'connectionFeature': {'elementInstanceType': 'Machine', "
                   "'featureName': 'services'}}, {'requestedType': 'Service', 'filters': [{'facetName': "
                   "'elementDisplayName', 'filterType': 'Equals', 'values': ['Windows Push Notifications User "
                   "Service_2d02eb']}, {'facetName': 'endTime', 'filterType': 'Between', 'values': [1669869087615, "
                   "1669869387615]}], 'isResult': True}], 'queryLimits': {'groupingFeature': {'elementInstanceType': "
                   "'Service', 'featureName': 'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, "
                   "'perGroupLimit': 1, 'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', "
                   "'binaryFile', 'ownerMachine', 'process', 'serviceStartName', 'commandLineArguments', "
                   "'description', 'displayName', 'endTime', 'isActive', 'startType', 'unitFilePath', 'serviceState', "
                   "'serviceSubState', 'isAutoRestartService', 'hasSuspicions', 'newServiceEvidence', "
                   "'rareServiceEvidence', 'serviceType', 'driver']}",
                   "{'queryPath': [{'requestedType': 'Machine', "
                   "'filters': [{'facetName': 'osVersionType', 'filterType': 'Equals', 'values': ["
                   "'Windows_Server_2016']}, {'facetName': 'lastSeenTimeStamp', 'filterType': 'Between', 'values': ["
                   "1669869087615, 1669869387615]}], 'connectionFeature': {'elementInstanceType': 'Machine', "
                   "'featureName': 'services'}}, {'requestedType': 'Service', 'filters': [{'facetName': "
                   "'serviceStartName', 'filterType': 'Equals', 'values': ['Windows Push Notifications User "
                   "Service_2d02eb']}, {'facetName': 'endTime', 'filterType': 'Between', 'values': [1669869087615, "
                   "1669869387615]}], 'isResult': True}], 'queryLimits': {'groupingFeature': {'elementInstanceType': "
                   "'Service', 'featureName': 'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, "
                   "'perGroupLimit': 1, 'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', "
                   "'binaryFile', 'ownerMachine', 'process', 'serviceStartName', 'commandLineArguments', "
                   "'description', 'displayName', 'endTime', 'isActive', 'startType', 'unitFilePath', 'serviceState', "
                   "'serviceSubState', 'isAutoRestartService', 'hasSuspicions', 'newServiceEvidence', "
                   "'rareServiceEvidence', 'serviceType', 'driver']}",
                   "{'queryPath': [{'requestedType': 'Machine', "
                   "'filters': [{'facetName': 'osVersionType', 'filterType': 'Equals', 'values': ["
                   "'Windows_Server_2016']}, {'facetName': 'lastSeenTimeStamp', 'filterType': 'Between', 'values': ["
                   "1669869087615, 1669869387615]}], 'connectionFeature': {'elementInstanceType': 'Machine', "
                   "'featureName': 'drivers'}}, {'requestedType': 'Driver', 'filters': [{'facetName': 'service', "
                   "'filterType': 'Equals', 'values': ['Windows Push Notifications User Service_2d02eb']}, "
                   "{'facetName': 'endTime', 'filterType': 'Between', 'values': [1669869087615, 1669869387615]}], "
                   "'isResult': True}], 'queryLimits': {'groupingFeature': {'elementInstanceType': 'Driver', "
                   "'featureName': 'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, "
                   "'perGroupLimit': 1, 'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', "
                   "'creationTime', 'file', 'ownerMachine', 'service', 'endTime', 'newDriverEvidence', "
                   "'hasSuspicions']}",
                   "{'queryPath': [{'requestedType': 'Machine', 'filters': [{'facetName': "
                   "'osVersionType', 'filterType': 'Equals', 'values': ['Windows_Server_2016']}, {'facetName': "
                   "'lastSeenTimeStamp', 'filterType': 'Between', 'values': [1669869087615, 1669869387615]}], "
                   "'connectionFeature': {'elementInstanceType': 'Machine', 'featureName': 'processes'}}, "
                   "{'requestedType': 'Process', 'filters': [{'facetName': 'service', 'filterType': 'Equals', "
                   "'values': ['Windows Push Notifications User Service_2d02eb']}, {'facetName': 'creationTime', "
                   "'filterType': 'Between', 'values': [1669869087615, 1669869387615]}], 'isResult': True}], "
                   "'queryLimits': {'groupingFeature': {'elementInstanceType': 'Process', 'featureName': "
                   "'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, "
                   "'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', 'creationTime', 'endTime', "
                   "'commandLine', 'imageFile.maliciousClassificationType', 'productType', 'children', "
                   "'parentProcess', 'ownerMachine', 'calculatedUser', 'imageFile', 'imageFile.sha1String', "
                   "'imageFile.md5String', 'imageFile.sha256String', 'imageFile.companyName', "
                   "'imageFile.productName', 'applicablePid', 'imageFileExtensionType', 'integrity', 'tid', "
                   "'isAggregate', 'isDotNetProtected', 'hasMalops', 'hasSuspicions', 'relatedToMalop', "
                   "'multipleSizeForHashEvidence', 'isImageFileVerified', 'knownMaliciousToolSuspicion', "
                   "'knownMalwareSuspicion', 'knownUnwantedSuspicion', 'isMaliciousByHashEvidence', "
                   "'imageFileMultipleCompanyNamesEvidence', 'multipleHashForUnsignedPeInfoEvidence', "
                   "'multipleNameForHashEvidence', 'unknownEvidence', 'rareHasPeMismatchEvidence', "
                   "'imageFile.signedInternalOrExternal', 'unknownUnsignedBySigningCompany', "
                   "'imageFileUnsignedEvidence', 'imageFileUnsignedHasSignedVersionEvidence', "
                   "'unwantedModuleSuspicion', 'imageFile.signerInternalOrExternal', 'architecture', "
                   "'commandLineContainsTempEvidence', 'hasChildren', 'hasClassification', 'hasVisibleWindows', "
                   "'hasWindows', 'isInstaller', 'isIdentifiedProduct', 'hasModuleFromTempEvidence', "
                   "'nonExecutableExtensionEvidence', 'isNotShellRunner', 'runningFromTempEvidence', "
                   "'shellOfNonShellRunnerSuspicion', 'shellWithElevatedPrivilegesEvidence', 'systemUserEvidence', "
                   "'hasExternalConnection', 'hasExternalConnectionToWellKnownPortEvidence', 'hasIncomingConnection', "
                   "'hasInternalConnection', 'hasMailConnectionForNonMailProcessEvidence', 'hasListeningConnection', "
                   "'hasOutgoingConnection', 'hasUnresolvedDnsQueriesFromDomain', "
                   "'multipleUnresolvedRecordNotExistsEvidence', 'hasNonDefaultResolverEvidence', "
                   "'parentProcessNotMatchHierarchySuspicion', 'parentProcessNotAdminUserEvidence', "
                   "'parentProcessFromRemovableDeviceEvidence', 'autorun', 'childrenCreatedByThread', 'connections', "
                   "'elevatedPrivilegeChildren', 'hackerToolChildren', 'hostProcess', 'hostUser', 'hostedChildren', "
                   "'injectedChildren', 'loadedModules', 'logonSession', 'remoteSession', 'service', 'execedBy', "
                   "'connectionsToMaliciousDomain', 'connectionsToMalwareAddresses', 'externalConnections', "
                   "'absoluteHighVolumeMaliciousAddressConnections', 'absoluteHighVolumeExternalConnections', "
                   "'incomingConnections', 'incomingExternalConnections', 'incomingInternalConnections', "
                   "'internalConnections', 'listeningConnections', 'localConnections', 'mailConnections', "
                   "'outgoingConnections', 'outgoingExternalConnections', 'outgoingInternalConnections', "
                   "'suspiciousExternalConnections', 'suspiciousInternalConnections', 'wellKnownPortConnections', "
                   "'lowTtlDnsQueries', 'nonDefaultResolverQueries', 'resolvedDnsQueriesDomainToDomain', "
                   "'resolvedDnsQueriesDomainToIp', 'resolvedDnsQueriesIpToDomain', "
                   "'suspiciousDnsQueryDomainToDomain', 'unresolvedQueryFromSuspiciousDomain', "
                   "'dnsQueryFromSuspiciousDomain', 'dnsQueryToSuspiciousDomain', 'unresolvedRecordNotExist', "
                   "'unresolvedDnsQueriesFromDomain', 'unresolvedDnsQueriesFromIp', "
                   "'maliciousToolClassificationModules', 'malwareClassificationModules', 'modulesNotInLoaderDbList', "
                   "'modulesFromTemp', 'unsignedWithSignedVersionModules', 'unwantedClassificationModules', "
                   "'accessToMalwareAddressInfectedProcess', 'connectingToBadReputationAddressSuspicion', "
                   "'hasMaliciousConnectionEvidence', 'hasSuspiciousExternalConnectionSuspicion', "
                   "'highNumberOfExternalConnectionsSuspicion', 'nonDefaultResolverSuspicion', "
                   "'hasRareExternalConnectionEvidence', 'hasRareRemoteAddressEvidence', 'suspiciousMailConnections', "
                   "'accessToMalwareAddressByUnknownProcess', "
                   "'hasAbsoluteHighVolumeConnectionToMaliciousAddressEvidence', "
                   "'hasAbsoluteHighVolumeExternalOutgoingConnectionEvidence', 'highDataTransmittedSuspicion', "
                   "'highDataVolumeTransmittedToMaliciousAddressSuspicion', "
                   "'highDataVolumeTransmittedByUnknownProcess', "
                   "'absoluteHighNumberOfInternalOutgoingEmbryonicConnectionsEvidence', 'dgaSuspicion', "
                   "'hasLowTtlDnsQueryEvidence', 'highUnresolvedToResolvedRateEvidence', "
                   "'manyUnresolvedRecordNotExistsEvidence', 'hasChildKnownHackerToolEvidence', "
                   "'hackingToolOfNonToolRunnerEvidence', 'hackingToolOfNonToolRunnerSuspicion', "
                   "'hasRareChildProcessKnownHackerToolEvidence', 'maliciousToolModuleSuspicion', "
                   "'deletedParentProcessEvidence', 'malwareModuleSuspicion', 'dualExtensionNameEvidence', "
                   "'hiddenFileExtensionEvidence', 'rightToLeftFileExtensionEvidence', "
                   "'screenSaverWithChildrenEvidence', 'suspicionsScreenSaverEvidence', 'hasPeFloatingCodeEvidence', "
                   "'hasSectionMismatchEvidence', 'detectedInjectedEvidence', 'detectedInjectingEvidence', "
                   "'detectedInjectingToProtectedProcessEvidence', 'hasInjectedChildren', "
                   "'hostingInjectedThreadEvidence', 'injectedProtectedProcessEvidence', "
                   "'maliciousInjectingCodeSuspicion', 'injectionMethod', 'isHostingInjectedThread', "
                   "'maliciousInjectedCodeSuspicion', 'maliciousPeExecutionSuspicion', "
                   "'hasSuspiciousInternalConnectionEvidence', 'highInternalOutgoingEmbryonicConnectionRateEvidence', "
                   "'highNumberOfInternalConnectionsEvidence', 'newProcessesAboveThresholdEvidence', "
                   "'hasRareInternalConnectionEvidence', 'elevatingPrivilegesToChildEvidence', "
                   "'parentProcessNotSystemUserEvidence', 'privilegeEscalationEvidence', "
                   "'firstExecutionOfDownloadedProcessEvidence', 'hasAutorun', 'newProcessEvidence', "
                   "'markedForPrevention', 'ransomwareAutoRemediationSuspended', 'totalNumOfInstances', "
                   "'lastMinuteNumOfInstances', 'lastSeenTimeStamp', 'wmiQueryStrings', 'isExectuedByWmi', "
                   "'absoluteHighNumberOfInternalConnectionsEvidence', 'scanningProcessSuspicion', "
                   "'imageFile.isDownloadedFromInternet', 'imageFile.downloadedFromDomain', "
                   "'imageFile.downloadedFromIpAddress', 'imageFile.downloadedFromUrl', "
                   "'imageFile.downloadedFromUrlReferrer', 'imageFile.downloadedFromEmailFrom', "
                   "'imageFile.downloadedFromEmailMessageId', 'imageFile.downloadedFromEmailSubject', 'rpcRequests', "
                   "'iconBase64', 'executionPrevented', 'isWhiteListClassification', 'matchedWhiteListRuleIds']}"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_not_include_filter_query(self):
        stix_pattern = "[domain-name:value!='dl.delivery.mp.microsoft.com']"
        query = translation.translate('cybereason', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'queryPath': [{'requestedType': 'Connection', 'filters': [{'facetName': 'domainName', "
                   "'filterType': 'NotEquals', 'values': ['dl.delivery.mp.microsoft.com']}, {'facetName': "
                   "'creationTime', 'filterType': 'Between', 'values': [1643109026511, 1643109326511]}], 'isResult': "
                   "True}], 'queryLimits': {'groupingFeature': {'elementInstanceType': 'Connection', 'featureName': "
                   "'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, "
                   "'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', 'direction', 'ownerMachine', "
                   "'ownerProcess', 'serverPort', 'serverAddress', 'portType', 'aggregatedReceivedBytesCount', "
                   "'aggregatedTransmittedBytesCount', 'remoteAddressCountryName', 'dnsQuery', "
                   "'calculatedCreationTime', 'domainName', 'endTime', 'localPort', 'portDescription', 'remotePort', "
                   "'state', 'isExternalConnection', 'isIncoming', 'remoteAddressInternalExternalLocal', "
                   "'transportProtocol', 'hasMalops', 'hasSuspicions', 'relatedToMalop', 'isWellKnownPort', "
                   "'isProcessLegit', 'isProcessMalware', 'localAddress', 'remoteAddress', 'urlDomains']}",
                   "{'queryPath': [{'requestedType': 'Connection', 'filters': [{'facetName': 'urlDomains', "
                   "'filterType': 'NotIncludes', 'values': ['dl.delivery.mp.microsoft.com']}, {'facetName': "
                   "'creationTime', 'filterType': 'Between', 'values': [1643109026511, 1643109326511]}], 'isResult': "
                   "True}], 'queryLimits': {'groupingFeature': {'elementInstanceType': 'Connection', 'featureName': "
                   "'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, "
                   "'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', 'direction', 'ownerMachine', "
                   "'ownerProcess', 'serverPort', 'serverAddress', 'portType', 'aggregatedReceivedBytesCount', "
                   "'aggregatedTransmittedBytesCount', 'remoteAddressCountryName', 'dnsQuery', "
                   "'calculatedCreationTime', 'domainName', 'endTime', 'localPort', 'portDescription', 'remotePort', "
                   "'state', 'isExternalConnection', 'isIncoming', 'remoteAddressInternalExternalLocal', "
                   "'transportProtocol', 'hasMalops', 'hasSuspicions', 'relatedToMalop', 'isWellKnownPort', "
                   "'isProcessLegit', 'isProcessMalware', 'localAddress', 'remoteAddress', 'urlDomains']}",
                   "{'queryPath': [{'requestedType': 'Machine', 'filters': [{'facetName': 'domainFqdn', 'filterType': "
                   "'NotEquals', 'values': ['dl.delivery.mp.microsoft.com']}, {'facetName': 'lastSeenTimeStamp', "
                   "'filterType': 'Between', 'values': [1643109026511, 1643109326511]}], 'isResult': True}], "
                   "'queryLimits': {'groupingFeature': {'elementInstanceType': 'Machine', 'featureName': "
                   "'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, "
                   "'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', 'mountPoints', 'processes', "
                   "'services', 'logonSessions', 'hasRemovableDevice', 'timezoneUTCOffsetMinutes', 'osVersionType', "
                   "'platformArchitecture', 'mbrHashString', 'osType', 'domainFqdn', 'ownerOrganization', 'pylumId', "
                   "'adSid', 'adOU', 'adOrganization', 'adCanonicalName', 'adCompany', 'adDNSHostName', "
                   "'adDepartment', 'adDisplayName', 'adLocation', 'adMachineRole', 'adDescription', 'freeDiskSpace', "
                   "'totalDiskSpace', 'freeMemory', 'totalMemory', 'cpuCount', 'isLaptop', 'deviceModel', "
                   "'isActiveProbeConnected', 'uptime', 'isIsolated', 'lastSeenTimeStamp', "
                   "'timeStampSinceLastConnectionTime', 'hasMalops', 'hasSuspicions', "
                   "'isSuspiciousOrHasSuspiciousProcessOrFile', 'maliciousTools', 'maliciousProcesses', "
                   "'suspiciousProcesses']}",
                   "{'queryPath': [{'requestedType': 'Machine', 'filters': [{'facetName': "
                   "'adDNSHostName', 'filterType': 'NotEquals', 'values': ['dl.delivery.mp.microsoft.com']}, "
                   "{'facetName': 'lastSeenTimeStamp', "
                   "'filterType': 'Between', 'values': [1643109026511, 1643109326511]}], 'isResult': True}],"
                   " 'queryLimits': {'groupingFeature': {'elementInstanceType': "
                   "'Machine', 'featureName': 'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, "
                   "'perGroupLimit': 1, 'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', "
                   "'mountPoints', 'processes', 'services', 'logonSessions', 'hasRemovableDevice', "
                   "'timezoneUTCOffsetMinutes', 'osVersionType', 'platformArchitecture', 'mbrHashString', 'osType', "
                   "'domainFqdn', 'ownerOrganization', 'pylumId', 'adSid', 'adOU', 'adOrganization', "
                   "'adCanonicalName', 'adCompany', 'adDNSHostName', 'adDepartment', 'adDisplayName', 'adLocation', "
                   "'adMachineRole', 'adDescription', 'freeDiskSpace', 'totalDiskSpace', 'freeMemory', 'totalMemory', "
                   "'cpuCount', 'isLaptop', 'deviceModel', 'isActiveProbeConnected', 'uptime', 'isIsolated', "
                   "'lastSeenTimeStamp', 'timeStampSinceLastConnectionTime', 'hasMalops', 'hasSuspicions', "
                   "'isSuspiciousOrHasSuspiciousProcessOrFile', 'maliciousTools', 'maliciousProcesses', "
                   "'suspiciousProcesses']}",
                   "{'queryPath': [{'requestedType': 'User', 'filters': [{'facetName': "
                   "'domain', 'filterType': 'NotEquals', 'values': ['dl.delivery.mp.microsoft.com']}, {'facetName': "
                   "'adCreated', 'filterType': 'Between', 'values': [1643109026511, 1643109326511]}], 'isResult': "
                   "True}], 'queryLimits': {'groupingFeature': {'elementInstanceType': 'User', 'featureName': "
                   "'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, "
                   "'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', 'domain', "
                   "'ownerOrganization.name', 'ownerMachine', 'isLocalSystem', 'isAdmin', 'username', 'emailAddress', "
                   "'numberOfMachines', 'passwordAgeDays', 'privileges', 'comment', 'adCanonicalName', 'adCreated', "
                   "'adDisplayName', 'adLogonName', 'adMail', 'adMemberOf', 'adOU', 'adPrimaryGroupID', "
                   "'adSamAccountName', 'adTitle', 'hasPowerTool', 'hasMaliciousProcess', 'hasSuspicions', "
                   "'hasSuspiciousProcess', 'runningMaliciousProcessEvidence', "
                   "'hasRareProcessWithExternalConnections']}",
                   "{'queryPath': [{'requestedType': 'User', 'filters': [{"
                   "'facetName': 'adAssociatedDomain', 'filterType': 'NotEquals', 'values': ["
                   "'dl.delivery.mp.microsoft.com']}, {'facetName': 'adCreated', "
                   "'filterType': 'Between', 'values': [1643109026511, 1643109326511]}],"
                   " 'isResult': True}], 'queryLimits': {'groupingFeature': {"
                   "'elementInstanceType': 'User', 'featureName': 'elementDisplayName'}}, 'perFeatureLimit': 1, "
                   "'totalResultLimit': 9999, 'perGroupLimit': 1, 'templateContext': 'CUSTOM', 'customFields': ["
                   "'elementDisplayName', 'domain', 'ownerOrganization.name', 'ownerMachine', 'isLocalSystem', "
                   "'isAdmin', 'username', 'emailAddress', 'numberOfMachines', 'passwordAgeDays', 'privileges', "
                   "'comment', 'adCanonicalName', 'adCreated', 'adDisplayName', 'adLogonName', 'adMail', "
                   "'adMemberOf', 'adOU', 'adPrimaryGroupID', 'adSamAccountName', 'adTitle', 'hasPowerTool', "
                   "'hasMaliciousProcess', 'hasSuspicions', 'hasSuspiciousProcess', "
                   "'runningMaliciousProcessEvidence', 'hasRareProcessWithExternalConnections']}"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_creation_with_in_operator_query(self):
        stix_pattern = "[process:created IN ('2020-11-01T08:43:10.003Z') ]"
        query = translation.translate('cybereason', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'queryPath': [{'requestedType': 'Process', 'filters': [{'facetName': 'creationTime', "
                   "'filterType': 'Equals', 'values': [1604220190003]}, {'facetName': 'creationTime', "
                   "'filterType': 'Between', 'values': [1642757566237, 1642757866237]}], 'isResult': True}],"
                   " 'queryLimits': {"
                   "'groupingFeature': {'elementInstanceType': 'Process', 'featureName': 'elementDisplayName'}}, "
                   "'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, 'templateContext': 'CUSTOM', "
                   "'customFields': ['elementDisplayName', 'creationTime', 'endTime', 'commandLine', "
                   "'imageFile.maliciousClassificationType', 'productType', 'children', 'parentProcess', "
                   "'ownerMachine', 'calculatedUser', 'imageFile', 'imageFile.sha1String', 'imageFile.md5String', "
                   "'imageFile.sha256String', 'imageFile.companyName', 'imageFile.productName', 'applicablePid', "
                   "'imageFileExtensionType', 'integrity', 'tid', 'isAggregate', 'isDotNetProtected', 'hasMalops', "
                   "'hasSuspicions', 'relatedToMalop', 'multipleSizeForHashEvidence', 'isImageFileVerified', "
                   "'knownMaliciousToolSuspicion', 'knownMalwareSuspicion', 'knownUnwantedSuspicion', "
                   "'isMaliciousByHashEvidence', 'imageFileMultipleCompanyNamesEvidence', "
                   "'multipleHashForUnsignedPeInfoEvidence', 'multipleNameForHashEvidence', 'unknownEvidence', "
                   "'rareHasPeMismatchEvidence', 'imageFile.signedInternalOrExternal', "
                   "'unknownUnsignedBySigningCompany', 'imageFileUnsignedEvidence', "
                   "'imageFileUnsignedHasSignedVersionEvidence', 'unwantedModuleSuspicion', "
                   "'imageFile.signerInternalOrExternal', 'architecture', 'commandLineContainsTempEvidence', "
                   "'hasChildren', 'hasClassification', 'hasVisibleWindows', 'hasWindows', 'isInstaller', "
                   "'isIdentifiedProduct', 'hasModuleFromTempEvidence', 'nonExecutableExtensionEvidence', "
                   "'isNotShellRunner', 'runningFromTempEvidence', 'shellOfNonShellRunnerSuspicion', "
                   "'shellWithElevatedPrivilegesEvidence', 'systemUserEvidence', 'hasExternalConnection', "
                   "'hasExternalConnectionToWellKnownPortEvidence', 'hasIncomingConnection', 'hasInternalConnection', "
                   "'hasMailConnectionForNonMailProcessEvidence', 'hasListeningConnection', 'hasOutgoingConnection', "
                   "'hasUnresolvedDnsQueriesFromDomain', 'multipleUnresolvedRecordNotExistsEvidence', "
                   "'hasNonDefaultResolverEvidence', 'parentProcessNotMatchHierarchySuspicion', "
                   "'parentProcessNotAdminUserEvidence', 'parentProcessFromRemovableDeviceEvidence', 'autorun', "
                   "'childrenCreatedByThread', 'connections', 'elevatedPrivilegeChildren', 'hackerToolChildren', "
                   "'hostProcess', 'hostUser', 'hostedChildren', 'injectedChildren', 'loadedModules', 'logonSession', "
                   "'remoteSession', 'service', 'execedBy', 'connectionsToMaliciousDomain', "
                   "'connectionsToMalwareAddresses', 'externalConnections', "
                   "'absoluteHighVolumeMaliciousAddressConnections', 'absoluteHighVolumeExternalConnections', "
                   "'incomingConnections', 'incomingExternalConnections', 'incomingInternalConnections', "
                   "'internalConnections', 'listeningConnections', 'localConnections', 'mailConnections', "
                   "'outgoingConnections', 'outgoingExternalConnections', 'outgoingInternalConnections', "
                   "'suspiciousExternalConnections', 'suspiciousInternalConnections', 'wellKnownPortConnections', "
                   "'lowTtlDnsQueries', 'nonDefaultResolverQueries', 'resolvedDnsQueriesDomainToDomain', "
                   "'resolvedDnsQueriesDomainToIp', 'resolvedDnsQueriesIpToDomain', "
                   "'suspiciousDnsQueryDomainToDomain', 'unresolvedQueryFromSuspiciousDomain', "
                   "'dnsQueryFromSuspiciousDomain', 'dnsQueryToSuspiciousDomain', 'unresolvedRecordNotExist', "
                   "'unresolvedDnsQueriesFromDomain', 'unresolvedDnsQueriesFromIp', "
                   "'maliciousToolClassificationModules', 'malwareClassificationModules', 'modulesNotInLoaderDbList', "
                   "'modulesFromTemp', 'unsignedWithSignedVersionModules', 'unwantedClassificationModules', "
                   "'accessToMalwareAddressInfectedProcess', 'connectingToBadReputationAddressSuspicion', "
                   "'hasMaliciousConnectionEvidence', 'hasSuspiciousExternalConnectionSuspicion', "
                   "'highNumberOfExternalConnectionsSuspicion', 'nonDefaultResolverSuspicion', "
                   "'hasRareExternalConnectionEvidence', 'hasRareRemoteAddressEvidence', 'suspiciousMailConnections', "
                   "'accessToMalwareAddressByUnknownProcess', "
                   "'hasAbsoluteHighVolumeConnectionToMaliciousAddressEvidence', "
                   "'hasAbsoluteHighVolumeExternalOutgoingConnectionEvidence', 'highDataTransmittedSuspicion', "
                   "'highDataVolumeTransmittedToMaliciousAddressSuspicion', "
                   "'highDataVolumeTransmittedByUnknownProcess', "
                   "'absoluteHighNumberOfInternalOutgoingEmbryonicConnectionsEvidence', 'dgaSuspicion', "
                   "'hasLowTtlDnsQueryEvidence', 'highUnresolvedToResolvedRateEvidence', "
                   "'manyUnresolvedRecordNotExistsEvidence', 'hasChildKnownHackerToolEvidence', "
                   "'hackingToolOfNonToolRunnerEvidence', 'hackingToolOfNonToolRunnerSuspicion', "
                   "'hasRareChildProcessKnownHackerToolEvidence', 'maliciousToolModuleSuspicion', "
                   "'deletedParentProcessEvidence', 'malwareModuleSuspicion', 'dualExtensionNameEvidence', "
                   "'hiddenFileExtensionEvidence', 'rightToLeftFileExtensionEvidence', "
                   "'screenSaverWithChildrenEvidence', 'suspicionsScreenSaverEvidence', 'hasPeFloatingCodeEvidence', "
                   "'hasSectionMismatchEvidence', 'detectedInjectedEvidence', 'detectedInjectingEvidence', "
                   "'detectedInjectingToProtectedProcessEvidence', 'hasInjectedChildren', "
                   "'hostingInjectedThreadEvidence', 'injectedProtectedProcessEvidence', "
                   "'maliciousInjectingCodeSuspicion', 'injectionMethod', 'isHostingInjectedThread', "
                   "'maliciousInjectedCodeSuspicion', 'maliciousPeExecutionSuspicion', "
                   "'hasSuspiciousInternalConnectionEvidence', 'highInternalOutgoingEmbryonicConnectionRateEvidence', "
                   "'highNumberOfInternalConnectionsEvidence', 'newProcessesAboveThresholdEvidence', "
                   "'hasRareInternalConnectionEvidence', 'elevatingPrivilegesToChildEvidence', "
                   "'parentProcessNotSystemUserEvidence', 'privilegeEscalationEvidence', "
                   "'firstExecutionOfDownloadedProcessEvidence', 'hasAutorun', 'newProcessEvidence', "
                   "'markedForPrevention', 'ransomwareAutoRemediationSuspended', 'totalNumOfInstances', "
                   "'lastMinuteNumOfInstances', 'lastSeenTimeStamp', 'wmiQueryStrings', 'isExectuedByWmi', "
                   "'absoluteHighNumberOfInternalConnectionsEvidence', 'scanningProcessSuspicion', "
                   "'imageFile.isDownloadedFromInternet', 'imageFile.downloadedFromDomain', "
                   "'imageFile.downloadedFromIpAddress', 'imageFile.downloadedFromUrl', "
                   "'imageFile.downloadedFromUrlReferrer', 'imageFile.downloadedFromEmailFrom', "
                   "'imageFile.downloadedFromEmailMessageId', 'imageFile.downloadedFromEmailSubject', 'rpcRequests', "
                   "'iconBase64', 'executionPrevented', 'isWhiteListClassification', 'matchedWhiteListRuleIds']}",
                   "{'queryPath': [{'requestedType': 'DetectionEvents', 'filters': [{'facetName': 'firstSeen', "
                   "'filterType': 'Equals', 'values': [1604220190003]}, {'facetName': 'firstSeen', "
                   "'filterType': 'Between', 'values': [1642757566237, 1642757866237]}], 'isResult': True}],"
                   " 'queryLimits': {"
                   "'groupingFeature': {'elementInstanceType': 'DetectionEvents', 'featureName': "
                   "'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, "
                   "'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', 'detectionEngine', "
                   "'decisionStatus', 'detectionValue', 'firstSeen', 'process', 'user', 'ownerMachine', "
                   "'detectionValueType', 'ownerMachine.isActiveProbeConnected', 'ownerMachine.osVersionType', "
                   "'process.calculatedName', 'process.calculatedUser', 'process.creationTime', 'process.endTime', "
                   "'process.imageFile.maliciousClassificationType']}"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_negate_for_like_operator(self):
        stix_pattern = "[x-cybereason-service:description NOT LIKE 'Windows']"
        query = translation.translate('cybereason', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'queryPath': [{'requestedType': 'Service', 'filters': [{'facetName': 'description', "
                   "'filterType': 'NotContainsIgnoreCase', 'values': ['Windows']}, {'facetName': 'endTime', "
                   "'filterType': 'Between', 'values': [1638778435982, 1638778735982]}], 'isResult': True}], "
                   "'queryLimits': {'groupingFeature': {'elementInstanceType': 'Service', 'featureName': "
                   "'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, "
                   "'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', 'binaryFile', "
                   "'ownerMachine', 'process', 'serviceStartName', 'commandLineArguments', 'description', "
                   "'displayName', 'endTime', 'isActive', 'startType', 'unitFilePath', 'serviceState', "
                   "'serviceSubState', 'isAutoRestartService', 'hasSuspicions', 'newServiceEvidence', "
                   "'rareServiceEvidence', 'serviceType', 'driver']}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_negate_for_greatherthan_or_equals_operator(self):
        stix_pattern = "[network-traffic:dst_port NOT >=22]"
        query = translation.translate('cybereason', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'queryPath': [{'requestedType': 'Connection', 'filters': [{'facetName': 'remotePort', "
                   "'filterType': 'LessThan', 'values': [22]}, {'facetName': 'creationTime', "
                   "'filterType': 'Between', 'values': [1638778810087, 1638779110087]}],"
                   " 'isResult': True}], 'queryLimits': {"
                   "'groupingFeature': {'elementInstanceType': 'Connection', 'featureName': 'elementDisplayName'}}, "
                   "'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, 'templateContext': "
                   "'CUSTOM', 'customFields': ['elementDisplayName', 'direction', 'ownerMachine', 'ownerProcess', "
                   "'serverPort', 'serverAddress', 'portType', 'aggregatedReceivedBytesCount', "
                   "'aggregatedTransmittedBytesCount', 'remoteAddressCountryName', 'dnsQuery', "
                   "'calculatedCreationTime', 'domainName', 'endTime', 'localPort', 'portDescription', 'remotePort', "
                   "'state', 'isExternalConnection', 'isIncoming', 'remoteAddressInternalExternalLocal', "
                   "'transportProtocol', 'hasMalops', 'hasSuspicions', 'relatedToMalop', 'isWellKnownPort', "
                   "'isProcessLegit', 'isProcessMalware', 'localAddress', 'remoteAddress', 'urlDomains']}"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_negate_for_lessthan_operator(self):
        stix_pattern = "[network-traffic:dst_port NOT < 22]"
        query = translation.translate('cybereason', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'queryPath': [{'requestedType': 'Connection', 'filters': [{'facetName': 'remotePort', "
                   "'filterType': 'GreaterOrEqualsTo', 'values': [22]}, {'facetName': 'creationTime', 'filterType': "
                   "'Between', 'values': [1638779059265, 1638779359265]}], 'isResult': True}], 'queryLimits': {"
                   "'groupingFeature': {'elementInstanceType': 'Connection', 'featureName': 'elementDisplayName'}}, "
                   "'perFeatureLimit': 1, 'totalResultLimit': 9999, 'perGroupLimit': 1, 'templateContext': "
                   "'CUSTOM', 'customFields': ['elementDisplayName', 'direction', 'ownerMachine', 'ownerProcess', "
                   "'serverPort', 'serverAddress', 'portType', 'aggregatedReceivedBytesCount', "
                   "'aggregatedTransmittedBytesCount', 'remoteAddressCountryName', 'dnsQuery', "
                   "'calculatedCreationTime', 'domainName', 'endTime', 'localPort', 'portDescription', 'remotePort', "
                   "'state', 'isExternalConnection', 'isIncoming', 'remoteAddressInternalExternalLocal', "
                   "'transportProtocol', 'hasMalops', 'hasSuspicions', 'relatedToMalop', 'isWellKnownPort', "
                   "'isProcessLegit', 'isProcessMalware', 'localAddress', 'remoteAddress', 'urlDomains']}"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_invalid_operator_for_int(self):
        stix_pattern = "[network-traffic:dst_port LIKE '22']"
        result = translation.translate('cybereason', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert 'LIKE OR MATCHES operator is not supported for Integer/Timestamp/Boolean fields' in result['error']

    def test_observation_with_invalid_link_between_element(self):
        stix_pattern = "[x-cybereason-connection:port_type LIKE 'HTTP' AND x-oca-event:file_event_user " \
                       "LIKE 'FET_DELETE']"
        result = translation.translate('cybereason', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert result['code'] == 'translation_error'
        assert 'Cybereason does not allow AND operation' in result['error']

    def test_observation_with_invalid_operator_for_string(self):
        stix_pattern = "[x-cybereason-connection:port_type > 'HTTP']"
        result = translation.translate('cybereason', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert 'operator is not supported for string type input' in result['error']

    def test_invalid_mac_address(self):
        stix_pattern = "[mac-addr:value = '00:00:00']"
        result = translation.translate('cybereason', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert 'Invalid mac address' in result['error']

    def test_invalid_email_address(self):
        stix_pattern = "[email-addr:value = 'Administrator']"
        result = translation.translate('cybereason', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert 'Invalid email address' in result['error']

    def test_timestamp_in_seconds_and_milliseconds(self):
        stix_pattern = "[network-traffic:src_port = 23]START t'2019-10-01T08:00:10Z' STOP t'2019-11-30T11:00:10Z' AND" \
                       "[network-traffic:protocols[*] = 'tcp'] START t'2019-10-01T08:43:10.003Z' STOP " \
                       "t'2019-11-30T10:43:10.005Z' "
        query = translation.translate('cybereason', 'query', '{}', stix_pattern)
        queries = [{
            'queryPath': [{
                'requestedType': 'Connection',
                'filters': [{
                    'facetName': 'localPort',
                    'filterType': 'Equals',
                    'values': [23]
                }, {
                    'facetName': 'creationTime',
                    'filterType': 'Between',
                    'values': [1569916810000, 1575111610000]
                }],
                'isResult': True
            }],
            'queryLimits': {
                'groupingFeature': {
                    'elementInstanceType': 'Connection',
                    'featureName': 'elementDisplayName'
                }
            },
            'perFeatureLimit': 1,
            'totalResultLimit': 9999,
            'perGroupLimit': 1,
            'templateContext': 'CUSTOM',
            'customFields': ['elementDisplayName', 'direction', 'ownerMachine', 'ownerProcess', 'serverPort',
                             'serverAddress', 'portType', 'aggregatedReceivedBytesCount',
                             'aggregatedTransmittedBytesCount', 'remoteAddressCountryName', 'dnsQuery',
                             'calculatedCreationTime', 'domainName', 'endTime', 'localPort', 'portDescription',
                             'remotePort', 'state', 'isExternalConnection', 'isIncoming',
                             'remoteAddressInternalExternalLocal', 'transportProtocol', 'hasMalops', 'hasSuspicions',
                             'relatedToMalop', 'isWellKnownPort', 'isProcessLegit', 'isProcessMalware', 'localAddress',
                             'remoteAddress', 'urlDomains']
        }, {
            'queryPath': [{
                'requestedType': 'Connection',
                'filters': [{
                    'facetName': 'transportProtocol',
                    'filterType': 'Equals',
                    'values': ['tcp']
                }, {
                    'facetName': 'creationTime',
                    'filterType': 'Between',
                    'values': [1569919390003, 1575110590005]
                }],
                'isResult': True
            }],
            'queryLimits': {
                'groupingFeature': {
                    'elementInstanceType': 'Connection',
                    'featureName': 'elementDisplayName'
                }
            },
            'perFeatureLimit': 1,
            'totalResultLimit': 9999,
            'perGroupLimit': 1,
            'templateContext': 'CUSTOM',
            'customFields': ['elementDisplayName', 'direction', 'ownerMachine', 'ownerProcess', 'serverPort',
                             'serverAddress', 'portType', 'aggregatedReceivedBytesCount',
                             'aggregatedTransmittedBytesCount', 'remoteAddressCountryName', 'dnsQuery',
                             'calculatedCreationTime', 'domainName', 'endTime', 'localPort', 'portDescription',
                             'remotePort', 'state', 'isExternalConnection', 'isIncoming',
                             'remoteAddressInternalExternalLocal', 'transportProtocol', 'hasMalops', 'hasSuspicions',
                             'relatedToMalop', 'isWellKnownPort', 'isProcessLegit', 'isProcessMalware', 'localAddress',
                             'remoteAddress', 'urlDomains']
        }]
        self._test_query_assertions(query, queries)

    def test_multiple_observation_with_and_without_linked_element(self):
        stix_pattern = "[ipv4-addr:value = '1.1.1.1' AND  x-cybereason-driver:name =  'test_driver'] " \
                       "OR [AND x-oca-asset:os_type = 'windows' AND x-cybereason-service:description LIKE 'service'  ]"
        query = translation.translate('cybereason', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'queryPath': [{'requestedType': 'Service', 'filters': [{'facetName': 'description', "
                   "'filterType': 'ContainsIgnoreCase', 'values': ['service']}, {'facetName': 'endTime', "
                   "'filterType': 'Between', 'values': [1669871110786, 1669871410786]}], 'connectionFeature': {"
                   "'elementInstanceType': 'Service', 'featureName': 'ownerMachine'}}, {'requestedType': 'Machine', "
                   "'filters': [{'facetName': 'osType', 'filterType': 'Equals', 'values': ['windows']}, {'facetName': "
                   "'lastSeenTimeStamp', 'filterType': 'Between', 'values': [1669871110786, 1669871410786]}], "
                   "'isResult': True}], 'queryLimits': {'groupingFeature': {'elementInstanceType': 'Machine', "
                   "'featureName': 'elementDisplayName'}}, 'perFeatureLimit': 1, 'totalResultLimit': 9999, "
                   "'perGroupLimit': 1, 'templateContext': 'CUSTOM', 'customFields': ['elementDisplayName', "
                   "'mountPoints', 'processes', 'services', 'logonSessions', 'hasRemovableDevice', "
                   "'timezoneUTCOffsetMinutes', 'osVersionType', 'platformArchitecture', 'mbrHashString', 'osType', "
                   "'domainFqdn', 'ownerOrganization', 'pylumId', 'adSid', 'adOU', 'adOrganization', "
                   "'adCanonicalName', 'adCompany', 'adDNSHostName', 'adDepartment', 'adDisplayName', 'adLocation', "
                   "'adMachineRole', 'adDescription', 'freeDiskSpace', 'totalDiskSpace', 'freeMemory', 'totalMemory', "
                   "'cpuCount', 'isLaptop', 'deviceModel', 'isActiveProbeConnected', 'uptime', 'isIsolated', "
                   "'lastSeenTimeStamp', 'timeStampSinceLastConnectionTime', 'hasMalops', 'hasSuspicions', "
                   "'isSuspiciousOrHasSuspiciousProcessOrFile', 'maliciousTools', 'maliciousProcesses', "
                   "'suspiciousProcesses']}"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)
