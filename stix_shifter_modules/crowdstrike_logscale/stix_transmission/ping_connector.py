from stix_shifter_utils.modules.base.stix_transmission.base_ping_connector import BasePingConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger


class PingConnector(BasePingConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    async def ping_connection(self):
        """
        Pings the data source to check the status of the server
        :return: return_obj, dict
        """
        return_obj = {}
        try:
            response = await self.api_client.ping_data_source()
            response_code = response.code
            response_str = response.read().decode('utf-8')

            if response_code == 200:
                return_obj['success'] = True
            else:
                return_obj = self.handle_api_exception(response_code, response_str)
        except Exception as ex:
            self.logger.error('error while pinging in Crowdstrike Falcon Logscale: %s', ex)
            code = 408 if "timeout_error" in str(ex) else None
            return_obj = self.handle_api_exception(code, str(ex))

        return return_obj

    def handle_api_exception(self, code, response_txt):
        """
        create the exception response
        :param code, int
        :param response_txt, dict
        :return: return_obj, dict
        """
        return_obj = {}
        response_dict = {'code': code, 'message': str(response_txt)} if code else {'message': str(response_txt)}
        ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj
