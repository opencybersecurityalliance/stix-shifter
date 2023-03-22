from stix_shifter_utils.modules.base.stix_transmission.base_json_sync_connector import BaseJsonSyncConnector
from .api_client import APIClient
import json
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger

DEFAULT_MAX_RESULTS_WINDOW_SIZE = 10000

class UnexpectedResponseException(Exception):
    pass


class Connector(BaseJsonSyncConnector):
    def __init__(self, connection, configuration):
        self.api_client = APIClient(connection, configuration)
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]
        self.max_result_window = None

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

    async def ping_connection(self):
        response_txt = None
        return_obj = dict()
        try:
            # test the pit
            #print(self.set_point_in_time())
            response = await self.api_client.ping_box()
            return self._handle_errors(response, return_obj)
        except Exception as e:
            if response_txt is not None:
                ErrorResponder.fill_error(return_obj, message='unexpected exception', connector=self.connector)
                self.logger.error('can not parse response: ' + str(response_txt))
            else:
                raise e

    async def get_pagesize(self, default_window_size):
        return_obj = dict()

        try:
            response = await self.api_client.get_max_result_window()
            return_obj = self._handle_errors(response, return_obj)
        except Exception:
            max_result_window = default_window_size
        else:
            if (return_obj['success']):
                response_json = json.loads(return_obj["data"])
                max_result_windows = []
                if response_json:
                    for index, item_json in response_json.items():
                        if 'index' in item_json['settings'] and 'max_result_window' in item_json['settings']['index']:
                            max_res_win = item_json['settings']['index']['max_result_window']
                        elif 'index' in item_json['defaults'] and 'max_result_window' in item_json['defaults']['index']:
                            max_res_win = item_json['defaults']['index']['max_result_window']
                        else:
                            ErrorResponder.fill_error(item_json,
                                                      message='max_result_window is not set in index: ' + str(index),
                                                      connector=self.connector)
                            self.logger.error('max_result_window is not set in index: ' + str(index))
                        max_result_windows.append(int(max_res_win))

                # return the smallest max_return_window in indices
                max_result_window = sorted(max_result_windows)[0] if max_result_windows else default_window_size

            else:  # land here if API call failed, e.g., no priviledge
                max_result_window = default_window_size

        return max_result_window

    async def create_results_connection(self, query, offset, length, metadata=None):
        response_txt = None
        return_obj = dict()

        try:
            # extract the max_result_window from elasticsearch
            if not self.max_result_window:
                self.max_result_window = await self.get_pagesize(DEFAULT_MAX_RESULTS_WINDOW_SIZE)
            # using search after API in ElasticSearch
            # pass the last searched value in metadata argument, ignore offset argument
            response = await self.api_client.search_pagination(query, metadata, min(int(length), self.max_result_window))
            return_obj = self._handle_errors(response, return_obj)

            if (return_obj['success']):
                response_json = json.loads(return_obj["data"])
                if response_json['hits']:
                    # and (response_json['hits']['total']['value'] >= 0 or response_json['hits']['total'] >= 0):
                    self.logger.error("Total # of hits:" + str(response_json['hits']['total']))
                    return_obj['data'] = [record['_source'] for record in response_json["hits"]["hits"]]
                    self.logger.error("Total # of records: " + str(len(return_obj['data'])))
                    if len(response_json["hits"]["hits"]) == 0:
                        return_obj['metadata'] = metadata
                    elif 'sort' in response_json["hits"]["hits"][-1]:
                        return_obj['metadata'] = response_json["hits"]["hits"][-1]['sort']
            return return_obj
        except Exception as e:
            if response_txt is not None:
                ErrorResponder.fill_error(return_obj, message='unexpected exception', connector=self.connector)
                self.logger.error('can not parse response: ' + str(response_txt))
            else:
                raise e

    async def set_point_in_time(self):
        response_txt = None
        return_obj = dict()
        try:
            response = await self.api_client.set_pit()
            return self._handle_errors(response, return_obj)
        except Exception as e:
            if response_txt is not None:
                ErrorResponder.fill_error(return_obj, message='unexpected exception', connector=self.connector)
                self.logger.error('can not parse response: ' + str(response_txt))
            else:
                raise e
