from stix_shifter_utils.modules.base.stix_transmission.base_delete_connector \
    import BaseDeleteConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger


class DeleteConnector(BaseDeleteConnector):
    """Delete connector class"""
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)

    async def delete_query_connection(self, search_id):
        """
        Delete query response
        :param queryId:
        :return:
        """
        try:
            #Construct a response object
            return_obj = {}
            response_dict = {}
            response = self.api_client.delete_search(search_id)
            response_code = response['code']

            if response_code == 200:
                return_obj['success'] = True
                return_obj['message'] = 'Delete operation of a search id is not supported in SentinelOne'

        except Exception as ex:
            response_dict['type'] = "unknown"
            response_dict['message'] = ex
            self.logger.error('error when delete request: %s', str(ex))
            ErrorResponder.fill_error(return_obj, response_dict, ['message'])
        return return_obj
