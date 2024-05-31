from stix_shifter.stix_translation import stix_translation
import unittest

translation = stix_translation.StixTranslation()


def _remove_timestamp_from_query(queries):
    """
    remove the timestamp in the query
    : param: queries: list
    : return: queries: list
    """
    for query in queries['queries']:
        for item in query['query']:
            if 'Timestamp - Event' in item['field']:
                query['query'].remove(item)
                break
    return queries


class TestQueryTranslator(unittest.TestCase):
    """
    class to perform unit test case for TRELLIX ENDPOINT SECURITY HX translate query
    """
    if __name__ == "__main__":
        unittest.main()

    def _test_query_assertions(self, query, queries):
        """
        to assert each query in the list against expected result
        """
        self.assertIsInstance(queries, dict)
        self.assertIsInstance(query, dict)
        self.assertIsInstance(query['queries'], list)
        self.assertEqual(query, queries)

    def test_ipv4_query(self):
        stix_pattern = "[ipv4-addr:value = '111.11.111.1']"
        query = translation.translate('trellix_endpoint_security_hx', 'query', '{}', stix_pattern,
                                      {"host_sets": "host_set1"})
        query = _remove_timestamp_from_query(query)
        queries = {"queries": [{"host_set": {"_id": "host_set1"},
                                "query": [{"field": "Local IP Address", "value": "111.11.111.1", "operator": "equals"},
                                          {"field": "Timestamp - Event", "operator": "between",
                                           "value": ["2024-03-14T13:28:18.977Z", "2024-03-14T13:33:18.977Z"]}]},
                               {"host_set": {"_id": "host_set1"},
                                "query": [
                                    {"field": "Remote IP Address", "value": "111.11.111.1", "operator": "equals"},
                                    {"field": "Timestamp - Event", "operator": "between",
                                     "value": ["2024-03-14T13:28:18.977Z", "2024-03-14T13:33:18.977Z"]}]}]}
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_ipv6_not_equal_operator(self):
        stix_pattern = "[ipv6-addr:value != '1001:0db8:85a3:0000:0000:8a2e:0370:7334']"
        query = translation.translate('trellix_endpoint_security_hx', 'query', '{}', stix_pattern,
                                      {"host_sets": "host_set1"})
        query = _remove_timestamp_from_query(query)
        queries = {"queries": [{"host_set": {"_id": "host_set1"}, "query": [
            {"field": "Local IP Address", "value": "1001:0db8:85a3:0000:0000:8a2e:0370:7334", "operator": "not equals"},
            {"field": "Timestamp - Event", "operator": "between",
             "value": ["2024-03-14T13:36:20.952Z", "2024-03-14T13:41:20.952Z"]}]},
                               {"host_set": {"_id": "host_set1"}, "query": [
                                   {"field": "Remote IP Address", "value": "1001:0db8:85a3:0000:0000:8a2e:0370:7334",
                                    "operator": "not equals"}, {"field": "Timestamp - Event", "operator": "between",
                                                                "value": ["2024-03-14T13:36:20.952Z",
                                                                          "2024-03-14T13:41:20.952Z"]}]}]}
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_network_traffic_gt_operator(self):
        stix_pattern = "[network-traffic:src_port > 1234]"
        query = translation.translate('trellix_endpoint_security_hx', 'query', '{}', stix_pattern,
                                      {"host_sets": "host_set1"})
        query = _remove_timestamp_from_query(query)
        queries = {"queries": [{"host_set": {"_id": "host_set1"}, "query": [{"field": "Local Port", "value": 1234,
                                                                             "operator": "greater than"},
                                                                            {"field": "Timestamp - Event",
                                                                             "operator": "between",
                                                                             "value": ["2024-03-14T13:40:04.718Z",
                                                                                       "2024-03-14T13:45:04.718Z"]}]}]}
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_network_traffic_LIKE_operator(self):
        stix_pattern = "[network-traffic:extensions.'http-request-ext'.request_value LIKE '/mail/u/0']"
        query = translation.translate('trellix_endpoint_security_hx', 'query', '{}', stix_pattern,
                                      {"host_sets": "host_set1"})
        query = _remove_timestamp_from_query(query)
        queries = {"queries": [
            {"host_set": {"_id": "host_set1"}, "query": [{"field": "URL", "value": "/mail/u/0", "operator": "contains"},
                                                         {"field": "Timestamp - Event", "operator": "between",
                                                          "value": ["2024-03-18T09:03:51.908Z",
                                                                    "2024-03-18T09:08:51.908Z"]}]}]}
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_directory_MATCHES_operator(self):
        stix_pattern = "[directory:path MATCHES 'C:\\\\Users\\\\Administrator\\\\AppData']"
        query = translation.translate('trellix_endpoint_security_hx', 'query', '{}', stix_pattern,
                                      {"host_sets": "host_set1"})
        query = _remove_timestamp_from_query(query)
        queries = {"queries": [{"host_set": {"_id": "host_set1"}, "query": [
            {"field": "File Full Path", "value": "C:\\Users\\Administrator\\AppData", "operator": "contains"},
            {"field": "Timestamp - Event", "operator": "between",
             "value": ["2024-03-18T09:15:35.409Z", "2024-03-18T09:20:35.409Z"]}]}]}
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_domain_name_NOT_LIKE_operator(self):
        stix_pattern = "[domain-name:value NOT LIKE 'dns']"
        query = translation.translate('trellix_endpoint_security_hx', 'query', '{}', stix_pattern,
                                      {"host_sets": "host_set1"})
        query = _remove_timestamp_from_query(query)
        queries = {"queries": [{"host_set": {"_id": "host_set1"},
                                "query": [{"field": "DNS Hostname", "value": "dns", "operator": "not contains"},
                                          {"field": "Timestamp - Event", "operator": "between",
                                           "value": ["2024-03-18T09:21:27.261Z", "2024-03-18T09:26:27.261Z"]}]}]}
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_process_IN_operator(self):
        stix_pattern = "[process:name IN ('cmd.exe','conhost.exe')]"
        query = translation.translate('trellix_endpoint_security_hx', 'query', '{}', stix_pattern,
                                      {"host_sets": "host_set1"})
        query = _remove_timestamp_from_query(query)
        queries = {"queries": [{"host_set": {"_id": "host_set1"},
                                "query": [{"field": "Process Name", "operator": "equals", "value": "cmd.exe"},
                                          {"field": "Process Name", "operator": "equals", "value": "conhost.exe"}]},
                               {"host_set": {"_id": "host_set1"},
                                "query": [{"field": "Parent Process Name", "operator": "equals", "value": "cmd.exe"},
                                          {"field": "Parent Process Name", "operator": "equals",
                                           "value": "conhost.exe"}]}]}
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_query_for_stix_attributes_joined_by_OR(self):
        stix_pattern = "[process:name='svchost.exe' OR file:name IN( 'svchost1','svchost2') OR file:name NOT IN(" \
                       "'file1'," \
                       "'file2')] START t'2024-02-10T16:43:26.000Z' STOP t'2024-03-10T16:43:26.003Z'"
        query = translation.translate('trellix_endpoint_security_hx', 'query', '{}', stix_pattern,
                                      {"host_sets": "host_set1"})
        query = _remove_timestamp_from_query(query)
        queries = {"queries": [{"host_set": {"_id": "host_set1"},
                                "query": [{"field": "File Name", "value": "file1", "operator": "not equals"},
                                          {"field": "File Name", "value": "file2", "operator": "not equals"},
                                          {"field": "Timestamp - Event", "operator": "between",
                                           "value": ["2024-02-10T16:43:26.000Z", "2024-03-10T16:43:26.003Z"]},
                                          {"field": "File Name", "value": "svchost1", "operator": "equals"},
                                          {"field": "File Name", "value": "svchost2", "operator": "equals"}]},
                               {"host_set": {"_id": "host_set1"},
                                "query": [{"field": "Process Name", "value": "svchost.exe", "operator": "equals"},
                                          {"field": "Timestamp - Event", "operator": "between",
                                           "value": ["2024-02-10T16:43:26.000Z", "2024-03-10T16:43:26.003Z"]}]},
                               {"host_set": {"_id": "host_set1"},
                                "query": [
                                    {"field": "Parent Process Name", "value": "svchost.exe", "operator": "equals"},
                                    {"field": "Timestamp - Event", "operator": "between",
                                     "value": ["2024-02-10T16:43:26.000Z", "2024-03-10T16:43:26.003Z"]}]}]}
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_query_for_morethan_two_comparison_expressions_joined_by_AND(self):
        stix_pattern = ("[ipv4-addr:value = '1.1.1.1' AND network-traffic:src_port > 1234 AND "
                        "process:name= 'cmd.exe' AND file:name='wpndatabase.db-wal' AND "
                        "user-account:user_id = 'NT AUTHORITY\\\\SYSTEM' ]")
        query = translation.translate('trellix_endpoint_security_hx', 'query', '{}', stix_pattern,
                                      {"host_sets": "host_set1"})
        query = _remove_timestamp_from_query(query)
        queries = {"queries": [
            {"host_set": {"_id": "host_set1"}, "query": [
                {"field": "Username", "value": "NT AUTHORITY\\SYSTEM",
                 "operator": "equals"},
                {"field": "Timestamp - Event", "operator": "between",
                 "value": ["2024-03-21T08:45:53.437Z",
                           "2024-03-21T08:50:53.437Z"]},
                {"field": "File Name", "value": "wpndatabase.db-wal",
                 "operator": "equals"},
                {"field": "Process Name", "value": "cmd.exe",
                 "operator": "equals"},
                {"field": "Local Port", "value": 1234,
                 "operator": "greater than"},
                {"field": "Local IP Address", "value": "1.1.1.1",
                 "operator": "equals"}]},
            {"host_set": {"_id": "host_set1"}, "query": [
                {"field": "Username", "value": "NT AUTHORITY\\SYSTEM", "operator": "equals"},
                {"field": "Timestamp - Event", "operator": "between",
                 "value": ["2024-03-21T08:45:53.437Z", "2024-03-21T08:50:53.437Z"]},
                {"field": "File Name", "value": "wpndatabase.db-wal", "operator": "equals"},
                {"field": "Process Name", "value": "cmd.exe", "operator": "equals"},
                {"field": "Local Port", "value": 1234, "operator": "greater than"},
                {"field": "Remote IP Address", "value": "1.1.1.1", "operator": "equals"}]},
            {"host_set": {"_id": "host_set1"}, "query": [
                {"field": "Username", "value": "NT AUTHORITY\\SYSTEM", "operator": "equals"},
                {"field": "Timestamp - Event", "operator": "between",
                 "value": ["2024-03-21T08:45:53.437Z", "2024-03-21T08:50:53.437Z"]},
                {"field": "File Name", "value": "wpndatabase.db-wal", "operator": "equals"},
                {"field": "Parent Process Name", "value": "cmd.exe", "operator": "equals"},
                {"field": "Local Port", "value": 1234, "operator": "greater than"},
                {"field": "Local IP Address", "value": "1.1.1.1", "operator": "equals"}]},
            {"host_set": {"_id": "host_set1"}, "query": [
                {"field": "Username", "value": "NT AUTHORITY\\SYSTEM", "operator": "equals"},
                {"field": "Timestamp - Event", "operator": "between",
                 "value": ["2024-03-21T08:45:53.437Z", "2024-03-21T08:50:53.437Z"]},
                {"field": "File Name", "value": "wpndatabase.db-wal", "operator": "equals"},
                {"field": "Parent Process Name", "value": "cmd.exe", "operator": "equals"},
                {"field": "Local Port", "value": 1234, "operator": "greater than"},
                {"field": "Remote IP Address", "value": "1.1.1.1", "operator": "equals"}]}]}
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_query_with_multiple_comparison_expressions_with_AND_OR_combinations(self):
        stix_pattern = "[ipv4-addr:value = '1.1.1.1' OR network-traffic:src_port > 1234 OR process:name= " \
                       "'amazon-ssm-agent.exe' AND  file:name='wpndatabase.db-wal']"
        query = translation.translate('trellix_endpoint_security_hx', 'query', '{}', stix_pattern,
                                      {"host_sets": "host_set1"})
        query = _remove_timestamp_from_query(query)
        queries = {"queries": [{"host_set": {"_id": "host_set1"},
                                "query": [{"field": "File Name", "value": "wpndatabase.db-wal", "operator": "equals"},
                                          {"field": "Timestamp - Event", "operator": "between",
                                           "value": ["2024-03-15T09:56:31.088Z", "2024-03-15T10:01:31.088Z"]}]},
                               {"host_set": {"_id": "host_set1"},
                                "query": [{"field": "Local IP Address", "value": "1.1.1.1", "operator": "equals"},
                                          {"field": "Timestamp - Event", "operator": "between",
                                           "value": ["2024-03-15T09:56:31.088Z", "2024-03-15T10:01:31.088Z"]}]},
                               {"host_set": {"_id": "host_set1"},
                                "query": [{"field": "Remote IP Address", "value": "1.1.1.1", "operator": "equals"},
                                          {"field": "Timestamp - Event", "operator": "between",
                                           "value": ["2024-03-15T09:56:31.088Z", "2024-03-15T10:01:31.088Z"]}]},
                               {"host_set": {"_id": "host_set1"},
                                "query": [{"field": "Local Port", "value": 1234, "operator": "greater than"},
                                          {"field": "Timestamp - Event", "operator": "between",
                                           "value": ["2024-03-15T09:56:31.088Z", "2024-03-15T10:01:31.088Z"]}]},
                               {"host_set": {"_id": "host_set1"},
                                "query": [{"field": "Process Name", "value": "amazon-ssm-agent.exe",
                                           "operator": "equals"},
                                          {"field": "Timestamp - Event", "operator": "between",
                                           "value": ["2024-03-15T09:56:31.088Z", "2024-03-15T10:01:31.088Z"]}]},
                               {"host_set": {"_id": "host_set1"},
                                "query": [{"field": "Parent Process Name", "value": "amazon-ssm-agent.exe",
                                           "operator": "equals"},
                                          {"field": "Timestamp - Event", "operator": "between",
                                           "value": ["2024-03-15T09:56:31.088Z", "2024-03-15T10:01:31.088Z"]}]}]}
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_query_for_multiple_observation_with_and_without_qualifier(self):
        stix_pattern = "[network-traffic:src_port > 50 OR domain-name:value='dns'] AND [ " \
                       "windows-registry-key:key='HKEY_LOCAL_MACHINE\\\\SOFTWARE\\\\Microsoft\\\\Windows' AND " \
                       "user-account:user_id = 'NT AUTHORITY\\\\SYSTEM'] OR " \
                       "[network-traffic:extensions.'http-request-ext'.request_header.'Accept-Encoding' LIKE 'gzip'] " \
                       "START t'2024-02-10T11:00:00.000Z'STOP t'2024-03-01T11:00:00.003Z'"
        query = translation.translate('trellix_endpoint_security_hx', 'query', '{}', stix_pattern,
                                      {"host_sets": "host_set1"})
        query = _remove_timestamp_from_query(query)
        queries = {"queries": [{"host_set": {"_id": "host_set1"},
                                "query": [{"field": "DNS Hostname", "value": "dns", "operator": "equals"},
                                          {"field": "Timestamp - Event", "operator": "between",
                                           "value": ["2024-03-21T09:09:37.814Z", "2024-03-21T09:14:37.814Z"]}]},
                               {"host_set": {"_id": "host_set1"},
                                "query": [{"field": "Local Port", "value": 50, "operator": "greater than"},
                                          {"field": "Timestamp - Event", "operator": "between",
                                           "value": ["2024-03-21T09:09:37.814Z", "2024-03-21T09:14:37.814Z"]}]},
                               {"host_set": {"_id": "host_set1"},
                                "query": [{"field": "Username", "value": "NT AUTHORITY\\SYSTEM",
                                           "operator": "equals"},
                                          {"field": "Timestamp - Event", "operator": "between",
                                           "value": ["2024-03-21T09:09:37.814Z", "2024-03-21T09:14:37.814Z"]},
                                          {"field": "Registry Key Full Path",
                                           "value": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows",
                                           "operator": "equals"}]},
                               {"host_set": {"_id": "host_set1"},
                                "query": [{"field": "HTTP Header", "value": "gzip",
                                           "operator": "contains"},
                                          {"field": "Timestamp - Event",
                                           "operator": "between",
                                           "value": ["2024-02-10T11:00:00.000Z",
                                                     "2024-03-01T11:00:00.003Z"]}
                                          ]}]}
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_observation_with_single_qualifier_with_precedence_bracket(self):
        stix_pattern = ("([network-traffic:extensions.'http-request-ext'.request_header.'User-Agent' MATCHES 'header' "
                        "AND windows-registry-key:values[*].name = 'ChangeId'] OR [file:hashes.MD5 = 'abc123' "
                        "OR network-traffic:extensions.'http-request-ext'.request_value "
                        "!='/latest/meta-data/iam/security-credentials/']) "
                        "START t'2024-02-15T11:20:35.000Z'STOP t'2024-03-10T11:00:00.003Z'")
        query = translation.translate('trellix_endpoint_security_hx', 'query', '{}', stix_pattern,
                                      {"host_sets": "host_set1"})
        query = _remove_timestamp_from_query(query)
        queries = {
            "queries": [
                {
                    "host_set": {
                        "_id": "host_set1"
                    },
                    "query": [
                        {
                            "field": "Registry Key Value Name",
                            "value": "ChangeId",
                            "operator": "equals"
                        },
                        {
                            "field": "Timestamp - Event",
                            "operator": "between",
                            "value": [
                                "2024-02-15T11:20:35.000Z",
                                "2024-03-10T11:00:00.003Z"
                            ]
                        },
                        {
                            "field": "HTTP Header",
                            "value": "header",
                            "operator": "contains"
                        }
                    ]
                },
                {
                    "host_set": {
                        "_id": "host_set1"
                    },
                    "query": [
                        {
                            "field": "URL",
                            "value": "/latest/meta-data/iam/security-credentials/",
                            "operator": "not equals"
                        },
                        {
                            "field": "Timestamp - Event",
                            "operator": "between",
                            "value": [
                                "2024-02-15T11:20:35.000Z",
                                "2024-03-10T11:00:00.003Z"
                            ]
                        }
                    ]
                },
                {
                    "host_set": {
                        "_id": "host_set1"
                    },
                    "query": [
                        {
                            "field": "File MD5 Hash",
                            "value": "abc123",
                            "operator": "equals"
                        },
                        {
                            "field": "Timestamp - Event",
                            "operator": "between",
                            "value": [
                                "2024-02-15T11:20:35.000Z",
                                "2024-03-10T11:00:00.003Z"
                            ]
                        }
                    ]
                }
            ]
        }
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_future_timestamp_qualifier(self):
        stix_pattern = "[network-traffic:src_port < 53]START t'2024-09-19T11:00:00.000Z' " \
                       "STOP t'2024-02-07T11:00:00.003Z'"
        result = translation.translate('trellix_endpoint_security_hx', 'query', '{}', stix_pattern,
                                       {"host_sets": "host_set1"})
        assert result['success'] is False
        assert "translation_error" == result['code']
        assert 'Start/Stop time should not be in the future UTC timestamp' in result['error']

    def test_stop_time_lesser_than_start_time(self):
        stix_pattern = "[network-traffic:src_port > 32794]START t'2024-01-19T11:00:00.000Z' " \
                       "STOP t'2023-02-07T11:00:00.003Z'"
        result = translation.translate('trellix_endpoint_security_hx', 'query', '{}', stix_pattern,
                                       {"host_sets": "host_set1"})
        assert result['success'] is False
        assert "translation_error" == result['code']
        assert 'Start time should be lesser than Stop time' in result['error']

    def test_invalid_operator_for_trellix(self):
        stix_pattern = "[file:size >= 50]"
        result = translation.translate('trellix_endpoint_security_hx', 'query', '{}', stix_pattern,
                                       {"host_sets": "host_set1"})
        assert result['success'] is False
        assert "mapping_error" == result['code']
        assert 'data mapping error : Unable to map the following STIX Operators: [GreaterThanOrEqual] to data source ' \
               'fields' in \
               result['error']

    def test_invalid_operator_for_string_fields(self):
        stix_pattern = "[process:name < 'process']"
        result = translation.translate('trellix_endpoint_security_hx', 'query', '{}', stix_pattern,
                                       {"host_sets": "host_set1"})
        assert result['success'] is False
        assert "not_implemented" == result['code']
        assert 'LessThan operator is not supported for string type field ' in result['error']

    def test_un_supported_operator(self):
        stix_pattern = "[file:size NOT MATCHES '50']"
        result = translation.translate('trellix_endpoint_security_hx', 'query', '{}', stix_pattern,
                                       {"host_sets": "host_set1"})
        assert result['success'] is False
        assert "not_implemented" == result['code']
        assert 'Matches operator is not supported for integer type field ' in result['error']

    def test_similar_stix_attributes_for_and_operator(self):
        stix_pattern = "[ipv4-addr:value = '1.1.1.1' AND network-traffic:src_ref.value = '2.2.2.2' AND process:name= " \
                       "'cmd.exe' AND file:name='file.exe']"
        result = translation.translate('trellix_endpoint_security_hx', 'query', '{}', stix_pattern,
                                       {"host_sets": "host_set1"})
        assert result['success'] is False
        assert "translation_error" == result['code']
        assert 'The expression [ipv4-addr:value] has same data source field mapping with another expression in the ' \
               'pattern which has only AND comparison operator. Recommended to Use OR operator.' in \
               result['error']

    def test_similar_mapping_fields_in_different_attributes_for_and_operator(self):
        stix_pattern = "[ipv4-addr:value = '1.1.1.1' AND ipv4-addr:value != '2.2.2.2']"
        result = translation.translate('trellix_endpoint_security_hx', 'query', '{}', stix_pattern,
                                       {"host_sets": "host_set1"})
        assert result['success'] is False
        assert "translation_error" == result['code']
        assert ('Multiple [ipv4-addr:value] expression is used in the pattern which has only AND comparison operator. '
                'Recommended to Use OR operator for similar STIX attributes.') in result['error']

    def test_ipv4_addr_not_supported_operator(self):
        stix_pattern = "[ipv4-addr:value LIKE '1.1.1.1']"
        result = translation.translate('trellix_endpoint_security_hx', 'query', '{}', stix_pattern,
                                       {"host_sets": "host_set1"})
        assert result['success'] is False
        assert "not_implemented" == result['code']
        assert ('Like operator is not supported for IP Address type field ipv4-addr:value.Possible supported '
                'operators are  =, !=, IN, NOT IN') in \
               result['error']

    def test_stix_field_not_supported_operator(self):
        stix_pattern = "[file:hashes.MD5 MATCHES 'abc123']"
        result = translation.translate('trellix_endpoint_security_hx', 'query', '{}', stix_pattern,
                                       {"host_sets": "host_set1"})
        assert result['success'] is False
        assert "not_implemented" == result['code']
        assert ('Matches operator is not supported for File Hash type field file:hashes.MD5.Possible '
                'supported operators are  =, !=, IN, NOT IN') in \
               result['error']
