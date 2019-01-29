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
        assert query == {'queries': queries, 'parsed_stix': parsed_stix}

    def test_query_map_coverage(self):
        stix_to_cb_mapping = {
                "[ipv4-addr:value = '198.51.100.5' AND ipv4-addr:value = '198.51.100.10']" : "ipaddr:198.51.100.10 and ipaddr:198.51.100.5",
                "[process:pid = 4]": "process_pid:4",
                "[process:parent_ref.pid = 7]": "parent_pid:7",
                "[network-traffic:src_port = 80]": "ipport:80",
                "[network-traffic:dst_port = 80]": "ipport:80",
                "[user-account:user_id = 'SYSTEM']": "username:SYSTEM",
                "[process:pid < 4]": "process_pid:[* TO 4]",
                "[process:pid >= 4]": "process_pid:[4 TO *]",
                "[file:hashes.MD5 ='79054025255fb1a26e4bc422aef54eb4']": "md5:79054025255fb1a26e4bc422aef54eb4",
                "[process:name NOT = 'cmd.exe']" : "-(process_name:cmd.exe)",
                "[process:name != 'cmd.exe']" : "-(process_name:cmd.exe)",
                "[process:pid = 4 START t'2019-01-22T00:04:52.937Z' STOP t'2019-02-22T00:04:52.937Z']": "((process_pid:4) and start:[2019-01-22T00:04:52 TO *] and last_update:[* TO 2019-02-22T00:04:52])",

                }
        for stix_pattern, query in stix_to_cb_mapping.items():
            result = translation.translate(module, 'query', '{}', stix_pattern)
            print(result)
            assert result['queries'] == [query]

    def test_nested_parenthesis_in_pattern(self):
        stix_pattern = "[(ipv4-addr:value = '192.168.122.83' or ipv4-addr:value = '100.100.122.90') and network-traffic:src_port = 37020] or [user-account:user_id = 'root']"
        query = translation.translate(module, 'query', '{}', stix_pattern)
        parsed_stix = [
            {'attribute': 'network-traffic:src_port', 'comparison_operator': '=', 'value': 37020},
            {'attribute': 'ipv4-addr:value', 'comparison_operator': '=', 'value': '100.100.122.90'},
            {'attribute': 'user-account:user_id', 'comparison_operator': '=', 'value': 'root'},
            {'attribute': 'ipv4-addr:value', 'comparison_operator': '=', 'value': '192.168.122.83'}
        ]
        print(query)
        desired_result = "(ipaddr:192.168.122.83 or ipaddr:100.100.122.90 ) and ipport:37020 or username:root"
        print("desired_result ", desired_result)
        #assert(query["queries"] == [desired_result])
        #assert(False)
