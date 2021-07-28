# -*- coding: utf-8 -*-
import json
import unittest
import uuid
from datetime import datetime

from stix_shifter_modules.infoblox.entry_point import EntryPoint


class TestResultTranslatorMixin:

    @staticmethod
    def get_dialect():
        raise NotImplementedError()

    @property
    def data_source(self):
        now = "{}Z".format(datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3])
        return {
            "id": "identity--" + str(uuid.uuid4()),
            "name": "name",
            "type": "identity",
            "identity_class": "individual",
            "created": now,
            "modified": now
        }

    @staticmethod
    def _find_by_type(objects, obj_type):
        return next((obj for obj in objects if obj["type"] == obj_type), None)

    @staticmethod
    def _find_object_by_type(objects: dict, obj_type):
        return next(((key, obj) for key, obj in objects.items() if obj["type"] == obj_type), None)

    @staticmethod
    def _find_objects_by_type(objects: dict, obj_type):
        return [(key, obj) for key, obj in objects.items() if obj["type"] == obj_type]

    @staticmethod
    def _find_object(objects: dict, obj_type, obj_value):
        return next(((key, obj) for key, obj in objects.items() if obj["type"] == obj_type and obj["value"] == obj_value), None)

    def _get_observed_objects(self, data):
        objects = self._get_objects(data)
        ob_data = self._find_by_type(objects, "observed-data")
        return ob_data["objects"]

    def translate_results(self, data):
        result = self.results_translator.translate_results(json.dumps(self.data_source), json.dumps(data))
        return result

    def _get_objects(self, data):
        result = self.translate_results(data)
        objects = result["objects"]
        return objects

class TestDNSEventResultTranslator(unittest.TestCase, TestResultTranslatorMixin):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.results_translator = EntryPoint().get_results_translator(self.get_dialect())

    @staticmethod
    def get_dialect():
        return "dnsEventData"

    def test_event_time(self):
        data = [{
            "event_time": "2021-05-24T20:26:04.000Z",
        }]
        objects = self._get_objects(data)
        ob_data = self._find_by_type(objects, "observed-data")

        result = { key: ob_data[key] for key in ["first_observed", "last_observed"] }
        self.assertEqual(result, {
            "first_observed": "2021-05-24T20:26:04.000Z",
            "last_observed": "2021-05-24T20:26:04.000Z"
        })

    def test_private_ip(self):
        data = [{
            "private_ip": "1.1.1.1",
        }]
        observed_objects = self._get_observed_objects(data)
        _, dnsEvent = self._find_object_by_type(observed_objects, "ipv4-addr")
        result = { key: dnsEvent[key] for key in ["type", "value"] }
        self.assertEqual(dnsEvent, {
            'type': 'ipv4-addr', 'value': '1.1.1.1'
        })

    def test_mac_address(self):
        data = [{
            "mac_address": "00:50:56:0b:06:58",
            "private_ip": "1.1.1.1",
        }]
        observed_objects = self._get_observed_objects(data)
        macKey, macData = self._find_object_by_type(observed_objects, "mac-addr")
        self.assertEqual(macData, {
            'type': 'mac-addr', 'value': '00:50:56:0b:06:58'
        })
        _, ipv4Data = self._find_object_by_type(observed_objects, "ipv4-addr")
        self.assertEqual(ipv4Data, {
            'type': 'ipv4-addr', 'resolves_to_refs': [macKey], 'value': '1.1.1.1'
        })

    def test_qip(self):
        data = [{
            "qip": "1.1.1.2",
        }]
        observed_objects = self._get_observed_objects(data)
        ipv4Key, ipv4Data = self._find_object_by_type(observed_objects, "ipv4-addr")
        result = { key: ipv4Data[key] for key in ["type", "value"] }
        self.assertEqual(ipv4Data, {
            'type': 'ipv4-addr', 'value': '1.1.1.2'
        })

        _, networkData = self._find_object_by_type(observed_objects, "network-traffic")
        result = { key: networkData[key] for key in ["type", "src_ref", "protocols"] }
        self.assertEqual(networkData, {
            'type': 'network-traffic', 'src_ref': ipv4Key, "protocols": ['domain']
        })

    def test_rip(self):
        data = [{
            "rip": "1.1.1.3",
        }]
        observed_objects = self._get_observed_objects(data)
        ipv4Key, ipv4Data = self._find_object_by_type(observed_objects, "ipv4-addr")
        result = { key: ipv4Data[key] for key in ["type", "value"] }
        self.assertEqual(ipv4Data, {
            'type': 'ipv4-addr', 'value': '1.1.1.3'
        })

        _, networkData = self._find_object_by_type(observed_objects, "network-traffic")
        result = { key: networkData[key] for key in ["type", "extensions"] }
        self.assertEqual(networkData, {
            'type': 'network-traffic', 'extensions': {'dns-ext': {'resolved_ip_refs': [ipv4Key]}}
        })

    def test_qname(self):
        data = [{
            "qname": "example.com.",
        }]
        observed_objects = self._get_observed_objects(data)
        ipv4Key, ipv4Data = self._find_object_by_type(observed_objects, "domain-name")
        result = { key: ipv4Data[key] for key in ["type", "value"] }
        self.assertEqual(ipv4Data, {
            'type': 'domain-name', 'value': 'example.com'
        })

        _, networkData = self._find_object_by_type(observed_objects, "network-traffic")
        result = { key: networkData[key] for key in ["type", "extensions"] }
        self.assertEqual(networkData, {
            'type': 'network-traffic', 'extensions': {'dns-ext': {'question': {'domain_ref': ipv4Key}}}
        })

    def test_user(self):
        data = [{
            "user": "rdp",
            "feed_name": "Base",
        }]
        observed_objects = self._get_observed_objects(data)
        userKey, userData = self._find_object_by_type(observed_objects, "user-account")
        result = { key: userData[key] for key in ["type", "user_id"] }
        self.assertEqual(userData, {
            'type': 'user-account', 'user_id': 'rdp'
        })

        _, networkData = self._find_object_by_type(observed_objects, "x-infoblox-dns-event")
        result = { key: networkData[key] for key in ["type", "user_ref", "feed_name"] }
        self.assertEqual(networkData, {
            'type': 'x-infoblox-dns-event', 'user_ref': userKey, 'feed_name': 'Base'
        })

    def test_network_traffic(self):
        data = [{
            "qtype": "A",
            "category": "",
            "confidence": "HIGH",
            "country": "unknown",
            "device": "DESKTOP-VT5P2QT",
            "dhcp_fingerprint": "",
            "feed_name": "Base",
            "feed_type": "FQDN",
            "network": "BloxOne Endpoint",
            "os_version": "Windows 10 Enterprise",
            "policy_name": "DFND",
            "qtype": "A",
            "rcode": "PASSTHRU",
            "rdata": "1.1.1.1,2.2.2.2",
            "severity": "HIGH",
            "tclass": "APT",
            "threat_indicator": "total-update.com",
            "tproperty": "MalwareC2"
        }]
        observed_objects = self._get_observed_objects(data)
        _, nt = self._find_object_by_type(observed_objects, "network-traffic")
        self.assertEqual(nt, {
            'type': 'network-traffic', 
            'extensions': {'dns-ext': {'type': 'A', 'response_code': 'PASSTHRU', 'answers': {'data': '1.1.1.1,2.2.2.2'}}}
        })

        _, dnsEvent = self._find_object_by_type(observed_objects, "x-infoblox-dns-event")
        self.assertEqual(dnsEvent, {
            'type': 'x-infoblox-dns-event', 
            'x_infoblox_confidence': 'HIGH', 'country': 'unknown', 'device': 'DESKTOP-VT5P2QT', 'feed_name': 'Base', 
            'feed_type': 'FQDN', 'network': 'BloxOne Endpoint', 'os_version': 'Windows 10 Enterprise', 'policy_name': 'DFND', 
            'x_infoblox_severity': 'HIGH', 'threat_class': 'APT', 'threat_indicator': 'total-update.com', 'threat_property': 'MalwareC2'
        })
