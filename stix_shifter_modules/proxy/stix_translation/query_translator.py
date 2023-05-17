import json
from .utils import unwrap_connection_options
from stix_shifter_utils.modules.base.stix_translation.empty_query_translator import EmptyQueryTranslator
from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync


class QueryTranslator(EmptyQueryTranslator):

    def read_json(self, filepath, options):
        return '{}'

    def get_language(self):
        return self.options.get('language')

    async def parse_query(self, data):
        proxy_host = self.options['proxy_host']
        proxy_port = self.options['proxy_port']

        connection, configuration = unwrap_connection_options(self.options)

        client = RestApiClientAsync(proxy_host, proxy_port, url_modifier_function=lambda host_port, endpoint, headers: f'https://{host_port}{endpoint}', cert_verify=self.options.get('proxy_cert'))
        response = await client.call_api('/parse_query', 'POST', data=json.dumps({'module': connection['type'],
                                                                            'data_source': {},
                                                                            'data': data,
                                                                            'options': connection['options']}),
                                   timeout=self.options.get('timeout'))
        return json.loads(response.bytes)

    async def transform_query(self, data):
        # A proxy translation call passes the entire data source connection object in as the options
        # Top-most connection host and port are for the proxy
        proxy_host = self.options['proxy_host']
        proxy_port = self.options['proxy_port']

        connection, configuration = unwrap_connection_options(self.options)

        client = RestApiClientAsync(proxy_host, proxy_port, url_modifier_function=lambda host_port, endpoint, headers: f'https://{host_port}{endpoint}', cert_verify=self.options.get('proxy_cert'))
        response = await client.call_api('/transform_query', 'POST', data=json.dumps({'module': connection['type'],
                                                                                'data_source': {},
                                                                                'data': data,
                                                                                'options': connection['options']}),
                                   timeout=self.options.get('timeout'))
        return json.loads(response.bytes)
