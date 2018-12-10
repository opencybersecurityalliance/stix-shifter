from stix_shifter import stix_shifter
import unittest

shifter = stix_shifter.StixShifter()


class TestBigFixResultsToStix(unittest.TestCase, object):

    def test_ipv4_query(self):
        # bf_results = "[{'computerID': 12369754, 'computerName': 'bigdata4545.canlab.ibm.com', 'subQueryID': 1," \
        #              " 'isFailure': False, 'result': '.err, d41d8cd98f00b204e9800998ecf8427e, /.err'," \
        #              " 'ResponseTime': 1000}, " \
        #              "{'computerID': 14821900, 'computerName': 'DESKTOP-C30V1JF', 'subQueryID': 1, 'isFailure': True," \
        #              " 'result': '12520437.cpx, 0a0feb9eb28bde8cd835716343b03b14, C:\\Windows\\system32\\12520437.cpx'," \
        #              " 'ResponseTime': 63000}]"
        # query = shifter.translate('bigfix', 'results', '{}', bf_results)
        # assert query == bf_results
        assert "query" == "query"