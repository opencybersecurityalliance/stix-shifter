from stix_shifter.stix_translation import stix_translation
import unittest
import re

translation = stix_translation.StixTranslation()


def _remove_timestamp_from_query(expected_query):
    pattern1 = r"@fields.epochdate\s:>\d{0,10}.\d{0,3}\s*AND\s*@fields.epochdate\s:<\d{0,10}.\d{0,3}"
    pattern2 = r"\,\s*\'timeframe\'\:\s*\'custom\'\,\s*\'time\'([^>]*)?\'\}"
    combined_pat = r'|'.join((pattern1, pattern2))
    if isinstance(expected_query, list):
        return [re.sub(combined_pat, '', str(query)) for query in expected_query]
    elif isinstance(expected_query, str):
        return re.sub(combined_pat, '', expected_query)


class TestqueryTranslator(unittest.TestCase):
    """
    class to perform unit test case Darktrace translate query
    """
    if __name__ == "__main__":
        unittest.main()

    def _test_query_assertions(self, actual_query, expected_query):
        """
        to assert the each query in the list against expected result
        """
        self.assertIsInstance(expected_query, list)
        self.assertIsInstance(actual_query, dict)
        self.assertIsInstance(actual_query['queries'], list)
        for index, each_query in enumerate(actual_query.get('queries'), start=0):
            self.assertEqual(each_query, expected_query[index])

    def test_mac_address_query(self):
        stix_pattern = "[mac-addr:value = '12:2f:23:46:35:5b']"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        actual_query['queries'] = _remove_timestamp_from_query(actual_query['queries'])
        expected_query = [{
            "search": "(@fields.mac:\"12:2f:23:46:35:5b\" AND (@fields.epochdate :>1651064608.076 AND "
                      "@fields.epochdate :<1651064908.076))",
            "fields": [],
            "timeframe": "custom",
            "time": {
                "from": "2022-04-27T13:03:28.076000Z",
                "to": "2022-04-27T13:08:28.076000Z"
            },
            "size": 10000
        }]
        expected_query = _remove_timestamp_from_query(expected_query)
        self._test_query_assertions(actual_query, expected_query)

    def test_file_query(self):
        stix_pattern = "[file:name = 'some_file.exe']"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        actual_query['queries'] = _remove_timestamp_from_query(actual_query['queries'])
        expected_query = [{
            "search": "(@fields.filename:\"some_file.exe\" AND (@fields.epochdate :>1649152970.31 AND"
                      " @fields.epochdate :<1649153270.31))",
            "fields": [],
            "timeframe": "custom",
            "time": {
                "from": "2022-04-05T10:02:50.310000Z",
                "to": "2022-04-05T10:07:50.310000Z"
            },
            "size": 10000
        }]
        expected_query = _remove_timestamp_from_query(expected_query)
        self._test_query_assertions(actual_query, expected_query)

    def test_user_account_query(self):
        stix_pattern = "[user-account:account_login = 'anonymous']"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        actual_query['queries'] = _remove_timestamp_from_query(actual_query['queries'])
        expected_query = [{
            "search": "((@fields.user:\"anonymous\" OR @fields.username:\"anonymous\") AND "
                      "(@fields.epochdate :>1649240843.165 AND @fields.epochdate :<1649241143.165))",
            "fields": [],
            "timeframe": "custom",
            "time": {
                "from": "2022-04-06T10:27:23.165000Z",
                "to": "2022-04-06T10:32:23.165000Z"
            },
            "size": 10000
        }]
        expected_query = _remove_timestamp_from_query(expected_query)
        self._test_query_assertions(actual_query, expected_query)

    def test_network_query_not_equals(self):
        stix_pattern = "[network-traffic:dst_port!=3389]"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        actual_query['queries'] = _remove_timestamp_from_query(actual_query['queries'])
        expected_query = [{
            "search": "(((@fields.dest_port:* AND NOT @fields.dest_port:3389) OR "
                      "(@fields.dst_p:* AND NOT @fields.dst_p:3389)) AND "
                      "(@fields.epochdate :>1649310118.117 AND @fields.epochdate :<1649310418.117))",
            "fields": [],
            "timeframe": "custom",
            "time": {
                "from": "2022-04-07T05:41:58.117000Z",
                "to": "2022-04-07T05:46:58.117000Z"
            },
            "size": 10000
        }]
        expected_query = _remove_timestamp_from_query(expected_query)
        self._test_query_assertions(actual_query, expected_query)

    def test_network_query_greater_than(self):
        stix_pattern = "[network-traffic:dst_port>3389]"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        actual_query['queries'] = _remove_timestamp_from_query(actual_query['queries'])
        expected_query = [{
            "search": "((@fields.dest_port:>3389 OR @fields.dst_p:>3389) AND "
                      "(@fields.epochdate :>1646092800.0 AND @fields.epochdate :<1648810800.003))",
            "fields": [],
            "timeframe": "custom",
            "time": {
                "from": "2022-03-01T00:00:00.000000Z",
                "to": "2022-04-01T11:00:00.003000Z"
            },
            "size": 10000
        }]
        expected_query = _remove_timestamp_from_query(expected_query)
        self._test_query_assertions(actual_query, expected_query)

    def test_network_query_less_than(self):
        stix_pattern = "[network-traffic:src_port<62298]"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        actual_query['queries'] = _remove_timestamp_from_query(actual_query['queries'])
        expected_query = [{
            "search": "((@fields.source_port:<62298 OR @fields.src_p:<62298) "
                      "AND (@fields.epochdate :>1646092800.0 AND @fields.epochdate :<1648810800.003))",
            "fields": [],
            "timeframe": "custom",
            "time": {
                "from": "2022-03-01T00:00:00.000000Z",
                "to": "2022-04-01T11:00:00.003000Z"
            },
            "size": 10000
        }]
        expected_query = _remove_timestamp_from_query(expected_query)
        self._test_query_assertions(actual_query, expected_query)

    def test_network_query_grater_than_or_equal(self):
        stix_pattern = "[network-traffic:src_port >= 58771]"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        actual_query['queries'] = _remove_timestamp_from_query(actual_query['queries'])
        expected_query = [{
            "search": "((@fields.source_port:>58770 OR @fields.src_p:>58770) "
                      "AND (@fields.epochdate :>1646092800.0 AND @fields.epochdate :<1648810800.003))",
            "fields": [],
            "timeframe": "custom",
            "time": {
                "from": "2022-03-01T00:00:00.000000Z",
                "to": "2022-04-01T11:00:00.003000Z"
            },
            "size": 10000
        }]
        expected_query = _remove_timestamp_from_query(expected_query)
        self._test_query_assertions(actual_query, expected_query)

    def test_network_query_less_than_or_equal(self):
        stix_pattern = "[network-traffic:src_port <= 58771]"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        actual_query['queries'] = _remove_timestamp_from_query(actual_query['queries'])
        expected_query = [{
            "search": "((@fields.source_port:<58772 OR @fields.src_p:<58772) "
                      "AND (@fields.epochdate :>1646092800.0 AND @fields.epochdate :<1648810800.003))",
            "fields": [],
            "timeframe": "custom",
            "time": {
                "from": "2022-03-01T00:00:00.000000Z",
                "to": "2022-04-01T11:00:00.003000Z"
            },
            "size": 10000
        }]
        expected_query = _remove_timestamp_from_query(expected_query)
        self._test_query_assertions(actual_query, expected_query)

    def test_network_query_less_than_or_equal_str(self):
        stix_pattern = "[network-traffic:src_port <= '58771']"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        actual_query['queries'] = _remove_timestamp_from_query(actual_query['queries'])
        expected_query = [{
            "search": "((@fields.source_port:<58772 OR @fields.src_p:<58772) "
                      "AND (@fields.epochdate :>1646092800.0 AND @fields.epochdate :<1648810800.003))",
            "fields": [],
            "timeframe": "custom",
            "time": {
                "from": "2022-03-01T00:00:00.000000Z",
                "to": "2022-04-01T11:00:00.003000Z"
            },
            "size": 10000
        }]
        expected_query = _remove_timestamp_from_query(expected_query)
        self._test_query_assertions(actual_query, expected_query)

    def test_network_query_grater_than_or_equal_str(self):
        stix_pattern = "[network-traffic:src_port >= '58771']"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        actual_query['queries'] = _remove_timestamp_from_query(actual_query['queries'])
        expected_query = [{
            "search": "((@fields.source_port:>58770 OR @fields.src_p:>58770) AND "
                      "(@fields.epochdate :>1646092800.0 AND @fields.epochdate :<1648810800.003))",
            "fields": [],
            "timeframe": "custom",
            "time": {
                "from": "2022-03-01T00:00:00.000000Z",
                "to": "2022-04-01T11:00:00.003000Z"
            },
            "size": 10000
        }]
        expected_query = _remove_timestamp_from_query(expected_query)
        self._test_query_assertions(actual_query, expected_query)

    def test_network_query_like(self):
        stix_pattern = "[network-traffic:protocols[*] LIKE 'tcp']"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        actual_query['queries'] = _remove_timestamp_from_query(actual_query['queries'])
        expected_query = [{
            "search": "((@fields.proto:*tcp* OR @fields.protocol:*tcp*) AND "
                      "(@fields.epochdate :>1646092800.0 AND @fields.epochdate :<1648810800.003))",
            "fields": [],
            "timeframe": "custom",
            "time": {
                "from": "2022-03-01T00:00:00.000000Z",
                "to": "2022-04-01T11:00:00.003000Z"
            },
            "size": 10000
        }]
        expected_query = _remove_timestamp_from_query(expected_query)
        self._test_query_assertions(actual_query, expected_query)

    def test_software_match(self):
        stix_pattern = "[software:name MATCHES 'Windows']"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        actual_query['queries'] = _remove_timestamp_from_query(actual_query['queries'])
        expected_query = [{
            "search": "(@fields.name:/Windows/ AND (@fields.epochdate :>1646092800.0 AND "
                      "@fields.epochdate :<1648810800.003))",
            "fields": [],
            "timeframe": "custom",
            "time": {
                "from": "2022-03-01T00:00:00.000000Z",
                "to": "2022-04-01T11:00:00.003000Z"
            },
            "size": 10000
        }]
        expected_query = _remove_timestamp_from_query(expected_query)
        self._test_query_assertions(actual_query, expected_query)

    def test_network_traffic_in(self):
        stix_pattern = "[network-traffic:protocols[*] IN ('tcp','dns')]"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        actual_query['queries'] = _remove_timestamp_from_query(actual_query['queries'])
        expected_query = [{
            "search": "((@fields.proto:(\"tcp\" OR \"dns\") OR @fields.protocol:(\"tcp\" OR \"dns\"))"
                      " AND (@fields.epochdate :>1646092800.0 AND @fields.epochdate :<1648810800.003))",
            "fields": [],
            "timeframe": "custom",
            "time": {
                "from": "2022-03-01T00:00:00.000000Z",
                "to": "2022-04-01T11:00:00.003000Z"
            },
            "size": 10000
        }]
        expected_query = _remove_timestamp_from_query(expected_query)
        self._test_query_assertions(actual_query, expected_query)

    def test_network_traffic_port_query(self):
        stix_pattern = "[network-traffic:src_port = 62298 OR network-traffic:dst_port = 3389]"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        actual_query['queries'] = _remove_timestamp_from_query(actual_query['queries'])
        expected_query = [{
            "search": "(((@fields.dest_port:3389 OR @fields.dst_p:3389) OR (@fields.source_port:62298 OR "
                      "@fields.src_p:62298)) AND (@fields.epochdate :>1646092800.0 AND "
                      "@fields.epochdate :<1648724400.003))",
            "fields": [],
            "timeframe": "custom",
            "time": {
                "from": "2022-03-01T00:00:00.000000Z",
                "to": "2022-03-31T11:00:00.003000Z"
            },
            "size": 10000
        }]
        expected_query = _remove_timestamp_from_query(expected_query)
        self._test_query_assertions(actual_query, expected_query)

    def test_x_darktrace_http_query_equals(self):
        stix_pattern = "[network-traffic:extensions.'http-request-ext'.request_method='GET']"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        actual_query['queries'] = _remove_timestamp_from_query(actual_query['queries'])
        expected_query = [{
            "search": "(@fields.method:\"GET\" AND (@fields.epochdate :>1651065067.574 AND "
                      "@fields.epochdate :<1651065367.574))",
            "fields": [],
            "timeframe": "custom",
            "time": {
                "from": "2022-04-27T13:11:07.574000Z",
                "to": "2022-04-27T13:16:07.574000Z"
            },
            "size": 10000
        }]
        expected_query = _remove_timestamp_from_query(expected_query)
        self._test_query_assertions(actual_query, expected_query)

    def test_x_http_or_x509_query(self):
        stix_pattern = "[network-traffic:extensions.'http-request-ext'.request_method='GET' AND " \
                       "x509-certificate:serial_number='76FDB38B8D5AA88844250EFE0EA89026']"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        actual_query['queries'] = _remove_timestamp_from_query(actual_query['queries'])
        expected_query = [{
            "search": "((@fields.certificate_serial:\"76FDB38B8D5AA88844250EFE0EA89026\" AND "
                      "@fields.method:\"GET\") AND (@fields.epochdate :>1651065261.707 AND "
                      "@fields.epochdate :<1651065561.707))",
            "fields": [],
            "timeframe": "custom",
            "time": {
                "from": "2022-04-27T13:14:21.707000Z",
                "to": "2022-04-27T13:19:21.707000Z"
            },
            "size": 10000
        }]
        expected_query = _remove_timestamp_from_query(expected_query)
        self._test_query_assertions(actual_query, expected_query)

    def test_network_traffic_port_and_query(self):
        stix_pattern = "[network-traffic:src_port > 53331 AND network-traffic:dst_port < 3380]"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        actual_query['queries'] = _remove_timestamp_from_query(actual_query['queries'])
        expected_query = [{
            "search": "(((@fields.dest_port:<3380 OR @fields.dst_p:<3380) AND "
                      "(@fields.source_port:>53331 OR @fields.src_p:>53331)) AND "
                      "(@fields.epochdate :>1646092800.0 AND @fields.epochdate :<1648724400.003))",
            "fields": [],
            "timeframe": "custom",
            "time": {
                "from": "2022-03-01T00:00:00.000000Z",
                "to": "2022-03-31T11:00:00.003000Z"
            },
            "size": 10000
        }]
        expected_query = _remove_timestamp_from_query(expected_query)
        self._test_query_assertions(actual_query, expected_query)

    def test_equal_or_operator(self):
        stix_pattern = "[software:name='Windows'] OR [file:created = '1648122134.845304']"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        actual_query['queries'] = _remove_timestamp_from_query(actual_query['queries'])
        expected_query = [{
            "search": "((@fields.name:\"Windows\" OR @fields.epochdate:1648122134.845304) "
                      "AND (@fields.epochdate :>1649152875.85 AND @fields.epochdate :<1649153175.85))",
            "fields": [],
            "timeframe": "custom",
            "time": {
                "from": "2022-04-05T10:01:15.850000Z",
                "to": "2022-04-05T10:06:15.850000Z"
            },
            "size": 10000
        }]
        expected_query = _remove_timestamp_from_query(expected_query)
        self._test_query_assertions(actual_query, expected_query)

    def test_multi_list_or_operator(self):
        stix_pattern = "[user-account:account_login = 'anonymous'] OR " \
                       "([file:name = 'input.csv'] OR [software:version='3.2.1']) " \
                       "START t'2022-03-01T00:00:00.000Z' STOP t'2022-03-31T11:00:00.003Z'"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        actual_query['queries'] = _remove_timestamp_from_query(actual_query['queries'])
        expected_query = [{
            "search": "((@fields.user:\"anonymous\" OR @fields.username:\"anonymous\") OR "
                      "((@fields.filename:\"input.csv\" OR @fields.version:\"3.2.1\") AND "
                      "(@fields.epochdate :>1646092800.0 AND @fields.epochdate :<1648724400.003)))",
            "fields": [],
            "timeframe": "custom",
            "time": {
                "from": "2022-03-01T00:00:00.000000Z",
                "to": "2022-03-31T11:00:00.003000Z"
            },
            "size": 10000
        }]
        expected_query = _remove_timestamp_from_query(expected_query)
        self._test_query_assertions(actual_query, expected_query)

    def test_x_oca_asset(self):
        stix_pattern = "[x-oca-asset:hostname = '169.254.169.254']"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        actual_query['queries'] = _remove_timestamp_from_query(actual_query['queries'])
        expected_query = [{
            "search": "(@fields.host:\"169.254.169.254\" AND (@fields.epochdate :>1649154023.919 "
                      "AND @fields.epochdate :<1649154323.919))",
            "fields": [],
            "timeframe": "custom",
            "time": {
                "from": "2022-04-05T10:20:23.919000Z",
                "to": "2022-04-05T10:25:23.919000Z"
            },
            "size": 10000
        }]
        expected_query = _remove_timestamp_from_query(expected_query)
        self._test_query_assertions(actual_query, expected_query)

    def test_software_match_cap_error(self):
        stix_pattern = "[software:name MATCHES 'Windows^']"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        assert actual_query['success'] is False

    def test_mac_match_error(self):
        stix_pattern = "[mac-addr:value MATCHES '12:2f:23:46:35:5b']"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        assert actual_query['success'] is False

    def test_software_match_dollar_error(self):
        stix_pattern = "[software:name MATCHES '$Windows']"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        assert actual_query['success'] is False

    def test_x509_like(self):
        stix_pattern = "[x509-certificate:version LIKE '12']"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        assert actual_query['success'] is False

    def test_mac_query_like(self):
        stix_pattern = "[mac-addr:value LIKE '12:2f:23:46:35:5b']"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        assert actual_query['success'] is False

    def test_network_query_less_than_or_equal_string_error(self):
        stix_pattern = "[network-traffic:src_port <= 'five']"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        assert actual_query['success'] is False

    def test_ipv4_query_time_error(self):
        stix_pattern = "[ipv4-addr:value = '172.31.81.98'] START t'2021-10-09T11:.0Z' STOP t'2021-10:00.003Z'"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern, {'validate_pattern': 'true'})
        assert actual_query['success'] is False
        assert actual_query['code'] == 'invalid_parameter'

    def test_ipv4_query(self):
        stix_pattern = "[ipv4-addr:value = '172.31.81.98']"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        actual_query['queries'] = _remove_timestamp_from_query(actual_query['queries'])
        expected_query = [{
            "search": "((@fields.source_ip:\"172.31.81.98\" OR @fields.dest_ip:\"172.31.81.98\" OR "
                      "@fields.src:\"172.31.81.98\" OR @fields.dst:\"172.31.81.98\" OR "
                      "@fields.ip:\"172.31.81.98\" OR @fields.subnet_mask:\"172.31.81.98\" OR "
                      "@fields.released_ip:\"172.31.81.98\" OR @fields.requested_ip:\"172.31.81.98\" OR "
                      "@fields.assigned_ip:\"172.31.81.98\") AND (@fields.epochdate :>1650946804.243 "
                      "AND @fields.epochdate :<1650947104.243))",
            "fields": [],
            "timeframe": "custom",
            "time": {
                "from": "2022-04-26T04:20:04.243000Z",
                "to": "2022-04-26T04:25:04.243000Z"
            },
            "size": 10000
        }]
        expected_query = _remove_timestamp_from_query(expected_query)
        self._test_query_assertions(actual_query, expected_query)

    def test_email_query(self):
        stix_pattern = "[email-addr:value = 'shahtanveer@gmail.com'] " \
                       "START t'2022-03-01T00:00:00.000Z' STOP t'2022-04-05T11:00:00.003Z'"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        actual_query['queries'] = _remove_timestamp_from_query(actual_query['queries'])
        expected_query = [{
            "search": "((@fields.mailfrom:\"shahtanveer@gmail.com\" OR @fields.rcptto:\"shahtanveer@gmail.com\" OR "
                      "@fields.from:\"shahtanveer@gmail.com\" OR @fields.to:\"shahtanveer@gmail.com\" OR "
                      "@fields.cc:\"shahtanveer@gmail.com\") AND (@fields.epochdate :>1646092800.0 AND "
                      "@fields.epochdate :<1649156400.003))",
            "fields": [],
            "timeframe": "custom",
            "time": {
                "from": "2022-03-01T00:00:00.000000Z",
                "to": "2022-04-05T11:00:00.003000Z"
            },
            "size": 10000
        }]
        expected_query = _remove_timestamp_from_query(expected_query)
        self._test_query_assertions(actual_query, expected_query)

    def test_network_query_packets(self):
        stix_pattern = "[network-traffic:src_packets = 10]"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        actual_query['queries'] = _remove_timestamp_from_query(actual_query['queries'])
        expected_query = [{
            "search": "((@fields.pkts_recv:10 OR @fields.orig_pkts:10) AND "
                      "(@fields.epochdate :>1650947018.067 AND @fields.epochdate :<1650947318.067))",
            "fields": [],
            "timeframe": "custom",
            "time": {
                "from": "2022-04-26T04:23:38.067000Z",
                "to": "2022-04-26T04:28:38.067000Z"
            },
            "size": 10000
        }]
        expected_query = _remove_timestamp_from_query(expected_query)
        self._test_query_assertions(actual_query, expected_query)

    def test_ipv4_query_time(self):
        stix_pattern = "[ipv4-addr:value = '172.31.81.98'] START t'2022-03-01T00:00:00.000Z'" \
                       " STOP t'2022-03-31T11:00:00.003Z'"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        actual_query['queries'] = _remove_timestamp_from_query(actual_query['queries'])
        expected_query = [{
            "search": "((@fields.source_ip:\"172.31.81.98\" OR @fields.dest_ip:\"172.31.81.98\" OR "
                      "@fields.src:\"172.31.81.98\" OR @fields.dst:\"172.31.81.98\" OR @fields.ip:\"172.31.81.98\""
                      " OR @fields.subnet_mask:\"172.31.81.98\" OR @fields.released_ip:\"172.31.81.98\""
                      " OR @fields.requested_ip:\"172.31.81.98\" OR @fields.assigned_ip:\"172.31.81.98\")"
                      " AND (@fields.epochdate :>1646092800.0 AND @fields.epochdate :<1648724400.003))",
            "fields": [],
            "timeframe": "custom",
            "time": {
                "from": "2022-03-01T00:00:00.000000Z",
                "to": "2022-03-31T11:00:00.003000Z"
            },
            "size": 10000
        }]
        expected_query = _remove_timestamp_from_query(expected_query)
        self._test_query_assertions(actual_query, expected_query)

    def test_ipv4_query_or(self):
        stix_pattern = "[ipv4-addr:value = '172.31.81.98' OR network-traffic:src_port > 62298]"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        actual_query['queries'] = _remove_timestamp_from_query(actual_query['queries'])
        expected_query = [{
            "search": "(((@fields.source_port:>62298 OR @fields.src_p:>62298) OR (@fields.source_ip:\"172.31.81.98\" OR"
                      " @fields.dest_ip:\"172.31.81.98\" OR @fields.src:\"172.31.81.98\" OR "
                      "@fields.dst:\"172.31.81.98\" OR @fields.ip:\"172.31.81.98\" OR "
                      "@fields.subnet_mask:\"172.31.81.98\" OR @fields.released_ip:\"172.31.81.98\" OR "
                      "@fields.requested_ip:\"172.31.81.98\" OR @fields.assigned_ip:\"172.31.81.98\")) AND "
                      "(@fields.epochdate :>1650947192.945 AND @fields.epochdate :<1650947492.945))",
            "fields": [],
            "timeframe": "custom",
            "time": {
                "from": "2022-04-26T04:26:32.945000Z",
                "to": "2022-04-26T04:31:32.945000Z"
            },
            "size": 10000
        }]
        expected_query = _remove_timestamp_from_query(expected_query)
        self._test_query_assertions(actual_query, expected_query)

    def test_domain_name_and_mac(self):
        stix_pattern = "[domain-name:value='ec2.internal'] AND [mac-addr:value = '12:2f:23:46:35:5b']"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        actual_query['queries'] = _remove_timestamp_from_query(actual_query['queries'])
        expected_query = [{
            "search": "(((@fields.domain_name:\"ec2.internal\" OR @fields.query:\"ec2.internal\") OR "
                      "@fields.mac:\"12:2f:23:46:35:5b\") AND (@fields.epochdate :>1651064544.474 AND "
                      "@fields.epochdate :<1651064844.474))",
            "fields": [],
            "timeframe": "custom",
            "time": {
                "from": "2022-04-27T13:02:24.474000Z",
                "to": "2022-04-27T13:07:24.474000Z"
            },
            "size": 10000
        }]
        expected_query = _remove_timestamp_from_query(expected_query)
        self._test_query_assertions(actual_query, expected_query)

    def test_set_or_operator(self):
        stix_pattern = "([ipv4-addr:value = '172.31.81.98'] OR [mac-addr:value = '12:2f:23:46:35:5b'])" \
                       " START t'2022-03-01T00:00:00.000Z' STOP t'2022-03-31T11:00:00.003Z'"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        actual_query['queries'] = _remove_timestamp_from_query(actual_query['queries'])
        expected_query = [{
            "search": "(((@fields.source_ip:\"172.31.81.98\" OR @fields.dest_ip:\"172.31.81.98\" OR "
                      "@fields.src:\"172.31.81.98\" OR @fields.dst:\"172.31.81.98\" OR @fields.ip:\"172.31.81.98\" OR "
                      "@fields.subnet_mask:\"172.31.81.98\" OR @fields.released_ip:\"172.31.81.98\" OR "
                      "@fields.requested_ip:\"172.31.81.98\" OR @fields.assigned_ip:\"172.31.81.98\") OR "
                      "@fields.mac:\"12:2f:23:46:35:5b\") AND (@fields.epochdate :>1646092800.0 AND "
                      "@fields.epochdate :<1648724400.003))",
            "fields": [],
            "timeframe": "custom",
            "time": {
                "from": "2022-03-01T00:00:00.000000Z",
                "to": "2022-03-31T11:00:00.003000Z"
            },
            "size": 10000
        }]
        expected_query = _remove_timestamp_from_query(expected_query)
        self._test_query_assertions(actual_query, expected_query)

    def test_two_sets_or_operator(self):
        stix_pattern = "([network-traffic:dst_port = '3389'] AND [domain-name:value = 'sample']) AND " \
                       "([software:name = 'word'] OR [mac-addr:value = '12:2f:23:46:35:5b']) " \
                       "START t'2022-03-01T00:00:00.000Z' STOP t'2022-03-31T11:00:00.003Z'"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        actual_query['queries'] = _remove_timestamp_from_query(actual_query['queries'])
        expected_query = [{
            "search": "(((@fields.dest_port:3389 OR @fields.dst_p:3389) OR (@fields.domain_name:\"sample\" OR "
                      "@fields.query:\"sample\")) OR ((@fields.name:\"word\" OR @fields.mac:\"12:2f:23:46:35:5b\") AND "
                      "(@fields.epochdate :>1646092800.0 AND @fields.epochdate :<1648724400.003)))",
            "fields": [],
            "timeframe": "custom",
            "time": {
                "from": "2022-03-01T00:00:00.000000Z",
                "to": "2022-03-31T11:00:00.003000Z"
            },
            "size": 10000
        }]
        expected_query = _remove_timestamp_from_query(expected_query)
        self._test_query_assertions(actual_query, expected_query)

    def test_comparison_and_operator(self):
        stix_pattern = "[email-message:from_ref.value = 'shahtanveer@gmail.com'] AND " \
                       "[email-addr:value != 'first@mail.com']"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        actual_query['queries'] = _remove_timestamp_from_query(actual_query['queries'])
        expected_query = [{
            "search": "((@fields.mailfrom:\"shahtanveer@gmail.com\" OR "
                      "((@fields.mailfrom:* AND NOT @fields.mailfrom:\"first@mail.com\") OR "
                      "(@fields.rcptto:* AND NOT @fields.rcptto:\"first@mail.com\") OR "
                      "(@fields.from:* AND NOT @fields.from:\"first@mail.com\") OR "
                      "(@fields.to:* AND NOT @fields.to:\"first@mail.com\") OR "
                      "(@fields.cc:* AND NOT @fields.cc:\"first@mail.com\"))) AND "
                      "(@fields.epochdate :>1650950251.463 AND @fields.epochdate :<1650950551.463))",
            "fields": [],
            "timeframe": "custom",
            "time": {
                "from": "2022-04-26T05:17:31.463000Z",
                "to": "2022-04-26T05:22:31.463000Z"
            },
            "size": 10000
        }]
        expected_query = _remove_timestamp_from_query(expected_query)
        self._test_query_assertions(actual_query, expected_query)

    def test_combinedcomparison_and_or_operator(self):
        stix_pattern = "[ipv4-addr:value = '172.31.81.98'] AND [mac-addr:value = '12:2f:23:46:35:5b'] "\
                       "START t'2022-03-01T00:00:00.000Z' STOP t'2022-03-31T11:00:00.003Z'"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        actual_query['queries'] = _remove_timestamp_from_query(actual_query['queries'])
        expected_query = [{
            "search": "((@fields.source_ip:\"172.31.81.98\" OR @fields.dest_ip:\"172.31.81.98\" OR "
                      "@fields.src:\"172.31.81.98\" OR @fields.dst:\"172.31.81.98\" OR @fields.ip:\"172.31.81.98\" OR "
                      "@fields.subnet_mask:\"172.31.81.98\" OR @fields.released_ip:\"172.31.81.98\" OR "
                      "@fields.requested_ip:\"172.31.81.98\" OR @fields.assigned_ip:\"172.31.81.98\") OR "
                      "(@fields.mac:\"12:2f:23:46:35:5b\" AND (@fields.epochdate :>1646092800.0 AND "
                      "@fields.epochdate :<1648724400.003)))",
            "fields": [],
            "timeframe": "custom",
            "time": {
                "from": "2022-03-01T00:00:00.000000Z",
                "to": "2022-03-31T11:00:00.003000Z"
            },
            "size": 10000
        }]
        expected_query = _remove_timestamp_from_query(expected_query)
        self._test_query_assertions(actual_query, expected_query)

    def test_qualifier_without_milliseconds(self):
        stix_pattern = "[x-oca-asset:hostname = '169.254.169.254'] " \
                       "START t'2022-03-01T11:50:21Z' STOP t'2022-03-31T11:55:25Z'"
        actual_query = translation.translate('darktrace', 'query', '{}', stix_pattern)
        expected_query = [{
            "search": "(@fields.host:\"169.254.169.254\" AND (@fields.epochdate :>1646135421.0 "
                      "AND @fields.epochdate :<1648727725.0))",
            "fields": [],
            "timeframe": "custom",
            "time": {
                "from": "2022-03-01T11:50:21.000000Z",
                "to": "2022-03-31T11:55:25.000000Z"
            },
            "size": 10000
        }]
        self._test_query_assertions(actual_query, expected_query)
