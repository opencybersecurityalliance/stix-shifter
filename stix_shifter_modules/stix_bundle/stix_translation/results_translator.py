from stix_shifter_utils.modules.base.stix_translation.base_results_translator import BaseResultTranslator
import json
import uuid


class ResultsTranslator(BaseResultTranslator):

    def read_mapping_file(self, file_path):
        return '{}'

    def translate_results(self, data_source, data):
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
        return bundle
