from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient


class APIClient():

    QUERY_ENDPOINT = 'web/api/v2.1/dv/init-query'
    RESULT_ENDPOINT = 'web/api/v2.1/dv/events'
    QUERY_STATUS = 'web/api/v2.1/dv/query-status'
    PING_STATUS = 'web/api/v2.1/system/status'

    def __init__(self, connection, configuration):

        headers = dict()
        self.auth = configuration.get('auth')
        self.api_key = "ApiToken " + self.auth.get('apitoken')
        headers['Authorization'] = self.api_key
        headers['Content-type'] = 'application/json'
        self.timeout = connection['options']['timeout']
        self.client = RestApiClient(connection.get('host'),
                                     connection.get('port', None),
                                     headers,
                                     url_modifier_function=None
                                     )

    def ping_datasource(self):
        """
        ping or check the system status
        """
        endpoint = self.PING_STATUS
        return self.client.call_api(endpoint, 'GET', headers=self.client.headers,
                                    timeout=self.timeout)

    def create_search(self, query_expression):
        """
        init query
        :param data source query
        :return:queryId
        """

        endpoint = self.QUERY_ENDPOINT
        data = query_expression
        data = data.encode('utf-8')
        return self.client.call_api(endpoint, 'POST', headers=self.client.headers, data=data,
                                    timeout=self.timeout)

    def get_search_status(self, search_id):
        """
        get query status
        :param queryId:
        :return:
        """

        endpoint = self.QUERY_STATUS + "?queryId=" + search_id
        params = {}
        params['output'] = 'json'
        return self.client.call_api(endpoint, 'GET', headers=self.client.headers, urldata=params,
                                    timeout=self.timeout)

    def get_search_results(self, search_id, offset, length, nextcursor=None):
        """
        Get results from Data Source
        :param query: Data Source QueryId,nextcursor,limit
        :return: Response Object
        """

        endpoint = self.RESULT_ENDPOINT + "?queryId=" + search_id
        #Max limit of getting result in a api call is 1000
        limit = 1000
        if nextcursor is not None:
            endpoint = endpoint + "&cursor=" + nextcursor
        endpoint = endpoint + "&limit=" + str(limit)

        params = {}
        params['output'] = 'json'
        return self.client.call_api(endpoint, 'GET', headers=self.client.headers, urldata=params,
                                    timeout=self.timeout)

    def delete_search(self, search_id):
        """
        delete api is not supported
        :param queryId:
        :return:dict
        """
        return {"code": 200, "success": True}
