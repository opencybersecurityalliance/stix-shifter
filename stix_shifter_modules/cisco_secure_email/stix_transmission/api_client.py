import base64
import json
from urllib import parse
from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync


class APIClient:
    QUERY_ENDPOINT = "esa/api/v2.0/message-tracking/messages?searchOption=messages&"
    PING_ENDPOINT = "esa/api/v2.0/login/privileges"
    TOKEN_ENDPOINT = "esa/api/v2.0/login"

    def __init__(self, connection, configuration):
        self.auth = configuration.get('auth')
        self.headers = {'Content-Type': 'application/json'}
        self.client = RestApiClientAsync(connection.get('host'), connection.get('port'), headers=self.headers,
                                         cert_verify=connection.get('selfSignedCert'))
        self.result_limit = connection['options'].get('result_limit')
        self.timeout = connection['options'].get('timeout')

    async def ping_data_source(self, token):
        """
        Ping the Data Source
        :return: Response object
        """
        self.headers['jwtToken'] = token
        return await self.client.call_api(self.PING_ENDPOINT, 'GET', headers=self.headers, data={},
                                          timeout=self.timeout)

    async def get_search_results(self, query, token):
        """
        Get results from Data Source
        :param query: Data Source Query
        :param token: Authentication token
        :return: Response Object
        """
        self.headers['jwtToken'] = token
        query = self.QUERY_ENDPOINT + parse.quote(query, safe='&,=')

        return await self.client.call_api(query, 'GET', headers=self.headers, data={}, timeout=self.timeout)

    async def generate_token(self):
        """Get Authorization token"""
        username = f"{base64.b64encode(self.auth['username'].encode('utf-8')).decode('utf-8')}"
        password = f"{base64.b64encode(self.auth['password'].encode('utf-8')).decode('utf-8')}"
        data = {
            "data": {
                "userName": username,
                "passphrase": password
            }
        }
        if 'jwtToken' in self.headers:
            self.headers.pop('jwtToken')
        payload = json.dumps(data)
        return await self.client.call_api(self.TOKEN_ENDPOINT, 'POST', headers=self.headers, data=payload,
                                          timeout=self.timeout)
