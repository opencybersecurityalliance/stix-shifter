from stix_shifter_utils.modules.base.stix_transmission.base_delete_connector import BaseDeleteConnector
from stix_shifter_utils.utils.error_response import ErrorResponder


class DeleteConnector(BaseDeleteConnector):

    def __init__(self, client):
        self.client = client
        self.connector = __name__.split('.')[1]

    async def delete_query_connection(self, search_id):
        """
        Function to delete search id if the status in Running or Scheduled
        :param search_id: str, search id
        :return: dict
        """
        return_obj = dict()
        response_dict = dict()
        try:
            search_id = search_id.split(':')[0]
            if 'dummy' in search_id:
                return_obj['success'] = True
                return return_obj
            response_dict = await self.client.makeRequest('athena', 'stop_query_execution', QueryExecutionId=search_id)
            return_obj['success'] = True
        except Exception as ex:
            response_dict['__type'] = ex.__class__.__name__
            response_dict['message'] = ex
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj
