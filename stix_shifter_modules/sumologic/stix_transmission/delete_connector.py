from stix_shifter_utils.modules.base.stix_transmission.base_delete_connector import BaseDeleteConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger


class DeleteConnector(BaseDeleteConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)

    def delete_query_connection(self, search_id):
        try:
            response_dict = self.api_client.delete_search(search_id)
            response_code = response_dict.code

            # Construct a response object
            return_obj = dict()
            if response_code == 200:
                if 'id' in response_dict.object:
                    return_obj['success'] = True
                elif 'error' in response_dict.object:
                    return_obj['success'] = False
                    return_obj['code'] = 'no_results'
            else:
                ErrorResponder.fill_error(return_obj, response_dict, ['message'])
            return return_obj
        except Exception as err:
            self.logger.error('error when deleting search {}:'.format(err))
            raise
