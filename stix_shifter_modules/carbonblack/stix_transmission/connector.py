import json
from stix_shifter_utils.modules.base.stix_transmission.base_json_sync_connector import BaseJsonSyncConnector
from .api_client import APIClient
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
from .event_parser import supported_event_types, parse_raw_event_to_obj, create_event_obj, extract_time_window, \
    get_timestamp_by_event_type, is_timestamp_in_window, format_timestamp


class UnexpectedResponseException(Exception):
    pass


class Connector(BaseJsonSyncConnector):
    def __init__(self, connection, configuration):
        self.api_client = APIClient(connection, configuration)
        self.show_events = Connector.get_show_events_mode(connection)
        self.result_limit = Connector.get_result_limit(connection)
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    @staticmethod
    def get_show_events_mode(connection):
        if 'options' in connection:
            return connection['options'].get('events_mode', False)
        return False

    @staticmethod
    def get_result_limit(connection):
        # result_limit = 0 => no limit
        default_result_limit = 10000
        if 'options' in connection:
            return connection['options'].get('result_limit', default_result_limit)
        return default_result_limit

    def _handle_errors(self, response, return_obj, results_key='results'):
        response_code = response.code
        response_txt = response.read().decode('utf-8')

        if 200 <= response_code < 300:
            return_obj['success'] = True
            if response_txt:
                response_json = json.loads(response_txt)
                if results_key in response_json:
                    return_obj['data'] = response_json[results_key]
        elif ErrorResponder.is_plain_string(response_txt):
            ErrorResponder.fill_error(return_obj, message=response_txt, connector=self.connector)
        elif ErrorResponder.is_json_string(response_txt):
            response_json = json.loads(response_txt)
            ErrorResponder.fill_error(return_obj, response_json, ['reason'], connector=self.connector)
        else:
            raise UnexpectedResponseException
        return return_obj

    @staticmethod
    def _get_events(process_data: dict, time_window: list):  # add time window to function
        raw_events = []
        for event_type in supported_event_types:
            event_key = '{}_complete'.format(event_type)
            if event_key in process_data:
                for event_data in process_data[event_key]:
                    parsed_event = parse_raw_event_to_obj(event_type, event_data)
                    if parsed_event is not None:
                        timestamp = get_timestamp_by_event_type(event_obj=parsed_event, event_type=event_type)
                        if timestamp:
                            if (time_window and is_timestamp_in_window(timestamp, time_window)) or (not time_window):
                                parsed_event['parsed_timestamp'] = format_timestamp(timestamp)
                                raw_events.append({
                                    'event_type': event_type,
                                    'parsed_event_data': parsed_event
                                })
        return raw_events

    async def ping_connection(self):
        response_txt = None
        return_obj = {}
        try:
            response = await self.api_client.ping_box()
            return self._handle_errors(response, return_obj)
        except Exception as e:
            if response_txt is not None:
                ErrorResponder.fill_error(return_obj, message='unexpected exception', connector=self.connector)
                self.logger.error('can not parse response: ' + str(response_txt))
            else:
                raise e

    async def create_results_connection(self, query, offset, length):
        response_txt = None
        return_obj = {}
        all_events = []
        try:
            processes_obj = {}
            processes_search_response = await self.api_client.run_processes_search(query, start=offset, rows=length)
            processes_search_parsed_response = self._handle_errors(processes_search_response, processes_obj)
            if not self.show_events or not processes_search_parsed_response.get('success', False):
                return processes_search_parsed_response
            if processes_search_parsed_response.get('success', False):
                time_window = extract_time_window(query)
                events_limit_reached = False
                for process in processes_search_parsed_response['data']:
                    try:
                        events_obj = {}
                        events_response = await self.api_client.run_events_search(process_id=process['id'],
                                                                            segment_id=process['segment_id'])
                        events_parsed_response = self._handle_errors(events_response, events_obj, results_key='process')
                        if events_parsed_response.get('success', False):
                            events = Connector._get_events(events_parsed_response['data'], time_window)
                            for raw_event in events:
                                event = create_event_obj(process, raw_event)
                                if event:
                                    all_events.append(event)
                                    if 0 < self.result_limit <= len(all_events):
                                        events_limit_reached = True
                                        break
                    except Exception:
                        self.logger.warn('cannot fetch events for process: ' + str(process['process_id']))
                    if events_limit_reached:
                        break
            return {'success': True, 'data': all_events}

        except Exception as e:
            if response_txt is not None:
                ErrorResponder.fill_error(return_obj, message='unexpected exception', connector=self.connector)
                self.logger.error('can not parse response: ' + str(response_txt))
            else:
                raise e
