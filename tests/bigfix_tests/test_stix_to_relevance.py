from stix_shifter import stix_shifter
import unittest

shifter = stix_shifter.StixShifter()


class TestStixToAql(unittest.TestCase, object):

    def test_ipv4_query(self):
        stix_pattern = "[ipv4-addr:value = '192.168.122.83' or ipv4-addr:value = '192.168.122.84']"
        query = shifter.translate('bigfix', 'query', '{}', stix_pattern)
        parsed_stix = [{'attribute': 'ipv4-addr:value', 'comparison_operator': '=', 'value': '192.168.122.84'}, {'attribute': 'ipv4-addr:value', 'comparison_operator': '=', 'value': '192.168.122.83'}]
        assert query == {'queries': stix_pattern, 'parsed_stix': parsed_stix}
