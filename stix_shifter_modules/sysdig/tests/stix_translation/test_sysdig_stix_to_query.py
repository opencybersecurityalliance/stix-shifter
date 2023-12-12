import re
import unittest
from stix_shifter.stix_translation import stix_translation

translation = stix_translation.StixTranslation()


def _remove_timestamp_from_query(queries):
    """ removes timestamp from query """
    pattern = r'[\^from\&to=\d]{47}'
    if isinstance(queries, list):
        return [re.sub(pattern, '', str(query)) for query in queries]
    elif isinstance(queries, str):
        return re.sub(pattern, '', queries)


class TestQueryTranslator(unittest.TestCase):
    """
    class to perform unit test case for sysdig translate query
    """
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

    def test_mac_addr_IN_operator(self):
        stix_pattern = "[mac-addr:value IN('00:aa:dd:99:77:00','00:77:66:99:11:dd')] START " \
                       "t'2023-08-01T00:00:00.00Z'STOP t'2023-08-14T10:00:00.00Z'"
        query = translation.translate('sysdig', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["from=1690848000000000000&to=1692007200000000000&filter=(machineId in "
                   "(\"00:aa:dd:99:77:00\",\"00:77:66:99:11:dd\"))andsource!=\"auditTrail\""]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_mac_addr_not_equal_operator(self):
        stix_pattern = "[mac-addr:value!='00:aa:dd:99:77:00'] START " \
                       "t'2023-08-01T00:00:00.00Z'STOP t'2023-08-14T10:00:00.00Z'"
        query = translation.translate('sysdig', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["from=1690848000000000000&to=1692007200000000000&filter=(machineId!="
                   "\"00:aa:dd:99:77:00\")andsource!=\"auditTrail\""]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_x_oca_asset_query(self):
        stix_pattern = "[x-oca-asset:extensions.'x-oca-container-ext'.x_repo != 'opencontent-etcd-operator']"
        query = translation.translate('sysdig', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["from=1695630479966000128&to=1695630779966000128&filter=(container."
                   "image.repo!=\"opencontent-etcd-operator\")andsource!=\"auditTrail\""]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_x_oca_asset_equal_operator(self):
        stix_pattern = "[x-oca-asset:extensions.'x-oca-container-ext'.x_repo = 'opencontent-etcd-operator']"
        query = translation.translate('sysdig', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["from=1695630479966000128&to=1695630779966000128&filter=(container."
                   "image.repo=\"opencontent-etcd-operator\")andsource!=\"auditTrail\""]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_x_cloud_provider(self):
        stix_pattern = "[x-cloud-provider:name='aws']"
        query = translation.translate('sysdig', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["from=1700445360000000000&to=1700791020003000064&filter=(cloudProvider.name=\"aws\")"
                   "andsource!=\"auditTrail\""]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_x_sysdig_policy_equal_operator(self):
        stix_pattern = "[x-sysdig-policy:policy_id = 11111111]"
        query = translation.translate('sysdig', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["from=1695901608584999936&to=1695901908584999936&filter=(policyId=11111111)"
                   "andsource!=\"auditTrail\""]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_x_sysdig_policy_not_equal_operator(self):
        stix_pattern = "[x-sysdig-policy:rule_name != 'Possible Backdoor using BPF']"
        query = translation.translate('sysdig', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["from=1695901830566000128&to=1695902130566000128&filter=(ruleName!=\"Possible "
                   "Backdoor using BPF\")andsource!=\"auditTrail\""]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_x_oca_asset_IN_operator(self):
        stix_pattern = "[x-oca-asset:extensions.'x-oca-container-ext'.x_repo IN('opencontent-etcd-operator')]"
        query = translation.translate('sysdig', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["from=1700133198447000064&to=1700133498447000064&filter=(container.image.repo in "
                   "(\"opencontent-etcd-operator\"))andsource!=\"auditTrail\""]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_x_ibm_finding_query(self):
        stix_pattern = "[x-ibm-finding:x_threat_source = 'syscall']"
        query = translation.translate('sysdig', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["from=1695631204718000128&to=1695631504718000128&filter=(source=\"syscall\")"
                   "andsource!=\"auditTrail\""]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_x_sysdig_deployment_query(self):
        stix_pattern = "[x-sysdig-deployment:name = 'ibm-cloud-provider-ip-111-11-11-111']"
        query = translation.translate('sysdig', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["from=1695632727713999872&to=1695633027713999872&filter=(kubernetes.deployment."
                   "name=\"ibm-cloud-provider-ip-111-11-11-111\")andsource!=\"auditTrail\""]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_x_sysdig_deployment_not_equal_operator(self):
        stix_pattern = "[x-sysdig-deployment:name != 'ibm-cloud-provider-ip-111-11-11-111']START " \
                       "t'2023-08-01T00:00:00.00Z'STOP t'2023-08-14T10:00:00.00Z'"
        query = translation.translate('sysdig', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["from=1697185737769999872&to=1697186037769999872&filter=(kubernetes.deployment."
                   "name!=\"ibm-cloud-provider-ip-111-11-11-111\")andsource!=\"auditTrail\""]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_x_ibm_finding_int_type_query(self):
        stix_pattern = "[x-ibm-finding:severity > 2]"
        query = translation.translate('sysdig', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["from=1695646240753999872&to=1695646540753999872&filter=(severity>2)andsource!=\"auditTrail\""]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_comparison(self):
        stix_pattern = "[x-sysdig-policy:policy_id = 77777777] AND [x-ibm-finding:severity != 2]"
        query = translation.translate('sysdig', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["from=1698317811217999872&to=1698318111217999872&filter=(policyId=77777777 or "
                   "severity!=2)andsource!=\"auditTrail\""]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_combined_comparison(self):
        stix_pattern = "[x-sysdig-policy:policy_id > 77777777 AND x-ibm-finding:severity <= 2]"
        query = translation.translate('sysdig', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["from=1698317511743000064&to=1698317811743000064&filter=(severity<=2andpolicyId>77777777)"
                   "andsource!=\"auditTrail\""]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_comparison_with_precedence_bracket(self):
        stix_pattern = "[(x-oca-asset:extensions.'x-oca-container-ext'.image_id='1a1a1a1a111a' " \
                       "AND x-sysdig-cluster:namespace != " \
                       "'openshift-cluster-node-tuning-operator' ) OR x-ibm-finding:x_category = 'runtime']" \
                       "START t'2023-09-01T08:43:10.003Z'STOP t'2023-09-10T10:43:10.005Z'"
        query = translation.translate('sysdig', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["from=1693557790003000064&to=1694342590004999936&filter=(category=\"runtime\"or"
                   "kubernetes.namespace.name!=\"openshift-cluster-node-tuning-operator\"andcontainer.image.id="
                   "\"1a1a1a1a111a\")andsource!=\"auditTrail\""]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_comparison_joined_by_AND_query(self):
        stix_pattern = "[x-sysdig-deployment:name = 'ibm-cloud-provider-ip-111-11-11-111' AND " \
                       "x-ibm-finding:x_threat_source = 'syscall']START t'2023-08-01T00:00:00.00Z' " \
                       "STOP t'2023-08-14T10:00:00.00Z'"
        query = translation.translate('sysdig', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["from=1690848000000000000&to=1692007200000000000&filter=(source=\"syscall\"and"
                   "kubernetes.deployment.name=\"ibm-cloud-provider-ip-111-11-11-111\")andsource!=\"auditTrail\""]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_comparison_joined_by_OR_query(self):
        stix_pattern = "[x-sysdig-deployment:name = 'ibm-cloud-provider-ip-111-11-11-111' OR " \
                       "x-ibm-finding:x_threat_source = 'syscall']START t'2023-08-01T00:00:00.00Z' " \
                       "STOP t'2023-08-14T10:00:00.00Z'"
        query = translation.translate('sysdig', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["from=1690848000000000000&to=1692007200000000000&filter=(source=\"syscall\"or"
                   "kubernetes.deployment.name=\"ibm-cloud-provider-ip-111-11-11-111\")andsource!=\"auditTrail\""]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_query_from_morethan_two_comparison_expressions_joined_by_and(self):
        stix_pattern = "[x-sysdig-cluster:namespace = 'dummycluster' AND x-sysdig-deployment:name != 'app-manager' " \
                       "AND mac-addr:value IN('00:aa:dd:99:77:00','00:77:66:99:11:dd')]"
        query = translation.translate('sysdig', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["from=1698317121307000064&to=1698317421307000064&filter=(machineId in "
                   "(\"00:aa:dd:99:77:00\",\"00:77:66:99:11:dd\")andkubernetes.deployment.name!=\"app-manager\"and"
                   "kubernetes.namespace.name=\"dummycluster\")andsource!=\"auditTrail\""]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_observation_with_qualifier_query(self):
        stix_pattern = "([x-sysdig-cluster:x_namespace='ap5s'AND x-sysdig-deployment:name='app-manager'] " \
                       "AND [mac-addr:value='00:77:66:99:11:dd' OR x-ibm-finding:name !='90-DayImageAge'] OR " \
                       "[x-oca-asset:extensions.'x-oca-container-ext'.x_repo='opencontent-etcd-operator'])" \
                       "START t'2023-09-10T08:43:10.003Z' STOP t'2023-09-20T10:43:10.005Z'"
        query = translation.translate('sysdig', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["from=1694335390003000064&to=1695206590004999936&filter=(ruleName!=\"90-DayImageAge\"ormachineId="
                   "\"00:77:66:99:11:dd\" or container.image.repo=\"opencontent-etcd-operator\")"
                   "andsource!=\"auditTrail\""
                   ]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_observation_without_qualifier_query(self):
        stix_pattern = "[x-sysdig-cluster:x_namespace!='dummycluster' OR x-sysdig-deployment:name='app-manager'] OR " \
                       "[mac-addr:value IN('00:aa:dd:99:77:99','66:77:88:99:11:dd') AND x-ibm-finding:name " \
                       "='90-DayImageAge'] AND [x-oca-asset:extensions.'x-oca-container-ext'." \
                       "x_repo='opencontent-etcd-operator']"
        query = translation.translate('sysdig', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["from=1699874733960000000&to=1699875033960000000&filter=(kubernetes.deployment.name=\"app-manager\" "
                   "or ruleName=\"90-DayImageAge\"andmachineId in (\"00:aa:dd:99:77:99\",\"66:77:88:99:11:dd\") "
                   "or container.image.repo=\"opencontent-etcd-operator\")andsource!=\"auditTrail\""]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_observation_with_and_without_qualifier_query(self):
        stix_pattern = "[x-oca-asset:extensions.'x-oca-container-ext'.image_id='1a1a1a1a1111a' " \
                       "OR x-sysdig-cluster:namespace != " \
                       "'openshift-cluster-node-tuning-operator' ]START t'2023-09-01T08:43:10.003Z'STOP " \
                       "t'2023-09-10T10:43:10.005Z' AND [x-ibm-finding:x_category = 'runtime']"
        query = translation.translate('sysdig', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["from=1693557790003000064&to=1694342590004999936&filter=(kubernetes.namespace.name!="
                   "\"openshift-cluster-node-tuning-operator\"orcontainer.image.id=\"1a1a1a1a1111a\")"
                   "andsource!=\"auditTrail\"",
                   "from=1698316240620000000&to=1698316540620000000&filter=(category="
                   "\"runtime\")andsource!=\"auditTrail\""]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_observation_by_AND_operator(self):
        stix_pattern = "[x-ibm-finding:severity <= 2] AND [x-sysdig-deployment:name = 'app-manager'] AND " \
                       "[x-sysdig-cluster:namespace = 'ap5s']START t'2023-09-01T08:43:10.003Z'STOP " \
                       "t'2023-09-10T10:43:10.005Z'"
        query = translation.translate('sysdig', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [
            "from=1699442518569999872&to=1699442818569999872&filter=(severity<=2 or kubernetes.deployment.name="
            "\"app-manager\")andsource!=\"auditTrail\"",
            "from=1693557790003000064&to=1694342590004999936&filter=(kubernetes.namespace.name=\"ap5s\")"
            "andsource!=\"auditTrail\""
        ]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_observation_combined_by_AND_OR_operators(self):
        stix_pattern = "[x-ibm-finding:severity >= 2 AND x-sysdig-deployment:name = 'app-manager']" \
                       "START t'2023-09-15T08:43:10.003Z'STOP t'2023-09-25T10:43:10.005Z' OR " \
                       "[x-sysdig-cluster:namespace = 'cluster'] AND [mac-addr:value IN " \
                       "('00:aa:dd:99:22:00','00:55:88:99:11:dd') OR x-ibm-finding:x_threat_source = 'syscall']" \
                       "START t'2023-09-01T08:43:10.003Z'STOP t'2023-09-10T10:43:10.005Z'"
        query = translation.translate('sysdig', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["from=1694767390003000064&to=1695638590004999936&filter=(kubernetes.deployment.name=\"app-manager\""
                   "andseverity>=2)andsource!=\"auditTrail\"",
                   "from=1699442789169999872&to=1699443089169999872&filter=(kubernetes.namespace.name=\"cluster\")"
                   "andsource!=\"auditTrail\"",
                   "from=1693557790003000064&to=1694342590004999936&filter=(source=\"syscall\"ormachineId in "
                   "(\"00:aa:dd:99:22:00\",\"00:55:88:99:11:dd\"))andsource!=\"auditTrail\""
                   ]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_comparison_with_OR_query(self):
        stix_pattern = "[x-ibm-finding:severity >= 2] OR [x-sysdig-deployment:name = 'app-manager'] OR " \
                       "[x-sysdig-cluster:namespace = 'cluster']START t'2023-09-01T08:43:10.003Z' STOP " \
                       "t'2023-09-10T10:43:10.005Z'"
        query = translation.translate('sysdig', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["from=1698304848484999936&to=1698305148484999936&filter=(severity>=2 or "
                   "kubernetes.deployment.name=\"app-manager\")andsource!=\"auditTrail\"",
                   "from=1693557790003000064&to=1694342590004999936&filter=(kubernetes.namespace.name=\"cluster\")"
                   "andsource!=\"auditTrail\""
                   ]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_invalid_int_type_value(self):
        stix_pattern = "[x-ibm-finding:severity = 'sysdig']"
        result = translation.translate('sysdig', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert "not_implemented" == result['code']
        assert "sysdig is not supported for integer type fields" in result['error']

    def test_with_greater_time_stamp_type(self):
        stix_pattern = "[x-sysdig-deployment:name = 'app-manager'] START t'2023-10-01T08:43:10.003Z' " \
                       "STOP t'2023-09-10T10:43:10.005Z'"
        result = translation.translate('sysdig', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert "translation_error" == result['code']
        assert "Start time should be lesser than Stop time" in result['error']

    def test_with_invalid_mapped_field_query(self):
        stix_pattern = "[x-ibm-finding:x_archived = 0]"
        result = translation.translate('sysdig', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert "mapping_error" == result['code']
        assert "Unable to map the following STIX objects and properties" in result['error']

    def test_not_supported_operator_MATCHES(self):
        stix_pattern = "[x-ibm-finding:severity MATCHES '2']"
        result = translation.translate('sysdig', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert "mapping_error" == result['code']
        assert "Unable to map the following STIX Operators" in result['error']

    def test_not_supported_operator_LIKE(self):
        stix_pattern = "[x-ibm-finding:severity LIKE 2]"
        result = translation.translate('sysdig', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert "mapping_error" == result['code']
        assert "Unable to map the following STIX Operators" in result['error']

    def test_check_invalid_mac_adr_format(self):
        stix_pattern = "[mac-addr:value='00.aa.dd.99.77.99']"
        result = translation.translate('sysdig', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert "not_implemented" == result['code']
        assert "Invalid mac address - 00.aa.dd.99.77.99 provide" in result['error']

    def test_check_invalid_operator(self):
        stix_pattern = "[x-sysdig-deployment:name > 'app-manager']"
        result = translation.translate('sysdig', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert "not_implemented" == result['code']
        assert "> operator is not supported for string type input" in result['error']

    def test_check_audittrail_error(self):
        stix_pattern = "[x-ibm-finding:x_threat_source = 'auditTrail']"
        result = translation.translate('sysdig', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert "not_implemented" == result['code']
        assert "Sysdig connector does not provide auditTrail event" in result['error']
