from ..base.base_ping import BasePing


class AsyncDummyPing(BasePing):
    def __init__(self, host, port, path):
        self.host = host
        self.port = port
        self.path = path

    def ping(self):
        return 'async ping'
