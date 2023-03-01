from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient
from stix_shifter_utils.utils import logger

DEFAULT_LIMIT = 10000
DEFAULT_OFFSET = 0


class APIClient:
    LOGIN_ENDPOINT = 'login.html'
    QUERY_ENDPOINT = 'rest/visualsearch/query/simple'
    STATUS_ENDPOINT = 'rest/monitor/global/reg-server/status'
    LOGOFF_ENDPOINT = 'logout'

    def __init__(self, connection, configuration):
        self.logger = logger.set_logger(__name__)
        headers = {'Content-Type': 'application/json'}
        url_modifier_function = None
        self.auth = configuration.get('auth')
        self.client = RestApiClient(connection.get('host'),
                                    connection.get('port', None),
                                    headers,
                                    url_modifier_function=url_modifier_function
                                    )
        self.timeout = connection['options'].get('timeout')

    def ping_box(self):
        """
        Ping the Data Source
        :return: Response object
        """
        headers = {}
        headers['Cookie'] = self.session_log_in()
        return self.client.call_api(self.STATUS_ENDPOINT, 'GET', headers=headers)

    def get_search_results(self, query):
        """
        Get results from Data Source
        :param query: Data Source Query
        :return: Response Object
        """
        headers = {'Cookie': self.session_log_in()}
        self.logger.debug("query: %s", query)
        return self.client.call_api(self.QUERY_ENDPOINT, 'POST', headers=headers, data=query)

    def session_log_in(self):
        """
        Create a login session and return the cookie id
        :return: str, cookie id
        """
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response_wrapper = self.client.call_api(self.LOGIN_ENDPOINT, 'POST', headers=headers, data=self.auth)
        cookie_id = response_wrapper.response.request.headers
        return cookie_id['Cookie']

    def session_log_out(self, response_wrapper):
        """
        Logging out of Session
        :return: response object
        """
        headers = {}
        cookie_dict = response_wrapper.response.request.headers
        cookie_id = cookie_dict["Cookie"]
        headers["Cookie"] = cookie_id
        return self.client.call_api(self.LOGOFF_ENDPOINT, 'GET', headers=headers)
