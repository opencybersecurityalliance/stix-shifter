import datetime
import json
from os import path

# Util file for transforming data

class Transformer():
    # this class will contain all data transformations
    # for the db2 result set
    def __init__(self):
        # initialize so it doesnt have to load every time
        self.protocol_json = self.load_json_dict()

    def load_json_dict(self):
        return_dict = dict()
        json_path = path.abspath(path.join(path.dirname(__file__), '../../..',
                                            'stix_shifter_modules/db2/stix_translation/json'
                                            '/network_protocol_map.json'))
        if path.exists(json_path):
            with open(json_path) as f_obj:
                protocols = json.load(f_obj)
                for key in protocols:
                    value = int(protocols[key])
                    return_dict[value] = str(key)
                return return_dict
        else:
            raise FileNotFoundError

    def protocol_transform(self, result):
        # protocol is in result as PROTOCOL with IANA
        value = result["PROTOCOL"]
        if isinstance(value, int):
            result["PROTOCOL"] = self.protocol_json[value]
        return

    def time_transform(self, result):
        result['STIME'] = result['STIME'].strftime("%s")
        result['ETIME'] = result['ETIME'].strftime("%s")

    def main(self, result):
        # main method to run transform on result
        self.protocol_transform(result)
        self.time_transform(result)
