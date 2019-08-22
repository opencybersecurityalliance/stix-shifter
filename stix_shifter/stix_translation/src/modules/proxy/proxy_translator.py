from ..base.base_translator import BaseTranslator
import json
import requests


class Translator(BaseTranslator):

    def transform_query(self, data, antlr_parsing_object={}, data_model_mapper={}, options={}, mapping=None):
        # A proxy translation call passes the entire data source connection object in as the options
        # Top-most connection host and port are for the proxy
        proxy_host = options['host']
        proxy_port = options['port']

        connection = self._unwrap_connection_options(options)
        request_http_path = "http://{}:{}".format(proxy_host, proxy_port)
        response = requests.post(request_http_path + "/transform_query",
                                 data=json.dumps({"query": data, "options": connection}))
        return response.json()

    def translate_results(self, data_source, data, options={}, mapping=None):
        # A proxy translation call passes the entire data source connection object in as the options
        # Top-most connection host and port are for the proxy
        proxy_host = options['host']
        proxy_port = options['port']

        connection = self._unwrap_connection_options(options)
        request_http_path = "http://{}:{}".format(proxy_host, proxy_port)
        response = requests.post(request_http_path + "/translate_results",
                                 data=json.dumps({"results": data, "options": connection}))
        return response.json()

    def _unwrap_connection_options(self, connection):
        connection_options = connection.get('options', {})
        embedded_connection_options = connection_options.get('options', {})
        if embedded_connection_options and embedded_connection_options.get('host'):
            connection['host'] = embedded_connection_options.get('host')
            connection['port'] = embedded_connection_options.get('port')
            connection['type'] = embedded_connection_options.get('type')
            del connection['options']
            connection.update(connection_options)
        elif connection_options and connection_options.get('host'):
            del connection['options']
            connection.update(connection_options)
        return connection

    def __init__(self):
        self.result_translator = self
        self.query_translator = self
