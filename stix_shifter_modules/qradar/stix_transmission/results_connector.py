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
        # Grab the response, extract the response code, and convert it to readable json

        response = self.api_client.get_search_results(search_id, 'application/json', min_range, max_range)
        response_code = response.code

        # Construct a response object
        return_obj = dict()
        error = None
        response_text = response.read()

        try:
            response_dict = json.loads(response_text)
        except ValueError as ex:
            self.logger.debug(response_text)
            error = Exception(f'Can not parse response: {ex} : {response_text}')
        
        if 200 <= response_code <= 299:
            return_obj['success'] = True
            return_obj['data'] = response_dict.get('events', response_dict.get('flows'))
        else:
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], error=error)

        return return_obj
