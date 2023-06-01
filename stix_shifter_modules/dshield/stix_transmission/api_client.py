
from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync
import json
from stix_shifter_utils.utils import logger

class APIClient():

    def __init__(self, connection, configuration):
        headers = dict()
        headers['Accept'] = 'application/xml'
        headers['Content-Type'] = 'application/xml'
        url_modifier_function = None
        # giving hostname statically 
        host = "isc.sans.edu/"
        self.client = RestApiClientAsync(host=host,
                                    port=None,
                                    headers=headers,
                                    url_modifier_function=url_modifier_function,
                                    )
        self.connection = connection
        self.namespace = connection.get('namespace')
        self.logger = logger.set_logger(__name__)

    async def ping_dshield(self):
        # Pings the data source
        ip = '91.109.5.28'
        ping_endpoint = 'api/ip/%s?json'%ip
        ping_response = await self.client.call_api(ping_endpoint, 'GET')
        return json.loads(ping_response.read().decode('utf-8')), ping_response.code

    async def delete_search(self, search_id):
        # Delete the search - Optional since this may not be supported by the data source API
        return {"code": 200, "success": True} 


    async def get_search_results(self, query_expression):
        # Queries the data source
        # extract the data
        self.data_type = query_expression['dataType']
        data = query_expression['data']
        enrichment_info = dict()
        if self.data_type == 'ip':
            query_endpoint = 'api/ip/%s?json'%data
            query_response = await self.client.call_api(query_endpoint, 'GET', headers = '')
            query_response =  json.loads(query_response.read().decode('utf-8'))if query_response.code == 200 else {}
            # Do we get valid results
            if self.data_type in query_response.keys():
                info = query_response[self.data_type]
                results = {'ioc_report' : info}
                if (info.get('maxrisk')):
                    results.update( {'maxrisk' : info['maxrisk']} )
                if (info.get('threatfeeds')):
                    results.update( {'threatfeedscount' : len(info['threatfeeds'])} )
                enrichment_info = prepare_response(self, results)
            else:
                enrichment_info["error"] = query_response
                enrichment_info["code"] = 400
            return enrichment_info, self.namespace
    

def prepare_response(self, response):
    response_data = dict()
    response_data["code"] = 200
    response_data["data"] = {
        "success" : True,
        "full" : response   
    }
    return response_data