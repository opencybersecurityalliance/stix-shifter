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
options = {}

sample_files_location = os.getcwd() + "/stix-shifter/stix_shifter_modules/tanium/tests"

class TestTaniumResultsToStix(unittest.TestCase, object):
    def test_confirm_objects_parse(self):
        sample_data_large = open(sample_files_location + "/Sample_Data.json", "r")
        sample_data_tanium = open(sample_files_location + "/Sample_Data_Tanium.json", "r")

        sample_data_large_json = json.load(sample_data_large)
        sample_data_tanium_json = json.load(sample_data_tanium)
        for alert in sample_data_large_json["data"]:
            result_bundle_large = json_to_stix_translator.convert_to_stix(data_source, map_data, [alert], get_module_transformers(MODULE), options)
            assert len(result_bundle_large["objects"][1]["objects"]) > 5
        
        result_bundle_tanium = json_to_stix_translator.convert_to_stix(data_source, map_data, [sample_data_tanium_json], get_module_transformers(MODULE), options)
        assert len(result_bundle_tanium["objects"][1]["objects"]) > 5
    
    def test_results_no_parent(self):
        sample_data_large = open(sample_files_location + "/Sample_Data.json", "r")
        sample_data_large_json = json.load(sample_data_large)
        
        #There are many events in the sample. For the unit testing I will only be using the first two.
        #The first one has no parent process. The second has one.
        alert = sample_data_large_json["data"][0]
        result_bundle_large = json_to_stix_translator.convert_to_stix(data_source, map_data, [alert], get_module_transformers(MODULE), options)
        result_bundle = result_bundle_large["objects"][1]["objects"]
        
        type_count = self.get_type_count(result_bundle)
        attempt_count = dict()
        for i in range(0, len(result_bundle), +1):
            index = str(i)
            if( "type" not in result_bundle[index]):
                assert False
            try:
                self._test_against_sample_data(result_bundle[index], result_bundle[index]["type"])        
            except:
                if (result_bundle[index]["type"] in attempt_count):
                    attempt_count[result_bundle[index]["type"]] = result_bundle[index]["type"] + 1
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
        except:
            raise

    def get_type_count(self, result_bundle):
        #There may be multiple objects with the same type name.
        #This gets a count of those objects.
        type_count = dict()
        for i in range(0, len(result_bundle), +1):
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
        assert result_bundle_object["time_observed"] == '2023-10-16T12:26:51.000Z'
        assert result_bundle_object["action"] == 'Testing eicar'
        assert result_bundle_object["description"] == 'Alerting on eicar file present on windows system'
        assert result_bundle_object["ttp_tagging_refs"] is not None
        
    def event_asserts(self, result_bundle_object):
        assert result_bundle_object["outcome"] == 'unresolved'
        assert result_bundle_object["severity"] == 0
        assert result_bundle_object["process_ref"] is not None
        assert result_bundle_object["file_ref"] is not None
        assert result_bundle_object["user_ref"] is not None
        assert result_bundle_object["host_ref"] is not None
        assert result_bundle_object["category"] == "process"
        assert result_bundle_object["created"] == '2023-10-16T12:26:51.000Z'
        assert result_bundle_object["provider"] == 'tanium-signal'
        assert result_bundle_object["action"] == 'Testing eicar'
        assert result_bundle_object["description"] == 'Alerting on eicar file present on windows system'
        
    def process_asserts(self, result_bundle_object):
        assert result_bundle_object["pid"] == 9080
        assert result_bundle_object["args"] == ['C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe', '--no-startup-window', '--continue-active-setup']
        assert result_bundle_object["name"] == 'msedge.exe'
        assert result_bundle_object["cwd"] == 'C:/Program Files (x86)/Microsoft/Edge/Application'
        assert result_bundle_object["created"] == '2023-10-13T14:46:31.000Z'
        assert result_bundle_object["binary_ref"] is not None
        assert result_bundle_object["creator_user_ref"] is not None
    
    def file_asserts(self, result_bundle_object):
        assert result_bundle_object["hashes"] == {'md5':'d193ea4b8d102d020c02dc45af23ff0d', "sha1":'469e259b884043aedac879a96356fb741f82daa8', "sha256":'9ba39dd15eff718ff357db346d0fda3a12c9dbb216511cbb41050fb0d6b3d9c9'}
        assert result_bundle_object["name"] == 'msedge.exe'
        assert result_bundle_object["parent_directory_ref"] is not None

    def directory_asserts(self, result_bundle_object):
        assert result_bundle_object["path"] == 'C:/Program Files (x86)/Microsoft/Edge/Application'
        
    def certificate_asserts(self, result_bundle_object):
        assert result_bundle_object["issuer"] == 'Microsoft Code Signing PCA 2011'
        assert result_bundle_object["subject"] == 'Microsoft Corporation'
        
    def user_asserts(self, result_bundle_object):
        assert result_bundle_object["display_name"] == 'username'
        assert result_bundle_object["is_service_account"] == True
        assert result_bundle_object["user_id"] == 'S-1-5-21-1252622098-4149316198-505502587-500'
        
    def software_asserts(self, result_bundle_object):
        assert result_bundle_object["name"] == 'Microsoft Windows 11 Pro'
        assert result_bundle_object["version"] == '10.0.22621.0.0'
        
    def asset_asserts(self, result_bundle_object):
        assert result_bundle_object["hostname"] == 'ComputerName'
        assert result_bundle_object["ip_refs"] is not None
        
    def ip_asserts(self, result_bundle_object):
        assert result_bundle_object["value"] == '1.1.1.1'
        
    def ttp_tagging_asserts(self, result_bundle_object):
        assert result_bundle_object["extensions"] is not None
        assert result_bundle_object["extensions"]["technique_id"] == 'T1134.002'
        assert result_bundle_object["extensions"]["technique_name"] == 'Access Token Manipulation Mitigation: Create Process with Token'
        assert result_bundle_object["extensions"]["tactic_name"] == ''
        assert result_bundle_object["name"] == 'Access Token Manipulation Mitigation: Create Process with Token'
