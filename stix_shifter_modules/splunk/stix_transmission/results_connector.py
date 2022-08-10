from stix_shifter_utils.modules.base.stix_transmission.base_results_connector import BaseResultsConnector
from .api_client import APIClient
import json
from stix_shifter_utils.utils.error_response import ErrorResponder
import re

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
            # for index, val in enumerate(return_obj['data']):
            #     has_dict_array = []
            #     if 'Hashes' in val:
            #         return_obj['data'][index]['Hashes'] = "b78bb50bdac5ec8c108f34104f788e214ac23635"

            for index, val in enumerate(return_obj['data']):
                if ('Hashes' in val):
                    hashes = val['Hashes'].split(",")
                    #check for , if not means falls in case 1 for regex
                    hshDict = {}
                    if(val['Hashes'].find(',') == -1):
                        file_hash_map = "file.hashes.{}"
                        if re.compile("^[a-f0-9]{32}$").match(val['Hashes']) is not None:
                            hshDict = {"md5hash":val['Hashes']}
                        elif re.compile(r'\b[0-9a-f]{40}\b').match(val['Hashes']) is not None:
                            hshDict = {"sha1hash":val['Hashes']}
                        elif re.compile("[A-Fa-f0-9]{64}").match(val['Hashes']) is not None:
                            hshDict = {"sha256hash":val['Hashes']}
                        else:
                            file_hash_map = file_hash_map.format("Unknown")
                            hshDict = file_hash_map

                    if(not bool(hshDict)):
                        for hash_string in hashes:
                            if (hash_string.find("SHA256", 0) != -1):
                                hshDict.update({"sha256hash": hash_string.lstrip("SHA256=")})
                            elif (hash_string.find("MD5", 0) != -1):
                                hshDict.update({"md5hash": hash_string.lstrip("MD5=")})
                            else:
                                hshDict.update({"IMPHASH": hash_string.lstrip("IMPHASH=")})
                    return_obj['data'][index]['Hashes'] = hshDict
        else:
            ErrorResponder.fill_error(return_obj, response_dict, ['messages', 0, 'text'], connector=self.connector)
        return return_obj
