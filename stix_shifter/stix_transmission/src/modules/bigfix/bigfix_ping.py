from ..base.base_ping import BasePing
from .....utils.error_response import ErrorResponder

class UnexpectedResponseException(Exception):
    pass

class BigFixPing(BasePing):

    ENDPOINT = '/api/clientquery'

    def __init__(self, api_client):
        self.api_client = api_client

    def ping(self):
        response_txt = None
        return_obj = dict()
        try:
            response = self.api_client.ping_box()
            response_code = response.code
            response_txt = response.read().decode('utf-8')
            
            if self.ENDPOINT in response_txt and 199 < response_code < 300:
                return_obj['success'] = True
            elif ErrorResponder.is_plain_string(response_txt):
                ErrorResponder.fill_error(return_obj, message=response_txt)
            else:
                raise UnexpectedResponseException
        except Exception as e:
            if response_txt is not None:
                ErrorResponder.fill_error(return_obj, message='unexpected exception')
                print('can not parse response: ' + str(response_txt))
            else:
                raise e
        
        return return_obj
