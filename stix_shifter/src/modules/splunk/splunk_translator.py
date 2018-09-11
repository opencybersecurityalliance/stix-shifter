# ..base.base_translator import BaseTranslator
from ..base.base_translator import BaseTranslator
from .stix_to_splunk import StixToSplunk

from os import path

class Translator(BaseTranslator):
    def __init__(self):
        self.result_translator = None
        self.query_translator = StixToSplunk()
