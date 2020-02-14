from stix_shifter.stix_translation import stix_translation
import unittest
import re

translation = stix_translation.StixTranslation()


def _remove_timestamp_from_query(queries):
    pattern = r'eventDateTime \w{2} \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z'
    if isinstance(queries, list):
        return [re.sub(pattern, "", query) for query in queries]
    elif isinstance(queries, str):
        return re.sub(pattern, "", queries)


class TestStixToQuery(unittest.TestCase):
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

    def test_file_comp_exp(self):
        stix_pattern = "[file:name = 'services.exe']"
        query = translation.translate('azure_sentinel', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ["(fileStates/any(query1:tolower(query1/name) eq 'services.exe')) and (eventDateTime ge "
                   "2019-12-24T09:21:51.505Z and eventDateTime le 2019-12-24T09:26:51.505Z)"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_process_comp_exp(self):
        stix_pattern = "[process:name = 'svchost.exe']"
        query = translation.translate('azure_sentinel', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ["(processes/any(query1:tolower(query1/name) eq 'svchost.exe')) and (eventDateTime ge "
                   "2019-12-24T09:22:44.667Z and eventDateTime le 2019-12-24T09:27:44.667Z)"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_network_comp_exp(self):
        stix_pattern = "[ipv4-addr:value = '172.16.2.22'] START t'2019-09-10T08:43:10.003Z' STOP " \
                       "t'2019-09-23T10:43:10.453Z'"
        query = translation.translate('azure_sentinel', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ["((networkConnections/any(query1:contains(tolower(query1/sourceAddress), "
                   "'172.16.2.22')) or networkConnections/any(query1:contains(tolower("
                   "query1/destinationAddress), '172.16.2.22')))) and (eventDateTime ge "
                   "2019-09-10T08:43:10.003Z and eventDateTime le 2019-09-23T10:43:10.453Z)"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_file_directory_exp(self):
        stix_pattern = "[file:parent_directory_ref.path = 'system32']" \
                       "START t'2019-10-01T08:43:10.003Z' STOP t'2019-10-30T10:43:10.003Z'"
        query = translation.translate('azure_sentinel', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ["(fileStates/any(query1:contains(tolower(query1/path), 'system32'))) and ("
                   "eventDateTime ge 2019-10-01T08:43:10.003Z and eventDateTime le "
                   "2019-10-30T10:43:10.003Z)"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_directory_path_exp(self):
        stix_pattern = "[directory:path = 'windows']"
        query = translation.translate('azure_sentinel', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ["(fileStates/any(query1:contains(tolower(query1/path), 'windows'))) and (eventDateTime ge "
                   "2019-12-24T09:46:34.835Z and eventDateTime le 2019-12-24T09:51:34.835Z)"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_noteq_comp_exp(self):
        stix_pattern = "[process:name != 'services.exe'] START t'2019-09-10T08:43:10.003Z' STOP " \
                       "t'2019-09-23T10:43:10.453Z'"
        query = translation.translate('azure_sentinel', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ["(processes/any(query1:tolower(query1/name) ne 'services.exe')) and (eventDateTime ge "
                   "2019-09-10T08:43:10.003Z and eventDateTime le 2019-09-23T10:43:10.453Z)"]
        queries = _remove_timestamp_from_query(queries)

        self._test_query_assertions(query, queries)

    def test_like_comp_exp(self):
        stix_pattern = "[file:name LIKE 'svc']"
        query = translation.translate('azure_sentinel', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ["(fileStates/any(query1:contains(tolower(query1/name), 'svc'))) and (eventDateTime ge "
                   "2019-12-24T09:48:37.359Z and eventDateTime le 2019-12-24T09:53:37.359Z)"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_matches_comp_exp(self):
        stix_pattern = "[file:name MATCHES 'serv']"
        query = translation.translate('azure_sentinel', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ["(fileStates/any(query1:contains(tolower(query1/name), 'serv'))) and (eventDateTime ge "
                   "2019-12-24T09:49:14.586Z and eventDateTime le 2019-12-24T09:54:14.586Z)"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_custom_in_comp_exp(self):
        stix_pattern = "[x-com-msazure-sentinel:tenant_id NOT IN ('Sb73e5ba','b73e5ba8')" \
                       "AND x-com-msazure-sentinel-alert:title LIKE 'Suspicious']"
        query = translation.translate('azure_sentinel', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ["(contains(tolower(title), 'suspicious') and tolower(azureTenantId) ne 'sb73e5ba' and tolower("
                   "azureTenantId) ne 'b73e5ba8') and (eventDateTime ge 2019-12-27T04:50:48.593Z and eventDateTime le "
                   "2019-12-27T04:55:48.593Z)"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_in_comp_exp(self):
        stix_pattern = "[process:name IN ('services.exe', 'svchost.exe')]"
        query = translation.translate('azure_sentinel', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ["(processes/any(query1:tolower(query1/name) eq 'services.exe') or processes/any(query1:tolower("
                   "query1/name) eq 'svchost.exe')) and (eventDateTime ge 2019-12-24T09:50:39.638Z and eventDateTime "
                   "le 2019-12-24T09:55:39.638Z)"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_comb_comparison_exp_1(self):
        stix_pattern = "[process:name IN ('services.exe', 'svchost.exe') OR file:name = 'notepad.exe'] START " \
                       "t'2019-09-10T08:43:10.003Z' STOP t'2019-09-23T10:43:10.453Z'"
        query = translation.translate('azure_sentinel', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ["(fileStates/any(query1:tolower(query1/name) eq 'notepad.exe') or processes/any(query2:tolower("
                   "query2/name) eq 'services.exe') or processes/any(query2:tolower(query2/name) eq 'svchost.exe')) "
                   "and (eventDateTime ge 2019-09-10T08:43:10.003Z and eventDateTime le 2019-09-23T10:43:10.453Z)"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_comb_comparison_exp_2(self):
        stix_pattern = "[network-traffic:src_port = '454' OR process:name NOT = 'powershell.exe'] START " \
                       "t'2019-09-10T08:43:10.003Z' STOP t'2019-09-23T10:43:10.453Z'"
        query = translation.translate('azure_sentinel', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ["(processes/any(query1:tolower(query1/name) ne 'powershell.exe') or networkConnections/any("
                   "query2:tolower(query2/sourcePort) eq '454')) and (eventDateTime ge 2019-09-10T08:43:10.003Z and "
                   "eventDateTime le 2019-09-23T10:43:10.453Z)"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_comb_observation_obs(self):
        stix_pattern = "[process:name = 'services.exe'] OR [network-traffic:dst_port >= 100]"
        query = translation.translate('azure_sentinel', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ["(processes/any(query1:tolower(query1/name) eq 'services.exe')) and (eventDateTime ge "
                   "2020-01-03T06:33:04.859Z and eventDateTime le 2020-01-03T06:38:04.859Z)",
                   "(networkConnections/any(query2:tolower(query2/destinationPort) ge '100')) and (eventDateTime ge "
                   "2020-01-03T06:33:04.859Z and eventDateTime le 2020-01-03T06:38:04.859Z)"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_comb_observation_obs_qualifier_one(self):
        stix_pattern = "([process:pid IN (110,220)] OR [network-traffic:src_ref.value = '52.94.233.129' AND " \
                       "user-account:account_last_login = '2019-09-23T10:43:10.453Z']) START " \
                       "t'2019-09-10T08:43:10.003Z' STOP t'2019-09-23T10:43:10.453Z'"
        query = translation.translate('azure_sentinel', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ['(processes/any(query1:query1/processId eq 110) or processes/any(query1:query1/processId eq 220)) '
                   'and (eventDateTime ge 2019-09-10T08:43:10.003Z and eventDateTime le 2019-09-23T10:43:10.453Z)',
                   "(userStates/any(query2:query2/logonDateTime eq 2019-09-23t10:43:10.453z) and "
                   "networkConnections/any(query3:contains(tolower(query3/sourceAddress), '52.94.233.129'))) and ("
                   "eventDateTime ge 2019-09-10T08:43:10.003Z and eventDateTime le 2019-09-23T10:43:10.453Z)"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_comb_observation_obs_qualifier_two(self):
        stix_pattern = "([file:hashes.'SHA-1' LIKE 'daf67'] OR [file:hashes.'SHA-1' = " \
                       "'b6d237154f2e528f0b503b58b025862d66b02b73'] OR [" \
                       "x-com-msazure-sentinel-alert:vendor = 'Microsoft'] AND [" \
                       "x-com-msazure-sentinel-alert:provider LIKE 'Microsoft']) START " \
                       "t'2019-09-10T08:43:10.003Z' STOP t'2019-09-23T10:43:10.453Z'"
        query = translation.translate('azure_sentinel', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ["((fileStates/any(query1:query1/fileHash/hashType eq 'sha1') and fileStates/any(query1:contains("
                   "tolower(query1/fileHash/hashValue), 'daf67')))) and (eventDateTime ge 2019-09-10T08:43:10.003Z "
                   "and eventDateTime le 2019-09-23T10:43:10.453Z)", "((fileStates/any("
                                                                     "query2:query2/fileHash/hashType eq 'sha1') and "
                                                                     "fileStates/any(query2:tolower("
                                                                     "query2/fileHash/hashValue) eq "
                                                                     "'b6d237154f2e528f0b503b58b025862d66b02b73'))) "
                                                                     "and (eventDateTime ge 2019-09-10T08:43:10.003Z "
                                                                     "and eventDateTime le "
                                                                     "2019-09-23T10:43:10.453Z)",
                   "(vendorInformation/vendor eq 'Microsoft') and (eventDateTime ge 2019-09-10T08:43:10.003Z and "
                   "eventDateTime le 2019-09-23T10:43:10.453Z)", "(contains(vendorInformation/provider, 'Microsoft')) "
                                                                 "and (eventDateTime ge 2019-09-10T08:43:10.003Z and "
                                                                 "eventDateTime le 2019-09-23T10:43:10.453Z)"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)
