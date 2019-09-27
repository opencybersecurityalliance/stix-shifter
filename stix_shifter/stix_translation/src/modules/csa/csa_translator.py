from ..base.base_translator import BaseTranslator
from .stix_to_query import StixToCloudSQL
from ...json_to_stix.json_to_stix import JSONToStix


from os import path

class Translator(BaseTranslator):
    def __init__(self, dialect="at", rows=1024):
        basepath = path.dirname(__file__)
        filepath = path.abspath(
            path.join(basepath, "json", dialect+"_to_stix_map.json"))
        self.mapping_filepath = filepath
        self.result_translator = JSONToStix(filepath)
        self.query_translator = StixToCloudSQL(dialect=dialect, rows=rows)
