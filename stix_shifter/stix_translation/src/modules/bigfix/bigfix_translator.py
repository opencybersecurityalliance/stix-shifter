from ..base.base_translator import BaseTranslator
from .stix_to_bigfix import StixToRelevanceQuery
from .bigfix_result_translator import BigfixResultTranslator


class Translator(BaseTranslator):

    def __init__(self):
        self.result_translator = BigfixResultTranslator()
        self.query_translator = StixToRelevanceQuery()
