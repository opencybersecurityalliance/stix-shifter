from ..base.base_translator import BaseTranslator
from .stix_to_cb import StixToCB
from ...json_to_stix.json_to_stix import JSONToStix

from os import path


class Translator(BaseTranslator):

    def __init__(self, dialect="process"):
        basepath = path.dirname(__file__)

        if dialect == "process":
            filename = "process_api_to_stix_map.json"
        elif dialect == "binary":
            filename = "binary_api_to_stix_map.json"
        else:
            raise RuntimeError("Invalid CarbonBlack dialect: {}".format(dialect))

        filepath = path.abspath(path.join(basepath, "json", filename))
        self.mapping_filepath = filepath

        self.result_translator = JSONToStix(filepath)
        self.query_translator = StixToCB(dialect)
