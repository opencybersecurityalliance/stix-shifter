from stix_shifter_utils.modules.base.stix_transmission.base_ping_connector import BasePingConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
import json
from aiohttp.client_exceptions import ClientConnectionError
from .response_mapper import ResponseMapper


class PingConnector(BasePingConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)

    async def ping_connection(self):
        """
        Ping the endpoint
        :return: dict
        """
        return_obj = {}
        response_dict = {}
        response_wrapper = None
        try:
            response_wrapper = await self.api_client.ping_data_source()
            response_code = response_wrapper.response.status_code
            response_text = json.loads(response_wrapper.read().decode('utf-8'))
            if response_code == 200 and 'reply' in response_text.keys():
                return_obj['success'] = True
            else:
                return_obj = ResponseMapper().status_code_mapping(response_code, response_text)

        except ValueError as ex:
            if response_wrapper is not None:
                self.logger.debug(response_wrapper.read())
            raise Exception(f'Cannot parse response: {ex}') from ex

        except ClientConnectionError:
            response_dict['type'] = "ConnectionError"
            response_dict['message'] = "Invalid Host"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.api_client.connector)

        except Exception as exe:
            if 'timeout_error' in str(exe):
                response_dict['type'] = 'TimeoutError'
            else:
                response_dict['type'] = exe.__class__.__name__
            response_dict['message'] = exe
            self.logger.error('error when getting search results: %s', exe)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.api_client.connector)
        return return_obj
