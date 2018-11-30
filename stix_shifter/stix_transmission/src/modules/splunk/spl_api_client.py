from .RestApiClient import RestApiClient
import urllib.parse
import json


# Inherits methods from RestApiClient
class APIClient(RestApiClient):

    # API METHODS

    # These methods are used to call Splunk's API methods through http requests.
    # Each method makes use of the http methods below to perform the requests.

    # This class will encode any data or query parameters which will then be
    # sent to the call_api() method of its inherited class.
    def __init__(self, server_ip, auth):

        # This version of the Splunk APIClient is designed to function with
        # Splunk Enterprise version >= 6.5.0 and <= 7.1.2
        # http://docs.splunk.com/Documentation/Splunk/7.1.2/RESTREF/RESTprolog
        self.endpoint_start = 'services/'
        super(APIClient, self).__init__(server_ip, auth)

    def ping_box(self):
        endpoint = self.endpoint_start + 'server/status'
        params = {'output_mode': self.output_mode}
        return self.call_api(endpoint, 'GET', self.headers, params=params)

    def create_search(self, query_expression):
        endpoint = self.endpoint_start + "search/jobs"
        # sends a POST request to 
        # https://<server_ip>:<port>/services/search/jobs
        data = {'search': query_expression, 'output_mode': self.output_mode}
        data = urllib.parse.urlencode(data)
        data = data.encode('utf-8')
        return self.call_api(endpoint, 'POST', self.headers, data=data)

    def get_search(self, search_id):
        endpoint = self.endpoint_start + 'search/jobs/' + search_id
        # sends a GET request to
        # https://<server_ip>:<port>/services/search/jobs/<search_id>
        # returns information about the search job and its properties.
        params = {'output_mode': self.output_mode}
        return self.call_api(endpoint, 'GET', self.headers, params=params)

    def get_search_results(self, search_id, offset, count):
        headers = self.headers.copy()
        # sends a GET request to
        # https://<server_ip>:<port>/services/search/jobs/<search_id>/results
        # returns results associated with the search job.
        endpoint = self.endpoint_start + "search/jobs/" + search_id + '/results'
        params = {'output_mode': self.output_mode}
        if ((offset is not None) and (count is not None)):
            params['offset'] = str(offset)
            params['count'] = str(count)
        
        # response object body should contain information pertaining to search.
        return self.call_api(endpoint, 'GET', headers, params=params)
    
    def delete_search(self, search_id):
        endpoint = self.endpoint_start + 'search/jobs/' + search_id
        data = {'output_mode': self.output_mode}
        data = urllib.parse.urlencode(data)
        data = data.encode('utf-8')
        # sends a DELETE request to
        # https://<server_ip>:<port>/services/search/jobs/<search_id>
        # cancels and deletes search created earlier.
        return self.call_api(endpoint, 'DELETE', self.headers, data=data)
