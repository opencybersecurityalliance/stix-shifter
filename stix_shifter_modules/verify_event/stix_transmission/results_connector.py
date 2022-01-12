from stix_shifter_utils.modules.base.stix_transmission.base_results_connector import BaseResultsConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
import json


class ResultsConnector(BaseResultsConnector):
    
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
    
    def create_results_connection(self, search_id, offset, length):
        min_range = offset
        max_range = offset + length
        size = int(length)-int(offset)
        search_id_expr =search_id+'&size='+str(size)

        # Grab the response, extract the response code, and convert it to readable json
        #response = self.api_client.get_search_results(search_id, 'application/json', min_range, max_range)
        try :
            response = self.api_client.run_search(search_id_expr)
            response_code = response['code']
        except ValueError as ex:
            self.logger.debug(ex)
            error = Exception(f'Can not retrieve response from verify server. {search_id_expr} : {ex}')
        
        return response
   