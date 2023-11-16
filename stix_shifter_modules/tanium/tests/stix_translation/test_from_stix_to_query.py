from stix_shifter.stix_translation import stix_translation
import unittest
import json
import os
translation = stix_translation.StixTranslation()

def _test_query_assertions(queryList, expectedQueryList):
    for index, each_query in enumerate(queryList.get('queries'), start=0):
        print(expectedQueryList[index])
        print(each_query)
        assert each_query == expectedQueryList[index]

def _translate_query(stix_pattern, test_options):
    return translation.translate('tanium', 'query', '{}', stix_pattern, options=test_options)

test_options = {}

default_values = {
    "x-oca-event:action": "Outlook Spawned Process Creating DLL Files",
    "x-oca-event:category": "process",
    "x-oca-event:description" : "test3",
    "x-oca-event:outcome" : "unresolved",
    "x-oca-event:provider" : "tanium-signal",
    "x-oca-event:host_ref.hostname" : "EndpointDevice-",
    "x-oca-event:host_ref.ip_ref.value" : "10.0.0.4",
    "x-oca-event:host_ref.os_ref.name" : "windows",
    "x-oca-event:file_ref.parent_directory_ref.path" : "Application",
    "x-oca-event:severity" : "info",
    "x-oca-event:x_ttp_tagging_refs.name" : "T1204",
}           
    
#[x-oca-event:action = 'Outlook Spawned Process Creating DLL Files'] AND [x-oca-event:category = 'process'] AND [x-oca-event:code = '34']  AND [x-oca-event:description = 'a']  AND [x-oca-event:outcome = 'unresolved']  AND [x-oca-event:provider = 'tanium-signal']  AND [x-oca-event:host_ref.hostname = 'EndpointDevice-']  AND [x-oca-event:host_ref.ip_ref.value = '10.0.0.4']  AND [x-oca-event: host_ref.os_ref.name = 'windows']  AND [x-oca-event:file_ref.parent_directory_ref.path = 'Application'] AND [x-oca-event:severity = 'info'] AND [x-oca-event:x_ttp_tagging_refs.name = 'T1204']    START t'2022-07-01T00:00:00.000Z' STOP t'2024-07-27T00:05:00.000Z"


def _test_stix_to_json(stix_pattern, expectedQueryList):
    query = _translate_query(stix_pattern, test_options)
    _test_query_assertions(query, expectedQueryList)

class TestQueryTranslator(unittest.TestCase, object):
    
    def test_action_query(self):
        stix_pattern = f"[x-oca-event:action = 'Outlook Spawned Process Creating DLL Files']"
        expectedQueryList = [f"intelDocName='{default_values.get('x-oca-event:action')}'" \
                             f"&limit=10000"]
        _test_stix_to_json(stix_pattern, expectedQueryList)
        
    def test_action_query_with_time_frame(self):
        stix_pattern = f"[x-oca-event:action = 'Outlook Spawned Process Creating DLL Files']" \
                            " START t'2022-07-01T00:00:00.000Z'" \
                            " STOP t'2024-07-27T00:05:00.000Z'"
        expectedQueryList = [f"intelDocName='{default_values.get('x-oca-event:action')}'" \
                             f"&alertedAtFrom=2022-07-01T00:00:00.000Z" \
                             f"&alertedAtUntil=2024-07-27T00:05:00.000Z" \
                             f"&limit=10000"]
        
        _test_stix_to_json(stix_pattern, expectedQueryList)
        
    def test_action_query_all_query(self):
        stix_pattern = "([x-oca-event:action = 'Outlook Spawned Process Creating DLL Files']" \
                            " AND [x-oca-event:category = 'process']" \
                            " AND [x-oca-event:description = 'test3']" \
                            " AND [x-oca-event:outcome = 'unresolved']" \
                            " AND [x-oca-event:provider = 'tanium-signal']" \
                            " AND [x-oca-event:host_ref.hostname = 'EndpointDevice-']" \
                            " AND [x-oca-event:host_ref.ip_ref.value = '10.0.0.4']" \
                            " AND [x-oca-event:host_ref.os_ref.name = 'windows']" \
                            " AND [x-oca-event:file_ref.parent_directory_ref.path = 'Application']" \
                            " AND [x-oca-event:severity = 'info']" \
                            " AND [x-oca-event:x_ttp_tagging_refs.name = 'T1204']" \
                            " START t'2022-07-01T00:00:00.000Z'" \
                            " STOP t'2024-07-27T00:05:00.000Z'"
        
        expectedQueryList = [f"intelDocName='{default_values.get('x-oca-event:action')}'" \
                             f"&matchType='{default_values.get('x-oca-event:category')}'" \
                             f"&details='{default_values.get('x-oca-event:description')}'" \
                             f"&state='{default_values.get('x-oca-event:outcome')}'" \
                             f"&intelType='{default_values.get('x-oca-event:provider')}'" \
                             f"&computerName='{default_values.get('x-oca-event:host_ref.hostname')}'" \
                             f"&computerIpAddress='{default_values.get('x-oca-event:host_ref.ip_ref.value')}'" \
                             f"&platforms='{default_values.get('x-oca-event:host_ref.os_ref.name')}'" \
                             f"&path='{default_values.get('x-oca-event:file_ref.parent_directory_ref.path')}'" \
                             f"&severity='{default_values.get('x-oca-event:severity')}'" \
                             f"&mitreId='{default_values.get('x-oca-event:x_ttp_tagging_refs.name')}'" \
                             f"&alertedAtFrom=2022-07-01T00:00:00.000Z" \
                             f"&alertedAtUntil=2024-07-27T00:05:00.000Z" \
                             f"&limit=10000"]
        _test_stix_to_json(stix_pattern, expectedQueryList)