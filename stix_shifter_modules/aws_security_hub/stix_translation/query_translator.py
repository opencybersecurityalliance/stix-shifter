from stix_shifter_utils.modules.base.stix_translation.base_query_translator import BaseQueryTranslator
from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import JSONToStix
from . import query_constructor
from os import path

class QueryTranslator(BaseQueryTranslator):

    def map_field(self, stix_object_name, stix_property_name):
        if stix_object_name in self.map_data and stix_property_name in self.map_data[stix_object_name]["fields"]:
            return self.map_data[stix_object_name]["fields"][stix_property_name]
        else:
            return []

    def transform_query(self, data, antlr_parsing_object):

        query_string = query_constructor.translate_pattern(
            antlr_parsing_object, self)
        return query_string
