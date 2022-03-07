from stix_shifter.stix_translation import stix_translation
from stix_shifter_utils.utils.error_response import ErrorCode

import unittest
import json

translation = stix_translation.StixTranslation()
module = "carbonblack"

def to_json(queries):
    return list(map(lambda x: json.dumps(x), queries))

def _test_query_assertions(query, queries):
    assert query['queries'] == queries

test_options = {"time_range": None} # retain old behavior (no default time range added) for existing tests

class TestQueryTranslator(unittest.TestCase, object):

    def test_file_query(self):
        test_options = {"time_range": None} 
        stix_pattern = "[file:name = 'some_file.exe']"
        query = translation.translate(module, 'query', '{}', stix_pattern, options=test_options)
        queries = ["(process_name:some_file.exe or childproc_name:some_file.exe)"]
        _test_query_assertions(query, queries)

    def test_file_and_domain_query(self):
        test_options = {"time_range": None} 
        stix_pattern = "[file:name = 'some_file.exe' AND domain-name:value = 'example.com']"
        query = translation.translate(module, 'query', '{}', stix_pattern, options=test_options)
        queries = ["((process_name:some_file.exe or childproc_name:some_file.exe) and (domain:example.com or hostname:example.com))"]
        _test_query_assertions(query, queries)

    def test_ipv4_query(self):
        stix_pattern = "[ipv4-addr:value = '10.0.0.1']"
        query = translation.translate(module, 'query', '{}', stix_pattern)
        queries = ["ipaddr:10.0.0.1 and last_update:-5m"]
        _test_query_assertions(query, queries)

    def test_hash_query(self):
        stix_pattern = "[file:hashes.MD5 = '5746bd7e255dd6a8afa06f7c42c1ba41']"
        query = translation.translate(module, 'query', '{}', stix_pattern)
        queries = ["md5:5746bd7e255dd6a8afa06f7c42c1ba41 and last_update:-5m"]
        _test_query_assertions(query, queries)

    def test_command_line_query(self):
        test_options = {"time_range": None} 
        stix_pattern = "[process:command_line = 'cmd.exe']"
        query = translation.translate(module, 'query', '{}', stix_pattern, options=test_options)
        queries = ["cmdline:cmd.exe"]
        _test_query_assertions(query, queries)

    def test_simple_or_query(self):
        test_options = {"time_range": None} 
        stix_pattern = "[ipv4-addr:value = '10.0.0.1' OR ipv4-addr:value = '10.0.0.2']"
        query = translation.translate(module, 'query', '{}', stix_pattern, options=test_options)
        queries = ["(ipaddr:10.0.0.1 or ipaddr:10.0.0.2)"]
        _test_query_assertions(query, queries)

    def test_simple_and_query(self):
        test_options = {"time_range": None} 
        stix_pattern = "[process:name = 'cmd.exe' AND process:creator_user_ref.user_id != 'SYSTEM']"
        query = translation.translate(module, 'query', '{}', stix_pattern, options=test_options)
        queries = ["((process_name:cmd.exe or crossproc_name:cmd.exe) and -username:SYSTEM)"]
        _test_query_assertions(query, queries)

    def test_custom_mapping(self):
        custom_mappings = {
            "from_stix_map": {
                "file" : {
                    "fields": {
                        "custom_name": ["observed_filename"],
                    }
                }
            }
        }
        custom_options = {"mapping" : custom_mappings, "time_range": None}

        stix_pattern = "[file:custom_name = 'some_file.exe']"
        query = translation.translate(module, 'query', '{}', stix_pattern, custom_options)
        queries = ["observed_filename:some_file.exe"]
        _test_query_assertions(query, queries)

    def test_query_map_coverage(self):
        stix_to_cb_mapping = {
                "[ipv4-addr:value = '198.51.100.5' AND ipv4-addr:value = '198.51.100.10']" : ["(ipaddr:198.51.100.5 and ipaddr:198.51.100.10)"],
                "[process:pid = 4]": ["process_pid:4"],
                "[process:parent_ref.pid = 7]": ["parent_pid:7"],
                "[network-traffic:src_port = 80]": ["ipport:80"],
                "[network-traffic:dst_port = 80]": ["ipport:80"],
                "[user-account:user_id = 'SYSTEM']": ["username:SYSTEM"],
                "[process:pid < 4]": ["process_pid:[* TO 4]"],
                "[process:pid >= 4]": ["process_pid:[4 TO *]"],
                "[process:pid > 4]": ["process_pid:[5 TO *]"],
                "[process:pid <= 4]": ["process_pid:[* TO 5]"],
                "[network-traffic:dst_port > 1024]": ["ipport:[1025 TO *]"],
                "[file:hashes.MD5 ='79054025255fb1a26e4bc422aef54eb4']": ["md5:79054025255fb1a26e4bc422aef54eb4"],
                "[process:name NOT = 'cmd.exe']" : ["-(process_name:cmd.exe or crossproc_name:cmd.exe)"],
                "[process:name != 'cmd.exe']" : ["-(process_name:cmd.exe or crossproc_name:cmd.exe)"],
                "[process:pid = 4] START t'2019-01-22T00:04:52.937Z' STOP t'2019-02-22T00:04:52.937Z'": ["process_pid:4 and last_update:[2019-01-22T00:04:52 TO 2019-02-22T00:04:52]"],
                "[process:pid = 5 OR process:pid = 6] START t'2014-01-13T07:03:17Z' STOP t'2014-01-13T07:03:17Z'": ["(process_pid:5 or process_pid:6) and last_update:[2014-01-13T07:03:17 TO 2014-01-13T07:03:17]"]
                }
        for stix_pattern, queries in stix_to_cb_mapping.items():
            test_options = {"time_range": None} 
            result = translation.translate(module, 'query', '{}', stix_pattern, options=test_options)
            assert result['queries'] == queries

    def test_unmapped_attribute_handling_with_OR(self):
        stix_pattern = "[ipv4-addr:value = '198.51.100.5' OR unmapped:attribute = 'something']"
        translated_query = ["ipaddr:198.51.100.5 and last_update:-5m"]
        result = translation.translate(module, 'query', '{}', stix_pattern)
        assert result['queries'] == translated_query

    def test_unmapped_attribute_handling_with_AND(self):
        test_options = {"time_range": None} 
        stix_pattern = "[ipv4-addr:value = '198.51.100.5' AND unmapped:attribute = 'something']"
        result = translation.translate(module, 'query', '{}', stix_pattern, options=test_options)
        assert result['success'] == False
        assert ErrorCode.TRANSLATION_MAPPING_ERROR.value == result['code']
        assert 'Unable to map the following STIX objects and properties' in result['error']

    def test_escape_query(self):
        stix_to_cb_mapping = {
                "[process:name = ' ']" : ["(process_name:\\  or crossproc_name:\\ )"],
                "[process:name = '(']" : ["(process_name:\\( or crossproc_name:\\()"],
                "[process:name = ')']" : ["(process_name:\\) or crossproc_name:\\))"],
                "[process:name = '\"']" : ['(process_name:\\" or crossproc_name:\\")'],
                }
        for stix_pattern, queries in stix_to_cb_mapping.items():
            test_options = {"time_range": None} 
            result = translation.translate(module, 'query', '{}', stix_pattern, options=test_options)
            assert result['queries'] == queries

    def test_binary_api_qualifier(self):
        stix_to_cb_mapping = {
                "[file:name = 'cmd.exe'] START t'2019-01-22T00:04:52.937Z' STOP t'2019-02-22T00:04:52.937Z']": ["(process_name:cmd.exe or childproc_name:cmd.exe) and last_update:[2019-01-22T00:04:52 TO 2019-02-22T00:04:52]"],
                "[file:hashes.MD5 = '79054025255fb1a26e4bc422aef54eb4']": ["md5:79054025255fb1a26e4bc422aef54eb4"],
                "[domain-name:value = 'example.com']": ["(domain:example.com or hostname:example.com)"],
                }
        for stix_pattern, queries in stix_to_cb_mapping.items():
            test_options = {"time_range": None} 
            result = translation.translate("carbonblack", 'query', '{}', stix_pattern, options=test_options)
            assert result['queries'] == queries

    def test_merge_apis(self):
        stix_to_cb_mapping = {
                "[process:name = 'cmd.exe']": ["(process_name:cmd.exe or crossproc_name:cmd.exe) and last_update:-5m"],
                "[process:name = 'cmd.exe' AND file:hashes.MD5 = 'blah']": ["((process_name:cmd.exe or crossproc_name:cmd.exe) and md5:blah) and last_update:-5m"],
                "[process:name = 'cmd.exe' OR file:hashes.MD5 = 'blah']": ["((process_name:cmd.exe or crossproc_name:cmd.exe) or md5:blah) and last_update:-5m"],
                "[file:hashes.MD5 = 'blah']": ["md5:blah and last_update:-5m"],
                "[process:name = 'cmd.exe'] OR [file:hashes.MD5 = 'blah']": ["(process_name:cmd.exe or crossproc_name:cmd.exe) or md5:blah and last_update:-5m"],
                "[process:name = 'cmd.exe'] OR [file:hashes.MD5 = 'blah'] OR [process:pid = 5]": ["(process_name:cmd.exe or crossproc_name:cmd.exe) or md5:blah or process_pid:5 and last_update:-5m"],
                }
        for stix_pattern, queries in stix_to_cb_mapping.items():
            result = translation.translate("carbonblack", 'query', '{}', stix_pattern)
            print(result)
            assert result['queries'] == queries

    def test_nested_parenthesis_in_pattern(self):
        stix_pattern = "[(ipv4-addr:value = '192.168.122.83' OR ipv4-addr:value = '100.100.122.90') AND network-traffic:src_port = 37020 OR user-account:user_id = 'root']"
        query = translation.translate(module, 'query', '{}', stix_pattern)
        queries = ["(((ipaddr:192.168.122.83 or ipaddr:100.100.122.90) and ipport:37020) or username:root) and last_update:-5m"]
        _test_query_assertions(query, queries)

    def test_start_stop_merged(self):
        stix_to_cb_mapping = {
                "[process:name = 'cmd.exe'] OR [file:name = 'notepad.exe'] START t'2014-01-13T07:03:17Z' STOP t'2014-01-13T07:03:17Z'" : ["(process_name:cmd.exe or crossproc_name:cmd.exe) or (process_name:notepad.exe or childproc_name:notepad.exe) and last_update:[2014-01-13T07:03:17 TO 2014-01-13T07:03:17]"],
                "[process:name = 'cmd.exe'] START t'2014-01-13T07:03:17Z' STOP t'2019-01-13T07:03:17Z'  OR [file:name = 'notepad.exe'] START t'2014-01-13T07:03:17Z' STOP t'2014-01-13T07:03:17Z'": ["(process_name:cmd.exe or crossproc_name:cmd.exe) and last_update:[2014-01-13T07:03:17 TO 2019-01-13T07:03:17] or (process_name:notepad.exe or childproc_name:notepad.exe) and last_update:[2014-01-13T07:03:17 TO 2014-01-13T07:03:17]"],
                "([process:name = 'cmd.exe'] OR [process:name = 'notepad.exe']) START t'2014-01-13T07:03:17Z' STOP t'2014-01-13T07:03:17Z'": ["(process_name:cmd.exe or crossproc_name:cmd.exe) and last_update:[2014-01-13T07:03:17 TO 2014-01-13T07:03:17] or (process_name:notepad.exe or crossproc_name:notepad.exe) and last_update:[2014-01-13T07:03:17 TO 2014-01-13T07:03:17]"],
                "([process:name = 'cmd.exe'] OR [file:name = 'notepad.exe']) START t'2014-01-13T07:03:17Z' STOP t'2014-01-13T07:03:17Z'" : ["(process_name:cmd.exe or crossproc_name:cmd.exe) and last_update:[2014-01-13T07:03:17 TO 2014-01-13T07:03:17] or (process_name:notepad.exe or childproc_name:notepad.exe) and last_update:[2014-01-13T07:03:17 TO 2014-01-13T07:03:17]"],
                }
        for stix_pattern, queries in stix_to_cb_mapping.items():
            test_options = {"time_range": None}
            result = translation.translate("carbonblack", 'query', '{}', stix_pattern, options=test_options)
            print(result)
            assert result['queries'] == queries

    def test_time_range(self):
        # note queries with a START STOP specifying a query range should not have the default time_range applied
        stix_to_cb_mapping = {
                "[ipv4-addr:value = '127.0.0.1'" : ['ipaddr:127.0.0.1 and last_update:-5m'],
                "[process:name = 'cmd.exe'] OR [file:name = 'notepad.exe'] START t'2014-01-13T07:03:17Z' STOP t'2014-01-13T07:03:17Z'" : ["(process_name:cmd.exe or crossproc_name:cmd.exe) or (process_name:notepad.exe or childproc_name:notepad.exe) and last_update:[2014-01-13T07:03:17 TO 2014-01-13T07:03:17]"],
                }
        for stix_pattern, queries in stix_to_cb_mapping.items():
            result = translation.translate("carbonblack", 'query', '{}', stix_pattern, options={"time_range": 5})
            assert result['queries'] == queries

    def test_in_operator(self):
        # test_options = {"time_range": None} 
        stix_pattern = "[ipv4-addr:value IN ('10.0.0.1', '10.0.0.2')]"
        query = translation.translate(module, 'query', '{}', stix_pattern)
        queries = ["(ipaddr:10.0.0.1 or ipaddr:10.0.0.2) and last_update:-5m"]
        _test_query_assertions(query, queries)
