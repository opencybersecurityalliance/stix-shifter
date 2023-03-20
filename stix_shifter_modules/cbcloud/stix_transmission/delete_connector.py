import json

from stix_shifter_utils.modules.base.stix_transmission.base_delete_connector import BaseDeleteConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger


class DeleteConnector(BaseDeleteConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    async def delete_query_connection(self, search_id):
        response = await self.api_client.delete_search(search_id)
        response_code = response.code
        response_text = response.read()
        error = None
        response_dict = dict()

        try:
            # Successful deletion returns a 204 status code and empty response
            if response_text:
                response_dict = json.loads(response_text)
        except ValueError as ex:
            self.logger.debug(response_text)
            error = Exception(f'Can not parse response: {ex}')

        # Construct a response object
        return_obj = dict()
        return_obj['success'] = False

        # Successful deletion returns a 204 status code and empty response
        if response_code == 204:
            return_obj['success'] = True
        else:
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], error=error, connector=self.connector)

        return return_obj
