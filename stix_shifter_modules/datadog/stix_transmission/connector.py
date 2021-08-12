import json

from stix_shifter_modules.datadog.stix_transmission.api_client import APIClient
from stix_shifter_utils.modules.base.stix_transmission.base_sync_connector import BaseSyncConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger


class Connector(BaseSyncConnector):
    def __init__(self, connection, configuration):
        self.api_client = APIClient(connection, configuration)
        self.logger = logger.set_logger(__name__)

    def ping_connection(self):
        try:
            response = self.api_client.ping_data_source()
            # Construct a response object
            return_obj = dict()
            if response.get("valid", False):
                return_obj['success'] = True
            else:
                ErrorResponder.fill_error(return_obj, response, ['message'])
            return return_obj
        except Exception as err:
            self.logger.error('error when pinging datasource {}:'.format(err))
            raise

    def create_results_connection(self, search_id, offset, length):
        try:
            final = []
            min_range = offset
            max_range = offset + length
            # Grab the response, extract the response code, and convert it to readable json
            response_dict = self.api_client.get_search_results(search_id, min_range, max_range)
            for event in response_dict["events"]:
                json_string = json.dumps(event.__dict__, default=str)
                final.append(json.loads(json_string))
            # # Construct a response object
            return_obj = dict()
            return_obj['success'] = True
            return_obj['data'] = final
            return return_obj
        except Exception as err:
            self.logger.error('error when getting search results: {}'.format(err))
            import traceback
            self.logger.error(traceback.print_stack())
            raise
