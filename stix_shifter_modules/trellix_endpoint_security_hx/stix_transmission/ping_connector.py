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
        """
        Pings the data source in the event of Ping operation
        :return: return_obj, dict
        """
        return_obj = {}
        try:

            token_obj = await self.__get_token()
            if token_obj:
                return token_obj
            response_wrapper = await self.api_client.ping_data_source()
            response_code = response_wrapper.code
            response_content = response_wrapper.read().decode('utf-8')
            if response_code == 200:
                return_obj['success'] = True
            else:
                return_obj = self.handle_api_exception(response_code, response_content)
        except Exception as err:
            self.logger.error('Error while pinging in Trellix endpoint Security HX: %s', err)
            return_obj = self.handle_api_exception(None, str(err))

        await self.api_client.delete_token()
        return return_obj

    def handle_api_exception(self, code, response_data):
        """
        create the exception response
        :param code, int
        :param response_data, dict
        :return: return_obj, dict
        """
        return_obj = {}
        try:
            response_data = json.loads(response_data)
            if response_data.get('details', []):
                message = response_data['details'][0]['message']
            else:
                message = response_data.get('message')
        except json.JSONDecodeError:
            message = response_data
        response_dict = {'code': code, 'message': message} if code else {'message': message}
        ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        return return_obj

    async def __get_token(self):
        """
        Generate a new API token
        :return:
        """
        return_obj = {}
        response = await self.api_client.generate_token()
        if response.code == 204 and response.headers.get('X-FeApi-Token'):
            self.api_client.headers['X-FeApi-Token'] = response.headers['X-FeApi-Token']
            if self.api_client.headers.get('Authorization'):
                self.api_client.headers.pop('Authorization')
        else:
            return_obj = self.handle_api_exception(response.code, response.read().decode('utf-8'))
        return return_obj
