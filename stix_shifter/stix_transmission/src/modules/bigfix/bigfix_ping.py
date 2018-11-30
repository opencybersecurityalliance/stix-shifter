from ..base.base_ping import BasePing


class BigFixPing(BasePing):

    ENDPOINT = '/api/clientquery'

    def __init__(self, api_client):
        self.api_client = api_client

    def ping(self):
        try:
            response = self.api_client.ping_box()
            response_code = response.code
            result = response.read().decode('utf-8')
            return_obj = dict()

            if self.ENDPOINT in result and 199 < response_code < 300:
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
