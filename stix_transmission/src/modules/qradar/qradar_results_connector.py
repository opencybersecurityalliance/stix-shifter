from ..base.base_results_connector import BaseResultsConnector
import json


class QRadarResultsConnector(BaseResultsConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def create_results_connection(self, search_id, offset, length):
        min_range = offset
        max_range = offset + length
        # Grab the response, extract the response code, and convert it to readable json
        try:
            response = self.api_client.get_search_results(search_id, 'application/json', min_range, max_range)
            response_code = response.code

            # Construct a response object
            return_obj = dict()
            if response_code == 200:
                return_obj['success'] = True
                response_json = json.loads(response.read())
                return_obj['data'] = response_json['events']
            else:
                return_obj['success'] = False
                return_obj['error'] = response_json['message']
            return return_obj
        except Exception as err:
            print('error when getting search results: {}'.format(err))
            raise
