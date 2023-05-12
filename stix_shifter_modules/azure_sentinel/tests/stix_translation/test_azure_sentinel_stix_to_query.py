from stix_shifter.stix_translation import stix_translation
import unittest
import re
import json
translation = stix_translation.StixTranslation()


def _remove_timestamp_from_query(queries):
    pattern_alert = r'eventDateTime \w{2} \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z'
    pattern_alertV2 = r'createdDateTime \w{2} \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z'
    query_list = []
    if isinstance(queries, list):
        for query in queries:
            if 'alert' in query:
                query_list.append(re.sub(pattern_alert, "", query['alert']))
            else:
                query_list.append(re.sub(pattern_alertV2, "", query['alertV2']))

    return query_list


class TestQueryTranslator(unittest.TestCase):
    """
    class to perform unit test case azure_sentinel translate query
    """

    def _test_query_assertions(self, query, queries):
        """
        to assert the each query in the list against expected result
        """
        self.assertIsInstance(query, dict)
        self.assertIsInstance(query['queries'], list)
        for index, each_query in enumerate(query.get('queries'), start=0):
            self.assertEqual(each_query, queries[index])

    def test_file_comp_exp(self):
        stix_pattern = "[file:name = 'services.exe']"
        query = translation.translate('azure_sentinel', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            {
                "alert": "(fileStates/any(query1:tolower(query1/name) eq 'services.exe')) and (eventDateTime ge 2023-04-26T14:05:28.029Z and eventDateTime le 2023-04-26T14:10:28.029Z)"
            }
        ]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_process_comp_exp(self):
        stix_pattern = "[process:name = 'svchost.exe']"
        query = translation.translate('azure_sentinel', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            {
                "alert": "((processes/any(query1:tolower(query1/name) eq 'svchost.exe') or processes/any(query1:tolower(query1/parentProcessName) eq 'svchost.exe'))) and (eventDateTime ge 2023-04-26T14:32:57.319Z and eventDateTime le 2023-04-26T14:37:57.319Z)"
            }
        ]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_ipaddr_comp_exp(self):
        stix_pattern = "[ipv4-addr:value = '172.16.2.22'] START t'2019-09-10T08:43:10.003Z' STOP " \
                       "t'2019-09-23T10:43:10.453Z'"
        query = translation.translate('azure_sentinel', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            {
                "alert": "((networkConnections/any(query1:contains(tolower(query1/sourceAddress), '172.16.2.22')) or "
                "networkConnections/any(query1:contains(tolower(query1/destinationAddress), '172.16.2.22')) or "
                "networkConnections/any(query1:tolower(query1/natSourceAddress) eq '172.16.2.22') or "
                "networkConnections/any(query1:tolower(query1/natDestinationAddress) eq '172.16.2.22'))) and "
                "(eventDateTime ge 2019-09-10T08:43:10.003Z and eventDateTime le 2019-09-23T10:43:10.453Z)"
            }
        ]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_file_directory_exp(self):
        stix_pattern = "[file:parent_directory_ref.path = 'system32']" \
                       "START t'2019-10-01T08:43:10.003Z' STOP t'2019-10-30T10:43:10.003Z'"
        query = translation.translate('azure_sentinel', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            {
                "alert": "(fileStates/any(query1:contains(tolower(query1/path), 'system32'))) and (eventDateTime ge 2019-10-01T08:43:10.003Z and eventDateTime le 2019-10-30T10:43:10.003Z)"
            }
        ]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_directory_path_exp(self):
        stix_pattern = "[directory:path = 'windows']"
        query = translation.translate('azure_sentinel', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            {
                "alert": "((fileStates/any(query1:contains(tolower(query1/path), 'windows')) or process/any(query1:tolower(query1/path) eq 'windows'))) and (eventDateTime ge 2023-04-26T14:39:07.023Z and eventDateTime le 2023-04-26T14:44:07.023Z)"
            }
        ]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_noteq_comp_exp(self):
        stix_pattern = "[process:name != 'services.exe'] START t'2019-09-10T08:43:10.003Z' STOP " \
                       "t'2019-09-23T10:43:10.453Z'"
        query = translation.translate('azure_sentinel', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            {
                "alert": "((processes/any(query1:tolower(query1/name) ne 'services.exe') or processes/any(query1:tolower(query1/parentProcessName) ne 'services.exe'))) and (eventDateTime ge 2019-09-10T08:43:10.003Z and eventDateTime le 2019-09-23T10:43:10.453Z)"
            }
        ]
        queries = _remove_timestamp_from_query(queries)

        self._test_query_assertions(query, queries)

    def test_like_comp_exp(self):
        stix_pattern = "[file:name LIKE 'svc']"
        query = translation.translate('azure_sentinel', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            {
                "alert": "(fileStates/any(query1:contains(tolower(query1/name), 'svc'))) and (eventDateTime ge 2023-04-26T14:40:18.624Z and eventDateTime le 2023-04-26T14:45:18.624Z)"
            }
        ]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_matches_comp_exp(self):
        stix_pattern = "[file:name MATCHES 'serv']"
        query = translation.translate('azure_sentinel', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            {
                "alert": "(fileStates/any(query1:contains(tolower(query1/name), 'serv'))) and (eventDateTime ge 2023-04-26T14:40:47.144Z and eventDateTime le 2023-04-26T14:45:47.144Z)"
            }
        ]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_custom_in_comp_exp(self):
        stix_pattern = "[x-msazure-sentinel:tenant_id NOT IN ('Sb73e5ba','b73e5ba8')" \
                       "AND x-ibm-finding:name LIKE 'Suspicious']"
        query = translation.translate('azure_sentinel', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            {
                "alert": "(contains(tolower(title), 'Suspicious') and tolower(azureTenantId) ne 'Sb73e5ba' and tolower(azureTenantId) ne 'b73e5ba8') and (eventDateTime ge 2023-04-26T14:41:33.013Z and eventDateTime le 2023-04-26T14:46:33.013Z)"
            }
        ]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_in_comp_exp(self):
        stix_pattern = "[process:name IN ('services.exe', 'svchost.exe')]"
        query = translation.translate('azure_sentinel', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
        {
            "alert": "((processes/any(query1:tolower(query1/name) eq 'services.exe') or processes/any(query1:tolower(query1/name) eq "
            "'svchost.exe') or processes/any(query1:tolower(query1/parentProcessName) eq 'services.exe') or "
            "processes/any(query1:tolower(query1/parentProcessName) eq 'svchost.exe'))) and "
            "(eventDateTime ge 2023-04-26T14:43:07.619Z and eventDateTime le 2023-04-26T14:48:07.619Z)"
        }
    ]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_comb_comparison_exp_1(self):
        stix_pattern = "[process:name IN ('services.exe', 'svchost.exe') OR file:name = 'notepad.exe'] START " \
                       "t'2019-09-10T08:43:10.003Z' STOP t'2019-09-23T10:43:10.453Z'"
        query = translation.translate('azure_sentinel', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            {
                "alert": "(fileStates/any(query1:tolower(query1/name) eq 'notepad.exe') or (processes/any(query2:tolower(query2/name) eq 'services.exe') or processes/any(query2:tolower(query2/name) eq 'svchost.exe') or processes/any(query2:tolower(query2/parentProcessName) eq 'services.exe') or processes/any(query2:tolower(query2/parentProcessName) eq 'svchost.exe'))) and (eventDateTime ge 2019-09-10T08:43:10.003Z and eventDateTime le 2019-09-23T10:43:10.453Z)"
            }
        ]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_comb_comparison_exp_2(self):
        stix_pattern = "[network-traffic:src_port = '454' OR process:name NOT = 'powershell.exe'] START " \
                       "t'2019-09-10T08:43:10.003Z' STOP t'2019-09-23T10:43:10.453Z'"
        query = translation.translate('azure_sentinel', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            {
                "alert": "((processes/any(query1:tolower(query1/name) ne 'powershell.exe') and processes/any(query1:tolower(query1/parentProcessName) ne 'powershell.exe')) or (networkConnections/any(query2:tolower(query2/sourcePort) eq '454') or networkConnections/any(query2:tolower(query2/natSourcePort) eq '454') or networkConnections/any(query2:tolower(query2/natDestinationPort) eq '454'))) and (eventDateTime ge 2019-09-10T08:43:10.003Z and eventDateTime le 2019-09-23T10:43:10.453Z)"
            }
        ]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_comb_observation_obs(self):
        stix_pattern = "[process:name = 'services.exe'] OR [network-traffic:dst_port >= 100]"
        query = translation.translate('azure_sentinel', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            {
                "alert": "((processes/any(query1:tolower(query1/name) eq 'services.exe') or processes/any(query1:tolower(query1/parentProcessName) eq 'services.exe'))) and (eventDateTime ge 2023-04-27T14:06:27.757Z and eventDateTime le 2023-04-27T14:11:27.757Z)"
            },
            {
                "alert": "((networkConnections/any(query2:tolower(query2/destinationPort) ge '100') or networkConnections/any(query2:tolower(query2/natDestinationPort) ge '100'))) and (eventDateTime ge 2023-04-27T14:06:27.757Z and eventDateTime le 2023-04-27T14:11:27.757Z)"
            }
        ]
        
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_comb_observation_obs_qualifier_one(self):
        stix_pattern = "([process:pid IN (110,220)] OR [network-traffic:src_ref.value = '52.94.233.129' AND " \
                       "user-account:account_last_login = '2019-09-23T10:43:10.453Z']) START " \
                       "t'2019-09-10T08:43:10.003Z' STOP t'2019-09-23T10:43:10.453Z'"
        query = translation.translate('azure_sentinel', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            {
                "alert": "((processes/any(query1:query1/processId eq 110) or processes/any(query1:query1/processId eq 220) or processes/any(query1:query1/parentProcessId eq 110) or processes/any(query1:query1/parentProcessId eq 220) or registryKeyStates/any(query1:query1/processId eq 110) or registryKeyStates/any(query1:query1/processId eq 220))) and (eventDateTime ge 2019-09-10T08:43:10.003Z and eventDateTime le 2019-09-23T10:43:10.453Z)"
            },
            {
                "alert": "(userStates/any(query2:query2/logonDateTime eq 2019-09-23T10:43:10.453Z) and networkConnections/any(query3:contains(tolower(query3/sourceAddress), '52.94.233.129'))) and (eventDateTime ge 2019-09-10T08:43:10.003Z and eventDateTime le 2019-09-23T10:43:10.453Z)"
            }
        ]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_comb_observation_obs_qualifier_two(self):
        stix_pattern = "[file:hashes.'SHA-1' LIKE 'daf67'] OR [file:hashes.'SHA-1' = 'b6d237154f2e528f0b503b58b025862d66b02b73'] " \
                        "OR [ipv4-addr:value = '1.1.1.1'] AND [ipv4-addr:value = '2.1.1.1'] START t'2019-09-10T08:43:10.003Z' " \
                        "STOP t'2019-09-23T10:43:10.453Z'"
        query = translation.translate('azure_sentinel', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries =  [
            {
                "alert": "((fileStates/any(query1:query1/fileHash/hashType eq 'sha1') and fileStates/any(query1:contains(tolower(query1/fileHash/hashValue), 'daf67')))) and (eventDateTime ge 2023-04-27T13:45:31.261Z and eventDateTime le 2023-04-27T13:50:31.261Z)"
            },
            {
                "alert": "((fileStates/any(query2:query2/fileHash/hashType eq 'sha1') and fileStates/any(query2:tolower(query2/fileHash/hashValue) eq 'b6d237154f2e528f0b503b58b025862d66b02b73'))) and (eventDateTime ge 2023-04-27T13:45:31.261Z and eventDateTime le 2023-04-27T13:50:31.261Z)"
            },
            {
                "alert": "((networkConnections/any(query3:contains(tolower(query3/sourceAddress), '1.1.1.1')) or networkConnections/any(query3:contains(tolower(query3/destinationAddress), '1.1.1.1')) or networkConnections/any(query3:tolower(query3/natSourceAddress) eq '1.1.1.1') or networkConnections/any(query3:tolower(query3/natDestinationAddress) eq '1.1.1.1'))) and (eventDateTime ge 2023-04-27T13:45:31.261Z and eventDateTime le 2023-04-27T13:50:31.261Z)"
            },
            {
                "alert": "((networkConnections/any(query4:contains(tolower(query4/sourceAddress), '2.1.1.1')) or networkConnections/any(query4:contains(tolower(query4/destinationAddress), '2.1.1.1')) or networkConnections/any(query4:tolower(query4/natSourceAddress) eq '2.1.1.1') or networkConnections/any(query4:tolower(query4/natDestinationAddress) eq '2.1.1.1'))) and (eventDateTime ge 2019-09-10T08:43:10.003Z and eventDateTime le 2019-09-23T10:43:10.453Z)"
            }
        ]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_x_ibm_finding(self):
        stix_pattern = "[x-ibm-finding:name = 'photos'] AND [x-ibm-finding:finding_type = 'test type'] " \
                       "AND [x-ibm-finding:description = 'test description'] AND " \
                       "[x-ibm-finding:severity = 'test severity'] AND " \
                       "[x-ibm-finding:src_geolocation = 'canada'] AND" \
                       "[x-ibm-finding:dst_geolocation = 'us']"
        query = translation.translate('azure_sentinel', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            {
                "alert": "(tolower(title) eq 'photos') and (eventDateTime ge 2023-04-27T13:49:25.393Z and eventDateTime le 2023-04-27T13:54:25.393Z)"
            },
            {
                "alert": "(tolower(category) eq 'test type') and (eventDateTime ge 2023-04-27T13:49:25.393Z and eventDateTime le 2023-04-27T13:54:25.393Z)"
            },
            {
                "alert": "(tolower(description) eq 'test description') and (eventDateTime ge 2023-04-27T13:49:25.393Z and eventDateTime le 2023-04-27T13:54:25.393Z)"
            },
            {
                "alert": "(tolower(severity) eq 'test severity') and (eventDateTime ge 2023-04-27T13:49:25.393Z and eventDateTime le 2023-04-27T13:54:25.393Z)"
            },
            {
                "alert": "(networkConnections/any(query5:tolower(query5/sourceLocation) eq 'canada')) and (eventDateTime ge 2023-04-27T13:49:25.393Z and eventDateTime le 2023-04-27T13:54:25.393Z)"
            },
            {
                "alert": "(networkConnections/any(query6:tolower(query6/destinationLocation) eq 'us')) and (eventDateTime ge 2023-04-27T13:49:25.393Z and eventDateTime le 2023-04-27T13:54:25.393Z)"
            },
            {
                "alertV2": "(tolower(severity) eq 'test severity') and (createdDateTime ge 2023-04-27T18:54:53.833Z and createdDateTime le 2023-04-27T18:59:53.833Z)"
            }
        ]
        queries = _remove_timestamp_from_query(queries)
        self.assertSetEqual(set(query['queries']), set(queries))
    
    def test_lamda_operator_with_collection(self):
        stix_pattern = "[x-ibm-finding:x_recommendedActions = 'Enforce' OR x-ibm-finding:x_detectionIds != '111']"
        query = translation.translate('azure_sentinel', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [{
                "alert": "(NOT(detectionIds/any(query1:query1 eq '111')) or recommendedActions/any(query2:query2 eq 'Enforce')) and "
                "(eventDateTime ge 2023-04-27T13:47:00.039Z and eventDateTime le 2023-04-27T13:52:00.039Z)"
            }
        ]
        
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)
