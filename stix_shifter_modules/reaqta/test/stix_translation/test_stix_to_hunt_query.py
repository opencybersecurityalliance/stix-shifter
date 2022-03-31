from stix_shifter.stix_translation import stix_translation
import unittest

translation = stix_translation.StixTranslation()


class TestQueryTranslator(unittest.TestCase):

    def test_source_timeinterval(self):
        stix_pattern = "[ipv4-addr:value = '172.16.60.184'] START t'2022-03-24T20:21:35.519Z' STOP t'2022-03-24T20:21:35.619Z'"
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['$ip = "172.16.60.184" AND happenedAfter = "2022-03-24T20:21:35.519Z" AND happenedBefore = "2022-03-24T20:21:35.619Z"']

        self.assertEqual(query, test_string)

    def test_ipv4_addr(self):
        stix_pattern = "[ipv4-addr:value = '192.168.122.83' OR ipv4-addr:value = '192.168.122.84']"
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['$ip = "192.168.122.84" OR $ip = "192.168.122.83"']

        self.assertEqual(query, test_string)

    def test_network_traffic_src_port(self):
        stix_pattern = "[network-traffic:src_port = 443] START t'2022-03-24T20:21:35.519Z' STOP t'2022-03-24T20:21:35.619Z'"
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['eventdata.localPort = "443" AND happenedAfter = "2022-03-24T20:21:35.519Z" AND happenedBefore = "2022-03-24T20:21:35.619Z"']

        self.assertEqual(query, test_string)

    def test_file_name(self):
        stix_pattern = "[file:name = 'file_name']"
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['$filename = "file_name"']

        self.assertEqual(query, test_string)

    def test_file_md5(self):
        stix_pattern = "[file:hashes.'MD5' = '7d351ff6fea9e9dc100b7deb0e03fd35']"
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['$md5 = "7d351ff6fea9e9dc100b7deb0e03fd35"']

        self.assertEqual(query, test_string)

    def test_combined(self):
        stix_pattern = "([network-traffic:src_ref.value = '127.0.0.1' AND file:hashes.'MD5' = '23db6982caef9e9152f1a5b2589e6ca3' OR file:hashes.'SHA-256' " \
                "= 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'] AND [ipv4-addr:value = '10.0.0.1' OR ipv4-addr:value = '12.0.0.1' OR " \
                "ipv4-addr:value = '12.0.0.2'] AND [url:value = 'http://aaa.bbb' OR url:value = 'http://ccc.ddd']) START t'2022-03-30T18:14:52Z' STOP t'2022-03-30T18:19:52Z'"
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['($sha256 = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad" OR ($md5 = "23db6982caef9e9152f1a5b2589e6ca3" ' \
                'AND eventdata.localIp = "127.0.0.1")) AND ($ip = "12.0.0.2" OR ($ip = "12.0.0.1" OR $ip = "10.0.0.1")) AND eventdata.url = "http://ccc.ddd" ' \
                'OR eventdata.url = "http://aaa.bbb" AND happenedAfter = "2022-03-30T18:14:52Z" AND happenedBefore = "2022-03-30T18:19:52Z"']

        self.assertEqual(query, test_string)
