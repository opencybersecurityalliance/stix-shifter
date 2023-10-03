from stix_shifter.stix_translation import stix_translation
import unittest
import re

translation = stix_translation.StixTranslation()


def _remove_timestamp_from_query(queries):
    pattern = r'detection.last_timestamp:\[([^>]*?)]'
    if isinstance(queries, list):
        return [re.sub(pattern, '', str(query)) for query in queries]
    elif isinstance(queries, str):
        return re.sub(pattern, '', queries)


class TestQueryTranslator(unittest.TestCase):
    """
    class to perform unit test case vectra translate query
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

    def test_equal_operator(self):
        stix_pattern = "[x-ibm-finding:confidence = 22]"
        query = translation.translate('vectra', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['query_string=((detection.certainty:"22") AND (detection.last_timestamp:[2023-07-05T0729 to '
                   '2023-07-05T0734]))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_not_equal_operator(self):
        stix_pattern = "[network-traffic:x_rpc_uuid != 'tp']"
        query = translation.translate('vectra', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['query_string=(((detection.grouped_details.uuid:* AND NOT detection.grouped_details.uuid:"tp")) '
                   'AND (detection.last_timestamp:[2023-07-05T0803 to 2023-07-05T0808]))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_like_operator(self):
        stix_pattern = "[domain-name:value LIKE 'google.com']"
        query = translation.translate('vectra', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['query_string=((detection.grouped_details.target_domains:google.com OR '
                   'detection.grouped_details.origin_domain:google.com OR '
                   'detection.grouped_details.events.target_domains:google.com OR '
                   'detection.grouped_details.connection_events.target_host.dst_dns:google.com) AND ('
                   'detection.last_timestamp:[2023-06-08T1159 to 2023-06-08T1204]))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_not_like_operator(self):
        stix_pattern = "[x-ibm-finding:x_state NOT LIKE 'unknown']"
        query = translation.translate('vectra', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['query_string=(((detection.state:* AND NOT detection.state:unknown)) AND ('
                   'detection.last_timestamp:[2023-07-05T0805 to 2023-07-05T0810]))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_greater_than_operator(self):
        stix_pattern = "[network-traffic:dst_port > 2]"
        query = translation.translate('vectra', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['query_string=((detection.grouped_details.dst_ports:>"2" OR '
                   'detection.grouped_details.dst_hosts.dst_port:>"2" OR detection.grouped_details.origin_port:>"2" '
                   'OR detection.grouped_details.sessions.dst_port:>"2" OR '
                   'detection.grouped_details.events.dst_ports:>"2" OR '
                   'detection.grouped_details.events.sessions.dst_port:>"2" OR '
                   'detection.grouped_details.events.target_summary.dst_port:>"2" OR '
                   'detection.grouped_details.connection_events.dst_port:>"2") AND (detection.last_timestamp:['
                   '2023-06-26T0839 to 2023-06-26T0844]))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_lt_operator(self):
        stix_pattern = "[network-traffic:src_byte_count < 120]"
        query = translation.translate('vectra', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['query_string=((detection.grouped_details.bytes_sent:<"120" OR '
                   'detection.grouped_details.sessions.bytes_sent:<"120" OR '
                   'detection.grouped_details.events.bytes_sent:<"120" OR '
                   'detection.grouped_details.connection_events.total_bytes_sent:<"120") AND ('
                   'detection.last_timestamp:[2023-06-08T1202 to 2023-06-08T1207]))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_gt_or_equal_operator(self):
        stix_pattern = "[network-traffic:dst_byte_count >= 175]"
        query = translation.translate('vectra', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['query_string=((detection.grouped_details.bytes_received:>="175" OR '
                   'detection.grouped_details.sessions.bytes_received:>="175" OR '
                   'detection.grouped_details.events.bytes_received:>="175" OR '
                   'detection.grouped_details.events.sessions.bytes_received:>="175" OR '
                   'detection.grouped_details.connection_events.total_bytes_rcvd:>="175") AND ('
                   'detection.last_timestamp:[2023-06-08T1152 to 2023-06-08T1157]))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_lt_or_equal_operator(self):
        stix_pattern = "[network-traffic:dst_port <= 176]"
        query = translation.translate('vectra', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['query_string=((detection.grouped_details.dst_ports:<="176" OR '
                   'detection.grouped_details.dst_hosts.dst_port:<="176" OR '
                   'detection.grouped_details.origin_port:<="176" OR '
                   'detection.grouped_details.sessions.dst_port:<="176" OR '
                   'detection.grouped_details.events.dst_ports:<="176" OR '
                   'detection.grouped_details.events.sessions.dst_port:<="176" OR '
                   'detection.grouped_details.events.target_summary.dst_port:<="176" OR '
                   'detection.grouped_details.connection_events.dst_port:<="176") AND (detection.last_timestamp:['
                   '2023-06-26T0834 to 2023-06-26T0839]))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_matches_operator(self):
        stix_pattern = "[network-traffic:protocols[*] MATCHES 'http']"
        query = translation.translate('vectra', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['query_string=((detection.grouped_details.protocol:*http* OR '
                   'detection.grouped_details.app_protocol:*http* OR detection.grouped_details.dst_protocol:*http* OR '
                   'detection.grouped_details.origin_protocol:*http* OR '
                   'detection.grouped_details.sessions.protocol:*http* OR '
                   'detection.grouped_details.sessions.app_protocol:*http* OR '
                   'detection.grouped_details.events.protocol:*http* OR '
                   'detection.grouped_details.events.sessions.app_protocol:*http* OR '
                   'detection.grouped_details.events.sessions.protocol:*http* OR '
                   'detection.grouped_details.events.target_summary.app_protocol:*http* OR '
                   'detection.grouped_details.events.target_summary.protocol:*http* OR '
                   'detection.grouped_details.connection_events.protocol:*http*) AND (detection.last_timestamp:['
                   '2023-06-08T1212 to 2023-06-08T1217]))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_not_matches_operator(self):
        stix_pattern = "[x-ibm-finding:x_sensor_name NOT MATCHES 'qualys']"
        query = translation.translate('vectra', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['query_string=(((detection.sensor_name:* AND NOT detection.sensor_name:*qualys*)) AND ('
                   'detection.last_timestamp:[2023-07-05T0807 to 2023-07-05T0812]))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_in_operator(self):
        stix_pattern = "[x-ibm-finding:description IN ('vulnerbility','threat')]"
        query = translation.translate('vectra', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['query_string=((detection.description:"vulnerbility" OR detection.description:"threat" OR '
                   'detection.summary.description:"vulnerbility" OR detection.summary.description:"threat") AND ('
                   'detection.last_timestamp:[2023-07-05T0731 to 2023-07-05T0736]))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_not_in_operator(self):
        stix_pattern = "[x-ibm-finding:description NOT IN ('attack','cyber')]"
        query = translation.translate('vectra', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['query_string=(((detection.description:* AND NOT detection.description:"attack") OR ('
                   'detection.description:* AND NOT detection.description:"cyber") OR ('
                   'detection.summary.description:* AND NOT detection.summary.description:"attack") OR ('
                   'detection.summary.description:* AND NOT detection.summary.description:"cyber")) AND ('
                   'detection.last_timestamp:[2023-07-05T0804 to 2023-07-05T0809]))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_combined_comparison_AND_operator(self):
        stix_pattern = "[x-ibm-finding:severity = '25' AND x-ibm-finding:time_observed = '2022-05-11T00:00:00Z']"
        query = translation.translate('vectra', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['query_string=(((detection.created_timestamp:"2022-05-11T0000") AND (detection.threat:"25")) AND ('
                   'detection.last_timestamp:[2023-07-05T0710 to 2023-07-05T0715]))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_combined_comparison_OR_operator(self):
        stix_pattern = "[network-traffic:severity < 5 OR network-traffic:x_rpc_uuid != 'operate'] START " \
                       "t'2022-05-15T16:43:26.000Z' STOP t'2023-10-25T16:43:26.003Z'"
        query = translation.translate('vectra', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['query_string=(((detection.grouped_details.uuid:* AND NOT '
                   'detection.grouped_details.uuid:"operate")) AND ())']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_observation_AND_operator(self):
        stix_pattern = "[network-traffic:src_ref.value = 192] AND [network-traffic:protocols[*] = 'tcp'] START " \
                       "t'2022-05-15T16:43:26.000Z' STOP t'2023-10-25T16:43:26.003Z'"
        query = translation.translate('vectra', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['query_string=(((detection.src_ip:"192") AND ()) OR ((detection.grouped_details.protocol:"tcp" OR '
                   'detection.grouped_details.app_protocol:"tcp" OR detection.grouped_details.dst_protocol:"tcp" OR '
                   'detection.grouped_details.origin_protocol:"tcp" OR '
                   'detection.grouped_details.sessions.protocol:"tcp" OR '
                   'detection.grouped_details.sessions.app_protocol:"tcp" OR '
                   'detection.grouped_details.events.protocol:"tcp" OR '
                   'detection.grouped_details.events.sessions.app_protocol:"tcp" OR '
                   'detection.grouped_details.events.sessions.protocol:"tcp" OR '
                   'detection.grouped_details.events.target_summary.app_protocol:"tcp" OR '
                   'detection.grouped_details.events.target_summary.protocol:"tcp" OR '
                   'detection.grouped_details.connection_events.protocol:"tcp") AND ()))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_observation_OR_operator(self):
        stix_pattern = "[x-ibm-finding:alert_id = '5678'] OR [x-ibm-finding:severity > 5]"
        query = translation.translate('vectra', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['query_string=(((detection.id:"5678") AND (detection.last_timestamp:[2023-07-05T0739 to '
                   '2023-07-05T0744])) OR ((detection.threat:>"5") AND (detection.last_timestamp:[2023-07-05T0739 to '
                   '2023-07-05T0744])))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_observation_with_combined_comparison(self):
        stix_pattern = "([network-traffic:protocol[*] MATCHES 't' AND network-traffic:src_ref.value = '1.1.1.1'] OR [" \
                       "x-oca-asset:hostname NOT LIKE '11.34.00.23']) START t'2022-11-07T00:00:01Z' STOP " \
                       "t'2023-03-06T11:00:00.003Z'"
        query = translation.translate('vectra', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['query_string=(((detection.src_host.name:* AND NOT detection.src_host.name:11.34.00.23)) AND ('
                   'detection.last_timestamp:[2022-11-07T0000 to 2023-03-06T1100]))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_observation_with_qualifire(self):
        stix_pattern = "([network-traffic:src_ref.value = '1.1.1.1'] OR [ x-oca-asset:hostname NOT LIKE " \
                       "'11.34.00.23']) START t'2022-11-07T00:00:01Z' STOP t'2023-03-06T11:00:00.003Z'"
        query = translation.translate('vectra', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['query_string=(((detection.src_ip:"1.1.1.1") AND (detection.last_timestamp:[2022-11-07T0000 to '
                   '2023-03-06T1100])) OR (((detection.src_host.name:* AND NOT detection.src_host.name:11.34.00.23)) '
                   'AND (detection.last_timestamp:[2022-11-07T0000 to 2023-03-06T1100])))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_lt_operator_with_timestamp(self):
        stix_pattern = "[network-traffic:start < '2023-05-30T00:00:01Z'] START t'2022-11-07T00:00:01Z' STOP " \
                       "t'2023-03-06T11:00:00.003Z'"
        query = translation.translate('vectra', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['query_string=((detection.first_timestamp:<"2023-05-30T0000" OR '
                   'detection.grouped_details.first_timestamp:<"2023-05-30T0000" OR '
                   'detection.grouped_details.sessions.first_timestamp:<"2023-05-30T0000" OR '
                   'detection.grouped_details.events.first_timestamp:<"2023-05-30T0000" OR '
                   'detection.grouped_details.events.sessions.first_timestamp:<"2023-05-30T0000" OR '
                   'detection.grouped_details.events.target_summary.first_timestamp:<"2023-05-30T0000" OR '
                   'detection.grouped_details.connection_events.first_timestamp:<"2023-05-30T0000") AND ('
                   'detection.last_timestamp:[2022-11-07T0000 to 2023-03-06T1100]))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_boolean_field(self):
        stix_pattern = "[x-ibm-finding:x_is_triaged = 'true']"
        query = translation.translate('vectra', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['query_string=((detection.is_triaged:"true") AND (detection.last_timestamp:[2023-07-05T0708 to '
                   '2023-07-05T0713]))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_split_OR_query(self):
        stix_pattern = "[network-traffic:protocols[*] = 'tcp' OR (ipv4-addr:value = '1.1.1.1')] OR [" \
                       "ipv4-addr:value = '11.111.111.11'] START t'2023-02-15T16:43:26.000Z' STOP " \
                       "t'2023-03-25T16:43:26.003Z'"
        query = translation.translate('vectra', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [
            'query_string=(detection.src_ip:"1.1.1.1" OR detection.grouped_details.dst_ips:"1.1.1.1" OR '
            'detection.grouped_details.dst_hosts.dst_ip:"1.1.1.1" OR '
            'detection.grouped_details.normal_admin_hosts.ip:"1.1.1.1" OR '
            'detection.grouped_details.dst_hosts.ip:"1.1.1.1" OR detection.grouped_details.origin_ip:"1.1.1.1" OR '
            'detection.grouped_details.sessions.dst_ip:"1.1.1.1" OR '
            'detection.grouped_details.events.dst_ip:"1.1.1.1" OR detection.grouped_details.events.dst_ips:"1.1.1.1" '
            'OR detection.grouped_details.events.sessions.dst_ip:"1.1.1.1" OR '
            'detection.grouped_details.connection_events.target_host.ip:"1.1.1.1") AND (detection.last_timestamp:['
            '2023-07-06T1315 to 2023-07-06T1320])',
            'query_string=(detection.grouped_details.protocol:"tcp" OR detection.grouped_details.app_protocol:"tcp" '
            'OR detection.grouped_details.dst_protocol:"tcp" OR detection.grouped_details.origin_protocol:"tcp" OR '
            'detection.grouped_details.sessions.protocol:"tcp" OR '
            'detection.grouped_details.sessions.app_protocol:"tcp" OR detection.grouped_details.events.protocol:"tcp" '
            'OR detection.grouped_details.events.sessions.app_protocol:"tcp" OR '
            'detection.grouped_details.events.sessions.protocol:"tcp" OR '
            'detection.grouped_details.events.target_summary.app_protocol:"tcp" OR '
            'detection.grouped_details.events.target_summary.protocol:"tcp" OR '
            'detection.grouped_details.connection_events.protocol:"tcp") AND (detection.last_timestamp:['
            '2023-07-06T1315 to 2023-07-06T1320])',
            'query_string=(detection.src_ip:"11.111.111.11" OR detection.grouped_details.dst_ips:"11.111.111.11" OR '
            'detection.grouped_details.dst_hosts.dst_ip:"11.111.111.11" OR '
            'detection.grouped_details.normal_admin_hosts.ip:"11.111.111.11" OR '
            'detection.grouped_details.dst_hosts.ip:"11.111.111.11" OR '
            'detection.grouped_details.origin_ip:"11.111.111.11" OR '
            'detection.grouped_details.sessions.dst_ip:"11.111.111.11" OR '
            'detection.grouped_details.events.dst_ip:"11.111.111.11" OR '
            'detection.grouped_details.events.dst_ips:"11.111.111.11" OR '
            'detection.grouped_details.events.sessions.dst_ip:"11.111.111.11" OR '
            'detection.grouped_details.connection_events.target_host.ip:"11.111.111.11") AND ('
            'detection.last_timestamp:[2023-02-15T1643 to 2023-03-25T1643])']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_split_IN_query(self):
        stix_pattern = "[network-traffic:protocols[*] IN ('tcp','udp') OR (user-account:id != 'ADMIN')] START " \
                       "t'2023-02-15T16:43:26.000Z' STOP t'2023-03-25T16:43:26.003Z'"
        query = translation.translate('vectra', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [
            'query_string=((detection.grouped_details.protocol:"tcp" OR detection.grouped_details.protocol:"udp" OR '
            'detection.grouped_details.app_protocol:"tcp" OR detection.grouped_details.app_protocol:"udp" OR '
            'detection.grouped_details.dst_protocol:"tcp" OR detection.grouped_details.dst_protocol:"udp" OR '
            'detection.grouped_details.origin_protocol:"tcp" OR detection.grouped_details.origin_protocol:"udp" OR '
            'detection.grouped_details.sessions.protocol:"tcp" OR detection.grouped_details.sessions.protocol:"udp" '
            'OR detection.grouped_details.sessions.app_protocol:"tcp" OR '
            'detection.grouped_details.sessions.app_protocol:"udp" OR detection.grouped_details.events.protocol:"tcp" '
            'OR detection.grouped_details.events.protocol:"udp" OR '
            'detection.grouped_details.events.sessions.app_protocol:"tcp" OR '
            'detection.grouped_details.events.sessions.app_protocol:"udp" OR '
            'detection.grouped_details.events.sessions.protocol:"tcp" )) AND (detection.last_timestamp:['
            '2023-02-15T1643 to 2023-03-25T1643])',
            'query_string=(( detection.grouped_details.events.sessions.protocol:"udp" OR '
            'detection.grouped_details.events.target_summary.app_protocol:"tcp" OR '
            'detection.grouped_details.events.target_summary.app_protocol:"udp" OR '
            'detection.grouped_details.events.target_summary.protocol:"tcp" OR '
            'detection.grouped_details.events.target_summary.protocol:"udp" OR '
            'detection.grouped_details.connection_events.protocol:"tcp" OR '
            'detection.grouped_details.connection_events.protocol:"udp")) AND (detection.last_timestamp:['
            '2023-02-15T1643 to 2023-03-25T1643])']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_split_multiple_operator(self):
        stix_pattern = "[ipv4-addr:value != '1.1.1.1' OR (network-traffic:x_time_duration > 4000 AND " \
                       "network-traffic:x_time_duration < 2000)] START t'2023-05-15T16:43:26.000Z' STOP " \
                       "t'2023-06-25T16:43:26.003Z'"
        query = translation.translate('vectra', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [
            'query_string=((detection.grouped_details.duration:<"2000" OR '
            'detection.grouped_details.events.duration:<"2000" OR '
            'detection.grouped_details.events.sessions.duration:<"2000" OR '
            'detection.grouped_details.connection_events.duration_int:<"2000") AND ('
            'detection.grouped_details.duration:>"4000" OR detection.grouped_details.events.duration:>"4000" OR '
            'detection.grouped_details.events.sessions.duration:>"4000" OR '
            'detection.grouped_details.connection_events.duration_int:>"4000") OR (detection.src_ip:* AND NOT '
            'detection.src_ip:"1.1.1.1") OR (detection.grouped_details.dst_ips:* AND NOT '
            'detection.grouped_details.dst_ips:"1.1.1.1") OR (detection.grouped_details.dst_hosts.dst_ip:* AND NOT '
            'detection.grouped_details.dst_hosts.dst_ip:"1.1.1.1") OR ('
            'detection.grouped_details.normal_admin_hosts.ip:* AND NOT '
            'detection.grouped_details.normal_admin_hosts.ip:"1.1.1.1")) AND (detection.last_timestamp:['
            '2023-05-15T1643 to 2023-06-25T1643])',
            'query_string=((detection.grouped_details.dst_hosts.ip:* AND NOT '
            'detection.grouped_details.dst_hosts.ip:"1.1.1.1") OR (detection.grouped_details.origin_ip:* AND NOT '
            'detection.grouped_details.origin_ip:"1.1.1.1") OR (detection.grouped_details.sessions.dst_ip:* AND NOT '
            'detection.grouped_details.sessions.dst_ip:"1.1.1.1") OR (detection.grouped_details.events.dst_ip:* AND NOT '
            'detection.grouped_details.events.dst_ip:"1.1.1.1") OR (detection.grouped_details.events.dst_ips:* AND '
            'NOT detection.grouped_details.events.dst_ips:"1.1.1.1") OR ('
            'detection.grouped_details.events.sessions.dst_ip:* AND NOT '
            'detection.grouped_details.events.sessions.dst_ip:"1.1.1.1") OR ('
            'detection.grouped_details.connection_events.target_host.ip:* AND NOT '
            'detection.grouped_details.connection_events.target_host.ip:"1.1.1.1")) AND (detection.last_timestamp:['
            '2023-05-15T1643 to 2023-06-25T1643])']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_split_contain_AND_query(self):
        stix_pattern = "[ipv4-addr:value != '1.1.1.1' AND network-traffic:x_time_duration < 2000] START " \
                       "t'2023-05-15T16:43:26.000Z' STOP t'2023-06-25T16:43:26.003Z'"

        query = translation.translate('vectra', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['query_string=(((detection.grouped_details.duration:<"2000" OR '
                   'detection.grouped_details.events.duration:<"2000" OR '
                   'detection.grouped_details.events.sessions.duration:<"2000" OR '
                   'detection.grouped_details.connection_events.duration_int:<"2000") AND ((detection.src_ip:* AND '
                   'NOT detection.src_ip:"1.1.1.1") OR (detection.grouped_details.dst_ips:* AND NOT '
                   'detection.grouped_details.dst_ips:"1.1.1.1") OR (detection.grouped_details.dst_hosts.dst_ip:* AND '
                   'NOT detection.grouped_details.dst_hosts.dst_ip:"1.1.1.1") OR ('
                   'detection.grouped_details.normal_admin_hosts.ip:* AND NOT '
                   'detection.grouped_details.normal_admin_hosts.ip:"1.1.1.1") OR ('
                   'detection.grouped_details.dst_hosts.ip:* AND NOT '
                   'detection.grouped_details.dst_hosts.ip:"1.1.1.1") OR (detection.grouped_details.origin_ip:* AND '
                   'NOT detection.grouped_details.origin_ip:"1.1.1.1") OR ('
                   'detection.grouped_details.sessions.dst_ip:* AND NOT '
                   'detection.grouped_details.sessions.dst_ip:"1.1.1.1") OR (detection.grouped_details.events.dst_ip:* AND '
                   'NOT detection.grouped_details.events.dst_ip:"1.1.1.1") OR ('
                   'detection.grouped_details.events.dst_ips:* AND NOT '
                   'detection.grouped_details.events.dst_ips:"1.1.1.1") OR ('
                   'detection.grouped_details.events.sessions.dst_ip:* AND NOT '
                   'detection.grouped_details.events.sessions.dst_ip:"1.1.1.1") OR ('
                   'detection.grouped_details.connection_events.target_host.ip:* AND NOT '
                   'detection.grouped_details.connection_events.target_host.ip:"1.1.1.1"))) AND ('
                   'detection.last_timestamp:[2023-05-15T1643 to 2023-06-25T1643]))']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_invalid_matches_operator(self):
        stix_pattern = "[network-traffic:src_byte_count MATCHES '120']"
        result = translation.translate('vectra', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert result['error'] == 'vectra connector error => wrong parameter : MATCHES operator is supported only for ' \
                                  'string type input'

    def test_invalid_matches_symbol(self):
        stix_pattern = "[x-ibm-finding:x_sensor_name NOT MATCHES 'qualys^']"
        result = translation.translate('vectra', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert result['error'] == 'vectra connector error => wrong parameter : ^ symbol should be at the starting ' \
                                  'position of the expression'

    def test_invalid_matches_contains_dollar(self):
        stix_pattern = "[network-traffic:protocols[*] MATCHES '$cd']"
        result = translation.translate('vectra', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert result['error'] == 'vectra connector error => wrong parameter : $ symbol should be at the ending ' \
                                  'position of the expression'

    def test_like_operator_for_integer_field(self):
        stix_pattern = "[network-traffic:dst_port LIKE '22']"
        result = translation.translate('vectra', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert result['error'] == 'vectra connector error => wrong parameter : LIKE operator is supported only for ' \
                                  'string type input'

    def test_string_input_for_integer_fields(self):
        stix_pattern = "[network-traffic:dst_port = 'none' ]"
        result = translation.translate('vectra', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert result['error'] == 'vectra connector error => wrong parameter : string type input - none is not ' \
                                  'supported for integer type fields'

    def test_invalid_timestamp_format(self):
        stix_pattern = "[network-traffic:start < '2023'] START t'2022-11-07T00:00:01Z' STOP t'2023-03-06T11:00:00.003Z'"
        result = translation.translate('vectra', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert result['error'] == 'vectra connector error => wrong parameter : cannot format the timestamp 2023'

    def test_invalid_boolean_operator(self):
        stix_pattern = "[x-ibm-finding:x_is_triaged > 'True']"
        result = translation.translate('vectra', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert 'vectra connector error => wrong parameter : :> operator is not supported for Boolean type input. ' \
               'Possible supported operator are [ =, !=, IN, NOT IN ]'

    def test_invalid_boolean(self):
        stix_pattern = "[x-ibm-finding:x_is_triaged = '10']"
        result = translation.translate('vectra', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert result['error'] == 'vectra connector error => wrong parameter : Boolean type field allows only ' \
                                  'true/false'

    def test_invalid_timestamp(self):
        stix_pattern = "[network-traffic:dst_port = 38] START t'0000-03-01T11:00:00.003Z' STOP " \
                       "t'2023-03-13T11:00:00.003Z'"
        result = translation.translate('vectra', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert result['error'] == 'vectra connector error => wrong parameter : cannot format the timestamp ' \
                                  '0000-03-01T11:00:00.003Z'

    def test_invalid_compare_operator(self):
        stix_pattern = "[x-ibm-finding:description > 'important']"
        result = translation.translate('vectra', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert result['error'] == 'vectra connector error => wrong parameter : > operator is not supported for string' \
                                  ' type input'

    def test_invalid_match_operator(self):
        stix_pattern = "[user-account:user_id MATCHES 'AR EX*']"
        result = translation.translate('vectra', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert result['error'] == 'vectra connector error => wrong parameter : MATCHES operator is not supported for ' \
                                  'value contains spaces'

    def test_invalid_like_operator(self):
        stix_pattern = "[network-traffic:x_reason LIKE 'LO ']"
        result = translation.translate('vectra', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert result['error'] == 'vectra connector error => wrong parameter : LIKE operator is not supported for ' \
                                  'value contains spaces'

    def test_invalid_not_operator(self):
        stix_pattern = "[network-traffic:dst_port != 22]"
        result = translation.translate('vectra', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert result['error'] == 'vectra connector error => wrong parameter : Not operator is only supported for ' \
                                  'string type fields'
