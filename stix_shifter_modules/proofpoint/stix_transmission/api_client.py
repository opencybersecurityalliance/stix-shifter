import base64
from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient

ENDPOINT_SINCESEC = 'all?format=syslog&sinceSeconds=3600'
ENDPOINT_ALL = 'all?format=json&'

class APIClient():

    def __init__(self, connection, configuration):
        # Uncomment when implementing data source API client.
        auth = configuration.get('auth')
        headers = dict()
        cred = tuple()
        if auth:
            if 'username' in auth and 'password' in auth:
                headers['Authorization'] = b"Basic " + base64.b64encode(
                    (auth['username'] + ':' + auth['password']).encode('ascii'))
        self.client = RestApiClient(connection.get('host'),
                                    port=None,
                                    headers=headers, url_modifier_function=None, cert_verify=True, sni=None, auth=None
                                    )

    def ping_data_source(self):
        # Pings the data source
        pingresult = self.client.call_api(endpoint=ENDPOINT_SINCESEC, method='GET')
        return pingresult

    def create_search(self, query_expression):
        # Queries the data source
        return {"code": 200, "query_id": "uuid_1234567890"}

    def get_search_status(self, search_id):
        # Check the current status of the search
        return {"code": 200, "status": "COMPLETED"}

    def get_search_results(self, search_id):
        # Return the search results. Results must be in JSON format before being translated into STIX
        resultdata = self.client.call_api(endpoint=ENDPOINT_ALL+search_id, method='GET')
        # Check the current status of the search
        return resultdata

    def delete_search(self, search_id):
        # Optional since this may not be supported by the data source API
        # Delete the search
        return {"code": 200, "success": True}
