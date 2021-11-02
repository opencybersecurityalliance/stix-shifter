from stix_shifter.stix_translation import stix_translation
from stix_shifter_utils.utils.error_response import ErrorCode
import unittest
import json
import datetime
import re



DEFAULT_LIMIT = 10000
DEFAULT_TIMERANGE = 5

translation = stix_translation.StixTranslation()

def _set_start_stop(query):
    stop_time = datetime.datetime.utcnow()
    go_back_in_minutes = datetime.timedaelta(minutes=DEFAULT_TIMERANGE)
    start_time = stop_time - go_back_in_minutes
    # converting from UTC timestamp 2019-04-13 23:13:06.130401 to
    # string format 2019-04-13 23:13:06.130Z
    converted_starttime = start_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    converted_stoptime = stop_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    return converted_starttime, converted_stoptime


class TestStixtoQuery(unittest.TestCase, object):

    def _test_query_assertions(self, translated_query, test_query):
        assert translated_query['queries'] == test_query

    def test_query(self):
        stix_pattern = "[email-addr:value = 'redhat@gmail.com'] START t'2021-08-28T12:54:01.009Z' STOP t'2021-09-05T12:54:01.009Z'"
        translated_query = translation.translate('trustar', 'query', '{}', stix_pattern)
        test_query = ["{\"searchTerm\": \"redhat@gmail.com\", \"from\": 1630155241000, \"to\": 1630846441000}"]
        self._test_query_assertions(translated_query, test_query)

    def test_searchterm(self):
        stix_pattern = "[x-trustar-query:x_searchTerm = 'redhat@gmail.com'] START t'2021-08-28T12:54:01.009Z' STOP t'2021-09-05T12:54:01.009Z'"
        translated_query = translation.translate('trustar', 'query', '{}', stix_pattern)
        test_query = ["{\"searchTerm\": \"redhat@gmail.com\", \"from\": 1630155241000, \"to\": 1630846441000}"]
        self._test_query_assertions(translated_query, test_query)

    def test_entitytype(self):
        stix_pattern = "[x-trustar-query:x_type = 'IP, MALWARE'] START t'2021-08-28T12:54:01.009Z' STOP t'2021-09-05T12:54:01.009Z'"
        translated_query = translation.translate('trustar', 'query', '{}', stix_pattern)
        test_query = ["{\"entityTypes\": \"IP, MALWARE\", \"from\": 1630155241000, \"to\": 1630846441000}"]
        self._test_query_assertions(translated_query, test_query)

    def test_ipv4(self):
        stix_pattern = "[ipv4-addr:value = '127.0.0.1'] START t'2021-08-28T12:54:01.009Z' STOP t'2021-09-05T12:54:01.009Z'"
        translated_query = translation.translate('trustar', 'query', '{}', stix_pattern)
        test_query = ["{\"searchTerm\": \"127.0.0.1\", \"from\": 1630155241000, \"to\": 1630846441000}"]
        self._test_query_assertions(translated_query, test_query)

    def test_report(self):
        stix_pattern = "[x-trustar-query:x_report_details = '9e509316-b8f2-428e-9981-0e552bb128bf'] START t'2021-08-28T12:54:01.009Z' STOP t'2021-09-05T12:54:01.009Z'"
        translated_query = translation.translate('trustar', 'query', '{}', stix_pattern)
        test_query = ["{\"reportId\": \"9e509316-b8f2-428e-9981-0e552bb128bf\", \"from\": 1630155241000, \"to\": 1630846441000}"]
        self._test_query_assertions(translated_query, test_query)