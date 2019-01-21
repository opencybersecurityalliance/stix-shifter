from ..base.base_results_connector import BaseResultsConnector
import json


class CarbonBlackResultsConnector(BaseResultsConnector):

    def __init__(self, api_client):
        self.api_client = api_client

    def create_results_connection(self, search_id, offset, length):
        try:
            query = search_id
            response = self.api_client.run_search(query)
            response_code = response.code
            response_json = json.loads(response.read())
            return_obj = dict()

            if 200 <= response_code < 300:
                return_obj['success'] = True
                return_obj['data'] = response_json
            else:
                return_obj['success'] = False
                return_obj['error'] = 'error when creating search'

            return return_obj
        except Exception as err:
            return_obj = dict()
            return_obj['success'] = False
            return_obj['error'] = 'error when creating search: {}'.format(err)
            return return_obj
