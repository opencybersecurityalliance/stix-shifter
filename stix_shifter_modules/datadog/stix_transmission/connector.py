import json
from stix_shifter_modules.datadog.stix_transmission.api_client import APIClient
from stix_shifter_utils.modules.base.stix_transmission.base_sync_connector import BaseSyncConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger


class Connector(BaseSyncConnector):
    def __init__(self, connection, configuration):
        self.api_client = APIClient(connection, configuration)
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    def ping_connection(self):
        try:
            response = self.api_client.ping_data_source()
            # Construct a response object
            return_obj = dict()
            if response["code"] == 200:
                return_obj['success'] = True
            else:
                ErrorResponder.fill_error(return_obj, response, ['message'], connector=self.connector)
            return return_obj
        except Exception as err:
            self.logger.error('error when pinging datasource {}:'.format(err))
            raise

    def create_results_connection(self, query_expr, offset, length):
        payload = json.loads(query_expr)
        if payload['source'] == 'events':
            return self.get_events(payload, offset, length)
        else:
            return self.get_processes(payload, offset, length)

    def get_events(self, query_expr, offset, length):
        length = int(length)
        offset = int(offset)

        # total records is the sum of the offset and length(limit) value
        total_records = offset + length
        try:
            # Separate out api supported url params
            query_expr, filter_attr = Connector.modify_query_expr(query_expr['query'])
            # Grab the response, extract the response code, and convert it to readable json
            response_dict = self.api_client.get_search_results(query_expr)
            event_list = []
            return_obj = dict()
            if response_dict["code"] == 200:
                response = response_dict["data"]["events"]
                response_list = response
                page = 1
                while len(response) == 1000 and total_records > len(response_list):
                    response = self.api_client.get_search_results(query_expr, page=page)
                    response = response["data"]["events"]
                    response_list = response_list + response
                    page = page + 1
                # Construct a response object
                for event in response_list:
                    json_string = json.dumps(event.__dict__, default=str)
                    event_list.append(json.loads(json_string)["_data_store"])
                return_obj['success'] = True
                return_obj['data'] = event_list
                # filter data based on filter_attr
                return_obj = Connector.filter_response(return_obj, filter_attr)
                # slice the records as per the provided offset and length(limit)
                return_obj['data'] = return_obj['data'][offset:total_records]
            else:
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
            return return_obj
        except Exception as err:
            self.logger.error('error when getting search results: {}'.format(err))
            import traceback
            self.logger.error(traceback.print_stack())
            raise

    def get_processes(self, query_expr, offset, length):
        length = int(length)
        offset = int(offset)

        # total records is the sum of the offset and length(limit) value
        total_records = offset + length
        try:
            # Separate out api supported url params
            query_expr, filter_attr = Connector.modify_query_expr(query_expr['query'])
            # Grab the response, extract the response code, and convert it to readable json
            response_dict = self.api_client.get_processes_results()
            process_list = []
            return_obj = dict()
            if response_dict["code"] == 200:
                response = response_dict["data"]["data"]
                response_list = response
                page = 1
                while len(response) == 1000 and total_records > len(response_list):
                    response = self.api_client.get_processes_results()
                    response = response["data"]["data"]
                    response_list = response_list + response
                    page = page + 1
                # Construct a response object
                for process in response_list:
                    json_string = json.dumps(process['attributes'].__dict__, default=str)
                    process_list.append(json.loads(json_string)["_data_store"])
                return_obj['success'] = True
                return_obj['data'] = process_list
                # filter data based on filter_attr
                return_obj = Connector.filter_response(return_obj, filter_attr)
                # slice the records as per the provided offset and length(limit)
                return_obj['data'] = return_obj['data'][offset:total_records]
            else:
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
            return return_obj
        except Exception as err:
            self.logger.error('error when getting processes results: {}'.format(err))
            import traceback
            self.logger.error(traceback.print_stack())
            raise

    @staticmethod
    def filter_response(response_dict, filter_attr):
        try:
            for attr in filter_attr:
                response_dict['data'] = list(
                    filter(lambda person: person[attr] in filter_attr[attr] if isinstance(filter_attr[attr], list) else
                    person[attr] == filter_attr[attr], response_dict['data']))
        except KeyError as ex:
            raise KeyError(f"Invalid parameter {ex}")
        return response_dict

    @staticmethod
    def modify_query_expr(query_expr):
        valid_filter_attributes = ["start", "end", "priority", "source", "tags", "unaggregated", "page"]
        filter_attr = dict()
        api_query_attr = dict()
        for attribute in query_expr:
            if attribute in valid_filter_attributes:
                if attribute == "unaggregated":
                    query_expr[attribute] = True if query_expr[attribute].lower() == "true" else False
                api_query_attr.update({attribute: query_expr[attribute]})
            else:
                value = query_expr[attribute].split(",") if isinstance(query_expr[attribute], str) else query_expr[attribute]
                filter_attr.update({attribute: value})
        return api_query_attr, filter_attr
