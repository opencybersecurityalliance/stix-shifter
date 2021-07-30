# -*- coding: utf-8 -*-
import json
import unittest
import uuid
from datetime import datetime

from stix_shifter_modules.infoblox.entry_point import EntryPoint
from . import utils

class TestTideResultTranslator(unittest.TestCase, utils.TestResultTranslatorMixin):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.results_translator = EntryPoint().get_results_translator(self.get_dialect())

    @staticmethod
    def get_dialect():
        return "tideDbData"

    # def test_event_time(self):
    #     data = [{
    #         "received": "2021-05-24T20:26:04.000Z",
    #         "detected": "2021-05-24T20:26:05.000Z",
    #     }]
    #     objects = self._get_objects(data)
    #     ob_data = self._find_by_type(objects, "observed-data")

    #     print (ob_data)
        
    #     result = { key: ob_data[key] for key in ["created", "modified", "first_observed", "last_observed"] }
    #     self.assertEqual(result, {
    #         "created": "2021-05-24T20:26:04.000Z",
    #         "modified": "2021-05-24T20:26:04.000Z",
    #         "first_observed": "2021-05-24T20:26:05.000Z",
    #         "last_observed": "2021-05-24T20:26:05.000Z"
    #     })

    def test_ip(self):
        data = [{
            "ip": "1.1.1.1",
        }]
        observed_objects = self._get_observed_objects(data)
        _, obj = self._find_object_by_type(observed_objects, "ipv4-addr")
        result = { key: obj[key] for key in ["type", "value"] }
        self.assertEqual(result, {
            'type': 'ipv4-addr', 'value': '1.1.1.1'
        })

    def test_domain(self):
        data = [{
            "domain": "example.com"
        }]
        observed_objects = self._get_observed_objects(data)
        _, obj = self._find_object_by_type(observed_objects, "domain-name")
        result = { key: obj[key] for key in ["type", "value"] }
        self.assertEqual(result, {
            'type': 'domain-name', 'value': 'example.com'
        })

    def test_email(self):
        data = [{
            "email": "foo@example.com",
            "class": "Threat Class"
        }]
        observed_objects = self._get_observed_objects(data)
        _, obj = self._find_object_by_type(observed_objects, "email-addr")
        result = { key: obj[key] for key in ["type", "value"] }
        self.assertEqual(obj, {
            'type': 'email-addr', 'value': 'foo@example.com'
        })

    
    def test_x_infoblox_threat(self):
        data = [{
            "id": "1d26606e-dfde-11eb-93d6-438342be5508",
            "type": "IP",
            "profile": "AISCOMM",
            "property": "Scanner_Generic",
            "class": "Scanner",
            "confidence": 80,
            "dga": False,
            "hash":"12345",
            "host": "sinkhole.eicar.network",
            "origin": "origin_string",
            "target": "target_string",
            "threat_level": 80,
            "tld": "website",
            "detected": "2021-07-08T11:16:41.685Z",
            "received": "2021-07-08T11:17:42.947Z",
            "imported": "2021-07-08T11:17:42.947Z",
            "expiration": "2021-07-22T11:16:41.685Z",
            "up": True,
            "url": "https://example.com/example/path",
            "batch_id": "1d21a511-dfde-11eb-93d6-438342be5508",
            "extended": {
                "ais_consent": "EVERYONE",
                "cyberint_guid": "13d95254b1792d5949e8ae73525c44b8"
            }
        }]

        observed_objects = self._get_observed_objects(data)
        _, xinfobloxThreat = self._find_object_by_type(observed_objects, "x-infoblox-threat")
        result = { key: xinfobloxThreat[key] for key in ["type", 
                                                         "threat_class",
                                                         "x_infoblox_confidence",
                                                         "dga",
                                                         "expiration",
                                                         "hash",
                                                         "host_name",
                                                         "imported",
                                                         "origin",
                                                         "profile",
                                                         "property",
                                                         "target",
                                                         "threat_level",
                                                         "top_level_domain",
                                                         "threat_type",
                                                         "active",
                                                         "url"] }

        self.assertEqual(result, {
            "type": "x-infoblox-threat",
            "threat_class": "Scanner",
            "x_infoblox_confidence": 80,
            "dga": False,
            "expiration": "2021-07-22T11:16:41.685Z",
            "hash": "12345",
            "host_name": "sinkhole.eicar.network",
            "imported": "2021-07-08T11:17:42.947Z",
            "origin": "origin_string",
            "profile": "AISCOMM",
            "property": "Scanner_Generic",
            "target": "target_string",
            "threat_level": 80,
            "top_level_domain": "website",
			"threat_type": "IP",
			"active": True,
            "url": "https://example.com/example/path",
            })