# tests.py
import json
import unittest
from unittest import mock
from functools import wraps
from stix_shifter_modules.dshield.stix_transmission.api_client import APIClient
from dshield_test_json_transmission import *

namespace = '8af42ea1-e30d-41a2-a3ee-1aec759cf789'

connection = {
    "namespace":namespace
}
config = {
    "auth": {
        "key": "testingKey"
    }
}

SAMPLE_DATA_IP = {"data": "101.81.5.6", "dataType": "ip"}

class TestDshieldTransmission(unittest.TestCase):
    def __init__(self,*args, **kwargs):
        super(TestDshieldTransmission, self).__init__(*args, **kwargs)
        self.api_client = APIClient(connection, config)
    
    @mock.patch('stix_shifter_modules.dshield.stix_transmission.api_client.RestApiClientAsync.call_api')
    async def test_dshield_results_ip(self, mock_client_get_json):
        mock_client_get_json.return_value = DATA_TRANS

        response = await self.api_client.get_search_results(SAMPLE_DATA_IP)
        assert response[0]['data']['success'] == True
        assert response[0]['code'] == 200
        assert response[0]['data']['full']['ioc_report']['number'] == "101.81.5.6"

    @mock.patch('stix_shifter_modules.threat_grid.stix_transmission.api_client.RestApiClientAsync.call_api')
    async def test_threat_grid_ping(self, mock_client_get_json):
        mock_client_get_json.return_value = DATA_TRANS
        response = await self.api_client.ping_dshield()

        assert response['code'] == 200