from stix_shifter.stix_transmission.src.modules.carbonblack import carbonblack_connector
from stix_shifter.stix_transmission.src.modules.base.base_status_connector import Status
from unittest.mock import patch
import unittest
from stix_shifter.stix_transmission.src.modules.utils.RestApiClient import ResponseWrapper


class CarbonBlackMockResponse:
    def __init__(self, response_code, object):
        self.code = response_code
        self.object = object

    def read(self):
        return self.object


@patch('stix_shifter.stix_transmission.src.modules.carbonblack.carbonblack_api_client.APIClient.__init__', autospec=True)
class TestCarbonBlackConnection(unittest.TestCase, object):

    @patch('stix_shifter.stix_transmission.src.modules.carbonblack.carbonblack_api_client.APIClient.ping_box')
    def test_ping_endpoint(self, mock_ping_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = '["mock", "placeholder"]'
        mock_ping_response.return_value = CarbonBlackMockResponse(200, mocked_return_value)

        module = carbonblack_connector
        config = {
            "auth": {
                "token": "bla"
            }
        }
        connection = {
            "host": "hostbla",
            "port": "8080"
        }
        ping_response = module.Connector(connection, config).ping()

        assert ping_response is not None
        assert ping_response['success']
