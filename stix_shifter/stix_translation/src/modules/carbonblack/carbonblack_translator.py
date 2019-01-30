
# ..base.base_translator import BaseTranslator
from ..base.base_translator import BaseTranslator
from .stix_to_cb import StixToCB
from ...json_to_stix.json_to_stix import JSONToStix

from os import path


class Translator(BaseTranslator):

    def __init__(self, dialect="process"):
        basepath = path.dirname(__file__)

        if dialect not in ["process", "binary"]:
            raise NotImplementedError # TODO what's the best exception type to raise?

        filepath = path.abspath(path.join(basepath, "json", "to_stix_map.json"))
        self.mapping_filepath = filepath

        self.result_translator = JSONToStix(filepath)
        self.query_translator = StixToCB(dialect)
