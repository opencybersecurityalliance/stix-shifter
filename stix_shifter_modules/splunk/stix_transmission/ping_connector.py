import json
from asyncio.exceptions import TimeoutError
from aiohttp.client_exceptions import ClientConnectionError
from stix_shifter_utils.modules.base.stix_transmission.base_ping_connector import BasePingConnector
from stix_shifter_utils.utils.error_response import ErrorResponder


class PingConnector(BasePingConnector):
    """Ping connector class """
    def __init__(self, api_client):
        self.api_client = api_client
        self.connector = __name__.split('.')[1]

    async def ping_connection(self):
        """
        Ping the endpoint
        :return: dict
        """
        return_obj = {}
        response_dict = {}
        try:
            response = await self.api_client.ping_box()
            response_code = response.code
            response_text = response.content

            response_dict = json.loads(response.read())

            if len(response_dict) > 0 and response_code == 200:
                return_obj['success'] = True
            else:
                response_dict['type'] = str(response_code)
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
