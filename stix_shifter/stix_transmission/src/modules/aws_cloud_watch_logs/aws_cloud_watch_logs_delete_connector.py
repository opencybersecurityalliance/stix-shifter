from ..base.base_delete_connector import BaseDeleteConnector
from .....utils.error_response import ErrorResponder


class AWSCloudWatchLogsDeleteConnector(BaseDeleteConnector):

    def __init__(self, client):
        self.client = client

    def delete_query_connection(self, search_id):
        """
        Function to delete search id if the status in Running or Scheduled
        :param search_id: str, search id
        :return: dict
        """
        return_obj = dict()
        response_dict = dict()
        try:
            query = dict()
            if ':' in search_id:
                search_id = search_id.split(':')[0]
            query['queryId'] = search_id
            self.client.stop_query(**query)
            return_obj['success'] = True
        except Exception as ex:
            response_dict['__type'] = ex.__class__.__name__
            response_dict['message'] = ex
            ErrorResponder.fill_error(return_obj, response_dict, ['message'])

        return return_obj
