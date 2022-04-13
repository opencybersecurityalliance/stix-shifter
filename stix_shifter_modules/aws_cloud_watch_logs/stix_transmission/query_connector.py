from stix_shifter_utils.modules.base.stix_transmission.base_connector import BaseQueryConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
import json

# aws maximum limit for start query loggroups
LOG_GROUP_NAMES_LIMIT = 20


class InvalidParameterException(Exception):
    pass


class QueryConnector(BaseQueryConnector):

    def __init__(self, client, log_group_names):
        self.client = client
        self.log_group_names = log_group_names
        self.connector = __name__.split('.')[1]

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
            log_type = query['logType']
            limit = query['limit']
            # add service specific loggroups to query if service logtype present
            # else loggroups in default type adds to query
            log_groups = self.log_group_names.get(log_type) if self.log_group_names.get(log_type) else \
                self.log_group_names.get('default')
            if log_groups:
                if isinstance(log_groups, list):
                    query['logGroupNames'] = log_groups
                else:
                    query['logGroupNames'] = [log_groups]
                # checking if loggroups is greater than maximum limit 20
                if len(query['logGroupNames']) > LOG_GROUP_NAMES_LIMIT:
                    raise InvalidParameterException("Too many log groups specified, log groups maximum limit is 20")
            # if loggroupnames is none, describe_log_groups api will be called
            else:
                log_group_response_dict = self.client.describe_log_groups(**{})
                log_group_names = []
                for log_group in log_group_response_dict['logGroups']:
                    log_group_names.append(log_group['logGroupName'])
                query['logGroupNames'] = log_group_names[:LOG_GROUP_NAMES_LIMIT]
            query.pop('logType')
            response_dict = self.client.start_query(**query)
            return_obj['success'] = True
            return_obj['search_id'] = response_dict['queryId'] + ':' + str(limit)
        except Exception as ex:
            response_dict['__type'] = ex.__class__.__name__
            response_dict['message'] = ex
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        return return_obj
