from ..base.base_connector import BaseConnector
from .async_dummy_ping import AsyncDummyPing
from .async_dummy_query_connector import AsyncDummyQueryConnector
from .async_dummy_status_connector import AsyncDummyStatusConnector
from .async_dummy_results_connector import AsyncDummyResultsConnector


class Connector(BaseConnector):
    def __init__(self, connection, configuration):
        host = connection.get('host')
        port = connection.get('port')
        path = connection.get('path')
        self.query_connector = AsyncDummyQueryConnector(host, port, path)
        self.status_connector = AsyncDummyStatusConnector(host, port, path)
        self.results_connector = AsyncDummyResultsConnector(host, port, path)
        self.is_async = True
        self.ping_connector = AsyncDummyPing(host, port, path)
