from stix_shifter.stix_translation import stix_translation
import unittest
import json
import re


FROM_STIX_MAPPING_FILE = open('stix_shifter_modules/mysql/stix_translation/json/from_stix_map.json').read()
FROM_STIX_MAPPINGS = json.loads(FROM_STIX_MAPPING_FILE)
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
    "directory_created_time": EPOCH,
    "directory_modified_time": EPOCH,
    "directory_accessed_time": EPOCH,
    "username": "'admin'",
    "source_port": 1234,
    "dest_port": 5678,
    "protocol": "'tcp'",
    "entry_time": TIMESTAMP,
    "system_name": "'computer'",
    "severity": 5,
    "file_created_time": EPOCH,
    "file_modified_time": EPOCH,
    "file_accessed_time": EPOCH,
    "process_id": 12345,
    "process_name": "'hackingAllTheThings'",
    "process_arguments": "'some args'",
    "process_created_time": EPOCH
}

translation = stix_translation.StixTranslation()


def _test_query_assertions(field, queries):
    for query in queries:
        assert field in query
        value = TEST_VALUES[field]
        if field == "entry_time":
            value = str(EPOCH)
        if not isinstance(value, str):
            value = str(value)
        assert value in query


def _translate_query(stix_pattern):
    return translation.translate('mysql', 'query', '{}', stix_pattern)


def _add_single_quotes(stix_property):
    stix_property = re.sub("SHA-256", "'SHA-256'", stix_property)
    stix_property = re.sub("MD5", "'MD5'", stix_property)
    return stix_property


class TestQueryTranslator(unittest.TestCase, object):

    def test_all_mappings(self):
        for stix_object, value in FROM_STIX_MAPPINGS.items():
            for stix_property, field_list in value["fields"].items():
                if stix_object == 'file':
                    stix_property = _add_single_quotes(stix_property)
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
                pattern_translation = _translate_query(stix_pattern)
                assert pattern_translation.get("queries"), "failed to translate {}".format(stix_pattern)
                for field in field_list:
                    _test_query_assertions(field, pattern_translation["queries"])
