import re
import json
from flatten_json import unflatten
from stix_shifter_utils.modules.base.stix_transmission.base_json_sync_connector import BaseJsonSyncConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
from .api_client import APIClient


# LogScale event fields starts with @timestamp and @error_msg will be overwritten while un-flattening.
# These fields are excluded while un flattening
DS_FLATTEN_KEY_EXCLUDE = ["@timestamp", "@error_msg"]


class Connector(BaseJsonSyncConnector):

    def __init__(self, connection, configuration):
        self.api_client = APIClient(connection, configuration)
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    async def ping_connection(self):
        """
        Ping the endpoint
        :return: return_object, dict
        """
        return_obj = {}
        response_dict = {}
        try:
            response = await self.api_client.ping_data_source()
            response_code = response.code
            response_str = response.read().decode('utf-8')
            if response_code == 200:
                return_obj['success'] = True
            else:
                return_obj = self.exception_response(response_code, response_str)

        except Exception as ex:
            if "timeout_error" in str(ex):
                response_dict['code'] = 408
            response_dict['message'] = str(ex)
            self.logger.error('error while pinging: %s', ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj

    async def create_results_connection(self, query, offset, length, metadata=None):
        """
        Fetching the results using query, offset and length
        :param query: str, Data Source query
        :param offset: str, Offset value
        :param length: str, Length value
        :param metadata: dict
        :return: return_obj, dict
        """
        return_obj = {}
        data = []
        response_dict = {}
        offset = int(offset)
        length = int(length)
        try:
            if isinstance(query, str):
                query = json.loads(query)
            source = query.get('source')

            response_wrapper = await self.api_client.get_search_results(json.dumps(query))
            response = response_wrapper.read().decode('utf-8')
            if response_wrapper.code == 200:
                return_obj['success'] = True
                data += json.loads(response)
            else:
                return_obj = self.exception_response(response_wrapper.code, response)
                data = []

            if data:
                # LogScale response is not in sorted order, sorting events based on @timestamp
                data = sorted(data, key=lambda event: event['@timestamp'], reverse=True)
                data = [{source: self.unflatten_json(event)} for event in data[offset: (offset + length)]]
                return_obj['data'] = data
            else:
                if not return_obj.get('error') and return_obj.get('success') is not False:
                    return_obj['success'] = True
                    return_obj['data'] = []

        except json.decoder.JSONDecodeError as ex:
            response_dict['code'] = 100
            response_dict['message'] = str(ex)
            self.logger.error('error while fetching results: %s', ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except Exception as ex:
            if "timeout_error" in str(ex):
                response_dict['code'] = 408
            response_dict['message'] = str(ex)
            self.logger.error('error while fetching results: %s', ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj

    def exception_response(self, code, response_txt):
        """
        create the exception response
        :param code, int
        :param response_txt, dict
        :return: return_obj, dict
        """
        return_obj = {}
        response_dict = {'code': code, 'message': str(response_txt)}
        ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj

    def unflatten_json(self, flatten_json):
        """
        Unflatten the flattened JSON event
        :param flatten_json: dict
        :return res,dict
        """
        res = {}
        # Excluded flatten keys
        excluded_keys = [key for key in flatten_json if key.startswith(tuple(DS_FLATTEN_KEY_EXCLUDE))]

        # copy excluded items to res and remove from flatten_json
        for key in excluded_keys:
            res[key] = flatten_json.pop(key)

        unflatten_json = unflatten(flatten_json, separator='.')
        # Format array indexed keys to proper json format
        unflatten_json = self.format_indexed_keys(unflatten_json)
        res = res | unflatten_json
        res['finding_type'] = 'alert'
        return res

    def format_indexed_keys(self, event):
        """
        Format array indexed string keys to single key
        :param event: dict
        :return res,dict
        """
        res = {}
        for key, value in event.items():
            match = re.search(r'(.*)\[(\d)\]$', key)
            if match:
                indexed_key, _ = match.groups()
                val = res.get(indexed_key, {}) or []
                if isinstance(value, dict):
                    response = self.format_indexed_keys(value)
                    val.append(response)
                else:
                    val.append(value)
                res[indexed_key] = val
            else:
                if isinstance(value, dict):
                    value = self.format_indexed_keys(value)
                res[key] = value
        return res
