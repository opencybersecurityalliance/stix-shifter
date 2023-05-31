import base64
from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync

ENDPOINT_ALL = 'v2/siem/all'

class APIClient():

    def __init__(self, connection, configuration):
        # Uncomment when implementing data source API client.
        auth = configuration.get('auth')
        self.timeout = connection['options'].get('timeout')
        headers = dict()
        if auth and 'principal' in auth and 'secret' in auth:
            token_decoded = auth['principal'] + ':' + auth['secret']
            token = base64.b64encode(token_decoded.encode('ascii'))
            headers['Authorization'] = "Basic %s" % token.decode('ascii')
        self.client = RestApiClientAsync(connection.get('host'),
                                    port=None,
                                    headers=headers, url_modifier_function=None, cert_verify=True, auth=None
                                    )

    async def ping_data_source(self):
        # Pings the data source
        endpoint = ENDPOINT_ALL + "?format=json&sinceSeconds=3600"
        pingresult = await self.client.call_api(endpoint=endpoint, method='GET', timeout=self.timeout)
        return pingresult

    async def create_search(self, query_expression):
        # Queries the data source
        return {"code": 200, "query_id": query_expression}

    async def get_search_status(self, search_id):
        # Check the current status of the search
        return {"code": 200, "status": "COMPLETED"}

    async def get_search_results(self, search_id):
        # Return the search results. Results must be in JSON format before being translated into STIX
        #resultdata = self.client.call_api(endpoint=ENDPOINT_ALL+search_id, method='GET')#working
        endpoint = ENDPOINT_ALL+"?format=json"
        resultdata = await self.client.call_api(endpoint=endpoint, method='GET', urldata=search_id, timeout=self.timeout)
        # Check the current status of the search
        return resultdata

    async def delete_search(self, search_id):
        # Optional since this may not be supported by the data source API
        # Delete the search
        return {"code": 200, "success": True}
