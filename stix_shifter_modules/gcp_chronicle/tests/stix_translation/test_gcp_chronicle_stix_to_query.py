from stix_shifter.stix_translation import stix_translation
from stix_shifter_utils.utils.error_response import ErrorCode
import unittest
import re

translation = stix_translation.StixTranslation()


def _remove_timestamp_from_query(queries):
    pattern1 = r"\s*rule_\d{0,10}"
    pattern2 = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z)"
    if isinstance(queries, list):
        modified_queries = []
        for query in queries:
            replace_pat1 = re.sub(pattern1, '', str(query))
            replace_pat2 = re.sub(pattern2, '{}', replace_pat1)
            modified_queries.append(replace_pat2)
        return modified_queries
    elif isinstance(queries, str):
        replace_pat1 = re.sub(pattern1, '', queries)
        return re.sub(pattern2, '{}', replace_pat1)


class TestQueryTranslator(unittest.TestCase):
    """
    class to perform unit test case gcp_chronicle translate query
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
        stix_pattern = "[ipv4-addr:value = '168.149.184.42']"
        query = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'ruleText': 'rule cp4s_gcp_udi_rule_1657866177 { meta: author = \"ibm cp4s user\" description = "
                   "\"Create event rule that should generate detections\" events: any $udm.src.ip = "
                   "\"168.149.184.42\" nocase or any $udm.target.ip = \"168.149.184.42\" nocase or any "
                   "$udm.principal.ip = \"168.149.184.42\" nocase condition: $udm}', 'startTime': "
                   "'2022-07-15T06:17:57.070Z', 'endTime': '2022-07-15T06:22:57.070Z'}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_not_in_operator(self):
        stix_pattern = "[x-ibm-finding:severity NOT IN (48,100)]"
        query = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'ruleText': 'rule cp4s_gcp_udi_rule_1659622650 { meta: author = \"ibm cp4s user\" description = "
                   "\"Create event rule that should generate detections\" events: ( all $udm.security_result.severity "
                   "!= \"LOW\"  and all $udm.security_result.severity != \"UNKNOWN_SEVERITY\" ) and ( all "
                   "$udm.security_result.severity != \"CRITICAL\"  and all $udm.security_result.severity != "
                   "\"UNKNOWN_SEVERITY\" ) condition: $udm}', 'startTime': '2022-08-04T14:12:30.243Z', 'endTime': "
                   "'2022-08-04T14:17:30.243Z'}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_network_traffic_query(self):
        stix_pattern = "[network-traffic:src_port = 52221]"
        query = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'ruleText': 'rule cp4s_gcp_udi_rule_1657869892 { meta: author = \"ibm cp4s user\" description = "
                   "\"Create event rule that should generate detections\" events: $udm.src.port = 52221 or "
                   "$udm.principal.port = 52221 condition: $udm}', 'startTime': '2022-07-15T07:19:52.556Z', "
                   "'endTime': '2022-07-15T07:24:52.556Z'}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_network_query_not_equals_operator(self):
        stix_pattern = "[network-traffic:src_port != 52221]"
        query = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'ruleText': 'rule cp4s_gcp_udi_rule_1659623807 { meta: author = \"ibm cp4s user\" description = "
                   "\"Create event rule that should generate detections\" events: ( $udm.src.port != 52221  and "
                   "$udm.src.port != 0 ) or ( $udm.principal.port != 52221  and $udm.principal.port != 0 ) condition: "
                   "$udm}', 'startTime': '2022-06-03T00:00:00.000000Z', 'endTime': '2022-06-15T00:00:00.000000Z'}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_network_query_greater_than_operator(self):
        stix_pattern = "[network-traffic:src_port > 52221]"
        query = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'ruleText': 'rule cp4s_gcp_udi_rule_1657870655 { meta: author = \"ibm cp4s user\" description = "
                   "\"Create event rule that should generate detections\" events: $udm.src.port > 52221 or "
                   "$udm.principal.port > 52221 condition: $udm}', 'startTime': '2022-07-15T07:32:35.696Z', "
                   "'endTime': '2022-07-15T07:37:35.696Z'}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_network_query_not_greater_than_operator(self):
        stix_pattern = "[network-traffic:src_port NOT > 52221]"
        query = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'ruleText': 'rule cp4s_gcp_udi_rule_1659623971 { meta: author = \"ibm cp4s user\" description = "
                   "\"Create event rule that should generate detections\" events: ( $udm.src.port <= 52221  and "
                   "$udm.src.port != 0 ) or ( $udm.principal.port <= 52221  and $udm.principal.port != 0 ) condition: "
                   "$udm}', 'startTime': '2022-08-04T14:34:31.496Z', 'endTime': '2022-08-04T14:39:31.496Z'}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_network_query_less_than_operator(self):
        stix_pattern = "[network-traffic:src_port < 52221]"
        query = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'ruleText': 'rule cp4s_gcp_udi_rule_1659624239 { meta: author = \"ibm cp4s user\" description = "
                   "\"Create event rule that should generate detections\" events: ( $udm.src.port < 52221  and "
                   "$udm.src.port != 0 ) or ( $udm.principal.port < 52221  and $udm.principal.port != 0 ) condition: "
                   "$udm}', 'startTime': '2022-08-04T14:38:59.430Z', 'endTime': '2022-08-04T14:43:59.430Z'}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_network_query_less_than_or_equals(self):
        stix_pattern = "[network-traffic:src_port <= 52221]"
        query = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'ruleText': 'rule cp4s_gcp_udi_rule_1659624514 { meta: author = \"ibm cp4s user\" description = "
                   "\"Create event rule that should generate detections\" events: ( $udm.src.port <= 52221  and "
                   "$udm.src.port != 0 ) or ( $udm.principal.port <= 52221  and $udm.principal.port != 0 ) condition: "
                   "$udm}', 'startTime': '2022-08-04T14:43:34.685Z', 'endTime': '2022-08-04T14:48:34.685Z'}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_network_query_greater_than_or_equals(self):
        stix_pattern = "[network-traffic:src_port >= 52221]"
        query = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'ruleText': 'rule cp4s_gcp_udi_rule_1657871257 { meta: author = \"ibm cp4s user\" description = "
                   "\"Create event rule that should generate detections\" events: $udm.src.port >= 52221 or "
                   "$udm.principal.port >= 52221 condition: $udm}', 'startTime': '2022-07-15T07:42:37.847Z', "
                   "'endTime': '2022-07-15T07:47:37.847Z'}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_query_in_operator(self):
        stix_pattern = "[x-ibm-finding:finding_type IN ('threat'," \
                       "'violation','alert','policy')] "
        query = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'ruleText': 'rule cp4s_gcp_udi_rule_1658996269 { meta: author = \"ibm cp4s user\" description = "
                   "\"Create event rule that should generate detections\" events: any $udm.security_result.category = "
                   "\"SOFTWARE_MALICIOUS\" or any $udm.security_result.category = \"SOFTWARE_PUA\" or any "
                   "$udm.security_result.category = \"NETWORK_MALICIOUS\" or any $udm.security_result.category = "
                   "\"MAIL_SPAM\" or any $udm.security_result.category = \"MAIL_PHISHING\" or any "
                   "$udm.security_result.category = \"MAIL_SPOOFING\" or any $udm.security_result.category = "
                   "\"ACL_VIOLATION\" or any $udm.security_result.category = \"AUTH_VIOLATION\" or any "
                   "$udm.security_result.category = \"SOFTWARE_SUSPICIOUS\" or any $udm.security_result.category = "
                   "\"NETWORK_SUSPICIOUS\" or any $udm.security_result.category = \"NETWORK_CATEGORIZED_CONTENT\" or "
                   "any $udm.security_result.category = \"NETWORK_DENIAL_OF_SERVICE\" or any "
                   "$udm.security_result.category = \"NETWORK_RECON\" or any $udm.security_result.category = "
                   "\"NETWORK_COMMAND_AND_CONTROL\" or any $udm.security_result.category = \"EXPLOIT\" or any "
                   "$udm.security_result.category = \"DATA_EXFILTRATION\" or any $udm.security_result.category = "
                   "\"DATA_AT_REST\" or any $udm.security_result.category = \"DATA_DESTRUCTION\" or any "
                   "$udm.security_result.category = \"POLICY_VIOLATION\" condition: $udm}', 'startTime': "
                   "'2022-07-28T08:12:49.775Z', 'endTime': '2022-07-28T08:17:49.775Z'}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_file_query(self):
        stix_pattern = "[file:hashes.'SHA-1' = '6cbce4a295c163791b60fc23d285e6d84f28ee4c']"
        query = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'ruleText': 'rule cp4s_gcp_udi_rule_1657872913 { meta: author = \"ibm cp4s user\" description = "
                   "\"Create event rule that should generate detections\" events: $udm.src.file.sha1 = "
                   "\"6cbce4a295c163791b60fc23d285e6d84f28ee4c\" nocase or $udm.target.file.sha1 = "
                   "\"6cbce4a295c163791b60fc23d285e6d84f28ee4c\" nocase or $udm.src.process.file.sha1 = "
                   "\"6cbce4a295c163791b60fc23d285e6d84f28ee4c\" nocase or $udm.target.process.file.sha1 = "
                   "\"6cbce4a295c163791b60fc23d285e6d84f28ee4c\" nocase or $udm.principal.process.file.sha1 = "
                   "\"6cbce4a295c163791b60fc23d285e6d84f28ee4c\" nocase or $udm.about.file.sha1 = "
                   "\"6cbce4a295c163791b60fc23d285e6d84f28ee4c\" nocase condition: $udm}', 'startTime': "
                   "'2022-07-15T08:10:13.278Z', 'endTime': '2022-07-15T08:15:13.278Z'}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_valid_email_address_query(self):
        stix_pattern = "[email-addr:value IN ('admin@hcl.com','user@hcl.com')]"
        query = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'ruleText': 'rule cp4s_gcp_udi_rule_1658995859 { meta: author = \"ibm cp4s user\" description = "
                   "\"Create event rule that should generate detections\" events: (any "
                   "$udm.principal.user.email_addresses = \"admin@hcl.com\" nocase or any "
                   "$udm.principal.user.email_addresses = \"user@hcl.com\" nocase) or (any "
                   "$udm.src.user.email_addresses = \"admin@hcl.com\" nocase or any $udm.src.user.email_addresses = "
                   "\"user@hcl.com\" nocase) or (any $udm.target.user.email_addresses = \"admin@hcl.com\" nocase or "
                   "any $udm.target.user.email_addresses = \"user@hcl.com\" nocase) or ($udm.network.email.from = "
                   "\"admin@hcl.com\" nocase or $udm.network.email.from = \"user@hcl.com\" nocase) or (any "
                   "$udm.network.email.to = \"admin@hcl.com\" nocase or any $udm.network.email.to = \"user@hcl.com\" "
                   "nocase) or (any $udm.network.email.cc = \"admin@hcl.com\" nocase or any $udm.network.email.cc = "
                   "\"user@hcl.com\" nocase) or (any $udm.network.email.bcc = \"admin@hcl.com\" nocase or any "
                   "$udm.network.email.bcc = \"user@hcl.com\" nocase) or (any $udm.security_result.about.email = "
                   "\"admin@hcl.com\" nocase or any $udm.security_result.about.email = \"user@hcl.com\" nocase) "
                   "condition: $udm}', 'startTime': '2022-07-28T08:05:59.718Z', "
                   "'endTime': '2022-07-28T08:10:59.718Z'}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_user_account_query(self):
        stix_pattern = "[user-account:user_id = 'projectViewer:gdc-iac-day0-trng-03']"
        query = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'ruleText': 'rule cp4s_gcp_udi_rule_1657873245 { meta: author = \"ibm cp4s user\" description = "
                   "\"Create event rule that should generate detections\" events: $udm.src.user.userid = "
                   "\"projectViewer:gdc-iac-day0-trng-03\" nocase or $udm.target.user.userid = "
                   "\"projectViewer:gdc-iac-day0-trng-03\" nocase or $udm.principal.user.userid = "
                   "\"projectViewer:gdc-iac-day0-trng-03\" nocase condition: $udm}', 'startTime': "
                   "'2022-07-15T08:15:45.325Z', 'endTime': '2022-07-15T08:20:45.325Z'}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_mac_address_query(self):
        stix_pattern = "[mac-addr:value ='12:83:0e:be:f3:1d']"
        query = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'ruleText': 'rule cp4s_gcp_udi_rule_1657873407 { meta: author = \"ibm cp4s user\" description = "
                   "\"Create event rule that should generate detections\" events: any $udm.src.mac = "
                   "\"12:83:0e:be:f3:1d\" nocase or any $udm.target.mac = \"12:83:0e:be:f3:1d\" nocase or any "
                   "$udm.principal.mac = \"12:83:0e:be:f3:1d\" nocase condition: $udm}', 'startTime': "
                   "'2022-07-15T08:18:27.969Z', 'endTime': '2022-07-15T08:23:27.969Z'}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_process_like_operator(self):
        stix_pattern = "[process:name LIKE 'powershell.exe']"
        query = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'ruleText': 'rule cp4s_gcp_udi_rule_1657873647 { meta: author = \"ibm cp4s user\" description = "
                   "\"Create event rule that should generate detections\" events: $udm.src.process.file.full_path = "
                   "/(?s)powershell\\\\.exe/ nocase or $udm.target.process.file.full_path = /(?s)powershell\\\\.exe/ "
                   "nocase or $udm.principal.process.file.full_path = /(?s)powershell\\\\.exe/ nocase or "
                   "$udm.target.process.parent_process.file.full_path = /(?s)powershell\\\\.exe/ nocase or "
                   "$udm.principal.process.parent_process.file.full_path = /(?s)powershell\\\\.exe/ nocase condition: "
                   "$udm}', 'startTime': '2022-07-15T08:22:27.039Z', 'endTime': '2022-07-15T08:27:27.039Z'}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_http_network_matches_operator(self):
        stix_pattern = "[network-traffic:extensions.'http-ext'.user_agent MATCHES '.\\\\w{5}/\\\\w{3}\\\\d\\\\d.']"
        query = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'ruleText': 'rule cp4s_gcp_udi_rule_1657895850 { meta: author = \"ibm cp4s user\" description = "
                   "\"Create event rule that should generate detections\" events: $udm.network.http.user_agent = /("
                   "?s).\\\\w{5}\\\\/\\\\w{3}\\\\d\\\\d./ nocase condition: "
                   "$udm}', 'startTime': '2022-07-15T14:32:30.572Z', 'endTime': '2022-07-15T14:37:30.572Z'}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_http_network_not_matches_operator(self):
        stix_pattern = "[network-traffic:extensions.'http-ext'.request_method NOT MATCHES " \
                       "'v1.compute.instances.setMetadata'] "
        query = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'ruleText': 'rule cp4s_gcp_udi_rule_1659625111 { meta: author = \"ibm cp4s user\" description = "
                   "\"Create event rule that should generate detections\" events:  $udm.network.http.method != /("
                   "?s)v1.compute.instances.setMetadata/ nocase  and $udm.network.http.method != \"\"  condition: "
                   "$udm}', 'startTime': '2022-08-04T14:53:31.720Z', 'endTime': '2022-08-04T14:58:31.720Z'}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_format_timestamp_fields(self):
        stix_pattern = "[file:modified >= '2022-04-01T11:00:00.000Z']"
        query = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'ruleText': 'rule cp4s_gcp_udi_rule_1658994681 { meta: author = \"ibm cp4s user\" description = "
                   "\"Create event rule that should generate detections\" events: "
                   "$udm.src.file.last_modification_time.seconds >= 1648810800 or "
                   "$udm.target.file.last_modification_time.seconds >= 1648810800 or "
                   "$udm.src.process.file.last_modification_time.seconds >= 1648810800 or "
                   "$udm.target.process.file.last_modification_time.seconds >= 1648810800 or "
                   "$udm.principal.process.file.last_modification_time.seconds >= 1648810800 or "
                   "$udm.about.file.last_modification_time.seconds >= 1648810800 condition: $udm}', 'startTime': "
                   "'2022-07-28T07:46:21.331Z', 'endTime': '2022-07-28T07:51:21.331Z'}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_query_from_multiple_comparison_expressions_joined_by_OR(self):
        stix_pattern = "[ipv4-addr:value = '10.0.1.4' OR network-traffic:src_port = '52221']"
        query = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'ruleText': 'rule cp4s_gcp_udi_rule_1657883991 { meta: author = \"ibm cp4s user\" description = "
                   "\"Create event rule that should generate detections\" events: ($udm.src.port = 52221 or "
                   "$udm.principal.port = 52221) or (any $udm.src.ip = \"10.0.1.4\" nocase or any $udm.target.ip = "
                   "\"10.0.1.4\" nocase or any $udm.principal.ip = \"10.0.1.4\" nocase) condition: $udm}', "
                   "'startTime': '2022-07-15T11:14:51.186Z', 'endTime': '2022-07-15T11:19:51.186Z'}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_query_for_morethan_two_comparison_expressions_joined_by_OR(self):
        stix_pattern = "[x-ibm-finding:name = 'user_change_password' OR file:hashes.'SHA-1' = " \
                       "'6cbce4a295c163791b60fc23d285e6d84f28ee4c' OR process:name = 'powershell.exe'] "
        query = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'ruleText': 'rule cp4s_gcp_udi_rule_1660217055 { meta: author = \"ibm cp4s user\" description "
                   "= \"Create event rule that should generate detections\" events: ($udm.src.process.file.full_path "
                   "= /(?s)powershell\\\\.exe/ nocase or $udm.target.process.file.full_path = /(?s)powershell\\\\.exe/ "
                   "nocase or $udm.principal.process.file.full_path = /(?s)powershell\\\\.exe/ nocase or "
                   "$udm.target.process.parent_process.file.full_path = /(?s)powershell\\\\.exe/ nocase or "
                   "$udm.principal.process.parent_process.file.full_path = /(?s)powershell\\\\.exe/ nocase) or (("
                   "$udm.src.file.sha1 = \"6cbce4a295c163791b60fc23d285e6d84f28ee4c\" nocase or $udm.target.file.sha1 "
                   "= \"6cbce4a295c163791b60fc23d285e6d84f28ee4c\" nocase or $udm.src.process.file.sha1 = "
                   "\"6cbce4a295c163791b60fc23d285e6d84f28ee4c\" nocase or $udm.target.process.file.sha1 = "
                   "\"6cbce4a295c163791b60fc23d285e6d84f28ee4c\" nocase or $udm.principal.process.file.sha1 = "
                   "\"6cbce4a295c163791b60fc23d285e6d84f28ee4c\" nocase or $udm.about.file.sha1 = "
                   "\"6cbce4a295c163791b60fc23d285e6d84f28ee4c\" nocase) or any $udm.security_result.summary = "
                   "\"user_change_password\" nocase) condition: $udm}', 'startTime': '2022-08-11T11:19:15.254Z', "
                   "'endTime': '2022-08-11T11:24:15.254Z'}"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_observation_with_and_without_qualifier_query(self):
        stix_pattern = "[process:command_line != '/usr/sbin/freeradius -f']START t'2022-04-01T00:00:00.030Z' STOP " \
                       "t'2022-04-07T00:00:00.030Z' AND [file:size >10 OR network-traffic:src_port <= 52221] "
        query = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'ruleText': 'rule cp4s_gcp_udi_rule_1659678676 { meta: author = \"ibm cp4s user\" description = "
                   "\"Create event rule that should generate detections\" events: ( $udm.src.process.command_line != "
                   "\"/usr/sbin/freeradius -f\" nocase  and $udm.src.process.command_line != \"\" ) or ( "
                   "$udm.target.process.command_line != \"/usr/sbin/freeradius -f\" nocase  and "
                   "$udm.target.process.command_line != \"\" ) or ( $udm.principal.process.command_line != "
                   "\"/usr/sbin/freeradius -f\" nocase  and $udm.principal.process.command_line != \"\" ) or ( "
                   "$udm.target.process.parent_process.command_line != \"/usr/sbin/freeradius -f\" nocase  and "
                   "$udm.target.process.parent_process.command_line != \"\" ) or ( "
                   "$udm.principal.process.parent_process.command_line != \"/usr/sbin/freeradius -f\" nocase  and "
                   "$udm.principal.process.parent_process.command_line != \"\" ) condition: $udm}', 'startTime': "
                   "'2022-04-01T00:00:00.030Z', 'endTime': '2022-04-07T00:00:00.030Z'}", "{'ruleText': 'rule "
                   "cp4s_gcp_udi_rule_1659678676 { meta: author = \"ibm cp4s user\" description = \"Create event "
                   "rule that should generate detections\" events: (( $udm.src.port <= 52221  and $udm.src.port != 0 ) "
                   "or ( $udm.principal.port <= 52221  and $udm.principal.port != 0 )) or ($udm.src.file.size > 10 "
                   "or $udm.target.file.size > 10 or $udm.src.process.file.size > 10 or $udm.target.process.file.size "
                   "> 10 or $udm.principal.process.file.size > 10 or $udm.about.file.size > 10) condition: $udm}', "
                   "'startTime': '2022-08-05T05:46:16.557Z', 'endTime': '2022-08-05T05:51:16.557Z'}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_combined_observation_AND(self):
        stix_pattern = "[ipv4-addr:value = '10.0.1.4' AND network-traffic:src_port = '52221'] AND " \
                       "[network-traffic:extensions.'http-ext'.user_agent = " \
                       "'v1.compute.instances.setMetadata' AND process:command_line != '/usr/sbin/freeradius " \
                       "-f'] START t'2022-04-01T11:00:00.000Z' STOP t'2022-04-07T11:00:00.003Z'"
        query = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'ruleText': 'rule cp4s_gcp_udi_rule_1659679133 { meta: author = \"ibm cp4s user\" description = "
                   "\"Create event rule that should generate detections\" events: ($udm.src.port = 52221 or "
                   "$udm.principal.port = 52221) and (any $udm.src.ip = \"10.0.1.4\" nocase or any $udm.target.ip = "
                   "\"10.0.1.4\" nocase or any $udm.principal.ip = \"10.0.1.4\" nocase) condition: $udm}', "
                   "'startTime': '2022-08-05T05:53:53.500Z', 'endTime': '2022-08-05T05:58:53.500Z'}", "{'ruleText': "
                   "'rule cp4s_gcp_udi_rule_1659679133 { meta: author = \"ibm cp4s user\" description = \"Create "
                   "event rule that should generate detections\" events: (( $udm.src.process.command_line != "
                   "\"/usr/sbin/freeradius -f\" nocase  and $udm.src.process.command_line != \"\" ) or "
                   "( $udm.target.process.command_line != \"/usr/sbin/freeradius -f\" nocase  and "
                   "$udm.target.process.command_line != \"\" ) or ( $udm.principal.process.command_line != "
                   "\"/usr/sbin/freeradius -f\" nocase  and $udm.principal.process.command_line != \"\" ) or "
                   "( $udm.target.process.parent_process.command_line != \"/usr/sbin/freeradius -f\" nocase  and "
                   "$udm.target.process.parent_process.command_line != \"\" ) or ( $udm.principal.process."
                   "parent_process.command_line != \"/usr/sbin/freeradius -f\" nocase  and $udm.principal.process."
                   "parent_process.command_line != \"\" )) and $udm.network.http.user_agent = \"v1.compute.instances."
                   "setMetadata\" nocase condition: $udm}', 'startTime': '2022-04-01T11:00:00.000Z', "
                   "'endTime': '2022-04-07T11:00:00.003Z'}"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_combined_observation_OR(self):
        stix_pattern = "[file:hashes.'SHA-1' = '6cbce4a295c163791b60fc23d285e6d84f28ee4c' OR process:name = " \
                       "'powershell.exe'] OR [ipv4-addr:value = '10.0.1.4' OR network-traffic:src_port = " \
                       "'52221']START t'2022-05-10T11:00:00.000Z' STOP t'2022-05-15T11:00:00.003Z'"
        query = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'ruleText': 'rule cp4s_gcp_udi_rule_1659679530 { meta: author = \"ibm cp4s user\" description = "
                   "\"Create event rule that should generate detections\" events: ($udm.src.process.file.full_path = "
                   "/(?s)powershell\\\\.exe/ nocase or $udm.target.process.file.full_path = /(?s)powershell\\\\.exe/ "
                   "nocase or $udm.principal.process.file.full_path = /(?s)powershell\\\\.exe/ nocase or "
                   "$udm.target.process.parent_process.file.full_path = /(?s)powershell\\\\.exe/ nocase or "
                   "$udm.principal.process.parent_process.file.full_path = /(?s)powershell\\\\.exe/ nocase) or ("
                   "$udm.src.file.sha1 = \"6cbce4a295c163791b60fc23d285e6d84f28ee4c\" nocase or $udm.target.file.sha1 "
                   "= \"6cbce4a295c163791b60fc23d285e6d84f28ee4c\" nocase or $udm.src.process.file.sha1 = "
                   "\"6cbce4a295c163791b60fc23d285e6d84f28ee4c\" nocase or $udm.target.process.file.sha1 = "
                   "\"6cbce4a295c163791b60fc23d285e6d84f28ee4c\" nocase or $udm.principal.process.file.sha1 = "
                   "\"6cbce4a295c163791b60fc23d285e6d84f28ee4c\" nocase or $udm.about.file.sha1 = "
                   "\"6cbce4a295c163791b60fc23d285e6d84f28ee4c\" nocase) condition: $udm}', 'startTime': "
                   "'2022-08-05T06:00:30.958Z', 'endTime': '2022-08-05T06:05:30.958Z'}", "{'ruleText': 'rule "
                   "cp4s_gcp_udi_rule_1659679530 { meta: author = \"ibm cp4s user\" description = \"Create event "
                   "rule that should generate detections\" events: ($udm.src.port = 52221 or $udm.principal.port = "
                   "52221) or (any $udm.src.ip = \"10.0.1.4\" nocase or any $udm.target.ip = \"10.0.1.4\" nocase or "
                   "any $udm.principal.ip = \"10.0.1.4\" nocase) condition: $udm}', 'startTime': "
                   "'2022-05-10T11:00:00.000Z', 'endTime': '2022-05-15T11:00:00.003Z'}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_integer_field_with_invalid_operator(self):
        stix_pattern = "[network-traffic:dst_port LIKE '53996']"
        result = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert 'LIKE operator is not supported for int type input' in result['error']

    def test_invalid_value_for_matches_operator(self):
        stix_pattern = "[network-traffic:src_port MATCHES '52221']"
        result = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert 'MATCHES operator is not supported for int type input' in result['error']

    def test_integer_field_with_invalid_string_input(self):
        stix_pattern = "[network-traffic:dst_port = 'TCP']"
        result = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert 'string type input - TCP is not supported for integer type fields' in result['error']

    def test_unsupported_enum_value_with_equal(self):
        stix_pattern = "[network-traffic:protocols[*] = 'tc']"
        result = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert "Unsupported ENUM values provided. Possible supported enum values are ['UNKNOWN_IP_PROTOCOL', 'EIGRP', "\
               "'ESP', 'ETHERIP', 'GRE', 'ICMP', 'IGMP', 'IP6IN4', 'PIM', 'TCP', 'UDP', 'VRRP', " \
               "'UNKNOWN_APPLICATION_PROTOCOL', 'AFP', 'APPC', 'AMQP', 'ATOM', 'BEEP', 'BITCOIN', 'BIT_TORRENT', " \
               "'CFDP', 'COAP', 'DDS', 'DEVICE_NET', 'DHCP', 'DNS', 'E_DONKEY', 'ENRP', 'FAST_TRACK', 'FINGER', " \
               "'FREENET', 'FTAM', 'GOPHER', 'HL7', 'H323', 'HTTP', 'HTTPS', 'IRCP', 'KADEMLIA', 'LDAP', 'LPD', " \
               "'MIME', 'MODBUS', 'MQTT', 'NETCONF', 'NFS', 'NIS', 'NNTP', 'NTCIP', 'NTP', 'OSCAR', 'PNRP', 'QUIC', " \
               "'RDP', 'RELP', 'RIP', 'RLOGIN', 'RPC', 'RTMP', 'RTP', 'RTPS', 'RTSP', 'SAP', 'SDP', 'SIP', 'SLP', " \
               "'SMB', 'SMTP', 'SNTP', 'SSH', 'SSMS', 'STYX', 'TCAP', 'TDS', 'TOR', 'TSP', 'VTP', 'WHOIS', 'WEB_DAV', "\
               "'X400', 'X500', 'XMPP']" in result['error']

    def test_unsupported_enum_value_with_in(self):
        stix_pattern = "[network-traffic:protocols[*] IN ('tc','ud')]"
        result = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert "Unsupported ENUM values provided. Possible supported enum values are ['UNKNOWN_IP_PROTOCOL', 'EIGRP', "\
               "'ESP', 'ETHERIP', 'GRE', 'ICMP', 'IGMP', 'IP6IN4', 'PIM', 'TCP', 'UDP', 'VRRP', " \
               "'UNKNOWN_APPLICATION_PROTOCOL', 'AFP', 'APPC', 'AMQP', 'ATOM', 'BEEP', 'BITCOIN', 'BIT_TORRENT', " \
               "'CFDP', 'COAP', 'DDS', 'DEVICE_NET', 'DHCP', 'DNS', 'E_DONKEY', 'ENRP', 'FAST_TRACK', 'FINGER', " \
               "'FREENET', 'FTAM', 'GOPHER', 'HL7', 'H323', 'HTTP', 'HTTPS', 'IRCP', 'KADEMLIA', 'LDAP', 'LPD', " \
               "'MIME', 'MODBUS', 'MQTT', 'NETCONF', 'NFS', 'NIS', 'NNTP', 'NTCIP', 'NTP', 'OSCAR', 'PNRP', 'QUIC', " \
               "'RDP', 'RELP', 'RIP', 'RLOGIN', 'RPC', 'RTMP', 'RTP', 'RTPS', 'RTSP', 'SAP', 'SDP', 'SIP', 'SLP', " \
               "'SMB', 'SMTP', 'SNTP', 'SSH', 'SSMS', 'STYX', 'TCAP', 'TDS', 'TOR', 'TSP', 'VTP', 'WHOIS', 'WEB_DAV', "\
               "'X400', 'X500', 'XMPP']" in result['error']

    def test_unsupported_enum_operator(self):
        stix_pattern = "[network-traffic:protocols[*] > 'TCP']"
        result = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert '> operator is not supported for Enum type input. Possible supported operator are ' \
               '[ =, !=, IN, NOT IN ]' in result['error']

    def test_invalid_stix_pattern(self):
        stix_pattern = "[not_a_valid_pattern]"
        result = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern, {'validate_pattern': 'true'})
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_STIX_VALIDATION.value == result['code']
        assert stix_pattern[1:-1] in result['error']

    def test_invalid_mac_address(self):
        stix_pattern = "[mac-addr:value = '00:00:00']"
        result = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert 'Invalid mac address' in result['error']

    def test_invalid_operator_for_string_input(self):
        stix_pattern = "[process:name < 'powershell.exe']"
        result = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert 'operator is not supported for string type input' in result['error']

    def test_invalid_qualifier(self):
        stix_pattern = "[file:size >10]START t'2021-11-28T00:00:00.000000Z' STOP " \
                       "t'2021-10-27T00:00:00.000000Z' "
        result = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert "translation_error" == result['code']
        assert 'Start time should be lesser than Stop time' in result['error']

    def test_invalid_email_address(self):
        stix_pattern = "[email-addr:value = 'Administrator_gmail.com']"
        result = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert 'Invalid email address' in result['error']

    def test_invalid_value_for_timestamp_field(self):
        stix_pattern = "[file:modified >= '2022-04-0111:00:00.000Z']"
        result = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert 'cannot convert the timestamp' in result['error']

    def test_query_for_multiple_observation(self):
        stix_pattern = "[file:hashes.'SHA-1' = '6cbce4a295c163791b60fc23d285e6d84f28ee4c'] OR [file:size >10 OR " \
                       "network-traffic:src_port <= 52221] AND [process:command_line ='\"MsMpEng.exe\"']START " \
                       "t'2022-05-01T00:00:00.030Z' STOP t'2022-05-05T00:00:00.030Z' OR [ipv4-addr:value = " \
                       "'168.149.184.42']START t'2022-05-01T00:00:00Z' STOP t'2022-05-10T00:00:00.030Z' "
        query = translation.translate('gcp_chronicle', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'ruleText': 'rule cp4s_gcp_udi_rule_1659680259 { meta: author = \"ibm cp4s user\" description = "
                   "\"Create event rule that should generate detections\" events: ($udm.src.file.sha1 = "
                   "\"6cbce4a295c163791b60fc23d285e6d84f28ee4c\" nocase or $udm.target.file.sha1 = "
                   "\"6cbce4a295c163791b60fc23d285e6d84f28ee4c\" nocase or $udm.src.process.file.sha1 = "
                   "\"6cbce4a295c163791b60fc23d285e6d84f28ee4c\" nocase or $udm.target.process.file.sha1 = "
                   "\"6cbce4a295c163791b60fc23d285e6d84f28ee4c\" nocase or $udm.principal.process.file.sha1 = "
                   "\"6cbce4a295c163791b60fc23d285e6d84f28ee4c\" nocase or $udm.about.file.sha1 = "
                   "\"6cbce4a295c163791b60fc23d285e6d84f28ee4c\" nocase) or ((( $udm.src.port <= 52221  and "
                   "$udm.src.port != 0 ) or ( $udm.principal.port <= 52221  and $udm.principal.port != 0 )) or ("
                   "$udm.src.file.size > 10 or $udm.target.file.size > 10 or $udm.src.process.file.size > 10 or "
                   "$udm.target.process.file.size > 10 or $udm.principal.process.file.size > 10 or "
                   "$udm.about.file.size > 10)) condition: $udm}', 'startTime': '2022-08-05T06:12:39.734Z', "
                   "'endTime': '2022-08-05T06:17:39.734Z'}", "{'ruleText': 'rule cp4s_gcp_udi_rule_1659680259 { meta: "
                   "author = \"ibm cp4s user\" description = \"Create event rule that should generate detections\" "
                   "events: $udm.src.process.command_line = \"\\\\\"MsMpEng.exe\\\\\"\" nocase or $udm.target.process."
                   "command_line = \"\\\\\"MsMpEng.exe\\\\\"\" nocase or $udm.principal.process.command_line = "
                   "\"\\\\\"MsMpEng.exe\\\\\"\" nocase or $udm.target.process.parent_process.command_line = "
                   "\"\\\\\"MsMpEng.exe\\\\\"\" nocase or $udm.principal.process.parent_process.command_line = "
                   "\"\\\\\"MsMpEng.exe\\\\\"\" nocase condition: $udm}', 'startTime': '2022-05-01T00:00:00.030Z', "
                   "'endTime': '2022-05-05T00:00:00.030Z'}", "{'ruleText': 'rule cp4s_gcp_udi_rule_1659680259 "
                   "{ meta: author = \"ibm cp4s user\" description = \"Create event rule that should generate "
                   "detections\" events: any $udm.src.ip = \"168.149.184.42\" nocase or any $udm.target.ip = "
                   "\"168.149.184.42\" nocase or any $udm.principal.ip = \"168.149.184.42\" nocase condition: $udm}', "
                   "'startTime': '2022-05-01T00:00:00Z', 'endTime': '2022-05-10T00:00:00.030Z'}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)
