import unittest
from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_modules.cybereason.entry_point import EntryPoint
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers

MODULE = "cybereason"
entry_point = EntryPoint()
map_data = entry_point.get_results_translator().map_data
data_source = {
    "type": "identity",
    "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
    "name": "cybereason",
    "identity_class": "events"
}
options = {}


class TestCybereasonResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for cybereason translate results
    """

    @staticmethod
    def get_first(itr, constraint):
        """
        return the obj in the itr if constraint is true
        """
        return next(
            (obj for obj in itr if constraint(obj)),
            None
        )

    @staticmethod
    def get_first_of_type(itr, typ):
        """
        to check whether the object belongs to respective stix object
        """
        return TestCybereasonResultsToStix.get_first(itr,
                                                     lambda o: isinstance(o, dict) and o.get('type') == typ)

    def test_common_prop(self):
        """to test common stix object properties"""

        data = {'Connection': {'direction': 'OUTGOING',
                               'remoteAddressInternalExternalLocal': 'EXTERNAL',
                               'serverAddress': '104.65.180.39',
                               'localPort': '61247',
                               'portType': 'SERVICE_HTTP',
                               'aggregatedTransmittedBytesCount': '1735',
                               'calculatedCreationTime': '1616688833056',
                               'remoteAddressCountryName': 'United States',
                               'isIncoming': 'false',
                               'isExternalConnection': 'true',
                               'state': 'CONNECTION_OPEN',
                               'hasSuspicions': 'false',
                               'serverPort': '443',
                               'isWellKnownPort': 'true',
                               'remotePort': '443',
                               'hasMalops': 'false',
                               'isProcessMalware': 'false',
                               'relatedToMalop': 'true',
                               'isProcessLegit': 'true',
                               'endTime': '1616689733224',
                               'transportProtocol': 'TCP',
                               'portDescription': 'Hypertext Transfer Protocol \
                                                   over TLS/SSL (HTTPS)',
                               'aggregatedReceivedBytesCount': '13013',
                               'elementDisplayName': '192.168.87.11:61247 > 104.65.180.39:443',
                               'localAddress': '192.168.87.11',
                               'domainName': 'disc801.prod.do.dsp.mp.microsoft.com',
                               'remoteAddress': '104.65.180.39',
                               'ownerMachine': 'd3test4',
                               'ownerProcess': 'svchost.exe',
                               'dnsQuery': 'disc801.prod.do.dsp.mp.microsoft.com > 104.65.180.39'
                               }}
        result_bundle = json_to_stix_translator.convert_to_stix(data_source, map_data, [data],
                                                                get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert observed_data is not None
        assert observed_data['id'] is not None
        assert observed_data['type'] == "observed-data"
        assert observed_data['created_by_ref'] == result_bundle_identity['id']
        assert observed_data['first_observed'] is not None
        assert observed_data['last_observed'] is not None
        assert observed_data['number_observed'] is not None

    def test_process_json_to_stix(self):
        """  to test process stix object properties  """
        data = {'Process': {'elementDisplayName': 'svchost.exe',
                            'imageFile.sha1String': '75c5a97f521f760e32a4a9639a653eed862e9c61',
                            'imageFile.sha256String': 'dd191a5b23df92e12a8852291f9fb\
                                                       5ed594b76a28a5a464418442584afd1e048',
                            'commandLine': 'C:\\WINDOWS\\System32\\svchost.exe -k NetworkServi\
                                            ce -p',
                            'imageFile.md5String': '27992d7ebe51aec655a088de88bad5c9',
                            'creationTime': '1596848617500',
                            'endTime': '1597955913267',
                            'imageFile': 'svchost.exe',
                            'parentProcess': 'services.exe',
                            'calculatedUser': '',
                            'imageFile.companyName': 'Microsoft Corporation',
                            'imageFile.productName': 'Microsoft\\u00ae Windows\\u00ae \
                                                      Operating System',
                            'imageFileExtensionType': 'EXECUTABLE_WINDOWS',
                            'integrity': 'yes',
                            'tid': 123,
                            'applicablePid': 456,
                            'isAggregate': False,
                            'isDotNetProtected': False,
                            'hasMalops': True,
                            'hasSuspicions': True,
                            'relatedToMalop': True,
                            'multipleSizeForHashEvidence': '',
                            'isImageFileVerified': True,
                            'knownMaliciousToolSuspicion': '',
                            'knownMalwareSuspicion': '',
                            'knownUnwantedSuspicion': '',
                            'isMaliciousByHashEvidence': '',
                            'imageFileMultipleCompanyNamesEvidence': '',
                            'multipleHashForUnsignedPeInfoEvidence': '',
                            'multipleNameForHashEvidence': '',
                            'unknownEvidence': '',
                            'rareHasPeMismatchEvidence': '',
                            'imageFile.signedInternalOrExternal': True,
                            'unknownUnsignedBySigningCompany': '',
                            'imageFileUnsignedEvidence': '',
                            'imageFileUnsignedHasSignedVersionEvidence': '',
                            'unwantedModuleSuspicion': '',
                            'imageFile.signerInternalOrExternal': 'Microsoft Windows',
                            'architecture': 'x64',
                            'commandLineContainsTempEvidence': '',
                            'hasChildren': False,
                            'hasClassification': False,
                            'hasVisibleWindows': '',
                            'hasWindows': True,
                            'isInstaller': False,
                            'isIdentifiedProduct': True,
                            'hasModuleFromTempEvidence': '',
                            'nonExecutableExtensionEvidence': '',
                            'isNotShellRunner': False,
                            'runningFromTempEvidence': '',
                            'shellOfNonShellRunnerSuspicion': '',
                            'shellWithElevatedPrivilegesEvidence': '',
                            'systemUserEvidence': '',
                            'hasExternalConnection': True,
                            'hasExternalConnectionToWellKnownPortEvidence': False,
                            'hasIncomingConnection': False,
                            'hasInternalConnection': False,
                            'hasMailConnectionForNonMailProcessEvidence': False,
                            'hasListeningConnection': False,
                            'hasOutgoingConnection': True,
                            'hasUnresolvedDnsQueriesFromDomain': True,
                            'multipleUnresolvedRecordNotExistsEvidence': '',
                            'hasNonDefaultResolverEvidence': '',
                            'parentProcessNotMatchHierarchySuspicion': '',
                            'parentProcessNotAdminUserEvidence': '',
                            'parentProcessFromRemovableDeviceEvidence': '',
                            'autorun': '',
                            'childrenCreatedByThread': '',
                            'connections': '',
                            'elevatedPrivilegeChildren': '',
                            'hackerToolChildren': '',
                            'hostProcess': '',
                            'hostUser': '',
                            'hostedChildren': '',
                            'injectedChildren': '',
                            'loadedModules': '',
                            'logonSession': 'cyb7-1510 > cyb7-1510',
                            'remoteSession': '',
                            'service': 'Delivery Optimization',
                            'execedBy': '',
                            'connectionsToMaliciousDomain': '',
                            'connectionsToMalwareAddresses': '',
                            'externalConnections': '',
                            'absoluteHighVolumeMaliciousAddressConnections': '',
                            'absoluteHighVolumeExternalConnections': '',
                            'incomingConnections': '',
                            'incomingExternalConnections': '',
                            'incomingInternalConnections': '',
                            'internalConnections': '',
                            'listeningConnections': '',
                            'localConnections': '',
                            'mailConnections': '',
                            'outgoingConnections': '',
                            'outgoingExternalConnections': '',
                            'outgoingInternalConnections': '',
                            'suspiciousExternalConnections': '',
                            'suspiciousInternalConnections': '',
                            'wellKnownPortConnections': '',
                            'lowTtlDnsQueries': '',
                            'nonDefaultResolverQueries': '',
                            'resolvedDnsQueriesDomainToDomain': '',
                            'resolvedDnsQueriesDomainToIp': '',
                            'resolvedDnsQueriesIpToDomain': '',
                            'suspiciousDnsQueryDomainToDomain': '',
                            'unresolvedQueryFromSuspiciousDomain': '',
                            'dnsQueryFromSuspiciousDomain': '',
                            'dnsQueryToSuspiciousDomain': '',
                            'unresolvedRecordNotExist': '',
                            'unresolvedDnsQueriesFromDomain': '',
                            'unresolvedDnsQueriesFromIp': '',
                            'maliciousToolClassificationModules': '',
                            'malwareClassificationModules': '',
                            'modulesNotInLoaderDbList': '',
                            'modulesFromTemp': '',
                            'unsignedWithSignedVersionModules': '',
                            'unwantedClassificationModules': '',
                            'accessToMalwareAddressInfectedProcess': '',
                            'connectingToBadReputationAddressSuspicion': '',
                            'hasMaliciousConnectionEvidence': '',
                            'hasSuspiciousExternalConnectionSuspicion': '',
                            'highNumberOfExternalConnectionsSuspicion': '',
                            'nonDefaultResolverSuspicion': '',
                            'hasRareExternalConnectionEvidence': '',
                            'hasRareRemoteAddressEvidence': '',
                            'suspiciousMailConnections': '',
                            'accessToMalwareAddressByUnknownProcess': '',
                            'hasAbsoluteHighVolumeConnectionToMaliciousAddressEvidence': '',
                            'hasAbsoluteHighVolumeExternalOutgoingConnectionEvidence': '',
                            'highDataTransmittedSuspicion': '',
                            'highDataVolumeTransmittedToMaliciousAddressSuspicion': '',
                            'highDataVolumeTransmittedByUnknownProcess': '',
                            'absoluteHighNumberOfInternalOutgoingEmbryonicConnectionsEvidence': '',
                            'dgaSuspicion': '',
                            'hasLowTtlDnsQueryEvidence': '',
                            'highUnresolvedToResolvedRateEvidence': '',
                            'manyUnresolvedRecordNotExistsEvidence': '',
                            'hasChildKnownHackerToolEvidence': '',
                            'hackingToolOfNonToolRunnerEvidence': '',
                            'hackingToolOfNonToolRunnerSuspicion': '',
                            'hasRareChildProcessKnownHackerToolEvidence': '',
                            'maliciousToolModuleSuspicion': '',
                            'deletedParentProcessEvidence': '',
                            'malwareModuleSuspicion': '',
                            'dualExtensionNameEvidence': '',
                            'hiddenFileExtensionEvidence': '',
                            'rightToLeftFileExtensionEvidence': '',
                            'screenSaverWithChildrenEvidence': '',
                            'suspicionsScreenSaverEvidence': '',
                            'hasPeFloatingCodeEvidence': '',
                            'hasSectionMismatchEvidence': '',
                            'detectedInjectedEvidence': '',
                            'detectedInjectingToProtectedProcessEvidence': '',
                            'hasInjectedChildren': '',
                            'hostingInjectedThreadEvidence': '',
                            'injectedProtectedProcessEvidence': '',
                            'maliciousInjectingCodeSuspicion': '',
                            'injectionMethod': '',
                            'isHostingInjectedThread': '',
                            'maliciousInjectedCodeSuspicion': '',
                            'maliciousPeExecutionSuspicion': '',
                            'hasSuspiciousInternalConnectionEvidence': '',
                            'highInternalOutgoingEmbryonicConnectionRateEvidence': '',
                            'highNumberOfInternalConnectionsEvidence': '',
                            'newProcessesAboveThresholdEvidence': '',
                            'hasRareInternalConnectionEvidence': '',
                            'elevatingPrivilegesToChildEvidence': '',
                            'parentProcessNotSystemUserEvidence': '',
                            'privilegeEscalationEvidence': '',
                            'firstExecutionOfDownloadedProcessEvidence': '',
                            'hasAutorun': '',
                            'newProcessEvidence': '',
                            'markedForPrevention': '',
                            'ransomwareAutoRemediationSuspended': '',
                            'totalNumOfInstances': '',
                            'lastMinuteNumOfInstances': '',
                            'lastSeenTimeStamp': '',
                            'wmiQueryStrings': '',
                            'isExectuedByWmi': True,
                            'absoluteHighNumberOfInternalConnectionsEvidence': '',
                            'scanningProcessSuspicion': '',
                            'imageFile.isDownloadedFromInternet': '',
                            'imageFile.downloadedFromDomain': '',
                            'imageFile.downloadedFromIpAddress': '',
                            'imageFile.downloadedFromUrl': '',
                            'imageFile.downloadedFromUrlReferrer': '',
                            'imageFile.downloadedFromEmailFrom': '',
                            'imageFile.downloadedFromEmailMessageId': '',
                            'imageFile.downloadedFromEmailSubject': '',
                            'rpcRequests': '',
                            'iconBase64': '',
                            'executionPrevented': '',
                            'isWhiteListClassification': '',
                            'matchedWhiteListRuleIds': ''
                            }}

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        process_obj = TestCybereasonResultsToStix.get_first_of_type(objects.values(), 'process')

        assert process_obj is not None
        assert process_obj.keys() == {'type', 'name', 'binary_ref', 'command_line',
                                      'created', 'parent_ref',
                                      'extensions', 'pid'}
        assert process_obj['type'] == 'process'
        assert process_obj['name'] == 'svchost.exe'
        assert process_obj['pid'] == 456
        assert process_obj['command_line'] == 'C:\\WINDOWS\\System32\\svchost.exe -k NetworkServi\
                                            ce -p'
        assert process_obj['created'] == '2020-08-08T01:03:37.500Z'
        assert process_obj['binary_ref'] == '0'

    def test_user_account_json_to_stix(self):
        """to test user-account stix object properties"""

        data = {'User': {'domain': 'd3cyber-win10-9',
                         'isLocalSystem': False,
                         'isAdmin': True,
                         'ownerOrganization.name': 'INTEGRATION',
                         'ownerMachine': 'hy01-yak',
                         'ActionType': '',
                         'username': 'administrator',
                         'numberOfMachines': 1,
                         'passwordAgeDays': 0,
                         'privileges': 'Admin',
                         'comment': 'Built-in account for administering the compute',
                         'adCanonicalName': 'pearson.net/SPECTER/Devin M',
                         'adCreated': '',
                         'adDisplayName': 'Admin',
                         'adLogonName': 'Admin',
                         'adMemberOf': '',
                         'adPrimaryGroupID': '',
                         'adSamAccountName': '',
                         'adTitle': '',
                         'hasPowerTool': True,
                         'hasMaliciousProcess': True,
                         'hasSuspicions': True,
                         'hasSuspiciousProcess': True,
                         'hasRareProcessWithExternalConnections': True}}

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        user_obj = TestCybereasonResultsToStix.get_first_of_type(objects.values(), 'user-account')
        assert user_obj is not None
        assert user_obj['type'] == 'user-account'
        assert user_obj['user_id'] == 'administrator'

    def test_user_account_json_to_stix_negative(self):
        """to test user-account stix object properties negative"""

        data = {'User': {'domain': 'd3cyber-win10-9',
                         'isLocalSystem': False,
                         'isAdmin': True,
                         'ownerOrganization.name': 'INTEGRATION',
                         'ownerMachine': 'hy01-yak',
                         'ActionType': '',
                         'username': 'administrator',
                         'numberOfMachines': 1,
                         'passwordAgeDays': 0,
                         'privileges': 'Admin',
                         'comment': 'Built-in account for administering the compute',
                         'adCanonicalName': 'pearson.net/SPECTER/Devin M',
                         'adCreated': '',
                         'adDisplayName': 'Admin',
                         'adLogonName': 'Admin',
                         'adMemberOf': '',
                         'adPrimaryGroupID': '',
                         'adSamAccountName': '',
                         'adTitle': '',
                         'hasPowerTool': True,
                         'hasMaliciousProcess': True,
                         'hasSuspicions': True,
                         'hasSuspiciousProcess': True,
                         'hasRareProcessWithExternalConnections': True}}

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        user_obj = TestCybereasonResultsToStix.get_first_of_type(objects.values(), 'file')
        assert user_obj is None

    def test_network_traffic_json_to_stix(self):
        """to test network-traffic stix object properties"""

        data = {'Connection': {'direction': 'OUTGOING',
                               'remoteAddressInternalExternalLocal': 'EXTERNAL',
                               'serverAddress': '104.65.180.39',
                               'localPort': '61247',
                               'portType': 'SERVICE_HTTP',
                               'aggregatedTransmittedBytesCount': '1735',
                               'calculatedCreationTime': '1616688833056',
                               'remoteAddressCountryName': 'United States',
                               'isIncoming': 'false',
                               'isExternalConnection': 'true',
                               'state': 'CONNECTION_OPEN',
                               'hasSuspicions': 'false',
                               'serverPort': '443',
                               'isWellKnownPort': 'true',
                               'remotePort': '443',
                               'hasMalops': 'false',
                               'isProcessMalware': 'false',
                               'relatedToMalop': 'true',
                               'isProcessLegit': 'true',
                               'endTime': '1616689733224',
                               'transportProtocol': 'TCP',
                               'portDescription': 'Hypertext Transfer Protocol \
                                                   over TLS/SSL (HTTPS)',
                               'aggregatedReceivedBytesCount': '13013',
                               'elementDisplayName': '192.168.87.11:61247 > 104.65.180.39:443',
                               'localAddress': '192.168.87.11',
                               'domainName': 'disc801.prod.do.dsp.mp.microsoft.com',
                               'remoteAddress': '104.65.180.39',
                               'ownerMachine': 'd3test4',
                               'ownerProcess': 'svchost.exe',
                               'dnsQuery': 'disc801.prod.do.dsp.mp.microsoft.com > 104.65.180.39'
                               }}

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        connection_obj = TestCybereasonResultsToStix.get_first_of_type(objects.values(),
                                                                       'network-traffic')
        assert connection_obj is not None
        assert connection_obj["type"] == 'network-traffic'
        assert connection_obj["src_port"] == 61247
        assert connection_obj['src_ref'] == '3'
        assert 'tcp' in connection_obj["protocols"]
        assert connection_obj["dst_port"] == 443
        assert connection_obj['dst_ref'] == '5'
        assert connection_obj["start"] == '2021-03-25T16:13:53.056Z'

    def test_file_json_to_stix(self):
        """to test File stix object properties"""

        data = {'File': {'elementDisplayName': 'sbsimulation_sb_265540_bs_254977.exe',
                         'sha1String': '75c5a97f521f760e32a4a9639a653eed862e9c61',
                         'md5String': '27992d7ebe51aec655a088de88bad5c9',
                         'sha256String': 'dd191a5b23df92e12a8852291f9fb\
                                                5ed594b76a28a5a464418442584afd1e048',
                         'createdTime': '1596848617500',
                         'modifiedTime': '1597955913267',
                         'size': 14346778,
                         'correctedPath': '',
                         'maliciousClassificationType': '',
                         'fileDescription': '',
                         'fileVersion': '1.0.0.0 (win7sp1_rtm.101119-1850)',
                         'productName': 'SafeBreach Endpoint Simulator',
                         'originalFileName': 'sbsimulation.exe',
                         'productVersion': '1.0.0000.00000',
                         'signedInternalOrExternal': '443',
                         'hasSuspicions': False,
                         'hasMalops': False,
                         'extensionType': 'Windows Executable',
                         'isPEFile': 'true',
                         'legalCopyright': 'SafeBreach LTD. All rights reserved',
                         'signatureVerifiedInternalOrExternal': 'Internal',
                         'companyName': 'SafeBreach LTD',
                         'avRemediationStatus': '',
                         'signerInternalOrExternal': 'External',
                         'autoruns': False,
                         'ownerMachine': 'disc801.prod.do.dsp.mp.microsoft.com',
                         'mount': 'c:',
                         'autorun': False,
                         'dualExtensionEvidence': '',
                         'hiddenFileExtensionEvidence': '',
                         'rightToLeftFileExtensionEvidence': '',
                         'hackingToolClassificationEvidence': '',
                         'classificationLink': '',
                         'executedByProcessEvidence': '',
                         'hasAutorun': True,
                         'isInstallerProperties': '',
                         'isFromRemovableDevice': '',
                         'productType': 'Not specific',
                         'secondExtensionType': '',
                         'temporaryFolderEvidence': '',
                         'multipleCompanyNamesEvidence': '',
                         'multipleHashForUnsignedPeInfoEvidence': '',
                         'unsignedHasSignedVersionEvidence': '',
                         'classificationComment': '',
                         'classificationBlocking': '',
                         'isDownloadedFromInternet': '',
                         'downloadedFromDomain': '',
                         'downloadedFromIpAddress': '',
                         'downloadedFromUrl': '',
                         'downloadedFromUrlReferrer': '',
                         'downloadedFromEmailFrom': '',
                         'downloadedFromEmailMessageId': '',
                         'downloadedFromEmailSubject': '',
                         'legalTrademarks': '',
                         'privateBuild': '',
                         'specialBuild': '',
                         'internalName': 'sbsimulation',
                         'comments': '',
                         'applicationIdentifier': ''
                         }}

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        file_obj = TestCybereasonResultsToStix.get_first_of_type(objects.values(), 'file')
        assert file_obj is not None
        assert file_obj['type'] == 'file'
        assert file_obj['name'] == 'sbsimulation_sb_265540_bs_254977.exe'
        assert file_obj['size'] == 14346778

    def test_registry_event_json_to_stix(self):
        """to test x-windows-registry-value-type custom object properties"""

        data = {'RegistryEvent': {'registryDataType': 'REG_DATATYPE_SZ',
                                  'registryOperationType': 'REG_MODIFY',
                                  'firstTime': '1596848617500',
                                  'timestamp': '1597955913267',
                                  'detectionTimesNumber': 11,
                                  'registryProcess': 'msiexec.exe',
                                  'registryEntry': 'hku\\s-1-5-21-1055018377-3212914418-3318\
                                                    909653-1001\\software\\microsoft\\windows\\currentver\
                                                    sion\\run\\geipupdater',
                                  'data': 'C:\\Program Files (x86)\\Proficy\\GEIPUpdaterInstaller\\GEIPUpdater.exe'
                                          ' --hide',
                                  'ownerMachine': 'hy01-yak'
                                  }
                }

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        registryevent_obj = TestCybereasonResultsToStix.get_first_of_type(
            objects.values(), 'x-windows-registry-value-type')
        assert registryevent_obj is not None
        assert registryevent_obj['type'] == 'x-windows-registry-value-type'
        assert registryevent_obj['data_type'] == 'REG_DATATYPE_SZ'
        assert registryevent_obj[
                   'data'] == 'C:\\Program Files (x86)\\Proficy\\GEIPUpdaterInstaller\\' \
                              'GEIPUpdater.exe --hide'

    def test_detection_events_json_to_stix(self):
        """to test x-oca-event object properties"""

        data = {'DetectionEvents': {'process': 'svchost.exe',
                                    'user': 'administrator',
                                    'process.creationTime': '1596848617500',
                                    'detectionEngine': 'Anti-Virus detected known malware',
                                    'decisionStatus': '',
                                    'detectionValue': 'Application.Lazagne.G',
                                    'firstSeen': '1596848617500',
                                    'ownerMachine': 'cyb10-110',
                                    'detectionValueType': 'Disinfected',
                                    'ownerMachine.isActiveProbeConnected': False,
                                    'ownerMachine.osVersionType': 'Windows 10',
                                    'process.calculatedName': '',
                                    'process.calculatedUser': '',
                                    'process.endTime': '',
                                    'process.imageFile.maliciousClassificationType': ''
                                    }}

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        detectionevent_obj = TestCybereasonResultsToStix.get_first_of_type(objects.values(),
                                                                           'x-oca-event')
        assert detectionevent_obj is not None
        assert detectionevent_obj['type'] == 'x-oca-event'
        assert detectionevent_obj['detection_value'] == 'Application.Lazagne.G'
        assert detectionevent_obj['detection_value_type'] == 'Disinfected'
        assert detectionevent_obj['engine'] == 'Anti-Virus detected known malware'

    def test_driver_json_to_stix(self):
        """to test x-cybereason-driver custom object properties"""

        data = {'Driver': {'file': 'tcpipreg.sys',
                           'creationTime': '1596848617500',
                           'elementDisplayName': 'tcpipreg.sys',
                           'ownerMachine': 'w10unprovisioned',
                           'service': '',
                           'endTime': '1616689733224',
                           'newDriverEvidence': 'No data',
                           'hasSuspicions': False
                           }}

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        driver_obj = TestCybereasonResultsToStix.get_first_of_type(objects.values(),
                                                                   'x-cybereason-driver')
        assert driver_obj is not None

        assert driver_obj['type'] == 'x-cybereason-driver'
        assert driver_obj['name'] == 'tcpipreg.sys'
        assert driver_obj['machine'] == 'w10unprovisioned'

    def test_machine_json_to_stix(self):
        """
        to test x-oca-asset custom object properties
        """
        data = {'Machine': {'elementDisplayName': 'w7-cbr-se2',
                            'mountPoints': '/run/snapd/ns/lxd.mnt',
                            'processes': 'powershell.exe',
                            'services': 'CaptureService_8ea4e',
                            'logonSessions': 'dc02 > dc02',
                            'hasRemovableDevice': False,
                            'timezoneUTCOffsetMinutes': '-420',
                            'osVersionType': 'Windows_7',
                            'platformArchitecture': 'ARCH_AMD64',
                            'mbrHashString': 'd81028da16f1d3e26ab10bedfc4747271443a4fa',
                            'osType': 'WINDOWS',
                            'domainFqdn': '',
                            'ownerOrganization': 'INTEGRATION',
                            'pylumId': 'PYLUMCLIENT_INTEGRATION_W7-CBR-SE2_02004C4F4F50',
                            'adSid': 'S-1-5-21-925260173-1387230621-1164276501-2222',
                            'adOU': '',
                            'adOrganization': '',
                            'adCanonicalName': 'cyberrange.attackiq.com/Computers/W7-CBR-SE2',
                            'adCompany': '',
                            'adDNSHostName': 'W7-CBR-SE2.cyberrange.attackiq.com',
                            'adDepartment': '',
                            'adDisplayName': '',
                            'adLocation': '',
                            'adMachineRole': '',
                            'adDescription': '',
                            'freeDiskSpace': '6839951360',
                            'totalDiskSpace': '34252779520',
                            'freeMemory': '2238136320',
                            'totalMemory': '4294561792',
                            'cpuCount': '2',
                            'isLaptop': False,
                            'deviceModel': '',
                            'isActiveProbeConnected': False,
                            'uptime': '16018880314',
                            'isIsolated': True,
                            'lastSeenTimeStamp': '1620506979024',
                            'timeStampSinceLastConnectionTime': '17415140810',
                            'hasMalops': False,
                            'hasSuspicions': False,
                            'isSuspiciousOrHasSuspiciousProcessOrFile': True,
                            'maliciousTools': '',
                            'maliciousProcesses': '',
                            'suspiciousProcesses': ''
                            }}

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        machine_obj = TestCybereasonResultsToStix.get_first_of_type(objects.values(),
                                                                    'x-oca-asset')
        assert machine_obj is not None
        assert machine_obj['type'] == 'x-oca-asset'
        assert machine_obj['name'] == 'w7-cbr-se2'
        assert machine_obj['processes'] == 'powershell.exe'
        assert machine_obj['services'] == 'CaptureService_8ea4e'

    def test_LogonSession_json_to_stix(self):
        """
        to test x-cybereason-logonsession custom object properties
        """
        data = {'LogonSession': {'elementDisplayName': 'w10-cbr-se2 > w10-cbr-se2',
                                 'processes': 'powershell.exe',
                                 'ownerMachine': 'w10-cbr-se2',
                                 'user': 'w10-cbr-se2\\system',
                                 'remoteMachine': 'w10-cbr-se2',
                                 'logonType': 'SLT_UknownSecurityLogonType',
                                 'creationTime': '1604334664819',
                                 'lastSeenTime': '1604334664822',
                                 'logonApplication': 'w10-cbr-se2',
                                 'hasSuspicions': False,
                                 'sourceIp': '192.168.87.72',
                                 'endTime': '1604334664828'
                                 }}

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        logon_session = TestCybereasonResultsToStix.get_first_of_type(objects.values(),
                                                                      'x-cybereason-logonsession')
        assert logon_session is not None
        assert logon_session.keys() == {'type', 'name', 'processes', 'owner_machine', 'remote_machine', 'logon_type',
                                        'creation_time', 'last_seen', 'application', 'end_time'}
        assert logon_session['type'] == 'x-cybereason-logonsession'
        assert logon_session['owner_machine'] == 'w10-cbr-se2'
        assert logon_session['remote_machine'] == 'w10-cbr-se2'
        assert logon_session['processes'] == 'powershell.exe'
        assert logon_session['creation_time'] == '2020-11-02T16:31:04.819Z'
        assert logon_session['logon_type'] == 'SLT_UknownSecurityLogonType'
        assert logon_session['application'] == 'w10-cbr-se2'

    def test_url_json_to_stix(self):
        """
        to test url stix object properties
        """
        data = {'Proxy': {'elementDisplayName': 'w7-cbr-se2',
                          'discoveryType': '',
                          'host': 't-ring.msedge.net',
                          'ipAddress': '172.22.32.1',
                          'pacUrl': 'c1.rfihub.net',
                          'port': '9443'
                          }}

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        proxy_obj = TestCybereasonResultsToStix.get_first_of_type(objects.values(),
                                                                  'url')
        assert proxy_obj is not None
        assert proxy_obj.keys() == {'type', 'value'}
        assert proxy_obj['type'] == 'url'
        assert proxy_obj['value'] == 'c1.rfihub.net'

    def test_windows_registry_key_json_to_stix(self):
        """
        to test windows_registry_key stix object properties
        """
        data = {'Autorun': {
            'elementDisplayName': 'hklm\\software\\microsoft\\windows nt\\currentversion\\'
                                  'winlogon\\gpextensions\\{'
                                  '3610eda5-77ef-11d2-8dc5-00c04fa31a66}\\dllname,',
            'value': '%SystemRoot%\\System32\\dskquota.dll',
            'dependInFile': False,
            'ownerMachine': 'bcybdw8888w10e0',
            'isPointingToTemp': False,
            'registryEntry': True,
            'endTime': '1618236837535'
        }
        }

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        autorun_obj = TestCybereasonResultsToStix.get_first_of_type(objects.values(),
                                                                    'windows-registry-key')
        assert autorun_obj is not None
        assert autorun_obj.keys() == {'type', 'key', 'extensions'}

        assert autorun_obj['type'] == 'windows-registry-key'
        assert autorun_obj['key'] == 'HKEY_LOCAL_MACHINE\\software\\microsoft\\windows nt\\' \
                                     'currentversion\\winlogon\\gpextensions\\{' \
                                     '3610eda5-77ef-11d2-8dc5-00c04fa31a66}\\dllname,'

    def test_service_json_to_stix(self):
        """
        to test x-cybereason-service custom object properties
        """
        data = {'Service': {'elementDisplayName': 'CaptureService_8ea4e',
                            'binaryFile': 'svchost.exe',
                            'ownerMachine': 'wb-qa-test-sw',
                            'process': 'amsvc.exe',
                            'serviceStartName': 'Windows Push Notifications User Service_2d02eb',
                            'commandLineArguments': '-k LocalService -p',
                            'description': 'Enables optional screen capture functionality \
                                            for applications that call the \
                                            Windows.Graphics.Capture API.',
                            'displayName': 'CaptureService_8ea4e',
                            'endTime': '1618236837535',
                            'isActive': False,
                            'startType': 'SERVICE_START_TYPE_DEMAND_START',
                            'unitFilePath': 'c:\\windows\\system32\\svchost.exe',
                            'serviceState': 'Activate',
                            'serviceSubState': 'Active',
                            'isAutoRestartService': False,
                            'hasSuspicions': False,
                            'newServiceEvidence': True,
                            'rareServiceEvidence': True,
                            'serviceType': 'Device',
                            'driver': 'tcpipreg.sys'
                            }
                }

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        service_obj = TestCybereasonResultsToStix.get_first_of_type(objects.values(),
                                                                    'x-cybereason-service')
        assert service_obj is not None
        assert service_obj['type'] == 'x-cybereason-service'
        assert service_obj['machine'] == 'wb-qa-test-sw'
        assert service_obj['start_type'] == 'SERVICE_START_TYPE_DEMAND_START'


    def test_macaddress_json_to_stix(self):
        """
        to test mac-address stix object properties
        """
        data = {'NetworkInterface': {'elementDisplayName': 'vEthernet (HyAdp608666d7)',
                                     'ipAddress': '172.22.32.1',
                                     'ownerMachine': 'desktop-8hcom22',
                                     'gateway': '10.10.1.255',
                                     'dnsServer': '10.255.0.17',
                                     'dhcpServer': '172.16.8.1',
                                     'macAddressFormat': '00:15:5D:96:00:01',
                                     'id': '{0927C898-664F-43D8-AA64-609C892799C3}',
                                     'proxies': ''
                                     }
                }

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        network_interface_obj = TestCybereasonResultsToStix.get_first_of_type(objects.values(),
                                                                              'mac-addr')

        assert network_interface_obj is not None
        assert network_interface_obj.keys() == {'type', 'value'}
        assert network_interface_obj['type'] == 'mac-addr'
        assert network_interface_obj['value'] == '00:15:5D:96:00:01'

    def test_directory_json_to_stix(self):
        """
        to test directory stix object properties
        """
        data = {'FileAccessEvent': {
            'elementDisplayName': 'amsvc.exe c:\\programdata\\apv2\\amworkspace\\tmp000001d8\\tmp0001a70f',
            'ownerProcess': 'amsvc.exe',
            'ownerMachine': 'win10-jzhang-49',
            'fileInfo': '',
            'path': 'c:\\programdata\\apv2\\amworkspace\\tmp000001d8\\tmp0001a70f',
            'fileEventType': 'FET_CREATE',
            'firstAccessTime': '1638180234064',
            'newPath': 'c:\\programdata\\apv2\\amworkspace\\tmp000001d8\\tmp0001a70f',
            'isHidden': False
        }
        }

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        file_access_event_obj = TestCybereasonResultsToStix.get_first_of_type(
            objects.values(), 'directory')
        assert file_access_event_obj is not None
        assert file_access_event_obj.keys() == {'type', 'path'}
        assert file_access_event_obj['type'] == 'directory'
        assert file_access_event_obj['path'] == 'c:\\programdata\\apv2\\amworkspace\\tmp000001d8'
