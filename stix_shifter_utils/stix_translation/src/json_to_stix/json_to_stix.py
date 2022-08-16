import json
import importlib
from stix_shifter_utils.modules.base.stix_translation.base_results_translator import BaseResultTranslator
from stix_shifter_utils.stix_translation.src.utils.exceptions import TranslationResultException

# Concrete BaseResultTranslator
class JSONToStix(BaseResultTranslator):

    def translate_results(self, data_source, data):
        """
        Translates JSON data into STIX results based on a mapping file
        :param data: JSON formatted data to translate into STIX format
        :type data: str
        :return: STIX formatted results
        :rtype: str
        """

        try:
            json_to_stix_translator = importlib.import_module('stix_shifter_modules.%s.stix_translation.json_to_stix_translator' % self.module_name)
        except Exception as ex:
            # fall back to default
            json_to_stix_translator = importlib.import_module('stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix_translator')

        try:
            results = json_to_stix_translator.convert_to_stix(data_source, self.map_data, data, self.transformers, self.options, self.callback)
        except Exception as ex:
            raise TranslationResultException("Error when converting results to STIX: {}".format(ex))
        
        return results
