import json
from .modules.qradar import qradar_translator


class TranslationInterface:

    DATASOURCES = ['qradar']
    INPUT_DATA_MODELS = ['sco']

    # new_module = __import__('modules/' + arg[0] + '/' + modulename)

    def stix_to_datasource_query(self, arg):
        # if translating STIX pattern to AQL...
        stix_pattern = arg[2]
        translator = qradar_translator.QRadarTranslator()
        aql_query = translator.stix_to_aql(stix_pattern)
        return aql_query

    def datasource_to_stix(self, arg):
        # if translating QRadar events to STIX...
        translator = qradar_translator.QRadarTranslator()

        data = json.loads(arg[2])

        stix_observables = translator.qradar_to_stix(data)

        print(stix_observables)
        return stix_observables
