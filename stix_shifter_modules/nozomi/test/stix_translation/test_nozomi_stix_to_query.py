from stix_shifter.stix_translation import stix_translation
import unittest
import re

translation = stix_translation.StixTranslation()


def _remove_timestamp_from_query(queries):
    pattern = r'\|\s*\bwhere\s*record_created_at\s*[><]=\s*\d+\b\s*'
    if isinstance(queries, list):
        return [re.sub(pattern, '', str(query)) for query in queries]
    elif isinstance(queries, str):
        return re.sub(pattern, '', queries)


class TestQueryTranslator(unittest.TestCase):
    """
    class to perform unit test case nozomi translate query
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

    def test_equal_operator(self):
        stix_pattern = "[ipv4-addr:value = '111.11.1.111'] START t'2023-11-01T11:00:00.000Z' " \
                       "STOP t'2023-12-06T11:54:00.000Z'"
        query = translation.translate('nozomi', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["query=alerts | where ip_dst==\"111.11.1.111\" | where record_created_at>=1698836400000 | "
                   "where record_created_at<=1701863640000"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_not_equal_operator(self):
        stix_pattern = "[ipv6-addr:value != '1234:a5a6:78910:1111:2222:3333'] START t'2023-11-01T11:00:00.000Z' " \
                       "STOP t'2023-12-06T11:54:00.000Z'"
        query = translation.translate('nozomi', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["query=alerts | where ip_dst!=\"1234:a5a6:78910:1111:2222:3333\" | where "
                   "record_created_at>=1698836400000 | where record_created_at<=1701863640000"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_gt_operator(self):
        stix_pattern = "[network-traffic:dst_port > 22] START t'2023-11-01T11:00:00.000Z' " \
                       "STOP t'2023-12-06T11:54:00.000Z'"
        query = translation.translate('nozomi', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["query=alerts | where port_dst>\"22\" | where record_created_at>=1698836400000 | where "
                   "record_created_at<=1701863640000"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_gt_eq_operator(self):
        stix_pattern = "[network-traffic:dst_port >= 22] START t'2023-11-01T11:00:00.000Z' " \
                       "STOP t'2023-12-06T11:54:00.000Z'"
        query = translation.translate('nozomi', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["query=alerts | where port_dst>=\"22\" | where record_created_at>=1698836400000 | where "
                   "record_created_at<=1701863640000"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_lt_operator(self):
        stix_pattern = "[network-traffic:src_port < 22] START t'2023-11-01T11:00:00.000Z' " \
                       "STOP t'2023-12-06T11:54:00.000Z'"
        query = translation.translate('nozomi', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["query=alerts | where port_src<\"22\" | where record_created_at>=1698836400000 | where "
                   "record_created_at<=1701863640000"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_lt_eq_operator(self):
        stix_pattern = "[network-traffic:src_port <= 22] START t'2023-11-01T11:00:00.000Z' " \
                       "STOP t'2023-12-06T11:54:00.000Z'"
        query = translation.translate('nozomi', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["query=alerts | where port_src<=\"22\" | where record_created_at>=1698836400000 | where "
                   "record_created_at<=1701863640000"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_IN_operator(self):
        stix_pattern = "[network-traffic:protocols[*] IN ('TCP','GTP')] START t'2023-11-01T11:00:00.000Z' " \
                       "STOP t'2023-12-06T11:54:00.000Z'"
        query = translation.translate('nozomi', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["query=alerts | where protocol in? [\"TCP\", \"GTP\"] OR transport_protocol in? [\"TCP\", \"GTP\"] |"
                   "where record_created_at>=1698836400000 | where record_created_at<=1701863640000"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_LIKE_operator(self):
        stix_pattern = "[mac-addr:value LIKE '01:01:01:01:01:01'] START t'2023-11-01T11:00:00.000Z' " \
                       "STOP t'2023-12-06T11:54:00.000Z'"
        query = translation.translate('nozomi', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["query=alerts | where mac_src include? \"01:01:01:01:01:01\" OR mac_dst include? "
                   "\"01:01:01:01:01:01\" |"
                   "where record_created_at>=1698836400000 | where record_created_at<=1701863640000"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_ISSUBSET_operator(self):
        stix_pattern = "[ipv4-addr:value ISSUBSET '111.11.1.111/16'] START t'2023-11-01T11:00:00.000Z' " \
                       "STOP t'2023-12-06T11:54:00.000Z'"
        query = translation.translate('nozomi', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["query=alerts | where ip_dst in_subnet? \"111.11.1.111/16\" | where record_created_at>=1698836400000"
                   " | where record_created_at<=1701863640000"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_directory_path(self):
        stix_pattern = "[directory:path = 'C:\\\\Windows\\\\System32']START t'2023-12-01T00:00:00.000Z' STOP " \
                       "t'2024-01-01T11:00:00.000Z'"
        query = translation.translate('nozomi', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["query=alerts | where properties/process/image_path include? \"C:\\Windows\\System32\" | where "
                   "record_created_at>=1672538160000 | where record_created_at<=1704074220003"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_enum_operator(self):
        stix_pattern = "[x-ibm-finding:finding_type = 'alert'] START t'2023-11-01T11:00:00.000Z' " \
                       "STOP t'2023-12-06T11:54:00.000Z'"
        query = translation.translate('nozomi', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["query=alerts | where threat_name==\"\" | where record_created_at>=1698836400000 | "
                   "where record_created_at<=1701863640000"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_int_operator(self):
        stix_pattern = "[x-ibm-finding:severity = '90'] START t'2023-11-01T11:00:00.000Z' " \
                       "STOP t'2023-12-06T11:54:00.000Z'"
        query = translation.translate('nozomi', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["query=alerts | where risk==\"9.0\" | where record_created_at>=1698836400000 | "
                   "where record_created_at<=1701863640000"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_combined_comparison_AND_operator(self):
        stix_pattern = "[network-traffic:dst_port = '445' AND (process:pid = '1010' AND user-account:user_id LIKE " \
                       "'user@Hostname')]START " \
                       "t'2023-12-01T00:00:00.000Z' STOP t'2024-01-01T11:00:00.000Z'"
        query = translation.translate('nozomi', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['query=alerts | where properties/process/user include? '
                   '"user@Hostname" | where properties/process/pid=="1010" | '
                   'where port_dst=="445" ']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_combined_comparison_OR_operator(self):
        stix_pattern = "[process:pid = '1010' OR user-account:user_id LIKE 'user@Hostname']START " \
                       "t'2023-12-01T00:00:00.000Z' STOP t'2024-01-01T11:00:00.000Z'"
        query = translation.translate('nozomi', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [
            "query=alerts | where properties/process/pid==\"1010\" OR properties/process/user include? "
            "\"user@Hostname\" | where record_created_at>=1701388800000 | where record_created_at<=1704106800000"
        ]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_combined_comparison_OR_AND_operators(self):
        stix_pattern = "[(x-ibm-finding:severity = '90' OR x-ibm-ttp-tagging:name LIKE 'Non-Application Layer " \
                       "Protocol') AND (x-nozomi-info:label != 'ABCD' AND x-ibm-finding:x_solution " \
                       "= 'Verify the device configuration and status')] START t'2023-12-01T00:00:00.000Z' " \
                       "STOP t'2024-01-01T11:00:00.000Z'"
        query = translation.translate('nozomi', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [
            "query=alerts | where properties/solution==\"Verify the device configuration and status\" | where "
            "label_src!=\"ABCD\" OR label_dst!=\"ABCD\" | where risk==\"9.0\" OR properties include? "
            "\"Non-Application Layer Protocol\" | where record_created_at>=1701388800000 | where "
            "record_created_at<=1704106800000"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_combined_comparison(self):
        stix_pattern = "[x-nozomi-info:is_public = 'true' OR (x-alert-properties:x_cause != 'Rule-dependent. A " \
                       "suspicious local event has been detected on a machine.' AND x-nozomi-info:is_public = " \
                       "'false') OR (x-nozomi-info:label != 'ABCD' AND x-ibm-finding:x_solution = 'Verify the device " \
                       "configuration and status')]START t'2023-12-01T00:00:00.000Z' STOP t'2024-01-01T11:00:00.000Z'"
        query = translation.translate('nozomi', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [
            "query=alerts | where properties/is_dst_public==\"true\" OR properties/is_src_public==\"true\" OR "
            "properties/solution==\"Verify the device configuration and status\" | where "
            "properties/is_dst_public==\"true\" OR properties/is_src_public==\"true\" OR label_src!=\"ABCD\" OR "
            "label_dst!=\"ABCD\" | where record_created_at>=1701388800000 | where record_created_at<=1704106800000"
        ]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_IN_operator_split_query(self):
        stix_pattern = "[file:hashes.'SHA-256' IN ('ABDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A" \
                       "', 'a737742b81292c764ac2a7e419a37ed7fdf4a1ed'," \
                       "'BBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A', " \
                       "'b737742b81292c764ac2a7e419a37ed7fdf4a1ed'," \
                       "'CBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A'," \
                       "'c737742b81292c764ac2a7e419a37ed7fdf4a1ed'," \
                       "'DBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A'," \
                       "'d737742b81292c764ac2a7e419a37ed7fdf4a1ed'," \
                       "'EBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A'," \
                       "'e737742b81292c764ac2a7e419a37ed7fdf4a1ed'," \
                       "'FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A'," \
                       "'f737742b81292c764ac2a7e419a37ed7fdf4a1ed','g737742b81292c764ac2a7e419a37ed7fdf4a1ed'," \
                       "'h737742b81292c764ac2a7e419a37ed7fdf4a1ed','i737742b81292c764ac2a7e419a37ed7fdf4a1ed'," \
                       "'j737742b81292c764ac2a7e419a37ed7fdf4a1ed'," \
                       "'KBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A'," \
                       "'LBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A'," \
                       "'MBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A'," \
                       "'NBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A')] START " \
                       "t'2023-11-01T11:00:00.000Z' STOP t'2023-12-06T11:54:00.000Z'"
        query = translation.translate('nozomi', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['query=alerts | where properties/details_hash_SHA256/value in? ['
                   '"ABDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A", '
                   '"a737742b81292c764ac2a7e419a37ed7fdf4a1ed", '
                   '"BBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A", '
                   '"b737742b81292c764ac2a7e419a37ed7fdf4a1ed", '
                   '"CBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A", '
                   '"c737742b81292c764ac2a7e419a37ed7fdf4a1ed", '
                   '"DBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A", '
                   '"d737742b81292c764ac2a7e419a37ed7fdf4a1ed", '
                   '"EBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A", '
                   '"e737742b81292c764ac2a7e419a37ed7fdf4a1ed", '
                   '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A", '
                   '"f737742b81292c764ac2a7e419a37ed7fdf4a1ed", "g737742b81292c764ac2a7e419a37ed7fdf4a1ed", '
                   '"h737742b81292c764ac2a7e419a37ed7fdf4a1ed", "i737742b81292c764ac2a7e419a37ed7fdf4a1ed", '
                   '"j737742b81292c764ac2a7e419a37ed7fdf4a1ed", '
                   '"KBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A", '
                   '"LBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A", '
                   '"MBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A", '
                   '"NBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A"] ',
                   'query=alerts | where properties/process/image_hash_sha256 in? ['
                   '"ABDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A", '
                   '"a737742b81292c764ac2a7e419a37ed7fdf4a1ed", '
                   '"BBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A", '
                   '"b737742b81292c764ac2a7e419a37ed7fdf4a1ed", '
                   '"CBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A", '
                   '"c737742b81292c764ac2a7e419a37ed7fdf4a1ed", '
                   '"DBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A", '
                   '"d737742b81292c764ac2a7e419a37ed7fdf4a1ed", '
                   '"EBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A", '
                   '"e737742b81292c764ac2a7e419a37ed7fdf4a1ed", '
                   '"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A", '
                   '"f737742b81292c764ac2a7e419a37ed7fdf4a1ed", "g737742b81292c764ac2a7e419a37ed7fdf4a1ed", '
                   '"h737742b81292c764ac2a7e419a37ed7fdf4a1ed", "i737742b81292c764ac2a7e419a37ed7fdf4a1ed", '
                   '"j737742b81292c764ac2a7e419a37ed7fdf4a1ed", '
                   '"KBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A", '
                   '"LBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A", '
                   '"MBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A", '
                   '"NBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A"] ']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_combined_comparison_split_query(self):
        stix_pattern = "[file:hashes.'SHA-256' = 'ABDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A' " \
                       "OR file:hashes.'SHA-1'= 'a737742b81292c764ac2a7e419a37ed7fdf4a1ed' OR " \
                       "file:hashes.'SHA-256' = " \
                       "'BBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A' OR file:hashes.'SHA-1'= " \
                       "'b737742b81292c764ac2a7e419a37ed7fdf4a1ed' OR file:hashes.'SHA-256' = " \
                       "'CBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A' OR file:hashes.'SHA-1'= " \
                       "'c737742b81292c764ac2a7e419a37ed7fdf4a1ed' OR file:hashes.'SHA-256' = " \
                       "'DBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A' OR file:hashes.'SHA-1'= " \
                       "'d737742b81292c764ac2a7e419a37ed7fdf4a1ed' OR file:hashes.'SHA-256' = " \
                       "'EBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A' OR file:hashes.'SHA-1'= " \
                       "'e737742b81292c764ac2a7e419a37ed7fdf4a1ed' OR file:hashes.'SHA-256' = " \
                       "'FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A' OR file:hashes.'SHA-1'= " \
                       "'f737742b81292c764ac2a7e419a37ed7fdf4a1ed'] START t'2023-11-01T11:00:00.000Z' STOP " \
                       "t'2023-12-06T11:54:00.000Z'"
        query = translation.translate('nozomi', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["query=alerts | where properties/details_hash_SHA1/value"
                   "==\"f737742b81292c764ac2a7e419a37ed7fdf4a1ed\" OR "
                   "properties/details_hash_SHA256/value"
                   "==\"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A\" OR "
                   "properties/process/image_hash_sha256"
                   "==\"FBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A\" OR "
                   "properties/details_hash_SHA1/value==\"e737742b81292c764ac2a7e419a37ed7fdf4a1ed\" OR "
                   "properties/details_hash_SHA256/value"
                   "==\"EBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A\" OR "
                   "properties/process/image_hash_sha256"
                   "==\"EBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A\" | where "
                   "record_created_at>=1698836400000 | where record_created_at<=1701863640000",
                   "query=alerts | where properties/details_hash_SHA256/value"
                   "==\"ABDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A\" OR "
                   "properties/process/image_hash_sha256==\"ABDF0C85B1A39656E616E428FCEFEDC"
                   "930761ACC5CF2846BBF8E60610016142A\" "
                   "OR properties/details_hash_SHA1/value==\"a737742b81292c764ac2a7e419a37ed7fdf4a1ed\" OR "
                   "properties/details_hash_SHA256/value==\"BBDF0C85B1A39656E616E428FCEFEDC93076"
                   "1ACC5CF2846BBF8E60610016142A\" "
                   "OR properties/process/image_hash_sha256==\"BBDF0C85B1A39656E616E428FCEFEDC93076"
                   "1ACC5CF2846BBF8E60610016142A"
                   "\" OR properties/details_hash_SHA1/value==\"b737742b81292c764ac2a7e419a37ed7fdf4a1ed\" OR "
                   "properties/details_hash_SHA256/value==\"CBDF0C85B1A39656E616E428FCEFEDC930761ACC5"
                   "CF2846BBF8E60610016142A\" "
                   "OR properties/process/image_hash_sha256==\"CBDF0C85B1A39656E616E428FCEFEDC9307"
                   "61ACC5CF2846BBF8E60610016142A"
                   "\" OR properties/details_hash_SHA1/value==\"c737742b81292c764ac2a7e419a37ed7fdf4a1ed\" OR "
                   "properties/details_hash_SHA256/value==\"DBDF0C85B1A39656E616E428FCEFEDC930761A"
                   "CC5CF2846BBF8E60610016142A\" "
                   "OR properties/process/image_hash_sha256==\"DBDF0C85B1A39656E616E428FCEFEDC930761A"
                   "CC5CF2846BBF8E60610016142A"
                   "\" OR properties/details_hash_SHA1/value==\"d737742b81292c764ac2a7e419a37ed7fdf4a1ed\" | where "
                   "record_created_at>=1698836400000 | where record_created_at<=1701863640000"
                   ]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_observation_AND_operator(self):
        stix_pattern = "[ipv4-addr:value = '1.1.1.1'] AND [file:name LIKE 'cmd.exe']START " \
                       "t'2023-12-01T01:56:00.000Z' STOP t'2024-01-01T01:57:00.003Z'"
        query = translation.translate('nozomi', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [
            "query=alerts | where properties/details_yara_file/value include? \"cmd.exe\" OR "
            "properties/process/image_path include? \"cmd.exe\" | where record_created_at>=1701395760000 | "
            "where record_created_at<=1704074220003",
            "query=alerts | where ip_dst==\"1.1.1.1\" | where record_created_at>=1708510638714 | where "
            "record_created_at<=1708510938714"
        ]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_observation_OR_operator(self):
        stix_pattern = "[x-nozomi-info:is_public = 'true'] OR [x-alert-properties:x_cause != 'Rule-dependent. " \
                       "A suspicious local event has been detected on a machine.']START t'2023-12-01T00:00:00.000Z' " \
                       "STOP t'2024-01-01T11:00:00.000Z'"
        query = translation.translate('nozomi', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["query=alerts | where properties/is_dst_public==\"true\" OR properties/is_src_public==\"true\" | "
                   "where record_created_at>=1704270267885 | where record_created_at<=1704270567885",
                   "query=alerts | where properties/cause!=\"Rule-dependent. A suspicious local event has been "
                   "detected on a "
                   "machine.\" | where record_created_at>=1701388800000 | where record_created_at<=1704106800000"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_observation_with_combined_comparison(self):
        stix_pattern = "[x-nozomi-info:is_public = 'true' AND x-alert-properties:x_cause != 'Rule-dependent. " \
                       "A suspicious local event has been detected on a machine.'] OR [mac-addr:value LIKE " \
                       "'01:01:01:01:01:01']START t'2023-12-01T01:56:00.000Z' STOP t'2024-01-01T01:57:00.003Z'"
        query = translation.translate('nozomi', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["query=alerts | where mac_src include? \"01:01:01:01:01:01\" OR mac_dst include?"
                   " \"01:01:01:01:01:01\" | where record_created_at>=1701395760000 "
                   "| where record_created_at<=1704074220003"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_combine_multiple_observation_with_same_date(self):
        stix_pattern = "([(x-ibm-ttp-tagging:extensions.'mitre-attack-ext'.technique_id = 'T100')] OR " \
                       "[(x-nozomi-info:zone='Internet')])START t'2023-01-01T01:56:00.000Z' " \
                       "STOP t'2024-01-01T01:57:00.003Z'"
        query = translation.translate('nozomi', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["query=alerts | where zone_dst==\"Internet\" OR zone_src==\"Internet\" OR properties "
                   "include? \"T100\" OR mitre_attack_techniques==\"T100\" | where "
                   "record_created_at>=1672538160000 | where record_created_at<=1704074220003"
                   ]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_invalid_MATCHES_operator(self):
        stix_pattern = "[x-nozomi-info:is_public MATCHES 'true'] START t'2023-12-15T16:43:26.000Z' STOP " \
                       "t'2024-01-02T16:43:26.003Z'"
        result = translation.translate('nozomi', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'mapping_error' == result['code']
        assert result['error'] == "nozomi connector error => data mapping error : Unable to map the following " \
                                  "STIX Operators: [Matches] to data source fields"

    def test_invalid_int_input(self):
        stix_pattern = "[x-ibm-finding:severity = 'nozomi']] START t'2023-02-15T16:43:26.000Z' STOP " \
                       "t'2023-08-18T16:43:26.003Z'"
        result = translation.translate('nozomi', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert result['error'] == 'nozomi connector error => wrong parameter : String type input nozomi is not ' \
                                  'supported for integer type field'

    def test_invalid_enum_value(self):
        stix_pattern = "[x-ibm-finding:finding_type = 'NOZOMI'] START t'2023-12-15T16:43:26.000Z' STOP " \
                       "t'2024-01-01T16:43:26.003Z'"
        result = translation.translate('nozomi', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert result['error'] == "nozomi connector error => wrong parameter : Unsupported ENUM values " \
                                  "provided. threat_name possible supported enum values are 'threat, alert'"

    def test_invalid_timestamp(self):
        stix_pattern = "[x-ibm-finding:finding_type = 'threat'] START t'0000-01-01T01:56:00.000Z' " \
                       "STOP t'2024-01-01T01:57:00.003Z'"
        result = translation.translate('nozomi', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert result['error'] == "nozomi connector error => wrong parameter : cannot convert the timestamp " \
                                  "0000-01-01T01:56:00.000Z to milliseconds"

    def test_invalid_mapping_value(self):
        stix_pattern = "[file:type LIKE 'cmd.exe']START t'2023-12-19T01:56:00.000Z' STOP t'2024-01-01T01:57:00.003Z'"
        result = translation.translate('nozomi', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'mapping_error' == result['code']
        assert result['error'] == "nozomi connector error => data mapping error : Unable to map the following STIX " \
                                  "objects and properties: ['file:type'] to data source fields"

    def test_severity_range(self):
        stix_pattern = "[x-ibm-finding:severity = '200']START t'2023-12-19T01:56:00.000Z' STOP " \
                       "t'2024-01-01T01:57:00.003Z'"
        result = translation.translate('nozomi', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert result['error'] == "nozomi connector error => wrong parameter : Severity allowed range from 0 to 100"

    def test_not_supported_operator_for_threat_name(self):
        stix_pattern = "[x-ibm-finding:finding_type LIKE 'alert']START t'2023-12-19T01:56:00.000Z' STOP " \
                       "t'2024-01-01T01:57:00.003Z'"
        result = translation.translate('nozomi', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert result['error'] == "nozomi connector error => wrong parameter : threat_name fields supports only for " \
                                  "Equal/Not Equal operator"

    def test_not_supported_operator_for_properties(self):
        stix_pattern = "[x-ibm-ttp-tagging:name > 'Non-Application Layer Protocol']START " \
                       "t'2023-12-19T01:56:00.000Z' STOP " \
                       "t'2024-01-01T01:57:00.003Z'"
        result = translation.translate('nozomi', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert result['error'] == "nozomi connector error => wrong parameter : Properties field supports only for " \
                                  "Equal/Not Equal/Like operator"

    def test_not_supported_operators(self):
        stix_pattern = "[network-traffic:dst_port NOT < '445'] START t'2023-11-01T11:00:00.000Z' STOP " \
                       "t'2023-12-06T11:54:00.000Z'"
        result = translation.translate('nozomi', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert result['error'] == "nozomi connector error => wrong parameter : Nozomi is not supported for NOT <, " \
                                  "NOT >, NOT <=, NOT >=, NOT ISSUBSET operators"

    def test_not_supported_for_ISSUBSET_operator(self):
        stix_pattern = "[x-nozomi-info:is_public ISSUBSET 'true'] START t'2023-11-01T11:00:00.000Z' STOP " \
                       "t'2023-12-06T11:54:00.000Z'"
        result = translation.translate('nozomi', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert result['error'] == "nozomi connector error => wrong parameter : ISSUBSET operator allows only subset " \
                                  "supported fields [\'ip_dst\']"
