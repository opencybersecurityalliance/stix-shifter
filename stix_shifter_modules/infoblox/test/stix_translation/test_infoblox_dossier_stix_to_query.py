# -*- coding: utf-8 -*-
import json
import unittest

from . import utils

class TestStixParsingDossier(unittest.TestCase, utils.TestStixParsingMixin):
    def get_dialect(self):
        return "dossierData"

    def test_hostname(self):
        pattern = "[domain-name:value = 'example.com']"
        expectation = 'value=example.com'
        self._test_pattern(pattern, expectation)

    def test_ipv4(self):
        pattern = "[ipv4-addr:value = '1.2.3.4']"
        expectation = 'value=1.2.3.4'
        self._test_pattern(pattern, expectation)

    def test_ipv6(self):
        pattern = "[ipv6-addr:value = '2001:db8:3333:4444:5555:6666:7777:8888']"
        expectation = 'value=2001:db8:3333:4444:5555:6666:7777:8888'
        self._test_pattern(pattern, expectation)

    def test_hostname_ref(self):
        pattern = "[x-infoblox-dossier-event-result-pdns:hostname_ref.value = 'example1.com']"
        expectation = 'value=example1.com'
        self._test_pattern(pattern, expectation)

    def test_ip_ref(self):
        pattern = "[x-infoblox-dossier-event-result-pdns:ip_ref.value = '203.0.113.33']"
        expectation = 'value=203.0.113.33'
        self._test_pattern(pattern, expectation)

    def test_subtype_host(self):
        pattern = "[domain-name:value = 'example.com']"
        result = self._retrieve_query(pattern)
        self.assertEqual(result, {
            'offset': 0,
            'query': 'value=example.com',
            'source': 'dossierData',
            'subtype': 'host'
        })

    def test_subtype_ip_ipv4(self):
        pattern = "[ipv4-addr:value = '1.2.3.4']"
        result = self._retrieve_query(pattern)
        self.assertEqual(result, {
            'offset': 0,
            'query': 'value=1.2.3.4',
            'source': 'dossierData',
            'subtype': 'ip'
        })

    def test_subtype_ip_ipv6(self):
        pattern = "[ipv6-addr:value = '2001:db8:3333:4444:5555:6666:7777:8888']"
        result = self._retrieve_query(pattern)
        self.assertEqual(result, {
            'offset': 0,
            'query': 'value=2001:db8:3333:4444:5555:6666:7777:8888',
            'source': 'dossierData',
            'subtype': 'ip'
        })

    def test_subtype_ip_ref(self):
        pattern = "[x-infoblox-dossier-event-result-pdns:ip_ref.value = '203.0.113.33']"
        result = self._retrieve_query(pattern)
        self.assertEqual(result, {
            'offset': 0,
            'query': 'value=203.0.113.33',
            'source': 'dossierData',
            'subtype': 'ip'
        })

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
        pattern = "[domain-name:value = 'example2.com' AND domain-name:value = 'example3.com']"
        result = self._parse_query(pattern, self.get_dialect())
        self._parse_query(pattern, self.get_dialect())
        self.assertEqual(result, {
            'success': False,
            'code': 'not_implemented',
            'error': 'wrong parameter : Multiple criteria for one field is not support in Infoblox connector'
        })

    def test_comparison_or(self):
        pattern = "[domain-name:value = 'example1.com' OR ipv4-addr:value = '1.1.1.1'"
        result = self._parse_query(pattern, self.get_dialect())
        self.assertEqual(result, {
            'success': False,
            'code': 'not_implemented',
            'error': 'wrong parameter : Comparison operator Or unsupported for Infoblox connector'
        })

    def test_comparison_and(self):
        pattern = "[domain-name:value = 'example1.com' AND ipv4-addr:value = '1.1.1.1'"
        result = self._parse_query(pattern, self.get_dialect())
        self.assertEqual(result, {
            'success': False,
            'code': 'not_implemented',
            'error': 'wrong parameter : Multiple criteria for one field is not support in Infoblox connector'
        })

    def test_multiple_operators(self):
        pattern = "[(domain-name:value = 'example.com' AND x-infoblox-dossier-event-result-pdns:ip_ref.value = '1.1.1.1') AND x-infoblox-dossier-event-result-pdns:hostname_ref.value = 'example4.com']"
        result = self._parse_query(pattern, self.get_dialect())
        self.assertEqual(result, {
            'success': False,
            'code': 'not_implemented',
            'error': 'wrong parameter : Multiple criteria for one field is not support in Infoblox connector'
        })
