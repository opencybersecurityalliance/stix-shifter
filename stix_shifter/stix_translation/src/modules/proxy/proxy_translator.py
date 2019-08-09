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
        if connection_options:
            proxy_auth = connection_options.get('proxy_auth')
            embedded_connection_options = connection_options.get('options', {})
            if proxy_auth and embedded_connection_options and embedded_connection_options.get('host'):
                connection['proxy_auth'] = connection['options'].pop('proxy_auth')
                connection['host'] = connection['options']['options'].pop('host')
                connection['port'] = connection['options']['options'].pop('port')
                connection['type'] = connection['options']['options'].pop('type')
                # TODO: This may overwrite stuff in the outer-most options we want to keep
                connection['options'] = connection['options'].pop('options')
        return connection

    def __init__(self):
        self.result_translator = self
        self.query_translator = self
