from ..base.base_ping import BasePing
import json
from .....utils.error_response import ErrorResponder


class QRadarPing(BasePing):
    def __init__(self, api_client):
        self.api_client = api_client

    def ping(self):
        response = self.api_client.ping_box()
        response_code = response.code

        response_dict = json.loads(response.read())

        return_obj = dict()
        return_obj['success'] = False

        if len(response_dict) > 0 and response_code == 200:
            return_obj['success'] = True
        else:
            ErrorResponder.fill_error(return_obj, response_dict, ['message'])
        return return_obj
