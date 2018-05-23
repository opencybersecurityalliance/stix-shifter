from .modules.qradar import qradar_translator


class TranslationInterface:

    def stix_to_datasource_query(self, arg):
        # if translating STIX pattern to AQL...
        translator = qradar_translator.QRadarTranslator()
        aql_query = translator.stix_to_aql("some stix pattern input")
        return aql_query

    def datasource_to_stix(self, arg):
        # if translating QRadar events to STIX...
        translator = qradar_translator.QRadarTranslator()
        stix_observables = translator.qradar_to_stix("some qradar events")
        return stix_observables
