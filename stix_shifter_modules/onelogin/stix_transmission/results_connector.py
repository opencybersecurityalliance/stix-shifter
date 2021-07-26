import json

from stix_shifter_utils.modules.base.stix_transmission.base_results_connector import BaseResultsConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger


class ResultsConnector(BaseResultsConnector):
    max_limit = 50

    def __init__(self, api_client):
        self.init_error = None
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.token_resp = self.get_token()
        if self.token_resp["code"] == 200:
            self.access_token = self.token_resp["access_token"]
        else:
            self.init_error = self.token_resp

    def create_results_connection(self, quary_expr, offset, length):
        length = int(length)
        offset = int(offset)

        # total records is the sum of the offset and length(limit) value
        total_records = offset + length
        try:
            if self.init_error:
                self.logger.error(f"Token Generation Failed: {self.init_error}")
                return self.init_error
            # Separate out api supported url params
            quary_expr, filter_attr = ResultsConnector.modify_query_expr(quary_expr)
            # Grab the response, extract the response code, and convert it to readable json
            if length <= self.max_limit:
                # $(offset) param not included as data source not support this
                response_dict = self.api_client.run_search(quary_expr, total_records, self.access_token)
            else:
                response_dict = self.api_client.run_search(quary_expr, self.max_limit, self.access_token)
            response_code = response_dict.code
            # Construct a response object
            response_dict = json.loads(response_dict.read())
            return_obj = dict()
            if response_code == 200:
                return_obj['success'] = True
                return_obj['data'] = response_dict['data']
                next_page_link = response_dict['pagination']['next_link']
                filter_flag = True
                while len(return_obj['data']) < total_records and next_page_link:
                    try:
                        response = self.api_client.next_page_run_search(next_page_link)
                        response_code = response.code
                        response_dict = json.loads(response.read())
                        if response_code == 200:
                            if filter_attr:
                                filter_flag = False
                                # filter data based on filter-attributes
                                response_dict = ResultsConnector.filter_response(response_dict, filter_attr)
                            return_obj['data'].extend(response_dict['data'])
                        else:
                            ErrorResponder.fill_error(return_obj, response_dict, ['status', 'message', 'description'])
                    except KeyError:
                        break
                # filter data if not filtered in above while loop
                if filter_flag:
                    return_obj = ResultsConnector.filter_response(return_obj, filter_attr)
                # slice the records as per the provided offset and length(limit)
                return_obj['data'] = return_obj['data'][offset:total_records]

            else:
                ErrorResponder.fill_error(return_obj, response_dict, ['status', 'message', 'description'])
            return return_obj
        except Exception as err:
            self.logger.error('error when getting search results: {}'.format(err))
            import traceback
            self.logger.error(traceback.print_stack())
            raise

    def get_token(self):
        return_obj = dict()
        try:
            response_dict = self.api_client.generate_token()
            response_code = response_dict.code
            response_dict = json.loads(response_dict.read())
            return_obj["code"] = response_code
            return_obj["access_token"] = response_dict["access_token"]
        except Exception as e:
            ErrorResponder.fill_error(return_obj, response_dict, ['status', 'message', 'description'])
            self.logger.error('Error while generating access token: {}'.format(e))
        return return_obj

    @staticmethod
    def modify_query_expr(quary_expr):
        valid_filter_attributes = ["client_id", "directory_id", "created_at", "id", "until", "event_type_id", "limit",
                                  "since", "resolution", "user_id"]
        api_quary_attr = []
        filter_attr = []
        quary_expr_list = quary_expr.split("&")
        for attribute in quary_expr_list:
            if attribute.split("=")[0] in valid_filter_attributes:
                api_quary_attr.append(attribute)
            else:
                filter_attr.append(attribute)
        quary_expr = '&'.join(api_quary_attr)
        return quary_expr, filter_attr

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

