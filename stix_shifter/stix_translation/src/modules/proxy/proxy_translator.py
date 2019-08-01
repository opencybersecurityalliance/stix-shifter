from ..base.base_translator import BaseTranslator
import json
import requests


class Translator(BaseTranslator):
    def transform_query(self, data, antlr_parsing_object={}, data_model_mapper={}, options={}, mapping=None):
        request_http_path = self._request_http_path(options.get('proxy', {}))
        response = requests.post(request_http_path + "/transform_query",
                                 data=json.dumps({"query": data, "options": options}))
        return response.json()

    def translate_results(self, data_source, data, options, mapping=None):
        request_http_path = self._request_http_path(options.get('proxy', {}))
        response = requests.post(request_http_path + "/translate_results",
                                 data=json.dumps({"results": data, "options": options}))
        return response.json()

    def _proxy_host(self, options):
        proxy_host = options.get('host')
        if not proxy_host:
            raise Exception("Missing proxy host")
        return proxy_host

    def _proxy_port(self, options):
        proxy_port = options.get('port')
        if not proxy_port:
            raise Exception("Missing proxy port")
        return proxy_port

    def _request_http_path(self, options):
        proxy_host = self._proxy_host(options)
        proxy_port = self._proxy_port(options)
        return "http://{}:{}".format(proxy_host, proxy_port)

    def __init__(self):
        self.result_translator = self
        self.query_translator = self
