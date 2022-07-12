from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient
import requests
from datetime import datetime, timedelta
import json

class APIClient():
    AUTH_ENDPOINT = "rqt-api/1/authenticate"
    EVENT_ENDPOINT = "rqt-api/1/events/hunt"

    def __init__(self, connection, configuration):
        self.headers = dict()
        self.headers['Accept'] = 'application/json'
        url_modifier_function = None
        auth = configuration.get('auth')

        self.client = RestApiClient(connection.get('host'),
                                    connection.get('port'),
                                    self.headers,
                                    url_modifier_function=url_modifier_function,
                                    cert_verify=connection.get('selfSignedCert', True),
                                    sni=connection.get('sni', None)
                                    )
        self.timeout = connection['options'].get('timeout')
        self.app_id = auth['app_id']
        self.secret_key = auth['secret_key']
        self.token = None
        self.token_expiresat = None

    def ping_data_source(self):
        # Pings the data source
        return self.get_token()

    def get_search_results(self, search_id, length):
        # Return the search results. Results must be in JSON format before being translated into STIX
        params = dict()
        params['count'] = length
        token_response = self.get_token()
        response_code = token_response['code']
        if response_code == 200:
            self.headers['Authorization'] = 'Bearer {}'.format(token_response['token'])
        else:
            raise Exception(token_response)

        body_data = {'query': search_id}
        
        return self.client.call_api(self.EVENT_ENDPOINT, 'POST', urldata=params, headers=self.headers, data=body_data)
    
    def page_search(self, search_id, next_page_url, length):
        params = dict()
        params['count'] = length
        if not self.token_expired():
            token_response = self.get_token()
            response_code = token_response['code']
            if response_code == 200:
                self.headers['Authorization'] = 'Bearer {}'.format(token_response['token'])
        
        body_data = {'query': search_id}
        page = next_page_url.split('?', maxsplit=1)[1]
        next_page_endpoint = self.EVENT_ENDPOINT + '?' + page
        
        return self.client.call_api(next_page_endpoint, 'POST', headers=self.headers, data=body_data)

    def get_token(self):
        auth_data = dict()
        response_dict= dict()
        auth_data['id'] = self.app_id
        auth_data['secret'] = self.secret_key

        try:
            response = self.client.call_api(self.AUTH_ENDPOINT, 'POST', headers=self.headers, data=auth_data)
            
            response_dict['code'] = response.code
            response_text = json.loads(response.read())
            if response.code == 200:
                response_dict['token'] = response_text['token']
                self.token_expiresat = response_text['expiresAt']
            else:
                response_dict['message'] = 'Authentication Error: Token Generation Failed. ' + response_text['message']
        except Exception as ex:
            if ex.__class__.__name__ == 'ConnectionError':
                raise ConnectionError('Token Generation Failed: ' + str(ex))
            else:
                raise ex

        return response_dict

    def token_expired(self) -> bool:
        """Check if the token is expired.
        :return: True if token is expired, False if not expired
        :rtype: bool
        """
        expires_at = datetime.fromtimestamp(self.token_expiresat)
        return expires_at >= datetime.now()