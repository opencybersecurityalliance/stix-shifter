import json

from . import json_to_stix_translator
from ..modules.base.base_result_translator import BaseResultTranslator
from . import transformers

# Concrete BaseResultTranslator


class JSONToStix(BaseResultTranslator):

    def translate_results(self, data, options, mapping=None):
        """
        Translates JSON data into STIX results based on a mapping file
        :param data: JSON formatted data to translate into STIX format
        :type data: str
        :param mapping: The mapping file path to use as instructions on how to translate the given JSON data to STIX. Defaults the path to whatever is passed into the constructor for JSONToSTIX (This should be the to_stix_map.json in the module's json directory)
        :type mapping: str (filepath)
        :return: STIX formatted results
        :rtype: str
        """
        json_data = json.loads(data)

        if(mapping is None):
            # If no mapping is passed in then we will use the default to_stix_map in the qradar module
            map_file = open(self.default_mapping_file_path).read()
            map_data = json.loads(map_file)
        else:
            map_data = json.loads(mapping)

        # todo: make datasource id/name dynamic
        datasource = {
            'id': '7c0de425-33bf-46be-9e38-e42319e36d95', 'name': 'events'}

        results = json_to_stix_translator.convert_to_stix(datasource, map_data, 
            json_data, transformers.get_all_transformers(), options)

        return json.dumps(results)
