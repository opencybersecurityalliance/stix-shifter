from stix_shifter_utils.modules.base.stix_transmission.base_ping_connector import BasePingConnector
import json
from stix_shifter_utils.utils.error_response import ErrorResponder


class GuardiumPingConnector(BasePingConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def ping_connection(self):
        # Implemented for Guardium using fetch_token
        response = self.api_client.ping_box()
        response_code = response.code

        response_dict = json.loads(response.read())

        return_obj = dict()
        return_obj['success'] = False

        if len(response_dict) > 0 and response_code == 200:
            return_obj['success'] = True
            #return_obj["search_id"] = response_dict.get('search_id',"NA")
        else:
            ErrorResponder.fill_error(return_obj, response_dict, ['message'])
        return return_obj
