# -*- coding: utf-8 -*-
import json
import unittest
import uuid
from datetime import datetime

from stix_shifter_modules.infoblox.entry_point import EntryPoint
from . import utils

class TestDossierResultTranslator(unittest.TestCase, utils.TestResultTranslatorMixin):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.results_translator = EntryPoint().get_results_translator(self.get_dialect())

    @staticmethod
    def get_dialect():
        return "dossierData"

    def test_create_time(self):
        data = [{
            "dossierData": [
                {
                    "job": {
                        "create_time": "2021-07-24T23:44:48.716Z"
                    }
                }
            ]
        }]
        objects = self._get_objects(data)
        ob_data = self._find_by_type(objects, "observed-data")

        result = { key: ob_data[key] for key in ["first_observed", "last_observed"] }
        self.assertEqual(result, {
            "first_observed": "2021-07-24T23:44:48.716Z",
            "last_observed": "2021-07-24T23:44:48.716Z"
        })

    def test_domain(self):
        data = [{
            "dossierData": [{
                "results": [
                    {
                        "data": {
                            "items": [
                                {
                                    "Domain": "example1.com",
                                    "Record_Type": "A"
                                }
                            ]
                        }
                    }
                ]
            }]
        }]
        observed_objects = self._get_observed_objects(data)
        domainKey, domainData = self._find_object_by_type(observed_objects, "domain-name")
        result = { key: domainData[key] for key in ["type", "value"] }
        self.assertEqual(domainData, {
            'type': 'domain-name', 'value': 'example1.com'
        })

        _, dossierData = self._find_object_by_type(observed_objects, "x-infoblox-dossier-event-result-pdns")
        result = { key: dossierData[key] for key in ["type", "domain_ref", "record_type"] }
        self.assertEqual(dossierData, {
            'type': 'x-infoblox-dossier-event-result-pdns', 'domain_ref': domainKey, 'record_type': 'A'
        })

    def test_hostname(self):
        data = [{
            "dossierData": [{
                "results": [
                    {
                        "data": {
                            "items": [
                                {
                                    "Hostname": "example1.com",
                                    "Record_Type": "A"
                                }
                            ]
                        }
                    }
                ]
            }]
        }]
        observed_objects = self._get_observed_objects(data)
        domainKey, domainData = self._find_object_by_type(observed_objects, "domain-name")
        result = { key: domainData[key] for key in ["type", "value"] }
        self.assertEqual(domainData, {
            'type': 'domain-name', 'value': 'example1.com'
        })

        _, dossierData = self._find_object_by_type(observed_objects, "x-infoblox-dossier-event-result-pdns")
        result = { key: dossierData[key] for key in ["type", "hostname_ref", "record_type"] }
        self.assertEqual(dossierData, {
            'type': 'x-infoblox-dossier-event-result-pdns', 'hostname_ref': domainKey, 'record_type': 'A'
        })

    def test_ipv4(self):
        data = [{
            "dossierData": [{
                "results": [
                    {
                        "data": {
                            "items": [
                                {
                                    "IP": "1.1.1.1",
                                    "Record_Type": "A"
                                }
                            ]
                        }
                    }
                ]
            }]
        }]
        observed_objects = self._get_observed_objects(data)
        ipv4Key, ipv4Data = self._find_object_by_type(observed_objects, "ipv4-addr")
        result = { key: ipv4Data[key] for key in ["type", "value"] }
        self.assertEqual(ipv4Data, {
            'type': 'ipv4-addr', 'value': '1.1.1.1'
        })

        _, dossierData = self._find_object_by_type(observed_objects, "x-infoblox-dossier-event-result-pdns")
        result = { key: dossierData[key] for key in ["type", "ip_ref", "record_type"] }
        self.assertEqual(dossierData, {
            'type': 'x-infoblox-dossier-event-result-pdns', 'ip_ref': ipv4Key, 'record_type': 'A'
        })

    def test_ipv6(self):
        data = [{
            "dossierData": [{
                "results": [
                    {
                        "data": {
                            "items": [
                                {
                                    "IP": "2001:db8:3333:4444:5555:6666:7777:8888",
                                    "Record_Type": "A"
                                }
                            ]
                        }
                    }
                ]
            }]
        }]
        observed_objects = self._get_observed_objects(data)
        ipv6Key, ipv6Data = self._find_object_by_type(observed_objects, "ipv6-addr")
        result = { key: ipv6Data[key] for key in ["type", "value"] }
        self.assertEqual(ipv6Data, {
            'type': 'ipv6-addr', 'value': '2001:db8:3333:4444:5555:6666:7777:8888'
        })

        _, dossierData = self._find_object_by_type(observed_objects, "x-infoblox-dossier-event-result-pdns")
        result = { key: dossierData[key] for key in ["type", "ip_ref", "record_type"] }
        self.assertEqual(dossierData, {
            'type': 'x-infoblox-dossier-event-result-pdns', 'ip_ref': ipv6Key, 'record_type': 'A'
        })

    def test_result_pdns(self):
        data = [{
            "dossierData": [{
                "results": [
                    {
                        "data": {
                            "items": [
                                {
                                    "Last_Seen": 1627160591,
                                    "NameServer": "name_server"
                                }
                            ]
                        }
                    }
                ]
            }]
        }]
        observed_objects = self._get_observed_objects(data)
        _, dossierData = self._find_object_by_type(observed_objects, "x-infoblox-dossier-event-result-pdns")
        result = { key: dossierData[key] for key in dossierData.keys() }
        self.assertEqual(dossierData, {
            'type': 'x-infoblox-dossier-event-result-pdns', 'last_seen': 1627160591, 'name_server': 'name_server'
        })
