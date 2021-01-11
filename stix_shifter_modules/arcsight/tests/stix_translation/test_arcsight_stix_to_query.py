from stix_shifter.stix_translation import stix_translation
import unittest
import json

translation = stix_translation.StixTranslation()


def _remove_timestamp_from_query(queries):
    if isinstance(queries, list):
        query_list = []
        for query in queries:
            query_dict = json.loads(query)
            query_dict.pop("start_time")
            query_dict.pop("end_time")
            query_list.append(query_dict)
        return query_list


class TestQueryTranslator(unittest.TestCase):
    """
    class to perform unit test case azure_sentinel translate query
    """

    def _test_query_assertions(self, query, queries):
        """
        to assert the each query in the list against expected result
        """
        self.assertIsInstance(query, dict)
        self.assertIsInstance(query['queries'], list)
        for index, each_query in enumerate(query.get('queries'), start=0):
            self.assertEqual(each_query, queries[index])

    def test_file_comp_exp_one(self):
        stix_pattern = "[file:name = 'nslookup.exe']"
        query = translation.translate('arcsight', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ['{"query": "fileName = nslookup.exe", "start_time": "2020-08-14T04:22:47.470Z", "end_time": '
                   '"2020-08-14T04:27:47.470Z"}']

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_file_comp_exp_two(self):
        stix_pattern = "[file:name = 'Microsoft Powershell']"
        query = translation.translate('arcsight', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ['{"query": "fileName = \\"Microsoft Powershell\\"", "start_time": "2020-08-14T04:22:47.470Z", '
                   '"end_time": "2020-08-14T04:27:47.470Z"}']

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_process_comp_exp(self):
        stix_pattern = "[process:name = 'powershell.exe'] START t'2020-06-18T14:20:00Z' STOP t'2020-06-18T14:30:00Z'"
        query = translation.translate('arcsight', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ['{"query": "(destinationProcessName = powershell.exe OR sourceProcessName = powershell.exe)", '
                   '"start_time": "2020-06-18T14:20:00.000Z", "end_time": "2020-06-18T14:30:00.000Z"}']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_network_comp_exp(self):
        stix_pattern = "[ipv4-addr:value = '10.10.20.6'] START t'2020-06-18T14:20:00Z' STOP t'2020-06-18T14:30:00Z'"
        query = translation.translate('arcsight', 'query', '{}', stix_pattern)

        queries = ['{"query": "(sourceAddress = 10.10.20.6 OR destinationAddress = 10.10.20.6)", "start_time": '
                   '"2020-06-18T14:20:00.000Z", "end_time": "2020-06-18T14:30:00.000Z"}']

        self._test_query_assertions(query, queries)

    def test_file_directory_exp(self):
        stix_pattern = "[file:parent_directory_ref.path = 'system32']" \
                       "START t'2020-06-18T14:20:00Z' STOP t'2020-06-18T14:30:00Z'"
        query = translation.translate('arcsight', 'query', '{}', stix_pattern)

        queries = ['{"query": "filePath = system32", "start_time": "2020-06-18T14:20:00.000Z", "end_time": '
                   '"2020-06-18T14:30:00.000Z"}']

        self._test_query_assertions(query, queries)

    def test_directory_path_exp(self):
        stix_pattern = "[directory:path = 'system32']"
        query = translation.translate('arcsight', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ['{"query": "filePath = system32", "start_time": "2020-06-18T14:20:00.000Z", "end_time": '
                   '"2020-06-18T14:30:00.000Z"}']

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_noteq_comp_exp(self):
        stix_pattern = "[process:name NOT = 'powershell.exe'] START " \
                       "t'2020-08-14T06:36:27.287Z' STOP t'2020-08-14T06:41:27.287Z'"
        query = translation.translate('arcsight', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ['{"query": "NOT (destinationProcessName = powershell.exe OR sourceProcessName = powershell.exe)", '
                   '"start_time": "2020-08-14T06:36:27.287.000Z", "end_time": '
                   '"2020-08-14T06:41:27.287.000Z"}']
        queries = _remove_timestamp_from_query(queries)

        self._test_query_assertions(query, queries)

    def test_like_comp_exp(self):
        stix_pattern = "[file:name LIKE '%tomcat']"
        query = translation.translate('arcsight', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ['{"query": "fileName = *tomcat", "start_time": "2020-08-14T05:47:41.261Z", "end_time": '
                   '"2020-08-14T05:52:41.261Z"}']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_matches_comp_exp(self):
        stix_pattern = "[file:name MATCHES '.exe']"
        query = translation.translate('arcsight', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['{"query": "fileName CONTAINS .exe", "start_time": "2020-08-14T05:47:41.261Z", "end_time": '
                   '"2020-08-14T05:52:41.261Z"}']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_custom_in_comp_exp(self):
        stix_pattern = "[x-arcsight-event-device:product LIKE 'Microsoft%' AND " \
                       "x-arcsight-event-device:vendor IN ('Sysmon', 'windows')] START t'2020-06-18T14:20:00Z' " \
                       "STOP t'2020-06-18T14:30:00Z'"
        query = translation.translate('arcsight', 'query', '{}', stix_pattern)

        queries = ['{"query": "deviceVendor IN [\\"Sysmon\\", \\"windows\\"] AND deviceProduct = Microsoft*", '
                   '"start_time": "2020-06-18T14:20:00.000Z", "end_time": "2020-06-18T14:30:00.000Z"}']
        self._test_query_assertions(query, queries)

    def test_in_comp_exp(self):
        stix_pattern = "[network-traffic:dst_port IN ('443', '3389')] START t'2020-06-18T14:20:00Z' " \
                       "STOP t'2020-06-18T14:30:00Z'"
        query = translation.translate('arcsight', 'query', '{}', stix_pattern)

        queries = ['{"query": "destinationPort IN [\\"443\\", \\"3389\\"]", "start_time": "2020-06-18T14:20:00.000Z", '
                   '"end_time": "2020-06-18T14:30:00.000Z"}']

        self._test_query_assertions(query, queries)

    def test_comb_comparison_exp_1(self):
        stix_pattern = "[process:name IN ('notepad.exe', 'nslookup.exe') OR file:name = 'notepad.exe'] START " \
                       "t'2020-08-14T06:36:27.287Z' STOP t'2020-08-14T06:41:27.287Z'"
        query = translation.translate('arcsight', 'query', '{}', stix_pattern)

        queries = ['{"query": "fileName = notepad.exe OR (destinationProcessName IN [\\"notepad.exe\\", '
                   '\\"nslookup.exe\\"] OR sourceProcessName IN [\\"notepad.exe\\", \\"nslookup.exe\\"])", '
                   '"start_time": "2020-08-14T06:36:27.287.000Z", "end_time": '
                   '"2020-08-14T06:41:27.287.000Z"}']

        self._test_query_assertions(query, queries)

    def test_comb_comparison_exp_2(self):
        stix_pattern = "[network-traffic:src_port NOT > '443' OR process:name NOT = 'powershell.exe'] START " \
                       "t'2020-06-18T14:20:00Z' STOP t'2020-06-18T14:30:00Z' "
        query = translation.translate('arcsight', 'query', '{}', stix_pattern)

        queries = [
            '{"query": "NOT (destinationProcessName = powershell.exe OR '
            'sourceProcessName = powershell.exe) OR NOT sourcePort > 443", '
            '"start_time": "2020-06-18T14:20:00.000Z", "end_time": "2020-06-18T14:30:00.000Z"}']

        self._test_query_assertions(query, queries)

    def test_comb_observation_obs(self):
        stix_pattern = "([process:name = 'notepad.exe'] OR [network-traffic:dst_port >= '100']) START " \
                       "t'2020-08-14T07:16:00Z' STOP t'2020-08-14T07:21:00Z'"
        query = translation.translate('arcsight', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            '{"query": "((destinationProcessName = notepad.exe OR sourceProcessName = notepad.exe)) OR '
            '(destinationPort >= 100)", "start_time": "2020-08-14T07:16:00.678Z", "end_time": '
            '"2020-08-14T07:21:00.678Z"}']

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_comb_observation_obs_qualifier_one(self):
        stix_pattern = "([network-traffic:dst_port IN (443, 3389)] OR [network-traffic:src_ref.value = '104.10.10.6' " \
                       "AND user-account:account_login = 'ADMINISTRATOR']) START t'2020-06-18T14:20:00Z' STOP " \
                       "t'2020-06-18T14:30:00Z'"
        query = translation.translate('arcsight', 'query', '{}', stix_pattern)

        queries = ['{"query": "(destinationPort IN [443, 3389]) OR ((destinationUserName = ADMINISTRATOR OR '
                   'sourceUserName = ADMINISTRATOR) AND sourceAddress = 104.10.10.6)", "start_time": '
                   '"2020-06-18T14:20:00.000Z", "end_time": '
                   '"2020-06-18T14:30:00.000Z"}']

        self._test_query_assertions(query, queries)

    def test_comb_observation_obs_qualifier_two(self):
        stix_pattern = "([file:name LIKE '%.exe'] OR [file:name LIKE '%.sh'] OR [x-arcsight-event-device:vendor = " \
                       "'Sysmon'] AND [x-arcsight-event-device:product LIKE 'Microsoft%']) START " \
                       "t'2020-06-18T14:20:00Z' STOP t'2020-06-18T14:30:00Z' "
        query = translation.translate('arcsight', 'query', '{}', stix_pattern)

        queries = ['{"query": "((fileName = *.exe) OR (fileName = *.sh)) OR ((deviceVendor = Sysmon) AND ('
                   'deviceProduct = Microsoft*))", "start_time": "2020-06-18T14:20:00.000Z", "end_time": '
                   '"2020-06-18T14:30:00.000Z"}']

        self._test_query_assertions(query, queries)

    def test_multiple_observation_obs_qualifier_one(self):
        stix_pattern = "[ipv4-addr:value = '51.143.106.177'] START t'2020-07-01T08:43:10Z' STOP " \
                       "t'2020-07-31T10:43:10Z' OR [network-traffic:protocols[*] = 'http']" \
                       " START t'2020-06-01T08:43:10Z' STOP t'2020-08-31T10:43:10Z'"
        query = translation.translate('arcsight', 'query', '{}', stix_pattern)

        queries = ['{"query": "(sourceAddress = 51.143.106.177 OR destinationAddress = 51.143.106.177)", '
                   '"start_time": "2020-07-01T08:43:10.000Z", "end_time": "2020-07-31T10:43:10.000Z"}',
                   '{"query": "(transportProtocol = http OR applicationProtocol = http)", '
                   '"start_time": "2020-06-01T08:43:10.000Z", "end_time": "2020-08-31T10:43:10.000Z"}']

        self._test_query_assertions(query, queries)

    def test_multiple_observation_obs_qualifier_two(self):
        stix_pattern = "[windows-registry-key:key LIKE '%driverVersion'] START t'2020-07-01T08:43:10Z' STOP " \
                       "t'2020-07-31T10:43:10Z' OR [ipv6-addr:value = 'fe80:0:0:0:1411:a12d:7746:e3a']" \
                       " START t'2020-06-01T08:43:10Z' STOP t'2020-08-31T10:43:10Z'"
        query = translation.translate('arcsight', 'query', '{}', stix_pattern)

        queries = ['{"query": "filePath = *driverVersion", "start_time": "2020-07-01T08:43:10.000Z", '
                   '"end_time": "2020-07-31T10:43:10.000Z"}', '{"query": "fe80:0:0:0:1411:a12d:7746:e3a", '
                   '"start_time": "2020-06-01T08:43:10.000Z", "end_time": "2020-08-31T10:43:10.000Z"}']

        self._test_query_assertions(query, queries)

    def test_non_indexed_fields_exp_one(self):
        stix_pattern = "[ipv6-addr:value = 'fe80:0:0:0:1411:a12d:7746:e3a']"
        query = translation.translate('arcsight', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ['{"query": "fe80:0:0:0:1411:a12d:7746:e3a", "start_time": "2020-08-14T04:22:47.470Z", "end_time": '
                   '"2020-08-14T04:27:47.470Z"}']

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_non_indexed_fields_exp_two(self):
        stix_pattern = "[file:hashes.'SHA-1' = '27F2684A8552E80C0825B55743BD8A4C6E71799E']"
        query = translation.translate('arcsight', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ['{"query": "27F2684A8552E80C0825B55743BD8A4C6E71799E", "start_time": "2020-08-14T04:22:47.470Z", '
                   '"end_time": "2020-08-14T04:27:47.470Z"}']

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_issubnet_comp_exp(self):
        stix_pattern = "[ipv4-addr:value ISSUBSET '172.31.64.0/20']"
        query = translation.translate('arcsight', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ['{"query": "(sourceAddress insubnet \\"172.31.64.0/20\\" OR destinationAddress insubnet '
                   '\\"172.31.64.0/20\\")", "start_time": "2020-08-14T04:22:47.470Z", "end_time": '
                   '"2020-08-14T04:27:47.470Z"}']

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)
