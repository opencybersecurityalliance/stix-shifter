import requests
import json
from .utils import unwrap_connection_options
from stix_shifter_utils.modules.base.stix_translation.base_results_translator import BaseResultTranslator
from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient

class ResultsTranslator(BaseResultTranslator):

    def read_json(self, filepath, options):
        return '{}'

    def translate_results(self, data_source, data):
        # A proxy translation call passes the entire data source connection object in as the options
        # Top-most connection host and port are for the proxy
        proxy_host = self.options['proxy_host']
        proxy_port = self.options['proxy_port']

        connection,configuration = unwrap_connection_options(self.options)

        client = RestApiClient(proxy_host, proxy_port, url_modifier_function=lambda host_port,endpoint,headers: f'http://{host_port}{endpoint}')
        response = client.call_api('/translate_results', 'POST', data=json.dumps({'module': connection['type'], "data_source": data_source, "results": data, "options": connection['options']}), timeout=self.options.get('timeout'))
        return json.loads(response.bytes)
