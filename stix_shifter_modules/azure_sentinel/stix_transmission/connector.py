import json
import adal
from stix_shifter_utils.modules.base.stix_transmission.base_sync_connector import BaseSyncConnector
from .api_client import APIClient
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
import pandas as pd
from datetime import datetime, timezone
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import ClientSecretCredential


class Connector(BaseSyncConnector):
    init_error = None
    max_limit = 1000

    def __init__(self, connection, configuration):
        """Initialization.
        :param connection: dict, connection dict
        :param configuration: dict,config dict"""
        self.logger = logger.set_logger(__name__)
        self.adal_response = Connector.generate_token(connection, configuration)
        if self.adal_response['success']:
            configuration['auth']['access_token'] = self.adal_response['access_token']
            self.api_client = APIClient(connection, configuration)
        else:
            self.init_error = True

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
        return_obj = dict()
        length = int(length)
        offset = int(offset)
        column_names = []
        final_result = []
        try:
            total_records = offset + length
            credential = ClientSecretCredential(tenant_id="924f8a12-f6bd-4b8d-93bf-9fa6e26cbf8b",
                                                client_id="15566bc1-0098-4e79-80a1-6390b97440ee",
                                                client_secret="AFv7Q~j3nXESOzqkzppQi86G0nhSckF6pw44G")
            client = LogsQueryClient(credential)
            query = """{query}""".format(query=query)
            start_time = datetime(2022, 2, 25, tzinfo=timezone.utc)
            end_time = datetime(2022, 3, 3, tzinfo=timezone.utc)
            response = client.query_workspace(
                workspace_id='e00daaf8-d6a4-4410-b50b-f5ef61c9cb45',
                query=query,
                timespan=(start_time, end_time)
            )
            if response.status == LogsQueryStatus.PARTIAL:
                error = response.partial_error
                data = response.partial_data
                print(error.message)
            elif response.status == LogsQueryStatus.SUCCESS:
                data = response.tables
            for table in data:
                df = pd.DataFrame(data=table.rows, columns=table.columns)
                return df.astype(str).to_dict(orient='records')
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
