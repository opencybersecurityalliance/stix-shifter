# ..base.base_translator import BaseTranslator
from ..base.base_translator import BaseTranslator
from ...json_to_stix.json_to_stix import JSONToStix
from .stix_to_query import StixToQuery
from .splunk_utils import hash_type_lookup

from os import path


class Translator(BaseTranslator):

    def __init__(self):
        basepath = path.dirname(__file__)
        filepath = path.abspath(
            path.join(basepath, "json", "to_stix_map.json"))
        self.mapping_filepath = filepath
        self.result_translator = JSONToStix(filepath, hash_type_lookup)
        self.query_translator = StixToQuery()
