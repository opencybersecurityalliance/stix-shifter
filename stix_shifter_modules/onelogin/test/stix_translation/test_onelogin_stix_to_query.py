import unittest

from stix_shifter.stix_translation import stix_translation

translation = stix_translation.StixTranslation()


def _test_query_assertions(query, queries):
    assert query['queries'] == [queries]


class TestStixToQuery(unittest.TestCase, object):

    def test_ipv4_query(self):
        stix_pattern = "[ipv4-addr:value = '192.168.122.83' AND user-account:user_id = '12345678']"
        query = translation.translate('onelogin', 'query', 'onelogin', stix_pattern, options={"result_limit": 100})
        queries = 'user_id=12345678&ipaddr=192.168.122.83&limit=100'
        _test_query_assertions(query, queries)

    def test_user_id_query(self):
        stix_pattern = "[user-account:user_id = '12345678'] START t'2021-01-28T12:24:01.009Z' STOP t'2021-07-25T12:54:01.009Z'"
        query = translation.translate('onelogin', 'query', 'onelogin', stix_pattern)
        queries = 'user_id=12345678&since=2021-01-28T12:24:01.009Z&until=2021-07-25T12:54:01.009Z&limit=1000'
        _test_query_assertions(query, queries)

    def test_account_id_query(self):
        stix_pattern = "[user-account:x_account_id = '12345678']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'account_id=12345678&limit=1000'
        _test_query_assertions(query, queries)

    def test_actor_user_id_query(self):
        stix_pattern = "[user-account:x_actor_user_id = '12345678']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'actor_user_id=12345678&limit=1000'
        _test_query_assertions(query, queries)

    def test_assuming_acting_user_id_query(self):
        stix_pattern = "[user-account:x_assuming_acting_user_id = '12345678']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'assuming_acting_user_id=12345678&limit=1000'
        _test_query_assertions(query, queries)

    def test_actor_user_name_query(self):
        stix_pattern = "[user-account:x_actor_user_name = 'Jon']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'actor_user_name=Jon&limit=1000'
        _test_query_assertions(query, queries)

    def test_display_name_query(self):
        stix_pattern = "[user-account:display_name = 'Jon']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'user_name=Jon&limit=1000'
        _test_query_assertions(query, queries)

    def test_client_id_query(self):
        stix_pattern = "[x-onelogin-finding:client_id = '12345678']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'client_id=12345678&limit=1000'
        _test_query_assertions(query, queries)

    def test_directory_id_query(self):
        stix_pattern = "[x-onelogin-finding:directory_id = '12345678']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'directory_id=12345678&limit=1000'
        _test_query_assertions(query, queries)

    def test_event_type_id_query(self):
        stix_pattern = "[x-onelogin-finding:event_type_id = '12345678']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'event_type_id=12345678&limit=1000'
        _test_query_assertions(query, queries)

    def test_id_query(self):
        stix_pattern = "[x-onelogin-finding:unique_id = '12345678']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'id=12345678&limit=1000'
        _test_query_assertions(query, queries)

    def test_resolution_query(self):
        stix_pattern = "[x-onelogin-finding:resolution = '12345678']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'resolution=12345678&limit=1000'
        _test_query_assertions(query, queries)

    def test_since_query(self):
        stix_pattern = "[x-ibm-finding:start = '2021-06-22T13:12:06.437Z']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'since=2021-06-22T13:12:06.437Z&limit=1000'
        _test_query_assertions(query, queries)

    def test_until_query(self):
        stix_pattern = "[x-ibm-finding:end = '2021-06-22T13:12:06.437Z']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'until=2021-06-22T13:12:06.437Z&limit=1000'
        _test_query_assertions(query, queries)

    def test_proxy_ip_query(self):
        stix_pattern = "[x-onelogin-finding:proxy_ip = '127.0.0.1']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'proxy_ip=127.0.0.1&limit=1000'
        _test_query_assertions(query, queries)

    def test_policy_id_query(self):
        stix_pattern = "[x-ibm-finding:policy_id = '12345678']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'policy_id=12345678&limit=1000'
        _test_query_assertions(query, queries)

    def test_policy_name_query(self):
        stix_pattern = "[x-ibm-finding:name = 'Default']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'policy_name=Default&limit=1000'
        _test_query_assertions(query, queries)

    def test_role_id_query(self):
        stix_pattern = "[x-onelogin-finding:role_id = '123']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'role_id=123&limit=1000'
        _test_query_assertions(query, queries)

    def test_app_id_query(self):
        stix_pattern = "[x-onelogin-finding:app_id = '1234']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'app_id=1234&limit=1000'
        _test_query_assertions(query, queries)

    def test_group_id_query(self):
        stix_pattern = "[x-onelogin-finding:group_id = '1234']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'group_id=1234&limit=1000'
        _test_query_assertions(query, queries)

    def test_otp_device_id_query(self):
        stix_pattern = "[x-onelogin-finding:otp_device_id = '1234']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'otp_device_id=1234&limit=1000'
        _test_query_assertions(query, queries)

    def test_actor_system_query(self):
        stix_pattern = "[x-onelogin-finding:actor_system = 'Default']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'actor_system=Default&limit=1000'
        _test_query_assertions(query, queries)

    def test_custom_message_query(self):
        stix_pattern = "[x-onelogin-finding:custom_message = 'Default']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'custom_message=Default&limit=1000'
        _test_query_assertions(query, queries)

    def test_role_name_query(self):
        stix_pattern = "[x-onelogin-finding:role_name = 'Default']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'role_name=Default&limit=1000'
        _test_query_assertions(query, queries)

    def test_app_name_query(self):
        stix_pattern = "[x-onelogin-finding:app_name = 'Default']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'app_name=Default&limit=1000'
        _test_query_assertions(query, queries)

    def test_group_name_query(self):
        stix_pattern = "[x-onelogin-finding:group_name = 'Default']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'group_name=Default&limit=1000'
        _test_query_assertions(query, queries)

    def test_otp_device_name_query(self):
        stix_pattern = "[x-onelogin-finding:otp_device_name = 'Default']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'otp_device_name=Default&limit=1000'
        _test_query_assertions(query, queries)

    def test_operation_name_query(self):
        stix_pattern = "[x-onelogin-finding:operation_name = 'Default']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'operation_name=Default&limit=1000'
        _test_query_assertions(query, queries)

    def test_directory_sync_run_id_query(self):
        stix_pattern = "[x-onelogin-finding:directory_sync_run_id = '1234']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'directory_sync_run_id=1234&limit=1000'
        _test_query_assertions(query, queries)

    def test_resource_type_id_query(self):
        stix_pattern = "[x-onelogin-finding:resource_type_id = '1234']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'resource_type_id=1234&limit=1000'
        _test_query_assertions(query, queries)

    def test_browser_fingerprint_query(self):
        stix_pattern = "[x-onelogin-finding:browser_fingerprint = 'True']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'browser_fingerprint=True&limit=1000'
        _test_query_assertions(query, queries)

    def test_notes_query(self):
        stix_pattern = "[x-onelogin-finding:notes = '1234']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'notes=1234&limit=1000'
        _test_query_assertions(query, queries)

    def test_created_at_query(self):
        stix_pattern = "[x-ibm-finding:time_observed = '2021-06-22T13:12:06.437Z']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'created_at=2021-06-22T13:12:06.437Z&limit=1000'
        _test_query_assertions(query, queries)

    def test_risk_score_query(self):
        stix_pattern = "[x-onelogin-risk:risk_score = '2']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'risk_score=2&limit=1000'
        _test_query_assertions(query, queries)

    def test_risk_reasons_query(self):
        stix_pattern = "[x-onelogin-risk:risk_reasons = 'Default']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'risk_reasons=Default&limit=1000'
        _test_query_assertions(query, queries)

    def test_risk_cookie_id_query(self):
        stix_pattern = "[x-onelogin-risk:risk_cookie_id = '5']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'risk_cookie_id=5&limit=1000'
        _test_query_assertions(query, queries)

    def test_error_description_query(self):
        stix_pattern = "[x-onelogin-risk:error_description = 'Default']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'error_description=Default&limit=1000'
        _test_query_assertions(query, queries)

    def test_query_from_multiple_observation_expressions_joined_by_AND(self):
        stix_pattern = "[ipv4-addr:value='127.0.0.1'] AND [user-account:user_id = '12345678']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = ['ipaddr=127.0.0.1&limit=1000', 'user_id=12345678&limit=1000']
        assert query['queries'] == queries
