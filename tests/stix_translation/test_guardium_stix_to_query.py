from stix_shifter.stix_translation import stix_translation
import unittest

translation = stix_translation.StixTranslation()


class TestStixToQuery(unittest.TestCase):
    """
    class to perform unit test case guardium translate query
    """

    def _test_query_assertions(self, query, queries):
        """
        to assert the each query in the list against expected result
        """
        self.assertIsInstance(query, dict)
        self.assertIsInstance(query['queries'], list)
        for index, each_query in enumerate(query.get('queries'), start=0):
            print(each_query)
            print("---------")
            #self.assertEqual(each_query, queries[index])
            self.assertEqual(True, each_query in queries)

    def test_pattern_translation(self):
        stix_pattern = "[x-com-guardium:remotesource = 'guardiumv10col01.guardiumlabservices.ibm.com'] START t'2018-06-01T00:00:00.009Z' STOP t'2019-11-01T01:11:11.009Z'"
        query = translation.translate('guardium', 'query', '{}', stix_pattern)

        queries = ['{"reportName": "--IBM SC Session Details", "indexFrom": "0", "fetchSize": "1000", "sortType": "asc", "reportParameter": {"QUERY_FROM_DATE": "2018-06-01 00:00:00", "QUERY_TO_DATE": "2019-11-01 01:11:11", "SHOW_ALIASES": "TRUE", "REMOTE_SOURCE": "guardiumv10col01.guardiumlabservices.ibm.com", "CLIENTIP": "%", "SERVERIP": "%", "DBUSERNAME": "%", "SERVICENAME": "%", "DATABASENAME": "%"}}',
                   '{"reportName": "--IBM SC Exception Details", "indexFrom": "0", "fetchSize": "1000", "sortType": "asc", "reportParameter": {"QUERY_FROM_DATE": "2018-06-01 00:00:00", "QUERY_TO_DATE": "2019-11-01 01:11:11", "SHOW_ALIASES": "TRUE", "REMOTE_SOURCE": "guardiumv10col01.guardiumlabservices.ibm.com", "CLIENTIP": "%", "SERVERIP": "%", "DBUSERNAME": "%", "SERVICENAME": "%", "OSUSER": "%", "DATABASENAME": "%", "ERRORCODE": "%"}}',
                   '{"reportName": "--IBM SC Activity Details", "indexFrom": "0", "fetchSize": "1000", "sortType": "asc", "reportParameter": {"QUERY_FROM_DATE": "2018-06-01 00:00:00", "QUERY_TO_DATE": "2019-11-01 01:11:11", "SHOW_ALIASES": "TRUE", "REMOTE_SOURCE": "guardiumv10col01.guardiumlabservices.ibm.com", "CLIENTIP": "%", "SERVERIP": "%", "DBUSERNAME": "%", "SERVICENAME": "%", "OSUSER": "%", "DATABASENAME": "%"}}']


        self._test_query_assertions(query, queries)
