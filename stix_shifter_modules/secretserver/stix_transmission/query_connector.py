from audioop import error

from stix_shifter_utils.modules.base.stix_transmission.base_connector import BaseQueryConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
import json

import json
from urllib import response
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.modules.base.stix_transmission.base_query_connector import BaseQueryConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger

class QueryConnector(BaseQueryConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    def create_query_connection(self, query):

            response = self.api_client.create_search(query)
            response_code = response.code
            response_dict = json.loads(response.read())

            # Construct a response object
            return_obj = dict()
            if response_code == 200:
                return_obj['success'] = True
                return_obj['search_id'] = response_dict['search_id']
            else:
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], error=error, connector=self.connector)

            return return_obj
