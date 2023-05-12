import json
from stix_shifter_modules.intezer.stix_transmission.ping_connector import PingConnector
from stix_shifter.stix_transmission import stix_transmission
from stix_shifter_modules.intezer.stix_transmission.results_connector import ResultsConnector
from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import ResponseWrapper
from unittest.mock import patch
from collections import namedtuple
import unittest
from unittest.mock import AsyncMock

namespace = "82345bf42ea1-e30d-41a2-a3ee-1aec759cf"
hash_value = '16cda323189d8eba4248c0a2f5ad0d8f'
SAMPLE_DATA = '{"data": "16cda323189d8eba4248c0a2f5ad0d8f", "dataType": "hash"}'
SAMPLE_DATA_URL = '{"data": "google.com", "dataType": "url"}'
MODULE_NAME = 'intezer'
DATA = {
    "code": 200,
    "data":
        {
            "analysis_url": "https://analyze.intezer.com/analyses/8b9f2363-fdca-4cce-9e20-93f8ca1dd88f",
            "code": 200,
            "report": [
                {
                    "analysis_id": "8b9f2363-fdca-4cce-9e20-93f8ca1dd88f",
                    "analysis_time": "Tue, 22 Feb 2022 07:41:53 GMT",
                    "analysis_url": "https://analyze.intezer.com/analyses/8b9f2363-fdca-4cce-9e20-93f8ca1dd88f",
                    "family_id": "4b6a00eb-3052-4b54-b1a3-4df563375ff3",
                    "family_name": "Carbanak",
                    "is_private": False,
                    "sha256": "b28531feb7299e60eabd01b20c1f1e9f79b9f72cbb58bf3df1ccd14e08dbf953",
                    "sub_verdict": "known_malicious",
                    "verdict": "malicious",
                    "iocs": {},
                    "dynamic_ttps": {},
                    "code_reuse": {
                        "common_gene_count": 0,
                        "families": [
                            {
                                "family_id": "4b6a00eb-3052-4b54-b1a3-4df563375ff3",
                                "family_name": "Carbanak",
                                "family_type": "malware",
                                "reused_gene_count": 15
                            }
                        ],
                        "gene_count": 15,
                        "gene_type": "native_windows",
                        "unique_gene_count": 0
                    }
                }
            ],
            "dataType": "hash",
            "namespace": "9d4bedaf-d351-4f50-930f-f8eb121e5bae1",
            "external_reference": {
                "source_name": "Intezer_Connector",
                "url": "https://analyze.intezer.com/analyses/8b9f2363-fdca-4cce-9e20-93f8ca1dd88f"
            }
        }
}
QUERY_DATA = {
    'result': {
        'analysis_id': 'a4cfa095-032f-4eab-9580-ee16a290a75e', 
        'analysis_time': 'Fri, 21 Apr 2023 20:38:37 GMT', 
        'analysis_url': 'https://analyze.intezer.com/url/a4cfa095-032f-4eab-9580-ee16a290a75e', 
        'api_void_risk_score': 0, 
        'certificate': {
            'issuer': 'GTS CA 1C3', 
            'protocol': 'TLS 1.3', 
            'subject_name': 'www.google.com', 
            'valid_from': '2023-04-03 08:25:07.000000', 
            'valid_to': '2023-06-26 08:25:06.000000'
        }, 
        'domain_info': {
            'creation_date': '1997-09-15 07:00:00.000000', 
            'domain_name': 'google.com', 
            'registrar': 'MarkMonitor, Inc.'
        }, 
        'indicators': [{
            'classification': 'informative', 
            'text': 'Valid https'
        }, 
        {
            'classification': 'informative', 
            'text': 'URL is accessible'
        }, 
        {
            'classification': 'informative', 
            'text': 'Assigned IPv4 domain'
        }, 
        {
            'classification': 'informative', 
            'text': 'Vaild IPv4 domain'
        }], 
        'ip': '2a00:1450:4001:82f::2004', 
        'redirect_chain': [{'response_status': 301, 'url': 'http://google.com/'}, 
        {'response_status': 302, 'url': 'http://www.google.com/'}, 
        {'response_status': 200, 'url': 'https://www.google.com/?gws_rd=ssl'}], 
        'scanned_url': 'https://www.google.com/?gws_rd=ssl', 
        'submitted_url': 'http://google.com', 
        'summary': {'description': 'No suspicious activity was detected for this URL', 'main_connection_gene_count': 0, 'main_connection_gene_percentage': 0.0, 'title': 'No Threats', 'verdict_name': 'no_threats', 'verdict_type': 'no_threats'}, 
        'verdict': 'no_threats'
    }, 
    'result_url': '/url/a4cfa095-032f-4eab-9580-ee16a290a75e', 
    'code': 200
}

Response = namedtuple('Response', ['data', 'response_code'])
connection = {
    "namespace":namespace
}
config = {
    "auth": {
        "key": "testkey"
    }
}

class MockHttpResponse:
    def __init__(self, string):
        self.string = string

    def decode(self, string):
        return self.string

class IntezerHttpResponse:
    def __init__(self, obj, response_code):
        self.code = response_code
        self.object = obj    

    def read(self):
        return self.object
class MockResponsejson:
    def __init__(self, json_data, status_code):
        self.content = str.encode(json.dumps(json_data))
        self.status_code = status_code

class ResponseWrapper:
    def __init__(self, obj, code):
        self.object = str.encode(json.dumps(obj))
        self.code = code

    def read(self):
        return self.object

@patch('stix_shifter_modules.intezer.stix_transmission.api_client.APIClient', autospec=True)
class TestIntezerConnection(unittest.TestCase, object):
    
    @patch('stix_shifter_modules.intezer.stix_transmission.api_client.APIClient.ping_intezer')
    def test_intezer_ping_exception(self, mock_ping_response, mock_api_client):
        response =  MockHttpResponse('/exception')
        mock_api_client.return_value = None
        mock_ping_response.return_value = IntezerHttpResponse(response, 400)
        mock_ping_response.side_effect = Exception('an error occured retriving ping information')

        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False

    async def test_intezer_results(self, mock_api_client):
        mock_api_client.get_search_results.return_value = DATA, namespace

        search_results = ResultsConnector(mock_api_client)
        search_results_response = await search_results.create_results_connection(query_data=SAMPLE_DATA, offset=1, length=1)
        report = search_results_response['data'][0]
        
        assert 'code' in report
        assert 'data' in report
        assert 'dataType' in report
        assert 'report' in report
        assert 'success' in search_results_response
        assert search_results_response['success'] is True
        assert type(search_results_response['data']) is list

    @patch('stix_shifter_modules.intezer.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    def test_Intezer_results_error(self, mock_result_connection, mock_api_client):
        mock_api_client.return_value = None
        mock_data = DATA = {
            "error": "Invalid",
            "success": False,
            "code": 400
        }
        mock_result_connection.return_value = mock_data, namespace
        mock_result_connection.side_effect = Exception('an error occured retriving ping information')
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.query(SAMPLE_DATA)

        assert query_response is not None
        assert 'search_id' in query_response
        assert query_response['search_id'] == SAMPLE_DATA

        search_results_response = transmission.results(query_response['search_id'], 0, 9)
        
        assert 'success' in search_results_response
        assert search_results_response['success'] is False
        assert 'code' in search_results_response, search_results_response['code'] == 'invalid_query'


    def test_intezer_status(self, mock_api_client):
        mock_api_client.return_value = None
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.status(SAMPLE_DATA)
        assert query_response is not None
        assert 'success' in query_response, query_response['success'] is True
        assert 'status' in query_response, query_response['status'] == 'COMPLETED'
        assert 'progress' in query_response, query_response['progress'] == 100
    
    @patch('stix_shifter_utils.modules.base.stix_transmission.base_sync_connector.BaseSyncConnector.create_status_connection', autospec=True)
    def test_intezer_status_exception(self, mock_status_response, mock_api_client):
        error_msg = 'an error occured while checking the status'
        mock_api_client.return_value = None
        mock_status_response.return_value = {'status':'FAILED', 'success':False}
        mock_status_response.side_effect = Exception(error_msg)
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.status(SAMPLE_DATA)
        assert query_response is not None
        assert 'success' in query_response, query_response['success'] is False
        assert 'error' in query_response, query_response['error'] == error_msg
            
    @patch('stix_shifter_utils.modules.base.stix_transmission.base_sync_connector.BaseSyncConnector.create_query_connection', autospec=True)
    def test_Intezer_query_exception(self, mock_query_response, mock_api_client):
        error_msg = 'cannot create a query connection'
        mock_api_client.return_value = None
        mock_query_response.return_value = {'search_id':'', 'success':False}
        mock_query_response.side_effect = Exception(error_msg)
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.query(SAMPLE_DATA)
        assert query_response is not None
        assert 'success' in query_response, query_response['success'] is False
        assert 'error' in query_response, query_response['error'] == error_msg
    
    def test_Intezer_is_async_query(self, mock_api_client):
        mock_api_client.return_value = None
        transmission = stix_transmission.StixTransmission("abc",  connection, config)
        is_async_result = transmission.is_async()
        assert 'success' in is_async_result
        assert is_async_result['success'] is False
        assert 'code' in is_async_result, is_async_result['code'] == 'unknown'

    @patch('stix_shifter_utils.utils.base_entry_point.BaseEntryPoint.is_async', autospec=True)
    def test_Intezer_is_async_query_exception(self, mock_async_response, mock_api_client):
        error_msg = 'an error occured while checking the if the query is async'
        mock_api_client.return_value = None
        mock_async_response.return_value = False
        mock_async_response.side_effect = Exception(error_msg)
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.is_async()
        assert query_response is not None
        assert 'success' in query_response, query_response['success'] is False
        assert 'error' in query_response, query_response['error'] == error_msg

    def test_delete_query(self, mock_api_client):
        mock_api_client.return_value = None
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.delete(SAMPLE_DATA)

        assert query_response is not None
        assert 'success' in query_response
        assert query_response['success'] is False
    
    
    @patch('stix_shifter_modules.intezer.stix_transmission.api_client.APIClient.delete_search', autospec=True)
    def test_delete_query_exception(self, mock_delete_response, mock_api_client):
        error_msg = 'an error occured while checking the if the query is deleted'
        mock_api_client.return_value = None
        mock_delete_response.return_value = False
        mock_delete_response.side_effect = Exception(error_msg)
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.delete("")
        assert 'success' in query_response, query_response['success'] is False
        assert 'error' in query_response, query_response['error'] == error_msg

class TestMockingDemo(unittest.IsolatedAsyncioTestCase):
    async def test_intezer_total_ping(self):
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        ping_response = await transmission.ping_async()
        assert ping_response is not None
        assert ping_response['success'] is True
        assert 'code' in ping_response and ping_response['code'] == 200
        assert 'connector' in ping_response and ping_response['connector'] == 'intezer'

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api', autospec=True)
    async def test_intezer_get_search_results_hash(self, mock_call_api):
        request_token = {"code": 200, "result": "unitTest Token"}
        mock_call_api.side_effect = [ResponseWrapper(request_token, 200), ResponseWrapper(DATA, 200)]
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        results_response = await transmission.results_async(SAMPLE_DATA, 1, 1)
        assert results_response is not None
        assert results_response['success'] is False
        assert 'code' in results_response and results_response['code'] == 'unknown'
        assert 'connector' in results_response and results_response['connector'] == 'intezer'

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api', autospec=True)
    async def test_intezer_get_search_results_url(self, mock_call_api):
        request_token = {"code": 200, "result": "unitTest Token"}
        mock_call_api.side_effect = [
            ResponseWrapper(request_token, 200), 
            ResponseWrapper(QUERY_DATA, 201),
            ResponseWrapper(QUERY_DATA, 200),
            ResponseWrapper({}, 200),
            ResponseWrapper({}, 200),
            ]
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        results_response = await transmission.results_async(SAMPLE_DATA_URL, 1, 1)
        assert results_response is not None
        assert results_response['success'] is False
        assert 'code' in results_response and results_response['code'] == 'unknown'
        assert 'connector' in results_response and results_response['connector'] == 'intezer'

    async def test_intezer_get_search_results_errors(self):
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        results_response = await transmission.results_async(SAMPLE_DATA, 1, 1)
        assert results_response is not None
        assert results_response['success'] is False
        assert 'code' in results_response and results_response['code'] == 400
        assert 'connector' in results_response and results_response['connector'] == 'intezer'

        results_response = await transmission.results_async(SAMPLE_DATA_URL, 1, 1)
        assert results_response is not None
        assert results_response['success'] is False
        assert 'code' in results_response and results_response['code'] == 400
        assert 'connector' in results_response and results_response['connector'] == 'intezer'

