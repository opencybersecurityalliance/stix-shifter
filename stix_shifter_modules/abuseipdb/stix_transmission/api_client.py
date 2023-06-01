from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync
import json


class APIClient():

    def __init__(self, connection, configuration):
        headers = dict()
        auth = configuration.get('auth')
        headers['Key'] = auth.get('key')
        headers['Accept'] = "application/json"
        host = "api.abuseipdb.com"
        self.namespace = connection.get('namespace')
        self.client = RestApiClientAsync(host=host, port=None, headers=headers)

    async def ping_abuseipdb(self):
        # Pings the data source
        response = await query_ip(self, "118.25.6.39")
        return response

    async def get_search_results(self, query_expression):
        # Queries the data source
        # extract the data
        self.data_type = query_expression['dataType']
        self.data = query_expression['data']
        if self.data_type == 'ip':
            rep = await query_ip(self, self.data)
            return rep, self.namespace
        else:
            return {"code": 401, "error": "IoC Type not supported"}, self.namespace
        
    async def delete_search(self, search_id):
        # Optional since this may not be supported by the data source API
        # Delete the search
        return {"code": 200, "success": True}

async def query_ip(self, data):
    
    response_data = dict()
    endpoint_uri = f'api/v2/check?ipAddress={data}'
    try:
        response = await self.client.call_api(endpoint_uri, 'GET')
        json_data = json.loads(response.read().decode('utf-8'))

        if response and response.code == 200 and 'data' in json_data:
            response_data["code"] = response.code
            response_data["data"] = [json_data['data']]
            return response_data
        elif 'errors' in json_data:
            if len(json_data['errors']) > 0:
                error_data = json_data['errors'][0]
                response_data['error'] = error_data['detail']
                response_data['code'] = error_data['status']
            else:
                response_data['error'] = 'API Access error'
                response_data['code'] = response.code
                return response_data
        else:
            response_data['error'] = 'API Access error'
            response_data['code'] = response.code
            return response_data
    except Exception as e:
        response_data["code"] = 500
        response_data["error"] = "OS error: {0}".format(e)

    return response_data
