from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync
import json


class APIClient():

    def __init__(self, connection, configuration):  
        auth_values = configuration.get('auth')
        headers = dict()
        headers['Accept'] = 'application/json'
        headers['Content-Type'] = 'application/json'
        url_modifier_function = None
        self.api_key = auth_values['api_key']
        
        # giving hostname statically 
        host = auth_values['tg_host'] 
        if host.startswith('https://'): 
            host = host.replace('https://', '') 
        self.client = RestApiClientAsync(host=host, port=None, headers=headers, url_modifier_function=url_modifier_function)
        self.connection = connection
        self.namespace = connection.get('namespace')
        self.headers = headers
        self.tg_host = host

    async def ping_threat_grid(self):
        # Pings the data source
        endpoint = 'api/v3/session/whoami?api_key=' + self.api_key
        ping_return = await self.client.call_api(endpoint, 'GET')
        data = json.loads(ping_return.read().decode('utf-8'))
        return data, ping_return.code

    async def get_search_results(self, query_expression):
        # Queries the data source
        # extract the data
        self.data_type = query_expression['dataType']
        self.data = query_expression['data']
        if self.data_type == "hash":
            hash_query_string = '?limit=1&sort_by=timestamp&sort_order=desc&threatscores=critical&q='+self.data+'&api_key='+self.api_key
            hash_endpoint = 'api/v2/search/submissions'+hash_query_string
            return await self.query_result(hash_endpoint)

        elif self.data_type == "domain":
            domain_query_string = '?limit=1&sort_by=timestamp&sort_order=desc&threatscores=critical&q='+self.data+'&api_key='+self.api_key+'&term=domain'
            domain_endpoint = 'api/v2/search/submissions'+domain_query_string
            return await self.query_result(domain_endpoint)

        elif self.data_type == "ip":
            ip_query_string = '?limit=1&sort_by=timestamp&sort_order=desc&threatscores=critical&q='+self.data+'&api_key='+self.api_key
            ip_endpoint = 'api/v2/search/submissions'+ip_query_string
            return await self.query_result(ip_endpoint)
        else:
            return {"code": 401, "error": "IoC Type not supported"}, self.namespace

    async def query_result(self, url):
        query_response = await self.client.call_api(url, 'GET')
        api_query_data = json.loads(query_response.read().decode('utf-8'))  
        # Verify response and store Sample ID
        if query_response.code==200:
            try:
                sample_id = api_query_data["data"]["items"][0]["item"]["sample"] 
                submission_data = api_query_data["data"]["items"][0]
                submission_data['total'] = api_query_data.get('data', {}).get('total')
                #implement this and use it to call get_sample_results
                response = await self.get_sample_results(sample_id, submission_data)
                return response, self.namespace
            except:
                response = prepare_response(self, {"message" : "No sample"})
                return response, self.namespace
        else:
            return {"code": query_response.code, "error": api_query_data['error']['message']}, self.namespace   

    async def get_sample_results(self, sample_id, submission_data = None):
        # Get Analysis JSON from Threat Grid
        analysis_url =  "api/v2/samples/{}/analysis.json".format(sample_id)+'?api_key='+self.api_key
        analysis_response = await self.client.call_api(analysis_url, 'GET')
        analysis_response = json.loads(analysis_response.read().decode('utf-8')) if analysis_response.code == 200 else {}

        # Get Sample Summary JSON from Threat Grid
        summary_url =  "api/v2/samples/{}/summary".format(sample_id)+'?api_key='+self.api_key
        summary_response = await self.client.call_api(summary_url, 'GET')
        summary_response = json.loads(summary_response.read().decode('utf-8')) if summary_response.code == 200 else {}

        # Build report from summary and analysis results
        # remove the iocs , network and domains  attributes from analysis_response to reduce the size
        analysis_response.pop('iocs')
        analysis_response.pop('network')
        analysis_response.pop('domains')
        analysis_response.pop('dynamic')
        analysis_response.pop('artifacts')
        return self.build_report(analysis_response, summary_response, submission_data, sample_id)

    def build_report(self, analysis_response, summary_response, submission_data = None, sample_id = None):
        # create this function, make final report
        raw_report = {"host": self.tg_host, "analysis_report": analysis_response, "submission_data": submission_data, "sample_id": sample_id}
        resp = prepare_response(self, raw_report)
        return resp

    async def delete_search(self, search_id):
        # Optional since this may not be supported by the data source API
        # Delete the search
        if(search_id):
            return {"code": 200, "success": True}
        else:
            return {"code": 200, "success": False}      


def prepare_response(self, raw_report):
    response_data = dict()
    response_data["code"] = 200
    response_data["data"] = {
        "success" : True,
        "full" : raw_report   
    }
    return response_data  
