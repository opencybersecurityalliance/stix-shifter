from stix_shifter_utils.modules.base.stix_transmission.base_ping_connector import BasePingConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger

class PingConnector(BasePingConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)

    def ping_connection(self):
        try:
            response_dict = self.api_client.ping_data_source()
            response_code = response_dict.code
            # Construct a response object
            return_obj = dict()
            if response_code >= 200 and response_code <= 204:
                return_obj['success'] = True
            else:
                ErrorResponder.fill_error(return_obj, str(response_code)+ ":"+str(response_dict.read().decode("utf-8")), ['message'])
            return return_obj
        except Exception as err:
            self.logger.error('error when pinging datasource {}:'.format(err))
            raise
