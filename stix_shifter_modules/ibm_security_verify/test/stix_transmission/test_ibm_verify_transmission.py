import json
import unittest
from unittest.mock import patch

from stix_shifter.stix_transmission import stix_transmission
from stix_shifter_modules.ibm_security_verify.entry_point import EntryPoint
from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import Status
from stix_shifter.stix_transmission.stix_transmission import run_in_thread
from tests.utils.async_utils import get_mock_response


class ReasonMockResponse:
    def __init__(self):
        self.reason = None


class TestVerifyConnection(unittest.TestCase, object):
    
    def test_is_async(self):
        entry_point = EntryPoint()

        check_async = entry_point.is_async()
        assert check_async is True


    def test_status_response(self):

        config = {"host": "connection.com"}
        connection = {"auth": {"clientId": "clientId", "clientSecret": "clientscred"}}

        search_id = "108cb8b0-0744-4dd9-8e35-ea8311cd6211"
        transmission = stix_transmission.StixTransmission("ibm_security_verify", config, connection)
        status_response = transmission.status(search_id)

        assert status_response["success"]
        assert status_response is not None
        assert "status" in status_response
        assert status_response["status"] == Status.COMPLETED.value


    @patch(
        "stix_shifter_modules.ibm_security_verify.stix_transmission.api_client.APIClient.run_search"
    )
    def test_query_response(self, mock_query_response):
        mock_query_response.return_value = {"success": 200}

        config = {"host": "cloudsecurity.com"}
        connection = {"auth": {"clientId": "clientid", "clientSecret": "secret"}}

        query = '{"query":"event_type="sso""}'
        transmission = stix_transmission.StixTransmission("ibm_security_verify", config, connection)
        query_response = transmission.query(query)

        assert query_response is not None
        assert "search_id" in query_response
        assert query_response["search_id"] == query


    @patch(
        "stix_shifter_modules.ibm_security_verify.stix_transmission.api_client.APIClient.generate_token"
    )
    def test_ping(self, mock_generate_token):

        config = {"host": "cloudsecurity.com"}
        connection = {"auth": {"clientId": "clientid", "clientSecret": "secret"}}
        mocked_return_value = get_mock_response(200, 200)
        mock_generate_token.return_value = mocked_return_value
        entry_point = EntryPoint(config, connection)
        ping_result = run_in_thread(entry_point.ping_connection)
        assert ping_result["success"] is True


    @patch("stix_shifter_modules.ibm_security_verify.stix_transmission.api_client.APIClient.generate_token")
    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_results_all_response(self, mock_results_response, mock_generate_token):
        mock_generate_token.return_value = get_mock_response(200, '{"code": 200}')
        # from https://community.ibm.com/community/user/security/blogs/adam-case/2019/05/30/get-event-log-details-and-sso-activity-from-ibm-cl
        mocked_return_value = {
            "response":{
                "events":{
                    "search_after":{
                        "total_events":54,
                        "max_size_limit":"false",
                        "time":"1559156150862",
                        "id":"def9ea72-30ce-4589-800a-7306e306ea2e"
                    },
                    "events":[
                        {
                            "geoip":{
                                "continent_name":"North America",
                                "country_iso_code":"US",
                                "country_name":"United States",
                                "location":{
                                    "lon":"-97.822",
                                    "lat":"37.751"
                                }
                            }
                        }  
                    ]
                }
            }
        }
        mock_results_response.return_value = get_mock_response(200, json.dumps(mocked_return_value), response=ReasonMockResponse())

        config = {"host": "ibmcloud.com"}
        connection = {"auth": {"clientId": "clientId", "clientSecret": "secret"}}
        query = 'event_type="sso"&limit=10000'
        offset = 0
        length = 101
        entry_point = EntryPoint(config, connection)
        results_response = run_in_thread(entry_point.create_results_connection, query, offset, length)

        assert results_response is not None
        assert results_response["success"]
        assert "data" in results_response
        assert results_response["data"] is not None
