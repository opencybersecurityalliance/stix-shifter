from stix_shifter.stix_translation import stix_translation
from stix_shifter.stix_translation.src.exceptions import DataMappingException
from stix_shifter.stix_translation.src.modules.carbonblack import stix_to_cb

import unittest

translation = stix_translation.StixTranslation()
module = "carbonblack"

class TestStixToCB(unittest.TestCase, object):

    def test_file_query(self):
        stix_pattern = "[file:name = 'some_file.exe']"
        query = translation.translate(module, 'query', '{}', stix_pattern)
        queries = ["process_name:some_file.exe"]
        parsed_stix = [{'attribute': 'file:name', 'comparison_operator': '=', 'value': 'some_file.exe'}]
        assert query == {'queries': queries, 'parsed_stix': parsed_stix}

    def test_file_and_domain_query(self):
        stix_pattern = "[file:name = 'some_file.exe' AND domain-name:value = 'example.com']"
        query = translation.translate(module, 'query', '{}', stix_pattern)
        queries = ["hostname:example.com and process_name:some_file.exe"]
        parsed_stix = [{'attribute': 'domain-name:value', 'comparison_operator': '=', 'value': 'example.com'}, {'attribute': 'file:name', 'comparison_operator': '=', 'value': 'some_file.exe'}]
        assert query == {'queries': queries, 'parsed_stix': parsed_stix}

    def test_ipv4_query(self):
        stix_pattern = "[ipv4-addr:value = '10.0.0.1']"
        query = translation.translate(module, 'query', '{}', stix_pattern)
        queries = ["ipaddr:10.0.0.1"]
        parsed_stix = [{'attribute': 'ipv4-addr:value', 'comparison_operator': '=', 'value': '10.0.0.1'}]
        assert query == {'queries': queries, 'parsed_stix': parsed_stix}

    def test_hash_query(self):
        stix_pattern = "[file:hashes.MD5 = '5746bd7e255dd6a8afa06f7c42c1ba41']"
        query = translation.translate(module, 'query', '{}', stix_pattern)
        queries = ["md5:5746bd7e255dd6a8afa06f7c42c1ba41"]
        parsed_stix = [{'attribute': 'file:hashes.MD5', 'comparison_operator': '=', 'value': '5746bd7e255dd6a8afa06f7c42c1ba41'}]
        assert query == {'queries': queries, 'parsed_stix': parsed_stix}

    def test_command_line_query(self):
        stix_pattern = "[process:command_line = 'cmd.exe']"
        query = translation.translate(module, 'query', '{}', stix_pattern)
        queries = ["cmdline:cmd.exe"]
        parsed_stix = [{'attribute': 'process:command_line', 'comparison_operator': '=', 'value': 'cmd.exe'}]
        assert query == {'queries': queries, 'parsed_stix': parsed_stix}

    def test_simple_or_query(self):
        stix_pattern = "[ipv4-addr:value = '10.0.0.1' OR ipv4-addr:value = '10.0.0.2']"
        query = translation.translate(module, 'query', '{}', stix_pattern)
        queries = ["ipaddr:10.0.0.2 or ipaddr:10.0.0.1"]
        parsed_stix = [{'attribute': 'ipv4-addr:value', 'comparison_operator': '=', 'value': '10.0.0.2'}, {'attribute': 'ipv4-addr:value', 'comparison_operator': '=', 'value': '10.0.0.1'}]
        print(query)
        assert query == {'queries': queries, 'parsed_stix': parsed_stix}
