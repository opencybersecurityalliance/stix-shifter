
# ..base.base_translator import BaseTranslator
from ..base.base_translator import BaseTranslator
from .stix_to_aql import StixToAQL
from ...json_to_stix.json_to_stix import JSONToStix

from os import path


class Translator(BaseTranslator):

    def __init__(self):
        basepath = path.dirname(__file__)
        filepath = path.abspath(
            path.join(basepath, "json", "to_stix_map.json"))

        self.result_translator = JSONToStix(filepath)
        self.query_translator = StixToAQL()
