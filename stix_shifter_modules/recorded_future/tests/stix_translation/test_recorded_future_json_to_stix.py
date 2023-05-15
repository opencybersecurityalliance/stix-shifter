import json
import unittest
from functools import wraps
from stix_shifter_modules.recorded_future.entry_point import EntryPoint

MODULE = "recorded_future"
DATA_SOURCE = {"type": "identity", "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3", "name": "RecordedFuture_Connector",
               "identity_class": "system"}
options = {'stix_validator':True}
entry_point = EntryPoint(options=options)
translation_options = {}
ip_value = "203.190.254.239"
domain_value = "moncleroutlets.com"
hash_value = "16cda323189d8eba4248c0a2f5ad0d8f"
extension_types = ["toplevel-property-extension"]
extension_properties = ["x_ibm_original_threat_feed_data", "threat_score", "threat_attributes"]
query_pattern = "[ipv4-addr:value='"+ip_value+"']"
transmitQueryData = {
            "data": [
                {
                    "code": 200,
                    "report": {
                        "success": 'true',
                        "isIOCFound": True,
                        "full": {
                            "data": {
                                "intelCard": "https://app.recordedfuture.com/live/sc/entity/ip%3A2.81.219.150",
                                "timestamps": {
                                    "firstSeen": "2019-03-26T16:58:58.989Z"
                                },
                                "risk": {
                                    "criticalityLabel": "Suspicious",
                                    "riskString": "5/54",
                                    "rules": 5,
                                    "criticality": 2,
                                    "riskSummary": "5 of 54 Risk Rules currently observed.",
                                    "score": 32,
                                    "evidenceDetails": [
                                        {
                                            "mitigationString": "",
                                            "evidenceString": "3 sightings on 2 sources: @InternetBadness, @sdpcthreatintel. Most recent tweet: 2.81.219.150 attempted MYSQL exploitation 2 time(s), DShield attacks: 1, Country: PT. Most recent link (Jul 17, 2021): https://twitter.com/sdpcthreatintel/statuses/1416444108772581381",
                                            "rule": "Historical Honeypot Sighting",
                                            "criticality": 1,
                                            "timestamp": "2021-07-17T17:06:06.000Z",
                                            "criticalityLabel": "Unusual"
                                        },
                                    ]
                                },
                                "metrics": [
                                    {
                                        "type": "unusualIPSightings",
                                        "value": 1
                                    },
                                    {
                                        "type": "technicalReportingHits",
                                        "value": 194
                                    }
                                ]
                            }
                        }
                    },
                    "data": ip_value,
                    "dataType": "ip",
                    "namespace": "8bf42ea1-e30d-41a2-a3ee-1aec759cf409",
                    "external_reference": {
                            "source_name": "RecordedFuture_Connector",
                            "url": "N/A"
                        }
                }
            ]
        }

transmitQueryData3 = {
            "data": [
                {
                    "code": 200,
                    "report": {
                        "success": 'true',                        
                        "isIOCFound": True,
                        "full": {
                            "data": {
                                "intelCard": "https://app.recordedfuture.com/live/sc/entity/ip%3A2.81.219.150",
                                "timestamps": {
                                    "firstSeen": "2019-03-26T16:58:58.989Z"
                                },
                                "risk": {
                                    "criticalityLabel": "Suspicious",
                                    "riskString": "5/54",
                                    "rules": 5,
                                    "criticality": 8,
                                    "riskSummary": "5 of 54 Risk Rules currently observed.",
                                    "score": 32,
                                    "evidenceDetails": [
                                        {
                                            "mitigationString": "",
                                            "evidenceString": "3 sightings on 2 sources: @InternetBadness, @sdpcthreatintel. Most recent tweet: 2.81.219.150 attempted MYSQL exploitation 2 time(s), DShield attacks: 1, Country: PT. Most recent link (Jul 17, 2021): https://twitter.com/sdpcthreatintel/statuses/1416444108772581381",
                                            "rule": "Historical Honeypot Sighting",
                                            "criticality": 1,
                                            "timestamp": "2021-07-17T17:06:06.000Z",
                                            "criticalityLabel": "Unusual"
                                        },
                                    ]
                                },
                                "metrics": [
                                    {
                                        "type": "unusualIPSightings",
                                        "value": 1
                                    },
                                    {
                                        "type": "technicalReportingHits",
                                        "value": 194
                                    }
                                ]
                            }
                        }
                    },
                    "data": ip_value,
                    "dataType": "ip",
                    "namespace": "8bf42ea1-e30d-41a2-a3ee-1aec759cf409",
                    "external_reference":  {
                        "source_name": "source_name",
                        "url": "N/A"
                    }                    
                }
            ]
        }      

transmitQueryData4 = {
            "data": [
                {
                    "code": 200,
                    "report": {
                        "success": 'true',
                        "isIOCFound": True,
                        "full": {
                            "data": {
                                "intelCard": "https://app.recordedfuture.com/live/sc/entity/ip%3A2.81.219.150",
                                "timestamps": {
                                    "firstSeen": "2019-03-26T16:58:58.989Z"
                                },
                                "risk": {
                                    "criticalityLabel": "Suspicious",
                                    "riskString": "5/54",
                                    "rules": 5,
                                    "criticality": 1,
                                    "riskSummary": "5 of 54 Risk Rules currently observed.",
                                    "score": 32,
                                    "evidenceDetails": [
                                        {
                                            "mitigationString": "",
                                            "evidenceString": "3 sightings on 2 sources: @InternetBadness, @sdpcthreatintel. Most recent tweet: 2.81.219.150 attempted MYSQL exploitation 2 time(s), DShield attacks: 1, Country: PT. Most recent link (Jul 17, 2021): https://twitter.com/sdpcthreatintel/statuses/1416444108772581381",
                                            "rule": "Historical Honeypot Sighting",
                                            "criticality": 1,
                                            "timestamp": "2021-07-17T17:06:06.000Z",
                                            "criticalityLabel": "Unusual"
                                        },
                                    ]
                                },
                                "metrics": [
                                    {
                                        "type": "unusualIPSightings",
                                        "value": 1
                                    },
                                    {
                                        "type": "technicalReportingHits",
                                        "value": 194
                                    }
                                ]
                            }
                        }
                    },
                    "data": ip_value,
                    "dataType": "ip",
                    "namespace": "8bf42ea1-e30d-41a2-a3ee-1aec759cf409",
                    "external_reference":  {
                        "source_name": "source_name",
                        "url": "N/A"
                    }                    
                }
            ]
        }      


transmitQueryData2 = {
            "data": [
                {
                    "code": 200,
                    "report": {
                        "success": 'true',
                        "isIOCFound": True,
                        "full": {
                            "data": {
                                "intelCard": "https://app.recordedfuture.com/live/sc/entity/ip%3A2.81.219.150",
                                "timestamps": {
                                    "firstSeen": "2019-03-26T16:58:58.989Z"
                                },
                                "risk": {
                                    "criticalityLabel": "Suspicious",
                                    "riskString": "5/54",
                                    "rules": 5,
                                    "criticality": 0,
                                    "riskSummary": "5 of 54 Risk Rules currently observed.",
                                    "score": 32,
                                    "evidenceDetails": [
                                        {
                                            "mitigationString": "",
                                            "evidenceString": "3 sightings on 2 sources: @InternetBadness, @sdpcthreatintel. Most recent tweet: 2.81.219.150 attempted MYSQL exploitation 2 time(s), DShield attacks: 1, Country: PT. Most recent link (Jul 17, 2021): https://twitter.com/sdpcthreatintel/statuses/1416444108772581381",
                                            "rule": "Historical Honeypot Sighting",
                                            "criticality": 1,
                                            "timestamp": "2021-07-17T17:06:06.000Z",
                                            "criticalityLabel": "Unusual"
                                        },
                                    ]
                                },
                                "metrics": [
                                    {
                                        "type": "unusualIPSightings",
                                        "value": 1
                                    },
                                    {
                                        "type": "technicalReportingHits",
                                        "value": 194
                                    }
                                ]
                            }
                        }
                    },
                    "data": ip_value,
                    "dataType": "ip",
                    "namespace": "8bf42ea1-e30d-41a2-a3ee-1aec759cf409",
                    "external_reference":  {
                        "source_name": "source_name",
                        "url": "N/A"
                    }                    
                }
            ]
        }       

transmitQueryDataNoIndicator = {
            "data": [
                {
                    "code": 200,
                    "report": {
                        "success": 'true',
                        "isIOCFound": True,
                        "summary": {
                        },
                        "full": {
                            "data": {
                                "intelCard": "https://app.recordedfuture.com/live/sc/entity/ip%3A2.81.219.150",
                                "timestamps": {
                                    "firstSeen": "2019-03-26T16:58:58.989Z"
                                },
                                "risk": {
                                    "criticalityLabel": "Suspicious",
                                    "riskString": "5/54",
                                    "rules": 5,
                                    "criticality": 2,
                                    "riskSummary": "5 of 54 Risk Rules currently observed.",
                                    "score": 32,
                                    "evidenceDetails": [
                                        {
                                            "mitigationString": "",
                                            "evidenceString": "3 sightings on 2 sources: @InternetBadness, @sdpcthreatintel. Most recent tweet: 2.81.219.150 attempted MYSQL exploitation 2 time(s), DShield attacks: 1, Country: PT. Most recent link (Jul 17, 2021): https://twitter.com/sdpcthreatintel/statuses/1416444108772581381",
                                            "rule": "Historical Honeypot Sighting",
                                            "criticality": 1,
                                            "timestamp": "2021-07-17T17:06:06.000Z",
                                            "criticalityLabel": "Unusual"
                                        },
                                    ]
                                },
                                "metrics": [
                                    {
                                        "type": "unusualIPSightings",
                                        "value": 1
                                    },
                                    {
                                        "type": "technicalReportingHits",
                                        "value": 194
                                    }
                                ]
                            }
                        }
                    },
                    "data": ip_value,
                    "dataType": "ip",
                    "namespace": "8bf42ea1-e30d-41a2-a3ee-1aec759cf409",
                    "external_reference":  {
                        "source_name": "source_name",
                        "url": "N/A"
                    }                    
                }
            ]
        }

transmitQueryData6_Malware = {
    "data": [{'code': 200, 'data': '99017f6eebbac24f351415dd410d522d', 'report': {'success': True, 'isIOCFound': True, 'full': {'data': {'analystNotes': [], 'timestamps': {'lastSeen': '2022-07-19T19:30:10.302Z', 'firstSeen': '2015-10-01T14:48:47.568Z'}, 'risk': {'criticalityLabel': 'Malicious', 'riskString': '2/14', 'rules': 2, 'criticality': 3, 'riskSummary': '2 of 14 Risk Rules currently observed.', 'score': 71, 'evidenceDetails': [{'mitigationString': '', 'evidenceString': '24 sightings on 2 sources: GitHub, PolySwarm. 11 related malware families including Hosts, KIllAV, Zeus, Botnet, KCloud. Most recent link (Mar 6, 2021): https://polyswarm.network/scan/results/file/52d3df0ed60c46f336c131bf2ca454f73bafdc4b04dfa2aea80746f5ba9e6d1c', 'rule': 'Linked to Malware', 'criticality': 2, 'timestamp': '2021-03-06T14:50:01.081Z', 'criticalityLabel': 'Suspicious'}, {'mitigationString': '', 'evidenceString': '2 sightings on 2 sources: ReversingLabs, PolySwarm. Most recent link (May 27, 2011): ReversingLabs malware file analysis.', 'rule': 'Positive Malware Verdict', 'criticality': 3, 'timestamp': '2020-12-11T11:11:59.000Z', 'criticalityLabel': 'Malicious'}]}, 'intelCard': 'https://app.recordedfuture.com/live/sc/entity/hash%3A99017f6eebbac24f351415dd410d522d', 'metrics': [{'type': 'sevenDaysHits', 'value': 0}, {'type': 'oneDayHits', 'value': 0}, {'type': 'totalHits', 'value': 503}, {'type': 'linkedToMalware', 'value': 2}, {'type': 'positiveMalwareVerdictSightings', 'value': 2}, {'type': 'whitelistedCount', 'value': 0}, {'type': 'positiveMalwareVerdict', 'value': 2}, {'type': 'socialMediaHits', 'value': 0}, {'type': 'undergroundForumHits', 'value': 0}, {'type': 'infoSecHits', 'value': 454}, {'type': 'linkedToMalwareSightings', 'value': 24}, {'type': 'maliciousHits', 'value': 26}, {'type': 'darkWebHits', 'value': 0}, {'type': 'publicSubscore', 'value': 71}, {'type': 'pasteHits', 'value': 31}, {'type': 'mitigatedCount', 'value': 0}, {'type': 'criticality', 'value': 3}, {'type': 'technicalReportingHits', 'value': 344}, {'type': 'malwareSubscore', 'value': 70}, {'type': 'sixtyDaysHits', 'value': 0}], 'relatedEntities': [{'entities': [{'count': 16, 'entity': {'id': '0efpT', 'name': 'Trojan', 'type': 'MalwareCategory'}}, {'count': 12, 'entity': {'id': '0edUR', 'name': 'Botnet', 'type': 'MalwareCategory'}}, {'count': 12, 'entity': {'id': 'J31vQ6', 'name': 'Banking Trojan', 'type': 'MalwareCategory'}}, {'count': 10, 'entity': {'id': '0fL5H', 'name': 'Adware', 'type': 'MalwareCategory'}}, {'count': 1, 'entity': {'id': 'OkPqZz', 'name': 'Keylogger', 'type': 'MalwareCategory'}}], 'type': 'RelatedMalwareCategory'}, {'entities': [{'count': 6, 'entity': {'id': 'hash:88817f6eebbac24f351415dd410d522d', 'name': '88817f6eebbac24f351415dd410d522d', 'type': 'Hash'}}, {'count': 6, 'entity': {'id': 'hash:8fcc2f670a166ea78ca239375ed312055c74efdc1f47e79d69966461dd1b2fb6', 'name': '8fcc2f670a166ea78ca239375ed312055c74efdc1f47e79d69966461dd1b2fb6', 'type': 'Hash'}}, {'count': 3, 'entity': {'id': 'hash:24799ca590d42134e7103b06d46fd960', 'name': '24799ca590d42134e7103b06d46fd960', 'type': 'Hash'}}, {'count': 3, 'entity': {'id': 'hash:cbcc219a31da557d424ae60bfe849fefb968c284f90125312d50fbe8913d8649', 'name': 'cbcc219a31da557d424ae60bfe849fefb968c284f90125312d50fbe8913d8649', 'type': 'Hash'}}, {'count': 2, 'entity': {'id': 'hash:097934e2736d951fc52a6b1e15ad42f2', 'name': '097934e2736d951fc52a6b1e15ad42f2', 'type': 'Hash'}}, {'count': 2, 'entity': {'id': 'hash:29fbe09f4b496ef87b8b5373494fc1f4584236be520faa6fc4ebcfda04cdbe5e', 'name': '29fbe09f4b496ef87b8b5373494fc1f4584236be520faa6fc4ebcfda04cdbe5e', 'type': 'Hash'}}, {'count': 2, 'entity': {'id': 'hash:2d3915cdc82e909357d44c4de1b8890bd753605c28df11b10299e3fd09d930b9', 'name': '2d3915cdc82e909357d44c4de1b8890bd753605c28df11b10299e3fd09d930b9', 'type': 'Hash'}}, {'count': 2, 'entity': {'id': 'hash:46dc088910439dad6a0d69da5e64227d04a640845fd1c31e90a7d4340c539fe0', 'name': '46dc088910439dad6a0d69da5e64227d04a640845fd1c31e90a7d4340c539fe0', 'type': 'Hash'}}, {'count': 2, 'entity': {'id': 'hash:66c305d6ea9a3d978b9cf0354edb398e', 'name': '66c305d6ea9a3d978b9cf0354edb398e', 'type': 'Hash'}}, {'count': 2, 'entity': {'id': 'hash:681b80f1ee0eb1531df11c6ae115d711', 'name': '681b80f1ee0eb1531df11c6ae115d711', 'type': 'Hash'}}, {'count': 2, 'entity': {'id': 'hash:a32e750bc1b0315530097434a7e1d324b843e1f5ffd95238b49d3a8aa8e6fe09', 'name': 'a32e750bc1b0315530097434a7e1d324b843e1f5ffd95238b49d3a8aa8e6fe09', 'type': 'Hash'}}, {'count': 2, 'entity': {'id': 'hash:cbdcb84268fcf2a25b844c1dca787de835c0376e82c1a2e62814a3c940a26cfb', 'name': 'cbdcb84268fcf2a25b844c1dca787de835c0376e82c1a2e62814a3c940a26cfb', 'type': 'Hash'}}, {'count': 2, 'entity': {'id': 'hash:d41d8cd98f00b204e9800998ecf8427e', 'name': 'd41d8cd98f00b204e9800998ecf8427e', 'type': 'Hash'}}, {'count': 1, 'entity': {'id': 'hash:1fe0ef5feca2f84eb450bc3617f839e317b2a686af4d651a9bada77a522201b0', 'name': '1fe0ef5feca2f84eb450bc3617f839e317b2a686af4d651a9bada77a522201b0', 'type': 'Hash'}}], 'type': 'RelatedHash'}, {'entities': [{'count': 2, 'entity': {'id': 'idn:generic.ml', 'name': 'generic.ml', 'type': 'InternetDomainName'}}, {'count': 2, 'entity': {'id': 'idn:secuscanpro.io', 'name': 'secuscanpro.io', 'type': 'InternetDomainName'}}], 'type': 'RelatedInternetDomainName'}, {'entities': [{'count': 8, 'entity': {'id': 'ip:4.6.4.2', 'name': '4.6.4.2', 'type': 'IpAddress'}}], 'type': 'RelatedIpAddress'}, {'entities': [{'count': 8, 'entity': {'id': 'PRhHS6', 'name': '.exe', 'type': 'FileNameExtension'}}, {'count': 3, 'entity': {'id': 'PRhgI_', 'name': '.bin', 'type': 'FileNameExtension'}}], 'type': 'RelatedFileNameExtension'}, {'entities': [{'count': 12, 'entity': {'id': 'J21f9C', 'name': 'Zeus', 'type': 'Malware'}}, {'count': 10, 'entity': {'id': 'K0T3Zv', 'name': 'Hosts', 'type': 'Malware'}}, {'count': 2, 'entity': {'id': 'Kj0AQb', 'name': 'Qhost', 'type': 'Malware'}}, {'count': 2, 'entity': {'id': 'K0VjWZ', 'name': 'Comame', 'type': 'Malware'}}, {'count': 2, 'entity': {'id': 'SbUUmV', 'name': 'KIllAV', 'type': 'Malware'}}, {'count': 1, 'entity': {'id': 'PD_NyS', 'name': 'KCloud', 'type': 'Malware'}}], 'type': 'RelatedMalware'}, {'entities': [{'count': 1, 'entity': {'id': 'hash:23d6716415cd22443d7b1efcafe9e370154ff13eafb2a6e9f6387c0e79c59ec4179db0ffb5d41342c61f9829b4f3ea0c6e81fb3f244e8354c2259c132bc1cd84', 'name': '23d6716415cd22443d7b1efcafe9e370154ff13eafb2a6e9f6387c0e79c59ec4179db0ffb5d41342c61f9829b4f3ea0c6e81fb3f244e8354c2259c132bc1cd84', 'type': 'Hash'}}, {'count': 1, 'entity': {'id': 'hash:325a18de6d0ce00129938a66abecb2af1c17024f', 'name': '325a18de6d0ce00129938a66abecb2af1c17024f', 'type': 'Hash'}}, {'count': 1, 'entity': {'id': 'hash:4d1740485713a2ab3a4f5822a01f645fe8387f92', 'name': '4d1740485713a2ab3a4f5822a01f645fe8387f92', 'type': 'Hash'}}, {'count': 1, 'entity': {'id': 'hash:52d3df0ed60c46f336c131bf2ca454f73bafdc4b04dfa2aea80746f5ba9e6d1c', 'name': '52d3df0ed60c46f336c131bf2ca454f73bafdc4b04dfa2aea80746f5ba9e6d1c', 'type': 'Hash'}}, {'count': 1, 'entity': {'id': 'hash:99017f6eebbac24f351415dd410d522d', 'name': '99017f6eebbac24f351415dd410d522d', 'type': 'Hash'}}], 'type': 'FileHashes'}, {'entities': [{'count': 64, 'entity': {'id': 'CE41CS', 'name': 'VirusTotal', 'type': 'Product'}}, {'count': 3, 'entity': {'id': 'I279St', 'name': 'F-Prot', 'type': 'Product'}}, {'count': 2, 'entity': {'id': 'Jugxon', 'name': 'AhnLab-V3', 'type': 'Product'}}, {'count': 1, 'entity': {'id': 'B_G85', 'name': 'Linux', 'type': 'Product'}}, {'count': 1, 'entity': {'id': 'CAUBV', 'name': 'Microsoft Visual Basic', 'type': 'Product'}}, {'count': 1, 'entity': {'id': 'mgDWj', 'name': 'ClamAV', 'type': 'Product'}}, {'count': 1, 'entity': {'id': 'CURfRc', 'name': 'Comodo', 'type': 'Product'}}], 'type': 'RelatedProduct'}]}, 'metadata': {'entries': [{'key': 'metrics', 'label': 'Metrics', 'type': 'list', 'item': {'type': 'dict', 'entries': [{'key': 'type', 'label': 'Metric type', 'type': 'text'}, {'key': 'value', 'label': 'Value', 'type': 'float'}]}}, {'key': 'timestamps', 'label': 'Event timestamps', 'type': 'dict', 'entries': [{'key': 'firstSeen', 'label': 'First seen', 'type': 'datetime'}, {'key': 'lastSeen', 'label': 'Last seen', 'type': 'datetime'}]}, {'key': 'risk', 'label': 'Event risk information', 'type': 'dict', 'entries': [{'key': 'score', 'label': 'Risk score', 'type': 'integer'}, {'key': 'rules', 'label': 'Risk rules triggered', 'type': 'integer'}, {'key': 'criticality', 'label': 'Criticality', 'type': 'integer'}, {'key': 'criticalityLabel', 'label': 'Criticality label', 'type': 'text'}, {'key': 'riskSummary', 'label': 'Risk summary', 'type': 'text'}, {'key': 'riskString', 'label': 'Risk string', 'type': 'text'}, {'key': 'evidenceDetails', 'label': 'Evidence details', 'type': 'list', 'item': {'type': 'dict', 'entries': [{'key': 'evidenceString', 'label': 'Evidence string', 'type': 'text'}, {'key': 'criticality', 'label': 'Criticality', 'type': 'integer'}, {'key': 'criticalityLabel', 'label': 'Criticality label', 'type': 'text'}, {'key': 'rule', 'label': 'Rule', 'type': 'text'}, {'key': 'timestamp', 'label': 'Timestamp', 'type': 'datetime'}, {'key': 'mitigationString', 'label': 'Mitigation string', 'type': 'text'}]}}]}, {'key': 'intelCard', 'label': 'Intel Card URL', 'type': 'link'}, {'key': 'relatedEntities', 'label': 'Related entities', 'type': 'list', 'item': {'type': 'dict', 'entries': [{'key': 'type', 'label': 'Relationship type', 'type': 'text'}, {'key': 'entities', 'label': 'Entities', 'type': 'list', 'item': {'type': 'dict', 'entries': [{'key': 'entity', 'label': 'Entity', 'type': 'Entity'}, {'key': 'count', 'label': 'Count', 'type': 'integer'}]}}]}}, {'key': 'analystNotes', 'label': 'Analyst Notes', 'item': {'entries': [{'key': 'id', 'label': 'Document ID', 'type': 'text'}, {'key': 'external_id', 'label': 'External ID', 'type': 'text'}, {'key': 'source', 'label': 'Source', 'type': 'entity'}, {'key': 'matching_entities', 'item': {'item': {'entries': [{'key': 'entity', 'label': 'entity', 'type': 'entity'}], 'type': 'dict'}, 'type': 'list'}, 'type': 'list'}, {'key': 'attributes', 'entries': [{'key': 'published', 'label': 'Published', 'type': 'datetime'}, {'key': 'external_id', 'label': 'External ID', 'type': 'text'}, {'key': 'title', 'label': 'Title', 'type': 'text'}, {'key': 'text', 'label': 'Text', 'type': 'text'}, {'key': 'authors', 'label': 'Authors', 'item': {'type': 'Entity'}, 'type': 'list'}, {'key': 'entities', 'label': 'Entities', 'item': {'type': 'Entity'}, 'type': 'list'}, {'key': 'note_entities', 'label': 'Note Entities', 'item': {'type': 'Entity'}, 'type': 'list'}, {'key': 'context_entities', 'label': 'Related Entities', 'item': {'type': 'Entity'}, 'type': 'list'}, {'key': 'tlp', 'label': 'TLP', 'type': 'text'}, {'key': 'validated_on', 'label': 'Validated On', 'type': 'datetime'}, {'key': 'validation_urls', 'label': 'Validation URLs', 'item': {'type': 'URL'}, 'type': 'list'}, {'key': 'labels', 'label': 'Labels', 'item': {'type': 'UserLabel'}, 'type': 'list'}, {'key': 'attachment', 'label': 'Attachment', 'type': 'text'}, {'key': 'header_image', 'label': 'Header Image', 'type': 'Entity'}, {'key': 'recommended_queries', 'label': 'Recommended Queries', 'item': {'type': 'URL'}, 'type': 'list'}, {'key': 'topic', 'label': 'Topic', 'required': True, 'type': 'Topic'}], 'type': 'dict'}], 'type': 'dict'}, 'type': 'list'}]}}}, 'dataType': 'hash', 'external_reference': {'source_name': 'RecordedFuture_Connector', 'url': 'https://app.recordedfuture.com/live/sc/entity/hash%3A99017f6eebbac24f351415dd410d522d'}, 'namespace': '9d4bedaf-d351-4f50-930f-f8eb121e5bae'}]
}

class TestRecordedFutureResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for translate results
    """

    def __init__(self,*args, **kwargs):
        super(TestRecordedFutureResultsToStix, self).__init__(*args, **kwargs)
        self.result_translator = entry_point.create_default_results_translator(dialect='default')
        self.result_bundle = self.result_translator.translate_results(data_source=DATA_SOURCE, data=transmitQueryData['data'])
        self.result_bundle_objects = self.result_bundle['objects']
        self.result_bundle2 = self.result_translator.translate_results(data_source=DATA_SOURCE, data=transmitQueryData2['data'])
        self.result_bundle_objects2 = self.result_bundle2['objects']
        self.result_bundle3 = self.result_translator.translate_results(data_source=DATA_SOURCE, data=transmitQueryData3['data'])
        self.result_bundle_objects3 = self.result_bundle3['objects']
        self.result_bundle4 = self.result_translator.translate_results(data_source=DATA_SOURCE, data=transmitQueryData4['data'])
        self.result_bundle_objects4 = self.result_bundle4['objects']
        self.result_bundle_no_indicator = self.result_translator.translate_results(data_source=DATA_SOURCE, data=transmitQueryDataNoIndicator['data'])
        self.result_bundle_objects_no_indicator = self.result_bundle_no_indicator['objects']

        self.result_bundle6_malware = self.result_translator.translate_results(data_source=DATA_SOURCE, data=transmitQueryData6_Malware['data'])
        self.result_bundle_objects6_malware = self.result_bundle6_malware['objects']
        self.extension_property_names = []
    
    @staticmethod
    def exists(obj, chain):
        """
        Check if the nested keys exist in the dictionary or not
        """
        _key = chain.pop(0)
        if _key in obj:
            return TestRecordedFutureResultsToStix.exists(obj[_key], chain) if chain else obj[_key]
    
    @staticmethod
    def get_first(itr, constraint):
        return next(
            (obj for obj in itr if constraint(obj)),
            None
        )

    @staticmethod
    def get_first_of_type(itr, typ):
        return TestRecordedFutureResultsToStix.get_first(itr, lambda o: type(o) == dict and o.get('type') == typ)
    
    def check_stix_bundle_type(func):
        """
        decorator function to convert the data source query result into stix bundle
        """
        @wraps(func)
        def wrapper_func(self, *args, **kwargs):
            assert self.result_bundle['type'] == 'bundle'
            return func(self, *args, **kwargs)
        return wrapper_func

    @check_stix_bundle_type
    def test_stix_identity_prop(self):
        """
        to test the identity stix object properties
        """
        stix_identity = TestRecordedFutureResultsToStix.get_first_of_type(self.result_bundle_objects, DATA_SOURCE['type'])
        assert 'type' in stix_identity and stix_identity['type'] == DATA_SOURCE['type']
        assert 'name' in stix_identity and stix_identity['name'] == DATA_SOURCE['name']
        assert 'identity_class' in stix_identity and stix_identity['identity_class'] == DATA_SOURCE['identity_class']
    
    @check_stix_bundle_type
    def test_stix_extension_prop(self):
        """
        to test the extension stix object properties
        """
        sdo_type = 'extension-definition'
        stix_extension = TestRecordedFutureResultsToStix.get_first_of_type(self.result_bundle_objects, sdo_type)
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
        stix_indicator = TestRecordedFutureResultsToStix.get_first_of_type(self.result_bundle_objects, sdo_type)
        assert 'type' in stix_indicator and stix_indicator['type'] == sdo_type
        assert 'pattern' in stix_indicator and stix_indicator['pattern'] == query_pattern
        assert 'valid_from' in stix_indicator
        assert 'indicator_types' in stix_indicator and len(stix_indicator['indicator_types']) == 1 \
               and stix_indicator['indicator_types'][0] == 'anomalous-activity'

    @check_stix_bundle_type
    def test_stix_indicator_prop_safe(self):
        """
        to test the indicator stix object properties
        """
        sdo_type = 'indicator'
        stix_indicator = TestRecordedFutureResultsToStix.get_first_of_type(self.result_bundle_objects2, sdo_type)
        assert 'type' in stix_indicator and stix_indicator['type'] == sdo_type
        assert 'pattern' in stix_indicator and stix_indicator['pattern'] == query_pattern
        assert 'valid_from' in stix_indicator
        assert 'indicator_types' in stix_indicator and len(stix_indicator['indicator_types']) == 1 \
               and stix_indicator['indicator_types'][0] == 'benign'

    @check_stix_bundle_type
    def test_stix_indicator_prop_malicious(self):
        """
        to test the indicator stix object properties
        """
        sdo_type = 'indicator'
        stix_indicator = TestRecordedFutureResultsToStix.get_first_of_type(self.result_bundle_objects3, sdo_type)
        assert 'type' in stix_indicator and stix_indicator['type'] == sdo_type
        assert 'pattern' in stix_indicator and stix_indicator['pattern'] == query_pattern
        assert 'valid_from' in stix_indicator
        assert 'indicator_types' in stix_indicator and len(stix_indicator['indicator_types']) == 1 \
               and stix_indicator['indicator_types'][0] == 'malicious-activity'

    @check_stix_bundle_type
    def test_stix_indicator_prop_unknown(self):
        """
        to test the indicator stix object properties
        """
        sdo_type = 'indicator'
        stix_indicator = TestRecordedFutureResultsToStix.get_first_of_type(self.result_bundle_objects4, sdo_type)
        assert 'type' in stix_indicator and stix_indicator['type'] == sdo_type
        assert 'pattern' in stix_indicator and stix_indicator['pattern'] == query_pattern
        assert 'valid_from' in stix_indicator
        assert 'indicator_types' in stix_indicator and len(stix_indicator['indicator_types']) == 1 \
               and stix_indicator['indicator_types'][0] == 'unknown'

    @check_stix_bundle_type
    def test_stix_indicator_prop_no(self):
        """
        to test the indicator stix object properties
        """
        sdo_type = 'indicator'
        stix_indicator = TestRecordedFutureResultsToStix.get_first_of_type(self.result_bundle_objects4, sdo_type)
        assert 'type' in stix_indicator and stix_indicator['type'] == sdo_type
        assert 'pattern' in stix_indicator and stix_indicator['pattern'] == query_pattern
        assert 'valid_from' in stix_indicator
        assert 'indicator_types' in stix_indicator and len(stix_indicator['indicator_types']) == 1 \
               and stix_indicator['indicator_types'][0] == 'unknown'
    
    @check_stix_bundle_type
    def test_stix_indicator_extensions_prop(self):
        """
        to test the indicator stix object extensions properties
        """
        stix_extension = TestRecordedFutureResultsToStix.get_first_of_type(self.result_bundle_objects, 'extension-definition')
        stix_indicator = TestRecordedFutureResultsToStix.get_first_of_type(self.result_bundle_objects, 'indicator')
        assert 'x_ibm_original_threat_feed_data' in stix_indicator
        extension_property = extension_properties[0]
        property_name = "x_ibm_original_threat_feed_data.full"
        is_exist = TestRecordedFutureResultsToStix.exists(stix_indicator, property_name.split("."))
        assert is_exist is not None
        assert stix_indicator[extension_property]["full"][0]

    @check_stix_bundle_type
    def test_stix_indicator_malware_prop(self):
        """
        to test the indicator stix object malware properties
        """
        stix_extension = TestRecordedFutureResultsToStix.get_first_of_type(self.result_bundle_objects6_malware, 'extension-definition')
        stix_indicator = TestRecordedFutureResultsToStix.get_first_of_type(self.result_bundle_objects6_malware, 'indicator')
        assert 'name' in stix_extension
        assert stix_extension['name'] == 'RecordedFuture_Connector extension'
        assert 'indicator_types' in stix_indicator
        assert stix_indicator['indicator_types'][0] == 'malicious-activity'