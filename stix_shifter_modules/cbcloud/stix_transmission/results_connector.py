import json
import ntpath
import re

from stix_shifter_utils.modules.base.stix_transmission.base_json_results_connector import BaseJsonResultsConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger


class ResultsConnector(BaseJsonResultsConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    async def create_results_connection(self, search_id, offset, length):
        response = await self.api_client.get_search_results(search_id, offset, length)
        response_code = response.code
        response_text = response.read()
        error = None
        response_dict = dict()

        try:
            response_dict = json.loads(response_text)
            ResultsConnector.modify_result(response_dict['results'])
        except ValueError as ex:
            self.logger.debug(response_text)
            error = Exception(f'Can not parse response: {ex}')

        return_obj = dict()
        return_obj['success'] = False

        if response_dict and response_code == 200:
            return_obj['success'] = True
            return_obj['data'] = response_dict['results']
        else:
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], error=error, connector=self.connector)

        return return_obj
        
    @classmethod
    def modify_result(cls, data):
        for json_entry in data:
            # Split process hash lists into separate md5 and sha256 entries
            if json_entry.get('process_hash', False):
                md5, sha256 = ResultsConnector.parse_hash(json_entry.pop('process_hash'))
                json_entry['process_md5'] = md5
                json_entry['process_sha256'] = sha256

            if json_entry.get('parent_hash', False):
                md5, sha256 = ResultsConnector.parse_hash(json_entry.pop('parent_hash'))
                json_entry['parent_md5'] = md5
                json_entry['parent_sha256'] = sha256

            # Convert the process_name and parent_name to split path and name fields
            if json_entry.get('process_name', False):
                tmp = json_entry['process_name']
                json_entry['process_name'] = ntpath.basename(tmp)
                json_entry['process_path'] = ntpath.dirname(tmp)

            if json_entry.get('parent_name', False):
                tmp = json_entry['parent_name']
                json_entry['parent_name'] = ntpath.basename(tmp)
                json_entry['parent_path'] = ntpath.dirname(tmp)

            # Convert list values
            for key in json_entry:
                if isinstance(json_entry.get(key, False), list):
                    # If only 1 value, replace the list with the value
                    if len(json_entry[key]) == 1:
                        json_entry[key] = json_entry[key][0]
                    # If more than 1 value, convert the list items to a string
                    elif len(json_entry[key]) > 1:
                        json_entry[key] = f"[{', '.join(str(x) for x in json_entry[key])}]"

    @staticmethod
    def parse_hash(hashlist):
        """Extract hash values from list."""
        md5 = ''
        sha256 = ''

        for hash_value in hashlist:
            if re.match('^[a-fA-F0-9]{32}$', hash_value):
                md5 = hash_value
            elif re.match('^[a-fA-F0-9]{64}$', hash_value):
                sha256 = hash_value

        return md5, sha256