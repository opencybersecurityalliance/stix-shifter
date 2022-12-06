import unittest
import re
import json
from stix_shifter.stix_translation import stix_translation
from stix_shifter_utils.utils.error_response import ErrorCode

MODULE = "azure_log_analytics"
translation = stix_translation.StixTranslation()


def _remove_timestamp_from_query(queries):
    pattern = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z'
    if isinstance(queries, list):
        return [re.sub(pattern, "", query) for query in queries]
    elif isinstance(queries, str):
        return re.sub(pattern, "", queries)


class TestStixtoQuery(unittest.TestCase, object):
    def _test_query_assertions(self, query, queries):
        """
        to assert the each query in the list against expected result
        """
        self.assertIsInstance(query, dict)
        self.assertIsInstance(query['queries'], list)
        for index, each_query in enumerate(query.get('queries'), start=0):
              self.assertEqual(each_query, queries[index])

    def test_file_params_query(self):
        stix_pattern = "[file:path = '/etc/path']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ["SecurityEvent | where (FilePath == '/etc/path') and (TimeGenerated between "
                   "(datetime(2022-07-12T13:25:17.925Z) .. datetime(2022-07-13T13:25:17.925Z)))"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_process_params_query(self):
        stix_pattern = "[process:name =  'Advapi  ']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ["SecurityEvent | where ((ProcessName == 'Advapi  ' or LogonProcessName == 'Advapi  ')) and "
                   "(TimeGenerated between (datetime(2022-07-12T14:08:35.514Z) .. datetime(2022-07-13T14:08:35.514Z)))"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_x_finding_params_query(self):
        stix_pattern = "[x-ibm-finding:name = 'Microsoft-Windows-Security-Auditing']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            "SecurityEvent | where (EventSourceName == 'Microsoft-Windows-Security-Auditing') and "
            "(TimeGenerated between (datetime(2022-07-12T14:09:21.480Z) .. datetime(2022-07-13T14:09:21.480Z)))",
            "SecurityIncident | where (IncidentName == 'Microsoft-Windows-Security-Auditing') and "
            "(TimeGenerated between (datetime(2022-07-12T14:09:21.481Z) .. datetime(2022-07-13T14:09:21.481Z)))",
            "SecurityAlert | where (AlertName == 'Microsoft-Windows-Security-Auditing') and "
            "(TimeGenerated between (datetime(2022-07-12T14:09:21.479Z) .. datetime(2022-07-13T14:09:21.479Z)))"
        ]
        queries = _remove_timestamp_from_query(queries)
        self.assertSetEqual(set(query['queries']), set(queries))

    def test_x_oca_params_query(self):
        stix_pattern = "[x-oca-event:code = '4625']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["SecurityEvent | where (EventID == '4625') and "
                   "(TimeGenerated between (datetime(2022-07-12T14:14:24.165Z) .. datetime(2022-07-13T14:14:24.165Z)))"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_url_params_query(self):
        stix_pattern = "[url:value = 'https://portal.azure.com/#asset/Microsoft_Azure_Security_Insights/Incident/subscriptions/dc26ff57-0597-4cc8-8092-aa5b929f8f39/resourceGroups/newresource/providers/Microsoft.OperationalInsights/workspaces/loganaly/providers/Microsoft.SecurityInsights/Incidents/919158c6-4c3f-4273-a730-a37f75622350']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            "SecurityEvent | where (QuarantineHelpURL == 'https://portal.azure.com/#asset/Microsoft_Azure_Security_Insights/Incident/subscriptions/dc26ff57-0597-4cc8-8092-aa5b929f8f39/resourceGroups/newresource/providers/Microsoft.OperationalInsights/workspaces/loganaly/providers/Microsoft.SecurityInsights/Incidents/919158c6-4c3f-4273-a730-a37f75622350') and (TimeGenerated between (datetime(2022-07-12T14:15:10.877Z) .. datetime(2022-07-13T14:15:10.877Z)))",
            "SecurityIncident | where (IncidentUrl == 'https://portal.azure.com/#asset/Microsoft_Azure_Security_Insights/Incident/subscriptions/dc26ff57-0597-4cc8-8092-aa5b929f8f39/resourceGroups/newresource/providers/Microsoft.OperationalInsights/workspaces/loganaly/providers/Microsoft.SecurityInsights/Incidents/919158c6-4c3f-4273-a730-a37f75622350') and (TimeGenerated between (datetime(2022-07-12T14:15:10.878Z) .. datetime(2022-07-13T14:15:10.878Z)))"
        ]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_domain_params_query(self):
        stix_pattern = "[domain-name:value = 'GSLAB']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ["SecurityEvent | where (TargetDomainName == 'GSLAB') and "
                   "(TimeGenerated between (datetime(2022-07-12T14:16:12.975Z) .. datetime(2022-07-13T14:16:12.975Z)))"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_no_eq__query(self):
        stix_pattern = "[ipv4-addr:value != '80.66.76.145']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ["SecurityEvent | where (IpAddress != '80.66.76.145') and "
                   "(TimeGenerated between (datetime(2022-07-12T14:16:50.268Z) .. datetime(2022-07-13T14:16:50.268Z)))"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_invalid_stix_pattern(self):
        stix_pattern = "[not_a_valid_pattern]"
        result = translation.translate(MODULE, 'query', '{}', stix_pattern, {'validate_pattern': 'true'})
        assert False == result['success']
        assert ErrorCode.TRANSLATION_STIX_VALIDATION.value == result['code']
        assert stix_pattern[1:-1] in result['error']

    def test_query_from_multiple_comparison_expressions_joined_by_AND(self):
        stix_pattern = "[x-msazure-sentinel-alert:status = 'New' AND x-msazure-sentinel-alert:alert_severity= 'Medium']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        # Expect the STIX AND to convert to an AQL AND.
        queries = ["SecurityAlert | where (AlertSeverity == 'Medium' and Status == 'New') and "
                   "(TimeGenerated between (datetime(2022-07-12T14:17:34.629Z) .. datetime(2022-07-13T14:17:34.629Z)))"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_query_from_multiple_comparison_expressions_joined_by_OR(self):
        stix_pattern = "[x-msazure-sentinel-alert:status = 'New' OR x-msazure-sentinel-alert:alert_severity= 'Medium']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        # Expect the STIX AND to convert to an AQL AND.
        queries = ["SecurityAlert | where (AlertSeverity == 'Medium' or Status == 'New') and "
                   "(TimeGenerated between (datetime(2022-07-12T14:18:24.375Z) .. datetime(2022-07-13T14:18:24.375Z)))"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_start_stop_qualifiers(self):
        stix_pattern = "[ipv4-addr:value = '80.66.76.145'] START t'2022-05-20T12:24:01.009Z' STOP t'2022-05-28T12:54:01.009Z'"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)

        queries = ["SecurityEvent | where (IpAddress == '80.66.76.145') and "
                   "(TimeGenerated between (datetime(2022-05-20T12:24:01.009Z) .. datetime(2022-05-28T12:54:01.009Z)))"]

        self._test_query_assertions(query, queries)

    def test_computer_query(self):
        stix_pattern = "[x-msazure-sentinel-event:computer = 'GslabAzure']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ["SecurityEvent | where (Computer == 'GslabAzure') and "
                   "(TimeGenerated between (datetime(2022-07-12T14:21:28.147Z) .. datetime(2022-07-13T14:21:28.147Z)))"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_incident_name_query(self):
        stix_pattern = "[x-msazure-sentinel-incident:incident_name = 'e1b1ea91-cd8d-4304-8689-bcb357e251f7']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ["SecurityIncident | where (IncidentName == 'e1b1ea91-cd8d-4304-8689-bcb357e251f7') and "
                   "(TimeGenerated between (datetime(2022-07-12T14:22:11.616Z) .. datetime(2022-07-13T14:22:11.616Z)))"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_user_account_query(self):
        stix_pattern = "[user-account:account_login = 'GS-2530']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ["SecurityEvent | where (TargetUserName == 'GS-2530') and "
                   "(TimeGenerated between (datetime(2022-07-12T14:22:45.070Z) .. datetime(2022-07-13T14:22:45.070Z)))"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)
