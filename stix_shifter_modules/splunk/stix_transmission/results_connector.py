from stix_shifter_utils.modules.base.stix_transmission.base_results_connector import BaseResultsConnector
from .api_client import APIClient
import json
from stix_shifter_utils.utils.error_response import ErrorResponder


class ResultsConnector(BaseResultsConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.connector = __name__.split('.')[1]

    def create_results_connection(self, search_id, offset, length):
        # Grab the response, extract the response code, and convert it to readable json
        response = self.api_client.get_search_results(search_id, offset, length)

        response_code = response.code
        response_dict = json.load(response)

        # Construct a response object
        return_obj = dict()
        if response_code == 200:
            if "results" in response_dict:
                results = response_dict['results']
            else:
                results = []
            return_obj['success'] = True
            return_obj['data'] = results

            # spliting hashes string into SHA256,MD5 and OTHERS
            for index, val in enumerate(return_obj['data']):
                has_dict_array = []
                if 'Hashes' in val:
                        return_obj['data'][index]['process_hash'] = return_obj['data'][index]['Hashes']
                        return_obj['data'][index]['file_hash'] = "f5568ea42e4cbd4bcf1f3bf6892d0049"
        else:
            ErrorResponder.fill_error(return_obj, response_dict, ['messages', 0, 'text'], connector=self.connector)
        return return_obj
