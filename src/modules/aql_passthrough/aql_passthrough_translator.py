
from ..base.base_translator import BaseTranslator
from ..dummy.dummy_query_translator import DummyQueryTranslator
from ...json_to_stix.json_to_stix import JSONToStix


class Translator(BaseTranslator):

    def __init__(self):
        self.result_translator = JSONToStix(
            'src/modules/aql_passthrough/json/to_stix_map.json')
        self.query_translator = DummyQueryTranslator()
