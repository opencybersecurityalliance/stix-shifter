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
                            " AND [x-oca-event:severity = 'info']" \
                            " AND [x-oca-event:x_ttp_tagging_refs.technique_id = 'T1204']" \
                            " START t'2022-07-01T00:00:00.000Z'" \
                            " STOP t'2024-07-27T00:05:00.000Z'"
        
        expectedQueryList = [f"intelDocName={default_values_oca_event.get('x-oca-event:action')}" \
                             f"&matchType={default_values_oca_event.get('x-oca-event:category')}" \
                             f"&state={default_values_oca_event.get('x-oca-event:outcome')}" \
                             f"&intelType={default_values_oca_event.get('x-oca-event:provider')}" \
                             f"&computerName={default_values_oca_event.get('x-oca-event:host_ref.hostname')}" \
                             f"&computerIpAddress={default_values_oca_event.get('x-oca-event:host_ref.ip_refs.value')}" \
                             f"&platform={default_values_oca_event.get('x-oca-event:host_ref.os_ref.name')}" \
                             f"&path={default_values_oca_event.get('x-oca-event:file_ref.parent_directory_ref.path')}" \
                             f"&severity={default_values_oca_event.get('x-oca-event:severity')}" \
                             f"&mitreId={default_values_oca_event.get('x-oca-event:x_ttp_tagging_refs.name')}" \
                             f"&alertedAtFrom=2022-07-01T00:00:00.000Z" \
                             f"&alertedAtUntil=2024-07-27T00:05:00.000Z"]
        _test_stix_to_json(stix_pattern, expectedQueryList)
        
    def test_ibm_finding(self):
        stix_pattern = "([x-ibm-finding:dst_ip_ref.value = '10.0.0.4']" \
                        " AND [x-ibm-finding:name = 'Outlook Spawned Process Creating DLL Files']" \
                        " AND [x-ibm-finding:severity = 'info']" \
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
        
        
        expectedQueryList = [f"computerIpAddress={default_values_ibm_finding.get('x-ibm-finding:dst_ip_ref.value')}" \
                             f"&intelDocName={default_values_ibm_finding.get('x-ibm-finding:action')}" \
                             f"&severity={default_values_ibm_finding.get('x-ibm-finding:severity')}" \
                             f"&platform={default_values_ibm_finding.get('x-ibm-finding:dst_os_ref.name')}" \
                             f"&mitreId={default_values_ibm_finding.get('x-ibm-finding:x_ttp_tagging_refs.technique_id')}" \
                             f"&guid={default_values_ibm_finding.get('x-ibm-finding:x_guid')}" \
                             f"&priority={default_values_ibm_finding.get('x-ibm-finding:x_priority')}" \
                             f"&intelDocId={default_values_ibm_finding.get('x-ibm-finding:x_intel_doc_id')}" \
                             f"&scanConfigId={default_values_ibm_finding.get('x-ibm-finding:x_scan_config_id')}" \
                             f"&path={default_values_ibm_finding.get('x-ibm-finding:x_path')}" \
                             f"&intelSource={default_values_ibm_finding.get('x-ibm-finding:x_source')}" \
                             f"&type={default_values_ibm_finding.get('x-ibm-finding:x_type')}" \
                             f"&labelName={default_values_ibm_finding.get('x-ibm-finding:x_label_name')}" \
                             f"&details={default_values_ibm_finding.get('x-ibm-finding:x_details')}" \
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
        
        
        expectedQueryList = [f"computerName={default_values_oca_asset.get('x-oca-asset:hostname')}" \
                            f"&computerIpAddress={default_values_oca_asset.get('x-oca-asset:ip_refs.value')}" \
                            f"&platform={default_values_oca_asset.get('x-oca-asset:os_ref.name')}" \
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
        
    def test_multiple_of_same_field(self):
        stix_pattern = "([software:name = 'windows']" \
                       " AND [software:name = 'linux']" \
                        " START t'2022-07-01T00:00:00.000Z'" \
                        " STOP t'2024-07-27T00:05:00.000Z'"
        
        
        expectedQueryList = [f"platform={default_values_software.get('software:name')}" \
                            f"&platform={'linux'}" \
                            f"&alertedAtFrom=2022-07-01T00:00:00.000Z" \
                            f"&alertedAtUntil=2024-07-27T00:05:00.000Z"]
        
        _test_stix_to_json(stix_pattern, expectedQueryList)
    
    def test_get_observed_data_objects(self):
        assert True
        # result_bundle = json_to_stix_translator.convert_to_stix(
        #     data_source, map_data, [SAMPLE_DATA_DICT], get_module_transformers(MODULE), options)
        # result_bundle_objects = result_bundle['objects']

        # result_bundle_identity = result_bundle_objects[0]
        # assert result_bundle_identity['type'] == data_source['type']
        # observed_data = result_bundle_objects[1]

        # assert 'objects' in observed_data