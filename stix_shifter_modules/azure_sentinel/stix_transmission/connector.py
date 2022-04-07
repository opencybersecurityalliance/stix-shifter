from calendar import c
import json
from multiprocessing import connection
import adal
from stix_shifter_utils.modules.base.stix_transmission.base_sync_connector import BaseSyncConnector
from .api_client import APIClient
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
import pandas as pd
from datetime import datetime, timezone
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import ClientSecretCredential
from datetime import datetime, timedelta
import re


class Connector(BaseSyncConnector):
    max_limit = 1000
    def __init__(self, connection, configuration):
        """Initialization.
        :param connection: dict, connection dict
        :param configuration: dict,config dict"""
        self.logger = logger.set_logger(__name__)
        self.workspace_id = connection.get('workspaceId')
        self.credential = ClientSecretCredential(tenant_id=configuration['auth']['tenant'],
                                                client_id=configuration['auth']['clientId'],
                                                client_secret=configuration['auth']['clientSecret'])

    def ping_connection(self):
        """Ping the endpoint."""
        return_obj = dict()
        if self.init_error:
            self.logger.error("Token Generation Failed:")
            return self.adal_response
        response = self.api_client.ping_box()
        response_code = response.code
        response_dict = json.loads(response.read())
        if 200 <= response_code < 300:
            return_obj['success'] = True
        else:
            ErrorResponder.fill_error(return_obj, response_dict, ['error', 'message'])
        return return_obj

    def delete_query_connection(self, search_id):
        """"delete_query_connection response
        :param search_id: str, search_id"""
        return {"success": True, "search_id": search_id}
    
    def create_results_connection(self, query, offset, length):
        """"built the response object
        :param query: str, search_id
        :param offset: int,offset value
        :param length: int,length value"""
        response = None
        length = int(length)
        offset = int(offset)

        try:
            client = LogsQueryClient(self.credential)
            query = """{query}""".format(query=query)
            matches = re.findall(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+?Z)', query)
            if matches:
                stop_time = datetime.strptime(matches[1].replace('Z', ""),"%Y-%m-%dT%H:%M:%S.%f")
                start_time =  datetime.strptime(matches[0].replace('Z', ""),"%Y-%m-%dT%H:%M:%S.%f")
            else: 
                stop_time = datetime.utcnow()
                start_time = stop_time - timedelta(hours=24)
            response = client.query_workspace(
                workspace_id=self.workspace_id,
                query=query,
                timespan=(start_time, stop_time)
            )
            if response.status == LogsQueryStatus.PARTIAL:
                error = response.partial_error
                data = response.partial_data
                print(error.message)
            elif response.status == LogsQueryStatus.SUCCESS:
                data = response.tables
            for table in data:
                df = pd.DataFrame(data=table.rows, columns=table.columns)
                return {"success": True, "data": df.astype(str).to_dict(orient='records')}
        except Exception as err:
            print("something fatal happened")
            print(err)

    @staticmethod
    def generate_token(connection, configuration):
        """To generate the Token
        :param connection: dict, connection dict
        :param configuration: dict,config dict"""
        return_obj = dict()
        authority_url = ('https://login.microsoftonline.com/' +
                         configuration['auth']['tenant'])
        resource = "https://" + str(connection.get('host'))

        try:
            context = adal.AuthenticationContext(
                authority_url, validate_authority=configuration['auth']['tenant'] != 'adfs',
            )
            response_dict = context.acquire_token_with_client_credentials(
                resource,
                configuration['auth']['clientId'],
                configuration['auth']['clientSecret'])

            return_obj['success'] = True
            return_obj['access_token'] = response_dict['accessToken']

        except Exception as ex:
            if ex.__class__.__name__ == 'AdalError':
                response_dict = ex.error_response
                ErrorResponder.fill_error(return_obj, response_dict, ['error_description'])
            else:
                ErrorResponder.fill_error(return_obj, message=str(ex))

        return return_obj
