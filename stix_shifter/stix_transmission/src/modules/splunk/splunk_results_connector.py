from ..base.base_results_connector import BaseResultsConnector
from .spl_api_client import APIClient
import json


class SplunkResultsConnector(BaseResultsConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def create_results_connection(self, search_id, offset, length):
        # Grab the response, extract the response code, and convert it to readable json
        try:
            response = self.api_client.get_search_results(search_id, offset, length)
            response_code = response.code
            response_json = json.load(response) 
            if "results" in response_json:
                results = [{}] if (response_json['results'] == []) else response_json['results']
            else:
                results = [{}]
            
            # Construct a response object
            return_obj = dict()
            if response_code == 200:
                return_obj['success'] = True
                return_obj['data'] = results
            else:
                return_obj['success'] = False
                return_obj['error'] = response_json['messages'][0]['text']
            return return_obj

        except Exception as err:
            print('error when getting search results: {}'.format(err))
            raise
