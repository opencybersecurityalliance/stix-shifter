from stix_shifter_utils.modules.base.stix_transmission.base_query_connector import BaseQueryConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
import json

class QueryConnector(BaseQueryConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    async def create_query_connection(self, query):
        try:
            await self.api_client.get_token()
            response = self.api_client.create_search(query)
            response_code = response.status_code
            
            # Construct a response object
            return_obj= dict()
            if response_code == 200:
                response_raw = response.read()
                response_dict = json.loads(response_raw)
                return_obj['search_id'] = response_dict['search_id']
                return_obj['success'] = True
            else:
                ErrorResponder.fill_error(return_obj, response, ['message'], connector=self.connector)
            return return_obj
        except Exception as err:
            self.logger.error('error when creating search: {}'.format(err))
            raise
