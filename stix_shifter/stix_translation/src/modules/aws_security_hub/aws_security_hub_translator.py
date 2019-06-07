from ..base.base_translator import BaseTranslator
from ...json_to_stix.json_to_stix import JSONToStix
# from stix_shifter.stix_translation.src.patterns.parser import generate_query
# from . import data_mapping
from . import query_constructor
from os import path
# from stix_shifter.stix_translation.src.unmapped_attribute_stripper import strip_unmapped_attributes


class Translator(BaseTranslator):
    def transform_query(self, data, antlr_parsing_object, data_model_mapper, options, mapping=None):
        # query_object = strip_unmapped_attributes(antlr_parsing_object, data_model_mapper)

        query_string = query_constructor.translate_pattern(
            antlr_parsing_object, data_model_mapper)
        return query_string

    def __init__(self):
        basepath = path.dirname(__file__)
        filepath = path.abspath(
            path.join(basepath, "json", "to_stix_map.json"))

        self.mapping_filepath = filepath
        self.result_translator = JSONToStix(filepath)
        self.query_translator = self
