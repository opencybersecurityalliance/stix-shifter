from stix_shifter_utils.modules.base.stix_transmission.base_results_connector import BaseResultsConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger


class ResultsConnector(BaseResultsConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    def create_results_connection(self, query, offset, length):
        return_obj = dict()
        response = self.api_client.run_search(query, start=offset, rows=length)
        response_code = response.get('code')
        response_txt = response.get('message')
        if response_code == 200:
            return_obj['success'] = True
            return_obj['data'] = response.get('result')
        else:
            ErrorResponder.fill_error(return_obj, response, ['message'], error=response_txt, connector=self.connector)
        return return_obj
