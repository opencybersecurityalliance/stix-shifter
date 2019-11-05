from stix_shifter.stix_translation import stix_translation
import unittest
import re

translation = stix_translation.StixTranslation()


def _remove_timestamp_from_query(queries):
    pattern = r'EventTime\s*>=\s*datetime\((\d{4})(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z\)\s*and\s*EventTime\s*<\s*' \
              r'datetime\((\d{4})(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z\)\s*'
    if isinstance(queries, list):
        return [re.sub(pattern, "", query) for query in queries]
    elif isinstance(queries, str):
        return re.sub(pattern, "", queries)


class TestStixToQuery(unittest.TestCase):
    """
    class to perform unit test case msatp translate query
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
        stix_pattern = "[file:name = 'updater.exe']"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            '(find withsource = TableName in (FileCreationEvents) where EventTime >= datetime('
            '2019-09-24T14:57:53.365122Z) and EventTime < datetime(2019-09-24T15:02:53.365122Z) | order by EventTime '
            'desc | where FileName =~ "updater.exe" or InitiatingProcessFileName =~ "updater.exe" or '
            'InitiatingProcessParentFileName =~ "updater.exe")']

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_process_comp_exp(self):
        stix_pattern = "[process:name = 'consent.exe' ]"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            '(find withsource = TableName in (ProcessCreationEvents) where EventTime >= datetime('
            '2019-09-24T14:59:03.947156Z) and EventTime < datetime(2019-09-24T15:04:03.947156Z) | order by EventTime '
            'desc | where FileName =~ "consent.exe")']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_network_comp_exp(self):
        stix_pattern = "[ipv4-addr:value = '172.16.2.22'] START t'2019-09-10T08:43:10.003Z' STOP " \
                       "t'2019-09-23T10:43:10.453Z'"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        queries = [
            '(find withsource = TableName in (NetworkCommunicationEvents) where EventTime >= datetime('
            '2019-09-10T08:43:10.003Z) and EventTime < datetime(2019-09-23T10:43:10.453Z) | order by EventTime desc | '
            'where LocalIP =~ "172.16.2.22" or RemoteIP =~ "172.16.2.22")']
        self._test_query_assertions(query, queries)

    def test_mac_comp_exp(self):
        stix_pattern = "[mac-addr:value = '48:4D:7E:9D:BD:97'] START t'2019-09-01T08:43:10.003Z' STOP " \
                       "t'2019-10-10T10:43:10.003Z'"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)

        queries = [
            '(find withsource = TableName in (NetworkCommunicationEvents) where EventTime >= datetime('
            '2019-09-01T08:43:10.003Z) and EventTime < datetime(2019-10-10T10:43:10.003Z) | extend FormattedTimeKey = '
            'bin(EventTime, 1m) | join kind= inner (MachineNetworkInfo | where EventTime >= datetime('
            '2019-09-01T08:43:10.003Z) and EventTime < datetime(2019-10-10T10:43:10.003Z) | extend FormattedTimeKey = '
            'bin(EventTime, 1m)| mvexpand parse_json(IPAddresses) | extend IP = IPAddresses.IPAddress | project '
            'EventTime ,MachineId , MacAddress, IP, FormattedTimeKey) on MachineId, $left.FormattedTimeKey == '
            '$right.FormattedTimeKey | where LocalIP == IP | where MacAddress =~ "484D7E9DBD97" | order by EventTime '
            'desc)']
        self._test_query_assertions(query, queries)

    def test_registry_comp_exp(self):
        stix_pattern = "[windows-registry-key:values[*] IN ('SD', 'Index')] START t'2019-09-01T08:43:10.003Z' STOP " \
                       "t'2019-10-10T10:43:10.003Z'"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)

        queries = [
            '(find withsource = TableName in (RegistryEvents) where EventTime >= datetime(2019-09-01T08:43:10.003Z) '
            'and EventTime < datetime(2019-10-10T10:43:10.003Z) | order by EventTime desc | where RegistryValueName '
            'in~ ("SD", "Index"))']
        self._test_query_assertions(query, queries)

    def test_directory_comp_exp(self):
        stix_pattern = "[directory:path LIKE 'ProgramData' OR ipv6-addr:value = 'fe80::4161:ca84:4dc5:f5fc'] " \
                       "START t'2019-10-01T08:43:10.003Z' STOP t'2019-10-30T10:43:10.003Z'"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)

        queries = ['(find withsource = TableName in (NetworkCommunicationEvents) where EventTime >= datetime('
                   '2019-10-01T08:43:10.003Z) and EventTime < datetime(2019-10-30T10:43:10.003Z) | order by EventTime '
                   'desc | where (LocalIP =~ "fe80::4161:ca84:4dc5:f5fc" or RemoteIP =~ "fe80::4161:ca84:4dc5:f5fc") '
                   'or (InitiatingProcessFolderPath contains "ProgramData"))']
        self._test_query_assertions(query, queries)

    def test_gt_eq_datetime_comp_exp(self):
        stix_pattern = "[process:created >= '2019-09-04T09:29:29.0882Z']"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            '(find withsource = TableName in (ProcessCreationEvents) where EventTime >= datetime('
            '2019-09-10T08:43:10.003Z) and EventTime < datetime(2019-09-23T10:43:10.453Z) | order by EventTime desc | '
            'where ProcessCreationTime >= datetime(2019-09-04T09:29:29.0882Z))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_lt_eq_datetime_comp_exp(self):
        stix_pattern = "[network-traffic:src_port < '443']"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            '(find withsource = TableName in (NetworkCommunicationEvents) where EventTime >= datetime('
            '2019-09-24T15:58:06.610239Z) and EventTime < datetime(2019-09-24T16:03:06.610239Z) | order by EventTime '
            'desc | where LocalPort < 443)']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_noteq_comp_exp(self):
        stix_pattern = "[process:name != 'consent.exe'] START t'2019-09-10T08:43:10.003Z' STOP " \
                       "t'2019-09-23T10:43:10.453Z'"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)

        queries = [
            '(find withsource = TableName in (ProcessCreationEvents) where EventTime >= datetime('
            '2019-09-10T08:43:10.003Z) and EventTime < datetime(2019-09-23T10:43:10.453Z) | order by EventTime desc | '
            'where FileName !~ "consent.exe")']
        self._test_query_assertions(query, queries)

    def test_like_comp_exp(self):
        stix_pattern = "[file:name LIKE  'upd']"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            '(find withsource = TableName in (FileCreationEvents) where EventTime >= datetime('
            '2019-09-24T15:15:27.875681Z) and EventTime < datetime(2019-09-24T15:20:27.875681Z) | order by EventTime '
            'desc | where FileName contains "upd" or InitiatingProcessFileName contains "upd" or '
            'InitiatingProcessParentFileName contains "upd")']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_matches_comp_exp(self):
        stix_pattern = "[file:name MATCHES '^chr']"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ['(find withsource = TableName in (FileCreationEvents) where EventTime >= datetime('
                   '2019-09-24T15:16:12.359886Z) and EventTime < datetime(2019-09-24T15:21:12.359886Z) | order by '
                   'EventTime desc | where FileName matches regex"(^chr)" or InitiatingProcessFileName matches '
                   'regex"(^chr)" or InitiatingProcessParentFileName matches regex"(^chr)")']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_in_comp_exp(self):
        stix_pattern = "[process:created IN ('2019-09-04T09:29:29.0882Z', '2019-09-04T09:29:29.0881372Z')]"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            '(find withsource = TableName in (ProcessCreationEvents) where EventTime >= datetime('
            '2019-09-24T15:16:53.671163Z) and EventTime < datetime(2019-09-24T15:21:53.671163Z) | order by EventTime '
            'desc | where ProcessCreationTime in~ (datetime(2019-09-04T09:29:29.0882Z), datetime('
            '2019-09-04T09:29:29.0881372Z)))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_comb_comparison_exp(self):
        stix_pattern = "[process:name IN ('consent.exe', 'reg.exe') OR file:name = 'updater.exe'] START " \
                       "t'2019-09-10T08:43:10.003Z' STOP t'2019-09-23T10:43:10.453Z'"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)

        queries = [
            '(find withsource = TableName in (ProcessCreationEvents) where EventTime >= datetime('
            '2019-09-10T08:43:10.003Z) and EventTime < datetime(2019-09-23T10:43:10.453Z) | order by EventTime desc | '
            'where (FileName =~ "updater.exe" or InitiatingProcessFileName =~ "updater.exe" or '
            'InitiatingProcessParentFileName =~ "updater.exe") or (FileName in~ ("consent.exe", "reg.exe")))']
        self._test_query_assertions(query, queries)

    def test_comb_comparison_exp_1(self):
        stix_pattern = "[network-traffic:src_port = '454' OR process:name NOT = 'python.exe'] START " \
                       "t'2019-09-10T08:43:10.003Z' STOP t'2019-09-23T10:43:10.453Z'"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)

        queries = [
            '(find withsource = TableName in (NetworkCommunicationEvents) where EventTime >= datetime('
            '2019-09-10T08:43:10.003Z) and EventTime < datetime(2019-09-23T10:43:10.453Z) | order by EventTime desc | '
            'where ((not (InitiatingProcessFileName =~ "python.exe" or InitiatingProcessParentFileName =~ '
            '"python.exe"))) or (tostring(LocalPort) =~ "454"))']
        self._test_query_assertions(query, queries)

    def test_comb_observation_obs(self):
        stix_pattern = "[process:created = '2019-09-04T09:29:29.0882Z'] OR [file:name LIKE 'upd_ter.exe']"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            'union (find withsource = TableName in (ProcessCreationEvents) where EventTime >= datetime('
            '2019-11-04T10:39:31.381Z) and EventTime < datetime(2019-11-04T10:44:31.381Z) | order by EventTime desc | '
            'where tostring(ProcessCreationTime) == datetime(2019-09-04T09:29:29.0882Z)),(find withsource = TableName '
            'in (FileCreationEvents) where EventTime >= datetime(2019-11-04T10:39:31.381Z) and EventTime < datetime('
            '2019-11-04T10:44:31.381Z) | order by EventTime desc | where FileName matches regex"(upd.ter.exe$)" or '
            'InitiatingProcessFileName matches regex"(upd.ter.exe$)" or InitiatingProcessParentFileName matches '
            'regex"(upd.ter.exe$)")']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)
