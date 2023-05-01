
def get_mock_response(status_code, content=None, return_type='str', response=None):
    return RequestMockResponse(status_code, content, return_type, response)

def get_aws_mock_response(obj):
    return AWSComposeMockResponse(obj)

class RequestMockResponse:
    def __init__(self, status_code, content, return_type='str', response=None):
        self.code = status_code
        self.content = content
        self.response = response
        self.object = response
        self.return_type = return_type
        self.history = []

    def read(self):
        if self.return_type == 'byte':
            return bytearray(self.content, 'utf-8')
        return self.content

class AWSComposeMockResponse:
    def __init__(self, object):
        self.object = object

    def __getitem__(self, prop):
        return self.object[prop]

    def __contains__(self, prop):
        return prop in self.object

    def get(self, prop, default=None):
        return self.object.get(prop, default)

