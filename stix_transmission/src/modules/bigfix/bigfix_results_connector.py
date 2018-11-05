from ..base.base_results_connector import BaseResultsConnector
import json


class BigFixResultsConnector(BaseResultsConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def create_results_connection(self, search_id, offset, length):
        try:
            response = self.api_client.get_search_results(search_id, offset, length)
            response_code = response.code
            return_obj = dict()
            if 199 < response_code < 300:
                response_results = response.read()
                response_json = json.loads(response_results)
                return_obj['success'] = True
                return_obj['data'] = response_json['results']
            else:
                return_obj['success'] = False
                return_obj['error'] = 'error when getting results'
            return return_obj
        except Exception as err:
            return_obj = dict()
            return_obj['success'] = False
            return_obj['error'] = 'error when getting results: {}'.format(err)
            return return_obj
