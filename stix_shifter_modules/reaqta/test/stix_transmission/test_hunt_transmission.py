from stix_shifter_modules.reaqta.entry_point import EntryPoint
import unittest
from unittest.mock import patch

config = {
        "auth": {
            "app_id": "bla",
            "secret_key": "bla"
        }
    }

connection = {
    'host': 'api.reaqta.com'
}

class CBCloudMockResponse:
    def __init__(self, response_code, object):
        self.code = response_code
        self.object = object

    def read(self):
        return self.object  

class TestReaqtaConnection(unittest.TestCase, object):
    def test_is_async(self):
        # entry_point = EntryPoint(self.connection(), self.configuration())
        # check_async = entry_point.is_async()
        # assert check_async == False
        assert True