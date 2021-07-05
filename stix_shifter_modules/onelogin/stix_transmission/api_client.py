from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient


class APIClient():

    def __init__(self, connection, configuration):
        auth = configuration.get('auth')
        auth = f"client_id:{auth.get('clientId')},client_secret:{auth.get('clientSecret')}"
        headers = dict()
        headers['Authorization'] = auth
        headers['Accept'] = 'application/json'
        headers['Content-Type'] = 'application/json'
        self.host = connection.get('host')
        self.client = RestApiClient(self.host,
                                    connection.get('port'),
                                    headers,
                                    cert_verify=connection.get('selfSignedCert', True)
                                    )

    def generate_token(self):
        """To generate the Token"""
        endpoint = "auth/oauth2/v2/token"
        payload = '{"grant_type": "client_credentials"}'
        return self.client.call_api(endpoint, 'POST', data=payload)

    def ping_data_source(self):
        # Pings the data source
        return {"code": 200, "success": True}

    def run_search(self, quary_expr, range_end=None, access_token=None):
        """get the response from onelogin endpoints
        :param quary_expr: str, search_id
        :param range_end: int,length value
        :param access_token: str, access_token
        :return: response, json object"""
        endpoint = "api/1/events?" + quary_expr
        headers = dict()
        headers['Accept'] = 'application/json'
        headers['Authorization'] = "bearer:" + access_token
        data = dict()
        if range_end is not None:
            data = {"limit": range_end}
        return self.client.call_api(endpoint, 'GET', headers, urldata=data)

    def next_page_run_search(self, next_page_url):
        """get the response from onelogin endpoints
        :param next_page_url: str, search_id
        :return: response, json object"""
        headers = dict()
        headers['Accept'] = 'application/json'
        url = next_page_url.split('?', maxsplit=1)[1]
        endpoint = "api/1/events?" + url
        return self.client.call_api(endpoint, 'GET', headers, timeout=self.timeout)

    def get_search_results(self, search_id, range_start=None, range_end=None):
        # Return the search results. Results must be in JSON format before being translated into STIX
        return {"code": 200, "data": "Results from search"}

    def delete_search(self, search_id):
        # Optional since this may not be supported by the data source API
        # Delete the search
        return {"code": 200, "success": True}
