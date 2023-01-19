from stix_shifter_utils.modules.base.stix_translation.empty_query_translator import EmptyQueryTranslator
import re
from datetime import datetime, timedelta

START_STOP_PATTERN = r"\s?START\s?t'\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d{1,3})?Z'\sSTOP\s?t'\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d{1,3})?Z'\s?"


class QueryTranslator(EmptyQueryTranslator):

    def transform_query(self, data):
        # Data is a STIX pattern.
        if not re.search(START_STOP_PATTERN, data):
            # add START STOP qualifier for last 5 minutes if none present
            now = datetime.now()
            five_minute_delta = timedelta(minutes=5)
            five_minutes_ago = now - five_minute_delta
            start_time = five_minutes_ago.strftime("START t'%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z'"
            stop_time = now.strftime("STOP t'%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z'"
            data = data + " " + start_time + " " + stop_time
        return {'queries': [data]}
