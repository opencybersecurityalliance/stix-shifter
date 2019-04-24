from ..base.base_translator import BaseTranslator

import json, requests

class Translator(BaseTranslator):
    def transform_query(self, data, options, mapping=None):
        #Data is a STIX pattern and we don't want to touch it
        return json.dumps(data)

    def translate_results(self, data_source, data, options, mapping=None):
        #Data is already STIX and we don't want to touch it
        for obs in data:
            obs["created_by_ref"] = data_source['id']
        return json.dumps(data)

    def __init__(self):
        self.result_translator = self
        self.query_translator = self
