import json
from asyncio.exceptions import TimeoutError
from aiohttp.client_exceptions import ClientConnectionError
from stix_shifter_utils.modules.base.stix_transmission.base_delete_connector import BaseDeleteConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger


class DeleteConnector(BaseDeleteConnector):
    """Delete connector class"""
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    async def delete_query_connection(self, search_id):
        """
        Delete query response
        :param search_id:
        :return:
        """
        return_obj = {}
        response_dict = {}
        try:
            # Grab the response, extract the response code, and convert it to readable json
            response = await self.api_client.delete_search(search_id)
            response_code = response.code
            response_dict = json.load(response)
            response_text = response.content

            if response_code == 200:
                return_obj['success'] = True
            else:
                response_dict['type'] = str(response_code)
                if response_code == 404:
                    response_dict['type'] = "Unknown_sid"
                self.logger.error('Fill Error: {}'.format(response_dict))
                response_dict['message'] = response_text
                ErrorResponder.fill_error(return_obj, response_dict,
                                          ['messages'], connector=self.connector)
        except ClientConnectionError:
            response_dict['type'] = "ConnectionError"
            response_dict['message'] = "Invalid Host"
            ErrorResponder.fill_error(return_obj, response_dict,
                                      ['message'], connector=self.connector)
        except TimeoutError as ex:
            response_dict['type'] = "Timeout"
            response_dict['messages'] = "TimeoutError"
            ErrorResponder.fill_error(return_obj, response_dict,
                                      ['messages'], connector=self.connector)
        except Exception as ex:
            if 'Authentication error' in str(ex):
                response_dict['type'] = "AuthenticationError"
            elif 'timeout_error' in str(ex):
                response_dict['type'] = "Timeout"
            response_dict['messages'] = str(ex)
            ErrorResponder.fill_error(return_obj, response_dict,
                                      ['messages'], connector=self.connector)

        return return_obj
