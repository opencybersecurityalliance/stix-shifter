from ..base.base_ping import BasePing
import json


class QRadarPing(BasePing):
    def __init__(self, api_client):
        self.api_client = api_client

    def ping(self):
        try:
            response = self.api_client.ping_box()
            response_code = response.code

            response_json = json.loads(response.read())

            return_obj = dict()
            return_obj['success'] = False

            if len(response_json) > 0 and response_code == 200:
                return_obj['success'] = True
            else:
                return_obj['error'] = response_json['message']

            return return_obj
        except Exception as err:
            print('error when pinging datasource {}:'.format(err))
            raise
