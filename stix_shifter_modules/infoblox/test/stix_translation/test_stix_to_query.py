# -*- coding: utf-8 -*-
import json
import unittest

from stix_shifter.stix_translation.stix_translation import StixTranslation

translation = StixTranslation()


class TestStixParsingMixin:

    @staticmethod
    def get_dialect():
        raise NotImplementedError()

    @staticmethod
    def _parse_query(stix_pattern, dialect):
        query = translation.translate(f'infoblox:{dialect}', 'query', '{}', stix_pattern)
        return query

    def _retrieve_query(self, stix_pattern):
        queries: dict = self._parse_query(stix_pattern, self.get_dialect())
        self.assertIn("queries", queries)
        query = json.loads(queries["queries"][0])
        return query

    def _test_time_range(self, stix_pattern, expectation):
        query = self._retrieve_query(stix_pattern)
        self.assertEqual(expectation, query["to"] - query["from"])

    def _test_pattern(self, pattern, expectation):
        query = self._retrieve_query(pattern)
        self.assertEqual(expectation, query["query"])

    def _test_regex_timestamp(self, pattern, expectation):
        query = self._retrieve_query(pattern)
        self.assertRegex(query["query"], r'^t0=\d{10}&t1=\d{10}&' + expectation)


class TestStixParsingDnsEvent(unittest.TestCase, TestStixParsingMixin):
    def get_dialect(self):
        return "dnsEventData"

    def test_invalid_ipv4_format(self):
        pattern = "[network-traffic:src_ref.value = '{203.0.113.33333333333333333']"
        result = self._parse_query(pattern, self.get_dialect())
        self.assertEqual(result, {
            'success': False,
            'code': 'mapping_error',
            'error': 'data mapping error : Unable to map the following STIX objects and properties to data source fields: []'
        })

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
            'error': 'wrong parameter : Comparison operator Like unsupported for Infoblox connector dnsEventData'
        })

    def test_operator_neq(self):
        pattern = "[domain-name:value != 'microsoft']"
        result = self._parse_query(pattern, self.get_dialect())
        self.assertEqual(result, {
            'success': False,
            'code': 'not_implemented',
            'error': 'wrong parameter : Comparison operator NotEqual unsupported for Infoblox connector dnsEventData'
        })

    def test_multiple_criteria(self):
        pattern = "[network-traffic:src_ref.value = '127.0.0.1' AND network-traffic:src_ref.value = '1.1.1.1']"
        result = self._parse_query(pattern, self.get_dialect())
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
            'error': 'wrong parameter : Comparison operator Or unsupported for Infoblox connector dnsEventData'
        })

    def test_comparison_and(self):
        pattern = "[domain-name:value = 'example.com' AND x-infoblox-dns-event:policy_name = 'DFND']"
        expectation = 'policy_name=DFND&qname=example.com.'
        self._test_regex_timestamp(pattern, expectation)

    def test_combined_observation_expression(self):
        pattern = "[domain-name:value = 'example.com'] AND [x-infoblox-dns-event:policy_name = 'DFND']"
        expectation = 'qname=example.com.&policy_name=DFND'
        self._test_regex_timestamp(pattern, expectation)

    def test_observation_expression_with_qualifier(self):
        pattern = "[domain-name:value = 'example.com' AND x-infoblox-dns-event:policy_name = 'DFND'] START t'2020-06-01T08:43:10Z' STOP t'2020-08-31T10:43:10Z'"
        expectation = 'policy_name=DFND&qname=example.com.'
        self._test_regex_timestamp(pattern, expectation)

    def test_combined_observation_expression_with_qualifier(self):
        pattern = "([domain-name:value = 'example.com'] AND [x-infoblox-dns-event:policy_name = 'DFND']) START t'2020-06-01T08:43:10Z' STOP t'2020-08-31T10:43:10Z'"
        expectation = 'qname=example.com.&policy_name=DFND'
        self._test_regex_timestamp(pattern, expectation)

    def test_multiple_operators(self):
        pattern = "[(domain-name:value = 'example.com' AND x-infoblox-dns-event:policy_name = 'DFND') AND network-traffic:src_ref.value = '127.0.0.1']"
        expectation = 'qip=127.0.0.1&policy_name=DFND&qname=example.com.'
        self._test_regex_timestamp(pattern, expectation)

    def test_multiple_operators_reverse(self):
        pattern = "[network-traffic:src_ref.value = '127.0.0.1' AND (x-infoblox-dns-event:policy_name = 'DFND' AND domain-name:value = 'example.com')]"
        expectation = 'qname=example.com.&policy_name=DFND&qip=127.0.0.1'
        self._test_regex_timestamp(pattern, expectation)

class TestStixParsingDossier(unittest.TestCase, TestStixParsingMixin):
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

    def test_threat_type_host(self):
        pattern = "[domain-name:value = 'example.com']"
        result = self._retrieve_query(pattern)
        self.assertEqual(result, {
            'offset': 0,
            'query': 'value=example.com',
            'source': 'dossierData',
            'threat_type': 'host'
        })

    def test_threat_type_ip_ipv4(self):
        pattern = "[ipv4-addr:value = '1.2.3.4']"
        result = self._retrieve_query(pattern)
        self.assertEqual(result, {
            'offset': 0,
            'query': 'value=1.2.3.4',
            'source': 'dossierData',
            'threat_type': 'ip'
        })

    def test_threat_type_ip_ipv6(self):
        pattern = "[ipv6-addr:value = '2001:db8:3333:4444:5555:6666:7777:8888']"
        result = self._retrieve_query(pattern)
        self.assertEqual(result, {
            'offset': 0,
            'query': 'value=2001:db8:3333:4444:5555:6666:7777:8888',
            'source': 'dossierData',
            'threat_type': 'ip'
        })

    def test_threat_type_ip_ref(self):
        pattern = "[x-infoblox-dossier-event-result-pdns:ip_ref.value = '203.0.113.33']"
        result = self._retrieve_query(pattern)
        self.assertEqual(result, {
            'offset': 0,
            'query': 'value=203.0.113.33',
            'source': 'dossierData',
            'threat_type': 'ip'
        })

    def test_operator_like(self):
        pattern = "[domain-name:value LIKE 'microsoft*']"
        result = self._parse_query(pattern, self.get_dialect())
        self.assertEqual(result, {
            'success': False,
            'code': 'not_implemented',
            'error': 'wrong parameter : Comparison operator Like unsupported for Infoblox connector dossierData'
        })

    def test_operator_neq(self):
        pattern = "[domain-name:value != 'microsoft']"
        result = self._parse_query(pattern, self.get_dialect())
        self.assertEqual(result, {
            'success': False,
            'code': 'not_implemented',
            'error': 'wrong parameter : Comparison operator NotEqual unsupported for Infoblox connector dossierData'
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
            'error': 'wrong parameter : Comparison operator Or unsupported for Infoblox connector dossierData'
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

class TestStixParsingTide(unittest.TestCase, TestStixParsingMixin):
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

    def test_host_like(self):
        pattern = "[x-infoblox-threat:host_name LIKE 'example.com']"
        expectation = 'period=5 minutes&text_search=example.com'
        self._test_pattern(pattern, expectation)

    def test_ipv4(self):
        pattern = "[ipv4-addr:value = '1.2.3.4']"
        expectation = 'period=5 minutes&ip=1.2.3.4'
        self._test_pattern(pattern, expectation)

    def test_ipv4_like(self):
        pattern = "[ipv4-addr:value LIKE '1.2.3.4']"
        expectation = 'period=5 minutes&text_search=1.2.3.4'
        self._test_pattern(pattern, expectation)

    def test_ipv6(self):
        pattern = "[ipv6-addr:value = '2001:db8:3333:4444:5555:6666:7777:8888']"
        expectation = 'period=5 minutes&ip=2001:db8:3333:4444:5555:6666:7777:8888'
        self._test_pattern(pattern, expectation)

    def test_url(self):
        pattern = "[x-infoblox-threat:url = 'https://example.com']"
        expectation = 'period=5 minutes&url=https://example.com'
        self._test_pattern(pattern, expectation)

    def test_url_like(self):
        pattern = "[x-infoblox-threat:url LIKE 'https://example.com']"
        expectation = 'period=5 minutes&text_search=https://example.com'
        self._test_pattern(pattern, expectation)

    def test_domain(self):
        pattern = "[domain-name:value = 'example.com']"
        expectation = 'period=5 minutes&domain=example.com'
        self._test_pattern(pattern, expectation)

    def test_domain_like(self):
        pattern = "[domain-name:value LIKE 'example.com']"
        expectation = 'period=5 minutes&text_search=example.com'
        self._test_pattern(pattern, expectation)

    def test_email(self):
        pattern = "[email-addr:value = 'foo@example.com']"
        expectation = 'period=5 minutes&email=foo@example.com'
        self._test_pattern(pattern, expectation)

    def test_email_like(self):
        pattern = "[email-addr:value LIKE 'foo@example.com']"
        result = self._parse_query(pattern, self.get_dialect())
        self.assertEqual(result, {
            'success': False,
            'code': 'not_implemented',
            'error': 'wrong parameter : Comparison operator Like unsupported for Infoblox connector tideDbData field email'
        })

    def test_tld(self):
        pattern = "[x-infoblox-threat:top_level_domain = 'tld.com']"
        expectation = 'period=5 minutes&tld=tld.com'
        self._test_pattern(pattern, expectation)

    def test_tld_like(self):
        pattern = "[x-infoblox-threat:top_level_domain LIKE 'tld.com']"
        result = self._parse_query(pattern, self.get_dialect())
        self.assertEqual(result, {
            'success': False,
            'code': 'not_implemented',
            'error': 'wrong parameter : Comparison operator Like unsupported for Infoblox connector tideDbData field tld'
        })

    def test_profile(self):
        pattern = "[x-infoblox-threat:profile = 'profile1']"
        expectation = 'period=5 minutes&profile=profile1'
        self._test_pattern(pattern, expectation)

    def test_profile_like(self):
        pattern = "[x-infoblox-threat:profile LIKE 'profile1']"
        expectation = 'period=5 minutes&text_search=profile1'
        self._test_pattern(pattern, expectation)

    def test_origin(self):
        pattern = "[x-infoblox-threat:origin = 'origin1']"
        expectation = 'period=5 minutes&origin=origin1'
        self._test_pattern(pattern, expectation)

    def test_origin_like(self):
        pattern = "[x-infoblox-threat:origin LIKE 'origin1']"
        expectation = 'period=5 minutes&text_search=origin1'
        self._test_pattern(pattern, expectation)

    def test_property(self):
        pattern = "[x-infoblox-threat:property = 'property1']"
        expectation = 'period=5 minutes&property=property1'
        self._test_pattern(pattern, expectation)

    def test_class(self):
        pattern = "[x-infoblox-threat:threat_class = 'class1']"
        expectation = 'period=5 minutes&class=class1'
        self._test_pattern(pattern, expectation)

    def test_class_like(self):
        pattern = "[x-infoblox-threat:threat_class LIKE 'class1']"
        expectation = 'period=5 minutes&text_search=class1'
        self._test_pattern(pattern, expectation)

    def test_threat_level(self):
        pattern = "[x-infoblox-threat:threat_level = 'threatclass1']"
        expectation = 'period=5 minutes&threat_level=threatclass1'
        self._test_pattern(pattern, expectation)

    def test_target(self):
        pattern = "[x-infoblox-threat:target = 'target1']"
        expectation = 'period=5 minutes&target=target1'
        self._test_pattern(pattern, expectation)

    def test_target_like(self):
        pattern = "[x-infoblox-threat:target LIKE 'target1']"
        expectation = 'period=5 minutes&text_search=target1'
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
            'source': 'tideDbData',
            'threat_type': 'host'
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
            'source': 'tideDbData',
            'threat_type': 'email'
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
        pattern = "[email-addr:value = 'example1.com' AND ipv4-addr:value = '1.1.1.1'"
        result = self._parse_query(pattern, self.get_dialect())
        self.assertEqual(result, {
            'success': False,
            'code': 'invalid_parameter',
            'error': 'Error when converting STIX pattern to data source query: Conflicting threat_type found, old=ip new=email'
        })

    def test_comparison_and_imported(self):
        pattern = "[x-infoblox-threat:imported > '2020-08-07' AND ipv4-addr:value = '1.1.1.1'"
        result = self._parse_query(pattern, self.get_dialect())
        self.assertEqual(result, {
            "queries": ['{"offset": 0, "query": "ip=1.1.1.1&imported_from_date=2020-08-07", "threat_type": "ip", "source": "tideDbData"}']
        })

    def test_comparison_and_host(self):
        pattern = "[x-infoblox-threat:host_name = 'example.host.com' AND domain-name:value = 'example.domain.com' AND x-infoblox-threat:profile = 'profile1'"
        result = self._parse_query(pattern, self.get_dialect())
        self.assertEqual(result, {
            "queries": ['{"offset": 0, "query": "period=5 minutes&profile=profile1&domain=example.domain.com&host=example.host.com", "threat_type": "host", "source": "tideDbData"}']
        })

    def test_multiple_operators(self):
        pattern = "[(domain-name:value = 'example.com' AND x-infoblox-threat:ip_ref.value = '1.1.1.1') AND x-infoblox-threat:domain_ref.value = 'example4.com']"
        result = self._parse_query(pattern, self.get_dialect())
        self.assertEqual(result, {
            'success': False,
            'code': 'not_implemented',
            'error': 'wrong parameter : Multiple criteria for one field is not support in Infoblox connector'
        })
