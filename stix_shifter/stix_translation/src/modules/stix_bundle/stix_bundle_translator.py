from ..base.base_translator import BaseTranslator

import json, requests

class Translator(BaseTranslator):
    def transform_query(self, data, options, mapping=None):
        #Data is a STIX pattern and we don't want to touch it
        return data

    def translate_results(self, data_source, data, options, mapping=None):
        #Data is already STIX and we don't want to touch it
        bundle_data = json.loads(data)
        data_source = json.loads(data_source)
        for obs in bundle_data:
            obs["created_by_ref"] = data_source['id']
        return json.dumps(bundle_data, indent=4, sort_keys=False)

    def __init__(self):
        self.result_translator = self
        self.query_translator = self
