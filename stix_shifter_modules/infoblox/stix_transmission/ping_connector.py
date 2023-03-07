"""
Ping Connector

See: https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/adapter-guide/develop-transmission-module.md
"""
from stix_shifter_utils.modules.base.stix_transmission.base_ping_connector import BasePingConnector
from stix_shifter_utils.utils import logger
from stix_shifter_utils.utils.error_response import ErrorResponder


class PingConnector(BasePingConnector):
    """
    Class that handles ping connector integration

    :param api_client: api_client for connecting with Infoblox APIs
    :type api_client: api_client

    Attributes:
        api_client (ApiClient): Infoblox API client
        logger (logger): Internal logger
    """
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    async def ping_connection(self):
        """
        Creates a synchronous ping connection.

        NOTE: This checks if the Infoblox APIs are up and available.

        :return: response object (includes success, code, and message fields)
        :rtype: object
        """
        try:
            response = await self.api_client.ping_data_source()
            response_code = response.code
            response_body = response.read().decode('utf-8')

            # Construct a response object
            return_obj = dict()
            if response_code == 200:
                return_obj['success'] = True
            else:
                response_dict = {'code': response_code, 'message': response_body}
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
            return return_obj
        except Exception as err:
            self.logger.error('error when pinging datasource: %s', err)
            raise
