from stix_shifter_utils.modules.base.stix_transmission.base_json_sync_connector import BaseJsonSyncConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
from .api_client import APIClient
import json
import re


class InvalidMetadataException(Exception):
    pass


class Connector(BaseJsonSyncConnector):
    VECTRA_MAX_PAGE_SIZE = 5000

    def __init__(self, connection, configuration):
        self.api_client = APIClient(connection, configuration)
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    async def ping_connection(self):
        return_obj = {}
        response_dict = {}
        try:
            response_wrapper = await self.api_client.ping_data_source()
            response_code = response_wrapper.code
            if response_code == 200:
                return_obj['success'] = True
            elif response_code in (401, 403):
                response_dict['code'] = response_code
                response_dict['message'] = "Invalid Authentication"
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        except Exception as ex:
            if "timeout_error" in str(ex):
                response_dict['code'] = 408
            response_dict['message'] = str(ex)
            self.logger.error('error when getting search results: %s', str(ex))
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj

    async def create_results_connection(self, query, offset, length, metadata=None):
        """
         Function to create query connection
        :param query: str
        :param offset: int
        :param length: str
        :param metadata: dict
        :return: list
        """
        response_dict = {}
        return_obj = {}
        data = []
        local_result_count = 0
        try:
            if metadata:
                if isinstance(metadata, dict) and metadata.get('result_count') and metadata.get('next_page_url'):
                    result_count, next_page_url = metadata['result_count'], metadata['next_page_url']
                    result_count = int(result_count)
                    total_records = int(length)
                    if abs(self.api_client.result_limit - result_count) < total_records:
                        total_records = abs(self.api_client.result_limit - result_count)

                else:
                    # raise exception when metadata doesnt contain result count or next page token
                    raise InvalidMetadataException(metadata)
            else:
                result_count, next_page_url = 0, None
                total_records = int(offset) + int(length)
                if self.api_client.result_limit < total_records:
                    total_records = self.api_client.result_limit
            if total_records <= Connector.VECTRA_MAX_PAGE_SIZE:
                page_size = total_records
            else:
                page_size = Connector.VECTRA_MAX_PAGE_SIZE

            if (result_count == 0 and next_page_url is None) or (next_page_url and result_count <
                                                                 self.api_client.result_limit):
                if next_page_url:
                    response_wrapper = await self.api_client.get_search_results(next_page_url)
                else:
                    query = f"page_size={page_size}&{query}&page=1"
                    response_wrapper = await self.api_client.get_search_results(query)
                response_dict = json.loads(response_wrapper.read().decode('utf-8'))
                response_code = response_wrapper.code
                response = response_dict
                if response_wrapper.code == 200:
                    return_obj['success'] = True
                    data += response_dict['results']
                    result_count += len(response_dict['results'])
                    local_result_count += len(response_dict['results'])
                    next_url = response_dict.get('next')
                    # loop until if there is next page link and records fetched is less than total records
                    while next_url:
                        if not metadata and result_count < total_records:
                            remaining_records = total_records - result_count
                        elif metadata and local_result_count < total_records:
                            remaining_records = total_records - local_result_count
                        else:
                            break

                        if remaining_records > Connector.VECTRA_MAX_PAGE_SIZE:
                            page_size = Connector.VECTRA_MAX_PAGE_SIZE
                        else:
                            page_size = remaining_records
                        next_url = re.sub(r'page_size=([^>]*?)&', f'page_size={page_size}&', next_url)
                        next_response_wrapper = await self.api_client.get_search_results(next_url)
                        next_response = json.loads(next_response_wrapper.read().decode('utf-8'))
                        response_code = next_response_wrapper.code
                        response = next_response
                        if next_response_wrapper.code == 200:
                            data += next_response['results']
                            next_url = response_dict.get('next')
                            result_count += len(next_response['results'])
                            local_result_count += len(next_response['results'])
                        else:
                            data = []
                            break
                    if data:
                        final_result = self.get_results_data(data)
                        if metadata:
                            return_obj['data'] = final_result if final_result else []
                        else:
                            return_obj['data'] = final_result[int(offset): total_records] if final_result else []
                        if next_url and result_count < self.api_client.result_limit:
                            return_obj['metadata'] = {"result_count": result_count,
                                                      "next_page_url": next_url}
                    else:
                        if not return_obj.get('error') and return_obj.get('success') is not False:
                            return_obj['success'] = True
                            return_obj['data'] = []
            else:
                return_obj['success'] = True
                return_obj['data'] = []

            # handling error response
            if response_code == 200:
                pass
            elif response_code in (422, 406):
                if 'page_size' in str(response) or 'invalid params' in str(response):
                    response_dict['code'] = response_code
                    response_dict['message'] = "Invalid Parameters"
                else:
                    response_dict['code'] = 421
                    response_dict['message'] = "Invalid Query"
                    if 'Query too long' in str(response):
                        response_dict['message'] += "- Query length is too long"
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
            elif response_code in (401, 403):
                response_dict['code'] = response_code
                response_dict['message'] = "Invalid Authentication"
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
            else:
                response_dict['message'] = str(response)
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except InvalidMetadataException as ex:
            response_dict['code'] = 422
            response_dict['message'] = f'Invalid metadata: {str(ex)}'
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except Exception as ex:
            if "timeout_error" in str(ex):
                response_dict['code'] = 408
            response_dict['message'] = str(ex)
            self.logger.error('error when getting search results: %s', str(ex))
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj

    def set_default_protocol(self, item):
        """
         Adds the default value for protocol if it doesn't exist in record.
        :param item: dict/list
        :return: None
        """
        if isinstance(item, list):
            for list_item in item:
                self.set_default_protocol(list_item)
        elif not (item.get('protocol') or item.get("app_protocol") or item.get("dst_protocol")):
            item['protocol'] = "tcp"

    @staticmethod
    def is_extensible(record) -> bool:
        """
         Checks whether the record is extensible for preprocessing.
        :param record: dict
        :return: bool
        """
        if record.get('detection_type') == 'Suspicious LDAP Query':
            return False
        if record.get('detection_type') in ('RPC Recon', 'Kerberoasting: SPN Sweep'):
            return True
        if len(record.get('grouped_details', [])) and \
            (record['grouped_details'][0].get('events') or
             record['grouped_details'][0].get('sessions') or
             record['grouped_details'][0].get('connection_events')):
            return True
        return False

    @staticmethod
    def set_destination_ip(item):
        """ set destination ip in each events.
        :param item: dict
        :return: dict """
        dest_ip = item.get('dst_ips')
        if isinstance(dest_ip, str):
            item['dest_ip'] = [dest_ip]

        if isinstance(dest_ip, list) and len(dest_ip):
            for index, value in enumerate(item['events']):
                if len(dest_ip)-1 >= index:
                    value['dst_ips'] = dest_ip[index]
                else:
                    value['dst_ips'] = dest_ip[0]
        return item

    def get_results_data(self, response_dict):
        """
         Preprocessing the response based on detection type
        :param response_dict: list
        :return: list
        """
        for record in response_dict:

            detection_type = record.get('detection_type', '')

            # if x-ibm-finding object event_count is not available, setting the default value to 1.
            # if default value is not set, CP4S inserts NaN value for event_count which causes rendering issue in UI.
            if record.get('summary') and \
                    'num_attempts' not in record['summary'] and 'num_sessions' not in record['summary']:
                record['summary']['num_sessions'] = 1

            if 'Privilege' in detection_type:
                # Skip any preprocessing for these detections.
                continue

            grouped_details = record.get('grouped_details', [])
            if detection_type in ('New Host Role', 'New Host'):
                # INFO detection category has a different stix translation mapping than grouped_details.
                record['grouped_details_info'] = record.pop('grouped_details')
                continue

            if self.is_extensible(record):
                # grouped_details_ex has a different stix translation mapping than grouped_details.
                record['grouped_details_ex'] = record.pop('grouped_details')
                grouped_details = record['grouped_details_ex']

            # set default protocol
            for group in grouped_details:
                item = group
                if record.get('grouped_details_ex'):
                    if group.get('events'):
                        if detection_type == 'Data Smuggler':
                            group = self.set_destination_ip(group)
                        item = group.get('events')
                    elif group.get('sessions'):
                        item = group.get('sessions')
                    elif group.get('connection_events'):
                        item = group.get('connection_events')
                    elif group.get('dst_hosts'):
                        item = group.get('dst_hosts')
                self.set_default_protocol(item)
        return response_dict
