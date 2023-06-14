from stix_shifter.stix_translation import stix_translation
import unittest
import re

translation = stix_translation.StixTranslation()


def _remove_timestamp_from_query(queries):
    pattern = r'[\^&since\-TZ.=:\&until\d]{62}'
    if isinstance(queries, list):
        return [re.sub(pattern, '', str(query)) for query in queries]
    elif isinstance(queries, str):
        return re.sub(pattern, '', queries)


class TestQueryTranslator(unittest.TestCase):
    """
    class to perform unit test case okta translate query
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

    def test_ipv4_query(self):
        stix_pattern = "[ipv4-addr:value = '168.149.166.41']"
        query = translation.translate('okta', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["filter=request.ipChain.ip eq \"168.149.166.41\" &since=2023-02-07T05:19:43.647Z"
                   "&until=2023-02-07T05:24:43.647Z"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_autonomous_system_not_equal_operator(self):
        stix_pattern = "[autonomous-system:name != 'amazon.com inc.']"
        query = translation.translate('okta', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["filter=securityContext.asOrg ne \"amazon.com inc.\" &since=2023-02-07T05:18:30.082Z"
                   "&until=2023-02-07T05:23:30.082Z"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_autonomous_system_gt_operator(self):
        stix_pattern = "[autonomous-system:number > 50]"
        query = translation.translate('okta', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["filter=securityContext.asNumber gt 50 &since=2023-02-07T05:17:30.842Z"
                   "&until=2023-02-07T05:22:30.842Z"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_autonomous_system_ge_operator(self):
        stix_pattern = "[autonomous-system:number >= 50]"
        query = translation.translate('okta', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["filter=securityContext.asNumber ge 50 &since=2023-02-07T05:16:48.556Z"
                   "&until=2023-02-07T05:21:48.556Z"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_autonomous_system_lt_operator(self):
        stix_pattern = "[autonomous-system:number < 50]"
        query = translation.translate('okta', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["filter=securityContext.asNumber lt 50 &since=2023-02-07T05:15:55.733Z"
                   "&until=2023-02-07T05:20:55.733Z"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_autonomous_system_Not_lt_operator(self):
        stix_pattern = "[autonomous-system:number NOT < 50]"
        query = translation.translate('okta', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["filter=not(securityContext.asNumber lt 50) &since=2023-02-07T05:14:29.430Z"
                   "&until=2023-02-07T05:19:29.430Z"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_autonomous_system_le_operator(self):
        stix_pattern = "[autonomous-system:number <= 50]"
        query = translation.translate('okta', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["filter=securityContext.asNumber le 50 &since=2023-02-07T05:13:40.306Z"
                   "&until=2023-02-07T05:18:40.306Z"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_domain_name_like_operator(self):
        stix_pattern = "[domain-name:value LIKE 'amazonaws.com']"
        query = translation.translate('okta', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["filter=securityContext.domain co \"amazonaws.com\" &since=2023-02-07T05:12:47.444Z"
                   "&until=2023-02-07T05:17:47.444Z"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_okta_target_matches_operator(self):
        stix_pattern = "[x-okta-target:target_id MATCHES '0oa4oexp00i4BMrzJ5d7']"
        query = translation.translate('okta', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["filter=target.id co \"0oa4oexp00i4BMrzJ5d7\" &since=2023-02-13T10:50:41.269Z"
                   "&until=2023-02-13T10:55:41.269Z"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_software_MATCHES_operator(self):
        stix_pattern = "[software:x_raw_user_agent MATCHES 'Mozilla/5.0 (Windows NT 10.0; " \
                       "Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                       "Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70']"
        query = translation.translate('okta', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["filter=client.userAgent.rawUserAgent co \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70\" "
                   "&since=2023-02-13T11:02:45.831Z&until=2023-02-13T11:07:45.831Z"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_x_oca_event_query(self):
        stix_pattern = "[x-oca-event:action = 'app.oauth2.authorize.code']"
        query = translation.translate('okta', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["filter=eventType eq \"app.oauth2.authorize.code\" "
                   "&since=2023-02-07T05:09:34.284Z&until=2023-02-07T05:14:34.284Z"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_x_okta_client_query(self):
        stix_pattern = "[x-okta-client:geolocation_postalcode= 600001]"
        query = translation.translate('okta', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["filter=client.geographicalContext.postalCode eq \"600001\" &since=2023-02-13T11:11:37.914Z"
                   "&until=2023-02-13T11:16:37.914Z"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_user_account_string_value_with_gt_operator(self):
        stix_pattern = "[user-account:display_name > 'Okta System']"
        query = translation.translate('okta', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["filter=actor.displayName gt \"Okta System\" &since=2023-02-13T12:21:07.168Z"
                   "&until=2023-02-13T12:26:07.168Z"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_autonomous_system_string_value_le_operator(self):
        stix_pattern = "[autonomous-system:x_isp <= 'google']"
        query = translation.translate('okta', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["filter=securityContext.isp le \"google\" &since=2023-02-13T12:17:01.526Z"
                   "&until=2023-02-13T12:22:01.526Z"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_user_account_string_value_with_lt_operator(self):
        stix_pattern = "[user-account:display_name < 'Okta System']"
        query = translation.translate('okta', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["filter=actor.displayName lt \"Okta System\" &since=2023-02-13T12:21:07.168Z"
                   "&until=2023-02-13T12:26:07.168Z"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_x_oca_event_string_value_with_ge_operator(self):
        stix_pattern = "[x-oca-event:x_legacy_event_type >= 'app.oauth2.authorize.code']"
        query = translation.translate('okta', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["filter=legacyEventType ge \"app.oauth2.authorize.code\" &since=2023-02-07T05:01:26.225Z"
                   "&until=2023-02-07T05:06:26.225Z"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_x_okta_authentication_context_query_in_operator(self):
        stix_pattern = "[x-okta-authentication-context:session_id IN " \
                       "('idxUPM3Tb1GQBe0MuFu_3OfRw','idxUPM3Tc1GQBe0MuFu_3OfRw')]"
        query = translation.translate('okta', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["filter=authenticationContext.externalSessionId eq \"idxUPM3Tb1GQBe0MuFu_3OfRw\" or "
                   "authenticationContext.externalSessionId eq \"idxUPM3Tc1GQBe0MuFu_3OfRw\" "
                   "&since=2023-02-07T04:56:53.455Z&until=2023-02-07T05:01:53.455Z"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_query_with_multiple_comparison_expressions_and_precedence_bracket(self):
        stix_pattern = "[(x-okta-target:target_id LIKE '00Tr22hj9U9LzFH0f5d6' OR " \
                       "x-okta-client:device != 'Computer') AND ipv4-addr:value = '1.1.1.1']"
        query = translation.translate('okta', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["filter=request.ipChain.ip eq \"1.1.1.1\" and (client.device ne \"Computer\" or"
                   " target.id co \"00Tr22hj9U9LzFH0f5d6\") "
                   "&since=2023-02-08T05:19:59.424Z&until=2023-02-08T05:24:59.424Z"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_query_with_multiple_comparison_expressions_joined_by_OR(self):
        stix_pattern = "[x-okta-target:target_id LIKE '0oa4oexp00i4BMrzJ5d7' OR " \
                       "x-okta-client:device != 'Computer']"
        query = translation.translate('okta', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["filter=client.device ne \"Computer\" or target.id co \"0oa4oexp00i4BMrzJ5d7\" "
                   "&since=2023-02-13T11:25:48.077Z&until=2023-02-13T11:30:48.077Z"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_query_for_morethan_two_comparison_expressions_joined_by_OR(self):
        stix_pattern = "[x-okta-client:device != 'Computer' OR x-okta-target:target_id LIKE'0oa4oexp00i4BMrzJ5d7' " \
                       "OR x-okta-client:geolocation_country = 'India']"
        query = translation.translate('okta', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["filter=client.geographicalContext.country eq \"India\" or (target.id co \"0oa4oexp00i4BMrzJ5d7\" "
                   "or client.device "
                   "ne \"Computer\") &since=2023-02-13T11:28:54.835Z&until=2023-02-13T11:33:54.835Z"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_observation_with_and_without_qualifier_query(self):
        stix_pattern = "[x-okta-target:target_id MATCHES '0oa4oexp00i4BMrzJ5d7'] START t'2022-12-19T11:00:00.000Z' " \
                       "STOP t'2023-01-31T11:00:00.003Z' AND [software:x_raw_user_agent " \
                       "LIKE 'Mozilla/5.0' OR x-okta-client:device != 'Computer']"
        query = translation.translate('okta', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["filter=target.id co \"0oa4oexp00i4BMrzJ5d7\" &since=2022-12-19T11:00:00.000Z"
                   "&until=2023-01-31T11:00:00.003Z",
                   "filter=client.device ne \"Computer\" or client.userAgent.rawUserAgent co \"Mozilla/5.0\" "
                   "&since=2023-02-13T12:06:27.334Z&until=2023-02-13T12:11:27.334Z"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_combined_observation_OR(self):
        stix_pattern = "[x-okta-target:target_id LIKE '0oa4oexp00i4BMrzJ5d7' OR " \
                       "x-okta-client:device != 'Computer']START t'2022-10-15T11:20:35.000Z' " \
                       "STOP t'2023-01-10T11:00:00.003Z' OR [x-oca-event:action = 'app.oauth2.authorize.code']" \
                       "START t'2022-12-15T11:20:35.000Z' STOP t'2023-01-31T11:00:00.003Z'"
        query = translation.translate('okta', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["filter=client.device ne \"Computer\" or target.id co \"0oa4oexp00i4BMrzJ5d7\" "
                   "&since=2022-10-15T11:20:35.000Z&until=2023-01-10T11:00:00.003Z",
                   "filter=eventType eq \"app.oauth2.authorize.code\" "
                   "&since=2022-12-15T11:20:35.000Z&until=2023-01-31T11:00:00.003Z"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_query_for_multiple_observation(self):
        stix_pattern = "[x-okta-target:target_id MATCHES '0oa4oexp00i4BMrzJ5d7' OR " \
                       "x-okta-client:device != 'Computer']AND[x-oca-event:outcome NOT IN ('SUCCESS','FAILURE') " \
                       "AND x-oca-event:x_legacy_event_type >= 'app.oauth2.authorize.code'] " \
                       "AND [x-oca-event:action = 'app.oauth2.authorize.code']START t'2022-12-15T11:20:35.000Z' " \
                       "STOP t'2023-01-31T11:00:00.003Z'"
        query = translation.translate('okta', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["filter=(client.device ne \"Computer\" or target.id co \"0oa4oexp00i4BMrzJ5d7\") or "
                   "(legacyEventType ge \"app.oauth2.authorize.code\" and not(outcome.result eq \"SUCCESS\" and "
                   "outcome.result eq \"FAILURE\")) &since=2023-02-13T11:54:29.295Z&until=2023-02-13T11:59:29.295Z",
                   "filter=eventType eq \"app.oauth2.authorize.code\" &since=2022-12-15T11:20:35.000Z"
                   "&until=2023-01-31T11:00:00.003Z"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_query_for_multiple_observation_with_brackets(self):
        stix_pattern = "([x-okta-target:target_id MATCHES '0oa4oexp00i4BMrzJ5d7' OR " \
                       "x-okta-client:device != 'Computer'] AND [x-oca-event:outcome NOT IN ('SUCCESS','FAILURE') " \
                       "AND x-oca-event:x_legacy_event_type >= 'app.oauth2.authorize.code']) " \
                       "START t'2022-10-15T11:20:35.000Z' STOP t'2023-02-03T11:00:00.003Z'" \
                       "AND [x-oca-event:action = 'app.oauth2.authorize.code']START t'2022-12-15T11:20:35.000Z' " \
                       "STOP t'2023-01-31T11:00:00.003Z'"
        query = translation.translate('okta', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["filter=(client.device ne \"Computer\" or target.id co \"0oa4oexp00i4BMrzJ5d7\") "
                   "or (legacyEventType ge \"app.oauth2.authorize.code\" and not(outcome.result eq \"SUCCESS\" "
                   "and outcome.result eq \"FAILURE\")) &since=2022-10-15T11:20:35.000Z&until=2023-02-03T11:00:00.003Z",
                   "filter=eventType eq \"app.oauth2.authorize.code\" &since=2022-12-15T11:20:35.000Z"
                   "&until=2023-01-31T11:00:00.003Z"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_x_oca_event_enum_value_with_IN_operator(self):
        stix_pattern = "[x-oca-event:outcome IN ('SUCCESS','failure')]"
        query = translation.translate('okta', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["filter=outcome.result eq \"SUCCESS\" or outcome.result eq \"FAILURE\" "
                   "&since=2023-02-07T04:40:37.789Z&until=2023-02-07T04:45:37.789Z"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_x_oca_event_enum_value_with_NOT_IN_operator(self):
        stix_pattern = "[x-oca-event:outcome NOT IN ('SuccESS','FAILURE')]"
        query = translation.translate('okta', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["filter=not(outcome.result eq \"SUCCESS\" and outcome.result eq \"FAILURE\") "
                   "&since=2023-02-07T04:42:14.523Z&until=2023-02-07T04:47:14.523Z"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_incorrect_enum_value_with_equal_operator(self):
        stix_pattern = "[x-oca-event:outcome = 'OUTCOME']"
        query = translation.translate('okta', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["filter=outcome.result eq \"OUTCOME\" &since=2023-02-07T04:43:40.749Z&"
                   "until=2023-02-07T04:48:40.749Z"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_wildcard_characters_like_operator(self):
        stix_pattern = "[domain-name:value LIKE '%amazonaws.com']"
        query = translation.translate('okta', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["filter=securityContext.domain co \"amazonaws.com\" &since=2023-02-07T04:45:09.392Z"
                   "&until=2023-02-07T04:50:09.392Z"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_invalid_qualifier_with_future_timestamp(self):
        stix_pattern = "[domain-name:value LIKE 'amazonaws.com'] " \
                       "START t'2023-01-19T11:00:00.000Z' STOP t'2024-02-07T11:00:00.003Z'"
        result = translation.translate('okta', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert "translation_error" == result['code']
        assert 'Start/Stop time should not be in the future UTC timestamp' in result['error']

    def test_invalid_operator_for_integer_type_field(self):
        stix_pattern = "[autonomous-system:number LIKE '50']"
        result = translation.translate('okta', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert "not_implemented" == result['code']
        assert 'LIKE/MATCHES operator is not supported for int type' in result['error']

    def test_string_value_for_int_type_field(self):
        stix_pattern = "[autonomous-system:number = 'amazonaws.com']"
        result = translation.translate('okta', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert "not_implemented" == result['code']
        assert 'wrong parameter' in result['error']

    def test_x_oca_event_enum_value_with_MATCHES_operator(self):
        stix_pattern = "[x-oca-event:outcome MATCHES 'SUCCESS']"
        result = translation.translate('okta', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert "not_implemented" == result['code']
        assert 'LIKE/MATCHES operator is not supported for enum type input' in result['error']

    def test_invalid_operator_for_request_uri(self):
        stix_pattern = "[x-okta-debug-context:request_uri LIKE 'cort/ferg']"
        result = translation.translate('okta', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert "not_implemented" == result['code']
        assert 'LIKE/MATCHES operator is not supported' in result['error']
