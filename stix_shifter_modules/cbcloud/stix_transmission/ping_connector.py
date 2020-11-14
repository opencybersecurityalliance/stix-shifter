import json

from stix_shifter_utils.modules.base.stix_transmission.base_ping_connector import BasePingConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger


class PingConnector(BasePingConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)

    def ping_connection(self):
        response = self.api_client.ping_data_source()
        response_code = response.code
        response_text = response.read()
        error = None
        response_dict = dict()

        try:
            response_dict = json.loads(response_text)
        except ValueError as ex:
            self.logger.debug(response_text)
            error = Exception('Can not parse response: ' + str(ex))

        return_obj = dict()
        return_obj['success'] = False

        if response_dict and response_code == 200:
            return_obj['success'] = True
        else:
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], error=error)

        return return_obj
