from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import BaseStatusConnector
from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import Status
from enum import Enum
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
import json
from requests.exceptions import ConnectionError
from .response_mapper import ResponseMapper


class InvalidResponseException(Exception):
    pass


class InvalidQueryException(Exception):
    pass


class PaloAltoStatus(Enum):
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'
    FAIL = 'FAIL'


class StatusConnector(BaseStatusConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)

    # Map data source status to connector status
    @staticmethod
    def get_status(status):
        """
        Return the status of the search id
        :param status: str,
        :return: str
        """
        switcher = {
            PaloAltoStatus.PENDING.value: Status.RUNNING,
            PaloAltoStatus.COMPLETED.value: Status.COMPLETED,
            PaloAltoStatus.FAIL.value: Status.ERROR
        }
        return switcher.get(status).value

    def create_status_connection(self, search_id):
        """
        Fetching the progress and the status of the search id
        :param search_id: str, search id
        :return: dict
        """
        return_obj = {}
        response_dict = {}
        response = None
        try:
            response = self.api_client.get_search_status(search_id)
            # Based on the response
            response_code = response.code
            response_read = response.read()
            response_text = json.loads(response_read)

            if response_code == 200:
                if 'status' in response_text['reply'].keys():
                    # Since PaloAlto API doesnt return the numerical value of progress, the value for Pending
                    # status is set to 50. If the status is completed, it is set to 100.
                    if response_text['reply']['status'] == "PENDING":
                        return_obj['success'] = True
                        return_obj['status'] = StatusConnector.get_status('PENDING')
                        return_obj['progress'] = 50
                    elif response_text['reply']['status'] == "SUCCESS":
                        if 'number_of_results' in response_text['reply'].keys():
                            return_obj['success'] = True
                            return_obj['status'] = StatusConnector.get_status('COMPLETED')
                            return_obj['progress'] = 100
                        else:
                            raise InvalidResponseException
                    else:
                        return_obj = self.handle_fail_response(response_text, return_obj, response_dict)
            else:
                return_obj = ResponseMapper().status_code_mapping(response_code, response_text)

        except ValueError as ex:
            if response is not None:
                self.logger.debug(response.read())
            raise Exception(f'Cannot parse response: {ex}') from ex

        except InvalidResponseException:
            response_dict['type'] = 'EmptyResultException'
            response_dict['message'] = 'Empty results received from Tenant'
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.api_client.connector)

        except ConnectionError:
            response_dict['type'] = "ConnectionError"
            response_dict['message'] = "Invalid Host"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.api_client.connector)
        except Exception as err:
            if 'timeout_error' in str(err):
                response_dict['type'] = 'TimeoutError'
            else:
                response_dict['type'] = err.__class__.__name__
            response_dict['message'] = err
            self.logger.error('error when getting search results: %s', err)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.api_client.connector)
        return return_obj

    def handle_fail_response(self, response_text, return_obj, response_dict):
        """
        Handle partial success or failed status response
        :param return_obj: dict
        :param response_dict: dict
        :param response_text: dict
        """
        try:
            if response_text['reply']['status'] == "PARTIAL_SUCCESS":
                return_obj['success'] = True
                return_obj['status'] = StatusConnector.get_status('COMPLETED')
                return_obj['message'] = "Partial Success -At least one tenant failed to execute the query"
            elif response_text['reply']['status'] == "FAIL":
                raise InvalidQueryException
        except InvalidQueryException:

            response_dict['type'] = "SyntaxError"
            response_dict['message'] = 'Tenant Query Failed'
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.api_client.connector)
        return return_obj
