""" test script to perform unit test case for symantec translate results """
import unittest
from stix_shifter_modules.symantec_endpoint_security.entry_point import EntryPoint
from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers

MODULE = "symantec_endpoint_security"
entry_point = EntryPoint()
map_data = entry_point.get_results_translator().map_data
data_source = {
    "type": "identity",
    "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
    "name": "symantec endpoint security",
    "identity_class": "events"
}
options = {}

symantec_sample_response = [{
    "device_os_type_id": 100,
    "lineage": [
        "C:\\Windows\\System32\\svchost.exe",
        "C:\\Windows\\System32\\services.exe",
        "C:\\Windows\\System32\\wininit.exe"
    ],
    "feature_uid": "1DF0351C-146D-4F07-B155-BF5C7077FF40",
    "type": "event_query_results",
    "seq_num": 24,
    "ref_uid": "DC931153-3860-4E7D-9A96-378662BC51F3",
    "legacy_product_uid": "ad66b334-9eb8-bf35-3f4e-f172b06200b0",
    "id": 1,
    "product_uid": "31B0C880-0229-49E8-94C5-48D56B1BD7B9",
    "feature_name": "DETECTION_RESPONSE",
    "device_group": "Default/TestEDRGroup",
    "product_name": "Symantec Endpoint Security",
    "version": "1.0.0",
    "command_uid": "",
    "device_ip": "10.10.10.10",
    "device_vhost": 12,
    "timezone": 0,
    "device_domain": "WORKGROUP",
    "product_ver": "14.3.10148.8000",
    "is_npvdi_client": "false",
    "device_name": "HOST_NAME",
    "category_id": 5,
    "device_networks": [
        {
            "ipv4": "10.10.10.10",
            "ipv6": "fe00:0000:0000:0000:000f:df0a:0000:00d0",
            "mac": "0a:0f:00:00:0c:00"
        }
    ],
    "device_os_name": "Windows Server 2019 Datacenter Edition",
    "type_id": 8001,
    "actor": {
        "session_id": 0,
        "pid": 1880,
        "uid": "C03AA311-0907-F1EF-848A-EAEACDB378C2",
        "tid": 5472,
        "start_time": "2024-05-03T04:44:04.920Z",
        "cmd_line": "C:\\Windows\\system32\\svchost.exe -k netsvcs -p -s Schedule",
        "integrity_id": 6,
        "file": {
            "type_id": 1,
            "created": "2022-09-14T16:17:52.744Z",
            "modified": "2022-09-14T16:17:52.744Z",
            "md5": "0dd00f000ac00d0f00f00f00e0aa0000",
            "sha2": "2b105fb153b1bcd619b00000000b3a93c60b000eef6837d3bb0099e4207aaf6b",
            "size": 51736,
            "signature_company_name": "Microsoft Windows Publisher",
            "signature_value_ids": [
                3,
                5
            ],
            "security_descriptor": "O:S-1-1-1-0-71241G:SYD:(A;;0x1fffff;;;S-1-1-1-0-71241)(A;;0x1400;;;BA)S:AI",
            "normalized_path": "CSIDL_SYSTEM\\svchost.exe",
            "path": "c:\\windows\\system32\\svchost.exe",
            "uid": "281474976968790",
            "name": "svchost.exe",
            "folder": "c:\\windows\\system32",
            "original_name": "svchost.exe",
            "signature_level_id": 60
        },
        "user": {
            "name": "SYSTEM",
            "sid": "S-1-1-11",
            "domain": "NT AUTHORITY"
        },
        "cmd_line_raw_length": 57
    },
    "device_mac": "0a:0f:00:00:0c:00",
    "device_uid": "X4oOxiAoQO6SuZAfO6lm4Q",
    "org_unit_uid": "_RE5UsoeSKSrteDkP3U2Mw",
    "severity_id": 1,
    "logging_device_post_time": "2024-05-03T06:49:06.299Z",
    "device_time": "2024-05-03T06:49:06.302Z",
    "user_name": "SYSTEM",
    "process": {
        "session_id": 0,
        "pid": 5396,
        "uid": "C03AB60B-0907-F1EF-848A-EAEACDB378C2",
        "start_time": "2024-05-03T06:49:06.302Z",
        "cmd_line": "\"C:\\Windows\\system32\\usoclient.exe\" StartScan",
        "integrity_id": 6,
        "file": {
            "type_id": 1,
            "created": "2020-03-18T06:42:21.265Z",
            "modified": "2020-03-18T06:42:21.265Z",
            "md5": "39750d00d000000b000adbb917f7b000",
            "sha2": "df0000cdc3c6f000000aaf2d4407c4e8aaa000000a00000fb4688e2bd099db85",
            "size": 48128,
            "signature_company_name": "Microsoft Windows",
            "signature_value_ids": [
                3,
                5
            ],
            "security_descriptor": "O:SYG:SYD:(A;;0x1fffff;;;SY)(A;;RC;;;OW)"
                                   "(A;;0x1fffff;;;S-1-1-10-0000092361-0000024937-000023819-0000237918-00005745)S:AI",
            "normalized_path": "CSIDL_SYSTEM\\usoclient.exe",
            "path": "c:\\windows\\system32\\usoclient.exe",
            "uid": "281474976969093",
            "name": "usoclient.exe",
            "folder": "c:\\windows\\system32",
            "original_name": "UsoClient",
            "signature_level_id": 60
        },
        "user": {
            "name": "SYSTEM",
            "sid": "S-1-1-11",
            "domain": "NT AUTHORITY"
        },
        "cmd_line_raw_length": 45
    },
    "edr_enriched_data": {
        "category_name": "Generic Data to be sent to ATP",
        "category_id": 201,
        "rule_id": 2101450,
        "rule_name": "IF.SchtasksLaunch!g2"
    },
    "feature_ver": "edr/1.3.0",
    "is_user_present": "false",
    "event_data_type": "fdr",
    "user": {
        "name": "SYSTEM"
    },
    "device_os_ver": "10.0.17763",
    "policy": {
        "uid": "a7124b68-abc1-43a4-8e44-716fb1966646",
        "name": "Default Detection and Response Policy",
        "version": "1"
    },
    "trans_event_raw_length": 3436,
    "attacks": [
        {
            "technique_uid": "T1053",
            "technique_name": "Scheduled Task/Job",
            "tactic_ids": [
                2,
                3,
                4
            ],
            "tactic_uids": [
                "TA0002",
                "TA0003",
                "TA0004"
            ]
        }
    ],
    "customer_uid": "IKhSB-yfRK2xeUR-xyCK2g",
    "device_public_ip": "22.22.22.22",
    "domain_uid": "B3dKzLSzR9CScPYAGhkgxA",
    "time": "2024-05-03T06:49:06.302Z",
    "log_time": "2024-05-03T06:49:24.770Z",
    "uuid": "8001:3c5831e0-0919-11ef-cf18-000006b4f3c8",
    "indexDate": "2024-05-03",
    "indexHash": "fdr_4_t2",
    "log_name": "c1.fdr_4_t2_2024-05-03",
    "es.mapping.id": "uuid",
    "epochLogTime": 1714718964770,
    "es.mapping.version": "epochLogTime"
}]

symantec_policy_sample_response = [{
    "category_id": 3,
    "change_type_id": 1,
    "curr_location": {"desc": "Default", "on_premises": False},
    "device_ip": "172.1.1.1",
    "device_location": {"desc": "Default", "on_premises": False},
    "device_time": 1714710446334,
    "feature_name": "AGENT_FRAMEWORK",
    "feature_uid": "1DF0351C-146D-4FFF-BBBB-BF5C7077FF40",
    "id": 4,
    "message": "Location changed. [Previous]:  [Current]: Default",
    "message_id": "0x1207020E",
    "policy": {"name": "Default System Policy", "uid": "f6e97ddb-eb48-4a1f-a862-d9895ec6d7dc",
               "version": "1"},
    "prev_location": {"desc": "", "on_premises": False},
    "raw_data": "",
    "severity_id": 1,
    "status_detail": "Smc",
    "status_id": 1,
    "type": "POLICY_CHANGE",
    "type_id": 4,
    "version": "1.0",
    "composite": 2,
    "device_domain": "WORKGROUP",
    "device_group": "Default/TestDevGroup",
    "device_name": "XZ-ABC",
    "device_networks": [{"ipv4": "172.1.1.1", "ipv6": "fe80::1111:1111:1111:a6d7", "mac": "12:AA:AA:AA:AA:AA"},
                        {"ipv4": "192.1.1.1", "ipv6": "fe80::2222:2222:2222:22fd", "mac": "86:AA:AA:AA:AA:AA"}],
    "device_os_name": "Windows Server 2019 Datacenter Edition",
    "device_uid": "X4oOxiAoQO6SuZAfO6lm5Q",
    "org_unit_uid": "KKqxxxxxxxxxxxySg",
    "product_data": {"sep_domain_uid": "", "sep_hw_uid": "D47E4AAAAAAAAAAAAAE"},
    "product_name": "Symantec Endpoint Security",
    "product_uid": "31B0C880-0229-49E8-94C5-48D56B1BDCCC",
    "product_ver": "14.3.10148.8000",
    "stic_hw_uid": "DB3AAAAAA-49AF-72A1-1169-AAAAAAAAD420",
    "stic_uid": "19AAAAAAA-999C-43CD-BFDF-AAAAAAAAAA81",
    "timezone": 0,
    "user_name": "Administrator",
    "customer_uid": "IKxxx-xxxxxxxxx-xyCK2g",
    "device_public_ip": "54.1.1.1",
    "domain_uid": "B3dKxxxxxxxxkgxABBBBBB",
    "event_data_type": "sep",
    "user": {"name": "Administrator"},
    "device_os_type_id": 100,
    "time": "2024-05-03T04:27:26.334Z",
    "log_time": "2024-05-03T04:34:57.379Z",
    "uuid": "4:71eeeeee-0905-11ef-f724-000001eeeec3",
    "indexDate": "2024-05-03",
    "indexHash": "event_service_4_t2",
    "log_name": "c1.event_service_4_t2_2024-05-03",
    "es.mapping.id": "uuid", "epochLogTime": 1714710897379, "es.mapping.version": "epochLogTime"}]

symantec_threat_sample_response = [{
    "category_id": 1,
    "content_ver": "Version: 2024-05-03 rev. 002; Sequence: 240503002",
    "count": 1,
    "cybox": {"files": [{"company_name": "KnowBe4, Inc.",
                         "folder": "C:\\Users\\Administrator\\Downloads\\Ransom App",
                         "name": "SimulatorSetup.exe",
                         "normalized_path": "CSIDL_PROFILE\\downloads\\ransom app\\simulatorsetup.exe",
                         "path": "C:\\Users\\Administrator\\Downloads\\Ransom App\\SimulatorSetup.exe",
                         "product_name": "KnowBe4 Rns Simulator",
                         "rep_discovered_band": 365, "rep_prevalence": 71, "rep_score": -105,
                         "sha2": "815B99BD82F3685F97F9A2DD24A434C1749D5A5C9097F2B6BCEA42F69EE01A05",
                         "signature_company_name": "DigiCert Trusted G4 Code Signing RSA4096 SHA384 2021 CA1",
                         "signature_created_date": 1677490376,
                         "signature_issuer": "KnowBe4 Inc.", "signature_value": 1099520606215,
                         "signature_value_ids": [1, 2, 3, 17, 20], "size": 181872248,
                         "type_id": 1, "version": "2.4.1.2"}]},
    "device_end_time": 1714740874000,
    "device_ip": "172.31.30.222",
    "device_location": {"desc": "Default", "on_premises": False},
    "device_time": 1714740874000,
    "feature_name": "MALWARE_PROTECTION",
    "feature_uid": "A36AAAAA-4F03-42DE-B55F-39AAAAAA89C8",
    "file": {"company_name": "KnowBe4, Inc.",
             "content_type": {"family_id": 3},
             "folder": "C:\\Users\\Administrator\\Downloads\\Ransom App",
             "name": "SimulatorSetup.exe",
             "normalized_path": "CSIDL_PROFILE\\downloads\\ransom app\\simulatorsetup.exe",
             "path": "C:\\Users\\Administrator\\Downloads\\Ransom App\\SimulatorSetup.exe",
             "product_name": "KnowBe4 Rns Simulator",
             "rep_discovered_band": 365,
             "rep_prevalence": 71,
             "rep_score": -105,
             "sha2": "815B99BD82F3685F97F9A2DD24A434C1749D5A5C9097F2B6BCEA42F69EE02AA5",
             "signature_company_name": "DigiCert Trusted G4 Code Signing RSA4096 SHA384 2021 CA1",
             "signature_created_date": 1677490376,
             "signature_fingerprints": [{"algorithm": "sha1", "value": "21EC32614C2BE32ADD9E2056CAA28CAB5A7FEEEA"}],
             "signature_issuer": "KnowBe4 Inc.", "signature_serial_number": "0E44DA59C6985D40A6040C9D9AAAAAAA",
             "signature_value": 1099520606215,
             "signature_value_ids": [1, 2, 3, 17, 20],
             "size": 181872248, "type_id": 1, "version": "2.4.1.2"},
    "id": 12, "policy": {"name": "Default Antimalware Policy", "rule_category_id": 1,
                         "uid": "5afbaaaa-d1fe-4104-b43b-63aaaaaaaa5b", "version": "1"},
    "quarantine_uid": "179830784",
    "reason_id": 2,
    "ref_uid": "f7caaaa-92d8-4908-8d51-bd7aaaaaa87",
    "scan_uid": "",
    "severity_id": 1,
    "threat": {"id": 42878, "name": "Trojan.Gen.MBT", "risk_id": 100, "type_id": 1},
    "type": "HOST_FILE_DETECTION", "type_id": 8031, "user_name": "SYSTEM", "version": "1.0", "composite": 2,
    "device_domain": "WORKGROUP", "device_group": "Default/TestEDRGroup", "device_name": "AMAZ-XXXXXX",
    "device_networks": [{"ipv4": "172.2.3.3", "ipv6": "fe80::3333:3333:3333:99d5", "mac": "0A:BB:BB:BB:BB:75"},
                        {"ipv4": "169.4.4.4", "ipv6": "fe80::4444:4444:4444:31cf", "mac": "86:CC:CC:CC:CC:89"}],
    "device_os_name": "Windows Server 2019 Datacenter Edition",
    "device_uid": "X4oOxiAoQO6SuZAfO6lm6Q", "org_unit_uid": "_RE5UsXXXXXXMw",
    "product_data": {"sep_domain_uid": "", "sep_hw_uid": "AD66B3BBBBBBBBBBBBBB200B0"},
    "product_name": "Symantec Endpoint Security",
    "product_uid": "31B0AAAA-0229-49E8-94C5-48AAAAAAA7B9", "product_ver": "14.3.10148.8000",
    "stic_hw_uid": "9FBC61111-5BC6-E087-DC55-1411111111C5",
    "stic_uid": "92EE1111-2C77-4401-9A10-4911111111CE", "timezone": 0,
    "customer_uid": "IKhSB-xxxxxxxxx-xyxxxx", "device_public_ip": "10.1.1.1",
    "domain_uid": "B3dKxxxxxxxxkgxABBBBAA",
    "event_data_type": "sep", "user": {"name": "SYSTEM"}, "device_os_type_id": 100, "time": "2024-05-03T12:54:34Z",
    "end_time": "2024-05-03T12:54:34.000Z",
    "log_time": "2024-05-03T12:54:41.184Z",
    "uuid": "8031:4a456100-094c-11ef-c4f3-0000029ebed4",
    "indexDate": "2024-05-03", "indexHash": "event_service_4_t2",
    "log_name": "c1.event_service_4_t2_2024-05-03",
    "es.mapping.id": "uuid", "epochLogTime": 1714740881184, "es.mapping.version": "epochLogTime"}]

symantec_file_sample_response = [{
    "file": {"path": "c:\\programdata\\apv2\\logs\\cybereasonactiveprobe.log.0.gz",
             "normalized_path": "CSIDL_COMMON_APPDATA\\apv2\\logs\\cybereasonactiveprobe.log.0.gz",
             "attributes": 128,
             "attribute_ids": 6,
             "security_descriptor": "O:BAG:SYD:AI(A;ID;FR;;;WD)(A;ID;FA;;;SY)(A;ID;FA;;;BA)(A;ID;0x1200a9;;;BU)",
             "size": 250931,
             "name": "cybereasonactiveprobe.log.0.gz",
             "folder": "c:\\programdata\\apv2\\logs",
             "content_type": {"family_id": 0, "type_id": 1}}}]

symantec_network_sample_response = [{
    "connection": {"src_ip": "::", "src_port": "59418", "dst_port": "0", "protocol_id": 17, "dst_ip": "0.0.0.0"},
    "state_id": 0,
    "id": 1,
    "product_uid": "31B0C880-0229-49E8-94C5-48D56B1BD7B9",
    "raw_data": {"PID": "3844", "ProcessName": "svchost.exe", "Protocol": "UDP", "LocalAddress": "::",
                 "LocalPort": "59418", "RemoteAddress": "0.0.0.0", "RemotePort": "0", "State": '',
                 "EvidenceType": '', "IsDefault": False, "IsSuspicious": False}}]


class TestSymantecResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for symantec translate results
    """

    @staticmethod
    def get_first(itr, constraint):
        """ return the obj in the itr if constraint is true """
        return next((obj for obj in itr if constraint(obj)), None)

    @staticmethod
    def get_first_of_type(itr, typ):
        """ check whether the object belongs to respective stix object """
        return TestSymantecResultsToStix.get_first(itr, lambda o: isinstance(o, dict) and o.get('type') == typ)

    @staticmethod
    def get_observed_data_objects(data):
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, data, get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        return observed_data['objects']

    def test_ipv4_addr_json_to_stix(self):
        """test ipv4-addr stix object properties"""
        objects = TestSymantecResultsToStix.get_observed_data_objects(symantec_sample_response)
        ipv4_obj = TestSymantecResultsToStix.get_first_of_type(objects.values(), 'ipv4-addr')
        ipv6_obj = TestSymantecResultsToStix.get_first_of_type(objects.values(), 'ipv6-addr')
        assert ipv4_obj is not None
        assert (ipv4_obj.keys() == {'type', 'value', 'resolves_to_refs'})
        assert ipv4_obj['type'] == 'ipv4-addr'
        assert ipv4_obj['value'] == '10.10.10.10'
        assert ipv6_obj['value'] == 'fe00:0000:0000:0000:000f:df0a:0000:00d0'

    def test_mac_addr_json_to_stix(self):
        """test mac-addr stix object properties"""
        objects = TestSymantecResultsToStix.get_observed_data_objects(symantec_sample_response)
        mac_addr_obj = TestSymantecResultsToStix.get_first_of_type(objects.values(), 'mac-addr')
        assert mac_addr_obj is not None
        assert (mac_addr_obj.keys() == {'type', 'value'})
        assert mac_addr_obj['type'] == 'mac-addr'
        assert mac_addr_obj['value'] == '0a:0f:00:00:0c:00'

    def test_file_json_to_stix(self):
        """test file stix object properties"""
        objects = TestSymantecResultsToStix.get_observed_data_objects(symantec_sample_response)
        file_obj = TestSymantecResultsToStix.get_first_of_type(objects.values(), 'file')
        assert file_obj is not None
        assert (file_obj.keys() == {'type', 'x_file_type', 'created', 'modified', 'hashes', 'size',
                                    'name', 'parent_directory_ref'})
        assert file_obj['type'] == 'file'
        assert file_obj['name'] == 'svchost.exe'
        assert file_obj['size'] == 51736

    def test_process_json_to_stix(self):
        """test process stix object properties"""
        objects = TestSymantecResultsToStix.get_observed_data_objects(symantec_sample_response)
        process_obj = TestSymantecResultsToStix.get_first_of_type(objects.values(), 'process')
        assert process_obj is not None
        assert (process_obj.keys() == {'type', 'pid', 'x_process_uid', 'x_process_tid', 'created',
                                       'command_line', 'binary_ref', 'creator_user_ref', 'child_refs'})
        assert process_obj['type'] == 'process'
        assert process_obj['pid'] == 1880
        assert process_obj['command_line'] == 'C:\\Windows\\system32\\svchost.exe -k netsvcs -p -s Schedule'

    def test_user_account_json_to_stix(self):
        """test user-account stix object properties"""
        objects = TestSymantecResultsToStix.get_observed_data_objects(symantec_sample_response)
        user_account_obj = TestSymantecResultsToStix.get_first_of_type(objects.values(), 'user-account')
        assert user_account_obj is not None
        assert (user_account_obj.keys() == {'type', 'user_id', 'x_user_sid', 'x_user_domain'})
        assert user_account_obj['type'] == 'user-account'
        assert user_account_obj['user_id'] == 'SYSTEM'

    def test_directory_json_to_stix(self):
        """test directory stix object properties"""
        objects = TestSymantecResultsToStix.get_observed_data_objects(symantec_sample_response)
        directory_obj = TestSymantecResultsToStix.get_first_of_type(objects.values(), 'directory')
        assert directory_obj is not None
        assert (directory_obj.keys() == {'type', 'path'})
        assert directory_obj['type'] == 'directory'
        assert directory_obj['path'] == 'c:\\windows\\system32'

    def test_x_ibm_ttp_tagging_obj_json_to_stix(self):
        """test x-ibm-ttp-tagging stix object properties"""
        objects = TestSymantecResultsToStix.get_observed_data_objects(symantec_sample_response)
        x_ibm_ttp_tagging_obj = TestSymantecResultsToStix.get_first_of_type(objects.values(), 'x-ibm-ttp-tagging')
        assert x_ibm_ttp_tagging_obj is not None
        assert (x_ibm_ttp_tagging_obj.keys() == {'type', 'extensions', 'name'})
        assert x_ibm_ttp_tagging_obj['type'] == 'x-ibm-ttp-tagging'
        assert x_ibm_ttp_tagging_obj['name'] == 'Scheduled Task/Job'
        assert x_ibm_ttp_tagging_obj['extensions'] is not None
        ibm_tagging = x_ibm_ttp_tagging_obj['extensions']['mitre-attack-ext']
        assert ibm_tagging['technique_id'] == 'T1053'
        assert ibm_tagging['tactic_id'] == 'TA0002'

    def test_x_symantec_policy_obj_json_to_stix(self):
        """test x-symantec-info stix object properties"""
        objects = TestSymantecResultsToStix.get_observed_data_objects(symantec_sample_response)
        x_symantec_info_obj = TestSymantecResultsToStix.get_first_of_type(objects.values(), 'x-symantec-policy')
        assert x_symantec_info_obj is not None
        assert (x_symantec_info_obj.keys() == {'type', 'name', 'version'})
        assert x_symantec_info_obj['type'] == 'x-symantec-policy'
        assert x_symantec_info_obj['name'] == 'Default Detection and Response Policy'
        assert x_symantec_info_obj['version'] == '1'

    def test_x_oca_asset_obj_json_to_stix(self):
        """test x-symantec-info stix object properties"""
        objects = TestSymantecResultsToStix.get_observed_data_objects(symantec_sample_response)
        x_symantec_info_obj = TestSymantecResultsToStix.get_first_of_type(objects.values(), 'x-oca-asset')
        assert x_symantec_info_obj is not None
        assert (x_symantec_info_obj.keys() == {'type', 'x_host_group', 'ip_refs', 'domain_ref', 'hostname',
                                               'mac_refs', 'os_ref'})
        assert x_symantec_info_obj['type'] == 'x-oca-asset'
        assert x_symantec_info_obj['hostname'] == 'HOST_NAME'
        assert x_symantec_info_obj['os_ref'] == '0'

    def test_software_obj_json_to_stix(self):
        """test x-symantec-info stix object properties"""
        objects = TestSymantecResultsToStix.get_observed_data_objects(symantec_sample_response)
        x_symantec_info_obj = TestSymantecResultsToStix.get_first_of_type(objects.values(), 'software')
        assert x_symantec_info_obj is not None
        assert (x_symantec_info_obj.keys() == {'type', 'name', 'version', 'x_os_type'})
        assert x_symantec_info_obj['type'] == 'software'
        assert x_symantec_info_obj['name'] == 'Windows Server 2019 Datacenter Edition'
        assert x_symantec_info_obj['version'] == '10.0.17763'
        assert x_symantec_info_obj['x_os_type'] == 'Windows'

    def test_x_oca_event_obj_json_to_stix_malware(self):
        """test x-symantec-info stix object properties"""
        objects = TestSymantecResultsToStix.get_observed_data_objects(symantec_sample_response)
        x_symantec_info_obj = TestSymantecResultsToStix.get_first_of_type(objects.values(), 'x-oca-event')
        assert x_symantec_info_obj is not None
        assert (x_symantec_info_obj.keys() == {'type', 'action', 'outcome', 'x_feature_name', 'provider',
                                               'x_event_type_version', 'timezone', 'x_provider_version', 'host_ref',
                                               'category', 'x_event_type', 'process_ref', 'file_ref', 'severity',
                                               'user_ref', 'x_policy_ref', 'created', 'code'})
        assert x_symantec_info_obj['type'] == 'x-oca-event'
        assert x_symantec_info_obj['action'] == 'event_query_results'
        assert x_symantec_info_obj['category'] == 'System Activity'
        assert x_symantec_info_obj['severity'] == 16
        assert x_symantec_info_obj['outcome'] == 'Blocked'
        assert x_symantec_info_obj['x_event_type'] == 8001

    def test_x_oca_event_obj_json_to_stix(self):
        """test x-symantec-info stix object properties"""
        objects = TestSymantecResultsToStix.get_observed_data_objects(symantec_policy_sample_response)
        x_symantec_info_obj = TestSymantecResultsToStix.get_first_of_type(objects.values(), 'x-oca-event')
        assert x_symantec_info_obj is not None
        assert (x_symantec_info_obj.keys() == {'type', 'category', 'x_feature_name', 'outcome', 'description', 'x_policy_ref',
                                               'severity', 'x_event_status', 'action', 'x_event_type',
                                               'x_event_type_version', 'host_ref', 'provider', 'x_provider_version',
                                               'timezone', 'user_ref', 'created', 'code'})
        assert x_symantec_info_obj['type'] == 'x-oca-event'
        assert x_symantec_info_obj['action'] == 'POLICY_CHANGE'
        assert x_symantec_info_obj['category'] == 'Application Activity'
        assert x_symantec_info_obj['severity'] == 16
        assert x_symantec_info_obj['outcome'] == 'Logged'
        assert x_symantec_info_obj['x_event_type'] == 4

    def test_x_ibm_finding_obj_json_to_stix(self):
        """test x-symantec-info stix object properties"""
        objects = TestSymantecResultsToStix.get_observed_data_objects(symantec_threat_sample_response)
        x_symantec_info_obj = TestSymantecResultsToStix.get_first_of_type(objects.values(), 'x-ibm-finding')
        assert x_symantec_info_obj is not None
        assert (x_symantec_info_obj.keys() == {'type', 'x_policy_ref', 'finding_type', 'alert_id', 'name',
                                               'severity', 'x_threat_type_id'})
        assert x_symantec_info_obj['type'] == 'x-ibm-finding'
        assert x_symantec_info_obj['alert_id'] == 42878
        assert x_symantec_info_obj['severity'] == 100
        assert x_symantec_info_obj['name'] == 'Trojan.Gen.MBT'
        assert x_symantec_info_obj['x_threat_type_id'] == 'Malware'

    def test_x509_certificate_obj_json_to_stix(self):
        """test x-symantec-info stix object properties"""
        objects = TestSymantecResultsToStix.get_observed_data_objects(symantec_threat_sample_response)
        x_symantec_info_obj = TestSymantecResultsToStix.get_first_of_type(objects.values(), 'x509-certificate')
        assert x_symantec_info_obj is not None
        assert (x_symantec_info_obj.keys() == {'type', 'x_signature_company_name',
                    'validity_not_before', 'hashes', 'issuer',
                    'serial_number', 'x_signature_value', 'x_signature_value_ids'})
        assert x_symantec_info_obj['type'] == 'x509-certificate'
        assert x_symantec_info_obj['x_signature_company_name'] == 'DigiCert Trusted G4 Code Signing RSA4096 SHA384 2021 CA1'
        assert x_symantec_info_obj['issuer'] == 'knowbe4 inc.'
        assert x_symantec_info_obj['serial_number'] == '0E44DA59C6985D40A6040C9D9AAAAAAA'
        assert x_symantec_info_obj['validity_not_before'] == '2023-02-27T09:32:56.000Z'

    def test_file_type_id_json_to_stix(self):
        """test file stix object properties"""
        objects = TestSymantecResultsToStix.get_observed_data_objects(symantec_file_sample_response)
        file_obj = TestSymantecResultsToStix.get_first_of_type(objects.values(), 'file')
        assert file_obj is not None
        assert (file_obj.keys() == {'type', 'parent_directory_ref', 'size', 'name', 'x_family_type', 'x_content_type'})
        assert file_obj['type'] == 'file'
        assert file_obj['size'] == 250931
        assert file_obj['x_content_type'] == 'Application'

    def test_network_json_to_stix(self):
        """test file stix object properties"""
        objects = TestSymantecResultsToStix.get_observed_data_objects(symantec_network_sample_response)
        network_obj = TestSymantecResultsToStix.get_first_of_type(objects.values(), 'network-traffic')
        assert network_obj is not None
        assert (network_obj.keys() == {'type', 'src_ref', 'scr_port', 'dst_port', 'protocols', 'dst_ref'})
        assert network_obj['type'] == 'network-traffic'
        assert network_obj['scr_port'] == 59418
