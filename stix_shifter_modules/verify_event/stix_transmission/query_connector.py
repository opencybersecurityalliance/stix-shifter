from stix_shifter_utils.modules.base.stix_transmission.base_connector import BaseQueryConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
import json


class QueryConnector(BaseQueryConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)

    def create_query_connection(self, query):
        
        error = None
        try :
            api_response = self.api_client.run_search(query)
            response_code = api_response['success']
        except ValueError as ex:
            self.logger.debug(ex)
            error = Exception(f'Can not parse response: {ex} ')


        return_obj = dict()
        if 200 <= response_code <= 299 and error is None:
            return_obj['success'] = True
            return_obj['search_id'] = query
        else:
            ErrorResponder.fill_error(return_obj, api_response, ['message'], error=error)
        
        return return_obj
