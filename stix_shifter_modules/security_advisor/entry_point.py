from stix_shifter_utils.utils.base_entry_point import BaseEntryPoint
from .stix_translation.query_translator import QueryTranslator
from .stix_translation.results_translator import JSONToStixObservablesDecorator
from .stix_transmission.ping_connector import PingConnector
from .stix_transmission.query_connector import QueryConnector
from .stix_transmission.status_connector import StatusConnector
from .stix_transmission.results_connector import ResultsConnector
from .stix_transmission.delete_connector import DeleteConnector


class EntryPoint(BaseEntryPoint):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(connection, configuration, options)
        self.set_async(False)
        if connection:
            auth = configuration.get("auth")
            host = connection.get("host")

            ping_connector = PingConnector(host, auth)
            query_connector = QueryConnector(host, auth)
            status_connector = StatusConnector(host, auth)
            results_connector = ResultsConnector(host, auth)
            delete_connector = DeleteConnector(host, auth)

            self.set_ping_connector(ping_connector)
            self.set_query_connector(query_connector)
            self.set_status_connector(status_connector)
            self.set_results_connector(results_connector)
            self.set_delete_connector(delete_connector)
        else:
            dialect = 'default'
            query_translator = QueryTranslator(options, dialect)
            results_translator = JSONToStixObservablesDecorator(options, dialect)
            self.add_dialect(dialect, query_translator=query_translator, results_translator=results_translator, default=True)
