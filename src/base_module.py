import json
from .modules.qradar import qradar_translator


class TranslationInterface:

    DATASOURCES = ['qradar']
    INPUT_DATA_MODELS = ['sco']

    def stix_to_datasource_query(self, arg):
        # if translating STIX pattern to a datasource query...
        raise NotImplementedError

    def datasource_to_stix(self, arg):
        # if translating some datasource to STIX results...
        raise NotImplementedError
