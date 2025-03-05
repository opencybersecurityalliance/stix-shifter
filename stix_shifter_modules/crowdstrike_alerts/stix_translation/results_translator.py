from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import JSONToStix


class ResultsTranslator(JSONToStix):

    def fetch_mapping(self, basepath, dialect, options, custom_mapping=None):
        if custom_mapping:
            return custom_mapping['to_stix_mapping']
        else:
            return super().fetch_mapping(basepath, dialect, options, custom_mapping)
