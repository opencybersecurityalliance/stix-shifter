from abc import ABCMeta, abstractmethod
from .base_result_translator import ResultTranslationInterface
from .base_query_translator import QueryTranslationInterface


class TranslationInterface:

    def __init__(self):
        self.result_translator = ResultTranslationInterface()
        self.query_translator = QueryTranslationInterface()

    def translate_results(self, data, mapping=None):
        return self.result_translator.translate_results(data, mapping)

    def transform_query(self, data, mapping=None):
        return self.query_translator.transform_query(data, mapping)
