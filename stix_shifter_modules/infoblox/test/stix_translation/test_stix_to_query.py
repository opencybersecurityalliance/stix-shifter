# -*- coding: utf-8 -*-
import os
import json
import unittest

from stix_shifter.stix_translation.stix_translation import StixTranslation
from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import (
    StartStopQualifier, BaseQualifier
)
from stix_shifter_modules.infoblox.stix_translation.query_constructor import QueryStringPatternTranslator

translation = StixTranslation()

class StartStopQualifier(BaseQualifier):
    def __init__(self):
        self.expression = "test"

class DataModelMapper:
    def __init__(self):
        self.dialect = "dialect"

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

    def _test_regex_timestamp(self, pattern, expectation):
        query = self._retrieve_query(pattern)
        self.assertRegex(query["query"], r'^t0=\d{10}&t1=\d{10}&' + expectation)

class TestStixParsing(unittest.TestCase, TestStixParsingMixin):
    def test_unknown_expression_type(self):
        pattern = StartStopQualifier()
        with self.assertRaises(Exception) as context:
            QueryStringPatternTranslator(pattern, DataModelMapper(), None)

        expectedString = 'Unknown Recursion Case for expression=<stix_shifter_modules.infoblox.test.stix_translation.test_stix_to_query.StartStopQualifier object'
        self.assertIn(expectedString, str(context.exception))

class TestStixParsingDnsEvent(unittest.TestCase, TestStixParsingMixin):
    @staticmethod
    def get_dialect():
        return "dnsEventData"

    def test_dynamic_timestamp_without_qualifier(self):
        pattern = "[ipv4-addr:value = '127.0.0.1']"
        expectation = 'qip=127.0.0.1'
        self._test_regex_timestamp(pattern, expectation)

class TestStixParsing(unittest.TestCase, TestStixParsingMixin):
    def _get_test_cases(self):
        dn = os.path.dirname(os.path.realpath(__file__))
        fn = os.path.join(dn,"test_stix_to_query_parsing.json")
        filehandler = open(fn, "r")
        return json.load(filehandler)

    def test_query_parsing(self):
        patterns = []
        testCases = self._get_test_cases()
        for case in testCases:
            patterns.append(case['pattern'])
            for dialect in ['tideDbData', 'dnsEventData', 'dossierData']:
                with self.subTest(msg="query parser", dialect=dialect, pattern=case['pattern']):
                    result = self._parse_query(case['pattern'], dialect)
                    expected = case['expected'][dialect]
                    if 'success' in result:
                        self.assertEqual(result.get('code'), expected.get('code'), "dialect={}, full result={}".format(dialect, result))
                    else:
                        self.assertEqual(result, expected, "dialect={}, full result={}".format(dialect, result))
        with self.subTest(msg="unique pattern tester", total_patterns=len(patterns)):
            duplicates = set([x for x in patterns if patterns.count(x) > 1])
            self.assertEqual(len(duplicates), 0, "duplicate patterns={}".format(duplicates))

