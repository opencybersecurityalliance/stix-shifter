from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync
import base64
import json

SERVER = 'hx/api/v3'
TOKEN_ENDPOINT = '/token'
PING_ENDPOINT = '/agents/sysinfo'
HOST_SET = '/host_sets'
QUERY_ENDPOINT = '/searches'
STATUS_ENDPOINT = '/searches/{search_id}'
RESULTS_ENDPOINT = '/searches/{search_id}/results'
DELETE_ENDPOINT = '/searches/{search_id}'
STOP_SEARCH_ENDPOINT = '/searches/{search_id}/actions'


class APIClient:

    def __init__(self, connection, configuration):

        auth = configuration.get('auth')
        token_decoded = auth['username'] + ':' + auth['password']
        token = base64.b64encode(token_decoded.encode('ascii'))
        self.encoded_token = f'Basic {token.decode("ascii")}'
        self.headers = {'Content-Type': 'application/json'}
        self.client = RestApiClientAsync(connection.get('host'),
                                         connection.get('port'),
                                         self.headers,
                                         cert_verify=connection.get('selfSignedCert', None)
                                         )
        self.timeout = connection['options'].get('timeout')
        self.result_limit = connection['options'].get('result_limit')
        self.progress_threshold = connection['options'].get('progress_threshold')

    async def ping_data_source(self):
        """
        Pings the data source
        :return: response object
        """
        return await self.client.call_api(SERVER + PING_ENDPOINT, 'GET', headers=self.headers,
                                          timeout=self.timeout)

    async def create_search(self, query):
        """
        Create an Enterprise search for the input query
        :param query: dict
        :return: response object
        """

        return await self.client.call_api(SERVER + QUERY_ENDPOINT, 'POST', headers=self.headers,
                                          timeout=self.timeout,
                                          data=json.dumps(query))

    async def get_search_status(self, search_id):
        """
        Fetch the status of the search
        :param search_id: str
        :return: response object
        """
        new_status_endpoint = STATUS_ENDPOINT.replace('{search_id}', str(search_id))
        return await self.client.call_api(SERVER + new_status_endpoint, 'GET', headers=self.headers,
                                          timeout=self.timeout)

    async def get_search_results(self, search_id, offset, limit):
        """
        Fetch the results of the search
        :param search_id: str
        :param offset: int
        :param limit: int
        :return: response object
        """
        params = {"offset": offset, "limit": limit}
        new_results_endpoint = RESULTS_ENDPOINT.replace('{search_id}', str(search_id))
        return await self.client.call_api(SERVER + new_results_endpoint, 'GET', headers=self.headers,
                                          timeout=self.timeout, urldata=params)

    async def delete_search(self, search_id):
        """
        Delete the corresponding search
        :param search_id: str
        :return: response object
        """
        new_del_endpoint = DELETE_ENDPOINT.replace('{search_id}', str(search_id))

        return await self.client.call_api(SERVER + new_del_endpoint, 'DELETE', headers=self.headers,
                                          timeout=self.timeout)

    async def stop_search(self, search_id):
        """ Stops collecting results from the hosts
        :param search_id: str
        :return: response object
        """
        new_stop_search_endpoint = STOP_SEARCH_ENDPOINT.replace('{search_id}', str(search_id))
        return await self.client.call_api(SERVER + new_stop_search_endpoint + '/stop', 'POST', headers=self.headers,
                                          timeout=self.timeout)

    async def generate_token(self):
        """ Generate new token"""
        self.headers['Authorization'] = self.encoded_token
        return await self.client.call_api(SERVER + TOKEN_ENDPOINT, 'GET', headers=self.headers, timeout=self.timeout)

    async def delete_token(self):
        """ Delete the generated API token to close the session"""
        if self.headers.get('X-FeApi-Token'):
            response = await self.client.call_api(SERVER + TOKEN_ENDPOINT, 'DELETE', headers=self.headers,
                                                  timeout=self.timeout)
            if response.code == 204:
                self.headers.pop('X-FeApi-Token')
            else:
                raise Exception

    async def get_host_set(self, host_set):
        """
        Fetching host set details
        """
        params = {"name": host_set}
        return await self.client.call_api(SERVER + HOST_SET, 'GET', headers=self.headers, timeout=self.timeout,
                                          urldata=params)
