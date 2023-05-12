from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync
import json, itertools, re
from datetime import datetime

class APIClient():

    def __init__(self, connection, configuration):
        auth_values = configuration.get('auth')
        auth = (auth_values['username'], auth_values['password'])
        headers = dict()
        headers['Accept'] = 'application/json'
        url_modifier_function = None
        # remove protocol from hostname
        host = auth_values['hostname']
        if host.startswith('https://'):
            host = host.replace('https://', '')
        self.client = RestApiClientAsync(host=host, port=None, headers=headers,
                                    url_modifier_function=url_modifier_function)
        self.connection = connection
        self.threatQ_auth = auth
        self.namespace = connection.get('namespace')
        self.client_id = None


    async def generate_client_id(self):
        init_endpoint = 'assets/js/config.js'
        init_response = await self.client.call_api(init_endpoint, 'GET')
        init_response_data = init_response.read().decode('utf-8')
        client_index = init_response_data.find('ClientId')
        self.client_id = init_response_data[client_index+12:len(init_response_data)-38]

    async def ping_threatQ(self):
        # Pings the data source
        ping_return = await request_token(self)
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
            else:
                enrichment_info = await query(self, data, data_type)
            return enrichment_info, self.namespace
        else:
            return {"code": token["code"], "error": "API access error"}


    async def delete_search(self, search_id):
        # Optional since this may not be supported by the data source API
        # Delete the search
        return {"code": 200, "success": True}

async def request_token(self):
    token_endpoint = '/api/token'
    params = dict()
    params['grant_type'] = 'password'
    if self.client_id is None:
        await self.generate_client_id()
    params['client_id'] = self.client_id
    body = {
        'email': self.threatQ_auth[0],
        'password': self.threatQ_auth[1],
        'grant_type': 'password',
        'client_id': self.client_id
    }

    response = await self.client.call_api(token_endpoint, 'POST', data = body, urldata = params)
    response_data = json.loads(response.read().decode('utf-8')) if response.code == 200 else {}
    if response.code == 200:
        response_data["code"] = response.code
        self.threatQ_token = response_data["access_token"]
    else:
        response_data["code"] = response.code
        response_data["error"] = 'API Access error'
    return response_data

async def query(self, data, data_type):
    # Queries the data source
    query_endpoint = '/api/indicators/query'
    params = dict() 
    params['limit'] = 500
    params['offset'] = 0

    if data_type == 'ip':
        threatQ_type = "IP Address"
    elif data_type == 'url':
        threatQ_type = "URL"
        uri_type = re.compile(r"https?://")
        data = uri_type.sub('', data).strip().strip('/')
    elif data_type == 'domain':
        threatQ_type = "FQDN"
        uri_type = re.compile(r"https?://")
        data = uri_type.sub('', data).strip().strip('/')
    else:
        return {"code": 401, "error": "IoC Type not supported"}

    
    threatQ_headers = { 'Authorization': f'Bearer {self.threatQ_token}', 'Content-Type': 'application/json'  }

    data = json.dumps({
        'criteria': {
            '+or': [
                {
                    'value': data
                }
            ],
            '+and': [
                {
                    'type': threatQ_type
                }
            ]
        }
    })

    query_response = await self.client.call_api(query_endpoint, 'POST', headers = threatQ_headers, data = data, urldata = params)
    query_data = json.loads(query_response.read().decode('utf-8')) if query_response.code == 200 else {}
    if query_data:
        query_data["code"] = 200
        if (len(query_data["data"])> 0):
            query_data["data"][0]["enrich_info"] = await get_enrichment(self, threatQ_headers, query_data)
            query_data["data"][0]["relationships"] = await get_relationships(self, threatQ_headers, query_data)
    else:
        query_data["code"] = query_response.code
        query_data["error"] = 'API Access error'
    return query_data

async def query_hash(self, data):
    query_endpoint = '/api/indicators/query'
    params = dict() 
    params['limit'] = 500
    params['offset'] = 0

    if (len(data) == 32):
        threatQ_hash_type = "MD5"
    elif (len(data) == 40):
        threatQ_hash_type = "SHA-1"
    elif (len(data) == 64):
        threatQ_hash_type = "SHA-256"
    else:
        return {"code": 401, "error": "Hash type not supported"}
    
    threatQ_headers = { 'Authorization': f'Bearer {self.threatQ_token}', 'Content-Type': 'application/json'  }

    data = json.dumps({
        'criteria': {
            '+or': [
                {
                    'value': data
                }
            ],
            '+and': [
                {
                    'type': threatQ_hash_type
                }
            ]
        }
    })

    query_response = await self.client.call_api(query_endpoint, 'POST', headers = threatQ_headers, data = data, urldata = params)
    query_data = json.loads(query_response.read().decode('utf-8')) if query_response.code == 200 else {}

    if query_data:
        query_data["code"] = 200
        if (len(query_data["data"])> 0):
            query_data["data"][0]["enrich_info"] = await get_enrichment(self, threatQ_headers, query_data)
            query_data["data"][0]["relationships"] = await get_relationships(self, threatQ_headers, query_data)
    else:
        query_data["code"] = query_response.code
        query_data["error"] = 'API Access error'
    return query_data

async def get_enrichment(self, threatQ_headers, query_data):
    indicator_id = query_data["data"][0]["id"]
    enrich_endpoint = '/api/indicators'
    enrich_params = dict()
    more_info = dict()
    enrich_params['with'] = 'adversaries,attachments.sources,attributes.sources, \
                            comments.sources,events.type,signatures.type,score,sources,status,tags,\
                            type.plugins.config,watchlist,tasks,indicators,malware,attack_pattern'
    enrich_response = await self.client.call_api('%s/%s/details' %(enrich_endpoint, indicator_id), 'GET', headers = threatQ_headers, urldata = enrich_params)
    enrich_data = json.loads(enrich_response.read().decode('utf-8')) if enrich_response.code == 200 else {}
    required_data = enrich_data["data"]

    if "attributes" in required_data:
        more_info["attributes"] = list(itertools.islice(required_data["attributes"], 8)) # get at most 8 attribute entries
    
    more_info["Comments"] = "Additional attribute information is available on the ThreatQ platform."

    return more_info

async def get_relationships(self, threatQ_headers, query_data):
    relationship_array = ['malware', 'attack_pattern', 'campaign', 'ttp', 'tool']
    indicator_id = query_data["data"][0]["id"]
    relationship_endpoint = '/api/indicators'
    relationships = dict()
    for rel in relationship_array:
        rel_response = await self.client.call_api('%s/%s/%s' %(relationship_endpoint, indicator_id, rel), \
            'GET', headers = threatQ_headers)
        rel_data = json.loads(rel_response.read().decode('utf-8')) if rel_response.code == 200 else {}
        rel_op = rel_data["data"]
        relationships[rel] = rel_op
    
    return relationships
