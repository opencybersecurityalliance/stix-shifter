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
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ['(DeviceFileEvents |  where Timestamp >= datetime(2021-04-25T14:05:49.853Z) and Timestamp < '
                   'datetime(2021-04-25T14:10:49.853Z)  | order by Timestamp desc | where (FileName =~ "updater.exe") '
                   'or (InitiatingProcessFileName =~ "updater.exe") or (InitiatingProcessParentFileName =~ '
                   '"updater.exe") | union kind=outer (DeviceProcessEvents |  where Timestamp >= datetime('
                   '2021-04-25T14:05:49.853Z) and Timestamp < datetime(2021-04-25T14:10:49.853Z)  | order by '
                   'Timestamp desc | where (FileName =~ "updater.exe") or (InitiatingProcessFileName =~ '
                   '"updater.exe") or (InitiatingProcessParentFileName =~ "updater.exe")) | union kind=outer ('
                   'DeviceNetworkEvents |  where Timestamp >= datetime(2021-04-25T14:05:49.853Z) and Timestamp < '
                   'datetime(2021-04-25T14:10:49.853Z)  | order by Timestamp desc | where (InitiatingProcessFileName '
                   '=~ "updater.exe") or (InitiatingProcessParentFileName =~ "updater.exe")) | union kind=outer ('
                   'DeviceRegistryEvents |  where Timestamp >= datetime(2021-04-25T14:05:49.853Z) and Timestamp < '
                   'datetime(2021-04-25T14:10:49.853Z)  | order by Timestamp desc | where (InitiatingProcessFileName '
                   '=~ "updater.exe") or (InitiatingProcessParentFileName =~ "updater.exe")))']

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_process_comp_exp(self):
        stix_pattern = "[process:name = 'consent.exe']"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            '(DeviceProcessEvents |  where Timestamp >= datetime(2021-04-25T14:06:27.864Z) and Timestamp < datetime('
            '2021-04-25T14:11:27.864Z)  | order by Timestamp desc | where FileName =~ "consent.exe" | union '
            'kind=outer (DeviceNetworkEvents |  where Timestamp >= datetime(2021-04-25T14:06:27.864Z) and Timestamp < '
            'datetime(2021-04-25T14:11:27.864Z)  | order by Timestamp desc | where (InitiatingProcessFileName =~ '
            '"consent.exe") or (InitiatingProcessParentFileName =~ "consent.exe")) | union kind=outer ('
            'DeviceRegistryEvents |  where Timestamp >= datetime(2021-04-25T14:06:27.864Z) and Timestamp < datetime('
            '2021-04-25T14:11:27.864Z)  | order by Timestamp desc | where (InitiatingProcessFileName =~ '
            '"consent.exe") or (InitiatingProcessParentFileName =~ "consent.exe")))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_network_comp_exp(self):
        stix_pattern = "[ipv4-addr:value = '172.16.2.22'] START t'2019-09-10T08:43:10.003Z' STOP " \
                       "t'2019-09-23T10:43:10.453Z'"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [
            '(find withsource = TableName in (DeviceNetworkEvents) where Timestamp >= datetime('
            '2021-04-25T14:07:00.509Z) and Timestamp < datetime(2021-04-25T14:12:00.509Z) | order by Timestamp desc | '
            'where (LocalIP =~ "172.16.2.22") or (RemoteIP =~ "172.16.2.22"))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_mac_comp_exp(self):
        stix_pattern = "[mac-addr:value = '48:4D:7E:9D:BD:97'] START t'2019-09-01T08:43:10.003Z' STOP " \
                       "t'2019-10-10T10:43:10.003Z'"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            '(find withsource = TableName in (DeviceNetworkInfo) where Timestamp >= datetime('
            '2021-04-25T14:07:24.832Z) and Timestamp < datetime(2021-04-25T14:12:24.832Z) | order by Timestamp desc | '
            'where MacAddress =~ "484D7E9DBD97")']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_registry_comp_exp(self):
        stix_pattern = "[windows-registry-key:values[*] IN ('SD', 'Index')] START t'2019-09-01T08:43:10.003Z' STOP " \
                       "t'2019-10-10T10:43:10.003Z'"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            '(find withsource = TableName in (DeviceRegistryEvents) where Timestamp >= datetime('
            '2021-04-25T14:08:00.799Z) and Timestamp < datetime(2021-04-25T14:13:00.799Z) | order by Timestamp desc | '
            'where RegistryValueName in~ ("SD", "Index"))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_directory_comp_exp(self):
        stix_pattern = "[directory:path LIKE 'ProgramData' OR ipv6-addr:value = 'fe80::4161:ca84:4dc5:f5fc'] " \
                       "START t'2019-10-01T08:43:10.003Z' STOP t'2019-10-30T10:43:10.003Z'"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ['(DeviceNetworkEvents |  where Timestamp >= datetime(2021-04-25T14:08:23.747Z) and Timestamp < '
                   'datetime(2021-04-25T14:13:23.747Z)  | order by Timestamp desc | where ('
                   'InitiatingProcessFolderPath contains "ProgramData") or ((LocalIP =~ "fe80::4161:ca84:4dc5:f5fc") '
                   'or (RemoteIP =~ "fe80::4161:ca84:4dc5:f5fc")) | union kind=outer (DeviceFileEvents |  where '
                   'Timestamp >= datetime(2021-04-25T14:08:23.747Z) and Timestamp < datetime('
                   '2021-04-25T14:13:23.747Z)  | order by Timestamp desc | where ((FolderPath contains "ProgramData") '
                   'or (InitiatingProcessFolderPath contains "ProgramData"))) | union kind=outer (DeviceProcessEvents '
                   '|  where Timestamp >= datetime(2021-04-25T14:08:23.747Z) and Timestamp < datetime('
                   '2021-04-25T14:13:23.747Z)  | order by Timestamp desc | where ((FolderPath contains "ProgramData") '
                   'or (InitiatingProcessFolderPath contains "ProgramData"))) | union kind=outer ('
                   'DeviceRegistryEvents |  where Timestamp >= datetime(2021-04-25T14:08:23.747Z) and Timestamp < '
                   'datetime(2021-04-25T14:13:23.747Z)  | order by Timestamp desc | where ('
                   'InitiatingProcessFolderPath contains "ProgramData")))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_gt_eq_datetime_comp_exp(self):
        stix_pattern = "[process:created >= '2019-09-04T09:29:29.0882Z']"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            '(DeviceProcessEvents |  where Timestamp >= datetime(2021-04-25T14:08:51.475Z) and Timestamp < datetime('
            '2021-04-25T14:13:51.475Z)  | order by Timestamp desc | where ProcessCreationTime >= datetime('
            '2019-09-04T09:29:29.0882Z) | union kind=outer (DeviceNetworkEvents |  where Timestamp >= datetime('
            '2021-04-25T14:08:51.475Z) and Timestamp < datetime(2021-04-25T14:13:51.475Z)  | order by Timestamp desc '
            '| where (InitiatingProcessCreationTime >= datetime(2019-09-04T09:29:29.0882Z)) or ('
            'InitiatingProcessParentCreationTime >= datetime(2019-09-04T09:29:29.0882Z))) | union kind=outer ('
            'DeviceRegistryEvents |  where Timestamp >= datetime(2021-04-25T14:08:51.475Z) and Timestamp < datetime('
            '2021-04-25T14:13:51.475Z)  | order by Timestamp desc | where (InitiatingProcessCreationTime >= datetime('
            '2019-09-04T09:29:29.0882Z)) or (InitiatingProcessParentCreationTime >= datetime('
            '2019-09-04T09:29:29.0882Z))))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_lt_eq_datetime_comp_exp(self):
        stix_pattern = "[network-traffic:src_port < '443']"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            '(find withsource = TableName in (DeviceNetworkEvents) where Timestamp >= datetime('
            '2021-04-25T14:09:15.093Z) and Timestamp < datetime(2021-04-25T14:14:15.093Z) | order by Timestamp desc | '
            'where LocalPort < 443)']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_noteq_comp_exp(self):
        stix_pattern = "[process:name != 'consent.exe'] START t'2019-09-10T08:43:10.003Z' STOP " \
                       "t'2019-09-23T10:43:10.453Z'"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            '(DeviceProcessEvents |  where Timestamp >= datetime(2021-04-25T14:09:57.517Z) and Timestamp < datetime('
            '2021-04-25T14:14:57.517Z)  | order by Timestamp desc | where FileName !~ "consent.exe" | union '
            'kind=outer (DeviceNetworkEvents |  where Timestamp >= datetime(2021-04-25T14:09:57.517Z) and Timestamp < '
            'datetime(2021-04-25T14:14:57.517Z)  | order by Timestamp desc | where (InitiatingProcessFileName !~ '
            '"consent.exe") or (InitiatingProcessParentFileName !~ "consent.exe")) | union kind=outer ('
            'DeviceRegistryEvents |  where Timestamp >= datetime(2021-04-25T14:09:57.517Z) and Timestamp < datetime('
            '2021-04-25T14:14:57.517Z)  | order by Timestamp desc | where (InitiatingProcessFileName !~ '
            '"consent.exe") or (InitiatingProcessParentFileName !~ "consent.exe")))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_like_comp_exp(self):
        stix_pattern = "[file:name LIKE  'upd']"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            '(DeviceFileEvents |  where Timestamp >= datetime(2021-04-25T14:10:57.699Z) and Timestamp < datetime('
            '2021-04-25T14:15:57.699Z)  | order by Timestamp desc | where (FileName contains "upd") or ('
            'InitiatingProcessFileName contains "upd") or (InitiatingProcessParentFileName contains "upd") | union '
            'kind=outer (DeviceProcessEvents |  where Timestamp >= datetime(2021-04-25T14:10:57.699Z) and Timestamp < '
            'datetime(2021-04-25T14:15:57.699Z)  | order by Timestamp desc | where (FileName contains "upd") or ('
            'InitiatingProcessFileName contains "upd") or (InitiatingProcessParentFileName contains "upd")) | union '
            'kind=outer (DeviceNetworkEvents |  where Timestamp >= datetime(2021-04-25T14:10:57.699Z) and Timestamp < '
            'datetime(2021-04-25T14:15:57.699Z)  | order by Timestamp desc | where (InitiatingProcessFileName '
            'contains "upd") or (InitiatingProcessParentFileName contains "upd")) | union kind=outer ('
            'DeviceRegistryEvents |  where Timestamp >= datetime(2021-04-25T14:10:57.699Z) and Timestamp < datetime('
            '2021-04-25T14:15:57.699Z)  | order by Timestamp desc | where (InitiatingProcessFileName contains "upd") '
            'or (InitiatingProcessParentFileName contains "upd")))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_matches_comp_exp(self):
        stix_pattern = "[file:name MATCHES '^chr']"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ['(DeviceFileEvents |  where Timestamp >= datetime(2021-04-25T14:11:29.078Z) and Timestamp < '
                   'datetime(2021-04-25T14:16:29.078Z)  | order by Timestamp desc | where (FileName matches regex"('
                   '^chr)") or (InitiatingProcessFileName matches regex"(^chr)") or (InitiatingProcessParentFileName '
                   'matches regex"(^chr)") | union kind=outer (DeviceProcessEvents |  where Timestamp >= datetime('
                   '2021-04-25T14:11:29.078Z) and Timestamp < datetime(2021-04-25T14:16:29.078Z)  | order by '
                   'Timestamp desc | where (FileName matches regex"(^chr)") or (InitiatingProcessFileName matches '
                   'regex"(^chr)") or (InitiatingProcessParentFileName matches regex"(^chr)")) | union kind=outer ('
                   'DeviceNetworkEvents |  where Timestamp >= datetime(2021-04-25T14:11:29.078Z) and Timestamp < '
                   'datetime(2021-04-25T14:16:29.078Z)  | order by Timestamp desc | where (InitiatingProcessFileName '
                   'matches regex"(^chr)") or (InitiatingProcessParentFileName matches regex"(^chr)")) | union '
                   'kind=outer (DeviceRegistryEvents |  where Timestamp >= datetime(2021-04-25T14:11:29.078Z) and '
                   'Timestamp < datetime(2021-04-25T14:16:29.078Z)  | order by Timestamp desc | where ('
                   'InitiatingProcessFileName matches regex"(^chr)") or (InitiatingProcessParentFileName matches '
                   'regex"(^chr)")))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_in_comp_exp(self):
        stix_pattern = "[process:created IN ('2019-09-04T09:29:29.0882Z', '2019-09-04T09:29:29.0881372Z')]"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            '(DeviceProcessEvents |  where Timestamp >= datetime(2021-04-25T14:12:22.721Z) and Timestamp < datetime('
            '2021-04-25T14:17:22.721Z)  | order by Timestamp desc | where ProcessCreationTime in~ (datetime('
            '2019-09-04T09:29:29.0882Z), datetime(2019-09-04T09:29:29.0881372Z)) | union kind=outer ('
            'DeviceNetworkEvents |  where Timestamp >= datetime(2021-04-25T14:12:22.721Z) and Timestamp < datetime('
            '2021-04-25T14:17:22.721Z)  | order by Timestamp desc | where (InitiatingProcessCreationTime in~ ('
            'datetime(2019-09-04T09:29:29.0882Z), datetime(2019-09-04T09:29:29.0881372Z))) or ('
            'InitiatingProcessParentCreationTime in~ (datetime(2019-09-04T09:29:29.0882Z), '
            'datetime(2019-09-04T09:29:29.0881372Z)))) | union kind=outer (DeviceRegistryEvents |  where Timestamp >= '
            'datetime(2021-04-25T14:12:22.721Z) and Timestamp < datetime(2021-04-25T14:17:22.721Z)  | order by '
            'Timestamp desc | where (InitiatingProcessCreationTime in~ (datetime(2019-09-04T09:29:29.0882Z), '
            'datetime(2019-09-04T09:29:29.0881372Z))) or (InitiatingProcessParentCreationTime in~ (datetime('
            '2019-09-04T09:29:29.0882Z), datetime(2019-09-04T09:29:29.0881372Z)))))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_comb_comparison_exp(self):
        stix_pattern = "[process:name IN ('consent.exe', 'reg.exe') OR file:name = 'updater.exe'] START " \
                       "t'2019-09-10T08:43:10.003Z' STOP t'2019-09-23T10:43:10.453Z'"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            '(DeviceFileEvents |  where Timestamp >= datetime(2021-04-25T14:12:50.578Z) and Timestamp < datetime('
            '2021-04-25T14:17:50.578Z)  | order by Timestamp desc | where ((FileName =~ "updater.exe") or ('
            'InitiatingProcessFileName =~ "updater.exe") or (InitiatingProcessParentFileName =~ "updater.exe")) | '
            'union kind=outer (DeviceProcessEvents |  where Timestamp >= datetime(2021-04-25T14:12:50.578Z) and '
            'Timestamp < datetime(2021-04-25T14:17:50.578Z)  | order by Timestamp desc | where (FileName in~ ('
            '"consent.exe", "reg.exe")) or ((FileName =~ "updater.exe") or (InitiatingProcessFileName =~ '
            '"updater.exe") or (InitiatingProcessParentFileName =~ "updater.exe"))) | union kind=outer ('
            'DeviceNetworkEvents |  where Timestamp >= datetime(2021-04-25T14:12:50.578Z) and Timestamp < datetime('
            '2021-04-25T14:17:50.578Z)  | order by Timestamp desc | where ((InitiatingProcessFileName in~ ('
            '"consent.exe", "reg.exe")) or (InitiatingProcessParentFileName in~ ("consent.exe", "reg.exe"))) or (('
            'InitiatingProcessFileName =~ "updater.exe") or (InitiatingProcessParentFileName =~ "updater.exe"))) | '
            'union kind=outer (DeviceRegistryEvents |  where Timestamp >= datetime(2021-04-25T14:12:50.578Z) and '
            'Timestamp < datetime(2021-04-25T14:17:50.578Z)  | order by Timestamp desc | where (('
            'InitiatingProcessFileName in~ ("consent.exe", "reg.exe")) or (InitiatingProcessParentFileName in~ ('
            '"consent.exe", "reg.exe"))) or ((InitiatingProcessFileName =~ "updater.exe") or ('
            'InitiatingProcessParentFileName =~ "updater.exe"))))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_comb_comparison_exp_1(self):
        stix_pattern = "[network-traffic:src_port = '454' OR process:name NOT = 'python.exe'] START " \
                       "t'2019-09-10T08:43:10.003Z' STOP t'2019-09-23T10:43:10.453Z'"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            '(DeviceProcessEvents |  where Timestamp >= datetime(2021-04-25T14:13:17.009Z) and Timestamp < datetime('
            '2021-04-25T14:18:17.009Z)  | order by Timestamp desc | where (not (FileName =~ "python.exe")) | union '
            'kind=outer (DeviceNetworkEvents |  where Timestamp >= datetime(2021-04-25T14:13:17.009Z) and Timestamp < '
            'datetime(2021-04-25T14:18:17.009Z)  | order by Timestamp desc | where (tostring(LocalPort) =~ "454") or '
            '(not ((InitiatingProcessFileName =~ "python.exe") or (InitiatingProcessParentFileName =~ '
            '"python.exe")))) | union kind=outer (DeviceRegistryEvents |  where Timestamp >= datetime('
            '2021-04-25T14:13:17.009Z) and Timestamp < datetime(2021-04-25T14:18:17.009Z)  | order by Timestamp desc '
            '| where (not ((InitiatingProcessFileName =~ "python.exe") or (InitiatingProcessParentFileName =~ '
            '"python.exe")))))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    # check about partesis
    def test_comb_observation_obs(self):
        stix_pattern = "[process:created = '2019-09-04T09:29:29.0882Z'] OR [file:name LIKE 'upd_ter.exe']"
        query = translation.translate('msatp', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            '(DeviceProcessEvents |  where Timestamp >= datetime(2021-04-25T14:13:43.438Z) and Timestamp < datetime('
            '2021-04-25T14:18:43.438Z)  | order by Timestamp desc | where ((FileName matches regex"(upd.ter.exe$)") '
            'or (InitiatingProcessFileName matches regex"(upd.ter.exe$)") or (InitiatingProcessParentFileName matches '
            'regex"(upd.ter.exe$)")) or (tostring(ProcessCreationTime) == datetime(2019-09-04T09:29:29.0882Z)) | '
            'union kind=outer (DeviceNetworkEvents |  where Timestamp >= datetime(2021-04-25T14:13:43.438Z) and '
            'Timestamp < datetime(2021-04-25T14:18:43.438Z)  | order by Timestamp desc | where (('
            'InitiatingProcessFileName matches regex"(upd.ter.exe$)") or (InitiatingProcessParentFileName matches '
            'regex"(upd.ter.exe$)")) or ((tostring(InitiatingProcessCreationTime) == datetime('
            '2019-09-04T09:29:29.0882Z)) or (tostring(InitiatingProcessParentCreationTime) == datetime('
            '2019-09-04T09:29:29.0882Z)))) | union kind=outer (DeviceRegistryEvents |  where Timestamp >= datetime('
            '2021-04-25T14:13:43.438Z) and Timestamp < datetime(2021-04-25T14:18:43.438Z)  | order by Timestamp desc '
            '| where ((InitiatingProcessFileName matches regex"(upd.ter.exe$)") or (InitiatingProcessParentFileName '
            'matches regex"(upd.ter.exe$)")) or ((tostring(InitiatingProcessCreationTime) == datetime('
            '2019-09-04T09:29:29.0882Z)) or (tostring(InitiatingProcessParentCreationTime) == datetime('
            '2019-09-04T09:29:29.0882Z)))) | union kind=outer (DeviceFileEvents |  where Timestamp >= datetime('
            '2021-04-25T14:13:43.438Z) and Timestamp < datetime(2021-04-25T14:18:43.438Z)  | order by Timestamp desc '
            '| where ((FileName matches regex"(upd.ter.exe$)") or (InitiatingProcessFileName matches regex"('
            'upd.ter.exe$)") or (InitiatingProcessParentFileName matches regex"(upd.ter.exe$)"))))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)
