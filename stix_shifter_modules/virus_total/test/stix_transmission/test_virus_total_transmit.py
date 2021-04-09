from stix_shifter_modules.virus_total.entry_point import EntryPoint
from stix_shifter_modules.virus_total.stix_transmission.ping_connector import PingConnector
from stix_shifter.stix_transmission import stix_transmission
from stix_shifter_modules.virus_total.stix_transmission.results_connector import ResultsConnector
from unittest.mock import patch
import os
import sys
import pathlib
import unittest

DATA = {
    'code': 200,
    'data': {
        'success': True,
        'summary': {
            'taxonomies': [
                {
                    'level': 'safe',
                    'namespace': 'VT',
                    'predicate': 'GetReport',
                    'value': '0 detected_url(s)'
                }
            ]
        },
        'artifacts': [
            {'dataType': 'url', 'data': 'https://www.icddrb.org/index.php?option=com_content'},
            {'dataType': 'hash', 'data': '190d3a0a0c03d022141434691492cb5966e343800e87cc4d15bbbeeb5abb0460'},
            {'dataType': 'url', 'data': 'https://blog.icddrb.org/'},
            {'dataType': 'fqdn', 'data': 'donate.icddrb.org'}, {'dataType': 'fqdn', 'data': 'www.icddrb.org'}
        ],
        'full': {
            'undetected_urls': [
                ['https://www.icddrb.org/index.php?option=com_content', '190d3a0a0c03d022141434691492cb5966e343800e87cc4d15bbbeeb5abb0460', 0, 84, '2021-03-04 12:11:28'],
                ['https://blog.icddrb.org/', 'a4412675f7e4475e8fb510ebd769720b3c204f4ac4c9d941a9c6ef05d4d7e87e', 0, 83, '2021-01-31 23:26:50'],
                ['https://covid19.icddrb.org/', 'da53fa616bf498d3467a0da87f7f665bd41f4fd6aceae610aa08f2ce269d8b56', 0, 83, '2021-01-25 09:44:17'],
                ['http://www.icddrb.org/', 'f028aa4d7843fbc5abb87bdb61940840b2323b26ec4f47702207e0bcb6429d51', 0, 70, '2019-06-28 08:55:07']
            ],
            'undetected_downloaded_samples': [
                {'date': '2020-11-20 11:08:14', 'positives': 0, 'total': 76, 'sha256': 'f4e301a60e8d885351b8df5614c54f3acc90435022b37fb6803b9a9bf0b0e09a'},
                {'date': '2019-10-16 15:56:26', 'positives': 0, 'total': 72, 'sha256': '14c08afc15e276b96c48de6598e86fcc933f3b105a2a18667d395d82c1ea97d5'}
            ],
            'country': 'BD',
            'response_code': 1,
            'as_owner': 'aamra networks limited',
            'detected_urls': [],
            'verbose_msg': 'IP address in dataset',
            'detected_downloaded_samples': [],
            'resolutions': [
                {'last_resolved': '2019-10-17 01:14:45', 'hostname': 'www.icddrb.org'}
            ],
            'asn': 24323
        }
    }
}
SAMPLE_DATA = '{"data": "203.190.254.239", "dataType": "ip"}'

@patch('stix_shifter_modules.virus_total.stix_transmission.api_client.APIClient', autospec=True)
class TestVirusTotalConnection(unittest.TestCase, object):
    def test_is_async(self, mock_api_client):
        mock_api_client.return_value = None
        entry_point = EntryPoint()
        check_async = entry_point.is_async()
        assert not check_async

    @patch('stix_shifter_utils.utils.loader')
    def test_virus_total_ping(self, mock_loader, mock_api_client):

        mock_api_client.ping_data_source.return_value = {
            'success': False,
            'response': {
                'success': False, 'input': {'config': {'service': 'get', 'key': 'REMOVED'}, 'data': '', 'dataType': ''},
                'errorMessage': 'Invalid data type'
            }
        }
        ping_connector = PingConnector(mock_api_client)
        ping_response = ping_connector.ping_connection()

        assert ping_response['success'] is False
        assert 'error' in ping_response

        mock_api_client.ping_data_source.return_value = {"success": True, "response": DATA}
        mock_loader.return_value = DATA
        ping_connector = PingConnector(mock_api_client)
        ping_response = ping_connector.ping_connection()

        assert ping_response['success'] is True

    @patch('stix_shifter_utils.utils.loader')
    def test_virus_total_results(self, mock_loader, mock_api_client):

        mock_api_client.get_search_results.return_value = DATA
        mock_loader.return_value = DATA

        config = {"host": "sample.host.addr"}
        connection = {"auth": {"key": "APIKEY"}}

        transmission = stix_transmission.StixTransmission("virus_total",  config, connection)
        search_results_response = transmission.results(SAMPLE_DATA, 1, 1)

        assert 'success' in search_results_response and search_results_response['success'] is False

        search_results = ResultsConnector(mock_api_client)
        search_results_response = search_results.create_results_connection(query_data=SAMPLE_DATA, offset=1, length=1)
        report = search_results_response['report']

        assert 'data' in search_results_response
        assert 'dataType' in search_results_response
        assert 'report' in search_results_response
        assert 'success' in search_results_response
        assert search_results_response['success'] is True
        assert report['summary']['taxonomies'][0]['namespace'] == 'VT'
        assert report['full']['response_code'] == 1

    @patch('stix_shifter_utils.utils.loader')
    def test_virus_total_api_client(self, mock_loader, mock_api_client):

        mock_api_client.get_search_results.return_value = DATA
        mock_loader.return_value = DATA
        vt_folder_path = os.path.dirname(os.path.dirname(pathlib.Path().absolute()))
        sys.path.append(vt_folder_path)

        config = {"host": "host.addr"}
        connection = {"auth": {"key": "VT_APIKEY"}}

        transmission = stix_transmission.StixTransmission("virus_total",  config, connection)
        response = transmission.results(SAMPLE_DATA, 1, 1)
        assert 'code' in response['error']
        # self.assertEqual(['error']['data']['errorMessage'], bad_status_message)
        # assert response['error']['data']['config']['key'] == 'REMOVED'
