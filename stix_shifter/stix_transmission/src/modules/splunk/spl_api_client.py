from ..utils.RestApiClient import RestApiClient, ResponseWrapper
import urllib.parse
import json
import base64
from urllib.parse import urlencode

class APIClient():
    # API METHODS

    # These methods are used to call Splunk's API methods through http requests.
    # Each method makes use of the http methods below to perform the requests.

    # This class will encode any data or query parameters which will then be
    # sent to the call_api() method of its inherited class.
    def __init__(self, connection, configuration):

        # This version of the Splunk APIClient is designed to function with
        # Splunk Enterprise version >= 6.5.0 and <= 7.1.2
        # http://docs.splunk.com/Documentation/Splunk/7.1.2/RESTREF/RESTprolog

        self.output_mode = 'json'
        self.endpoint_start = 'services/'
        headers = dict()
        self.client = RestApiClient(connection.get('host'),
                                    connection.get('port'),
                                    connection.get('cert', None),
                                    headers,
                                    cert_verify=connection.get('cert_verify', 'True')
                                    )
        auth = configuration.get('auth')                
        self.set_splunk_auth_token(auth, headers)

        
    def set_splunk_auth_token(self, auth, headers):
        data = {'username': auth['username'], 'password': auth['password'], 'output_mode': 'json'}
        endpoint = self.endpoint_start + 'auth/login'
        try:
            data = urlencode(data)
            data = data.encode('utf-8')
            response_json = json.load(self.client.call_api(endpoint, 'POST', headers, data=data))
            headers['Authorization'] = "Splunk " + response_json['sessionKey']
        except Exception as e:
            print('Authentication error occured while getting auth token.')
            raise e        

    def ping_box(self):
        endpoint = self.endpoint_start + 'server/status'
        data = {'output_mode': self.output_mode}
        return self.client.call_api(endpoint, 'GET', data=data)
        
    def create_search(self, query_expression):
        # sends a POST request to 
        # https://<server_ip>:<port>/services/search/jobs
        endpoint = self.endpoint_start + "search/jobs"
        data = {'search': query_expression, 'output_mode': self.output_mode}
        data = urllib.parse.urlencode(data)
        data = data.encode('utf-8')
        return self.client.call_api(endpoint, 'POST', data=data)

    def get_search(self, search_id):
        # sends a GET request to
        # https://<server_ip>:<port>/services/search/jobs/<search_id>
        # returns information about the search job and its properties.
        endpoint = self.endpoint_start + 'search/jobs/' + search_id        
        data = {'output_mode': self.output_mode}        
        return self.client.call_api(endpoint, 'GET', data=data)

    def get_search_results(self, search_id, offset, count):
        # sends a GET request to
        # https://<server_ip>:<port>/services/search/jobs/<search_id>/results
        # returns results associated with the search job.
        endpoint = self.endpoint_start + "search/jobs/" + search_id + '/results'
        data = {'output_mode': self.output_mode}
        if ((offset is not None) and (count is not None)):
            data['offset'] = str(offset)
            data['count'] = str(count)
        # response object body should contain information pertaining to search.
        return self.client.call_api(endpoint, 'GET', data=data)
    
    def delete_search(self, search_id):
        # sends a DELETE request to
        # https://<server_ip>:<port>/services/search/jobs/<search_id>
        # cancels and deletes search created earlier.
        endpoint = self.endpoint_start + 'search/jobs/' + search_id
        data = {'output_mode': self.output_mode}
        data = urllib.parse.urlencode(data)
        data = data.encode('utf-8')
        return self.client.call_api(endpoint, 'DELETE', data=data)