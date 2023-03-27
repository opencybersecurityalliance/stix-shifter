from stix_shifter.stix_translation import stix_translation
import unittest
import re

translation = stix_translation.StixTranslation()


def _remove_timestamp_from_query(queries):
    pattern = r'datetime\((\d{4})(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z\)'
    if isinstance(queries, list):
        return [re.sub(pattern, "<<timestamp>>", query) for query in queries]
    elif isinstance(queries, str):
        return re.sub(pattern, "<<timestamp>>", queries)


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
            self.assertEqual(queries[index], each_query)

    def test_file_comp_exp(self):
        stix_pattern = "[file:name = 'updater.exe']"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [('union (find withsource = TableName in (DeviceFileEvents)  where Timestamp >= '
                    '<<timestamp>> and Timestamp < <<timestamp>>  | order by Timestamp desc | '
                    'where (FileName =~ "updater.exe") or (InitiatingProcessFileName =~ '
                    '"updater.exe") or (InitiatingProcessParentFileName =~ "updater.exe")),(find '
                    'withsource = TableName in (DeviceProcessEvents)  where Timestamp >= '
                    '<<timestamp>> and Timestamp < <<timestamp>>  | order by Timestamp desc | '
                    'where (FileName =~ "updater.exe") or (InitiatingProcessFileName =~ '
                    '"updater.exe") or (InitiatingProcessParentFileName =~ "updater.exe")),(find '
                    'withsource = TableName in (DeviceNetworkEvents)  where Timestamp >= '
                    '<<timestamp>> and Timestamp < <<timestamp>>  | order by Timestamp desc | '
                    'where (InitiatingProcessFileName =~ "updater.exe") or '
                    '(InitiatingProcessParentFileName =~ "updater.exe")),(find withsource = '
                    'TableName in (DeviceRegistryEvents)  where Timestamp >= <<timestamp>> and '
                    'Timestamp < <<timestamp>>  | order by Timestamp desc | where '
                    '(InitiatingProcessFileName =~ "updater.exe") or '
                    '(InitiatingProcessParentFileName =~ "updater.exe")),(find withsource = '
                    'TableName in (DeviceEvents)  where Timestamp >= <<timestamp>> and Timestamp '
                    '< <<timestamp>>  | order by Timestamp desc | where (FileName =~ '
                    '"updater.exe") or (InitiatingProcessFileName =~ "updater.exe") or '
                    '(InitiatingProcessParentFileName =~ "updater.exe")),(find withsource = '
                    'TableName in (DeviceImageLoadEvents)  where Timestamp >= <<timestamp>> and '
                    'Timestamp < <<timestamp>>  | order by Timestamp desc | where (FileName =~ '
                    '"updater.exe") or (InitiatingProcessFileName =~ "updater.exe") or '
                    '(InitiatingProcessParentFileName =~ "updater.exe"))')]
        self._test_query_assertions(query, queries)

    def test_process_comp_exp(self):
        stix_pattern = "[process:name = 'consent.exe']"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            ('union (find withsource = TableName in (DeviceProcessEvents)  where Timestamp '
             '>= <<timestamp>> and Timestamp < <<timestamp>>  | order by Timestamp desc | '
             'where (FileName =~ "consent.exe") or (InitiatingProcessFileName =~ '
             '"consent.exe")),(find withsource = TableName in (DeviceEvents)  where '
             'Timestamp >= <<timestamp>> and Timestamp < <<timestamp>>  | order by '
             'Timestamp desc | where (FileName =~ "consent.exe") or '
             '(InitiatingProcessFileName =~ "consent.exe")),(find withsource = TableName '
             'in (DeviceFileEvents)  where Timestamp >= <<timestamp>> and Timestamp < '
             '<<timestamp>>  | order by Timestamp desc | where InitiatingProcessFileName '
             '=~ "consent.exe"),(find withsource = TableName in (DeviceNetworkEvents)  '
             'where Timestamp >= <<timestamp>> and Timestamp < <<timestamp>>  | order by '
             'Timestamp desc | where InitiatingProcessFileName =~ "consent.exe"),(find '
             'withsource = TableName in (DeviceRegistryEvents)  where Timestamp >= '
             '<<timestamp>> and Timestamp < <<timestamp>>  | order by Timestamp desc | '
             'where InitiatingProcessFileName =~ "consent.exe"),(find withsource = '
             'TableName in (DeviceImageLoadEvents)  where Timestamp >= <<timestamp>> and '
             'Timestamp < <<timestamp>>  | order by Timestamp desc | where '
             'InitiatingProcessFileName =~ "consent.exe")')]
        self._test_query_assertions(query, queries)

    def test_network_comp_exp(self):
        stix_pattern = "[ipv4-addr:value = '172.16.2.22'] START t'2019-09-10T08:43:10.003Z' STOP " \
                       "t'2019-09-23T10:43:10.453Z'"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [
            ('union (find withsource = TableName in (DeviceNetworkEvents)  where Timestamp '
             '>= <<timestamp>> and Timestamp < <<timestamp>>  | order by Timestamp desc | '
             'where (LocalIP =~ "172.16.2.22") or (RemoteIP =~ "172.16.2.22")),(find '
             'withsource = TableName in (DeviceEvents)  where Timestamp >= <<timestamp>> '
             'and Timestamp < <<timestamp>>  | order by Timestamp desc | where (RemoteIP '
             '=~ "172.16.2.22") or (LocalIP =~ "172.16.2.22"))')]
        self._test_query_assertions(query, queries)

    def test_mac_comp_exp(self):
        stix_pattern = "[mac-addr:value = '48:4D:7E:9D:BD:97'] START t'2019-09-01T08:43:10.003Z' STOP " \
                       "t'2019-10-10T10:43:10.003Z'"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            '(find withsource = TableName in (DeviceNetworkInfo)  where Timestamp >= datetime('
            '2019-09-01T08:43:10.003Z) and Timestamp < datetime(2019-10-10T10:43:10.003Z)  | order by Timestamp desc '
            '| where MacAddress =~ "484D7E9DBD97")']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_registry_comp_exp(self):
        stix_pattern = "[windows-registry-key:values[*] IN ('SD', 'Index')] START t'2019-09-01T08:43:10.003Z' STOP " \
                       "t'2019-10-10T10:43:10.003Z'"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            ('union (find withsource = TableName in (DeviceRegistryEvents)  where '
             'Timestamp >= <<timestamp>> and Timestamp < <<timestamp>>  | order by '
             'Timestamp desc | where RegistryValueName in~ ("SD", "Index")),(find '
             'withsource = TableName in (DeviceEvents)  where Timestamp >= <<timestamp>> '
             'and Timestamp < <<timestamp>>  | order by Timestamp desc | where '
             'RegistryValueName in~ ("SD", "Index"))')]
        self._test_query_assertions(query, queries)

    def test_directory_comp_exp(self):
        stix_pattern = "[directory:path LIKE 'ProgramData' OR ipv6-addr:value = 'fe80::4161:ca84:4dc5:f5fc'] " \
                       "START t'2019-10-01T08:43:10.003Z' STOP t'2019-10-30T10:43:10.003Z'"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [('union (find withsource = TableName in (DeviceNetworkEvents)  where Timestamp '
                    '>= <<timestamp>> and Timestamp < <<timestamp>>  | order by Timestamp desc | '
                    'where (InitiatingProcessFolderPath contains "ProgramData") or ((LocalIP =~ '
                    '"fe80::4161:ca84:4dc5:f5fc") or (RemoteIP =~ '
                    '"fe80::4161:ca84:4dc5:f5fc"))),(find withsource = TableName in '
                    '(DeviceEvents)  where Timestamp >= <<timestamp>> and Timestamp < '
                    '<<timestamp>>  | order by Timestamp desc | where ((FolderPath contains '
                    '"ProgramData") or (InitiatingProcessFolderPath contains "ProgramData")) or '
                    '((RemoteIP =~ "fe80::4161:ca84:4dc5:f5fc") or (LocalIP =~ '
                    '"fe80::4161:ca84:4dc5:f5fc"))),(find withsource = TableName in '
                    '(DeviceFileEvents)  where Timestamp >= <<timestamp>> and Timestamp < '
                    '<<timestamp>>  | order by Timestamp desc | where ((FolderPath contains '
                    '"ProgramData") or (InitiatingProcessFolderPath contains '
                    '"ProgramData"))),(find withsource = TableName in (DeviceProcessEvents)  '
                    'where Timestamp >= <<timestamp>> and Timestamp < <<timestamp>>  | order by '
                    'Timestamp desc | where ((FolderPath contains "ProgramData") or '
                    '(InitiatingProcessFolderPath contains "ProgramData"))),(find withsource = '
                    'TableName in (DeviceRegistryEvents)  where Timestamp >= <<timestamp>> and '
                    'Timestamp < <<timestamp>>  | order by Timestamp desc | where '
                    '(InitiatingProcessFolderPath contains "ProgramData")),(find withsource = '
                    'TableName in (DeviceImageLoadEvents)  where Timestamp >= <<timestamp>> and '
                    'Timestamp < <<timestamp>>  | order by Timestamp desc | where ((FolderPath '
                    'contains "ProgramData") or (InitiatingProcessFolderPath contains '
                    '"ProgramData")))')]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_gt_eq_datetime_comp_exp(self):
        stix_pattern = "[process:created >= '2019-09-04T09:29:29.0882Z']"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            ('union (find withsource = TableName in (DeviceProcessEvents)  where Timestamp '
             '>= <<timestamp>> and Timestamp < <<timestamp>>  | order by Timestamp desc | '
             'where ProcessCreationTime >= <<timestamp>>),(find withsource = TableName in '
             '(DeviceEvents)  where Timestamp >= <<timestamp>> and Timestamp < '
             '<<timestamp>>  | order by Timestamp desc | where ProcessCreationTime >= '
             '<<timestamp>>),(find withsource = TableName in (DeviceNetworkEvents)  where '
             'Timestamp >= <<timestamp>> and Timestamp < <<timestamp>>  | order by '
             'Timestamp desc | where InitiatingProcessCreationTime >= <<timestamp>>),(find '
             'withsource = TableName in (DeviceRegistryEvents)  where Timestamp >= '
             '<<timestamp>> and Timestamp < <<timestamp>>  | order by Timestamp desc | '
             'where InitiatingProcessCreationTime >= <<timestamp>>),(find withsource = '
             'TableName in (DeviceFileEvents)  where Timestamp >= <<timestamp>> and '
             'Timestamp < <<timestamp>>  | order by Timestamp desc | where '
             'InitiatingProcessCreationTime >= <<timestamp>>),(find withsource = TableName '
             'in (DeviceImageLoadEvents)  where Timestamp >= <<timestamp>> and Timestamp < '
             '<<timestamp>>  | order by Timestamp desc | where '
             'InitiatingProcessCreationTime >= <<timestamp>>)')]
        self._test_query_assertions(query, queries)

    def test_lt_eq_datetime_comp_exp(self):
        stix_pattern = "[network-traffic:src_port < '443']"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            ('union (find withsource = TableName in (DeviceNetworkEvents)  where Timestamp '
             '>= <<timestamp>> and Timestamp < <<timestamp>>  | order by Timestamp desc | '
             'where LocalPort < 443),(find withsource = TableName in (DeviceEvents)  where '
             'Timestamp >= <<timestamp>> and Timestamp < <<timestamp>>  | order by '
             'Timestamp desc | where LocalPort < 443)')]
        self._test_query_assertions(query, queries)

    def test_noteq_comp_exp(self):
        stix_pattern = "[process:name != 'consent.exe'] START t'2019-09-10T08:43:10.003Z' STOP " \
                       "t'2019-09-23T10:43:10.453Z'"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            ('union (find withsource = TableName in (DeviceProcessEvents)  where Timestamp '
             '>= <<timestamp>> and Timestamp < <<timestamp>>  | order by Timestamp desc | '
             'where (FileName !~ "consent.exe") or (InitiatingProcessFileName !~ '
             '"consent.exe")),(find withsource = TableName in (DeviceEvents)  where '
             'Timestamp >= <<timestamp>> and Timestamp < <<timestamp>>  | order by '
             'Timestamp desc | where (FileName !~ "consent.exe") or '
             '(InitiatingProcessFileName !~ "consent.exe")),(find withsource = TableName '
             'in (DeviceFileEvents)  where Timestamp >= <<timestamp>> and Timestamp < '
             '<<timestamp>>  | order by Timestamp desc | where InitiatingProcessFileName '
             '!~ "consent.exe"),(find withsource = TableName in (DeviceNetworkEvents)  '
             'where Timestamp >= <<timestamp>> and Timestamp < <<timestamp>>  | order by '
             'Timestamp desc | where InitiatingProcessFileName !~ "consent.exe"),(find '
             'withsource = TableName in (DeviceRegistryEvents)  where Timestamp >= '
             '<<timestamp>> and Timestamp < <<timestamp>>  | order by Timestamp desc | '
             'where InitiatingProcessFileName !~ "consent.exe"),(find withsource = '
             'TableName in (DeviceImageLoadEvents)  where Timestamp >= <<timestamp>> and '
             'Timestamp < <<timestamp>>  | order by Timestamp desc | where '
             'InitiatingProcessFileName !~ "consent.exe")')]
        self._test_query_assertions(query, queries)

    def test_like_comp_exp(self):
        stix_pattern = "[file:name LIKE  'upd']"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            ('union (find withsource = TableName in (DeviceFileEvents)  where Timestamp >= '
             '<<timestamp>> and Timestamp < <<timestamp>>  | order by Timestamp desc | '
             'where (FileName contains "upd") or (InitiatingProcessFileName contains '
             '"upd") or (InitiatingProcessParentFileName contains "upd")),(find withsource '
             '= TableName in (DeviceProcessEvents)  where Timestamp >= <<timestamp>> and '
             'Timestamp < <<timestamp>>  | order by Timestamp desc | where (FileName '
             'contains "upd") or (InitiatingProcessFileName contains "upd") or '
             '(InitiatingProcessParentFileName contains "upd")),(find withsource = '
             'TableName in (DeviceNetworkEvents)  where Timestamp >= <<timestamp>> and '
             'Timestamp < <<timestamp>>  | order by Timestamp desc | where '
             '(InitiatingProcessFileName contains "upd") or '
             '(InitiatingProcessParentFileName contains "upd")),(find withsource = '
             'TableName in (DeviceRegistryEvents)  where Timestamp >= <<timestamp>> and '
             'Timestamp < <<timestamp>>  | order by Timestamp desc | where '
             '(InitiatingProcessFileName contains "upd") or '
             '(InitiatingProcessParentFileName contains "upd")),(find withsource = '
             'TableName in (DeviceEvents)  where Timestamp >= <<timestamp>> and Timestamp '
             '< <<timestamp>>  | order by Timestamp desc | where (FileName contains "upd") '
             'or (InitiatingProcessFileName contains "upd") or '
             '(InitiatingProcessParentFileName contains "upd")),(find withsource = '
             'TableName in (DeviceImageLoadEvents)  where Timestamp >= <<timestamp>> and '
             'Timestamp < <<timestamp>>  | order by Timestamp desc | where (FileName '
             'contains "upd") or (InitiatingProcessFileName contains "upd") or '
             '(InitiatingProcessParentFileName contains "upd"))')]
        self._test_query_assertions(query, queries)

    def test_matches_comp_exp(self):
        stix_pattern = "[file:name MATCHES '^chr']"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [('union (find withsource = TableName in (DeviceFileEvents)  where Timestamp >= '
                    '<<timestamp>> and Timestamp < <<timestamp>>  | order by Timestamp desc | '
                    'where (FileName matches regex"(^chr)") or (InitiatingProcessFileName matches '
                    'regex"(^chr)") or (InitiatingProcessParentFileName matches '
                    'regex"(^chr)")),(find withsource = TableName in (DeviceProcessEvents)  where '
                    'Timestamp >= <<timestamp>> and Timestamp < <<timestamp>>  | order by '
                    'Timestamp desc | where (FileName matches regex"(^chr)") or '
                    '(InitiatingProcessFileName matches regex"(^chr)") or '
                    '(InitiatingProcessParentFileName matches regex"(^chr)")),(find withsource = '
                    'TableName in (DeviceNetworkEvents)  where Timestamp >= <<timestamp>> and '
                    'Timestamp < <<timestamp>>  | order by Timestamp desc | where '
                    '(InitiatingProcessFileName matches regex"(^chr)") or '
                    '(InitiatingProcessParentFileName matches regex"(^chr)")),(find withsource = '
                    'TableName in (DeviceRegistryEvents)  where Timestamp >= <<timestamp>> and '
                    'Timestamp < <<timestamp>>  | order by Timestamp desc | where '
                    '(InitiatingProcessFileName matches regex"(^chr)") or '
                    '(InitiatingProcessParentFileName matches regex"(^chr)")),(find withsource = '
                    'TableName in (DeviceEvents)  where Timestamp >= <<timestamp>> and Timestamp '
                    '< <<timestamp>>  | order by Timestamp desc | where (FileName matches '
                    'regex"(^chr)") or (InitiatingProcessFileName matches regex"(^chr)") or '
                    '(InitiatingProcessParentFileName matches regex"(^chr)")),(find withsource = '
                    'TableName in (DeviceImageLoadEvents)  where Timestamp >= <<timestamp>> and '
                    'Timestamp < <<timestamp>>  | order by Timestamp desc | where (FileName '
                    'matches regex"(^chr)") or (InitiatingProcessFileName matches regex"(^chr)") '
                    'or (InitiatingProcessParentFileName matches regex"(^chr)"))')]
        self._test_query_assertions(query, queries)

    def test_in_comp_exp(self):
        stix_pattern = "[process:created IN ('2019-09-04T09:29:29.0882Z', '2019-09-04T09:29:29.0881372Z')]"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            ('union (find withsource = TableName in (DeviceProcessEvents)  where Timestamp '
             '>= <<timestamp>> and Timestamp < <<timestamp>>  | order by Timestamp desc | '
             'where ProcessCreationTime in~ (<<timestamp>>, <<timestamp>>)),(find '
             'withsource = TableName in (DeviceEvents)  where Timestamp >= <<timestamp>> '
             'and Timestamp < <<timestamp>>  | order by Timestamp desc | where '
             'ProcessCreationTime in~ (<<timestamp>>, <<timestamp>>)),(find withsource = '
             'TableName in (DeviceNetworkEvents)  where Timestamp >= <<timestamp>> and '
             'Timestamp < <<timestamp>>  | order by Timestamp desc | where '
             'InitiatingProcessCreationTime in~ (<<timestamp>>, <<timestamp>>)),(find '
             'withsource = TableName in (DeviceRegistryEvents)  where Timestamp >= '
             '<<timestamp>> and Timestamp < <<timestamp>>  | order by Timestamp desc | '
             'where InitiatingProcessCreationTime in~ (<<timestamp>>, '
             '<<timestamp>>)),(find withsource = TableName in (DeviceFileEvents)  where '
             'Timestamp >= <<timestamp>> and Timestamp < <<timestamp>>  | order by '
             'Timestamp desc | where InitiatingProcessCreationTime in~ (<<timestamp>>, '
             '<<timestamp>>)),(find withsource = TableName in (DeviceImageLoadEvents)  '
             'where Timestamp >= <<timestamp>> and Timestamp < <<timestamp>>  | order by '
             'Timestamp desc | where InitiatingProcessCreationTime in~ (<<timestamp>>, '
             '<<timestamp>>))')]
        self._test_query_assertions(query, queries)

    def test_comb_comparison_exp(self):
        stix_pattern = "[process:name IN ('consent.exe', 'reg.exe') OR file:name = 'updater.exe'] START " \
                       "t'2019-09-10T08:43:10.003Z' STOP t'2019-09-23T10:43:10.453Z'"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        # process name mapping:
        # DeviceEvents, DeviceProcessEvents - FileName or InitiatingProcessFileName
        # DeviceFileEvents, DeviceNetworkEvents, DeviceRegistryEvents, DeviceImageLoadEvents - InitiatingProcessFileName
        # file name mapping:
        # DeviceEvents, DeviceProcessEvents, DeviceFileEvents -
        #       FileName or InitiatingProcessFileName or InitiatingProcessParentFileName
        # DeviceNetworkEvents, DeviceRegistryEvents, DeviceImageLoadEvents -
        #       InitiatingProcessFileName or InitiatingProcessParentFileName

        queries = [
            (('union (find withsource = TableName in (DeviceFileEvents)  where Timestamp >= '
              '<<timestamp>> and Timestamp < <<timestamp>>  | order by Timestamp desc | '
              'where (InitiatingProcessFileName in~ ("consent.exe", "reg.exe")) or '
              '((FileName =~ "updater.exe") or (InitiatingProcessFileName =~ "updater.exe") '
              'or (InitiatingProcessParentFileName =~ "updater.exe"))),(find withsource = '
              'TableName in (DeviceProcessEvents)  where Timestamp >= <<timestamp>> and '
              'Timestamp < <<timestamp>>  | order by Timestamp desc | where ((FileName in~ '
              '("consent.exe", "reg.exe")) or (InitiatingProcessFileName in~ '
              '("consent.exe", "reg.exe"))) or ((FileName =~ "updater.exe") or '
              '(InitiatingProcessFileName =~ "updater.exe") or '
              '(InitiatingProcessParentFileName =~ "updater.exe"))),(find withsource = '
              'TableName in (DeviceNetworkEvents)  where Timestamp >= <<timestamp>> and '
              'Timestamp < <<timestamp>>  | order by Timestamp desc | where '
              '(InitiatingProcessFileName in~ ("consent.exe", "reg.exe")) or '
              '((InitiatingProcessFileName =~ "updater.exe") or '
              '(InitiatingProcessParentFileName =~ "updater.exe"))),(find withsource = '
              'TableName in (DeviceRegistryEvents)  where Timestamp >= <<timestamp>> and '
              'Timestamp < <<timestamp>>  | order by Timestamp desc | where '
              '(InitiatingProcessFileName in~ ("consent.exe", "reg.exe")) or '
              '((InitiatingProcessFileName =~ "updater.exe") or '
              '(InitiatingProcessParentFileName =~ "updater.exe"))),(find withsource = '
              'TableName in (DeviceEvents)  where Timestamp >= <<timestamp>> and Timestamp '
              '< <<timestamp>>  | order by Timestamp desc | where ((FileName in~ '
              '("consent.exe", "reg.exe")) or (InitiatingProcessFileName in~ '
              '("consent.exe", "reg.exe"))) or ((FileName =~ "updater.exe") or '
              '(InitiatingProcessFileName =~ "updater.exe") or '
              '(InitiatingProcessParentFileName =~ "updater.exe"))),(find withsource = '
              'TableName in (DeviceImageLoadEvents)  where Timestamp >= <<timestamp>> and '
              'Timestamp < <<timestamp>>  | order by Timestamp desc | where '
              '(InitiatingProcessFileName in~ ("consent.exe", "reg.exe")) or ((FileName =~ '
              '"updater.exe") or (InitiatingProcessFileName =~ "updater.exe") or '
              '(InitiatingProcessParentFileName =~ "updater.exe")))'))
        ]
        self._test_query_assertions(query, queries)

    def test_comb_comparison_exp_1(self):
        stix_pattern = "[network-traffic:src_port = '454' OR process:name NOT = 'python.exe'] START " \
                       "t'2019-09-10T08:43:10.003Z' STOP t'2019-09-23T10:43:10.453Z'"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            (('union (find withsource = TableName in (DeviceProcessEvents)  where Timestamp '
              '>= <<timestamp>> and Timestamp < <<timestamp>>  | order by Timestamp desc | '
              'where (not ((FileName =~ "python.exe") or (InitiatingProcessFileName =~ '
              '"python.exe")))),(find withsource = TableName in (DeviceEvents)  where '
              'Timestamp >= <<timestamp>> and Timestamp < <<timestamp>>  | order by '
              'Timestamp desc | where (tostring(LocalPort) =~ "454") or (not ((FileName =~ '
              '"python.exe") or (InitiatingProcessFileName =~ "python.exe")))),(find '
              'withsource = TableName in (DeviceFileEvents)  where Timestamp >= '
              '<<timestamp>> and Timestamp < <<timestamp>>  | order by Timestamp desc | '
              'where (not (InitiatingProcessFileName =~ "python.exe"))),(find withsource = '
              'TableName in (DeviceNetworkEvents)  where Timestamp >= <<timestamp>> and '
              'Timestamp < <<timestamp>>  | order by Timestamp desc | where '
              '(tostring(LocalPort) =~ "454") or (not (InitiatingProcessFileName =~ '
              '"python.exe"))),(find withsource = TableName in (DeviceRegistryEvents)  '
              'where Timestamp >= <<timestamp>> and Timestamp < <<timestamp>>  | order by '
              'Timestamp desc | where (not (InitiatingProcessFileName =~ '
              '"python.exe"))),(find withsource = TableName in (DeviceImageLoadEvents)  '
              'where Timestamp >= <<timestamp>> and Timestamp < <<timestamp>>  | order by '
              'Timestamp desc | where (not (InitiatingProcessFileName =~ "python.exe")))'))
        ]
        self._test_query_assertions(query, queries)

    # check about partesis
    def test_comb_observation_obs(self):
        stix_pattern = "[process:created = '2019-09-04T09:29:29.0882Z'] OR [file:name LIKE 'upd_ter.exe']"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [('union (find withsource = TableName in (DeviceProcessEvents)  where Timestamp '
                    '>= <<timestamp>> and Timestamp < <<timestamp>>  | order by Timestamp desc | '
                    'where ((FileName matches regex"(upd.ter.exe$)") or '
                    '(InitiatingProcessFileName matches regex"(upd.ter.exe$)") or '
                    '(InitiatingProcessParentFileName matches regex"(upd.ter.exe$)")) or '
                    '(tostring(ProcessCreationTime) == <<timestamp>>)),(find withsource = '
                    'TableName in (DeviceEvents)  where Timestamp >= <<timestamp>> and Timestamp '
                    '< <<timestamp>>  | order by Timestamp desc | where ((FileName matches '
                    'regex"(upd.ter.exe$)") or (InitiatingProcessFileName matches '
                    'regex"(upd.ter.exe$)") or (InitiatingProcessParentFileName matches '
                    'regex"(upd.ter.exe$)")) or (tostring(ProcessCreationTime) == '
                    '<<timestamp>>)),(find withsource = TableName in (DeviceNetworkEvents)  where '
                    'Timestamp >= <<timestamp>> and Timestamp < <<timestamp>>  | order by '
                    'Timestamp desc | where ((InitiatingProcessFileName matches '
                    'regex"(upd.ter.exe$)") or (InitiatingProcessParentFileName matches '
                    'regex"(upd.ter.exe$)")) or (tostring(InitiatingProcessCreationTime) == '
                    '<<timestamp>>)),(find withsource = TableName in (DeviceRegistryEvents)  '
                    'where Timestamp >= <<timestamp>> and Timestamp < <<timestamp>>  | order by '
                    'Timestamp desc | where ((InitiatingProcessFileName matches '
                    'regex"(upd.ter.exe$)") or (InitiatingProcessParentFileName matches '
                    'regex"(upd.ter.exe$)")) or (tostring(InitiatingProcessCreationTime) == '
                    '<<timestamp>>)),(find withsource = TableName in (DeviceFileEvents)  where '
                    'Timestamp >= <<timestamp>> and Timestamp < <<timestamp>>  | order by '
                    'Timestamp desc | where ((FileName matches regex"(upd.ter.exe$)") or '
                    '(InitiatingProcessFileName matches regex"(upd.ter.exe$)") or '
                    '(InitiatingProcessParentFileName matches regex"(upd.ter.exe$)")) or '
                    '(tostring(InitiatingProcessCreationTime) == <<timestamp>>)),(find withsource '
                    '= TableName in (DeviceImageLoadEvents)  where Timestamp >= <<timestamp>> and '
                    'Timestamp < <<timestamp>>  | order by Timestamp desc | where ((FileName '
                    'matches regex"(upd.ter.exe$)") or (InitiatingProcessFileName matches '
                    'regex"(upd.ter.exe$)") or (InitiatingProcessParentFileName matches '
                    'regex"(upd.ter.exe$)")) or (tostring(InitiatingProcessCreationTime) == '
                    '<<timestamp>>))')]
        self._test_query_assertions(query, queries)

    def test_and_op_comb_comparison_exp(self):
        stix_pattern = "[ipv4-addr:value = '9.147.31.113' AND process:name = 'python3']"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        # ip can appear in either DeviceNetworkEvents or DeviceEvents. process can appear in any table.
        # after AND these two tables are left.
        # process name can appear in FileName or InititatingProcessFileName in DeviceEvents (this is the only table in
        # which a process may appear as FileName or may not.
        # process name can appear in InitiatingProcessFileName in DeviceNetworkEvents
        queries = [
            (('union (find withsource = TableName in (DeviceEvents)  where Timestamp >= '
              '<<timestamp>> and Timestamp < <<timestamp>>  | order by Timestamp desc | '
              'where ((RemoteIP =~ "9.147.31.113") or (LocalIP =~ "9.147.31.113")) and '
              '((FileName =~ "python3") or (InitiatingProcessFileName =~ "python3"))),(find '
              'withsource = TableName in (DeviceNetworkEvents)  where Timestamp >= '
              '<<timestamp>> and Timestamp < <<timestamp>>  | order by Timestamp desc | '
              'where ((LocalIP =~ "9.147.31.113") or (RemoteIP =~ "9.147.31.113")) and '
              '(InitiatingProcessFileName =~ "python3"))'))
        ]
        self._test_query_assertions(query, queries)

    def test_registry_key(self):
        stix_pattern = r"[windows-registry-key:key = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows Advanced Threat Protection']"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        # ip can appear in either DeviceNetworkEvents or DeviceEvents. process can appear in any table.
        # after AND these two tables are left.
        # process name can appear in FileName or InititatingProcessFileName in DeviceEvents (this is the only table in
        # which a process may appear as FileName or may not.
        # process name can appear in InitiatingProcessFileName in DeviceNetworkEvents
        queries = [
            ('union (find withsource = TableName in (DeviceRegistryEvents)  where '
             'Timestamp >= <<timestamp>> and Timestamp < <<timestamp>>  | order by '
             'Timestamp desc | where RegistryKey =~ '
             '"HKEY_LOCAL_MACHINE\\\\SOFTWARE\\\\Microsoft\\\\Windows Advanced Threat '
             'Protection"),(find withsource = TableName in (DeviceEvents)  where Timestamp '
             '>= <<timestamp>> and Timestamp < <<timestamp>>  | order by Timestamp desc | '
             'where RegistryKey =~ "HKEY_LOCAL_MACHINE\\\\SOFTWARE\\\\Microsoft\\\\Windows '
             'Advanced Threat Protection")')
        ]
        self._test_query_assertions(query, queries)


    def test_config_no_info(self):
        stix_pattern = "[process:name = 'consent.exe']"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            ('union (find withsource = TableName in (DeviceProcessEvents)  where Timestamp '
             '>= <<timestamp>> and Timestamp < <<timestamp>>  | order by Timestamp desc | '
             'where (FileName =~ "consent.exe") or (InitiatingProcessFileName =~ '
             '"consent.exe")),(find withsource = TableName in (DeviceEvents)  where '
             'Timestamp >= <<timestamp>> and Timestamp < <<timestamp>>  | order by '
             'Timestamp desc | where (FileName =~ "consent.exe") or '
             '(InitiatingProcessFileName =~ "consent.exe")),(find withsource = TableName '
             'in (DeviceFileEvents)  where Timestamp >= <<timestamp>> and Timestamp < '
             '<<timestamp>>  | order by Timestamp desc | where InitiatingProcessFileName '
             '=~ "consent.exe"),(find withsource = TableName in (DeviceNetworkEvents)  '
             'where Timestamp >= <<timestamp>> and Timestamp < <<timestamp>>  | order by '
             'Timestamp desc | where InitiatingProcessFileName =~ "consent.exe"),(find '
             'withsource = TableName in (DeviceRegistryEvents)  where Timestamp >= '
             '<<timestamp>> and Timestamp < <<timestamp>>  | order by Timestamp desc | '
             'where InitiatingProcessFileName =~ "consent.exe"),(find withsource = '
             'TableName in (DeviceImageLoadEvents)  where Timestamp >= <<timestamp>> and '
             'Timestamp < <<timestamp>>  | order by Timestamp desc | where '
             'InitiatingProcessFileName =~ "consent.exe")')]
        self._test_query_assertions(query, queries)