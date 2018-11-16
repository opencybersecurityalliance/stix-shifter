from ..base.base_translator import BaseTranslator
from .stix_to_dummy_query import StixToDummyQuery
from ...json_to_stix.json_to_stix import JSONToStix
from os import path
# from .dummy_query_translator import DummyQueryTranslator
# from .dummy_result_translator import DummyResultTranslator


class Translator(BaseTranslator):

    def __init__(self):
        # self.result_translator = DummyResultTranslator()
        # self.query_translator = DummyQueryTranslator()

        basepath = path.dirname(__file__)
        filepath = path.abspath(
            path.join(basepath, "json", "to_stix_map.json"))
        self.mapping_filepath = filepath
        self.result_translator = JSONToStix(filepath)
        self.query_translator = StixToDummyQuery()
