# ..base.base_translator import BaseTranslator
from ..base.base_translator import BaseTranslator
from .cim_to_stix.cim_to_stix import CIMToStix
from .splunk_result_translator import SplunkResultTranslator
from .stix_to_splunk import StixToSplunk

from os import path


class Translator(BaseTranslator):

    def __init__(self):
        basepath = path.dirname(__file__)
        filepath = path.abspath(
            path.join(basepath, "json", "to_stix_map.json"))
       
        self.mapping_filepath = filepath
        self.result_translator = CIMToStix(filepath)
        self.query_translator = StixToSplunk()