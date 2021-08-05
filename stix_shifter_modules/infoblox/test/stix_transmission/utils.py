# -*- coding: utf-8 -*-

CONNECTION = {
    "host": "mock-host.test",
    "port": 443,
    "options": {"timeout": 60, "result_limit": 1000}
}
CONFIG = {
    "auth": {
        "token": "token"
    }
}
MODULE = "infoblox"

class MockResponse:
    def __init__(self, response_code, obj):
        self.code = response_code
        self.object = obj

    def read(self):
        return bytearray(self.object, 'utf-8')