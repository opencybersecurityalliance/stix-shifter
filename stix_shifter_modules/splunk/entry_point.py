from stix_shifter_utils.utils.entry_point_base import EntryPointBase
from stix_shifter_utils.modules.cim.stix_translation.cim_data_mapper import CimDataMapper
from stix_shifter_utils.modules.car.stix_translation.car_data_mapper import CarDataMapper
from .stix_transmission.spl_api_client import APIClient
from .stix_transmission.splunk_ping_connector import SplunkPingConnector
from .stix_transmission.splunk_query_connector import SplunkQueryConnector
from .stix_transmission.splunk_status_connector import SplunkStatusConnector
from .stix_transmission.splunk_results_connector import SplunkResultsConnector
from .stix_transmission.splunk_delete_connector import SplunkDeleteConnector
from .stix_transmission.splunk_auth import SplunkAuth
from .stix_translation.query_translator import QueryTranslator

class EntryPoint(EntryPointBase):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(options)
        if connection:
            api_client = APIClient(connection, configuration)
            ping_connector = SplunkPingConnector(api_client)
            query_connector = SplunkQueryConnector(api_client)
            status_connector = SplunkStatusConnector(api_client)
            results_connector = SplunkResultsConnector(api_client)
            delete_connector = SplunkDeleteConnector(api_client)

            self.set_ping_connector(ping_connector)
            self.set_query_connector(query_connector)
            self.set_status_connector(status_connector)
            self.set_results_connector(results_connector)
            self.set_delete_connector(delete_connector)
        else:
            query_translator = QueryTranslator()
            self.add_dialect('default', query_translator=query_translator, data_mapper=CimDataMapper(options), default=True)
            self.add_dialect('cim', query_translator=query_translator, data_mapper=CimDataMapper(options), default=False, default_include=False)
            self.add_dialect('car', query_translator=query_translator, data_mapper=CarDataMapper(options), default=False, default_include=False)