from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import JSONToStix
from ..stix_transmission.connector import Connector
import os
import json


class ResultsTranslator(JSONToStix):

    def __init__(self, options, dialect, base_file_path=None, callback=None):
        super().__init__(options, dialect, base_file_path, callback)
        show_events = Connector.get_show_events_mode({'options': options})
        if show_events:
            filepath = os.path.abspath(os.path.join(base_file_path, "json", "to_stix_map_events.json"))
            self.map_data = self.read_json(filepath, options)

    def translate_results(self, data_source, data):
        """
        Translates JSON data into STIX results based on a mapping file
        :param data: JSON formatted data to translate into STIX format
        :type data: str
        :return: STIX formatted results
        :rtype: str
        """

        results = super().translate_results(data_source, data)
        json_data = json.loads(data)

        if len(results['objects']) - 1 == len(json_data):
            for i in range(1, len(results['objects'])):
                results['objects'][i]['number_observed'] = 1
        else:
            raise RuntimeError("Incorrect number of result objects after translation. Found: {}, expected: {}.".format(len(results['objects']) - 1, len(json_data)))

        return results
