from stix_shifter_modules.okta.entry_point import EntryPoint
import unittest
from unittest.mock import patch
from stix_shifter.stix_transmission import stix_transmission
import json
from stix_shifter.stix_transmission.stix_transmission import run_in_thread
from tests.utils.async_utils import get_mock_response


class OktaMockResponse:
    """ class for okta mock response"""

    def __init__(self, code, data, headers):
        self.code = code
        self.content = data
        self.headers = headers

    def read(self):
        return bytearray(self.content, 'utf-8')


class TestOktaConnection(unittest.TestCase, object):
    mocked_response = [{
        'actor': {
            'id': '00u85ek33bjW0rqu75d7',
            'type': 'User',
            'alternateId': 'aps@google.com',
            'displayName': 'aps',
            'detailEntry': None
        },
        'client': {
            'userAgent': {
                'rawUserAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 '
                                '(KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
                'os': 'Windows 10',
                'browser': 'CHROME'
            },
            'zone': 'null',
            'device': 'Computer',
            'id': None,
            'ipAddress': '1.1.1.1',
            'geographicalContext': {
                'city': None,
                'state': None,
                'country': 'India',
                'postalCode': None,
                'geolocation': {
                    'lat': 21.9974,
                    'lon': 79.0011
                }
            }
        },
        'device': None,
        'authenticationContext': {
            'authenticationProvider': None,
            'credentialProvider': None,
            'credentialType': None,
            'issuer': None,
            'interface': None,
            'authenticationStep': 0,
            'externalSessionId': '102SVz3tGtUS9iOMunoGfsHOw'
        },
        'displayMessage': 'Activate factor for user',
        'eventType': 'user.mfa.factor.activate',
        'outcome': {
            'result': 'SUCCESS',
            'reason': 'User set up EMAIL_FACTOR factor'
        },
        'published': '2023-01-30T14:18:01.558Z',
        'securityContext': {
            'asNumber': 396982,
            'asOrg': 'avago technologies u.s. inc.',
            'isp': 'google',
            'domain': '.',
            'isProxy': False
        },
        'severity': 'INFO',
        'debugContext': {
            'debugData': {
                'requestId': 'Y9fRmYykc1ctVN0C0LEKkgAABQw',
                'dtHash': '699c736419fe6b1f1f991d986b6be07d782d67352161ace7dd768c7c7a3c344a',
                'requestUri': '/api/v1/users',
                'url': '/api/v1/users?activate=true'
            }
        },
        'legacyEventType': 'core.user.factor.activate',
        'transaction': {
            'type': 'WEB',
            'id': 'Y9fRmYykc1ctVN0C0LEKkgAABQw',
            'detail': {}
        },
        'uuid': 'e766d84e-a0a8-11ed-a750-9f5fc296ce63',
        'version': '0',
        'request': {
            'ipChain': [{
                'ip': '2.2.2.2',
                'geographicalContext': {
                    'city': 'Chennai',
                    'state': 'Tamil Nadu',
                    'country': 'India',
                    'postalCode': '600002',
                    'geolocation': {
                        'lat': 12.8996,
                        'lon': 80.2209
                    }
                },
                'version': 'V4',
                'source': None
            }, {
                'ip': '1.1.1.1',
                'geographicalContext': {
                    'city': None,
                    'state': None,
                    'country': 'India',
                    'postalCode': None,
                    'geolocation': {
                        'lat': 21.9974,
                        'lon': 79.0011
                    }
                },
                'version': 'V4',
                'source': None
            }]
        },
        'target': [{
            'id': '00u85ek33bjW0rqu75d7',
            'type': 'User',
            'alternateId': 'aps@google.com',
            'displayName': 'aps',
            'detailEntry': None
        }]
    }]

    def connection(self):
        """format for connection"""
        return {
            "host": "hostbla"
        }

    def configuration(self):
        """format for configuration"""
        return {
            "auth": {
                "api_token": "u"
            }
        }

    def test_is_async(self):
        """check for synchronous or asynchronous"""
        entry_point = EntryPoint(self.connection(), self.configuration())
        check_async = entry_point.is_async()
        assert check_async is False

    @patch('stix_shifter_modules.okta.stix_transmission.api_client.APIClient.ping_data_source')
    def test_get_ping_results(self, mock_ping_response):
        """test ping connection"""
        mock_ping_response.return_value = get_mock_response(200, json.dumps(TestOktaConnection.mocked_response), 'byte')
        entry_point = EntryPoint(self.connection(), self.configuration())
        ping_response = run_in_thread(entry_point.ping_connection)
        assert ping_response is not None
        assert ping_response['success'] is True

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_success_query_results(self, mock_result_response):
        """ test success result response"""
        mocked_return_value = json.dumps(TestOktaConnection.mocked_response)
        headers = {
            'Link': '<https://ourhost/api/v1/logs?since=2023-01-19T11%3A00%3A00.000Z'
                    '&until=2023-01-31T11%3A00%3A00.003Z&limit=1000&filter=request.ipChain.ip+eq+%221.1.1.1%22+>'
                    '; rel="self"'}
        query = "filter=request.ipChain.ip eq \"1.1.1.1\" &since=2023-01-19T11:00:00.000Z" \
                "&until=2023-01-31T11:00:00.003Z"
        mock_result_response.return_value = OktaMockResponse(200, mocked_return_value, headers)
        transmission = stix_transmission.StixTransmission('okta', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is True
        assert 'data' in result_response
        assert result_response['data'] == [{
            'actor': {
                'id': '00u85ek33bjW0rqu75d7',
                'type': 'User',
                'alternateId': 'aps@google.com',
                'displayName': 'aps',
                'detailEntry': None
            },
            'client': {
                'userAgent': {
                    'rawUserAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) '
                                    'Chrome/109.0.0.0 Safari/537.36',
                    'os': 'Windows 10',
                    'browser': 'CHROME'
                },
                'zone': 'null',
                'device': 'Computer',
                'id': None,
                'ipAddress': '1.1.1.1',
                'geographicalContext': {
                    'city': None,
                    'state': None,
                    'country': 'India',
                    'postalCode': None,
                    'geolocation': {
                        'lat': 21.9974,
                        'lon': 79.0011
                    }
                }
            },
            'device': None,
            'authenticationContext': {
                'authenticationProvider': None,
                'credentialProvider': None,
                'credentialType': None,
                'issuer': None,
                'interface': None,
                'authenticationStep': 0,
                'externalSessionId': '102SVz3tGtUS9iOMunoGfsHOw'
            },
            'displayMessage': 'Activate factor for user',
            'eventType': 'user.mfa.factor.activate',
            'outcome': {
                'result': 'SUCCESS',
                'reason': 'User set up EMAIL_FACTOR factor'
            },
            'published': '2023-01-30T14:18:01.558Z',
            'securityContext': {
                'asNumber': 396982,
                'asOrg': 'avago technologies u.s. inc.',
                'isp': 'google',
                'isProxy': False
            },
            'severity': 'INFO',
            'debugContext': [{
                'debugData': {
                    'requestId': 'Y9fRmYykc1ctVN0C0LEKkgAABQw',
                    'dtHash': '699c736419fe6b1f1f991d986b6be07d782d67352161ace7dd768c7c7a3c344a',
                    'requestUri': '/api/v1/users',
                    'url': '/api/v1/users?activate=true'
                }
            }],
            'legacyEventType': 'core.user.factor.activate',
            'transaction': {
                'type': 'WEB',
                'id': 'Y9fRmYykc1ctVN0C0LEKkgAABQw',
                'detail': {}
            },
            'uuid': 'e766d84e-a0a8-11ed-a750-9f5fc296ce63',
            'version': '0',
            'request': {
                'ipChain': {
                    'ip': ['2.2.2.2']
                }
            },
            'target': [{
                'id': '00u85ek33bjW0rqu75d7',
                'type': 'User',
                'alternateId': 'aps@google.com',
                'displayName': 'aps',
                'detailEntry': None
            }]
        }]

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_sucess_query_with_pagination_results(self, mock_result_response):
        """ test success pagination result response """
        mocked_response_1 = [{
            "actor": {
                "id": "00u4oexp0nQ82Fx405d7",
                "type": "User",
                "alternateId": "kd@hcl.com",
                "displayName": "kk",
                "detailEntry": None
            },
            "client": {
                "userAgent": {
                    "rawUserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                    "(KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
                    "os": "Windows 10",
                    "browser": "CHROME"
                },
                "zone": "null",
                "device": "Computer",
                "id": None,
                "ipAddress": "1.2.2.3",
                "geographicalContext": {
                    "city": "Ashburn",
                    "state": "Virginia",
                    "country": "United States",
                    "postalCode": "20149",
                    "geolocation": {
                        "lat": 39.0469,
                        "lon": -77.4903
                    }
                }
            },
            "device": None,
            "authenticationContext": {
                "authenticationProvider": None,
                "credentialProvider": None,
                "credentialType": None,
                "issuer": None,
                "interface": None,
                "authenticationStep": 0,
                "externalSessionId": "idxLW553XTNSo-z-E6y3Myslg"
            },
            "displayMessage": "User login to Okta",
            "eventType": "user.session.start",
            "outcome": {
                "result": "FAILURE",
                "reason": "INVALID_CREDENTIALS"
            },
            "published": "2022-11-17T06:27:22.463Z",
            "securityContext": {
                "asNumber": 14618,
                "asOrg": "amazon data services nova",
                "isp": "amazon.com  inc.",
                "domain": "amazonaws.com",
                "isProxy": False
            },
            "severity": "WARN",
            "debugContext": {
                "debugData": {
                    "deviceFingerprint": "79b3d09740e361498e304e60a2f2d398",
                    "requestId": "Y3XUSWl9qTFxJTRaZiEMEwAAB5o",
                    "dtHash": "90e356b2709974d2d7d2a55c48d478292c674a4026a5e6d4a011e0f6c57f0f29",
                    "requestUri": "/idp/idx/identify",
                    "threatSuspected": "false",
                    "url": "/idp/idx/identify?"
                }
            },
            "legacyEventType": "core.user_auth.login_failed",
            "transaction": {
                "type": "WEB",
                "id": "Y3XUSWl9qTFxJTRaZiEMEwAAB5o",
                "detail": {}
            },
            "uuid": "e5056745-6640-11ed-869e-9507ab80c238",
            "version": "0",
            "request": {
                "ipChain": [
                    {
                        "ip": "1.2.2.3",
                        "geographicalContext": {
                            "city": "Ashburn",
                            "state": "Virginia",
                            "country": "United States",
                            "postalCode": "20149",
                            "geolocation": {
                                "lat": 39.0469,
                                "lon": -77.4903
                            }
                        },
                        "version": "V4",
                        "source": None
                    }
                ]
            },
            "target": [
                {
                    "id": "laefh9uuieEi7TCR55d6",
                    "type": "AuthenticatorEnrollment",
                    "alternateId": "unknown",
                    "displayName": "Password",
                    "detailEntry": None
                },
                {
                    "id": "0oa4oexov63QrxhVt5d7",
                    "type": "AppInstance",
                    "alternateId": "Okta Admin Console",
                    "displayName": "Okta Admin Console",
                    "detailEntry": None
                }
            ]
        }]
        mocked_response_2 = [{
            "actor": {
                "id": "00u4oexp0nQ82Fx405d7",
                "type": "User",
                "alternateId": "kd@hcl.com",
                "displayName": "kk",
                "detailEntry": None
            },
            "client": {
                "userAgent": {
                    "rawUserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                    "(KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
                    "os": "Windows 10",
                    "browser": "CHROME"
                },
                "zone": "null",
                "device": "Computer",
                "id": None,
                "ipAddress": "1.2.2.3",
                "geographicalContext": {
                    "city": "Ashburn",
                    "state": "Virginia",
                    "country": "United States",
                    "postalCode": "20149",
                    "geolocation": {
                        "lat": 39.0469,
                        "lon": -77.4903
                    }
                }
            },
            "device": None,
            "authenticationContext": {
                "authenticationProvider": "FACTOR_PROVIDER",
                "credentialProvider": "OKTA_CREDENTIAL_PROVIDER",
                "credentialType": None,
                "issuer": None,
                "interface": None,
                "authenticationStep": 0,
                "externalSessionId": "idxLW553XTNSo-z-E6y3Myslg"
            },
            "displayMessage": "Authentication of user via MFA",
            "eventType": "user.authentication.auth_via_mfa",
            "outcome": {
                "result": "FAILURE",
                "reason": "INVALID_CREDENTIALS"
            },
            "published": "2022-11-17T06:27:22.460Z",
            "securityContext": {
                "asNumber": 14618,
                "asOrg": "amazon data services nova",
                "isp": "amazon.com  inc.",
                "domain": "amazonaws.com",
                "isProxy": False
            },
            "severity": "INFO",
            "debugContext": {
                "debugData": {
                    "deviceFingerprint": "79b3d09740e361498e304e60a2f2d398",
                    "requestId": "Y3XUSWl9qTFxJTRaZiEMEwAAB5o",
                    "dtHash": "90e356b2709974d2d7d2a55c48d478292c674a4026a5e6d4a011e0f6c57f0f29",
                    "requestUri": "/idp/idx/identify",
                    "threatSuspected": "false",
                    "factor": "PASSWORD_AS_FACTOR",
                    "factorIntent": "AUTHENTICATION",
                    "url": "/idp/idx/identify?"
                }
            },
            "legacyEventType": "core.user.factor.attempt_fail",
            "transaction": {
                "type": "WEB",
                "id": "Y3XUSWl9qTFxJTRaZiEMEwAAB5o",
                "detail": {}
            },
            "uuid": "e504f214-6640-11ed-869e-9507ab80c238",
            "version": "0",
            "request": {
                "ipChain": [
                    {
                        "ip": "11.111.111",
                        "geographicalContext": {
                            "city": "Ashburn",
                            "state": "Virginia",
                            "country": "United States",
                            "postalCode": "20149",
                            "geolocation": {
                                "lat": 39.0469,
                                "lon": -77.4903
                            }
                        },
                        "version": "V4",
                        "source": None
                    }
                ]
            },
            "target": [
                {
                    "id": "00u4oexp0nQ82Fx405d7",
                    "type": "User",
                    "alternateId": "kd@hcl.com",
                    "displayName": "kk",
                    "detailEntry": None
                },
                {
                    "id": "laefh9uuieEi7TCR55d6",
                    "type": "AuthenticatorEnrollment",
                    "alternateId": "unknown",
                    "displayName": "Password",
                    "detailEntry": {
                        "methodTypeUsed": "Password"
                    }
                }
            ]
        }]
        mocked_return_value_1 = json.dumps(mocked_response_1)
        mocked_return_value_2 = json.dumps(mocked_response_2)
        headers_1 = {
            'Link': '<https://ourhost/api/v1/logs?since=2022-01-19T11%3A00%3A00.000Z&'
                    'until=2023-01-31T11%3A00%3A00.003Z&filter=request.ipChain.ip+ne+%221.1.1.1%22+&'
                    'after=1670301642462_1>; rel="next"'}
        headers_2 = {'Link': '<https://ourhost/api/v1/logs?since=2022-01-19T11%3A00%3A00.000Z&'
                             'until=2023-01-31T11%3A00%3A00.003Z&filter=request.ipChain.ip+ne+%221.1.1.1%22+&'
                             'after=1670301642453_1>; rel="next"'}
        query = "filter=request.ipChain.ip ne \"1.1.1.1\" &since=2022-01-19T11:00:00.000Z" \
                "&until=2023-01-31T11:00:00.003Z"
        response_1 = OktaMockResponse(200, mocked_return_value_1, headers_1)
        response_2 = OktaMockResponse(200, mocked_return_value_2, headers_2)
        mock_result_response.side_effect = [response_1, response_2]
        connection_with_limit = {
            "host": "hostbla",
            "options": {"result_limit": 3}
        }
        transmission = stix_transmission.StixTransmission('okta', connection_with_limit, self.configuration())
        offset = 0
        length = 2
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is True
        assert 'data' in result_response
        assert result_response['data'][0]['client']['ipAddress'] == '1.2.2.3'
        assert 'request' not in result_response['data'][0]
        assert type(result_response['data'][0]['debugContext']) is list
        assert 'metadata' in result_response
        assert result_response['metadata']['next_page_token'] == "after=1670301642453_1"

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_ping_invalid_host(self, mock_result_response):
        """Test Invalid host for ping"""
        mock_result_response.side_effect = Exception("client_connector_error")
        transmission = stix_transmission.StixTransmission('okta', self.connection(), self.configuration())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert "client_connector_error" in ping_response['error']
        assert ping_response['code'] == "service_unavailable"

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_ping_invalid_auth(self, mock_results_response):
        """Test invalid authentication for ping"""
        error = json.dumps({'errorSummary': 'Invalid session'})
        mock_results_response.return_value = get_mock_response(401, error, 'byte')
        transmission = stix_transmission.StixTransmission('okta', self.connection(), self.configuration())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert ping_response['code'] == "authentication_fail"
        assert "Invalid session" in ping_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_results_invalid_auth(self, mock_results_response):
        """Test invalid authentication for results"""
        error = json.dumps({'errorSummary': 'Invalid session'})
        query = "filter=request.ipChain.ip ne \"1.1.1.1\" &since=2022-01-19T11:00:00.000Z" \
                "&until=2023-01-31T11:00:00.003Z"
        mock_results_response.return_value = get_mock_response(401, error, 'byte')
        transmission = stix_transmission.StixTransmission('okta', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert result_response['code'] == "authentication_fail"
        assert 'Invalid session' in result_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_exception_for_ping_results(self, mock_ping_response):
        """Test General Exception for ping"""
        mock_ping_response.return_value = get_mock_response(200, """Invalid Json""", 'byte')
        transmission = stix_transmission.StixTransmission('okta', self.connection(), self.configuration())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert 'error' in ping_response
        assert 'Expecting value: line 1 column 1 (char 0)' in ping_response['error']

    @patch('stix_shifter_modules.okta.stix_transmission.api_client.APIClient.get_search_results')
    def test_exception_for_search_results(self, mock_result_response):
        """Test General Exception for results"""
        mock_result_response.return_value = get_mock_response(200, """[success=true]""", 'byte')
        query = "filter=client.device ne \"Computer\" and transaction.detail.requestApiTokenId co" \
                " \"00Tr22hj9U9LzFH0f5d6\" &since=2023-02-10T08:52:26.900Z&until=2023-02-10T08:57:26.900Z"
        transmission = stix_transmission.StixTransmission('okta', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert 'error' in result_response
        assert 'Expecting value: line 1 column 2 (char 1)' in result_response['error']

    @patch('stix_shifter_modules.okta.stix_transmission.api_client.APIClient.get_search_results')
    def test_connection_error_results(self, mock_result_response):
        """Test Invalid host for results"""
        mock_result_response.side_effect = Exception("client_connector_error")
        query = "filter=client.device ne \"Computer\" and transaction.detail.requestApiTokenId co " \
                "\"00Tr22hj9U9LzFH0f5d6\" &since=2023-02-10T08:52:26.900Z&until=2023-02-10T08:57:26.900Z"
        transmission = stix_transmission.StixTransmission('okta', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert "client_connector_error" in result_response['error']
        assert result_response['code'] == "service_unavailable"

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_success_query_with_metadata_parameter(self, mock_result_response):
        """ test success result response with metadata parameter"""
        mocked_return_value = json.dumps(TestOktaConnection.mocked_response)
        metadata = {"result_count": 200, 'next_page_token': '123a'}
        headers = {
            'Link': '<https://ourhost/api/v1/logs?since=2023-01-19T11%3A00%3A00.000Z'
                    '&until=2023-01-31T11%3A00%3A00.003Z&limit=1000&filter=request.ipChain.ip+eq+%221.1.1.1%22+>'
                    '; rel="self"'}
        query = "filter=request.ipChain.ip eq \"1.1.1.1\" &since=2023-01-19T11:00:00.000Z" \
                "&until=2023-01-31T11:00:00.003Z"
        mock_result_response.return_value = OktaMockResponse(200, mocked_return_value, headers)
        transmission = stix_transmission.StixTransmission('okta', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length, metadata)
        assert result_response is not None
        assert result_response['success'] is True
        assert 'data' in result_response

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_with_invalid_metadata_parameter(self, mock_result_response):
        """ test invalid metadata parameter"""
        mocked_return_value = json.dumps(TestOktaConnection.mocked_response)
        metadata = {'next_page_token': '123a'}
        headers = {
            'Link': '<https://ourhost/api/v1/logs?since=2023-01-19T11%3A00%3A00.000Z'
                    '&until=2023-01-31T11%3A00%3A00.003Z&limit=1000&filter=request.ipChain.ip+eq+%221.1.1.1%22+>'
                    '; rel="self"'}
        query = "filter=request.ipChain.ip eq \"1.1.1.1\" &since=2023-01-19T11:00:00.000Z" \
                "&until=2023-01-31T11:00:00.003Z"
        mock_result_response.return_value = OktaMockResponse(200, mocked_return_value, headers)
        transmission = stix_transmission.StixTransmission('okta', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length, metadata)
        assert result_response is not None
        assert result_response['success'] is False
        assert "Invalid metadata" in result_response['error']
        assert result_response['code'] == "invalid_parameter"

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_results_with_429_request_exception(self, mock_result_response):
        """ test 429 exception in results"""
        query = "filter=request.ipChain.ip eq \"1.1.1.1\" &since=2022-01-19T11:00:00.000Z" \
                "&until=2023-01-31T11:00:00.003Z"
        mock_result_response.side_effect = Exception("too_many_requests with max retry")
        transmission = stix_transmission.StixTransmission('okta', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert result_response['code'] == 'too_many_requests'

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_results_with_invaid_exception_during_pagination(self, mock_result_response):
        """ test 401 error code during pagination"""
        mocked_return_value = json.dumps(TestOktaConnection.mocked_response)
        headers = {'Link': '<https://ourhost/api/v1/logs?since=2022-01-19T11%3A00%3A00.000Z&'
                           'until=2023-01-31T11%3A00%3A00.003Z&filter=request.ipChain.ip+eq+%221.1.1.1%22+&'
                           'after=1670301642453_1>; rel="next"'}
        query = "filter=request.ipChain.ip eq \"1.1.1.1\" &since=2022-01-19T11:00:00.000Z" \
                "&until=2023-01-31T11:00:00.003Z"
        error = json.dumps({'errorSummary': 'Invalid session'})
        result_response = OktaMockResponse(200, mocked_return_value, headers)
        mock_result_response.side_effect = [result_response, OktaMockResponse(403, error, {})]
        transmission = stix_transmission.StixTransmission('okta', self.connection(), self.configuration())
        offset = 0
        length = 5
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert 'Invalid session' in result_response['error']
        assert result_response['code'] == 'forbidden'

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_time_out_exception_for_results(self, mock_result_response):
        """Test timeout exception for results"""
        mock_result_response.side_effect = Exception("timeout_error")
        query = "filter=client.device ne \"Computer\" and transaction.detail.requestApiTokenId co" \
                " \"00Tr22hj9U9LzFH0f5d6\" &since=2023-02-10T08:52:26.900Z&until=2023-02-10T08:57:26.900Z"
        transmission = stix_transmission.StixTransmission('okta', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert 'error' in result_response
        assert 'timeout_error' in result_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_time_out_exception_for_ping(self, mock_ping_response):
        """Test timeout exception for ping"""
        mock_ping_response.side_effect = Exception("timeout_error")
        transmission = stix_transmission.StixTransmission('okta', self.connection(), self.configuration())
        result_response = transmission.ping()
        assert result_response is not None
        assert result_response['success'] is False
        assert 'error' in result_response
        assert 'timeout_error' in result_response['error']
