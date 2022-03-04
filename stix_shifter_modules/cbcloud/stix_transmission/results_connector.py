import json

from stix_shifter_utils.modules.base.stix_transmission.base_results_connector import BaseResultsConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger


class ResultsConnector(BaseResultsConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    def create_results_connection(self, search_id, offset, length):
        response = self.api_client.get_search_results(search_id, offset, length)
        response_code = response.code
        response_text = response.read()
        error = None
        response_dict = dict()

        try:
            response_dict = json.loads(response_text)
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
