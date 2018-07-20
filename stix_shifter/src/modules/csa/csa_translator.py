from ..base.base_translator import BaseTranslator
from .stix_to_mongo import StixToMongo

from os import path

class Translator(BaseTranslator):
    def __init__(self):
        basepath = path.dirname(__file__)
        self.query_translator = StixToMongo()
