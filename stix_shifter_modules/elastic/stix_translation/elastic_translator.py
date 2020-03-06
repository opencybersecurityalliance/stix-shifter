from stix_shifter_utils.modules.base.stix_translation.base_translator import BaseTranslator
from .stix_to_elastic import StixToElastic

from os import path

class Translator(BaseTranslator):
    def __init__(self, dialect=None):
        self.result_translator = None
        self.query_translator = StixToElastic()
