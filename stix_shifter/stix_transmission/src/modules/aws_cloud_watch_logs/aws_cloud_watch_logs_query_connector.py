from ..base.base_query_connector import BaseQueryConnector
from .....utils.error_response import ErrorResponder
import json


class AWSCloudWatchLogsQueryConnector(BaseQueryConnector):

    def __init__(self, client, log_group_names):
        self.client = client
        self.log_group_names = log_group_names

    def create_query_connection(self, query):
        """
        Function to create query connection
        :param query: str, Query
        :return: dict
        """
        return_obj = dict()
        response_dict = dict()
        try:
            query = json.loads(query)
            is_logtypepresent = False
            if self.log_group_names:
                if isinstance(self.log_group_names, dict):
                    for key, value in self.log_group_names.items():
                        if key == query['logType']:
                            is_logtypepresent = True
                            if isinstance(value, list):
                                query['logGroupNames'] = value
                            else:
                                query['logGroupNames'] = [value]
            if not is_logtypepresent:
                log_group_response_dict = self.client.describe_log_groups(**{})
                log_group_names = []
                for log_group in log_group_response_dict['logGroups']:
                    log_group_names.append(log_group['logGroupName'])
                query['logGroupNames'] = log_group_names
            query.pop('logType')
            response_dict = self.client.start_query(**query)
            return_obj['success'] = True
            return_obj['search_id'] = response_dict['queryId']
        except Exception as ex:
            response_dict['__type'] = ex.__class__.__name__
            response_dict['message'] = ex
            ErrorResponder.fill_error(return_obj, response_dict, ['message'])

        return return_obj
