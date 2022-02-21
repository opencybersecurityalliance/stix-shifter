import json
import traceback

from stix_shifter_utils.modules.base.stix_transmission.base_results_connector import \
    BaseResultsConnector
from stix_shifter_utils.utils import logger
from stix_shifter_utils.utils.error_response import ErrorResponder


class ResultsConnector(BaseResultsConnector):

    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)

    def create_results_connection(self, search_id, offset, length):
        offset = int(offset)
        length = int(length)

        try:
            response = self.api_client.run_search(search_id, length)
            response_code = response['code']
            # Construct a response object
            return_obj = dict()
            if response_code == 200:
                return_obj['success'] = True
                return_obj['data'] = response.get("event_data", [])
                return_obj['search_after'] = response.get("search_after", [])
                # filter data based on filter_attr
                # slice the records as per the provided offset and length(limit)
                return_obj['data'] = return_obj['data'][offset:length]
            else:
                ErrorResponder.fill_error(return_obj, response, ['message'])

        except Exception as err:
            self.logger.error(
                'error when getting search results: {}'.format(err))
            self.logger.error(traceback.print_stack())
            raise
        return return_obj
