# -*- coding: utf-8 -*-
import json
import unittest

from . import utils

class TestStixParsingDnsEvent(unittest.TestCase, utils.TestStixParsingMixin):
    def get_dialect(self):
        return "dnsEventData"

    def test_start_end_time(self):
        pattern = "[ipv4-addr:value = '127.0.0.1'] START t'2020-06-01T08:43:10Z' STOP t'2020-08-31T10:43:10Z'"
        expectation = 't0=1591000990&t1=1598870590&qip=127.0.0.1'
        self._test_pattern(pattern, expectation)

    def test_network(self):
        pattern = "[x-infoblox-dns-event:network = 'BloxOne Endpoint']"
        expectation = 'network=BloxOne Endpoint'
        self._test_regex_timestamp(pattern, expectation)
        pass

    def test_ipv4(self):
        pattern = "[ipv4-addr:value = '127.0.0.1']"
        expectation = 'qip=127.0.0.1'
        self._test_regex_timestamp(pattern, expectation)

    def test_domain_name(self):
        pattern = "[domain-name:value = 'example.com']"
        expectation = 'qname=example.com.'
        self._test_regex_timestamp(pattern, expectation)

    def test_policy_name(self):
        pattern = "[x-infoblox-dns-event:policy_name = 'DFND']"
        expectation = 'policy_name=DFND'
        self._test_regex_timestamp(pattern, expectation)

    def test_severity(self):
        pattern = "[x-infoblox-dns-event:x_infoblox_severity = 'HIGH']"
        expectation = 'threat_level=3'
        self._test_regex_timestamp(pattern, expectation)

    def test_threat_class(self):
        pattern = "[x-infoblox-dns-event:threat_class = 'APT']"
        expectation = 'threat_class=APT'
        self._test_regex_timestamp(pattern, expectation)

    def test_network_domain_ref(self):
        pattern = "[network-traffic:extensions.'dns-ext'.question.domain_ref.value = 'example1.com']"
        expectation = 'qname=example1.com.'
        self._test_regex_timestamp(pattern, expectation)

    def test_network_src_ref(self):
        pattern = "[network-traffic:src_ref.value = '203.0.113.33']"
        expectation = 'qip=203.0.113.33'
        self._test_regex_timestamp(pattern, expectation)

    def test_operator_like(self):
        pattern = "[domain-name:value LIKE 'microsoft*']"
        result = self._parse_query(pattern, self.get_dialect())
        self.assertEqual(result, {
            'success': False,
            'code': 'not_implemented',
            'error': 'wrong parameter : Comparison operator Like unsupported for Infoblox connector'
        })

    def test_operator_neq(self):
        pattern = "[domain-name:value != 'microsoft']"
        result = self._parse_query(pattern, self.get_dialect())
        self.assertEqual(result, {
            'success': False,
            'code': 'not_implemented',
            'error': 'wrong parameter : Comparison operator NotEqual unsupported for Infoblox connector'
        })

    def test_multiple_criteria(self):
        pattern = "[network-traffic:src_ref.value = '127.0.0.1' AND network-traffic:src_ref.value = '1.1.1.1']"
        result = self._parse_query(pattern, self.get_dialect())
        self._parse_query(pattern, self.get_dialect())
        self.assertEqual(result, {
            'success': False,
            'code': 'not_implemented',
            'error': 'wrong parameter : Multiple criteria for one field is not support in Infoblox connector'
        })

    def test_comparison_or(self):
        pattern = "[domain-name:value = 'example.com' OR x-infoblox-dns-event:policy_name = 'DFND'"
        result = self._parse_query(pattern, self.get_dialect())
        self.assertEqual(result, {
            'success': False,
            'code': 'not_implemented',
            'error': 'wrong parameter : Comparison operator Or unsupported for Infoblox connector'
        })

    def test_comparison_and(self):
        pattern = "[domain-name:value = 'example.com' AND x-infoblox-dns-event:policy_name = 'DFND']"
        expectation = 'policy_name=DFND&qname=example.com.'
        self._test_regex_timestamp(pattern, expectation)

    def test_multiple_operators(self):
        pattern = "[(domain-name:value = 'example.com' AND x-infoblox-dns-event:policy_name = 'DFND') AND network-traffic:src_ref.value = '127.0.0.1']"
        expectation = 'qip=127.0.0.1&policy_name=DFND&qname=example.com.'
        self._test_regex_timestamp(pattern, expectation)
