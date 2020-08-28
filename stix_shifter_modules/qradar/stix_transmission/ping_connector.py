from stix_shifter_utils.modules.base.stix_transmission.base_ping_connector import BasePingConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger as utils_logger
import json


class PingConnector(BasePingConnector):

    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = utils_logger.set_logger(__name__)

    def ping_connection(self):
        response = self.api_client.ping_box()
        response_code = response.code

        response_txt = response.read()
        error = None
        response_dict = dict()
        try:
            response_dict = json.loads(response_txt)
        except Exception as ex:
            self.logger.debug(response_txt)
            error = Exception('Can not parse response: ' + str(ex))

        return_obj = dict()
        return_obj['success'] = False

        if len(response_dict) > 0 and response_code == 200:
            return_obj['success'] = True
        else:
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], error=error)
        return return_obj
