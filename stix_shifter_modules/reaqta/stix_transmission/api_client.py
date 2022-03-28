from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient
import requests
import json

class APIClient():
    AUTH_ENDPOINT = "rqt-api/1/authenticate"
    EVENT_ENDPOINT = "rqt-api/1/events/hunt"

    def __init__(self, connection, configuration):
        self.headers = dict()
        self.headers['Accept'] = 'application/json'
        url_modifier_function = None
        auth = configuration.get('auth')
        self.host = connection.get('host')
        self.client = RestApiClient(connection.get('host'),
                                    None,
                                    self.headers,
                                    url_modifier_function=url_modifier_function,
                                    cert_verify=connection.get('selfSignedCert', True),
                                    sni=connection.get('sni', None)
                                    )
        self.timeout = connection['options'].get('timeout')
        self.app_id = auth['app_id']
        self.secret_key = auth['secret_key']

    def ping_data_source(self):
        # Pings the data source
        # return requests.post(auth_host, data=auth_data)
        # return self.client.call_api(self.AUTH_ENDPOINT, 'POST', data=auth_data)
        return self.get_token()

    def get_search_results(self, search_id, range_start=None, range_end=None):
        # Return the search results. Results must be in JSON format before being translated into STIX

        params = dict()
        token_response = self.get_token()
        response_code = token_response['code']
        if response_code == 200:
            self.headers['Authorization'] = 'Bearer {}'.format(token_response['token'])
        
        # LOOKS LIKE MAX COUNT is 500. response doesn't show why it fails
        params['count'] = int(range_end) - int(range_start)
        
        #$ip="192.168.122.83" OR $ip="192.168.122.84" AND happenedAfter="yyyy-MM-ddTHH:mm:ss.SSSZ" AND happenedBefore="yyyy-MM-ddTHH:mm:ss.SSSZ"
        # search_id = '$ip="172.16.60.184" and hasAlert=t'
        body_data = {'query': search_id}
        
        return self.client.call_api(self.EVENT_ENDPOINT, 'POST', urldata=params, headers=self.headers, data=body_data)
        events=json.loads(response.response.text)
        
        print(json.dumps(events, indent=4))

        # return {"code": 200, "data": "Results from search"}
    
    def get_token(self):
        auth_data = dict()
        response_dict= dict()
        auth_data['id'] = self.app_id
        auth_data['secret'] = self.secret_key
        # auth_data = {'id' : self.app_id, 'secret' : self.secret_key}
        try:
            response = self.client.call_api(self.AUTH_ENDPOINT, 'POST', headers=self.headers, data=auth_data)
            
            response_dict['code'] = response.code
            response_text = json.loads(response.response.text)
            if response.code == 200:
                response_dict['token'] = response_text['token']
            else:
                response_dict['message'] = response_text
        except Exception as ex:
            if ex.__class__.__name__ is 'ConnectionError':
                raise ConnectionError(ex)
            else:
                response_dict['type'] = ex.__class__.__name__
                response_dict['message'] = ex

        return response_dict