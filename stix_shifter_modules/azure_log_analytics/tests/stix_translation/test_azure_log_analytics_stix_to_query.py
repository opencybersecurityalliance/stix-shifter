import unittest
import re
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
        stix_pattern = "[process:x_mandatory_label =  'test']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ["SecurityEvent | where (MandatoryLabel == 'test') and (TimeGenerated between (datetime("
                   "2023-05-18T05:07:01.882Z) .. datetime(2023-05-19T05:07:01.882Z)))"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_x_finding_params_query(self):
        stix_pattern = "[x-ibm-finding:name = 'Microsoft-Windows-Security-Auditing']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ["SecurityAlert | where (AlertName == 'Microsoft-Windows-Security-Auditing') and (TimeGenerated "
                   "between (datetime(2023-04-10T03:01:39.225Z) .. datetime(2023-04-11T03:01:39.225Z)))",
                   "SecurityEvent | where (Activity == 'Microsoft-Windows-Security-Auditing') and (TimeGenerated "
                   "between (datetime(2023-04-10T03:01:39.231Z) .. datetime(2023-04-11T03:01:39.231Z)))",
                   "SecurityIncident | where (Title == 'Microsoft-Windows-Security-Auditing') and (TimeGenerated "
                   "between (datetime(2023-04-10T03:01:39.236Z) .. datetime(2023-04-11T03:01:39.236Z)))"]

        queries = _remove_timestamp_from_query(queries)
        self.assertSetEqual(set(query['queries']), set(queries))

    def test_x_oca_params_query(self):
        stix_pattern = "[x-oca-event:code = '4625']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["SecurityEvent | where (EventID == 4625) and "
                   "(TimeGenerated between (datetime(2022-07-12T14:14:24.165Z) .. datetime(2022-07-13T14:14:24.165Z)))"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_url_params_query(self):
        stix_pattern = "[url:value = 'https://portal.azure.com'] "
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ["SecurityAlert | mv-expand parsed_entities = parse_json(Entities) | where (parsed_entities.Url == "
                   "'https://portal.azure.com') and (TimeGenerated between (datetime(2023-04-23T10:46:37.351Z) .. "
                   "datetime(2023-04-24T10:46:37.351Z))) | summarize arg_max(TimeGenerated, *) by TimeGenerated, "
                   "SystemAlertId",
                   "SecurityEvent | where (QuarantineHelpURL == 'https://portal.azure.com') and (TimeGenerated "
                   "between (datetime(2023-04-23T10:46:37.355Z) .. datetime(2023-04-24T10:46:37.355Z)))",
                   "SecurityIncident | where (IncidentUrl == 'https://portal.azure.com') and (TimeGenerated between ("
                   "datetime(2023-04-23T10:46:37.359Z) .. datetime(2023-04-24T10:46:37.359Z)))"]

        queries = _remove_timestamp_from_query(queries)
        self.assertSetEqual(set(query['queries']), set(queries))

    def test_domain_params_query(self):
        stix_pattern = "[domain-name:value = 'GSLAB']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["SecurityAlert | mv-expand parsed_entities = parse_json(Entities) | where ("
                   "parsed_entities.DomainName == 'GSLAB') and (TimeGenerated between (datetime("
                   "2023-04-02T07:32:08.854Z) .. datetime(2023-04-03T07:32:08.854Z))) | summarize arg_max("
                   "TimeGenerated, *) by TimeGenerated, SystemAlertId",
                   "SecurityEvent | where (TargetDomainName == 'GSLAB') and (TimeGenerated between (datetime("
                   "2023-04-02T07:32:08.858Z) .. datetime(2023-04-03T07:32:08.858Z)))"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_not_eq_query(self):
        stix_pattern = "[ipv4-addr:x_location_ref.organization != 'test_domain']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ["SecurityAlert | mv-expand parsed_entities = parse_json(Entities) | where (notnull("
                   "parsed_entities.Location.Organization) and parsed_entities.Location.Organization != "
                   "'test_domain') and (TimeGenerated between (datetime(2023-05-04T12:03:12.180Z) .. datetime("
                   "2023-05-05T12:03:12.180Z))) | summarize arg_max(TimeGenerated, *) by TimeGenerated, SystemAlertId"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_invalid_stix_pattern(self):
        stix_pattern = "[not_a_valid_pattern]"
        result = translation.translate(MODULE, 'query', '{}', stix_pattern, {'validate_pattern': 'true'})
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_STIX_VALIDATION.value == result['code']
        assert stix_pattern[1:-1] in result['error']

    def test_query_from_multiple_comparison_expressions_joined_by_AND(self):
        stix_pattern = "[user-account:user_id = 'testuser' AND x-ibm-finding:severity IN (100,50)]"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        # Expect the STIX AND to convert to an KQL AND.
        queries = ["SecurityAlert | mv-expand parsed_entities = parse_json(Entities) | where (AlertSeverity in~ ("
                   "'High', 'Low') and parsed_entities.Name == 'testuser') and (TimeGenerated between (datetime() .. "
                   "datetime())) | summarize arg_max(TimeGenerated, *) by TimeGenerated, SystemAlertId"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_query_from_multiple_comparison_expressions_joined_by_OR(self):
        stix_pattern = "[x-oca-event:module = 'test' OR x-oca-event:x_requester = 'test1']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        # Expect the STIX AND to convert to an KQL AND.
        queries = ["SecurityEvent | where (Requester == 'test1' or Channel == 'test') and (TimeGenerated between ("
                   "datetime(2023-05-02T03:48:36.871Z) .. datetime(2023-05-03T03:48:36.871Z)))"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_start_stop_qualifiers(self):
        stix_pattern = "[x-logon-info:guid = 'XXXXXXXX-XXXX-XXXX'] START t'2022-05-20T12:24:01Z' STOP " \
                       "t'2022-05-28T12:54:01.009Z' "
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)

        queries = ["SecurityEvent | where (LogonGuid == 'XXXXXXXX-XXXX-XXXX') and (TimeGenerated between (datetime("
                   "2022-05-20T12:24:01.000Z) .. datetime(2022-05-28T12:54:01.009Z)))"]
        self._test_query_assertions(query, queries)

    def test_computer_query(self):
        stix_pattern = "[x-oca-asset:x_nt_domain = 'GslabAzure']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ["SecurityAlert | mv-expand parsed_entities = parse_json(Entities) | where ("
                   "parsed_entities.NTDomain == 'GslabAzure') and (TimeGenerated between (datetime() .. datetime())) "
                   "| summarize arg_max(TimeGenerated, *) by TimeGenerated, SystemAlertId"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_user_account_query(self):
        stix_pattern = "[user-account:account_login = 'GS-2530']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ["SecurityEvent | where ((TargetAccount == 'GS-2530' or SubjectAccount == 'GS-2530')) and ("
                   "TimeGenerated between (datetime(2023-05-16T02:51:23.271Z) .. datetime(2023-05-17T02:51:23.271Z)))"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_in_operator(self):
        stix_pattern = ("[process:parent_ref.name IN ('pwsh.exe','powershell.exe', 'cmd.exe')]"
                        " START t'2023-02-14T19:43:08.674Z' STOP t'2023-02-28T19:43:08.674Z'")
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ["SecurityEvent | where (ParentProcessName in~ ('pwsh.exe', 'powershell.exe', 'cmd.exe')) and ("
                   "TimeGenerated between (datetime(2023-02-14T19:43:08.674Z) .. datetime(2023-02-28T19:43:08.674Z)))"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_like_operator(self):
        stix_pattern = "[user-account:x_nt_domain LIKE 'azure']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["SecurityAlert | mv-expand parsed_entities = parse_json(Entities) | where ("
                   "parsed_entities.NTDomain contains 'azure') and (TimeGenerated between (datetime("
                   "2023-05-16T02:53:31.647Z) .. datetime(2023-05-17T02:53:31.647Z))) | summarize arg_max("
                   "TimeGenerated, *) by TimeGenerated, SystemAlertId"]
        queries = _remove_timestamp_from_query(queries)
        self.assertSetEqual(set(query['queries']), set(queries))

    def test_match_operator(self):
        stix_pattern = "[x-oca-event:code MATCHES '123']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["SecurityEvent | where (tostring(EventID) matches regex '123') and (TimeGenerated between ("
                   "datetime(2023-04-02T08:01:52.362Z) .. datetime(2023-04-03T08:01:52.362Z)))"]
        queries = _remove_timestamp_from_query(queries)
        self.assertSetEqual(set(query['queries']), set(queries))

    def test_not_in_operator(self):
        stix_pattern = "[email-addr:display_name NOT IN ('test1@azure.com','test2@azure.com')]"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["SecurityIncident | where (not (Owner.assignedTo in~ ('test1@azure.com', 'test2@azure.com'))) and "
                   "(TimeGenerated between (datetime(2023-05-03T11:03:18.209Z) .. datetime("
                   "2023-05-04T11:03:18.209Z)))"]
        queries = _remove_timestamp_from_query(queries)
        self.assertSetEqual(set(query['queries']), set(queries))

    def test_comparator_operator(self):
        stix_pattern = "[x-oca-event:x_task > 200 AND x-oca-event:x_task < 300]"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['SecurityEvent | where (Task < 300 and Task > 200) and (TimeGenerated between (datetime('
                   '2023-04-10T03:24:58.513Z) .. datetime(2023-04-11T03:24:58.513Z)))']
        queries = _remove_timestamp_from_query(queries)
        self.assertSetEqual(set(query['queries']), set(queries))

    def test_invalid_comparator_operator(self):
        stix_pattern = "[process:command_line >= 200]"
        result = translation.translate(MODULE, 'query', '{}', stix_pattern)
        assert False is result['success']
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']

    def test_invalid_enum_operator(self):
        stix_pattern = "[x-ibm-finding:severity LIKE 100]"
        result = translation.translate(MODULE, 'query', '{}', stix_pattern)
        assert False is result['success']
        assert result['error'] == "azure_log_analytics connector error => wrong parameter : Like operator is not " \
                                  "supported for Enum type input. Possible supported operator are [ =, !=, IN, " \
                                  "NOT IN ]"
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']

    def test_invalid_enum_value(self):
        stix_pattern = "[x-ibm-finding:severity == 101]"
        result = translation.translate(MODULE, 'query', '{}', stix_pattern)
        assert False is result['success']
        assert result['error'] == 'azure_log_analytics connector error => wrong parameter : Unsupported ENUM values ' \
                                  'provided. Possible supported enum values are [\'25\', \'50\', \'75\', \'100\']'
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']

    def test_multiple_observation(self):
        stix_pattern = "[x-host-logon-session:session_id == 123] AND [x-cloud-resource:resource_type = 'host']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["SecurityAlert | mv-expand parsed_entities = parse_json(Entities) | mv-expand parsed_properties = "
                   "parse_json(ExtendedProperties) | where (parsed_entities.SessionId == 123) and (TimeGenerated "
                   "between (datetime(2023-05-21T11:02:30.723Z) .. datetime(2023-05-22T11:02:30.723Z))) or ("
                   "parsed_properties.resourceType == 'host') and (TimeGenerated between (datetime("
                   "2023-05-21T11:02:30.723Z) .. datetime(2023-05-22T11:02:30.723Z))) | summarize arg_max("
                   "TimeGenerated, *) by TimeGenerated, SystemAlertId"]
        queries = _remove_timestamp_from_query(queries)
        self.assertSetEqual(set(query['queries']), set(queries))

    def test_multiple_observation_with_qualifier(self):
        stix_pattern = "([x-ibm-finding:severity == '75'] OR [file:hashes.MD5 IN ('file1', 'file2')]) START " \
                       "t'2023-03-01T11:00:00.003Z' STOP t'2023-03-20T11:00:00.003Z' "
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["SecurityAlert | mv-expand parsed_entities = parse_json(Entities) | where (AlertSeverity == "
                   "'Medium') and (TimeGenerated between (datetime(2023-03-01T11:00:00.003Z) .. datetime("
                   "2023-03-20T11:00:00.003Z))) or ((parsed_entities.Algorithm == 'MD5' and parsed_entities.Value in~ "
                   "('file1', 'file2'))) and (TimeGenerated between (datetime(2023-03-01T11:00:00.003Z) .. datetime("
                   "2023-03-20T11:00:00.003Z))) | summarize arg_max(TimeGenerated, *) by TimeGenerated, SystemAlertId",
                   "SecurityEvent | where (FileHash in~ ('file1', 'file2')) and (TimeGenerated between (datetime("
                   "2023-03-01T11:00:00.003Z) .. datetime(2023-03-20T11:00:00.003Z)))",
                   "SecurityIncident | where (Severity == 'Medium') and (TimeGenerated between (datetime("
                   "2023-03-01T11:00:00.003Z) .. datetime(2023-03-20T11:00:00.003Z)))"]
        queries = _remove_timestamp_from_query(queries)
        self.assertSetEqual(set(query['queries']), set(queries))

    def test_score_conversion(self):
        stix_pattern = "[x-ibm-finding:confidence = 81 AND x-ibm-finding:confidence IN (81, 90) AND " \
                       "x-ibm-finding:confidence LIKE '90'] "
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["SecurityAlert | where (tostring(ConfidenceScore) contains '9.0' and (ConfidenceScore in~ ('8.1', "
                   "'9.0') and ConfidenceScore == 8.1)) and (TimeGenerated between (datetime("
                   "2023-04-19T08:28:56.987Z) .. datetime(2023-04-20T08:28:56.987Z)))"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_hexa_field_query(self):
        stix_pattern = "[x-host-logon-session:session_id = '0x427d8dd9']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['SecurityAlert | mv-expand parsed_entities = parse_json(Entities) | where ('
                   'parsed_entities.SessionId == 1115524569) and (TimeGenerated between (datetime('
                   '2023-05-17T09:22:12.628Z) .. datetime(2023-05-18T09:22:12.628Z))) | summarize arg_max('
                   'TimeGenerated, *) by TimeGenerated, SystemAlertId']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_hexa_invalid_stix_pattern(self):
        stix_pattern = "[x-host-logon-session:session_id LIKE '0x427d8dd9']"
        result = translation.translate(MODULE, 'query', '{}', stix_pattern, {'validate_pattern': 'true'})
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert 'IN/LIKE/MATCHES operator is unsupported for hexadecimal fields in AZURE LOG ANALYTICS' in \
               result['error']
