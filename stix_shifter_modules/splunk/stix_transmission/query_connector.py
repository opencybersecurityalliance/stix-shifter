import json
from asyncio.exceptions import TimeoutError
from aiohttp.client_exceptions import ClientConnectionError
from stix_shifter_utils.modules.base.stix_transmission.base_connector import BaseQueryConnector
from stix_shifter_utils.utils.error_response import ErrorResponder


class QueryConnector(BaseQueryConnector):
    """ Query connector base class """
    def __init__(self, api_client):
        self.api_client = api_client
        self.connector = __name__.split('.')[1]

    async def create_query_connection(self, query):
        """
        init query
        :param query
        :return:search id
        """
        # Construct a response object
        return_obj = {}
        response_dict = {}
        try:
            # Grab the response, extract the response code, and convert it to readable json
            response = await self.api_client.create_search(query)
            response_code = response.code
            response_dict = json.loads(response.read())
            response_text = response.content

            if response_code == 201:
                return_obj['success'] = True
                return_obj['search_id'] = response_dict['sid']
            else:
                response_dict['type'] = str(response_code)
                if response_code == 400:
                    response_dict['type'] = "Unable_to_parse_search"
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
