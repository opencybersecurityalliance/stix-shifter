from stix_shifter_modules.guardium.entry_point import EntryPoint
from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import Status
from stix_shifter.stix_transmission import stix_transmission
from unittest.mock import patch
import unittest


class GuardiumMockResponse:
    def __init__(self, response_code, object):
        self.code = response_code
        self.object = object

    def read(self):
        return self.object    

@patch('stix_shifter_modules.guardium.stix_transmission.api_client.APIClient.__init__', autospec=True)
class TestGuardiumConnection(unittest.TestCase, object):
    def test_is_async(self, mock_api_client):
        mock_api_client.return_value = None
        entry_point = EntryPoint()

        config = {
            "auth": {
                "username": "admin",
                "password": "12345678"
            }
        }
        connection = {
            "client_id": 'WHO',
            "client_secret": "57695f99-fe23-4bb4-5116-4b7985c8532b",
            "host": "where.ibm.com",
            "port": "22",
            "selfSignedCert": False
        }
        check_async = entry_point.is_async()

        assert not check_async

    @patch('stix_shifter_modules.guardium.stix_transmission.api_client.APIClient.create_search')
    def test_query_response(self, mock_query_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = '{"search_id": "108cb8b0-0744-4dd9-8e35-ea8311cd6211"}'
        mock_query_response.return_value = GuardiumMockResponse(200, mocked_return_value)

        config = {
            "auth": {
                "username": "admin",
                "password": "12345678"
            }
        }
        connection = {
            "client_id": 'WHO',
            "client_secret": "57695f99-fe23-4bb4-5116-4b7985c8532b",
            "host": "where.ibm.com",
            "port": "22",
            "selfSignedCert": False
        }

        query = '[x-ibm-finding:database_name=\'ggg\' AND  ipv4-addr:dst_ip=\'10.0.0.2\']'
        transmission = stix_transmission.StixTransmission('guardium',  connection, config)
        query_response = transmission.query(query)

        assert query_response is not None
        assert 'search_id' in query_response
        assert query_response['search_id'] == "108cb8b0-0744-4dd9-8e35-ea8311cd6211"

    @patch('stix_shifter_modules.guardium.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    def test_status_response(self, mock_status_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = '{"search_id": "108cb8b0-0744-4dd9-8e35-ea8311cd6211", "status": "COMPLETED", "progress": "100"}'
        mock_status_response.return_value = GuardiumMockResponse(200, mocked_return_value)

        config = {
            "auth": {
                "username": "admin",
                "password": "12345678"
            }
        }
        connection = {
            "client_id": 'WHO',
            "client_secret": "57695f99-fe23-4bb4-5116-4b7985c8532b",
            "host": "where.ibm.com",
            "port": "22",
            "selfSignedCert": False
        }
        
        search_id = "108cb8b0-0744-4dd9-8e35-ea8311cd6211"
        transmission = stix_transmission.StixTransmission('guardium',  connection, config)
        status_response = transmission.status(search_id)

        assert status_response['success']
        assert status_response is not None
        assert 'status' in status_response
        assert status_response['status'] == Status.COMPLETED.value

