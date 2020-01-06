from ..base.base_delete_connector import BaseDeleteConnector
import json


class CloudSQLDeleteConnector(BaseDeleteConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def delete_query_connection(self, search_id):
        success = False
        try:
            response = self.api_client.delete_result(search_id)
            if response is None:
                response_json = {}
                response_json['message'] = "Delete failed"
            else:
                success = True
                response_json = json.loads(response.to_json(orient='records'))
        except ValueError as e:
            response_json = {}
            response_json['message'] = repr(e)

        # Construct a response object
        return_obj = dict()
        return_obj['success'] = success
        if not success:
            return_obj['error'] = response_json['message']

        return return_obj
