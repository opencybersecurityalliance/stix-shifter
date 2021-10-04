import json

from stix_shifter_utils.modules.base.stix_transmission.base_results_connector import BaseResultsConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger

class ResultsConnector(BaseResultsConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)

    def create_results_connection(self, search_id, offset, length):
        # try:
            min_range = int(offset)
            max_range = int(length)
            # Grab the response, extract the response code, and convert it to readable json
            # response_dict = self.api_client.get_search_results(search_id, min_range, max_range)
            response = self.api_client.get_search_results(search_id, min_range, max_range)
            return_obj = dict()
            return_obj['success'] = True
            return_obj['data'] =response
            return return_obj
