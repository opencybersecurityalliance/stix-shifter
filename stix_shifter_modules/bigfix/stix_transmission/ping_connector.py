from stix_shifter_utils.modules.base.stix_transmission.base_ping_connector import BasePingConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger


class UnexpectedResponseException(Exception):
    pass


class PingConnector(BasePingConnector):

    ENDPOINT = '/api/clientquery'

    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    async def ping_connection(self):
        response_txt = None
        return_obj = dict()
        try:
            response = await self.api_client.ping_box()
            response_code = response.code
            response_txt = response.read().decode('utf-8')
            
            if self.ENDPOINT in response_txt and 199 < response_code < 300:
                return_obj['success'] = True
            elif ErrorResponder.is_plain_string(response_txt):
                ErrorResponder.fill_error(return_obj, message=response_txt, connector=self.connector)
            else:
                raise UnexpectedResponseException
        except Exception as e:
            if response_txt is not None:
                ErrorResponder.fill_error(return_obj, message='unexpected exception', connector=self.connector)
                self.logger.error('can not parse response: ' + str(response_txt))
            else:
                raise e
        
        return return_obj
