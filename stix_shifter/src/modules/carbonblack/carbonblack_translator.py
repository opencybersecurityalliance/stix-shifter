from ..base.base_translator import BaseTranslator
from .carbonblack_query_translator import CarbonBlackQueryTranslator
from .carbonblack_result_translator import CarbonBlackResultTranslator


class Translator(BaseTranslator):

    def __init__(self):
        self.result_translator = CarbonBlackResultTranslator()
        self.query_translator = CarbonBlackQueryTranslator()
