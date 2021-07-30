# -*- coding: utf-8 -*-
import json
import unittest

from . import utils

class TestStixParsingTide(unittest.TestCase, utils.TestStixParsingMixin):
    def get_dialect(self):
        return "tideDbData"

    def test_hostname(self):
        pattern = "[domain-name:value = 'example.com']"
        expectation = 'domain=example.com'
        self._test_pattern(pattern, expectation)

    def test_email(self):
        pattern = "[email-addr:value = 'foo@example.com']"
        expectation = 'email=foo@example.com'
        self._test_pattern(pattern, expectation)

    def test_ip(self):
        pattern = "[ipv4-addr:value = '1.2.3.4']"
        expectation = 'ip=1.2.3.4'
        self._test_pattern(pattern, expectation)

    # TODO: test references
    # TODO: test like operator
    # TODO: test neq operator
    # TODO: test observation and/or
    # TODO: test multiple operators
    # TODO: test multiple criteria (same op like ipv4-addr:value='127.0.0.1' OR  ipv4-addr:value='127.0.0.2')
    # TODO: test and/or comparision
