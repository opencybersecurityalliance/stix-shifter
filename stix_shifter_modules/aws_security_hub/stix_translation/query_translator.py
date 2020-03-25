from stix_shifter_utils.modules.base.stix_translation.base_translator import BaseQueryTranslator
from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import JSONToStix
from . import query_constructor
from os import path

class QueryTranslator(BaseQueryTranslator):

    def transform_query(self, data, antlr_parsing_object, data_model_mapper, options, mapping=None):

        query_string = query_constructor.translate_pattern(
            antlr_parsing_object, data_model_mapper)
        return query_string
