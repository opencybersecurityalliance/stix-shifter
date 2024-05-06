import datetime
import json

from stix_shifter_modules.ibm_security_verify.stix_transmission.api_client import \
    APIClient
from stix_shifter_utils.modules.base.stix_transmission.base_ping_connector import \
    BasePingConnector
from stix_shifter_utils.utils import logger
from stix_shifter_utils.utils.error_response import ErrorResponder


class PingConnector(BasePingConnector):

    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    async def ping_connection(self):
        '''
        ping the connection and return status details.
        '''
        try:
            response = await self.api_client.generate_token()
            # Construct a response object
            return_obj = dict()
            if response.code == 200:
                return_obj['success'] = True
            else:
                message_obj = {"message": response.read(), "code": response.code}
                ErrorResponder.fill_error(return_obj, message_obj, ['message', 'code'], connector=self.connector)
            return return_obj
        except Exception as err:
            self.logger.error('error when pinging datasource {}:'.format(err))
            raise
