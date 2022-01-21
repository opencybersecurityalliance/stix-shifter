from unicodedata import category
import unittest
import json
import logging
from stix_shifter.stix_translation import stix_translation
from stix_shifter_modules.verify.entry_point import EntryPoint
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers
translation = stix_translation.StixTranslation()
# config_file = open('stix_shifter_modules/verify_event/configuration/config.json').read()
# from_stix_file = open('stix_shifter_modules/verify_event/stix_translation/json/from_stix_map.json').read()
# to_stix_file = open('stix_shifter_modules/verify_event/stix_translation/json/to_stix_map.json').read()
# OPTIONS = json.loads(from_stix_file)

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger()
MODULE = 'verify'
RESULTS = 'results'
TRANSFORMERS = get_module_transformers(MODULE)
epoch_to_timestamp_class = TRANSFORMERS.get('EpochToTimestamp')
EPOCH_START = 1531169112
EPOCH_END = 1531169254
START_TIMESTAMP = epoch_to_timestamp_class.transform(EPOCH_START)
END_TIMESTAMP = epoch_to_timestamp_class.transform(EPOCH_END)
entry_point = EntryPoint()
MAP_DATA = entry_point.get_results_translator().map_data


DATA_SOURCE ={
    "type": "identity",
    "id": "identity--32a23267-52fb-4e82-859b-0a15d6a2d334",
    "name":"verify",
    "identity_class":"events"
    }
OPTION = json.dumps(DATA_SOURCE)
def _test_query_assertions(query, queries):
    assert query['queries'] == [queries]

def _translate_query(stix_pattern):
        return translation.translate('verify', 'query', '{}', stix_pattern)

class TestStixToQuery(unittest.TestCase, object):
    
    def test_event_type(self):
        stix_pattern = "[x-oca-event:category='authentication']"
        query = _translate_query(stix_pattern)
        queries = "event_type=\"authentication\"&size=10000"
        _test_query_assertions(query, queries)

    def test_IPV4_query(self):
        stix_pattern = "[ipv4-addr:value='27.58.174.31']"
        query = _translate_query(stix_pattern)
        expected_queries = 'filter_key=data.origin&filter_value="27.58.174.31"&size=10000'
        _test_query_assertions(query, expected_queries)

    def test_oca_event_extension(self):
        stix_pattern = "[x-oca-event:extensions.'x-ibm-iam-ext'.user_id='652001LT0R']"
        query = _translate_query(stix_pattern)
        expected_queries = 'filter_key=data.userid&filter_value="652001LT0R"&size=10000'
        _test_query_assertions(query,expected_queries)

    def test_event_type_and_fiter(self):
        stix_pattern = "[x-oca-event:category = 'sso' AND x-oca-event:domain_ref.value = '77.169.74.152']START t'2022-01-17T18:24:00.000Z' STOP t'2022-01-20T18:24:00.000Z' "
        query = _translate_query(stix_pattern)
        expected_queries = 'filter_key=tenantname&filter_value="77.169.74.152"&event_type="sso"&from=1642443840000&to=1642703040000&size=10000'
        _test_query_assertions(query, expected_queries)

    def test_domain_name_query(self):
        stix_pattern ="[domain-name:value = 'isrras.ice.ibmcloud.com']"
        query = _translate_query(stix_pattern)
        expected_queries = 'filter_key=tenantname&filter_value="isrras.ice.ibmcloud.com"&size=10000'
        _test_query_assertions(query,expected_queries)
  