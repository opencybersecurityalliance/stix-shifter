import unittest

from stix_shifter.stix_translation import stix_translation

translation = stix_translation.StixTranslation()


def _test_query_assertions(query, queries):
    assert query['queries'] == [queries]


class TestStixToQuery(unittest.TestCase, object):

    def test_ipv4_query(self):
        stix_pattern = "[ipv4-addr:value = '192.168.122.83' OR ipv4-addr:value = '192.168.122.84']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'ipaddr=192.168.122.84&ipaddr=192.168.122.83&limit=50'
        _test_query_assertions(query, queries)

    def test_user_id_query(self):
        stix_pattern = "[user-account:user_id = '12345678']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'user_id=12345678&limit=50'
        _test_query_assertions(query, queries)

    def test_account_id_query(self):
        stix_pattern = "[user-account:account_id = '12345678']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'account_id=12345678&limit=50'
        _test_query_assertions(query, queries)

    def test_actor_user_id_query(self):
        stix_pattern = "[user-account:actor_user_id = '12345678']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'actor_user_id=12345678&limit=50'
        _test_query_assertions(query, queries)

    def test_assuming_acting_user_id_query(self):
        stix_pattern = "[user-account:assuming_acting_user_id = '12345678']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'assuming_acting_user_id=12345678&limit=50'
        _test_query_assertions(query, queries)

    def test_actor_user_name_query(self):
        stix_pattern = "[user-account:actor_user_name = 'Jon']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'actor_user_name=Jon&limit=50'
        _test_query_assertions(query, queries)

    def test_display_name_query(self):
        stix_pattern = "[user-account:display_name = 'Jon']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'user_name=Jon&limit=50'
        _test_query_assertions(query, queries)

    def test_client_id_query(self):
        stix_pattern = "[x-onelogin:client_id = '12345678']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'client_id=12345678&limit=50'
        _test_query_assertions(query, queries)

    def test_directory_id_query(self):
        stix_pattern = "[x-onelogin:directory_id = '12345678']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'directory_id=12345678&limit=50'
        _test_query_assertions(query, queries)

    def test_event_type_id_query(self):
        stix_pattern = "[x-onelogin:event_type_id = '12345678']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'event_type_id=12345678&limit=50'
        _test_query_assertions(query, queries)

    def test_id_query(self):
        stix_pattern = "[x-onelogin:id = '12345678']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'id=12345678&limit=50'
        _test_query_assertions(query, queries)

    def test_resolution_query(self):
        stix_pattern = "[x-onelogin:resolution = '12345678']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'resolution=12345678&limit=50'
        _test_query_assertions(query, queries)

    def test_since_query(self):
        stix_pattern = "[x-onelogin:since = '2021-06-22T13:12:06.437Z']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'since=2021-06-22T13:12:06.437Z&limit=50'
        _test_query_assertions(query, queries)

    def test_until_query(self):
        stix_pattern = "[x-onelogin:until = '2021-06-22T13:12:06.437Z']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'until=2021-06-22T13:12:06.437Z&limit=50'
        _test_query_assertions(query, queries)

    def test_proxy_ip_query(self):
        stix_pattern = "[x-onelogin:proxy_ip = '127.0.0.1']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'proxy_ip=127.0.0.1&limit=50'
        _test_query_assertions(query, queries)

    def test_policy_id_query(self):
        stix_pattern = "[x-onelogin:policy_id = '12345678']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'policy_id=12345678&limit=50'
        _test_query_assertions(query, queries)

    def test_policy_name_query(self):
        stix_pattern = "[x-onelogin:policy_name = 'Default']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'policy_name=Default&limit=50'
        _test_query_assertions(query, queries)

    def test_risk_score_query(self):
        stix_pattern = "[x-onelogin-risk:risk_score = 'Default']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'risk_score=Default&limit=50'
        _test_query_assertions(query, queries)

    def test_risk_reasons_query(self):
        stix_pattern = "[x-onelogin-risk:risk_reasons = 'Default']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'risk_reasons=Default&limit=50'
        _test_query_assertions(query, queries)

    def test_risk_cookie_id_query(self):
        stix_pattern = "[x-onelogin-risk:risk_cookie_id = 'Default']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'risk_cookie_id=Default&limit=50'
        _test_query_assertions(query, queries)

    def test_error_description_query(self):
        stix_pattern = "[x-onelogin-risk:error_description = 'Default']"
        query = translation.translate('onelogin', 'query', '{}', stix_pattern)
        queries = 'error_description=Default&limit=50'
        _test_query_assertions(query, queries)
