import json
from .modules.qradar import qradar_translator


class TranslationInterface:

    DATASOURCES = ['qradar']
    INPUT_DATA_MODELS = ['sco']

    # new_module = __import__('modules/' + arg[0] + '/' + modulename)

    def stix_to_datasource_query(self, arg):
        # if translating STIX pattern to a datasource query...
        raise NotImplementedError

    def datasource_to_stix(self, arg):
        # if translating some datasource to STIX results...
        raise NotImplementedError
