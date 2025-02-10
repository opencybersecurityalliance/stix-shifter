from stix_shifter_utils.modules.base.stix_transmission.base_json_sync_connector import BaseJsonSyncConnector
from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync
from .api_client import APIClient
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
from .api_client import APIResponseException
import json


class Connector(BaseJsonSyncConnector):
    def __init__(self, connection, configuration):
        self.connector = __name__.split('.')[1]
        self.api_client = APIClient()
        self.logger = logger.set_logger(__name__)
        self.result_limit = connection['options'].get('result_limit', 1000)  # Default to 1000
        self.client = RestApiClientAsync(connection.get('host'), None, {})

        auth = configuration.get('auth')
        self.auth_headers = {
            'Content-Type': 'application/json',
            'user-agent': 'oca_stixshifter_1.0',
            'username': auth["username"],
            'password': auth["password"],
            'validity': '365'
        }

        self.base_url = connection.get('host')
        self.timeout = connection['options'].get('timeout')
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'user-agent': 'oca_stixshifter_1.0'
        }

    async def ping_connection(self):
        try:
            response = await self.api_client.ping_box(
                self.client,
                self.base_url,
                self.auth_headers,
                self.headers,
                self.timeout
            )
            return {"success": response.code == 200}
        except Exception as e:
            return self._handle_errors(e)

    async def create_results_connection(self, query, offset, length):
        return_obj = {}
        queryId = None
        nextCursorMarker = None
        all_events = []
        has_more_data = True

        try:
            while has_more_data:
                response = await self.api_client.get_securonix_data(
                    query,
                    self.client,
                    self.base_url,
                    self.auth_headers,
                    self.headers,
                    self.timeout,
                    queryId=queryId,
                    nextCursorMarker=nextCursorMarker
                )

                if response.code == 200:
                    response_data = json.loads(response.content)
                    events = response_data.get('events', [])
                    all_events.extend(events)  # Accumulate events

                    # Check if there's more data based on response
                    queryId = response_data.get('queryId')
                    nextCursorMarker = response_data.get('nextCursorMarker')

                    if not events or not (queryId and nextCursorMarker):
                        has_more_data = False
                        return_obj['metadata'] = None
                    else:
                        has_more_data = True  # Prepare for the next iteration
                else:
                    return self._handle_errors(response)

            return_obj['success'] = True
            return_obj['data'] = all_events[offset:offset + length]  # consider offset and length
            return return_obj

        except Exception as e:
            return self._handle_errors(e)

    def _handle_errors(self, error):
        response_dict = {}
        return_obj = {}

        if isinstance(error, APIResponseException):
            if error.content_header_type == 'application/json':
                response = json.loads(error.error_message)
                response_dict['message'] = response.get('error') or response.get('message') or str(error.error_message)

                if error.error_code == 400:
                    response_dict['type'] = 'ValidationError'
                elif error.error_code == 401:
                    response_dict['type'] = 'AuthenticationError'
                elif error.error_code == 403:
                    response_dict['type'] = 'TokenError'
            else:
                response_dict['message'] = f'Error connecting to datasource: {error.error_message}'

        ErrorResponder.fill_error(return_obj, response_dict, ['message'], error=error, connector=self.connector)
        return return_obj
