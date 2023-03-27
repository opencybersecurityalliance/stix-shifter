from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger
import os.path as path
import json

LOGGER = logger.set_logger(__name__)

class ProtocolNumToName(ValueTransformer):
    """A value transformer to convert QRadar ObjectName to windows-registry-key.key STIX"""

    @staticmethod
    def transform(protocol_decimal):
        PROTOCOL_LOOKUP_JSON_FILE = 'json/network_protocol_map.json'
        
        try:
            _json_path = path.abspath(path.join(path.join(__file__, ".."), PROTOCOL_LOOKUP_JSON_FILE))
            
            if path.exists(_json_path):
                with open(_json_path) as f_obj:
                    protocol_dict = json.load(f_obj)
            else:
                raise FileNotFoundError

            for key, value in protocol_dict.items():
                if str(protocol_decimal) == value:
                    protocol = key
            return [protocol]
        except ValueError:
            LOGGER.error("Cannot convert protocol number to protocol name")