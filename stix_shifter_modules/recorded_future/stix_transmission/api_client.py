from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync
import json
from urllib.parse import quote_plus

class APIClient():

    def __init__(self, connection, configuration):
        # Uncomment when implementing data source API client.
        auth_values = configuration.get('auth')
        recordedfuture_key = auth_values['key']
        headers = dict()
        headers['Accept'] = 'application/json'
        headers['Content-Type'] = 'application/json'
        # remove protocol from hostname and retriving hostname from connection not giving statically 
        host = "api.recordedfuture.com"
        self.client = RestApiClientAsync(host, None, headers)

        self.connection = connection
        self.headers = headers
        self.recordedfuture_key = recordedfuture_key
        self.namespace = connection.get('namespace')

    async def ping_recorded_future(self):
        headers = self.headers
        headers["X-RFToken"] = self.recordedfuture_key
        ip_data = '9.9.9.9'
        query_endpoint = 'v2/ip/{}'.format(ip_data)  
        query_response = await self.client.call_api(query_endpoint, 'GET', headers = headers)
        return query_response.read().decode('utf-8'), query_response.code

    async def get_search_results(self, query_expression, range_start=None, range_end=None):
        # Queries the data source
        # extract the data
        data_type = query_expression['dataType']
        if data_type in ['domain', 'ip', 'hash', 'url']:       
            enrichment_info = await self.query_all(query_expression)
        return enrichment_info, self.namespace

    async def delete_search(self, search_id):
        # Delete the search - Optional since this may not be supported by the data source API
        return {"code": 200, "success": True}
    
    async def query_all(self, query_expression):
        data_type = query_expression['dataType']
        data = query_expression['data']
        headers = self.headers 
        headers["X-RFToken"] = self.recordedfuture_key

        if data_type == "url":
            data = quote_plus(data)

        query_endpoint = f'v2/{data_type}/{data}?fields=metrics,timestamps,risk,intelCard,relatedEntities,analystNotes&metadata=true'
        query_response = await self.client.call_api(query_endpoint, 'GET', headers = headers)
        api_query_data = json.loads(query_response.read().decode('utf-8')) if query_response.code == 200 else {}

        query_data = dict()
        query_data["code"] = 200
        query_data["data"] = dict()
        query_data["data"]["success"] = True
        if query_response.code == 200:
            query_data["data"]["isIOCFound"] = True
            query_data["data"]["full"] = api_query_data
        else:
            query_data["data"]["isIOCFound"] = False
            query_data["data"]["full"] = {
                "message": "IOC Not Found."
            }
        return query_data