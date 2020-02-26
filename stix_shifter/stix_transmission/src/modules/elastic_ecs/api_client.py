import base64
from ..utils.RestApiClient import RestApiClient
import json
import re

DEFAULT_LIMIT = 10000


class APIClient():
    PING_ENDPOINT = '_cluster/health?pretty'
    PING_TIMEOUT_IN_SECONDS = 10

    def __init__(self, connection, configuration):
        headers = dict()
        url_modifier_function = None
        auth = configuration.get('auth')
        self.indices = configuration.get('elastic_ecs', {}).get('indices', None)

        if isinstance(self.indices, list):  # Get list of all indices
            self.indices = ",".join(self.indices)

        if self.indices:
            self.endpoint = self.indices + '/' +'_search'
        else:
            self.endpoint = '_search'

        if auth:
            if 'username' in auth and 'password' in auth:
                headers['Authorization'] = b"Basic " + base64.b64encode(
                    (auth['username'] + ':' + auth['password']).encode('ascii'))
            elif 'api_key' in auth and 'id' in auth:
                headers['Authorization'] = b"ApiKey " + base64.b64encode(
                    (auth['id'] + ':' + auth['api_key']).encode('ascii'))
            elif 'access_token' in auth:
                headers['Authorization'] = "Bearer " + auth['access_token']

        self.client = RestApiClient(connection.get('host'),
                                    connection.get('port'),
                                    connection.get('cert', None),
                                    headers,
                                    url_modifier_function=url_modifier_function,
                                    cert_verify=connection.get('selfSignedCert', True),
                                    mutual_auth=connection.get('use_securegateway', False),
                                    sni=connection.get('sni', None)
                                    )

    def ping_box(self):
        return self.client.call_api(self.PING_ENDPOINT, 'GET',timeout=self.PING_TIMEOUT_IN_SECONDS)

    def run_search(self, query_expression, offset=None, length=DEFAULT_LIMIT):
        headers = dict()
        headers['Content-Type'] = 'application/json'

        endpoint = self.endpoint

        uri_search = False  # For testing and debugging two ways of _search API methods

        # URI Search
        if uri_search:
            if query_expression is not None:
                # update/add size value
                if length is not None:
                    if re.search(r"&size=\d+", query_expression):
                        query_expression = re.sub(r"(?<=&size=)\d+", str(length), query_expression)
                    else:
                        query_expression = '{}&size={}'.format(query_expression, length)

                # add offset to query expression
                if offset is not None:
                    query_expression = '{}&from={}'.format(query_expression, offset)

            # addition of QueryString to API END point
            endpoint = endpoint + '?q=' + query_expression

            return self.client.call_api(endpoint, 'GET', headers)
        # Request body search
        else:
            # add size value
            if length is not None:
                endpoint = "{}?size={}".format(endpoint, length)

            # add offset value
            if offset is not None:
                endpoint = "{}&from={}".format(endpoint, offset)

            data = {
                "_source": {
                    "includes": ["@timestamp", "source.*", "destination.*", "event.*", "client.*", "server.*",
                                 "host.*","network.*", "process.*", "user.*", "file.*", "url.*"]
                },
                "query": {
                    "query_string": {
                      "query": query_expression
                    }
                }
            }

            print("URL endpoint: " + endpoint)
            print("URL data: " + json.dumps(data))

            return self.client.call_api(endpoint, 'GET', headers, data=json.dumps(data))