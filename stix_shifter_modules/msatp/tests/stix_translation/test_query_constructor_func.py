from stix_shifter_modules.msatp.stix_translation import query_constructor
from stix_shifter_modules.msatp.stix_translation.query_constructor import QueryStringPatternTranslator
import unittest


class MergeDictTests(unittest.TestCase):
    def test_with_overlapping_keys(self):
        dict_01 = {1: 'a', 2: 'b', 3: 'c', 4: 'd'}
        dict_02 = {1: 'a', 2: 'b', 3: 'c', 4: 'd'}
        expected_res = {1: ['a', 'a'], 2: ['b', 'b'], 3: ['c', 'c'], 4: ['d', 'd']}
        self.assertDictEqual(QueryStringPatternTranslator.mergeDict(dict_01, dict_02), expected_res, "incorrect result")

    def test_without_overlapping_keys(self):
        dict_01 = {1: 'a', 2: 'b', 3: 'c', 4: 'd'}
        dict_02 = {5: 'e', 6: 'f', 7: 'g', 8: 'h'}
        expected_res = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h'}
        self.assertDictEqual(QueryStringPatternTranslator.mergeDict(dict_01, dict_02), expected_res, "incorrect result")

    def test_with_empty_map(self):
        dict_01 = {1: 'a', 2: 'b'}
        dict_02 = {}
        self.assertDictEqual(QueryStringPatternTranslator.mergeDict(dict_01, dict_02), dict_01, "incorrect result")


class ConstructIntersecMap(unittest.TestCase):
    def test_non_empty_intersection(self):
        dict_01 = {1: 'a', 2: 'b', 3: 'c'}
        dict_02 = {1: 'a', 2: 'b', 4: 'd'}
        expected_res = {1: ['a', 'a'], 2: ['b', 'b']}
        self.assertDictEqual(QueryStringPatternTranslator.construct_intesec_map(dict_01, dict_02), expected_res,
                             "incorrect result")

    def test_empty_intersection(self):
        dict_01 = {1: 'a', 2: 'b', 3: 'c'}
        dict_02 = {4: 'd', 5: 'e', 6: 'f'}
        self.assertDictEqual(QueryStringPatternTranslator.construct_intesec_map(dict_01, dict_02), {},
                             "incorrect result")

    def test_with_empty_map(self):
        dict_01 = {1: 'a', 2: 'b'}
        dict_02 = {}
        self.assertDictEqual(QueryStringPatternTranslator.construct_intesec_map(dict_01, dict_02), dict_02, "incorrect result")


    def test_construct_and_op_map(self):
        test_mep_01 = {"DeviceNetworkEvents": 'DeviceName =~ "2.client-channel.google.com"',
                       "DeviceProcessEvents": 'InitiatingProcessFileName =~ "WmiPrvSE.exe"'}
        test_map_02 = {"DeviceNetworkEvents": 'InitiatingProcessFileName =~ "demo-gthread-3.6.dll"'}
        expected_res = {"DeviceNetworkEvents": '(InitiatingProcessFileName =~ "demo-gthread-3.6.dll") and (DeviceName '
                                               '=~ "2.client-channel.google.com")'}
        self.assertDictEqual(QueryStringPatternTranslator.construct_and_op_map(test_mep_01, test_map_02), expected_res, "incorrect result")

    def test_construct_and_op_map_with_empty_map(self):
        test_mep_01 = {}
        test_map_02 = {"DeviceNetworkEvents": 'InitiatingProcessFileName =~ "demo-gthread-3.6.dll"'}
        self.assertDictEqual(QueryStringPatternTranslator.construct_and_op_map(test_mep_01, test_map_02), {}, "incorrect result")

    def test_construct_and_op_map_with_empty_intersec(self):
        test_mep_01 = {"DeviceProcessEvents": 'InitiatingProcessFileName =~ "WmiPrvSE.exe"'}
        test_map_02 = {"DeviceNetworkEvents": 'InitiatingProcessFileName =~ "demo-gthread-3.6.dll"'}
        self.assertDictEqual(QueryStringPatternTranslator.construct_and_op_map(test_mep_01, test_map_02), {}, "incorrect result")


class ParseTimeRangeExc(unittest.TestCase):
    def test_parse_time_range_exception(self):
        with self.assertRaises(Exception) as context:
            QueryStringPatternTranslator._parse_time_range(None, None)


class ParseExpressionExc(unittest.TestCase):
    def test_parse_expression_exception(self):
        with self.assertRaises(Exception) as context:
            QueryStringPatternTranslator._parse_expression(None)






