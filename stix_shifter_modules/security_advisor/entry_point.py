from stix_shifter_utils.utils.entry_point_base import EntryPointBase
from .stix_translation.security_advisor_query_translator import SecurityAdvisorQueryTranslator
from .stix_translation.security_advisor_results_translator import JSONToStixObservablesDecorator
from .stix_transmission.security_advisor_ping_connector import SecurityAdvisorPingConnector
from .stix_transmission.security_advisor_query_connector import SecurityAdvisorQueryConnector
from .stix_transmission.security_advisor_status_connector import SecurityAdvisorStatusConnector
from .stix_transmission.security_advisor_results_connector import SecurityAdvisorResultsConnector
from .stix_transmission.security_advisor_delete_connector import SecurityAdvisorDeleteConnector
from stix_shifter_utils.modules.base.stix_translation.empty_data_mapper import EmptyDataMapper
from os import path

class EntryPoint(EntryPointBase):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(options)
        self.set_async(False)
        if connection:
            auth = configuration.get("auth")
            host = connection.get("host")

            ping_connector = SecurityAdvisorPingConnector(host, auth)
            query_connector = SecurityAdvisorQueryConnector(host, auth)
            status_connector = SecurityAdvisorStatusConnector(host, auth)
            results_connector = SecurityAdvisorResultsConnector(host, auth)
            delete_connector = SecurityAdvisorDeleteConnector(host, auth)

            self.set_ping_connector(ping_connector)
            self.set_query_connector(query_connector)
            self.set_status_connector(status_connector)
            self.set_results_connector(results_connector)
            self.set_delete_connector(delete_connector)
        else:
            dialect = 'default'
            query_translator = SecurityAdvisorQueryTranslator(dialect)
            results_translator = JSONToStixObservablesDecorator(options, dialect)
            self.add_dialect(dialect, query_translator=query_translator, results_translator=results_translator, data_mapper=EmptyDataMapper(options, dialect, None), default=True)