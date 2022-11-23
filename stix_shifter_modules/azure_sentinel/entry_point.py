import os
import importlib
from .stix_translation.query_translator import QueryTranslator
from stix_shifter_utils.utils.base_entry_point import BaseEntryPoint
from stix_shifter_utils.modules.base.stix_transmission.base_connector import BaseConnector
from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import JSONToStix


class EntryPoint(BaseEntryPoint):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(connection, configuration, options)
        self.set_async(False)

        if connection:
            module_name = "azure_sentinel"
            module_path = "stix_shifter_modules." + module_name + ".stix_transmission." + options.get("api")
            module = importlib.import_module(module_path + ".connector")
            connector = module.Connector(connection, configuration)

            if not isinstance(connector, BaseConnector):
                raise Exception('connector is not instance of BaseConnector')
            self.set_query_connector(connector)
            self.set_status_connector(connector)
            self.set_results_connector(connector)
            self.set_delete_connector(connector)
            self.set_ping_connector(connector)

        if options.get("api"):
            api_type = options.get("api")
        else:
            api_type = "Log Analytics"

        basepath = os.path.dirname(__file__)
        filepath = os.path.abspath(os.path.join(basepath, "stix_translation", api_type))

        if api_type == "Graph Security":
            dialect = 'default'
            query_translator = QueryTranslator(options, dialect, filepath)
            results_translator = JSONToStix(options, dialect, filepath)
            self.add_dialect(dialect, query_translator=query_translator, results_translator=results_translator,
                             default=True)

        if api_type == "Log Analytics":
            dialect = 'SecurityAlert'
            query_translator = QueryTranslator(options, dialect, filepath)
            results_translator = JSONToStix(options, dialect, filepath)
            self.add_dialect(dialect, query_translator=query_translator, results_translator=results_translator,
                             default=True)
            dialect = 'SecurityEvent'
            query_translator = QueryTranslator(options, dialect, filepath)
            results_translator = JSONToStix(options, dialect, filepath)
            self.add_dialect(dialect, query_translator=query_translator, results_translator=results_translator,
                             default=False)
            dialect = 'SecurityIncident'
            query_translator = QueryTranslator(options, dialect, filepath)
            results_translator = JSONToStix(options, dialect, filepath)
            self.add_dialect(dialect, query_translator=query_translator, results_translator=results_translator,
                             default=False)
