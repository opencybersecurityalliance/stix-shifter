from stix_shifter.stix_translation import stix_translation
import re
import unittest
from stix2patterns.validator import run_validator as pattern_validator

translation = stix_translation.StixTranslation()

TEST_START_DATE1 = "2022-04-06T00:00:00.000Z"
TEST_STOP_DATE1 = "2022-04-06T00:05:00.000Z"
TEST_START_STOP_STIX_VALUE1 = "START t'{}' STOP t'{}'".format(TEST_START_DATE1, TEST_STOP_DATE1)
TEST_START_STOP_TRANSLATED1 = 'AND happenedAfter = "{}" AND happenedBefore = "{}"'.format(TEST_START_DATE1, TEST_STOP_DATE1)

TEST_START_DATE2 = "2022-04-07T00:00:00.000Z"
TEST_STOP_DATE2 = "2022-04-07T00:05:00.000Z"
TEST_START_STOP_STIX_VALUE2 = "START t'{}' STOP t'{}'".format(TEST_START_DATE2, TEST_STOP_DATE2)
TEST_START_STOP_TRANSLATED2 = 'AND happenedAfter = "{}" AND happenedBefore = "{}"'.format(TEST_START_DATE2, TEST_STOP_DATE2)

TEST_DATE_PATTERN = r"(\"\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z\")"


class TestQueryTranslator(unittest.TestCase):

    def assertPattern(self, stix_pattern):
        errors = pattern_validator(stix_pattern, stix_version='2.1')

        # print('\nPattern:', stix_pattern)
        # print('Errors', errors)

        assert len(errors) == 0


    def assertQuery(self, query, test_string, stix_pattern):
        self.assertPattern(stix_pattern)

        # print('\nTranslated:', query[0])
        # print('Expected  :', test_string[0])

        self.assertEqual(query, test_string)

    ####################################
    ## Operators and qualifier checks ##
    ####################################

    def test_timeinterval(self):
        stix_pattern = "[ipv4-addr:value = '172.16.60.184'] {}".format(TEST_START_STOP_STIX_VALUE1)
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['(($ip = "172.16.60.184" OR login.ip = "172.16.60.184")) {}'.format(TEST_START_STOP_TRANSLATED1)]

        self.assertQuery(query, test_string, stix_pattern)

    def test_no_timeinterval(self):
        '''
        The missing qualifier for thw observation expressio should be added using default time interval
        '''
        stix_pattern = "[ipv4-addr:value = '192.168.1.2']"
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries'][0]
        
        assert '(($ip = "192.168.1.2" OR login.ip = "192.168.1.2")) AND happenedAfter = "' in query

        found = re.findall(TEST_DATE_PATTERN, query)
        assert len(found) == 2

    def test_timeinterval_without_milliseconds(self):
        test_start_date = "2022-04-06T00:00:00Z"
        test_stop_date = "2022-04-06T00:05:00Z"
        translated_start_date = "2022-04-06T00:00:00.000Z"
        translated_stop_date = "2022-04-06T00:05:00.000Z"
        test_start_stop_value = "START t'{}' STOP t'{}'".format(test_start_date, test_stop_date)
        transalted_start_stop_value = 'AND happenedAfter = "{}" AND happenedBefore = "{}"'.format(translated_start_date, translated_stop_date)

        stix_pattern = "[ipv4-addr:value = '172.16.60.184'] {}".format(test_start_stop_value)
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['(($ip = "172.16.60.184" OR login.ip = "172.16.60.184")) {}'.format(transalted_start_stop_value)]

        self.assertQuery(query, test_string, stix_pattern)

    def test_one_observation_expression_with_timeinterval(self):
        stix_pattern = "[ipv4-addr:value = '192.168.1.2' OR url:value = 'www.example.com'] {}".format(TEST_START_STOP_STIX_VALUE1)
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['(eventdata.url = "www.example.com" OR ($ip = "192.168.1.2" OR login.ip = "192.168.1.2")) {}'.format(TEST_START_STOP_TRANSLATED1, TEST_START_STOP_TRANSLATED1)]
        
        self.assertQuery(query, test_string, stix_pattern)

    def test_two_observation_expressions_with_two_timeintervals(self):
        stix_pattern = "[ipv4-addr:value = '192.168.1.2'] {} OR [url:value = 'www.example.com'] {}".format(TEST_START_STOP_STIX_VALUE1, TEST_START_STOP_STIX_VALUE2)
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['(($ip = "192.168.1.2" OR login.ip = "192.168.1.2")) {} OR (eventdata.url = "www.example.com") {}'.format(TEST_START_STOP_TRANSLATED1, TEST_START_STOP_TRANSLATED2)]
        
        self.assertQuery(query, test_string, stix_pattern)

    def test_two_observation_expressions_with_one_timeinterval(self):
        '''
        Only one qualifier is present for 2 observation expressions.
        The missing qualifier should be added using default time interval
        '''
        stix_pattern = "[ipv4-addr:value = '192.168.1.2'] OR [url:value = 'www.example.com'] {}".format(TEST_START_STOP_STIX_VALUE1)
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['(($ip = "192.168.1.2") {}) OR ((eventdata.url = "www.example.com") {})'.format(TEST_START_STOP_TRANSLATED1, TEST_START_STOP_TRANSLATED1)]
        self.assertNotEqual(query, test_string)

        assert '(($ip = "192.168.1.2" OR login.ip = "192.168.1.2")) AND happenedAfter = "' in query[0]
        assert 'OR (eventdata.url = "www.example.com") AND happenedAfter = "' in query[0]

        found = re.findall(TEST_DATE_PATTERN, query[0])
        assert len(found) == 4
        

    def test_combined_observation_expressions_with_timeintervals(self):
        stix_pattern = "([ipv4-addr:value = '192.168.1.2'] {} OR [url:value = 'www.example.com']) {}".format(TEST_START_STOP_STIX_VALUE1, TEST_START_STOP_STIX_VALUE2)
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['(($ip = "192.168.1.2" OR login.ip = "192.168.1.2")) {} OR (eventdata.url = "www.example.com") {}'.format(TEST_START_STOP_TRANSLATED1, TEST_START_STOP_TRANSLATED2)]
        
        self.assertQuery(query, test_string, stix_pattern)


    def test_not_operator(self):
        stix_pattern = "[ipv4-addr:value NOT = '172.31.60.104' OR network-traffic:src_ref.value != '172.31.60.104']" \
                        "START t'2022-03-24T20:21:35.519Z' STOP t'2022-03-24T20:21:35.619Z'"
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['($ip != "172.31.60.104" OR (NOT $ip = "172.31.60.104" OR NOT login.ip = "172.31.60.104"))' \
                        ' AND happenedAfter = "2022-03-24T20:21:35.519Z" AND happenedBefore = "2022-03-24T20:21:35.619Z"']

        self.assertQuery(query, test_string, stix_pattern)

        
    def test_in_operator(self):
        stix_pattern = "[network-traffic:src_port IN (443, 446)] {} OR [ipv4-addr:value IN ('127.0.0.1', '127.0.0.2')] {}".format(TEST_START_STOP_STIX_VALUE1, TEST_START_STOP_STIX_VALUE2)
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['(eventdata.localPort = "443" OR eventdata.localPort = "446") {} OR (($ip = "127.0.0.1" OR login.ip = "127.0.0.1" OR $ip = "127.0.0.2" OR login.ip = "127.0.0.2")) {}'.format(TEST_START_STOP_TRANSLATED1, TEST_START_STOP_TRANSLATED2)]

        self.assertQuery(query, test_string, stix_pattern)

        
    def test_match_operator(self):
        stix_pattern = "[file:name MATCHES 'serv'] {}".format(TEST_START_STOP_STIX_VALUE1)
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['((consumer.script.filename = "serv" OR fsName = "serv")) {}'.format(TEST_START_STOP_TRANSLATED1)]

        self.assertQuery(query, test_string, stix_pattern)

        
    def test_like_operator(self):
        stix_pattern = "[file:name LIKE 'svc'] {}".format(TEST_START_STOP_STIX_VALUE1)
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['((consumer.script.filename = "svc" OR fsName = "svc")) {}'.format(TEST_START_STOP_TRANSLATED1)]

        self.assertQuery(query, test_string, stix_pattern)

    def test_combined(self):
        stix_pattern = "([network-traffic:src_ref.value = '127.0.0.1' AND file:hashes.MD5 != '23db6982caef9e9152f1a5b2589e6ca3' OR file:hashes.'SHA-256' = 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad']  " \
                "AND [ipv4-addr:value = '10.0.0.1' OR ipv4-addr:value = '12.0.0.1' OR ipv4-addr:value = '12.0.0.2'] " \
                "AND [url:value = 'http://aaa.bbb' OR url:value = 'http://ccc.ddd']) {}".format(TEST_START_STOP_STIX_VALUE1)

        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['($sha256 = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad" OR $md5 != "23db6982caef9e9152f1a5b2589e6ca3" AND $ip = "127.0.0.1") {} ' \
                        'AND (($ip = "12.0.0.2" OR login.ip = "12.0.0.2") OR ($ip = "12.0.0.1" OR login.ip = "12.0.0.1") OR ($ip = "10.0.0.1" OR login.ip = "10.0.0.1")) {} ' \
                        'AND (eventdata.url = "http://ccc.ddd" OR eventdata.url = "http://aaa.bbb") {}'
                        .format(TEST_START_STOP_TRANSLATED1, TEST_START_STOP_TRANSLATED1, TEST_START_STOP_TRANSLATED1)]

        self.assertQuery(query, test_string, stix_pattern)

    ########################
    ## stix objects check ##
    ########################

    def test_ipv4_addr(self):
        stix_pattern = "[ipv4-addr:value = '192.168.122.83' OR ipv4-addr:value = '192.168.122.84'] {}".format(TEST_START_STOP_STIX_VALUE1)
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['(($ip = "192.168.122.84" OR login.ip = "192.168.122.84") OR ($ip = "192.168.122.83" OR login.ip = "192.168.122.83")) {}'.format(TEST_START_STOP_TRANSLATED1)]

        self.assertQuery(query, test_string, stix_pattern)

    def test_ipv6_addr(self):
        stix_pattern = "[ipv6-addr:value = '2001:db8:3333:4444:5555:6666:7777:8888'] {}".format(TEST_START_STOP_STIX_VALUE1)
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['($ip = "2001:db8:3333:4444:5555:6666:7777:8888") {}'.format(TEST_START_STOP_TRANSLATED1)]

        self.assertQuery(query, test_string, stix_pattern)

    def test_url(self):
        stix_pattern = "[url:value = 'https://example.com/example/path'] {}".format(TEST_START_STOP_STIX_VALUE1)
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['(eventdata.url = "https://example.com/example/path") {}'.format(TEST_START_STOP_TRANSLATED1)]

        self.assertQuery(query, test_string, stix_pattern)

    def test_file_name(self):
        stix_pattern = "[file:name = 'winword.exe'] {}".format(TEST_START_STOP_STIX_VALUE1)
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['((consumer.script.filename = "winword.exe" OR fsName = "winword.exe")) {}'.format(TEST_START_STOP_TRANSLATED1)]

        self.assertQuery(query, test_string, stix_pattern)

    def test_file_sha1(self):
        stix_pattern = "[file:hashes.'SHA-1' = 'D56C753E0F8CE84BA3D3AB284628CF6594FDAA74'] {}".format(TEST_START_STOP_STIX_VALUE1)
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['($sha1 = "D56C753E0F8CE84BA3D3AB284628CF6594FDAA74") {}'.format(TEST_START_STOP_TRANSLATED1)]

        self.assertQuery(query, test_string, stix_pattern)

    def test_file_sha256(self):
        stix_pattern = "[file:hashes.'SHA-256' = '47D1D8273710FD6F6A5995FAC1A0983FE0E8828C288E35E80450DDC5C4412DEF'] {}".format(TEST_START_STOP_STIX_VALUE1)
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['($sha256 = "47D1D8273710FD6F6A5995FAC1A0983FE0E8828C288E35E80450DDC5C4412DEF") {}'.format(TEST_START_STOP_TRANSLATED1)]

        self.assertQuery(query, test_string, stix_pattern)

    def test_file_md5(self):
        stix_pattern = "[file:hashes.MD5 = '7d351ff6fea9e9dc100b7deb0e03fd35'] {}".format(TEST_START_STOP_STIX_VALUE1)
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['($md5 = "7d351ff6fea9e9dc100b7deb0e03fd35") {}'.format(TEST_START_STOP_TRANSLATED1)]

        self.assertQuery(query, test_string, stix_pattern)

    def test_directory_file_path(self):
        stix_pattern = "[file:parent_directory_ref.path = 'c:\\\\program files\\\\microsoft office\\\\root\\\\office16\\\\winword.exe' OR directory:path = 'c:\\\\program files\\\\microsoft office\\\\root\\\\office16\\\\winword.exe'] {}".format(TEST_START_STOP_STIX_VALUE1)
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        path = "c:\\program files\\microsoft office\\root\\office16\\winword.exe"

        test_string = ['((__etwHomePath = "{}" OR accessor.path = "{}" OR consumer.workingDirectory = "{}" OR $path = "{}") OR $path = "{}") {}'.format(path, path, path, path, path, TEST_START_STOP_TRANSLATED1)]

        self.assertQuery(query, test_string, stix_pattern)

    def test_network_traffic_src_port(self):
        stix_pattern = "[network-traffic:src_port = 443] {}".format(TEST_START_STOP_STIX_VALUE1)
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['(eventdata.localPort = "443") {}'.format(TEST_START_STOP_TRANSLATED1)]

        self.assertQuery(query, test_string, stix_pattern)
        
    def test_network_traffic_ip_port(self):
        stix_pattern = "[network-traffic:src_ref.value = '169.62.55.114' AND network-traffic:src_port = 3389 AND network-traffic:dst_ref.value = '143.244.41.203' AND network-traffic:dst_port = 60008] {}".format(TEST_START_STOP_STIX_VALUE1)
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['(eventdata.remotePort = "60008" AND $ip = "143.244.41.203" AND eventdata.localPort = "3389" AND $ip = "169.62.55.114") {}'.format(TEST_START_STOP_TRANSLATED1)]

        self.assertQuery(query, test_string, stix_pattern)

    def test_file_size_greater_less_or_equal_than(self):
        stix_pattern = "[file:size <= '10' AND file:size >= '50'] {}".format(TEST_START_STOP_STIX_VALUE1)
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['(eventdata.size.gte = 50 AND eventdata.size.lte = 10) {}'.format(TEST_START_STOP_TRANSLATED1)]

        self.assertQuery(query, test_string, stix_pattern)

    ###############################
    ## custom stix objects check ##
    ###############################


    def test_x_ibm_finding(self):
        stix_pattern = "[x-ibm-finding:dst_ip_ref.value = '169.62.55.114' AND x-ibm-finding:finding_type = '8' AND x-ibm-finding:src_ip_ref.value = '143.244.41.203'] {}".format(TEST_START_STOP_STIX_VALUE1)
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['($ip = "143.244.41.203" AND antimalware.threatType = "8" AND $ip = "169.62.55.114") {}'.format(TEST_START_STOP_TRANSLATED1)]

        self.assertQuery(query, test_string, stix_pattern)

    def test_oca_asset(self):
        stix_pattern = "[x-oca-asset:ip_refs[*].value = '143.244.41.203'] {}".format(TEST_START_STOP_STIX_VALUE1)
        queries = translation.translate('reaqta', 'query', '{}', stix_pattern)
        query = queries['queries']

        test_string = ['($ip = "143.244.41.203") {}'.format(TEST_START_STOP_TRANSLATED1)]

        self.assertQuery(query, test_string, stix_pattern)



