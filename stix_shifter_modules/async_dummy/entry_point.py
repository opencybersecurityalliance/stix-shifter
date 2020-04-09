from stix_shifter_utils.utils.entry_point_base import EntryPointBase
from .stix_transmission.async_dummy_api_client import APIClient
from .stix_transmission.async_dummy_ping_connector import AsyncDummyPingConnector
from .stix_transmission.async_dummy_query_connector import AsyncDummyQueryConnector
from .stix_transmission.async_dummy_status_connector import AsyncDummyStatusConnector
from .stix_transmission.async_dummy_results_connector import AsyncDummyResultsConnector
from .stix_transmission.async_dummy_delete_connector import AsyncDummyDeleteConnector
from .stix_translation.data_mapper import DataMapper
from .stix_translation.query_translator import QueryTranslator
from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import JSONToStix
import os

class EntryPoint(EntryPointBase):

    # python main.py translate async_dummy query '{}' "[ipv4-addr:value = '127.0.0.1']"
    # python main.py translate async_dummy:dialect1 query '{}' "[ipv4-addr:value = '127.0.0.1']"
    # python main.py translate async_dummy:dialect2 query '{}' "[ipv4-addr:value = '127.0.0.1']"

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(options)
        if connection:
            api_client = APIClient(connection, configuration)
            ping_connector = AsyncDummyPingConnector(api_client)
            query_connector = AsyncDummyQueryConnector(api_client)
            status_connector = AsyncDummyStatusConnector(api_client)
            results_connector = AsyncDummyResultsConnector(api_client)
            delete_connector = AsyncDummyDeleteConnector(api_client)

            self.set_ping_connector(ping_connector)
            self.set_query_connector(query_connector)
            self.set_status_connector(status_connector)
            self.set_results_connector(results_connector)
            self.set_delete_connector(delete_connector)
        else:
            
            # self.setup_translation_simple('default')      #   <-------------
            # all the lines below can be replaced with one line configuration |
            
            query_translator = QueryTranslator()
            basepath = os.path.dirname(__file__)
            filepath = os.path.abspath(
                os.path.join(basepath, "stix_translation", "json", "to_stix_map.json"))
            results_translator = JSONToStix(filepath)

            dialect = 'dialect1'
            data_mapper = DataMapper(options, dialect=dialect)
            self.add_dialect(dialect, data_mapper=data_mapper, query_translator=query_translator, results_translator=results_translator, default=True)

            dialect = 'dialect2'
            data_mapper = DataMapper(options, dialect=dialect)
            self.add_dialect(dialect, data_mapper=data_mapper, query_translator=query_translator, results_translator=results_translator, default=False)