import json
import unittest
from functools import wraps
from stix_shifter_modules.threat_q.entry_point import EntryPoint

MODULE = "threat_q"
DATA_SOURCE = {"type": "identity", "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
               "name": "ThreatQ_Connector", "identity_class": "system"}
options = {'stix_validator':True}
entry_point = EntryPoint(options=options)
ip_value = "167.62.182.250"
extension_types = ['toplevel-property-extension']
extension_properties = ['x_ibm_original_threat_feed_data','threat_score', 'threat_attributes']
query_pattern = "[ipv4-addr:value='"+ip_value+"']"
hash_value = '35d60d2723c649c97b414b3cb701df1c'
hash_query_pattern = "[file:hashes.MD5='"+hash_value+"']"
url_value = "linkprotect.cudasvc.com/url"
url_query_pattern = "[url:value='"+url_value+"']"
domain_name = "www.cnn.com"
domain_query_pattern = "[domain-name:value='"+domain_name+"']"
transmitQueryData = {
            "data": [
                {
                    "total": 1,
                    "offset": 0,
                    "limit": 500,
                    "code": 200,
                    "code": 200,
                    "report": [
                            {
                            "class": "network",
                            "score": 0,
                            "value": "167.62.182.250",
                            "expires_calculated_at": "2022-03-18 10:30:43",
                            "touched_at": "2022-03-18 11:02:00",
                            "id": 2543380,
                            "updated_at": "2022-03-18 10:29:12",
                            "published_at": "2022-03-11 10:15:03",
                            "created_at": "2022-03-18 10:29:12",
                            "status_id": 1,
                            "hash": "d76a48506da0edfdff3947118b8b5731",
                            "type_id": 15,
                            "adversaries": [],
                            "type": {
                                "name": "IP Address",
                                "id": 15,
                                "class": "network"
                            },
                            "status": {
                                "name": "Active",
                                "id": 1,
                                "description": "Poses a threat and is being exported to detection tools."
                            },
                            "attributes": [
                                {
                                    "value": "Dridex - 2020826",
                                    "created_at": "2022-03-18 10:29:13",
                                    "indicator_id": 2543380,
                                    "updated_at": "2022-03-18 10:29:13",
                                    "attribute_id": 184,
                                    "id": 5252913,
                                    "touched_at": "2022-03-18 10:29:13",
                                    "name": "Title"
                                },
                                {
                                    "value": "2022-04-09T00:00:00",
                                    "created_at": "2022-03-18 10:29:13",
                                    "indicator_id": 2543380,
                                    "updated_at": "2022-03-18 10:29:13",
                                    "attribute_id": 186,
                                    "id": 5252914,
                                    "touched_at": "2022-03-18 10:29:13",
                                    "name": "Expiration"
                                },
                                {
                                    "value": "True",
                                    "created_at": "2022-03-18 10:29:13",
                                    "indicator_id": 2543380,
                                    "updated_at": "2022-03-18 10:29:13",
                                    "attribute_id": 187,
                                    "id": 5252915,
                                    "touched_at": "2022-03-18 10:29:13",
                                    "name": "Is Active"
                                }
                            ],
                            "sources": [
                                {
                                    "indicator_id": 2543380,
                                    "indicator_status_id": 1,
                                    "published_at": "2022-03-11 10:15:03",
                                    "source_id": 20,
                                    "id": 13604439,
                                    "created_at": "2022-03-18 10:29:13",
                                    "source_type": "connectors",
                                    "creator_source_id": 20,
                                    "indicator_type_id": 15,
                                    "reference_id": 11,
                                    "updated_at": "2022-03-18 10:29:13",
                                    "name": "AlienVault OTX Pulse"
                                }
                            ],
                            "enrich_info": {
                                "attributes": [
                                    {
                                        "id": 5252913,
                                        "indicator_id": 2543380,
                                        "attribute_id": 184,
                                        "value": "Dridex - 2020826",
                                        "created_at": "2022-03-18 10:29:13",
                                        "updated_at": "2022-03-18 10:29:13",
                                        "touched_at": "2022-03-18 10:29:13.014",
                                        "name": "Title",
                                        "sources": [
                                            {
                                                "id": 20,
                                                "type": "connectors",
                                                "reference_id": 11,
                                                "name": "AlienVault OTX Pulse",
                                                "tlp_id": None,
                                                "created_at": "2022-03-18 10:29:13",
                                                "updated_at": "2022-03-18 10:29:13",
                                                "published_at": "2022-03-11 10:15:03.000",
                                                "pivot": {
                                                    "indicator_attribute_id": 5252913,
                                                    "source_id": 20,
                                                    "id": 5269046,
                                                    "creator_source_id": 20
                                                }
                                            }
                                        ],
                                        "attribute": {
                                            "id": 184,
                                            "name": "Title",
                                            "created_at": "2022-01-19 20:22:43",
                                            "updated_at": "2022-01-19 20:22:43"
                                        }
                                    },
                                    {
                                        "id": 5252914,
                                        "indicator_id": 2543380,
                                        "attribute_id": 186,
                                        "value": "2022-04-09T00:00:00",
                                        "created_at": "2022-03-18 10:29:13",
                                        "updated_at": "2022-03-18 10:29:13",
                                        "touched_at": "2022-03-18 10:29:13.021",
                                        "name": "Expiration",
                                        "sources": [
                                            {
                                                "id": 20,
                                                "type": "connectors",
                                                "reference_id": 11,
                                                "name": "AlienVault OTX Pulse",
                                                "tlp_id": None,
                                                "created_at": "2022-03-18 10:29:13",
                                                "updated_at": "2022-03-18 10:29:13",
                                                "published_at": "2022-03-11 10:15:03.000",
                                                "pivot": {
                                                    "indicator_attribute_id": 5252914,
                                                    "source_id": 20,
                                                    "id": 5269047,
                                                    "creator_source_id": 20
                                                }
                                            }
                                        ],
                                        "attribute": {
                                            "id": 186,
                                            "name": "Expiration",
                                            "created_at": "2022-01-19 20:22:43",
                                            "updated_at": "2022-01-19 20:22:43"
                                        }
                                    },
                                    {
                                        "id": 5252915,
                                        "indicator_id": 2543380,
                                        "attribute_id": 187,
                                        "value": "True",
                                        "created_at": "2022-03-18 10:29:13",
                                        "updated_at": "2022-03-18 10:29:13",
                                        "touched_at": "2022-03-18 10:29:13.028",
                                        "name": "Is Active",
                                        "sources": [
                                            {
                                                "id": 20,
                                                "type": "connectors",
                                                "reference_id": 11,
                                                "name": "AlienVault OTX Pulse",
                                                "tlp_id": None,
                                                "created_at": "2022-03-18 10:29:13",
                                                "updated_at": "2022-03-18 10:29:13",
                                                "published_at": "2022-03-11 10:15:03.000",
                                                "pivot": {
                                                    "indicator_attribute_id": 5252915,
                                                    "source_id": 20,
                                                    "id": 5269048,
                                                    "creator_source_id": 20
                                                }
                                            }
                                        ],
                                        "attribute": {
                                            "id": 187,
                                            "name": "Is Active",
                                            "created_at": "2022-01-19 20:22:43",
                                            "updated_at": "2022-01-19 20:22:43"
                                        }
                                    }
                                ],
                                "Comments": "Additional attribute information is available on the ThreatQ platform."
                            },
                            "relationships": {
                                "malware": [],
                                "attack_pattern": [],
                                "campaign": [],
                                "ttp": [],
                                "tool": []
                            }
                        }
                    ],
                    "data": ip_value,
                    "dataType": "ip",
                    "namespace": "8bf42ea1-e30d-41a2-a3ee-1aec759cf409",
                    "external_reference": {
                        "source_name": "ThreatQ_Connector",
                        "url": "https://threatq.com"
                    },
                }
            ]
        }

class TestThreatQResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for translate results
    """

    def __init__(self,*args, **kwargs):
        super(TestThreatQResultsToStix, self).__init__(*args, **kwargs)
        self.result_translator = entry_point.create_default_results_translator(dialect='default')
    
    @staticmethod
    def exists(obj, chain):
        """
        Check if the nested keys exist in the dictionary or not
        """
        _key = chain.pop(0)
        if _key in obj:
            return TestThreatQResultsToStix.exists(obj[_key], chain) if chain else obj[_key]
    
    @staticmethod
    def get_first(itr, constraint):
        return next(
            (obj for obj in itr if constraint(obj)),
            None
        )

    @staticmethod
    def get_first_of_type(itr, typ):
        return TestThreatQResultsToStix.get_first(itr, lambda o: type(o) == dict and o.get('type') == typ)
    
    def check_stix_bundle_type(func):
        """
        decorator function to convert the data source query result into stix bundle
        """
        @wraps(func)
        def wrapper_func(self, *args, **kwargs):
            self.result_bundle = self.result_translator.translate_results(data_source=DATA_SOURCE, data=transmitQueryData['data'])
            self.result_bundle_objects = self.result_bundle['objects']
            assert self.result_bundle['type'] == 'bundle'
            return func(self, *args, **kwargs)
        return wrapper_func

    @check_stix_bundle_type
    def test_stix_identity_prop(self):
        """
        to test the identity stix object properties
        """
        stix_identity = TestThreatQResultsToStix.get_first_of_type(self.result_bundle_objects, DATA_SOURCE['type'])
        assert 'type' in stix_identity and stix_identity['type'] == DATA_SOURCE['type']
        assert 'name' in stix_identity and stix_identity['name'] == DATA_SOURCE['name']
        assert 'identity_class' in stix_identity and stix_identity['identity_class'] == DATA_SOURCE['identity_class']
    
    @check_stix_bundle_type
    def test_stix_extension_prop(self):
        """
        to test the extension stix object properties
        """
        sdo_type = 'extension-definition'
        stix_extension = TestThreatQResultsToStix.get_first_of_type(self.result_bundle_objects, sdo_type)
        assert 'type' in stix_extension and stix_extension['type'] == sdo_type
        assert 'name' in stix_extension
        assert 'version' in stix_extension
        assert 'extension_types' in stix_extension and stix_extension['extension_types'] == extension_types
        assert 'extension_properties' in stix_extension and stix_extension['extension_properties'] == extension_properties
    
    @check_stix_bundle_type
    def test_stix_indicator_prop(self):
        """
        to test the indicator stix object properties
        """
        sdo_type = 'indicator'
        stix_indicator = TestThreatQResultsToStix.get_first_of_type(self.result_bundle_objects, sdo_type)
        assert 'type' in stix_indicator and stix_indicator['type'] == sdo_type
        assert 'pattern' in stix_indicator and stix_indicator['pattern'] == query_pattern
        assert 'valid_from' in stix_indicator
        assert 'created' in stix_indicator
        assert 'modified' in stix_indicator
        assert 'indicator_types' in stix_indicator and len(stix_indicator['indicator_types']) == 1 \
               and stix_indicator['indicator_types'][0] == 'malicious-activity'
        assert 'external_references' in stix_indicator and len(stix_indicator['external_references']) > 0
        assert 'url' in stix_indicator['external_references'][0]
    
    @check_stix_bundle_type
    def test_stix_indicator_extensions_prop(self):
        """
        to test the indicator stix object extensions properties
        """
        stix_indicator = TestThreatQResultsToStix.get_first_of_type(
            self.result_bundle_objects, 'indicator')
        assert 'x_ibm_original_threat_feed_data' in stix_indicator
        extension_property = extension_properties[0]
        property_name = "x_ibm_original_threat_feed_data.full"
        is_exist = TestThreatQResultsToStix.exists(
            stix_indicator, property_name.split("."))
        assert is_exist is not None
        assert stix_indicator[extension_property]["full"][0]
        assert stix_indicator[extension_property]["full"][0]['attributes']
        assert stix_indicator[extension_property]["full"][0]['enrich_info']
        attribute_property = "threat_attributes"
        assert attribute_property in stix_indicator
        assert "threat_score" in stix_indicator
    
    def test_indicator_hash_query_pattern(self):
        """
        to test the indicator stix object extensions properties with hash query pattern
        """
        transmitData = {
            "data": [
                {
                    "total": 1,
                    "offset": 0,
                    "limit": 500,
                    "code": 200,
                    "code": 200,
                    "report": [
                        {
                            "class": "host",
                            "score": 0,
                            "value": "35d60d2723c649c97b414b3cb701df1c",
                            "expires_calculated_at": "2022-03-18 10:30:43",
                            "touched_at": "2022-03-18 11:01:54",
                            "id": 2543358,
                            "updated_at": "2022-03-18 10:28:15",
                            "published_at": "2020-01-23 09:27:39",
                            "created_at": "2022-03-18 10:28:15",
                            "status_id": 1,
                            "hash": "56a6b7766ee4ff9c78b3d6a000d16156",
                            "type_id": 18,
                            "adversaries": [],
                            "type": {
                                "name": "MD5",
                                "id": 18,
                                "class": "host"
                            },
                            "status": {
                                "name": "Active",
                                "id": 1,
                                "description": "Poses a threat and is being exported to detection tools."
                            },
                            "attributes": [
                                {
                                    "value": "True",
                                    "created_at": "2022-03-18 10:28:16",
                                    "indicator_id": 2543358,
                                    "updated_at": "2022-03-18 10:28:16",
                                    "attribute_id": 187,
                                    "id": 5252887,
                                    "touched_at": "2022-03-18 10:28:16",
                                    "name": "Is Active"
                                }
                            ],
                            "sources": [
                                {
                                    "indicator_id": 2543358,
                                    "indicator_status_id": 1,
                                    "published_at": "2020-01-23 09:27:39",
                                    "source_id": 20,
                                    "id": 13600530,
                                    "created_at": "2022-03-18 10:28:16",
                                    "source_type": "connectors",
                                    "creator_source_id": 20,
                                    "indicator_type_id": 18,
                                    "reference_id": 11,
                                    "updated_at": "2022-03-18 10:28:16",
                                    "name": "AlienVault OTX Pulse"
                                }
                            ],
                            "enrich_info": {
                                "attributes": [
                                    {
                                        "id": 5252887,
                                        "indicator_id": 2543358,
                                        "attribute_id": 187,
                                        "value": "True",
                                        "created_at": "2022-03-18 10:28:16",
                                        "updated_at": "2022-03-18 10:28:16",
                                        "touched_at": "2022-03-18 10:28:16.013",
                                        "name": "Is Active",
                                        "sources": [
                                            {
                                                "id": 20,
                                                "type": "connectors",
                                                "reference_id": 11,
                                                "name": "AlienVault OTX Pulse",
                                                "tlp_id": None,
                                                "created_at": "2022-03-18 10:28:16",
                                                "updated_at": "2022-03-18 10:28:16",
                                                "published_at": "2020-01-23 09:27:39.000",
                                                "pivot": {
                                                    "indicator_attribute_id": 5252887,
                                                    "source_id": 20,
                                                    "id": 5269020,
                                                    "creator_source_id": 20
                                                }
                                            }
                                        ],
                                        "attribute": {
                                            "id": 187,
                                            "name": "Is Active",
                                            "created_at": "2022-01-19 20:22:43",
                                            "updated_at": "2022-01-19 20:22:43"
                                        }
                                    }
                                ],
                                "Comments": "Additional attribute information is available on the ThreatQ platform."
                            },
                            "relationships": {
                                "malware": [],
                                "attack_pattern": [],
                                "campaign": [],
                                "ttp": [],
                                "tool": []
                            }
                        }
                    ],
                    "data": hash_value,
                    "dataType": "hash",
                    "namespace": "8bf42ea1-e30d-41a2-a3ee-1aec759cf409",
                    "external_reference": {
                        "source_name": "ThreatQ_Connector",
                        "url": "https://threatq.com"
                    },
                }
            ]
        }
        sdo_type = 'indicator'
        result_bundle = self.result_translator.translate_results(data_source=DATA_SOURCE, data=transmitData['data'])
        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']
        stix_indicator = TestThreatQResultsToStix.get_first_of_type(result_bundle_objects, sdo_type)
        assert 'type' in stix_indicator and stix_indicator['type'] == sdo_type
        assert 'pattern' in stix_indicator and stix_indicator['pattern'] == hash_query_pattern

    def test_indicator_url_query_pattern(self):
        """
        to test the indicator stix object extensions properties with hash query pattern
        """
        transmitData = {
            "data": [
                {
                    "total": 1,
                    "data": url_value,
                    "offset": 0,
                    "limit": 500,
                    "code": 200,
                    "report": [
                        {
                            "class": "network",
                            "score": 0,
                            "value": url_value,
                            "expires_calculated_at": "2022-01-17 15:20:06",
                            "touched_at": "2022-01-18 15:17:48",
                            "id": 14213,
                            "updated_at": "2022-01-15 15:15:47",
                            "published_at": "2022-01-15 15:15:47",
                            "created_at": "2022-01-15 15:15:47",
                            "status_id": 1,
                            "hash": "d5bde55bcc50e107e68369e73124ffde",
                            "type_id": 30,
                            "adversaries": [],
                            "type": {
                                "name": "URL",
                                "id": 30,
                                "class": "network"
                            },
                            "status": {
                                "name": "Active",
                                "id": 1,
                                "description": "Poses a threat and is being exported to detection tools."
                            },
                            "attributes": [
                                {
                                    "value": "US",
                                    "created_at": "2022-01-15 15:15:50",
                                    "indicator_id": 14213,
                                    "updated_at": "2022-01-18 15:17:39",
                                    "attribute_id": 10,
                                    "id": 174338,
                                    "touched_at": "2022-01-18 15:17:39",
                                    "name": "Country"
                                }
                            ],
                            "sources": [
                                {
                                    "indicator_id": 14213,
                                    "indicator_status_id": 1,
                                    "published_at": "2022-01-15 15:15:50",
                                    "source_id": 16,
                                    "id": 101803,
                                    "created_at": "2022-01-15 15:15:50",
                                    "source_type": "connectors",
                                    "creator_source_id": 16,
                                    "indicator_type_id": 30,
                                    "reference_id": 5,
                                    "updated_at": "2022-01-18 15:17:48",
                                    "name": "PhishTank"
                                }
                            ],
                            "enrich_info": {
                                "attributes": [
                                    {
                                        "id": 174338,
                                        "indicator_id": 14213,
                                        "attribute_id": 10,
                                        "value": "US",
                                        "created_at": "2022-01-15 15:15:50",
                                        "updated_at": "2022-01-18 15:17:39",
                                        "touched_at": "2022-01-18 15:17:39.815",
                                        "name": "Country",
                                        "sources": [
                                            {
                                                "id": 16,
                                                "type": "connectors",
                                                "reference_id": 5,
                                                "name": "PhishTank",
                                                "tlp_id": "None",
                                                "created_at": "2022-01-15 15:15:50",
                                                "updated_at": "2022-01-18 15:17:39",
                                                "published_at": "None",
                                                "pivot": {
                                                    "indicator_attribute_id": 174338,
                                                    "source_id": 16,
                                                    "id": 174338,
                                                    "creator_source_id": 16
                                                }
                                            }
                                        ],
                                        "attribute": {
                                            "id": 10,
                                            "name": "Country",
                                            "created_at": "2022-01-13 15:13:55",
                                            "updated_at": "2022-01-13 15:13:55"
                                        }
                                    }
                                ],
                                "Comments": "Additional attribute information is available on the ThreatQ platform."
                            },
                            "relationships": {
                                "malware": [],
                                "attack_pattern": [],
                                "campaign": [],
                                "ttp": [],
                                "tool": []
                            }
                        }
                    ],
                    "dataType": "url",
                    "namespace": "8bf42ea1-e30d-41a2-a3ee-1aec759cf409",
                    "external_reference": {
                        "source_name": "ThreatQ_Connector",
                        "url": "https://threatq.com"
                    }
                }
            ]
        }
        sdo_type = 'indicator'
        result_bundle = self.result_translator.translate_results(data_source=DATA_SOURCE, data=transmitData['data'])
        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']
        stix_indicator = TestThreatQResultsToStix.get_first_of_type(result_bundle_objects, sdo_type)
        assert 'type' in stix_indicator and stix_indicator['type'] == sdo_type
        assert 'pattern' in stix_indicator and stix_indicator['pattern'] == url_query_pattern
    
    def test_indicator_domain_query_pattern(self):
        """
        to test the indicator stix object extensions properties with hash query pattern
        """
        transmitData = {
                "data": [
                    {
                        "total": 0,
                        "data": domain_name,
                        "offset": 0,
                        "limit": 500,
                        "code": 200,
                        "report": [
                            {
                                "class": "network",
                                "score": 0,
                                "value": "www.cnn.com",
                                "expires_calculated_at": "2022-03-16 14:58:43",
                                "touched_at": "2022-03-16 14:58:43",
                                "id": 1827576,
                                "updated_at": "2022-03-12 06:31:54",
                                "published_at": "2021-05-30 13:17:37",
                                "created_at": "2022-03-12 06:31:54",
                                "status_id": 1,
                                "hash": "2a234ef920b48f0463fd170b28b3730d",
                                "type_id": 11,
                                "adversaries": [],
                                "type": {
                                    "name": "FQDN",
                                    "id": 11,
                                    "class": "network"
                                },
                                "status": {
                                    "name": "Active",
                                    "id": 1,
                                    "description": "Poses a threat and is being exported to detection tools."
                                },
                                "attributes": [
                                    {
                                        "value": "True",
                                        "created_at": "2022-03-12 06:31:55",
                                        "indicator_id": 1827576,
                                        "updated_at": "2022-03-12 11:51:04",
                                        "attribute_id": 187,
                                        "id": 3907550,
                                        "touched_at": "2022-03-12 11:51:04",
                                        "name": "Is Active"
                                    },
                                    {
                                        "value": "http",
                                        "created_at": "2022-03-12 06:31:55",
                                        "indicator_id": 1827576,
                                        "updated_at": "2022-03-12 06:31:55",
                                        "attribute_id": 75,
                                        "id": 3907551,
                                        "touched_at": "2022-03-12 06:31:55",
                                        "name": "Scheme"
                                    }
                                ],
                                "sources": [
                                    {
                                        "indicator_id": 1827576,
                                        "indicator_status_id": 1,
                                        "published_at": "2021-05-30 13:17:37",
                                        "source_id": 20,
                                        "id": 12241213,
                                        "created_at": "2022-03-12 06:31:55",
                                        "source_type": "connectors",
                                        "creator_source_id": 20,
                                        "indicator_type_id": 11,
                                        "reference_id": 11,
                                        "updated_at": "2022-03-12 11:51:04",
                                        "name": "AlienVault OTX Pulse"
                                    }
                                ],
                                "enrich_info": {
                                    "attributes": [
                                        {
                                            "id": 3907550,
                                            "indicator_id": 1827576,
                                            "attribute_id": 187,
                                            "value": "True",
                                            "created_at": "2022-03-12 06:31:55",
                                            "updated_at": "2022-03-12 11:51:04",
                                            "touched_at": "2022-03-12 11:51:04.919",
                                            "name": "Is Active",
                                            "sources": [
                                                {
                                                    "id": 20,
                                                    "type": "connectors",
                                                    "reference_id": 11,
                                                    "name": "AlienVault OTX Pulse",
                                                    "tlp_id": None,
                                                    "created_at": "2022-03-12 06:31:55",
                                                    "updated_at": "2022-03-12 11:51:04",
                                                    "published_at": "2021-05-30 13:17:37.000",
                                                    "pivot": {
                                                        "indicator_attribute_id": 3907550,
                                                        "source_id": 20,
                                                        "id": 3922003,
                                                        "creator_source_id": 20
                                                    }
                                                }
                                            ],
                                            "attribute": {
                                                "id": 187,
                                                "name": "Is Active",
                                                "created_at": "2022-01-19 20:22:43",
                                                "updated_at": "2022-01-19 20:22:43"
                                            }
                                        },
                                        {
                                            "id": 3907551,
                                            "indicator_id": 1827576,
                                            "attribute_id": 75,
                                            "value": "http",
                                            "created_at": "2022-03-12 06:31:55",
                                            "updated_at": "2022-03-12 06:31:55",
                                            "touched_at": "2022-03-12 06:31:55.288",
                                            "name": "Scheme",
                                            "sources": [
                                                {
                                                    "id": 20,
                                                    "type": "connectors",
                                                    "reference_id": 11,
                                                    "name": "AlienVault OTX Pulse",
                                                    "tlp_id": None,
                                                    "created_at": "2022-03-12 06:31:55",
                                                    "updated_at": "2022-03-12 06:31:55",
                                                    "published_at": None,
                                                    "pivot": {
                                                        "indicator_attribute_id": 3907551,
                                                        "source_id": 20,
                                                        "id": 3922004,
                                                        "creator_source_id": 20
                                                    }
                                                }
                                            ],
                                            "attribute": {
                                                "id": 75,
                                                "name": "Scheme",
                                                "created_at": "2022-01-13 15:15:11",
                                                "updated_at": "2022-01-13 15:15:11"
                                            }
                                        }
                                    ],
                                    "Comments": "Additional attribute information is available on the ThreatQ platform."
                                },
                                "relationships": {
                                    "malware": [],
                                    "attack_pattern": [],
                                    "campaign": [],
                                    "ttp": [],
                                    "tool": []
                                }
                            }
                        ],
                        "dataType": "domain",
                        "external_reference": {
                            "source_name": "ThreatQ_Connector",
                            "url": "N/A"
                        },
                        "namespace": "8bf42ea1-e30d-41a2-a3ee-1aec759cf409"
                    }
                ]
            }

        sdo_type = 'indicator'
        result_bundle = self.result_translator.translate_results(data_source=DATA_SOURCE, data=transmitData['data'])
        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']
        stix_indicator = TestThreatQResultsToStix.get_first_of_type(result_bundle_objects, sdo_type)
        assert 'type' in stix_indicator and stix_indicator['type'] == sdo_type
        assert 'pattern' in stix_indicator and stix_indicator['pattern'] == domain_query_pattern
