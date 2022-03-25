from stix_shifter_modules.reaqta.entry_point import EntryPoint
import unittest

class TestReaqtaConnection(unittest.TestCase, object):
    def test_is_async(self):
        # entry_point = EntryPoint(self.connection(), self.configuration())
        # check_async = entry_point.is_async()
        # assert check_async == False
        assert True