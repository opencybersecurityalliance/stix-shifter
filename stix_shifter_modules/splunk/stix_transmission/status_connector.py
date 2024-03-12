import json
import math
from enum import Enum
from asyncio.exceptions import TimeoutError
from aiohttp.client_exceptions import ClientConnectionError
from stix_shifter_utils.modules.base.stix_transmission.\
    base_status_connector import BaseStatusConnector, Status
from stix_shifter_utils.utils.error_response import ErrorResponder


class StatusSplunk(Enum):
    """query status values"""
    COMPLETED = 'DONE'
    ERROR = 'FAILED'
    RUNNING = 'RUNNING'


class StatusConnector(BaseStatusConnector):
    """check query status class"""
    def __init__(self, api_client):
        self.api_client = api_client
        self.connector = __name__.split('.')[1]

    async def create_status_connection(self, search_id):
        """
        get query status
        :param search_id
        :return: data response
        """
        # Grab the response, extract the response code, and convert it to readable json

        return_obj = {}
        response_dict = {}
        try:
            response = await self.api_client.get_search(search_id)
            response_code = response.code
            response_dict = json.load(response)
            response_text = response.content

            status, progress = '', ''

            if 'entry' in response_dict and isinstance(response_dict['entry'], list):
                content = response_dict['entry'][0]['content']
                progress = math.ceil(content['doneProgress'] * 100)  # convert 0-1.0 scale to <int>0-100
                status = content['dispatchState']

                if status == StatusSplunk.COMPLETED.value:
                    status = Status.COMPLETED.value
                elif status == StatusSplunk.ERROR.value:
                    status = Status.ERROR.value
                elif content['isFinalized'] is True:
                    status = Status.CANCELED.value
                else:
                    status = Status.RUNNING.value

            if response_code == 200:
                return_obj['success'] = True
                return_obj['status'] = status
                return_obj['progress'] = progress
            else:
                response_dict['type'] = str(response_code)
                if response_code == 404:
                    response_dict['type'] = "Unknown_sid"
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
