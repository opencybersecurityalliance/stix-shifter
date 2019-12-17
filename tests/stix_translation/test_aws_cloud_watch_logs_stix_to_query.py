from stix_shifter.stix_translation import stix_translation
import unittest
import json

translation = stix_translation.StixTranslation()


def _remove_timestamp_from_query(queries):
    if isinstance(queries, list):
        query_dict = {}
        for query in queries:
            query_dict = json.loads(query)
            query_dict.pop("startTime")
            query_dict.pop("endTime")
        return [query_dict]


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
        for index, each_query in enumerate(query.get('queries'), start=0):
            self.assertEqual(each_query, queries[index])

    def test_network_exp(self):
        stix_pattern = "[ipv4-addr:value = '172.31.88.63']"
        query = translation.translate('aws_cloud_watch_logs', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [
            '{"logType": "guardduty", "limit": 1000, "queryString": "fields @timestamp, source, @message | parse '
            'detail.resource.instanceDetails.networkInterfaces.0 \'\\"privateIpAddress\\":\\"*\\"\' as '
            'private_ip_address | parse detail.resource.instanceDetails.networkInterfaces.0 \'\\"publicIp\\":\\"*\\"\' '
            'as public_ip | parse @message /(?:\\"ipAddressV4\\"\\\\:\\")(?<remote_ip>((25[0-5]|2[0-4][0-9]|[01]?[0-9]['
            '0-9]?)\\\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(?:\\")/ | filter source = \'aws.guardduty\' or '
            'strlen (private_ip_address) > 0 or strlen (public_ip) > 0 or strlen (remote_ip) > 0 | filter (('
            'private_ip_address =~ /^(?i)172.31.88.63$/ OR public_ip =~ /^(?i)172.31.88.63$/ OR remote_ip =~ /^('
            '?i)172.31.88.63$/))", "startTime": 1569919390, "endTime": 1572432190}',
            '{"logType": "vpcflow", "limit": 1000, "queryString": "fields @timestamp, srcAddr, dstAddr, srcPort, '
            'dstPort, protocol, start, '
            'end, accountId, interfaceId, bytes, packets | filter strlen(srcAddr) > 0 or strlen(dstAddr) > 0 or '
            'strlen(protocol) > 0 | filter ((srcAddr =~ /^(?i)172.31.88.63$/ OR dstAddr =~ /^(?i)172.31.88.63$/))", '
            '"startTime": 1569919390, "endTime": 1572432190}']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_network_protocol_exp(self):
        stix_pattern = "[network-traffic:protocols[*] IN ('tcp','igp')] START t'2019-10-01T08:43:10.003Z' STOP " \
                       "t'2019-10-30T10:43:10.003Z'"
        query = translation.translate('aws_cloud_watch_logs', 'query', '{}', stix_pattern)
        queries = [
            '{"logType": "guardduty", "limit": 1000, "queryString": "fields @timestamp, source, @message | parse '
            'detail.service.action.networkConnectionAction.protocol \\"\\" as protocol | filter source = '
            '\'aws.guardduty\' or strlen (protocol) > 0 | filter (protocol IN [\'TCP\', \'tcp\', \'IGP\', '
            '\'igp\'])", "startTime": 1569919390, "endTime": 1572432190}',
            '{"logType": "vpcflow", "limit": 1000, "queryString": "fields @timestamp, srcAddr, dstAddr, srcPort, '
            'dstPort, protocol, start, '
            'end, accountId, interfaceId, bytes, packets | filter strlen(srcAddr) > 0 or strlen(dstAddr) > 0 or '
            'strlen(protocol) > 0 | filter (protocol IN [\'6\', \'9\'])", "startTime": 1569919390, "endTime": '
            '1572432190}']
        self._test_query_assertions(query, queries)

    def test_like_comp_exp(self):
        stix_pattern = "[network-traffic:src_ref.value LIKE '58'] START t'2019-10-01T08:43:10.003Z' STOP " \
                       "t'2019-10-30T10:43:10.003Z'"
        query = translation.translate('aws_cloud_watch_logs', 'query', '{}', stix_pattern)
        queries = [
            '{"logType": "guardduty", "limit": 1000, "queryString": "fields @timestamp, source, @message | parse '
            'detail.resource.instanceDetails.networkInterfaces.0 \'\\"privateIpAddress\\":\\"*\\"\' as '
            'private_ip_address | filter source = \'aws.guardduty\' or strlen (private_ip_address) > 0 | filter ('
            'private_ip_address LIKE /(?i)58/)", "startTime": 1569919390, "endTime": 1572432190}',
            '{"logType": "vpcflow", "limit": 1000, "queryString": "fields @timestamp, srcAddr, dstAddr, srcPort, '
            'dstPort, protocol, start, '
            'end, accountId, interfaceId, bytes, packets | filter strlen(srcAddr) > 0 or strlen(dstAddr) > 0 or '
            'strlen(protocol) > 0 | filter (srcAddr LIKE /(?i)58/)", "startTime": 1569919390, "endTime": 1572432190}']
        self._test_query_assertions(query, queries)

    def test_in_comp_exp(self):
        stix_pattern = "[ipv4-addr:value IN ('54.239.30.177','113.204.228.66')] START t'2019-10-01T08:43:10.003Z' " \
                       "STOP " \
                       "t'2019-10-30T10:43:10.003Z'"
        query = translation.translate('aws_cloud_watch_logs', 'query', '{}', stix_pattern)
        queries = [
            '{"logType": "guardduty", "limit": 1000, "queryString": "fields @timestamp, source, @message | parse '
            'detail.resource.instanceDetails.networkInterfaces.0 \'\\"privateIpAddress\\":\\"*\\"\' as '
            'private_ip_address | parse detail.resource.instanceDetails.networkInterfaces.0 \'\\"publicIp\\":\\"*\\"\' '
            'as public_ip | parse @message /(?:\\"ipAddressV4\\"\\\\:\\")(?<remote_ip>((25[0-5]|2[0-4][0-9]|[01]?[0-9]['
            '0-9]?)\\\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(?:\\")/ | filter source = \'aws.guardduty\' or '
            'strlen (private_ip_address) > 0 or strlen (public_ip) > 0 or strlen (remote_ip) > 0 | filter (('
            'private_ip_address IN [\'54.239.30.177\', \'113.204.228.66\'] OR public_ip IN [\'54.239.30.177\', '
            '\'113.204.228.66\'] OR remote_ip IN [\'54.239.30.177\', \'113.204.228.66\']))", "startTime": 1569919390, '
            '"endTime": 1572432190}',
            '{"logType": "vpcflow", "limit": 1000, "queryString": "fields @timestamp, srcAddr, dstAddr, srcPort, '
            'dstPort, protocol, start, '
            'end, accountId, interfaceId, bytes, packets | filter strlen(srcAddr) > 0 or strlen(dstAddr) > 0 or '
            'strlen(protocol) > 0 | filter ((srcAddr IN [\'54.239.30.177\', \'113.204.228.66\'] OR dstAddr IN ['
            '\'54.239.30.177\', \'113.204.228.66\']))", "startTime": 1569919390, "endTime": 1572432190}']
        self._test_query_assertions(query, queries)

    def test_matches_comp_exp(self):
        stix_pattern = "[network-traffic:src_port MATCHES '\\\\d+'] START t'2019-10-01T08:43:10.003Z' STOP " \
                       "t'2019-10-30T10:43:10.003Z'"
        query = translation.translate('aws_cloud_watch_logs', 'query', '{}', stix_pattern)
        queries = [
            '{"logType": "guardduty", "limit": 1000, "queryString": "fields @timestamp, source, @message '
            '| parse @message '
            '\'\\"localPortDetails\\":{\\"port\\":*,\' as local_port | filter source = \'aws.guardduty\' or strlen ('
            'local_port) > 0 | filter (local_port LIKE /\\\\d+/)", "startTime": 1569919390, "endTime": 1572432190}',
            '{"logType": "vpcflow", "limit": 1000, "queryString": "fields @timestamp, srcAddr, dstAddr, srcPort, '
            'dstPort, protocol, start, '
            'end, accountId, interfaceId, bytes, packets | filter strlen(srcAddr) > 0 or strlen(dstAddr) > 0 or '
            'strlen(protocol) > 0 | filter (srcPort LIKE /\\\\d+/)", "startTime": 1569919390, "endTime": 1572432190}']
        self._test_query_assertions(query, queries)

    def test_network_comp_exp(self):
        stix_pattern = "[ipv4-addr:value = '54.239.30.177' OR ipv4-addr:value = '167.71.118.48'] START " \
                       "t'2019-10-01T08:43:10.003Z' STOP t'2019-10-30T10:43:10.003Z'"
        query = translation.translate('aws_cloud_watch_logs', 'query', '{}', stix_pattern)
        queries = [
            '{"logType": "guardduty", "limit": 1000, "queryString": "fields @timestamp, source, @message | parse '
            'detail.resource.instanceDetails.networkInterfaces.0 \'\\"privateIpAddress\\":\\"*\\"\' as '
            'private_ip_address | parse detail.resource.instanceDetails.networkInterfaces.0 \'\\"publicIp\\":\\"*\\"\' '
            'as public_ip | parse @message /(?:\\"ipAddressV4\\"\\\\:\\")(?<remote_ip>((25[0-5]|2[0-4][0-9]|[01]?[0-9]['
            '0-9]?)\\\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(?:\\")/ | filter source = \'aws.guardduty\' or '
            'strlen (private_ip_address) > 0 or strlen (public_ip) > 0 or strlen (remote_ip) > 0 | filter ((('
            'private_ip_address =~ /^(?i)167.71.118.48$/ OR public_ip =~ /^(?i)167.71.118.48$/ OR remote_ip =~ /^('
            '?i)167.71.118.48$/)) OR ((private_ip_address =~ /^(?i)54.239.30.177$/ '
            'OR public_ip =~ /^(?i)54.239.30.177$/ '
            'OR remote_ip =~ /^(?i)54.239.30.177$/)))", "startTime": 1569919390, "endTime": 1572432190}',
            '{"logType": "vpcflow", "limit": 1000, "queryString": "fields @timestamp, srcAddr, dstAddr, srcPort, '
            'dstPort, protocol, start, '
            'end, accountId, interfaceId, bytes, packets | filter strlen(srcAddr) > 0 or strlen(dstAddr) > 0 or '
            'strlen(protocol) > 0 | filter (((srcAddr =~ /^(?i)167.71.118.48$/ OR dstAddr =~ /^(?i)167.71.118.48$/)) '
            'OR ((srcAddr =~ /^(?i)54.239.30.177$/ OR dstAddr =~ /^(?i)54.239.30.177$/)))", "startTime": 1569919390, '
            '"endTime": 1572432190}']
        self._test_query_assertions(query, queries)

    def test_network_comb_obs_exp(self):
        stix_pattern = "([ipv4-addr:value = '54.239.30.177' OR ipv4-addr:value = '167.71.118.48'] OR [" \
                       "network-traffic:src_port = '22']) START t'2019-10-01T08:43:10.003Z' STOP " \
                       "t'2019-10-30T10:43:10.003Z'"
        query = translation.translate('aws_cloud_watch_logs', 'query', '{}', stix_pattern)
        queries = [
            '{"logType": "guardduty", "limit": 1000, "queryString": "fields @timestamp, source, @message | parse '
            'detail.resource.instanceDetails.networkInterfaces.0 \'\\"privateIpAddress\\":\\"*\\"\' as '
            'private_ip_address | parse detail.resource.instanceDetails.networkInterfaces.0 \'\\"publicIp\\":\\"*\\"\' '
            'as public_ip | parse @message /(?:\\"ipAddressV4\\"\\\\:\\")(?<remote_ip>((25[0-5]|2[0-4][0-9]|[01]?[0-9]['
            '0-9]?)\\\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(?:\\")/ | filter source = \'aws.guardduty\' or '
            'strlen (private_ip_address) > 0 or strlen (public_ip) > 0 or strlen (remote_ip) > 0 | filter ((('
            'private_ip_address =~ /^(?i)167.71.118.48$/ OR public_ip =~ /^(?i)167.71.118.48$/ OR remote_ip =~ /^('
            '?i)167.71.118.48$/)) OR ((private_ip_address =~ /^(?i)54.239.30.177$/ '
            'OR public_ip =~ /^(?i)54.239.30.177$/ '
            'OR remote_ip =~ /^(?i)54.239.30.177$/)))", "startTime": 1569919390, "endTime": 1572432190}',
            '{"logType": "guardduty", "limit": 1000, "queryString": "fields @timestamp, source, @message '
            '| parse @message '
            '\'\\"localPortDetails\\":{\\"port\\":*,\' as local_port | filter source = \'aws.guardduty\' or strlen ('
            'local_port) > 0 | filter (local_port =~ /^(?i)22$/)", "startTime": 1569919390, "endTime": 1572432190}',
            '{"logType": "vpcflow", "limit": 1000, "queryString": "fields @timestamp, srcAddr, dstAddr, srcPort, '
            'dstPort, protocol, start, '
            'end, accountId, interfaceId, bytes, packets | filter strlen(srcAddr) > 0 or strlen(dstAddr) > 0 or '
            'strlen(protocol) > 0 | filter (((srcAddr =~ /^(?i)167.71.118.48$/ OR dstAddr =~ /^(?i)167.71.118.48$/)) '
            'OR ((srcAddr =~ /^(?i)54.239.30.177$/ OR dstAddr =~ /^(?i)54.239.30.177$/)))", "startTime": 1569919390, '
            '"endTime": 1572432190}',
            '{"logType": "vpcflow", "limit": 1000, "queryString": "fields @timestamp, srcAddr, dstAddr, srcPort, '
            'dstPort, protocol, start, '
            'end, accountId, interfaceId, bytes, packets | filter strlen(srcAddr) > 0 or strlen(dstAddr) > 0 or '
            'strlen(protocol) > 0 | filter (srcPort =~ /^(?i)22$/)", "startTime": 1569919390, "endTime": 1572432190}']
        self._test_query_assertions(query, queries)

    def test_start_end_exp(self):
        stix_pattern = "[network-traffic:start = '2019-10-15T09:10:10.003Z'] START t'2019-10-01T08:43:10.003Z' STOP " \
                       "t'2019-10-30T10:43:10.003Z'"
        query = translation.translate('aws_cloud_watch_logs', 'query', '{}', stix_pattern)
        queries = [
            '{"logType": "vpcflow", "limit": 1000, "queryString": "fields @timestamp, srcAddr, dstAddr, srcPort, '
            'dstPort, protocol, start, '
            'end, accountId, interfaceId, bytes, packets | filter strlen(srcAddr) > 0 or strlen(dstAddr) > 0 or '
            'strlen(protocol) > 0 | filter ((start = \'1571130610\'))", "startTime": 1569919390, "endTime": '
            '1572432190}']
        self._test_query_assertions(query, queries)

    def test_cust_attr_updatedAt_exp(self):
        stix_pattern = "[x_com_aws_cwl:updated_at = '2019-10-15T09:10:10.003Z'] START " \
                       "t'2019-10-01T08:43:10.003Z' STOP t'2019-10-30T10:43:10.003Z'"
        query = translation.translate('aws_cloud_watch_logs', 'query', '{}', stix_pattern)
        queries = [
            '{"logType": "guardduty", "limit": 1000, "queryString": "fields @timestamp, source, '
            '@message | parse detail.updatedAt \\"\\" as '
            'updated_at | filter source = \'aws.guardduty\' or strlen (updated_at) > 0 | filter ((updated_at = '
            '\'2019-10-15T09:10:10.003Z\'))", "startTime": 1569919390, "endTime": 1572432190}']
        self._test_query_assertions(query, queries)
