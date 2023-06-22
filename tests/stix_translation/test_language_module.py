from stix_shifter.stix_translation import stix_translation

translation = stix_translation.StixTranslation()

AQL_QUERY = 'blablabl'
SQL_QUERY = "[ipv4-addr:value = '192.168.0.100']"


class TestStartParameters(object):

    def validate_aql_result(self, result):
        assert 'queries' in result
        assert len(result['queries']) == 1
        assert result['queries'][0] == AQL_QUERY

    def validate_stix_result(self, result, length):
        assert 'queries' in result
        assert len(result['queries']) == length

    def validate_error_result(self, result):
        print(str(result))
        assert 'queries' not in result

    def test_aql_options_language_aql(self):
        # python main.py translate qradar query '' "bla-bla-aql" '{"language":"aql"}'
        result = translation.translate('qradar', 'query', '', AQL_QUERY, {'language': 'aql'})
        self.validate_aql_result(result)

    def test_aql_module_aql(self):
        # python main.py translate qradar:aql query '' "bla-bla-aql" '{}'
        result = translation.translate('qradar:aql', 'query', '', AQL_QUERY, {})
        self.validate_aql_result(result)

    # def test_aql_module_options_dialect_aql(self):
    #     # python main.py translate qradar query '' "bla-bla-aql" '{"dialects": ["aql"]}'
    #     result = translation.translate('qradar', 'query', '', AQL_QUERY, {"dialects": ["aql"]})
    #     self.validate_aql_result(result)

    # def test_aql_module_options_language_aql_dialect_aql(self):
    #     # python main.py translate qradar query '' "bla-bla-aql" '{"language":"aql", "dialects": ["aql"]}'
    #     result = translation.translate('qradar', 'query', '', AQL_QUERY, {"language": "aql", "dialects": ["aql"]})
    #     self.validate_aql_result(result)

    def test_stix_2_results(self):
        # python main.py translate qradar query '' "[ipv4-addr:value = '192.168.0.100']" '{}'
        result = translation.translate('qradar', 'query', '', SQL_QUERY, {})
        self.validate_stix_result(result, 2)

    def test_stix_1_result_options(self):
        # python main.py translate qradar query '' "[ipv4-addr:value = '192.168.0.100']" '{"dialects": ["events"]}'
        result = translation.translate('qradar', 'query', '', SQL_QUERY, {"dialects": ["events"]})
        self.validate_stix_result(result, 1)

    def test_stix_1_result_module(self):
        # python main.py translate qradar:events query '' "[ipv4-addr:value = '192.168.0.100']" '{}'
        result = translation.translate('qradar:events', 'query', '', SQL_QUERY, {})
        print(str(result))
        self.validate_stix_result(result, 1)

    def test_error_language_stix_dialects_aql(self):
        # python main.py translate qradar query '' "bla-bla-aql" '{"language": "stix", "dialects": ["aql"]}'
        result = translation.translate('qradar', 'query', '', AQL_QUERY, {"language": "stix", "dialects": ["aql"]})
        self.validate_error_result(result)

    def test_error_wrong_language_stix(self):
        # python main.py translate qradar:events query '' "bla-bla-aql" '{"language": "stix", "dialects": ["aql"]}'
        result = translation.translate('qradar:events', 'query', '', AQL_QUERY, {"language": "stix", "dialects": ["aql"]})
        self.validate_error_result(result)

    def test_error_wrong_language_aql(self):
        # python main.py translate qradar query '' "bla-bla-aql" '{"language":"aql", "dialects": ["events"]}'
        result = translation.translate('qradar', 'query', '', AQL_QUERY, {"language": "aql", "dialects": ["events"]})
        self.validate_error_result(result)
    