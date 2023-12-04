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

SAMPLE_DATA_DICT = {
    "details":
    {
        "finding": 
        {
            "whats": 
            [{
                "intel_intra_ids": 
                [{
                    "id": 1204114022
                },
                {
                    "id": 1670888670
                },
                {
                    "id": 2753281896
                },
                {
                    "id": 3854795733
                }],
                "source_name": "recorder",
                "artifact_activity": 
                {
                    "relevant_actions": [{
                    },
                    {
                        "verb": 6,
                        "target": 
                        {
                            "file": 
                            {
                                "path": "C:\\Users\\Bob\\AppData\\Local\\Temp\\gfw-install-CZejgRlL.exe",
                                "hash": 
                                {
                                    "md5": "d41d8cd98f00b204e9800998ecf8427e",
                                    "sha1": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
                                    "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
                                },
                                "size_bytes": 
                                {  
                                },
                                "modification_time": "2022-06-10T23:19:37.000Z",
                                "instance_hash_salt": "132993767777627641"
                            },
                            "instance_hash": "8639093369865776459",
                            "artifact_hash": "15425104092171844481"
                        },
                        "timestamp": "2022-06-10T23:19:37.000Z",
                        "tanium_recorder_event_table_id": "4611686018468280136"
                    },
                    {
                        "verb": 6,
                        "target": 
                        {
                            "file": 
                            {
                                "path": "C:\\Users\\Bob\\AppData\\Local\\Temp\\gfw-install-CZejgRlL.exe",
                                "hash": 
                                {
                                    "md5": "d41d8cd98f00b204e9800998ecf8427e",
                                    "sha1": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
                                    "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
                                },
                                "size_bytes": 
                                {
                                },
                                "modification_time": "2022-06-10T23:19:37.000Z",
                                "instance_hash_salt": "132993767777627641"
                            },
                            "instance_hash": "8639093369865776459",
                            "artifact_hash": "15425104092171844481"
                        },
                        "timestamp": "2022-06-10T23:19:37.000Z",
                        "tanium_recorder_event_table_id": "4611686018468280136"
                    }],
                    "acting_artifact": 
                    {
                        "process": 
                        {
                            "handles": 
                            [
                            ],
                            "pid": 8372,
                            "arguments": "\"C:\\Program Files\\Git\\usr\\bin\\mktemp.exe\" -t gfw-install-XXXXXXXX.exe",
                            "file": 
                            {
                                "file": 
                                {
                                    "path": "C:\\Program Files\\Git\\usr\\bin\\mktemp.exe",
                                    "hash": 
                                    {
                                        "md5": "2204459dcbf34aed8906daac26db6f56"
                                    }
                                },
                                "instance_hash": "7306911300040087486",
                                "artifact_hash": "7306911300040087486"
                            },
                            "user": 
                            {
                                "user": 
                                {
                                    "name": "Bob",
                                    "domain": "MEDIATOO"
                                }
                            },
                            "parent": 
                            {
                                "process": 
                                {
                                    "handles": 
                                    [],
                                    "pid": 7528,
                                    "arguments": "sh \"C:\\\\Program Files\\\\Git\\\\mingw64\\\\bin\\\\git-update-git-for-windows\" --quiet --gui",
                                    "file": 
                                    {
                                        "file": 
                                        {
                                            "path": "C:\\Program Files\\Git\\usr\\bin\\sh.exe",
                                            "hash": 
                                            {
                                                "md5": "0d46559e826c8a7b5d432d0a91954ba2"
                                            }
                                        },
                                        "instance_hash": "4573824187960625975",
                                        "artifact_hash": "4573824187960625975"
                                    },
                                    "user": 
                                    {
                                        "user": 
                                        {
                                            "name": "Bob",
                                            "domain": "MEDIATOO"
                                        }
                                    },
                                    "start_time": "2022-06-10T23:19:37.000Z",
                                    "tanium_unique_id": "8426546338933681227"
                                },
                                "instance_hash": "2725601412602158353",
                                "artifact_hash": "6063500060437154276"
                            },
                            "start_time": "2022-06-10T23:19:37.000Z",
                            "tanium_unique_id": "3601155573093657773"
                        },
                        "instance_hash": "17370642301569032073",
                        "artifact_hash": "16343609532904785305",
                        "is_intel_target": "true"
                    }
                }
            }],
            "domain": "threatresponse",
            "intel_id": "365:2:761d796b-b362-455f-98ae-6d0472ecf640",
            "hunt_id": "1",
            "threat_id": "1204114022,1670888670,2753281896,3854795733",
            "source_name": "recorder",
            "system_info": 
            {
                "os": "Microsoft Windows 11 Pro",
                "bits": 64,
                "platform": "Windows",
                "build_number": "22000",
                "patch_level": "10.0.22000.0.0"
            },
            "first_seen": "2022-06-10T23:19:38.000Z",
            "last_seen": "2022-06-10T23:19:38.000Z",
            "finding_id": "2433404061633741123",
            "reporting_id": "reporting-id-placeholder"
        },
        "match": 
        {
            "version": 1,
            "type": "process",
            "source": "recorder",
            "hash": "16343609532904785305",
            "properties": 
            {
                "pid": 8372,
                "args": "\"C:\\Program Files\\Git\\usr\\bin\\mktemp.exe\" -t gfw-install-XXXXXXXX.exe",
                "recorder_unique_id": "3601155573093657773",
                "start_time": "2022-06-10T23:19:37.000Z",
                "ppid": 7528,
                "user": "MEDIATOO\\Bob",
                "file": 
                {
                    "md5": "2204459dcbf34aed8906daac26db6f56",
                    "fullpath": "C:\\Program Files\\Git\\usr\\bin\\mktemp.exe"
                },
                "parent": 
                {
                    "pid": 7528,
                    "args": "sh \"C:\\\\Program Files\\\\Git\\\\mingw64\\\\bin\\\\git-update-git-for-windows\" --quiet --gui",
                    "recorder_unique_id": "8426546338933681227",
                    "start_time": "2022-06-10T23:19:37.000Z",
                    "ppid": 10396,
                    "user": "MEDIATOO\\Bob",
                    "file": 
                    {
                        "md5": "0d46559e826c8a7b5d432d0a91954ba2",
                        "fullpath": "C:\\Program Files\\Git\\usr\\bin\\sh.exe"
                    }
                }
            }
        }
    },
    "MITRE Techniques": "[\"T1036\",\"T1036.001\"]",
    "Impact Score": ""
}

class TestTaniumResultsToStix(unittest.TestCase, object):
    def test_get_observed_data_objects(self):
        result_bundle = json_to_stix_translator.convert_to_stix(
        data_source, map_data, [SAMPLE_DATA_DICT], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        print(result_bundle_objects)

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data