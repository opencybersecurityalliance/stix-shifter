import json
from .utils import unwrap_connection_options
from stix_shifter_utils.modules.base.stix_translation.empty_query_translator import EmptyQueryTranslator
from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient


class QueryTranslator(EmptyQueryTranslator):

    def read_json(self, filepath, options):
        return '{}'

    def get_language(self):
        return self.options.get('language')

    def transform_query(self, data):
        # A proxy translation call passes the entire data source connection object in as the options
        # Top-most connection host and port are for the proxy
        proxy_host = self.options['proxy_host']
        proxy_port = self.options['proxy_port']

        connection, configuration = unwrap_connection_options(self.options)

        client = RestApiClient(proxy_host, proxy_port, url_modifier_function=lambda host_port, endpoint, headers: f'http://{host_port}{endpoint}')
        response = client.call_api('/transform_query', 'POST', data=json.dumps({'module': connection['type'],
                                                                                'query': data,
                                                                                'options': connection['options']}),
                                   timeout=self.options.get('timeout'))
        return json.loads(response.bytes)
