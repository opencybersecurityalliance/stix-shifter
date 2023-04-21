import urllib
from urllib3.exceptions import InsecureRequestWarning
from urllib.parse import urlparse
import geoip2.webservice
import ast

class APIClient():

    def __init__(self, connection, configuration):
        headers = dict()
        auth = configuration.get('auth')
        self.auth = configuration.get('auth')
        self.client = geoip2.webservice.AsyncClient(auth.get('user_id'), auth.get('license_key'))
        self.namespace = connection.get('namespace')

    async def ping_source(self):
        ping_endpoint = '169.62.230.148'
        ping_return = await self.client.insights(ping_endpoint)
        await self.client.close()
        return ping_return.raw

    async def get_search_results(self, query_expression, range_start=None, range_end=None):
        # Queries the data source
        # extract the data
        self.data_type = query_expression['dataType']
        self.data = query_expression['data']
        if self.data_type == 'ip':
            try:
                response = await self.client.insights(self.data)
                str_resp = str(response)
                s = str_resp.split('{', 1)[1]
                s = '{'+s
                s = s.rsplit(',', 1)[0]
                rep = prepare_response(self, ast.literal_eval(s))
                return rep, self.namespace
            except Exception as e:
                return prepare_response(self, {'error': str(e)}), self.namespace
        else:
            return prepare_response(self, {'error': "IoC Type not supported"}), self.namespace

    async def delete_search(self, search_id):
        # Optional since this may not be supported by the data source API
        # Delete the search
        return {"code": 200, "success": True}

def prepare_response(self, response):
    response_data = dict()
    if response.get('error'):
        response_data['code'] = 400
        response_data['success'] = False
        response_data['message'] = response['error']
        return response_data
    response_data["code"] = 200
    response_data["data"] = {
        "success" : True,
        "full" : response   
    }

    return response_data