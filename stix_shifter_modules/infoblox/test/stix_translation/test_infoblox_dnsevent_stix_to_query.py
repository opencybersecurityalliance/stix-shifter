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
        self._test_pattern(pattern, expectation)
        pass

    def test_ipv4(self):
        pattern = "[ipv4-addr:value = '127.0.0.1']"
        expectation = 'qip=127.0.0.1'
        self._test_pattern(pattern, expectation)

    def test_domain_name(self):
        pattern = "[domain-name:value = 'example.com']"
        expectation = 'qname=example.com.'
        self._test_pattern(pattern, expectation)

    def test_policy_name(self):
        pattern = "[x-infoblox-dns-event:policy_name = 'DFND']"
        expectation = 'policy_name=DFND'
        self._test_pattern(pattern, expectation)

    def test_severity(self):
        pattern = "[x-infoblox-dns-event:x_infoblox_severity = 'HIGH']"
        expectation = 'threat_level=3'
        self._test_pattern(pattern, expectation)

    def test_threat_class(self):
        pattern = "[x-infoblox-dns-event:threat_class = 'APT']"
        expectation = 'threat_class=APT'
        self._test_pattern(pattern, expectation)

    # TODO: test references
    # TODO: test like operator
    # TODO: test neq operator
    # TODO: test observation and/or
    # TODO: test multiple operators
    # TODO: test multiple criteria (same op like ipv4-addr:value='127.0.0.1' OR  ipv4-addr:value='127.0.0.2')
    # TODO: test and/or comparision
