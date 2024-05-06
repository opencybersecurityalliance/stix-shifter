from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import JSONToStix
from ..stix_transmission.connector import Connector
import os


class ResultsTranslator(JSONToStix):

    def __init__(self, options, dialect, base_file_path=None, callback=None):
        super().__init__(options, dialect, base_file_path, callback)
        show_events = Connector.get_show_events_mode({'options': options})
        if show_events:
            filepath = os.path.abspath(os.path.join(base_file_path, "json", "events_to_stix_map.json"))
            self.map_data = self.read_json(filepath, options)
