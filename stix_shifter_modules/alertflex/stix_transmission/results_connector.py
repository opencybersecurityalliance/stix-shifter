from stix_shifter_utils.modules.base.stix_transmission.base_results_connector import BaseResultsConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
import json


class ResultsConnector(BaseResultsConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)

    def create_results_connection(self, search_id, offset, length):
        try:
            min_range = offset
            max_range = offset + length
            # Grab the response, extract the response code, and convert it to readable json
            response = self.api_client.get_search_results(search_id, min_range, max_range)
            response_code = response.code
            response_dict = json.loads(response.read())

            # # Construct a response object
            return_obj = dict()

            if 200 <= response_code < 300:
                return_obj['success'] = True
                return_obj['data'] = response_dict
            else:
                ErrorResponder.fill_error(return_obj, response_dict, ['messages', 0, 'text'])
            return return_obj

        except Exception as err:
            self.logger.error('error when getting search results: {}'.format(err))
            import traceback
            self.logger.error(traceback.print_stack())
            raise
