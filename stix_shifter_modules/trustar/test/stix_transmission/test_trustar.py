from stix_shifter_modules.trustar.entry_point import EntryPoint
from unittest.mock import patch
import unittest
import json
import os
from stix_shifter.stix_transmission import stix_transmission
from stix_shifter_utils.utils.error_response import ErrorCode

class TrustarMockResponse:
    def __init__(self, response_code, object):
        self.code = response_code
        self.object = object

    def read(self):
        return bytearray(self.object, 'utf-8')


@patch('stix_shifter_modules.trustar.stix_transmission.api_client.APIClient.__init__',  autospec=True)
class TestTrustarConnection(unittest.TestCase, object):
    def test_is_async(self, mock_api_client):
        mock_api_client.return_value = None
        entry_point = EntryPoint()

        check_async = entry_point.is_async()

        assert check_async is False

    def test_query_response(self, mock_api_client):
        mock_api_client.return_value = None

        config = {
            "auth": {
                "clientId": "foo",
                "clientSecret": "bar"
            }
        }
        connection = {
            "host": "api.trustar.co",
            "port": 443
        }

        query = "{\"searchTerm\": \"192.155.88.196\"}"
        transmission = stix_transmission.StixTransmission('trustar', connection, config)
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert 'search_id' in query_response
        assert query_response['search_id'] == query


    @patch('stix_shifter_modules.trustar.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    def test_results_response(self, mock_results_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = """{
    "indicatorType": "IP",
            "value": "9.30.116.81",
            "priorityLevel": "NOT_FOUND",
            "firstSeen": 1630071439159,
            "lastSeen": 1630588132716,
            "guid": "IP|9.30.116.81",
            "IP": "9.30.116.81",
            "reports": [
                {
                    "id": "9ca88e1d-bd3c-412d-9e34-8db32dcc5540",
                    "created": 1630588132711,
                    "updated": 1630588132711,
                    "title": "QRadar Vulnerability Report",
                    "distributionType": "ENCLAVE",
                    "enclaveIds": [
                        "46d916e1-4e40-469d-b3df-d3b1d706a28d"
                    ]
                },
                {
                    "id": "a5e5895f-c1e9-4a80-9b1f-dabc4581e051",
                    "created": 1630577472499,
                    "updated": 1630577472499,
                    "title": "QRadar Authention Report",
                    "distributionType": "ENCLAVE",
                    "enclaveIds": [
                        "df82c00f-ec71-4910-8c1e-747292981571"
                    ]
                },
                {
                    "id": "3e17c2cd-bf6c-4808-8b08-573a9f1c8ddd",
                    "created": 1630071602240,
                    "updated": 1630321684919,
                    "title": "Asset Details-Qradar",
                    "distributionType": "ENCLAVE",
                    "enclaveIds": [
                        "7c42062e-060d-430d-9dcb-9a28031f71c4"
                    ]
                }
            ],
            "indicatorSummary": [],
            "meta": {
                "indicatorType": "IP",
                "value": "9.30.116.81",
                "correlationCount": 0,
                "priorityLevel": "NOT_FOUND",
                "noteCount": 0,
                "sightings": 5,
                "firstSeen": 1630071439159,
                "lastSeen": 1630588132716,
                "enclaveIds": [
                    "46d916e1-4e40-469d-b3df-d3b1d706a28d",
                    "7c42062e-060d-430d-9dcb-9a28031f71c4",
                    "df82c00f-ec71-4910-8c1e-747292981571"
                ],
                "tags": [
                    {
                        "guid": "119431b6-e75b-49fc-af8f-a87bdca93f8c",
                        "name": "offensetag2",
                        "enclaveId": "df82c00f-ec71-4910-8c1e-747292981571"
                    },
                    {
                        "guid": "ec53d371-3ff9-4cbd-87b8-907070a8bafd",
                        "name": "vatag1",
                        "enclaveId": "46d916e1-4e40-469d-b3df-d3b1d706a28d"
                    }
                ],
                "source": "",
                "notes": [],
                "guid": "IP|9.30.116.81"
            }

}"""
        mock_results_response.return_value = TrustarMockResponse(200, mocked_return_value)

        config = {
            "auth": {
                "clientId": "foo",
                "clientSecret": "bar"
            }
        }
        connection = {
            "host": "api.trustar.co",
            "port": 443
        }

        query = "{\"searchTerm\": \"192.155.88.196\", \"from\": 1630155241000, \"to\": 1630846441000}"
        offset = 0
        length = 1
        transmission = stix_transmission.StixTransmission('trustar', connection, config)
        results_response = transmission.results(query, offset, length)

        assert results_response is not None
    
    