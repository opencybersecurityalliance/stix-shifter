from stix_shifter_utils.modules.base.stix_translation.base_results_translator import BaseResultTranslator
import json
import requests
from .utils import unwrap_connection_options

class ResultsTranslator(BaseResultTranslator):

    def read_mapping_file(self, path):
        return '{}'

    def translate_results(self, data_source, data, options={}, mapping=None):
        # A proxy translation call passes the entire data source connection object in as the options
        # Top-most connection host and port are for the proxy
        proxy_host = options['host']
        proxy_port = options['port']

        connection = self.unwrap_connection_options(options)
        request_http_path = "http://{}:{}".format(proxy_host, proxy_port)
        response = requests.post(request_http_path + "/translate_results",
                                 data=json.dumps({"results": data, "options": connection}))
        return response.json()