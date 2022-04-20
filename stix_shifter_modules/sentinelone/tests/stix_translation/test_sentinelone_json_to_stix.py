import unittest
from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_modules.sentinelone.entry_point import EntryPoint
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers

MODULE = "sentinelone"
entry_point = EntryPoint()
map_data = entry_point.get_results_translator().map_data
data_source = {
    "type": "identity",
    "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
    "name": "sentinelone",
    "identity_class": "events"
}
options = {}

common_data = {"activeContentFileId": None,
               "activeContentHash": None,
               "activeContentPath": None,
               "activeContentSignedStatus": None,
               "activeContentType": None,
               "agentDomain": "WORKGROUP",
               "agentGroupId": "1336793312883045044",
               "agentId": "1337419724165944028",
               "agentInfected": False,
               "agentIp": "54.91.158.243",
               "agentIsActive": False,
               "agentIsDecommissioned": False,
               "agentMachineType": "server",
               "agentName": "EC2AMAZ-IQFSLIL",
               "agentNetworkStatus": "connected",
               "agentOs": "windows",
               "agentTimestamp": "2022-01-24T18:49:35.296Z",
               "agentUuid": "f5875d2abd9f4198824885126b4f4d07",
               "agentVersion": "21.6.6.1200",
               "childProcCount": "28",
               "connectionStatus": "SUCCESS",
               "containerId": None,
               "containerImage": None,
               "containerLabels": None,
               "containerName": None,
               "createdAt": "2022-01-24T18:49:35.296000Z",
               "crossProcCount": "0",
               "crossProcDupRemoteProcHandleCount": "0",
               "crossProcDupThreadHandleCount": "0",
               "crossProcOpenProcCount": "0",
               "crossProcOutOfStorylineCount": "0",
               "crossProcThreadCreateCount": "0",
               "srcProcRpid": None,
               "rpid": None,
               "tid": None,
               "verifiedStatus": "verified"
               }

class TestSentineloneResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for sentinelone translate results
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
        return TestSentineloneResultsToStix.get_first(itr,
                                                      lambda o: isinstance(o, dict) and
                                                                o.get('type') == typ)

    def test_common_prop(self):
        """to test common stix object properties"""

        result_data = {}
        result_data = common_data

        data = {"direction": "INCOMING",
                "dnsCount": "0",
                "dstIp": "172.31.31.67",
                "dstPort": 3389,
                "endpointMachineType": "server",
                "endpointName": "EC2AMAZ-IQFSLIL",
                "endpointOs": "windows",
                "eventIndex": "15",
                "eventTime": "2022-01-24T18:49:35.296Z",
                "eventType": "IP Connect",
                "fileIsExecutable": "True",
                "fileMd5": "8a0a29438052faed8a2532da50455756",
                "fileSha256": "7fd065bac18c5278777ae44908101cdfed72d26fa741367f0ad4d02020787ab6",
                "id": "649568400931684352",
                "metaEventName": "TCPV4",
                "moduleCount": "541721",
                "netConnCount": "180525",
                "netConnInCount": "180525",
                "netConnOutCount": "0",
                "netConnStatus": "SUCCESS",
                "netEventDirection": "INCOMING",
                "netProtocolName": "ms-wbt-server",
                "objectType": "ip",
                "parentPid": "868",
                "parentProcessName": "services.exe",
                "parentProcessStartTime": "2022-01-20T07:03:11.124Z",
                "parentProcessUniqueKey": "0E1224C52E1F3667",
                "pid": "1188",
                "processCmd": "C:\\Windows\\System32\\svchost.exe -k termsvcs -s TermService",
                "processDisplayName": "Host Process for Windows Services",
                "processGroupId": "B9913CE1424F6FB2",
                "processImagePath": "C:\\Windows\\system32\\svchost.exe",
                "processImageSha1Hash": "a1385ce20ad79f55df235effd9780c31442aa234",
                "processIntegrityLevel": "SYSTEM",
                "processIsRedirectedCommandProcessor": "False",
                "processIsWow64": "False",
                "processName": "svchost.exe",
                "processRoot": "True",
                "processSessionId": "0",
                "processStartTime": "2022-01-20T07:03:12.554Z",
                "processSubSystem": "SYS_WIN32",
                "processUniqueKey": "0E1224C52E1F3667",
                "publisher": "MICROSOFT WINDOWS PUBLISHER",
                "registryChangeCount": "0",
                "relatedToThreat": "False",
                "signatureSignedInvalidReason": None,
                "signedStatus": "signed",
                "siteId": "1336793312849490611",
                "siteName": "Default site",
                "srcIp": "87.251.64.138",
                "srcPort": 3428,
                "srcProcActiveContentFileId": None,
                "srcProcActiveContentHash": None,
                "srcProcActiveContentPath": None,
                "srcProcActiveContentSignedStatus": None,
                "srcProcActiveContentType": None,
                "srcProcBinaryisExecutable": "True",
                "srcProcCmdLine": "C:\\Windows\\System32\\svchost.exe -k termsvcs -s TermService",
                "srcProcDisplayName": "Host Process for Windows Services",
                "srcProcImageMd5": "8a0a29438052faed8a2532da50455756",
                "srcProcImagePath": "C:\\Windows\\system32\\svchost.exe",
                "srcProcImageSha1": "a1385ce20ad79f55df235effd9780c31442aa234",
                "srcProcImageSha256": "7fd065bac18c5278777ae44908101cdfed72d26f"
                                      "a741367f0ad4d02020787ab6",
                "srcProcIntegrityLevel": "SYSTEM",
                "srcProcIsNative64Bit": "False",
                "srcProcIsRedirectCmdProcessor": "False",
                "srcProcIsStorylineRoot": "True",
                "srcProcName": "svchost.exe",
                "srcProcParentActiveContentFileId": None,
                "srcProcParentActiveContentHash": None,
                "srcProcParentActiveContentPath": None,
                "srcProcParentActiveContentSignedStatus": None,
                "srcProcParentActiveContentType": None,
                "srcProcParentCmdLine": "C:\\Windows\\system32\\services.exe",
                "srcProcParentDisplayName": "Services and Controller app",
                "srcProcParentImageMd5": "94f2383da5fa7b9717d03e33cdee5c81",
                "srcProcParentImagePath": "C:\\Windows\\system32\\services.exe",
                "srcProcParentImageSha1": "106a001c4c9820a6aec6a8ba17d3836525faf80e",
                "srcProcParentImageSha256": "7ef551eb51992b5f0f3c76fcf1996bca5ca8ef"
                                            "aa87ab527f55835936165f420d",
                "srcProcParentIntegrityLevel": "SYSTEM",
                "srcProcParentIsNative64Bit": "False",
                "srcProcParentIsRedirectCmdProcessor": "False",
                "srcProcParentIsStorylineRoot": "True",
                "srcProcParentName": "services.exe",
                "srcProcParentPid": "868",
                "srcProcParentProcUid": "4B8DD1628A27EDE6",
                "srcProcParentPublisher": "MICROSOFT WINDOWS PUBLISHER",
                "srcProcParentReasonSignatureInvalid": None,
                "srcProcParentSessionId": "0",
                "srcProcParentSignedStatus": "signed",
                "srcProcParentStartTime": "2022-01-20T07:03:11.124Z",
                "srcProcParentStorylineId": "13D130A04AF01959",
                "srcProcParentUid": "4B8DD1628A27EDE6",
                "srcProcParentUser": "NT AUTHORITY\\SYSTEM",
                "srcProcPid": "1188",
                "srcProcPublisher": "MICROSOFT WINDOWS PUBLISHER",
                "srcProcReasonSignatureInvalid": None,
                "srcProcRelatedToThreat": "False",
                "srcProcSessionId": "0",
                "srcProcSignedStatus": "signed",
                "srcProcStartTime": "2022-01-20T07:03:12.554Z",
                "srcProcStorylineId": "B9913CE1424F6FB2",
                "srcProcSubsystem": "SYS_WIN32",
                "srcProcTid": None,
                "srcProcUid": "0E1224C52E1F3667",
                "srcProcUser": "NT AUTHORITY\\NETWORK SERVICE",
                "srcProcVerifiedStatus": "verified",
                "storyline": "B9913CE1424F6FB2",
                "tgtFileCreationCount": "0",
                "tgtFileDeletionCount": "0",
                "tgtFileModificationCount": "0",
                "tiindicatorRelatedEventTime": None,
                "traceId": "01FT6PSXBV4SKNZ2TVW7D7TE8G",
                "trueContext": "B9913CE1424F6FB2",
                "user": "NT AUTHORITY\\NETWORK SERVICE"
                }

        result_data.update(data)

        result_bundle = json_to_stix_translator.convert_to_stix(data_source, map_data, [result_data],
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
        result_data = {}
        result_data = common_data
        data = {"direction": "INCOMING",
                "dnsCount": "0",
                "dstIp": "172.31.31.67",
                "dstPort": 3389,
                "endpointMachineType": "server",
                "endpointName": "EC2AMAZ-IQFSLIL",
                "endpointOs": "windows",
                "eventIndex": "15",
                "eventTime": "2022-01-24T18:49:35.296Z",
                "eventType": "IP Connect",
                "fileIsExecutable": "True",
                "fileMd5": "8a0a29438052faed8a2532da50455756",
                "fileSha256": "7fd065bac18c5278777ae44908101cdfed72d26fa741367f0ad4d02020787ab6",
                "id": "649568400931684352",
                "metaEventName": "TCPV4",
                "moduleCount": "541721",
                "netConnCount": "180525",
                "netConnInCount": "180525",
                "netConnOutCount": "0",
                "netConnStatus": "SUCCESS",
                "netEventDirection": "INCOMING",
                "netProtocolName": "ms-wbt-server",
                "objectType": "ip",
                "parentPid": "868",
                "parentProcessName": "services.exe",
                "parentProcessStartTime": "2022-01-20T07:03:11.124Z",
                "parentProcessUniqueKey": "0E1224C52E1F3667",
                "pid": "1188",
                "processCmd": "C:\\Windows\\System32\\svchost.exe -k termsvcs -s TermService",
                "processDisplayName": "Host Process for Windows Services",
                "processGroupId": "B9913CE1424F6FB2",
                "processImagePath": "C:\\Windows\\system32\\svchost.exe",
                "processImageSha1Hash": "a1385ce20ad79f55df235effd9780c31442aa234",
                "processIntegrityLevel": "SYSTEM",
                "processIsRedirectedCommandProcessor": "False",
                "processIsWow64": "False",
                "processName": "svchost.exe",
                "processRoot": "True",
                "processSessionId": "0",
                "processStartTime": "2022-01-20T07:03:12.554Z",
                "processSubSystem": "SYS_WIN32",
                "processUniqueKey": "0E1224C52E1F3667",
                "publisher": "MICROSOFT WINDOWS PUBLISHER",
                "registryChangeCount": "0",
                "relatedToThreat": "False",
                "signatureSignedInvalidReason": None,
                "signedStatus": "signed",
                "siteId": "1336793312849490611",
                "siteName": "Default site",
                "srcIp": "87.251.64.138",
                "srcPort": 3428,
                "srcProcActiveContentFileId": None,
                "srcProcActiveContentHash": None,
                "srcProcActiveContentPath": None,
                "srcProcActiveContentSignedStatus": None,
                "srcProcActiveContentType": None,
                "srcProcBinaryisExecutable": "True",
                "srcProcCmdLine": "C:\\Windows\\System32\\svchost.exe -k termsvcs -s TermService",
                "srcProcDisplayName": "Host Process for Windows Services",
                "srcProcImageMd5": "8a0a29438052faed8a2532da50455756",
                "srcProcImagePath": "C:\\Windows\\system32\\svchost.exe",
                "srcProcImageSha1": "a1385ce20ad79f55df235effd9780c31442aa234",
                "srcProcImageSha256": "7fd065bac18c5278777ae44908101cdfed72"
                                      "d26fa741367f0ad4d02020787ab6",
                "srcProcIntegrityLevel": "SYSTEM",
                "srcProcIsNative64Bit": "False",
                "srcProcIsRedirectCmdProcessor": "False",
                "srcProcIsStorylineRoot": "True",
                "srcProcName": "svchost.exe",
                "srcProcParentActiveContentFileId": None,
                "srcProcParentActiveContentHash": None,
                "srcProcParentActiveContentPath": None,
                "srcProcParentActiveContentSignedStatus": None,
                "srcProcParentActiveContentType": None,
                "srcProcParentCmdLine": "C:\\Windows\\system32\\services.exe",
                "srcProcParentDisplayName": "Services and Controller app",
                "srcProcParentImageMd5": "94f2383da5fa7b9717d03e33cdee5c81",
                "srcProcParentImagePath": "C:\\Windows\\system32\\services.exe",
                "srcProcParentImageSha1": "106a001c4c9820a6aec6a8ba17d3836525faf80e",
                "srcProcParentImageSha256": "7ef551eb51992b5f0f3c76fcf1996bca5ca"
                                            "8efaa87ab527f55835936165f420d",
                "srcProcParentIntegrityLevel": "SYSTEM",
                "srcProcParentIsNative64Bit": "False",
                "srcProcParentIsRedirectCmdProcessor": "False",
                "srcProcParentIsStorylineRoot": "True",
                "srcProcParentName": "services.exe",
                "srcProcParentPid": "868",
                "srcProcParentProcUid": "4B8DD1628A27EDE6",
                "srcProcParentPublisher": "MICROSOFT WINDOWS PUBLISHER",
                "srcProcParentReasonSignatureInvalid": None,
                "srcProcParentSessionId": "0",
                "srcProcParentSignedStatus": "signed",
                "srcProcParentStartTime": "2022-01-20T07:03:11.124Z",
                "srcProcParentStorylineId": "13D130A04AF01959",
                "srcProcParentUid": "4B8DD1628A27EDE6",
                "srcProcParentUser": "NT AUTHORITY\\SYSTEM",
                "srcProcPid": "1188",
                "srcProcPublisher": "MICROSOFT WINDOWS PUBLISHER",
                "srcProcReasonSignatureInvalid": None,
                "srcProcRelatedToThreat": "False",
                "srcProcSessionId": "0",
                "srcProcSignedStatus": "signed",
                "srcProcStartTime": "2022-01-20T07:03:12.554Z",
                "srcProcStorylineId": "B9913CE1424F6FB2",
                "srcProcSubsystem": "SYS_WIN32",
                "srcProcTid": None,
                "srcProcUid": "0E1224C52E1F3667",
                "srcProcUser": "NT AUTHORITY\\NETWORK SERVICE",
                "srcProcVerifiedStatus": "verified",
                "storyline": "B9913CE1424F6FB2",
                "tgtFileCreationCount": "0",
                "tgtFileDeletionCount": "0",
                "tgtFileModificationCount": "0",
                "tiindicatorRelatedEventTime": None,
                "traceId": "01FT6PSXBV4SKNZ2TVW7D7TE8G",
                "trueContext": "B9913CE1424F6FB2",
                "user": "NT AUTHORITY\\NETWORK SERVICE"
                }

        result_data.update(data)

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [result_data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        process_obj = TestSentineloneResultsToStix.get_first_of_type(objects.values(), 'process')

        assert process_obj is not None
        assert process_obj['type'] == 'process'
        assert process_obj['name'] == 'svchost.exe'
        assert process_obj['pid'] == 1188
        assert process_obj['command_line'] == 'C:\\Windows\\System32\\svchost.exe -k term' \
                                              'svcs -s TermService'
        assert process_obj['created'] == '2022-01-20T07:03:12.554Z'
        assert process_obj['parent_ref']  is not None

    def test_user_account_json_to_stix(self):
        """to test user-account stix object properties"""
        result_data = {}
        result_data = common_data
        data = {"direction": "INCOMING",
                "dnsCount": "0",
                "dstIp": "172.31.31.67",
                "dstPort": 3389,
                "endpointMachineType": "server",
                "endpointName": "EC2AMAZ-IQFSLIL",
                "endpointOs": "windows",
                "eventIndex": "15",
                "eventTime": "2022-01-24T18:49:35.296Z",
                "eventType": "IP Connect",
                "fileIsExecutable": "True",
                "fileMd5": "8a0a29438052faed8a2532da50455756",
                "fileSha256": "7fd065bac18c5278777ae44908101cdfed72d26f"
                              "a741367f0ad4d02020787ab6",
                "id": "649568400931684352",
                "metaEventName": "TCPV4",
                "moduleCount": "541721",
                "netConnCount": "180525",
                "netConnInCount": "180525",
                "netConnOutCount": "0",
                "netConnStatus": "SUCCESS",
                "netEventDirection": "INCOMING",
                "netProtocolName": "ms-wbt-server",
                "objectType": "ip",
                "parentPid": "868",
                "parentProcessName": "services.exe",
                "parentProcessStartTime": "2022-01-20T07:03:11.124Z",
                "parentProcessUniqueKey": "0E1224C52E1F3667",
                "pid": "1188",
                "processCmd": "C:\\Windows\\System32\\svchost.exe -k termsvcs -s TermService",
                "processDisplayName": "Host Process for Windows Services",
                "processGroupId": "B9913CE1424F6FB2",
                "processImagePath": "C:\\Windows\\system32\\svchost.exe",
                "processImageSha1Hash": "a1385ce20ad79f55df235effd9780c31442aa234",
                "processIntegrityLevel": "SYSTEM",
                "processIsRedirectedCommandProcessor": "False",
                "processIsWow64": "False",
                "processName": "svchost.exe",
                "processRoot": "True",
                "processSessionId": "0",
                "processStartTime": "2022-01-20T07:03:12.554Z",
                "processSubSystem": "SYS_WIN32",
                "processUniqueKey": "0E1224C52E1F3667",
                "publisher": "MICROSOFT WINDOWS PUBLISHER",
                "registryChangeCount": "0",
                "relatedToThreat": "False",
                "signatureSignedInvalidReason": None,
                "signedStatus": "signed",
                "siteId": "1336793312849490611",
                "siteName": "Default site",
                "srcIp": "87.251.64.138",
                "srcPort": 3428,
                "srcProcActiveContentFileId": None,
                "srcProcActiveContentHash": None,
                "srcProcActiveContentPath": None,
                "srcProcActiveContentSignedStatus": None,
                "srcProcActiveContentType": None,
                "srcProcBinaryisExecutable": "True",
                "srcProcCmdLine": "C:\\Windows\\System32\\svchost.exe -k termsvcs -s TermService",
                "srcProcDisplayName": "Host Process for Windows Services",
                "srcProcImageMd5": "8a0a29438052faed8a2532da50455756",
                "srcProcImagePath": "C:\\Windows\\system32\\svchost.exe",
                "srcProcImageSha1": "a1385ce20ad79f55df235effd9780c31442aa234",
                "srcProcImageSha256": "7fd065bac18c5278777ae44908101cdfed72d"
                                      "26fa741367f0ad4d02020787ab6",
                "srcProcIntegrityLevel": "SYSTEM",
                "srcProcIsNative64Bit": "False",
                "srcProcIsRedirectCmdProcessor": "False",
                "srcProcIsStorylineRoot": "True",
                "srcProcName": "svchost.exe",
                "srcProcParentActiveContentFileId": None,
                "srcProcParentActiveContentHash": None,
                "srcProcParentActiveContentPath": None,
                "srcProcParentActiveContentSignedStatus": None,
                "srcProcParentActiveContentType": None,
                "srcProcParentCmdLine": "C:\\Windows\\system32\\services.exe",
                "srcProcParentDisplayName": "Services and Controller app",
                "srcProcParentImageMd5": "94f2383da5fa7b9717d03e33cdee5c81",
                "srcProcParentImagePath": "C:\\Windows\\system32\\services.exe",
                "srcProcParentImageSha1": "106a001c4c9820a6aec6a8ba17d3836525faf80e",
                "srcProcParentImageSha256": "7ef551eb51992b5f0f3c76fcf1996bca5c"
                                            "a8efaa87ab527f55835936165f420d",
                "srcProcParentIntegrityLevel": "SYSTEM",
                "srcProcParentIsNative64Bit": "False",
                "srcProcParentIsRedirectCmdProcessor": "False",
                "srcProcParentIsStorylineRoot": "True",
                "srcProcParentName": "services.exe",
                "srcProcParentPid": "868",
                "srcProcParentProcUid": "4B8DD1628A27EDE6",
                "srcProcParentPublisher": "MICROSOFT WINDOWS PUBLISHER",
                "srcProcParentReasonSignatureInvalid": None,
                "srcProcParentSessionId": "0",
                "srcProcParentSignedStatus": "signed",
                "srcProcParentStartTime": "2022-01-20T07:03:11.124Z",
                "srcProcParentStorylineId": "13D130A04AF01959",
                "srcProcParentUid": "4B8DD1628A27EDE6",
                "srcProcParentUser": "NT AUTHORITY\\SYSTEM",
                "srcProcPid": "1188",
                "srcProcPublisher": "MICROSOFT WINDOWS PUBLISHER",
                "srcProcReasonSignatureInvalid": None,
                "srcProcRelatedToThreat": "False",
                "srcProcSessionId": "0",
                "srcProcSignedStatus": "signed",
                "srcProcStartTime": "2022-01-20T07:03:12.554Z",
                "srcProcStorylineId": "B9913CE1424F6FB2",
                "srcProcSubsystem": "SYS_WIN32",
                "srcProcTid": None,
                "srcProcUid": "0E1224C52E1F3667",
                "srcProcUser": "NT AUTHORITY\\NETWORK SERVICE",
                "srcProcVerifiedStatus": "verified",
                "storyline": "B9913CE1424F6FB2",
                "tgtFileCreationCount": "0",
                "tgtFileDeletionCount": "0",
                "tgtFileModificationCount": "0",
                "tiindicatorRelatedEventTime": None,
                "traceId": "01FT6PSXBV4SKNZ2TVW7D7TE8G",
                "trueContext": "B9913CE1424F6FB2",
                "user": "NT AUTHORITY\\NETWORK SERVICE"
                }

        result_data.update(data)
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [result_data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        user_obj = TestSentineloneResultsToStix.get_first_of_type(objects.values(), 'user-account')
        assert user_obj is not None
        assert user_obj['type'] == 'user-account'
        assert user_obj['user_id'] == 'NT AUTHORITY\\NETWORK SERVICE'

    def test_network_traffic_json_to_stix(self):
        """to test network-traffic stix object properties"""
        result_data = {}
        result_data = common_data
        data = {"direction": "INCOMING",
                "dnsCount": "0",
                "dstIp": "172.31.31.67",
                "dstPort": 3389,
                "endpointMachineType": "server",
                "endpointName": "EC2AMAZ-IQFSLIL",
                "endpointOs": "windows",
                "eventIndex": "15",
                "eventTime": "2022-01-24T18:49:35.296Z",
                "eventType": "IP Connect",
                "fileIsExecutable": "True",
                "fileMd5": "8a0a29438052faed8a2532da50455756",
                "fileSha256": "7fd065bac18c5278777ae44908101cdfed72d2"
                              "6fa741367f0ad4d02020787ab6",
                "id": "649568400931684352",
                "metaEventName": "TCPV4",
                "moduleCount": "541721",
                "netConnCount": "180525",
                "netConnInCount": "180525",
                "netConnOutCount": "0",
                "netConnStatus": "SUCCESS",
                "netEventDirection": "INCOMING",
                "netProtocolName": "ms-wbt-server",
                "objectType": "ip",
                "parentPid": "868",
                "parentProcessName": "services.exe",
                "parentProcessStartTime": "2022-01-20T07:03:11.124Z",
                "parentProcessUniqueKey": "0E1224C52E1F3667",
                "pid": "1188",
                "processCmd": "C:\\Windows\\System32\\svchost.exe -k termsvcs -s TermService",
                "processDisplayName": "Host Process for Windows Services",
                "processGroupId": "B9913CE1424F6FB2",
                "processImagePath": "C:\\Windows\\system32\\svchost.exe",
                "processImageSha1Hash": "a1385ce20ad79f55df235effd9780c31442aa234",
                "processIntegrityLevel": "SYSTEM",
                "processIsRedirectedCommandProcessor": "False",
                "processIsWow64": "False",
                "processName": "svchost.exe",
                "processRoot": "True",
                "processSessionId": "0",
                "processStartTime": "2022-01-20T07:03:12.554Z",
                "processSubSystem": "SYS_WIN32",
                "processUniqueKey": "0E1224C52E1F3667",
                "publisher": "MICROSOFT WINDOWS PUBLISHER",
                "registryChangeCount": "0",
                "relatedToThreat": "False",
                "signatureSignedInvalidReason": None,
                "signedStatus": "signed",
                "siteId": "1336793312849490611",
                "siteName": "Default site",
                "srcIp": "87.251.64.138",
                "srcPort": 3428,
                "srcProcActiveContentFileId": None,
                "srcProcActiveContentHash": None,
                "srcProcActiveContentPath": None,
                "srcProcActiveContentSignedStatus": None,
                "srcProcActiveContentType": None,
                "srcProcBinaryisExecutable": "True",
                "srcProcCmdLine": "C:\\Windows\\System32\\svchost.exe -k termsvcs -s TermService",
                "srcProcDisplayName": "Host Process for Windows Services",
                "srcProcImageMd5": "8a0a29438052faed8a2532da50455756",
                "srcProcImagePath": "C:\\Windows\\system32\\svchost.exe",
                "srcProcImageSha1": "a1385ce20ad79f55df235effd9780c31442aa234",
                "srcProcImageSha256": "7fd065bac18c5278777ae44908101cdfed72"
                                      "d26fa741367f0ad4d02020787ab6",
                "srcProcIntegrityLevel": "SYSTEM",
                "srcProcIsNative64Bit": "False",
                "srcProcIsRedirectCmdProcessor": "False",
                "srcProcIsStorylineRoot": "True",
                "srcProcName": "svchost.exe",
                "srcProcParentActiveContentFileId": None,
                "srcProcParentActiveContentHash": None,
                "srcProcParentActiveContentPath": None,
                "srcProcParentActiveContentSignedStatus": None,
                "srcProcParentActiveContentType": None,
                "srcProcParentCmdLine": "C:\\Windows\\system32\\services.exe",
                "srcProcParentDisplayName": "Services and Controller app",
                "srcProcParentImageMd5": "94f2383da5fa7b9717d03e33cdee5c81",
                "srcProcParentImagePath": "C:\\Windows\\system32\\services.exe",
                "srcProcParentImageSha1": "106a001c4c9820a6aec6a8ba17d3836525faf80e",
                "srcProcParentImageSha256": "7ef551eb51992b5f0f3c76fcf1996bca5"
                                            "ca8efaa87ab527f55835936165f420d",
                "srcProcParentIntegrityLevel": "SYSTEM",
                "srcProcParentIsNative64Bit": "False",
                "srcProcParentIsRedirectCmdProcessor": "False",
                "srcProcParentIsStorylineRoot": "True",
                "srcProcParentName": "services.exe",
                "srcProcParentPid": "868",
                "srcProcParentProcUid": "4B8DD1628A27EDE6",
                "srcProcParentPublisher": "MICROSOFT WINDOWS PUBLISHER",
                "srcProcParentReasonSignatureInvalid": None,
                "srcProcParentSessionId": "0",
                "srcProcParentSignedStatus": "signed",
                "srcProcParentStartTime": "2022-01-20T07:03:11.124Z",
                "srcProcParentStorylineId": "13D130A04AF01959",
                "srcProcParentUid": "4B8DD1628A27EDE6",
                "srcProcParentUser": "NT AUTHORITY\\SYSTEM",
                "srcProcPid": "1188",
                "srcProcPublisher": "MICROSOFT WINDOWS PUBLISHER",
                "srcProcReasonSignatureInvalid": None,
                "srcProcRelatedToThreat": "False",
                "srcProcSessionId": "0",
                "srcProcSignedStatus": "signed",
                "srcProcStartTime": "2022-01-20T07:03:12.554Z",
                "srcProcStorylineId": "B9913CE1424F6FB2",
                "srcProcSubsystem": "SYS_WIN32",
                "srcProcTid": None,
                "srcProcUid": "0E1224C52E1F3667",
                "srcProcUser": "NT AUTHORITY\\NETWORK SERVICE",
                "srcProcVerifiedStatus": "verified",
                "storyline": "B9913CE1424F6FB2",
                "tgtFileCreationCount": "0",
                "tgtFileDeletionCount": "0",
                "tgtFileModificationCount": "0",
                "tiindicatorRelatedEventTime": None,
                "traceId": "01FT6PSXBV4SKNZ2TVW7D7TE8G",
                "trueContext": "B9913CE1424F6FB2",
                "user": "NT AUTHORITY\\NETWORK SERVICE"
                }

        result_data.update(data)
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [result_data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        network_traffic = TestSentineloneResultsToStix.get_first_of_type(objects.values(),
                                                                         'network-traffic')
        assert network_traffic is not None
        assert network_traffic["type"] == 'network-traffic'
        assert network_traffic["src_port"] == 3428
        assert network_traffic['src_ref'] == '4'
        assert 'ms-wbt-server' in network_traffic["protocols"]
        assert network_traffic["dst_port"] == 3389
        assert network_traffic['dst_ref'] == '2'

    def test_file_json_to_stix(self):
        """to test File stix object properties"""
        result_data = {}
        result_data = common_data
        data = {"dnsCount": None,
                "endpointMachineType": "server",
                "endpointName": "EC2AMAZ-Q2H45ST",
                "endpointOs": "windows",
                "eventIndex": "132",
                "eventTime": "2022-02-18T11:10:31.024Z",
                "eventType": "File Modification",
                "fileCreatedAt": "2022-02-18T11:10:31.024Z",
                "fileFullName": "C:\\Users\\Administrator\\AppData\\Local\\Microsoft\\Internet "
                                "Explorer\\Recovery\\High\\Last Active\\Recov"
                                "eryStore.{61E7D981-90AB-11EC-8361-0A65F81405B1}.dat",
                "fileId": "4DFAF8097B0FBB80",
                "fileIsExecutable": None,
                "fileLocation": None,
                "fileMd5": None,
                "fileModifyAt": "2022-02-18T11:10:31.024Z",
                "fileSha1": "fdd4f36fa5f6315f50852736d9635f077ddf4c22",
                "fileSha256": None,
                "fileSize": "4608",
                "fileType": None,
                "id": "658257929423945763",
                "indicatorBootConfigurationUpdateCount": None,
                "metaEventName": "FILEMODIFICATION",
                "moduleCount": None,
                "netConnCount": None,
                "netConnInCount": None,
                "netConnOutCount": None,
                "newFileName": None,
                "objectType": "file",
                "oldFileMd5": None,
                "oldFileName": None,
                "oldFileSha1": None,
                "oldFileSha256": None,
                "parentPid": None,
                "parentProcessName": "explorer.exe",
                "parentProcessStartTime": "2022-02-18T09:38:15.202Z",
                "parentProcessUniqueKey": "2846952F099AFE85",
                "pid": "3368",
                "processCmd": "\"C:\\Program Files\\internet explorer\\iexplore.exe\"",
                "processDisplayName": None,
                "processGroupId": "56B10F8DB8885000",
                "processImagePath": "C:\\Program Files\\internet explorer\\iexplore.exe",
                "processImageSha1Hash": "714169f0ac0e08673528d9c3bc12ca0d03235e9c",
                "processIntegrityLevel": "HIGH",
                "processIsRedirectedCommandProcessor": None,
                "processIsWow64": None,
                "processName": "iexplore.exe",
                "processRoot": None,
                "processSessionId": None,
                "processStartTime": "2022-02-18T09:45:53.204Z",
                "processSubSystem": None,
                "processUniqueKey": "2846952F099AFE85",
                "publisher": "MICROSOFT CORPORATION",
                "registryChangeCount": None,
                "relatedToThreat": "False",
                "signatureSignedInvalidReason": None,
                "signedStatus": "signed",
                "siteId": "1336793312849490611",
                "siteName": "Default site",
                "srcProcActiveContentFileId": None,
                "srcProcActiveContentHash": None,
                "srcProcActiveContentPath": None,
                "srcProcActiveContentSignedStatus": None,
                "srcProcActiveContentType": None,
                "srcProcBinaryisExecutable": None,
                "srcProcCmdLine": "\"C:\\Program Files\\internet explorer\\iexplore.exe\"",
                "srcProcDisplayName": None,
                "srcProcImageMd5": None,
                "srcProcImagePath": "C:\\Program Files\\internet explorer\\iexplore.exe",
                "srcProcImageSha1": "714169f0ac0e08673528d9c3bc12ca0d03235e9c",
                "srcProcImageSha256": None,
                "srcProcIntegrityLevel": "HIGH",
                "srcProcIsNative64Bit": None,
                "srcProcIsRedirectCmdProcessor": None,
                "srcProcIsStorylineRoot": None,
                "srcProcName": "iexplore.exe",
                "srcProcParentActiveContentFileId": None,
                "srcProcParentActiveContentHash": None,
                "srcProcParentActiveContentPath": None,
                "srcProcParentActiveContentSignedStatus": None,
                "srcProcParentActiveContentType": None,
                "srcProcParentCmdLine": None,
                "srcProcParentDisplayName": None,
                "srcProcParentImageMd5": None,
                "srcProcParentImagePath": "C:\\Windows\\explorer.exe",
                "srcProcParentImageSha1": "7caf46864357e582c8a8acca3d62791f456e12a7",
                "srcProcParentImageSha256": None,
                "srcProcParentIntegrityLevel": None,
                "srcProcParentIsNative64Bit": None,
                "srcProcParentIsRedirectCmdProcessor": None,
                "srcProcParentIsStorylineRoot": None,
                "srcProcParentName": "explorer.exe",
                "srcProcParentPid": None,
                "srcProcParentProcUid": "0349A99A9CA02EAD",
                "srcProcParentPublisher": None,
                "srcProcParentReasonSignatureInvalid": None,
                "srcProcParentSessionId": None,
                "srcProcParentSignedStatus": None,
                "srcProcParentStartTime": "2022-02-18T09:38:15.202Z",
                "srcProcParentStorylineId": None,
                "srcProcParentUid": "0349A99A9CA02EAD",
                "srcProcParentUser": None,
                "srcProcPid": "3368",
                "srcProcPublisher": "MICROSOFT CORPORATION",
                "srcProcReasonSignatureInvalid": None,
                "srcProcRelatedToThreat": "False",
                "srcProcSessionId": None,
                "srcProcSignedStatus": "signed",
                "srcProcStartTime": "2022-02-18T09:45:53.204Z",
                "srcProcStorylineId": "56B10F8DB8885000",
                "srcProcSubsystem": None,
                "srcProcTid": None,
                "srcProcUid": "2846952F099AFE85",
                "srcProcUser": "EC2AMAZ-Q2H45ST\\Administrator",
                "srcProcVerifiedStatus": "verified",
                "storyline": "56B10F8DB8885000",
                "tgtFileConvictedBy": None,
                "tgtFileCreatedAt": "2022-02-18T11:10:30.991Z",
                "tgtFileCreationCount": None,
                "tgtFileDeletionCount": None,
                "tgtFileDescription": None,
                "tgtFileExtension": None,
                "tgtFileId": "4DFAF8097B0FBB80",
                "tgtFileInternalName": None,
                "tgtFileIsExecutable": None,
                "tgtFileIsSigned": None,
                "tgtFileLocation": None,
                "tgtFileMd5": None,
                "tgtFileModificationCount": None,
                "tgtFileModifiedAt": "2022-02-18T11:10:30.991Z",
                "tgtFileOldMd5": None,
                "tgtFileOldPath": None,
                "tgtFileOldSha1": None,
                "tgtFileOldSha256": None,
                "tgtFilePath": "C:\\Users\\Administrator\\AppData\\Local\\Microsoft\\Internet "
                               "Explorer\\Recovery\\High\\Last "
                               "Active\\RecoveryStore.{61E7D981-90AB-11EC-8361-0A65F81405B1}.dat",
                "tgtFileSha1": "fdd4f36fa5f6315f50852736d9635f077ddf4c22",
                "tgtFileSha256": None,
                "tgtFileSize": "4608",
                "tgtFileType": None,
                "tiindicatorRelatedEventTime": None,
                "traceId": "01FW68DKMPDY5VJHEG7F60EJEG",
                "TrueContext": "56B10F8DB8885000",
                "user": "EC2AMAZ-Q2H45ST\\Administrator"
                }

        result_data.update(data)
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [result_data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        file_obj = TestSentineloneResultsToStix.get_first_of_type(objects.values(), 'file')
        assert file_obj is not None
        assert file_obj['type'] == 'file'
        assert file_obj['created'] == '2022-02-18T11:10:30.991Z'
        assert file_obj['modified'] == '2022-02-18T11:10:30.991Z'
        assert file_obj['parent_directory_ref'] is not None

    def test_registry_json_to_stix(self):
        """to test windows-registry object properties"""
        result_data = {}
        result_data = common_data
        data = {"dnsCount": None,
                "endpointMachineType": "server",
                "endpointName": "EC2AMAZ-Q2H45ST",
                "endpointOs": "windows",
                "eventIndex": "243",
                "eventTime": "2022-02-23T03:20:44.108Z",
                "eventType": "Registry Value Modified",
                "fileIsExecutable": None,
                "fileMd5": None,
                "fileSha256": None,
                "id": "658273900981256192",
                "metaEventName": "REGVALUEMODIFIED",
                "moduleCount": None,
                "netConnCount": None,
                "netConnInCount": None,
                "netConnOutCount": None,
                "objectType": "registry",
                "parentPid": None,
                "parentProcessName": "services.exe",
                "parentProcessStartTime": "2022-02-18T11:13:25.373Z",
                "parentProcessUniqueKey": "40BF36EC97F04403",
                "pid": "1468",
                "processCmd": "C:\\Windows\\system32\\svchost.exe -k NetworkService -p",
                "processDisplayName": None,
                "processGroupId": "33722D0F34FC18DA",
                "processImagePath": "C:\\Windows\\system32\\svchost.exe",
                "processImageSha1Hash": "a1385ce20ad79f55df235effd9780c31442aa234",
                "processIntegrityLevel": "SYSTEM",
                "processIsRedirectedCommandProcessor": None,
                "processIsWow64": None,
                "processName": "svchost.exe",
                "processRoot": None,
                "processSessionId": None,
                "processStartTime": "2022-02-18T11:13:27.730Z",
                "processSubSystem": None,
                "processUniqueKey": "40BF36EC97F04403",
                "publisher": "MICROSOFT WINDOWS PUBLISHER",
                "registryChangeCount": None,
                "registryId": None,
                "registryKeyPath": "MACHINE\\SYSTEM\\ControlSet001\\Services\\VSS\\Diag\\System "
                                   "Writer\\BACKUPCOMPLETE (Enter)",
                "registryOldValue": "48000000000000003966A5C94228D801BC05000094060000F60"
                                    "30000010000000500000000000000A308CF3E73F44F4181B3",
                "registryOldValueFullSize": None,
                "registryOldValueIsComplete": None,
                "registryOldValueType": "BINARY",
                "registryPath": "MACHINE\\SYSTEM\\ControlSet001\\Services\\VSS\\Diag\\System "
                                "Writer\\BACKUPCOMPLETE (Enter)",
                "registryUid": None,
                "registryUuid": None,
                "registryValue": "48000000000000006FE753566428D801BC05000008060000F"
                                 "60300000100000005000000000000004461718D485CFB459B58",
                "registryValueFullSize": None,
                "registryValueIsComplete": None,
                "registryValueType": None,
                "relatedToThreat": "False",
                "signatureSignedInvalidReason": None,
                "signedStatus": "signed",
                "siteId": "1336793312849490611",
                "siteName": "Default site",
                "srcProcActiveContentFileId": None,
                "srcProcActiveContentHash": None,
                "srcProcActiveContentPath": None,
                "srcProcActiveContentSignedStatus": None,
                "srcProcActiveContentType": None,
                "srcProcBinaryisExecutable": None,
                "srcProcCmdLine": "C:\\Windows\\system32\\svchost.exe -k NetworkService -p",
                "srcProcDisplayName": None,
                "srcProcImageMd5": None,
                "srcProcImagePath": "C:\\Windows\\system32\\svchost.exe",
                "srcProcImageSha1": "a1385ce20ad79f55df235effd9780c31442aa234",
                "srcProcImageSha256": None,
                "srcProcIntegrityLevel": "SYSTEM",
                "srcProcIsNative64Bit": None,
                "srcProcIsRedirectCmdProcessor": None,
                "srcProcIsStorylineRoot": None,
                "srcProcName": "svchost.exe",
                "srcProcParentActiveContentFileId": None,
                "srcProcParentActiveContentHash": None,
                "srcProcParentActiveContentPath": None,
                "srcProcParentActiveContentSignedStatus": None,
                "srcProcParentActiveContentType": None,
                "srcProcParentCmdLine": None,
                "srcProcParentDisplayName": None,
                "srcProcParentImageMd5": None,
                "srcProcParentImagePath": "C:\\Windows\\system32\\services.exe",
                "srcProcParentImageSha1": "106a001c4c9820a6aec6a8ba17d3836525faf80e",
                "srcProcParentImageSha256": None,
                "srcProcParentIntegrityLevel": None,
                "srcProcParentIsNative64Bit": None,
                "srcProcParentIsRedirectCmdProcessor": None,
                "srcProcParentIsStorylineRoot": None,
                "srcProcParentName": "services.exe",
                "srcProcParentPid": None,
                "srcProcParentProcUid": "27717F70F7FD180D",
                "srcProcParentPublisher": None,
                "srcProcParentReasonSignatureInvalid": None,
                "srcProcParentSessionId": None,
                "srcProcParentSignedStatus": None,
                "srcProcParentStartTime": "2022-02-18T11:13:25.373Z",
                "srcProcParentStorylineId": None,
                "srcProcParentUid": "27717F70F7FD180D",
                "srcProcParentUser": None,
                "srcProcPid": "1468",
                "srcProcPublisher": "MICROSOFT WINDOWS PUBLISHER",
                "srcProcReasonSignatureInvalid": None,
                "srcProcRelatedToThreat": "False",
                "srcProcSessionId": None,
                "srcProcSignedStatus": "signed",
                "srcProcStartTime": "2022-02-18T11:13:27.730Z",
                "srcProcStorylineId": "33722D0F34FC18DA",
                "srcProcSubsystem": None,
                "srcProcTid": None,
                "srcProcUid": "40BF36EC97F04403",
                "srcProcUser": "NT AUTHORITY\\NETWORK SERVICE",
                "srcProcVerifiedStatus": "verified",
                "storyline": "33722D0F34FC18DA",
                "tgtFileCreationCount": None,
                "tgtFileDeletionCount": None,
                "tgtFileModificationCount": None,
                "tiindicatorRelatedEventTime": None,
                "traceId": "01FWJ9HT9ARJ6WAWJ4XPPDF5R2",
                "TrueContext": "33722D0F34FC18DA",
                "user": "NT AUTHORITY\\NETWORK SERVICE"
                }
        result_data.update(data)

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [result_data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        registry_obj = TestSentineloneResultsToStix.get_first_of_type(
            objects.values(), 'windows-registry-key')

        assert registry_obj is not None
        assert registry_obj['type'] == 'windows-registry-key'
        assert registry_obj['values'] is not None

    def test_events_json_to_stix(self):
        """to test x-oca-event object properties"""
        result_data = {}
        result_data = common_data
        data = {"direction": "INCOMING",
                "dnsCount": "0",
                "dstIp": "172.31.31.67",
                "dstPort": 3389,
                "endpointMachineType": "server",
                "endpointName": "EC2AMAZ-IQFSLIL",
                "endpointOs": "windows",
                "eventIndex": "15",
                "eventTime": "2022-01-24T18:49:35.296Z",
                "eventType": "IP Connect",
                "fileIsExecutable": "True",
                "fileMd5": "8a0a29438052faed8a2532da50455756",
                "fileSha256": "7fd065bac18c5278777ae44908101cdfed72d26fa741367f0ad4d02020787ab6",
                "id": "649568400931684352",
                "metaEventName": "TCPV4",
                "moduleCount": "541721",
                "netConnCount": "180525",
                "netConnInCount": "180525",
                "netConnOutCount": "0",
                "netConnStatus": "SUCCESS",
                "netEventDirection": "INCOMING",
                "netProtocolName": "ms-wbt-server",
                "objectType": "ip",
                "parentPid": "868",
                "parentProcessName": "services.exe",
                "parentProcessStartTime": "2022-01-20T07:03:11.124Z",
                "parentProcessUniqueKey": "0E1224C52E1F3667",
                "pid": "1188",
                "processCmd": "C:\\Windows\\System32\\svchost.exe -k termsvcs -s TermService",
                "processDisplayName": "Host Process for Windows Services",
                "processGroupId": "B9913CE1424F6FB2",
                "processImagePath": "C:\\Windows\\system32\\svchost.exe",
                "processImageSha1Hash": "a1385ce20ad79f55df235effd9780c31442aa234",
                "processIntegrityLevel": "SYSTEM",
                "processIsRedirectedCommandProcessor": "False",
                "processIsWow64": "False",
                "processName": "svchost.exe",
                "processRoot": "True",
                "processSessionId": "0",
                "processStartTime": "2022-01-20T07:03:12.554Z",
                "processSubSystem": "SYS_WIN32",
                "processUniqueKey": "0E1224C52E1F3667",
                "publisher": "MICROSOFT WINDOWS PUBLISHER",
                "registryChangeCount": "0",
                "relatedToThreat": "False",
                "signatureSignedInvalidReason": None,
                "signedStatus": "signed",
                "siteId": "1336793312849490611",
                "siteName": "Default site",
                "srcIp": "87.251.64.138",
                "srcPort": 3428,
                "srcProcActiveContentFileId": None,
                "srcProcActiveContentHash": None,
                "srcProcActiveContentPath": None,
                "srcProcActiveContentSignedStatus": None,
                "srcProcActiveContentType": None,
                "srcProcBinaryisExecutable": "True",
                "srcProcCmdLine": "C:\\Windows\\System32\\svchost.exe -k termsvcs -s TermService",
                "srcProcDisplayName": "Host Process for Windows Services",
                "srcProcImageMd5": "8a0a29438052faed8a2532da50455756",
                "srcProcImagePath": "C:\\Windows\\system32\\svchost.exe",
                "srcProcImageSha1": "a1385ce20ad79f55df235effd9780c31442aa234",
                "srcProcImageSha256": "7fd065bac18c5278777ae44908101cdfed72d26f"
                                      "a741367f0ad4d02020787ab6",
                "srcProcIntegrityLevel": "SYSTEM",
                "srcProcIsNative64Bit": "False",
                "srcProcIsRedirectCmdProcessor": "False",
                "srcProcIsStorylineRoot": "True",
                "srcProcName": "svchost.exe",
                "srcProcParentActiveContentFileId": None,
                "srcProcParentActiveContentHash": None,
                "srcProcParentActiveContentPath": None,
                "srcProcParentActiveContentSignedStatus": None,
                "srcProcParentActiveContentType": None,
                "srcProcParentCmdLine": "C:\\Windows\\system32\\services.exe",
                "srcProcParentDisplayName": "Services and Controller app",
                "srcProcParentImageMd5": "94f2383da5fa7b9717d03e33cdee5c81",
                "srcProcParentImagePath": "C:\\Windows\\system32\\services.exe",
                "srcProcParentImageSha1": "106a001c4c9820a6aec6a8ba17d3836525faf80e",
                "srcProcParentImageSha256": "7ef551eb51992b5f0f3c76fcf1996bca5ca8e"
                                            "faa87ab527f55835936165f420d",
                "srcProcParentIntegrityLevel": "SYSTEM",
                "srcProcParentIsNative64Bit": "False",
                "srcProcParentIsRedirectCmdProcessor": "False",
                "srcProcParentIsStorylineRoot": "True",
                "srcProcParentName": "services.exe",
                "srcProcParentPid": "868",
                "srcProcParentProcUid": "4B8DD1628A27EDE6",
                "srcProcParentPublisher": "MICROSOFT WINDOWS PUBLISHER",
                "srcProcParentReasonSignatureInvalid": None,
                "srcProcParentSessionId": "0",
                "srcProcParentSignedStatus": "signed",
                "srcProcParentStartTime": "2022-01-20T07:03:11.124Z",
                "srcProcParentStorylineId": "13D130A04AF01959",
                "srcProcParentUid": "4B8DD1628A27EDE6",
                "srcProcParentUser": "NT AUTHORITY\\SYSTEM",
                "srcProcPid": "1188",
                "srcProcPublisher": "MICROSOFT WINDOWS PUBLISHER",
                "srcProcReasonSignatureInvalid": None,
                "srcProcRelatedToThreat": "False",
                "srcProcSessionId": "0",
                "srcProcSignedStatus": "signed",
                "srcProcStartTime": "2022-01-20T07:03:12.554Z",
                "srcProcStorylineId": "B9913CE1424F6FB2",
                "srcProcSubsystem": "SYS_WIN32",
                "srcProcTid": None,
                "srcProcUid": "0E1224C52E1F3667",
                "srcProcUser": "NT AUTHORITY\\NETWORK SERVICE",
                "srcProcVerifiedStatus": "verified",
                "storyline": "B9913CE1424F6FB2",
                "tgtFileCreationCount": "0",
                "tgtFileDeletionCount": "0",
                "tgtFileModificationCount": "0",
                "tiindicatorRelatedEventTime": None,
                "traceId": "01FT6PSXBV4SKNZ2TVW7D7TE8G",
                "trueContext": "B9913CE1424F6FB2",
                "user": "NT AUTHORITY\\NETWORK SERVICE"
                }
        result_data.update(data)
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [result_data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        event_obj = TestSentineloneResultsToStix.get_first_of_type(objects.values(),
                                                                   'x-oca-event')
        assert event_obj is not None
        assert event_obj['type'] == 'x-oca-event'
        assert event_obj['created'] == '2022-01-24T18:49:35.296Z'
        assert event_obj['action'] == 'IP Connect'
        assert event_obj['category'] == ['ip']

    def test_url_json_to_stix(self):
        """
        to test url stix object properties
        """
        result_data = {}
        result_data = common_data
        data = {"dnsCount": None,
                "endpointMachineType": "server",
                "endpointName": "EC2AMAZ-Q2H45ST",
                "endpointOs": "windows",
                "eventIndex": "60",
                "eventTime": "2022-02-18T11:25:03.669Z",
                "eventType": "POST",
                "fileIsExecutable": None,
                "fileMd5": None,
                "fileSha256": None,
                "id": "658248195266969600",
                "metaEventName": "HTTP",
                "moduleCount": None,
                "netConnCount": None,
                "netConnInCount": None,
                "netConnOutCount": None,
                "networkMethod": "POST",
                "networkSource": None,
                "networkUrl": "https://checkappexec.microsoft.com/windows/shell/actions",
                "objectType": "url",
                "parentPid": None,
                "parentProcessName": "explorer.exe",
                "parentProcessStartTime": "2022-02-18T11:24:42.730Z",
                "parentProcessUniqueKey": "0AB4BB5C4DD5DDEE",
                "pid": "4888",
                "processCmd": "C:\\Windows\\System32\\smartscreen.exe -Embedding",
                "processDisplayName": None,
                "processGroupId": "907C659E4DCC23E7",
                "processImagePath": "C:\\Windows\\system32\\smartscreen.exe",
                "processImageSha1Hash": "6aa7a1e3843d9311d45d648d0d4c60204789a6d3",
                "processIntegrityLevel": "HIGH",
                "processIsRedirectedCommandProcessor": None,
                "processIsWow64": None,
                "processName": "smartscreen.exe",
                "processRoot": None,
                "processSessionId": None,
                "processStartTime": "2022-02-18T11:25:01.452Z",
                "processSubSystem": None,
                "processUniqueKey": "0AB4BB5C4DD5DDEE",
                "publisher": "MICROSOFT WINDOWS",
                "registryChangeCount": None,
                "relatedToThreat": "False",
                "signatureSignedInvalidReason": None,
                "signedStatus": "signed",
                "siteId": "1336793312849490611",
                "siteName": "Default site",
                "srcProcActiveContentFileId": None,
                "srcProcActiveContentHash": None,
                "srcProcActiveContentPath": None,
                "srcProcActiveContentSignedStatus": None,
                "srcProcActiveContentType": None,
                "srcProcBinaryisExecutable": None,
                "srcProcCmdLine": "C:\\Windows\\System32\\smartscreen.exe -Embedding",
                "srcProcDisplayName": None,
                "srcProcImageMd5": None,
                "srcProcImagePath": "C:\\Windows\\system32\\smartscreen.exe",
                "srcProcImageSha1": "6aa7a1e3843d9311d45d648d0d4c60204789a6d3",
                "srcProcImageSha256": None,
                "srcProcIntegrityLevel": "HIGH",
                "srcProcIsNative64Bit": None,
                "srcProcIsRedirectCmdProcessor": None,
                "srcProcIsStorylineRoot": None,
                "srcProcName": "smartscreen.exe",
                "srcProcParentActiveContentFileId": None,
                "srcProcParentActiveContentHash": None,
                "srcProcParentActiveContentPath": None,
                "srcProcParentActiveContentSignedStatus": None,
                "srcProcParentActiveContentType": None,
                "srcProcParentCmdLine": None,
                "srcProcParentDisplayName": None,
                "srcProcParentImageMd5": None,
                "srcProcParentImagePath": "C:\\Windows\\explorer.exe",
                "srcProcParentImageSha1": "7caf46864357e582c8a8acca3d62791f456e12a7",
                "srcProcParentImageSha256": None,
                "srcProcParentIntegrityLevel": None,
                "srcProcParentIsNative64Bit": None,
                "srcProcParentIsRedirectCmdProcessor": None,
                "srcProcParentIsStorylineRoot": None,
                "srcProcParentName": "explorer.exe",
                "srcProcParentPid": None,
                "srcProcParentProcUid": "D399D2F211C40483",
                "srcProcParentPublisher": None,
                "srcProcParentReasonSignatureInvalid": None,
                "srcProcParentSessionId": None,
                "srcProcParentSignedStatus": None,
                "srcProcParentStartTime": "2022-02-18T11:24:42.730Z",
                "srcProcParentStorylineId": None,
                "srcProcParentUid": "D399D2F211C40483",
                "srcProcParentUser": None,
                "srcProcPid": "4888",
                "srcProcPublisher": "MICROSOFT WINDOWS",
                "srcProcReasonSignatureInvalid": None,
                "srcProcRelatedToThreat": "False",
                "srcProcSessionId": None,
                "srcProcSignedStatus": "signed",
                "srcProcStartTime": "2022-02-18T11:25:01.452Z",
                "srcProcStorylineId": "907C659E4DCC23E7",
                "srcProcSubsystem": None,
                "srcProcTid": None,
                "srcProcUid": "0AB4BB5C4DD5DDEE",
                "srcProcUser": "EC2AMAZ-Q2H45ST\\Administrator",
                "srcProcVerifiedStatus": "verified",
                "storyline": "907C659E4DCC23E7",
                "tgtFileCreationCount": None,
                "tgtFileDeletionCount": None,
                "tgtFileModificationCount": None,
                "tiindicatorRelatedEventTime": None,
                "traceId": "01FW69920952HKVEMWZX6Z8EFD",
                "trueContext": "907C659E4DCC23E7",
                "url": "https://checkappexec.microsoft.com/windows/shell/actions",
                "urlAction": "POST",
                "user": "EC2AMAZ-Q2H45ST\\Administrator"
                }
        result_data.update(data)

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [result_data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        url_obj = TestSentineloneResultsToStix.get_first_of_type(objects.values(),
                                                                 'url')
        assert url_obj is not None
        assert url_obj['type'] == 'url'
        assert url_obj['value'] == 'https://checkappexec.microsoft.com/windows/shell/actions'

    def test_asset_json_to_stix(self):
        """
        to test x-oca-asset custom object properties
        """
        result_data = {}
        result_data = common_data
        data = {"direction": "INCOMING",
                "dnsCount": "0",
                "dstIp": "172.31.31.67",
                "dstPort": 3389,
                "endpointMachineType": "server",
                "endpointName": "EC2AMAZ-IQFSLIL",
                "endpointOs": "windows",
                "eventIndex": "15",
                "eventTime": "2022-01-24T18:49:35.296Z",
                "eventType": "IP Connect",
                "fileIsExecutable": "True",
                "fileMd5": "8a0a29438052faed8a2532da50455756",
                "fileSha256": "7fd065bac18c5278777ae44908101cdfed72d26fa741367f0ad4d02020787ab6",
                "id": "649568400931684352",
                "indicatorBootConfigurationUpdateCount": "0",
                "metaEventName": "TCPV4",
                "moduleCount": "541721",
                "netConnCount": "180525",
                "netConnInCount": "180525",
                "netConnOutCount": "0",
                "netConnStatus": "SUCCESS",
                "netEventDirection": "INCOMING",
                "netProtocolName": "ms-wbt-server",
                "objectType": "ip",
                "parentPid": "868",
                "parentProcessName": "services.exe",
                "parentProcessStartTime": "2022-01-20T07:03:11.124Z",
                "parentProcessUniqueKey": "0E1224C52E1F3667",
                "pid": "1188",
                "processCmd": "C:\\Windows\\System32\\svchost.exe -k termsvcs -s TermService",
                "processDisplayName": "Host Process for Windows Services",
                "processGroupId": "B9913CE1424F6FB2",
                "processImagePath": "C:\\Windows\\system32\\svchost.exe",
                "processImageSha1Hash": "a1385ce20ad79f55df235effd9780c31442aa234",
                "processIntegrityLevel": "SYSTEM",
                "processIsRedirectedCommandProcessor": "False",
                "processIsWow64": "False",
                "processName": "svchost.exe",
                "processRoot": "True",
                "processSessionId": "0",
                "processStartTime": "2022-01-20T07:03:12.554Z",
                "processSubSystem": "SYS_WIN32",
                "processUniqueKey": "0E1224C52E1F3667",
                "publisher": "MICROSOFT WINDOWS PUBLISHER",
                "registryChangeCount": "0",
                "relatedToThreat": "False",
                "signatureSignedInvalidReason": None,
                "signedStatus": "signed",
                "siteId": "1336793312849490611",
                "siteName": "Default site",
                "srcIp": "87.251.64.138",
                "srcPort": 3428,
                "srcProcActiveContentFileId": None,
                "srcProcActiveContentHash": None,
                "srcProcActiveContentPath": None,
                "srcProcActiveContentSignedStatus": None,
                "srcProcActiveContentType": None,
                "srcProcBinaryisExecutable": "True",
                "srcProcCmdLine": "C:\\Windows\\System32\\svchost.exe -k termsvcs -s TermService",
                "srcProcDisplayName": "Host Process for Windows Services",
                "srcProcImageMd5": "8a0a29438052faed8a2532da50455756",
                "srcProcImagePath": "C:\\Windows\\system32\\svchost.exe",
                "srcProcImageSha1": "a1385ce20ad79f55df235effd9780c31442aa234",
                "srcProcImageSha256": "7fd065bac18c5278777ae44908101cdfed72"
                                      "d26fa741367f0ad4d02020787ab6",
                "srcProcIntegrityLevel": "SYSTEM",
                "srcProcIsNative64Bit": "False",
                "srcProcIsRedirectCmdProcessor": "False",
                "srcProcIsStorylineRoot": "True",
                "srcProcName": "svchost.exe",
                "srcProcParentActiveContentFileId": None,
                "srcProcParentActiveContentHash": None,
                "srcProcParentActiveContentPath": None,
                "srcProcParentActiveContentSignedStatus": None,
                "srcProcParentActiveContentType": None,
                "srcProcParentCmdLine": "C:\\Windows\\system32\\services.exe",
                "srcProcParentDisplayName": "Services and Controller app",
                "srcProcParentImageMd5": "94f2383da5fa7b9717d03e33cdee5c81",
                "srcProcParentImagePath": "C:\\Windows\\system32\\services.exe",
                "srcProcParentImageSha1": "106a001c4c9820a6aec6a8ba17d3836525faf80e",
                "srcProcParentImageSha256": "7ef551eb51992b5f0f3c76fcf1996bca5ca8e"
                                            "faa87ab527f55835936165f420d",
                "srcProcParentIntegrityLevel": "SYSTEM",
                "srcProcParentIsNative64Bit": "False",
                "srcProcParentIsRedirectCmdProcessor": "False",
                "srcProcParentIsStorylineRoot": "True",
                "srcProcParentName": "services.exe",
                "srcProcParentPid": "868",
                "srcProcParentProcUid": "4B8DD1628A27EDE6",
                "srcProcParentPublisher": "MICROSOFT WINDOWS PUBLISHER",
                "srcProcParentReasonSignatureInvalid": None,
                "srcProcParentSessionId": "0",
                "srcProcParentSignedStatus": "signed",
                "srcProcParentStartTime": "2022-01-20T07:03:11.124Z",
                "srcProcParentStorylineId": "13D130A04AF01959",
                "srcProcParentUid": "4B8DD1628A27EDE6",
                "srcProcParentUser": "NT AUTHORITY\\SYSTEM",
                "srcProcPid": "1188",
                "srcProcPublisher": "MICROSOFT WINDOWS PUBLISHER",
                "srcProcReasonSignatureInvalid": None,
                "srcProcRelatedToThreat": "False",
                "srcProcSessionId": "0",
                "srcProcSignedStatus": "signed",
                "srcProcStartTime": "2022-01-20T07:03:12.554Z",
                "srcProcStorylineId": "B9913CE1424F6FB2",
                "srcProcSubsystem": "SYS_WIN32",
                "srcProcTid": None,
                "srcProcUid": "0E1224C52E1F3667",
                "srcProcUser": "NT AUTHORITY\\NETWORK SERVICE",
                "srcProcVerifiedStatus": "verified",
                "storyline": "B9913CE1424F6FB2",
                "tiOriginalEventId": None,
                "tiOriginalEventIndex": None,
                "tiOriginalEventTraceId": None,
                "tiindicatorRelatedEventTime": None,
                "traceId": "01FT6PSXBV4SKNZ2TVW7D7TE8G",
                "trueContext": "B9913CE1424F6FB2",
                "user": "NT AUTHORITY\\NETWORK SERVICE"
                }
        result_data.update(data)
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [result_data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        asset_obj = TestSentineloneResultsToStix.get_first_of_type(objects.values(),
                                                                   'x-oca-asset')
        assert asset_obj is not None
        assert asset_obj['type'] == 'x-oca-asset'
        assert asset_obj['ip_refs'] == ['2', '4']
        assert asset_obj['hostname'] == 'EC2AMAZ-IQFSLIL'
        assert asset_obj['extensions']['x-sentinelone-endpoint']['agent_uuid'] == 'f5875d2abd9f4198824885126b4f4d07'

    def test_directory_json_to_stix(self):
        """
        to test directory stix object properties
        """
        result_data = {}
        result_data = common_data
        data = {"dnsCount": None,
                "endpointMachineType": "server",
                "endpointName": "EC2AMAZ-Q2H45ST",
                "endpointOs": "windows",
                "eventIndex": "70",
                "eventTime": "2022-02-27T21:06:00.103Z",
                "eventType": "File Rename",
                "fileCreatedAt": "2022-02-27T21:06:00.103Z",
                "fileFullName": "C:\\ProgramData\\Amazon\\SSM\\InstanceData\\i-05ab21e6c"
                                "7fbd9683\\channels\\health\\surveyor-2022"
                                "0218111331-13216",
                "fileId": "15B1561A6C8602F6",
                "fileIsExecutable": None,
                "fileLocation": None,
                "fileMd5": None,
                "fileModifyAt": "2022-02-27T21:06:00.103Z",
                "fileSha1": None,
                "fileSha256": None,
                "fileSize": None,
                "fileType": None,
                "id": "659317783064215552",
                "lastActivatedAt": None,
                "metaEventName": "FILERENAME",
                "moduleCount": None,
                "netConnCount": None,
                "netConnInCount": None,
                "netConnOutCount": None,
                "newFileName": None,
                "objectType": "file",
                "oldFileMd5": None,
                "oldFileName": "C:\\ProgramData\\Amazon\\SSM\\InstanceData\\i-05ab"
                               "21e6c7fbd9683\\channels\\health\\tmp\\surveyor-202"
                               "20218111331-13216",
                "oldFileSha1": None,
                "oldFileSha256": None,
                "parentPid": None,
                "parentProcessName": "services.exe",
                "parentProcessStartTime": "2022-02-18T11:13:25.373Z",
                "parentProcessUniqueKey": "D98B1BFE4E018755",
                "pid": "1296",
                "processCmd": "\"C:\\Program Files\\Amazon\\SSM\\amazon-ssm-agent.exe\"",
                "processDisplayName": None,
                "processGroupId": "15660BC0A986390A",
                "processImagePath": "C:\\Program Files\\Amazon\\SSM\\amazon-ssm-agent.exe",
                "processImageSha1Hash": "f11a24de4db9a3781056ee4759"
                                        "7391c60a1b7fa0",
                "processIntegrityLevel": "SYSTEM",
                "processIsRedirectedCommandProcessor": None,
                "processIsWow64": None,
                "processName": "amazon-ssm-agent.exe",
                "processRoot": None,
                "processSessionId": None,
                "processStartTime": "2022-02-18T11:13:30.006Z",
                "processSubSystem": None,
                "processUniqueKey": "D98B1BFE4E018755",
                "publisher": "AMAZON.COM SERVICES LLC",
                "registryChangeCount": None,
                "relatedToThreat": "False",
                "signatureSignedInvalidReason": None,
                "signedStatus": "signed",
                "siteId": "1336793312849490611",
                "siteName": "Default site",
                "srcProcActiveContentFileId": None,
                "srcProcActiveContentHash": None,
                "srcProcActiveContentPath": None,
                "srcProcActiveContentSignedStatus": None,
                "srcProcActiveContentType": None,
                "srcProcBinaryisExecutable": None,
                "srcProcCmdLine": "\"C:\\Program Files\\Amazon\\SSM\\amazon-ssm-agent.exe\"",
                "srcProcDisplayName": None,
                "srcProcImageMd5": None,
                "srcProcImagePath": "C:\\Program Files\\Amazon\\SSM\\amazon-ssm-agent.exe",
                "srcProcImageSha1": "f11a24de4db9a3781056ee4759"
                                    "7391c60a1b7fa0",
                "srcProcImageSha256": None,
                "srcProcIntegrityLevel": "SYSTEM",
                "srcProcIsNative64Bit": None,
                "srcProcIsRedirectCmdProcessor": None,
                "srcProcIsStorylineRoot": None,
                "srcProcName": "amazon-ssm-agent.exe",
                "srcProcParentActiveContentFileId": None,
                "srcProcParentActiveContentHash": None,
                "srcProcParentActiveContentPath": None,
                "srcProcParentActiveContentSignedStatus": None,
                "srcProcParentActiveContentType": None,
                "srcProcParentCmdLine": None,
                "srcProcParentDisplayName": None,
                "srcProcParentImageMd5": None,
                "srcProcParentImagePath": "C:\\Windows\\system32\\services.exe",
                "srcProcParentImageSha1": "106a001c4c9820a6aec6a8ba17d3836525faf80e",
                "srcProcParentImageSha256": None,
                "srcProcParentIntegrityLevel": None,
                "srcProcParentIsNative64Bit": None,
                "srcProcParentIsRedirectCmdProcessor": None,
                "srcProcParentIsStorylineRoot": None,
                "srcProcParentName": "services.exe",
                "srcProcParentPid": None,
                "srcProcParentProcUid": "27717F70F7FD180D",
                "srcProcParentPublisher": None,
                "srcProcParentReasonSignatureInvalid": None,
                "srcProcParentSessionId": None,
                "srcProcParentSignedStatus": None,
                "srcProcParentStartTime": "2022-02-18T11:13:25.373Z",
                "srcProcParentStorylineId": None,
                "srcProcParentUid": "27717F70F7FD180D",
                "srcProcParentUser": None,
                "srcProcPid": "1296",
                "srcProcPublisher": "AMAZON.COM SERVICES LLC",
                "srcProcReasonSignatureInvalid": None,
                "srcProcRelatedToThreat": "False",
                "srcProcSessionId": None,
                "srcProcSignedStatus": "signed",
                "srcProcStartTime": "2022-02-18T11:13:30.006Z",
                "srcProcStorylineId": "15660BC0A986390A",
                "srcProcSubsystem": None,
                "srcProcTid": None,
                "srcProcUid": "D98B1BFE4E018755",
                "srcProcUser": "NT AUTHORITY\\SYSTEM",
                "srcProcVerifiedStatus": "verified",
                "storyline": "15660BC0A986390A",
                "tgtFileConvictedBy": None,
                "tgtFileCreatedAt": "2022-02-27T21:06:00.103Z",
                "tgtFileCreationCount": None,
                "tgtFileDeletionCount": None,
                "tgtFileDescription": None,
                "tgtFileExtension": None,
                "tgtFileId": "15B1561A6C8602F6",
                "tgtFileInternalName": None,
                "tgtFileIsExecutable": None,
                "tgtFileIsSigned": None,
                "tgtFileLocation": None,
                "tgtFileMd5": None,
                "tgtFileModificationCount": None,
                "tgtFileModifiedAt": "2022-02-27T21:06:00.103Z",
                "tgtFileOldMd5": None,
                "tgtFileOldPath": "C:\\ProgramData\\Amazon\\SSM\\InstanceData\\i-05"
                                  "ab21e6c7fbd9683\\channels\\health\\tmp\\surveyor-2"
                                  "0220218111331-13216",
                "tgtFileOldSha1": None,
                "tgtFileOldSha256": None,
                "tgtFilePath": "C:\\ProgramData\\Amazon\\SSM\\InstanceData\\i-05ab2"
                               "1e6c7fbd9683\\channels\\health\\surveyor-2022021"
                               "8111331-13216",
                "tgtFileSha1": None,
                "tgtFileSha256": None,
                "tgtFileSize": None,
                "tgtFileType": None,
                "tiindicatorRelatedEventTime": None,
                "traceId": "01FWYG2YZYVV19ZR9TN0QQE1N3",
                "TrueContext": "15660BC0A986390A",
                "user": "NT AUTHORITY\\SYSTEM"
                }

        result_data.update(data)

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [result_data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        directory_obj = TestSentineloneResultsToStix.get_first_of_type(
            objects.values(), 'directory')
        assert directory_obj is not None
        assert directory_obj['type'] == 'directory'
        assert directory_obj['path'] == 'C:\\Program Files\\Amazon\\SSM'

    def test_domain_json_to_stix(self):
        """
        to test domain object properties
        """
        result_data = {}
        result_data = common_data
        data = {"dnsCount": None,
                "dnsRequest": "ctldl.windowsupdate.com",
                "dnsResponse": "type:  5 wu-bg-shim.trafficmanager.net;type:  "
                               "5 cds.d2s7q6s2.hwcdn.net;209.197.3.8;",
                "endpointMachineType": "server",
                "endpointName": "EC2AMAZ-Q2H45ST",
                "endpointOs": "windows",
                "eventIndex": "0",
                "eventTime": "2022-02-19T00:12:44.459Z",
                "eventType": "DNS Resolved",
                "fileIsExecutable": None,
                "fileMd5": None,
                "fileSha256": None,
                "id": "658228036380262424",

                "metaEventName": "DNS",
                "moduleCount": None,
                "netConnCount": None,
                "netConnInCount": None,
                "netConnOutCount": None,
                "objectType": "dns",
                "parentPid": None,
                "parentProcessName": "services.exe",
                "parentProcessStartTime": "2022-02-18T11:13:25.373Z",
                "parentProcessUniqueKey": "40BF36EC97F04403",
                "pid": "1468",
                "processCmd": "C:\\Windows\\system32\\svchost.exe -k NetworkService -p",
                "processDisplayName": None,
                "processGroupId": "33722D0F34FC18DA",
                "processImagePath": "C:\\Windows\\system32\\svchost.exe",
                "processImageSha1Hash": "a1385ce20ad79f55df235effd9780c31442aa234",
                "processIntegrityLevel": "SYSTEM",
                "processIsRedirectedCommandProcessor": None,
                "processIsWow64": None,
                "processName": "svchost.exe",
                "processRoot": None,
                "processSessionId": None,
                "processStartTime": "2022-02-18T11:13:27.730Z",
                "processSubSystem": None,
                "processUniqueKey": "40BF36EC97F04403",
                "publisher": "MICROSOFT WINDOWS PUBLISHER",
                "registryChangeCount": None,
                "relatedToThreat": "False",
                "signatureSignedInvalidReason": None,
                "signedStatus": "signed",
                "siteId": "1336793312849490611",
                "siteName": "Default site",
                "srcProcActiveContentFileId": None,
                "srcProcActiveContentHash": None,
                "srcProcActiveContentPath": None,
                "srcProcActiveContentSignedStatus": None,
                "srcProcActiveContentType": None,
                "srcProcBinaryisExecutable": None,
                "srcProcCmdLine": "C:\\Windows\\system32\\svchost.exe -k NetworkService -p",
                "srcProcDisplayName": None,
                "srcProcImageMd5": None,
                "srcProcImagePath": "C:\\Windows\\system32\\svchost.exe",
                "srcProcImageSha1": "a1385ce20ad79f55df235effd9780c31442aa234",
                "srcProcImageSha256": None,
                "srcProcIntegrityLevel": "SYSTEM",
                "srcProcIsNative64Bit": None,
                "srcProcIsRedirectCmdProcessor": None,
                "srcProcIsStorylineRoot": None,
                "srcProcName": "svchost.exe",
                "srcProcParentActiveContentFileId": None,
                "srcProcParentActiveContentHash": None,
                "srcProcParentActiveContentPath": None,
                "srcProcParentActiveContentSignedStatus": None,
                "srcProcParentActiveContentType": None,
                "srcProcParentCmdLine": None,
                "srcProcParentDisplayName": None,
                "srcProcParentImageMd5": None,
                "srcProcParentImagePath": "C:\\Windows\\system32\\services.exe",
                "srcProcParentImageSha1": "106a001c4c9820a6aec6a8ba17d3836525faf80e",
                "srcProcParentImageSha256": None,
                "srcProcParentIntegrityLevel": None,
                "srcProcParentIsNative64Bit": None,
                "srcProcParentIsRedirectCmdProcessor": None,
                "srcProcParentIsStorylineRoot": None,
                "srcProcParentName": "services.exe",
                "srcProcParentPid": None,
                "srcProcParentProcUid": "27717F70F7FD180D",
                "srcProcParentPublisher": None,
                "srcProcParentReasonSignatureInvalid": None,
                "srcProcParentSessionId": None,
                "srcProcParentSignedStatus": None,
                "srcProcParentStartTime": "2022-02-18T11:13:25.373Z",
                "srcProcParentStorylineId": None,
                "srcProcParentUid": "27717F70F7FD180D",
                "srcProcParentUser": None,
                "srcProcPid": "1468",
                "srcProcPublisher": "MICROSOFT WINDOWS PUBLISHER",
                "srcProcReasonSignatureInvalid": None,
                "srcProcRelatedToThreat": "False",
                "srcProcSessionId": None,
                "srcProcSignedStatus": "signed",
                "srcProcStartTime": "2022-02-18T11:13:27.730Z",
                "srcProcStorylineId": "33722D0F34FC18DA",
                "srcProcSubsystem": None,
                "srcProcTid": None,
                "srcProcUid": "40BF36EC97F04403",
                "srcProcUser": "NT AUTHORITY\\NETWORK SERVICE",
                "srcProcVerifiedStatus": "verified",
                "storyline": "33722D0F34FC18DA",
                "tgtFileCreationCount": None,
                "tgtFileDeletionCount": None,
                "tgtFileModificationCount": None,
                "tiindicatorRelatedEventTime": None,
                "traceId": "01FW7N6S2T3F4RMPD76SE3MTR6",
                "trueContext": "33722D0F34FC18DA",
                "user": "NT AUTHORITY\\NETWORK SERVICE"
                }
        result_data.update(data)

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [result_data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        domain_obj = TestSentineloneResultsToStix.get_first_of_type(objects.values(),
                                                                    'domain-name')
        assert domain_obj is not None
        assert domain_obj['type'] == 'domain-name'
        assert domain_obj['value'] == 'ctldl.windowsupdate.com'
