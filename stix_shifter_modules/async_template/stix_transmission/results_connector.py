from stix_shifter_utils.modules.base.stix_transmission.base_json_results_connector import BaseJsonResultsConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger

class ResultsConnector(BaseJsonResultsConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    async def create_results_connection(self, search_id, offset, length):
        try:
            min_range = offset
            max_range = offset + length
            # Grab the response, extract the response code, and convert it to readable json
            response_dict = await self.api_client.get_search_results(search_id, min_range, max_range)
            response_code = response_dict["code"]

            # Construct a response object
            return_obj = dict()
            if response_code == 200:
                return_obj['success'] = True
                return_obj['data'] = response_dict['data']
            else:
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
            return return_obj
        except Exception as err:
            self.logger.error('error when getting search results: {}'.format(err))
            raise
