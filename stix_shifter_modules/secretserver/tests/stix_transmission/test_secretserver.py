
from stix_shifter.stix_transmission import stix_transmission
from stix_shifter_modules.secretserver.entry_point import EntryPoint
from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import Status
import unittest
from unittest.mock import patch


class SecretServerMockResponse:
    def __init__(self, response_code, object):
        self.code = response_code
        self.object = object

    def read(self):
        return self.object

@patch('stix_shifter_modules.secretserver.stix_transmission.api_client.APIClient.__init__', autospec=True)
class TestSecretServerConnection(unittest.TestCase, object):
    def test_is_async(self, mock_api_client):
        mock_api_client.return_value = None
        entry_point = EntryPoint()

        config = {
            "auth": {
                "username": "admin",
                "password": "password123"
            }
        }
        connection = {
            "host": "secretserver.com"
        }
        check_async = entry_point.is_async()

        assert not check_async

    @patch('stix_shifter_modules.secretserver.stix_transmission.api_client.APIClient.create_search')
    def test_query_response(self, mock_query_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = '{"search_id": "eyJxdWVyeSI6ICJTRUxFQ1QgKiBGUk9NIFNlY3JldEV2ZW50RGV0YWlsX25ldyBXSEVSRSBFdmVudFN1YmplY3QgTElLRSAnJSUlJyBTVEFSVCB0JzIwMTktMDEtMjhUMTI6MjQ6MDEuMDA5WicgU1RPUCB0JzIwMjEtMDctMTRUMTI6NTQ6MDEuMDA5WiciLCAidGFyZ2V0IiA6ICJodHRwOi8vOS40Ni44Ni4xMjAvU2VjcmV0U2VydmVyL29hdXRoMi90b2tlbiJ9"}'
        mock_query_response.return_value = SecretServerMockResponse(200, mocked_return_value)

        config = {
            "auth": {
                "username": "admin",
                "password": "password123"
            }
        }
        connection = {
            "host": "secretserver.com",

        }

        query = "[x-secret-finding:name LIKE '%'] START t'2019-01-28T12:24:01.009Z' STOP t'2021-07-14T12:54:01.009Z'"
        transmission = stix_transmission.StixTransmission('secretserver', connection, config)
        query_response = transmission.query(query)

        assert query_response is not None
        assert 'search_id' in query_response
        assert query_response['search_id'] == "eyJxdWVyeSI6ICJTRUxFQ1QgKiBGUk9NIFNlY3JldEV2ZW50RGV0YWlsX25ldyBXSEVSRSBFdmVudFN1YmplY3QgTElLRSAnJSUlJyBTVEFSVCB0JzIwMTktMDEtMjhUMTI6MjQ6MDEuMDA5WicgU1RPUCB0JzIwMjEtMDctMTRUMTI6NTQ6MDEuMDA5WiciLCAidGFyZ2V0IiA6ICJodHRwOi8vOS40Ni44Ni4xMjAvU2VjcmV0U2VydmVyL29hdXRoMi90b2tlbiJ9"

    @patch('stix_shifter_modules.secretserver.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    def test_status_response(self, mock_status_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = '{"search_id": "eyJxdWVyeSI6ICJTRUxFQ1QgKiBGUk9NIFNlY3JldEV2ZW50RGV0YWlsX25ldyBXSEVSRSBFdmVudFN1YmplY3QgTElLRSAnJSUlJyBTVEFSVCB0JzIwMTktMDEtMjhUMTI6MjQ6MDEuMDA5WicgU1RPUCB0JzIwMjEtMDctMTRUMTI6NTQ6MDEuMDA5WiciLCAidGFyZ2V0IiA6ICJodHRwOi8vOS40Ni44Ni4xMjAvU2VjcmV0U2VydmVyL29hdXRoMi90b2tlbiJ9", "status": "COMPLETED", "progress": "100"}'
        mock_status_response.return_value = SecretServerMockResponse(200, mocked_return_value)

        config = {
            "auth": {
                "username": "admin",
                "password": "password123"
            }
        }
        connection = {

            "host": "secretserver.com",

        }

        search_id = "eyJxdWVyeSI6ICJTRUxFQ1QgKiBGUk9NIFNlY3JldEV2ZW50RGV0YWlsX25ldyBXSEVSRSBFdmVudFN1YmplY3QgTElLRSAnJSUlJyBTVEFSVCB0JzIwMTktMDEtMjhUMTI6MjQ6MDEuMDA5WicgU1RPUCB0JzIwMjEtMDctMTRUMTI6NTQ6MDEuMDA5WiciLCAidGFyZ2V0IiA6ICJodHRwOi8vOS40Ni44Ni4xMjAvU2VjcmV0U2VydmVyL29hdXRoMi90b2tlbiJ9"
        transmission = stix_transmission.StixTransmission('secretserver', connection, config)
        status_response = transmission.status(search_id)

        assert status_response['success']
        assert status_response is not None
        assert 'status' in status_response
        assert status_response['status'] == Status.COMPLETED.value

    @patch('stix_shifter_modules.secretserver.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    def test_results_response(self, mock_results_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = """{
               "success": true, 
               "data": [
                   "ItemId": 1,
                   "SecretName":"abc,
                   "EventTime":"2021-07-06T02:56:58.413",
                   "EventSubject" : "[[SecretServer]] [Secret] MySql_130 [Check Out] by New",
                   "IpAddress": "127.0.0.1",
                    "username": "New",
                    "Server": "9.202.181.130"
                       
                   ]
           }"""
        mock_results_response.return_value = SecretServerMockResponse(200, mocked_return_value)

        config = {
            "auth": {
                "username": "admin",
                "password": "password123"
            }
        }
        connection = {

            "host": "secretserver.com",

        }

        search_id = "eyJxdWVyeSI6ICJTRUxFQ1QgKiBGUk9NIFNlY3JldEV2ZW50RGV0YWlsX25ldyBXSEVSRSBFdmVudFN1YmplY3QgTElLRSAnJSUlJyBTVEFSVCB0JzIwMTktMDEtMjhUMTI6MjQ6MDEuMDA5WicgU1RPUCB0JzIwMjEtMDctMTRUMTI6NTQ6MDEuMDA5WiciLCAidGFyZ2V0IiA6ICJodHRwOi8vOS40Ni44Ni4xMjAvU2VjcmV0U2VydmVyL29hdXRoMi90b2tlbiJ9"
        offset = 0
        length = 1
        transmission = stix_transmission.StixTransmission('secretserver', connection, config)
        results_response = transmission.results(search_id, offset, length)

        assert results_response is not None
        assert results_response['success']
        assert 'data' in results_response
