import json
from stix_shifter_utils.modules.base.stix_transmission.base_ping_connector import BasePingConnector
from stix_shifter_utils.utils.error_response import ErrorResponder


class PingConnector(BasePingConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.connector = __name__.split('.')[1]

    def ping_connection(self):
        """
        Ping the endpoint
        :return: dict
        """
        return_obj = dict()

        try:
            return_obj = self.api_client.ping_data_source()
        except Exception as err:
            return_obj = dict()
            response_error = err
            ErrorResponder.fill_error(return_obj, response_error, ['message'], connector=self.connector)
        return return_obj