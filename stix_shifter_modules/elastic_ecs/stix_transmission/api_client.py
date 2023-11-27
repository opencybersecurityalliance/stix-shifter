import base64
from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync
from stix_shifter_utils.utils import logger
import json
import re

DEFAULT_LIMIT = 10000


class APIClient():
    PING_ENDPOINT = '_cluster/health?pretty'

    def __init__(self, connection, configuration):
        self.logger = logger.set_logger(__name__)
        headers = dict()
        url_modifier_function = None
        auth = configuration.get('auth')
        self.indices = connection.get('indices', None)

        if self.indices and type(self.indices) == str:
            self.indices = self.indices.split(",")

        if isinstance(self.indices, list):  # Get list of all indices
            self.indices = [i.strip(' ') for i in self.indices]
            self.indices = ",".join(self.indices)

        if self.indices:
            self.endpoint = self.indices + '/' + '_search'
            self.pit_endpoint = self.indices + '/' + '_pit'
            self.setting_endpoint = self.indices + '/' + '_settings'
        else:
            self.endpoint = '_search'
            self.pit_endpoint = '_pit'
            self.setting_endpoint = '_settings'

        if auth:
            if 'username' in auth and 'password' in auth:
                token_decoded = auth['username'] + ':' + auth['password']
                token = base64.b64encode(token_decoded.encode('ascii'))
                headers['Authorization'] = "Basic %s" % token.decode('ascii')

            elif 'api_key' in auth and 'id' in auth:
                token_decoded = auth['id'] + ':' + auth['api_key']
                token = base64.b64encode(token_decoded.encode('ascii'))
                headers['Authorization'] = "ApiKey %s" % token.decode('ascii')
            elif 'access_token' in auth:
                headers['Authorization'] = "Bearer " + auth['access_token']

        self.client = RestApiClientAsync(connection.get('host'),
                                    connection.get('port'),
                                    headers,
                                    url_modifier_function=url_modifier_function,
                                    cert_verify=connection.get('selfSignedCert')
                                    )

        self.timeout = connection['options'].get('timeout')

    async def ping_box(self):
        return await self.client.call_api(self.PING_ENDPOINT, 'GET', timeout=self.timeout)

    async def search_pagination(self, query_expression, lastsortvalue=None, length=DEFAULT_LIMIT):
        headers = dict()
        headers['Content-Type'] = 'application/json'

        data = {
            "_source": {
                "includes": ["@timestamp", "source.*", "destination.*", "event.*", "client.*", "server.*", "observer.*",
                             "host.*", "network.*", "process.*", "user.*", "file.*", "url.*", "registry.*", "dns.*",
                             "tags"]
            },
            "size": length,
            "query": {
                "query_string": {
                    "query": query_expression
                }
            },
            "sort": [
                {"@timestamp": "asc"},
            ]
        }

        if lastsortvalue:
            data["search_after"] = lastsortvalue

        self.logger.debug("URL endpoint: " + self.endpoint)
        self.logger.debug("URL data: " + json.dumps(data))

        return await self.client.call_api(self.endpoint, 'GET', headers, data=json.dumps(data), timeout=self.timeout)

    async def get_max_result_window(self):
        max_result_window_url = self.setting_endpoint + "/index.max_result_window?include_defaults=true"
        return await self.client.call_api(max_result_window_url, 'GET', timeout=self.timeout)

    async def set_pit(self):
        headers = dict()
        headers['Content-Type'] = 'application/json'

        # GET PIT
        # POST /my-index-000001/_pit?keep_alive=1m
        endpoint = "{}?keep_alive=1m&pretty".format(self.pit_endpoint)

        return await self.client.call_api(endpoint, 'POST', headers, timeout=self.timeout)



