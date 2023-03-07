from stix_shifter_utils.modules.base.stix_transmission.base_delete_connector import BaseDeleteConnector
from stix_shifter_utils.utils.error_response import ErrorResponder


class DeleteConnector(BaseDeleteConnector):

    def __init__(self, api_client):
        self.api_client = api_client

    async def delete_query_connection(self, search_id):
        return_obj = dict()
        return_obj['success'] = True
        return return_obj
