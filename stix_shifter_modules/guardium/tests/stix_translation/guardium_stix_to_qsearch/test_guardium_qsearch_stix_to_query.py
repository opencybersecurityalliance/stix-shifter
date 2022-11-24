
from stix_shifter.stix_translation import stix_translation
from stix_shifter_utils.utils.error_response import ErrorCode
from stix_shifter.stix_translation.stix_translation import MAPPING_ERROR
import unittest


options_file = open('stix_shifter_modules/guardium/tests/stix_translation/guardium_stix_to_qsearch/options.json').read()

category = "\"category\": \"VIOLATION\""
reportName = "\"reportName\": \"ATA Open Cases\""
translation = stix_translation.StixTranslation()



def _test_query_assertions(queries, num, filters):
    count = 0
    for query in queries:
        if filters in query or category in query:
            count = 1
    assert count == num


def _translate_query(stix_pattern):
    return translation.translate('guardium:qsearch', 'query', '{}', stix_pattern)


class TestQueryTranslator(unittest.TestCase, object):

    def test_db_user_query(self):
        stix_pattern = "[ user-account:db_user='MARCI']"
        query = _translate_query(stix_pattern)
        filters = "\"filters\":\"name=DB User&value=MARCI&isGroup=false\""
        _test_query_assertions(query['queries'], 1, filters)

    def test_db_network_traffic_query(self):
        stix_pattern = "[network-traffic:dst_ref.value='9.42.54.193']"
        query = _translate_query(stix_pattern)
        filters = "\"filters\":\"name=Server&value=9.42.54.193&isGroup=false\""
        _test_query_assertions(query['queries'], 1, filters)
        stix_pattern = "[network-traffic:src_ref.value='9.42.54.193']"
        query = _translate_query(stix_pattern)
        filters = "\"filters\":\"name=Client IP&value=9.42.54.193&isGroup=false\""
        _test_query_assertions(query['queries'], 1, filters)

    def test_ipv4_query(self):
        stix_pattern = "[ipv4-addr:value = '1.2.3.4']"
        query = _translate_query(stix_pattern)
        filters = "\"filters\":\"name=Client IP&value=1.2.3.4&isGroup=false\""
        _test_query_assertions(query['queries'], 1, filters)        
        filters = "\"filters\":\"name=Server&value=1.2.3.4&isGroup=false\""
        _test_query_assertions(query['queries'], 1, filters)

    def test_ipv6_query(self):
        stix_pattern = "[ipv6-addr:value = '1:2:3:4:5:6:7:8']"
        query = _translate_query(stix_pattern)
        filters = "\"filters\":\"name=Client IP&value=1:2:3:4:5:6:7:8&isGroup=false\""
        _test_query_assertions(query['queries'], 1, filters)        
        filters = "\"filters\":\"name=Server&value=1:2:3:4:5:6:7:8&isGroup=false\""
        _test_query_assertions(query['queries'], 1, filters)

    def test_query_or(self):
        stix_pattern = "[ user-account:db_user='MARCI' OR ipv4-addr:value = '1.2.3.4']"
        query = _translate_query(stix_pattern)
        filters = "\"filters\":\"name=Client IP&value=1.2.3.4&isGroup=false\""
        _test_query_assertions(query['queries'], 1, filters)
        filters = "\"filters\":\"name=Server&value=1.2.3.4&isGroup=false\""
        _test_query_assertions(query['queries'], 1, filters)
        filters = "\"filters\":\"name=DB User&value=MARCI&isGroup=false\""
        _test_query_assertions(query['queries'], 1, filters)

    def test_query_and(self):
        stix_pattern = "[ user-account:db_user='MARCI' AND ipv4-addr:value = '1.2.3.4']"
        query = _translate_query(stix_pattern)
        filters = "name=DB User&value=MARCI&isGroup=false"
        _test_query_assertions(query['queries'], 1, filters)
        #filters = "name=Server&value=1.2.3.4&isGroup=false"
        #_test_query_assertions(query['queries'], 1, filters)
        filters = "name=Client IP&value=1.2.3.4&isGroup=false"
        _test_query_assertions(query['queries'], 1, filters)
        filters = "name=DB User&value=MARCI&isGroup=false"
        _test_query_assertions(query['queries'], 1, filters)
        filters = "name=Server&value=1.2.3.4&isGroup=false"
        _test_query_assertions(query['queries'], 1, filters)

    def test_query_or_with_non_qs_field(self):
        stix_pattern = "[ unmapped-object:some_invalid_attribute = 'whatever' OR ipv4-addr:value = '1.2.3.4']"
        query = _translate_query(stix_pattern)
        filters = "\"filters\":\"name=Server&value=1.2.3.4&isGroup=false\""
        _test_query_assertions(query['queries'], 1, filters)
        filters = "name=Client IP&value=1.2.3.4&isGroup=false"
        _test_query_assertions(query['queries'], 1, filters)
        assert 2 == len(query['queries'])

    def test_query_and_with_non_qs_field(self):
        stix_pattern = "[ unmapped-object:some_invalid_attribute = 'whatever' AND ipv4-addr:value = '1.2.3.4']"
        query = _translate_query(stix_pattern)
        assert not query['success']
        assert ErrorCode.TRANSLATION_MAPPING_ERROR.value == query['code']
        assert MAPPING_ERROR in query['error']

    def test_severity_query(self):
        stix_pattern = "[ x-guardium:severity='Low']"
        query = _translate_query(stix_pattern)
        filters = "\"query\":\"Severity>01\""
        _test_query_assertions(query['queries'], 1, filters)

    def test_in_comparison_operator(self):
        stix_pattern = "[ipv4-addr:value IN ('127.0.0.1', '127.0.0.2')]"
        query = translation.translate('guardium', 'query', '{}', stix_pattern)
        filters = "\"ServerIP\": \"127.0.0.1\""
        _test_query_assertions(query['queries'], 1, filters)
        filters = "\"ServerIP\": \"127.0.0.2\""
        _test_query_assertions(query['queries'], 1, filters)
        filters = "\"filters\":\"name=Client IP&value=127.0.0.1&isGroup=false\""
        _test_query_assertions(query['queries'], 1, filters)
        filters = "\"filters\":\"name=Server&value=127.0.0.2&isGroup=false\""
        _test_query_assertions(query['queries'], 1, filters)
        filters = "\"filters\":\"name=Server&value=127.0.0.1&isGroup=false\""
        _test_query_assertions(query['queries'], 1, filters)
        filters = "\"filters\":\"name=Client IP&value=127.0.0.2&isGroup=false\""
        _test_query_assertions(query['queries'], 1, filters)

