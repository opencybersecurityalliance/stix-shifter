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
            response = self.api_client.ping_data_source()
            raw_response = response.read()
            response_code = response.code

            if 199 < response_code < 300:
                return_obj['success'] = True
            # arcsight logger error codes - currently unavailable state
            elif response_code in [500, 503]:
                response_string = raw_response.decode()
                ErrorResponder.fill_error(return_obj, response_string, ['message'], connector=self.connector)
            elif isinstance(json.loads(raw_response), dict):
                response_error_ping = json.loads(raw_response)
                response_dict = response_error_ping['errors'][0]
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
            else:
                raise Exception(raw_response)

        except Exception as err:
            return_obj = dict()
            response_error_ping = err
            ErrorResponder.fill_error(return_obj, response_error_ping, ['message'], connector=self.connector)

        return return_obj
