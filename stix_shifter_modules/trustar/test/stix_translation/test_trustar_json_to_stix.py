import unittest
import json
from stix_shifter_modules.trustar.entry_point import EntryPoint
from stix_shifter.stix_translation import stix_translation
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers

MODULE = "trustar"
entry_point = EntryPoint()
map_data = entry_point.get_results_translator().map_data
data_source = {
    "type": "identity",
    "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
    "name": "Trustar",
    "identity_class": "events"
}
options = {}

indicator_data = """[
        {
            "indicatorType": "SHA256",
            "value": "02b95ef7a33a87cc2b3b6fd47db03e711045974e1ecf631d3ba9e076e1e374e9",
            "priorityLevel": "NOT_FOUND",
            "firstSeen": 1580083200000,
            "lastSeen": 1631909009550,
            "guid": "SHA256|02b95ef7a33a87cc2b3b6fd47db03e711045974e1ecf631d3ba9e076e1e374e9",
            "SHA256": "02b95ef7a33a87cc2b3b6fd47db03e711045974e1ecf631d3ba9e076e1e374e9",
            "indicatorSummary": {
                "reportId": "dd410136-1fd0-4596-9cd0-a08f8257ef23",
                "enclaveId": "e813003b-4a31-4250-a55d-b669878c4e47",
                "source": {
                    "key": "IBM X-Force",
                    "name": "IBM X-Force"
                },
                "type": "SHA256",
                "value": "02b95ef7a33a87cc2b3b6fd47db03e711045974e1ecf631d3ba9e076e1e374e9",
                "score": {
                    "name": "Malicious Score",
                    "value": "HIGH"
                },
                "description": "SHA256",
                "attributes": [
                    {
                        "name": "MALWARE",
                        "value": "graftor"
                    }
                ],
                "severityLevel": 3
            },
            "meta": {
                "indicatorType": "SHA256",
                "value": "02b95ef7a33a87cc2b3b6fd47db03e711045974e1ecf631d3ba9e076e1e374e9",
                "correlationCount": 0,
                "priorityLevel": "NOT_FOUND",
                "noteCount": 0,
                "sightings": 3,
                "firstSeen": 1580083200000,
                "lastSeen": 1631909009550,
                "enclaveIds": [
                    "a4f3bf67-459e-4332-9483-8f3cd30b515e",
                    "e813003b-4a31-4250-a55d-b669878c4e47",
                    "f7070f51-5153-42ff-b2d7-dd93148597b3"
                ],
                "tags": [],
                "source": "",
                "notes": [],
                "guid": "SHA256|02b95ef7a33a87cc2b3b6fd47db03e711045974e1ecf631d3ba9e076e1e374e9"
            }
        },
        {
            "id": "dd410136-1fd0-4596-9cd0-a08f8257ef23",
            "created": 1631909009549,
            "updated": 1631909009549,
            "title": "X-Force SHA256 02b95ef7a33a87cc2b3b6fd47db03e711045974e1ecf631d3ba9e076e1e374e9",
            "distributionType": "ENCLAVE",
            "enclaveIds": [
                "e813003b-4a31-4250-a55d-b669878c4e47"
            ],
            "tags": [],
            "indicators": [
                {
                    "indicatorType": "SHA256",
                    "value": "02b95ef7a33a87cc2b3b6fd47db03e711045974e1ecf631d3ba9e076e1e374e9",
                    "guid": "SHA256|02b95ef7a33a87cc2b3b6fd47db03e711045974e1ecf631d3ba9e076e1e374e9"
                }
            ]
        },
        {
            "id": "9e509316-b8f2-428e-9981-0e552bb128bf",
            "created": 1631908125997,
            "updated": 1631908125997,
            "title": "XFTI_loader_LockdownLoader.yar",
            "distributionType": "ENCLAVE",
            "enclaveIds": [
                "a4f3bf67-459e-4332-9483-8f3cd30b515e"
            ],
            "tags": [
                {
                    "guid": "github",
                    "name": "github",
                    "enclaveId": "a4f3bf67-459e-4332-9483-8f3cd30b515e"
                },
                {
                    "guid": "yara",
                    "name": "yara",
                    "enclaveId": "a4f3bf67-459e-4332-9483-8f3cd30b515e"
                }
            ],
            "indicators": [
                {
                    "indicatorType": "SHA256",
                    "value": "02b95ef7a33a87cc2b3b6fd47db03e711045974e1ecf631d3ba9e076e1e374e9",
                    "guid": "SHA256|02b95ef7a33a87cc2b3b6fd47db03e711045974e1ecf631d3ba9e076e1e374e9"
                },
                {
                    "indicatorType": "SHA256",
                    "value": "5062feb40494a654ec45020041e25e5fd2b31980b2345567b75057f25643b240",
                    "guid": "SHA256|5062feb40494a654ec45020041e25e5fd2b31980b2345567b75057f25643b240"
                },
                {
                    "indicatorType": "SHA256",
                    "value": "572035998404c20482c0af1062beb261f5a6235305041f77b24ff5031e7c0694",
                    "guid": "SHA256|572035998404c20482c0af1062beb261f5a6235305041f77b24ff5031e7c0694"
                },
                {
                    "indicatorType": "SOFTWARE",
                    "value": "kernel32.dll",
                    "guid": "SOFTWARE|kernel32.dll"
                },
                {
                    "indicatorType": "SOFTWARE",
                    "value": "svchost.bin",
                    "guid": "SOFTWARE|svchost.bin"
                }
            ]
        }
    ]"""

class TestTrustarTransform(unittest.TestCase, object):
    @staticmethod
    def get_first(itr, constraint):
        return next(
            (obj for obj in itr if constraint(obj)),
            None
        )

    @staticmethod
    def get_first_of_type(itr, typ):
        return TestTrustarTransform.get_first(itr, lambda o: type(o) == dict and o.get('type') == typ)

    @staticmethod
    def get_first_process(itr, typ):
        return TestTrustarTransform.get_first(itr, lambda o: type(o) == dict and o.get(
            'type') == typ and "parent_ref" in o)

    def test_trustar_api_results_to_stix(self):
        results = json.loads(indicator_data)
        result_bundle = entry_point.translate_results(json.dumps(data_source), json.dumps(results))

        assert (result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert ('objects' in observed_data)
        objects = observed_data['objects']

        curr_obj = TestTrustarTransform.get_first_of_type(objects.values(), 'file')
        assert (curr_obj is not None), 'file object type not found'
        assert (curr_obj.keys() == {'type','hashes'})
        assert (curr_obj['hashes']['SHA-256'] == '02b95ef7a33a87cc2b3b6fd47db03e711045974e1ecf631d3ba9e076e1e374e9')

        curr_obj = TestTrustarTransform.get_first_of_type(objects.values(), 'x-trustar-indicator')
        assert (curr_obj is not None), 'x-trustar-indicator object type not found'
        assert (curr_obj.keys() == {'type', 'attributes','firstseen', 'lastseen', 'prioritylevel', 'guid', 'meta', 'enclaveid', 'source', 'score','name', 'severitylevel'})
        assert (curr_obj['firstseen'] == '2020-01-27T00:00:00.000Z')
        assert (curr_obj['lastseen'] == '2021-09-17T20:03:29.550Z')
