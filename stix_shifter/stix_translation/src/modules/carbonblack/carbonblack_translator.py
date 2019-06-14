from ..base.base_translator import BaseTranslator
from .stix_to_query import StixToQuery
from ...json_to_stix import json_to_stix_translator
from stix_shifter.stix_translation.src.utils import transformers


from os import path
import json


class Translator(BaseTranslator):

    def __init__(self):
        basepath = path.dirname(__file__)
        filepath = path.abspath(path.join(basepath, "json", "to_stix_map.json"))
        self.mapping_filepath = filepath
        self.query_translator = StixToQuery()

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
        json_data = json.loads(data)
        data_source = json.loads(data_source)

        if(not self.mapping):
            map_file = open(self.mapping_filepath).read()
            map_data = json.loads(map_file)
        else:
            map_data = self.mapping

        results = json_to_stix_translator.convert_to_stix(data_source, map_data, json_data,
                                                          transformers.get_all_transformers(), options)

        if len(results['objects']) - 1 == len(json_data):
            for i in range(1, len(results['objects'])):
                results['objects'][i]['number_observed'] = 1
        else:
            raise RuntimeError("Incorrect number of result objects after translation. Found: {}, expected: {}.".format(len(results['objects']) - 1, len(json_data)))

        return json.dumps(results, indent=4, sort_keys=False)
