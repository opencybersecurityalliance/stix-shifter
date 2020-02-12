import json
from . import json_to_stix_translator
from ..modules.base.base_result_translator import BaseResultTranslator
from stix_shifter.stix_translation.src.utils import transformers
from stix_shifter.stix_translation.src.utils.exceptions import LoadJsonResultsException, TranslationResultException

# Concrete BaseResultTranslator


class JSONToStix(BaseResultTranslator):

    def translate_results(self, data_source, data, options, mapping=None):
        """
        Translates JSON data into STIX results based on a mapping file
        :param data: JSON formatted data to translate into STIX format
        :type data: str
        :param mapping: The mapping file path to use as instructions on how to translate the given JSON data to STIX. 
            Defaults the path to whatever is passed into the constructor for JSONToSTIX (This should be the to_stix_map.json in the module's json directory)
        :type mapping: str (filepath)
        :return: STIX formatted results
        :rtype: str
        """
        self.mapping = options['mapping'] if 'mapping' in options else {}
        try:
            json_data = json.loads(data)
            data_source = json.loads(data_source)
        except Exception:
            raise LoadJsonResultsException()

        if(not self.mapping):
            map_file = open(self.default_mapping_file_path).read()
            map_data = json.loads(map_file)
        else:
            map_data = self.mapping

        try:
            results = json_to_stix_translator.convert_to_stix(data_source, map_data, json_data, transformers.get_all_transformers(), options, self.callback)
        except Exception as ex:
            raise TranslationResultException("Error when converting results to STIX: {}".format(ex))

        return json.dumps(results, indent=4, sort_keys=False)
