from ..base.base_ping import BasePing


class SynchronousDummyPing(BasePing):
    def ping(self):
        return "synchronous ping"
