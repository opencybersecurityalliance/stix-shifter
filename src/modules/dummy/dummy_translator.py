from ..base.base_translator import BaseTranslator
from .dummy_query_translator import DummyQueryTranslator
from .dummy_result_translator import DummyResultTranslator


class Translator(BaseTranslator):

    def __init__(self):
        self.result_translator = DummyResultTranslator()
        self.query_translator = DummyQueryTranslator()
