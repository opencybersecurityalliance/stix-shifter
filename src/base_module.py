import json
from .modules.qradar import qradar_translator


class TranslationInterface:

    def stix_to_datasource_query(self, data, mapping=None):
        # if translating STIX pattern to a datasource query...
        raise NotImplementedError

    def datasource_results_to_stix(self, data, mapping=None):
        # if translating some datasource to STIX results...
        raise NotImplementedError
