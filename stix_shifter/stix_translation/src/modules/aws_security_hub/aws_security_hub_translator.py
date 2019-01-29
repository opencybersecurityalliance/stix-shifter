from ..base.base_translator import BaseTranslator
from ...json_to_stix.json_to_stix import JSONToStix
from stix_shifter.stix_translation.src.patterns.parser import generate_query
from . import data_mapping
from . import query_constructor
from os import path

class Translator(BaseTranslator):
    def transform_query(self, data, options, mapping=None):
        query_object = generate_query(data)
        data_model_mapper = data_mapping.DataMapper(options)

        query_string = query_constructor.translate_pattern(
            query_object, data_model_mapper)
        return query_string

    def __init__(self):
        basepath = path.dirname(__file__)
        filepath = path.abspath(
            path.join(basepath, "json", "to_stix_map.json"))

        self.mapping_filepath = filepath
        self.result_translator = JSONToStix(filepath)
        self.query_translator = self
