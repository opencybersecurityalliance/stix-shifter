from stix_shifter_utils.utils.entry_point_base import EntryPointBase
from .stix_translation.security_advisor_translator import Translator
from .stix_transmission.security_advisor_ping import SecurityAdvisorPing
from .stix_transmission.security_advisor_query_connector import SecurityAdvisorQueryConnector
from .stix_transmission.security_advisor_status_connector import SecurityAdvisorStatusConnector
from .stix_transmission.security_advisor_results_connector import SecurityAdvisorResultsConnector
from .stix_transmission.security_advisor_delete_connector import SecurityAdvisorDeleteConnector

class EntryPoint(EntryPointBase):

    def __init__(self, connection={}, configuration={}, options={}):
        super(EntryPoint, self).__init__(options)
        self.set_async(False)
        if connection:
            auth = configuration.get("auth")
            host = connection.get("host")

            query_connector = SecurityAdvisorQueryConnector(host, auth)
            status_connector = SecurityAdvisorStatusConnector(host, auth)
            results_connector = SecurityAdvisorResultsConnector(host, auth)
            delete_connector = SecurityAdvisorDeleteConnector(host, auth)
            ping_connector = SecurityAdvisorPing(host, auth)

            self.set_results_connector(results_connector)
            self.set_status_connector(status_connector)
            self.set_delete_connector(delete_connector)
            self.set_query_connector(query_connector)
            self.set_ping_connector(ping_connector)
        else:
            self.add_dialect('default', Translator(), None, True)