from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient
import json

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
        self.authenticated = False
        headers = dict()
        self.client = RestApiClient(connection.get('host'),
                                    connection.get('port'),
                                    headers,
                                    cert_verify=connection.get('selfSignedCert', True),
                                    sni=connection.get('sni', None)
                                    )
        self.auth = configuration.get('auth')
        self.headers = headers
        self.timeout = connection['options'].get('timeout')

    def authenticate(self):
        if not self.authenticated:
            self.set_splunk_auth_token(self.auth, self.headers)
            self.authenticated = True
        
    def set_splunk_auth_token(self, auth, headers):
        data = {'username': auth['username'], 'password': auth['password'], 'output_mode': 'json'}
        endpoint = self.endpoint_start + 'auth/login'
        try:
            response_json = json.load(self.client.call_api(endpoint, 'POST', headers, data=data, timeout=self.timeout))
            headers['Authorization'] = "Splunk " + response_json['sessionKey']
        except KeyError as e:
            raise Exception('Authentication error occured while getting auth token: ' + str(e))

    def ping_box(self):
        self.authenticate()
        endpoint = self.endpoint_start + 'server/status'
        data = {'output_mode': self.output_mode}
        return self.client.call_api(endpoint, 'GET', data=data, timeout=self.timeout)
        
    def create_search(self, query_expression):
        # sends a POST request to 
        # https://<server_ip>:<port>/services/search/jobs
        self.authenticate()
        endpoint = self.endpoint_start + "search/jobs"
        data = {'search': query_expression, 'output_mode': self.output_mode}
        return self.client.call_api(endpoint, 'POST', data=data, timeout=self.timeout)

    def get_search(self, search_id):
        # sends a GET request to
        # https://<server_ip>:<port>/services/search/jobs/<search_id>
        # returns information about the search job and its properties.
        self.authenticate()
        endpoint = self.endpoint_start + 'search/jobs/' + search_id        
        data = {'output_mode': self.output_mode}        
        return self.client.call_api(endpoint, 'GET', data=data, timeout=self.timeout)

    def get_search_results(self, search_id, offset, count):
        # sends a GET request to
        # https://<server_ip>:<port>/services/search/jobs/<search_id>/results
        # returns results associated with the search job.
        self.authenticate()
        endpoint = self.endpoint_start + "search/jobs/" + search_id + '/results'
        data = {'output_mode': self.output_mode}
        if ((offset is not None) and (count is not None)):
            data['offset'] = str(offset)
            data['count'] = str(count)
        # response object body should contain information pertaining to search.
        return self.client.call_api(endpoint, 'GET', urldata=data, timeout=self.timeout)
    
    def delete_search(self, search_id):
        # sends a DELETE request to
        # https://<server_ip>:<port>/services/search/jobs/<search_id>
        # cancels and deletes search created earlier.
        self.authenticate()
        endpoint = self.endpoint_start + 'search/jobs/' + search_id
        data = {'output_mode': self.output_mode}
        return self.client.call_api(endpoint, 'DELETE', data=data, timeout=self.timeout)
