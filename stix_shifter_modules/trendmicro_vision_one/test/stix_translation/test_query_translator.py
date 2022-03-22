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
        query = translation.translate(f'trendmicro_vision_one:{dialect}', 'query', '{}', stix_pattern)
        return query

    def retrieve_query(self, stix_pattern):
        queries: dict = self._parse_query(stix_pattern, self.get_dialect())
        self.assertIn("queries", queries)
        query = json.loads(queries["queries"][0])
        return query

    def _test_time_range(self, stix_pattern, expectation):
        query = self.retrieve_query(stix_pattern)
        self.assertEqual(expectation, query["to"] - query["from"])

    def _test_pattern(self, pattern, expectation):
        query = self.retrieve_query(pattern)
        self.assertEqual(expectation, query["query"])


class TestStixParsingEndpoint(unittest.TestCase, TestStixParsingMixin):

    def get_dialect(self):
        return "endpointActivityData"

    def test_default_time_range(self):
        stix_pattern = "[user-account:user_id = 'Admin']"
        expectation = 300
        self._test_time_range(stix_pattern, expectation)

    def test_time_range(self):
        stix_pattern = "[user-account:user_id = 'Admin'] START t'2021-04-13T02:55:18Z' STOP t'2021-04-14T02:55:18Z'"
        expectation = 86400
        self._test_time_range(stix_pattern, expectation)

    def test_domain_name(self):
        pattern = "[domain-name:value = 'aaa.bbb.ccc']"
        expectation = 'hostName:"aaa.bbb.ccc"'
        self._test_pattern(pattern, expectation)

    def test_file_sha1(self):
        pattern = "[file:hashes.'SHA-1' = '5e5a7065f1b551eb3632fb189ce1baefd23158aa']"
        expectation = '(srcFileHashSha1:"5e5a7065f1b551eb3632fb189ce1baefd23158aa" OR objectFileHashSha1:"5e5a7065f1b551eb3632fb189ce1baefd23158aa" OR parentFileHashSha1:"5e5a7065f1b551eb3632fb189ce1baefd23158aa" OR processFileHashSha1:"5e5a7065f1b551eb3632fb189ce1baefd23158aa")'
        self._test_pattern(pattern, expectation)

    def test_ipv4(self):
        pattern = "[ipv4-addr:value = '127.0.0.1']"
        expectation = '(src:"127.0.0.1" OR dst:"127.0.0.1" OR objectIp:"127.0.0.1" OR objectIps:"127.0.0.1")'
        self._test_pattern(pattern, expectation)

    def test_ipv6(self):
        pattern = "[ipv6-addr:value = 'fd96:7568:9882:12:9588:1c63:9106:d30d']"
        expectation = '(src:"fd96:7568:9882:12:9588:1c63:9106:d30d" OR dst:"fd96:7568:9882:12:9588:1c63:9106:d30d" OR objectIp:"fd96:7568:9882:12:9588:1c63:9106:d30d" OR objectIps:"fd96:7568:9882:12:9588:1c63:9106:d30d")'
        self._test_pattern(pattern, expectation)

    def test_dst_port(self):
        pattern = "[network-traffic:dst_port = 443]"
        expectation = '(dpt:"443" OR objectPort:"443")'
        self._test_pattern(pattern, expectation)

    def test_dst(self):
        pattern = "[network-traffic:dst_ref.value = '203.0.113.33']"
        expectation = 'dst:"203.0.113.33" OR objectIp:"203.0.113.33"'
        self._test_pattern(pattern, expectation)

    def test_source_port(self):
        pattern = "[network-traffic:src_port = 443]"
        expectation = 'spt:"443"'
        self._test_pattern(pattern, expectation)

    def test_src(self):
        pattern = "[network-traffic:src_ref.value = '203.0.113.33']"
        expectation = 'src:"203.0.113.33"'
        self._test_pattern(pattern, expectation)

    def test_command_line(self):
        pattern = r"[process:command_line = 'c:\\program files\\internet explorer\\iexplore.exe']"
        expectation = '(processCmd:"c:\\program files\\internet explorer\\iexplore.exe" OR parentCmd:"c:\\program files\\internet explorer\\iexplore.exe" OR objectCmd:"c:\\program files\\internet explorer\\iexplore.exe")'
        self._test_pattern(pattern, expectation)

    def test_url(self):
        pattern = "[url:value = 'https://aaa.bbb.ccc']"
        expectation = 'request:"https://aaa.bbb.ccc"'
        self._test_pattern(pattern, expectation)

    def test_account_login(self):
        pattern = "[user-account:account_login = 'Admin']"
        expectation = 'logonUser:"Admin"'
        self._test_pattern(pattern, expectation)

    def test_registry_key(self):
        pattern = r"[windows-registry-key:key = 'hkcu\\software\\microsoft\\internet explorer\\domstorage\\office.com']"
        expectation = r'objectRegistryKeyHandle:"hkcu\software\microsoft\internet explorer\domstorage\office.com"'
        self._test_pattern(pattern, expectation)

    def test_registry_key_value_name(self):
        pattern = "[windows-registry-key:values[*].name = 'AAAAAAAAAAAAAA']"
        expectation = 'objectRegistryValue:"AAAAAAAAAAAAAA"'
        self._test_pattern(pattern, expectation)

    def test_registry_key_value_data(self):
        pattern = "[windows-registry-key:values[*].data = 'AAAAAAAAAAAAAA']"
        expectation = 'objectRegistryData:"AAAAAAAAAAAAAA"'
        self._test_pattern(pattern, expectation)

    def test_operator_like(self):
        pattern = "[domain-name:value LIKE 'microsoft']"
        expectation = 'hostName:microsoft'
        self._test_pattern(pattern, expectation)

    def test_operator_like_escape(self):
        pattern = r"[process:command_line LIKE '(x86)\\internet']"
        expectation = r'(processCmd:\(x86\)\\internet OR parentCmd:\(x86\)\\internet OR objectCmd:\(x86\)\\internet)'
        self._test_pattern(pattern, expectation)

        pattern = r'''[process:command_line LIKE '"C:\\Program'] START t'2021-05-18T05:41:39Z' STOP t'2021-05-19T05:41:39Z' '''
        expectation = r'(processCmd:\"C\:\\Program OR parentCmd:\"C\:\\Program OR objectCmd:\"C\:\\Program)'
        self._test_pattern(pattern, expectation)

    def test_operator_neq(self):
        pattern = "[domain-name:value != 'aaa.bbb.ccc']"
        expectation = 'NOT (hostName:"aaa.bbb.ccc")'
        self._test_pattern(pattern, expectation)

    def test_observation_and(self):
        pattern = "[network-traffic:src_port = 443] AND [network-traffic:src_ref.value = '127.0.0.1']"
        expectation = '(spt:"443") AND (src:"127.0.0.1")'
        self._test_pattern(pattern, expectation)

    def test_observation_or(self):
        pattern = "[network-traffic:src_port = 443] OR [network-traffic:src_ref.value = '127.0.0.1']"
        expectation = '(spt:"443") OR (src:"127.0.0.1")'
        self._test_pattern(pattern, expectation)

    def test_comparison_and(self):
        pattern = "[network-traffic:src_port = 443 AND network-traffic:src_ref.value = '127.0.0.1']"
        expectation = 'src:"127.0.0.1" AND spt:"443"'
        self._test_pattern(pattern, expectation)

    def test_comparison_or(self):
        pattern = "[network-traffic:src_port = 443 OR network-traffic:src_port = 443]"
        expectation = 'spt:"443" OR spt:"443"'
        self._test_pattern(pattern, expectation)

    def test_comparison_in(self):
        pattern = "[network-traffic:src_port IN (443, 446)]"
        expectation = '(spt:"443" OR spt:"446")'
        self._test_pattern(pattern, expectation)

    def test_comparison_in_and(self):
        pattern = "[network-traffic:src_port = 443 AND network-traffic:src_ref.value IN ('127.0.0.1', '127.0.0.2')]"
        expectation = '(src:"127.0.0.1" OR src:"127.0.0.2") AND spt:"443"'
        self._test_pattern(pattern, expectation)


class TestStixParsingMessage(unittest.TestCase, TestStixParsingMixin):
    def get_dialect(self):
        return "messageActivityData"

    def test_domain_name(self):
        pattern = "[domain-name:value = 'aaa.bbb.ccc']"
        expectation = 'source_domain:"aaa.bbb.ccc"'
        self._test_pattern(pattern, expectation)

    def test_message_id(self):
        pattern = "[email-message:message_id = '<89ca86fa053847de8bd45aeb658a4d36-4KNWXI4A=@aaa.bbb.ccc>']"
        expectation = 'message_id:"<89ca86fa053847de8bd45aeb658a4d36-4KNWXI4A=@aaa.bbb.ccc>"'
        self._test_pattern(pattern, expectation)

    def test_sender(self):
        pattern = "[email-message:sender_ref.value = 'o365mc@aaa.bbb.ccc']"
        expectation = '(sender:"o365mc@aaa.bbb.ccc" OR mailbox:"o365mc@aaa.bbb.ccc")'
        self._test_pattern(pattern, expectation)

    def test_subject(self):
        pattern = "[email-message:subject = 'Message Center Major Change Update Notification']"
        expectation = 'subject:"Message Center Major Change Update Notification"'
        self._test_pattern(pattern, expectation)

    def test_to(self):
        pattern = "[email-message:to_refs[*].value = 'o365mc@aaa.bbb.ccc']"
        expectation = '(recipient:"o365mc@aaa.bbb.ccc" OR mailbox:"o365mc@aaa.bbb.ccc")'
        self._test_pattern(pattern, expectation)

    def test_file_name(self):
        pattern = "[file:name = 'abc.txt']"
        expectation = 'file_name:"abc.txt"'
        self._test_pattern(pattern, expectation)

    def test_ipv4(self):
        pattern = "[ipv4-addr:value = '127.0.0.1']"
        expectation = 'source_ip:"127.0.0.1"'
        self._test_pattern(pattern, expectation)

    def test_ipv6(self):
        pattern = "[ipv6-addr:value = '2404:6800:4012:1::2004']"
        expectation = 'source_ip:"2404:6800:4012:1::2004"'
        self._test_pattern(pattern, expectation)

    def test_src(self):
        pattern = "[network-traffic:src_ref.value = '203.0.113.33']"
        expectation = 'source_ip:"203.0.113.33"'
        self._test_pattern(pattern, expectation)

    def test_url(self):
        pattern = "[url:value = 'https://aaa.bbb.ccc']"
        expectation = 'url:"https://aaa.bbb.ccc"'
        self._test_pattern(pattern, expectation)

    def test_operator_like(self):
        pattern = "[domain-name:value LIKE 'microsoft']"
        expectation = 'source_domain:microsoft'
        self._test_pattern(pattern, expectation)

    def test_operator_neq(self):
        pattern = "[domain-name:value != 'aaa.bbb.ccc']"
        # expectation = 'NOT (source_domain:"aaa.bbb.ccc")'
        result = self._parse_query(pattern, self.get_dialect())
        self.assertFalse(result['success'])
        self.assertEqual(result['code'], "not_implemented")

    def test_observation_and(self):
        pattern = "[file:name = 'abc.txt' AND network-traffic:src_ref.value = '127.0.0.1']"
        expectation = 'source_ip:"127.0.0.1" AND file_name:"abc.txt"'
        self._test_pattern(pattern, expectation)

    def test_observation_or(self):
        pattern = "[file:name = 'abc.txt' OR network-traffic:src_ref.value = '127.0.0.1']"
        expectation = 'source_ip:"127.0.0.1" OR file_name:"abc.txt"'
        self._test_pattern(pattern, expectation)

    def test_multiple_operator(self):
        pattern = "[(email-message:to_refs[*].value = 'o365mc@aaa.bbb.ccc' OR email-message:subject = 'o365@aaa.bbb.ccc') AND network-traffic:src_ref.value = '127.0.0.1']"
        result = self._parse_query(pattern, self.get_dialect())
        self.assertFalse(result['success'])
        self.assertEqual(result['code'], "not_implemented")

    def test_multiple_criteria(self):
        pattern = "[network-traffic:src_ref.value = '127.0.0.1' OR network-traffic:src_ref.value = '1.1.1.1']"
        result = self._parse_query(pattern, self.get_dialect())
        self._parse_query(pattern, self.get_dialect())
        self.assertFalse(result['success'])
        self.assertEqual(result['code'], "not_implemented")

    def test_comparison_and(self):
        pattern = "[file:name = 'abc.txt' AND network-traffic:src_ref.value = '127.0.0.1']"
        expectation = 'source_ip:"127.0.0.1" AND file_name:"abc.txt"'
        self._test_pattern(pattern, expectation)

    def test_comparison_or(self):
        pattern = "[file:name = 'abc.txt' OR network-traffic:src_ref.value = '127.0.0.1']"
        expectation = 'source_ip:"127.0.0.1" OR file_name:"abc.txt"'
        self._test_pattern(pattern, expectation)
