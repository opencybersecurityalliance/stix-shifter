from ..base.base_translator import BaseTranslator
from .bigfix_query_translator import BigfixQueryTranslator
from .bigfix_result_translator import BigfixResultTranslator


class Translator(BaseTranslator):

    def __init__(self):
        self.result_translator = BigfixResultTranslator()
        self.query_translator = BigfixQueryTranslator()
