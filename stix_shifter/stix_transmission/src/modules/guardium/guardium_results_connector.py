from ..base.base_results_connector import BaseResultsConnector
import json
from .....utils.error_response import ErrorResponder

class GuardiumResultsConnector(BaseResultsConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def create_results_connection(self, search_id, offset, length):
        # Grab the response, extract the response code, and convert it to readable json
        # Verify the input

        response = self.api_client.get_search_results(search_id, 'application/json', offset, length)
        response_code = response.code

        # Construct a response object
        return_obj = dict()
        results = json.loads(response.read())

        if response_code == 200:
            return_obj['success'] = True
            # In the case of no results datasource returns a json/dict type reponse : 
            #       {'ID': 0, 'Message': 'The Query did not retrieve any records'}
            #  Therefore setting empty list after checking the datatype
            if isinstance(results, dict):
                 return_obj['data'] = []
            else:
                return_obj['data'] = results

            return_obj["search_id"] = search_id
        else:
            ErrorResponder.fill_error(return_obj, results, ['message'])

        return return_obj
