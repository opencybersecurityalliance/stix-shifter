from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync
import json
import time

class APIClient():

    def __init__(self, connection, configuration):
        auth_values = configuration.get('auth')
        intezer_auth_key = auth_values['key']
        headers = dict()
        headers['Accept'] = 'application/json'
        headers['Content-Type'] = 'application/json'
        url_modifier_function = None
        # giving hostname statically 
        host = "analyze.intezer.com"
        self.client = RestApiClientAsync(host=host, port=None, headers=headers, url_modifier_function=url_modifier_function)
        self.connection = connection
        self.namespace = connection.get('namespace')
        self.intezer_auth_key = intezer_auth_key
        self.intezer_token = None

    async def ping_intezer(self):
        # Pings the data source
        ping_endpoint = 'api/v2-0/is-available'
        ping_return = await self.client.call_api(ping_endpoint, 'GET')
        return ping_return

    async def get_search_results(self, query_expression, range_start=None, range_end=None):
        # Queries the data source
        # extract the data
        token = await request_token (self)
        if token["code"] == 200:
            data_type = query_expression['dataType']
            data = query_expression['data']
            if data_type == 'hash':
                enrichment_info = await query_hash(self, data)
            if data_type == 'url' or  data_type == 'domain':
                enrichment_info = await query_url(self, data)
            return enrichment_info, self.namespace
        else:
            enrichment_info = {"code": token["code"], "error": token["error"]}
            return enrichment_info, self.namespace


    async def delete_search(self, search_id):
        # Optional since this may not be supported by the data source API
        # Delete the search
        return {"code": 200, "success": True}        

async def request_token(self):
    token_endpoint = 'api/v2-0/get-access-token'
    body = json.dumps({
        "api_key": self.intezer_auth_key
    })

    response = await self.client.call_api(token_endpoint, 'POST', data = body)
    response_data = json.loads(response.read().decode('utf-8'))
    if response.code == 200:
        response_data["code"] = response.code
        self.intezer_token = response_data["result"]
    else:
        response_data["code"] = response.code  

    return response_data

async def query_hash(self, data):
    
    intezer_headers = { 'Authorization': f'Bearer {self.intezer_token}', 'Content-Type': 'application/json', 'Accept': 'application/json'}
    # previously scanned hash hence Analysis is available in Intezer Database - API call and endpoints(it will reduce credit usage and response time)
    previously_scanned_hash_endpoint = 'api/v2-0/files/'+data
    previously_scanned_response = await self.client.call_api(previously_scanned_hash_endpoint, 'GET', headers = intezer_headers)
    previously_scanned_data =  json.loads(previously_scanned_response.read().decode('utf-8'))
    query_data = dict()
    if ('result_url' in previously_scanned_data) and previously_scanned_response.code==200:
        analyses_url =  'api/v2-0'+ previously_scanned_data["result_url"]
        query_data["data"] = previously_scanned_data['result']
        query_data["code"] = previously_scanned_response.code

    elif previously_scanned_response.code==404 or previously_scanned_response.code==410:
        query_endpoint = 'api/v2-0/analyze-by-hash'
        data = json.dumps({'hash': data})
        query_response = await self.client.call_api(query_endpoint, 'POST', headers = intezer_headers, data = data )
        query_data =  json.loads(query_response.read().decode('utf-8'))
        analyses_url = '/'
        if 'result_url' in query_data and query_response.code == 201:
            analyses_url =  'api/v2-0'+ query_data["result_url"]
            #Below while loop logic: If we get API call status 202=Queued/Inprocess then we need to call API till we get status 200
            query_data = await get_analyses(self, intezer_headers, analyses_url)
            while (query_data["code"]!=200 and query_data["code"]==202):
                time.sleep(1)
                query_data = await get_analyses(self, intezer_headers, analyses_url)
        elif(query_data["error"]=='File not found') and query_response.code==404:
            query_data['data'] = dict()
            query_data['data']['errortext'] = 'File has not previously been analyzed by Intezer!'
            query_data['data']['iocs'] = {}
            query_data['data']['dynamic_ttps'] = {}
            query_data['data']['code_reuse'] = {}
            query_data["code"] = 200
        else:
            query_data["code"] = query_response.code
    else:
        query_data["code"] = previously_scanned_response.code
    #call for other APIs       
    if(query_data["code"]==200 and 'error' not in query_data):    
        query_data["data"]["iocs"] = await get_hash_iocs(self, intezer_headers, analyses_url)
        query_data["data"]["dynamic_ttps"] = await get_hash_dynamic_ttps(self, intezer_headers, analyses_url)
        query_data["data"]["code_reuse"] = await get_hash_code_reuse(self, intezer_headers, analyses_url)         
    return query_data

async def get_analyses(self, intezer_headers, analyses_url):

    analyses_response = await self.client.call_api(analyses_url, 'GET', headers = intezer_headers, data = None, urldata = None)
    analyses_data = json.loads(analyses_response.read().decode('utf-8'))
    result_data = dict()
    if 'result' in analyses_data:
        result_data['data'] = analyses_data["result"]
    elif 'description' in analyses_data:
        result_data['error'] = analyses_data["description"] 
    elif 'error' in analyses_data:
        result_data['error'] = analyses_data["error"] 
    if 'result_url' in analyses_data:
        result_data['result_url'] = analyses_data["result_url"]
    result_data['code'] =  analyses_response.code           
    return result_data

async def query_url(self, data):

    intezer_headers = { 'Authorization': f'Bearer {self.intezer_token}', 'Content-Type': 'application/json', 'Accept': 'application/json'}
    # previously scanned hash hence Analysis is available in Intezer Database - API call and endpoints(it will reduce credit usage and response time)
    query_endpoint = 'api/v2-0/url/'
    data = json.dumps({'url': data})

    query_response = await self.client.call_api(query_endpoint, 'POST', headers = intezer_headers, data = data )
    query_data =  json.loads(query_response.read().decode('utf-8'))
    if query_response.code==201 and query_data["result_url"]:
        analyses_url =  'api/v2-0'+ query_data["result_url"]
        #Below while loop logic: If we get API call status 202=Queued/Inprocess then we need to call API till we get status 200
        query_data = await get_analyses(self, intezer_headers, analyses_url)
        while (query_data["code"]!=200 and query_data["code"]==202):
            time.sleep(1)
            query_data = await get_analyses(self, intezer_headers, analyses_url)
    else:
        query_data["code"] = query_response.code

    #call for other APIs       
    if(query_data["code"]==200): 
        query_data["data"]["verdict"] = query_data["data"]["summary"]["verdict_type"]
        query_data["data"]["threat_score"] = query_data["data"]["api_void_risk_score"]
        query_data["data"]["iocs"] = await get_hash_iocs(self, intezer_headers, analyses_url)
        query_data["data"]["dynamic_ttps"] = await get_hash_dynamic_ttps(self, intezer_headers, analyses_url)
        query_data["data"]["code_reuse"] = await get_hash_code_reuse(self, intezer_headers, analyses_url)      

    elif(query_data.get('result', {}).get('is_url_offline')) and query_data["code"]==400:
        query_data['data'] = dict()
        query_data['data']['error'] = query_data.get('error')
        query_data['data']['iocs'] = {}
        query_data['data']['dynamic_ttps'] = {}
        query_data['data']['code_reuse'] = {}
        query_data['data']['result'] = query_data.get('result')
        query_data["code"] = 200
    return query_data

async def get_hash_iocs(self, intezer_headers, analyses_url):

    iocs_url = analyses_url+'/iocs'
    iocs_response = await self.client.call_api(iocs_url, 'GET', headers = intezer_headers, data = None, urldata = None)
    iocs_data = json.loads(iocs_response.read().decode('utf-8')) if iocs_response.code == 200 else {}
    if 'result' in iocs_data:
        iocs_data = iocs_data["result"]
    return iocs_data


async def get_hash_dynamic_ttps(self, intezer_headers, analyses_url):

    dynamic_ttps_url = analyses_url+'/dynamic-ttps'
    dynamic_ttps_response = await self.client.call_api(dynamic_ttps_url, 'GET', headers = intezer_headers)
    dynamic_ttps_data = json.loads(dynamic_ttps_response.read().decode('utf-8')) if dynamic_ttps_response.code == 200  else {}
    if 'result' in dynamic_ttps_data:
        dynamic_ttps_data = dynamic_ttps_data["result"]
    return dynamic_ttps_data       

async def get_hash_code_reuse(self, intezer_headers, analyses_url):
    sub_analyses_url = analyses_url+'/sub-analyses'
    sub_analyses_response = await self.client.call_api(sub_analyses_url, 'GET', headers = intezer_headers)
    sub_analyses_data = json.loads(sub_analyses_response.read().decode('utf-8')) if sub_analyses_response.code == 200  else {}
    if 'sub_analyses' in sub_analyses_data:
        code_reuse_url = analyses_url+'/sub-analyses/'+sub_analyses_data['sub_analyses'][0]['sub_analysis_id']+'/code-reuse'
        code_reuse_response = await self.client.call_api(code_reuse_url, 'GET', headers = intezer_headers)
        code_reuse_data = json.loads(code_reuse_response.read().decode('utf-8')) if code_reuse_response.code == 200  else {}
    else:
        code_reuse_data = {}    
    return code_reuse_data
