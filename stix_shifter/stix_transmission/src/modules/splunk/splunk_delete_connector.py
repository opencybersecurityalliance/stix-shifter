from ..base.base_delete_connector import BaseDeleteConnector
import json
from .....utils.error_response import ErrorResponder


class SplunkDeleteConnector(BaseDeleteConnector):
    def __init__(self, api_client):
        self.api_client = api_client
    
    def delete_query_connection(self, search_id):
        # Grab the response, extract the response code, and convert it to readable json
        response = self.api_client.delete_search(search_id)
        response_code = response.code
        response_dict = json.load(response)

        # Construct a response object
        return_obj = dict()
        if response_code == 200:
            return_obj['success'] = True
        else:
            ErrorResponder.fill_error(return_obj, response_dict, ['messages',0,'text'])

        return return_obj
