from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient
from .guard_utils import GuardUtil

class APIClient():

    def __init__(self, connection, configuration):
        # Uncomment when implementing data source API client.
        # auth = configuration.get('auth')
        # headers = dict()
        # headers['X-Auth-Token'] = auth.get('token')
        # self.client = RestApiClient(connection.get('host'),
        #                             connection.get('port'),
        #                             connection.get('cert', None),
        #                             headers,
        #                             cert_verify=connection.get('cert_verify', 'True')
        #                             )

        # Placeholder client to allow dummy transmission calls.
        # Remove when implementing data source API client.
        url = "https://"+connection["host"]+":"+connection["port"]
        self.client = GuardUtil(connection["options"]["client_id"], url, connection["options"]["client_secret"], configuration["auth"]["username"], configuration["auth"]["password"])
        #self.client = "data source API client"

    def ping_data_source(self):
        
        # Pings the data source
        return {"code": 200, "success": True}

    def get_search_results(self, search_id, range_start=None, range_end=None):
        # Return the search results. Results must be in JSON format before being translated into STIX
        return {"code": 200, "data": "Results from search"}

    def delete_search(self, search_id):
        # Optional since this may not be supported by the data source API
        # Delete the search
        return {"code": 200, "success": True}
    
    def create_search(self, query):
        self.client.create_search(query)