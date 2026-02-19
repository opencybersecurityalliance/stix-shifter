from stix_shifter_modules.azure_sentinel.entry_point import EntryPoint
from stix_shifter.stix_transmission.stix_transmission import run_in_thread
from stix_shifter.stix_transmission import stix_transmission
from tests.utils.async_utils import get_mock_response

from unittest.mock import patch
from unittest import TestCase

import json


@patch('stix_shifter_modules.azure_sentinel.stix_transmission.api_client.APIClient.__init__')
class TestAzureSentinalConnection(TestCase):
    def config(self):
        return {
                "auth": {
                    "tenant": "abc12345",
                    "clientId": "abc12345",
                    "clientSecret": "abc12345",
                    }
                }

    def connection(self):
        return {
                "port": 443,
                "options": {
                        "alert": True
                    }
                }

    def test_is_async(self, mock_api_client):
        mock_api_client.return_value = None
        entry_point = EntryPoint(self.connection(), self.config())
        check_async = entry_point.is_async()

        assert check_async is False

    @patch('stix_shifter_modules.azure_sentinel.stix_transmission.api_client.APIClient.ping_box')
    def test_ping_endpoint(self, mock_ping_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = '["mock", "placeholder"]'
        mock_ping_response.return_value = get_mock_response(200, mocked_return_value, 'byte')
        transmission = stix_transmission.StixTransmission('azure_sentinel', self.connection(), self.config())
        ping_response = transmission.ping()

        assert ping_response is not None
        assert ping_response['success']

    @patch('stix_shifter_modules.azure_sentinel.stix_transmission.api_client.APIClient.ping_box')
    def test_ping_endpoint_exception(self, mock_ping_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = """{
          "error": {
            "code": "BadRequest",
            "message": "Resource not found for the segment 'alert'.",
            "innerError": {
              "request-id": "ba365a15-50ff-4041-bdc4-9dbacbd45239",
              "date": "2019-11-26T11:36:27"
            }
          }
        }"""
        mock_ping_response.return_value = get_mock_response(400, mocked_return_value)

        transmission = stix_transmission.StixTransmission('azure_sentinel', self.connection(), self.config())
        ping_response = transmission.ping()
        assert ping_response['success'] is False
        assert ping_response['error'] == "azure_sentinel connector error => Resource not found for the segment \'alert\'."
        assert ping_response['code'] == "invalid_parameter"

    def test_query_connection(self, mock_api_client):
        mock_api_client.return_value = None

        query = "fileStates/any(a:a/path eq 'c:\\windows\\system32\\services.exe') and eventDateTime ge " \
                "2019-10-13T08:00Z and eventDateTime le 2019-11-13T08:00Z"
        transmission = stix_transmission.StixTransmission('azure_sentinel', self.connection(), self.config())
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert 'search_id' in query_response
        assert query_response['search_id'] == query

    @patch('stix_shifter_modules.azure_sentinel.stix_transmission.api_client.APIClient.run_search',
           autospec=True)
    def test_results_all_response(self, mock_results_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = """{
            "@odata.context": "https://graph.microsoft.com/beta/$metadata#Security/alerts(fileStates)",
            "@odata.nextLink": "https://graph.microsoft.com/beta/security/alerts?$select=filestates&$filter=fileStates%\
            2fany(x%3ax%2fname+eq+%27services.exe%27)+and+eventDateTime+ge+2019-10-13T08%3a00Z+and+eventDateTime+le\
            +2019-11-13T08%3a00Z&$top=1&$skip=1&$skiptoken=45e372bf-0f5d-4d0b-b244-7d762a909a0e",
            "value": [
                {
                    "fileStates": [
                        {
                            "name": "services.exe",
                            "path": "c:\\\\windows\\\\system32\\\\services.exe",
                            "riskScore": null,
                            "fileHash": {
                               "hashType": "sha256",
                               "hashValue": "00a1cf85c6ab96df38a4023f0cee4df60f62280768fc9c06a235e6d2d644169d"
                             }
                        },
                        {
                            "name": "svchost.exe",
                            "path": "c:\\\\windows\\\\system32\\\\svchost.exe",
                            "riskScore": null,
                            "fileHash": {
                               "hashType": "sha256",
                               "hashValue": "33a1cf85c6ab96df38a4023f0cee4df60f62280768fc9c06a235e6d644169d"
                             }
                        }
                    ],
                    "processes": [
                        {
                            "processId": 1234,
                            "fileHash": {
                               "hashType": "sha256",
                               "hashValue": "33a1cf85c6ab96df38a4023f0cee4df60f62280768fc9c06a235e6d644169d"
                            }
                        }
                    ]
                }
            ]
        }"""
        mock_results_response.return_value = get_mock_response(200, mocked_return_value)

        query = {"alert": "$select=filestates&$filter=fileStates/any(x:x/name eq 'services.exe') and eventDateTime ge \
                 2019-10-13T08:00Z and eventDateTime le 2019-11-13T08:00Z&$top=1&$skip=1"}
        offset = 0
        length = 1
        transmission = stix_transmission.StixTransmission('azure_sentinel', self.connection(), self.config())
        results_response = transmission.results(query, offset, length)

        assert results_response is not None
        assert results_response['success']
        assert 'data' in results_response
        assert results_response['data'] is not None

    @patch('stix_shifter_modules.azure_sentinel.stix_transmission.api_client.APIClient'
           '.next_page_run_search', autospec=True)
    @patch('stix_shifter_modules.azure_sentinel.stix_transmission.api_client.APIClient.run_search',
           autospec=True)
    def test_results_paging_response(self, mock_results_response, mock_next_page_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = """{
            "@odata.context": "https://graph.microsoft.com/beta/$metadata#Security/alerts(fileStates)",
            "@odata.nextLink": "https://graph.microsoft.com/beta/security/alerts?$select=filestates&$filter=fileStates%\
            2fany(x%3ax%2fname+eq+%27services.exe%27)+and+eventDateTime+ge+2019-10-13T08%3a00Z+and+eventDateTime+le\
            +2019-11-13T08%3a00Z&$top=1&$skip=1&$skiptoken=45e372bf-0f5d-4d0b-b244-7d762a909a0e",
            "value": [
                {
                    "fileStates": [
                        {
                            "name": "services.exe",
                            "path": "c:\\\\windows\\\\system32\\\\services.exe",
                            "riskScore": null,
                            "fileHash": {
                               "hashType": "sha256",
                               "hashValue": "00a1cf85c6ab96df38a4023f0cee4df60f62280768fc9c06a235e6d2d644169d"
                             }
                        },
                        {
                            "name": "svchost.exe",
                            "path": "c:\\\\windows\\\\system32\\\\svchost.exe",
                            "riskScore": null,
                            "fileHash": {
                               "hashType": "sha256",
                               "hashValue": "33a1cf85c6ab96df38a4023f0cee4df60f62280768fc9c06a235e6d644169d"
                             }
                        }
                    ],
                    "processes": [
                        {
                            "fileHash": {
                               "hashType": "sha256",
                               "hashValue": "33a1cf85c6ab96df38a4023f0cee4df60f62280768fc9c06a235e6d644169d"
                            }
                        }
                    ]
                }
            ]
        }"""
        mocked_next_page_return_value = """{
            "@odata.context": "https://graph.microsoft.com/beta/$metadata#Security/alerts(fileStates)",
            "@odata.nextLink": "https://graph.microsoft.com/beta/security/alerts?$select=filestates&$filter=fileStates%\
            2fany(x%3ax%2fname+eq+%27services.exe%27)+and+eventDateTime+ge+2019-10-13T08%3a00Z+and+eventDateTime+le\
            +2019-11-13T08%3a00Z&$top=1&$skip=1&$skiptoken=45e372bf-0f5d-4d0b-b244-7d762a909a0e",
            "value": [
                {
                    "fileStates": [
                        {
                            "name": "cmd.exe",
                            "path": "c:\\\\windows\\\\system32\\\\services.exe",
                            "riskScore": null,
                            "fileHash": {
                               "hashType": "sha256",
                               "hashValue": "88a1cf85c6ab96df38a4023f0cee4df60f62280768fc9c06a235e6d2d644169d"
                             }
                        },
                        {
                            "name": "notepad.exe",
                            "path": "c:\\\\windows\\\\system32\\\\svchost.exe",
                            "riskScore": null,
                            "fileHash": {
                               "hashType": "sha256",
                               "hashValue": "77a1cf85c6ab96df38a4023f0cee4df60f62280768fc9c06a235e6d644169d"
                             }
                        }
                    ],
                    "processes": [
                        {
                            "fileHash": {
                               "hashType": "sha256",
                               "hashValue": "33a1cf85c6ab96df38a4023f0cee4df60f62280768fc9c06a235e6d644169d"
                            }
                        }
                    ]
                }
            ]
        }"""
        mock_results_response.return_value = get_mock_response(200, mocked_return_value)
        mock_next_page_response.return_value = get_mock_response(200, mocked_next_page_return_value)

        query = {"alert": "$select=filestates&$filter=fileStates/any(x:x/name eq 'services.exe') and eventDateTime ge "\
                 "2019-10-13T08:00Z and eventDateTime le 2019-11-13T08:00Z&$top=1&$skip=1"}
        offset = 0
        length = 2
        transmission = stix_transmission.StixTransmission('azure_sentinel', self.connection(), self.config())
        results_response = transmission.results(query, offset, length)
        print(json.dumps(results_response,indent=4))
        assert results_response is not None
        assert results_response['success']
        assert 'data' in results_response
        assert results_response['data'] is not None

    @patch('stix_shifter_modules.azure_sentinel.stix_transmission.api_client.APIClient.run_search',
           autospec=True)
    def test_results_response_exception(self, mock_results_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = """ {
          "error": {
            "code": "BadRequest",
            "message": "Invalid filter clause",
            "innerError": {
              "request-id": "e8904fd5-0f2c-496d-9ed0-4ee5c58946ff",
              "date": "2019-11-26T11:30:51"
            }
          }
        } """
        mock_results_response.return_value = get_mock_response(404, mocked_return_value)

        query = {"alert": "$select=filestates&$filter=fileStates/any(x:x/name eq 'services.exe') and eventDateTime ge \
                 2019-10-13T08:00Z and eventDateTime le 2019-11-13T08:00Z&$top=1&$skip=1"}
        offset = 0
        length = 1
        transmission = stix_transmission.StixTransmission('azure_sentinel', self.connection(), self.config())
        results_response = transmission.results(query, offset, length)
        print(results_response)

        assert results_response['success'] is False
        assert results_response['error'] == "azure_sentinel connector error => Invalid filter clause"
        assert results_response['code'] == "invalid_parameter"

    def test_delete_query(self, mock_api_client):
        mock_api_client.return_value = None

        search_id = "$select=filestates&$filter=fileStates/any(x:x/name eq 'services.exe') and eventDateTime ge \
                 2019-10-13T08:00Z and eventDateTime le 2019-11-13T08:00Z&$top=1&$skip=1"

        entry_point = EntryPoint(self.connection(), self.config())
        status_response = run_in_thread(entry_point.delete_query_connection, search_id)
        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is True

    def test_status_query(self, mock_api_client):
        mock_api_client.return_value = None

        search_id = "$select=filestates&$filter=fileStates/any(x:x/name eq 'services.exe') and eventDateTime ge \
                 2019-10-13T08:00Z and eventDateTime le 2019-11-13T08:00Z&$top=1&$skip=1"

        entry_point = EntryPoint(self.connection(), self.config())
        status_response = run_in_thread(entry_point.create_status_connection, search_id)
        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is True

    @patch('stix_shifter_modules.azure_sentinel.stix_transmission.api_client.APIClient.run_search',
           autospec=True)
    def test_alert_v2_results(self, mock_results_response, mock_api_client):
        mock_api_client.return_value = None

        mock_return_value = open('stix_shifter_modules/azure_sentinel/tests/jsons/alert_v2.json', 'r').read()
        mock_results_response.return_value = get_mock_response(200, mock_return_value)
        search_id = {"alertV2": "(tolower(severity) eq 'low') and (eventDateTime ge 2023-04-17T20:05:42.261Z and eventDateTime le 2023-04-17T20:10:42.261Z)"}

        offset = 0
        length = 1

        entry_point = EntryPoint(self.connection(), self.config())
        results_response = run_in_thread(entry_point.create_results_connection, search_id, offset, length)

        assert results_response is not None
        assert results_response['success']
        assert 'data' in results_response
        assert results_response['data'] is not None
