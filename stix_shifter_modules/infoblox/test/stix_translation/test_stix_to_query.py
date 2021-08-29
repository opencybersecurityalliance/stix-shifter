# -*- coding: utf-8 -*-
import json
import unittest

from stix_shifter.stix_translation.stix_translation import StixTranslation

translation = StixTranslation()

class TestStixParsingMixin:

    @staticmethod
    def get_dialect():
        raise NotImplementedError()

    @staticmethod
    def _parse_query(stix_pattern, dialect):
        query = translation.translate(f'infoblox:{dialect}', 'query', '{}', stix_pattern)
        return query

class TestStixParsing(unittest.TestCase, TestStixParsingMixin):
    TEST_CASES = [
        {
            'pattern': "[(domain-name:value = 'domain1.com') AND x-infoblox-threat:domain_ref.value = 'domain4.com']",
            'expected': {
                'tideDbData': {
                    'queries': [
                        '{"offset": 0, "query": "period=5 minutes&domain=domain4.com", "threat_type": "host", "source": "tideDbData"}',
                        '{"offset": 0, "query": "period=5 minutes&domain=domain1.com", "threat_type": "host", "source": "tideDbData"}'
                    ]
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:domain_ref.value']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:domain_ref.value']]"
                }
            }
        },
        {
            'pattern': "[x-infoblox-threat:host_name = 'example.host.com' AND domain-name:value = 'example.domain.com' AND x-infoblox-threat:profile = 'profile1']",
            'expected': {
                'tideDbData': {
                    'queries': [
                        '{"offset": 0, "query": "period=5 minutes&profile=profile1&domain=example.domain.com&host=example.host.com", "threat_type": "host", "source": "tideDbData"}'
                    ]
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:profile', 'x-infoblox-threat:host_name']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:profile', 'x-infoblox-threat:host_name']]"
                }
            }
        },
        {
            'pattern': "[(domain-name:value = 'domain1.com' AND domain-name:value = 'domain2.com') OR ipv4-addr:value = '1.1.1.1'] START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z'",
            'expected': {
                'tideDbData': {
                    'queries': [
                        '{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&ip=1.1.1.1", "threat_type": "ip", "source": "tideDbData"}',
                        '{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&domain=domain2.com", "threat_type": "host", "source": "tideDbData"}',
                        '{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&domain=domain1.com", "threat_type": "host", "source": "tideDbData"}'
                    ]
                },
                'dnsEventData': {
                    'queries': [
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&qip=1.1.1.1", "threat_type": null, "source": "dnsEventData"}',
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&qname=domain2.com.", "threat_type": null, "source": "dnsEventData"}',
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&qname=domain1.com.", "threat_type": null, "source": "dnsEventData"}'
                    ]
                },
                'dossierData': {
                    'queries': [
                        '{"offset": 0, "query": "value=1.1.1.1", "threat_type": "ip", "source": "dossierData"}',
                        '{"offset": 0, "query": "value=domain2.com", "threat_type": "host", "source": "dossierData"}',
                        '{"offset": 0, "query": "value=domain1.com", "threat_type": "host", "source": "dossierData"}'
                    ]
                }
            }
        },
        {
            'pattern': "[x-infoblox-threat:imported > '2020-08-07' AND ipv4-addr:value = '1.1.1.1']",
            'expected': {
                'tideDbData': {
                    "queries": ['{"offset": 0, "query": "ip=1.1.1.1&imported_from_date=2020-08-07", "threat_type": "ip", "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:imported']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:imported']]"
                }
            }
        },
        {
            'pattern': "[x-infoblox-threat:domain_ref.value = 'domain1.com']",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "period=5 minutes&domain=domain1.com", "threat_type": "host", "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:domain_ref.value']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:domain_ref.value']]"
                }
            }
        },
        {
            'pattern': "[x-infoblox-threat:email_ref.value = 'foo@email1.com']",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "period=5 minutes&email=foo@email1.com", "threat_type": "email", "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:email_ref.value']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:email_ref.value']]"
                }
            }
        },
        {
            'pattern': "[x-infoblox-threat:ip_ref.value = '1.1.1.2']",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "period=5 minutes&ip=1.1.1.2", "threat_type": "ip", "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:ip_ref.value']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:ip_ref.value']]"
                }
            }
        },
        {
            'pattern': "[(ipv4-addr:value = '127.0.0.1' AND ipv4-addr:value = '127.0.0.2') OR domain-name:value = 'domain1.com'] START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z' OR [x-infoblox-threat:host_name = 'root'] AND [email-addr:value= 'test@email.com']",
            'expected': {
                'tideDbData': {
                    'queries': [
                        '{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&domain=domain1.com", "threat_type": "host", "source": "tideDbData"}',
                        '{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&ip=127.0.0.2", "threat_type": "ip", "source": "tideDbData"}',
                        '{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&ip=127.0.0.1", "threat_type": "ip", "source": "tideDbData"}',
                        '{"offset": 0, "query": "period=5 minutes&host=root", "threat_type": "host", "source": "tideDbData"}',
                        '{"offset": 0, "query": "period=5 minutes&email=test@email.com", "threat_type": "email", "source": "tideDbData"}'
                    ]
                },
                'dnsEventData': {
                    'queries': [
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&qname=domain1.com.", "threat_type": null, "source": "dnsEventData"}',
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&qip=127.0.0.2", "threat_type": null, "source": "dnsEventData"}',
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&qip=127.0.0.1", "threat_type": null, "source": "dnsEventData"}'
                    ]
                },
                'dossierData': {
                    'queries': [
                        '{"offset": 0, "query": "value=domain1.com", "threat_type": "host", "source": "dossierData"}',
                        '{"offset": 0, "query": "value=127.0.0.2", "threat_type": "ip", "source": "dossierData"}',
                        '{"offset": 0, "query": "value=127.0.0.1", "threat_type": "ip", "source": "dossierData"}'
                    ]
                }
            }
        },
        {
            'pattern': "[(domain-name:value = 'domain1.com' AND x-infoblox-threat:profile = 'domain2' AND x-infoblox-threat:threat_type = 'host') AND ipv4-addr:value = '1.1.1.1']",
            'expected': {
                'tideDbData': {
                    'success': False,
                    'code': 'invalid_parameter',
                    'error': "Error when converting STIX pattern to data source query: Conflicting threat_type found, ['host', 'ip']"
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:threat_type', 'x-infoblox-threat:profile']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:threat_type', 'x-infoblox-threat:profile']]"
                }
            }
        },
        {
            'pattern': "[(domain-name:value = 'domain1.com' OR domain-name:value = 'domain2.com') AND x-infoblox-threat:profile = 'profile1'] START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z'",
            'expected': {
                'tideDbData': {
                    'queries': [
                        '{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&profile=profile1&domain=domain2.com", "threat_type": "host", "source": "tideDbData"}',
                        '{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&profile=profile1&domain=domain1.com", "threat_type": "host", "source": "tideDbData"}'
                    ]
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:profile']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:profile']]"
                }
            }
        },
        {
            'pattern': "[domain-name:value = 'domain1.com' OR ipv4-addr:value = '1.1.1.1'] START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z'",
            'expected': {
                'tideDbData': {
                    'queries': [
                        '{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&ip=1.1.1.1", "threat_type": "ip", "source": "tideDbData"}',
                        '{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&domain=domain1.com", "threat_type": "host", "source": "tideDbData"}',
                    ]
                },
                'dnsEventData': {
                    'queries': [
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&qip=1.1.1.1", "threat_type": null, "source": "dnsEventData"}',
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&qname=domain1.com.", "threat_type": null, "source": "dnsEventData"}'
                    ]
                },
                'dossierData': {
                    'queries': [
                        '{"offset": 0, "query": "value=1.1.1.1", "threat_type": "ip", "source": "dossierData"}',
                        '{"offset": 0, "query": "value=domain1.com", "threat_type": "host", "source": "dossierData"}'
                    ]
                }
            }
        },
        {
            'pattern': "[domain-name:value = 'domain1.com' AND ipv4-addr:value = '1.1.1.1'] START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z'",
            'expected': {
                'tideDbData': {
                    'success': False,
                    'code': 'invalid_parameter',
                    'error': 'Error when converting STIX pattern to data source query: Conflicting threat_type found, [\'host\', \'ip\']'
                },
                'dnsEventData': {
                    'queries': ['{"offset": 0, "query": "t0=1624845034&t1=1624848934&qip=1.1.1.1&qname=domain1.com.", "threat_type": null, "source": "dnsEventData"}']
                },
                'dossierData': {
                    'queries': [
                        '{"offset": 0, "query": "value=1.1.1.1", "threat_type": "ip", "source": "dossierData"}',
                        '{"offset": 0, "query": "value=domain1.com", "threat_type": "host", "source": "dossierData"}'
                    ]
                }
            }
        },
        {
            'pattern': "[domain-name:value = 'domain1.com' AND domain-name:value = 'domain2.com'] START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z'",
            'expected': {
                'tideDbData': {
                    'queries': [
                        '{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&domain=domain2.com", "threat_type": "host", "source": "tideDbData"}',
                        '{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&domain=domain1.com", "threat_type": "host", "source": "tideDbData"}',
                    ]
                },
                'dnsEventData': {
                    'queries': [
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&qname=domain2.com.", "threat_type": null, "source": "dnsEventData"}',
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&qname=domain1.com.", "threat_type": null, "source": "dnsEventData"}'
                    ]
                },
                'dossierData': {
                    'queries': [
                        '{"offset": 0, "query": "value=domain2.com", "threat_type": "host", "source": "dossierData"}',
                        '{"offset": 0, "query": "value=domain1.com", "threat_type": "host", "source": "dossierData"}'
                    ]
                }
            }
        },
        {
            'pattern': "[domain-name:value = 'domain1.com' OR domain-name:value = 'domain2.com'] START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z'",
            'expected': {
                'tideDbData': {
                    'queries': [
                        '{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&domain=domain2.com", "threat_type": "host", "source": "tideDbData"}',
                        '{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&domain=domain1.com", "threat_type": "host", "source": "tideDbData"}',
                    ]
                },
                'dnsEventData': {
                    'queries': [
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&qname=domain2.com.", "threat_type": null, "source": "dnsEventData"}',
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&qname=domain1.com.", "threat_type": null, "source": "dnsEventData"}'
                    ]
                },
                'dossierData': {
                    'queries': [
                        '{"offset": 0, "query": "value=domain2.com", "threat_type": "host", "source": "dossierData"}',
                        '{"offset": 0, "query": "value=domain1.com", "threat_type": "host", "source": "dossierData"}'
                    ]
                }
            }
        },
        {
            'pattern':  "[domain-name:value = 'domain1.com'] START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z' OR [x-infoblox-threat:profile = 'profile1' AND x-infoblox-threat:threat_type = 'host'] OR [x-infoblox-dns-event:policy_name = 'policy'] START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z'",
            'expected': {
                'tideDbData': {
                    'queries': [
                        '{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&domain=domain1.com", "threat_type": "host", "source": "tideDbData"}',
                        '{"offset": 0, "query": "period=5 minutes&type=host&profile=profile1", "threat_type": "host", "source": "tideDbData"}'
                    ]
                },
                'dnsEventData': {
                    'queries': [
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&qname=domain1.com.", "threat_type": null, "source": "dnsEventData"}',
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&policy_name=policy", "threat_type": null, "source": "dnsEventData"}'
                    ]
                },
                'dossierData': {
                    'queries': [
                        '{"offset": 0, "query": "value=domain1.com", "threat_type": "host", "source": "dossierData"}'
                    ]
                }
            }
        },
        {
            'pattern': "[domain-name:value = 'domain1.com'] START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z' AND [x-infoblox-threat:profile = 'profile1' AND x-infoblox-threat:threat_type = 'host'] AND [x-infoblox-dns-event:policy_name = 'policy'] START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z'",
            'expected': {
                'tideDbData': {
                    'queries': [
                        '{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&domain=domain1.com", "threat_type": "host", "source": "tideDbData"}',
                        '{"offset": 0, "query": "period=5 minutes&type=host&profile=profile1", "threat_type": "host", "source": "tideDbData"}'
                    ]
                },
                'dnsEventData': {
                    'queries': [
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&qname=domain1.com.", "threat_type": null, "source": "dnsEventData"}',
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&policy_name=policy", "threat_type": null, "source": "dnsEventData"}'
                    ]
                },
                'dossierData': {
                    'queries': [
                        '{"offset": 0, "query": "value=domain1.com", "threat_type": "host", "source": "dossierData"}'
                    ]
                }
            }
        },
        {
            'pattern': "[domain-name:value = 'domain1.com'] START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z' OR [x-infoblox-threat:profile = 'profile1' AND x-infoblox-threat:threat_type = 'url']",
            'expected': {
                'tideDbData': {
                    'queries': [
                        '{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&domain=domain1.com", "threat_type": "host", "source": "tideDbData"}',
                        '{"offset": 0, "query": "period=5 minutes&type=url&profile=profile1", "threat_type": "url", "source": "tideDbData"}'
                    ]
                },
                'dnsEventData': {
                    'queries': ['{"offset": 0, "query": "t0=1624845034&t1=1624848934&qname=domain1.com.", "threat_type": null, "source": "dnsEventData"}']
                },
                'dossierData': {
                    'queries': ['{"offset": 0, "query": "value=domain1.com", "threat_type": "host", "source": "dossierData"}']
                }
            }
        },
        {
            'pattern': "[domain-name:value = 'domain1.com'] START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z' AND [x-infoblox-threat:profile = 'profile1' AND x-infoblox-threat:threat_type = 'url']",
            'expected': {
                'tideDbData': {
                    'queries': [
                        '{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&domain=domain1.com", "threat_type": "host", "source": "tideDbData"}',
                        '{"offset": 0, "query": "period=5 minutes&type=url&profile=profile1", "threat_type": "url", "source": "tideDbData"}'
                    ]
                },
                'dnsEventData': {
                    'queries': ['{"offset": 0, "query": "t0=1624845034&t1=1624848934&qname=domain1.com.", "threat_type": null, "source": "dnsEventData"}']
                },
                'dossierData': {
                    'queries': ['{"offset": 0, "query": "value=domain1.com", "threat_type": "host", "source": "dossierData"}']
                }
            }
        },
        {
            'pattern': "[ipv4-addr:value = '1.1.1.1'] START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z' OR [ipv4-addr:value = '2.2.2.2'] START t'2021-08-28T01:50:34Z' STOP t'2021-08-28T02:55:34Z'",
            'expected': {
                'tideDbData': {
                    'queries': [
                        '{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&ip=1.1.1.1", "threat_type": "ip", "source": "tideDbData"}',
                        '{"offset": 0, "query": "from_date=2021-08-28T01:50:34.000Z&to_date=2021-08-28T02:55:34.000Z&ip=2.2.2.2", "threat_type": "ip", "source": "tideDbData"}'
                    ]
                },
                'dnsEventData': {
                    'queries': [
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&qip=1.1.1.1", "threat_type": null, "source": "dnsEventData"}',
                        '{"offset": 0, "query": "t0=1630115434&t1=1630119334&qip=2.2.2.2", "threat_type": null, "source": "dnsEventData"}'
                    ]
                },
                'dossierData': {
                    'queries': [
                        '{"offset": 0, "query": "value=1.1.1.1", "threat_type": "ip", "source": "dossierData"}',
                        '{"offset": 0, "query": "value=2.2.2.2", "threat_type": "ip", "source": "dossierData"}'
                    ]
                }
            }
        },
        {
            'pattern': "[ipv4-addr:value = '1.1.1.1'] START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z' AND [ipv4-addr:value = '2.2.2.2'] START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z'",
            'expected': {
                'tideDbData': {
                    'queries': [
                        '{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&ip=1.1.1.1", "threat_type": "ip", "source": "tideDbData"}',
                        '{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&ip=2.2.2.2", "threat_type": "ip", "source": "tideDbData"}'
                    ]
                },
                'dnsEventData': {
                    'queries': [
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&qip=1.1.1.1", "threat_type": null, "source": "dnsEventData"}',
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&qip=2.2.2.2", "threat_type": null, "source": "dnsEventData"}'
                    ]
                },
                'dossierData': {
                    'queries': [
                        '{"offset": 0, "query": "value=1.1.1.1", "threat_type": "ip", "source": "dossierData"}',
                        '{"offset": 0, "query": "value=2.2.2.2", "threat_type": "ip", "source": "dossierData"}'
                    ]
                }
            }
        },
        {
            'pattern': "[domain-name:value = 'domain2.com'] START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z' OR [domain-name:value = 'domain3.com'] START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z'",
            'expected': {
                'tideDbData': {
                    'queries': [
                        '{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&domain=domain2.com", "threat_type": "host", "source": "tideDbData"}',
                        '{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&domain=domain3.com", "threat_type": "host", "source": "tideDbData"}'
                    ]
                },
                'dnsEventData': {
                    'queries': [
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&qname=domain2.com.", "threat_type": null, "source": "dnsEventData"}',
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&qname=domain3.com.", "threat_type": null, "source": "dnsEventData"}'
                    ]
                },
                'dossierData': {
                    'queries': [
                        '{"offset": 0, "query": "value=domain2.com", "threat_type": "host", "source": "dossierData"}',
                        '{"offset": 0, "query": "value=domain3.com", "threat_type": "host", "source": "dossierData"}'
                    ]
                }
            }
        },
        {
            'pattern': "[domain-name:value = 'domain2.com'] START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z' AND [domain-name:value = 'domain3.com'] START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z'",
            'expected': {
                'tideDbData': {
                    'queries': [
                        '{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&domain=domain2.com", "threat_type": "host", "source": "tideDbData"}',
                        '{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&domain=domain3.com", "threat_type": "host", "source": "tideDbData"}'
                    ]
                },
                'dnsEventData': {
                    'queries': [
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&qname=domain2.com.", "threat_type": null, "source": "dnsEventData"}',
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&qname=domain3.com.", "threat_type": null, "source": "dnsEventData"}'
                    ]
                },
                'dossierData': {
                    'queries': [
                        '{"offset": 0, "query": "value=domain2.com", "threat_type": "host", "source": "dossierData"}',
                        '{"offset": 0, "query": "value=domain3.com", "threat_type": "host", "source": "dossierData"}'
                    ]
                }
            }
        },
        {
            'pattern': "[domain-name:value != 'microsoft']",
            'expected': {
                'tideDbData': {
                    'success': False,
                    'code': 'not_implemented',
                    'error': 'wrong parameter : Comparison operator NotEqual unsupported for Infoblox connector tideDbData'
                },
                'dnsEventData': {
                    'success': False,
                    'code': 'not_implemented',
                    'error': 'wrong parameter : Comparison operator NotEqual unsupported for Infoblox connector dnsEventData'
                },
                'dossierData': {
                    'success': False,
                    'code': 'not_implemented',
                    'error': 'wrong parameter : Comparison operator NotEqual unsupported for Infoblox connector dossierData'
                }
            }
        },
        {
            'pattern':"[x-infoblox-threat:threat_type = 'HOST']",
            'expected': {
                'tideDbData': {
                    'queries': [
                        '{"offset": 0, "query": "period=5 minutes&type=host", "threat_type": "host", "source": "tideDbData"}'
                    ]
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:threat_type']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:threat_type']]"
                }
            }
        },
        {
            'pattern': "[x-infoblox-threat:id = 'uuid1']",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "period=5 minutes&id=uuid1", "threat_type": null, "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:id']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:id']]"
                }
            }
        },
        {
            'pattern': "[x-infoblox-threat:host_name = 'domain1.com']",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "period=5 minutes&host=domain1.com", "threat_type": "host", "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:host_name']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:host_name']]"
                }
            }
        },
        {
            'pattern': "[x-infoblox-threat:host_name LIKE 'domain1.com']",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "period=5 minutes&text_search=domain1.com", "threat_type": "host", "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:host_name']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:host_name']]"
                }
            }
        },
        {
            'pattern': "[ipv4-addr:value = '1.1.1.1'] START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z'",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&ip=1.1.1.1", "threat_type": "ip", "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'queries': ['{"offset": 0, "query": "t0=1624845034&t1=1624848934&qip=1.1.1.1", "threat_type": null, "source": "dnsEventData"}']
                },
                'dossierData': {
                    'queries': ['{"offset": 0, "query": "value=1.1.1.1", "threat_type": "ip", "source": "dossierData"}']
                }
            }
        },
        {
            'pattern': "[ipv4-addr:value LIKE '1.1.1.1']",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "period=5 minutes&text_search=1.1.1.1", "threat_type": "ip", "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'not_implemented',
                    'error': "wrong parameter : Comparison operator Like unsupported for Infoblox connector dnsEventData"
                },
                'dossierData': {
                    'success': False, 'code': 'not_implemented',
                    'error': "wrong parameter : Comparison operator Like unsupported for Infoblox connector dossierData"
                }
            }
        },
        {
            'pattern': "[ipv6-addr:value = '2001:db8:3333:4444:5555:6666:7777:8888']",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "period=5 minutes&ip=2001:db8:3333:4444:5555:6666:7777:8888", "threat_type": "ip", "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['ipv6-addr:value']]"
                },
                'dossierData': {
                    'queries': ['{"offset": 0, "query": "value=2001:db8:3333:4444:5555:6666:7777:8888", "threat_type": "ip", "source": "dossierData"}']
                }
            }
        },
        {
            'pattern': "[x-infoblox-threat:url = 'https://domain1.com']",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "period=5 minutes&url=https://domain1.com", "threat_type": "url", "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:url']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:url']]"
                }
            }
        },
        {
            'pattern': "[x-infoblox-threat:url LIKE 'https://domain1.com']",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "period=5 minutes&text_search=https://domain1.com", "threat_type": "url", "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:url']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:url']]"
                }
            }
        },
        {
            'pattern': "[domain-name:value = 'domain1.com'] START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z'",
            'expected': {
                'tideDbData': {
                    'queries': [
                        '{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&domain=domain1.com", "threat_type": "host", "source": "tideDbData"}'
                    ]
                },
                'dnsEventData': {
                    'queries': ['{"offset": 0, "query": "t0=1624845034&t1=1624848934&qname=domain1.com.", "threat_type": null, "source": "dnsEventData"}']
                },
                'dossierData': {
                    'queries': ['{"offset": 0, "query": "value=domain1.com", "threat_type": "host", "source": "dossierData"}']
                }
            }
        },
        {
            'pattern': "[domain-name:value LIKE 'domain1.com']",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "period=5 minutes&text_search=domain1.com", "threat_type": "host", "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'not_implemented',
                    'error': "wrong parameter : Comparison operator Like unsupported for Infoblox connector dnsEventData"
                },
                'dossierData': {
                    'success': False, 'code': 'not_implemented',
                    'error': "wrong parameter : Comparison operator Like unsupported for Infoblox connector dossierData"
                }
            }
        },
        {
            'pattern': "[email-addr:value = 'foo@email1.com']",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "period=5 minutes&email=foo@email1.com", "threat_type": "email", "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['email-addr:value']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['email-addr:value']]"
                }
            }
        },
        {
            'pattern': "[email-addr:value LIKE 'foo@email1.com']",
            'expected': {
                'tideDbData': {
                    'success': False, 'code': 'not_implemented',
                    'error': 'wrong parameter : Comparison operator Like unsupported for Infoblox connector tideDbData field email'
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['email-addr:value']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['email-addr:value']]"
                }
            }
        },
        {
            'pattern':  "[x-infoblox-threat:top_level_domain = 'tld.com']",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "period=5 minutes&tld=tld.com", "threat_type": null, "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:top_level_domain']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:top_level_domain']]"
                }
            }
        },
        {
            'pattern':  "[x-infoblox-threat:top_level_domain LIKE 'tld.com']",
            'expected': {
                'tideDbData': {
                    'success': False, 'code': 'not_implemented',
                    'error': 'wrong parameter : Comparison operator Like unsupported for Infoblox connector tideDbData field tld'
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:top_level_domain']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:top_level_domain']]"
                }
            }
        },
        {
            'pattern':  "[x-infoblox-threat:profile = 'profile1']",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "period=5 minutes&profile=profile1", "threat_type": null, "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:profile']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:profile']]"
                }
            }
        },
        {
            'pattern':  "[x-infoblox-threat:profile LIKE 'profile1']",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "period=5 minutes&text_search=profile1", "threat_type": null, "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:profile']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:profile']]"
                }
            }
        },
        {
            'pattern': "[x-infoblox-threat:origin = 'origin1']",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "period=5 minutes&origin=origin1", "threat_type": null, "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:origin']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:origin']]"
                }
            }
        },
        {
            'pattern': "[x-infoblox-threat:origin LIKE 'origin1']",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "period=5 minutes&text_search=origin1", "threat_type": null, "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:origin']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:origin']]"
                }
            }
        },
        {
            'pattern': "[x-infoblox-threat:property = 'property1']",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "period=5 minutes&property=property1", "threat_type": null, "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:property']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:property']]"
                }
            }
        },
        {
            'pattern': "[x-infoblox-threat:threat_class = 'class1']",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "period=5 minutes&class=class1", "threat_type": null, "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:threat_class']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:threat_class']]"
                }
            }
        },
        {
            'pattern': "[x-infoblox-threat:threat_class LIKE 'class1']",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "period=5 minutes&text_search=class1", "threat_type": null, "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:threat_class']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:threat_class']]"
                }
            }
        },
        {
            'pattern': "[x-infoblox-threat:threat_level = 'threatclass1']",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "period=5 minutes&threat_level=threatclass1", "threat_type": null, "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:threat_level']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:threat_level']]"
                }
            }
        },
        {
            'pattern': "[x-infoblox-threat:target = 'target1']",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "period=5 minutes&target=target1", "threat_type": null, "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:target']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:target']]"
                }
            }
        },
        {
            'pattern': "[x-infoblox-threat:target LIKE 'target1']",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "period=5 minutes&text_search=target1", "threat_type": null, "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:target']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:target']]"
                }
            }
        },
        {
            'pattern': "[x-infoblox-threat:expiration = '2021-05-24T20:26:04.000Z']",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "expiration=2021-05-24T20:26:04.000Z", "threat_type": null, "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:expiration']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:expiration']]"
                }
            }
        },
        {
            'pattern': "[x-infoblox-threat:imported = '2021-05-24T20:26:04.000Z']",
            'expected': {
                'tideDbData': {
                    'success': False, 'code': 'invalid_parameter',
                    'error': 'Error when converting STIX pattern to data source query: Equal'
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:imported']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:imported']]"
                }
            }
        },
        {
            'pattern': "[x-infoblox-threat:imported > '2021-05-24T20:26:04.000Z']",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "imported_from_date=2021-05-24T20:26:04.000Z", "threat_type": null, "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:imported']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:imported']]"
                }
            }
        },
        {
            'pattern': "[x-infoblox-threat:imported >= '2021-05-24T20:26:04.000Z']",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "imported_from_date=2021-05-24T20:26:04.000Z", "threat_type": null, "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:imported']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:imported']]"
                }
            }
        },
        {
            'pattern': "[x-infoblox-threat:imported < '2021-05-24T20:26:04.000Z']",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "imported_to_date=2021-05-24T20:26:04.000Z", "threat_type": null, "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:imported']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:imported']]"
                }
            }
        },
        {
            'pattern': "[x-infoblox-threat:imported <= '2021-05-24T20:26:04.000Z']",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "imported_to_date=2021-05-24T20:26:04.000Z", "threat_type": null, "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:imported']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:imported']]"
                }
            }
        },
        {
            'pattern': "[x-infoblox-threat:imported > '2021-05-24T20:26:04.000Z' AND x-infoblox-threat:imported < '2021-06-24T20:26:04.000Z']",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "imported_to_date=2021-06-24T20:26:04.000Z&imported_from_date=2021-05-24T20:26:04.000Z", "threat_type": null, "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:imported', 'x-infoblox-threat:imported']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:imported', 'x-infoblox-threat:imported']]"
                }
            }
        },
        {
            'pattern': "[x-infoblox-threat:derivative = 'true']",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "period=5 minutes&derivative=true", "threat_type": null, "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:derivative']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:derivative']]"
                }
            }
        },
        {
            'pattern': "[x-infoblox-threat:dga = 'true']",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "period=5 minutes&dga=true", "threat_type": null, "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:dga']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:dga']]"
                }
            }
        },
        {
            'pattern': "[x-infoblox-threat:active = 'true']",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "period=5 minutes&up=true", "threat_type": null, "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:active']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:active']]"
                }
            }
        },
        {
            'pattern': "[x-infoblox-threat:x_infoblox_confidence = '50']",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "period=5 minutes&confidence=50", "threat_type": null, "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:x_infoblox_confidence']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:x_infoblox_confidence']]"
                }
            }
        },
        {
            'pattern':  "[x-infoblox-threat:hash = 'hash1']",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "period=5 minutes&hash=hash1", "threat_type": null, "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:hash']]"
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-threat:hash']]"
                }
            }
        },
        {
            'pattern': "[(domain-name:value = 'domain1.com' AND x-infoblox-dossier-event-result-pdns:ip_ref.value = '1.1.1.1') AND x-infoblox-dossier-event-result-pdns:hostname_ref.value = 'domain2.com']",
            'expected': {
                'tideDbData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-dossier-event-result-pdns:hostname_ref.value', 'x-infoblox-dossier-event-result-pdns:ip_ref.value']]"
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-dossier-event-result-pdns:hostname_ref.value', 'x-infoblox-dossier-event-result-pdns:ip_ref.value']]"
                },
                'dossierData': {
                    'success': False, 'code': 'invalid_parameter',
                    'error': "Error when converting STIX pattern to data source query: Conflicting threat_type found, ['host', 'ip']"
                }
            }
        },
        {
            'pattern': "[x-infoblox-dossier-event-result-pdns:hostname_ref.value = 'domain1.com']",
            'expected': {
                'tideDbData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-dossier-event-result-pdns:hostname_ref.value']]"
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-dossier-event-result-pdns:hostname_ref.value']]"
                },
                'dossierData': {
                    'queries': ['{"offset": 0, "query": "value=domain1.com", "threat_type": "host", "source": "dossierData"}']
                }
            }
        },
        {
            'pattern': "[x-infoblox-dossier-event-result-pdns:ip_ref.value = '1.1.1.1']",
            'expected': {
                'tideDbData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-dossier-event-result-pdns:ip_ref.value']]"
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-dossier-event-result-pdns:ip_ref.value']]"
                },
                'dossierData': {
                    'queries': ['{"offset": 0, "query": "value=1.1.1.1", "threat_type": "ip", "source": "dossierData"}']
                }
            }
        },
        {
            'pattern': "[ipv4-addr:value = '(1.1.1.11111111111111'] START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z'",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&ip=(1.1.1.11111111111111", "threat_type": "ip", "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'queries': ['{"offset": 0, "query": "t0=1624845034&t1=1624848934&qip=(1.1.1.11111111111111", "threat_type": null, "source": "dnsEventData"}']
                },
                'dossierData': {
                    'queries': ['{"offset": 0, "query": "value=(1.1.1.11111111111111", "threat_type": "ip", "source": "dossierData"}']
                }
            }
        },
        {
            'pattern': "[network-traffic:src_ref.value = '{203.0.113.33333333333333333']",
            'expected': {
                'tideDbData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['network-traffic:src_ref.value']]"
                },
                'dnsEventData': {
                    'success': False, 'code': 'mapping_error',
                    'error': 'data mapping error : Unable to map the following STIX objects and properties to data source fields: []'
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['network-traffic:src_ref.value']]"
                }
            }
        },
        {
            'pattern': "[x-infoblox-dns-event:network = 'BloxOne Endpoint'] START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z'",
            'expected': {
                'tideDbData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-dns-event:network']]"
                },
                'dnsEventData': {
                    'queries': ['{"offset": 0, "query": "t0=1624845034&t1=1624848934&network=BloxOne Endpoint", "threat_type": null, "source": "dnsEventData"}']
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-dns-event:network']]"
                }
            }
        },
        {
            'pattern': "[x-infoblox-dns-event:policy_name = 'policy'] START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z'",
            'expected': {
                'tideDbData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-dns-event:policy_name']]"
                },
                'dnsEventData': {
                    'queries': ['{"offset": 0, "query": "t0=1624845034&t1=1624848934&policy_name=policy", "threat_type": null, "source": "dnsEventData"}']
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-dns-event:policy_name']]"
                }
            }
        },
        {
            'pattern': "[x-infoblox-dns-event:x_infoblox_severity = 'HIGH'] START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z'",
            'expected': {
                'tideDbData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-dns-event:x_infoblox_severity']]"
                },
                'dnsEventData': {
                    'queries': ['{"offset": 0, "query": "t0=1624845034&t1=1624848934&threat_level=3", "threat_type": null, "source": "dnsEventData"}']
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-dns-event:x_infoblox_severity']]"
                }
            }
        },
        {
            'pattern': "[x-infoblox-dns-event:threat_class = 'class1'] START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z'",
            'expected': {
                'tideDbData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-dns-event:threat_class']]"
                },
                'dnsEventData': {
                    'queries': ['{"offset": 0, "query": "t0=1624845034&t1=1624848934&threat_class=class1", "threat_type": null, "source": "dnsEventData"}']
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-dns-event:threat_class']]"
                }
            }
        },
        {
            'pattern': "[network-traffic:extensions.'dns-ext'.question.domain_ref.value = 'domain1.com'] START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z'",
            'expected': {
                'tideDbData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['network-traffic:extensions.dns-ext.question.domain_ref.value']]"
                },
                'dnsEventData': {
                    'queries': ['{"offset": 0, "query": "t0=1624845034&t1=1624848934&qname=domain1.com.", "threat_type": null, "source": "dnsEventData"}']
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['network-traffic:extensions.dns-ext.question.domain_ref.value']]"
                }
            }
        },
        {
            'pattern': "[network-traffic:src_ref.value = '1.1.1.1'] START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z'",
            'expected': {
                'tideDbData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['network-traffic:src_ref.value']]"
                },
                'dnsEventData': {
                    'queries': ['{"offset": 0, "query": "t0=1624845034&t1=1624848934&qip=1.1.1.1", "threat_type": null, "source": "dnsEventData"}']
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['network-traffic:src_ref.value']]"
                }
            }
        },
        {
            'pattern': "[network-traffic:src_ref.value = '1.1.1.1' AND network-traffic:src_ref.value = '2.2.2.2'] START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z'",
            'expected': {
                'tideDbData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['network-traffic:src_ref.value', 'network-traffic:src_ref.value']]"
                },
                'dnsEventData': {
                    'queries': [
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&qip=2.2.2.2", "threat_type": null, "source": "dnsEventData"}',
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&qip=1.1.1.1", "threat_type": null, "source": "dnsEventData"}'
                    ]
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['network-traffic:src_ref.value', 'network-traffic:src_ref.value']]"
                }
            }
        },
        {
            'pattern': "([domain-name:value = 'domain1.com'] AND [domain-name:value = 'domain2.com']) START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z'",
            'expected': {
                'tideDbData': {
                    'queries': [
                        '{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&domain=domain1.com", "threat_type": "host", "source": "tideDbData"}',
                        '{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&domain=domain2.com", "threat_type": "host", "source": "tideDbData"}'
                    ]
                },
                'dnsEventData': {
                    'queries': [
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&qname=domain1.com.", "threat_type": null, "source": "dnsEventData"}',
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&qname=domain2.com.", "threat_type": null, "source": "dnsEventData"}'
                    ]
                },
                'dossierData': {
                    'queries': [
                        '{"offset": 0, "query": "value=domain1.com", "threat_type": "host", "source": "dossierData"}',
                        '{"offset": 0, "query": "value=domain2.com", "threat_type": "host", "source": "dossierData"}'
                    ]
                }
            }
        },
        {
            'pattern': "([ipv4-addr:value = '1.1.1.1'] AND [ipv4-addr:value = '2.2.2.2']) START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z'",
            'expected': {
                'tideDbData': {
                    'queries': [
                        '{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&ip=1.1.1.1", "threat_type": "ip", "source": "tideDbData"}',
                        '{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&ip=2.2.2.2", "threat_type": "ip", "source": "tideDbData"}'
                    ]
                },
                'dnsEventData': {
                    'queries': [
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&qip=1.1.1.1", "threat_type": null, "source": "dnsEventData"}',
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&qip=2.2.2.2", "threat_type": null, "source": "dnsEventData"}'
                    ]
                },
                'dossierData': {
                    'queries': [
                        '{"offset": 0, "query": "value=1.1.1.1", "threat_type": "ip", "source": "dossierData"}',
                        '{"offset": 0, "query": "value=2.2.2.2", "threat_type": "ip", "source": "dossierData"}'
                    ]
                }
            }
        },
        {
            'pattern': "([ipv4-addr:value = '1.1.1.1'] OR [ipv4-addr:value = '2.2.2.2']) START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z'",
            'expected': {
                'tideDbData': {
                    'queries': [
                        '{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&ip=1.1.1.1", "threat_type": "ip", "source": "tideDbData"}',
                        '{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&ip=2.2.2.2", "threat_type": "ip", "source": "tideDbData"}'
                    ]
                },
                'dnsEventData': {
                    'queries': [
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&qip=1.1.1.1", "threat_type": null, "source": "dnsEventData"}',
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&qip=2.2.2.2", "threat_type": null, "source": "dnsEventData"}'
                    ]
                },
                'dossierData': {
                    'queries': [
                        '{"offset": 0, "query": "value=1.1.1.1", "threat_type": "ip", "source": "dossierData"}',
                        '{"offset": 0, "query": "value=2.2.2.2", "threat_type": "ip", "source": "dossierData"}'
                    ]
                }
            }
        },
        {
            'pattern': "[domain-name:value = 'domain1.com' OR x-infoblox-dns-event:policy_name = 'policy'] START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z'",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&domain=domain1.com", "threat_type": "host", "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'queries': [
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&policy_name=policy", "threat_type": null, "source": "dnsEventData"}',
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&qname=domain1.com.", "threat_type": null, "source": "dnsEventData"}'
                    ]
                },
                'dossierData': {
                    'queries': ['{"offset": 0, "query": "value=domain1.com", "threat_type": "host", "source": "dossierData"}']
                }
            }
        },
        {
            'pattern': "[domain-name:value = 'domain1.com' AND x-infoblox-dns-event:policy_name = 'policy'] START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z'",
            'expected': {
                'tideDbData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-dns-event:policy_name']]"
                },
                'dnsEventData': {
                    'queries': ['{"offset": 0, "query": "t0=1624845034&t1=1624848934&policy_name=policy&qname=domain1.com.", "threat_type": null, "source": "dnsEventData"}']
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-dns-event:policy_name']]"
                }
            }
        },
        {
            'pattern': "([domain-name:value = 'domain1.com'] AND [x-infoblox-dns-event:policy_name = 'policy']) START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z'",
            'expected': {
                'tideDbData': {
                    'queries': ['{"offset": 0, "query": "from_date=2021-06-28T01:50:34.000Z&to_date=2021-06-28T02:55:34.000Z&domain=domain1.com", "threat_type": "host", "source": "tideDbData"}']
                },
                'dnsEventData': {
                    'queries': [
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&qname=domain1.com.", "threat_type": null, "source": "dnsEventData"}',
                        '{"offset": 0, "query": "t0=1624845034&t1=1624848934&policy_name=policy", "threat_type": null, "source": "dnsEventData"}'
                    ]
                },
                'dossierData': {
                    'queries': ['{"offset": 0, "query": "value=domain1.com", "threat_type": "host", "source": "dossierData"}']
                }
            }
        },
        {
            'pattern': "[(domain-name:value = 'domain1.com' AND x-infoblox-dns-event:policy_name = 'policy') AND network-traffic:src_ref.value = '1.1.1.1'] START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z'",
            'expected': {
                'tideDbData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['network-traffic:src_ref.value', 'x-infoblox-dns-event:policy_name']]"
                },
                'dnsEventData': {
                    'queries': ['{"offset": 0, "query": "t0=1624845034&t1=1624848934&qip=1.1.1.1&policy_name=policy&qname=domain1.com.", "threat_type": null, "source": "dnsEventData"}']
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['network-traffic:src_ref.value', 'x-infoblox-dns-event:policy_name']]"
                }
            }
        },
        {
            'pattern': "[network-traffic:src_ref.value = '1.1.1.1' AND (x-infoblox-dns-event:policy_name = 'policy' AND domain-name:value = 'domain1.com')] START t'2021-06-28T01:50:34Z' STOP t'2021-06-28T02:55:34Z'",
            'expected': {
                'tideDbData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-dns-event:policy_name', 'network-traffic:src_ref.value']]"
                },
                'dnsEventData': {
                    'queries': ['{"offset": 0, "query": "t0=1624845034&t1=1624848934&qname=domain1.com.&policy_name=policy&qip=1.1.1.1", "threat_type": null, "source": "dnsEventData"}']
                },
                'dossierData': {
                    'success': False, 'code': 'mapping_error',
                    'error': "data mapping error : Unable to map the following STIX objects and properties to data source fields: [['x-infoblox-dns-event:policy_name', 'network-traffic:src_ref.value']]"
                }
            }
        },
    ]

    def test_query_parsing(self):
        patterns = []
        for case in self.TEST_CASES:
            patterns.append(case['pattern'])
            for dialect in ['tideDbData', 'dnsEventData', 'dossierData']:
                with self.subTest(msg="query parser", dialect=dialect, pattern=case['pattern']):
                    result = self._parse_query(case['pattern'], dialect)
                    self.assertEqual(result, case['expected'][dialect], "dialect={}, full result={}".format(dialect, result))
        with self.subTest(msg="unique pattern tester", total_patterns=len(patterns)):
            duplicates = set([x for x in patterns if patterns.count(x) > 1])
            self.assertEqual(len(duplicates), 0, "duplicate patterns={}".format(duplicates))

