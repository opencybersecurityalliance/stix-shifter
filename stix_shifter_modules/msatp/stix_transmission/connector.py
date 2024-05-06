import json
from stix_shifter_utils.modules.base.stix_transmission.base_json_sync_connector import BaseJsonSyncConnector
from .api_client import APIClient
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger

from .connector_post_processing import ConnectorPostProcessing


class Connector(BaseJsonSyncConnector):
    logger = logger.set_logger(__name__)

    def __init__(self, connection, configuration):
        """Initialization.
        :param connection: dict, connection dict
        :param configuration: dict,config dict"""
        self.connector = __name__.split('.')[1]
        self.options = connection['options']
        self.api_client = APIClient(connection, configuration)

    def _handle_errors(self, response, return_obj):
        """Handling API error response
        :param response: response for the API
        :param return_obj: dict, response for the API call with status
        """
        response_code = response.code
        response_txt = response.read().decode('utf-8')

        if 200 <= response_code < 300:
            return_obj['success'] = True
            return_obj['data'] = response_txt
            return return_obj
        elif ErrorResponder.is_plain_string(response_txt):
            ErrorResponder.fill_error(return_obj, message=response_txt, connector=self.connector)
            raise Exception(return_obj)
        elif ErrorResponder.is_json_string(response_txt):
            response_json = json.loads(response_txt)
            ErrorResponder.fill_error(return_obj, response_json, ['reason'], connector=self.connector)
            raise Exception(return_obj)
        else:
            raise Exception(return_obj)

    async def ping_connection(self):
        """Ping the endpoint."""
        return_obj = dict()
        response = await self.api_client.ping_box()
        response_code = response.code
        if 200 <= response_code < 300:
            return_obj['success'] = True
        else:
            ErrorResponder.fill_error(return_obj, message='unexpected exception', connector=self.connector)
        return return_obj

    async def delete_query_connection(self, search_id):
        """"delete_query_connection response
        :param search_id: str, search_id"""
        return {"success": True, "search_id": search_id}

    async def create_results_connection(self, query, offset, length):
        """"built the response object
        :param query: str, search_id
        :param offset: int,offset value
        :param length: int,length value"""

        util = ConnectorPostProcessing(self.options, False)
        response_txt = None
        return_obj = {
            'success': True,
            'data': []
        }

        try:
            joined_query = util.join_query_with_other_tables(query)
            response_data = await self.api_client_run_search(joined_query, length, offset)

            async def api_run(q):
                return await self.api_client_run_search(q, length, offset)

            return util.post_process(response_data, return_obj, api_run)
        except Exception as ex:
            if response_txt is not None:
                ErrorResponder.fill_error(return_obj, message='unexpected exception', connector=self.connector)
                self.logger.error('can not parse response: ' + str(response_txt))
            else:
                raise ex

    async def api_client_run_search(self, joined_query, length, offset):
        temp_return_obj = dict()
        response = await self.api_client.run_search(joined_query, offset, length)
        temp_return_obj = self._handle_errors(response, temp_return_obj)
        response_data = json.loads(temp_return_obj["data"]).get("Results")
        return response_data
