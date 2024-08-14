import json
import os
from stix_shifter_modules.tanium.entry_point import EntryPoint
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers
from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
import unittest

MODULE = "tanium"
entry_point = EntryPoint()
map_data = entry_point.get_results_translator().map_data
data_source = {
    "type": "identity",
    "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
    "name": "Tanium",
    "identity_class": "events"
}
options = {"unmapped_fallback":"true"}


sample_files_location = os.getcwd() + "/stix_shifter_modules/tanium/tests"

class TestTaniumResultsToStix(unittest.TestCase, object):
    def test_confirm_objects_parse(self):
        sample_data_large = open(sample_files_location + "/Sample_Data.json", "r")

        sample_data_large_json = json.load(sample_data_large)
        for alert in sample_data_large_json["data"]:
            result_bundle_large = json_to_stix_translator.convert_to_stix(data_source, map_data, [alert], get_module_transformers(MODULE), options)
            assert len(result_bundle_large["objects"][1]["objects"]) > 5
            
    def test_results(self):
        sample_data_large = open(sample_files_location + "/Sample_Data.json", "r")
        sample_data_large_json = json.load(sample_data_large)
        
        #There are many events in the sample. For the unit testing I will only be using the first one.
        alert = sample_data_large_json["data"][0]
        result_bundle_large = json_to_stix_translator.convert_to_stix(data_source, map_data, [alert], get_module_transformers(MODULE), options)
        result_bundle = result_bundle_large["objects"][1]["objects"]
        
        type_count = self.get_type_count(result_bundle,1)
        attempt_count = dict()
        for i in range(0, len(result_bundle), +1):
            index = str(i)
            if( "type" not in result_bundle[index]):
                assert False
            try:
                self._test_against_sample_data(result_bundle[index], result_bundle[index]["type"])        
            except:
                if (result_bundle[index]["type"] in attempt_count):
                    attempt_count[result_bundle[index]["type"]] = attempt_count[result_bundle[index]["type"]] + 1
                else:
                    attempt_count[result_bundle[index]["type"]] = 1
                
                if(attempt_count[result_bundle[index]["type"]] >= type_count[result_bundle[index]["type"]]):
                    raise   
                
    def test_results_severity_low(self):
        sample_data_large = open(sample_files_location + "/Sample_Data.json", "r")
        sample_data_large_json = json.load(sample_data_large)
        
        #There are many events in the sample. For the unit testing I will only be using the first two.
        #The first one has no parent process. The second has one.
        alert = sample_data_large_json["data"][1]
        result_bundle_large = json_to_stix_translator.convert_to_stix(data_source, map_data, [alert], get_module_transformers(MODULE), options)
        result_bundle = result_bundle_large["objects"][1]["objects"]
        
        for i in range(0, len(result_bundle)):
            index = str(i)
            if(result_bundle[index]["type"] == "x-ibm-finding" or result_bundle[index]["type"] == "x-oca-event" ):
                assert result_bundle[index]["severity"] == 40
                return
        assert False
            
    def test_results_severity_high(self):
        sample_data_large = open(sample_files_location + "/Sample_Data.json", "r")
        sample_data_large_json = json.load(sample_data_large)
               
        alert = sample_data_large_json["data"][2]
        result_bundle_large = json_to_stix_translator.convert_to_stix(data_source, map_data, [alert], get_module_transformers(MODULE), options)
        result_bundle = result_bundle_large["objects"][1]["objects"]
        
        for i in range(0, len(result_bundle)):
            index = str(i)
            if(result_bundle[index]["type"] == "x-ibm-finding" or result_bundle[index]["type"] == "x-oca-event" ):
                assert result_bundle[index]["severity"] == 80
                return
        assert False
        
    def test_results_stix_21_unique_fields(self):
        entry_point = EntryPoint(options={"stix_2.1":"true"})
        map_data = entry_point.get_results_translator().map_data
        sample_data_large = open(sample_files_location + "/Sample_Data.json", "r")
        sample_data_large_json = json.load(sample_data_large)
               
        alert = sample_data_large_json["data"][0]
        options.update({"stix_2.1":"true", "unmapped_fallback":"true"})
        result_bundle_large = json_to_stix_translator.convert_to_stix(data_source, map_data, [alert], get_module_transformers(MODULE), options)
        result_bundle = result_bundle_large["objects"]
        
        type_count = self.get_type_count(result_bundle, 2)
        attempt_count = dict()
        for i in range(2, len(result_bundle)):
            index = i
            if( "type" not in result_bundle[index]):
                assert False
            try:
                self._test_against_sample_data_stix21(result_bundle[index], result_bundle[index]["type"])        
            except:
                if (result_bundle[index]["type"] in attempt_count):
                    attempt_count[result_bundle[index]["type"]] = attempt_count[result_bundle[index]["type"]] + 1
                else:
                    attempt_count[result_bundle[index]["type"]] = 1
                
                if(attempt_count[result_bundle[index]["type"]] >= type_count[result_bundle[index]["type"]]):
                    raise   
            
    def _test_against_sample_data(self, result_bundle_object, type_name):
        try:
            if(type_name == "x-ibm-finding"):
                self.alert_asserts(result_bundle_object)
            elif(type_name == 'x-oca-event'):
                self.event_asserts(result_bundle_object)       
            elif(type_name == 'process'):
                self.process_asserts(result_bundle_object)   
            elif(type_name == 'file'):
                self.file_asserts(result_bundle_object)   
            elif(type_name == 'directory'):
                self.directory_asserts(result_bundle_object)   
            elif(type_name == 'x509-certificate'):
                self.certificate_asserts(result_bundle_object)   
            elif(type_name == 'user-account'):
                self.user_asserts(result_bundle_object)   
            elif(type_name == 'software'):
                self.software_asserts(result_bundle_object)   
            elif(type_name == 'x-oca-asset'):
                self.asset_asserts(result_bundle_object)   
            elif(type_name == 'ipv4-addr'):
                self.ip_asserts(result_bundle_object)   
            elif(type_name == 'x-ibm-ttp-tagging'):
                self.ttp_tagging_asserts(result_bundle_object)
            elif(type_name == 'x-tanium-action'):
                self.x_action(result_bundle_object)
            elif(type_name == 'x-tanium-inteldocument'):
                self.x_tanium_inteldocument(result_bundle_object)
            elif(type_name == 'x-compiled-terms'):
                self.x_compiled_terms(result_bundle_object)
            elif(type_name == 'x-Tanium'):
                #Unmapped fields aren't necessarily an error (In this case they map be duplicates)
                self.x_tanium(result_bundle_object)
            else:
                raise   
        except:
            raise
        
    def _test_against_sample_data_stix21(self, result_bundle_object, type_name):
        try:
            if(type_name == "x-ibm-finding"):
                self.alert_asserts(result_bundle_object)
            elif(type_name == 'x-oca-event'):
                self.event_asserts(result_bundle_object)       
            elif(type_name == 'process'):
                self.process_asserts21(result_bundle_object)   
            elif(type_name == 'file'):
                self.file_asserts21(result_bundle_object)   
            elif(type_name == 'directory'):
                self.directory_asserts(result_bundle_object)   
            elif(type_name == 'x509-certificate'):
                self.certificate_asserts(result_bundle_object)   
            elif(type_name == 'user-account'):
                self.user_asserts(result_bundle_object)   
            elif(type_name == 'software'):
                self.software_asserts(result_bundle_object)   
            elif(type_name == 'x-oca-asset'):
                self.asset_asserts(result_bundle_object)   
            elif(type_name == 'ipv4-addr'):
                self.ip_asserts(result_bundle_object)   
            elif(type_name == 'x-ibm-ttp-tagging'):
                self.ttp_tagging_asserts(result_bundle_object)
            elif(type_name == 'x-tanium-action'):
                self.x_action(result_bundle_object)
            elif(type_name == 'x-tanium-inteldocument'):
                self.x_tanium_inteldocument(result_bundle_object)
            elif(type_name == 'x-compiled-terms'):
                self.x_compiled_terms(result_bundle_object)
            elif(type_name == 'x-Tanium'):
                #Unmapped fields aren't necessarily an error (In this case they map be duplicates)
                self.x_tanium(result_bundle_object)
            else:
                raise   
        except:
            raise

    def get_type_count(self, result_bundle, initial_index):
        #There may be multiple objects with the same type name.
        #This gets a count of those objects.
        type_count = dict()
        
        for i in range(initial_index, len(result_bundle)):
            index = i
            if(initial_index == 1):
                index = str(i)

            if( "type" not in result_bundle[index]):
                assert False
            
            if (result_bundle[index]["type"] in type_count):
                type_count[result_bundle[index]["type"]] =  type_count[result_bundle[index]["type"]] + 1
            else:
                type_count[result_bundle[index]["type"]] = 1
            
        return type_count
    
    def alert_asserts(self, result_bundle_object):
        assert result_bundle_object["finding_type"] == "alert"        
        assert result_bundle_object["alert_id"] == 2
        assert result_bundle_object["severity"] == 0
        assert result_bundle_object["dst_os_user_ref"] is not None
        assert result_bundle_object["dst_os_ref"] is not None
        assert result_bundle_object["dst_ip_ref"] is not None
        assert result_bundle_object["time_observed"] == "2023-10-16T12:29:34.849Z"
        assert result_bundle_object["name"] == "Testing eicar"
        assert result_bundle_object["description"] == "Alerting on eicar file present on windows system"
        assert result_bundle_object["event_count"] == 8
        assert result_bundle_object["ttp_tagging_refs"] is not None
        
        assert result_bundle_object["x_eid"] == 1003
        assert result_bundle_object["x_type"] == "detect.match"
        assert result_bundle_object["x_guid"] == "00000000-0000-0000-114a-7429237cffc5"
        assert result_bundle_object["x_priority"] == "high"
        assert result_bundle_object["x_intel_id"] == 700
        assert result_bundle_object["x_config_rev_id"] == 1
        assert result_bundle_object["x_intel_doc_id"] == 700
        assert result_bundle_object["x_grouping_id"] == 2
        assert result_bundle_object["x_intel_doc_revision_id"] == 1
        assert result_bundle_object["x_config_id"] == 2
        assert result_bundle_object["x_path"] == 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
        assert result_bundle_object["x_received_at"] == '2023-10-16T12:29:34.609Z'
        assert result_bundle_object["x_alerted_at"] == "2023-10-16T12:26:51.000Z"
        assert result_bundle_object["x_acked_at"] == "2023-10-16T12:38:03.961Z"
        assert result_bundle_object["x_first_eid_resolution_attempt"] == "2023-10-16T12:29:37.091Z"
        assert result_bundle_object["x_intel_doc_ref"] is not None
        
        assert result_bundle_object["x_match_hash"] == "17914125682699366401"
        assert result_bundle_object["x_match_type"] == "process"
        assert result_bundle_object["x_match_source"] == "recorder"
        assert result_bundle_object["x_match_version"] == 1
        assert result_bundle_object["x_match_unique_event_id"] == "4611686018427965350"
        assert result_bundle_object["x_match_process_ref"] is not None
        assert result_bundle_object["x_match_recorder_id"] == "3994044258139188996"
        assert result_bundle_object["x_match_unique_event_id"] == "4611686018427965350"
        assert result_bundle_object["x_match_process_ref"]  is not None
        assert result_bundle_object["x_match_recorder_id"] == "3994044258139188996"
        
        assert result_bundle_object["x_finding_source_name"] == "recorder"
        assert result_bundle_object["x_finding_process_ref"]  is not None
        assert result_bundle_object["x_finding_id"] == "1245935966959239109"
        assert result_bundle_object["x_finding_domain"] == "threatresponse"
        assert result_bundle_object["x_finding_hunt_id"] == "2"
        assert result_bundle_object["x_finding_intel_id"] == "700:1:8ebe28bf-1acb-41b7-9f30-7b40a9145b1d"
        assert result_bundle_object["x_finding_last_seen"] == "2023-10-16T12:26:51.000Z"
        assert result_bundle_object["x_finding_threat_id"] == "901388892329936882"
        assert result_bundle_object["x_finding_finding_id"] == "1245935966959239109"
        assert result_bundle_object["x_finding_last_seen"] == "2023-10-16T12:26:51.000Z"
        assert result_bundle_object["x_finding_reporting_id"] == "reporting-id-placeholder"
        
        assert len(result_bundle_object["x_action"]) == 2
                
    def event_asserts(self, result_bundle_object):
        assert result_bundle_object["outcome"] == 'unresolved'
        assert result_bundle_object["process_ref"] is not None
        assert result_bundle_object["file_ref"] is not None
        assert result_bundle_object["user_ref"] is not None
        assert result_bundle_object["category"] == "process"
        assert result_bundle_object["provider"] == 'tanium-signal'
        assert result_bundle_object["action"] == 'Testing eicar'
        assert result_bundle_object["description"] == 'Alerting on eicar file present on windows system'
        assert result_bundle_object["ttp_tagging_refs"] is not None
        
    def process_asserts(self, result_bundle_object):
        assert result_bundle_object["pid"] == 9080
        assert result_bundle_object["arguments"] == ['C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe', '--no-startup-window', '--continue-active-setup']
        assert result_bundle_object["name"] == 'msedge.exe'
        assert result_bundle_object["cwd"] == 'C:/Program Files (x86)/Microsoft/Edge/Application'
        assert result_bundle_object["created"] == '2023-10-13T14:46:31.000Z'
        assert result_bundle_object["binary_ref"] is not None
        assert result_bundle_object["creator_user_ref"] is not None
        
    def process_asserts21(self, result_bundle_object):
        assert result_bundle_object["pid"] == 9080
        assert result_bundle_object["command_line"] == '"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe" --no-startup-window --continue-active-setup'
        assert result_bundle_object["name"] == 'msedge.exe'
        assert result_bundle_object["cwd"] == 'C:/Program Files (x86)/Microsoft/Edge/Application'
        assert result_bundle_object["created_time"] == '2023-10-13T14:46:31.000Z'
        assert result_bundle_object["image_ref"] is not None
        assert result_bundle_object["creator_user_ref"] is not None
    
    def file_asserts(self, result_bundle_object):
        assert result_bundle_object["hashes"] == {'md5':'d193ea4b8d102d020c02dc45af23ff0d', "sha1":'469e259b884043aedac879a96356fb741f82daa8', "sha256":'9ba39dd15eff718ff357db346d0fda3a12c9dbb216511cbb41050fb0d6b3d9c9'}
        assert result_bundle_object["name"] == 'msedge.exe'
        assert result_bundle_object["parent_directory_ref"] is not None
        assert result_bundle_object["x_artifact_hash"] == "15257803663505479322"
        assert result_bundle_object["x_instance_hash"] == "15257803663505479322"
        
    def file_asserts21(self, result_bundle_object):
        assert result_bundle_object["hashes"] == {'MD5':'d193ea4b8d102d020c02dc45af23ff0d', "SHA-1":'469e259b884043aedac879a96356fb741f82daa8', "SHA-256":'9ba39dd15eff718ff357db346d0fda3a12c9dbb216511cbb41050fb0d6b3d9c9'}
        assert result_bundle_object["name"] == 'msedge.exe'
        assert result_bundle_object["parent_directory_ref"] is not None
        assert result_bundle_object["x_artifact_hash"] == "15257803663505479322"
        assert result_bundle_object["x_instance_hash"] == "15257803663505479322"

    def directory_asserts(self, result_bundle_object):
        assert result_bundle_object["path"] == 'C:/Program Files (x86)/Microsoft/Edge/Application'

        
    def certificate_asserts(self, result_bundle_object):
        assert result_bundle_object["issuer"] == 'Microsoft Code Signing PCA 2011'
        assert result_bundle_object["subject"] == 'Microsoft Corporation'
        assert result_bundle_object["x_status"] == 1

        
    def user_asserts(self, result_bundle_object):
        assert result_bundle_object["display_name"] == 'username'
        assert result_bundle_object["is_service_account"] == True
        assert result_bundle_object["user_id"] == 'S-1-5-21-1252622098-4149316198-505502587-500'
        
    def software_asserts(self, result_bundle_object):
        assert result_bundle_object["name"] == 'Microsoft Windows 11 Pro'
        assert result_bundle_object["version"] == '10.0.22621.0.0'
        
    def asset_asserts(self, result_bundle_object):
        assert result_bundle_object["name"] == 'ComputerName'
        assert result_bundle_object["ip_refs"] is not None
        
    def ip_asserts(self, result_bundle_object):
        assert result_bundle_object["value"] == '1.1.1.1'
        
    def ttp_tagging_asserts(self, result_bundle_object):
        assert result_bundle_object["extensions"] is not None
        assert result_bundle_object["extensions"]["technique_id"] == 'T1134.002'
        assert result_bundle_object["extensions"]["technique_name"] == 'Access Token Manipulation Mitigation: Create Process with Token'
        assert result_bundle_object["name"] == 'Access Token Manipulation Mitigation: Create Process with Token'
        
    def x_action(self, result_bundle_object):
        assert result_bundle_object["verb"] == 6
        assert result_bundle_object["binary_ref"] is not None
        assert result_bundle_object["instance_hash"] == "8639093369865776459"
        assert result_bundle_object["artifact_hash"] == "15425104092171844481"
        assert result_bundle_object["timestamp"] == "2022-06-10T23:19:37.000Z"
        assert result_bundle_object["recorder_event_table_id"] == "4611686018468280136"
        
    def x_tanium_inteldocument(self, result_bundle_object):
        assert result_bundle_object["intel_doc_id"] == 700
        assert result_bundle_object["type_version"] == "1.0"
        assert result_bundle_object["md5"] == "b5050a54c2556267931541b944ab0481"
        assert result_bundle_object["blob_id"] == "4ef7353d-ae4c-4eac-9c0b-75522592b438"
        assert result_bundle_object["revision_id"] == 1
        assert result_bundle_object["size"] == 276
        assert result_bundle_object["x_compiled_terms"] is not None
        assert result_bundle_object["operator"] == "or"
        assert result_bundle_object["text"] == "file.path contains 'eicar'"
        assert result_bundle_object["syntax_version"] == 6
        assert result_bundle_object["is_schema_valid"] == True
        assert result_bundle_object["source_id"] == 2
        assert result_bundle_object["unresolved_alert_count"] == 8
        assert result_bundle_object["throttled_finding_count"] == 0
        assert result_bundle_object["allow_auto_disable"] == True
        assert result_bundle_object["disabled"] == False
        assert result_bundle_object["disabled_endpoint_count"] == 0
        assert result_bundle_object["first_deployment_timestamp"] == "2023-10-13T19:28:05.584Z"
        assert result_bundle_object["last_deployment_timestamp"] == "2023-11-28T18:50:31.920Z"
        assert result_bundle_object["status"] == "HIGH_FIDELITY"

    def x_compiled_terms(self, result_bundle_object):
        assert result_bundle_object["condition"] == "contains"
        assert result_bundle_object["negate"] == False
        assert result_bundle_object["value"] == "eicar"
        assert result_bundle_object["object"] == "file"
        assert result_bundle_object["property"] == "path"
        
    #Unmapped fields
    def x_tanium(self, result_bundle_object):
        assert result_bundle_object["intel_intra_ids"] == [{'id_v2': '901388892329936882'}]
