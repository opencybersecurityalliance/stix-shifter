from stix_shifter.stix_translation import stix_translation
import unittest
from datetime import datetime, timedelta

translation = stix_translation.StixTranslation()


def _remove_timestamp_from_query(queries):
    if isinstance(queries, list):
        query_list = []
        for query in queries:
            query.pop("start_date")
            query.pop("end_date")
            query_list.append(query)
        return query_list


class TestQueryTranslator(unittest.TestCase):
    """
    class to perform unit test case symantec translate query
    """
    end_time = datetime.strftime(datetime.utcnow(), '%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    start_time = datetime.strftime(datetime.utcnow() - timedelta(days =1), '%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
	
    if __name__ == "__main__":
        unittest.main()

    def _test_query_assertions(self, query, queries):
        """
        to assert each query in the list against expected result
        """
        self.assertIsInstance(queries, list)
        self.assertIsInstance(query, dict)
        self.assertIsInstance(query['queries'], list)
        for index, each_query in enumerate(query.get('queries'), start=0):
            self.assertEqual(each_query, queries[index])

    def test_equal_operator(self):
        stix_pattern = f"[ipv4-addr:value = '111.11.1.111'] START t'{self.start_time}' STOP t'{self.end_time}'"
        query = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'feature_name': 'ALL', 'product': 'SAEP',
                    'query': 'device_ip:"111.11.1.111" OR connection.src_ip:"111.11.1.111" OR '
                             'connection.dst_ip:"111.11.1.111" OR device_public_ip:"111.11.1.111" OR '
                             'device_networks.ipv4:"111.11.1.111" OR device_networks.gateway_ip:"111.11.1.111"',
                    'start_date': '2023-11-01T11:00:00.000+00:00', 'end_date': '2024-05-06T11:54:00.000+00:00'}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_not_equal_operator(self):
        stix_pattern = f"[ipv6-addr:value != '1234:a5a6:78910:1111:2222:3333'] START t'{self.start_time}' " \
                       f"STOP t'{self.end_time}'"
        query = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'feature_name': 'ALL', 'product': 'SAEP',
                    'query': '-device_ip:"1234\\:a5a6\\:78910\\:1111\\:2222\\:3333" OR'
                             ' -connection.src_ip:"1234\\:a5a6\\:78910\\:1111\\:2222\\:3333" OR'
                             ' -connection.dst_ip:"1234\\:a5a6\\:78910\\:1111\\:2222\\:3333" OR'
                             ' -device_networks.ipv6:"1234\\:a5a6\\:78910\\:1111\\:2222\\:3333"',
                    'start_date': '2023-11-01T11:00:00.000+00:00', 'end_date': '2024-05-06T11:54:00.000+00:00'}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_gt_operator(self):
        stix_pattern = f"[network-traffic:dst_port > 22] START t'{self.start_time}' STOP t'{self.end_time}'"
        query = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'feature_name': 'ALL', 'product': 'SAEP', 'query': 'connection.dst_port:{22 TO *}',
                    'start_date': '2023-11-01T11:00:00.000+00:00', 'end_date': '2024-05-06T11:54:00.000+00:00'}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_gt_eq_operator(self):
        stix_pattern = f"[network-traffic:dst_port >= 22] START t'{self.start_time}' STOP t'{self.end_time}'"
        query = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'feature_name': 'ALL', 'product': 'SAEP', 'query': 'connection.dst_port:[22 TO *}',
                    'start_date': '2023-11-01T11:00:00.000+00:00', 'end_date': '2024-05-06T11:54:00.000+00:00'}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_lt_operator(self):
        stix_pattern = f"[network-traffic:src_port < 22] START t'{self.start_time}' STOP t'{self.end_time}'"
        query = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'feature_name': 'ALL', 'product': 'SAEP', 'query': 'connection.src_port:{* TO 22}',
                    'start_date': '2023-11-01T11:00:00.000+00:00', 'end_date': '2024-05-06T11:54:00.000+00:00'}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_lt_eq_operator(self):
        stix_pattern = f"[network-traffic:src_port <= 22] START t'{self.start_time}' STOP t'{self.end_time}'"
        query = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'feature_name': 'ALL', 'product': 'SAEP', 'query': 'connection.src_port:{* TO 22]',
                    'start_date': '2024-05-01T11:00:00.000+00:00', 'end_date': '2024-05-06T11:54:00.000+00:00'}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_IN_operator(self):
        stix_pattern = f"[network-traffic:protocols[*] IN ('tcp', 'udp')] START t'{self.start_time}' " \
                       f"STOP t'{self.end_time}'"
        query = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'feature_name': 'ALL', 'product': 'SAEP', 'query': 'connection.protocol_id:("6" OR "17")',
                    'start_date': '2023-11-01T11:00:00.000+00:00', 'end_date': '2024-05-06T11:54:00.000+00:00'}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_like_operator(self):
        stix_pattern = f"[user-account:user_id LIKE 'SYSTEM'] START t'{self.start_time}' STOP t'{self.end_time}'"
        query = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'feature_name': 'ALL', 'product': 'SAEP', 'query': 'user.name:SYSTEM* OR actor.user.name:SYSTEM*'
                                                                       ' OR session.user.name:SYSTEM*',
                    'start_date': '2024-05-01T11:00:00.000+00:00', 'end_date': '2024-05-06T11:54:00.000+00:00'}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_matches_operator(self):
        stix_pattern = f"[process:name MATCHES 'host[a-z].exe'] START t'{self.start_time}' STOP t'{self.end_time}'"
        query = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'feature_name': 'ALL', 'product': 'SAEP',
                    'query': 'actor.app_name:/host[a-z].exe/ OR process.app_name:/host[a-z].exe/ OR'
                             ' parent.app_name:/host[a-z].exe/',
                    'start_date': '2024-05-01T11:00:00.000+00:00', 'end_date': '2024-05-06T11:54:00.000+00:00'}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_bool_operator(self):
        stix_pattern = f"[x-oca-geo:x_is_on_premises = 'true'] START t'{self.start_time}' STOP t'{self.end_time}'"
        query = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'feature_name': 'ALL', 'product': 'SAEP', 'query': 'device_location.on_premises:"true"',
                    'start_date': '2024-05-01T11:00:00.000+00:00', 'end_date': '2024-05-06T11:54:00.000+00:00'}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_date_supported_properries(self):
        stix_pattern = f"[file:created = '2024-03-19T04:43:06.377Z'] START t'{self.start_time}' STOP t'{self.end_time}'"
        query = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'feature_name': 'ALL', 'product': 'SAEP',
                    'query': 'actor.file.created:[ 1710823386377 TO 1710823386377 ] OR '
                             'parent.file.created:[ 1710823386377 TO 1710823386377 ] OR '
                             'process.file.created:[ 1710823386377 TO 1710823386377 ] OR '
                             'startup_app.file.created:[ 1710823386377 TO 1710823386377 ]',
                    'start_date': '2024-05-01T11:00:00.000+00:00', 'end_date': '2024-05-06T11:54:00.000+00:00'}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_not_supported_properties_for_like(self):
        stix_pattern = f"[mac-addr:value LIKE '11:aa:aa:11:11:11'] START t'{self.start_time}' STOP t'{self.end_time}'"
        query = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        assert False is query['success']
        assert 'not_implemented' == query['code']
        assert query['error'] == 'symantec_endpoint_security connector error => wrong parameter : LIKE/MATCHES ' \
                                 'operator is not supported for this fields device_mac,device_networks.mac,' \
                                 'device_networks.gateway_mac'

    def test_directory_path(self):
        stix_pattern = f"[directory:path = 'C:\\\\users\\\\administrator\\\\local\\\\data']" \
                       f"START t'{self.start_time}' STOP t'{self.end_time}'"
        query = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'feature_name': 'ALL', 'product': 'SAEP',
                    'query': 'file.folder:"C\\:\\\\users\\\\administrator\\\\local\\\\data" OR'
                             ' directory.folder:"C\\:\\\\users\\\\administrator\\\\local\\\\data" OR'
                             ' actor.file.folder:"C\\:\\\\users\\\\administrator\\\\local\\\\data" OR'
                             ' parent.file.folder:"C\\:\\\\users\\\\administrator\\\\local\\\\data" OR'
                             ' process.file.folder:"C\\:\\\\users\\\\administrator\\\\local\\\\data" OR'
                             ' module.folder:"C\\:\\\\users\\\\administrator\\\\local\\\\data" OR'
                             ' startup_app.file.folder:"C\\:\\\\users\\\\administrator\\\\local\\\\data"',
                    'start_date': '2024-05-01T00:00:00.000+00:00', 'end_date': '2024-05-01T11:00:00.000+00:00'}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_enum_operator(self):
        stix_pattern = f"[x-oca-event:severity = 15] START t'{self.start_time}' STOP t'{self.end_time}'"
        query = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'feature_name': 'ALL', 'product': 'SAEP', 'query': 'severity_id:"1"',
                    'start_date': '2023-11-01T11:00:00.000+00:00', 'end_date': '2024-05-06T11:54:00.000+00:00'}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_int_operator(self):
        stix_pattern = f"[process:pid > 1235] START t'{self.start_time}' STOP t'{self.end_time}'"
        query = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'feature_name': 'ALL', 'product': 'SAEP',
                    'query': 'actor.pid:{1235 TO *} OR process.pid:{1235 TO *} OR parent.pid:{1235 TO *}',
                    'start_date': '2023-11-01T11:00:00.000+00:00', 'end_date': '2024-05-06T11:54:00.000+00:00'}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_event_date_attribute(self):
        stix_pattern = f"[x-oca-event:created = '2024-05-21T13:27:21.526Z'] START t'{self.start_time}'" \
                       f" STOP t'{self.end_time}'"
        query = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{
                        "feature_name": "ALL",
                        "product": "SAEP",
                        "query": "time:[ 1716298041526 TO 1716298041526 ]",
                        "start_date": "2024-05-01T11:00:00.000+00:00",
                        "end_date": "2024-05-23T00:00:00.000+00:00"
                    }]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_file_date_attribute(self):
        stix_pattern = f"[file:created = '2024-03-19T04:43:06.377Z'] START t'{self.start_time}' STOP t'{self.end_time}'"
        query = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{
                    "feature_name": "ALL",
                    "product": "SAEP",
                    "query": "actor.file.created:[ 1710823386377 TO 1710823386377 ] OR "
                             "parent.file.created:[ 1710823386377 TO 1710823386377 ] OR "
                             "process.file.created:[ 1710823386377 TO 1710823386377 ] OR "
                             "startup_app.file.created:[ 1710823386377 TO 1710823386377 ]",
                    "start_date": "2024-05-01T11:00:00.000+00:00",
                    "end_date": "2024-05-23T00:00:00.000+00:00"
                }]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_protocol_attribute(self):
        stix_pattern = f"[network-traffic:protocols[*]='udp'] START t'{self.start_time}' STOP t'{self.end_time}'"
        query = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{
                    "feature_name": "ALL",
                    "product": "SAEP",
                    "query": "connection.protocol_id:\"17\"",
                    "start_date": "2024-03-15T16:43:26.000+00:00",
                    "end_date": "2024-05-25T06:23:26.003+00:00"
                }]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_combined_comparison_AND_operator(self):
        stix_pattern = "[network-traffic:dst_port = 445 AND (process:pid = 1010 AND user-account:user_id LIKE " \
                       f"'Administrator')] START t'{self.start_time}' STOP t'{self.end_time}'"
        query = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'feature_name': 'ALL', 'product': 'SAEP',
                    'query': '(connection.dst_port:"445") AND '
                             '((actor.pid:"1010" OR process.pid:"1010" OR parent.pid:"1010") AND'
                             ' (user.name:Administrator* OR actor.user.name:Administrator* OR'
                             ' session.user.name:Administrator*))',
                    'start_date': '2024-05-01T00:00:00.000+00:00', 'end_date': '2024-05-01T11:00:00.000+00:00'}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_combined_comparison_OR_operator(self):
        stix_pattern = f"[process:pid = 1010 OR user-account:user_id LIKE 'Administrator'] START t'{self.start_time}'" \
                       f" STOP t'{self.end_time}'"
        query = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'feature_name': 'ALL', 'product': 'SAEP',
                    'query': '(actor.pid:"1010" OR process.pid:"1010" OR parent.pid:"1010") OR'
                             ' (user.name:Administrator* OR actor.user.name:Administrator* OR'
                             ' session.user.name:Administrator*)',
                    'start_date': '2024-05-01T00:00:00.000+00:00', 'end_date': '2024-05-01T11:00:00.000+00:00'}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_combined_comparison_OR_AND_operators(self):
        stix_pattern = "[(x-oca-event:severity = 15 OR x-oca-event:category = 'Security') AND " \
                       "(x-oca-asset:host_type = 'server' AND x-symantec-policy:name = 'default')]" \
                       f" START t'{self.start_time}' STOP t'{self.end_time}'"
        query = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'feature_name': 'ALL', 'product': 'SAEP',
                    'query': '((severity_id:"1") OR (category_id:"1")) AND'
                             ' ((device_type:"server") AND (policy.name:"default"))',
                    'start_date': '2024-05-01T00:00:00.000+00:00', 'end_date': '2024-05-01T11:00:00.000+00:00'}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_combined_comparison(self):
        stix_pattern = "[x-ibm-finding:x_threat_type_id = 'Malware' OR " \
                       "(x-symantec-policy:name = 'malware_detection' AND" \
                       " x-ibm-ttp-tagging:name = 'Drive by Compromise') OR" \
                       " (x-user-session:is_remote = 'true' AND network-traffic:src_port = 22)]" \
                       f"START t'{self.start_time}' STOP t'{self.end_time}'"
        query = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'feature_name': 'ALL', 'product': 'SAEP',
                    'query': '((threat.type_id:"1") OR ((policy.name:"malware_detection") AND '
                             '(attacks.technique_name:"Drive by Compromise"))) OR '
                             '((session.remote:"true" OR actor.session.remote:"true") AND (connection.src_port:"22"))',
                    'start_date': '2024-05-01T00:00:00.000+00:00', 'end_date': '2024-05-01T11:00:00.000+00:00'}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_IN_operator_split_query(self):
        stix_pattern = "[file:hashes.'SHA-256' IN ('ABDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" \
                       "', 'ABDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B'," \
                       "'BBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A', " \
                       "'BBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B'," \
                       "'CBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A'," \
                       "'CBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B'," \
                       "'DBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A'," \
                       "'DBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B'," \
                       "'EBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A'," \
                       "'EBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B'," \
                       "'FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A'," \
                       "'FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B'," \
                       "'FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142C'," \
                       "'FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142E'," \
                       "'FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142F'," \
                       "'FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142G'," \
                       "'BBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A'," \
                       "'DBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A'," \
                       "'ABDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A'," \
                       f"'DDDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A')] START t'{self.start_time}' " \
                       f"STOP t'{self.end_time}'"
        query = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'feature_name': 'ALL', 'product': 'SAEP',
                    'query': 'file.sha2:("ABDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"ABDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"BBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"BBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"CBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"CBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"DBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"DBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"EBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"EBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142C" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142E" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142F" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142G" OR '
                             '"BBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"DBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"ABDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"DDDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A") OR '
                             'actor.file.sha2:('
                             '"ABDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"ABDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"BBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"BBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"CBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"CBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"DBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"DBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"EBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"EBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142C" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142E" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142F" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142G" OR '
                             '"BBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"DBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"ABDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"DDDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A") OR '
                             'module.sha2:('
                             '"ABDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"ABDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"BBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"BBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"CBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"CBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"DBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"DBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"EBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"EBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142C" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142E" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142F" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142G" OR '
                             '"BBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"DBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"ABDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"DDDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A") OR '
                             'parent.file.sha2:('
                             '"ABDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"ABDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"BBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"BBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"CBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"CBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"DBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"DBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"EBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"EBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142C" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142E" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142F" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142G" OR '
                             '"BBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"DBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"ABDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"DDDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A") OR '
                             'process.file.sha2:('
                             '"ABDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"ABDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"BBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"BBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"CBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"CBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"DBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"DBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"EBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"EBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142C" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142E" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142F" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142G" OR '
                             '"BBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"DBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"ABDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"DDDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A") OR '
                             'startup_app.file.sha2:('
                             '"ABDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"ABDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"BBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"BBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"CBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"CBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"DBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"DBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"EBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"EBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142B" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142C" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142E" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142F" OR '
                             '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142G" OR '
                             '"BBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"DBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"ABDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" OR '
                             '"DDDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A")',
                    'start_date': '2024-05-01T11:00:00.000+00:00', 'end_date': '2024-05-06T11:54:00.000+00:00'}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_observation_AND_operator(self):
        stix_pattern = f"([ipv4-addr:value = '1.1.1.1'] AND [file:name = 'cmd.exe']) START t'{self.start_time}' " \
                       f"STOP t'{self.end_time}'"
        query = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'feature_name': 'ALL', 'product': 'SAEP',
                    'query': '(file.name:"cmd.exe" OR directory.name:"cmd.exe" OR actor.file.name:"cmd.exe" OR '
                             'parent.file.name:"cmd.exe" OR process.file.name:"cmd.exe" OR module.name:"cmd.exe" OR '
                             'startup_app.file.name:"cmd.exe") OR '
                             '(device_ip:"1.1.1.1" OR connection.src_ip:"1.1.1.1" OR connection.dst_ip:"1.1.1.1" OR '
                             'device_public_ip:"1.1.1.1" OR device_networks.ipv4:"1.1.1.1" OR '
                             'device_networks.gateway_ip:"1.1.1.1")',
                    'start_date': '2024-05-01T01:56:00.000+00:00', 'end_date': '2024-05-01T01:57:00.003+00:00'}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_observation_OR_operator(self):
        stix_pattern = "([x-oca-event:severity = 15] OR [x-oca-asset:host_type = 'server'])" \
                       f"START t'{self.start_time}' STOP t'{self.end_time}'"
        query = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'feature_name': 'ALL', 'product': 'SAEP', 'query': '(device_type:"server") OR (severity_id:"1")',
                    'start_date': '2024-05-01T00:00:00.000+00:00', 'end_date': '2024-05-01T11:00:00.000+00:00'}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_observation_with_combined_comparison(self):
        stix_pattern = "([x-oca-asset:host_type = 'server' AND x-symantec-policy:name = 'default'] OR " \
                       "[mac-addr:value = '11:aa:aa:11:11:11'])" \
                       f"START t'{self.start_time}' STOP t'{self.end_time}'"
        query = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'feature_name': 'ALL', 'product': 'SAEP',
                    'query': '(device_mac:"11\\:aa\\:aa\\:11\\:11\\:11" OR '
                             'device_networks.mac:"11\\:aa\\:aa\\:11\\:11\\:11" OR'
                             ' device_networks.gateway_mac:"11\\:aa\\:aa\\:11\\:11\\:11") OR '
                             '((device_type:"server") AND (policy.name:"default"))',
                    'start_date': '2024-05-01T01:56:00.000+00:00', 'end_date': '2024-05-01T01:57:00.003+00:00'}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_combine_multiple_observation_with_same_date(self):
        stix_pattern = "([software:name IN ('Windows 10', 'iOS', 'Android')] OR " \
                       f"[(domain-name:value='internal.ec2.com')])START t'{self.start_time}' STOP t'{self.end_time}'"
        query = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'feature_name': 'ALL', 'product': 'SAEP',
                    'query': '(device_domain:"internal.ec2.com") OR '
                             '(device_os_name:("Windows 10" OR "iOS" OR "Android"))',
                    'start_date': '2024-01-01T01:56:00.000+00:00', 'end_date': '2024-05-01T01:57:00.003+00:00'}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_split_multiple_observation_OR_operator(self):
        """This case is to test proper parenthesis for date, if observation are not enclosed,
            split into 2 queries
        """
        stix_pattern = "[x-oca-event:severity = 15] OR [x-oca-asset:host_type = 'server']" \
                       f"START t'{self.start_time}' STOP t'{self.end_time}'"
        query = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'feature_name': 'ALL', 'product': 'SAEP', 'query': 'severity_id:"1"',
                    'start_date': '2024-05-16T03:18:59.120+00:00', 'end_date': '2024-05-16T03:23:59.120+00:00'},
                   {'feature_name': 'ALL', 'product': 'SAEP', 'query': 'device_type:"server"',
                    'start_date': '2024-05-01T00:00:00.000+00:00', 'end_date': '2024-05-01T11:00:00.000+00:00'}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_invalid_MATCHES_operator(self):
        stix_pattern = f"[user-account:is_privileged MATCHES 'true'] START t'{self.start_time}' STOP t'{self.end_time}'"
        query = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        assert False is query['success']
        assert 'not_implemented' == query['code']
        assert query['error'] == "symantec_endpoint_security connector error => wrong parameter : LIKE/MATCHES " \
                                 "operator is not supported for this fields actor.user.is_admin,session.user.is_admin"

    def test_invalid_int_input(self):
        stix_pattern = f"[process:pid = '123456789123'] START t'{self.start_time}' STOP t'{self.end_time}'"
        result = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert result['error'] == 'symantec_endpoint_security connector error => wrong parameter : String type input' \
                                  ' 123456789123 is not supported for integer type field'

    def test_invalid_enum_value(self):
        stix_pattern = f"[x-oca-event:category = 'TEST'] START t'{self.start_time}' STOP t'{self.end_time}'"
        result = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert result['error'] == "symantec_endpoint_security connector error => wrong parameter : Unsupported ENUM " \
                                  "values provided. category_id possible supported enum values are " \
                                  "'Security,Application Activity,System Activity'"

    def test_invalid_timestamp(self):
        stix_pattern = f"[network-traffic:dst_port = 'symantec'] START t'2024' STOP t'{self.end_time}'"
        result = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'translation_error' == result['code']
        assert result['error'] == "symantec_endpoint_security connector error => STIX translation " \
                                  "error: Invalid STIX timestamp None"

    def test_invalid_mapping_value(self):
        stix_pattern = f"[file:type LIKE 'cmd.exe']START t'{self.start_time}' STOP t'{self.end_time}'"
        result = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'mapping_error' == result['code']
        assert result['error'] == "symantec_endpoint_security connector error => data mapping error : Unable to map " \
                                  "the following STIX objects and properties: [\'file:type\'] to data source fields"

    def test_severity_range(self):
        stix_pattern = f"[x-oca-event:severity = 200]START t'{self.start_time}' STOP t'{self.end_time}'"
        result = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert result[
                   'error'] == "symantec_endpoint_security connector error => wrong parameter : Severity allowed" \
                               " range from 0 to 100"

    def test_not_supported_operators(self):
        stix_pattern = f"[network-traffic:dst_port ISSUBSET '445'] START t'{self.start_time}' STOP t'{self.end_time}'"
        result = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'mapping_error' == result['code']
        assert result['error'] == "symantec_endpoint_security connector error => data mapping error : Unable to map" \
                                  " the following STIX Operators: [IsSubSet] to data source fields"

    def test_invalid_like_values(self):
        stix_pattern = f"[user-account:user_id LIKE 'LOCAL SERVICE'] START t'{self.start_time}' STOP t'{self.end_time}'"
        result = translation.translate('symantec_endpoint_security', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert result['error'] == "symantec_endpoint_security connector error => wrong parameter : LIKE does not " \
                                  "support on phrases, supports on single term. LOCAL SERVICE contains multiple terms"
