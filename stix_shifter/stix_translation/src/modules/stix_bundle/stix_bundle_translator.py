from ..base.base_translator import BaseTranslator
import json
import requests
import re
import uuid

START_STOP_PATTERN = "\s?START\s?t'\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z'\sSTOP\s?t'\d{4}(-\d{2}){2}T(\d{2}:){2}\d{2}.\d{1,3}Z'\s?"


class Translator(BaseTranslator):
    def transform_query(self, data, antlr_parsing_object={}, data_model_mapper={}, options={}, mapping=None):
        # Data is a STIX pattern.
        # stix2-matcher will break on START STOP qualifiers so remove before returning pattern.
        # Remove this when ever stix2-matcher supports proper qualifier timestamps
        data = re.sub(START_STOP_PATTERN, " ", data)
        return data

    def translate_results(self, data_source, data, options, mapping=None):
        # Wrap data in a STIX bundle and insert the data_source identity object as the first object
        bundle = {
            "type": "bundle",
            "id": "bundle--" + str(uuid.uuid4()),
            "objects": []
        }

        data_source = json.loads(data_source)
        bundle['objects'] += [data_source]
        # Data is already STIX and we don't want to touch it
        bundle_data = json.loads(data)

        for obs in bundle_data:
            obs["created_by_ref"] = data_source['id']

        bundle['objects'] += bundle_data
        return json.dumps(bundle, indent=4, sort_keys=False)

    def __init__(self):
        self.result_translator = self
        self.query_translator = self
