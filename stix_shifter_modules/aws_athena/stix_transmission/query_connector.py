from venv import logger
from stix_shifter_modules.aws_athena.stix_transmission import status_connector
from stix_shifter_modules.aws_athena.stix_transmission.post_query_connector_error_handling import PostQueryConnectorErrorHandler
from stix_shifter_utils.modules.base.stix_transmission.base_connector import BaseQueryConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
import json
import re
import time
import uuid

# static lookup for athena service types
service_types = {
                'guardduty': ['guardduty_database_name', 'guardduty_table_name'],
                'vpcflow': ['vpcflow_database_name', 'vpcflow_table_name'],
                'ocsf': ['ocsf_database_name', 'ocsf_table_name']
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
        self.total_try_count = 0

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
            table_config = self.connection[config_details[0]] + '."' + self.connection[config_details[1]] + '"'
            
            other_tables = ''
            findall = re.finditer("##UNNEST.*?##", query[query_service_type])
            if findall:
                for match in findall:
                    if match.group():
                        match_str = str(match.group())
                        query[query_service_type] = query[query_service_type].replace(match_str, '')
                        other_tables += ' %s%s%s ' % ('LEFT JOIN ', match_str.replace('##', ''), ' ON TRUE ')

            if query_service_type == 'ocsf':
                columns = await self.column_list(self.connection[config_details[0]], self.connection[config_details[1]])
                column_cast = []
                for column in columns:
                    column_cast.append("CAST(%s as JSON) AS %s" % (column, column))

                select_statement = "SELECT %s FROM %s%s WHERE " % (", ".join(column_cast), table_config, other_tables)
            else:
                select_statement = "SELECT %s.* FROM %s%s WHERE " % (table_config, table_config, other_tables)
                        
            #self.get_list_of_columns_and_rows(query[query_service_type])
            #await self.row_list(self.connection[config_details[0]], self.connection[config_details[1]])
            # for multiple observation operators union and intersect, select statement will be added
            if 'UNION' in query[query_service_type] or 'INTERSECT' in query[query_service_type]:
                query_string = re.sub(r'\(\(', '(({}'.format(select_statement), query[query_service_type], 1)
                query_with_select = query_string.replace('UNION (', 'UNION ({}'.format(select_statement)).\
                    replace('INTERSECT (', 'INTERSECT ({}'.format(select_statement))
            else:
                query_with_select = select_statement + query[query_service_type]
            result_config = self.get_result_config()
            
            return await self.query_api(query_with_select, result_config, query_service_type, return_obj)
            
        except Exception as ex:
            response_dict['__type'] = ex.__class__.__name__
            response_dict['message'] = ex
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj

    async def query_api(self, query, result_config, query_service_type, return_obj):
        """Creates a query job and ensures that none of the columns requested are missing from the query.

        Args:
            query (String): The original query without modification. 
            result_config (Dict): Query configuration.
            query_service_type (String): The type of query ("OCSF", "VPCFlow, etc)
            return_obj (Dict): Contains the metadata about the request.

        Returns:
            Dict: The metadata about the request such as the query/search ID and the status.
        """
        logger.debug(f"The current query is : {query}")

        #Creates the initial query job.
        query_args = {"QueryString": query, "ResultConfiguration": result_config}
        response_dict = await self.client.makeRequest('athena', 'start_query_execution', **query_args)
        return_obj['search_id'] = response_dict['QueryExecutionId'] + ":" + query_service_type

        modified_query = dict()
        modified_query = await PostQueryConnectorErrorHandler.check_status_for_missing_column(self.client, return_obj['search_id'], query)
        #If the query is successful (or the exception isn't column related) than it's considered a success and exits.
        #If 10 columns are not found or it fails to replace a column 10 times, than it exits (to prevent endless loops).
        #If the query is not successful, than it will retry the query with the modified query.
        if(modified_query == "CONNECTOR_FACTORY_SUCCESS" or self.total_try_count > 10):
            logger.debug(f"The total attempt count was {self.total_try_count}")
            if(self.total_try_count >= 10):
                logger.warn("There were 10 failed exceptions related to columns. This could be because there were more invalid columns than 10, \
                             or alternatively that the replacement failed to remove the offending column.")
            return_obj['success'] = True
            return return_obj
        else:
            self.total_try_count = self.total_try_count + 1
            return await self.query_api(modified_query, result_config, query_service_type, return_obj)
            
    async def column_list(self, database, table):
        columns = []
        query = f"SELECT column_name,data_type FROM information_schema.columns WHERE table_name = '{table}' AND table_schema = '{database}'" 
        result_config = self.get_result_config()
        query_args = {"QueryString": query, "ResultConfiguration": result_config}
        response_dict = await self.client.makeRequest('athena', 'start_query_execution', **query_args)
        execution_id = response_dict['QueryExecutionId']

        state = "RUNNING"
        max_execution = 10
        while max_execution > 0 and state in ["RUNNING", "QUEUED"]:
            max_execution -= 1
            response = await self.client.makeRequest('athena', 'get_query_execution', QueryExecutionId=execution_id)
            if (
                "QueryExecution" in response
                and "Status" in response["QueryExecution"]
                and "State" in response["QueryExecution"]["Status"]
            ):
                state = response["QueryExecution"]["Status"]["State"]
                s3_output_location = response['QueryExecution']['ResultConfiguration']['OutputLocation']
                if state == "SUCCEEDED":
                    break
            time.sleep(1)

        if state == "SUCCEEDED":
            response = await self.client.makeRequest('athena', 'get_query_results', QueryExecutionId=execution_id)
            results = response['ResultSet']['Rows'][1:]
            for row in results:
                columns.append(row['Data'][0]['VarCharValue'])
        else:
            raise InvalidParameterException("Error in getting Athena table column list")
        
        s3_output_bucket_with_file = s3_output_location.split('//')[1]
        s3_output_bucket = s3_output_bucket_with_file.split('/')[0]
        s3_output_key = '/'.join(s3_output_bucket_with_file.split('/')[1:])
        s3_output_key_metadata = s3_output_key + '.metadata'
        delete = dict()
        delete['Objects'] = [{'Key': s3_output_key}, {'Key': s3_output_key_metadata}]
        # Api call to delete s3 object
        delete_object = await self.client.makeRequest('s3', 'delete_objects', Bucket=s3_output_bucket, Delete=delete)
        if delete_object.get('Errors'):
            message = delete_object.get('Errors')[0].get('Message')
            raise Exception("Error in deleting s3 metadata after Athena query: " + message)
        
        if not columns:
            raise InvalidParameterException('No Athena table with name ' + table)

        return columns

    def get_rows_from_response(self, data, parent, row_list):
        data = data.casefold()
        ##Root of the tree.
        if(data.startswith("row(".casefold()) or data.startwith("array(".casefold())):
            remainder = data[data.find("("):data.rfind(")")]
            self.get_rows_from_response(remainder, parent, row_list)            
        
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
    