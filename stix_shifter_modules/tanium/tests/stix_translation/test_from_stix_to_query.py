from stix_shifter.stix_translation import stix_translation
import unittest
translation = stix_translation.StixTranslation()

def _test_query_assertions(queryList, expectedQueryList):
    for index, each_query in enumerate(queryList.get('queries'), start=0):
        print(expectedQueryList[index])
        print(each_query)
        assert each_query == expectedQueryList[index]

def _translate_query(stix_pattern, test_options):
    return translation.translate('tanium', 'query', '{}', stix_pattern, options=test_options)

test_options = {}

default_values_oca_event = {
    "x-oca-event:action": "Outlook Spawned Process Creating DLL Files",
    "x-oca-event:category": "process",
    "x-oca-event:outcome" : "unresolved",
    "x-oca-event:provider" : "tanium-signal",
    "x-oca-event:host_ref.hostname" : "EndpointDevice-",
    "x-oca-event:host_ref.ip_refs.value" : "10.0.0.4",
    "x-oca-event:host_ref.os_ref.name" : "windows",
    "x-oca-event:file_ref.parent_directory_ref.path" : "Application",
    "x-oca-event:severity" : "info",
    "x-oca-event:x_ttp_tagging_refs.name" : "T1204",
}

default_values_ibm_finding = {
    "x-ibm-finding:dst_ip_ref.value" : "10.0.0.4",
    "x-ibm-finding:action": "Outlook Spawned Process Creating DLL Files",
    "x-ibm-finding:severity" : "info",
    "x-ibm-finding:dst_os_ref.name" : "windows",
    "x-ibm-finding:x_ttp_tagging_refs.technique_id" : "T1204",
    "x-ibm-finding:x_guid" : "00000000-0000-0000-114a-7429237cffc5",
    "x-ibm-finding:x_priority" : "high",
    "x-ibm-finding:x_intel_doc_id" : 700,
    "x-ibm-finding:x_scan_config_id" : 2,
    "x-ibm-finding:x_path" : "Program",
    "x-ibm-finding:x_source" : "r",
    "x-ibm-finding:x_type" : "tanium-signal",
    "x-ibm-finding:x_label_name" : "t",
    "x-ibm-finding:x_details" : "te"
}

default_values_IPV4 = {
    "ipv4-addr:value" : "10.0.0.4"
}     

default_values_IPV6 = {
    "ipv6-addr:value" : "10.0.0.4"
}     

default_values_oca_asset = {
    "x-oca-asset:hostname" : "EndpointDevice-",
    "x-oca-asset:ip_refs.value" : "10.0.0.4",
    "x-oca-asset:os_ref.name" : "windows"
}     

default_values_software = {
    "software:name" : "windows"
}
    
#[x-oca-event:action = 'Outlook Spawned Process Creating DLL Files'] AND [x-oca-event:category = 'process'] AND [x-oca-event:code = '34']  AND [x-oca-event:description = 'a']  AND [x-oca-event:outcome = 'unresolved']  AND [x-oca-event:provider = 'tanium-signal']  AND [x-oca-event:host_ref.hostname = 'EndpointDevice-']  AND [x-oca-event:host_ref.ip_ref.value = '10.0.0.4']  AND [x-oca-event: host_ref.os_ref.name = 'windows']  AND [x-oca-event:file_ref.parent_directory_ref.path = 'Application'] AND [x-oca-event:severity = 'info'] AND [x-oca-event:x_ttp_tagging_refs.name = 'T1204']    START t'2022-07-01T00:00:00.000Z' STOP t'2024-07-27T00:05:00.000Z"


def _test_stix_to_json(stix_pattern, expectedQueryList):
    query = _translate_query(stix_pattern, test_options)
    _test_query_assertions(query, expectedQueryList)

class TestQueryTranslator(unittest.TestCase, object):
    
    def test_action_query(self):
        stix_pattern = f"[x-oca-event:action = 'Outlook Spawned Process Creating DLL Files']"
        expectedQueryList = [f"intelDocName={default_values_oca_event.get('x-oca-event:action')}"]
        _test_stix_to_json(stix_pattern, expectedQueryList)
        
    def test_action_query_with_time_frame(self):
        stix_pattern = f"[x-oca-event:action = 'Outlook Spawned Process Creating DLL Files']" \
                            " START t'2022-07-01T00:00:00.000Z'" \
                            " STOP t'2024-07-27T00:05:00.000Z'"
                            
        expectedQueryList = [f"intelDocName={default_values_oca_event.get('x-oca-event:action')}" \
                             f"&alertedAtFrom=2022-07-01T00:00:00.000Z" \
                             f"&alertedAtUntil=2024-07-27T00:05:00.000Z"]

        _test_stix_to_json(stix_pattern, expectedQueryList)
        
    def test_event_oca_query(self):
        stix_pattern = "([x-oca-event:action = 'Outlook Spawned Process Creating DLL Files']" \
                            " AND [x-oca-event:category = 'process']" \
                            " AND [x-oca-event:outcome = 'unresolved']" \
                            " AND [x-oca-event:provider = 'tanium-signal']" \
                            " AND [x-oca-event:host_ref.hostname = 'EndpointDevice-']" \
                            " AND [x-oca-event:host_ref.ip_refs.value = '10.0.0.4']" \
                            " AND [x-oca-event:host_ref.os_ref.name = 'windows']" \
                            " AND [x-oca-event:file_ref.parent_directory_ref.path = 'Application']" \
                            " AND [x-oca-event:severity = 0]" \
                            " AND [x-oca-event:x_ttp_tagging_refs.technique_id = 'T1204']" \
                            " START t'2022-07-01T00:00:00.000Z'" \
                            " STOP t'2024-07-27T00:05:00.000Z'"
        
        expectedQueryList = [f"intelDocName={default_values_oca_event.get('x-oca-event:action')}",
                             f"matchType={default_values_oca_event.get('x-oca-event:category')}",
                             f"state={default_values_oca_event.get('x-oca-event:outcome')}",
                             f"intelType={default_values_oca_event.get('x-oca-event:provider')}",
                             f"computerName={default_values_oca_event.get('x-oca-event:host_ref.hostname')}",
                             f"computerIpAddress={default_values_oca_event.get('x-oca-event:host_ref.ip_refs.value')}",
                             f"platform={default_values_oca_event.get('x-oca-event:host_ref.os_ref.name')}",
                             f"path={default_values_oca_event.get('x-oca-event:file_ref.parent_directory_ref.path')}",
                             f"severity={default_values_oca_event.get('x-oca-event:severity')}",
                             f"mitreId={default_values_oca_event.get('x-oca-event:x_ttp_tagging_refs.name')}" \
                             f"&alertedAtFrom=2022-07-01T00:00:00.000Z" \
                             f"&alertedAtUntil=2024-07-27T00:05:00.000Z"]
        
        _test_stix_to_json(stix_pattern, expectedQueryList)
        
    def test_ibm_finding(self):
        stix_pattern = "([x-ibm-finding:dst_ip_ref.value = '10.0.0.4']" \
                        " AND [x-ibm-finding:name = 'Outlook Spawned Process Creating DLL Files']" \
                        " AND [x-ibm-finding:severity = 0]" \
                        " AND [x-ibm-finding:dst_os_ref.name = 'windows']" \
                        " AND [x-ibm-finding:x_ttp_tagging_refs.technique_id = 'T1204']" \
                        " AND [x-ibm-finding:x_guid = '00000000-0000-0000-114a-7429237cffc5']" \
                        " AND [x-ibm-finding:x_priority = 'high']" \
                        " AND [x-ibm-finding:x_intel_doc_id = '700']" \
                        " AND [x-ibm-finding:x_scan_config_id = '2']" \
                        " AND [x-ibm-finding:x_path = 'Program']" \
                        " AND [x-ibm-finding:x_source = 'r']" \
                        " AND [x-ibm-finding:x_type = 'tanium-signal']" \
                        " AND [x-ibm-finding:x_label_name = 't']" \
                        " AND [x-ibm-finding:x_details = 'te']" \
                        " START t'2022-07-01T00:00:00.000Z'" \
                        " STOP t'2024-07-27T00:05:00.000Z'"
        
        expectedQueryList = [f"computerIpAddress={default_values_ibm_finding.get('x-ibm-finding:dst_ip_ref.value')}",
                             f"intelDocName={default_values_ibm_finding.get('x-ibm-finding:action')}",
                             f"severity={default_values_ibm_finding.get('x-ibm-finding:severity')}",
                             f"platform={default_values_ibm_finding.get('x-ibm-finding:dst_os_ref.name')}",
                             f"mitreId={default_values_ibm_finding.get('x-ibm-finding:x_ttp_tagging_refs.technique_id')}",
                             f"guid={default_values_ibm_finding.get('x-ibm-finding:x_guid')}",
                             f"priority={default_values_ibm_finding.get('x-ibm-finding:x_priority')}",
                             f"intelDocId={default_values_ibm_finding.get('x-ibm-finding:x_intel_doc_id')}",
                             f"scanConfigId={default_values_ibm_finding.get('x-ibm-finding:x_scan_config_id')}",
                             f"path={default_values_ibm_finding.get('x-ibm-finding:x_path')}",
                             f"intelSource={default_values_ibm_finding.get('x-ibm-finding:x_source')}",
                             f"type={default_values_ibm_finding.get('x-ibm-finding:x_type')}",
                             f"labelName={default_values_ibm_finding.get('x-ibm-finding:x_label_name')}",
                             f"details={default_values_ibm_finding.get('x-ibm-finding:x_details')}" \
                             f"&alertedAtFrom=2022-07-01T00:00:00.000Z" \
                             f"&alertedAtUntil=2024-07-27T00:05:00.000Z"]
        
        _test_stix_to_json(stix_pattern, expectedQueryList)
    
    def test_ipv4(self):
        stix_pattern = "([ipv4-addr:value = '10.0.0.4']" \
                        " START t'2022-07-01T00:00:00.000Z'" \
                        " STOP t'2024-07-27T00:05:00.000Z'"
        
        expectedQueryList = [f"computerIpAddress={default_values_IPV4.get('ipv4-addr:value')}" \
                             f"&alertedAtFrom=2022-07-01T00:00:00.000Z" \
                             f"&alertedAtUntil=2024-07-27T00:05:00.000Z"]
        
        _test_stix_to_json(stix_pattern, expectedQueryList)
        
    def test_ipv6(self):
        stix_pattern = "([ipv6-addr:value = '10.0.0.4']" \
                        " START t'2022-07-01T00:00:00.000Z'" \
                        " STOP t'2024-07-27T00:05:00.000Z'"
        
        expectedQueryList = [f"computerIpAddress={default_values_IPV6.get('ipv6-addr:value')}" \
                            f"&alertedAtFrom=2022-07-01T00:00:00.000Z" \
                            f"&alertedAtUntil=2024-07-27T00:05:00.000Z"]
        
        _test_stix_to_json(stix_pattern, expectedQueryList)
            
    def test_ipv6(self):
        stix_pattern = "([ipv6-addr:value = '10.0.0.4']" \
                        " START t'2022-07-01T00:00:00.000Z'" \
                        " STOP t'2024-07-27T00:05:00.000Z'"
        
        expectedQueryList = [f"computerIpAddress={default_values_IPV6.get('ipv6-addr:value')}" \
                            f"&alertedAtFrom=2022-07-01T00:00:00.000Z" \
                            f"&alertedAtUntil=2024-07-27T00:05:00.000Z"]
        
        _test_stix_to_json(stix_pattern, expectedQueryList)
        
    def test_asset(self):
    
        stix_pattern = "([x-oca-asset:hostname = 'EndpointDevice-']" \
                        " AND [x-oca-asset:ip_refs.value = '10.0.0.4']" \
                        " AND [x-oca-asset:os_ref.name = 'windows']" \
                        " START t'2022-07-01T00:00:00.000Z'" \
                        " STOP t'2024-07-27T00:05:00.000Z'"
        
        expectedQueryList = [f"computerName={default_values_oca_asset.get('x-oca-asset:hostname')}",
                            f"computerIpAddress={default_values_oca_asset.get('x-oca-asset:ip_refs.value')}",
                            f"platform={default_values_oca_asset.get('x-oca-asset:os_ref.name')}" \
                            f"&alertedAtFrom=2022-07-01T00:00:00.000Z" \
                            f"&alertedAtUntil=2024-07-27T00:05:00.000Z"]
        
        _test_stix_to_json(stix_pattern, expectedQueryList)
        
    def test_software(self):
        stix_pattern = "([software:name = 'windows']" \
                        " START t'2022-07-01T00:00:00.000Z'" \
                        " STOP t'2024-07-27T00:05:00.000Z'"
        
        expectedQueryList = [f"platform={default_values_software.get('software:name')}" \
                            f"&alertedAtFrom=2022-07-01T00:00:00.000Z" \
                            f"&alertedAtUntil=2024-07-27T00:05:00.000Z"]
        
        _test_stix_to_json(stix_pattern, expectedQueryList)
        
    def test_invalid_and_only_2_fields(self):
        expected_results = 'tanium connector error => STIX translation error: The translation is not valid as this API does not support AND queries between the same field.'
        stix_pattern = "[software:name = 'windows'" \
                    " AND software:name = 'linux']" \
                    " START t'2022-07-01T00:00:00.000Z'" \
                    " STOP t'2024-07-27T00:05:00.000Z'"
        results = _translate_query(stix_pattern, test_options)
        assert expected_results == results["error"]
    
    def test_alternating_and_or_valid_observation(self):
        stix_pattern = "([x-ibm-finding:dst_ip_ref.value = '10.0.0.4']" \
                        " OR [x-ibm-finding:dst_ip_ref.value = '10.0.0.2']" \
                        " OR [x-ibm-finding:dst_ip_ref.value = '10.0.0.1']" \
                        " AND [x-ibm-finding:dst_os_ref.name = 'windows']" \
                        " OR [x-ibm-finding:dst_os_ref.name = 'osx']" \
                        " OR [x-ibm-finding:dst_os_ref.name = 'linux']" \
                        " AND [x-ibm-finding:x_priority = 'high']" \
                        " OR [x-ibm-finding:x_priority = 'low']" \
                        " AND [x-ibm-finding:x_scan_config_id = '2']" \
                        " OR [x-ibm-finding:x_scan_config_id = '3']" \
                        " OR [x-ibm-finding:x_scan_config_id = '4']" \
                        " OR [x-ibm-finding:x_scan_config_id = '5']" \
                        " AND [x-ibm-finding:x_label_name = 't']" \
                        " AND [x-ibm-finding:x_details = 'te']" \
                        " START t'2022-07-01T00:00:00.000Z'" \
                        " STOP t'2024-07-27T00:05:00.000Z'"
        
        expectedQueryList = [f"computerIpAddress=10.0.0.4",
                             f"computerIpAddress=10.0.0.2",
                             f"computerIpAddress=10.0.0.1",
                             f"platform=windows",
                             f"platform=osx",
                             f"platform=linux",
                             f"priority=high",
                             f"priority=low",
                             f"scanConfigId=2",
                             f"scanConfigId=3",
                             f"scanConfigId=4",
                             f"scanConfigId=5",
                             f"labelName=t",
                             f"details=te&alertedAtFrom=2022-07-01T00:00:00.000Z&alertedAtUntil=2024-07-27T00:05:00.000Z"]
       
        _test_stix_to_json(stix_pattern, expectedQueryList)

    def test_alternating_and_or_valid_comparison(self):
        stix_pattern = "[(x-ibm-finding:dst_ip_ref.value = '10.0.0.4'" \
                        " OR x-ibm-finding:dst_ip_ref.value = '10.0.0.2'" \
                        " OR x-ibm-finding:dst_ip_ref.value = '10.0.0.1')" \
                        " AND (x-ibm-finding:dst_os_ref.name = 'windows'" \
                        " OR x-ibm-finding:dst_os_ref.name = 'osx'" \
                        " OR x-ibm-finding:dst_os_ref.name = 'linux')" \
                        " AND (x-ibm-finding:x_priority = 'high'" \
                        " OR x-ibm-finding:x_priority = 'low')" \
                        " AND (x-ibm-finding:x_scan_config_id = '2'" \
                        " OR x-ibm-finding:x_scan_config_id = '3'" \
                        " OR x-ibm-finding:x_scan_config_id = '4'" \
                        " OR x-ibm-finding:x_scan_config_id = '5')" \
                        " AND (x-ibm-finding:x_label_name = 't')" \
                        " AND (x-ibm-finding:x_details = 'te')]" \
                        " START t'2022-07-01T00:00:00.000Z'" \
                        " STOP t'2024-07-27T00:05:00.000Z'"

        expectedQueryList = [f"computerIpAddress=10.0.0.4" \
                             f"&computerIpAddress=10.0.0.2" \
                             f"&computerIpAddress=10.0.0.1" \
                             f"&platform=windows" \
                             f"&platform=osx" \
                             f"&platform=linux" \
                             f"&priority=high" \
                             f"&priority=low" \
                             f"&scanConfigId=2" \
                             f"&scanConfigId=3" \
                             f"&scanConfigId=4" \
                             f"&scanConfigId=5" \
                             f"&labelName=t" \
                             f"&details=te" \
                             f"&alertedAtFrom=2022-07-01T00:00:00.000Z" \
                             f"&alertedAtUntil=2024-07-27T00:05:00.000Z"]
        _test_stix_to_json(stix_pattern, expectedQueryList)
        
    def test_alternating_and_or_valid_comparison_with_in(self):
        stix_pattern = "[(x-ibm-finding:dst_ip_ref.value = '10.0.0.4'" \
                        " OR x-ibm-finding:dst_ip_ref.value = '10.0.0.2'" \
                        " OR x-ibm-finding:dst_ip_ref.value = '10.0.0.1')" \
                        " AND (x-ibm-finding:dst_os_ref.name IN ('windows','osx','linux'))" \
                        " AND (x-ibm-finding:x_priority = 'high'" \
                        " OR x-ibm-finding:x_priority = 'low')" \
                        " AND (x-ibm-finding:x_scan_config_id = '2'" \
                        " OR x-ibm-finding:x_scan_config_id = '3'" \
                        " OR x-ibm-finding:x_scan_config_id = '4'" \
                        " OR x-ibm-finding:x_scan_config_id = '5')" \
                        " AND (x-ibm-finding:x_label_name = 't')" \
                        " AND (x-ibm-finding:x_details = 'te')]" \
                        " START t'2022-07-01T00:00:00.000Z'" \
                        " STOP t'2024-07-27T00:05:00.000Z'"

        expectedQueryList = [f"computerIpAddress=10.0.0.4" \
                             f"&computerIpAddress=10.0.0.2" \
                             f"&computerIpAddress=10.0.0.1" \
                             f"&platform=windows" \
                             f"&platform=osx" \
                             f"&platform=linux" \
                             f"&priority=high" \
                             f"&priority=low" \
                             f"&scanConfigId=2" \
                             f"&scanConfigId=3" \
                             f"&scanConfigId=4" \
                             f"&scanConfigId=5" \
                             f"&labelName=t" \
                             f"&details=te" \
                             f"&alertedAtFrom=2022-07-01T00:00:00.000Z" \
                             f"&alertedAtUntil=2024-07-27T00:05:00.000Z"]
    
        _test_stix_to_json(stix_pattern, expectedQueryList)
    
    def test_alternating_and_invalid_comparison(self):
        #This one fails because there are two AND's involving the scan_config_id. This isn't possible in the API.
        expected_results = 'tanium connector error => STIX translation error: The translation is not valid as this API does not support AND queries between the same field.'
        stix_pattern = "[x-ibm-finding:dst_ip_ref.value = '10.0.0.4'" \
                        " OR x-ibm-finding:dst_ip_ref.value = '10.0.0.2'" \
                        " OR x-ibm-finding:dst_ip_ref.value = '10.0.0.1'" \
                        " AND x-ibm-finding:dst_os_ref.name = 'windows'" \
                        " OR x-ibm-finding:dst_os_ref.name = 'osx'" \
                        " OR x-ibm-finding:dst_os_ref.name = 'linux'" \
                        " AND x-ibm-finding:x_scan_config_id = '1'" \
                        " AND x-ibm-finding:x_priority = 'high'" \
                        " OR x-ibm-finding:x_priority = 'low'" \
                        " AND x-ibm-finding:x_scan_config_id = '2'" \
                        " OR x-ibm-finding:x_scan_config_id = '3'" \
                        " OR x-ibm-finding:x_scan_config_id = '4'" \
                        " OR x-ibm-finding:x_scan_config_id = '5'" \
                        " AND x-ibm-finding:x_label_name = 't'" \
                        " AND x-ibm-finding:x_details = 'te']" \
                        " START t'2022-07-01T00:00:00.000Z'" \
                        " STOP t'2024-07-27T00:05:00.000Z'"
        results = _translate_query(stix_pattern, test_options)
        assert expected_results == results["error"] 
        
    def test_alternating_or_invalid_comparison(self):
        #This test should fail. The order is important here. All of the AND are combined togather, than the OR are checked with the combined ANDs.
        #This is a fail because your first check of an OR is (ip=1.0.0.4 OR ip=1.0.0.2) OR (ip=1.0.0.1 AND platform=windows)
        #This is invalid because you cannot do this with the API. 
        expected_results = 'tanium connector error => STIX translation error: The translation is not valid as this API does not support OR queries between different fields.'
        stix_pattern = "[x-ibm-finding:dst_ip_ref.value = '10.0.0.4'" \
                        " OR x-ibm-finding:dst_ip_ref.value = '10.0.0.2'" \
                        " OR x-ibm-finding:dst_ip_ref.value = '10.0.0.1'" \
                        " AND x-ibm-finding:dst_os_ref.name = 'windows'" \
                        " OR x-ibm-finding:dst_os_ref.name = 'osx'" \
                        " OR x-ibm-finding:dst_os_ref.name = 'linux'" \
                        " AND x-ibm-finding:x_priority = 'high'" \
                        " OR x-ibm-finding:x_priority = 'low'" \
                        " AND x-ibm-finding:x_scan_config_id = '2'" \
                        " OR x-ibm-finding:x_scan_config_id = '3'" \
                        " OR x-ibm-finding:x_scan_config_id = '4'" \
                        " OR x-ibm-finding:x_scan_config_id = '5'" \
                        " AND x-ibm-finding:x_label_name = 't'" \
                        " OR x-ibm-finding:dst_ip_ref.value = '10.0.0.2'" \
                        " AND x-ibm-finding:x_details = 'te']" \
                        " START t'2022-07-01T00:00:00.000Z'" \
                        " STOP t'2024-07-27T00:05:00.000Z'"
        results = _translate_query(stix_pattern, test_options)
        assert expected_results == results["error"]                       
            
    def test_in_operator(self):
        stix_pattern = f"[x-oca-event:action IN ('test1','test2','test3')]" \
                            " START t'2022-07-01T00:00:00.000Z'" \
                            " STOP t'2024-07-27T00:05:00.000Z'"
                            
        expectedQueryList = [f"intelDocName=test1" \
                             f"&intelDocName=test2" \
                             f"&intelDocName=test3" \
                             f"&alertedAtFrom=2022-07-01T00:00:00.000Z" \
                             f"&alertedAtUntil=2024-07-27T00:05:00.000Z"]
        
        _test_stix_to_json(stix_pattern, expectedQueryList)
    
    
    def test_observation_with_qualifier_and_three_comparisons(self):
        stix_pattern = "[x-ibm-finding:dst_ip_ref.value = '10.0.0.1'" \
                        " AND x-ibm-finding:dst_os_ref.name = 'windows'" \
                        " AND x-ibm-finding:x_priority = 'low']" \
                        " START t'2022-07-01T00:00:00.001Z'" \
                        " STOP t'2024-07-27T00:05:00.001Z'" \
                        " AND [x-ibm-finding:dst_ip_ref.value = '10.0.0.2'" \
                        " AND x-ibm-finding:dst_os_ref.name = 'linux'" \
                        " AND x-ibm-finding:x_priority = 'lower']" \
                        " START t'2022-07-01T00:00:00.002Z'" \
                        " STOP t'2024-07-27T00:05:00.002Z'" \
                        " OR [x-ibm-finding:dst_ip_ref.value = '10.0.0.3'" \
                        " AND x-ibm-finding:dst_os_ref.name = 'macos'" \
                        " AND x-ibm-finding:x_priority = 'medium']" \
                        " START t'2022-07-01T00:00:00.003Z'" \
                        " STOP t'2024-07-27T00:05:00.003Z'" \
                        " AND [x-ibm-finding:dst_ip_ref.value = '10.0.0.4'" \
                        " AND x-ibm-finding:dst_os_ref.name = 'windows2'" \
                        " AND x-ibm-finding:x_priority = 'high']" \
                        " START t'2022-07-01T00:00:00.004Z'" \
                        " STOP t'2024-07-27T00:05:00.004Z'"

        expectedQueryList = [f"computerIpAddress=10.0.0.1" \
                             f"&platform=windows" \
                             f"&priority=low" \
                             f"&alertedAtFrom=2022-07-01T00:00:00.001Z" \
                             f"&alertedAtUntil=2024-07-27T00:05:00.001Z",
                             f"computerIpAddress=10.0.0.2" \
                             f"&platform=linux" \
                             f"&priority=lower" \
                             f"&alertedAtFrom=2022-07-01T00:00:00.002Z" \
                             f"&alertedAtUntil=2024-07-27T00:05:00.002Z",
                             f"computerIpAddress=10.0.0.3" \
                             f"&platform=macos" \
                             f"&priority=medium" \
                             f"&alertedAtFrom=2022-07-01T00:00:00.003Z" \
                             f"&alertedAtUntil=2024-07-27T00:05:00.003Z",
                             f"computerIpAddress=10.0.0.4" \
                             f"&platform=windows2" \
                             f"&priority=high" \
                             f"&alertedAtFrom=2022-07-01T00:00:00.004Z" \
                             f"&alertedAtUntil=2024-07-27T00:05:00.004Z"]
        _test_stix_to_json(stix_pattern, expectedQueryList)
        
    def test_observation_with_qualifier_and_three_comparisons_odd(self):
        stix_pattern = "[x-ibm-finding:dst_ip_ref.value = '10.0.0.1'" \
                        " OR x-ibm-finding:dst_ip_ref.value = '10.0.1.1']" \
                        " START t'2022-07-01T00:00:00.001Z'" \
                        " STOP t'2024-07-27T00:05:00.001Z'" \
                        " AND [x-ibm-finding:dst_ip_ref.value = '10.0.0.2'" \
                        " OR x-ibm-finding:dst_ip_ref.value = '10.0.1.2']" \
                        " OR [x-ibm-finding:dst_ip_ref.value = '10.0.0.3'" \
                        " OR x-ibm-finding:dst_ip_ref.value = '10.0.1.3']" \
                        " START t'2022-07-01T00:00:00.003Z'" \
                        " STOP t'2024-07-27T00:05:00.003Z'" \

        expectedQueryList = [f"computerIpAddress=10.0.0.1" \
                             f"&computerIpAddress=10.0.1.1" \
                             f"&alertedAtFrom=2022-07-01T00:00:00.001Z" \
                             f"&alertedAtUntil=2024-07-27T00:05:00.001Z",
                             f"computerIpAddress=10.0.0.2" \
                             f"&computerIpAddress=10.0.1.2",
                             f"computerIpAddress=10.0.0.3" \
                             f"&computerIpAddress=10.0.1.3" \
                             f"&alertedAtFrom=2022-07-01T00:00:00.003Z" \
                             f"&alertedAtUntil=2024-07-27T00:05:00.003Z"]
        _test_stix_to_json(stix_pattern, expectedQueryList)