import json
from ..base.base_translator import TranslationInterface
from .stix_to_aql import StixToAQL
from ...json_to_stix.json_to_stix import JSONToStix
from abc import ABCMeta, abstractmethod


class Translator(TranslationInterface):

    def __init__(self):
        self.result_translator = JSONToStix()
        self.query_translator = StixToAQL()
