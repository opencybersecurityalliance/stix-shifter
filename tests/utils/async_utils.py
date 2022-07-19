import sys
from unittest.mock import MagicMock
from asyncinit import asyncinit


def get_mock_response(status_code, content, return_type='str'):
    if sys.version_info.major == 3:
        if sys.version_info.minor < 8:
            return RequestMockResponseOld(status_code, content, return_type)
        else:
            return RequestMockResponse(status_code, content, return_type)

@asyncinit
class RequestMockResponseOld:
    def __init__(self, status_code, content, return_type):
        self.code = status_code
        self.content = content
        self.return_type = return_type

    def read(self):
        if self.return_type == 'byte':
            return bytearray(self.content, 'utf-8')
        return self.content

class RequestMockResponse:
    def __init__(self, status_code, content, return_type):
        self.code = status_code
        self.content = content
        self.return_type = return_type

    def read(self):
        if self.return_type == 'byte':
            return bytearray(self.content, 'utf-8')
        return self.content

class AsyncMock(MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)
