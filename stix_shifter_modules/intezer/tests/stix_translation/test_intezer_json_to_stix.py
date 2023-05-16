import json
import unittest
from functools import wraps
from stix_shifter_modules.intezer.entry_point import EntryPoint

MODULE = "intezer"
DATA_SOURCE = {"type": "identity", "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
               "name": "Intezer_Connector", "identity_class": "system"}
options = {'stix_validator':True}
entry_point = EntryPoint(options=options)
extension_types = ['toplevel-property-extension']
extension_properties = ['x_ibm_original_threat_feed_data','threat_score', 'threat_attributes']
hash_value = 'f5ae03de0ad60f5b17b82f2cd68402fe'
hash_query_pattern = "[file:hashes.MD5='"+hash_value+"']"
url_value = "https://abc.com/"
url_query_pattern = "[url:value='"+url_value+"']"
domain_name = "linkprotect.cudasvc.com"
domain_query_pattern = "[domain-name:value='"+domain_name+"']"
transmitQueryData = {
    "success": "true",
    "data": [
        {
            "total": 1,
            "data": hash_value,
            "offset": 0,
            "limit": 500,
            "code": 200,
            "report": [
                {
                    "analysis_id": "439bf56e-97fd-4a78-bcc2-37ee29f23d2f",
                    "analysis_time": "Mon, 24 Jan 2022 11:42:22 GMT",
                    "analysis_url": "https://analyze.intezer.com/analyses/439bf56e-97fd-4a78-bcc2-37ee29f23d2f","family_id": "48217a46-eb92-4d58-8367-7eacf4d512c3",
        "family_name": "XMRig Miner",
                    "is_private": "true",
                    "sha256": "18ffd3868dfa7f2dde1295407df64944b035b171ed39e00569dbfb3cd7a5d7e7",
                    "sub_verdict": "malicious",
                    "verdict": "malicious",
                    "dynamic_ttps": [
                          {
                              "data": [
                                  {
                                      "IP": "84.53.158.230:80 (Europe)"
                                  },
                                  {
                                      "IP": "107.154.146.161:443 (United States)"
                                  },
                                  {
                                      "IP": "23.51.100.179:80 (Netherlands)"
                                  }
                              ],
                              "description": "Attempts to connect to a dead IP:Port (3 unique times)",
                              "name": "dead_connect",
                              "severity": 1
                          },
                          {
                              "data": [],
                              "description": "Bad response status for URL",
                              "name": "URL is down",
                              "severity": 2
                          },
                          {
                              "data": [
                                  {
                                      "http_request": "excel.exe_InternetCrackUrlA_https://arthurkade.com"
                                  },
                                  {
                                      "http_request": "excel.exe_WSASend_get / http/1.1\r\nconnection: keep-alive\r\naccept: */*\r\nuser-agent: microsoft-cryptoapi/6.1\r\nhost: r3.i.lencr.org\r\n\r\n"
                                  },
                                  {
                                      "http_downloadurl": "excel.exe_URLDownloadToFileW_https://arthurkade.com/21.psd"
                                  },
                                  {
                                      "http_request": "excel.exe_WSASend_get / http/1.1\r\nconnection: keep-alive\r\naccept: */*\r\nuser-agent: microsoft-cryptoapi/6.1\r\nhost: x1.i.lencr.org\r\n\r\n"
                                  }
                              ],
                              "description": "A document file initiated network communications indicative of a potential exploit or payload download",
                              "name": "network_document_http",
                              "severity": 3
                          }
                      ],
                    "iocs": {
                            "files": [
                                {
                                    "analysis_id": "439bf56e-97fd-4a78-bcc2-37ee29f23d2f",
                                    "family": "null",
                                    "path": "18ffd3868dfa7f2dde1295407df64944b035b171ed39e00569dbfb3cd7a5d7e7",
                                    "sha256": "18ffd3868dfa7f2dde1295407df64944b035b171ed39e00569dbfb3cd7a5d7e7",
                                    "type": "main_file",
                                    "verdict": "malicious"
                                }
                            ],
                            "network": [
                                {
                                    "ioc": "23.51.100.179",
                                    "source": [
                                        "Network communication"
                                    ],
                                    "type": "ip"
                                },
                                {
                                    "ioc": "arthurkade.com",
                                    "source": [
                                        "Network communication"
                                    ],
                                    "type": "domain"
                                },
                                {
                                    "ioc": "http://r3.i.lencr.org/",
                                    "source": [
                                        "Network communication"
                                    ],
                                    "type": "url"
                                }
                            ]
                      },
                    "code_reuse": {
                        "common_gene_count": 0,
                        "families": [
                            {
                                "family_id": "4b6a00eb-3052-4b54-b1a3-4df563375ff3",
                                "family_name": "Carbanak",
                                "family_type": "malware",
                                "reused_gene_count": 15
                            }
                        ],
                        "gene_count": 15,
                        "gene_type": "native_windows",
                        "unique_gene_count": 0
                    }
                }
            ],
            "dataType": "hash",
            "external_reference": {
                "source_name": "Intezer_Connector",
                "url": "https://analyze.intezer.com"
            },
            "namespace": "8bf42ea1-e30d-41a2-a3ee-1aec759cf409"
        }
    ]
}

class TestIntezerResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for translate results
    """

    def __init__(self,*args, **kwargs):
        super(TestIntezerResultsToStix, self).__init__(*args, **kwargs)
        self.result_translator = entry_point.create_default_results_translator(dialect='default')
        self.result_bundle = None
    
    @staticmethod
    def exists(obj, chain):
        """
        Check if the nested keys exist in the dictionary or not
        """
        _key = chain.pop(0)
        if _key in obj:
            return TestIntezerResultsToStix.exists(obj[_key], chain) if chain else obj[_key]
    
    @staticmethod
    def get_first(itr, constraint):
        return next(
            (obj for obj in itr if constraint(obj)),
            None
        )

    @staticmethod
    def get_first_of_type(itr, typ):
        return TestIntezerResultsToStix.get_first(itr, lambda o: type(o) == dict and o.get('type') == typ)
    
    def check_stix_bundle_type(func):
        """
        decorator function to convert the data source query result into stix bundle
        """
        @wraps(func)
        def wrapper_func(self, *args, **kwargs):
            if not self.result_bundle:
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
        stix_identity = TestIntezerResultsToStix.get_first_of_type(self.result_bundle_objects, DATA_SOURCE['type'])
        assert 'type' in stix_identity and stix_identity['type'] == DATA_SOURCE['type']
        assert 'name' in stix_identity and stix_identity['name'] == DATA_SOURCE['name']
        assert 'identity_class' in stix_identity and stix_identity['identity_class'] == DATA_SOURCE['identity_class']
    
    @check_stix_bundle_type
    def test_stix_extension_prop(self):
        """
        to test the extension stix object properties
        """
        sdo_type = 'extension-definition'
        stix_extension = TestIntezerResultsToStix.get_first_of_type(self.result_bundle_objects, sdo_type)
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
        stix_indicator = TestIntezerResultsToStix.get_first_of_type(self.result_bundle_objects, sdo_type)
        assert 'type' in stix_indicator and stix_indicator['type'] == sdo_type
        assert 'pattern' in stix_indicator and stix_indicator['pattern'] == hash_query_pattern
        assert 'valid_from' in stix_indicator
        assert 'indicator_types' in stix_indicator and len(stix_indicator['indicator_types']) == 1 \
               and stix_indicator['indicator_types'][0] == 'malicious-activity'
        assert 'description' in stix_indicator
        assert 'threat_score' in stix_indicator
        assert 'external_references' in stix_indicator
        assert 'x_ibm_original_threat_feed_data' in stix_indicator
    
    @check_stix_bundle_type
    def test_stix_malware_prop(self):
        """
        to test the malware stix object properties
        """
        sdo_type = 'malware'
        stix_malware = TestIntezerResultsToStix.get_first_of_type(self.result_bundle_objects, sdo_type)
        assert 'type' in stix_malware and stix_malware['type'] == sdo_type
        assert 'id' in stix_malware
        malware_id = stix_malware['id']
        assert 'malware_types' in stix_malware and len(stix_malware['malware_types']) > 0
        assert 'is_family' in stix_malware

        stix_indicator = TestIntezerResultsToStix.get_first_of_type(self.result_bundle_objects, 'indicator')
        related_sdo_type = 'relationship'
        relationship_object = TestIntezerResultsToStix.get_first_of_type(self.result_bundle_objects, related_sdo_type)
        assert 'type' in relationship_object and relationship_object['type'] == related_sdo_type
        assert 'target_ref' in relationship_object and relationship_object['target_ref'] == malware_id
        assert 'source_ref' in relationship_object and relationship_object['source_ref'] == stix_indicator['id']
        assert 'relationship_type' in relationship_object and relationship_object['relationship_type'] == 'indicates'
    
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
                        "analysis_id": "aef7621c-65cb-4ac6-be12-3ac5d05b3cc0",
                        "api_void_risk_score": 0,
                        "certificate": {
                            "issuer": "Amazon",
                            "protocol": "TLS 1.3",
                            "subject_name": "watchdisneyfe.com",
                            "valid_from": "2021-07-23 00:00:00.000000",
                            "valid_to": "2022-08-21 23:59:59.000000"
                        },
                        "domain_info": {
                            "creation_date": "1996-05-22 00:00:00.000000",
                            "domain_name": "abc.com",
                            "registrar": "CSC CORPORATE DOMAINS, INC."
                        },
                        "indicators": [
                            {
                                "classification": "informative",
                                "text": "Valid https"
                            },
                            {
                                "classification": "informative",
                                "text": "URL is accessible"
                            },
                            {
                                "classification": "informative",
                                "text": "Assigned IPv4 domain"
                            },
                            {
                                "classification": "informative",
                                "text": "Vaild IPv4 domain"
                            }
                        ],
                        "ip": "52.85.61.5",
                        "redirect_chain": [
                            {
                                "response_status": 200,
                                "url": "https://abc.com/"
                            }
                        ],
                        "scanned_url": "https://abc.com/",
                        "submitted_url": "https://abc.com/",
                        "summary": {
                            "description": "No suspicious activity was detected for this URL",
                            "main_connection_gene_count": 0,
                            "main_connection_gene_percentage": 0.0,
                            "title": "No Threats",
                            "verdict_name": "no_threats",
                            "verdict_type": "no_threats"
                        },
                        "verdict": "no_threats",
                        "threat_score": 0,
                        "iocs": {},
                        "dynamic_ttps": {},
                        "code_reuse": {}
                    }
                    ],
                    "dataType": "url",
                    "namespace": "8bf42ea1-e30d-41a2-a3ee-1aec759cf409",
                    "external_reference": {
                        "source_name": "Intezer_Connector",
                        "url": "https://analyze.intezer.com"
                    }
                }
            ]
        }
        sdo_type = 'indicator'
        result_bundle = self.result_translator.translate_results(data_source=DATA_SOURCE, data=transmitData['data'])
        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']
        stix_indicator = TestIntezerResultsToStix.get_first_of_type(result_bundle_objects, sdo_type)
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
                        "code": 200,
                        "report": [
                            {
                                "analysis_id": "e6a15882-c068-439a-9e43-649f9b518946",
                                "api_void_risk_score": 0,
                                "domain_info": {
                                    "creation_date": "2010-05-17 18:53:55.000000",
                                    "domain_name": "cudasvc.com",
                                    "registrar": "CSC CORPORATE DOMAINS, INC."
                                },
                                "indicators": [
                                    {
                                        "classification": "informative",
                                        "text": "URL is accessible"
                                    },
                                    {
                                        "classification": "suspicious",
                                        "text": "Has empty page title"
                                    },
                                    {
                                        "classification": "informative",
                                        "text": "Assigned IPv4 domain"
                                    },
                                    {
                                        "classification": "informative",
                                        "text": "Vaild IPv4 domain"
                                    }
                                ],
                                "ip": "34.231.167.97",
                                "redirect_chain": [
                                    {
                                        "response_status": 200,
                                        "url": "http://linkprotect.cudasvc.com/"
                                    }
                                ],
                                "scanned_url": "http://linkprotect.cudasvc.com/",
                                "submitted_url": "linkprotect.cudasvc.com",
                                "summary": {
                                    "description": "No suspicious activity was detected for this URL",
                                    "main_connection_gene_count": 0,
                                    "main_connection_gene_percentage": 0.0,
                                    "title": "No Threats",
                                    "verdict_name": "no_threats",
                                    "verdict_type": "no_threats"
                                },
                                "verdict": "no_threats",
                                "threat_score": 0,
                                "iocs": {},
                                "dynamic_ttps": {},
                                "code_reuse": {}
                            }
                        ],
                        "dataType": "domain",
                        "external_reference": {
                            "source_name": "Intezer_Connector",
                            "url": "https://analyze.intezer.com"
                        },
                        "namespace": "8bf42ea1-e30d-41a2-a3ee-1aec759cf409"
                    }
                ]
            }

        sdo_type = 'indicator'
        result_bundle = self.result_translator.translate_results(data_source=DATA_SOURCE, data=transmitData['data'])
        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']
        stix_indicator = TestIntezerResultsToStix.get_first_of_type(result_bundle_objects, sdo_type)
        assert 'type' in stix_indicator and stix_indicator['type'] == sdo_type
        assert 'pattern' in stix_indicator and stix_indicator['pattern'] == domain_query_pattern
