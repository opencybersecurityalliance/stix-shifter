from stix_shifter_utils.modules.base.stix_transmission.base_ping_connector import BasePingConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
from json.decoder import JSONDecodeError
import json


class PingConnector(BasePingConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)

    def ping_connection(self):
        """
        Ping the endpoint
        :return: dict
        """
        return_obj = {}
        response_dict = {}
        try:
            response = self.api_client.ping_box()
            response_code = response.response.status_code
            response_dict = json.loads(response.response.text)
            if response_code == 200 and response_dict['status'] == 'SUCCESS':
                return_obj['success'] = True
        except JSONDecodeError:
            response_dict['type'] = "AuthenticationError"
            response_dict['message'] = "Invalid Authentication"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'])
        except Exception as ex:
            response_dict['type'] = ex.__class__.__name__
            response_dict['message'] = ex
            self.logger.error('error while pinging: %s', ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'])
        return return_obj
