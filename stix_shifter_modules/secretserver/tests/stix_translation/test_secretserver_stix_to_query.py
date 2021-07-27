import json

from stix_shifter.stix_translation import stix_translation
import unittest


options_file = open('stix_shifter_modules/secretserver/stix_translation/json/aql_events_fields.json').read()
DEFAULT_SELECTIONS = json.loads(options_file)
DEFAULT_LIMIT = 10000
DEFAULT_time_range = 5
MAPPING_ERROR = "Unable to map the following STIX objects and properties to data source fields:"


selections = "SELECT {}".format(", ".join(DEFAULT_SELECTIONS['default']))
from_statement = " FROM secretserverevents "


default_limit = "limit {}".format(DEFAULT_LIMIT)
default_time = "last {} minutes".format(DEFAULT_time_range)

translation = stix_translation.StixTranslation()


def _test_query_assertions(translated_query, test_query):
    assert translated_query['queries'] == test_query

def _translate_query(stix_pattern):
    return translation.translate('secretserver', 'query', '{}', stix_pattern)



class TestQueryTranslator(unittest.TestCase, object):

    def test_secretserver_user_query(self):
        stix_pattern = "[x-ibm-finding:username = 'admin']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE username = 'admin' {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_ipv4_query(self):
        stix_pattern = "[ipv4-addr:value = '192.168.122.83' OR ipv4-addr:value = '192.168.122.84/10']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE (('192.168.122.84/10',IpAddress) OR ('192.168.122.84/10',Server)  OR (IpAddress = '192.168.122.83' OR Server = '192.168.122.83') {} {}".format(
            default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_url_query(self):
        stix_pattern = "[url:value = 'http://www.testaddress.com']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE url = 'http://www.testaddress.com' {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_network_traffic_start_stop(self):
        stix_pattern = "[network-traffic:'start' = '2018-06-14T08:36:24.000Z' OR network-traffic:end = '2021-06-14T08:36:24.567Z']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE endtime = '2018/06/14' OR starttime = '2021/06/14' {} {}".format(default_limit,
                                                                                                        default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_LIKE_operator(self):
        search_string = 'example.com'
        stix_pattern = "[url:value LIKE '{}']".format(search_string)
        query = _translate_query(stix_pattern)
        where_statement = "WHERE url LIKE '%{0}%' {1} {2}".format(search_string, default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_x_ibm_search(self):
        stix_pattern = "[x-ibm-finding:EventSubject = 'abcd']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE EventSubject = 'abcd' {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

        stix_pattern = "[x-ibm-finding:SecretName = 'xyz']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE SecretName = 'xyz' {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)


