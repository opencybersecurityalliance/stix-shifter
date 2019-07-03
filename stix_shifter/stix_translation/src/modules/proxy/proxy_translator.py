from ..base.base_translator import BaseTranslator
# from stix_shifter.stix_translation.src.patterns.parser import generate_query

import json
import requests


class Translator(BaseTranslator):
    def transform_query(self, data, antlr_parsing_object={}, data_model_mapper={}, options={}, mapping=None):
        response = requests.post("http://" + options["proxy_host"] + ":" + options["proxy_port"] + "/transform_query",
                                 data=json.dumps({"query": data}))
        return response.text

    def translate_results(self, data_source, data, options, mapping=None):
        response = requests.post("http://" + options["proxy_host"] + ":" + options["proxy_port"] + "/translate_results",
                                 data=json.dumps({"results": data}))
        return response.text

    def __init__(self):
        self.result_translator = self
        self.query_translator = self
