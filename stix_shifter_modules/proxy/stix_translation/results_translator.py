from stix_shifter_utils.modules.base.stix_translation.base_results_translator import BaseResultTranslator
import json
import requests
from .utils import unwrap_connection_options

class ResultsTranslator(BaseResultTranslator):

    def read_json(self, filepath, options):
        return '{}'

    def translate_results(self, data_source, data):
        # A proxy translation call passes the entire data source connection object in as the options
        # Top-most connection host and port are for the proxy
        proxy_host = self.options['proxy_host']
        proxy_port = self.options['proxy_port']

        connection,configuration = unwrap_connection_options(self.options)
        request_http_path = f"http://{proxy_host}:{proxy_port}"
        response = requests.post(request_http_path + "/translate_results",
                                 data=json.dumps({'module': connection['type'], "data_source": data_source, "results": data, "options": connection['options']}), timeout=self.options.get('timeout'))
        return response.json()