from ..base.base_translator import BaseTranslator
from .stix_to_bigfix import StixToRelevanceQuery
from .bigfix_to_stix.big_to_stix import BigFixToStix

from os import path

class Translator(BaseTranslator):

    def __init__(self):
        basepath = path.dirname(__file__)
        filepath = path.abspath(
            path.join(basepath, "json", "to_stix_map.json"))
        
        self.mapping_filepath = filepath
        self.result_translator = BigFixToStix(filepath)
        self.query_translator = StixToRelevanceQuery()
