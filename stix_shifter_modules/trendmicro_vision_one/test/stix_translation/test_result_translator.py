# -*- coding: utf-8 -*-
import unittest
import uuid
from datetime import datetime

from stix_shifter_utils.stix_translation.src.utils.exceptions import LoadJsonResultsException, TranslationResultException

from stix_shifter_modules.trendmicro_vision_one.entry_point import EntryPoint


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
        result = self.results_translator.translate_results(self.data_source, data)
        return result

    def _get_objects(self, data):
        result = self.translate_results(data)
        objects = result["objects"]
        return objects


class TestEndpointResultTranslator(unittest.TestCase, TestResultTranslatorMixin):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.results_translator = EntryPoint().get_results_translator(self.get_dialect())

    @staticmethod
    def get_dialect():
        return "endpointActivityData"

    def test_event_time(self):
        data = [{
            "eventTime": 1602729658866,
        }]
        objects = self._get_objects(data)
        ob_data = self._find_by_type(objects, "observed-data")
        self.assertTrue(ob_data, "No observed-data")
        first_observed = ob_data["first_observed"]
        last_observed = ob_data["last_observed"]
        self.assertEqual(first_observed, "2020-10-15T02:40:58.866Z")
        self.assertEqual(last_observed, "2020-10-15T02:40:58.866Z")

    def test_dst(self):
        data = [{
            "dst": "1.1.1.1",
        }]
        observed_objects = self._get_observed_objects(data)
        ip_key, ip_value = self._find_object_by_type(observed_objects, "ipv4-addr")
        self.assertEqual(ip_value["value"], data[0]["dst"])
        nt_key, nt_value = self._find_object_by_type(observed_objects, "network-traffic")
        self.assertEqual(nt_value["dst_ref"], ip_key)

    def test_dpt(self):
        data = [{
            "dpt": 88,
        }]
        observed_objects = self._get_observed_objects(data)
        key, value = self._find_object_by_type(observed_objects, "network-traffic")
        self.assertEqual(value["dst_port"], data[0]["dpt"])

    def test_src(self):
        data = [{
            "src": "2.2.2.2",
        }]
        observed_objects = self._get_observed_objects(data)
        ip_key, ip_value = self._find_object_by_type(observed_objects, "ipv4-addr")
        self.assertEqual(ip_value["value"], data[0]["src"])
        nt_key, nt_value = self._find_object_by_type(observed_objects, "network-traffic")
        self.assertEqual(nt_value["src_ref"], ip_key)

    def test_spt(self):
        data = [{
            "spt": 99,
        }]
        observed_objects = self._get_observed_objects(data)
        key, value = self._find_object_by_type(observed_objects, "network-traffic")
        self.assertEqual(value["src_port"], data[0]["spt"])

    def test_network_traffic(self):
        data = [{
            "dst": "1.1.1.1",
            "dpt": 88,
            "src": "2.2.2.2",
            "spt": 99,
        }]
        observed_objects = self._get_observed_objects(data)
        key, value = self._find_object_by_type(observed_objects, "network-traffic")
        src_ip_key, src_ip_value = self._find_object(observed_objects, "ipv4-addr", data[0]["src"])
        dst_ip_key, dst_ip_value = self._find_object(observed_objects, "ipv4-addr", data[0]["dst"])
        self.assertEqual(value["src_ref"], src_ip_key)
        self.assertEqual(value["src_port"], data[0]["spt"])
        self.assertEqual(value["dst_ref"], dst_ip_key)
        self.assertEqual(value["dst_port"], data[0]["dpt"])

    def test_endpoint_ip(self):
        data = [{
            "endpointIp": [
                "10.10.58.51",
                "127.0.0.1",
                "fe80::f8e9:b28:a7a5:4b89",
                "::1",
            ]
        }]
        observed_objects = self._get_observed_objects(data)
        self.assertTrue(self._find_object(observed_objects, "ipv4-addr", data[0]["endpointIp"][0]))
        self.assertTrue(self._find_object(observed_objects, "ipv4-addr", data[0]["endpointIp"][1]))
        self.assertTrue(self._find_object(observed_objects, "ipv6-addr", data[0]["endpointIp"][2]))
        self.assertTrue(self._find_object(observed_objects, "ipv6-addr", data[0]["endpointIp"][3]))

    def test_object_ip(self):
        data = [{
            "objectIp": "9.9.9.9",
        }]
        observed_objects = self._get_observed_objects(data)
        self.assertTrue(self._find_object(observed_objects, "ipv4-addr", data[0]["objectIp"]))

    def test_object_port(self):
        data = [{
            "objectPort": 99,
        }]
        observed_objects = self._get_observed_objects(data)
        key, value = self._find_object_by_type(observed_objects, "network-traffic")
        self.assertEqual(value["dst_port"], data[0]["objectPort"])

    def test_object_network_traffic(self):
        data = [{
            "objectIp": "9.9.9.9",
            "objectPort": 999,
        }]
        observed_objects = self._get_observed_objects(data)
        key, value = self._find_object_by_type(observed_objects, "network-traffic")
        dst_ip_key, dst_ip_value = self._find_object(observed_objects, "ipv4-addr", data[0]["objectIp"])
        self.assertEqual(value["dst_ref"], dst_ip_key)
        self.assertEqual(value["dst_port"], data[0]["objectPort"])

    def test_object_ips(self):
        data = [{
            "objectIps": [
                "10.10.58.51",
                "127.0.0.1",
                "fe80::f8e9:b28:a7a5:4b89",
                "::1",
            ]
        }]
        observed_objects = self._get_observed_objects(data)
        self.assertTrue(self._find_object(observed_objects, "ipv4-addr", data[0]["objectIps"][0]))
        self.assertTrue(self._find_object(observed_objects, "ipv4-addr", data[0]["objectIps"][1]))
        self.assertTrue(self._find_object(observed_objects, "ipv6-addr", data[0]["objectIps"][2]))
        self.assertTrue(self._find_object(observed_objects, "ipv6-addr", data[0]["objectIps"][3]))

    def test_logon_user(self):
        data = [{
            "logonUser": "Admin",
        }]
        observed_objects = self._get_observed_objects(data)
        key, value = self._find_object_by_type(observed_objects, "user-account")
        self.assertEqual(value["account_login"], data[0]["logonUser"])

    def test_object_user(self):
        data = [{
            "objectUser": "1001",
        }]
        observed_objects = self._get_observed_objects(data)
        key, value = self._find_object_by_type(observed_objects, "user-account")
        self.assertEqual(value["user_id"], data[0]["objectUser"])

    def test_user_account(self):
        data = [{
            "logonUser": "Admin",
            "objectUser": "1001",
        }]
        observed_objects = self._get_observed_objects(data)
        key, value = self._find_object_by_type(observed_objects, "user-account")
        self.assertEqual(value["account_login"], data[0]["logonUser"])
        self.assertEqual(value["user_id"], data[0]["objectUser"])

    def test_host_name(self):
        data = [{
            "hostName": "aaa.bbb.ccc",
        }]
        observed_objects = self._get_observed_objects(data)
        key, value = self._find_object_by_type(observed_objects, "domain-name")
        self.assertEqual(value["value"], data[0]["hostName"])

    def test_object_host_name(self):
        data = [{
            "objectHostName": "aaa.bbb.ccc",
        }]
        observed_objects = self._get_observed_objects(data)
        key, value = self._find_object_by_type(observed_objects, "domain-name")
        self.assertEqual(value["value"], data[0]["objectHostName"])

    def test_object_cmd(self):
        data = [{
            "objectCmd": "c:\\bin\\object_command.bat",
            "objectFileHashSha1": "999404bd02d9752f406f7440567daf2495870e14",
            "objectFilePath": "c:\\users\\debbie\\appdata\\local\\microsoft\\onedrive\\19.192.0926.0012\\filesync.localizedresources.dll",
        }]
        observed_objects = self._get_observed_objects(data)

        dir_key, dir_value = self._find_object_by_type(observed_objects, "directory")
        self.assertEqual(dir_value["path"], "c:\\users\\debbie\\appdata\\local\\microsoft\\onedrive\\19.192.0926.0012")

        file_key, file_value = self._find_object_by_type(observed_objects, "file")
        self.assertEqual(file_value["name"], "filesync.localizedresources.dll")
        self.assertEqual(file_value["parent_directory_ref"], dir_key)
        self.assertEqual(file_value["hashes"]["SHA-1"], data[0]["objectFileHashSha1"])

        key, value = self._find_object_by_type(observed_objects, "process")
        self.assertEqual(value["command_line"], data[0]["objectCmd"])
        self.assertEqual(value["binary_ref"], file_key)

    def test_object_registry(self):
        data = [{
            "objectRegistryData": "4359",
            "objectRegistryKeyHandle": "hkcu\\software\\microsoft\\internet explorer\\domstorage\\office.com",
            "objectRegistryValue": "total",
        }]
        observed_objects = self._get_observed_objects(data)
        key_key, key_value = self._find_object_by_type(observed_objects, "windows-registry-key")
        self.assertEqual(key_value["key"], r"HKEY_CURRENT_USER\software\microsoft\internet explorer\domstorage\office.com")
        self.assertDictEqual(key_value["values"][0], {'name': data[0]["objectRegistryValue"], 'data': data[0]["objectRegistryData"]})

    def test_process_cmd(self):
        data = [{
            "processCmd": "c:\\program files (x86)\\internet explorer\\iexplore.exe scodef:14872 credat:17410 /prefetch:2",
            "processFileHashSha1": "0b603b11d39ffaf773bf71df3fe854cd652c1a05",
            "processFilePath": "c:\\program files (x86)\\internet explorer\\iexplore.exe",
        }]
        observed_objects = self._get_observed_objects(data)

        dir_key, dir_value = self._find_object_by_type(observed_objects, "directory")
        self.assertEqual(dir_value["path"], "c:\\program files (x86)\\internet explorer")

        file_key, file_value = self._find_object_by_type(observed_objects, "file")
        self.assertEqual(file_value["name"], "iexplore.exe")
        self.assertEqual(file_value["parent_directory_ref"], dir_key)
        self.assertEqual(file_value["hashes"]["SHA-1"], data[0]["processFileHashSha1"])

        key, value = self._find_object_by_type(observed_objects, "process")
        self.assertEqual(value["command_line"], data[0]["processCmd"])
        self.assertEqual(value["binary_ref"], file_key)

    def test_request(self):
        data = [{
            "request": "https://aaa.bbb.ccc",
        }]
        observed_objects = self._get_observed_objects(data)
        key, value = self._find_object_by_type(observed_objects, "url")
        self.assertEqual(value["value"], data[0]["request"])

    def test_parent_cmd(self):
        data = [{
            "parentCmd": "c:\\program files\\internet explorer\\iexplore.exe",
            "parentFileHashSha1": "b1a662c917938e4071d0999e2a942a42d8e2395f",
            "parentFilePath": "c:\\program files\\internet explorer\\iexplore.exe",
        }]
        observed_objects = self._get_observed_objects(data)

        dir_key, dir_value = self._find_object_by_type(observed_objects, "directory")
        self.assertEqual(dir_value["path"], "c:\\program files\\internet explorer")

        file_key, file_value = self._find_object_by_type(observed_objects, "file")
        self.assertEqual(file_value["name"], "iexplore.exe")
        self.assertEqual(file_value["parent_directory_ref"], dir_key)
        self.assertEqual(file_value["hashes"]["SHA-1"], data[0]["parentFileHashSha1"])

        key, value = self._find_object_by_type(observed_objects, "process")
        self.assertEqual(value["command_line"], data[0]["parentCmd"])
        self.assertEqual(value["binary_ref"], file_key)

    def test_src_file(self):
        data = [{
            "srcFileHashSha1": "999404bd02d9752f406f7440567daf2495870e14",
            "srcFilePath": "/src_aaa/bbb/ccc.dat",
        }]
        observed_objects = self._get_observed_objects(data)

        dir_key, dir_value = self._find_object_by_type(observed_objects, "directory")
        self.assertEqual(dir_value["path"], "/src_aaa/bbb")

        file_key, file_value = self._find_object_by_type(observed_objects, "file")
        self.assertEqual(file_value["name"], "ccc.dat")
        self.assertEqual(file_value["parent_directory_ref"], dir_key)
        self.assertEqual(file_value["hashes"]["SHA-1"], data[0]["srcFileHashSha1"])

    def test_malformed_payload(self):
        self.assertRaises(LoadJsonResultsException, self.translate_results, "test")

    def test_missing_id(self):
        self.assertRaises(TranslationResultException, self.results_translator.translate_results, {}, {})


class TestMessageResultTranslator(unittest.TestCase, TestResultTranslatorMixin):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.results_translator = EntryPoint().get_results_translator(self.get_dialect())

    @staticmethod
    def get_dialect():
        return "messageActivityData"

    def test_sender(self):
        data = [{
            "mail_message_sender": "aaa@bbb.ccc.ddd",
        }]
        observed_objects = self._get_observed_objects(data)
        addr_key, addr_value = self._find_object_by_type(observed_objects, "email-addr")
        self.assertEqual(addr_value["value"], data[0]["mail_message_sender"])
        mail_key, mail_value = self._find_object_by_type(observed_objects, "email-message")
        self.assertEqual(mail_value["sender_ref"], addr_key)

    def test_recipient(self):
        data = [{
            "mail_message_recipient": [
                "111xdrwbtest@xdrintwb.bbb.ccc",
                "222xdrwbtest@xdrintwb.bbb.ccc"
            ],
        }]
        observed_objects = self._get_observed_objects(data)
        values_1 = self._find_object(observed_objects, "email-addr", "111xdrwbtest@xdrintwb.bbb.ccc")
        self.assertTrue(values_1)
        value_2 = self._find_object(observed_objects, "email-addr", "222xdrwbtest@xdrintwb.bbb.ccc")
        self.assertTrue(value_2)
        mail_key, mail_value = self._find_object_by_type(observed_objects, "email-message")
        self.assertSetEqual(set(mail_value["to_refs"]), {values_1[0], value_2[0]})

    def test_subject(self):
        data = [{
            "mail_message_subject": "Message Center Major Change Update Notification",
        }]
        observed_objects = self._get_observed_objects(data)
        key, value = self._find_object_by_type(observed_objects, "email-message")
        self.assertEqual(value["subject"], data[0]["mail_message_subject"])

    def test_delivery_time(self):
        data = [{
            "mail_message_delivery_time": "2021-04-13T08:30:56.000Z",
        }]
        observed_objects = self._get_observed_objects(data)
        key, value = self._find_object_by_type(observed_objects, "email-message")
        self.assertEqual(value["date"], data[0]["mail_message_delivery_time"])

    def test_headers(self):
        data = [{
            "mail_message_id": "<abcdef@aaa.bbb.ccc>",
            "mail_internet_headers": [
                {
                    "Value": "aaa@bbb.ccc.ddd",
                    "HeaderName": "Return-Path"
                },
                {
                    "Value": "spf=pass (sender IP is 207.46.50.224); compauth=pass reason=100",
                    "HeaderName": "Authentication-Results"
                }
            ],
        }]
        observed_objects = self._get_observed_objects(data)
        key, value = self._find_object_by_type(observed_objects, "email-message")
        self.assertDictEqual(value["additional_header_fields"], {
            data[0]["mail_internet_headers"][0]["HeaderName"]: data[0]["mail_internet_headers"][0]["Value"],
            data[0]["mail_internet_headers"][1]["HeaderName"]: data[0]["mail_internet_headers"][1]["Value"],
            "Message-ID": data[0]["mail_message_id"],
        })

    def test_message_id(self):
        data = [{
            "mail_message_id": "<abcdef@aaa.bbb.ccc>",
        }]
        observed_objects = self._get_observed_objects(data)
        key, value = self._find_object_by_type(observed_objects, "email-message")
        self.assertDictEqual(value["additional_header_fields"], {
            "Message-ID": data[0]["mail_message_id"],
        })

    def test_email_message(self):
        data = [{
            "mail_message_sender": "aaa@bbb.ccc.ddd",
            "mail_message_recipient": [
                "111xdrwbtest@xdrintwb.bbb.ccc",
                "222xdrwbtest@xdrintwb.bbb.ccc"
            ],
            "mail_message_subject": "Message Center Major Change Update Notification",
            "mail_message_delivery_time": "2021-04-13T08:30:56.000Z",
            "mail_message_id": "<abcdef@aaa.bbb.ccc>",
            "mail_internet_headers": [
                {
                    "Value": "aaa@bbb.ccc.ddd",
                    "HeaderName": "Return-Path"
                },
                {
                    "Value": "spf=pass (sender IP is 207.46.50.224); compauth=pass reason=100",
                    "HeaderName": "Authentication-Results"
                }
            ],
        }]
        observed_objects = self._get_observed_objects(data)
        sender_addr_key, sender_addr_value = self._find_object(observed_objects, "email-addr", "aaa@bbb.ccc.ddd")
        self.assertEqual(sender_addr_value["value"], data[0]["mail_message_sender"])
        values_1 = self._find_object(observed_objects, "email-addr", "111xdrwbtest@xdrintwb.bbb.ccc")
        self.assertTrue(values_1)
        value_2 = self._find_object(observed_objects, "email-addr", "222xdrwbtest@xdrintwb.bbb.ccc")
        self.assertTrue(value_2)
        mail_key, mail_value = self._find_object_by_type(observed_objects, "email-message")
        self.assertEqual(mail_value["sender_ref"], sender_addr_key)
        self.assertSetEqual(set(mail_value["to_refs"]), {values_1[0], value_2[0]})
        self.assertEqual(mail_value["subject"], data[0]["mail_message_subject"])
        self.assertEqual(mail_value["date"], data[0]["mail_message_delivery_time"])
        self.assertDictEqual(mail_value["additional_header_fields"], {
            data[0]["mail_internet_headers"][0]["HeaderName"]: data[0]["mail_internet_headers"][0]["Value"],
            data[0]["mail_internet_headers"][1]["HeaderName"]: data[0]["mail_internet_headers"][1]["Value"],
            "Message-ID": data[0]["mail_message_id"],
        })

    def test_mail_urls(self):
        data = [{
            "mail_urls": [
                "https://aaa.bbb.ccc/ddd",
                "https://bbb.ccc.ddd/eee"
            ],
        }]
        observed_objects = self._get_observed_objects(data)
        urls = {value[1]["value"] for value in self._find_objects_by_type(observed_objects, "url")}
        self.assertSetEqual(urls, set(data[0]["mail_urls"]))

    def test_source_domain(self):
        data = [{
            "source_domain": "aaa.bbb.ccc",
        }]
        observed_objects = self._get_observed_objects(data)
        key, value = self._find_object_by_type(observed_objects, "domain-name")
        self.assertEqual(value["value"], data[0]["source_domain"])

    def test_source_ip(self):
        data = [{
            "source_ip": "207.46.50.224",
        }]
        observed_objects = self._get_observed_objects(data)
        ip_key, ip_value = self._find_object_by_type(observed_objects, "ipv4-addr")
        self.assertEqual(ip_value["value"], data[0]["source_ip"])
        nt_key, nt_value = self._find_object_by_type(observed_objects, "network-traffic")
        self.assertEqual(nt_value["src_ref"], ip_key)

    def test_attachments(self):
        data = [{
            "mail_attachments": [
                {
                    "file_name": "test111.txt"
                },
                {
                    "file_sha1": "46932d56cd30feda77c878e2f72432fce2736918",
                },
                {
                    "file_sha1": "823c3ee108cbfbf27c39361682592f83cdd8ad24",
                    "file_name": "tes333.txt"
                }
            ],
        }]
        observed_objects = self._get_observed_objects(data)
        file_obj = [value[1] for value in self._find_objects_by_type(observed_objects, "file")]
        file_item = file_obj[0]
        self.assertEqual(file_item["name"], data[0]["mail_attachments"][0].get("file_name", ""))
        file_item = file_obj[1]
        self.assertEqual(file_item["hashes"]["SHA-1"], data[0]["mail_attachments"][1]["file_sha1"])
        file_item = file_obj[2]
        self.assertEqual(file_item["name"], data[0]["mail_attachments"][2].get("file_name", ""))
        self.assertEqual(file_item["hashes"]["SHA-1"], data[0]["mail_attachments"][2]["file_sha1"])
