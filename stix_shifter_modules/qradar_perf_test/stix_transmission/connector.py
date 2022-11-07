from stix_shifter_utils.modules.base.stix_transmission.base_sync_connector import BaseSyncConnector
from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync
import json
from stix_shifter_utils.utils.error_response import ErrorResponder


class UnexpectedResponseException(Exception):
    pass


class Connector(BaseSyncConnector):
    def __init__(self, connection, configuration):
        self.connector = __name__.split('.')[1]
        self.connection = connection
        self.configuration = configuration
        self.timeout = connection['options'].get('timeout')
        self.bundle_url = self.connection.get('url')
        auth = None
        conf_auth = configuration.get('auth', {})
        if 'username' in conf_auth and 'password' in conf_auth:
            auth = (conf_auth['username'], conf_auth['password'])
        self.client = RestApiClientAsync(None,
                                    auth=auth,
                                    url_modifier_function=lambda host_port, endpoint, headers: f'{endpoint}')

    def ping_connection(self):
        return_obj = dict()

        response = self.client.call_api(self.bundle_url, 'head', timeout=self.timeout)
        response_txt = response.raise_for_status()

        if response.code == 200:
            return_obj['success'] = True
        elif response.code == 301:
            self.bundle_url = response.headers.get('Location')
            return self.ping_connection()
        else:
            ErrorResponder.fill_error(return_obj, response_txt, ['message'], connector=self.connector)
        return return_obj

    def create_results_connection(self, search_id, offset, length):
        return_obj = dict()
        response = self.client.call_api(self.bundle_url, 'get', timeout=self.timeout)

        if response.code != 200:
            response_txt = response.raise_for_status()
            if ErrorResponder.is_plain_string(response_txt):
                ErrorResponder.fill_error(return_obj, message=response_txt, connector=self.connector)
            elif ErrorResponder.is_json_string(response_txt):
                response_json = json.loads(response_txt)
                ErrorResponder.fill_error(return_obj, response_json, ['reason'], connector=self.connector)
            else:
                raise UnexpectedResponseException
        else:
            try:
                response_text = response.read().decode('utf-8')
                response_code = response.code

                # Construct a response object
                error = None
                response_text = response.read()

                try:
                    response_dict = json.loads(response_text)
                except ValueError as ex:
                    self.logger.debug(response_text)
                    error = Exception(f'Can not parse response: {ex} : {response_text}')
                
                if 200 <= response_code <= 299:
                    return_obj['success'] = True
                    return_obj['data'] = response_dict.get('events', response_dict.get('flows'))[:int(length)]
                else:
                    ErrorResponder.fill_error(return_obj, response_dict, ['message'], error=error, connector=self.connector)
            except Exception as ex:
                ErrorResponder.fill_error(return_obj,  message='Invalid STIX bundle. Malformed JSON: ' + str(ex), connector=self.connector)

            return return_obj

    def delete_query_connection(self, search_id):
        return_obj = dict()
        return_obj['success'] = True
        return return_obj
