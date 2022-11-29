import base64
from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync


class APIClient():

    def __init__(self, connection, configuration):
        self.endpoint_start = 'alertflex-ctrl/rest/stix-alerts'
        headers = dict()
        auth = configuration.get('auth')
        headers['Authorization'] = b"Basic " + base64.b64encode(
            (auth['username'] + ':' + auth['password']).encode('ascii'))
        url_modifier_function = None
        self.timeout = connection['options'].get('timeout')
        self.client = RestApiClientAsync(connection.get('host'),
                                    connection.get('port'),
                                    headers,
                                    url_modifier_function,
                                    cert_verify=connection.get('selfSignedCert', False))

    async def ping_data_source(self):
        endpoint = self.endpoint_start + '/status'
        return await self.client.call_api(endpoint, 'GET', timeout=self.timeout)

    async def get_search_results(self, query_expression, offset=None, length=None):
        endpoint = self.endpoint_start + '/search'
        data = {'query': query_expression}
        result = await self.client.call_api(endpoint, 'GET', urldata=data)
        return result

    async def delete_search(self, search_id):
        # Optional since this may not be supported by the data source API
        # Delete the search
        return {"code": 200, "success": True}
