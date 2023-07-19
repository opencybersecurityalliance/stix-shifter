from stix_shifter_utils.modules.base.stix_transmission.base_json_sync_connector import BaseJsonSyncConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
from .api_client import APIClient
import json


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

    async def create_results_connection(self, query, offset, length):
        """
         Function to create query connection
        :param query: str
        :param offset: int
        :param length: str
        :return: list
        """
        response_dict = {}
        return_obj = {}
        data = []
        try:
            offset = int(offset)
            length = int(length)
            pagination_offset = offset
            total_records = length
            page = 1

            # changing offset to page number
            if offset > length:
                pagination_offset = offset % length
                if pagination_offset < 5:
                    page = round(offset / length) + 1
                else:
                    page = round(offset / length)

            # set total record count
            if self.api_client.result_limit < total_records:
                total_records = self.api_client.result_limit

            # set page size
            if total_records <= Connector.VECTRA_MAX_PAGE_SIZE:
                page_size = total_records
            else:
                page_size = Connector.VECTRA_MAX_PAGE_SIZE

            query = f"page_size={page_size}&{query}&page={page}"
            response_wrapper = await self.api_client.get_search_results(query)
            response_code = response_wrapper.code
            response = json.loads(response_wrapper.read().decode('utf-8'))

            if response_code == 200:
                data += response['results']
                next_url = response.get('next')
                while next_url:
                    if len(data) >= total_records:
                        break
                    next_url = next_url.split('/api/v2.4/search/detections/?')
                    query = next_url[1]
                    next_response_wrapper = await self.api_client.get_search_results(query)
                    response_code = next_response_wrapper.code
                    next_response = json.loads(next_response_wrapper.read().decode('utf-8'))
                    next_url = next_response.get('next')
                    if response_code == 200:
                        data += next_response['results']
                    else:
                        response = next_response
                        break

                if response_code == 200:
                    return_obj['success'] = True
                    return_obj['data'] = self.get_results_data(data[pagination_offset:total_records])

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
