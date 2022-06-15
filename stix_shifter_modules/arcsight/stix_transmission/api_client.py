import time
from datetime import datetime, timedelta
import json
from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger


class APIClient:
    TOKEN_ENDPOINT = 'core-service/rest/LoginService/login'
    LOGOUT_ENDPOINT = 'core-service/rest/LoginService/logout'
    STATUS_ENDPOINT = 'server/search/status'
    QUERY_ENDPOINT = 'server/search'
    RESULT_ENDPOINT = 'server/search/events'
    DELETE_ENDPOINT = 'server/search/close'

    def __init__(self, connection, configuration):
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]
        self.auth = configuration.get('auth')
        headers = {'Accept': 'application/json'}
        self.client = RestApiClient(connection.get('host'),
                                    connection.get('port'),
                                    headers,
                                    cert_verify=connection.get('selfSignedCert', True)
                                    )

    def ping_data_source(self):
        return_obj, data, headers = dict(), dict(), dict()
        data['search_session_id'] = int(round(time.time() * 1000))
        auth_token = self.get_user_session_id()
        data['user_session_id'] = auth_token
        data['start_time'] = self.get_current_time()['start_time']
        data['end_time'] = self.get_current_time()['end_time']
        headers['Content-Type'] = 'application/json'
        headers['Accept-Charset'] = 'utf-8'
        try:   
            response = self.client.call_api(self.LOGOUT_ENDPOINT, 'POST', headers, data=json.dumps(data))
            raw_response = response.read()
            response_code = response.code

            if 199 < response_code < 300:
                return_obj['success'] = True
                try:
                    self.session_logout(auth_token)
                except Exception as err:
                    self.logger.warn('Unable to logout from the Restful Web service: ' + str(err))
            # arcsight logger error codes - currently unavailable state
            elif response_code in [500, 503]:
                response_string = raw_response.decode()
                ErrorResponder.fill_error(return_obj, response_string, ['message'], connector=self.connector)
            elif isinstance(json.loads(raw_response), dict):
                response_error_ping = json.loads(raw_response)
                response_dict = response_error_ping['errors'][0]
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
            else:
                raise Exception(raw_response)
            
            return return_obj
        except Exception as err:
            raise err


    def create_search(self, query_expression):
        return_obj = dict()
        auth = dict()
        auth['search_session_id'] = int(round(time.time() * 1000))
        auth['user_session_id'] = self.get_user_session_id()
        try:
            query = json.loads(query_expression)
            query.update(auth)
            headers = {'Content-Type': 'application/json', 'Accept-Charset': 'utf-8'}
            response = self.client.call_api(self.QUERY_ENDPOINT, 'POST', headers, data=json.dumps(query))
            raw_response = response.read()
            response_code = response.code

            if 199 < response_code < 300:
                response_dict = json.loads(raw_response)
                if response_dict.get('sessionId'):
                    return_obj['success'] = True
                    return_obj['search_id'] = str(auth['search_session_id']) + ':' + str(auth['user_session_id'])
            # arcsight logger error codes - currently unavailable state
            elif response_code in [500, 503]:
                response_string = raw_response.decode()
                self.logger.error(response_string)
            elif isinstance(json.loads(raw_response), dict):
                response_error = json.loads(raw_response)
                response_dict = response_error['errors'][0]
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
            else:
                raise Exception(raw_response)

            return return_obj
        except Exception as err:
            raise err

    def get_search_status(self, search_session_id, user_session_id):
        headers, params = dict(), dict()
        params['search_session_id'] = int(search_session_id)
        params['user_session_id'] = user_session_id
        headers['Content-Type'] = 'application/json'
        headers['Accept-Charset'] = 'utf-8'
        return self.client.call_api(self.STATUS_ENDPOINT, 'POST', headers, data=json.dumps(params))

    def get_search_results(self, search_session_id, user_session_id, range_start=None, range_end=None):
        headers, params = dict(), dict()
        params['search_session_id'] = int(search_session_id)
        params['user_session_id'] = user_session_id
        params['offset'] = int(range_start)
        params['length'] = int(range_end)
        headers['Content-Type'] = 'application/json'
        headers['Accept-Charset'] = 'utf-8'
        return self.client.call_api(self.RESULT_ENDPOINT, 'POST', headers, data=json.dumps(params))

    def delete_search(self, search_session_id, user_session_id):
        headers, params = dict(), dict()
        params['search_session_id'] = int(search_session_id)
        params['user_session_id'] = user_session_id
        headers['Content-Type'] = 'application/json'
        headers['Accept-Charset'] = 'utf-8'
        return self.client.call_api(self.DELETE_ENDPOINT, 'POST', headers, data=json.dumps(params))

    def get_user_session_id(self):
        try:
            response = self.client.call_api(self.TOKEN_ENDPOINT, 'POST', data=self.auth)
            if response.code == 200:
                response_text = json.loads(response.read())
                token = response_text['log.loginResponse']['log.return']
            elif response.read().decode("utf-8") == '':
                return_dict = 'Request error or authentication failure.'
                raise Exception(return_dict)
            else:
                raise Exception(response)

            return token
        except Exception as err:
            raise err

    def session_logout(self, auth_token):
        data = dict()
        data['authToken'] = auth_token
        try:
            response = self.client.call_api(self.LOGOUT_ENDPOINT, 'POST', urldata=data)
            if response.code == 200:
                self.logger.info('Successful logout from the Restful Web Service')
            elif response.read().decode("utf-8") == '':
                return_dict = 'Request error or authentication failure.'
                raise Exception(return_dict)
            else:
                raise Exception(response)

        except Exception as err:
            raise err

    @staticmethod
    def get_current_time():
        ping_time = dict()
        end_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        start_time = (datetime.utcnow() - timedelta(minutes=5)).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        ping_time['start_time'] = start_time
        ping_time['end_time'] = end_time
        return ping_time
