from stix_shifter_utils.modules.base.stix_transmission.base_json_results_connector import BaseJsonResultsConnector
from stix_shifter_utils.utils import logger
from stix_shifter_utils.utils.error_response import ErrorResponder


class ResultsConnector(BaseJsonResultsConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    async def create_results_connection(self, search_id, offset, length):
        response_dict = dict()
        return_obj = dict()
        try:
            offset_i = int(offset)
            len_i = int(length)
            min_range = offset_i
            if len_i > 1000:
                self.logger.warning("The length exceeds length limit. Use default length: 1000")
            max_range = offset_i + len_i if len_i <= 1000 else offset_i + 1000
            # Grab the response, extract the response code, and convert it to readable json
            response_dict = await self.api_client.get_search_results(search_id, min_range, max_range)
            response_code = response_dict["code"]

            # # Construct a response object
            if response_code == 200:
                return_obj['success'] = True
                return_obj['data'] = response_dict['data']['logs']
            else:
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
            return return_obj
        except Exception as err:
            self.logger.error('error when getting search results: %s', err, exc_info=True)
            return_obj['success'] = False
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], error=err)
            return return_obj
