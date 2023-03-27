from stix_shifter_utils.modules.base.stix_translation.base_results_translator import BaseResultTranslator
import json
import uuid


class ResultsTranslator(BaseResultTranslator):

    def read_json(self, filepath, options):
        return '{}'

    def translate_results(self, data_source, data):
        # Wrap data in a STIX bundle and insert the data_source identity object as the first object
        bundle = {
            "type": "bundle",
            "id": "bundle--" + str(uuid.uuid4()),
            "objects": []
        }

        bundle['objects'] += [data_source]
        # Data is already STIX and we don't want to touch it
        for obs in data:
            obs["created_by_ref"] = data_source['id']

        bundle['objects'] += data
        return bundle
