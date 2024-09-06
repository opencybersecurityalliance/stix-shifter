import json
from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync

class SecuronixAPIClient:
    def __init__(self, connection, configuration):
        """
        Initializes the Securonix API client.
        """
        self.authenticated = False
        headers = {}
        self.client = RestApiClientAsync(
                                         headers,
                                         )


        self.auth = configuration.get('auth')
        self.endpoint_start = self.auth.get('base_url')
        self.endpoint_start = self.endpoint_start + '/ws/'
        self.headers = headers
        self.timeout = connection['options'].get('timeout')

    async def authenticate(self):
        """Method to authenticate."""
        if not self.authenticated:
            await self.set_securonix_auth_token(self.auth, self.headers)
            self.authenticated = True

    async def set_securonix_auth_token(self, auth, headers):
        """Method to set Securonix auth token."""
        params = {
            'username': auth['username'],
            'password': auth['password'],
            'validity': '365'
        }
        endpoint = self.endpoint_start + 'token/generate'
        try:
            response = await self.client.call_api(endpoint, 'GET', headers, urldata=params, timeout=self.timeout)
            response_json = json.loads(response.read())
            headers['token'] = response_json['token']
        except KeyError as e:
            raise Exception('Authentication error occurred while getting auth token: ' + str(e))

    async def ping_box(self):
        """Ping or check the system status."""
        await self.authenticate()
        endpoint = self.endpoint_start + 'incident/listAllTenants'
        return await self.client.call_api(endpoint, 'GET', headers=self.headers, timeout=self.timeout)

    async def search_by_ip(self, query_expression):
        """Search incidents by IP address."""
        await self.authenticate()
        params = {'query': query_expression}
        # How to get these here ? 
        # if start_time and end_time:
        #     params['eventtime_from'] = start_time
        #     params['eventtime_to'] = end_time
        endpoint = self.endpoint_start + 'spotter/index/search'
        return await self.client.call_api(endpoint, 'GET', headers=self.headers, urldata=params, timeout=self.timeout)

    async def search_by_hash(self, query_expression):
        """Search incidents by file hash."""
        await self.authenticate()
        params = {'query': query_expression}
        # if start_time and end_time:
        #     params['eventtime_from'] = start_time
        #     params['eventtime_to'] = end_time
        endpoint = self.endpoint_start + 'spotter/index/search'
        return await self.client.call_api(endpoint, 'GET', headers=self.headers, urldata=params, timeout=self.timeout)

    async def search_by_domain(self, query_expression):
        """Search incidents by domain."""
        await self.authenticate()
        params = {'query': query_expression}
        # if start_time and end_time:
        #     params['eventtime_from'] = start_time
        #     params['eventtime_to'] = end_time
        endpoint = self.endpoint_start + 'spotter/index/search'
        return await self.client.call_api(endpoint, 'GET', headers=self.headers, urldata=params, timeout=self.timeout)
