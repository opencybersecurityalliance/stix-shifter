from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync
import json

PING_ENDPOINT = 'api/v1/status'
JOB_ENDPOINT = 'api/v1/repositories'

class APIClient:

    def __init__(self, connection, configuration):
        auth = configuration.get('auth')
        self.headers = {"Authorization": f"Bearer {auth.get('api_token')}", "Content-Type": "application/json",
                        "Accept": "application/json"}
        self.client = RestApiClientAsync(connection.get('host'), headers=self.headers)
        self.timeout = connection['options'].get('timeout')
        self.result_limit = connection['options'].get('result_limit')
        self.api_page_size = connection['options'].get('api_page_size')
        self.api_endpoint = f"{JOB_ENDPOINT}/{connection.get('repository')}/queryjobs"

    async def ping_data_source(self):
        """
        Pings the data source
        :return: response object
        """
        return await self.client.call_api(PING_ENDPOINT, 'GET', headers=self.headers, data={})

    async def create_search(self, query_expression):
        """
        Create an Enterprise search for the input query
        :param query_expression: dict
        :return: response object
        """
        return await self.client.call_api(self.api_endpoint, 'POST', headers=self.headers,
                                          data=json.dumps(query_expression),
                                          timeout=self.timeout)

    async def poll_query_job(self, search_id):
        """
         Fetch the status and results of the query job
         :param search_id: str
         :return: response object
         """
        poll_endpoint = f'{self.api_endpoint}/{search_id}'
        return await self.client.call_api(poll_endpoint, 'GET', headers=self.headers,
                                          timeout=self.timeout)

    async def delete_search(self, search_id):
        """
        Delete the corresponding search
        :param search_id: str
        :return: response object
        """
        poll_endpoint = f'{self.api_endpoint}/{search_id}'
        return await self.client.call_api(poll_endpoint, 'DELETE', headers=self.headers,
                                          timeout=self.timeout)

