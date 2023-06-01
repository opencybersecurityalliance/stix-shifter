from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync
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
        self.client = RestApiClientAsync(connection.get('host'),
                                    connection.get('port', None),
                                    headers,
                                    url_modifier_function=url_modifier_function
                                    )
        self.timeout = connection['options'].get('timeout')
        self.host = 'https://'+connection.get('host')+':'+str(connection.get('port'))+'/'

    async def ping_box(self):
        """
        Ping the Data Source
        :return: Response object
        """
        headers = {}

        headers['Cookie'] = await self.session_log_in()
        return await self.client.call_api(self.STATUS_ENDPOINT, 'GET', headers=headers, timeout=self.timeout)

    async def get_search_results(self, query):
        """
        Get results from Data Source
        :param query: Data Source Query
        :return: Response Object
        """
        headers = {'Cookie': await self.session_log_in()}
        self.logger.debug("query: %s", query)
        return await self.client.call_api(self.QUERY_ENDPOINT, 'POST', headers=headers, data=query, timeout=self.timeout)

    async def session_log_in(self):
        """
        Create a login session and return the cookie id
        :return: str, cookie id
        """
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        url = self.host + self.LOGIN_ENDPOINT
        response = await self.client.call_api(self.LOGIN_ENDPOINT, 'POST', headers=headers, data=self.auth, timeout=self.timeout)
        cookie = response.get_cookies(url)
        cookie = str(cookie).replace('Set-Cookie: ', '')
        return cookie

    async def session_log_out(self, response_wrapper):
        """
        Logging out of Session
        :return: response object
        """
        headers = {}
        cookie_dict = response_wrapper.response.request_info.headers.get('Cookie')
        headers["Cookie"] = cookie_dict
        return await self.client.call_api(self.LOGOFF_ENDPOINT, 'GET', headers=headers, timeout=self.timeout)
