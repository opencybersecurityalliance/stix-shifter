import json
from stix_shifter_utils.modules.base.stix_transmission.base_sync_connector import BaseSyncConnector
from azure.identity import ClientSecretCredential
from .api_client import APIClient
from stix_shifter_utils.utils.error_response import ErrorResponder
import pandas as pd
from stix_shifter_utils.utils import logger
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from datetime import datetime, timedelta
import re


class Connector(BaseSyncConnector):
    max_limit = 1000
    init_error = None

    def __init__(self, connection, configuration):
        """Initialization.
        :param connection: dict, connection dict
        :param configuration: dict,config dict"""
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]
        self.workspace_id = connection.get('workspaceId')
        self.credential = ClientSecretCredential(tenant_id=configuration["auth"]["tenant"],
                                                 client_id=configuration["auth"]["clientId"],
                                                 client_secret=configuration["auth"]["clientSecret"])

        token = self.credential.get_token("https://{host}/.default".format(host=connection["host"]))
        configuration['auth']['access_token'] = token.token
        self.api_client = APIClient(connection, configuration)

    def ping_connection(self):
        """Ping the endpoint."""
        return_obj = dict()
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
        length = int(length)
        offset = int(offset)
        total_record = length + offset
        return_obj = dict()
        try:
            client = LogsQueryClient(self.credential)
            query = """{query} | limit {len}""".format(query=query, len=length)
            matches = re.findall(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+?Z)', query)
            if matches:
                stop_time = datetime.strptime(matches[1].replace('Z', ""), "%Y-%m-%dT%H:%M:%S.%f")
                start_time = datetime.strptime(matches[0].replace('Z', ""), "%Y-%m-%dT%H:%M:%S.%f")
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
                return_obj = {"success": True, "data": df.astype(str).to_dict(orient='records')}
                return_obj['data'] = return_obj['data'][offset:total_record]
            return return_obj
        except ValueError as ve:
            print("Missing WorkSpaceID. %s" % ve)
        except Exception as err:
            print("something fatal happened")
            print(err)
