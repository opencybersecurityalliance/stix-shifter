from stix_shifter_utils.modules.base.stix_translation.empty_query_translator import EmptyQueryTranslator
import re
from time import sleep
from datetime import datetime, timedelta

START_STOP_PATTERN = r"\s?START\s?t'\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d{1,3})?Z'\sSTOP\s?t'\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d{1,3})?Z'\s?"

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
        time_range = self.options['time_range'] # Passed from global config

        # Data is a STIX pattern.
        if not re.search(START_STOP_PATTERN, data):
            # add START STOP qualifier for last x minutes if none present
            now = datetime.now()
            timerange_delta = timedelta(minutes=time_range)
            some_minutes_ago = now - timerange_delta
            start_time = some_minutes_ago.strftime("START t'%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z'"
            stop_time = now.strftime("STOP t'%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z'"
            data = data + " " + start_time + " " + stop_time
        return {'queries': [data]}
