from stix_shifter_utils.modules.base.stix_transmission.base_ping_connector import BasePingConnector
from stix_shifter_utils.utils import logger
from stix_shifter_utils.utils.error_response import ErrorResponder


class PingConnector(BasePingConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    async def ping_connection(self):
        return_obj = dict()
        response_dict = dict()
        try:
            response_dict = await self.api_client.ping_data_source()
            response_code = response_dict["code"]

            # Construct a response object
            if response_code == 200:
                return_obj['success'] = True
            else:
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
            return return_obj
        except Exception as err:
            self.logger.error('error when pinging datasource: %s', err, exc_info=True)
            return_obj['success'] = False
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], error=err)
            return return_obj
