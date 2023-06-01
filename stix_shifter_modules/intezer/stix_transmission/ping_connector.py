from stix_shifter_utils.modules.base.stix_transmission.base_ping_connector import BasePingConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
import json

class PingConnector(BasePingConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    async def ping_connection(self):
        try:
            response_dict = await self.api_client.ping_intezer()
            response_code = response_dict.code
            return_obj = dict()
            response = json.loads(response_dict.read().decode('utf-8'))

            if response_code == 200 and response['is_available']==True:
                return_obj['success'] = True
                return_obj['code'] = response_code
                return_obj['connector'] = self.connector
            else:
                ErrorResponder.fill_error(return_obj, response, ['message'], connector=self.connector)
                self.logger.error(response)
            return return_obj
        except Exception as err:
            self.logger.error('error when pinging datasource {}:'.format(err))
            raise
