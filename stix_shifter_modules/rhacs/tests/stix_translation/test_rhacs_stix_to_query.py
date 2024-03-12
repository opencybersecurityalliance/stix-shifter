import re
import unittest
from stix_shifter.stix_translation import stix_translation
from stix_shifter_utils.utils.error_response import ErrorCode

translation = stix_translation.StixTranslation()


def _remove_timestamp_from_query(queries):
    """ removes timestamp from query """
    pattern = r'\+Violation\s*Time:>=\d{2}/\d{2}/\d{4}'
    if isinstance(queries, list):
        val = [re.sub(pattern, '', str(query)) for query in queries]
    elif isinstance(queries, str):
        val = re.sub(pattern, '', queries)
    return val


def _multiple_observation_query(queries):
    """ for removing timestamp from multiple observation query"""
    query_list = []
    if len(queries) > 1:
        for query in queries:
            string_1 = _remove_timestamp_from_query(query)
            query_list.append(string_1)
    return query_list


class TestQueryTranslator(unittest.TestCase):
    """
    class to perform unit test case for rhacs translate query
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

    def test_low_severity_query(self):
        """ test to check x-ibm-finding low severity query """
        stix_pattern = "[x-ibm-finding:severity = 2]"
        query = translation.translate('rhacs', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['Severity:"LOW_SEVERITY"+Violation Time:>=06/30/2021']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_medium_severity_query(self):
        """ test to check x-ibm-finding medium severity query """
        stix_pattern = "[x-ibm-finding:severity = 40]"
        query = translation.translate('rhacs', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['Severity:"MEDIUM_SEVERITY"+Violation Time:>=06/30/2021']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_high_severity_query(self):
        """ test to check x-ibm-finding high severity query """
        stix_pattern = "[x-ibm-finding:severity = 70]"
        query = translation.translate('rhacs', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['Severity:"HIGH_SEVERITY"+Violation Time:>=06/30/2021']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_critical_severity_query(self):
        """ test to check x-ibm-finding critical severity query """
        stix_pattern = "[x-ibm-finding:severity = 90]"
        query = translation.translate('rhacs', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['Severity:"CRITICAL_SEVERITY"+Violation Time:>=06/30/2021']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_cluster_name_traffic_query(self):
        """ test to check x-rhacs-cluster stix pattern with equal operator to native data source query """
        stix_pattern = "[x-rhacs-cluster:name = 'cp4s-cluster']"
        query = translation.translate('rhacs', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['Cluster:"cp4s-cluster"+Violation Time:>=06/30/2022']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_like_operator_query(self):
        """ test to check like operator stix pattern to native data source query """
        stix_pattern = "[x-rhacs-cluster:name LIKE 'cp4s']"
        query = translation.translate('rhacs', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['Cluster:r/cp4s.*+Violation Time:>=06/30/2022']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_match_operator_query(self):
        """ test to check MATCHES operator stix pattern to native data source query """
        stix_pattern = "[x-rhacs-cluster:name MATCHES 'cp4.*']"
        query = translation.translate('rhacs', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['Cluster:r/cp4.*+Violation Time:>=06/30/2022']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_not_equal_operator(self):
        """ test to check not equal operator stix pattern to native data source query """
        stix_pattern = "[x-rhacs-cluster:name != 'cp4s-cluster']"
        query = translation.translate('rhacs', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['Cluster:!"cp4s-cluster"+Violation Time:>=06/30/2022']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_observation_query(self):
        """ test to check multiple observation stix pattern to native data source query """
        stix_pattern = "[x-rhacs-cluster:name = 'cp4s-cluster'] " \
                       "AND [x-rhacs-cluster:name = 'rhacs-cluster']"
        query = translation.translate('rhacs', 'query', '{}', stix_pattern)
        if len(query['queries']) > 1:
            query['queries'] = _multiple_observation_query(query['queries'])
        queries = ['Cluster:"cp4s-cluster"+Violation Time:>=08/26/2022',
                   'Cluster:"rhacs-cluster"+Violation Time:>=08/26/2022']
        queries = _multiple_observation_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_comparison_query(self):
        """ test to check multiple comparison stix pattern to native data source query """
        stix_pattern = "[x-ibm-finding:name = 'Unauthorized Network' AND " \
                       "x-ibm-finding:extensions.'x-rhacs-finding'.violation_state = 'RESOLVED']"
        query = translation.translate('rhacs', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['Violation State:"RESOLVED"+Policy:"Unauthorized Network"'
                   '+Violation Time:>=06/30/2022']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_cluster_id_query(self):
        """ test to check cluster id stix pattern to native data source query """
        stix_pattern = "[x-rhacs-cluster:id LIKE 'dbe']"
        query = translation.translate('rhacs', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['Cluster ID:r/dbe.*+Violation Time:>=06/30/2022']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_query_from_multiple_comparison_expressions_joined_by_and(self):
        """
        test to check multiple comparison expression with AND
        operator stix pattern to native data source query
        """
        stix_pattern = "[x-rhacs-cluster:namespace = 'cp4s' AND x-rhacs-deployment:name = 'app-manager'] " \
                       "START t'2022-06-22T08:43:10.003Z' STOP t'2022-06-23T10:43:10.005Z'"
        query = translation.translate('rhacs', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['Deployment:"app-manager"+Namespace:"cp4s"+Violation Time:>=06/22/2022']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_query_from_morethan_two_comparison_expressions_joined_by_and(self):
        """ test to check more than two comparison expressions joined by AND operator"""
        stix_pattern = "[x-rhacs-cluster:namespace = 'cp4s' AND x-rhacs-deployment:name = 'app-manager' " \
                       "AND x-rhacs-deployment:isactive = 'true']"
        query = translation.translate('rhacs', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['Inactive Deployment:True+Deployment:"app-manager"+Namespace:'
                   '"cp4s"+Violation Time:>=06/30/2022']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_negate_query(self):
        """ test to check negate query """
        stix_pattern = "[x-ibm-finding:name  NOT = '90-Day Image Age']"
        query = translation.translate('rhacs', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['Policy:!"90-Day Image Age"+Violation Time:>=06/30/2022']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_boolean_true_value_query(self):
        """ test to check boolean true query """
        stix_pattern = "[x-rhacs-deployment:isactive = 'true']"
        query = translation.translate('rhacs', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['Inactive Deployment:True+Violation Time:>=06/30/2022']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_boolean_false_value_query(self):
        """ test to check boolean false query """
        stix_pattern = "[x-rhacs-deployment:isactive = 'false']"
        query = translation.translate('rhacs', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['Inactive Deployment:False+Violation Time:>=06/30/2022']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_observation_with_qualifier_query(self):
        """ test to check multiple observation with qualifier query """
        stix_pattern = "[x-rhacs-cluster:namespace = 'cp4s' AND " \
                       "x-rhacs-deployment:name = 'app-manager' AND " \
                       "x-rhacs-deployment:isactive = 'true'] " \
                       "START t'2022-06-22T08:43:10.003Z' " \
                       "STOP t'2022-06-23T10:43:10.005Z' AND " \
                       "[x-ibm-finding:name  NOT = '90-Day Image Age']" \
                       "START t'2022-06-15T08:43:10.003Z' STOP t'2022-06-16T10:43:10.005Z'"
        query = translation.translate('rhacs', 'query', '{}', stix_pattern)
        if len(query['queries']) > 1:
            query['queries'] = _multiple_observation_query(query['queries'])
        queries = ['Inactive Deployment:True+Deployment:"app-manager"+Namespace:"cp4s"'
                   '+Violation Time:>=06/22/2022',
                   'Policy:!"90-Day Image Age"+Violation Time:>=06/15/2022']
        queries = _multiple_observation_query(queries)
        self._test_query_assertions(query, queries)

    def test_not_include_filter_query(self):
        """test to check not include filter query"""
        stix_pattern = "[x-rhacs-deployment:name != 'app-manager']"
        query = translation.translate('rhacs', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['Deployment:!"app-manager"+Violation Time:>=06/30/2022']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_negate_for_like_operator(self):
        """test to check negate for like query"""
        stix_pattern = "[x-rhacs-deployment:name NOT LIKE 'app']"
        query = translation.translate('rhacs', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['Deployment:!r/app.*+Violation Time:>=06/30/2022']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_unmapped_attribute_handling_with_and(self):
        """test to check unmapped attribute"""
        stix_pattern = "[url:value = 'http://www.testaddress.com' AND unmapped:attribute = 'something']"
        result = translation.translate('rhacs', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_MAPPING_ERROR.value == result['code']
        assert 'Unable to map the following STIX objects and properties' in result['error']

    def test_invalid_stix_pattern(self):
        """test to check invalid stix pattern"""
        stix_pattern = "[not_a_valid_pattern]"
        result = translation.translate('rhacs', 'query', '{}', stix_pattern, {'validate_pattern': 'true'})
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_STIX_VALIDATION.value == result['code']
        assert stix_pattern[1:-1] in result['error']

    def test_for_multiple_observation_with_or_operator(self):
        """test to check multiple observation with OR operator query"""
        stix_pattern = "[x-ibm-finding:extensions.'x-rhacs-finding'.categories[*] = 'Docker CIS'] " \
                       "START t'2022-06-22T08:43:10.003Z' STOP t'2022-06-23T10:43:10.005Z' " \
                       "OR [x-rhacs-deployment:name = 'app-manager'] " \
                       "START t'2022-06-15T08:43:10.003Z' STOP t'2022-06-16T10:43:10.005Z'"
        query = translation.translate('rhacs', 'query', '{}', stix_pattern)
        if len(query['queries']) > 1:
            query['queries'] = _multiple_observation_query(query['queries'])
        queries = ['Category:"Docker CIS"+Violation Time:>=06/22/2022',
                   'Deployment:"app-manager"+Violation Time:>=06/15/2022']
        queries = _multiple_observation_query(queries)
        self._test_query_assertions(query, queries)

    def test_invalid_boolean_value(self):
        """test to check invalid boolean pattern"""
        stix_pattern = "[x-rhacs-deployment:isactive = 2]"
        result = translation.translate('rhacs', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert 'wrong parameter : Invalid boolean type input' in result['error']

    def test_pattern_with_enum_fields_query(self):
        """test to check enum fields to query"""
        stix_pattern = "[x-ibm-finding:extensions.'x-rhacs-finding'.lifecycle_stage = 'runtime' " \
                       "AND x-ibm-finding:extensions.'x-rhacs-finding'.violation_state = 'ACTIVE']"
        query = translation.translate('rhacs', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['Violation State:"ACTIVE"+Lifecycle Stage:"RUNTIME"'
                   '+Violation Time:>=06/30/2022']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_enum_fields_query(self):
        """test to check multiple enum fields to query"""
        stix_pattern = "[x-ibm-finding:extensions.'x-rhacs-finding'.lifecycle_stage = 'runtime' " \
                       "AND x-ibm-finding:extensions.'x-rhacs-finding'.violation_state = 'ACTIVE' AND" \
                       " x-ibm-finding:extensions.'x-rhacs-finding'.resource_type = 'DEPLOYMENT']"
        query = translation.translate('rhacs', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['Resource Type:"DEPLOYMENT"+Violation State:"ACTIVE"+Lifecycle Stage:"RUNTIME"'
                   '+Violation Time:>=06/30/2022']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_violation_query(self):
        """ test to check x-ibm-finding time_observed pattern to native data source query """
        stix_pattern = "[x-ibm-finding:time_observed = t'2022-07-04T00:00:00.030Z']"
        query = translation.translate('rhacs', 'query', '{}', stix_pattern)
        queries = ['Violation Time:07/04/2022']
        self._test_query_assertions(query, queries)

    def test_violation_multiple_comparison_query(self):
        """ test to check violation time multiple comparison to native data source query """
        stix_pattern = "[x-ibm-finding:time_observed = t'2022-07-04T00:00:00.030Z' AND " \
                       "x-ibm-finding:extensions.'x-rhacs-finding'.lifecycle_stage = 'runtime']"
        query = translation.translate('rhacs', 'query', '{}', stix_pattern)
        queries = ['Lifecycle Stage:"RUNTIME"+Violation Time:07/04/2022']
        self._test_query_assertions(query, queries)

    def test_violation_multiple_observation_query(self):
        """ test to check violation time multiple observation to native data source query """
        stix_pattern = "[x-ibm-finding:time_observed = t'2022-07-04T00:00:00.030Z'] " \
                       "START t'2022-06-26T08:43:10.003Z' STOP t'2022-06-27T10:43:10.005Z' " \
                       "AND [x-ibm-finding:extensions.'x-rhacs-finding'.lifecycle_stage = 'runtime'] " \
                       "START t'2022-06-15T08:43:10.003Z' STOP t'2022-06-16T10:43:10.005Z'"
        query = translation.translate('rhacs', 'query', '{}', stix_pattern)
        if len(query['queries']) > 1:
            query['queries'] = _multiple_observation_query(query['queries'])
        queries = ['Violation Time:07/04/2022', 'Lifecycle Stage:"RUNTIME"+Violation Time:>=06/15/2022']
        queries = _multiple_observation_query(queries)
        self._test_query_assertions(query, queries)

    def test_invalid_enum_fields_query(self):
        """test to check invalid  enum field value """
        stix_pattern = "[x-ibm-finding:extensions.'x-rhacs-finding'.lifecycle_stage = 'abc']"
        result = translation.translate('rhacs', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert result['error'] == "rhacs connector error => wrong parameter : " \
                                  "Unsupported ENUM values provided. " \
                                  "Possible supported enum values are['RUNTIME', 'DEPLOY']"

    def test_invalid_enum_fields_with_multiple_element(self):
        """test to check invalid  enum fields value with multiple element"""
        stix_pattern = "[x-ibm-finding:extensions.'x-rhacs-finding'.lifecycle_stage = 'xyz' " \
                       "AND x-ibm-finding:extensions.'x-rhacs-finding'.violation_state = 'abc' " \
                       "AND x-ibm-finding:extensions.'x-rhacs-finding'.resource_type = 'def']"
        result = translation.translate('rhacs', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert result['error'] == "rhacs connector error => wrong parameter : " \
                                  "Unsupported ENUM values provided. " \
                                  "Possible supported enum values are['DEPLOYMENT']"

    def test_invalid_operator_string_field(self):
        """test to check invalid operator with string field"""
        stix_pattern = "[x-rhacs-cluster:namespace > 'abc']"
        result = translation.translate('rhacs', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert result['error'] == 'rhacs connector error => wrong parameter ' \
                                  ': :> operator is not supported for string type input'

    def test_invalid_operator_enum_field(self):
        """test to check invalid operator with enum field"""
        stix_pattern = "[x-ibm-finding:extensions.'x-rhacs-finding'.lifecycle_stage > 'runtime']"
        result = translation.translate('rhacs', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert result['error'] == 'rhacs connector error => wrong parameter ' \
                                  ': :> operator is not supported for enum type input'

    def test_like_operator_with_enum_field(self):
        """test to check like operator with enum field"""
        stix_pattern = "[x-ibm-finding:extensions.'x-rhacs-finding'.lifecycle_stage LIKE 'runtime']"
        result = translation.translate('rhacs', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert result['error'] == 'rhacs connector error => wrong parameter : LIKE operator ' \
                                  'is supported only for string type input'

    def test_matches_operator_with_enum_field(self):
        """test to check matches operator with enum field"""
        stix_pattern = "[x-ibm-finding:extensions.'x-rhacs-finding'.lifecycle_stage MATCHES 'run.*']"
        result = translation.translate('rhacs', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert result['error'] == 'rhacs connector error => wrong parameter : ' \
                                  'MATCHES operators is supported only for string type input'

    def test_query_from_morethan_two_comparison_expressions_joined_by_or(self):
        """ test to check more than two comparison expressions joined by OR operator"""
        stix_pattern = "[x-rhacs-cluster:namespace = 'cp4s' OR x-rhacs-deployment:name = 'app-manager' " \
                       "AND x-rhacs-deployment:isactive = 'true']"
        result = translation.translate('rhacs', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert result['error'] == 'rhacs connector error => wrong parameter ' \
                                  ': comparison expression OR operator is not supported in rhacs'

    def test_out_of_bound_severity_query(self):
        """ test to check out of bound severity value"""
        stix_pattern = "[x-ibm-finding:severity = 102]"
        result = translation.translate('rhacs', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert result['error'] == 'rhacs connector error => wrong parameter : ' \
                                  'only 1-100 integer values are supported with this field'

    def test_invalid_operator_severity_query(self):
        """test to check invalid operator on severity field"""
        stix_pattern = "[x-ibm-finding:severity >= 102]"
        result = translation.translate('rhacs', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert result['error'] == 'rhacs connector error => ' \
                                  'wrong parameter : :>= comparator is not supported with this field'

    def test_invalid_start_stop_pattern(self):
        """test to check check invalid start stop pattern"""
        stix_pattern = "[x-ibm-finding:extensions.'x-rhacs-finding'.lifecycle_stage = 'runtime'] " \
                       "START t'2022-06-17T08:43:10.003Z' STOP t'2022-06-16T10:43:10.005Z'"
        result = translation.translate('rhacs', 'query', '{}', stix_pattern)
        print(result)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_MODULE_DEFAULT_ERROR.value == result['code']
        assert result['error'] == 'rhacs connector error => STIX translation error: Start time should be lesser than Stop time'
