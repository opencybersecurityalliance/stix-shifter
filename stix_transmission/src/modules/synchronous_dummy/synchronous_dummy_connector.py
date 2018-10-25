from ..base.base_connector import BaseConnector
from .synchronous_dummy_results_connector import SynchronousDummyResultsConnector
from .synchronous_dummy_ping import SynchronousDummyPing


class Connector(BaseConnector):
    def __init__(self):
        self.results_connector = SynchronousDummyResultsConnector()
        self.is_async = False
        self.ping = SynchronousDummyPing()
