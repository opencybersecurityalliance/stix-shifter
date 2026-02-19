from stix_shifter_utils.modules.base.stix_transmission.base_json_sync_connector import BaseJsonSyncConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
from .api_client import APIClient
import json
import re

SYMANTEC_MAX_QUERY_RESULTS = 10000
QUERY_TIME_FORMAT = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+?Z)"


class InvalidMetadataException(Exception):
    pass


class Connector(BaseJsonSyncConnector):

    def __init__(self, connection, configuration):
        self.api_client = APIClient(connection, configuration)
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    async def create_results_connection(self, query, offset, length, metadata=None):
        """
        Fetching the results using query, offset and length
        :param query: str, Data Source query
        :param offset: str, Offset value
        :param length: str, Length value
        :param metadata: dict
        :return: return_obj, dict
        Symantec Endpoint Security API has result limit of maximum 10,000 results from the API call.
        The maximum page size is 1000. Hence, 10 API calls will be made to get 10,000 results.
        If the query has results more than 10,000 , then to fetch those records, the following steps are done:-
        1. Get the timestamp of the last record.
        2. Get the count of events with that timestamp.
        3. Set the above values in metadata
        4. Create a new query with start_date, next from above timestamp and event_count.
        5. Skip the records with the same timestamp using the 'next' value in metadata.
        """
        data = []
        try:
            offset = int(offset)
            length = int(length)
            start_index = offset
            end_index = offset + length
            # Adjusting the end index if it exceeds the result limit.
            if self.api_client.result_limit < end_index:
                end_index = self.api_client.result_limit

            # Generating token
            token, return_obj = await self.__get_token()
            if return_obj:
                return return_obj

            if not isinstance(query, dict):
                query = json.loads(query)

            query['limit'] = self.api_client.api_page_size
            query['next'] = offset

            # Update query start_date and next values from metadata to get more than 10k results.
            self.update_query_from_metadata(query, offset, metadata)
            is_query_start_date_updated = False
            while start_index < end_index:
                self.set_query_limit_value(query)
                response_wrapper = await self.api_client.get_search_results(query, token)
                response_dict, return_obj = self.handle_api_response(response_wrapper)
                if return_obj:
                    return return_obj
                return_obj['success'] = True
                processed_data = response_dict['events'][:length]
                data += processed_data
                processed_data_count = len(processed_data)
                start_index += processed_data_count
                query['next'] = self.get_next_index(start_index, metadata)
                remaining_data = response_dict['events'][length:]
                metadata_event_count = metadata.get('start_date_event_count') if metadata else 0
                # If reached the limit of 10,000, resetting the start_date and next for query.
                if (offset + len(data) + metadata_event_count) % SYMANTEC_MAX_QUERY_RESULTS == 0 and processed_data:
                    metadata = self.get_metadata(response_dict['events'][:length])
                    self.update_query_from_metadata(query, 0, metadata)
                    is_query_start_date_updated = True

                # if the current page results are not fully utilized or doesn't have a next page.
                if remaining_data or not response_dict.get('next'):
                    break
                # Adjust the length for the next slicing.
                length -= processed_data_count
            return_obj = self.handle_data(data, return_obj)
            if metadata:
                # metadata will not be set if result limit reached or no more events from the query.
                if (offset + len(return_obj['data'])) < self.api_client.result_limit and start_index == end_index:
                    # setting metadata with last event from the data to avoid duplicate events from next batch call
                    return_obj['metadata'] = self.get_metadata(data) if is_query_start_date_updated else metadata

        except Exception as ex:
            return_obj = self.handle_api_exception(None, str(ex))

        return return_obj

    async def ping_connection(self):
        """
        Ping the endpoint
        Generating authentication token and confirms connectivity to the product.
        :return: return_object, dict
        """
        token, return_obj = await self.__get_token()
        if token:
            return_obj['success'] = True
        return return_obj

    async def __get_token(self):
        """
        Generate new token
        :return: token, string
                 return_obj, dict
        """
        response_wrapper = await self.api_client.generate_token()
        response_dict, return_obj = self.handle_api_response(response_wrapper)
        token = response_dict.get('access_token')
        return token, return_obj

    def handle_api_exception(self, code=None, response_txt=''):
        """
        create the exception response
        :param code, int
        :param response_txt, str
        :return: return_obj, dict
        """
        return_obj = {}
        message = None

        # setting code 401 for 400 code if it is authentication failure.
        if "Invalid Client token" in str(response_txt) or 'Credential mismatch' in str(response_txt):
            message = "Invalid oauth_credentials."
            code = 401

        # setting code 403 for 400 code if it is an invalid query.
        if 'Invalid query' in str(response_txt):
            code = 403

        # setting code 429 with the custom message.
        if 'Max retries exceeded. too_many_requests with max retry' in str(response_txt):
            message = "Too many request were made in the last hour. This API is limited to 500 requests per hour."
            code = 429

        if not message:
            message = str(response_txt)

        response_dict = {'code': code, 'message': message}
        self.logger.error('%s error while fetching results: %s', self.connector, message)
        ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj

    def handle_api_response(self, response_wrapper):
        """
        Handling response codes
        :param response_wrapper, object
        :return: response_dict, dict
                 return_obj, dict
        """
        response_dict = {}
        return_obj = {}

        response = response_wrapper.read().decode('utf-8')
        try:
            response_dict = json.loads(response)
        except ValueError as e:
            response_dict['message'] = response

        if response_wrapper.code != 200:
            response_dict['message'] = response_dict.get('message', '')
            if response_dict.get('fault'):
                response_dict['message'] = response_dict.get('fault', '').get('faultstring', '')
            return_obj = self.handle_api_exception(response_wrapper.code, response_dict.get('message', ''))

        return response_dict, return_obj

    @staticmethod
    def handle_data(data, return_obj):
        """
         Process the data
        :param data, list
        :param return_obj, dict
        :return: return_obj, dict
        """
        if data:
            data = Connector.get_results_data(data)
            return_obj['data'] = data if data else []
        else:
            if not return_obj.get('error') and return_obj.get('success') is not False:
                return_obj['success'] = True
                return_obj['data'] = []
        return return_obj

    @staticmethod
    def update_query_from_metadata(query, offset, metadata):
        """
        Update query 'start_date' and 'next' values from metadata.
        Skipping the event with the same time stamp by adding the 'start_date_event_count' from metadata.
        :param query, (dict) datasource query
        param offset, int
        :param metadata, (dict) metadata with start data and count of the events with start data
        """
        if metadata:
            if isinstance(metadata, dict) and metadata.get('start_date_event_count') and metadata.get('start_date'):
                query['next'] = offset % SYMANTEC_MAX_QUERY_RESULTS + int(metadata.get('start_date_event_count', 0))
                query['start_date'] = metadata.get('start_date')
            else:
                # raise exception when metadata doesnt contain page_index and start_date
                raise InvalidMetadataException(metadata)

    @staticmethod
    def get_metadata(event_data):
        """
        Set query 'start_date' and 'next' values and metadata query start date event count
         and start_date fields.
        :param event_data, (list) datasource search events
        :return metadata, (dict) new metadata fields
        """
        start_date = event_data[-1].get('time')
        event_count = Connector.get_next_start_time_event_count(event_data)
        # Converting timestamp if not in ''%Y-%m-%dT%H:%M:%S.%fZ' format
        pattern = re.compile(QUERY_TIME_FORMAT)
        if not pattern.match(start_date):
            start_date.replace('Z', '.000Z')
        metadata = {'start_date_event_count': event_count,
                    'start_date': start_date}
        return metadata

    @staticmethod
    def get_next_index(processed_event_count, metadata):
        """
        Get the 'next' field value( starting index) for the data source API to get next set of records
        :param processed_event_count, (int) Total events processed
        :param metadata,
        return: next_index (int), next index for the query.
        """
        next_index = processed_event_count % SYMANTEC_MAX_QUERY_RESULTS
        # Skip duplicate events
        if metadata:
            next_index = next_index + metadata.get('start_date_event_count', 0)
        return next_index

    @staticmethod
    def get_next_start_time_event_count(events):
        """
        Get the count of events having the same end timestamp from the list of events.-
        :param events, (list) Datasource events sorted by default with time.
        return: event_count (int)
        """
        event_count = 0
        if events:
            end_timestamp = events[-1].get('time')
            end_index = len(events) - 1
            while end_index >= 0:
                if end_timestamp == events[end_index].get('time'):
                    event_count += 1
                    end_index -= 1
                else:
                    break
        return event_count

    def set_query_limit_value(self, query):
        """
        Update the query limit value if it is beyond 10K
        param Query, (dict) API query.
        """
        if query.get('next') + query.get('limit') >= SYMANTEC_MAX_QUERY_RESULTS:
            query['limit'] = SYMANTEC_MAX_QUERY_RESULTS - (query.get('next'))
        else:
            query['limit'] = self.api_client.api_page_size

    @staticmethod
    def set_attributes(record):
        """
        Preprocesses signature-related attributes in the provided response list. If standard attributes corresponding
        to an x509-certificate object are not present, custom attributes are set to None, as an x509-certificate object
        requires at least one standard attribute (signature_issuer, signature_serial_number, signature_created_date,
        signature_fingerprints).

        :param response: A list containing signature attributes.
        :return response: The modified list after preprocessing.
        """
        if record.get('signature_issuer') is None and \
                record.get('signature_serial_number') is None and \
                record.get('signature_created_date') is None and \
                record.get('signature_fingerprints') is None:
            if record.get('signature_value'):
                record['signature_value'] = None
            if record.get('signature_level_id'):
                record['signature_level_id'] = None
            if record.get('signature_value_ids'):
                record['signature_value_ids'] = None
            if record.get('signature_company_name'):
                record['signature_company_name'] = None

        return record

    @staticmethod
    def process_data(record, keys):
        """
         Process items corresponding to keys which are present in the record.

        :param response: list
        :param keys: key element of record
        :return response: list
        """
        if keys[1]:
            if record.get(keys[0]) and record.get(keys[0]).get(keys[1]):
                record[keys[0]][keys[1]] = Connector.set_attributes(record[keys[0]][keys[1]])
        else:
            if record.get(keys[0]):
                record[keys[0]] = Connector.set_attributes(record[keys[0]])

        return record

    @staticmethod
    def get_results_data(response):
        """
         Preprocessing the response.
        :param response: list
        :return response: list
        """
        for record in response:
            # If device_os_name is not present set value None to other related attributes,
            # as device_os_name is required attribute for software stix object.
            if record.get('device_os_name', '') is (None or ''):
                record['device_os_type_id'] = None
                record['device_os_ver'] = None
                record['device_os_lang'] = None

            # If the dict containing signature related attributes is present,
            # then data needs some preprocessing. Check the following items in record for
            # signature related attributes.
            item_list = [('file', None), ('directory', None), ('actor', 'file'),
                        ('actor', 'module'), ('process', 'file'), ('parent', 'file'),
                        ('module', None), ('startup_app', 'file')]

            for item in item_list:
                record = Connector.process_data(record, item)

        return response
