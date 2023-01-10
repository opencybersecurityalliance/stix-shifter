import datetime
import json
from stix_shifter_utils.modules.base.stix_transmission.base_json_sync_connector import BaseJsonSyncConnector
from .api_client import APIClient
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger


class Connector(BaseJsonSyncConnector):
    max_limit = 50

    def __init__(self, connection, configuration):
        self.api_client = APIClient(connection, configuration)
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    async def ping_connection(self):
        try:
            response = self.api_client.generate_token()
            # Construct a response object
            return_obj = dict()
            if response['code'] == 200:
                return_obj['success'] = True
            else:
                ErrorResponder.fill_error(return_obj, response, ['message'], connector=self.connector)
            return return_obj
        except Exception as err:
            self.logger.error('error when pinging datasource {}:'.format(err))
            raise

    async def create_results_connection(self, query_expr, offset, length):
        length = int(length)
        offset = int(offset)

        try:
            # Separate out api supported url params
            query_expr, filter_attr = Connector.modify_query_expr(query_expr)
            limit = int(query_expr.get('limit', 50))
            if limit > 50:
                if length > limit:
                    length = limit
                query_expr["limit"] = 50
            # Grab the response, extract the response code, and convert it to readable json
            # $(offset) param not included as data source not support this
            response = self.api_client.run_search(query_expr, length)
            response_code = response['code']
            # Construct a response object
            event_list = []
            for event in response.get("data", []):
                event = json.dumps(event.__dict__, default=Connector.default)
                event_list.append(json.loads(event))
            return_obj = dict()
            if response_code == 200:
                return_obj['success'] = True
                return_obj['data'] = event_list
                # filter data based on filter_attr
                return_obj = Connector.filter_response(return_obj, filter_attr)
                # slice the records as per the provided offset and length(limit)
                return_obj['data'] = return_obj['data'][offset:length]
            else:
                ErrorResponder.fill_error(return_obj, response, ['message'], connector=self.connector)
            return return_obj
        except Exception as err:
            self.logger.error('error when getting search results: {}'.format(err))
            import traceback
            self.logger.error(traceback.print_stack())
            raise

    @staticmethod
    def modify_query_expr(quary_expr):
        valid_filter_attributes = ["client_id", "directory_id", "created_at", "id", "until", "event_type_id", "limit",
                                   "since", "resolution", "user_id"]
        api_quary_attr = dict()
        filter_attr = []
        quary_expr_list = quary_expr.split("&")
        for attribute in quary_expr_list:
            if attribute.split("=")[0] in valid_filter_attributes:
                api_quary_attr.update({attribute.split("=")[0]: attribute.split("=")[1]})
            else:
                filter_attr.append(attribute)
        return api_quary_attr, filter_attr

    @staticmethod
    def filter_response(response_dict, filter_attr):
        try:
            for attr in filter_attr:
                response_dict['data'] = list(
                    filter(lambda person: person[attr.split("=")[0]] == attr.split("=")[1],
                           response_dict['data']))
        except KeyError as ex:
            raise KeyError(f"Invalid parameter {ex}")
        return response_dict

    @staticmethod
    def default(obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
