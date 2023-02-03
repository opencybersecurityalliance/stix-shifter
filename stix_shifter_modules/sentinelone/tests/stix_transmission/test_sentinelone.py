from unittest.mock import patch
import unittest
import json
from aiohttp.client_exceptions import ClientConnectionError

from stix_shifter_modules.sentinelone.entry_point import EntryPoint
from stix_shifter.stix_transmission import stix_transmission
from tests.utils.async_utils import get_mock_response


class TestSentineloneConnection(unittest.TestCase):
    """ class for test sentinelone connection"""

    @staticmethod
    def config():
        """format for configuration"""
        return {
            "auth": {
                "apitoken": "test"
            }
        }

    @staticmethod
    def connection():
        """format for connection"""
        return {
            "host": "testhost",
            "port": 443
        }

    def test_is_async(self):
       """check for synchronous or asynchronous"""
       entry_point = EntryPoint(self.connection(), self.config())
       check_async = entry_point.is_async()
       assert check_async is True

    @patch('stix_shifter_modules.sentinelone.stix_transmission.api_client'
           '.APIClient.ping_datasource')
    def test_ping_endpoint(self, mock_ping_source):
        """ test to check ping_data_source function"""
        obj = """{"data":{"health":"ok"}}"""
        response = get_mock_response(200, obj, 'byte')
        mock_ping_source.return_value = response

        
        transmission = stix_transmission.StixTransmission('sentinelone',
                                                          self.connection(),
                                                          self.config())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is True
        assert ping_response['code'] is not None


    @patch('stix_shifter_modules.sentinelone.stix_transmission.api_client'
           '.APIClient.ping_datasource')
    def test_ping_endpoint_error(self, mock_ping_source):
        """ test to check ping_data_source function"""
        obj = """{"errors":[{"code":4000040,"detail":"empty result"}]}"""
        response = get_mock_response(400, obj)
        mock_ping_source.return_value = response

        
        transmission = stix_transmission.StixTransmission('sentinelone',
                                                          self.connection(),
                                                          self.config())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert ping_response['code'] is not None


    @patch('stix_shifter_modules.sentinelone.stix_transmission.api_client'
           '.APIClient.ping_datasource')
    def test_ping_endpoint_parseerror(self, mock_ping_source):
        """ test to check ping_data_source parse error"""
        obj = """{"errors":"error"n}"""
        response = get_mock_response(400, obj)
        mock_ping_source.return_value = response

        transmission = stix_transmission.StixTransmission('sentinelone',
                                                          self.connection(),
                                                          self.config())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert ping_response['error'] is not None
        assert ping_response['connector'] is not None
        assert ping_response['code'] is not None

    @patch('stix_shifter_modules.sentinelone.stix_transmission.api_client'
           '.APIClient.create_search')
    def test_process_query(self, mock_create_search):
        """ test to check query of process """
        obj = """{"data":{"queryId":"qf7a4b38c654e93d22b33017b1a0faadf"}}"""
        response = get_mock_response(200, obj, 'byte')
        mock_create_search.return_value = response

        query = json.dumps('{"query": "(SrcProcName In Contains (\\"host.exe\\") and EventTime ' \
                'BETWEEN \\"2022-01-02T18:49:35.296Z\\" AND \\"2022-02-18T18:49:35.296Z\\")",' \
                '"limit": 1, "toDate": "2022-02-22T04:49:26.257525Z", "fromDate": "2022-02-10T04:49:26.257525Z" }')

        transmission = stix_transmission.StixTransmission('sentinelone',
                                                          self.connection(),
                                                          self.config())
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert query_response['search_id'] is not None
        assert query_response['search_id'] == 'qf7a4b38c654e93d22b33017b1a0faadf'


    @patch('stix_shifter_modules.sentinelone.stix_transmission.api_client'
           '.APIClient.create_search')
    def test_search_query_error(self, mock_create_search):
        """ test to check search query error """
        obj = """{"errors":[{"code":4000040,"detail":"bad request"}]}"""
        response = get_mock_response(400, obj)
        mock_create_search.return_value = response

        query = json.dumps('{"query": "(SrcProcName In Contains (\\"host.exe\\") and TestEventTime ' \
                           'BETWEEN \\"2022-01-02T18:49:35.296Z\\" AND \\"2022-02-18T18:49:35.296Z\\")",' \
                           '"limit": 1, "toDate": "2022-02-22T04:49:26.257525Z", "fromDate": "2022-02-10T04:49:26.257525Z" }')

        transmission = stix_transmission.StixTransmission('sentinelone',
                                                          self.connection(),
                                                          self.config())
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is False
        assert query_response['error'] is not None
        assert query_response['connector'] is not None
        assert query_response['code'] is not None

    @patch('stix_shifter_modules.sentinelone.stix_transmission.api_client'
           '.APIClient.create_search')
    def test_search_query_limiterror(self, mock_create_search):
        """ test to check search query limit error """
        obj = '{"errors":[{"code":4000010,"detail":"Limit must be greater than or ' \
              'equals to 1 and less than equals to 100000"}]}'
        response = get_mock_response(400, obj)
        mock_create_search.return_value = response

        query = json.dumps('{"query": "(SrcProcName In Contains (\\"host.exe\\") and EventTime ' \
                           'BETWEEN \\"2022-01-02T18:49:35.296Z\\" AND \\"2022-02-18T18:49:35.296Z\\")",' \
                           '"limit": 100010, "toDate": "2022-02-22T04:49:26.257525Z", "fromDate": "2022-02-10T04:49:26.257525Z" }')

        transmission = stix_transmission.StixTransmission('sentinelone',
                                                          self.connection(),
                                                          self.config())
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is False
        assert query_response['error'] is not None
        assert query_response['connector'] is not None
        assert query_response['code'] is not None

    @patch('stix_shifter_modules.sentinelone.stix_transmission.api_client'
           '.APIClient.create_search')
    def test_search_authentication_error(self, mock_create_search):
        """ test to check search query authentication error """
        obj = '{"errors":[{"code":4010010,"detail":"Authentication failed"}]}'
        response = get_mock_response(401, obj)
        mock_create_search.return_value = response

        query = json.dumps('{"query": "(SrcProcName In Contains (\\"host.exe\\") and EventTime ' \
                           'BETWEEN \\"2022-01-02T18:49:35.296Z\\" AND \\"2022-02-18T18:49:35.296Z\\")",' \
                           '"limit": 100000, "toDate": "2022-02-22T04:49:26.257525Z", "fromDate": "2022-02-10T04:49:26.257525Z" }')

        transmission = stix_transmission.StixTransmission('sentinelone',
                                                          self.connection(),
                                                          self.config())
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is False
        assert query_response['error'] is not None
        assert query_response['connector'] is not None
        assert query_response['code'] is not None

    @patch('stix_shifter_modules.sentinelone.stix_transmission.api_client'
           '.APIClient.create_search')
    def test_file_query(self, mock_create_search):
        """ test to check query of file object """
        obj = """{"data":{"queryId":"qf7a4b38c654e93d22b33017b1a0faadf"}}"""
        response = get_mock_response(200, obj, 'byte')
        mock_create_search.return_value = response

        query = json.dumps('{"query": "(TgtFilePath  In Contains (\\"wildfire\\") and EventTime ' \
                           'BETWEEN \\"2022-01-02T18:49:35.296Z\\" AND \\"2022-02-18T18:49:35.296Z\\")",' \
                           '"limit": 1, "toDate": "2022-02-22T04:49:26.257525Z", "fromDate": "2022-02-10T04:49:26.257525Z" }')

        transmission = stix_transmission.StixTransmission('sentinelone',
                                                          self.connection(),
                                                          self.config())
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert query_response['search_id'] is not None

 
    @patch('stix_shifter_modules.sentinelone.stix_transmission.api_client'
           '.APIClient.create_search')
    def test_network_traffic_query(self, mock_create_search):
        """ test to check query of network traffic """
        obj = """{"data":{"queryId":"qf7a4b38c654e93d22b33017b1a0faadf"}}"""
        response = get_mock_response(200, obj, 'byte')
        mock_create_search.return_value = response

        query = json.dumps('{"query": "(SrcIP = \\"172-31-31-110\\" OR DstIP = \\"172-31-31-110\\") '
                           'and EventTime BETWEEN \\"2022-01-02T18:49:35.296Z\\" AND \\"2022-02-18T18:49:35.296Z\\")",' \
                           '"limit": 1, "toDate": "2022-02-22T04:49:26.257525Z", '
                           '"fromDate": "2022-02-10T04:49:26.257525Z" }')

        transmission = stix_transmission.StixTransmission('sentinelone',
                                                          self.connection(),
                                                          self.config())
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert query_response['search_id'] is not None


    @patch('stix_shifter_modules.sentinelone.stix_transmission.api_client'
           '.APIClient.get_search_results')
    def test_process_result(self, mock_results_response):
        """ test to check result of process object"""
        obj = """{"data":[{
            "activeContentFileId": null,
            "activeContentHash": null,
            "activeContentPath": null,
            "activeContentSignedStatus": null,
            "activeContentType": null,
            "agentDomain": "WORKGROUP",
            "agentGroupId": "1336793312883045044",
            "agentId": "1337419724165944028",
            "agentInfected": false,
            "agentIp": "54.91.158.243",
            "agentIsActive": false,
            "agentIsDecommissioned": false,
            "agentMachineType": "server",
            "agentName": "EC2AMAZ-IQFSLIL",
            "agentNetworkStatus": "connected",
            "agentOs": "windows",
            "agentTimestamp": "2022-01-24T18:49:35.296Z",
            "agentUuid": "f5875d2abd9f4198824885126b4f4d07",
            "agentVersion": "21.6.6.1200",
            "childProcCount": "28",
            "connectionStatus": "SUCCESS",
            "containerId": null,
            "containerImage": null,
            "containerLabels": null,
            "containerName": null,
            "createdAt": "2022-01-24T18:49:35.296000Z",
            "crossProcCount": "0",
            "crossProcDupRemoteProcHandleCount": "0",
            "crossProcDupThreadHandleCount": "0",
            "crossProcOpenProcCount": "0",
            "crossProcOutOfStorylineCount": "0",
            "crossProcThreadCreateCount": "0",
            "direction": "INCOMING",
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
            "indicatorEvasionCount": "0",
            "indicatorExploitationCount": "0",
            "indicatorGeneralCount": "48",
            "indicatorInfostealerCount": "0",
            "indicatorInjectionCount": "0",
            "indicatorPersistenceCount": "0",
            "indicatorPostExploitationCount": "0",
            "indicatorRansomwareCount": "0",
            "indicatorReconnaissanceCount": "0",
            "k8sClusterName": null,
            "k8sControllerLabels": null,
            "k8sControllerName": null,
            "k8sControllerType": null,
            "k8sNamespace": null,
            "k8sNamespaceLabels": null,
            "k8sNode": null,
            "k8sPodLabels": null,
            "k8sPodName": null,
            "metaEventName": "TCPV4",
            "moduleCount": "541721",
            "netConnCount": "180525",
            "netConnInCount": "180525",
            "netConnOutCount": "0",
            "netConnStatus": "SUCCESS",
            "netEventDirection": "INCOMING",
            "netProtocolName": "ms-wbt-server",
            "objectType": "ip",
            "osSrcChildProcCount": null,
            "osSrcCrossProcCount": null,
            "osSrcCrossProcDupRemoteProcHandleCount": null,
            "osSrcCrossProcDupThreadHandleCount": null,
            "osSrcCrossProcOpenProcCount": null,
            "osSrcCrossProcOutOfStorylineCount": null,
            "osSrcCrossProcThreadCreateCount": null,
            "osSrcDnsCount": null,
            "osSrcIndicatorBootConfigurationUpdateCount": null,
            "osSrcIndicatorEvasionCount": null,
            "osSrcIndicatorExploitationCount": null,
            "osSrcIndicatorGeneralCount": null,
            "osSrcIndicatorInfostealerCount": null,
            "osSrcIndicatorInjectionCount": null,
            "osSrcIndicatorPersistenceCount": null,
            "osSrcIndicatorPostExploitationCount": null,
            "osSrcIndicatorRansomwareCount": null,
            "osSrcIndicatorReconnaissanceCount": null,
            "osSrcModuleCount": null,
            "osSrcNetConnCount": null,
            "osSrcNetConnInCount": null,
            "osSrcNetConnOutCount": null,
            "osSrcProcActiveContentFileId": null,
            "osSrcProcActiveContentHash": null,
            "osSrcProcActiveContentPath": null,
            "osSrcProcActiveContentSignedStatus": null,
            "osSrcProcActiveContentType": null,
            "osSrcProcBinaryisExecutable": null,
            "osSrcProcCmdLine": null,
            "osSrcProcDisplayName": null,
            "osSrcProcImageMd5": null,
            "osSrcProcImagePath": null,
            "osSrcProcImageSha1": null,
            "osSrcProcImageSha256": null,
            "osSrcProcIntegrityLevel": null,
            "osSrcProcIsNative64Bit": null,
            "osSrcProcIsRedirectCmdProcessor": null,
            "osSrcProcIsStorylineRoot": null,
            "osSrcProcName": null,
            "osSrcProcParentActiveContentFileId": null,
            "osSrcProcParentActiveContentHash": null,
            "osSrcProcParentActiveContentPath": null,
            "osSrcProcParentActiveContentSignedStatus": null,
            "osSrcProcParentActiveContentType": null,
            "osSrcProcParentCmdLine": null,
            "osSrcProcParentDisplayName": null,
            "osSrcProcParentImageMd5": null,
            "osSrcProcParentImagePath": null,
            "osSrcProcParentImageSha1": null,
            "osSrcProcParentImageSha256": null,
            "osSrcProcParentIntegrityLevel": null,
            "osSrcProcParentIsNative64Bit": null,
            "osSrcProcParentIsRedirectCmdProcessor": null,
            "osSrcProcParentIsStorylineRoot": null,
            "osSrcProcParentName": null,
            "osSrcProcParentPid": null,
            "osSrcProcParentPublisher": null,
            "osSrcProcParentReasonSignatureInvalid": null,
            "osSrcProcParentSessionId": null,
            "osSrcProcParentSignedStatus": null,
            "osSrcProcParentStartTime": null,
            "osSrcProcParentStorylineId": null,
            "osSrcProcParentUid": null,
            "osSrcProcParentUser": null,
            "osSrcProcPid": null,
            "osSrcProcPublisher": null,
            "osSrcProcReasonSignatureInvalid": null,
            "osSrcProcRelatedToThreat": "False",
            "osSrcProcSessionId": null,
            "osSrcProcSignedStatus": null,
            "osSrcProcStartTime": null,
            "osSrcProcStorylineId": null,
            "osSrcProcSubsystem": null,
            "osSrcProcUid": null,
            "osSrcProcUser": null,
            "osSrcProcVerifiedStatus": null,
            "osSrcRegistryChangeCount": null,
            "osSrcTgtFileCreationCount": null,
            "osSrcTgtFileDeletionCount": null,
            "osSrcTgtFileModificationCount": null,
            "parentPid": "868",
            "parentProcessName": "services.exe",
            "parentProcessStartTime": "2022-01-20T07:03:11.124Z",
            "parentProcessUniqueKey": "0E1224C52E1F3667",
            "pid": "1188",
            "processCmd": "C:\\\\Windows\\\\System32\\\\svchost.exe -k termsvcs -s TermService",
            "processDisplayName": "Host Process for Windows Services",
            "processGroupId": "B9913CE1424F6FB2",
            "processImagePath": "C:\\\\Windows\\\\system32\\\\svchost.exe",
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
            "rpid": null,
            "signatureSignedInvalidReason": null,
            "signedStatus": "signed",
            "siteId": "1336793312849490611",
            "siteName": "Default site",
            "srcIp": "87.251.64.138",
            "srcPort": 3428,
            "srcProcActiveContentFileId": null,
            "srcProcActiveContentHash": null,
            "srcProcActiveContentPath": null,
            "srcProcActiveContentSignedStatus": null,
            "srcProcActiveContentType": null,
            "srcProcBinaryisExecutable": "True",
            "srcProcCmdLine": "C:\\\\Windows\\\\System32\\\\svchost.exe\\" -k termsvcs -s TermService",
            "srcProcDisplayName": "Host Process for Windows Services",
            "srcProcImageMd5": "8a0a29438052faed8a2532da50455756",
            "srcProcImagePath": "C:\\\\Windows\\\\system32\\\\svchost.exe",
            "srcProcImageSha1": "a1385ce20ad79f55df235effd9780c31442aa234",
            "srcProcImageSha256": "7fd065bac18c5278777ae44908101cdfed72d26fa741367f0ad4d02020787ab6",
            "srcProcIntegrityLevel": "SYSTEM",
            "srcProcIsNative64Bit": "False",
            "srcProcIsRedirectCmdProcessor": "False",
            "srcProcIsStorylineRoot": "True",
            "srcProcName": "svchost.exe",
            "srcProcParentActiveContentFileId": null,
            "srcProcParentActiveContentHash": null,
            "srcProcParentActiveContentPath": null,
            "srcProcParentActiveContentSignedStatus": null,
            "srcProcParentActiveContentType": null,
            "srcProcParentCmdLine": "C:\\\\Windows\\\\system32\\\\services.exe",
            "srcProcParentDisplayName": "Services and Controller app",
            "srcProcParentImageMd5": "94f2383da5fa7b9717d03e33cdee5c81",
            "srcProcParentImagePath": "C:\\\\Windows\\\\system32\\\\services.exe",
            "srcProcParentImageSha1": "106a001c4c9820a6aec6a8ba17d3836525faf80e",
            "srcProcParentImageSha256": "7ef551eb51992b5f0f3c76fcf1996bca5ca8efaa87ab527f55835936165f420d",
            "srcProcParentIntegrityLevel": "SYSTEM",
            "srcProcParentIsNative64Bit": "False",
            "srcProcParentIsRedirectCmdProcessor": "False",
            "srcProcParentIsStorylineRoot": "True",
            "srcProcParentName": "services.exe",
            "srcProcParentPid": "868",
            "srcProcParentProcUid": "4B8DD1628A27EDE6",
            "srcProcParentPublisher": "MICROSOFT WINDOWS PUBLISHER",
            "srcProcParentReasonSignatureInvalid": null,
            "srcProcParentSessionId": "0",
            "srcProcParentSignedStatus": "signed",
            "srcProcParentStartTime": "2022-01-20T07:03:11.124Z",
            "srcProcParentStorylineId": "13D130A04AF01959",
            "srcProcParentUid": "4B8DD1628A27EDE6",
            "srcProcParentUser": "NT AUTHORITY\\\\SYSTEM",
            "srcProcPid": "1188",
            "srcProcPublisher": "MICROSOFT WINDOWS PUBLISHER",
            "srcProcReasonSignatureInvalid": null,
            "srcProcRelatedToThreat": "False",
            "srcProcRpid": null,
            "srcProcSessionId": "0",
            "srcProcSignedStatus": "signed",
            "srcProcStartTime": "2022-01-20T07:03:12.554Z",
            "srcProcStorylineId": "B9913CE1424F6FB2",
            "srcProcSubsystem": "SYS_WIN32",
            "srcProcTid": null,
            "srcProcUid": "0E1224C52E1F3667",
            "srcProcUser": "NT AUTHORITY\\\\NETWORK SERVICE",
            "srcProcVerifiedStatus": "verified",
            "storyline": "B9913CE1424F6FB2",
            "tgtFileCreationCount": "0",
            "tgtFileDeletionCount": "0",
            "tgtFileModificationCount": "0",
            "tiOriginalEventId": null,
            "tiOriginalEventIndex": null,
            "tiOriginalEventTraceId": null,
            "tid": null,
            "tiindicatorRelatedEventTime": null,
            "traceId": "01FT6PSXBV4SKNZ2TVW7D7TE8G",
            "trueContext": "B9913CE1424F6FB2",
            "user": "NT AUTHORITY\\\\NETWORK SERVICE",
            "verifiedStatus": "verified"                     
        }],
        "pagination": {"nextCursor": null,
        "totalItems": 1}
        }"""
        response = get_mock_response(200, obj, 'byte')
        mock_results_response.return_value = response

        search_id = "qf7a4b38c654e93d22b33017b1a0faadf"

        transmission = stix_transmission.StixTransmission('sentinelone',
                                                          self.connection(),
                                                          self.config())
        offset = 0
        length = 1
        results_response = transmission.results(search_id, offset, length)
        assert results_response is not None
        assert results_response['success'] is True
        assert 'data' in results_response
        assert results_response['data'] is not None


    @patch('stix_shifter_modules.sentinelone.stix_transmission.api_client'
           '.APIClient.get_search_results')
    def test_process_result_error(self, mock_results_response):
        """ test to check result of process """
        obj =  obj = '{"errors":[{"code":4000010,"detail":"Limit must be greater than or ' \
              'equals to 1 and less than equals to 1000"}]}'
        response = get_mock_response(400, obj)
        mock_results_response.return_value = response

        search_id = "qf7a4b38c654e93d22b33017b1a0faadf"

        transmission = stix_transmission.StixTransmission('sentinelone',
                                                          self.connection(),
                                                          self.config())
        offset = 0
        length = 1
        results_response = transmission.results(search_id, offset, length)

        assert results_response is not None
        assert results_response['success'] is False
        assert results_response['error'] is not None
        assert results_response['connector'] is not None
        assert results_response['code'] is not None

    @patch('stix_shifter_modules.sentinelone.stix_transmission.api_client'
           '.APIClient.get_search_results')
    def test_result_query_id_notfound_error(self, mock_results_response):
        """ test to check result of process """
        obj = '{"errors":[{"code":4040010,"detail":"QueryId not found"}]}'
        response = get_mock_response(404, obj)
        mock_results_response.return_value = response

        search_id = "qf7a4b38c654e93d22b33017b1a0faadf"

        transmission = stix_transmission.StixTransmission('sentinelone',
                                                          self.connection(),
                                                          self.config())
        offset = 0
        length = 1
        results_response = transmission.results(search_id, offset, length)
        assert results_response is not None
        assert results_response['success'] is False
        assert results_response['error'] is not None
        assert results_response['connector'] is not None
        assert results_response['code'] is not None

    @patch('stix_shifter_modules.sentinelone.stix_transmission.api_client'
           '.APIClient.get_search_results')
    def test_process_result_auth_error(self, mock_results_response):
        """ test to check result auth error """
        obj = '{"errors":[{"code":4010010,"detail":"Authentication failed"}]}'
        response = get_mock_response(401, obj)
        mock_results_response.return_value = response

        search_id = "qf7a4b38c654e93d22b33017b1a0faadf"

        transmission = stix_transmission.StixTransmission('sentinelone',
                                                          self.connection(),
                                                          self.config())
        offset = 0
        length = 1
        results_response = transmission.results(search_id, offset, length)

        assert results_response is not None
        assert results_response['success'] is False
        assert results_response['error'] is not None
        assert results_response['connector'] is not None
        assert results_response['code'] is not None

    @patch('stix_shifter_modules.sentinelone.stix_transmission.api_client'
           '.APIClient.get_search_results')
    def test_file_result(self, mock_results_response):
        """ test to check result of files object"""
        obj = """{"data":[{
            "activeContentFileId": null,
            "activeContentHash": null,
            "activeContentPath": null,
            "activeContentSignedStatus": null,
            "activeContentType": null,
            "agentDomain": "WORKGROUP",
            "agentGroupId": "1336793312883045044",
            "agentId": "1337419724165944028",
            "agentInfected": false,
            "agentIp": "54.91.158.243",
            "agentIsActive": false,
            "agentIsDecommissioned": false,
            "agentMachineType": "server",
            "agentName": "EC2AMAZ-IQFSLIL",
            "agentNetworkStatus": "connected",
            "agentOs": "windows",
            "agentTimestamp": "2022-01-24T18:49:35.296Z",
            "agentUuid": "f5875d2abd9f4198824885126b4f4d07",
            "agentVersion": "21.6.6.1200",
            "childProcCount": "28",
            "connectionStatus": "SUCCESS",
            "containerId": null,
            "containerImage": null,
            "containerLabels": null,
            "containerName": null,
            "createdAt": "2022-01-24T18:49:35.296000Z",
            "crossProcCount": "0",
            "crossProcDupRemoteProcHandleCount": "0",
            "crossProcDupThreadHandleCount": "0",
            "crossProcOpenProcCount": "0",
            "crossProcOutOfStorylineCount": "0",
            "crossProcThreadCreateCount": "0",
            "direction": "INCOMING",
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
            "indicatorEvasionCount": "0",
            "indicatorExploitationCount": "0",
            "indicatorGeneralCount": "48",
            "indicatorInfostealerCount": "0",
            "indicatorInjectionCount": "0",
            "indicatorPersistenceCount": "0",
            "indicatorPostExploitationCount": "0",
            "indicatorRansomwareCount": "0",
            "indicatorReconnaissanceCount": "0",
            "k8sClusterName": null,
            "k8sControllerLabels": null,
            "k8sControllerName": null,
            "k8sControllerType": null,
            "k8sNamespace": null,
            "k8sNamespaceLabels": null,
            "k8sNode": null,
            "k8sPodLabels": null,
            "k8sPodName": null,
            "metaEventName": "TCPV4",
            "moduleCount": "541721",
            "netConnCount": "180525",
            "netConnInCount": "180525",
            "netConnOutCount": "0",
            "netConnStatus": "SUCCESS",
            "netEventDirection": "INCOMING",
            "netProtocolName": "ms-wbt-server",
            "objectType": "ip",
            "osSrcChildProcCount": null,
            "osSrcCrossProcCount": null,
            "osSrcCrossProcDupRemoteProcHandleCount": null,
            "osSrcCrossProcDupThreadHandleCount": null,
            "osSrcCrossProcOpenProcCount": null,
            "osSrcCrossProcOutOfStorylineCount": null,
            "osSrcCrossProcThreadCreateCount": null,
            "osSrcDnsCount": null,
            "osSrcIndicatorBootConfigurationUpdateCount": null,
            "osSrcIndicatorEvasionCount": null,
            "osSrcIndicatorExploitationCount": null,
            "osSrcIndicatorGeneralCount": null,
            "osSrcIndicatorInfostealerCount": null,
            "osSrcIndicatorInjectionCount": null,
            "osSrcIndicatorPersistenceCount": null,
            "osSrcIndicatorPostExploitationCount": null,
            "osSrcIndicatorRansomwareCount": null,
            "osSrcIndicatorReconnaissanceCount": null,
            "osSrcModuleCount": null,
            "osSrcNetConnCount": null,
            "osSrcNetConnInCount": null,
            "osSrcNetConnOutCount": null,
            "osSrcProcActiveContentFileId": null,
            "osSrcProcActiveContentHash": null,
            "osSrcProcActiveContentPath": null,
            "osSrcProcActiveContentSignedStatus": null,
            "osSrcProcActiveContentType": null,
            "osSrcProcBinaryisExecutable": null,
            "osSrcProcCmdLine": null,
            "osSrcProcDisplayName": null,
            "osSrcProcImageMd5": null,
            "osSrcProcImagePath": null,
            "osSrcProcImageSha1": null,
            "osSrcProcImageSha256": null,
            "osSrcProcIntegrityLevel": null,
            "osSrcProcIsNative64Bit": null,
            "osSrcProcIsRedirectCmdProcessor": null,
            "osSrcProcIsStorylineRoot": null,
            "osSrcProcName": null,
            "osSrcProcParentActiveContentFileId": null,
            "osSrcProcParentActiveContentHash": null,
            "osSrcProcParentActiveContentPath": null,
            "osSrcProcParentActiveContentSignedStatus": null,
            "osSrcProcParentActiveContentType": null,
            "osSrcProcParentCmdLine": null,
            "osSrcProcParentDisplayName": null,
            "osSrcProcParentImageMd5": null,
            "osSrcProcParentImagePath": null,
            "osSrcProcParentImageSha1": null,
            "osSrcProcParentImageSha256": null,
            "osSrcProcParentIntegrityLevel": null,
            "osSrcProcParentIsNative64Bit": null,
            "osSrcProcParentIsRedirectCmdProcessor": null,
            "osSrcProcParentIsStorylineRoot": null,
            "osSrcProcParentName": null,
            "osSrcProcParentPid": null,
            "osSrcProcParentPublisher": null,
            "osSrcProcParentReasonSignatureInvalid": null,
            "osSrcProcParentSessionId": null,
            "osSrcProcParentSignedStatus": null,
            "osSrcProcParentStartTime": null,
            "osSrcProcParentStorylineId": null,
            "osSrcProcParentUid": null,
            "osSrcProcParentUser": null,
            "osSrcProcPid": null,
            "osSrcProcPublisher": null,
            "osSrcProcReasonSignatureInvalid": null,
            "osSrcProcRelatedToThreat": "False",
            "osSrcProcSessionId": null,
            "osSrcProcSignedStatus": null,
            "osSrcProcStartTime": null,
            "osSrcProcStorylineId": null,
            "osSrcProcSubsystem": null,
            "osSrcProcUid": null,
            "osSrcProcUser": null,
            "osSrcProcVerifiedStatus": null,
            "osSrcRegistryChangeCount": null,
            "osSrcTgtFileCreationCount": null,
            "osSrcTgtFileDeletionCount": null,
            "osSrcTgtFileModificationCount": null,
            "parentPid": "868",
            "parentProcessName": "services.exe",
            "parentProcessStartTime": "2022-01-20T07:03:11.124Z",
            "parentProcessUniqueKey": "0E1224C52E1F3667",
            "pid": "1188",
            "processCmd": "C:\\\\Windows\\\\System32\\\\svchost.exe\\" -k termsvcs -s TermService",
            "processDisplayName": "Host Process for Windows Services",
            "processGroupId": "B9913CE1424F6FB2",
            "processImagePath": "C:\\\\Windows\\\\system32\\\\svchost.exe",
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
            "rpid": null,
            "signatureSignedInvalidReason": null,
            "signedStatus": "signed",
            "siteId": "1336793312849490611",
            "siteName": "Default site",
            "srcIp": "87.251.64.138",
            "srcPort": 3428,
            "srcProcActiveContentFileId": null,
            "srcProcActiveContentHash": null,
            "srcProcActiveContentPath": null,
            "srcProcActiveContentSignedStatus": null,
            "srcProcActiveContentType": null,
            "srcProcBinaryisExecutable": "True",
            "srcProcCmdLine": "C:\\\\Windows\\\\System32\\\\svchost.exe -k termsvcs -s TermService",
            "srcProcDisplayName": "Host Process for Windows Services",
            "srcProcImageMd5": "8a0a29438052faed8a2532da50455756",
            "srcProcImagePath": "C:\\\\Windows\\\\system32\\\\svchost.exe",
            "srcProcImageSha1": "a1385ce20ad79f55df235effd9780c31442aa234",
            "srcProcImageSha256": "7fd065bac18c5278777ae44908101cdfed72d26fa741367f0ad4d02020787ab6",
            "srcProcIntegrityLevel": "SYSTEM",
            "srcProcIsNative64Bit": "False",
            "srcProcIsRedirectCmdProcessor": "False",
            "srcProcIsStorylineRoot": "True",
            "srcProcName": "svchost.exe",
            "srcProcParentActiveContentFileId": null,
            "srcProcParentActiveContentHash": null,
            "srcProcParentActiveContentPath": null,
            "srcProcParentActiveContentSignedStatus": null,
            "srcProcParentActiveContentType": null,
            "srcProcParentCmdLine": "C:\\\\Windows\\\\system32\\\\services.exe",
            "srcProcParentDisplayName": "Services and Controller app",
            "srcProcParentImageMd5": "94f2383da5fa7b9717d03e33cdee5c81",
            "srcProcParentImagePath": "C:\\\\Windows\\\\system32\\\\services.exe",
            "srcProcParentImageSha1": "106a001c4c9820a6aec6a8ba17d3836525faf80e",
            "srcProcParentImageSha256": "7ef551eb51992b5f0f3c76fcf1996bca5ca8efaa87ab527f55835936165f420d",
            "srcProcParentIntegrityLevel": "SYSTEM",
            "srcProcParentIsNative64Bit": "False",
            "srcProcParentIsRedirectCmdProcessor": "False",
            "srcProcParentIsStorylineRoot": "True",
            "srcProcParentName": "services.exe",
            "srcProcParentPid": "868",
            "srcProcParentProcUid": "4B8DD1628A27EDE6",
            "srcProcParentPublisher": "MICROSOFT WINDOWS PUBLISHER",
            "srcProcParentReasonSignatureInvalid": null,
            "srcProcParentSessionId": "0",
            "srcProcParentSignedStatus": "signed",
            "srcProcParentStartTime": "2022-01-20T07:03:11.124Z",
            "srcProcParentStorylineId": "13D130A04AF01959",
            "srcProcParentUid": "4B8DD1628A27EDE6",
            "srcProcParentUser": "NT AUTHORITY\\\\SYSTEM",
            "srcProcPid": "1188",
            "srcProcPublisher": "MICROSOFT WINDOWS PUBLISHER",
            "srcProcReasonSignatureInvalid": null,
            "srcProcRelatedToThreat": "False",
            "srcProcRpid": null,
            "srcProcSessionId": "0",
            "srcProcSignedStatus": "signed",
            "srcProcStartTime": "2022-01-20T07:03:12.554Z",
            "srcProcStorylineId": "B9913CE1424F6FB2",
            "srcProcSubsystem": "SYS_WIN32",
            "srcProcTid": null,
            "srcProcUid": "0E1224C52E1F3667",
            "srcProcUser": "NT AUTHORITY\\\\NETWORK SERVICE",
            "srcProcVerifiedStatus": "verified",
            "storyline": "B9913CE1424F6FB2",
            "tgtFileInternalName": null,
            "tgtFileIsExecutable": null,
            "tgtFileIsSigned": null,
            "tgtFileLocation": null,
            "tgtFileMd5": null,
            "tgtFileModificationCount": null,
            "tgtFileModifiedAt": "2022-02-21T16:24:50.666Z",
            "tgtFileOldMd5": null,
            "tgtFileOldPath": null,
            "tgtFileOldSha1": null,
            "tgtFileOldSha256": null,
            "tgtFilePath": "C:\\\\Users\\\\Administrator\\\\Downloads\\\\wildfire-test-pe-file.exe",
            "tgtFileSha1": "1b9fa754cc0546a58fcbad6478842af722a93d0e",
            "tgtFileCreationCount": "0",
            "tgtFileDeletionCount": "0",
            "tgtFileModificationCount": "0",
            "tiOriginalEventId": null,
            "tiOriginalEventIndex": null,
            "tiOriginalEventTraceId": null,
            "tid": null,
            "tiindicatorRelatedEventTime": null,
            "traceId": "01FT6PSXBV4SKNZ2TVW7D7TE8G",
            "trueContext": "B9913CE1424F6FB2",
            "user": "NT AUTHORITY\\\\NETWORK SERVICE",
            "verifiedStatus": "verified"                     
        }],
        "pagination": {"nextCursor": null,
        "totalItems": 1}
        }"""
        response = get_mock_response(200, obj, 'byte')
        mock_results_response.return_value = response

        

        search_id = "qf7a4b38c654e93d22b33017b1a0faadf"

        transmission = stix_transmission.StixTransmission('sentinelone',
                                                          self.connection(),
                                                          self.config())
        offset = 0
        length = 1
        results_response = transmission.results(search_id, offset, length)
        assert results_response is not None
        assert results_response['success'] is True
        assert 'data' in results_response
        assert results_response['data'] is not None


    @patch('stix_shifter_modules.sentinelone.stix_transmission.api_client'
           '.APIClient.create_search')
    def test_multiobject_query(self, mock_create_search):
        """ test to check query of multi object"""
        obj = """{"data":{"queryId":"qf7a4b38c654e93d22b33017b1a0faadf"}}"""
        response = get_mock_response(200, obj, 'byte')
        mock_create_search.return_value = response

        query = json.dumps('{"query": "(SrcProcName In Contains (\\"host.exe\\") and EventTime ' \
                'BETWEEN \\"2022-01-02T18:49:35.296Z\\" AND \\"2022-02-18T18:49:35.296Z\\") or '
                '(TgtFilePath  In Contains (\\"wildfire\\")  and EventTime '
                'BETWEEN "\\2022-01-02T18:49:35.296Z\\" AND "\\2022-02-24T18:49:35.296Z\\")",' \
                '"limit": 1, "toDate": "2022-02-22T04:49:26.257525Z", '
                '"fromDate": "2022-02-10T04:49:26.257525Z" }')

        transmission = stix_transmission.StixTransmission('sentinelone',
                                                          self.connection(),
                                                          self.config())
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert query_response['search_id'] is not None
        assert query_response['search_id'] == 'qf7a4b38c654e93d22b33017b1a0faadf'


    @patch('stix_shifter_modules.sentinelone.stix_transmission.api_client'
           '.APIClient.create_search')
    def test_multiobject_query_parseerror(self, mock_create_search):
        """ test to check query of multi object error"""
        obj = """{"data":{"queryId":"test"n}}"""
        response = get_mock_response(200, obj)
        mock_create_search.return_value = response

        query = json.dumps('{"query": "(SrcProcName In Contains (\\"host.exe\\") and EventTime ' \
                           'BETWEEN \\"2022-01-02T18:49:35.296Z\\" AND \\"2022-02-18T18:49:35.296Z\\") or '
                           '(TgtFilePath  In Contains (\\"wildfire\\")  and EventTime '
                           'BETWEEN "\\2022-01-02T18:49:35.296Z\\" ANDDD "\\2022-02-24T18:49:35.296Z\\")",' \
                           '"limit": 1, "toDate": "2022-02-22T04:49:26.257525Z", '
                           '"fromDate": "2022-02-10T04:49:26.257525Z" }')

        transmission = stix_transmission.StixTransmission('sentinelone',
                                                          self.connection(),
                                                          self.config())
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is False
        assert query_response['error'] is not None
        assert query_response['connector'] is not None
        assert query_response['code'] is not None

    @patch('stix_shifter_modules.sentinelone.stix_transmission.api_client'
           '.APIClient.get_search_results')
    def test_multiobject_result(self, mock_results_response):
        """ test to check result of multi object"""
        obj = """{"data":[{
            "activeContentFileId": null,
            "activeContentHash": null,
            "activeContentPath": null,
            "activeContentSignedStatus": null,
            "activeContentType": null,
            "agentDomain": "WORKGROUP",
            "agentGroupId": "1336793312883045044",
            "agentId": "1337419724165944028",
            "agentInfected": false,
            "agentIp": "54.91.158.243",
            "agentIsActive": false,
            "agentIsDecommissioned": false,
            "agentMachineType": "server",
            "agentName": "EC2AMAZ-IQFSLIL",
            "agentNetworkStatus": "connected",
            "agentOs": "windows",
            "agentTimestamp": "2022-01-24T18:49:35.296Z",
            "agentUuid": "f5875d2abd9f4198824885126b4f4d07",
            "agentVersion": "21.6.6.1200",
            "childProcCount": "28",
            "connectionStatus": "SUCCESS",
            "containerId": null,
            "containerImage": null,
            "containerLabels": null,
            "containerName": null,
            "createdAt": "2022-01-24T18:49:35.296000Z",
            "crossProcCount": "0",
            "crossProcDupRemoteProcHandleCount": "0",
            "crossProcDupThreadHandleCount": "0",
            "crossProcOpenProcCount": "0",
            "crossProcOutOfStorylineCount": "0",
            "crossProcThreadCreateCount": "0",
            "direction": "INCOMING",
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
            "indicatorEvasionCount": "0",
            "indicatorExploitationCount": "0",
            "indicatorGeneralCount": "48",
            "indicatorInfostealerCount": "0",
            "indicatorInjectionCount": "0",
            "indicatorPersistenceCount": "0",
            "indicatorPostExploitationCount": "0",
            "indicatorRansomwareCount": "0",
            "indicatorReconnaissanceCount": "0",
            "k8sClusterName": null,
            "k8sControllerLabels": null,
            "k8sControllerName": null,
            "k8sControllerType": null,
            "k8sNamespace": null,
            "k8sNamespaceLabels": null,
            "k8sNode": null,
            "k8sPodLabels": null,
            "k8sPodName": null,
            "metaEventName": "TCPV4",
            "moduleCount": "541721",
            "netConnCount": "180525",
            "netConnInCount": "180525",
            "netConnOutCount": "0",
            "netConnStatus": "SUCCESS",
            "netEventDirection": "INCOMING",
            "netProtocolName": "ms-wbt-server",
            "objectType": "ip",
            "osSrcChildProcCount": null,
            "osSrcCrossProcCount": null,
            "osSrcCrossProcDupRemoteProcHandleCount": null,
            "osSrcCrossProcDupThreadHandleCount": null,
            "osSrcCrossProcOpenProcCount": null,
            "osSrcCrossProcOutOfStorylineCount": null,
            "osSrcCrossProcThreadCreateCount": null,
            "osSrcDnsCount": null,
            "osSrcIndicatorBootConfigurationUpdateCount": null,
            "osSrcIndicatorEvasionCount": null,
            "osSrcIndicatorExploitationCount": null,
            "osSrcIndicatorGeneralCount": null,
            "osSrcIndicatorInfostealerCount": null,
            "osSrcIndicatorInjectionCount": null,
            "osSrcIndicatorPersistenceCount": null,
            "osSrcIndicatorPostExploitationCount": null,
            "osSrcIndicatorRansomwareCount": null,
            "osSrcIndicatorReconnaissanceCount": null,
            "osSrcModuleCount": null,
            "osSrcNetConnCount": null,
            "osSrcNetConnInCount": null,
            "osSrcNetConnOutCount": null,
            "osSrcProcActiveContentFileId": null,
            "osSrcProcActiveContentHash": null,
            "osSrcProcActiveContentPath": null,
            "osSrcProcActiveContentSignedStatus": null,
            "osSrcProcActiveContentType": null,
            "osSrcProcBinaryisExecutable": null,
            "osSrcProcCmdLine": null,
            "osSrcProcDisplayName": null,
            "osSrcProcImageMd5": null,
            "osSrcProcImagePath": null,
            "osSrcProcImageSha1": null,
            "osSrcProcImageSha256": null,
            "osSrcProcIntegrityLevel": null,
            "osSrcProcIsNative64Bit": null,
            "osSrcProcIsRedirectCmdProcessor": null,
            "osSrcProcIsStorylineRoot": null,
            "osSrcProcName": null,
            "osSrcProcParentActiveContentFileId": null,
            "osSrcProcParentActiveContentHash": null,
            "osSrcProcParentActiveContentPath": null,
            "osSrcProcParentActiveContentSignedStatus": null,
            "osSrcProcParentActiveContentType": null,
            "osSrcProcParentCmdLine": null,
            "osSrcProcParentDisplayName": null,
            "osSrcProcParentImageMd5": null,
            "osSrcProcParentImagePath": null,
            "osSrcProcParentImageSha1": null,
            "osSrcProcParentImageSha256": null,
            "osSrcProcParentIntegrityLevel": null,
            "osSrcProcParentIsNative64Bit": null,
            "osSrcProcParentIsRedirectCmdProcessor": null,
            "osSrcProcParentIsStorylineRoot": null,
            "osSrcProcParentName": null,
            "osSrcProcParentPid": null,
            "osSrcProcParentPublisher": null,
            "osSrcProcParentReasonSignatureInvalid": null,
            "osSrcProcParentSessionId": null,
            "osSrcProcParentSignedStatus": null,
            "osSrcProcParentStartTime": null,
            "osSrcProcParentStorylineId": null,
            "osSrcProcParentUid": null,
            "osSrcProcParentUser": null,
            "osSrcProcPid": null,
            "osSrcProcPublisher": null,
            "osSrcProcReasonSignatureInvalid": null,
            "osSrcProcRelatedToThreat": "False",
            "osSrcProcSessionId": null,
            "osSrcProcSignedStatus": null,
            "osSrcProcStartTime": null,
            "osSrcProcStorylineId": null,
            "osSrcProcSubsystem": null,
            "osSrcProcUid": null,
            "osSrcProcUser": null,
            "osSrcProcVerifiedStatus": null,
            "osSrcRegistryChangeCount": null,
            "osSrcTgtFileCreationCount": null,
            "osSrcTgtFileDeletionCount": null,
            "osSrcTgtFileModificationCount": null,
            "parentPid": "868",
            "parentProcessName": "services.exe",
            "parentProcessStartTime": "2022-01-20T07:03:11.124Z",
            "parentProcessUniqueKey": "0E1224C52E1F3667",
            "pid": "1188",
            "processCmd": "C:\\\\Windows\\\\System32\\\\svchost.exe -k termsvcs -s TermService",
            	   "processDisplayName": "Host Process for Windows Services",
            "processGroupId": "B9913CE1424F6FB2",
            "processImagePath": "C:\\\\Windows\\\\system32\\\\svchost.exe",
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
            "rpid": null,
            "signatureSignedInvalidReason": null,
            "signedStatus": "signed",
            "siteId": "1336793312849490611",
            "siteName": "Default site",
            "srcIp": "87.251.64.138",
            "srcPort": 3428,
            "srcProcActiveContentFileId": null,
            "srcProcActiveContentHash": null,
            "srcProcActiveContentPath": null,
            "srcProcActiveContentSignedStatus": null,
            "srcProcActiveContentType": null,
            "srcProcBinaryisExecutable": "True",
            "srcProcCmdLine": "C:\\\\Windows\\\\System32\\\\svchost.exe -k termsvcs -s TermService",
            "srcProcDisplayName": "Host Process for Windows Services",
            "srcProcImageMd5": "8a0a29438052faed8a2532da50455756",
            "srcProcImagePath": "C:\\\\Windows\\\\system32\\\\svchost.exe",
            "srcProcImageSha1": "a1385ce20ad79f55df235effd9780c31442aa234",
            "srcProcImageSha256": "7fd065bac18c5278777ae44908101cdfed72d26fa741367f0ad4d02020787ab6",
            "srcProcIntegrityLevel": "SYSTEM",
            "srcProcIsNative64Bit": "False",
            "srcProcIsRedirectCmdProcessor": "False",
            "srcProcIsStorylineRoot": "True",
            "srcProcName": "svchost.exe",
            "srcProcParentActiveContentFileId": null,
            "srcProcParentActiveContentHash": null,
            "srcProcParentActiveContentPath": null,
            "srcProcParentActiveContentSignedStatus": null,
            "srcProcParentActiveContentType": null,
            "srcProcParentCmdLine": "C:\\\\Windows\\\\system32\\\\services.exe",
            "srcProcParentDisplayName": "Services and Controller app",
            "srcProcParentImageMd5": "94f2383da5fa7b9717d03e33cdee5c81",
            "srcProcParentImagePath": "C:\\\\Windows\\\\system32\\\\services.exe",
            "srcProcParentImageSha1": "106a001c4c9820a6aec6a8ba17d3836525faf80e",
            "srcProcParentImageSha256": "7ef551eb51992b5f0f3c76fcf1996bca5ca8efaa87ab527f55835936165f420d",
            "srcProcParentIntegrityLevel": "SYSTEM",
            "srcProcParentIsNative64Bit": "False",
            "srcProcParentIsRedirectCmdProcessor": "False",
            "srcProcParentIsStorylineRoot": "True",
            "srcProcParentName": "services.exe",
            "srcProcParentPid": "868",
            "srcProcParentProcUid": "4B8DD1628A27EDE6",
            "srcProcParentPublisher": "MICROSOFT WINDOWS PUBLISHER",
            "srcProcParentReasonSignatureInvalid": null,
            "srcProcParentSessionId": "0",
            "srcProcParentSignedStatus": "signed",
            "srcProcParentStartTime": "2022-01-20T07:03:11.124Z",
            "srcProcParentStorylineId": "13D130A04AF01959",
            "srcProcParentUid": "4B8DD1628A27EDE6",
            "srcProcParentUser": "NT AUTHORITY\\\\SYSTEM",
            "srcProcPid": "1188",
            "srcProcPublisher": "MICROSOFT WINDOWS PUBLISHER",
            "srcProcReasonSignatureInvalid": null,
            "srcProcRelatedToThreat": "False",
            "srcProcRpid": null,
            "srcProcSessionId": "0",
            "srcProcSignedStatus": "signed",
            "srcProcStartTime": "2022-01-20T07:03:12.554Z",
            "srcProcStorylineId": "B9913CE1424F6FB2",
            "srcProcSubsystem": "SYS_WIN32",
            "srcProcTid": null,
            "srcProcUid": "0E1224C52E1F3667",
            "srcProcUser": "NT AUTHORITY\\\\NETWORK SERVICE",
            "srcProcVerifiedStatus": "verified",
            "storyline": "B9913CE1424F6FB2",
            "tgtFileCreationCount": "0",
            "tgtFileDeletionCount": "0",
            "tgtFileModificationCount": "0",
            "tiOriginalEventId": null,
            "tiOriginalEventIndex": null,
            "tiOriginalEventTraceId": null,
            "tid": null,
            "tiindicatorRelatedEventTime": null,
            "traceId": "01FT6PSXBV4SKNZ2TVW7D7TE8G",
            "trueContext": "B9913CE1424F6FB2",
            "user": "NT AUTHORITY\\\\NETWORK SERVICE",
            "verifiedStatus": "verified"                     
        }]}"""
        response = get_mock_response(200, obj, 'byte')
        mock_results_response.return_value = response

        search_id = "qf7a4b38c654e93d22b33017b1a0faadf"

        transmission = stix_transmission.StixTransmission('sentinelone',
                                                          self.connection(),
                                                          self.config())
        offset = 0
        length = 1
        results_response = transmission.results(search_id, offset, length)

        assert results_response is not None
        assert results_response['success'] is True
        assert 'data' in results_response
        assert results_response['data'] is not None


    @patch('stix_shifter_modules.sentinelone.stix_transmission.api_client'
           '.APIClient.get_search_results')
    def test_multiobject_result_parseerror(self, mock_results_response):
        """ test to check result of multi object parse error"""
        obj = """{"data":[{
                "activeContentFileId": null,
                "activeContentHash": null,
                "activeContentPath": null,
                "activeContentSignedStatus": null,
                "activeContentType": null,
                "agentDomain": "WORKGROUP",
                "agentGroupId": "1336793312883045044",
                "agentId": "1337419724165944028",
                "agentInfected": false,
                "agentIp": "54.91.158.243",
                "agentIsActive": false,
                "agentIsDecommissioned": false,
                "agentMachineType": "server",
                "agentName": "EC2AMAZ-IQFSLIL",
                "agentNetworkStatus": "connected",
                "agentOs": "windows",
                "agentTimestamp": "2022-01-24T18:49:35.296Z",
                "agentUuid": "f5875d2abd9f4198824885126b4f4d07",
                "agentVersion": "21.6.6.1200",
                "childProcCount": "28",
                "connectionStatus": "SUCCESS",
                }"""
        response = get_mock_response(200, obj)
        mock_results_response.return_value = response

        search_id = "qf7a4b38c654e93d22b33017b1a0faadf"

        transmission = stix_transmission.StixTransmission('sentinelone',
                                                          self.connection(),
                                                          self.config())
        offset = 0
        length = 1
        results_response = transmission.results(search_id, offset, length)

        assert results_response is not None
        assert results_response['success'] is False
        assert results_response['error'] is not None
        assert results_response['connector'] is not None
        assert results_response['code'] is not None


    @patch('stix_shifter_modules.sentinelone.stix_transmission.api_client.APIClient.get_search_status')
    def test_search_status(self, mock_status_response):
        """ test to check query status function"""

        obj = """{"data":{"progressStatus":"100","responseState":"FINISHED"}}"""
        response = get_mock_response(200, obj, 'byte')
        mock_status_response.return_value = response

        search_id = "qf7a4b38c654e93d22b33017b1a0faadf"

        transmission = stix_transmission.StixTransmission('sentinelone',
                                                          self.connection(),
                                                          self.config())
        ping_response = transmission.status(search_id)
        assert ping_response is not None
        assert ping_response['success'] is True
        assert ping_response['status'] is not None

 
    @patch('stix_shifter_modules.sentinelone.stix_transmission.api_client'
           '.APIClient.get_search_status')
    def test_search_status_Running(self, mock_status_response):
        """ test to check query status function"""
        obj = """{"data":{"progressStatus":"60","responseState":"RUNNING"}}"""
        response = get_mock_response(200, obj, 'byte')
        mock_status_response.return_value = response
        
        search_id = "qf7a4b38c654e93d22b33017b1a0faadf"

        transmission = stix_transmission.StixTransmission('sentinelone',
                                                          self.connection(),
                                                          self.config())
        ping_response = transmission.status(search_id)
        assert ping_response is not None
        assert ping_response['success'] is True
        assert ping_response['status'] is not None


    @patch('stix_shifter_modules.sentinelone.stix_transmission.api_client'
           '.APIClient.get_search_status')
    def test_search_status_notfound_error(self, mock_status_response):
        """ test to check query status error function"""
        obj = """{"errors":[{"code":4040010,"detail":"Query Not Found"}]}"""
        response = get_mock_response(404, obj)
        mock_status_response.return_value = response

        search_id = "test"

        transmission = stix_transmission.StixTransmission('sentinelone',
                                                          self.connection(),
                                                          self.config())
        ping_response = transmission.status(search_id)
        assert ping_response is not None
        assert ping_response['success'] is False
        assert ping_response['error'] is not None
        assert ping_response['connector'] is not None
        assert ping_response['code'] is not None

    @patch('stix_shifter_modules.sentinelone.stix_transmission.api_client'
           '.APIClient.get_search_status')
    def test_search_status_error(self, mock_status_response):
        """ test to check query status error function"""
        obj = """{"errors":"test"n}"""
        response = get_mock_response(404, obj)
        mock_status_response.return_value = response

        search_id = "test"

        transmission = stix_transmission.StixTransmission('sentinelone',
                                                          self.connection(),
                                                          self.config())
        ping_response = transmission.status(search_id)
        assert ping_response is not None
        assert ping_response['success'] is False
        assert ping_response['error'] is not None
        assert ping_response['connector'] is not None
        assert ping_response['code'] is not None

    @patch('stix_shifter_modules.sentinelone.stix_transmission.api_client'
           '.APIClient.get_search_status')
    def test_search_status_auth_error(self, mock_status_response):
        """ test to check query status auth error """
        obj = '{"errors":[{"code":4010010,"detail":"Authentication failed"}]}'
        response = get_mock_response(401, obj)
        mock_status_response.return_value = response

        search_id = "test"

        transmission = stix_transmission.StixTransmission('sentinelone',
                                                          self.connection(),
                                                          self.config())
        ping_response = transmission.status(search_id)
        assert ping_response is not None
        assert ping_response['success'] is False
        assert ping_response['error'] is not None
        assert ping_response['connector'] is not None
        assert ping_response['code'] is not None

    @patch('stix_shifter_modules.sentinelone.stix_transmission.api_client'
           '.APIClient.delete_search')
    def test_delete_search(self, mock_status_response):
        """ test to check query cancel function"""

        response = {"code":200,"success": True}
        mock_status_response.return_value = response

        search_id = "qf7a4b38c654e93d22b33017b1a0faadf"

        transmission = stix_transmission.StixTransmission('sentinelone',
                                                          self.connection(),
                                                          self.config())
        ping_response = transmission.delete(search_id)
        assert ping_response is not None
        assert ping_response['success'] is True
        assert ping_response['message'] is not None


    @patch('stix_shifter_modules.sentinelone.stix_transmission.api_client'
           '.APIClient.delete_search')
    def test_delete_queryparse_error(self, mock_status_response):
        """ test to check query status parse error"""
        obj = """{"errors":"test"n}"""
        mock_status_response.return_value = obj
        search_id = "test"

        transmission = stix_transmission.StixTransmission('sentinelone',
                                                          self.connection(),
                                                          self.config())
        ping_response = transmission.delete(search_id)
        assert ping_response is not None
        assert ping_response['success'] is False
        assert ping_response['error'] is not None


    @patch('stix_shifter_modules.sentinelone.stix_transmission.api_client'
           '.APIClient.ping_datasource')
    def test_ping_maxretried_error(self, mock_ping_source):
        """ test to check ping_data_source function"""
        mock_ping_source.side_effect = Exception('Max retries exceeded')

        transmission = stix_transmission.StixTransmission('sentinelone',
                                                          self.connection(),
                                                          self.config())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert ping_response['error'] is not None
        assert ping_response['connector'] is not None
        assert ping_response['code'] is not None

    @patch('stix_shifter_modules.sentinelone.stix_transmission.api_client'
           '.APIClient.get_search_status')
    def test_search_status_maxretried_error(self, mock_status_response):
        """ test to check query status function"""
        #obj = """{"data":{"progressStatus":"100","responseState":"FINISHED"}}"""
        #response = get_mock_response(200, obj)
        #mock_status_response.return_value = response
        mock_status_response.side_effect = Exception('Max retries exceeded')

        search_id = "qf7a4b38c654e93d22b33017b1a0faadf"

        transmission = stix_transmission.StixTransmission('sentinelone',
                                                          self.connection(),
                                                          self.config())
        ping_response = transmission.status(search_id)
        assert ping_response is not None
        assert ping_response['status'] == "RUNNING"
        assert ping_response['progress'] is not None

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_invalid_host_ping(self, mock_ping):
        """Test Invalid host"""
        mock_ping.side_effect = ClientConnectionError("Invalid Host")
        transmission = stix_transmission.StixTransmission('sentinelone', self.connection(), self.config())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert "Invalid Host" in ping_response['error']
        assert ping_response['connector'] is not None
        assert ping_response['code'] is not None

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_invalid_host_status(self, mock_ping):
        """Test Invalid host"""
        mock_ping.side_effect = ClientConnectionError("Invalid Host")
        transmission = stix_transmission.StixTransmission('sentinelone', self.connection(), self.config())
        search_id = "test"
        ping_response = transmission.status(search_id)
        assert ping_response is not None
        assert ping_response['success'] is False
        assert "Invalid Host" in ping_response['error']
        assert ping_response['connector'] is not None
        assert ping_response['code'] is not None

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_invalid_host_query(self, mock_create_search):
        """ test to check query of process """

        """Test Invalid host"""
        mock_create_search.side_effect = ClientConnectionError("Invalid Host")
        transmission = stix_transmission.StixTransmission('sentinelone', self.connection(), self.config())

        query = json.dumps('{"query": "(SrcProcName In Contains (\\"host.exe\\") and EventTime ' \
                           'BETWEEN \\"2022-01-02T18:49:35.296Z\\" AND \\"2022-02-18T18:49:35.296Z\\")",' \
                           '"limit": 1, "toDate": "2022-02-22T04:49:26.257525Z", "fromDate": "2022-02-10T04:49:26.257525Z" }')

        transmission = stix_transmission.StixTransmission('sentinelone',
                                                          self.connection(),
                                                          self.config())
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is False
        assert "Invalid Host" in query_response['error']
        assert query_response['connector'] is not None
        assert query_response['code'] is not None

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_invalid_host_result(self, mock_result):
        """Test Invalid host"""
        mock_result.side_effect = ClientConnectionError("Invalid Host")
        transmission = stix_transmission.StixTransmission('sentinelone', self.connection(), self.config())

        search_id = "test"

        transmission = stix_transmission.StixTransmission('sentinelone',
                                                          self.connection(),
                                                          self.config())
        offset = 0
        length = 1
        results_response = transmission.results(search_id, offset, length)

        assert results_response is not None
        assert results_response['success'] is False
        assert "Invalid Host" in results_response['error']
        assert results_response['connector'] is not None
        assert results_response['code'] is not None
