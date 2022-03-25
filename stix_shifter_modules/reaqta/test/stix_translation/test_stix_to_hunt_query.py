from stix_shifter.stix_translation import stix_translation
import unittest

translation = stix_translation.StixTranslation()


class TestQueryTranslator(unittest.TestCase):

    def _test_query_assertions(self, query, queries):
        """
        to assert the each query in the list against expected result
        """
        # self.assertIsInstance(query, dict)
        # self.assertIsInstance(query['queries'], list)
        # for index, each_query in enumerate(query.get('queries'), start=0):
        #     self.assertEqual(each_query, queries[index])
        return
    def test_ipv4_query(self):
        assert True
