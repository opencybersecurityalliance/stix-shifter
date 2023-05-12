# tests.py
import json
import unittest
from unittest import mock
from functools import wraps
from stix_shifter_modules.threat_grid.stix_transmission.api_client import APIClient
from stix_shifter_modules.threat_grid.stix_transmission.ping_connector import PingConnector
from json_transmission import *

namespace = '8af42ea1-e30d-41a2-a3ee-1aec759cf789'

connection = {
    "namespace":namespace
}
config = {
    "auth": {
       "tg_host": "panacea.threatgrid.com", "api_key": "test"
    }
}

SAMPLE_DATA_IP = {"data": "20.110.52.48", "dataType": "ip"}
SAMPLE_DATA_HASH = {"data": "16cda323189d8eba4248c0a2f5ad0d8f", "dataType": "hash"}
SAMPLE_DATA_URL = {"data": "linkprotect.cudasvc.com/url", "dataType": "url"}
SAMPLE_DATA_DOMAIN = {"data": "moncleroutlets.com", "dataType": "domain"}

class TestThreatGridTransmission(unittest.TestCase):
    def __init__(self,*args, **kwargs):
        super(TestThreatGridTransmission, self).__init__(*args, **kwargs)
        self.api_client = APIClient(connection, config)
    
    @mock.patch('stix_shifter_modules.threat_grid.stix_transmission.api_client.RestApiClientAsync.call_api')
    async def test_threat_grid_results_ip(self, mock_client_get_json):
        mock_client_get_json.return_value = DATA_TRANS

        response = await self.api_client.get_search_results(SAMPLE_DATA_IP)

        assert response[0]['data']['success'] == True
        assert response[0]['code'] == 200
        assert response[0]['data']['full']
        assert response[1] == namespace

    @mock.patch('stix_shifter_modules.threat_grid.stix_transmission.api_client.RestApiClientAsync.call_api')
    async def test_threat_grid_results_hash(self, mock_client_get_json):
        mock_client_get_json.return_value = DATA_TRANS

        response = await self.api_client.get_search_results(SAMPLE_DATA_HASH)

        assert response[0]['data']['success'] == True
        assert response[0]['code'] == 200
        assert response[0]['data']['full']
        assert response[1] == namespace

    @mock.patch('stix_shifter_modules.threat_grid.stix_transmission.api_client.RestApiClientAsync.call_api')
    async def test_threat_grid_results_URL(self, mock_client_get_json):
        mock_client_get_json.return_value = DATA_TRANS

        response = await self.api_client.get_search_results(SAMPLE_DATA_URL)

        assert response[0]['error']
        assert response[0]['code'] == 401
        assert response[1] == namespace
    
    @mock.patch('stix_shifter_modules.threat_grid.stix_transmission.api_client.RestApiClientAsync.call_api')
    async def test_threat_grid_results_domain(self, mock_client_get_json):
        mock_client_get_json.return_value = DATA_TRANS

        response = await self.api_client.get_search_results(SAMPLE_DATA_DOMAIN)

        assert response[0]['data']['success'] == True
        assert response[0]['code'] == 200
        assert response[0]['data']['full']
        assert response[1] == namespace

    
    @mock.patch('stix_shifter_modules.threat_grid.stix_transmission.api_client.RestApiClientAsync.call_api')
    async def test_threat_grid_ping(self, mock_client_get_json):
        mock_client_get_json.return_value = DATA_TRANS

        ping = PingConnector(self.api_client)
        response = await ping.ping_connection()
        
        assert response['success'] == True