import unittest
import json
from unittest.mock import Mock, patch, AsyncMock

from stix_shifter.stix_transmission import stix_transmission
from stix_shifter_modules.stix_bundle.entry_point import EntryPoint
from stix_shifter.stix_transmission.stix_transmission import run_in_thread
from stix_shifter_modules.stix_bundle.stix_transmission.connector import Connector, UnexpectedResponseException

class TestSTIXBundleConnector(unittest.TestCase, object):
    configuration = {
        "auth": {
            "username": "",
            "password": ""
        }
    }

    connection = {
        'url': 'https://raw.githubusercontent.com/opencybersecurityalliance/stix-shifter/develop/data/cybox/qradar/qradar_observed_2000.json'
    }

    def test_ping(self):
        entry_point = EntryPoint(self.connection, self.configuration)
        ping_result = run_in_thread(entry_point.ping_connection)
        assert ping_result["success"] is True

    def test_ping_failure(self):
        connection = {
            'url': 'https://invalid_host.com/org/master/data/bundle.json'
        }
        entry_point = EntryPoint(connection, self.configuration)
        ping_result = run_in_thread(entry_point.ping_connection)

        assert ping_result["success"] is False
        assert ping_result["code"] == 'service_unavailable'

    def test_query(self):
        query = "[ipv4-addr:value = '9.28.234.169'] START t'2020-09-30T16:24:59.988Z' STOP t'2020-09-30T16:25:59.988Z'"
        transmission = stix_transmission.StixTransmission("stix_bundle", self.connection, self.configuration)
        query_response = transmission.query(query)
        self.assertTrue(query_response["success"])
        self.assertEqual(query_response["search_id"], query)
    
    
    def test_status(self):
        transmission = stix_transmission.StixTransmission("stix_bundle", self.connection, self.configuration)
        status_response = transmission.status("search_id")
        self.assertTrue(status_response["success"])
        self.assertEqual(status_response["status"], "COMPLETED")
        self.assertEqual(status_response["progress"], 100)
    
    def test_results(self):
        result_file = open('stix_shifter_modules/stix_bundle/test/qradar_observed_2000.json', 'r').read()
        data = json.loads(result_file)
        result_bundle_objects = data['objects']
        observed_data = result_bundle_objects[1]

        transmission = stix_transmission.StixTransmission('stix_bundle', self.connection, self.configuration)
        results_response = transmission.results("[ipv4-addr:value = '9.28.234.169'] START t'2020-09-30T16:24:59.988Z' STOP t'2020-09-30T16:25:59.988Z'", 0, 1)
        assert results_response["success"] is True
        assert results_response["data"] == [observed_data]

    def test_ping_with_redirect(self):
        """Test HTTP 301 redirect handling in ping_connection"""
        connection = {
            'url': 'https://example.com/bundle.json',
            'options': {}
        }
        connector = Connector(connection, self.configuration)

        # Create mock responses for the redirect scenario
        mock_response_301 = Mock()
        mock_response_301.code = 301
        mock_response_301.headers = {'Location': 'https://example.com/new-bundle.json'}
        mock_response_301.raise_for_status = Mock(return_value=None)

        mock_response_200 = Mock()
        mock_response_200.code = 200
        mock_response_200.raise_for_status = Mock(return_value=None)

        with patch.object(connector.client, 'call_api', new_callable=AsyncMock) as mock_call:
            # First call returns 301, second call returns 200
            mock_call.side_effect = [mock_response_301, mock_response_200]

            result = run_in_thread(connector.ping_connection)

            assert result["success"] is True
            assert mock_call.call_count == 2
            # Verify the URL was updated to the redirect location
            assert connector.bundle_url == 'https://example.com/new-bundle.json'

    def test_results_with_unexpected_response(self):
        """Test UnexpectedResponseException when response is neither plain string nor JSON"""
        connection = {
            'url': 'https://example.com/bundle.json',
            'options': {}
        }
        connector = Connector(connection, self.configuration)

        # Create a mock response that returns bytes that are neither plain text nor JSON
        mock_response = Mock()
        mock_response.code = 500
        # Return binary data that's not a string and not valid JSON
        mock_response.raise_for_status = Mock(return_value=b'\x80\x81\x82\x83')

        with patch.object(connector.client, 'call_api', new_callable=AsyncMock) as mock_call:
            mock_call.return_value = mock_response

            result = run_in_thread(connector.create_results_connection, "test_query", 0, 10)

            # Should handle the UnexpectedResponseException gracefully
            assert result["success"] is False

    def test_results_with_stix_21(self):
        """Test STIX 2.1 results processing"""
        # Create a STIX 2.1 bundle structure
        stix_21_bundle = {
            "type": "bundle",
            "id": "bundle--test",
            "objects": [
                {
                    "type": "identity",
                    "id": "identity--test",
                    "name": "Test"
                },
                {
                    "type": "observed-data",
                    "id": "observed-data--1",
                    "object_refs": ["ipv4-addr--1"],
                    "first_observed": "2020-09-30T16:24:59.988Z",
                    "last_observed": "2020-09-30T16:25:59.988Z",
                    "number_observed": 1
                },
                {
                    "type": "ipv4-addr",
                    "id": "ipv4-addr--1",
                    "value": "9.28.234.169"
                }
            ]
        }

        connection_21 = {
            'url': 'https://example.com/bundle.json',
            'options': {"stix_2.1": True}
        }

        connector = Connector(connection_21, self.configuration)

        mock_response = Mock()
        mock_response.code = 200
        mock_response.read = Mock(return_value=json.dumps(stix_21_bundle).encode('utf-8'))

        with patch.object(connector.client, 'call_api', new_callable=AsyncMock) as mock_call:
            mock_call.return_value = mock_response

            result = run_in_thread(
                connector.create_results_connection,
                "[ipv4-addr:value = '9.28.234.169'] START t'2020-09-30T16:24:59.988Z' STOP t'2020-09-30T16:25:59.988Z'",
                0,
                10
            )

            assert result["success"] is True
            assert "data" in result
            # In STIX 2.1, results should include observed-data and referenced objects
            assert len(result["data"]) > 0

    def test_timestamp_with_start_stop_qualifier(self):
        """Test that START/STOP qualifiers work correctly with the compatibility patch"""
        connection = {
            'url': 'https://example.com/bundle.json',
            'options': {}
        }
        connector = Connector(connection, self.configuration)

        # Create valid observed data with timestamps
        observations = [{
            "type": "observed-data",
            "id": "observed-data--test",
            "created": "2020-01-01T00:00:00.000Z",
            "modified": "2020-01-01T00:00:00.000Z",
            "first_observed": "2020-01-01T00:00:00.000Z",
            "last_observed": "2020-01-01T00:00:00.000Z",
            "number_observed": 1,
            "objects": {
                "0": {
                    "type": "ipv4-addr",
                    "value": "192.168.1.1"
                }
            }
        }]

        # Create a pattern with START/STOP qualifiers to exercise the compatibility patch
        pattern = "[ipv4-addr:value = '192.168.1.1'] START t'2020-01-01T00:00:00.000Z' STOP t'2020-01-02T00:00:00.000Z'"

        # Test that the match function works correctly with timestamps
        result = connector.match(pattern, observations, False, '2.0')
        assert isinstance(result, list)
        assert len(result) == 1

    def test_test_start_stop_format(self):
        """Test the START/STOP format validation helper method"""
        connection = {
            'url': 'https://example.com/bundle.json',
            'options': {}
        }
        connector = Connector(connection, self.configuration)

        # Valid format
        valid_query = "[ipv4-addr:value = '127.0.0.1'] START t'2020-01-01T00:00:00.000Z' STOP t'2020-01-02T00:00:00.000Z'"
        assert connector.test_START_STOP_format(valid_query) is True

        # Invalid format (missing STOP)
        invalid_query = "[ipv4-addr:value = '127.0.0.1'] START t'2020-01-01T00:00:00.000Z'"
        assert connector.test_START_STOP_format(invalid_query) is False

    def test_match_no_results(self):
        """Test match function when no results are found"""
        connection = {
            'url': 'https://example.com/bundle.json',
            'options': {}
        }
        connector = Connector(connection, self.configuration)

        observations = [{
            "type": "observed-data",
            "id": "observed-data--test",
            "created": "2020-01-01T00:00:00.000Z",
            "modified": "2020-01-01T00:00:00.000Z",
            "first_observed": "2020-01-01T00:00:00.000Z",
            "last_observed": "2020-01-01T00:00:00.000Z",
            "number_observed": 1,
            "objects": {
                "0": {
                    "type": "ipv4-addr",
                    "value": "192.168.1.1"
                }
            }
        }]

        # Pattern that won't match (different IP)
        pattern = "[ipv4-addr:value = '10.0.0.1']"
        result = connector.match(pattern, observations, False, '2.0')
        assert result == []

    def test_ping_error_response(self):
        """Test ping_connection with error response"""
        connection = {
            'url': 'https://example.com/bundle.json',
            'options': {}
        }
        connector = Connector(connection, self.configuration)

        mock_response = Mock()
        mock_response.code = 500
        mock_response.raise_for_status = Mock(return_value="Internal Server Error")

        with patch.object(connector.client, 'call_api', new_callable=AsyncMock) as mock_call:
            mock_call.return_value = mock_response

            result = run_in_thread(connector.ping_connection)

            assert result["success"] is False
            assert "error" in result

    def test_delete_query(self):
        """Test delete_query_connection"""
        connection = {
            'url': 'https://example.com/bundle.json',
            'options': {}
        }
        connector = Connector(connection, self.configuration)

        result = run_in_thread(connector.delete_query_connection, "test_search_id")
        assert result["success"] is True

    def test_results_with_json_error_response(self):
        """Test create_results_connection with JSON error response"""
        connection = {
            'url': 'https://example.com/bundle.json',
            'options': {}
        }
        connector = Connector(connection, self.configuration)

        mock_response = Mock()
        mock_response.code = 400
        mock_response.raise_for_status = Mock(return_value='{"reason": "Bad Request"}')

        with patch.object(connector.client, 'call_api', new_callable=AsyncMock) as mock_call:
            mock_call.return_value = mock_response

            result = run_in_thread(connector.create_results_connection, "test_query", 0, 10)

            assert result["success"] is False
            assert "error" in result

    def test_results_with_plain_string_error_response(self):
        """Test create_results_connection with plain string error response"""
        connection = {
            'url': 'https://example.com/bundle.json',
            'options': {}
        }
        connector = Connector(connection, self.configuration)

        mock_response = Mock()
        mock_response.code = 404
        mock_response.raise_for_status = Mock(return_value="Not Found")

        with patch.object(connector.client, 'call_api', new_callable=AsyncMock) as mock_call:
            mock_call.return_value = mock_response

            result = run_in_thread(connector.create_results_connection, "test_query", 0, 10)

            assert result["success"] is False
            assert "error" in result

    def test_results_with_pattern_match_error(self):
        """Test create_results_connection when pattern matching fails"""
        connection = {
            'url': 'https://example.com/bundle.json',
            'options': {}
        }
        connector = Connector(connection, self.configuration)

        # Return valid JSON but with an invalid structure that will cause pattern matching to fail
        invalid_bundle = {
            "type": "bundle",
            "id": "bundle--test",
            "objects": []
        }

        mock_response = Mock()
        mock_response.code = 200
        mock_response.read = Mock(return_value=json.dumps(invalid_bundle).encode('utf-8'))

        with patch.object(connector.client, 'call_api', new_callable=AsyncMock) as mock_call:
            mock_call.return_value = mock_response

            # Use an invalid pattern to trigger an exception
            result = run_in_thread(connector.create_results_connection, "[[[invalid pattern", 0, 10)

            assert result["success"] is False
            assert "error" in result

    def test_results_with_malformed_json(self):
        """Test create_results_connection with malformed JSON"""
        connection = {
            'url': 'https://example.com/bundle.json',
            'options': {}
        }
        connector = Connector(connection, self.configuration)

        mock_response = Mock()
        mock_response.code = 200
        mock_response.read = Mock(return_value=b'{invalid json}')

        with patch.object(connector.client, 'call_api', new_callable=AsyncMock) as mock_call:
            mock_call.return_value = mock_response

            result = run_in_thread(connector.create_results_connection, "test_query", 0, 10)

            assert result["success"] is False
            assert "error" in result

    def test_results_with_zero_results_after_slicing(self):
        """Test create_results_connection when results are empty after offset/length slicing"""
        result_file = open('stix_shifter_modules/stix_bundle/test/qradar_observed_2000.json', 'r').read()
        data = json.loads(result_file)

        connector = Connector(self.connection, self.configuration)

        mock_response = Mock()
        mock_response.code = 200
        mock_response.read = Mock(return_value=json.dumps(data).encode('utf-8'))

        with patch.object(connector.client, 'call_api', new_callable=AsyncMock) as mock_call:
            mock_call.return_value = mock_response

            # Use an offset that's beyond the available results (file has 2000 observed-data objects)
            result = run_in_thread(
                connector.create_results_connection,
                "[ipv4-addr:value = '9.28.234.169'] START t'2020-09-30T16:24:59.988Z' STOP t'2020-09-30T16:25:59.988Z'",
                2100,  # offset beyond available results
                10
            )

            assert result["success"] is True
            assert result["data"] == []