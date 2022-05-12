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
                if 'Hashes' in val:
                    hashes = val['Hashes'].split(",")
                    hash_dict = {}
                    for hash_string in hashes:
                        if hash_string.find("SHA256", 0) != -1:
                            hash_dict.update({"SHA256": hash_string.lstrip("SHA256=")})
                        elif hash_string.find("MD5", 0) != -1:
                            hash_dict.update({"MD5": hash_string.lstrip("MD5=")})
                        else:
                            other_hash_list = []
                            other_hash_key = hash_string[:hash_string.index("=")]
                            others_hashes = {other_hash_key: hash_string.strip(other_hash_key + "=")}
                            other_hash_list.append(others_hashes)
                            hash_dict.update({"OTHERS": other_hash_list})
                        return_obj['data'][index]['Hashes'] = hash_dict
        else:
            ErrorResponder.fill_error(return_obj, response_dict, ['messages', 0, 'text'], connector=self.connector)
        return return_obj
