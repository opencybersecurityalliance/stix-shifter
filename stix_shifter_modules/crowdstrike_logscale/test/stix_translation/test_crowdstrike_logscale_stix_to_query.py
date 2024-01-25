from stix_shifter.stix_translation import stix_translation
import unittest

translation = stix_translation.StixTranslation()


def _remove_timestamp_from_query(queries):
    """
    remove the timestamp in the query
    : param: queries: list
    : return: queries: list
    """
    if isinstance(queries, list):
        for query in queries:
            del query['start']
            del query['end']
        return queries


class TestQueryTranslator(unittest.TestCase):
    """
    class to perform unittest case CrowdStrike LogScale translate query
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
        stix_pattern = "[ipv4-addr:value = '111.111.11.111']"
        query = translation.translate('crowdstrike_logscale', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'source': 'crowdstrikeedr', 'queryString': 'device.local_ip = \"111.111.11.111\" or '
                                                                'device.external_ip = \"111.111.11.111\" | tail(10000)',
                    'start': 1700213537397, 'end': 1700213837397}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_equals_operator_for_list_of_dict(self):
        stix_pattern = "[file:name = 'cmd.exe']"
        query = translation.translate('crowdstrike_logscale', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'source': 'crowdstrikeedr', 'queryString': '@rawstring = /\"behaviors\"\\s*:\\s*\\[.*\"filename\"'
                                                                '\\s*:\\s*\"cmd\\.exe\"/ | tail(10000)',
                    'start': 1700213537397, 'end': 1700213837397}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_not_equals_operator_for_list_of_dict_attribute(self):
        stix_pattern = "[file:name != 'cmd.exe']"
        query = translation.translate('crowdstrike_logscale', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'source': 'crowdstrikeedr', 'queryString': '@rawstring != /\"behaviors\"\\s*:\\s*\\[.*\"filename\"'
                                                                '\\s*:\\s*\"cmd\\.exe\"/ | tail(10000)',
                    'start': 1700213537397, 'end': 1700213837397}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_not_equals_operator(self):
        stix_pattern = "[x-oca-asset:hostname != 'EC2AMAZ']"
        query = translation.translate('crowdstrike_logscale', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'source': 'crowdstrikeedr', 'queryString': 'device.hostname != \"EC2AMAZ\" '
                                                                'and device.hostname = \"*\" | tail(10000)',
                    'start': 1700213537397, 'end': 1700213837397}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_gt_operator(self):
        stix_pattern = "[x-ibm-finding:severity > 50]"
        query = translation.translate('crowdstrike_logscale', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'source': 'crowdstrikeedr', 'queryString': 'max_severity > 50 | tail(10000)',
                    'start': 1700214399519, 'end': 1700214699519}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_not_less_than_operator(self):
        stix_pattern = "[x-ibm-finding:severity NOT < 50]"
        query = translation.translate('crowdstrike_logscale', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'source': 'crowdstrikeedr', 'queryString': 'not max_severity < 50 and max_severity = \"*\"'
                                                                ' | tail(10000)',
                    'start': 1700214399519, 'end': 1700214699519}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_in_operator_for_list_of_dict_field(self):
        stix_pattern = "[process:name IN ('mstsc.exe', 'test.exe')] START t'2023-11-04T16:43:26.000Z' " \
                       "STOP t'2023-11-12T00:43:26.003Z'"
        query = translation.translate('crowdstrike_logscale', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'source': 'crowdstrikeedr', 'queryString': '@rawstring = /"behaviors"\\s*:\\s*\\['
                                                                '.*"filename"\\s*:\\s*("mstsc\\.exe"|"test\\.exe")/ | '
                                                                'tail(10000)', 'start': 1699116206000,
                    'end': 1699749806003}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_in_operator(self):
        stix_pattern = "[x-ibm-finding:name IN ('123','456')]"
        query = translation.translate('crowdstrike_logscale', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'source': 'crowdstrikeedr', 'queryString': 'detection_id = \"123\" or detection_id = '
                                                                '\"456\" | tail(10000)', 'start': 1699116206000,
                    'end': 1699749806003}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_not_in_operator_for_list_of_dict_field(self):
        stix_pattern = "[process:name NOT IN ('mstsc.exe', 'test.exe')] START t'2023-11-04T16:43:26.000Z' " \
                       "STOP t'2023-11-12T00:43:26.003Z'"
        query = translation.translate('crowdstrike_logscale', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'source': 'crowdstrikeedr', 'queryString': 'not @rawstring = /\"behaviors\"\\s*:\\s*\\'
                                                                '[.*\"filename\"\\s*:\\s*(\"mstsc\\.exe\"|\"test\\.exe'
                                                                '\")/ | tail(10000)', 'start': 1699116206000,
                    'end': 1699749806003}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_not_in_operator(self):
        stix_pattern = "[ipv4-addr:value NOT IN ('1.1.1.1','2.2.2.2')]"
        query = translation.translate('crowdstrike_logscale', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'source': 'crowdstrikeedr',
                    'queryString': '((not device.local_ip = \"1.1.1.1\" and device.local_ip = \"*\") and '
                                   '(not device.local_ip = \"2.2.2.2\" and device.local_ip = \"*\")) or '
                                   '((not device.external_ip = \"1.1.1.1\" and device.external_ip = \"*\") '
                                   'and (not device.external_ip = \"2.2.2.2\" and device.external_ip = \"*\")) '
                                   '| tail(10000)', 'start': 1699116206000,
                    'end': 1699749806003}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_like_operator(self):
        stix_pattern = "[mac-addr:value LIKE '11-22-28-67%']"
        query = translation.translate('crowdstrike_logscale', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'source': 'crowdstrikeedr',
                    'queryString': 'device.mac_address = /11-22-28-67.*/i | tail(10000)',
                    'start': 1700215236531, 'end': 1700215536531}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_not_matches_operator(self):
        stix_pattern = "[x-oca-asset:device_id NOT MATCHES '^7adb1f5eb5164fde90279ab0a1600d49']"
        query = translation.translate('crowdstrike_logscale', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'source': 'crowdstrikeedr',
                    'queryString': 'not device.device_id = /^7adb1f5eb5164fde90279ab0a1600d49/i and '
                                   'device.device_id = \"*\" | tail(10000)',
                    'start': 1700215742090, 'end': 1700216042090}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_subset_operator(self):
        stix_pattern = "[ipv6-addr:value NOT ISSUBSET '1.2.3.4/30']"
        query = translation.translate('crowdstrike_logscale', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'source': 'crowdstrikeedr',
                    'queryString': 'device.local_ip =~ !cidr(subnet="1.2.3.4/30") | tail(10000)',
                    'start': 1700216196932, 'end': 1700216496932},
                   {'source': 'crowdstrikeedr',
                    'queryString': 'device.external_ip =~ !cidr(subnet="1.2.3.4/30") | tail(10000)',
                    'start': 1700216196932, 'end': 1700216496932}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_equals_for_array_attribute(self):
        stix_pattern = "[x-ibm-finding:x_behaviors_processed[*] = '123']"
        query = translation.translate('crowdstrike_logscale', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'source': 'crowdstrikeedr',
                    'queryString': 'array:contains(array=\"behaviors_processed[]\",value = '
                                   '\"123\") | tail(10000)',
                    'start': 1700216196932, 'end': 1700216496932}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_matches_operator_for_array_attribute(self):
        stix_pattern = "[ x-oca-asset:x_device_groups[*] MATCHES '97350feebe4541e8a615c0d3f18acdf3']"
        query = translation.translate('crowdstrike_logscale', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'source': 'crowdstrikeedr',
                    'queryString': 'array:regex(array=\"device.groups[]\",regex = \"97350feebe4541e8a615c0d3f18acdf3\"'
                                   ', flags=i) | tail(10000)',
                    'start': 1700216196932, 'end': 1700216496932}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_not_equals_operator_for_array_attribute(self):
        stix_pattern = "[ x-oca-asset:x_device_groups[*] != '97350feebe4541e8a615c0d3f18acdf3']"
        query = translation.translate('crowdstrike_logscale', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'source': 'crowdstrikeedr',
                    'queryString': '!array:contains(array=\"device.groups[]\",value = '
                                   '\"97350feebe4541e8a615c0d3f18acdf3\") | tail(10000)',
                    'start': 1700216196932, 'end': 1700216496932}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_not_like_operator_for_array_attribute(self):
        stix_pattern = "[ x-oca-asset:x_device_groups[*] NOT LIKE '97350feebe4541e8a615c0d3f18acdf3']"
        query = translation.translate('crowdstrike_logscale', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'source': 'crowdstrikeedr',
                    'queryString': 'not array:regex(array=\"device.groups[]\",regex = '
                                   '\"97350feebe4541e8a615c0d3f18acdf3\"'
                                   ', flags=i) | tail(10000)',
                    'start': 1700216196932, 'end': 1700216496932}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_combined_comparison_without_timestamp(self):
        stix_pattern = ("[(x-ibm-ttp-tagging:extensions.'mitre-attack-ext'.technique_name != 'test' OR "
                        "ipv4-addr:value = '11.111.111.111') AND (mac-addr:value = '11-11-11-11-1a-1b' OR "
                        "file:hashes.MD5 = '11111111114a00996a9f5aaf9c0db84b')]")
        query = translation.translate('crowdstrike_logscale', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'source': 'crowdstrikeedr',
                    'queryString': '((@rawstring = /\"behaviors\"\\s*:\\s*\\[.*\"parent_details\"\\s*:\\s*\\'
                                   '{.*\"parent_md5\"\\s*:\\s*\"11111111114a00996a9f5aaf9c0db84b\"/ or @rawstring '
                                   '= /\"behaviors\"\\s*:\\s*\\[.*\"md5\"\\s*:\\s*'
                                   '\"11111111114a00996a9f5aaf9c0db84b\"/) or device.mac_address = '
                                   '\"11-11-11-11-1a-1b\") and ((device.local_ip = \"11.111.111.111\" or '
                                   'device.external_ip = \"11.111.111.111\") or @rawstring != /\"behaviors\"\\s*:'
                                   '\\s*\\[.*\"technique\"\\s*:\\s*\"test\"/) | tail(10000)',
                    'start': 1700559682224, 'end': 1700559982224}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_observation_with_common_timestamp(self):
        stix_pattern = ("([x-crowdstrike-detection-behavior:severity IN (50,30)] OR [directory:path != "
                        "'\\\\Device\\\\HarddiskVolume1\\\\Windows\\\\System32\\\\cmd.exe']) START "
                        "t'2023-11-15T01:43:26Z' STOP t'2023-11-20T00:43:26Z'")
        query = translation.translate('crowdstrike_logscale', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{'source': 'crowdstrikeedr',
                    'queryString': '(@rawstring = /\"behaviors\"\\s*:\\s*\\[.*\"severity\"\\s*:\\s*(50|30)/) '
                                   'or (@rawstring != /\"behaviors\"\\s*:\\s*\\[.*\"filepath\"\\s*:\\s*\"\\\\\\\\'
                                   'Device\\\\\\\\HarddiskVolume1\\\\\\\\Windows\\\\\\\\System32\\\\\\\\cmd\\.exe\"/) '
                                   '| tail(10000)',
                    'start': 1700012606000, 'end': 1700441006000}]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_observation_with_different_timestamp(self):
        stix_pattern = ("[software:name = 'Windows'] START t'2023-11-15T01:43:26Z' STOP t'2023-11-20T00:43:26Z' "
                        "AND [software:x_minor_version = '0'] START t'2023-12-10T01:43:26Z' STOP "
                        "t'2023-12-17T00:43:26Z'")
        query = translation.translate('crowdstrike_logscale', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{
            'source': 'crowdstrikeedr',
            'queryString': 'device.platform_name = \"Windows\" | tail(10000)',
            "start": 1700012606000,
            "end": 1700441006000
        }, {
            'source': 'crowdstrikeedr',
            'queryString': 'device.minor_version = \"0\" | tail(10000)',
            "start": 1702172606000,
            "end": 1702172606000
        }]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_expression_with_filter_function_joined_by_and_operator(self):
        stix_pattern = ("[user-account:user_id = 'S-1-5-18' AND ipv4-addr:value ISSUBSET '1.2.3.4/32' AND "
                        "process:parent_ref.command_line = '\"C:\\\\Windows\\\\system32\\\\cmd.exe\" /d "
                        "/c C:\\\\Windows\\\\system32\\\\silcollector.cmd configure']START t'2023-12-10T01:43:26Z' "
                        "STOP t'2023-12-16T00:43:26Z'")
        query = translation.translate('crowdstrike_logscale', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{
            'source': 'crowdstrikeedr',
            'queryString': 'device.local_ip =~ cidr(subnet=\"1.2.3.4/32\") | @rawstring = '
                           '/\"behaviors\"\\s*:\\s*\\[.*\"parent_details\"\\s*:\\s*\\{.*\"parent_cmdline\"'
                           '\\s*:\\s*\"\\\\\"C:\\\\\\\\Windows\\\\\\\\system32\\\\\\\\cmd\\.exe\\\\\"\\ \\/d\\ '
                           '\\/c\\ C:\\\\\\\\Windows\\\\\\\\system32\\\\\\\\silcollector\\.cmd\\ configure\"/ '
                           'and (@rawstring = /\"behaviors\"\\s*:\\s*\\[.*\"user_id\"\\s*:\\s*\"S\\-1\\-5\\-18\"/) '
                           '| tail(10000)',
            'start': 1702172606000,
            'end': 1702687406000
        }, {
            'source': 'crowdstrikeedr',
            'queryString': 'device.external_ip =~ cidr(subnet=\"1.2.3.4/32\") | @rawstring = '
                           '/\"behaviors\"\\s*:\\s*\\[.*\"parent_details\"\\s*:\\s*\\{.*\"parent_cmdline\"'
                           '\\s*:\\s*\"\\\\\"C:\\\\\\\\Windows\\\\\\\\system32\\\\\\\\cmd\\.exe\\\\\"\\ \\/d\\ '
                           '\\/c\\ C:\\\\\\\\Windows\\\\\\\\system32\\\\\\\\silcollector\\.cmd\\ configure\"/ and '
                           '(@rawstring = /\"behaviors\"\\s*:\\s*\\[.*\"user_id\"\\s*:\\s*\"S\\-1\\-5\\-18\"/) '
                           '| tail(10000)',
            'start': 1702172606000,
            'end': 1702687406000
        }]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_expression_with_filter_function_joined_by_combination_of_or_and_operator(self):
        stix_pattern = ("[user-account:user_id = 'S-1-5-18' AND ipv4-addr:value ISSUBSET '1.2.3.4/32' AND "
                        "process:parent_ref.command_line = '\"C:\\\\Windows\\\\system32\\\\cmd.exe\" /d "
                        "/c C:\\\\Windows\\\\system32\\\\silcollector.cmd configure' OR x-ibm-finding:"
                        "x_behaviors_processed[*] NOT LIKE '123']START t'2023-12-10T01:43:26Z' "
                        "STOP t'2023-12-16T00:43:26Z'")
        query = translation.translate('crowdstrike_logscale', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{
            'source': 'crowdstrikeedr',
            'queryString': 'not array:regex(array=\"behaviors_processed[]\",regex = \"123\", flags=i) | tail(10000)',
            'start': 1702172606000,
            'end': 1702687406000
        },
            {
                'source': 'crowdstrikeedr',
                'queryString': 'device.local_ip =~ cidr(subnet=\"1.2.3.4/32\") | tail(10000)',
                'start': 1702172606000,
                'end': 1702687406000
            },
            {
                'source': 'crowdstrikeedr',
                'queryString': 'device.external_ip =~ cidr(subnet=\"1.2.3.4/32\") | tail(10000)',
                'start': 1702172606000,
                'end': 1702687406000
            },
            {
                'source': 'crowdstrikeedr',
                'queryString': '(@rawstring = /\"behaviors\"\\s*:\\s*\\[.*\"parent_details\"\\s*:\\s*\\'
                               '{.*\"parent_cmdline\"\\s*:\\s*\"\\\\\"C:\\\\\\\\Windows\\\\\\\\system32\\\\\\\\cmd\\.'
                               'exe\\\\\"\\ \\/d\\ \\/c\\ C:\\\\\\\\Windows\\\\\\\\system32\\\\\\\\silcollector\\.'
                               'cmd\\ configure\"/ and (@rawstring = /\"behaviors\"\\s*:\\s*\\[.*\"user_id\"\\s*:\\'
                               's*\"S\\-1\\-5\\-18\"/)) | tail(10000)',
                'start': 1702172606000,
                'end': 1702687406000
            }]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_filter_functions_in_multiple_observation(self):

        stix_pattern = ("[user-account:user_id = 'S-1-5-18' AND ipv4-addr:value ISSUBSET '1.2.3.4/32' AND "
                        "process:parent_ref.command_line = '\"C:\\\\Windows\\\\system32\\\\cmd.exe\" /d /c "
                        "C:\\\\Windows\\\\system32\\\\silcollector.cmd configure'] START t'2023-12-10T01:43:26Z' "
                        "STOP t'2023-12-16T00:43:26Z' OR [x-ibm-finding:x_behaviors_processed LIKE "
                        "'pid:84f9f480747a43469228f876063b0ece:38864991970:41002' AND "
                        "x-oca-asset:hostname = 'EC2AMAZ']")
        query = translation.translate('crowdstrike_logscale', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{
            'source': 'crowdstrikeedr',
            'queryString': 'device.local_ip =~ cidr(subnet=\"1.2.3.4/32\") | @rawstring = '
                           '/\"behaviors\"\\s*:\\s*\\[.*\"parent_details\"\\s*:\\s*\\{.*\"parent_cmdline\"\\s*:'
                           '\\s*\"\\\\\"C:\\\\\\\\Windows\\\\\\\\system32\\\\\\\\cmd\\.exe\\\\\"\\ \\/d\\ \\/c\\ '
                           'C:\\\\\\\\Windows\\\\\\\\system32\\\\\\\\silcollector\\.cmd\\ configure\"/ and '
                           '(@rawstring = /\"behaviors\"\\s*:\\s*\\[.*\"user_id\"\\s*:\\s*\"S\\-1\\-5\\-18\"/) |'
                           ' tail(10000)',
            'start': 1702172606000,
            'end': 1702687406000
        },
            {
                'source': 'crowdstrikeedr',
                'queryString': 'device.external_ip =~ cidr(subnet=\"1.2.3.4/32\") | @rawstring = '
                               '/\"behaviors\"\\s*:'
                               '\\s*\\[.*\"parent_details\"\\s*:\\s*\\{.*\"parent_cmdline\"\\s*:\\s*\"\\\\\"C:\\\\\\\\'
                               'Windows\\\\\\\\system32\\\\\\\\cmd\\.exe\\\\\"\\ \\/d\\ \\/c\\ C:\\\\\\\\Windows'
                               '\\\\\\\\'
                               'system32\\\\\\\\silcollector\\.cmd\\ configure\"/ and (@rawstring = /\"behaviors\"\\s*:'
                               '\\s*\\[.*\"user_id\"\\s*:\\s*\"S\\-1\\-5\\-18\"/) | tail(10000)',
                'start': 1702172606000,
                'end': 1702687406000
            },
            {
                'source': 'crowdstrikeedr',
                'queryString': 'array:regex(array=\"behaviors_processed[]\",regex = '
                               '\"pid:84f9f480747a43469228f876063b0ece'
                               ':38864991970:41002\", flags=i) | tail(10000)',
                'start': 1702830883582,
                'end': 1702831183582
            },
            {
                'source': 'crowdstrikeedr',
                'queryString': 'device.hostname = \"EC2AMAZ\" | tail(10000)',
                'start': 1702830883582,
                'end': 1702831183582
            }]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_invalid_int_value(self):
        stix_pattern = "[software:version < 'fifty']"
        result = translation.translate('crowdstrike_logscale', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert "not_implemented" == result['code']
        assert 'ComparisonComparators.LessThan operator is not supported string type value: fifty' in result['error']

    def test_unsupported_like_field(self):
        stix_pattern = "[process:name LIKE 'test']"
        result = translation.translate('crowdstrike_logscale', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert "not_implemented" == result['code']
        assert 'ComparisonComparators.Like is not supported for list of dictionary fields' \
               in result['error']

    def test_invalid_timestamp_range(self):
        stix_pattern = "[file:name = 'mstsc.exe'] START t'2023-11-20T01:43:26.000Z' STOP t'2023-11-19T00:43:26.003Z'"
        result = translation.translate('crowdstrike_logscale', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert "translation_error" == result['code']
        assert 'Start time should be lesser than Stop time' in result['error']

    def test_invalid_operator_for_array_attribute(self):
        stix_pattern = "[x-ibm-finding:x_behaviors_processed[*] IN ('123')]"
        result = translation.translate('crowdstrike_logscale', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert "not_implemented" == result['code']
        assert 'ComparisonComparators.In is not supported for array attribute' in result['error']
