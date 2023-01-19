from stix_shifter_utils.modules.base.stix_transmission.base_ping_connector import BasePingConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger


class PingConnector(BasePingConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)

    async def ping_connection(self):
        try:
            response = await self.api_client.ping_reversinglabs()

            # response = json.loads(response_dict.read().decode('utf-8'))
            # response_code = response_dict.code
            # response_dict = {'code': 1010, 'message': 'remote system error message'} # <-- simulate error in response to test error mapping
            # response_code = response_dict["code"]

            # Construct a response object
            return_obj = dict()
            if response['code'] == 200:
                return_obj['success'] = True
            else:
                response['message'] = 'Pinging failed'
                ErrorResponder.fill_error(return_obj, response, ['message'], connector='reversinglabs')
            return return_obj
        except Exception as err:
            self.logger.error('error when pinging datasource {}:'.format(err))
            raise