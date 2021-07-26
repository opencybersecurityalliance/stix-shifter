from stix_shifter_utils.modules.base.stix_translation.empty_query_translator import EmptyQueryTranslator
import re

START_STOP_PATTERN = "\s?START\s?t'\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z'\sSTOP\s?t'\d{4}(-\d{2}){2}T(\d{2}:){2}\d{2}.\d{1,3}Z'\s?"


class QueryTranslator(EmptyQueryTranslator):

    def transform_query(self, data):
        # Data is a STIX pattern.
        return {'queries': [data]}
