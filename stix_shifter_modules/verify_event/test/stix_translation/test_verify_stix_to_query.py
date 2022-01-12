import unittest
import json
import logging
from stix_shifter.stix_translation import stix_translation
translation = stix_translation.StixTranslation()
# config_file = open('stix_shifter_modules/verify_event/configuration/config.json').read()
# from_stix_file = open('stix_shifter_modules/verify_event/stix_translation/json/from_stix_map.json').read()
# to_stix_file = open('stix_shifter_modules/verify_event/stix_translation/json/to_stix_map.json').read()
# OPTIONS = json.loads(from_stix_file)

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger()

data_source = {
    "type": "identity",
    "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
    "name": "crowdstrike",
    "identity_class": "events"
}

data_source ={
    "type": "identity",
    "id": "32a23267-52fb-4e82-859b-0a15d6a2d334",
    "name":"verify_event",
    "identity_class":"events"
    }
OPTION = json.dumps(data_source)
def _test_query_assertions(query, queries):
    assert query['queries'] == [queries]

def _translate_query(stix_pattern):
        return translation.translate('verify_event', 'query', '{}', stix_pattern)

class TestStixToQuery(unittest.TestCase, object):

    def test_event_type(self):
        stix_pattern = "[event_type:value='authentication']"
        query = _translate_query(stix_pattern)
        print(query['queries'])
        queries = "event_type=\"authentication\"&limit=10000"
        _test_query_assertions(query, queries)

    def test_IPV4_query(self):
        stix_pattern = "[ipv4-addr:value='27.58.174.31']"
        query = _translate_query(stix_pattern)
        print("queryies :",query['queries'])
        #filter_key:value="data.origin" & filter_value:value="27.58.174.31"&limit=10000
        queries = 'filter_key=data.origin&filter_value="27.58.174.31"&limit=10000'
        _test_query_assertions(query, queries)
