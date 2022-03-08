from stix_shifter_utils.modules.base.stix_transmission.base_ping_connector import BasePingConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger


class PingConnector(BasePingConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    def ping_connection(self):
        response = self.api_client.ping_data_source()
        response_code = response.get('code')
        response_txt = response.get('message')
        return_obj = dict()
        return_obj['success'] = False

        if len(response) > 0 and response_code == 200:
            return_obj['success'] = True
        else:
            ErrorResponder.fill_error(return_obj, response, ['message'], error=response_txt, connector=self.connector)
        return return_obj
