import json

from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync

DEFAULT_FIELDS = [
    "*",
    "process_cmdline",
    "process_start_time",
    "device_internal_ip",
    "device_external_ip",
    "parent_hash",
    "parent_name",
    "device_os"
]


class APIClient():
    def __init__(self, connection, configuration):
        auth = configuration.get('auth')
        headers = dict()
        headers['X-Auth-Token'] = auth.get('token')
        headers['Accept'] = 'application/json'
        headers['Content-Type'] = 'application/json'
        self.org_key = auth.get('org_key')
        self.client = RestApiClientAsync(
            connection.get('host'),
            connection.get('port'),
            headers,
            cert_verify=connection.get('selfSignedCert', True),
            sni=connection.get('sni', None)
        )
        self.timeout = connection['options'].get('timeout')
        self.result_limit = connection['options'].get('result_limit')

    async def ping_data_source(self):
        """Verifies the data source API is working by sending a GET request to
        https://<server_ip>/api/investigate/v1/orgs/{org_key}/processes/limits

        Status codes:
        200: successfully fetched the upper and lower time limits (i.e API works)
        400: malformed JSON body or invalid value
        403: forbidden
        500: internal server error
        """
        endpoint = f'api/investigate/v1/orgs/{self.org_key}/processes/limits'
        return await self.client.call_api(endpoint, 'GET', timeout=self.timeout)

    async def create_search(self, query_expression):
        """Queries the data source by sending a POST request to
        https://<server_ip>/api/investigate/v2/orgs/{org_key}/processes/search_jobs

        200: successfully submitted search for processes
        400: malformed JSON body or invalid value
        403: forbidden
        500: internal server error
        """
        endpoint = f'api/investigate/v2/orgs/{self.org_key}/processes/search_jobs'
        data = {
            'query': query_expression,
            'fields': DEFAULT_FIELDS,
            'start': 0,
            'rows': self.result_limit,
            'sort': [{
                'field': 'device_timestamp',
                'order': 'asc'
            }]
        }
        return await self.client.call_api(endpoint, 'POST', data=json.dumps(data), timeout=self.timeout)

    async def get_search_status(self, job_id):
        """ Check the status of the search by sending a GET request to
        https://<server_ip>/api/investigate/v1/orgs/{org_key}/processes/search_jobs/{job_id}

        200: successfully retrieved status of process search
        400: malformed JSON body or invalid value
        403: forbidden
        500: internal server error
        """
        endpoint = f'api/investigate/v1/orgs/{self.org_key}/processes/search_jobs/{job_id}'
        return await self.client.call_api(endpoint, 'GET', timeout=self.timeout)

    async def get_search_results(self, job_id, start=0, rows=100):
        """Return the JSON-formatted search results by sending a GET request to
        https://<server_ip>/api/investigate/v2/orgs/{org_key}/processes/search_jobs/{job_id}/results

        200: successfully fetched processes
        400: malformed JSON body or invalid value
        403: forbidden
        500: internal server error
        """
        urldata = [("start", start), ("rows", rows)]
        endpoint = f'api/investigate/v2/orgs/{self.org_key}/processes/search_jobs/{job_id}/results'
        return await self.client.call_api(endpoint, 'GET', urldata=urldata, timeout=self.timeout)

    async def delete_search(self, job_id):
        """Delete the search by sending a DELETE request to
        https://<server_ip>/api/investigate/v1/orgs/{orgkey}/processes/search_jobs/{job_id}

        204: success deleted a process search
        400: malformed JSON body or invalid value
        403: forbidden
        500: internal server error
        """
        endpoint = f'api/investigate/v1/orgs/{self.org_key}/processes/search_jobs/{job_id}'
        return await self.client.call_api(endpoint, 'DELETE', timeout=self.timeout)
