from stix_shifter.stix_translation import stix_translation
import unittest
import re

translation = stix_translation.StixTranslation()


def _remove_timestamp_from_query(queries):
    pattern = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z'
    if isinstance(queries, list):
        return [re.sub(pattern, '', str(query)) for query in queries]
    elif isinstance(queries, str):
        return re.sub(pattern, '', queries)


class TestQueryTranslator(unittest.TestCase):
    """
    class to perform unit test case cisco secure email translate query
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

    def test_equal_operator(self):
        stix_pattern = "[ipv4-addr:value = '1.1.1.1'] START t'2023-02-15T16:43:00.000Z' STOP " \
                       "t'2023-08-18T16:43:00.000Z'"
        query = translation.translate('cisco_secure_email', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['senderIp=1.1.1.1&startDate=2023-02-15T16:43:00.000Z&endDate=2023-08-18T16:43:00.000Z']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_IN_operator(self):
        stix_pattern = "[x-cisco-email-msgevent:quarantined_to IN ('test','test2')] START t'2023-02-15T16:43:26.000Z' " \
                       "STOP t'2023-08-18T16:43:26.003Z'"
        query = translation.translate('cisco_secure_email', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['quarantinedTo=test,test2&startDate=2023-02-15T16:43:00.000Z&endDate=2023-08-18T16:43:00.000Z']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_LIKE_operator(self):
        stix_pattern = "[email-message:subject LIKE 'Reply'] START t'2023-02-15T16:43:26.000Z' STOP " \
                       "t'2023-03-25T16:43:26.003Z'"
        query = translation.translate('cisco_secure_email', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['subjectfilterOperator=contains&subjectfilterValue=Reply&startDate=2023-02-15T16:43:00.000Z'
                   '&endDate=2023-03-25T16:43:00.000Z']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_bool_operator(self):
        stix_pattern = "[x-cisco-email-msgevent:message_delivered = 'true'] START t'2023-02-15T16:43:26.000Z' STOP " \
                       "t'2023-03-25T16:43:26.003Z'"
        query = translation.translate('cisco_secure_email', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['message_delivered=True&startDate=2023-02-15T16:43:00.000Z&endDate=2023-03-25T16:43:00.000Z']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_enum_operator(self):
        stix_pattern = "[x-cisco-email-msgevent:message_status = 'DELIVERED'] START t'2023-02-15T16:43:26.000Z' " \
                       "STOP t'2023-03-25T16:43:26.003Z'"
        query = translation.translate('cisco_secure_email', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['deliveryStatus=DELIVERED&startDate=2023-02-15T16:43:00.000Z&endDate=2023-03-25T16:43:00.000Z']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_file_attribute(self):
        stix_pattern = "[file:name LIKE 'MicrosoftEdgeSetup'] START t'2023-02-15T16:43:26.000Z' STOP " \
                       "t'2023-03-25T16:43:26.003Z'"
        query = translation.translate('cisco_secure_email', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['attachmentNameOperator=contains&attachmentNameValue=MicrosoftEdgeSetup&startDate=2023-02-15T16:43'
                   ':00.000Z&endDate=2023-03-25T16:43:00.000Z']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_file_hashes(self):
        stix_pattern = "[file:hashes.'SHA-256' = '271c0119ac4455fc8db4ef4a8caf8e2bfcfb8bbd3b8c894e117a9ae9f743894b'] " \
                       "START t'2023-02-15T16:43:26.000Z' STOP " \
                       "t'2023-03-25T16:43:26.003Z'"
        query = translation.translate('cisco_secure_email', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['fileSha256=271c0119ac4455fc8db4ef4a8caf8e2bfcfb8bbd3b8c894e117a9ae9f743894b&startDate=2023-02'
                   '-15T16:43:00.000Z&endDate=2023-03-25T16:43:00.000Z']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_combined_comparison_AND_operator(self):
        stix_pattern = "[ipv4-addr:value = '1.1.1.1' AND domain-name:value LIKE 'amazonses']START " \
                       "t'2022-10-01T00:00:00.000Z' STOP t'2022-11-07T11:00:00.000Z'"
        query = translation.translate('cisco_secure_email', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['domainNameOperator=contains&domainNameValue=amazonses&senderIp=1.1.1.1&startDate=2022-10-01T00:00'
                   ':00.000Z&endDate=2022-11-07T11:00:00.000Z']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_comparison_OR_operator_for_basic_attributes(self):
        stix_pattern = "[email-message:x_sender_ip_ref = '3.87.209.25' OR email-message:subject = 'important']START " \
                       "t'2022-10-01T00:00:00.000Z' STOP t'2022-11-07T11:00:00.000Z'"
        query = translation.translate('cisco_secure_email', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['subjectfilterOperator=is&subjectfilterValue=important&startDate=2022-10-01T00:00:00.000Z&endDate'
                   '=2022-11-07T11:00:00.000Z',
                   'senderIp=3.87.209.25&startDate=2022-10-01T00:00:00.000Z&endDate=2022-11-07T11:00:00.000Z']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_combined_comparison_OR_AND_operator_for_basic_attributes(self):
        stix_pattern = "[(ipv4-addr:value = '1.1.1.1' OR email-message:from_ref = 'user1@.com') AND (file:name LIKE " \
                       "'Microsoft' OR file:hashes.'SHA-256' = " \
                       "'271c0119ac4455fc8db4ef4a8caf8e2bfcfb8bbd3b8c894e117a9ae9f743894b')]START " \
                       "t'2023-07-19T01:56:00.000Z' STOP " \
                       "t'2023-09-01T01:57:00.000Z'"
        query = translation.translate('cisco_secure_email', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['fileSha256=271c0119ac4455fc8db4ef4a8caf8e2bfcfb8bbd3b8c894e117a9ae9f743894b'
                   '&envelopeSenderfilterOperator=is&envelopeSenderfilterValue=user1@.com&startDate=2023-07-19T01:56'
                   ':00.000Z&endDate=2023-09-01T01:57:00.000Z',
                   'fileSha256=271c0119ac4455fc8db4ef4a8caf8e2bfcfb8bbd3b8c894e117a9ae9f743894b&senderIp=1.1.1.1'
                   '&startDate=2023-07-19T01:56:00.000Z&endDate=2023-09-01T01:57:00.000Z',
                   'attachmentNameOperator=contains&attachmentNameValue=Microsoft&envelopeSenderfilterOperator=is'
                   '&envelopeSenderfilterValue=user1@.com&startDate=2023-07-19T01:56:00.000Z&endDate=2023-09-01T01:57'
                   ':00.000Z', 'attachmentNameOperator=contains&attachmentNameValue=Microsoft&senderIp=1.1.1.1'
                               '&startDate=2023-07-19T01:56:00.000Z&endDate=2023-09-01T01:57:00.000Z']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_comparison_OR_operator_for_basic_and_event_attributes(self):
        stix_pattern = "[ipv4-addr:value = '1.1.1.1' OR x-cisco-email-msgevent:spam_positive = 'true']" \
                       "START t'2023-07-19T01:56:00.000Z' STOP t'2023-09-01T01:57:00.000Z'"
        query = translation.translate('cisco_secure_email', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['spamPositive=True&startDate=2023-07-19T01:56:00.000Z&endDate=2023-09-01T01:57:00.000Z',
                   'senderIp=1.1.1.1&startDate=2023-07-19T01:56:00.000Z&endDate=2023-09-01T01:57:00.000Z']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_observation_AND_operator(self):
        stix_pattern = "[ipv4-addr:value = '1.1.1.1'] AND [file:name LIKE 'Microsoft']START " \
                       "t'2023-07-19T01:56:00.000Z' STOP t'2023-09-01T01:57:00.003Z'"
        query = translation.translate('cisco_secure_email', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['senderIp=1.1.1.1&startDate=2023-09-04T07:08:00.000Z&endDate=2023-09-04T07:13:00.000Z',
                   'attachmentNameOperator=contains&attachmentNameValue=Microsoft&startDate=2023-07-19T01:56:00.000Z'
                   '&endDate=2023-09-01T01:57:00.000Z']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_observation_OR_operator(self):
        stix_pattern = "[email-message:from_ref LIKE 'user1'] OR [email-message:x_sender_ip_ref = '3.87.209.25']START " \
                       "t'2023-07-19T01:56:00.000Z' STOP t'2023-09-01T01:57:00.003Z'"
        query = translation.translate('cisco_secure_email', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['envelopeSenderfilterOperator=contains&envelopeSenderfilterValue=user1&startDate=2023-09-04T07:12'
                   ':00.000Z&endDate=2023-09-04T07:17:00.000Z',
                   'senderIp=3.87.209.25&startDate=2023-07-19T01:56:00.000Z&endDate=2023-09-01T01:57:00.000Z']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_observation_with_combined_comparison(self):
        stix_pattern = "[ipv4-addr:value = '1.1.1.1' AND file:hashes.'SHA-256' = " \
                       "'271c0119ac4455fc8db4ef4a8caf8e2bfcfb8bbd3b8c894e117a9ae9f743894b' ] OR [" \
                       "x-cisco-email-msgevent:message_status = 'DELIVERED']START t'2023-07-19T01:56:00.000Z' STOP " \
                       "t'2023-09-01T01:57:00.003Z'"
        query = translation.translate('cisco_secure_email', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['fileSha256=271c0119ac4455fc8db4ef4a8caf8e2bfcfb8bbd3b8c894e117a9ae9f743894b&senderIp=1.1.1.1'
                   '&startDate=2023-09-08T05:53:00.000Z&endDate=2023-09-08T05:58:00.000Z',
                   'deliveryStatus=DELIVERED&startDate=2023-07-19T01:56:00.000Z&endDate=2023-09-01T01:57:00.000Z']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_combine_multiple_observation_with_same_date(self):
        stix_pattern = "([(x-cisco-email-msgevent:virus_positive = 'true')] OR [(x-cisco-email-msgevent:spam_positive " \
                       "= 'true')]) START t'2023-07-19T01:56:00.000Z' STOP t'2023-09-01T01:57:00.003Z'"
        query = translation.translate('cisco_secure_email', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['virusPositive=True&startDate=2023-07-19T01:56:00.000Z&endDate=2023-09-01T01:57:00.000Z'
                   '&spamPositive=True']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_combine_IN_supported_fields(self):
        stix_pattern = "[x-cisco-email-msgevent:quarantined_to = 'test1' OR x-cisco-email-msgevent:quarantined_to = " \
                       "'test2'OR x-cisco-email-msgevent:quarantined_to = 'test3'] START t'2023-02-15T16:43:26.000Z' " \
                       "STOP t'2023-08-18T16:43:26.003Z'"
        query = translation.translate('cisco_secure_email', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ['startDate=2023-02-15T16:43:00.000Z&endDate=2023-08-18T16:43:00.000Z&quarantinedTo=test3,test2,test1']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_invalid_boolean_operator(self):
        stix_pattern = "[x-cisco-email-msgevent:message_delivered LIKE 'true'] START t'2023-02-15T16:43:26.000Z' STOP " \
                       "t'2023-03-25T16:43:26.003Z'"
        result = translation.translate('cisco_secure_email', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert result['error'] == 'cisco_secure_email connector error => wrong parameter : Boolean fields supports ' \
                                  'only for Equal operator'

    def test_invalid_boolean_value(self):
        stix_pattern = "[x-cisco-email-msgevent:message_delivered = 'False'] START t'2023-02-15T16:43:26.000Z' STOP " \
                       "t'2023-03-25T16:43:26.003Z'"
        result = translation.translate('cisco_secure_email', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert result['error'] == 'cisco_secure_email connector error => wrong parameter : Boolean field supported' \
                                  ' value is only True'

    def test_invalid_IN_operator(self):
        stix_pattern = "[x-cisco-email-msgevent:ip_reputation IN ('1', '-1')] START t'2023-02-15T16:43:26.000Z' STOP " \
                       "t'2023-03-25T16:43:26.003Z'"
        result = translation.translate('cisco_secure_email', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert result['error'] == 'cisco_secure_email connector error => wrong parameter : IN operator is not ' \
                                  'supported for this field'

    def test_invalid_AND_operator(self):
        stix_pattern = "[x-cisco-email-msgevent:message_delivered = 'true' AND x-cisco-email-msgevent:message_status " \
                       "= 'DELIVERED']START t'2023-02-15T16:43:26.000Z' STOP t'2023-03-25T16:43:26.003Z'"
        result = translation.translate('cisco_secure_email', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert result['error'] == "cisco_secure_email connector error => wrong parameter : AND operator is not " \
                                  "supported for ('deliveryStatus', 'message_delivered') message event fields"

    def test_invalid_string_input(self):
        stix_pattern = "[x-cisco-email-msgevent:ip_reputation = 'delivered'] START t'2023-02-15T16:43:26.000Z' STOP " \
                       "t'2023-08-18T16:43:26.003Z'"
        result = translation.translate('cisco_secure_email', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert result['error'] == 'cisco_secure_email connector error => wrong parameter : String type input ' \
                                  'delivered is not supported for integer type field'

    def test_invalid_enum_value(self):
        stix_pattern = "[x-cisco-email-msgevent:message_status = 'DELIV'] START t'2023-02-15T16:43:26.000Z' STOP " \
                       "t'2023-08-25T16:43:26.003Z'"
        result = translation.translate('cisco_secure_email', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert result['error'] == "cisco_secure_email connector error => wrong parameter : Unsupported ENUM values " \
                                  "provided. deliveryStatus possible supported enum values are 'DELIVERED,DROPPED," \
                                  "ABORTED,BOUNCED'"

    def test_invalid_LIKE_input(self):
        stix_pattern = "[ipv4-addr:value LIKE '3.87.209.25'] START t'2023-02-15T16:43:00.000Z' STOP " \
                       "t'2023-08-18T16:43:00.000Z'"
        result = translation.translate('cisco_secure_email', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert result['error'] == 'cisco_secure_email connector error => wrong parameter : LIKE operator is not ' \
                                  'supported for this field'

    def test_invalid_timestamp(self):
        stix_pattern = "[x-cisco-email-msgevent:ip_reputation = -1] START t'0000-03-01T11:00:00.003Z' STOP " \
                       "t'2023-03-13T11:00:00.003Z'"
        result = translation.translate('cisco_secure_email', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert result['error'] == 'cisco_secure_email connector error => wrong parameter : cannot format the ' \
                                  'timestamp 0000-03-01T11:00:00.003Z'

    def test_invalid_duplicate_value(self):
        stix_pattern = "[x-cisco-email-msgevent:message_status = 'DELIVERED' OR x-cisco-email-msgevent:message_status " \
                       "='DROPPED']START t'2023-07-19T01:56:00.000Z' STOP t'2023-09-01T01:57:00.003Z'"
        result = translation.translate('cisco_secure_email', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert result['error'] == 'cisco_secure_email connector error => wrong parameter : deliveryStatus cannot be ' \
                                  'allowed more than once in query'

    def test_invalid_NOT_operator(self):
        stix_pattern = "[ipv4-addr:value NOT LIKE '1.1.1.1'] START t'2023-07-19T01:56:00.000Z' STOP " \
                       "t'2023-09-01T01:57:00.003Z'"
        result = translation.translate('cisco_secure_email', 'query', '{}', stix_pattern)
        assert False is result['success']
        assert 'not_implemented' == result['code']
        assert result['error'] == 'cisco_secure_email connector error => wrong parameter : Not operator is ' \
                                  'unsupported for cisco secure email'
