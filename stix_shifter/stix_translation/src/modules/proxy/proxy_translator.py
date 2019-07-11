from ..base.base_translator import BaseTranslator
# from stix_shifter.stix_translation.src.patterns.parser import generate_query

import json
import requests


class Translator(BaseTranslator):
    def transform_query(self, data, antlr_parsing_object={}, data_model_mapper={}, options={}, mapping=None):
        proxy_port = self._proxy_port(options)
        proxy_host = self._proxy_host(options)
        response = requests.post("http://" + proxy_host + ":" + proxy_port + "/transform_query",
                                 data=json.dumps({"query": data}))
        return response.text

    def translate_results(self, data_source, data, options, mapping=None):
        proxy_port = self._proxy_port(options)
        proxy_host = self._proxy_host(options)
        response = requests.post("http://" + proxy_host + ":" + proxy_port + "/translate_results",
                                 data=json.dumps({"results": data}))
        return response.text

    def _proxy_host(self, options):
        proxy_host = options.get('proxy', {}).get('host')
        if not proxy_host:
            raise Exception("Missing proxy host")
        return proxy_host

    def _proxy_port(self, options):
        proxy_port = options.get('proxy', {}).get('port')
        if not proxy_port:
            raise Exception("Missing proxy port")
        return proxy_port

    def __init__(self):
        self.result_translator = self
        self.query_translator = self
