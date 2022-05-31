from modulefinder import Module
from stix_shifter.stix_translation import stix_translation
from stix_shifter_utils.utils.error_response import ErrorCode
import unittest
import re


MODULE = "azure_sentinel"
translation = stix_translation.StixTranslation()

def _test_query_assertions(translated_query, test_query):
    assert translated_query['queries'] == test_query


class TestStixtoQuery(unittest.TestCase, object):

    def test_file_params_query(self):
        stix_pattern = "[file:path = '/etc/path']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        queries = ["SecurityEvent | where FilePath == '/etc/path'"]
        _test_query_assertions(query, queries)
    
    def test_process_params_query(self):
        stix_pattern = "[process:name =  'Advapi  ']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        queries = ["SecurityEvent | where ProcessName == 'Advapi  ' or LogonProcessName == 'Advapi  '"]
        _test_query_assertions(query, queries)

    def test_x_finding_params_query(self):
        stix_pattern = "[x-ibm-finding:name = 'Microsoft-Windows-Security-Auditing']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        queries = ["SecurityAlert | where AlertName == 'Microsoft-Windows-Security-Auditing'",
        "SecurityEvent | where EventSourceName == 'Microsoft-Windows-Security-Auditing'",
        "SecurityIncident | where IncidentName == 'Microsoft-Windows-Security-Auditing'"]
        _test_query_assertions(query, queries)

    def test_x_oca_params_query(self):
        stix_pattern = "[x-oca-event:code = '4625']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        queries = ["SecurityEvent | where EventID == '4625'"]
        _test_query_assertions(query, queries)

    def test_url_params_query(self):
        stix_pattern = "[url:name = 'https://portal.azure.com/#asset/Microsoft_Azure_Security_Insights/Incident/subscriptions/dc26ff57-0597-4cc8-8092-aa5b929f8f39/resourceGroups/newresource/providers/Microsoft.OperationalInsights/workspaces/loganaly/providers/Microsoft.SecurityInsights/Incidents/919158c6-4c3f-4273-a730-a37f75622350']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        queries = ["SecurityEvent | where QuarantineHelpURL == 'https://portal.azure.com/#asset/Microsoft_Azure_Security_Insights/Incident/subscriptions/dc26ff57-0597-4cc8-8092-aa5b929f8f39/resourceGroups/newresource/providers/Microsoft.OperationalInsights/workspaces/loganaly/providers/Microsoft.SecurityInsights/Incidents/919158c6-4c3f-4273-a730-a37f75622350'",
        "SecurityIncident | where IncidentUrl == 'https://portal.azure.com/#asset/Microsoft_Azure_Security_Insights/Incident/subscriptions/dc26ff57-0597-4cc8-8092-aa5b929f8f39/resourceGroups/newresource/providers/Microsoft.OperationalInsights/workspaces/loganaly/providers/Microsoft.SecurityInsights/Incidents/919158c6-4c3f-4273-a730-a37f75622350'"]
        _test_query_assertions(query, queries)

    def test_domain_params_query(self):
        stix_pattern = "[domain-name:value = 'GSLAB']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        queries = ["SecurityEvent | where TargetDomainName == 'GSLAB' or SubjectDomainName == 'GSLAB'"]
        _test_query_assertions(query, queries)

    def test_no_eq__query(self):
        stix_pattern = "[ipv4-addr:value != '80.66.76.145']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        queries = ["SecurityEvent | where IpAddress != '80.66.76.145'"]
        _test_query_assertions(query, queries)

    def test_invalid_stix_pattern(self):
        stix_pattern = "[not_a_valid_pattern]"
        result = translation.translate(MODULE, 'query', '{}', stix_pattern, {'validate_pattern': 'true'})
        assert False == result['success']
        assert ErrorCode.TRANSLATION_STIX_VALIDATION.value == result['code']
        assert stix_pattern[1:-1] in result['error']

    def test_query_from_multiple_comparison_expressions_joined_by_AND(self):
        stix_pattern = "[x-msazure-sentinel-alert:status = 'New' AND x-msazure-sentinel-alert:alert_severity= 'Medium']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        # Expect the STIX AND to convert to an AQL AND.
        queries = ["SecurityAlert | where AlertSeverity == 'Medium' and Status == 'New'"]
        _test_query_assertions(query, queries)
    
    def test_query_from_multiple_comparison_expressions_joined_by_OR(self):
        stix_pattern = "[x-msazure-sentinel-alert:status = 'New' OR x-msazure-sentinel-alert:alert_severity= 'Medium']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        # Expect the STIX AND to convert to an AQL AND.
        queries = ["SecurityAlert | where AlertSeverity == 'Medium' or Status == 'New'"]
        _test_query_assertions(query, queries)

    def test_start_stop_qualifiers(self):
        stix_pattern = "[ipv4-addr:value = '80.66.76.145'] START t'2022-05-20T12:24:01.009Z' STOP t'2022-05-28T12:54:01.009Z'"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        queries = ["SecurityEvent | where IpAddress == '80.66.76.145' and TimeGenerated between (datetime(2022-05-20T12:24:01.009Z) .. datetime(2022-05-28T12:54:01.009Z))"]
        _test_query_assertions(query, queries)

    def test_computer_query(self):
        stix_pattern = "[x-msazure-sentinel-event:computer = 'GslabAzure']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        queries = ["SecurityEvent | where Computer == 'GslabAzure'"]
        _test_query_assertions(query, queries)
    
    def test_incident_name_query(self):
        stix_pattern = "[x-msazure-sentinel-incident:incident_name = 'e1b1ea91-cd8d-4304-8689-bcb357e251f7']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        queries = ["SecurityIncident | where IncidentName == 'e1b1ea91-cd8d-4304-8689-bcb357e251f7'"]
        _test_query_assertions(query, queries)

    def test_user_account_query(self):
        stix_pattern = "[user-account:account_login = 'GS-2530']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        queries = ["SecurityEvent | where TargetUserName == 'GS-2530'"]
        _test_query_assertions(query, queries)