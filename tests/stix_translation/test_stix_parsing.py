from stix_shifter.stix_translation import stix_translation
import unittest
import json

options_file = open('tests/stix_translation/qradar_stix_to_aql/options.json').read()
selections_file = open('stix_shifter/stix_translation/src/modules/qradar/json/aql_event_fields.json').read()
protocols_file = open('stix_shifter/stix_translation/src/modules/qradar/json/network_protocol_map.json').read()
OPTIONS = json.loads(options_file)
DEFAULT_SELECTIONS = json.loads(selections_file)
DEFAULT_LIMIT = 10000
DEFAULT_TIMERANGE = 5
PROTOCOLS = json.loads(protocols_file)


selections = "SELECT {}".format(", ".join(DEFAULT_SELECTIONS['default']))
custom_selections = "SELECT {}".format(", ".join(OPTIONS['select_fields']))
from_statement = " FROM events "


default_limit = "limit {}".format(DEFAULT_LIMIT)
default_time = "last {} minutes".format(DEFAULT_TIMERANGE)

translation = stix_translation.StixTranslation()


def _parse_query(stix_pattern):
    return translation.translate('qradar', 'parse', '{}', stix_pattern)


class TestStixParsing(unittest.TestCase, object):

    def test_default_timerange(self):
        stix_pattern = "[ipv4-addr:value = '192.168.122.83' OR ipv4-addr:value = '192.168.122.84/10']"
        parsing = _parse_query(stix_pattern)
        parsed_stix = [{'attribute': 'ipv4-addr:value', 'comparison_operator': '=', 'value': '192.168.122.84/10'},
                       {'attribute': 'ipv4-addr:value', 'comparison_operator': '=', 'value': '192.168.122.83'}]
        assert parsing['parsed_stix'] == parsed_stix
        # Time window should be last 5 minutes (300000 ms)
        assert parsing['start_time'] is not None
        assert parsing['end_time'] is not None
        assert parsing['end_time'] - parsing['start_time'] == 300000

    def test_multiple_start_stop_qualifiers(self):
        start_time_01 = "t'2016-06-01T01:30:00.123Z'"
        stop_time_01 = "t'2016-06-01T02:20:00.123Z'"
        start_time_02 = "t'2016-06-01T03:55:00.123Z'"
        stop_time_02 = "t'2016-06-01T04:30:24.743Z'"
        stix_pattern = "[network-traffic:src_port = 37020 AND user-account:user_id = 'root'] START {} STOP {} OR [ipv4-addr:value = '192.168.122.83'] START {} STOP {}".format(start_time_01, stop_time_01, start_time_02, stop_time_02)
        parsing = _parse_query(stix_pattern)
        parsed_stix = [{'attribute': 'user-account:user_id', 'comparison_operator': '=', 'value': 'root'},
                       {'attribute': 'network-traffic:src_port', 'comparison_operator': '=', 'value': 37020},
                       {'attribute': 'ipv4-addr:value', 'comparison_operator': '=', 'value': '192.168.122.83'}]
        assert parsing['parsed_stix'] == parsed_stix
        # The biggest time window should be returned
        assert parsing['start_time'] == 1464744600123
        assert parsing['end_time'] == 1464755424743

    def test_not_equals_operator(self):
        stix_pattern = "[url:value != 'example.com' OR url:value NOT = 'test.com']"
        parsing = _parse_query(stix_pattern)
        parsed_stix = [{'attribute': 'url:value', 'comparison_operator': 'NOT =', 'value': 'test.com'},
                       {'attribute': 'url:value', 'comparison_operator': '!=', 'value': 'example.com'}]
        assert parsing['parsed_stix'] == parsed_stix
        # Time window should be last 5 minutes (300000 ms)
        assert parsing['start_time'] is not None
        assert parsing['end_time'] is not None
        assert parsing['end_time'] - parsing['start_time'] == 300000
