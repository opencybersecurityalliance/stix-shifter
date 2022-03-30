from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient
import json
import hashlib
class APIClient():

    def __init__(self, connection, configuration):
        # Uncomment when implementing data source API client.
        auth_values = configuration.get('auth')
        auth = (auth_values['username'], auth_values['password'])
        headers = dict()
        headers['Accept'] = 'application/json'

        connection['host'] = 'data.reversinglabs.com'
        url_modifier_function = None
        self.client = RestApiClient(host=connection.get('host'),
                                    port=None,
                                    headers=headers,
                                    url_modifier_function=url_modifier_function,
                                    auth=auth
                                    )
        self.connection = connection
        self.namespace = connection.get('namespace')


    def ping_reversinglabs(self):

        endpoint = 'api/uri/statistics/uri_state/sha1/4b84b15bff6ee5796152495a230e45e3d7e947d9?format=json'
        response = self.client.call_api(endpoint, 'GET')
        json_data = json.loads(response.read().decode('utf-8'))

        if response.code == 200:
            status_code = 200

        return json_data, status_code

    def get_search_results(self, query_expression, range_start=None, range_end=None):
        # Return the search results. Results must be in JSON format before being translated into STIX
        # query_expression = (json.loads(query_expression))
        data_type = query_expression['dataType']
        data = query_expression['data']
        uri = get_uri_sha1(data)

        if data_type == 'ip' or data_type == 'domain':
            endpoint_uri_state = f'api/uri/statistics/uri_state/sha1/{uri}?format=json'
            uri_state = self.client.call_api(endpoint_uri_state, 'GET')
            json_data_uri_state = json.loads(uri_state.read().decode('utf-8')) if uri_state.code == 200 else {}

            if uri_state.code == 200:
                json_data_uri_state['namespace'] = self.namespace
                return json_data_uri_state, uri_state.code
            else:
                json_data_uri_state['error'] = uri_state.read().decode('utf-8')
                json_data_uri_state['code'] = uri_state.code
                json_data_uri_state['indicator_types'] = [ "unknown" ]
                json_data_uri_state['description'] =  uri_state.read().decode('utf-8')
                json_data_uri_state['namespace'] = self.namespace
                return json_data_uri_state, uri_state.code

        elif data_type == 'url':

            post_body = json.dumps({
                "rl": {
                    "query": {
                        "url": data,
                        "response_format": "json"
                    }

                }
            })

            endpoint_url = 'api/networking/url/v1/report/query/json'
            url_response = self.client.call_api(endpoint_url, 'POST', data = post_body)
            json_data_url = json.loads(url_response.read().decode('utf-8')) if url_response.code == 200 else {}

            if url_response.code == 200:
                status_code = 200
                json_data_url['namespace'] = self.namespace
                return json_data_url, status_code

            else:
                json_data_url['error'] = url_response.read().decode('utf-8')
                json_data_url['code'] = url_response.code
                json_data_url['indicator_types'] = ["unknown"]
                json_data_url['description'] = url_response.read().decode('utf-8')
                json_data_url['namespace'] = self.namespace
                return json_data_url, url_response.code


        elif data_type == 'hash':
            HASH_LENGTH = {'40': 'sha1', '64': 'sha256', '32': 'md5'}
            hash_type = HASH_LENGTH.get(str(len(data)), '')

            endpoint_malware_presence = f'api/databrowser/malware_presence/query/{hash_type}/{data}?format=json&extended=true'
            malware_presence = self.client.call_api(endpoint_malware_presence, 'GET')
            json_data_malware_presence = json.loads(malware_presence.read().decode('utf-8')) if malware_presence.code == 200 else {}

            if malware_presence.code == 200:
                status_code = 200
                json_data_malware_presence['namespace'] = self.namespace
                return json_data_malware_presence, status_code
            else:
                json_data_malware_presence['error'] = malware_presence.read().decode('utf-8')
                json_data_malware_presence['code'] = malware_presence.code
                json_data_malware_presence['indicator_types'] = ["unknown"]
                json_data_malware_presence['description'] = malware_presence.read().decode('utf-8')
                json_data_malware_presence['namespace'] = self.namespace
                return json_data_malware_presence, malware_presence.code

        else:
            return {"code": 401, "error": "IoC Type not supported"}

        # return response

    def delete_search(self, search_id):
        # Optional since this may not be supported by the data source API
        # Delete the search
        return {"code": 200, "success": True}

def get_uri_sha1(uri):
    uri_bytes = bytes(uri, "utf-8")
    hash_object = hashlib.sha1(uri_bytes)
    uri_hash = hash_object.hexdigest()
    return uri_hash