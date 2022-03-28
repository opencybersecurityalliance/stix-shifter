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
        response_dict = dict()
        try:
            response = self.api_client.ping_data_source()
            response_code = response['code']
            
            return_obj = dict()
            if response_code == 200:
                return_obj['success'] = True
            elif response_code == 401:
                response_dict['type'] = 'AuthenticationError'
                response_dict['message'] = 'Invalid App Secret key. API Response: {}'.format(response['message'])
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
            else:
                response_dict['type'] = 'AuthenticationError'
                response_dict['message'] = 'Invalid Authentication: Verify App ID. API Response: {}'.format(response['message'])
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
            return return_obj
        except Exception as err:
            self.logger.error('error when pinging datasource {}:'.format(err))
            raise
    
    def create_results_connection(self, search_id, offset, length):
        try:
            min_range = offset
            max_range = offset + length
            # Grab the response, extract the response code, and convert it to readable json
            response = self.api_client.get_search_results(search_id, min_range, max_range)
            response_code = response.code
            response_text = response.read()
            try:
                response_dict = json.loads(response_text)
            except ValueError as ex:
                self.logger.debug(response_text)
                error = Exception(f'Can not parse response from reaqta. The response is not a valid json: {response_text} : {ex}')
            
            # # Construct a response object
            return_obj = dict()
            if response_code == 200:
                return_obj['success'] = True
                return_obj['data'] = response_dict['result']
            else:
                response_string = response_text.decode()
                ErrorResponder.fill_error(return_obj, response_string, ['message'], connector=self.connector)
            return return_obj
        except Exception as err:
            self.logger.error('error when getting search results: {}'.format(err))
            import traceback
            self.logger.error(traceback.print_stack())
            raise