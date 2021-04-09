from stix_shifter_utils.modules.base.stix_transmission.base_results_connector import BaseResultsConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
import json

class ResultsConnector(BaseResultsConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)

    def create_results_connection(self, query_data, offset, length):
        try:
            min_range = offset
            max_range = offset + length

            response_dict = self.api_client.get_search_results(query_data, min_range, max_range)
            response_code = response_dict["code"]

            query_data = query_data.replace('\'', "\"")
            query_json = json.loads(query_data)

            # # Construct a response object
            return_obj = dict()
            if response_code == 200:
                return_obj['success'] = True
                return_obj['report'] = response_dict['data']
                return_obj['data'] = query_json['data']
                return_obj['dataType'] =  query_json['dataType']
            else:
                ErrorResponder.fill_error(return_obj, response_dict, ['message'])
            return return_obj
        except Exception as err:
            self.logger.error('error when getting search results: {}'.format(err))
            import traceback
            self.logger.error(traceback.print_stack())
            raise
