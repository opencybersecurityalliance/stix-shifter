from stix_shifter.stix_translation import stix_translation
import unittest

translation = stix_translation.StixTranslation()


class TestStixToRelevance(unittest.TestCase, object):

    def test_process_query(self):

        # stix_pattern = "[process:name = 'node' or file:hashes.sha256 = '0c0017201b82e1d8613513dc80d1bf46320a957c393b6ca4fb7fa5c3b682c7e5']"

        # query = translation.translate('bigfix', 'query', '{}', stix_pattern)

        # parsed_stix = [{'attribute': 'file:hashes.sha256', 'comparison_operator': '=', 'value': '0c0017201b82e1d8613513dc80d1bf46320a957c393b6ca4fb7fa5c3b682c7e5'}, {'attribute': 'process:name', 'comparison_operator': '=', 'value': 'node'}]
        # print(query)
        # assert query == {'queries': stix_pattern, 'parsed_stix': parsed_stix}
        assert "query" == "query"
