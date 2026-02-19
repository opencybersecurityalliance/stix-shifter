from stix_shifter_utils.modules.base.stix_transmission.base_ping_connector import BasePingConnector
from stix_shifter_utils.utils.error_response import ErrorResponder


class PingConnector(BasePingConnector):

    def __init__(self, client):
        self.client = client
        self.connector = __name__.split('.')[1]

    async def ping_connection(self):
        """
        Ping the endpoint
        :return: dict
        """
        return_obj = dict()
        response_dict = dict()
        try:
            await self.client.makeRequest('athena', 'list_work_groups')
            return_obj['success'] = True
        except Exception as ex:
            response_dict['__type'] = ex.__class__.__name__
            response_dict['message'] = ex
            if response_dict['__type'] == 'KeyError':
                if '(InvalidClientTokenId)' in str(response_dict['message']):
                    response_dict['__type'] = 'InvalidClientTokenId'
                elif '(SignatureDoesNotMatch)' in str(response_dict['message']):
                    response_dict['__type'] = 'SignatureDoesNotMatch'
                elif '(ValidationError)' in str(response_dict['message']):
                    response_dict['__type'] = 'ValidationError'

            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj
