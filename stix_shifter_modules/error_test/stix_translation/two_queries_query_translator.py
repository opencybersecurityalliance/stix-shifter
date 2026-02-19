from stix_shifter_utils.modules.base.stix_translation.empty_query_translator import EmptyQueryTranslator
import re
from time import sleep
from datetime import datetime, timedelta

START_STOP_PATTERN = r"\s?START\s?t'\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d{1,3})?Z'\sSTOP\s?t'\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d{1,3})?Z'\s?"

class TwoQueriesQueryTranslator(EmptyQueryTranslator):

    def get_language(self):
        return '2queries'

    def transform_query(self, data):
        return {'queries': ['query1', 'query2']}
