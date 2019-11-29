import requests_mock
from stix_shifter.stix_transmission.src.modules.security_advisor import security_advisor_connector
from stix_shifter.stix_transmission.src.modules.security_advisor import security_advisor_auth
from unittest.mock import patch
import unittest
from stix_shifter.stix_transmission import stix_transmission


class SecurityAdvisorMockJsonResponse:
    def __init__(self, response_code, obj):
        self.code = response_code
        self.object = obj.encode()

    def read(self):
        return self.object


class MockHttpResponse:
    def __init__(self, string):
        self.string = string

    def decode(self, string):
        return self.string

CONFIG = {
    "auth": {
        "accountID": "abc",
        "apiKey": "xyz"
    }
}

CONNECTION = {
    "host": "http://test_sec_adv.com",
}

class TestSecurityAdvisorConnection(unittest.TestCase):
    
    def test_is_async(self):
        module = security_advisor_connector

        check_async = module.Connector(CONNECTION, CONFIG).is_async
        assert check_async == False

    def test_auth_apiKey_not_found_error(self):
        CONFIG = {
            "auth": {
                "accountID": "abc",
            }
        }
        transmission = stix_transmission.StixTransmission('security_advisor', CONNECTION, CONFIG)
        ping_response = transmission.ping()

        assert ping_response is not None
        assert 'success' in ping_response
        assert ping_response['success'] is False

    def test_auth_access_token_failed(self):
        
        transmission = stix_transmission.StixTransmission('security_advisor', CONNECTION, CONFIG)
        ping_response = transmission.ping()

        assert ping_response is not None
        assert 'success' in ping_response
        assert ping_response['success'] is False

    
    @requests_mock.mock()
    def test_ping_endpoint_good_return(self, mock_ping_response):

        mock_ping_response.post('https://iam.cloud.ibm.com/identity/token', text= '{ "access_token" : "ertyuiojhgfcvbnbv" }')
        mock_ping_response.get('http://test_sec_adv.com/abc/providers', text= '{ "status_code" : 200 }')

        transmission = stix_transmission.StixTransmission('security_advisor', CONNECTION, CONFIG)
        ping_response = transmission.ping()

        assert ping_response is not None
        assert 'success' in ping_response
        assert ping_response['success']
    
    @requests_mock.mock()
    def test_ping_endpoint_auth_failed(self, mock_ping_response):

        mock_ping_response.post('https://iam.cloud.ibm.com/identity/token', status_code = 500)
        mock_ping_response.get('http://test_sec_adv.com/abc/providers', status_code = 500)

        transmission = stix_transmission.StixTransmission('security_advisor', CONNECTION, CONFIG)
        ping_response = transmission.ping()
        
        assert ping_response is not None
        assert 'success' in ping_response
        assert ping_response['success'] is False

    @requests_mock.mock()
    def test_ping_endpoint_bad_return_code(self, mock_ping_response):

        mock_ping_response.post('https://iam.cloud.ibm.com/identity/token', text= '{ "access_token" : "ertyuiojhgfcvbnbv" }')
        mock_ping_response.get('http://test_sec_adv.com/abc/providers', status_code = 500)

        transmission = stix_transmission.StixTransmission('security_advisor', CONNECTION, CONFIG)
        ping_response = transmission.ping()
        
        assert ping_response is not None
        assert 'success' in ping_response
        assert ping_response['success'] is False

    @requests_mock.mock()
    def test_ping_endpoint_exception(self, mock_ping_response):

        mock_ping_response.post('https://iam.cloud.ibm.com/identity/token', text= '{ "access_token" : "ertyuiojhgfcvbnbv" }')

        transmission = stix_transmission.StixTransmission('security_advisor', CONNECTION, CONFIG)
        ping_response = transmission.ping()

        assert ping_response is not None
        assert 'success' in ping_response
        assert ping_response['success'] is False
        assert ping_response['error'] is not None

    def test_query_response_found(self):
        query = "[url:value = 'test@gmail.com']"
        transmission = stix_transmission.StixTransmission('security_advisor', CONNECTION, CONFIG)
        query_response = transmission.query(query)

        assert query_response is not None
        assert 'success' in query_response
        assert query_response['success'] is True
        assert 'search_id' in query_response
        assert query_response['search_id'] == "[url:value = 'test@gmail.com']"

    def test_status_response_completed( self):
        search_id = "[url:value = 'test@gmail.com']"

        transmission = stix_transmission.StixTransmission('security_advisor', CONNECTION, CONFIG)
        status_response = transmission.status(search_id)

        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is True
        assert 'status' in status_response
        assert status_response['status'] == "COMPLETED"
        assert 'progress' in status_response
        assert status_response['progress'] == "100"

    @staticmethod
    def test_delete_query():
        search_id = "[url:value = 'test@gmail.com']"

        module = security_advisor_connector
        status_response = module.Connector(CONNECTION, CONFIG).delete_query_connection(search_id)
        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is True

    @requests_mock.mock()
    def test_results_response(self, mock_results_response):
        
        mock_results_response.post('https://iam.cloud.ibm.com/identity/token', text= '{ "access_token" : "ertyuiojhgfcvbnbv" }')
        mock_results_response.post('http://test_sec_adv.com/abc/graph', text= '{ "data" : {"occurrences" : [ {} ] } }')

        search_id = "[url:value = 'test@gmail.com'] AND [url:value = 'test@gmail.com'] OR [url:value = 'test@gmail.com'] START t'2019-01-28T12:24:01.009Z' STOP t'2019-11-20T12:24:01.009Z'"
        offset = "0"
        length = "100"
        transmission = stix_transmission.StixTransmission('security_advisor', CONNECTION, CONFIG)
        results_response = transmission.results(search_id, offset, length)

        assert results_response is not None
        assert 'success' in results_response
        assert results_response['success'] is True
        assert 'data' in results_response
        assert len(results_response['data']) == 0         

    @requests_mock.mock()
    def test_graph_ql_exception(self, mock_results_response):
        
        mock_results_response.post('https://iam.cloud.ibm.com/identity/token', text= '{ "access_token" : "ertyuiojhgfcvbnbv" }')
        mock_results_response.post('http://test_sec_adv.com/abc/graph',status_code = 500)

        search_id = "[url:value = 'test@gmail.com'] AND [url:value = 'test@gmail.com'] OR [url:value = 'test@gmail.com'] START t'2019-01-28T12:24:01.009Z' STOP t'2019-11-20T12:24:01.009Z'"
        offset = "0"
        length = "100"
        transmission = stix_transmission.StixTransmission('security_advisor', CONNECTION, CONFIG)
        results_response = transmission.results(search_id, offset, length)

        print("results_response", results_response)
        assert results_response is not None
        assert 'success' in results_response
        assert results_response['success'] is False
        assert 'error' in results_response
                


    @requests_mock.mock()
    def test_results_response_start_time(self, mock_results_response):
        
        mock_results_response.post('https://iam.cloud.ibm.com/identity/token', text= '{ "access_token" : "ertyuiojhgfcvbnbv" }')
        mock_results_response.post('http://test_sec_adv.com/abc/graph', text= '{ "data" : {"occurrences" : [ {} ] } }')

        search_id = "[url:value = 'test@gmail.com'] AND [url:value = 'test@gmail.com'] OR [url:value = 'test@gmail.com'] START t'2019-01-28T12:24:01.009Z'"
        offset = "0"
        length = "100"
        transmission = stix_transmission.StixTransmission('security_advisor', CONNECTION, CONFIG)
        results_response = transmission.results(search_id, offset, length)

        assert results_response is not None
        assert 'success' in results_response
        assert results_response['success'] is True
        assert 'data' in results_response
        assert len(results_response['data']) == 0        

    @requests_mock.mock()
    def test_results_query_failed(self, mock_results_response):
        
        mock_results_response.post('https://iam.cloud.ibm.com/identity/token', text= '{ "access_token" : "ertyuiojhgfcvbnbv" }')
        mock_results_response.post('http://test_sec_adv.com/abc/graph', text= '{ "data" : {"occurrences" : [ {} ] } }')

        search_id = "[url:value = 'test@gmail.com'] AND [url:value = 'test@gmail.com'] OR [url:value = 'test@gmail.com'] STOP t'2019-01-28T12:24:01.009Z'"
        offset = "0"
        length = "100"
        transmission = stix_transmission.StixTransmission('security_advisor', CONNECTION, CONFIG)
        results_response = transmission.results(search_id, offset, length)

        assert results_response is not None
        assert 'success' in results_response
        assert results_response['success'] is False
        assert 'error' in results_response


    @requests_mock.mock()
    def test_results_auth_failed(self, mock_results_response):
        
        mock_results_response.post('https://iam.cloud.ibm.com/identity/token', status_code = 500)
        mock_results_response.post('http://test_sec_adv.com/abc/graph', text= '{ "data" : {"occurrences" : [ {} ] } }')

        search_id = "[url:value = 'test@gmail.com']"
        offset = "0"
        length = "100"
        transmission = stix_transmission.StixTransmission('security_advisor', CONNECTION, CONFIG)
        results_response = transmission.results(search_id, offset, length)

        assert results_response is not None
        assert 'success' in results_response
        assert results_response['success'] is False
        assert 'error' in results_response