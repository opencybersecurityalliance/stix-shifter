from ..base.base_translator import BaseTranslator
from .stix_to_query import StixToQuery
from ...json_to_stix.json_to_stix import JSONToStix
from os import path
import logging


class Translator(BaseTranslator):

    def __init__(self):
        basepath = path.dirname(__file__)
        filepath = path.abspath(
            path.join(basepath, "json", "to_stix_map.json"))
        self.mapping_filepath = filepath
        self.result_translator = JSONToStix(filepath)
        self.query_translator = StixToQuery()
        #
        # It is for Guardium
        # Start logging based on logLevel -- for debugging purpuse -- SB
        logFile = "../runlogs/ss_guardium_translation_run.log"
        logging.basicConfig(filename=logFile, level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info('-----------Translation Run Started.------------')
