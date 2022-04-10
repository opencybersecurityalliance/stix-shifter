import datetime
import json
from stix_shifter_utils.modules.base.stix_transmission.base_sync_connector import BaseSyncConnector
from .api_client import APIClient
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger


class Connector(BaseSyncConnector):

    def __init__(self, connection, configuration):
        self.api_client = APIClient(connection, configuration)
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    def ping_connection(self):
        response = self.api_client.ping_data_source()
        response_code = response.get('code')
        response_txt = response.get('message')
        return_obj = dict()
        return_obj['success'] = False

        if len(response) > 0 and response_code == 200:
            return_obj['success'] = True
        else:
            ErrorResponder.fill_error(return_obj, response, ['message'], error=response_txt, connector=self.connector)
        return return_obj

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