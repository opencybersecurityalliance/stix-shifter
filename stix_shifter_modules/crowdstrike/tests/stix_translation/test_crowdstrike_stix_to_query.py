from stix_shifter.stix_translation import stix_translation
import unittest

translation = stix_translation.StixTranslation()


def _remove_timestamp_from_query(queries):
    timestamp_str = '+ behaviors.timestamp'
    ret = []
    for q in queries:
        ind = q.index(timestamp_str)
        ret.append(q[1:ind - 1])
    return ret


class TestQueryTranslator(unittest.TestCase):
    """
    class to perform unit test case crowdstrike translate query
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
        query = translation.translate('crowdstrike', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            "((behaviors.filename: 'updater.exe') + behaviors.timestamp:> '2002-06-02T07:07:58.931211')"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_process_comp_exp(self):
        stix_pattern = "[process:name = 'consent.exe']"
        query = translation.translate('crowdstrike', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            "((behaviors.filename: 'consent.exe') + behaviors.timestamp:> '2002-06-02T07:08:22.401869')"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_network_comp_exp(self):
        stix_pattern = "[ipv4-addr:value = '172.16.2.22'] START t'2019-09-10T08:43:10.003Z' STOP " \
                       "t'2019-09-23T10:43:10.453Z'"
        query = translation.translate('crowdstrike', 'query', '{}', stix_pattern)
        queries = [
            "(device.local_ip: '172.16.2.22') + (behaviors.timestamp:>= '2019-09-10T08:43:10' + "
            "behaviors.timestamp:<= '2019-09-23T10:43:10')"]
        self._test_query_assertions(query, queries)

    def test_mac_comp_exp(self):
        stix_pattern = "[mac-addr:value = '48:4D:7E:9D:BD:97'] START t'2019-09-01T08:43:10.003Z' STOP " \
                       "t'2019-10-10T10:43:10.003Z'"
        query = translation.translate('crowdstrike', 'query', '{}', stix_pattern)

        queries = [
            "(device.mac_address: '48:4D:7E:9D:BD:97') + (behaviors.timestamp:>= '2019-09-01T08:43:10' + "
            "behaviors.timestamp:<= '2019-10-10T10:43:10')"]
        self._test_query_assertions(query, queries)

    def test_directory_comp_exp(self):  # NOT OK
        stix_pattern = "[directory:path = 'ProgramData' OR ipv6-addr:value = 'fe80::4161:ca84:4dc5:f5fc'] " \
                       "START t'2019-10-01T08:43:10.003Z' STOP t'2019-10-30T10:43:10.003Z'"
        query = translation.translate('crowdstrike', 'query', '{}', stix_pattern)

        queries = ["(behaviors.filepath: 'ProgramData' , device.local_ip: 'fe80::4161:ca84:4dc5:f5fc') + ("
                   "behaviors.timestamp:>= '2019-10-01T08:43:10' + behaviors.timestamp:<= '2019-10-30T10:43:10')"]
        self._test_query_assertions(query, queries)

    def test_file_and_domain_exp(self):
        stix_pattern = "[file:name = 'some_file.exe' AND domain-name:value = 'example.com']"
        query = translation.translate('crowdstrike', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["((behaviors.filename: 'some_file.exe' + device.machine_domain: 'example.com') + "
                   "behaviors.timestamp:> '2002-06-02T07:10:42.958765')"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_gt_eq_datetime_comp_exp(self):
        stix_pattern = "[process:created >= '2019-09-04T09:29:29.0882Z']"
        query = translation.translate('crowdstrike', 'query', '{}', stix_pattern)
        #query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            "behaviors.timestamp:>= '2019-09-04T09:29:29.0882Z'"]
        #queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_noteq_comp_exp(self):
        stix_pattern = "[process:name != 'consent.exe'] START t'2019-09-10T08:43:10.003Z' STOP " \
                       "t'2019-09-23T10:43:10.453Z'"
        query = translation.translate('crowdstrike', 'query', '{}', stix_pattern)

        queries = [
            "(behaviors.filename:! 'consent.exe') + (behaviors.timestamp:>= '2019-09-10T08:43:10' + "
            "behaviors.timestamp:<= '2019-09-23T10:43:10')"]
        self._test_query_assertions(query, queries)

    def test_in_comp_exp(self):
        stix_pattern = "[process:created > '2019-09-04T09:29:29.0882Z']"
        query = translation.translate('crowdstrike', 'query', '{}', stix_pattern)
        #query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            "behaviors.timestamp:> '2019-09-04T09:29:29.0882Z'"]
        #queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_comb_comparison_exp(self):
        stix_pattern = "[process:name = 'reg.exe' OR file:name = 'updater.exe'] START " \
                       "t'2019-09-10T08:43:10.003Z' STOP t'2019-09-23T10:43:10.453Z'"
        query = translation.translate('crowdstrike', 'query', '{}', stix_pattern)

        queries = [
            "(behaviors.filename: 'reg.exe' , behaviors.filename: 'updater.exe') + (behaviors.timestamp:>= "
            "'2019-09-10T08:43:10' + behaviors.timestamp:<= '2019-09-23T10:43:10')"]
        self._test_query_assertions(query, queries)

    def test_comb_observation_obs(self):
        stix_pattern = "[process:created = '2019-09-04T09:29:29.0882Z'] OR [file:name = 'upd_ter.exe']"
        query = translation.translate('crowdstrike', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            "behaviors.timestamp: '2019-09-04T09:29:29.0882Z',((behaviors.filename: 'upd_ter.exe') + "
            "behaviors.timestamp:> '2002-06-02T07:14:15.098673')"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_unmapped_attribute_handling_with_OR(self):
        stix_pattern = "[ipv4-addr:value = '198.51.100.5' OR unmapped:attribute = 'something']"
        query = translation.translate('crowdstrike', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["((device.local_ip: '198.51.100.5') + behaviors.timestamp:> '2002-06-02T07:14:52.919437')"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_nested_parenthesis_in_pattern(self):
        stix_pattern = "[(ipv4-addr:value = '192.168.122.83' OR ipv4-addr:value = '100.100.122.90') AND file:name = " \
                       "'powershell.exe' OR user-account:user_id = 'root']"
        query = translation.translate('crowdstrike', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["((((device.local_ip: '192.168.122.83' , device.local_ip: '100.100.122.90') + behaviors.filename: "
                   "'powershell.exe') , behaviors.user_id: 'root') + behaviors.timestamp:> "
                   "'2002-06-02T07:15:35.411587')"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)
