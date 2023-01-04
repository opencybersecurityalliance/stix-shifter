from stix_shifter_utils.modules.base.stix_translation.empty_query_translator import EmptyQueryTranslator
import re
from time import sleep

START_STOP_PATTERN = "\s?START\s?t'\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z'\sSTOP\s?t'\d{4}(-\d{2}){2}T(\d{2}:){2}\d{2}.\d{1,3}Z'\s?"

ERROR_TYPE_PARSE_EXCEPTION = 'parse_exception'
ERROR_TYPE_TRANSFORM_EXCEPTION = 'transform_exception'
ERROR_TYPE_TRANSFORM_DELAY_SEC = 'transform_delay_sec_'

class QueryTranslator(EmptyQueryTranslator):

    def parse_query(self, data):
        if self.options.get('error_type') == ERROR_TYPE_PARSE_EXCEPTION:
            raise Exception('test exception in parse query')
        return super().parse_query(data)

    def transform_query(self, data):
        error_type = self.options.get('error_type')
        if error_type == ERROR_TYPE_TRANSFORM_EXCEPTION:
            raise Exception('test exception in transform query')
        if error_type.startswith(ERROR_TYPE_TRANSFORM_DELAY_SEC):
            delay = int(error_type[len(ERROR_TYPE_TRANSFORM_DELAY_SEC):])
            sleep(delay)
        # Data is a STIX pattern.
        # stix2-matcher will break on START STOP qualifiers so remove before returning pattern.
        # Remove this when ever stix2-matcher supports proper qualifier timestamps
        data = re.sub(START_STOP_PATTERN, " ", data)
        return {'queries': [data]}
