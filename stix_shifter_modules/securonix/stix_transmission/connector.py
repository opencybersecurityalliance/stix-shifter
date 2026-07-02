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
        self.result_limit = connection['options'].get('result_limit', 1000)

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

        try:
            response = await self.api_client.get_securonix_data(
                query,
                self.client,
                self.base_url,
                self.auth_headers,
                self.headers,
                self.timeout
            )

            if response.code == 200:
                response_data = json.loads(response.content)
                events = response_data.get('events', [])

                return_obj['success'] = True
                return_obj['data'] = events

                if len(events) < self.result_limit:
                    return_obj['metadata'] = None
                else:
                    return_obj['metadata'] = {
                        'queryId': response_data.get('queryId'),
                        'result_count': len(events)
                    }
            else:
                return self._handle_errors(response)

        except Exception as e:
            return self._handle_errors(e)

        return return_obj

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
