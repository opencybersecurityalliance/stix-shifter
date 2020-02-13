from stix_shifter.stix_translation import stix_translation
import unittest
import json

translation = stix_translation.StixTranslation()


def _remove_timestamp_from_query(queries):
    if isinstance(queries, list):
        query_list = []
        for query in queries:
            query_dict = json.loads(query)
            query_dict.pop("startTime")
            query_dict.pop("endTime")
            query_list.append(query_dict)
        return query_list


class TestStixToQuery(unittest.TestCase):
    """
    class to perform unit test case aws cloudwatch logs translate query
    """

    def _test_query_assertions(self, query, queries):
        """
        to assert the each query in the list against expected result
        """
        self.assertIsInstance(query, dict)
        self.assertIsInstance(query['queries'], list)
        for each_query in query.get('queries'):
            self.assertIn(each_query, queries)

    def test_network_exp(self):
        """
        Test with Equal operator
        """
        stix_pattern = "[ipv4-addr:value = '172.31.88.63'] START t'2019-10-01T08:43:10.003Z' " \
                       "STOP t'2019-10-30T10:43:10.003Z'"
        query = translation.translate('aws_cloud_watch_logs', 'query', '{}', stix_pattern)
        queries = [
            '{"logType": "guardduty", "limit": 10000, "queryString": "fields @timestamp, source, @message | parse '
            'detail.resource.instanceDetails.networkInterfaces.0 \'\\"privateIpAddress\\":\\"*\\"\' as '
            'eth0_private_ip | parse detail.resource.instanceDetails.networkInterfaces.1 '
            '\'\\"privateIpAddress\\":\\"*\\"\' as eth1_private_ip | parse '
            'detail.resource.instanceDetails.networkInterfaces.0 \'\\"publicIp\\":\\"*\\"\' as public_ip | parse '
            '@message /(?:\\"ipAddressV4\\"\\\\:\\")(?<remote_ip>((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\\\.){3}(25['
            '0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(?:\\")/ | filter source = \'aws.guardduty\' or strlen('
            'eth0_private_ip) > 0 or strlen(eth1_private_ip) > 0 or strlen(public_ip) > 0 or strlen(remote_ip) > 0 '
            '| filter ((tolower(eth0_private_ip) = tolower(\'172.31.88.63\') OR tolower(eth1_private_ip) = tolower('
            '\'172.31.88.63\') OR tolower(public_ip) = tolower(\'172.31.88.63\') OR tolower(remote_ip) = tolower('
            '\'172.31.88.63\')))", "startTime": 1569919390, "endTime": 1572432190}',
            '{"logType": "vpcflow", "limit": 10000, "queryString": "fields @timestamp, srcAddr, dstAddr, srcPort, '
            'dstPort, protocol, start, end, accountId, interfaceId | filter strlen(srcAddr) > 0 or strlen(dstAddr) > '
            '0 or strlen(protocol) > 0 | filter ((tolower(srcAddr) = tolower(\'172.31.88.63\') OR tolower(dstAddr) = '
            'tolower(\'172.31.88.63\')))", "startTime": 1569919390, "endTime": 1572432190}']
        self._test_query_assertions(query, queries)

    def test_network_protocol_exp(self):
        """
        Test with IN operator
        """
        stix_pattern = "[network-traffic:protocols[*] IN ('tcp','igp')] START t'2019-10-01T08:43:10.003Z' STOP " \
                       "t'2019-10-30T10:43:10.003Z'"
        query = translation.translate('aws_cloud_watch_logs', 'query', '{}', stix_pattern)
        queries = [
            '{"logType": "guardduty", "limit": 10000, "queryString": "fields @timestamp, source, @message | parse '
            'detail.service.action.networkConnectionAction.protocol \\"\\" as protocol | filter source = '
            '\'aws.guardduty\' or strlen(protocol) > 0 | filter ((tolower(protocol) = tolower(\'tcp\') OR tolower('
            'protocol) = tolower(\'igp\')))", "startTime": 1569919390, "endTime": 1572432190}',
            '{"logType": "vpcflow", "limit": 10000, "queryString": "fields @timestamp, srcAddr, dstAddr, srcPort, '
            'dstPort, protocol, start, end, accountId, interfaceId | filter strlen(srcAddr) > 0 or strlen(dstAddr) > '
            '0 or strlen(protocol) > 0 | filter (protocol IN [\'6\', \'9\'])", "startTime": 1569919390, "endTime": '
            '1572432190}']
        self._test_query_assertions(query, queries)

    def test_like_comp_exp(self):
        """
        Test with LIKE operator
        """
        stix_pattern = "[network-traffic:src_ref.value LIKE '58'] START t'2019-10-01T08:43:10.003Z' STOP " \
                       "t'2019-10-30T10:43:10.003Z'"
        query = translation.translate('aws_cloud_watch_logs', 'query', '{}', stix_pattern)
        queries = [
            '{"logType": "guardduty", "limit": 10000, "queryString": "fields @timestamp, source, @message | parse '
            'detail.resource.instanceDetails.networkInterfaces.0 \'\\"privateIpAddress\\":\\"*\\"\' as '
            'eth0_private_ip | filter source = \'aws.guardduty\' or strlen(eth0_private_ip) > 0 | filter ('
            'eth0_private_ip LIKE /(?i)58/)", "startTime": 1569919390, "endTime": 1572432190}',
            '{"logType": "vpcflow", "limit": 10000, "queryString": "fields @timestamp, srcAddr, dstAddr, srcPort, '
            'dstPort, protocol, start, end, accountId, interfaceId | filter strlen(srcAddr) > 0 or strlen(dstAddr) > '
            '0 or strlen(protocol) > 0 | filter (srcAddr LIKE /(?i)58/)", "startTime": 1569919390, "endTime": '
            '1572432190}']
        self._test_query_assertions(query, queries)

    def test_in_comp_exp(self):
        """
        Test with IN operator
        """
        stix_pattern = "[ipv4-addr:value IN ('54.239.30.177','113.204.228.66')] START t'2019-10-01T08:43:10.003Z' " \
                       "STOP " \
                       "t'2019-10-30T10:43:10.003Z'"
        query = translation.translate('aws_cloud_watch_logs', 'query', '{}', stix_pattern)
        queries = [
            '{"logType": "guardduty", "limit": 10000, "queryString": "fields @timestamp, source, @message | parse '
            'detail.resource.instanceDetails.networkInterfaces.0 \'\\"privateIpAddress\\":\\"*\\"\' as '
            'eth0_private_ip | parse detail.resource.instanceDetails.networkInterfaces.1 '
            '\'\\"privateIpAddress\\":\\"*\\"\' as eth1_private_ip | parse '
            'detail.resource.instanceDetails.networkInterfaces.0 \'\\"publicIp\\":\\"*\\"\' as public_ip | parse '
            '@message /(?:\\"ipAddressV4\\"\\\\:\\")(?<remote_ip>((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\\\.){3}(25['
            '0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(?:\\")/ | filter source = \'aws.guardduty\' or strlen('
            'eth0_private_ip) > 0 or strlen(eth1_private_ip) > 0 or strlen(public_ip) > 0 or strlen(remote_ip) > 0 '
            '| filter (((tolower(eth0_private_ip) = tolower(\'54.239.30.177\') OR tolower(eth0_private_ip) = tolower('
            '\'113.204.228.66\')) OR (tolower(eth1_private_ip) = tolower(\'54.239.30.177\') OR tolower('
            'eth1_private_ip) = tolower(\'113.204.228.66\')) OR (tolower(public_ip) = tolower(\'54.239.30.177\') OR '
            'tolower(public_ip) = tolower(\'113.204.228.66\')) OR (tolower(remote_ip) = tolower(\'54.239.30.177\') OR '
            'tolower(remote_ip) = tolower(\'113.204.228.66\'))))", "startTime": 1569919390, "endTime": 1572432190}',
            '{"logType": "vpcflow", "limit": 10000, "queryString": "fields @timestamp, srcAddr, dstAddr, srcPort, '
            'dstPort, protocol, start, end, accountId, interfaceId | filter strlen(srcAddr) > 0 or strlen(dstAddr) > '
            '0 or strlen(protocol) > 0 | filter (((tolower(srcAddr) = tolower(\'54.239.30.177\') OR tolower(srcAddr) '
            '= tolower(\'113.204.228.66\')) OR (tolower(dstAddr) = tolower(\'54.239.30.177\') OR tolower(dstAddr) = '
            'tolower(\'113.204.228.66\'))))", "startTime": 1569919390, "endTime": 1572432190}']
        self._test_query_assertions(query, queries)

    def test_matches_comp_exp(self):
        """
        Test with MATCHES operator
        :return:
        """
        stix_pattern = "[network-traffic:src_port MATCHES '\\\\d+'] START t'2019-10-01T08:43:10.003Z' STOP " \
                       "t'2019-10-30T10:43:10.003Z'"
        query = translation.translate('aws_cloud_watch_logs', 'query', '{}', stix_pattern)
        queries = [
            '{"logType": "guardduty", "limit": 10000, "queryString": "fields @timestamp, source, @message | parse '
            '@message \'\\"localPortDetails\\":{\\"port\\":*,\' as local_port | filter source = \'aws.guardduty\' or '
            'strlen(local_port) > 0 | filter (local_port LIKE /\\\\d+/)", "startTime": 1569919390, "endTime": '
            '1572432190}',
            '{"logType": "vpcflow", "limit": 10000, "queryString": "fields @timestamp, srcAddr, dstAddr, srcPort, '
            'dstPort, protocol, start, end, accountId, interfaceId | filter strlen(srcAddr) > 0 or strlen(dstAddr) > '
            '0 or strlen(protocol) > 0 | filter (srcPort LIKE /\\\\d+/)", "startTime": 1569919390, "endTime": '
            '1572432190}']
        self._test_query_assertions(query, queries)

    def test_network_comp_exp(self):
        """
        Test with OR operator
        :return:
        """
        stix_pattern = "[ipv4-addr:value = '54.239.30.177' OR ipv4-addr:value = '167.71.118.48'] START " \
                       "t'2019-10-01T08:43:10.003Z' STOP t'2019-10-30T10:43:10.003Z'"
        query = translation.translate('aws_cloud_watch_logs', 'query', '{}', stix_pattern)
        queries = [
            '{"logType": "guardduty", "limit": 10000, "queryString": "fields @timestamp, source, @message | parse '
            'detail.resource.instanceDetails.networkInterfaces.0 \'\\"privateIpAddress\\":\\"*\\"\' as '
            'eth0_private_ip | parse detail.resource.instanceDetails.networkInterfaces.1 '
            '\'\\"privateIpAddress\\":\\"*\\"\' as eth1_private_ip | parse '
            'detail.resource.instanceDetails.networkInterfaces.0 \'\\"publicIp\\":\\"*\\"\' as public_ip | parse '
            '@message /(?:\\"ipAddressV4\\"\\\\:\\")(?<remote_ip>((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\\\.){3}(25['
            '0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(?:\\")/ | filter source = \'aws.guardduty\' or strlen('
            'eth0_private_ip) > 0 or strlen(eth1_private_ip) > 0 or strlen(public_ip) > 0 or strlen(remote_ip) > 0 '
            '| filter (((tolower(eth0_private_ip) = tolower(\'167.71.118.48\') OR tolower(eth1_private_ip) = tolower('
            '\'167.71.118.48\') OR tolower(public_ip) = tolower(\'167.71.118.48\') OR tolower(remote_ip) = tolower('
            '\'167.71.118.48\'))) OR ((tolower(eth0_private_ip) = tolower(\'54.239.30.177\') OR tolower('
            'eth1_private_ip) = tolower(\'54.239.30.177\') OR tolower(public_ip) = tolower(\'54.239.30.177\') OR '
            'tolower(remote_ip) = tolower(\'54.239.30.177\'))))", "startTime": 1569919390, "endTime": 1572432190}',
            '{"logType": "vpcflow", "limit": 10000, "queryString": "fields @timestamp, srcAddr, dstAddr, srcPort, '
            'dstPort, protocol, start, end, accountId, interfaceId | filter strlen(srcAddr) > 0 or strlen(dstAddr) > '
            '0 or strlen(protocol) > 0 | filter (((tolower(srcAddr) = tolower(\'167.71.118.48\') OR tolower(dstAddr) '
            '= tolower(\'167.71.118.48\'))) OR ((tolower(srcAddr) = tolower(\'54.239.30.177\') OR tolower(dstAddr) = '
            'tolower(\'54.239.30.177\'))))", "startTime": 1569919390, "endTime": 1572432190}']
        self._test_query_assertions(query, queries)

    def test_network_comb_obs_exp(self):
        """
        Test with two observation expression
        """
        stix_pattern = "([ipv4-addr:value = '54.239.30.177' OR ipv4-addr:value = '167.71.118.48'] OR [" \
                       "network-traffic:src_port = '22']) START t'2019-10-01T08:43:10.003Z' STOP " \
                       "t'2019-10-30T10:43:10.003Z'"
        query = translation.translate('aws_cloud_watch_logs', 'query', '{}', stix_pattern)
        queries = [
            '{"logType": "guardduty", "limit": 10000, "queryString": "fields @timestamp, source, @message | parse '
            'detail.resource.instanceDetails.networkInterfaces.0 \'\\"privateIpAddress\\":\\"*\\"\' as '
            'eth0_private_ip | parse detail.resource.instanceDetails.networkInterfaces.1 '
            '\'\\"privateIpAddress\\":\\"*\\"\' as eth1_private_ip | parse '
            'detail.resource.instanceDetails.networkInterfaces.0 \'\\"publicIp\\":\\"*\\"\' as public_ip | parse '
            '@message /(?:\\"ipAddressV4\\"\\\\:\\")(?<remote_ip>((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\\\.){3}(25['
            '0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(?:\\")/ | filter source = \'aws.guardduty\' or strlen('
            'eth0_private_ip) > 0 or strlen(eth1_private_ip) > 0 or strlen(public_ip) > 0 or strlen(remote_ip) > 0 '
            '| filter (((tolower(eth0_private_ip) = tolower(\'167.71.118.48\') OR tolower(eth1_private_ip) = tolower('
            '\'167.71.118.48\') OR tolower(public_ip) = tolower(\'167.71.118.48\') OR tolower(remote_ip) = tolower('
            '\'167.71.118.48\'))) OR ((tolower(eth0_private_ip) = tolower(\'54.239.30.177\') OR tolower('
            'eth1_private_ip) = tolower(\'54.239.30.177\') OR tolower(public_ip) = tolower(\'54.239.30.177\') OR '
            'tolower(remote_ip) = tolower(\'54.239.30.177\'))))", "startTime": 1569919390, "endTime": 1572432190}',
            '{"logType": "guardduty", "limit": 10000, "queryString": "fields @timestamp, source, @message | parse '
            '@message \'\\"localPortDetails\\":{\\"port\\":*,\' as local_port | filter source = \'aws.guardduty\' or '
            'strlen(local_port) > 0 | filter (local_port = \'22\')", "startTime": 1569919390, "endTime": 1572432190}',
            '{"logType": "vpcflow", "limit": 10000, "queryString": "fields @timestamp, srcAddr, dstAddr, srcPort, '
            'dstPort, protocol, start, end, accountId, interfaceId | filter strlen(srcAddr) > 0 or strlen(dstAddr) > '
            '0 or strlen(protocol) > 0 | filter (((tolower(srcAddr) = tolower(\'167.71.118.48\') OR tolower(dstAddr) '
            '= tolower(\'167.71.118.48\'))) OR ((tolower(srcAddr) = tolower(\'54.239.30.177\') OR tolower(dstAddr) = '
            'tolower(\'54.239.30.177\'))))", "startTime": 1569919390, "endTime": 1572432190}',
            '{"logType": "vpcflow", "limit": 10000, "queryString": "fields @timestamp, srcAddr, dstAddr, srcPort, '
            'dstPort, protocol, start, end, accountId, interfaceId | filter strlen(srcAddr) > 0 or strlen(dstAddr) > '
            '0 or strlen(protocol) > 0 | filter (srcPort = \'22\')", "startTime": 1569919390, "endTime": 1572432190}']
        self._test_query_assertions(query, queries)

    def test_start_end_exp(self):
        """
        test observation expression with Stix field start
        """
        stix_pattern = "[network-traffic:start = '2019-10-15T09:10:10.003Z'] START t'2019-10-01T08:43:10.003Z' STOP " \
                       "t'2019-10-30T10:43:10.003Z'"
        query = translation.translate('aws_cloud_watch_logs', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [
            '{"logType": "vpcflow", "limit": 10000, "queryString": "fields @timestamp, srcAddr, dstAddr, srcPort, '
            'dstPort, protocol, start, end, accountId, interfaceId | filter strlen(srcAddr) > 0 or strlen(dstAddr) > '
            '0 or strlen(protocol) > 0 | filter (start = \'1571130610\')", "startTime": 1569919390, '
            '"endTime": 1572432190}']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_oper_issuperset(self):
        """
        Test Unsupportted operator
        """
        stix_pattern = "([ipv4-addr:value ISSUPERSET '54.239.30.177'] START t'2019-10-01T08:43:10.003Z' STOP " \
                       "t'2019-10-30T10:43:10.003Z')"
        query = translation.translate('aws_cloud_watch_logs', 'query', '{}', stix_pattern)
        assert query['success'] is False
        assert query['code'] == 'not_implemented'
        assert query['error'] == 'wrong parameter : Comparison operator IsSuperSet unsupported for AWS CloudWatch ' \
                                 'logs adapter'
