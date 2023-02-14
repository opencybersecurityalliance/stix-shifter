from stix_shifter_utils.modules.base.stix_transmission.base_sync_connector import BaseSyncConnector
from .api_client import APIClient
import json
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger


class UnexpectedResponseException(Exception):
    pass


class Connector(BaseSyncConnector):
    def __init__(self, connection, configuration):
        self.api_client = APIClient(connection, configuration)
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]
        self.max_result_window = 10000
        # extract the max_result_window from elasticsearch
        try:
            self.get_pagesize()
        except Exception as e:
            pass

    def _handle_errors(self, response, return_obj):
        response_code = response.code
        response_txt = response.read().decode('utf-8')

        if 200 <= response_code < 300:
            return_obj['success'] = True
            return_obj['data'] = response_txt
        elif ErrorResponder.is_plain_string(response_txt):
            ErrorResponder.fill_error(return_obj, message=response_txt, connector=self.connector)
        elif ErrorResponder.is_json_string(response_txt):
            response_json = json.loads(response_txt)
            ErrorResponder.fill_error(return_obj, response_json, ['reason'], connector=self.connector)
        else:
            raise UnexpectedResponseException
        return return_obj

    def ping_connection(self):
        response_txt = None
        return_obj = dict()
        try:
            # test the pit
            #print(self.set_point_in_time())
            response = self.api_client.ping_box()
            return self._handle_errors(response, return_obj)
        except Exception as e:
            if response_txt is not None:
                ErrorResponder.fill_error(return_obj, message='unexpected exception', connector=self.connector)
                self.logger.error('can not parse response: ' + str(response_txt))
            else:
                raise e

    def get_pagesize(self):
        response_txt = None
        return_obj = dict()
        try:
            response = self.api_client.get_max_result_window()
            return_obj = self._handle_errors(response, return_obj)
            if (return_obj['success']):
                response_json = json.loads(return_obj["data"])
                max_result_windows = set()
                if not (response_json is None):
                    for _, item_json in response_json.items():
                        max_res_win = item_json['defaults']['index']['max_result_window']
                        max_result_windows.add(max_res_win)
                if len(max_result_windows) != 1:
                    ErrorResponder.fill_error(max_result_windows, message='inconsistent max_result_window settings', connector=self.connector)
                    self.logger.error('inconsistent max_result_window settings: ' + str(max_result_windows))
                self.max_result_window = int(max_result_windows.pop())
                return self.max_result_window
        except Exception as e:
            if response_txt is not None:
                ErrorResponder.fill_error(return_obj, message='unexpected exception', connector=self.connector)
                self.logger.error('can not parse response: ' + str(response_txt))
            else:
                raise e

    def create_results_connection(self, query, offset, length, metadata=None):
        response_txt = None
        return_obj = dict()

        try:
            # using search after API in ElasticSearch
            # pass the last searched value in metadata argument, ignore offset argument
            response = self.api_client.search_pagination(query, metadata, min(length, self.max_result_window))
            return_obj = self._handle_errors(response, return_obj)

            if (return_obj['success']):
                response_json = json.loads(return_obj["data"])
                if response_json['hits']:
                    # and (response_json['hits']['total']['value'] >= 0 or response_json['hits']['total'] >= 0):
                    self.logger.error("Total # of hits:" + str(response_json['hits']['total']))
                    return_obj['data'] = [record['_source'] for record in response_json["hits"]["hits"]]
                    self.logger.error("Total # of records: " + str(len(return_obj['data'])))
                    if len(response_json["hits"]["hits"]) == 0:
                        return_obj['lastsort'] = metadata
                    elif 'sort' in response_json["hits"]["hits"][-1]:
                        return_obj['lastsort'] = response_json["hits"]["hits"][-1]['sort']
            return return_obj
        except Exception as e:
            if response_txt is not None:
                ErrorResponder.fill_error(return_obj, message='unexpected exception', connector=self.connector)
                self.logger.error('can not parse response: ' + str(response_txt))
            else:
                raise e



    def set_point_in_time(self):
        response_txt = None
        return_obj = dict()
        try:
            response = self.api_client.set_pit()
            return self._handle_errors(response, return_obj)
        except Exception as e:
            if response_txt is not None:
                ErrorResponder.fill_error(return_obj, message='unexpected exception', connector=self.connector)
                self.logger.error('can not parse response: ' + str(response_txt))
            else:
                raise e
