import json

from stix_shifter.stix_translation import stix_translation
import unittest


DEFAULT_LIMIT = 10000
DEFAULT_time_range = 5
MAPPING_ERROR = "Unable to map the following STIX objects and properties to data source fields:"
selections = "SELECT *"
from_statement = " FROM SecretEventDetail "


default_limit = "limit {}".format(DEFAULT_LIMIT)
default_time = "last {} minutes".format(DEFAULT_time_range)

translation = stix_translation.StixTranslation()


def _test_query_assertions(query,selections, from_statement, where_statement):
    assert query['queries'] == [selections + from_statement + where_statement]

def _translate_query(stix_pattern):
    return translation.translate('secretserver', 'query', '{}', stix_pattern)



class TestQueryTranslator(unittest.TestCase, object):

    def test_ipv4_query(self):
        stix_pattern = "[ipv4-addr:value = '192.168.122.83']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE (IpAddress = \'192.168.122.83\' OR Server = \'192.168.122.83\')"
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_url_query(self):
        stix_pattern = "[url:value = 'http://www.testaddress.com']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE url = 'http://www.testaddress.com'"
        _test_query_assertions(query,selections, from_statement, where_statement)

    def test_LIKE_operator(self):
        search_string = 'example.com'
        stix_pattern = "[url:value LIKE '{}']".format(search_string)
        query = _translate_query(stix_pattern)
        where_statement = "WHERE url LIKE '%example.com%'"
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_x_ibm_search(self):
        stix_pattern = "[x-ibm-finding:event_name = 'abcd']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE EventSubject = 'abcd'"
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_x_secret_search(self):
        stix_pattern = "[x-secret:secret_name = 'xyz']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE SecretName = 'xyz'"
        _test_query_assertions(query, selections, from_statement, where_statement)

