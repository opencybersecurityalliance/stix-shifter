import copy
from stix_shifter_utils.modules.base.stix_transmission.base_json_results_connector import BaseJsonResultsConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
import json

TRELLIX_PER_HOST_LIMIT = 20


class InvalidMetadataException(Exception):
    pass


class ResultsConnector(BaseJsonResultsConnector):
    last_host_record_count = 0

    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    async def create_results_connection(self, search_id, offset, length, metadata=None):
        """
        Fetching the results of the search id using offset and length
        :param search_id: str
        :param offset: str
        :param length: str
        :param metadata: dict
        :return: return_obj, dict
        """

        return_obj = {}
        try:
            data = []
            offset = int(offset)
            length = int(length)
            host_offset = host_length = -1

            token_obj = await self.__get_token()
            if token_obj:
                return token_obj
            input_search_id = search_id.split(":")[0]
            host_set = search_id.split(":")[1]

            current_host_offset, host_index, total_records = await self.fetch_host_details(offset, length, metadata)

            while len(data) < total_records:
                host_offset, host_length = ResultsConnector.calculate_host_offset_length(current_host_offset,
                                                                                         total_records, data,
                                                                                         host_offset, host_length,
                                                                                         metadata)
                response_code, response_content = await self.make_api_call(input_search_id, host_offset, host_length)
                if response_code == 200:
                    records = ResultsConnector.fetch_records(response_content, host_index, host_set)
                    if not records:
                        host_offset = None
                        break
                    data += records
                    host_index = 0
                else:
                    return_obj = self.handle_api_exception(response_code, response_content)
                    if return_obj.get('status'):
                        token_obj = await self.__get_token()
                        if token_obj:
                            return token_obj
                        continue
                    break
            if data:
                return_obj = self.prepare_data_and_metadata(data, total_records, offset, host_offset, host_length,
                                                            metadata)
            else:
                if not return_obj.get('success') and not return_obj.get('error'):
                    return_obj['success'] = True
                    return_obj['data'] = []
            # stop the searches on the host set.
            if return_obj.get('data') and ((len(return_obj['data']) < total_records and metadata) or
                                           (not metadata and len(return_obj['data']) < (total_records - offset))):
                await self.api_client.stop_search(input_search_id)
            # delete the token to end the session
            await self.api_client.delete_token()

        except InvalidMetadataException:
            return_obj = self.handle_api_exception(100, "Invalid Metadata")

        except Exception as err:
            response_dict = {'message': str(err)}
            if "timeout_error" in str(err):
                response_dict['code'] = 408
            self.logger.error('error while getting results in Trellix Endpoint Security HX: %s', err)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj

    def prepare_data_and_metadata(self, data, total_records, offset, host_offset, host_length, metadata):
        """
        Apply Offset and length in data, and create metadata
        :param data: list
        :param total_records: int
        :param offset: int
        :param host_offset: int
        :param host_length: int
        :param metadata: dict
        :return: dict
        """
        return_obj = {'success': True}
        if len(data) > total_records:
            additional_records = len(data) - total_records
            data = data[:-additional_records]  # Remove the additional records from the data
            # calculate the next index of the last host set to be used in next iteration
            index = (ResultsConnector.last_host_record_count - additional_records) + 1
        else:
            index = 0

        if metadata:
            return_obj['data'] = data
        else:
            return_obj['data'] = data[offset:total_records]
        if offset + len(return_obj['data']) < self.api_client.result_limit and host_offset is not None:
            new_offset = (host_offset + host_length) if index == 0 else (host_offset + host_length) - 1
            return_obj['metadata'] = {'host_offset': new_offset,
                                      'host_record_index': index
                                      }

        return return_obj

    async def fetch_host_details(self, offset, length, metadata):
        """
        Calculate host index, host offset, total records
        :param offset: int
        :param length: int
        :param metadata: dict
        :return: int
        """
        if metadata:
            if (isinstance(metadata, dict) and 'host_record_index' in metadata.keys()
                    and 'host_offset' in metadata.keys()):
                current_host_offset, host_index = metadata['host_offset'], metadata['host_record_index']
                total_records = length
                records_fetched = offset
                if abs(self.api_client.result_limit - records_fetched) < total_records:
                    total_records = abs(self.api_client.result_limit - records_fetched)
            else:
                raise InvalidMetadataException(f'Invalid Metadata{metadata}')
        else:
            current_host_offset = -1
            host_index = 0
            total_records = offset + length
            if self.api_client.result_limit < total_records:
                total_records = self.api_client.result_limit
        return current_host_offset, host_index, total_records

    @staticmethod
    def calculate_host_offset_length(current_host_offset, total_records, data, host_offset, host_length, metadata):
        """
        Calculate the host offset and length for the API
        :param current_host_offset: int
        :param total_records: int
        :param data: list
        :param host_offset: int
        :param host_length: int
        :param metadata: dict
        :return: int
        """
        if not data:
            records_to_be_fetched = total_records
            if metadata:
                host_offset = current_host_offset
            else:
                host_offset = 0
        else:
            records_to_be_fetched = total_records - len(data)
            host_offset = host_offset + host_length

        if records_to_be_fetched % TRELLIX_PER_HOST_LIMIT == 0:
            host_length = records_to_be_fetched // TRELLIX_PER_HOST_LIMIT
        elif records_to_be_fetched % TRELLIX_PER_HOST_LIMIT > 0:
            host_length = (records_to_be_fetched // TRELLIX_PER_HOST_LIMIT) + 1

        return host_offset, host_length

    async def __get_token(self):
        """
        Generate a new Fireeye API token
        :return: dict
        """
        return_obj = {}
        response = await self.api_client.generate_token()
        if response.code == 204 and response.headers.get('X-FeApi-Token'):
            self.api_client.headers['X-FeApi-Token'] = response.headers['X-FeApi-Token']
            if self.api_client.headers.get('Authorization'):
                self.api_client.headers.pop('Authorization')
        else:
            return_obj = self.handle_api_exception(response.code, response.read().decode('utf-8'))
        return return_obj

    async def make_api_call(self, search_id, host_offset, host_length):
        """
        Perform the API call and read the response
        :param search_id: str
        :param host_offset: int
        :param host_length: int
        :return: int, str
        """
        response = await self.api_client.get_search_results(search_id, host_offset, host_length)
        response_code = response.code
        response_content = response.read().decode('utf-8')
        return response_code, response_content

    @staticmethod
    def fetch_records(response_content, host_index, host_set):
        """
        Format the results and slice the records based on the host offset
        :param response_content: str
        :param host_index: int
        :param host_set: str
        :return: list
        """
        data = json.loads(response_content)
        if host_index:
            formatted_data = ResultsConnector.format_results(data, host_set)[(host_index - 1):]
        else:
            formatted_data = ResultsConnector.format_results(data, host_set)

        return formatted_data

    @staticmethod
    def format_results(response_data, host_set):
        """
        Formats the response
        :param response_data: dict
        :param host_set : str
        :return:  list
        """
        data = []
        if response_data.get('data') and response_data['data'].get('total', 0) > 0:
            if response_data['data'].get('entries'):
                for record in response_data['data']['entries']:
                    if record.get('host') and record.get('results'):
                        host_id = record['host']['_id']
                        host_name = record['host']['hostname']
                        for event in record['results']:
                            temp_event = copy.deepcopy(event['data'])
                            temp_event['Host ID'] = host_id
                            temp_event['Hostname'] = host_name
                            temp_event['Event Type'] = event['type']
                            temp_event['Host Set'] = host_set
                            temp_event = ResultsConnector.format_events(temp_event)
                            if not temp_event.get('Timestamp - Modified'):
                                temp_event['Timestamp - Modified'] = temp_event['Timestamp - Event']
                            data.append(temp_event)
                if data:
                    # Fetch the record count of the last host
                    total_host = len(response_data['data']['entries'])
                    ResultsConnector.last_host_record_count = len(response_data['data']['entries'][total_host - 1]
                                                                  ['results'])
        return data

    @staticmethod
    def format_events(temp_event):
        """
        Format the events
        :param temp_event:
        :return: dict
        """
        if temp_event.get("Registry Key Value Name"):
            temp_event = ResultsConnector.format_registry(temp_event)
        if 'network' in temp_event['Event Type'].lower():
            temp_event['Port Protocol'] = 'ipv4' if 'IPv4' in temp_event['Event Type'] else 'ipv6'
        if temp_event.get('HTTP Header'):
            temp_event = ResultsConnector.format_http_header(temp_event)
            temp_event['Port Protocol'] = 'http'
        if temp_event.get('File Text Written'):
            temp_event = ResultsConnector.format_file(temp_event)
        if temp_event.get('Process Name') and not temp_event.get('File Name'):
            temp_event = ResultsConnector.format_process(temp_event)

        return temp_event

    @staticmethod
    def format_file(temp_event):
        """
        Add file name for binary references if file not found
        :param temp_event:
        :return: dict
        """
        if temp_event.get('File Name'):
            temp_event['Write Event File Name'] = temp_event['File Name']
            temp_event.pop('File Name')
        if temp_event.get('File Full Path'):
            temp_event['Write Event File Full Path'] = temp_event['File Full Path']
            temp_event.pop('File Full Path')
        if temp_event.get('File Text Written'):
            temp_event['Write Event File Text Written'] = temp_event['File Text Written']
            temp_event.pop('File Text Written')
        if temp_event.get('File Bytes Written'):
            temp_event['Write Event File Bytes Written'] = temp_event['File Bytes Written']
            temp_event.pop('File Bytes Written')
        if temp_event.get('File MD5 Hash'):
            temp_event['Write Event File MD5 Hash'] = temp_event['File MD5 Hash']
            temp_event.pop('File MD5 Hash')
        if temp_event.get('Size in bytes'):
            temp_event['Write Event Size in bytes'] = temp_event['Size in bytes']
            temp_event.pop('Size in bytes')
        return temp_event

    @staticmethod
    def format_process(temp_event):
        """
        Add file name for binary references if file not found
        :param temp_event:
        :return: dict
        """
        temp_event['File Name'] = copy.deepcopy(temp_event['Process Name'])
        if temp_event.get('Parent Process Name'):
            temp_event['Parent File Name'] = copy.deepcopy(temp_event['Parent Process Name'])
        return temp_event

    @staticmethod
    def format_http_header(temp_event):
        """
        Modify the value of HTTP header string into a dictionary format
        :param temp_event:
        :return:
        """
        header = temp_event.get('HTTP Header').split("\n")
        temp_event['HTTP Header'] = {}
        for value in header:
            if "Host:" in value:
                temp_event['HTTP Header']['Host'] = value.split("Host:")[1].strip()
            elif 'User-Agent:' in value:
                temp_event['HTTP Header']['User-Agent'] = value.split("User-Agent:")[1].strip()
            elif 'Accept-Encoding:' in value:
                temp_event['HTTP Header']['Accept-Encoding'] = value.split("Accept-Encoding:")[1].strip()
        return temp_event

    @staticmethod
    def format_registry(temp_event):
        """
        Format the values for registry object
        :param temp_event:
        :return:
        """
        registry_value = {"name": temp_event["Registry Key Value Name"]}
        temp_event.pop("Registry Key Value Name")
        if temp_event.get('Registry Key Value Type'):
            registry_value['data_type'] = temp_event['Registry Key Value Type']
            temp_event.pop("Registry Key Value Type")
        if temp_event.get('Registry Key Value Text'):
            registry_value['data'] = temp_event['Registry Key Value Text']
            temp_event.pop("Registry Key Value Text")
        temp_event['Registry Key Values'] = [registry_value]
        return temp_event

    def handle_api_exception(self, code, response_data):
        """
        create the exception response
        :param code, int
        :param response_data, dict
        :return: dict
        """
        return_obj = {}
        try:
            response_data = json.loads(response_data)
            if response_data.get('details', []):
                message = response_data['details'][0]['message']
            else:
                message = response_data.get('message')
        except json.JSONDecodeError:
            message = response_data
        if code == 401 and message == "Unauthorized":
            return_obj['status'] = 'authorized'
        else:
            response_dict = {'code': code, 'message': message}
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj
