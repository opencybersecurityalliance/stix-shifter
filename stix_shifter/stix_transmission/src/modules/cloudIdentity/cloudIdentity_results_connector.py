from ..base.base_connector import BaseConnector
from ..base.base_results_connector import BaseResultsConnector
import json
import pprint
from .....utils.error_response import ErrorResponder


class CloudIdentityResultsConnector(BaseConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def create_results_connection(self, search_id, offset, length):

        response = self.api_client.get_search_results(search_id)
        results = json.loads(response.read())
        return_obj = dict()
        if(response.code == 200):
            return_obj['success'] = True
            return_obj['data'] = results

            results['search_id'] = search_id

        return return_obj

    def checkResponse(self, response):
        if(response.code == 200):
            return True
        
        return False