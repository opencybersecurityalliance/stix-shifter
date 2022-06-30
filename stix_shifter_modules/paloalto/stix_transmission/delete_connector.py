from stix_shifter_utils.modules.base.stix_transmission.base_delete_connector import BaseDeleteConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger


class DeleteConnector(BaseDeleteConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)

    def delete_query_connection(self, search_id):
        """
        Delete operation of a search id is not supported in Palo Alto Cortex XDR
        :param search_id:str
        :return dict
        """
        try:
            response_dict = self.api_client.delete_search()
            response_code = response_dict['code']
            # Construct a response object
            return_obj = {}
            if response_code == 200:
                return_obj['success'] = response_dict['success']
                return_obj['message'] = 'Delete operation of a search id is not supported in Palo Alto Cortex XDR'
            else:
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.api_client.connector)
            return return_obj
        except Exception as err:
            self.logger.error('error when deleting search %s:', err)
            raise NotImplementedError('Error in delete search id operation') from err
