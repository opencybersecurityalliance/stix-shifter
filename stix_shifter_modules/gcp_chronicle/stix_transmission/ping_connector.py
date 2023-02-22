from stix_shifter_utils.modules.base.stix_transmission.base_ping_connector import BasePingConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
import json
from aiogoogle.excs import HTTPError
from aiohttp.client_exceptions import ClientConnectionError
from asyncio.exceptions import TimeoutError


class PingConnector(BasePingConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
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
            response_code = response.status_code
            response_text = response.content
            if response_code == 200:
                return_obj['success'] = True
            else:
                response_dict['code'] = response_code
                response_dict['message'] = response_text
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except ClientConnectionError:
            response_dict['code'] = 1010
            response_dict['message'] = "Invalid Host"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except HTTPError as ex:
            if 'invalid_grant' in str(ex):
                response_dict['code'] = 1015
                response_dict['message'] = "Invalid Client Email"
            else:
                response_dict['message'] = str(ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except ValueError as v_ex:
            if 'Could not deserialize key data' in str(v_ex):
                response_dict['message'] = v_ex
                response_dict['code'] = 1015
            else:
                response_dict['message'] = f'cannot parse {v_ex}'
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except TimeoutError as ex:
            response_dict['code'] = 120
            response_dict['message'] = 'TimeoutError ' + str(ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except Exception as ex:
            response_dict['message'] = ex
            self.logger.error('error when getting search results: %s', ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        return return_obj
