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

    def test_not_operator(self):
        stix_pattern = "[ipv4-addr:value NOT = '172.31.60.104' OR network-traffic:src_ref.value != '172.31.60.104']" \
                        "START t'2022-03-24T20:21:35.519Z' STOP t'2022-03-24T20:21:35.619Z'"
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['(eventdata.localIp != "172.31.60.104" OR NOT $ip = "172.31.60.104")' \
                        ' AND happenedAfter = "2022-03-24T20:21:35.519Z" AND happenedBefore = "2022-03-24T20:21:35.619Z"']

        self.assertEqual(query, test_string)

        
    def test_in_operator(self):
        stix_pattern = "[network-traffic:src_port IN (443, 446)] OR [ipv4-addr:value IN ('127.0.0.1', '127.0.0.2')] START t'2022-03-24T20:21:35.519Z' STOP t'2022-03-24T20:21:35.619Z'"
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['((eventdata.localPort = "443" OR eventdata.localPort = "446") OR ($ip = "127.0.0.1" OR $ip = "127.0.0.2")) AND happenedAfter = "2022-03-24T20:21:35.519Z" AND happenedBefore = "2022-03-24T20:21:35.619Z"']

        self.assertEqual(query, test_string)

        
    def test_match_operator(self):
        stix_pattern = "[file:name MATCHES 'serv']"
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['$filename = "serv"']

        self.assertEqual(query, test_string)

        
    def test_like_operator(self):
        stix_pattern = "[file:name LIKE 'svc']"
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['$filename = "svc"']

        self.assertEqual(query, test_string)

    def test_ipv4_addr(self):
        stix_pattern = "[ipv4-addr:value = '192.168.122.83' OR ipv4-addr:value = '192.168.122.84']"
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['$ip = "192.168.122.84" OR $ip = "192.168.122.83"']

        self.assertEqual(query, test_string)

    def test_ipv6_addr(self):
        stix_pattern = "[ipv6-addr:value = '2001:db8:3333:4444:5555:6666:7777:8888']"
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['$ip = "2001:db8:3333:4444:5555:6666:7777:8888"']

        self.assertEqual(query, test_string)

    def test_url(self):
        stix_pattern = "[url:value = 'https://example.com/example/path']"
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['eventdata.url = "https://example.com/example/path"']

        self.assertEqual(query, test_string)

    def test_file_name(self):
        stix_pattern = "[file:name = 'winword.exe']"
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['$filename = "winword.exe"']

        self.assertEqual(query, test_string)

    def test_file_sha1(self):
        stix_pattern = "[file:hashes.'SHA-1' = 'D56C753E0F8CE84BA3D3AB284628CF6594FDAA74']"
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['$sha1 = "D56C753E0F8CE84BA3D3AB284628CF6594FDAA74"']

        self.assertEqual(query, test_string)

    def test_file_sha256(self):
        stix_pattern = "[file:hashes.'SHA-256' = '47D1D8273710FD6F6A5995FAC1A0983FE0E8828C288E35E80450DDC5C4412DEF']"
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['$sha256 = "47D1D8273710FD6F6A5995FAC1A0983FE0E8828C288E35E80450DDC5C4412DEF"']

        self.assertEqual(query, test_string)

    def test_file_md5(self):
        stix_pattern = "[file:hashes.'MD5' = '7d351ff6fea9e9dc100b7deb0e03fd35']"
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['$md5 = "7d351ff6fea9e9dc100b7deb0e03fd35"']

        self.assertEqual(query, test_string)

    def test_path(self):
        stix_pattern = "[file:parent_directory_ref.path = 'c:\\\program files\\\microsoft office\\\\root\\\office16\\\winword.exe' OR directory:path = 'c:\\\program files\\\microsoft office\\\\root\\\office16\\\winword.exe']"
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['$path = "c:\\program files\\microsoft office\\root\\office16\\winword.exe" OR $path = "c:\\program files\\microsoft office\\root\\office16\\winword.exe"']

        self.assertEqual(query, test_string)

    def test_network_traffic_src_port(self):
        stix_pattern = "[network-traffic:src_port = 443] START t'2022-03-24T20:21:35.519Z' STOP t'2022-03-24T20:21:35.619Z'"
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['eventdata.localPort = "443" AND happenedAfter = "2022-03-24T20:21:35.519Z" AND happenedBefore = "2022-03-24T20:21:35.619Z"']

        self.assertEqual(query, test_string)
        
    def test_network_traffic_ip_port(self):
        stix_pattern = "[network-traffic:src_ref.value = '169.62.55.114' AND network-traffic:src_port = 3389 AND network-traffic:dst_ref.value = '143.244.41.203' AND network-traffic:dst_port = 60008]"
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['eventdata.remotePort = "60008" AND (eventdata.remoteIp = "143.244.41.203" AND (eventdata.localPort = "3389" AND eventdata.localIp = "169.62.55.114"))']

        self.assertEqual(query, test_string)


        

    def test_combined(self):
        stix_pattern = "([network-traffic:src_ref.value = '127.0.0.1' AND file:hashes.'MD5' != '23db6982caef9e9152f1a5b2589e6ca3' OR file:hashes.'SHA-256'= 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad']  " \
                "AND [ipv4-addr:value = '10.0.0.1' OR ipv4-addr:value = '12.0.0.1' OR ipv4-addr:value = '12.0.0.2'] " \
                "AND [url:value = 'http://aaa.bbb' OR url:value = 'http://ccc.ddd']) START t'2022-03-30T18:14:52Z' STOP t'2022-03-30T18:19:52Z'"

        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['(' \
                        '($sha256 = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad" OR ($md5 != "23db6982caef9e9152f1a5b2589e6ca3" AND eventdata.localIp = "127.0.0.1")) ' \
                        'AND ' \
                        '($ip = "12.0.0.2" OR ($ip = "12.0.0.1" OR $ip = "10.0.0.1")) ' \
                        'AND eventdata.url = "http://ccc.ddd" OR eventdata.url = "http://aaa.bbb"' \
                    ') ' \
                    'AND happenedAfter = "2022-03-30T18:14:52Z" AND happenedBefore = "2022-03-30T18:19:52Z"']

        self.assertEqual(query, test_string)
