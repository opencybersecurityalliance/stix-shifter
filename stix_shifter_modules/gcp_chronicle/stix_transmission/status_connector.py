from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import BaseStatusConnector
from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import Status
from enum import Enum
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
import json
from httplib2 import ServerNotFoundError
from google.auth.exceptions import RefreshError
import time


class InvalidResponseException(Exception):
    pass


class GCPChronicleStatus(Enum):
    RUNNING = 'RUNNING'
    DONE = 'DONE'
    CANCELLED = 'CANCELLED'
    STATE_UNSPECIFIED = 'STATE_UNSPECIFIED'


class StatusConnector(BaseStatusConnector):
    PROGRESS_PERCENTAGE = 0

    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    @staticmethod
    def get_status(status):
        """
        Return the status of the search id
        :param status: str,
        :return: str
        """
        switcher = {
            GCPChronicleStatus.RUNNING.value: Status.RUNNING,
            GCPChronicleStatus.DONE.value: Status.COMPLETED,
            GCPChronicleStatus.CANCELLED.value: Status.CANCELED,
            GCPChronicleStatus.STATE_UNSPECIFIED.value: Status.ERROR
        }
        return switcher.get(status).value

    async def create_status_connection(self, search_id):
        """
        Fetching the progress and the status of the search id
        :param search_id: str, search id
        :return: dict
        """

        return_obj = {}
        response_dict = {}
        try:
            response_wrapper = await self.api_client.get_search_status(search_id)
            response_text = json.loads(response_wrapper[1])

            if response_wrapper[0].status == 200:
                if 'state' in response_text.keys():
                    if response_text['state'] in ("RUNNING", "CANCELLED"):
                        return_obj['success'] = True
                        return_obj['progress'] = response_text['progressPercentage'] \
                            if 'progressPercentage' in response_text.keys() else 0
                        StatusConnector.PROGRESS_PERCENTAGE = return_obj['progress']
                        return_obj['status'] = StatusConnector.get_status(response_text['state'])

                    elif response_text['state'] == "DONE":
                        return_obj['success'] = True
                        return_obj['progress'] = 100
                        return_obj['status'] = StatusConnector.get_status(response_text['state'])

                    elif response_text['state'] == "STATE_UNSPECIFIED":
                        return_obj['success'] = False
                        return_obj['status'] = StatusConnector.get_status(response_text['state'])
                        return_obj['progress'] = 0
                else:
                    raise InvalidResponseException

            else:
                # sleep of 1 sec has been added to reduce the resource exhaustion in data source
                if response_wrapper[0].status == 429:
                    return_obj['success'] = True
                    return_obj['status'] = "RUNNING"
                    return_obj['progress'] = StatusConnector.PROGRESS_PERCENTAGE
                    time.sleep(1)
                    return return_obj
                response_dict['code'] = response_wrapper[0].status
                response_dict['message'] = response_text['error'].get('message')
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except ServerNotFoundError:
            response_dict['code'] = 1010
            response_dict['message'] = "Invalid Host"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except InvalidResponseException:
            response_dict['code'] = 100
            response_dict['message'] = "Invalid Response"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except RefreshError:
            response_dict['code'] = 1015
            response_dict['message'] = "Invalid Client Email"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except ValueError as v_err:
            if 'Could not deserialize key data' in str(v_err):
                response_dict['message'] = v_err
                response_dict['code'] = 1015
            else:
                response_dict['message'] = f'cannot parse {v_err}'
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except Exception as err:
            if "timed out" in str(err):
                response_dict['code'] = 120
                response_dict['message'] = str(err)
            else:
                response_dict['message'] = err
            self.logger.error('error when getting search results: %s', err)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        return return_obj
