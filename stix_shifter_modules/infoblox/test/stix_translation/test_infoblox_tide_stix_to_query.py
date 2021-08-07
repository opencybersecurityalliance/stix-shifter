# -*- coding: utf-8 -*-
import json
import unittest

from . import utils

class TestStixParsingTide(unittest.TestCase, utils.TestStixParsingMixin):
    def get_dialect(self):
        return "tideDbData"

    def test_start_end_time(self):
        pattern = "[ipv4-addr:value = '127.0.0.1'] START t'2017-07-24T17:27:39.423Z' STOP t'2017-07-24T17:27:39.423Z'"
        expectation = 'from_date=2017-07-24T17:27:39.423Z&to_date=2017-07-24T17:27:39.423Z&ip=127.0.0.1'
        self._test_pattern(pattern, expectation)

    def test_id(self):
        pattern = "[x-infoblox-threat:id = 'uuid1']"
        expectation = 'period=5 minutes&id=uuid1'
        self._test_pattern(pattern, expectation)

    def test_host(self):
        pattern = "[x-infoblox-threat:host_name = 'example.com']"
        expectation = 'period=5 minutes&host=example.com'
        self._test_pattern(pattern, expectation)

    def test_ipv4(self):
        pattern = "[ipv4-addr:value = '1.2.3.4']"
        expectation = 'period=5 minutes&ip=1.2.3.4'
        self._test_pattern(pattern, expectation)

    def test_ipv6(self):
        pattern = "[ipv6-addr:value = '2001:db8:3333:4444:5555:6666:7777:8888']"
        expectation = 'period=5 minutes&ip=2001:db8:3333:4444:5555:6666:7777:8888'
        self._test_pattern(pattern, expectation)

    def test_url(self):
        pattern = "[x-infoblox-threat:url = 'https://example.com']"
        expectation = 'period=5 minutes&url=https://example.com'
        self._test_pattern(pattern, expectation)

    def test_domain(self):
        pattern = "[domain-name:value = 'example.com']"
        expectation = 'period=5 minutes&domain=example.com'
        self._test_pattern(pattern, expectation)

    def test_email(self):
        pattern = "[email-addr:value = 'foo@example.com']"
        expectation = 'period=5 minutes&email=foo@example.com'
        self._test_pattern(pattern, expectation)

    def test_tld(self):
        pattern = "[x-infoblox-threat:top_level_domain = 'tld.com']"
        expectation = 'period=5 minutes&tld=tld.com'
        self._test_pattern(pattern, expectation)

    def test_profile(self):
        pattern = "[x-infoblox-threat:profile = 'profile1']"
        expectation = 'period=5 minutes&profile=profile1'
        self._test_pattern(pattern, expectation)

    def test_origin(self):
        pattern = "[x-infoblox-threat:origin = 'origin1']"
        expectation = 'period=5 minutes&origin=origin1'
        self._test_pattern(pattern, expectation)

    def test_property(self):
        pattern = "[x-infoblox-threat:property = 'property1']"
        expectation = 'period=5 minutes&property=property1'
        self._test_pattern(pattern, expectation)

    def test_class(self):
        pattern = "[x-infoblox-threat:threat_class = 'class1']"
        expectation = 'period=5 minutes&class=class1'
        self._test_pattern(pattern, expectation)

    def test_threat_level(self):
        pattern = "[x-infoblox-threat:threat_level = 'threatclass1']"
        expectation = 'period=5 minutes&threat_level=threatclass1'
        self._test_pattern(pattern, expectation)

    def test_target(self):
        pattern = "[x-infoblox-threat:target = 'target1']"
        expectation = 'period=5 minutes&target=target1'
        self._test_pattern(pattern, expectation)

    def test_expiration(self):
        pattern = "[x-infoblox-threat:expiration = '2021-05-24T20:26:04.000Z']"
        expectation = 'expiration=2021-05-24T20:26:04.000Z'
        self._test_pattern(pattern, expectation)

    def test_imported_eq(self):
        pattern = "[x-infoblox-threat:imported = '2021-05-24T20:26:04.000Z']"
        result = self._parse_query(pattern, self.get_dialect())
        self.assertEqual(result, {
            'success': False,
            'code': 'invalid_parameter',
            'error': 'Error when converting STIX pattern to data source query: Equal'
        })

    def test_imported_from_eq(self):
        pattern = "[x-infoblox-threat:imported > '2021-05-24T20:26:04.000Z']"
        expectation = 'imported_from_date=2021-05-24T20:26:04.000Z'
        self._test_pattern(pattern, expectation)

    def test_imported_from_geq(self):
        pattern = "[x-infoblox-threat:imported >= '2021-05-24T20:26:04.000Z']"
        expectation = 'imported_from_date=2021-05-24T20:26:04.000Z'
        self._test_pattern(pattern, expectation)

    def test_imported_to_eq(self):
        pattern = "[x-infoblox-threat:imported < '2021-05-24T20:26:04.000Z']"
        expectation = 'imported_to_date=2021-05-24T20:26:04.000Z'
        self._test_pattern(pattern, expectation)

    def test_imported_to_leq(self):
        pattern = "[x-infoblox-threat:imported <= '2021-05-24T20:26:04.000Z']"
        expectation = 'imported_to_date=2021-05-24T20:26:04.000Z'
        self._test_pattern(pattern, expectation)

    def test_imported_from_to(self):
        pattern = "[x-infoblox-threat:imported > '2021-05-24T20:26:04.000Z' AND x-infoblox-threat:imported < '2021-06-24T20:26:04.000Z']"
        expectation = 'imported_to_date=2021-06-24T20:26:04.000Z&imported_from_date=2021-05-24T20:26:04.000Z'
        self._test_pattern(pattern, expectation)

    def test_derivative(self):
        pattern = "[x-infoblox-threat:derivative = 'true']"
        expectation = 'period=5 minutes&derivative=true'
        self._test_pattern(pattern, expectation)

    def test_dga(self):
        pattern = "[x-infoblox-threat:dga = 'true']"
        expectation = 'period=5 minutes&dga=true'
        self._test_pattern(pattern, expectation)

    def test_up(self):
        pattern = "[x-infoblox-threat:active = 'true']"
        expectation = 'period=5 minutes&up=true'
        self._test_pattern(pattern, expectation)

    def test_confidence(self):
        pattern = "[x-infoblox-threat:x_infoblox_confidence = '50']"
        expectation = 'period=5 minutes&confidence=50'
        self._test_pattern(pattern, expectation)

    def test_expiration(self):
        pattern = "[x-infoblox-threat:expiration = '2021-05-24T20:26:04.000Z']"
        expectation = 'expiration=2021-05-24T20:26:04.000Z'
        self._test_pattern(pattern, expectation)

    def test_hash(self):
        pattern = "[x-infoblox-threat:hash = 'hash1']"
        expectation = 'period=5 minutes&hash=hash1'
        self._test_pattern(pattern, expectation)

    def test_threat_type(self):
        pattern = "[x-infoblox-threat:threat_type = 'HOST']"
        result = self._retrieve_query(pattern)
        self.assertEqual(result, {
            'offset': 0,
            'query': 'period=5 minutes&type=host',
            'source': 'tideDbData'
        })

    def test_operator_like(self):
        pattern = "[domain-name:value LIKE 'microsoft*']"
        result = self._parse_query(pattern, self.get_dialect())
        self.assertEqual(result, {
            'success': False,
            'code': 'not_implemented',
            'error': 'wrong parameter : Comparison operator Like unsupported for Infoblox connector tideDbData'
        })

    def test_operator_neq(self):
        pattern = "[domain-name:value != 'microsoft']"
        result = self._parse_query(pattern, self.get_dialect())
        self.assertEqual(result, {
            'success': False,
            'code': 'not_implemented',
            'error': 'wrong parameter : Comparison operator NotEqual unsupported for Infoblox connector tideDbData'
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
            'error': 'wrong parameter : Comparison operator Or unsupported for Infoblox connector tideDbData'
        })

    def test_ip_ref(self):
        pattern = "[x-infoblox-threat:ip_ref.value = '1.1.1.2']"
        result = self._retrieve_query(pattern)
        self.assertEqual(result, {
            'offset': 0,
            'query': 'period=5 minutes&ip=1.1.1.2',
            'source': 'tideDbData',
            'threat_type': 'ip'
        })

    def test_email_ref(self):
        pattern = "[x-infoblox-threat:email_ref.value = 'foo@example.com']"
        result = self._retrieve_query(pattern)
        self.assertEqual(result, {
            'offset': 0,
            'query': 'period=5 minutes&email=foo@example.com',
            'source': 'tideDbData'
        })

    def test_domain_ref(self):
        pattern = "[x-infoblox-threat:domain_ref.value = 'example.com']"
        result = self._retrieve_query(pattern)
        self.assertEqual(result, {
            'offset': 0,
            'query': 'period=5 minutes&domain=example.com',
            'source': 'tideDbData'
        })

    def test_comparison_different_threat_type(self):
        pattern = "[domain-name:value = 'example1.com' AND ipv4-addr:value = '1.1.1.1'"
        result = self._parse_query(pattern, self.get_dialect())
        self.assertEqual(result, {
            'success': False,
            'code': 'invalid_parameter',
            'error': 'Error when converting STIX pattern to data source query: Conflicting threat_type found, old=ip new=host'
        })

    def test_comparison_and(self):
        pattern = "[x-infoblox-threat:imported > '2020-08-07' AND ipv4-addr:value = '1.1.1.1'"
        result = self._parse_query(pattern, self.get_dialect())
        self.assertEqual(result, {
            "queries": ['{"offset": 0, "query": "ip=1.1.1.1&imported_from_date=2020-08-07", "threat_type": "ip", "source": "tideDbData"}']
        })

    def test_multiple_operators(self):
        pattern = "[(domain-name:value = 'example.com' AND x-infoblox-threat:ip_ref.value = '1.1.1.1') AND x-infoblox-threat:domain_ref.value = 'example4.com']"
        result = self._parse_query(pattern, self.get_dialect())
        self.assertEqual(result, {
            'success': False,
            'code': 'not_implemented',
            'error': 'wrong parameter : Multiple criteria for one field is not support in Infoblox connector'
        })
