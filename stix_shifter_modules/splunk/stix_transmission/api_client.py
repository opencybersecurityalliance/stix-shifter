import json
from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync


class APIClient():
    # API METHODS

    # These methods are used to call Splunk's API methods through http requests.
    # Each method makes use of the http methods below to perform the requests.

    # This class will encode any data or query parameters which will then be
    # sent to the call_api() method of its inherited class.

    def __init__(self, connection, configuration):

        # This version of the Splunk APIClient is designed to function with
        # Splunk Enterprise version >= 6.5.0 and <= 7.1.2
        # http://docs.splunk.com/Documentation/Splunk/7.1.2/RESTREF/RESTprolog .

        self.output_mode = 'json'
        self.endpoint_start = 'services/'
        self.authenticated = False
        headers = {}
        self.client = RestApiClientAsync(connection.get('host'),
                                    connection.get('port'),
                                    headers,
                                    cert_verify=connection.get('selfSignedCert', True)
                                    )
        self.auth = configuration.get('auth')
        self.headers = headers
        self.timeout = connection['options'].get('timeout')

    async def authenticate(self):
        """ method to authenticate """
        if not self.authenticated:
            await self.set_splunk_auth_token(self.auth, self.headers)
            self.authenticated = True

    async def set_splunk_auth_token(self, auth, headers):
        """ method to set splunk auth token """
        data = {'username': auth['username'], 'password': auth['password'], 'output_mode': 'json'}
        endpoint = self.endpoint_start + 'auth/login'
        try:
            data = await self.client.call_api(endpoint, 'POST', headers, data=data, timeout=self.timeout)
            response_json = json.load(data)
            headers['Authorization'] = "Splunk " + response_json['sessionKey']
        except KeyError as e:
            raise Exception('Authentication error occured while getting auth token: ' + str(e))

    async def ping_box(self):
        """
        ping or check the system status
        """
        await self.authenticate()
        endpoint = self.endpoint_start
        data = {'output_mode': self.output_mode}
        return await self.client.call_api(endpoint, 'GET', data=data, timeout=self.timeout)

    async def create_search(self, query_expression):
        """
        init query
        :param data source query
        :return:queryId
        """
        # sends a POST request to
        # https://<server_ip>:<port>/services/search/jobs
        await self.authenticate()
        endpoint = self.endpoint_start + "search/jobs"
        data = {'search': query_expression, 'output_mode': self.output_mode}
        return await self.client.call_api(endpoint, 'POST', data=data, timeout=self.timeout)

    async def get_search(self, search_id):
        """
        get query status
        :param queryId:
        :return: information about the search job and its properties
        """
        # sends a GET request to
        # https://<server_ip>:<port>/services/search/jobs/<search_id>
        # returns information about the search job and its properties.
        await self.authenticate()
        endpoint = self.endpoint_start + 'search/jobs/' + search_id
        data = {'output_mode': self.output_mode}
        return await self.client.call_api(endpoint, 'GET', data=data, timeout=self.timeout)

    async def get_search_results(self, search_id, offset, count):
        """
        Get results from Data Source
        :param query: Data Source search_id,offset,count
        :return: Response Object
        """
        # sends a GET request to
        # https://<server_ip>:<port>/services/search/jobs/<search_id>/results
        # returns results associated with the search job.
        await self.authenticate()
        endpoint = self.endpoint_start + "search/v2/jobs/" + search_id + '/results'
        data = {'output_mode': self.output_mode}
        if ((offset is not None) and (count is not None)):
            data['offset'] = str(offset)
            data['count'] = str(count)
        # response object body should contain information pertaining to search.
        return await self.client.call_api(endpoint, 'GET', urldata=data, timeout=self.timeout)

    async def delete_search(self, search_id):
        """
        :param search_id:
        :return:dict
        """
        # sends a DELETE request to
        # https://<server_ip>:<port>/services/search/jobs/<search_id>
        # cancels and deletes search created earlier.
        await self.authenticate()
        endpoint = self.endpoint_start + 'search/jobs/' + search_id
        data = {'output_mode': self.output_mode}
        return await self.client.call_api(endpoint, 'DELETE', data=data, timeout=self.timeout)
