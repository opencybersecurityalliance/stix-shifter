from stix_shifter_utils.modules.base.stix_transmission.base_query_connector import BaseQueryConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
import json
from aiohttp.client_exceptions import ClientConnectionError
from .response_mapper import ResponseMapper


class QueryConnector(BaseQueryConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)

    async def create_query_connection(self, query):
        """
        Function to create query connection
        :param query: dict, Query
        :return: dict
        """
        return_obj = {}
        response_dict = {}
        response_wrapper = None
        try:
            response_wrapper = await self.api_client.create_search(query)
            if isinstance(response_wrapper, dict):
                return response_wrapper
            response_code = response_wrapper.code
            response_text = json.loads(response_wrapper.read().decode('utf-8'))
            if response_code == 200 and 'reply' in response_text.keys():
                return_obj['success'] = True
                return_obj['search_id'] = response_text['reply']
            else:
                return_obj = ResponseMapper().status_code_mapping(response_code, response_text)
        except ValueError as ex:
            if response_wrapper is not None and not isinstance(response_wrapper, dict):
                self.logger.debug(response_wrapper.read())
            raise Exception(f'Cannot parse response: {ex}') from ex

        except ClientConnectionError:
            response_dict['type'] = "ConnectionError"
            response_dict['message'] = "Invalid Host"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.api_client.connector)

        except Exception as exep:
            if 'timeout_error' in str(exep):
                response_dict['type'] = 'TimeoutError'
            else:
                response_dict['type'] = exep.__class__.__name__
            response_dict['message'] = exep
            self.logger.error('error when getting search results: %s', exep)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.api_client.connector)
        return return_obj
