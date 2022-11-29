import sys
from unittest.mock import MagicMock
from asyncinit import asyncinit


def get_mock_response(status_code, content=None, return_type='str', response=None):
    if sys.version_info.major == 3:
        if sys.version_info.minor < 8:
            return RequestMockResponseOld(status_code, content, return_type, response)
        else:
            return RequestMockResponse(status_code, content, return_type, response)

def get_aws_mock_response(obj):
    if sys.version_info.major == 3:
        if sys.version_info.minor < 8:
            return AWSComposeMockResponseOld(obj)
        else:
            return AWSComposeMockResponse(obj)

def get_adal_mock_response():
    return AdalMockResponse()

@asyncinit
class RequestMockResponseOld:
    def __init__(self, status_code, content, return_type='str', response=None):
        self.code = status_code
        self.status_code = status_code
        self.content = content
        self.response = response
        self.object = response
        self.return_type = return_type
        self.history = []

    def read(self):
        if self.return_type == 'byte':
            return bytearray(self.content, 'utf-8')
        return self.content

class RequestMockResponse:
    def __init__(self, status_code, content, return_type='str', response=None):
        self.code = status_code
        self.status_code = status_code
        self.content = content
        self.response = response
        self.object = response
        self.return_type = return_type
        self.history = []

    def read(self):
        if self.return_type == 'byte':
            return bytearray(self.content, 'utf-8')
        return self.content

@asyncinit
class AWSComposeMockResponseOld:
    def __init__(self, object):
        self.object = object

    def __getitem__(self, prop):
        return self.object[prop]

    def get(self, prop, default=None):
        return self.object.get(prop, default)

class AWSComposeMockResponse:
    def __init__(self, object):
        self.object = object

    def __getitem__(self, prop):
        return self.object[prop]

    def __contains__(self, prop):
        return prop in self.object

    def get(self, prop, default=None):
        return self.object.get(prop, default)



class AdalMockResponse:
    @staticmethod
    def acquire_token_with_client_credentials(resource, client_id, client_secret):
        context_response = dict()
        context_response['accessToken'] = 'abc12345'
        return context_response

class AsyncMock(MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)



class InnerResponse:
    """ class for capturing response"""

    def __init__(self, st_code, txt):
        self.status_code = st_code
        self.text = txt
        self.history = []