from stix_shifter.stix_translation import stix_translation
from stix_shifter.utils.error_response import ErrorCode

import unittest
import json

translation = stix_translation.StixTranslation()
module = "carbonblack"

def to_json(queries):
    return list(map(lambda x: json.dumps(x), queries))

def _test_query_assertions(query, queries):
    assert query['queries'] == queries

test_options = {"timeRange": None} # retain old behavior (no default time range added) for existing tests

class TestStixToQuery(unittest.TestCase, object):

    def test_file_query(self):
        stix_pattern = "[file:name = 'some_file.exe']"
        query = translation.translate(module, 'query', '{}', stix_pattern, options=test_options)
        queries = to_json([{"query": "observed_filename:some_file.exe", "dialect": "binary"}])
        _test_query_assertions(query, queries)

    def test_file_and_domain_query(self):
        stix_pattern = "[file:name = 'some_file.exe' AND domain-name:value = 'example.com']"
        query = translation.translate(module, 'query', '{}', stix_pattern, options=test_options)
        queries = to_json([{"query": "observed_filename:some_file.exe and domain:example.com", "dialect": "process"}])
        _test_query_assertions(query, queries)

    def test_ipv4_query(self):
        stix_pattern = "[ipv4-addr:value = '10.0.0.1']"
        query = translation.translate(module, 'query', '{}', stix_pattern, options=test_options)
        queries = to_json([{"query": "ipaddr:10.0.0.1", "dialect": "process"}])
        _test_query_assertions(query, queries)

    def test_hash_query(self):
        stix_pattern = "[file:hashes.MD5 = '5746bd7e255dd6a8afa06f7c42c1ba41']"
        query = translation.translate(module, 'query', '{}', stix_pattern, options=test_options)
        queries = to_json([{"query": "md5:5746bd7e255dd6a8afa06f7c42c1ba41", "dialect": "binary"}])
        _test_query_assertions(query, queries)

    def test_command_line_query(self):
        stix_pattern = "[process:command_line = 'cmd.exe']"
        query = translation.translate(module, 'query', '{}', stix_pattern, options=test_options)
        queries = to_json([{"query": "cmdline:cmd.exe", "dialect": "process"}])
        _test_query_assertions(query, queries)

    def test_simple_or_query(self):
        stix_pattern = "[ipv4-addr:value = '10.0.0.1' OR ipv4-addr:value = '10.0.0.2']"
        query = translation.translate(module, 'query', '{}', stix_pattern, options=test_options)
        queries = to_json([{"query": "ipaddr:10.0.0.1 or ipaddr:10.0.0.2", "dialect": "process"}])
        _test_query_assertions(query, queries)

    def test_simple_and_query(self):
        stix_pattern = "[process:name = 'cmd.exe' AND process:creator_user_ref.user_id != 'SYSTEM']"
        query = translation.translate(module, 'query', '{}', stix_pattern, options=test_options)
        queries = to_json([{"query": "process_name:cmd.exe and -(username:SYSTEM)", "dialect": "process"}])
        _test_query_assertions(query, queries)

    def test_custom_mapping(self):
        custom_mappings = {"binary":{}, "process":
                {
                    "file" : {
                        "fields": {
                            "custom_name": ["observed_filename"],
                            }
                        }
                    }
                }
        custom_options = {"mappings" : custom_mappings, "timeRange": None}

        stix_pattern = "[file:custom_name = 'some_file.exe']"
        query = translation.translate(module, 'query', '{}', stix_pattern, custom_options)
        queries = to_json([{"query": "observed_filename:some_file.exe", "dialect": "process"}])
        _test_query_assertions(query, queries)

    def test_query_map_coverage(self):
        stix_to_cb_mapping = {
                "[ipv4-addr:value = '198.51.100.5' AND ipv4-addr:value = '198.51.100.10']" : [{"query": "ipaddr:198.51.100.5 and ipaddr:198.51.100.10", "dialect": "process"}],
                "[process:pid = 4]": [{"query": "process_pid:4", "dialect": "process"}],
                "[process:parent_ref.pid = 7]": [{"query": "parent_pid:7", "dialect": "process"}],
                "[network-traffic:src_port = 80]": [{"query": "ipport:80", "dialect": "process"}],
                "[network-traffic:dst_port = 80]": [{"query": "ipport:80", "dialect": "process"}],
                "[user-account:user_id = 'SYSTEM']": [{"query": "username:SYSTEM", "dialect": "process"}],
                "[process:pid < 4]": [{"query": "process_pid:[* TO 4]", "dialect": "process"}],
                "[process:pid >= 4]": [{"query": "process_pid:[4 TO *]", "dialect": "process"}],
                "[process:pid > 4]": [{"query": "process_pid:[5 TO *]", "dialect": "process"}],
                "[process:pid <= 4]": [{"query": "process_pid:[* TO 5]", "dialect": "process"}],
                "[network-traffic:dst_port > 1024]": [{"query": "ipport:[1025 TO *]", "dialect": "process"}],
                "[file:hashes.MD5 ='79054025255fb1a26e4bc422aef54eb4']": [{"query": "md5:79054025255fb1a26e4bc422aef54eb4", "dialect": "binary"}],
                "[process:name NOT = 'cmd.exe']" : [{"query": "-(process_name:cmd.exe)", "dialect": "process"}],
                "[process:name != 'cmd.exe']" : [{"query": "-(process_name:cmd.exe)", "dialect": "process"}],
                "[process:pid = 4] START t'2019-01-22T00:04:52.937Z' STOP t'2019-02-22T00:04:52.937Z'": [{"query": "((process_pid:4) and start:[2019-01-22T00:04:52 TO *] and last_update:[* TO 2019-02-22T00:04:52])", "dialect": "process"}],
                "[process:pid = 5 OR process:pid = 6] START t'2014-01-13T07:03:17Z' STOP t'2014-01-13T07:03:17Z'": [{"query": "((process_pid:5 or process_pid:6) and start:[2014-01-13T07:03:17 TO *] and last_update:[* TO 2014-01-13T07:03:17])", "dialect": "process"}]
                }
        for stix_pattern, queries in stix_to_cb_mapping.items():
            result = translation.translate(module, 'query', '{}', stix_pattern, options=test_options)
            print(result)
            assert result['queries'] == to_json(queries)

    def test_unmapped_attribute_handling_with_OR(self):
        stix_pattern = "[ipv4-addr:value = '198.51.100.5' OR unmapped:attribute = 'something']"
        translated_query = [{"query": "ipaddr:198.51.100.5", "dialect": "process"}]
        result = translation.translate(module, 'query', '{}', stix_pattern, options=test_options)
        assert result['queries'] == to_json(translated_query)

    def test_unmapped_attribute_handling_with_AND(self):
        stix_pattern = "[ipv4-addr:value = '198.51.100.5' AND unmapped:attribute = 'something']"
        result = translation.translate(module, 'query', '{}', stix_pattern, options=test_options)
        assert result['success'] == False
        assert ErrorCode.TRANSLATION_MAPPING_ERROR.value == result['code']
        assert 'Unable to map the following STIX objects and properties' in result['error']

    def test_escape_query(self):
        stix_to_cb_mapping = {
                "[process:name = ' ']" : [{"query": "process_name:\\ ", "dialect": "process"}],
                "[process:name = '(']" : [{"query": "process_name:\\(", "dialect": "process"}],
                "[process:name = ')']" : [{"query": "process_name:\\)", "dialect": "process"}],
                "[process:name = '\"']" : [{"query": "process_name:\\\"", "dialect": "process"}],
                }
        for stix_pattern, queries in stix_to_cb_mapping.items():
            result = translation.translate(module, 'query', '{}', stix_pattern, options=test_options)
            print(result)
            assert result['queries'] == to_json(queries)

    def test_binary_api_qualifier(self):
        stix_to_cb_mapping = {
                "[file:name = 'cmd.exe'] START t'2019-01-22T00:04:52.937Z' STOP t'2019-02-22T00:04:52.937Z']": [{"query": "((observed_filename:cmd.exe) and server_added_timestamp:[2019-01-22T00:04:52 TO 2019-02-22T00:04:52])", "dialect": "binary"}],
                "[file:hashes.MD5 = '79054025255fb1a26e4bc422aef54eb4']": [{"query": "md5:79054025255fb1a26e4bc422aef54eb4", "dialect": "binary"}],
                "[domain-name:value = 'example.com']": [{"query": "domain:example.com", "dialect": "process"}],
                }
        for stix_pattern, queries in stix_to_cb_mapping.items():
            result = translation.translate("carbonblack", 'query', '{}', stix_pattern, options=test_options)
            print(result)
            assert result['queries'] == to_json(queries)

    def test_merge_apis(self):
        stix_to_cb_mapping = {
                "[process:name = 'cmd.exe']": [{"query": "process_name:cmd.exe", "dialect": "process"}],
                "[process:name = 'cmd.exe' AND file:hashes.MD5 = 'blah']": [{"query": "process_name:cmd.exe and md5:blah", "dialect": "process"}],
                "[process:name = 'cmd.exe' OR file:hashes.MD5 = 'blah']": [{"query": "process_name:cmd.exe or md5:blah", "dialect": "process"}],
                "[file:hashes.MD5 = 'blah']": [{"query": "md5:blah", "dialect": "binary"}],
                "[process:name = 'cmd.exe'] OR [file:hashes.MD5 = 'blah']": [{"query": "process_name:cmd.exe", "dialect": "process"}, {"query": "md5:blah", "dialect": "binary"}],
                "[process:name = 'cmd.exe'] OR [file:hashes.MD5 = 'blah'] OR [process:pid = 5]": [{"query": "(process_name:cmd.exe) or (process_pid:5)", "dialect": "process"}, {"query": "md5:blah", "dialect": "binary"}],
                }
        for stix_pattern, queries in stix_to_cb_mapping.items():
            result = translation.translate("carbonblack", 'query', '{}', stix_pattern, options=test_options)
            print(result)
            assert result['queries'] == to_json(queries)

    def test_nested_parenthesis_in_pattern(self):
        stix_pattern = "[(ipv4-addr:value = '192.168.122.83' OR ipv4-addr:value = '100.100.122.90') AND network-traffic:src_port = 37020 OR user-account:user_id = 'root']"
        query = translation.translate(module, 'query', '{}', stix_pattern, options=test_options)
        queries = to_json([{"query": "((ipaddr:192.168.122.83 or ipaddr:100.100.122.90) and ipport:37020) or username:root", "dialect": "process"}])
        _test_query_assertions(query, queries)

    def test_start_stop_merged(self):
        stix_to_cb_mapping = {
                "[process:name = 'cmd.exe'] OR [file:name = 'notepad.exe'] START t'2014-01-13T07:03:17Z' STOP t'2014-01-13T07:03:17Z'" : [{'query': 'process_name:cmd.exe', 'dialect': 'process'}, {'query': '((observed_filename:notepad.exe) and server_added_timestamp:[2014-01-13T07:03:17 TO 2014-01-13T07:03:17])', 'dialect': 'binary'}],
                "[process:name = 'cmd.exe'] START t'2014-01-13T07:03:17Z' STOP t'2019-01-13T07:03:17Z'  OR [file:name = 'notepad.exe'] START t'2014-01-13T07:03:17Z' STOP t'2014-01-13T07:03:17Z'": [{'query': '((process_name:cmd.exe) and start:[2014-01-13T07:03:17 TO *] and last_update:[* TO 2019-01-13T07:03:17])', 'dialect': 'process'}, {'query': '((observed_filename:notepad.exe) and server_added_timestamp:[2014-01-13T07:03:17 TO 2014-01-13T07:03:17])', 'dialect': 'binary'}],
                "([process:name = 'cmd.exe'] OR [process:name = 'notepad.exe']) START t'2014-01-13T07:03:17Z' STOP t'2014-01-13T07:03:17Z'": [{'query': '(((process_name:cmd.exe) and start:[2014-01-13T07:03:17 TO *] and last_update:[* TO 2014-01-13T07:03:17])) or (((process_name:notepad.exe) and start:[2014-01-13T07:03:17 TO *] and last_update:[* TO 2014-01-13T07:03:17]))', 'dialect': 'process'}],
                "([process:name = 'cmd.exe'] OR [file:name = 'notepad.exe']) START t'2014-01-13T07:03:17Z' STOP t'2014-01-13T07:03:17Z'" : [{'query': '((process_name:cmd.exe) and start:[2014-01-13T07:03:17 TO *] and last_update:[* TO 2014-01-13T07:03:17])', 'dialect': 'process'}, {'query': '((observed_filename:notepad.exe) and server_added_timestamp:[2014-01-13T07:03:17 TO 2014-01-13T07:03:17])', 'dialect': 'binary'}],
                }
        for stix_pattern, queries in stix_to_cb_mapping.items():
            result = translation.translate("carbonblack", 'query', '{}', stix_pattern, options=test_options)
            print(result)
            assert result['queries'] == to_json(queries)

    def test_timerange(self):
        # note queries with a START STOP specifying a query range should not have the default timerange applied
        stix_to_cb_mapping = {
                "[ipv4-addr:value = '127.0.0.1'" : [{'query': '((ipaddr:127.0.0.1) and (start:-5m or last_update:-5m))', 'dialect': 'process'}],
                "[process:name = 'cmd.exe'] OR [file:name = 'notepad.exe'] START t'2014-01-13T07:03:17Z' STOP t'2014-01-13T07:03:17Z'" : [{'query': '((process_name:cmd.exe) and (start:-5m or last_update:-5m))', 'dialect': 'process'}, {'query': '((observed_filename:notepad.exe) and server_added_timestamp:[2014-01-13T07:03:17 TO 2014-01-13T07:03:17])', 'dialect': 'binary'}],
                }
        for stix_pattern, queries in stix_to_cb_mapping.items():
            result = translation.translate("carbonblack", 'query', '{}', stix_pattern, options={"timeRange": 5})
            print(result)
            assert result['queries'] == to_json(queries)
