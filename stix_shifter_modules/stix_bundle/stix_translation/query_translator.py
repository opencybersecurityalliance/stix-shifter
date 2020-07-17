from stix_shifter_utils.modules.base.stix_translation.empty_query_translator import EmptyQueryTranslator
import re

START_STOP_PATTERN = "\s?START\s?t'\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z'\sSTOP\s?t'\d{4}(-\d{2}){2}T(\d{2}:){2}\d{2}.\d{1,3}Z'\s?"


class QueryTranslator(EmptyQueryTranslator):

    def transform_query(self, data, antlr_parsing_object={}):
        # Data is a STIX pattern.
        # stix2-matcher will break on START STOP qualifiers so remove before returning pattern.
        # Remove this when ever stix2-matcher supports proper qualifier timestamps
        data = re.sub(START_STOP_PATTERN, " ", data)
        return data
