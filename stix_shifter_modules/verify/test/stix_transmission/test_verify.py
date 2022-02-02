
import json
from sre_constants import ASSERT_NOT
import unittest
from unittest.mock import ANY
from unittest.mock import patch
from stix_shifter.stix_transmission import stix_transmission
from stix_shifter_modules.verify.entry_point import EntryPoint
from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import Status
from stix_shifter_utils.stix_transmission.utils.RestApiClient import ResponseWrapper
from unittest.mock import patch


class VerifyMockResponse:
    def __init__(self, response_code, object):
        self.code = response_code
        self.object = object
        
    def read(self):
        return self.object   

class VerifyMockPingResponse:
    def __init__(self, response_code, status_code):
        self.code = response_code
        self.status_code =status_code
        
    def read(self):
        return self.object   


@patch('stix_shifter_modules.verify.stix_transmission.api_client.APIClient.__init__', autospec=True)
class TestVerifyConnection(unittest.TestCase, object):
    
    def test_is_async(self, mock_api_client):
        mock_api_client.return_value = None
        entry_point = EntryPoint()

        config = {
            "auth": {
                "sec": "bla"
            }
        }
        connection = {
            "host": "hostbla",
            "port": 8080,
            "selfSignedCert": "cert"
        }
        check_async = entry_point.is_async()
        assert check_async is not True

    @patch('stix_shifter_modules.verify.stix_transmission.api_client.APIClient.get_search', autospec=True)
    def test_status_response(self, mock_status_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = '{"search_id": "108cb8b0-0744-4dd9-8e35-ea8311cd6211", "status": "COMPLETED", "progress": "100"}'
        mock_status_response.return_value = VerifyMockResponse(200, mocked_return_value)

        config = {
            "auth": {
                "sec": "bla"
            }
        }
        connection = {
            "host": "hostbla",
            "port": 8080,
            "selfSignedCert": "cert"
        }
        
        search_id = "108cb8b0-0744-4dd9-8e35-ea8311cd6211"
        transmission = stix_transmission.StixTransmission('verify',  config, connection)
        status_response = transmission.status(search_id)

        assert status_response['success']
        assert status_response is not None
        assert 'status' in status_response
        assert status_response['status'] == Status.COMPLETED.value

    @patch('stix_shifter_modules.verify.stix_transmission.api_client.APIClient.run_search')
    def test_query_response(self, mock_query_response, mock_api_client):
        mock_api_client.return_value = None
        mock_query_response.return_value = {"success":200}

        config = {
            "auth": {
                "sec": "bla"
            }
        }
        connection = {
            "host": "hostbla",
            "port": 8080,
            "selfSignedCert": "cert"
        }

        query = '{"query":"event_type=\"sso\""}'        
        transmission = stix_transmission.StixTransmission('verify',  config, connection)
        query_response = transmission.query(query)

        assert query_response is not None
        assert 'search_id' in query_response
        assert query_response['search_id'] == query

  
    @patch('stix_shifter_modules.verify.stix_transmission.api_client.APIClient.generate_token')
    def test_ping(self, mock_generate_token, mock_api_client):

        config = {
            "auth": {
                "sec": "bla"
            }
        }
        connection = {
            "host": "hostbla",
            "port": 8080,
            "selfSignedCert": "cert"
        }
        mocked_return_value = VerifyMockPingResponse(200,200)
        mock_generate_token.return_value = mocked_return_value
        mock_api_client.return_value = None
        entry_point = EntryPoint(config, connection)
        ping_result = entry_point.ping_connection()
        assert ping_result["success"] is True


    @patch('stix_shifter_modules.verify.stix_transmission.api_client.APIClient.generate_token')
    @patch('stix_shifter_modules.verify.stix_transmission.api_client.APIClient.run_search',
           autospec=True)
    def test_results_all_response(self, mock_results_response, mock_generate_token, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = {"code": 200}
        mock_generate_token.return_value = mocked_return_value
        config = {
            "auth": {
                "sec": "bla"
            }
        }
        connection = {
            "host": "hostbla",
            "port": 8080,
            "selfSignedCert": "cert"
        }

        mocked_return_value = {
            "code": 200, 
            "success":200,
            "data": [
          {"id":123, "created_at":"2022-01-16T16:45:16.112Z", "account_id":123, "ipaddr":"12.22.33.44"}
          ]}

        mock_results_response.return_value = mocked_return_value

        query = "event_type=\"sso\"&limit=10000"

        offset = 0
        length = 101
        entry_point = EntryPoint(config, connection)
        results_response = entry_point.create_results_connection(query, offset, length)

        assert results_response is not None
        assert results_response['success']
        assert 'data' in results_response
        assert results_response['data'] is not None

    