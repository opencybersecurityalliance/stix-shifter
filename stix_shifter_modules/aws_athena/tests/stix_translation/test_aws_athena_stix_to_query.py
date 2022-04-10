from stix_shifter.stix_translation import stix_translation
import unittest
import re

translation = stix_translation.StixTranslation()


def _remove_timestamp_from_query(queries):
    timestamp_removed = []
    for query in queries:
        for key, value in query.items():
            query = re.sub(r'AND\supdatedat\sBETWEEN\s(\'(\d{4})(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)Z\')\sAND\s\'(\d{4})'
                           r'(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)Z\'|AND\sstarttime\sBETWEEN\s\d+\sAND\s\d+', "", value)
            timestamp_removed.append({key: query})
    return timestamp_removed


class TestQueryTranslator(unittest.TestCase):
    """
    class to perform unit test case aws_athena translate query
    """

    def _test_query_assertions(self, query, queries):
        """
        to assert the each query in the list against expected result
        """
        self.assertIsInstance(query, dict)
        self.assertIsInstance(query['queries'], list)
        for each_query in query.get('queries'):
            self.assertIn(each_query, queries)

    def test_network_exp(self):
        """
        Test with Equal operator
        """
        stix_pattern = "[ipv4-addr:value = '172.31.76.105'] START t'2020-10-01T08:43:10.003Z' " \
                       "STOP t'2020-10-30T10:43:10.003Z'"
        query = translation.translate('aws_athena', 'query', '{}', stix_pattern)
        queries = [{
            "guardduty": "((lower(json_extract_scalar(resource,'$.instancedetails.networkinterfaces.0."
                         "privateipaddress')) = lower('172.31.76.105') OR lower(json_extract_"
                         "scalar(resource,'$.instancedetails.networkinterfaces.1.privateipaddress')) = "
                         "lower('172.31.76.105') OR lower(json_extract_scalar(resource,'$.instancedetails."
                         "networkinterfaces.0.publicip')) = lower('172.31.76.105') OR "
                         "lower(json_extract_scalar(service,'$.action.networkconnectionaction.remoteipdetails."
                         "ipaddressv4')) = lower('172.31.76.105') OR lower(json_extract_scalar(service,"
                         "'$.action.portprobeaction.remoteipdetails.ipaddressv4')) = lower('172.31.76.105') OR "
                         "lower(json_extract_scalar(service,'$.action.awsapicallaction.remoteipdetails.ipaddressv4')) "
                         "= lower('172.31.76.105')) AND updatedat BETWEEN '2020-10-01T08:43:10.003Z' "
                         "AND '2020-10-30T10:43:10.003Z') LIMIT 10000"
        }, {
            "vpcflow": "((lower(sourceaddress) = lower('172.31.76.105') OR lower(destinationaddress) = "
                       "lower('172.31.76.105')) AND starttime BETWEEN 1601541790 AND 1604054590) LIMIT 10000"
        }]
        self._test_query_assertions(query, queries)

    def test_network_protocol(self):
        """
        Test with IN operator
        """
        stix_pattern = "[network-traffic:protocols[*] IN ('tcp','igp')] START t'2020-10-01T08:43:10.003Z' " \
                       "STOP t'2020-10-30T10:43:10.003Z'"
        query = translation.translate('aws_athena', 'query', '{}', stix_pattern)
        queries = [{
            "guardduty": "(lower(json_extract_scalar(service,'$.action.networkconnectionaction.protocol')) IN "
                         "(lower('TCP'),lower('IGP')) AND updatedat BETWEEN '2020-10-01T08:43:10.003Z' AND "
                         "'2020-10-30T10:43:10.003Z') LIMIT 10000"
        }, {
            "vpcflow": "(CAST(protocol AS varchar) IN ('6', '9') AND starttime BETWEEN 1601541790 AND 1604054590) "
                       "LIMIT 10000"
        }]
        self._test_query_assertions(query, queries)

    def test_like_comp_exp(self):
        """
        Test with LIKE operator
        """
        stix_pattern = "[network-traffic:src_ref.value LIKE '172.31.60.104'] START t'2020-10-01T08:43:10.003Z' " \
                       "STOP t'2020-10-30T10:43:10.003Z'"
        query = translation.translate('aws_athena', 'query', '{}', stix_pattern)
        queries = [{
            "guardduty": "(lower(json_extract_scalar(resource,'$.instancedetails.networkinterfaces.0.privateipaddress'"
                         ")) LIKE lower('172.31.60.104') AND updatedat BETWEEN '2020-10-01T08:43:10.003Z' AND "
                         "'2020-10-30T10:43:10.003Z') LIMIT 10000"
        }, {
            "vpcflow": "(lower(sourceaddress) LIKE lower('172.31.60.104') AND starttime BETWEEN 1601541790 AND "
                       "1604054590) LIMIT 10000"
        }]
        self._test_query_assertions(query, queries)

    def test_matches_comp_exp(self):
        """
        Test with MATCHES operator
        :return:
        """
        stix_pattern = "[network-traffic:src_ref.value MATCHES '\\\\d+'] START t'2020-10-01T08:43:10.003Z' STOP " \
                       "t'2020-10-30T10:43:10.003Z'"
        query = translation.translate('aws_athena', 'query', '{}', stix_pattern)
        queries = [{
            "guardduty": "(REGEXP_LIKE(CAST(json_extract_scalar(resource,"
                         "'$.instancedetails.networkinterfaces.0.privateipaddress') as varchar), '\\d+') AND "
                         "updatedat BETWEEN '2020-10-01T08:43:10.003Z' AND '2020-10-30T10:43:10.003Z') LIMIT 10000"
        }, {
            "vpcflow": "(REGEXP_LIKE(CAST(sourceaddress as varchar), '\\d+') AND starttime BETWEEN 1601541790 AND "
                       "1604054590) LIMIT 10000"
        }]
        self._test_query_assertions(query, queries)

    def test_network_comb_obs_exp(self):
        """
        Test with two observation expression
        """
        stix_pattern = "([ipv4-addr:value = '172.31.60.104' OR ipv4-addr:value = '18.210.22.128'] OR " \
                       "[network-traffic:src_port = '22']) START t'2020-10-01T08:43:10.003Z' STOP " \
                       "t'2020-10-30T10:43:10.003Z'"
        query = translation.translate('aws_athena', 'query', '{}', stix_pattern)
        queries = [{
            "guardduty": "((((lower(json_extract_scalar(resource,'$."
                         "instancedetails.networkinterfaces.0.privateipaddress')) = lower('18.210.22.128') OR "
                         "lower(json_extract_scalar(resource,'$.instancedetails.networkinterfaces."
                         "1.privateipaddress')) "
                         "= lower('18.210.22.128') OR "
                         "lower(json_extract_scalar(resource,'$.instancedetails.networkinterfaces.0.publicip')) = "
                         "lower('18.210.22.128') OR lower(json_extract_scalar(service,'$.action.networkconnect"
                         "ionaction.remoteipdetails.ipaddressv4')) = lower('18.210.22.128') OR lower(json_extract_"
                         "scalar(service,'$.action.portprobeaction.remoteipdetails.ipaddressv4')) = "
                         "lower('18.210.22.128') OR lower(json_extract_scalar(service,'$.action.awsapicallaction."
                         "remoteipdetails.ipaddressv4')) = lower('18.210.22.128')) OR (lower(json_extract_scalar"
                         "(resource,'$.instancedetails.networkinterfaces.0.privateipaddress')) = "
                         "lower('172.31.60.104') "
                         "OR lower(json_extract_scalar(resource,'$.instancedetails.networkinterfaces.1."
                         "privateipaddress')) = lower('172.31.60.104') OR lower(json_extract_scalar(resource,"
                         "'$.instancedetails.networkinterfaces.0.publicip')) = lower('172.31.60.104') "
                         "OR lower(json_extract_scalar(service,'$.action.networkconnectionaction.remoteipdetails."
                         "ipaddressv4')) = lower('172.31.60.104') OR lower(json_extract_scalar(service,"
                         "'$.action.portprobeaction.remoteipdetails.ipaddressv4')) = lower('172.31.60.104') OR "
                         "lower(json_extract_scalar(service,'$.action.awsapicallaction.remoteipdetails.ipaddressv4')) "
                         "= lower('172.31.60.104'))) AND updatedat BETWEEN '2020-10-01T08:43:10.003Z' AND "
                         "'2020-10-30T10:43:10.003Z') UNION "
                         "((CAST(json_extract_scalar(service,'$.action.networkconnectionaction.localportdetails.port') "
                         "AS varchar) = '22' OR CAST(json_extract_scalar(service,"
                         "'$.action.portprobeaction.localportdetails.port') AS varchar) = '22') AND updatedat "
                         "BETWEEN '2020-10-01T08:43:10.003Z' AND '2020-10-30T10:43:10.003Z')) LIMIT 10000"
        }, {
            "vpcflow": "((((lower(sourceaddress) = lower('18.210.22.128') OR lower(destinationaddress) = "
                       "lower('18.210.22.128')) OR (lower(sourceaddress) = lower('172.31.60.104') OR "
                       "lower(destinationaddress) = lower('172.31.60.104'))) AND starttime BETWEEN 1601541790 AND "
                       "1604054590) UNION (CAST(sourceport AS varchar) = '22' AND starttime BETWEEN "
                       "1601541790 AND 1604054590)) LIMIT 10000"
        }]
        self._test_query_assertions(query, queries)

    def test_start_end_exp(self):
        """
        test observation expression with Stix field start
        """
        stix_pattern = "[network-traffic:start >= '2020-10-02T09:10:10.003Z'] START t'2020-10-01T08:43:10.003Z' STOP " \
                       "t'2020-10-30T10:43:10.003Z'"
        query = translation.translate('aws_athena', 'query', '{}', stix_pattern)
        queries = [{
            "vpcflow": "(CAST(starttime as REAL) >= 1601629810 AND starttime BETWEEN 1601541790 AND 1604054590) "
                       "LIMIT 10000"
        }]
        self._test_query_assertions(query, queries)

    def test_start_stop_exp(self):
        """
        test observation expression with Stix field start
        """
        stix_pattern = "[network-traffic:src_ref.value LIKE '172.31.60.104']"
        query = translation.translate('aws_athena', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{
            "guardduty": "(lower(json_extract_scalar(resource,'$.instancedetails.networkinterfaces.0.privateipaddress'"
                         ")) LIKE lower('172.31.60.104') AND updatedat BETWEEN '2020-10-01T08:43:10.003Z' AND "
                         "'2020-10-30T10:43:10.003Z') LIMIT 10000"
        }, {
            "vpcflow": "(lower(sourceaddress) LIKE lower('172.31.60.104') AND starttime BETWEEN 1601541790 AND "
                       "1604054590) LIMIT 10000"
        }]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_not_comp_exp(self):
        """
        Test with NOT operator
        :return:
        """
        stix_pattern = "[ipv4-addr:value NOT = '172.31.60.104' OR network-traffic:src_ref.value NOT = " \
                       "'172.31.60.104'] START t'2020-05-01T08:43:10.003Z' " \
                       "STOP t'2020-10-30T10:43:10.003Z'"
        query = translation.translate('aws_athena', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = [{
            "guardduty": "((NOT lower(json_extract_scalar(resource,'$.instancedetails.networkinterfaces.0."
                         "privateipaddress')) = lower('172.31.60.104') OR (NOT lower(json_extract_scalar(resource,"
                         "'$.instancedetails.networkinterfaces.0.privateipaddress')) = lower('172.31.60.104') OR NOT "
                         "lower(json_extract_scalar(resource,'$.instancedetails.networkinterfaces.1.privateipaddress'))"
                         " = lower('172.31.60.104') OR NOT lower(json_extract_scalar(resource,'$.instancedetails."
                         "networkinterfaces.0.publicip')) = lower('172.31.60.104') OR NOT lower(json_extract_"
                         "scalar(service,'$.action.networkconnectionaction.remoteipdetails.ipaddressv4')) = "
                         "lower('172.31.60.104') OR NOT lower(json_extract_scalar(service,'$.action.portprobeaction."
                         "remoteipdetails.ipaddressv4')) = lower('172.31.60.104') OR NOT lower(json_extract_"
                         "scalar(service,'$.action.awsapicallaction.remoteipdetails.ipaddressv4')) = "
                         "lower('172.31.60.104'))) AND updatedat BETWEEN '2020-05-01T08:43:10.003Z' AND "
                         "'2020-10-30T10:43:10.003Z') LIMIT 10000"
        }, {
            "vpcflow": "((NOT lower(sourceaddress) = lower('172.31.60.104') OR (NOT lower(sourceaddress) = "
                       "lower('172.31.60.104') OR NOT lower(destinationaddress) = lower('172.31.60.104'))) AND "
                       "starttime BETWEEN 1588322590 AND 1604054590) LIMIT 10000"
        }]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_ibm_finding_start_exp(self):
        """
        test observation expression with STIX object ibm finding and Stix field start
        """
        stix_pattern = "[x-ibm-finding:start = '2020-09-22T10:09:11Z'] START t'2020-05-01T08:43:10.003Z' " \
                       "STOP t'2020-10-30T10:43:10.003Z'"
        query = translation.translate('aws_athena', 'query', '{}', stix_pattern)
        queries = [{
            "guardduty": "(lower(json_extract_scalar(service,'$.eventfirstseen')) = lower('2020-09-22T10:09:11Z') "
                         "AND updatedat BETWEEN '2020-05-01T08:43:10.003Z' AND '2020-10-30T10:43:10.003Z') LIMIT 10000"
        }, {
            "vpcflow": "(CAST(starttime AS varchar) = '1600769351' AND starttime BETWEEN 1588322590 AND 1604054590) "
                       "LIMIT 10000"
        }
        ]
        self._test_query_assertions(query, queries)

    def test_oper_issuperset(self):
        """
        Test Unsupportted operator
        """
        stix_pattern = "[ipv4-addr:value ISSUPERSET '54.239.30.177'] START t'2020-10-01T08:43:10.003Z' STOP " \
                       "t'2020-10-30T10:43:10.003Z'"
        query = translation.translate('aws_athena', 'query', '{}', stix_pattern)
        assert query['success'] is False
        assert query['connector'] == 'aws_athena'
        assert query['code'] == 'mapping_error'
        assert query['error'] == "aws_athena connector error => data mapping error : Unable to map the following STIX Operators: [IsSuperSet] to data source fields"
