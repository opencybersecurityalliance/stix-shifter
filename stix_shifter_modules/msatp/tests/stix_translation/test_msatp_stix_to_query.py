from stix_shifter.stix_translation import stix_translation
import unittest
import re

translation = stix_translation.StixTranslation()


def _remove_timestamp_from_query(queries):
    pattern = r'Timestamp\s*>=\s*datetime\((\d{4})(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z\)\s*and\s*Timestamp\s*<\s*' \
              r'datetime\((\d{4})(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z\)\s*'
    if isinstance(queries, list):
        return [re.sub(pattern, "", query) for query in queries]
    elif isinstance(queries, str):
        return re.sub(pattern, "", queries)


class TestQueryTranslator(unittest.TestCase):
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
        query['queries'] = [_remove_timestamp_from_query(q) for q in query['queries']]

        queries = ['(find withsource = TableName in (DeviceFileEvents)  where | order by Timestamp desc | where ('
                   'FileName =~ "updater.exe") or (InitiatingProcessFileName =~ "updater.exe") or ('
                   'InitiatingProcessParentFileName =~ "updater.exe"))', '(find withsource = TableName in ('
                                                                         'DeviceProcessEvents)  where | order by '
                                                                         'Timestamp desc | where (FileName =~ '
                                                                         '"updater.exe") or ('
                                                                         'InitiatingProcessFileName =~ "updater.exe") '
                                                                         'or (InitiatingProcessParentFileName =~ '
                                                                         '"updater.exe"))', '(find withsource = '
                                                                                            'TableName in ('
                                                                                            'DeviceNetworkEvents)  '
                                                                                            'where | order by '
                                                                                            'Timestamp desc | where ('
                                                                                            'InitiatingProcessFileName =~ "updater.exe") or (InitiatingProcessParentFileName =~ "updater.exe"))',
                   '(find withsource = TableName in (DeviceRegistryEvents)  where | order by Timestamp desc | where ('
                   'InitiatingProcessFileName =~ "updater.exe") or (InitiatingProcessParentFileName =~ '
                   '"updater.exe"))',
                   '(find withsource = TableName in (DeviceEvents)  where | order by Timestamp desc | where (FileName '
                   '=~ "updater.exe") or (InitiatingProcessFileName =~ "updater.exe") or ('
                   'InitiatingProcessParentFileName =~ "updater.exe"))']

        queries = [_remove_timestamp_from_query(q) for q in queries]
        self._test_query_assertions(query, queries)

    def test_process_comp_exp(self):
        stix_pattern = "[process:name = 'consent.exe']"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = [_remove_timestamp_from_query(q) for q in query['queries']]

        queries = [
            '(find withsource = TableName in (DeviceProcessEvents)  where | order by Timestamp desc | where (FileName '
            '=~ "consent.exe") or (InitiatingProcessFileName =~ "consent.exe") or (InitiatingProcessParentFileName =~ '
            '"consent.exe"))',
            '(find withsource = TableName in (DeviceNetworkEvents)  where | order by Timestamp desc | where ('
            'InitiatingProcessFileName =~ "consent.exe") or (InitiatingProcessParentFileName =~ "consent.exe"))',
            '(find withsource = TableName in (DeviceRegistryEvents)  where | order by Timestamp desc | where ('
            'InitiatingProcessFileName =~ "consent.exe") or (InitiatingProcessParentFileName =~ "consent.exe"))',
            '(find withsource = TableName in (DeviceEvents)  where | order by Timestamp desc | where ('
            'InitiatingProcessFileName =~ "consent.exe") or (InitiatingProcessParentFileName =~ "consent.exe"))']

        queries = [_remove_timestamp_from_query(q) for q in queries]
        self._test_query_assertions(query, queries)

    def test_network_comp_exp(self):
        stix_pattern = "[ipv4-addr:value = '172.16.2.22'] START t'2019-09-10T08:43:10.003Z' STOP " \
                       "t'2019-09-23T10:43:10.453Z'"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = [_remove_timestamp_from_query(q) for q in query['queries']]

        queries = ['(find withsource = TableName in (DeviceNetworkEvents)  where | order by Timestamp desc | where ('
                   'LocalIP =~ "172.16.2.22") or (RemoteIP =~ "172.16.2.22"))', '(find withsource = TableName in ('
                                                                                'DeviceEvents)  where | order by '
                                                                                'Timestamp desc | where (RemoteIP =~ '
                                                                                '"172.16.2.22") or (LocalIP =~ '
                                                                                '"172.16.2.22"))']

        queries = [_remove_timestamp_from_query(q) for q in queries]
        self._test_query_assertions(query, queries)

    def test_mac_comp_exp(self):
        stix_pattern = "[mac-addr:value = '48:4D:7E:9D:BD:97'] START t'2019-09-01T08:43:10.003Z' STOP " \
                       "t'2019-10-10T10:43:10.003Z'"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = [_remove_timestamp_from_query(q) for q in query['queries']]

        queries = ['(find withsource = TableName in (DeviceNetworkInfo)  where Timestamp >= datetime('
                   '2019-09-01T08:43:10.003Z) and Timestamp < datetime(2019-10-10T10:43:10.003Z)  | order by '
                   'Timestamp desc | where MacAddress =~ "484D7E9DBD97")']

        queries = [_remove_timestamp_from_query(q) for q in queries]
        self._test_query_assertions(query, queries)

    def test_registry_comp_exp(self):
        stix_pattern = "[windows-registry-key:values[*] IN ('SD', 'Index')] START t'2019-09-01T08:43:10.003Z' STOP " \
                       "t'2019-10-10T10:43:10.003Z'"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = [_remove_timestamp_from_query(q) for q in query['queries']]

        queries = ['(find withsource = TableName in (DeviceRegistryEvents)  where Timestamp >= datetime('
                   '2019-09-01T08:43:10.003Z) and Timestamp < datetime(2019-10-10T10:43:10.003Z)  | order by '
                   'Timestamp desc | where RegistryValueName in~ ("SD", "Index"))']

        queries = [_remove_timestamp_from_query(q) for q in queries]
        self._test_query_assertions(query, queries)

    def test_directory_comp_exp(self):
        stix_pattern = "[directory:path LIKE 'ProgramData' OR ipv6-addr:value = 'fe80::4161:ca84:4dc5:f5fc'] " \
                       "START t'2019-10-01T08:43:10.003Z' STOP t'2019-10-30T10:43:10.003Z'"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = [_remove_timestamp_from_query(q) for q in query['queries']]

        queries = ['(find withsource = TableName in (DeviceNetworkEvents)  where | order by Timestamp desc | where ('
                   'InitiatingProcessFolderPath contains "ProgramData") or ((LocalIP =~ "fe80::4161:ca84:4dc5:f5fc") '
                   'or (RemoteIP =~ "fe80::4161:ca84:4dc5:f5fc")))', '(find withsource = TableName in (DeviceEvents)  '
                                                                     'where | order by Timestamp desc | where (('
                                                                     'FolderPath contains "ProgramData") or ('
                                                                     'InitiatingProcessFolderPath contains '
                                                                     '"ProgramData")) or ((RemoteIP =~ '
                                                                     '"fe80::4161:ca84:4dc5:f5fc") or (LocalIP =~ '
                                                                     '"fe80::4161:ca84:4dc5:f5fc")))',
                   '(find withsource = TableName in (DeviceFileEvents)  where | order by Timestamp desc | where (('
                   'FolderPath contains "ProgramData") or (InitiatingProcessFolderPath contains "ProgramData")))',
                   '(find withsource = TableName in (DeviceProcessEvents)  where | order by Timestamp desc | where (('
                   'FolderPath contains "ProgramData") or (InitiatingProcessFolderPath contains "ProgramData")))',
                   '(find withsource = TableName in (DeviceRegistryEvents)  where | order by Timestamp desc | where ('
                   'InitiatingProcessFolderPath contains "ProgramData"))']

        queries = [_remove_timestamp_from_query(q) for q in queries]
        self._test_query_assertions(query, queries)

    def test_alert_comp_exp(self):
        stix_pattern = "[x-ibm-finding:alert_id = '1234567890_1234567890']" \
                       "START t'2019-10-01T08:43:10.003Z' STOP t'2019-10-30T10:43:10.003Z'"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = [_remove_timestamp_from_query(q) for q in query['queries']]

        queries = ['(find withsource = TableName in (DeviceAlertEvents)  where Timestamp >= '
                   'datetime(2022-03-08T00:16:00.000Z) and Timestamp < datetime(2022-03-09T00:16:00.000Z)  | '
                   'order by Timestamp desc | where AlertId =~ "1234567890_1234567890")']

        queries = [_remove_timestamp_from_query(q) for q in queries]
        self._test_query_assertions(query, queries)

    def test_gt_eq_datetime_comp_exp(self):
        stix_pattern = "[process:created >= '2019-09-04T09:29:29.0882Z']"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = [_remove_timestamp_from_query(q) for q in query['queries']]

        queries = ['(find withsource = TableName in (DeviceProcessEvents)  where Timestamp >= datetime('
                   '2021-04-28T01:00:13.120Z) and Timestamp < datetime(2021-07-06T11:40:13.120Z)  | order by '
                   'Timestamp desc | where (ProcessCreationTime >= datetime(2019-09-04T09:29:29.0882Z)) or ('
                   'InitiatingProcessParentCreationTime >= datetime(2019-09-04T09:29:29.0882Z)))', '(find withsource '
                                                                                                   '= TableName in ('
                                                                                                   'DeviceNetworkEvents)  where Timestamp >= datetime(2021-04-28T01:00:13.120Z) and Timestamp < datetime(2021-07-06T11:40:13.120Z)  | order by Timestamp desc | where (InitiatingProcessCreationTime >= datetime(2019-09-04T09:29:29.0882Z)) or (InitiatingProcessParentCreationTime >= datetime(2019-09-04T09:29:29.0882Z)))',
                   '(find withsource = TableName in (DeviceRegistryEvents)  where Timestamp >= datetime('
                   '2021-04-28T01:00:13.120Z) and Timestamp < datetime(2021-07-06T11:40:13.120Z)  | order by '
                   'Timestamp desc | where (InitiatingProcessCreationTime >= datetime(2019-09-04T09:29:29.0882Z)) or '
                   '(InitiatingProcessParentCreationTime >= datetime(2019-09-04T09:29:29.0882Z)))',
                   '(find withsource = TableName in (DeviceFileEvents)  where Timestamp >= datetime('
                   '2021-04-28T01:00:13.120Z) and Timestamp < datetime(2021-07-06T11:40:13.120Z)  | order by '
                   'Timestamp desc | where (InitiatingProcessCreationTime >= datetime(2019-09-04T09:29:29.0882Z)) or '
                   '(InitiatingProcessParentCreationTime >= datetime(2019-09-04T09:29:29.0882Z)))']

        queries = [_remove_timestamp_from_query(q) for q in queries]
        self._test_query_assertions(query, queries)

    def test_lt_eq_datetime_comp_exp(self):
        stix_pattern = "[network-traffic:src_port < '443']"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = [_remove_timestamp_from_query(q) for q in query['queries']]

        queries = ['(find withsource = TableName in (DeviceNetworkEvents)  where | order by Timestamp desc | where '
                   'LocalPort < 443)', '(find withsource = TableName in (DeviceEvents)  where | order by Timestamp '
                                       'desc | where LocalPort < 443)']

        queries = [_remove_timestamp_from_query(q) for q in queries]
        self._test_query_assertions(query, queries)

    def test_noteq_comp_exp(self):
        stix_pattern = "[process:name != 'consent.exe'] START t'2019-09-10T08:43:10.003Z' STOP " \
                       "t'2019-09-23T10:43:10.453Z'"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = [_remove_timestamp_from_query(q) for q in query['queries']]

        queries = ['(find withsource = TableName in (DeviceProcessEvents)  where | order by Timestamp desc | where ('
                   'FileName !~ "consent.exe") or (InitiatingProcessFileName !~ "consent.exe") or ('
                   'InitiatingProcessParentFileName !~ "consent.exe"))', '(find withsource = TableName in ('
                                                                         'DeviceNetworkEvents)  where | order by '
                                                                         'Timestamp desc | where ('
                                                                         'InitiatingProcessFileName !~ "consent.exe") '
                                                                         'or (InitiatingProcessParentFileName !~ '
                                                                         '"consent.exe"))', '(find withsource = '
                                                                                            'TableName in ('
                                                                                            'DeviceRegistryEvents)  '
                                                                                            'where | order by '
                                                                                            'Timestamp desc | where ('
                                                                                            'InitiatingProcessFileName !~ "consent.exe") or (InitiatingProcessParentFileName !~ "consent.exe"))',
                   '(find withsource = TableName in (DeviceEvents)  where | order by Timestamp desc | where ('
                   'InitiatingProcessFileName !~ "consent.exe") or (InitiatingProcessParentFileName !~ '
                   '"consent.exe"))']

        queries = [_remove_timestamp_from_query(q) for q in queries]
        self._test_query_assertions(query, queries)

    def test_like_comp_exp(self):
        stix_pattern = "[file:name LIKE  'upd']"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = [_remove_timestamp_from_query(q) for q in query['queries']]

        queries = ['(find withsource = TableName in (DeviceFileEvents)  where | order by Timestamp desc | where ('
                   'FileName contains "upd") or (InitiatingProcessFileName contains "upd") or ('
                   'InitiatingProcessParentFileName contains "upd"))', '(find withsource = TableName in ('
                                                                       'DeviceProcessEvents)  where | order by '
                                                                       'Timestamp desc | where (FileName contains '
                                                                       '"upd") or (InitiatingProcessFileName contains '
                                                                       '"upd") or (InitiatingProcessParentFileName '
                                                                       'contains "upd"))', '(find withsource = '
                                                                                           'TableName in ('
                                                                                           'DeviceNetworkEvents)  '
                                                                                           'where | order by '
                                                                                           'Timestamp desc | where ('
                                                                                           'InitiatingProcessFileName '
                                                                                           'contains "upd") or ('
                                                                                           'InitiatingProcessParentFileName contains "upd"))',
                   '(find withsource = TableName in (DeviceRegistryEvents)  where | order by Timestamp desc | where (InitiatingProcessFileName contains "upd") or (InitiatingProcessParentFileName contains "upd"))',
                   '(find withsource = TableName in (DeviceEvents)  where | order by Timestamp desc | where (FileName contains "upd") or (InitiatingProcessFileName contains "upd") or (InitiatingProcessParentFileName contains "upd"))']

        queries = [_remove_timestamp_from_query(q) for q in queries]
        self._test_query_assertions(query, queries)

    def test_matches_comp_exp(self):
        stix_pattern = "[file:name MATCHES '^chr']"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = [_remove_timestamp_from_query(q) for q in query['queries']]

        queries = ['(find withsource = TableName in (DeviceFileEvents)  where | order by Timestamp desc | where ('
                   'FileName matches regex"(^chr)") or (InitiatingProcessFileName matches regex"(^chr)") or ('
                   'InitiatingProcessParentFileName matches regex"(^chr)"))', '(find withsource = TableName in ('
                                                                              'DeviceProcessEvents)  where | order by '
                                                                              'Timestamp desc | where (FileName '
                                                                              'matches regex"(^chr)") or ('
                                                                              'InitiatingProcessFileName matches '
                                                                              'regex"(^chr)") or ('
                                                                              'InitiatingProcessParentFileName '
                                                                              'matches regex"(^chr)"))',
                   '(find withsource = TableName in (DeviceNetworkEvents)  where | order by Timestamp desc | where ('
                   'InitiatingProcessFileName matches regex"(^chr)") or (InitiatingProcessParentFileName matches '
                   'regex"(^chr)"))', '(find withsource = TableName in (DeviceRegistryEvents)  where | order by '
                                      'Timestamp desc | where (InitiatingProcessFileName matches regex"(^chr)") or ('
                                      'InitiatingProcessParentFileName matches regex"(^chr)"))', '(find withsource = '
                                                                                                 'TableName in ('
                                                                                                 'DeviceEvents)  '
                                                                                                 'where | order by '
                                                                                                 'Timestamp desc | '
                                                                                                 'where (FileName '
                                                                                                 'matches regex"('
                                                                                                 '^chr)") or ('
                                                                                                 'InitiatingProcessFileName matches regex"(^chr)") or (InitiatingProcessParentFileName matches regex"(^chr)"))']

        queries = [_remove_timestamp_from_query(q) for q in queries]
        self._test_query_assertions(query, queries)

    def test_in_comp_exp(self):
        stix_pattern = "[process:created IN ('2019-09-04T09:29:29.0882Z', '2019-09-04T09:29:29.0881372Z')]"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = [_remove_timestamp_from_query(q) for q in query['queries']]

        queries = ['(find withsource = TableName in (DeviceProcessEvents)  where Timestamp >= datetime('
                   '2021-04-28T01:15:43.809Z) and Timestamp < datetime(2021-07-06T11:55:43.809Z)  | order by '
                   'Timestamp desc | where (ProcessCreationTime in~ (datetime(2019-09-04T09:29:29.0882Z), '
                   'datetime(2019-09-04T09:29:29.0881372Z))) or (InitiatingProcessParentCreationTime in~ (datetime('
                   '2019-09-04T09:29:29.0882Z), datetime(2019-09-04T09:29:29.0881372Z))))', '(find withsource = '
                                                                                            'TableName in ('
                                                                                            'DeviceNetworkEvents)  '
                                                                                            'where Timestamp >= '
                                                                                            'datetime('
                                                                                            '2021-04-28T01:15:43.809Z'
                                                                                            ') and Timestamp < '
                                                                                            'datetime('
                                                                                            '2021-07-06T11:55:43.809Z'
                                                                                            ')  | order by Timestamp '
                                                                                            'desc | where ('
                                                                                            'InitiatingProcessCreationTime in~ (datetime(2019-09-04T09:29:29.0882Z), datetime(2019-09-04T09:29:29.0881372Z))) or (InitiatingProcessParentCreationTime in~ (datetime(2019-09-04T09:29:29.0882Z), datetime(2019-09-04T09:29:29.0881372Z))))',
                   '(find withsource = TableName in (DeviceRegistryEvents)  where Timestamp >= datetime('
                   '2021-04-28T01:15:43.809Z) and Timestamp < datetime(2021-07-06T11:55:43.809Z)  | order by '
                   'Timestamp desc | where (InitiatingProcessCreationTime in~ (datetime(2019-09-04T09:29:29.0882Z), '
                   'datetime(2019-09-04T09:29:29.0881372Z))) or (InitiatingProcessParentCreationTime in~ (datetime('
                   '2019-09-04T09:29:29.0882Z), datetime(2019-09-04T09:29:29.0881372Z))))',
                   '(find withsource = TableName in (DeviceFileEvents)  where Timestamp >= datetime('
                   '2021-04-28T01:15:43.809Z) and Timestamp < datetime(2021-07-06T11:55:43.809Z)  | order by '
                   'Timestamp desc | where (InitiatingProcessCreationTime in~ (datetime(2019-09-04T09:29:29.0882Z), '
                   'datetime(2019-09-04T09:29:29.0881372Z))) or (InitiatingProcessParentCreationTime in~ (datetime('
                   '2019-09-04T09:29:29.0882Z), datetime(2019-09-04T09:29:29.0881372Z))))']

        queries = [_remove_timestamp_from_query(q) for q in queries]
        self._test_query_assertions(query, queries)

    def test_comb_comparison_exp(self):
        stix_pattern = "[process:name IN ('consent.exe', 'reg.exe') OR file:name = 'updater.exe'] START " \
                       "t'2019-09-10T08:43:10.003Z' STOP t'2019-09-23T10:43:10.453Z'"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = [_remove_timestamp_from_query(q) for q in query['queries']]

        queries = [
            '(find withsource = TableName in (DeviceFileEvents)  where | order by Timestamp desc | where ((FileName '
            '=~ "updater.exe") or (InitiatingProcessFileName =~ "updater.exe") or (InitiatingProcessParentFileName =~ '
            '"updater.exe")))',
            '(find withsource = TableName in (DeviceProcessEvents)  where | order by Timestamp desc | where (('
            'FileName in~ ("consent.exe", "reg.exe")) or (InitiatingProcessFileName in~ ("consent.exe", "reg.exe")) '
            'or (InitiatingProcessParentFileName in~ ("consent.exe", "reg.exe"))) or ((FileName =~ "updater.exe") or '
            '(InitiatingProcessFileName =~ "updater.exe") or (InitiatingProcessParentFileName =~ "updater.exe")))',
            '(find withsource = TableName in (DeviceNetworkEvents)  where | order by Timestamp desc | where (('
            'InitiatingProcessFileName in~ ("consent.exe", "reg.exe")) or (InitiatingProcessParentFileName in~ ('
            '"consent.exe", "reg.exe"))) or ((InitiatingProcessFileName =~ "updater.exe") or ('
            'InitiatingProcessParentFileName =~ "updater.exe")))',
            '(find withsource = TableName in (DeviceRegistryEvents)  where | order by Timestamp desc | where (('
            'InitiatingProcessFileName in~ ("consent.exe", "reg.exe")) or (InitiatingProcessParentFileName in~ ('
            '"consent.exe", "reg.exe"))) or ((InitiatingProcessFileName =~ "updater.exe") or ('
            'InitiatingProcessParentFileName =~ "updater.exe")))',
            '(find withsource = TableName in (DeviceEvents)  where | order by Timestamp desc | where (('
            'InitiatingProcessFileName in~ ("consent.exe", "reg.exe")) or (InitiatingProcessParentFileName in~ ('
            '"consent.exe", "reg.exe"))) or ((FileName =~ "updater.exe") or (InitiatingProcessFileName =~ '
            '"updater.exe") or (InitiatingProcessParentFileName =~ "updater.exe")))']

        queries = [_remove_timestamp_from_query(q) for q in queries]
        self._test_query_assertions(query, queries)

    def test_comb_comparison_exp_1(self):
        stix_pattern = "[network-traffic:src_port = '454' OR process:name NOT = 'python.exe'] START " \
                       "t'2019-09-10T08:43:10.003Z' STOP t'2019-09-23T10:43:10.453Z'"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = [_remove_timestamp_from_query(q) for q in query['queries']]

        queries = [
            '(find withsource = TableName in (DeviceProcessEvents)  where | order by Timestamp desc | where (not (('
            'FileName =~ "python.exe") or (InitiatingProcessFileName =~ "python.exe") or ('
            'InitiatingProcessParentFileName =~ "python.exe"))))',
            '(find withsource = TableName in (DeviceNetworkEvents)  where | order by Timestamp desc | where ('
            'tostring(LocalPort) =~ "454") or (not ((InitiatingProcessFileName =~ "python.exe") or ('
            'InitiatingProcessParentFileName =~ "python.exe"))))',
            '(find withsource = TableName in (DeviceRegistryEvents)  where | order by Timestamp desc | where (not (('
            'InitiatingProcessFileName =~ "python.exe") or (InitiatingProcessParentFileName =~ "python.exe"))))',
            '(find withsource = TableName in (DeviceEvents)  where | order by Timestamp desc | where (tostring('
            'LocalPort) =~ "454") or (not ((InitiatingProcessFileName =~ "python.exe") or ('
            'InitiatingProcessParentFileName =~ "python.exe"))))']

        queries = [_remove_timestamp_from_query(q) for q in queries]
        self._test_query_assertions(query, queries)

    # check about partesis
    def test_comb_observation_obs(self):
        stix_pattern = "[process:created = '2019-09-04T09:29:29.0882Z'] OR [file:name LIKE 'upd_ter.exe']"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = [_remove_timestamp_from_query(q) for q in query['queries']]

        queries = ['(find withsource = TableName in (DeviceProcessEvents)  where | order by Timestamp desc | where (('
                   'FileName matches regex"(upd.ter.exe$)") or (InitiatingProcessFileName matches regex"('
                   'upd.ter.exe$)") or (InitiatingProcessParentFileName matches regex"(upd.ter.exe$)")) or (('
                   'tostring(ProcessCreationTime) == datetime(2019-09-04T09:29:29.0882Z)) or (tostring('
                   'InitiatingProcessParentCreationTime) == datetime(2019-09-04T09:29:29.0882Z))))',
                   '(find withsource = TableName in (DeviceNetworkEvents)  where | order by Timestamp desc | where (('
                   'InitiatingProcessFileName matches regex"(upd.ter.exe$)") or (InitiatingProcessParentFileName '
                   'matches regex"(upd.ter.exe$)")) or ((tostring(InitiatingProcessCreationTime) == datetime('
                   '2019-09-04T09:29:29.0882Z)) or (tostring(InitiatingProcessParentCreationTime) == datetime('
                   '2019-09-04T09:29:29.0882Z))))', '(find withsource = TableName in (DeviceRegistryEvents)  where | '
                                                    'order by Timestamp desc | where ((InitiatingProcessFileName '
                                                    'matches regex"(upd.ter.exe$)") or ('
                                                    'InitiatingProcessParentFileName matches regex"(upd.ter.exe$)")) '
                                                    'or ((tostring(InitiatingProcessCreationTime) == datetime('
                                                    '2019-09-04T09:29:29.0882Z)) or (tostring('
                                                    'InitiatingProcessParentCreationTime) == datetime('
                                                    '2019-09-04T09:29:29.0882Z))))', '(find withsource = TableName in '
                                                                                     '(DeviceFileEvents)  where | '
                                                                                     'order by Timestamp desc | where '
                                                                                     '((FileName matches regex"('
                                                                                     'upd.ter.exe$)") or ('
                                                                                     'InitiatingProcessFileName '
                                                                                     'matches regex"(upd.ter.exe$)") '
                                                                                     'or ('
                                                                                     'InitiatingProcessParentFileName '
                                                                                     'matches regex"(upd.ter.exe$)")) '
                                                                                     'or ((tostring('
                                                                                     'InitiatingProcessCreationTime) '
                                                                                     '== datetime('
                                                                                     '2019-09-04T09:29:29.0882Z)) or '
                                                                                     '(tostring('
                                                                                     'InitiatingProcessParentCreationTime) == datetime(2019-09-04T09:29:29.0882Z))))',
                   '(find withsource = TableName in (DeviceEvents)  where | order by Timestamp desc | where (('
                   'FileName matches regex"(upd.ter.exe$)") or (InitiatingProcessFileName matches regex"('
                   'upd.ter.exe$)") or (InitiatingProcessParentFileName matches regex"(upd.ter.exe$)")))']

        queries = [_remove_timestamp_from_query(q) for q in queries]
        self._test_query_assertions(query, queries)

    def test_and_op_comb_comparison_exp(self):
        stix_pattern = "[ipv4-addr:value = '9.147.31.113' AND process:name = 'python3']"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            '(find withsource = TableName in (DeviceNetworkEvents)  where | order by Timestamp desc | where ((LocalIP '
            '=~ "9.147.31.113") or (RemoteIP =~ "9.147.31.113")) and ((InitiatingProcessFileName =~ "python3") or ('
            'InitiatingProcessParentFileName =~ "python3")))',
            '(find withsource = TableName in (DeviceEvents)  where | order by Timestamp desc | where ((RemoteIP =~ '
            '"9.147.31.113") or (LocalIP =~ "9.147.31.113")) and ((InitiatingProcessFileName =~ "python3") or ('
            'InitiatingProcessParentFileName =~ "python3")))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)
