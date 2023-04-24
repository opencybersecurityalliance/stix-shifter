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

    def _get_observed_objects(self, data):
        objects = self._get_objects(data)
        ob_data = self._find_by_type(objects, "observed-data")
        return ob_data["objects"]

    def translate_results(self, data):
        result = self.results_translator.translate_results(self.data_source, data)
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
        data = [{ "dnsEventData": { "event_time": "2021-05-24T20:26:04.000Z" } }]
        objects = self._get_objects(data)
        ob_data = self._find_by_type(objects, "observed-data")

        result = { key: ob_data[key] for key in ["first_observed", "last_observed"] }
        self.assertEqual(result, {
            "first_observed": "2021-05-24T20:26:04.000Z",
            "last_observed": "2021-05-24T20:26:04.000Z"
        })

    def test_private_ip(self):
        data = [{"dnsEventData": {"private_ip": "1.1.1.1"}}]
        observed_objects = self._get_observed_objects(data)
        _, dnsEvent = self._find_object_by_type(observed_objects, "ipv4-addr")
        self.assertEqual(dnsEvent, {'type': 'ipv4-addr', 'value': '1.1.1.1'})

    def test_mac_address(self):
        data = [{"dnsEventData": {"mac_address": "00:50:56:0b:06:58", "private_ip": "1.1.1.1"}}]
        observed_objects = self._get_observed_objects(data)
        macKey, macData = self._find_object_by_type(observed_objects, "mac-addr")
        self.assertEqual(macData, {'type': 'mac-addr', 'value': '00:50:56:0b:06:58'})
        _, ipv4Data = self._find_object_by_type(observed_objects, "ipv4-addr")
        self.assertEqual(ipv4Data, {'type': 'ipv4-addr', 'resolves_to_refs': [macKey], 'value': '1.1.1.1'})

    def test_qip(self):
        data = [{"dnsEventData": {"qip": "1.1.1.2"}}]
        observed_objects = self._get_observed_objects(data)
        ipv4Key, ipv4Data = self._find_object_by_type(observed_objects, "ipv4-addr")
        result = { key: ipv4Data[key] for key in ["type", "value"] }
        self.assertEqual(ipv4Data, {'type': 'ipv4-addr', 'value': '1.1.1.2'})

        _, networkData = self._find_object_by_type(observed_objects, "network-traffic")
        self.assertEqual(networkData, {'type': 'network-traffic', 'src_ref': ipv4Key, "protocols": ['domain']})

    def test_rip(self):
        data = [{"dnsEventData": {"rip": "1.1.1.3",}}]
        observed_objects = self._get_observed_objects(data)
        ipv4Key, ipv4Data = self._find_object_by_type(observed_objects, "ipv4-addr")
        result = { key: ipv4Data[key] for key in ["type", "value"] }
        self.assertEqual(ipv4Data, {'type': 'ipv4-addr', 'value': '1.1.1.3'})

        _, networkData = self._find_object_by_type(observed_objects, "network-traffic")
        self.assertEqual(networkData, {
            'type': 'network-traffic', 'extensions': {'dns-ext': {'resolved_ip_refs': [ipv4Key]}}
        })

    def test_qname(self):
        data = [{"dnsEventData": {"qname": "example.com."}}]
        observed_objects = self._get_observed_objects(data)
        ipv4Key, ipv4Data = self._find_object_by_type(observed_objects, "domain-name")
        result = { key: ipv4Data[key] for key in ["type", "value"] }
        self.assertEqual(ipv4Data, {'type': 'domain-name', 'value': 'example.com'})

        _, networkData = self._find_object_by_type(observed_objects, "network-traffic")
        result = { key: networkData[key] for key in ["type", "extensions"] }
        self.assertEqual(networkData, {'type': 'network-traffic', 'extensions': {'dns-ext': {'question': {'domain_ref': ipv4Key}}}})

    def test_user(self):
        data = [{"dnsEventData": {"user": "rdp", "feed_name": "Base"}}]
        observed_objects = self._get_observed_objects(data)
        userKey, userData = self._find_object_by_type(observed_objects, "user-account")
        result = { key: userData[key] for key in ["type", "user_id"] }
        self.assertEqual(userData, {'type': 'user-account', 'user_id': 'rdp'})

        _, networkData = self._find_object_by_type(observed_objects, "x-infoblox-dns-event")
        result = { key: networkData[key] for key in ["type", "user_ref", "feed_name"] }
        self.assertEqual(networkData, {'type': 'x-infoblox-dns-event', 'user_ref': userKey, 'feed_name': 'Base'})

    def test_network_traffic(self):
        data = [{"dnsEventData": {"qtype": "A", "category": "", "confidence": "HIGH", "country": "unknown", "device": "DESKTOP-VT5P2QT", "dhcp_fingerprint": "", "feed_name": "Base",
                "feed_type": "FQDN", "network": "BloxOne Endpoint", "os_version": "Windows 10 Enterprise", "policy_name": "DFND", "qtype": "A", "rcode": "PASSTHRU", "rdata": "1.1.1.1,2.2.2.2",
                "severity": "HIGH", "tclass": "APT", "threat_indicator": "total-update.com", "tproperty": "MalwareC2"}}]
        observed_objects = self._get_observed_objects(data)
        _, nt = self._find_object_by_type(observed_objects, "network-traffic")
        self.assertEqual(nt, {'type': 'network-traffic','extensions': {'dns-ext': {'type': 'A', 'response_code': 'PASSTHRU', 'answers': {'data': '1.1.1.1,2.2.2.2'}}}})

        _, dnsEvent = self._find_object_by_type(observed_objects, "x-infoblox-dns-event")
        self.assertEqual(dnsEvent, {'type': 'x-infoblox-dns-event','x_infoblox_confidence': 'HIGH', 'country': 'unknown', 'device': 'DESKTOP-VT5P2QT', 'feed_name': 'Base',
            'feed_type': 'FQDN', 'network': 'BloxOne Endpoint', 'os_version': 'Windows 10 Enterprise', 'policy_name': 'DFND',
            'x_infoblox_severity': 'HIGH', 'threat_class': 'APT', 'threat_indicator': 'total-update.com', 'threat_property': 'MalwareC2'
        })

class TestDossierResultTranslator(unittest.TestCase, TestResultTranslatorMixin):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.results_translator = EntryPoint().get_results_translator(self.get_dialect())

    @staticmethod
    def get_dialect():
        return "dossierData"

    def test_create_time(self):
        data = [{"dossierData": [{"job": {"create_time": "2021-07-24T23:44:48.716Z"}}]}]
        objects = self._get_objects(data)
        ob_data = self._find_by_type(objects, "observed-data")

        result = { key: ob_data[key] for key in ["first_observed", "last_observed"] }
        self.assertEqual(result, {"first_observed": "2021-07-24T23:44:48.716Z","last_observed": "2021-07-24T23:44:48.716Z"})

    def test_domain(self):
        data = [{"dossierData": [{"results": [{"data": {"items": [{"Domain": "example1.com","Record_Type": "A"}]}}]}]}]
        observed_objects = self._get_observed_objects(data)
        domainKey, domainData = self._find_object_by_type(observed_objects, "domain-name")
        result = { key: domainData[key] for key in ["type", "value"] }
        self.assertEqual(domainData, {'type': 'domain-name', 'value': 'example1.com'})

        _, dossierData = self._find_object_by_type(observed_objects, "x-infoblox-dossier-event-result-pdns")
        result = { key: dossierData[key] for key in ["type", "domain_ref", "record_type"] }
        self.assertEqual(dossierData, {'type': 'x-infoblox-dossier-event-result-pdns', 'domain_ref': domainKey, 'record_type': 'A'})

    def test_hostname(self):
        data = [{"dossierData": [{"results": [{"data": {"items": [{"Hostname": "example1.com","Record_Type": "A"}]}}]}]}]
        observed_objects = self._get_observed_objects(data)
        domainKey, domainData = self._find_object_by_type(observed_objects, "domain-name")
        result = { key: domainData[key] for key in ["type", "value"] }
        self.assertEqual(domainData, {'type': 'domain-name', 'value': 'example1.com'})

        _, dossierData = self._find_object_by_type(observed_objects, "x-infoblox-dossier-event-result-pdns")
        result = { key: dossierData[key] for key in ["type", "hostname_ref", "record_type"] }
        self.assertEqual(dossierData, {'type': 'x-infoblox-dossier-event-result-pdns', 'hostname_ref': domainKey, 'record_type': 'A'})

    def test_ipv4(self):
        data = [{"dossierData": [{"results": [{"data": {"items": [{"IP": "1.1.1.1","Record_Type": "A"}]}}]}]}]
        observed_objects = self._get_observed_objects(data)
        ipv4Key, ipv4Data = self._find_object_by_type(observed_objects, "ipv4-addr")
        result = { key: ipv4Data[key] for key in ["type", "value"] }
        self.assertEqual(ipv4Data, {'type': 'ipv4-addr', 'value': '1.1.1.1'})

        _, dossierData = self._find_object_by_type(observed_objects, "x-infoblox-dossier-event-result-pdns")
        result = { key: dossierData[key] for key in ["type", "ip_ref", "record_type"] }
        self.assertEqual(dossierData, {'type': 'x-infoblox-dossier-event-result-pdns', 'ip_ref': ipv4Key, 'record_type': 'A'})

    def test_ipv6(self):
        data = [{"dossierData": [{"results": [{"data": {"items": [{"IP": "2001:db8:3333:4444:5555:6666:7777:8888","Record_Type": "A"}]}}]}]}]
        observed_objects = self._get_observed_objects(data)
        ipv6Key, ipv6Data = self._find_object_by_type(observed_objects, "ipv6-addr")
        result = { key: ipv6Data[key] for key in ["type", "value"] }
        self.assertEqual(ipv6Data, {'type': 'ipv6-addr', 'value': '2001:db8:3333:4444:5555:6666:7777:8888'})

        _, dossierData = self._find_object_by_type(observed_objects, "x-infoblox-dossier-event-result-pdns")
        result = { key: dossierData[key] for key in ["type", "ip_ref", "record_type"] }
        self.assertEqual(dossierData, {'type': 'x-infoblox-dossier-event-result-pdns', 'ip_ref': ipv6Key, 'record_type': 'A'})

    def test_result_pdns(self):
        data = [{"dossierData": [{"results": [{"data": {"items": [{"Last_Seen": 1627160591,"NameServer": "name_server"}]}}]}]}]
        observed_objects = self._get_observed_objects(data)
        _, dossierData = self._find_object_by_type(observed_objects, "x-infoblox-dossier-event-result-pdns")
        result = { key: dossierData[key] for key in dossierData.keys() }
        self.assertEqual(dossierData, {'type': 'x-infoblox-dossier-event-result-pdns', 'last_seen': 1627160591, 'name_server': 'name_server'})


class TestTideResultTranslator(unittest.TestCase, TestResultTranslatorMixin):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.results_translator = EntryPoint().get_results_translator(self.get_dialect())

    @staticmethod
    def get_dialect():
        return "tideDbData"

    def test_detected_time(self):
        data = [{"tideDbData": {"detected": "2021-05-24T20:26:04.000Z",}}]
        objects = self._get_objects(data)
        ob_data = self._find_by_type(objects, "observed-data")

        result = { key: ob_data[key] for key in ["first_observed", "last_observed"] }
        self.assertEqual(result, {"first_observed": "2021-05-24T20:26:04.000Z","last_observed": "2021-05-24T20:26:04.000Z"})

    def test_ipv4(self):
        data = [{"tideDbData" : [{"ip": "1.1.1.1"}]}]
        observed_objects = self._get_observed_objects(data)
        _, obj = self._find_object_by_type(observed_objects, "ipv4-addr")
        self.assertEqual(obj, {'type': 'ipv4-addr', 'value': '1.1.1.1'})

    def test_ipv6(self):
        data = [{"tideDbData" : [{ "ip": "2001:db8:3333:4444:5555:6666:7777:8888"}]}]
        observed_objects = self._get_observed_objects(data)
        _, obj = self._find_object_by_type(observed_objects, "ipv6-addr")
        self.assertEqual(obj, {'type': 'ipv6-addr', 'value': '2001:db8:3333:4444:5555:6666:7777:8888'})


    def test_domain(self):
        data = [{"tideDbData" : [{"domain": "example.com"}]}]
        observed_objects = self._get_observed_objects(data)
        _, obj = self._find_object_by_type(observed_objects, "domain-name")
        self.assertEqual(obj, {'type': 'domain-name', 'value': 'example.com'})

    def test_email(self):
        data = [{"tideDbData" : [{"email": "foo@example.com"}]}]

        observed_objects = self._get_observed_objects(data)
        _, obj = self._find_object_by_type(observed_objects, "email-addr")
        self.assertEqual(obj, {'type': 'email-addr', 'value': 'foo@example.com'})


    def test_multiple_entries(self):
        data = [{"tideDbData" : [{"type": "IP"},{"type": "IP"}]}]

        observed_objects = self._get_observed_objects(data)
        self.assertEqual(2, len(observed_objects))
        for index in observed_objects:
            obj = observed_objects[index]
            self.assertEqual(obj, {'threat_type': 'IP', 'type': 'x-infoblox-threat'})

    def test_x_infoblox_threat(self):
        data = [{"tideDbData" : [{"id": "1d26606e-dfde-11eb-93d6-438342be5508","type": "IP","profile": "AISCOMM","property": "Scanner_Generic","class": "Scanner","confidence": 80,
                "dga": False,"hash":"12345","host": "sinkhole.eicar.network","origin": "origin_string","target": "target_string","threat_level": 80,"tld": "website",
                "detected": "2021-07-08T11:16:41.685Z","received": "2021-07-08T11:17:42.947Z","imported": "2021-07-08T11:17:42.947Z","expiration": "2021-07-22T11:16:41.685Z","up": True,
                "url": "https://example.com/example/path","batch_id": "1d21a511-dfde-11eb-93d6-438342be5508","extended": {"ais_consent": "EVERYONE","cyberint_guid": "13d95254b1792d5949e8ae73525c44b8"}}]}]

        observed_objects = self._get_observed_objects(data)
        _, xinfobloxThreat = self._find_object_by_type(observed_objects, "x-infoblox-threat")
        self.assertEqual(xinfobloxThreat, {"id": "1d26606e-dfde-11eb-93d6-438342be5508","type": "x-infoblox-threat","threat_class": "Scanner","x_infoblox_confidence": 80,"dga": False,
            "expiration": "2021-07-22T11:16:41.685Z","hash": "12345","host_name": "sinkhole.eicar.network","imported": "2021-07-08T11:17:42.947Z","received": "2021-07-08T11:17:42.947Z",
            "origin": "origin_string","profile": "AISCOMM","property": "Scanner_Generic","target": "target_string","threat_level": 80,"top_level_domain": "website",
			"threat_type": "IP","active": True,"url": "https://example.com/example/path",
        })