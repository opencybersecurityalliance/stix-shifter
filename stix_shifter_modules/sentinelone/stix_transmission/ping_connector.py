import json
from stix_shifter_utils.modules.base.stix_transmission.base_ping_connector \
    import BasePingConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from requests.exceptions import ConnectionError
from stix_shifter_utils.utils import logger


class PingConnector(BasePingConnector):
    """Ping connector class """
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)

    def ping_connection(self):
        """
        Ping the endpoint
        :return: dict
        """
        try:
            # Construct a response object
            return_obj = {}
            response_dict = {}

            response = self.api_client.ping_datasource()

            response_code = response.code
            response_txt = response.read().decode('utf-8')

            response_dict = json.loads(response_txt)

            if response_code == 200:
                return_obj['success'] = True
                return_obj['code'] = response_code
            else:
                return_obj['success'] = False
                return_obj['code'] = response_code

        except ConnectionError:
            response_dict['type'] = "ConnectionError"
            response_dict['message'] = "Invalid Host"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'])
        except Exception as ex:
            if 'Max retries exceeded' in str(ex):
                return_obj['success'] = True
                return_obj['code'] = 200
                return return_obj
            else:
                self.logger.error('error when ping: %s', str(ex))
                ErrorResponder.fill_error(return_obj, response_dict, ['message'])

        return return_obj