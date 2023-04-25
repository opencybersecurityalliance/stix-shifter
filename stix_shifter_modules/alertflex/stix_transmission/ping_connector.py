import json
from stix_shifter_utils.modules.base.stix_transmission.base_ping_connector import BasePingConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger

class PingConnector(BasePingConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    async def ping_connection(self):
        try:
            response = await self.api_client.ping_data_source()
            response_code = response.code
            response_text = json.loads(response.read().decode('utf-8'))
            # Construct a response object
            return_obj = dict()
            response_dict = dict()

            if response_code == 200:
                return_obj['success'] = True
            elif response_code == 401:
                return_obj['success'] = False
                response_dict['type'] = 'AuthenticationError'
                response_dict['message'] = 'Invalid credentials provided. {}'.format(response_text)
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
            else:
                return_obj['success'] = False
                response_dict['message'] = 'Error. {}'.format(response_text)
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
            return return_obj
        except Exception as err:
            self.logger.error('error when pinging datasource {}:'.format(err))
            raise
