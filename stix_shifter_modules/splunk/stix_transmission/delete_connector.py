from stix_shifter_utils.modules.base.stix_transmission.base_delete_connector import BaseDeleteConnector
import json
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger


class DeleteConnector(BaseDeleteConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]
    
    async def delete_query_connection(self, search_id):
        # Grab the response, extract the response code, and convert it to readable json
        response = await self.api_client.delete_search(search_id)
        response_code = response.code
        response_dict = json.load(response)

        # Construct a response object
        return_obj = dict()
        if response_code == 200:
            return_obj['success'] = True
        else:
            self.logger.error('Fill Error: {}'.format(response_dict))
            ErrorResponder.fill_error(return_obj, response_dict, ['messages',0,'text'], connector=self.connector)

        return return_obj
