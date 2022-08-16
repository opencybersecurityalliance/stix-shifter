from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import JSONToStix
from os import path

class ResultsTranslator(JSONToStix):

    def __init__(self, options, dialect, base_file_path=path.dirname(__file__), callback=None):
        super().__init__(options, dialect, base_file_path=base_file_path)


    def translate_results(self, data_source, data):
        """
        Translates JSON data into STIX results based on a mapping file
        :param data: JSON formatted data to translate into STIX format
        :type data: str
        :param mapping: The mapping file path to use as instructions on how to translate the given JSON data to STIX.
            Defaults the path to whatever is passed into the constructor for JSONToSTIX (This should be the to_stix_map.json in the module's json directory)
        :type mapping: str (filepath)
        :return: STIX formatted results
        :rtype: str
        """
        results = super().translate_results(data_source, data)

        if len(results['objects']) - 1 == len(data):
            for i in range(1, len(results['objects'])):
                results['objects'][i]['number_observed'] = 1
        else:
            raise RuntimeError("Incorrect number of result objects after translation. Found: {}, expected: {}.".format(
                len(results['objects']) - 1, len(data)))

        return results