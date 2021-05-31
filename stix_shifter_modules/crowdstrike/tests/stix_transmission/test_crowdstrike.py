from stix_shifter_modules.crowdstrike.entry_point import EntryPoint
from unittest.mock import patch
import unittest
from stix_shifter.stix_transmission import stix_transmission
from stix_shifter_utils.utils.error_response import ErrorCode


class CrowdStrikeMockResponse:
    def __init__(self, response_code, obj):
        self.code = response_code
        self.object = obj

    def read(self):
        return bytearray(self.object, 'utf-8')


@patch('stix_shifter_modules.crowdstrike.stix_transmission.api_client.APIClient.__init__')
class TestcrowdstrikeConnection(unittest.TestCase):
    def config(self):
        return {
            "auth": {
                "client_id": "bla",
                "client_secret": "bla"
            }
        }

    def connection(self):
        return {
            "host": "hostbla",
            "selfSignedCert": "cert"
        }

    def test_is_async(self, mock_api_client):
        mock_api_client.return_value = None
        entry_point = EntryPoint(self.connection(), self.config())
        check_async = entry_point.is_async()

        assert check_async is False

    def test_query_connection(self, mock_api_client):
        mock_api_client.return_value = None

        query = "((behaviors.timestamp:> '2019-09-04T09:29:29.0882Z') + device.last_seen:> '2002-05-27T03:51:40.090688')"

        transmission = stix_transmission.StixTransmission('crowdstrike', self.connection(), self.config())
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert 'search_id' in query_response
        assert query_response['search_id'] == query

    @patch('stix_shifter_modules.crowdstrike.stix_transmission.api_client.APIClient.get_detections_IDs')
    def test_query(self, mock_query_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = '{"job_id": "108cb8b0-0744-4dd9-8e35-ea8311cd6211"}'
        mock_query_response.return_value = CrowdStrikeMockResponse(200, mocked_return_value)

        entry_point = EntryPoint(self.connection(), self.config())
        query = [
            "((behaviors.timestamp:> '2019-09-04T09:29:29.0882Z') + device.last_seen:> '2002-05-27T03:51:40.090688')"]
        query_response = entry_point.create_query_connection(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert 'search_id' in query_response
        assert query_response['search_id'] == query
