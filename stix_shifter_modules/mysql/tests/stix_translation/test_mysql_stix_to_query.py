from stix_shifter.stix_translation import stix_translation
import unittest
import json
import re


FROM_STIX_MAPPING_FILE_2_0 = open('stix_shifter_modules/mysql/stix_translation/json/from_stix_map.json').read()
FROM_STIX_MAPPINGS_2_0 = json.loads(FROM_STIX_MAPPING_FILE_2_0)
FROM_STIX_MAPPING_FILE_2_1 = open('stix_shifter_modules/mysql/stix_translation/json/stix_2_1/from_stix_map.json').read()
FROM_STIX_MAPPINGS_2_1 = json.loads(FROM_STIX_MAPPING_FILE_2_1)
EPOCH = 1634657528000
TIMESTAMP = "'2021-10-19T15:32:08.000Z'"

TEST_VALUES = {
    "source_ipaddr": "'0.0.0.0'",
    "dest_ipaddr": "'1.1.1.1'",
    "url": "'www.example.com'",
    "filename": "'somefile.exe'",
    "sha256hash": "'sha256filehash'",
    "md5hash": "'md5filehash'",
    "file_path": "'C:/directory/'",
    "directory_created_time": TIMESTAMP,
    "directory_modified_time": TIMESTAMP,
    "directory_accessed_time": TIMESTAMP,
    "username": "'admin'",
    "source_port": 1234,
    "dest_port": 5678,
    "protocol": "'tcp'",
    "entry_time": TIMESTAMP,
    "system_name": "'computer'",
    "severity": 5,
    "file_created_time": TIMESTAMP,
    "file_modified_time": TIMESTAMP,
    "file_accessed_time": TIMESTAMP,
    "process_id": 12345,
    "process_name": "'hackingAllTheThings'",
    "process_arguments": "'some args'",
    "process_created_time": TIMESTAMP
}

translation = stix_translation.StixTranslation()


def _test_query_assertions(field, queries):
    for query in queries:
        assert field in query
        value = TEST_VALUES[field]
        if value == TIMESTAMP:
            value = EPOCH
        if not isinstance(value, str):
            value = str(value)
        assert value in query


def _translate_query(stix_pattern, options={}):
    return translation.translate('mysql', 'query', '{}', stix_pattern, options)



def _test_mappings(mappings, stix_spec='2.0'):
    for stix_object, value in mappings.items():
        for stix_property, field_list in value["fields"].items():
            field_count = len(field_list)
            stix_pattern = "["
            for field in field_list:
                test_value = TEST_VALUES.get(field)
                if not test_value:
                    assert False, "'{}' datasource field missing from TEST_VALUES dictionary.".format(field)
                stix_pattern += "{}:{} = {}".format(stix_object, stix_property, TEST_VALUES.get(field))
                if field_count > 1:
                    stix_pattern += " OR "
                field_count -= 1
            stix_pattern += "]"
            if stix_spec == "2.1":
                pattern_translation = _translate_query(stix_pattern, {"table": "demo_table", "stix_2.1": True})
            else:
                pattern_translation = _translate_query(stix_pattern, {"table": "demo_table"})
            assert pattern_translation.get("queries"), "failed to translate {}".format(stix_pattern)
            for field in field_list:
                _test_query_assertions(field, pattern_translation["queries"])

class TestQueryTranslator(unittest.TestCase, object):

    def test_all_mappings_stix_2_0(self):
        _test_mappings(FROM_STIX_MAPPINGS_2_0)


    def test_all_mappings_stix_2_1(self):
        _test_mappings(FROM_STIX_MAPPINGS_2_1, "2.1")

    def test_start_stop_qualifiers_with_one_observation(self):
        start_time_01 = "t'2016-06-01T01:30:00.123Z'"
        stop_time_01 = "t'2016-06-01T02:20:00.123Z'"
        unix_start_time_01 = 1464744600123
        unix_stop_time_01 = 1464747600123
        stix_pattern = "[url:value = 'www.example.com'] START {} STOP {}".format(start_time_01, stop_time_01)
        query = _translate_query(stix_pattern, {"table": "demo_table"})
        where_statement = "SELECT * FROM demo_table WHERE url = 'www.example.com' AND (entry_time >= {} AND entry_time <= {}) limit 10000".format(unix_start_time_01, unix_stop_time_01)
        assert len(query['queries']) == 1
        assert query['queries'] == [where_statement]

