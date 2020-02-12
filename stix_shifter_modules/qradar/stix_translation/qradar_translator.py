
#DELETEME from ..base.base_translator import BaseTranslator
from stix_shifter_utils.modules.base.stix_translation.base_translator import BaseTranslator
from .stix_to_query import StixToQuery
#DELETEME from ...json_to_stix.json_to_stix import JSONToStix
from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import JSONToStix
from .qradar_utils import hash_type_lookup

from os import path


class Translator(BaseTranslator):

    def __init__(self, dialect=None):
        basepath = path.dirname(__file__)
        filepath = path.abspath(
            path.join(basepath, "json", "to_stix_map.json"))
        self.mapping_filepath = filepath
        # Pass in callback function to handle hashes with unknown type
        self.result_translator = JSONToStix(filepath, hash_type_lookup)
        self.query_translator = StixToQuery()
