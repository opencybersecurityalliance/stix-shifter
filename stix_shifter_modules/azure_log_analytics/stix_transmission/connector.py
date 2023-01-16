import json
from stix_shifter_utils.modules.base.stix_transmission.base_sync_connector import BaseSyncConnector
from .api_client import APIClient
from stix_shifter_utils.utils.error_response import ErrorResponder
import pandas as pd
from stix_shifter_utils.utils import logger
from azure.monitor.query import LogsQueryStatus
from azure.core.exceptions import ODataV4Format
from datetime import datetime, timedelta
import re


class Connector(BaseSyncConnector):

    def __init__(self, connection, configuration):
        """Initialization.
        :param connection: dict, connection dict
        :param configuration: dict,config dict"""
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]
        self.api_client = APIClient(connection, configuration)

    def ping_connection(self):
        """Ping the endpoint."""
        return_obj = dict()
        response = self.api_client.ping_box()
        response_code = response.code
        try:
            response_dict = json.loads(response.read())
        except:
            response_dict = json.loads(response.bytes)
        
        if 200 <= response_code < 300: 
            return_obj['success'] = True
        elif response_code == 404:
            error_dict = {"error": response_dict['error']['message'], "code": response_dict['error']['code']}
            ErrorResponder.fill_error(return_obj, error_dict, ['error', 'message'], connector=self.connector)
        else:
            ErrorResponder.fill_error(return_obj, response_dict, ['error', 'message'], connector=self.connector)

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
        query = """{query} | limit {len}""".format(query=query, len=length)
        matches = re.findall(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+?Z)', query)
        if matches:
            stop_time = datetime.strptime(matches[1].replace('Z', ""), "%Y-%m-%dT%H:%M:%S.%f")
            start_time = datetime.strptime(matches[0].replace('Z', ""), "%Y-%m-%dT%H:%M:%S.%f")
        else:
            stop_time = datetime.utcnow()
            start_time = stop_time - timedelta(hours=24)

        response = self.api_client.run_search(query, start_time, stop_time,
                                              total_record)

        if response["success"]:
            if response["response"].status == LogsQueryStatus.PARTIAL:
                error = response["response"].partial_error
                data = response["response"].partial_data
                self.logger.warn(error.message)
            elif response["response"].status == LogsQueryStatus.SUCCESS:
                data = response["response"].tables

            for table in data:
                df = pd.DataFrame(data=table.rows, columns=table.columns)
                return_obj = {"success": True, "data": df.astype(str).to_dict(orient='records')}
                return_obj['data'] = return_obj['data'][offset:total_record]

        else:
            if isinstance(response["error"], ODataV4Format):
                response_dict = {"error": response["error"], "code": response["error"].code}
            else:
                response_dict = {"error": response["error"]}
            ErrorResponder.fill_error(return_obj, response_dict, ['error', 'message'], connector=self.connector)
        return return_obj
