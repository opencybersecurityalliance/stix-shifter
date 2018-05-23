# Module to handle conversion


class QRadarTranslator:

    def stix_to_aql(self, pattern: str) -> str:
        return "Some AQL query"

    def qradar_to_stix(self, qradar_query_results):
        return "QRadar events as STIX observables in JSON format"
