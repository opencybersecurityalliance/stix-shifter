from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers
from stix_shifter_modules.virus_total.entry_point import EntryPoint
import unittest

MODULE = 'virus_total'
RESULTS = 'results'
TRANSFORMERS = get_module_transformers(MODULE)
epoch_to_timestamp_class = TRANSFORMERS.get('EpochToTimestamp')
entry_point = EntryPoint()
DATA_SOURCE = {"type": "identity", "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3", "name": "VirusTotal", "identity_class": "system"}
options = {}
MAP_DATA = entry_point.get_mapping()


class TestTransform(unittest.TestCase):
    def test_virus_total_translation(self):
        ip_data = "203.190.254.239"
        url_data = "https://test.com"
        hash_sha1 = "D5DD920BE5BCFEB904E95DA4B6D0CCCA0727D692"
        data_type_ip = "ip"
        data_type_url = "url"
        data_type_hash = "hash"

        data = {
            "data": [
                {
                    "code": 200,
                    "report": {
                        "success": 'true',
                        "summary": {
                            "taxonomies": [
                                {
                                    "level": "safe",
                                    "namespace": "VT",
                                    "predicate": "GetReport",
                                    "value": "0 detected_url(s)"
                                }
                            ]
                        },
                        "artifacts": [
                            {
                                "dataType": "url",
                                "data": "http://www.icddrb.org/"
                            },
                        ],
                        "full": {
                            "asn": 24323,
                            "undetected_urls": [
                                [
                                    "http://donate.icddrb.org/",
                                    "27343f46e1a7c22d765d92e72cfbf238d5fc973ab2db6ee06113d181e8a5744e",
                                    0,
                                    70,
                                    "2019-06-28 08:58:08"
                                ]
                            ],
                            "undetected_downloaded_samples": [
                                {
                                    "date": "2020-11-20 11:08:14",
                                    "positives": 0,
                                    "total": 76,
                                    "sha256": "f4e301a60e8d885351b8df5614c54f3acc90435022b37fb6803b9a9bf0b0e09a"
                                },
                                {
                                    "date": "2019-10-16 15:56:26",
                                    "positives": 0,
                                    "total": 72,
                                    "sha256": "14c08afc15e276b96c48de6598e86fcc933f3b105a2a18667d395d82c1ea97d5"
                                }
                            ],
                            "country": "BD",
                            "response_code": 1,
                            "as_owner": "aamra networks limited",
                            "verbose_msg": "IP address in dataset",
                            "detected_downloaded_samples": [],
                            "detected_urls": [],
                            "resolutions": [
                                {
                                    "last_resolved": "2019-09-12 00:30:38",
                                    "hostname": "blog.icddrb.org"
                                },
                            ]
                        }
                    },
                    "data": "203.190.254.239",
                    "dataType": "ip"
                }
            ]
        }

        result_translator = entry_point.create_default_results_translator(dialect='default')
        result_translator.map_data = MAP_DATA['to_stix_map']
        ipv4_pattern = result_translator.get_pattern_from_json(data['data'][0])

        data['data'][0]['data'] = url_data
        data['data'][0]['dataType'] = data_type_url
        url_pattern = result_translator.get_pattern_from_json(data['data'][0])

        data['data'][0]['data'] = hash_sha1
        data['data'][0]['dataType'] = data_type_hash
        hash_pattern = result_translator.get_pattern_from_json(data['data'][0])

        data = data['data']
        data = str(data).replace('\'', "\"")
        translate_results = result_translator.translate_results(data_source=str(DATA_SOURCE).replace('\'', "\""), data=data)

        assert ipv4_pattern['pattern'] == "[ipv4-addr:value='203.190.254.239']"
        assert url_pattern['pattern'] == "[url:value='https://test.com']"
        assert hash_pattern['pattern'] == "[file:hashes.'SHA-1'='D5DD920BE5BCFEB904E95DA4B6D0CCCA0727D692']"

        objects = translate_results['objects']
        assert len(objects) == 2

        stix_identity = objects[0]
        stix_indicator = objects[1]

        assert 'type' in stix_identity and stix_identity['type'] == 'identity'
        assert 'spec_version' in translate_results and translate_results['spec_version'] == '2.1'

        assert 'type' in stix_indicator and stix_indicator['type'] == 'indicator'
        assert 'pattern' in stix_indicator
        assert 'valid_from' in stix_indicator
        assert 'type' in stix_indicator and stix_indicator['type'] == 'indicator'

        assert 'x_original_report' in stix_indicator
        assert 'indicator_types' in stix_indicator and len(stix_indicator['indicator_types']) == 1 \
               and stix_indicator['indicator_types'][0] == 'benign'
