from stix_shifter_utils.modules.base.stix_translation.base_query_translator import BaseQueryTranslator
import json
import requests
from .utils import unwrap_connection_options

class QueryTranslator(BaseQueryTranslator):

    def fetch_mapping(self, basepath):
        return {}

    def transform_query(self, data, antlr_parsing_object={}):
        # A proxy translation call passes the entire data source connection object in as the options
        # Top-most connection host and port are for the proxy
        proxy_host = self.options['host']
        proxy_port = self.options['port']

        connection = unwrap_connection_options(self.options)
        request_http_path = "http://{}:{}".format(proxy_host, proxy_port)
        response = requests.post(request_http_path + "/transform_query",
                                 data=json.dumps({"query": data, "options": connection}))
        return response.json()