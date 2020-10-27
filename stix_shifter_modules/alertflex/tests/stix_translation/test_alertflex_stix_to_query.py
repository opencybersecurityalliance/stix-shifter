from stix_shifter.stix_translation import stix_translation
import unittest

translation = stix_translation.StixTranslation()


class TestQueryTranslator(unittest.TestCase):
    """
    class to perform unit test case alertflex translate query
    """

    def test_ipv4_addr(self):
        stix_pattern = "[ipv4-addr:value = '192.168.1.1']"
        queries = translation.translate('alertflex', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ["SELECT a FROM Alert a WHERE (a.dstIp = '192.168.1.1' OR a.srcIp = '192.168.1.1')"]

        self.assertEqual(query, test_string)

    def test_file_name(self):
        stix_pattern = "[file:name = 'file_name']"
        queries = translation.translate('alertflex', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ["SELECT a FROM Alert a WHERE a.fileName = 'file_name'"]

        self.assertEqual(query, test_string)

    def test_file_md5(self):
        stix_pattern = "[file:hashes.MD5 = '7d351ff6fea9e9dc100b7deb0e03fd35']"
        queries = translation.translate('alertflex', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ["SELECT a FROM Alert a WHERE a.hashMd5 = '7d351ff6fea9e9dc100b7deb0e03fd35'"]

        self.assertEqual(query, test_string)

    def test_process(self):
        stix_pattern = "[process:name = 'process_name']"
        queries = translation.translate('alertflex', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ["SELECT a FROM Alert a WHERE a.processName = 'process_name'"]

        self.assertEqual(query, test_string)


    def test_user(self):
        stix_pattern = "[user-account:user_id = 'user_id']"
        queries = translation.translate('alertflex', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ["SELECT a FROM Alert a WHERE a.userName = 'user_id'"]

        self.assertEqual(query, test_string)

    def test_source(self):
        stix_pattern = "[x_org_alertflex:source = 'Wazuh']"
        queries = translation.translate('alertflex', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ["SELECT a FROM Alert a WHERE a.alertSource = 'Wazuh'"]

        self.assertEqual(query, test_string)

    def test_source_node(self):
        stix_pattern = "[x_org_alertflex:source = 'Wazuh' AND x_org_alertflex:node = 'test01']"
        queries = translation.translate('alertflex', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ["SELECT a FROM Alert a WHERE a.nodeId = 'test01' AND a.alertSource = 'Wazuh'"]

        self.assertEqual(query, test_string)

    def test_source_timeinterval(self):
        stix_pattern = "[x_org_alertflex:source = 'Wazuh'] START t'2020-06-09T00:00:00Z' STOP t'2020-06-09T20:11:11Z'"
        queries = translation.translate('alertflex', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ["SELECT a FROM Alert a WHERE a.alertSource = 'Wazuh' AND a.timeCollr BETWEEN '2020-06-09 00:00:00' AND '2020-06-09 20:11:11'"]

        self.assertEqual(query, test_string)