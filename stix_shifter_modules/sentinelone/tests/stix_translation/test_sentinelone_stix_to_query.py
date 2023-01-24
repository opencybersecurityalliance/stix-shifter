import re
import unittest
from stix_shifter.stix_translation import stix_translation
from stix_shifter_utils.utils.error_response import ErrorCode

translation = stix_translation.StixTranslation()


def _remove_timestamp_from_query_ver1(queries):
    pattern = r'\s*AND\s*EventTime\s*BETWEEN\s*\\"\d{4}-\d{2}-\d{2}T\d{2}:' \
              r'\d{2}:\d{2}\.\d{3}Z\\"\s*AND\s*\\"\d{4}-\d{2}-\d{2}T\d{2}:' \
              r'\d{2}:\d{2}\.\d{3}Z\\"",\s*"fromDate":\s*"\d{4}-\d{2}-\d{2}T\d{2}:' \
              r'\d{2}:\d{2}\.\d{3}Z",\s*"toDate":\s*"\d{4}-\d{2}-\d{2}T\d{2}:' \
              r'\d{2}:\d{2}\.\d{3}Z",\s*"limit":\s*10000'

    if isinstance(queries, list):
        return [re.sub(pattern, '', str(query)) for query in queries]
    elif isinstance(queries, str):
        return re.sub(pattern, '', queries)


def _remove_timestamp_from_query_ver2(queries):
    pattern = r'\s*AND\s*EventTime\s*BETWEEN\s*\\"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:' \
              r'\d{2}\.\d{3}Z\\"\s*AND\s*\\"\d{4}-\d{2}-\d{2}T\d{2}:' \
              r'\d{2}:\d{2}\.\d{3}Z\\"\)",\s*"fromDate":\s*"\d{4}-\d{2}-\d{2}T\d{2}:' \
              r'\d{2}:\d{2}\.\d{3}Z",\s*"toDate":\s*"\d{4}-\d{2}-\d{2}T\d{2}:' \
              r'\d{2}:\d{2}\.\d{3}Z",\s*"limit":\s*10000'

    if isinstance(queries, list):
        return [re.sub(pattern, '', str(query)) for query in queries]
    elif isinstance(queries, str):
        return re.sub(pattern, '', queries)


class TestQueryTranslator(unittest.TestCase):
    """
    class to perform unit test case for sentinelone translate query
    """
    if __name__ == "__main__":
        unittest.main()

    def _test_query_assertions(self, query, queries):
        """
        to assert the each query in the list against expected result
        """
        self.assertIsInstance(queries, list)
        self.assertIsInstance(query, dict)
        self.assertIsInstance(query['queries'], list)
        for index, each_query in enumerate(query.get('queries'), start=0):
            self.assertEqual(each_query, queries[index])

    def test_ipv4_query(self):
        """ test to check ipv4 stix pattern to native data source query """
        stix_pattern = "[ipv4-addr:value = '164.132.169.172']"
        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query_ver1(query['queries'])
        queries = ['{"query": "(srcIp = \\"164.132.169.172\\" '
                   'OR dstIp = \\"164.132.169.172\\" '
                   'OR srcMachineIP = \\"164.132.169.172\\") AND EventTime  '
                   'BETWEEN \\"2022-04-15T12:33:32.255Z\\" '
                   'AND \\"2022-04-15T12:38:32.255Z\\"", '
                   '"fromDate": "2022-04-15T12:33:32.255Z", '
                   '"toDate": "2022-04-15T12:38:32.255Z", "limit": 10000}']
        queries = _remove_timestamp_from_query_ver1(queries)
        self._test_query_assertions(query, queries)

    def test_network_traffic_query(self):
        """ test to check network traffic stix pattern to native data source query """
        stix_pattern = "[network-traffic:dst_port= 3389]"
        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query_ver1(query['queries'])
        queries = ['{"query": "dstPort = \\"3389\\" AND EventTime  '
                   'BETWEEN \\"2022-02-22T09:16:24.526Z\\" AND \\"2022-02-22T09:21:24.526Z\\"", '
                   '"fromDate": "2022-02-22T09:16:24.526Z", '
                   '"toDate": "2022-02-22T09:21:24.526Z", "limit": 10000}']
        queries = _remove_timestamp_from_query_ver1(queries)
        self._test_query_assertions(query, queries)

    def test_network_query_greater_than(self):
        """ test to check network traffic stix pattern to native data source query """
        stix_pattern = "[network-traffic:dst_port> 3000]"
        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query_ver1(query['queries'])
        queries = ['{"query": "dstPort > \\"3000\\" AND EventTime  '
                   'BETWEEN \\"2022-02-22T09:18:09.727Z\\" AND \\"2022-02-22T09:23:09.727Z\\"", '
                   '"fromDate": "2022-02-22T09:18:09.727Z", '
                   '"toDate": "2022-02-22T09:23:09.727Z", "limit": 10000}']
        queries = _remove_timestamp_from_query_ver1(queries)
        self._test_query_assertions(query, queries)

    def test_network_query_not_equals(self):
        """ test to check network traffic stix pattern to native data source query """
        stix_pattern = "[network-traffic:dst_port!= 22]"
        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query_ver1(query['queries'])
        queries = ['{"query": "dstPort != \\"22\\" AND EventTime  '
                   'BETWEEN \\"2022-02-22T09:20:09.933Z\\" AND \\"2022-02-22T09:25:09.933Z\\"", '
                   '"fromDate": "2022-02-22T09:20:09.933Z", '
                   '"toDate": "2022-02-22T09:25:09.933Z", "limit": 10000}']
        queries = _remove_timestamp_from_query_ver1(queries)
        self._test_query_assertions(query, queries)

    def test_network_query_less_than(self):
        """ test to check network traffic stix pattern to native data source query """
        stix_pattern = "[network-traffic:dst_port< 22]"
        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query_ver1(query['queries'])
        queries = ['{"query": "dstPort < \\"22\\" AND EventTime  '
                   'BETWEEN \\"2022-02-22T09:21:54.124Z\\" '
                   'AND \\"2022-02-22T09:26:54.124Z\\"", '
                   '"fromDate": "2022-02-22T09:21:54.124Z", '
                   '"toDate": "2022-02-22T09:26:54.124Z", "limit": 10000}']
        queries = _remove_timestamp_from_query_ver1(queries)
        self._test_query_assertions(query, queries)

    def test_network_query_lessthan_or_equals(self):
        """ test to check network traffic stix pattern to native data source query """
        stix_pattern = "[network-traffic:dst_port<= 22]"

        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query_ver1(query['queries'])
        queries = ['{"query": "dstPort <= \\"22\\" AND EventTime  '
                   'BETWEEN \\"2022-02-22T09:23:42.790Z\\" '
                   'AND \\"2022-02-22T09:28:42.790Z\\"", '
                   '"fromDate": "2022-02-22T09:23:42.790Z", '
                   '"toDate": "2022-02-22T09:28:42.790Z", "limit": 10000}']
        queries = _remove_timestamp_from_query_ver1(queries)
        self._test_query_assertions(query, queries)

    def test_network_query_greaterthan_or_equals(self):
        """ test to check network traffic stix pattern to native data source query """
        stix_pattern = "[network-traffic:dst_port>= 22]"
        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query_ver1(query['queries'])
        queries = [
            '{"query": "dstPort >= \\"22\\" AND EventTime  BETWEEN \\"2022-02-20T12:16:36.638Z\\" '
            'AND \\"2022-02-20T12:21:36.638Z\\"", "fromDate": "2022-02-20T12:16:36.638Z", '
            '"toDate": "2022-02-20T12:21:36.638Z", "limit": 10000}']
        queries = _remove_timestamp_from_query_ver1(queries)
        self._test_query_assertions(query, queries)

    def test_network_query_in_operator(self):
        """ test to check network traffic stix pattern to native data source query """
        stix_pattern = "[network-traffic:dst_port IN (80,3389)]"
        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query_ver1(query['queries'])
        queries = [
            '{"query": "dstPort IN (\\"80\\",\\"3389\\") AND EventTime  '
            'BETWEEN \\"2022-02-20T12:23:23.975Z\\" AND \\"2022-02-20T12:28:23.975Z\\"", '
            '"fromDate": "2022-02-20T12:23:23.975Z", '
            '"toDate": "2022-02-20T12:28:23.975Z", "limit": 10000}']
        queries = _remove_timestamp_from_query_ver1(queries)
        self._test_query_assertions(query, queries)

    def test_process_like_operator(self):
        """ test to check process stix pattern to native data source query """
        stix_pattern = "[process:name LIKE 'svchost.exe']"
        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query_ver1(query['queries'])
        queries = ['{"query": "(srcProcName in contains anycase (\\"svchost.exe\\") '
                   'OR srcProcParentName in contains anycase (\\"svchost.exe\\") '
                   'OR tgtProcName in contains anycase (\\"svchost.exe\\")) '
                   'AND EventTime  BETWEEN \\"2022-03-17T06:49:36.915Z\\" '
                   'AND \\"2022-03-17T06:54:36.915Z\\"", '
                   '"fromDate": "2022-03-17T06:49:36.915Z", '
                   '"toDate": "2022-03-17T06:54:36.915Z", "limit": 10000}']
        queries = _remove_timestamp_from_query_ver1(queries)
        self._test_query_assertions(query, queries)

    def test_process_matches_operator(self):
        """ test to check process stix pattern to native data source query """
        stix_pattern = "[process:name MATCHES 'svchost.exe']"
        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query_ver1(query['queries'])
        queries = ['{"query": "(srcProcName regexp \\"svchost.exe\\" '
                   'OR srcProcParentName regexp \\"svchost.exe\\" '
                   'OR tgtProcName regexp \\"svchost.exe\\") '
                   'AND EventTime  BETWEEN \\"2022-03-17T06:53:00.681Z\\" '
                   'AND \\"2022-03-17T06:58:00.681Z\\"", '
                   '"fromDate": "2022-03-17T06:53:00.681Z", '
                   '"toDate": "2022-03-17T06:58:00.681Z", "limit": 10000}']
        queries = _remove_timestamp_from_query_ver1(queries)
        self._test_query_assertions(query, queries)

    def test_process_created_query(self):
        """ test to check process stix pattern to native data source query """
        stix_pattern = "[process:created >= '2019-09-04T09:29:29.0882Z']"
        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query_ver1(query['queries'])
        queries = ['{"query": "(srcProcStartTime >= \\"2019-09-04T09:29:29.0882Z\\" '
                   'OR tgtProcStartTime >= \\"2019-09-04T09:29:29.0882Z\\" '
                   'OR srcProcParentStartTime >= \\"2019-09-04T09:29:29.0882Z\\") '
                   'AND EventTime  BETWEEN \\"2022-04-15T12:45:11.518Z\\" '
                   'AND \\"2022-04-15T12:50:11.518Z\\"", '
                   '"fromDate": "2022-04-15T12:45:11.518Z", '
                   '"toDate": "2022-04-15T12:50:11.518Z", "limit": 10000}']
        queries = _remove_timestamp_from_query_ver1(queries)
        self._test_query_assertions(query, queries)

    def test_query_from_multiple_comparison_expressions_joined_by_and(self):
        """ test to check multiple comparison stix pattern to native data source query """
        stix_pattern = "[  x-oca-asset:extensions.'x-sentinelone-endpoint'." \
                       "endpoint_os = 'windows' AND " \
                       "file:extensions.'x-sentinelone-file'.file_type IN ('PE')]"
        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query_ver1(query['queries'])
        queries = ['{"query": "(tgtFileType IN (\\"PE\\") '
                   'AND endpointOs = \\"WINDOWS\\") AND EventTime  '
                   'BETWEEN \\"2022-03-11T10:34:07.700Z\\" '
                   'AND \\"2022-03-11T10:39:07.700Z\\"", '
                   '"fromDate": "2022-03-11T10:34:07.700Z", '
                   '"toDate": "2022-03-11T10:39:07.700Z", "limit": 10000}']
        queries = _remove_timestamp_from_query_ver1(queries)
        self._test_query_assertions(query, queries)

    def test_file_query(self):
        """ test to check file stix pattern to native data source query """
        stix_pattern = "[file:name LIKE 'WindowsApplication1']"
        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query_ver1(query['queries'])
        queries = ['{"query": "fileFullName in contains anycase (\\"WindowsApplication1\\") '
                   'AND EventTime  BETWEEN \\"2022-03-17T04:25:39.478Z\\" '
                   'AND \\"2022-03-17T04:30:39.478Z\\"", '
                   '"fromDate": "2022-03-17T04:25:39.478Z", '
                   '"toDate": "2022-03-17T04:30:39.478Z", "limit": 10000}']
        queries = _remove_timestamp_from_query_ver1(queries)
        self._test_query_assertions(query, queries)

    def test_query_from_morethan_two_comparison_expressions_joined_by_and(self):
        """ test to check more than two comparison expressions """
        stix_pattern = "[user-account:account_login LIKE 'ADMINISTRATOR' " \
                       "AND x-oca-asset:extensions.'x-sentinelone-endpoint'." \
                       "endpoint_os = 'windows' " \
                       "AND x-sentinelone-indicator:indicator_name = 'PreloadInjection']"
        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query_ver1(query['queries'])
        queries = ['{"query": "(indicatorName = \\"PreloadInjection\\" '
                   'AND (endpointOs = \\"WINDOWS\\" '
                   'AND loginsUserName in contains anycase (\\"ADMINISTRATOR\\"))) '
                   'AND EventTime  BETWEEN \\"2022-04-15T12:48:51.738Z\\" '
                   'AND \\"2022-04-15T12:53:51.738Z\\"", '
                   '"fromDate": "2022-04-15T12:48:51.738Z", '
                   '"toDate": "2022-04-15T12:53:51.738Z", "limit": 10000}']
        queries = _remove_timestamp_from_query_ver1(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_observation_query(self):
        """ test to check multiple observation query """
        stix_pattern = "([file: hashes.MD5 = '0bbd4d92d3a0178463ef6e0ad46c986a' " \
                       "AND file:extensions.'x-sentinelone-file'.file_extension = 'log'" \
                       " AND x-oca-event:action = 'File Rename'] AND " \
                       "[file:extensions.'x-sentinelone-file'.file_type = 'PE'] AND " \
                       "[ x-oca-asset:extensions.'x-sentinelone-endpoint'." \
                       "agent_version = '21.6.6.1200' " \
                       "AND network-traffic:extensions.'x-sentinelone-network-action'." \
                       "connection_status ='SUCCESS' ])" \
                       "START t'2019-10-01T00:00:00.030Z' STOP t'2021-10-07T00:00:00.030Z' "
        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        queries = ['{"query": "((eventType = \\"FILE RENAME\\" AND '
                   '(tgtFileExtension = \\"log\\" AND '
                   '(tgtFileMd5 = \\"0bbd4d92d3a0178463ef6e0ad46c986a\\" OR '
                   'tgtFileOldMd5 = \\"0bbd4d92d3a0178463ef6e0ad46c986a\\" OR '
                   'srcProcImageMd5 = \\"0bbd4d92d3a0178463ef6e0ad46c986a\\" OR '
                   'tgtProcImageMd5 = \\"0bbd4d92d3a0178463ef6e0ad46c986a\\"))) '
                   'AND EventTime  BETWEEN \\"2019-10-01T00:00:00.030Z\\" '
                   'AND \\"2021-10-07T00:00:00.030Z\\") '
                   'OR (tgtFileType = \\"PE\\" AND EventTime  '
                   'BETWEEN \\"2019-10-01T00:00:00.030Z\\" AND \\"2021-10-07T00:00:00.030Z\\") '
                   'OR ((netConnStatus = \\"SUCCESS\\" AND agentVersion = \\"21.6.6.1200\\") '
                   'AND EventTime  BETWEEN \\"2019-10-01T00:00:00.030Z\\" '
                   'AND \\"2021-10-07T00:00:00.030Z\\")", '
                   '"fromDate": "2019-10-01T00:00:00.030Z", '
                   '"toDate": "2021-10-07T00:00:00.030Z", "limit": 10000}']
        self._test_query_assertions(query, queries)

    def test_negate_query(self):
        """ test to check negate query """
        stix_pattern = "[x-oca-asset:extensions.'x-sentinelone-endpoint'." \
                       "endpoint_os NOT IN('windows')]"
        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query_ver1(query['queries'])
        queries = ['{"query": "endpointOs NOT IN (\\"WINDOWS\\") AND EventTime  '
                   'BETWEEN \\"2022-02-25T11:17:57.613Z\\" AND \\"2022-02-25T11:22:57.613Z\\"", '
                   '"fromDate": "2022-02-25T11:17:57.613Z", '
                   '"toDate": "2022-02-25T11:22:57.613Z", "limit": 10000}']
        queries = _remove_timestamp_from_query_ver1(queries)
        self._test_query_assertions(query, queries)

    def test_boolean_true_value_query(self):
        """ test to check boolean true query """
        stix_pattern = "[user-account:is_privileged = 'true']"
        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query_ver1(query['queries'])
        queries = ['{"query": "loginIsAdministratorEquivalent is true AND EventTime  '
                   'BETWEEN \\"2022-02-20T13:17:01.361Z\\" AND \\"2022-02-20T13:22:01.361Z\\"", '
                   '"fromDate": "2022-02-20T13:17:01.361Z", '
                   '"toDate": "2022-02-20T13:22:01.361Z", "limit": 10000}']
        queries = _remove_timestamp_from_query_ver1(queries)
        self._test_query_assertions(query, queries)

    def test_boolean_false_value_query(self):
        """ test to check boolean false query """
        stix_pattern = "[user-account:is_privileged = 'false']"
        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query_ver1(query['queries'])
        queries = [
            '{"query": "loginIsAdministratorEquivalent is false AND EventTime  '
            'BETWEEN \\"2022-02-20T13:18:21.764Z\\" AND \\"2022-02-20T13:23:21.764Z\\"", '
            '"fromDate": "2022-02-20T13:18:21.764Z", '
            '"toDate": "2022-02-20T13:23:21.764Z", "limit": 10000}']
        queries = _remove_timestamp_from_query_ver1(queries)
        self._test_query_assertions(query, queries)

    def test_merge_similar_element_timestamp_query(self):
        """ test to check similar element timestamp query """
        stix_pattern = "[network-traffic:src_port = 62024 AND " \
                       "network-traffic:protocols[*] = 'tcp'] START " \
                       "t'2019-10-01T08:43:10.003Z' STOP t'2019-11-30T10:43:10.005Z' "
        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        queries = ['{"query": "(netProtocolName = \\"tcp\\" AND srcPort = \\"62024\\") '
                   'AND EventTime  BETWEEN \\"2019-10-01T08:43:10.003Z\\" '
                   'AND \\"2019-11-30T10:43:10.005Z\\"", '
                   '"fromDate": "2019-10-01T08:43:10.003Z", '
                   '"toDate": "2019-11-30T10:43:10.005Z", "limit": 10000}']
        self._test_query_assertions(query, queries)

    def test_is_reversed_parm_query(self):
        """ test to check reversed parameter query """
        stix_pattern = "[process:extensions.'x-sentinelone-process'." \
                       "publisher = 'MICROSOFT WINDOWS PUBLISHER' " \
                       "AND network-traffic:src_port = 62024 ] START " \
                       "t'2019-10-01T08:43:10.003Z' STOP t'2019-11-30T10:43:10.005Z' "
        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        queries = ['{"query": "(srcPort = \\"62024\\" '
                   'AND (srcProcPublisher = \\"MICROSOFT WINDOWS PUBLISHER\\" '
                   'OR tgtProcPublisher = \\"MICROSOFT WINDOWS PUBLISHER\\")) '
                   'AND EventTime  BETWEEN \\"2019-10-01T08:43:10.003Z\\" '
                   'AND \\"2019-11-30T10:43:10.005Z\\"", '
                   '"fromDate": "2019-10-01T08:43:10.003Z", '
                   '"toDate": "2019-11-30T10:43:10.005Z", "limit": 10000}']
        self._test_query_assertions(query, queries)

    def test_multiple_observation_with_qualifier_query(self):
        """ test to check multiple observation qualifier query """
        stix_pattern = "[file:size > 10 ] START t'2022-01-01T00:00:00.030Z' " \
                       "STOP t'2022-02-28T00:00:00.030Z' AND [ " \
                       "file:extensions.'x-sentinelone-file'." \
                       "file_description = 'Windows Push " \
                       "Notifications User Service_2d02eb' AND " \
                       "x-oca-asset:extensions.'x-sentinelone-endpoint'." \
                       "endpoint_os = 'windows'] "
        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query_ver2(query['queries'])
        queries = ['{"query": "(tgtFileSize > \\"10\\" AND EventTime  '
                   'BETWEEN \\"2022-01-01T00:00:00.030Z\\" '
                   'AND \\"2022-02-28T00:00:00.030Z\\") '
                   'OR ((endpointOs = \\"WINDOWS\\" AND '
                   'tgtFileDescription = \\"Windows Push Notifications '
                   'User Service_2d02eb\\") AND EventTime  '
                   'BETWEEN \\"2022-03-03T06:11:48.907Z\\" '
                   'AND \\"2022-03-03T06:16:48.907Z\\")", '
                   '"fromDate": "2022-01-01T00:00:00.030Z", '
                   '"toDate": "2022-03-03T06:16:48.907Z", "limit": 10000}']
        queries = _remove_timestamp_from_query_ver2(queries)
        self._test_query_assertions(query, queries)

    def test_not_include_filter_query(self):
        """test to check not include filter query"""
        stix_pattern = "[domain-name:value!='dc-integrations.traps.paloaltonetworks.com']"
        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query_ver1(query['queries'])
        queries = ['{"query": "(dnsRequest != \\"dc-integrations.traps.paloaltonetworks.com\\" '
                   'OR dnsResponse != \\"dc-integrations.traps.paloaltonetworks.com\\" '
                   'OR loginAccountDomain != \\"dc-integrations.traps.paloaltonetworks.com\\") '
                   'AND EventTime  BETWEEN \\"2022-04-15T12:42:44.494Z\\" '
                   'AND \\"2022-04-15T12:47:44.494Z\\"", "fromDate": "2022-04-15T12:42:44.494Z", '
                   '"toDate": "2022-04-15T12:47:44.494Z", "limit": 10000}']
        queries = _remove_timestamp_from_query_ver1(queries)
        self._test_query_assertions(query, queries)

    def test_creation_with_in_operator_query(self):
        """test to check in operator query"""
        stix_pattern = "[process:pid IN (443) ]"
        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query_ver1(query['queries'])
        queries = ['{"query": "(srcProcPid IN (\\"443\\") OR tgtProcPid IN (\\"443\\") '
                   'OR srcProcParentPid IN (\\"443\\")) AND EventTime  '
                   'BETWEEN \\"2022-02-22T16:10:35.305Z\\" AND \\"2022-02-22T16:15:35.305Z\\"", '
                   '"fromDate": "2022-02-22T16:10:35.305Z", '
                   '"toDate": "2022-02-22T16:15:35.305Z", "limit": 10000}']
        queries = _remove_timestamp_from_query_ver1(queries)
        self._test_query_assertions(query, queries)

    def test_negate_for_like_operator(self):
        """test to check negate for like query"""
        stix_pattern = "[file:extensions.'x-sentinelone-file'." \
                       "file_description NOT LIKE 'Windows']"
        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query_ver1(query['queries'])
        queries = ['{"query": "NOT tgtFileDescription in contains anycase (\\"Windows\\") '
                   'AND EventTime  BETWEEN \\"2022-03-17T04:33:13.901Z\\" '
                   'AND \\"2022-03-17T04:38:13.901Z\\"", '
                   '"fromDate": "2022-03-17T04:33:13.901Z", '
                   '"toDate": "2022-03-17T04:38:13.901Z", "limit": 10000}']
        queries = _remove_timestamp_from_query_ver1(queries)
        self._test_query_assertions(query, queries)

    def test_negate_for_greater_than_or_equals_operator(self):
        """test to check negate greater than or equal query"""
        stix_pattern = "[network-traffic:dst_port NOT >= 22]"
        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query_ver1(query['queries'])
        queries = ['{"query": "dstPort < \\"22\\" AND EventTime  '
                   'BETWEEN \\"2022-02-25T11:25:55.150Z\\" AND \\"2022-02-25T11:30:55.150Z\\"", '
                   '"fromDate": "2022-02-25T11:25:55.150Z", '
                   '"toDate": "2022-02-25T11:30:55.150Z", "limit": 10000}']
        queries = _remove_timestamp_from_query_ver1(queries)
        self._test_query_assertions(query, queries)

    def test_negate_for_less_than_operator(self):
        """test to check negate for lessthan  query"""
        stix_pattern = "[network-traffic:dst_port NOT < 22]"
        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query_ver1(query['queries'])
        queries = ['{"query": "dstPort >= \\"22\\" AND EventTime  '
                   'BETWEEN \\"2022-02-25T11:28:23.103Z\\" '
                   'AND \\"2022-02-25T11:33:23.103Z\\"", '
                   '"fromDate": "2022-02-25T11:28:23.103Z", '
                   '"toDate": "2022-02-25T11:33:23.103Z", "limit": 10000}']
        queries = _remove_timestamp_from_query_ver1(queries)
        self._test_query_assertions(query, queries)

    def test_unmapped_attribute_handling_with_and(self):
        """test to check unmapped attribute"""
        stix_pattern = "[url:value = 'http://www.testaddress.com' AND unmapped:attribute = 'something']"
        result = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_MAPPING_ERROR.value == result['code']
        assert 'Unable to map the following STIX objects and properties' in result['error']

    def test_invalid_stix_pattern(self):
        """test to check invalid stix pattern"""
        stix_pattern = "[not_a_valid_pattern]"
        result = translation.translate('sentinelone', 'query', '{}', stix_pattern, {'validate_pattern': 'true'})
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_STIX_VALIDATION.value == result['code']
        assert stix_pattern[1:-1] in result['error']

    def test_for_match_operator(self):
        """test to check regex operator query"""
        stix_pattern = "[process:name MATCHES '[a-zA-Z0-9_%]+[.exe]']"
        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query_ver1(query['queries'])
        queries = ['{"query": "(srcProcName regexp \\"[a-zA-Z0-9_%]+[.exe]\\" '
                   'OR srcProcParentName regexp \\"[a-zA-Z0-9_%]+[.exe]\\" '
                   'OR tgtProcName regexp \\"[a-zA-Z0-9_%]+[.exe]\\") '
                   'AND EventTime  BETWEEN \\"2022-03-17T06:45:46.514Z\\" '
                   'AND \\"2022-03-17T06:50:46.514Z\\"", '
                   '"fromDate": "2022-03-17T06:45:46.514Z", '
                   '"toDate": "2022-03-17T06:50:46.514Z", "limit": 10000}']
        queries = _remove_timestamp_from_query_ver1(queries)
        self._test_query_assertions(query, queries)

    def test_for_multiple_observation_with_timestamp(self):
        """test to multiple start stop qualifier observation query"""
        stix_pattern = "[file: hashes.MD5 = '0bbd4d92d3a0178463ef6e0ad46c986a']START " \
                       "t'2022-01-05T00:00:00.030Z' STOP t'2022-02-20T00:00:00.030Z' " \
                       "AND [ x-oca-asset:extensions.'x-sentinelone-endpoint'." \
                       "agent_version = '21.6.6.1200']START " \
                       "t'2022-01-01T00:00:00.030Z' STOP t'2022-02-28T00:00:00.030Z'"
        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        queries = ['{"query": "((tgtFileMd5 = \\"0bbd4d92d3a0178463ef6e0ad46c986a\\" '
                   'OR tgtFileOldMd5 = \\"0bbd4d92d3a0178463ef6e0ad46c986a\\" '
                   'OR srcProcImageMd5 = \\"0bbd4d92d3a0178463ef6e0ad46c986a\\" '
                   'OR tgtProcImageMd5 = \\"0bbd4d92d3a0178463ef6e0ad46c986a\\") '
                   'AND EventTime  BETWEEN \\"2022-01-05T00:00:00.030Z\\" '
                   'AND \\"2022-02-20T00:00:00.030Z\\") '
                   'OR (agentVersion = \\"21.6.6.1200\\" '
                   'AND EventTime  BETWEEN \\"2022-01-01T00:00:00.030Z\\" '
                   'AND \\"2022-02-28T00:00:00.030Z\\")", '
                   '"fromDate": "2022-01-01T00:00:00.030Z", '
                   '"toDate": "2022-02-28T00:00:00.030Z", "limit": 10000}']
        self._test_query_assertions(query, queries)

    def test_invalid_boolean_value(self):
        """test to check invalid boolean pattern"""
        stix_pattern = "[user-account:is_privileged = '2']"
        result = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert 'wrong parameter : Invalid boolean type input' in result['error']

    def test_or_operator_query(self):
        """test to check or pattern to query"""
        stix_pattern = "[x-oca-asset:extensions.'x-sentinelone-endpoint'." \
                       "endpoint_os   = 'windows' " \
                       "OR network-traffic:extensions.'x-sentinelone-network-action'." \
                       "connection_status ='SUCCESS' " \
                       "AND network-traffic:src_port > 100 ]"
        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query_ver1(query['queries'])
        queries = ['{"query": "((srcPort > \\"100\\" AND netConnStatus = \\"SUCCESS\\") '
                   'OR endpointOs = \\"WINDOWS\\") AND EventTime  '
                   'BETWEEN \\"2022-03-03T06:45:13.380Z\\" '
                   'AND \\"2022-03-03T06:50:13.380Z\\"", '
                   '"fromDate": "2022-03-03T06:45:13.380Z", '
                   '"toDate": "2022-03-03T06:50:13.380Z", "limit": 10000}']
        queries = _remove_timestamp_from_query_ver1(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_pattern_with_or_query(self):
        """test to check multiple pattern with or to query"""
        stix_pattern = "[network-traffic:extensions.'x-sentinelone-network-action'." \
                       "connection_status ='SUCCESS' " \
                       "AND network-traffic:src_port > 100] START " \
                       "t'2019-10-01T08:43:10.003Z' STOP t'2019-11-30T10:43:10.005Z' " \
                       "AND [x-oca-asset:extensions.'x-sentinelone-endpoint'." \
                       "endpoint_os = 'windows' " \
                       "OR x-oca-event:action = 'File Rename']"
        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query_ver2(query['queries'])
        queries = ['{"query": "((srcPort > \\"100\\" AND netConnStatus = \\"SUCCESS\\") '
                   'AND EventTime  BETWEEN \\"2019-10-01T08:43:10.003Z\\" '
                   'AND \\"2019-11-30T10:43:10.005Z\\") '
                   'OR ((eventType = \\"FILE RENAME\\" OR endpointOs = \\"WINDOWS\\") '
                   'AND EventTime  BETWEEN \\"2022-03-11T10:24:41.029Z\\" '
                   'AND \\"2022-03-11T10:29:41.029Z\\")", '
                   '"fromDate": "2019-10-01T08:43:10.003Z", '
                   '"toDate": "2022-03-11T10:29:41.029Z", "limit": 10000}']
        queries = _remove_timestamp_from_query_ver2(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_combination_or_pattern_query(self):
        """test to check multiple combination or operator to query"""
        stix_pattern = "[network-traffic:extensions.'x-sentinelone-network-action'." \
                       "connection_status ='SUCCESS' " \
                       "OR network-traffic:src_port > 100 " \
                       "AND x-oca-asset:extensions.'x-sentinelone-endpoint'." \
                       "endpoint_os = 'windows' " \
                       "OR process:extensions.'x-sentinelone-process'." \
                       "integrity_level = 'SYSTEM' ]"
        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query_ver1(query['queries'])
        queries = ['{"query": "((srcProcIntegrityLevel = \\"SYSTEM\\" '
                   'OR tgtProcIntegrityLevel = \\"SYSTEM\\") '
                   'OR ((endpointOs = \\"WINDOWS\\" AND srcPort > \\"100\\") '
                   'OR netConnStatus = \\"SUCCESS\\")) '
                   'AND EventTime  BETWEEN \\"2022-03-11T09:51:06.719Z\\" '
                   'AND \\"2022-03-11T09:56:06.719Z\\"", '
                   '"fromDate": "2022-03-11T09:51:06.719Z", '
                   '"toDate": "2022-03-11T09:56:06.719Z", "limit": 10000}']
        queries = _remove_timestamp_from_query_ver1(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_or_operator_query(self):
        """test to check multiple or operator to query"""
        stix_pattern = "[network-traffic:extensions.'x-sentinelone-network-action'." \
                       "connection_status ='SUCCESS' " \
                       "OR network-traffic:src_port > 100 " \
                       "OR x-oca-asset:extensions.'x-sentinelone-endpoint'." \
                       "endpoint_os = 'windows']"
        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query_ver1(query['queries'])
        queries = ['{"query": "(endpointOs = \\"WINDOWS\\" OR (srcPort > \\"100\\" '
                   'OR netConnStatus = \\"SUCCESS\\")) AND EventTime  '
                   'BETWEEN \\"2022-03-03T10:09:10.017Z\\" '
                   'AND \\"2022-03-03T10:14:10.017Z\\"", '
                   '"fromDate": "2022-03-03T10:09:10.017Z", '
                   '"toDate": "2022-03-03T10:14:10.017Z", "limit": 10000}']
        queries = _remove_timestamp_from_query_ver1(queries)
        self._test_query_assertions(query, queries)

    def test_pattern_with_enum_fields_query(self):
        """test to check enum fields to query"""
        stix_pattern = "[file:extensions.'x-sentinelone-file'.file_type IN ('PE') " \
                       "OR windows-registry-key:extensions.'x-sentinelone-registry'." \
                       "full_size = 72]"
        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query_ver1(query['queries'])
        queries = ['{"query": "(registryValueFullSize = \\"72\\" '
                   'OR tgtFileType IN (\\"PE\\")) AND EventTime  '
                   'BETWEEN \\"2022-03-11T10:30:30.099Z\\" '
                   'AND \\"2022-03-11T10:35:30.099Z\\"", '
                   '"fromDate": "2022-03-11T10:30:30.099Z", '
                   '"toDate": "2022-03-11T10:35:30.099Z", "limit": 10000}']
        queries = _remove_timestamp_from_query_ver1(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_enum_fields_query(self):
        """test to check multiple enum fields to query"""
        stix_pattern = "[network-traffic:extensions.'x-sentinelone-network-action'." \
                       "connection_status " \
                       "IN ('SUCCESS') OR " \
                       " file:extensions.'x-sentinelone-file'." \
                       "file_type IN ('PE') " \
                       "AND user-account:extensions.'x-sentinelone-login'." \
                       "login_type IN ('SYSTEM') ]"
        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query_ver1(query['queries'])
        queries = ['{"query": "((loginType IN (\\"SYSTEM\\") '
                   'AND tgtFileType IN (\\"PE\\")) OR netConnStatus '
                   'IN (\\"SUCCESS\\")) AND EventTime  '
                   'BETWEEN \\"2022-03-11T09:59:55.322Z\\" '
                   'AND \\"2022-03-11T10:04:55.322Z\\"", '
                   '"fromDate": "2022-03-11T09:59:55.322Z", '
                   '"toDate": "2022-03-11T10:04:55.322Z", "limit": 10000}']
        queries = _remove_timestamp_from_query_ver1(queries)
        self._test_query_assertions(query, queries)

    def test_invalid_enum_fields_query(self):
        """test to check invalid  enum field pattern """
        stix_pattern = "[file:extensions.'x-sentinelone-file'.file_type = 'abc']"
        result = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert result['error'] == "sentinelone connector error => " \
                                  "wrong parameter : Unsupported ENUM values provided. " \
                                  "Possible supported enum values " \
                                  "are['UNKNOWN', 'PE', 'ELF', 'MACH', 'VECT', 'PDF', " \
                                  "'COM', 'OLE', 'OPENXML', 'PKZIP', 'RAR', " \
                                  "'LZMA', 'BZIP2', 'TAR', 'CABINET', 'SFX', " \
                                  "'DOTNET', 'EICAR', 'LNK']"

    def test_invalid_enum_fields_with_in_operator(self):
        """test to check invalid  enum fields """
        stix_pattern = "[x-oca-asset:extensions.'x-sentinelone-endpoint'." \
                       "endpoint_os IN ('mac')]"
        result = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert result['error'] == "sentinelone connector error => " \
                                  "wrong parameter : Unsupported ENUM values provided. " \
                                  "Possible supported enum values " \
                                  "are['windows', 'osx', 'linux']"

    def test_invalid_enum_fields_with_multiple_element(self):
        """test to check invalid  enum fields with multiple element"""
        stix_pattern = "[x-oca-asset:extensions.'x-sentinelone-endpoint'." \
                       "endpoint_os IN ('mac') " \
                       "OR file:extensions.'x-sentinelone-file'.file_type IN ('PE')]"
        result = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert result['error'] == "sentinelone connector error => " \
                                  "wrong parameter : Unsupported ENUM values provided. " \
                                  "Possible supported enum values " \
                                  "are['windows', 'osx', 'linux']"

    def test_multiple_invalid_fields(self):
        """test to check multiple invalid fields"""
        stix_pattern = "[x-oca-asset:extensions.'x-sentinelone-endpoint'." \
                       "endpoint_os IN ('mac') " \
                       "OR file:extensions.'x-sentinelone-file'.file_type IN ('abc')]"
        result = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert result['error'] == "sentinelone connector error => " \
                                  "wrong parameter : Unsupported ENUM values provided. " \
                                  "Possible supported enum values " \
                                  "are['UNKNOWN', 'PE', 'ELF', 'MACH', 'VECT', 'PDF', " \
                                  "'COM', 'OLE', 'OPENXML', 'PKZIP', 'RAR', " \
                                  "'LZMA', 'BZIP2', 'TAR', 'CABINET', 'SFX', " \
                                  "'DOTNET', 'EICAR', 'LNK']"

    def test_indicator_field_query(self):
        """test to check indicator fields"""
        stix_pattern = "[x-sentinelone-indicator:indicator_category = 'Malware']"
        query = translation.translate('sentinelone', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query_ver1(query['queries'])
        queries = ['{"query": "indicatorCategory = \\"MALWARE\\" '
                   'AND EventTime  BETWEEN \\"2022-03-30T06:17:37.577Z\\" '
                   'AND \\"2022-03-30T06:22:37.577Z\\"", '
                   '"fromDate": "2022-03-30T06:17:37.577Z", '
                   '"toDate": "2022-03-30T06:22:37.577Z", "limit": 10000}']
        queries = _remove_timestamp_from_query_ver1(queries)
        self._test_query_assertions(query, queries)
