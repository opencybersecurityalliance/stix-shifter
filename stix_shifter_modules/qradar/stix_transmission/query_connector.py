from stix_shifter_utils.modules.base.stix_transmission.base_connector import BaseQueryConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
import json


class QueryConnector(BaseQueryConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    async def create_query_connection(self, query):
        # Grab the response, extract the response code, and convert it to readable json
        response = await self.api_client.create_search(query)
        response_code = response.code
        response_text = response.read()
        error = None
        response_dict = dict()

        try:
            response_dict = json.loads(response_text)
        except ValueError as ex:
            self.logger.debug(response_text)
            error = Exception(f'Can not parse response: {ex} : {response_text}')

        # Construct a response object
        return_obj = dict()

        if response_code == 201:
            return_obj['success'] = True
            return_obj['search_id'] = response_dict['search_id']
        else:
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], error=error, connector=self.connector)
        
        return return_obj
