from stix_shifter_utils.modules.base.stix_transmission.base_connector import BaseQueryConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
import json


class QueryConnector(BaseQueryConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def create_query_connection(self, query):
        # Grab the response, extract the response code, and convert it to readable json
        response = self.api_client.create_search(query)
        response_code = response.code
        response_dict = json.loads(response.read())

        # Construct a response object
        return_obj = dict()

        if response_code == 201:
            return_obj['success'] = True
            return_obj['search_id'] = response_dict['search_id']
        else:
            ErrorResponder.fill_error(return_obj, response_dict, ['message'])
        
        return return_obj
