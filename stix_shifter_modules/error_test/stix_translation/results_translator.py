from stix_shifter_utils.modules.base.stix_translation.base_results_translator import BaseResultTranslator
from stix_shifter_utils.stix_translation.src.utils.exceptions import TranslationResultException
import json
import uuid

ERROR_TYPE_TRANSLATE_EXCEPTION = 'translate_exception'

class ResultsTranslator(BaseResultTranslator):

    def read_json(self, filepath, options):
        return '{}'

    def translate_results(self, data_source, data):
        error_type = self.options.get('error_type')
        if self.options.get('error_type') == ERROR_TYPE_TRANSLATE_EXCEPTION:
            raise TranslationResultException("Test exception in translate_results")
        
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
