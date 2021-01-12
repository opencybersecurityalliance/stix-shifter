from stix_shifter_utils.modules.base.stix_translation.base_query_translator import BaseQueryTranslator
from datetime import datetime, timedelta
import re

START_TIME = 'start_time'
END_TIME = 'end_time'


class AqlQueryTranslator(BaseQueryTranslator):

    def parse_query(self, data):
        last_time_criteria = "\s?LAST\s?(\d*)\s?(MINUTES|HOURS|DAYS)"
        time_patterns = {
            "'(\d{4}(-\d{2}){2}\s?(\d{2}:\d{2}))'": "%Y-%m-%d %H:%M",
            "'(\d{4}(-\d{2}){2}\s?\d{2}(:\d{2}){2})'": "%Y-%m-%d %H:%M:%S",
            "'(\d{4}(/\d{2}){2}\s?\d{2}(:\d{2}){2})'": "%Y/%m/%d %H:%M:%S",
            "'(\d{4}(/\d{2}){2}\s?\d{2}(:\d{2}){2})'": "%Y/%m/%d-%H:%M:%S",
            "'(\d{4}(:\d{2}){2}-\d{2}(:\d{2}){2})'": "%Y:%m:%d-%H:%M:%S",
        }

        labels = {'START': START_TIME, 'STOP': END_TIME}
        result = {}
        for label in labels.keys():
            result[labels[label]] = None
        
        match = re.search(last_time_criteria, data, re.IGNORECASE)
        if match:
            time_value = match.group(1)
            interval_value = match.group(2)
            current_time = datetime.now()
            if interval_value.lower() == 'MINUTES'.lower():
                before_time = current_time - timedelta(minutes=int(time_value))
            elif interval_value.lower() == 'HOURS'.lower():
                before_time = current_time - timedelta(hours=int(time_value))
            elif interval_value.lower() == 'DAYS'.lower():
                before_time = current_time - timedelta(days=int(time_value))
            start_dt_obj = datetime.strptime(str(before_time), '%Y-%m-%d %H:%M:%S.%f').strftime('%s.%f')
            result[START_TIME] = int(float(start_dt_obj)*1000)
        else:
            for label in labels.keys():
                result[labels[label]] = self.search_for_pattern(data, time_patterns, label)

        if not result.get(END_TIME):
            current_time = datetime.now()
            result[END_TIME] = int(float(datetime.strptime(str(current_time), '%Y-%m-%d %H:%M:%S.%f').strftime('%s.%f'))*1000)

        return result

    def get_language(self):
        return 'aql'

    def fetch_mapping(self, basepath, dialect, options):
        pass

    def transform_antlr(self, data, unused_antlr_parsing_object=None):
        return data

    def search_for_pattern(self, data, time_pattens, label):
        time_value = None
        for key, value in time_pattens.items():
            match = re.search(f'{label}\\s?{key}', data, re.IGNORECASE)
            if match:
                time_match = match.group(1)
                time_value = int(float(datetime.strptime(time_match, value).strftime('%s.%f'))*1000)              
        return time_value
