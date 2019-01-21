from ..base.base_ping import BasePing
import json


class CarbonBlackPing(BasePing):

    def __init__(self, api_client):
        self.api_client = api_client

    def ping(self):
        try:
            response = self.api_client.ping_box()
            response_code = response.code
            response_json = json.loads(response.read())

            return_obj = dict()

            if len(response_json) > 0 and 200 <= response_code < 300:
                return_obj['success'] = True
            else:
                return_obj['success'] = False
                return_obj['error'] = 'error when pinging data source'
            return return_obj
        except Exception as err:
            return_obj = dict()
            return_obj['success'] = False
            return_obj['error'] = 'error when pinging data source: {}'.format(err)
            return return_obj
