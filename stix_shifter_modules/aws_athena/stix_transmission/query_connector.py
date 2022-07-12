from stix_shifter_utils.modules.base.stix_transmission.base_connector import BaseQueryConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
import json
import re
import uuid

# static lookup for athena service types
service_types = {
                'guardduty': ['guardduty_database_name', 'guardduty_table_name'],
                'vpcflow': ['vpcflow_database_name', 'vpcflow_table_name']
                }


class InvalidParameterException(Exception):
    """
    Raise when encountering invalid connection parameters
    """


class QueryConnector(BaseQueryConnector):

    def __init__(self, client, connection):
        self.client = client
        self.connection = connection
        self.connector = __name__.split('.')[1]

    async def create_query_connection(self, query):
        """
        Function to create query connection
        :param query: dict, Query
        :return: dict
        """
        return_obj = dict()
        response_dict = dict()
        try:
            if not isinstance(query, dict):
                query = json.loads(query)
            query_service_type = list(query.keys())[0]
            config_details = service_types[query_service_type]
            if all([True if config not in self.connection.keys() else False for config in config_details]):
                return_obj = {'success': True, 'search_id': str(uuid.uuid4()) + '-dummy:' + query_service_type}
                return return_obj
            for config in config_details:
                if config not in self.connection.keys():
                    raise InvalidParameterException("{} is required for {} query operation".format(config,
                                                                                                   query_service_type))
            table_config = self.connection[config_details[0]] + "." + self.connection[config_details[1]]
            select_statement = "SELECT * FROM %s WHERE " % (table_config)
            # for multiple observation operators union and intersect, select statement will be added
            if 'UNION' in query[query_service_type] or 'INTERSECT' in query[query_service_type]:
                query_string = re.sub(r'\(\(', '(({}'.format(select_statement), query[query_service_type], 1)
                query = query_string.replace('UNION (', 'UNION ({}'.format(select_statement)).\
                    replace('INTERSECT (', 'INTERSECT ({}'.format(select_statement))
            else:
                query = select_statement + query[query_service_type]
            result_config = self.get_result_config()
            query_args = {"QueryString": query, "ResultConfiguration": result_config}
            response_dict = await self.client.makeRequest('athena', 'start_query_execution', **query_args)
            return_obj['success'] = True
            return_obj['search_id'] = response_dict['QueryExecutionId'] + ":" + query_service_type

        except Exception as ex:
            response_dict['__type'] = ex.__class__.__name__
            response_dict['message'] = ex
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj

    def get_result_config(self):
        """
        Output location and encryption configuration are added
        :return: dict, result configuration
        """
        output_location = ''
        path = self.connection.get('s3_bucket_location').strip()
        if path.startswith('s3://'):
            output_location = path
        elif path.startswith('s3'):
            split_path = path.split('s3', 1)[1]
            for i, char in enumerate(split_path):
                if char.isalnum():
                    output_location = 's3://' + split_path[i:]
                    break
        else:
            output_location = 's3://' + path
        result_config = {'OutputLocation': output_location}
        return result_config
