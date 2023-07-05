from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import JSONToStix


class ResultsTranslator(JSONToStix):
    def __init__(self, options, dialect, base_file_path=None, callback=None):
        super().__init__(options, dialect, base_file_path)

    def translate_results(self, data_source, data):
        for result in data:
            if result.get('_raw'):
                result['mime_type_raw'] = 'text/plain'

        return super().translate_results(data_source, data)
