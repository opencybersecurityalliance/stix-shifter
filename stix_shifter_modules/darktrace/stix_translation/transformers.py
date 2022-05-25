from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger
import re

LOGGER = logger.set_logger(__name__)


class SecondsToTimeStamp(ValueTransformer):
    """A value transformer for the seconds in 00h00m00s format"""

    @staticmethod
    def transform(obj):
        try:
            seconds = int(obj)
            hours, seconds = seconds // 3600, seconds % 3600
            minutes, seconds = seconds // 60, seconds % 60
            return f"{hours:02d}h{minutes:02d}m{seconds:02d}s"
        except ValueError:
            LOGGER.error("Cannot convert epoch value %s to timestamp", obj)
        return None


class ConnStateToDesc(ValueTransformer):
    """A value transformer for the connection state description"""

    @staticmethod
    def transform(obj):
        """CONN::TCP CONN STATE
            The human readable connection state, which varies for TCP and UDP connections.
            Update from Darktrace API Documentation"""

        dt_conn_description = {
            "OTH": "OTH : Midstream traffic : No SYN seen, just midstream traffic (a “partial connection” "
                   "that was not later closed).",
            "REJ": "REJ : Rejected : Connection attempt rejected.",
            "RST": "RST : RST : Only one side of the connection was inactive, and the other side sent RST.",
            "RSTO": "RSTO : Originator aborted : Connection established, originator aborted (sent a RST).",
            "RSTOS0": "RSTOS0 : Originator SYN + RST : Originator sent a SYN followed by a RST. A SYN-ACK was "
                      "not seen from the responder.",
            "RSTR": "RSTR : Responder aborted : Responder sent a RST.",
            "RSTRH": "RSTRH : Responder SYN ACK + RST : Responder sent a SYN ACK followed by a RST. SYN from"
                     " the (purported) originator was not seen.",
            "S0": "S0 : Attempt : Connection attempt seen, no reply.",
            "S1": "S1 : Established : Connection established, not terminated.",
            "S2": "S2 : Originator close only : Connection established and close attempt by originator seen,"
                  " but no reply from responder.",
            "S3": "S3 : Responder close only : Connection established and close attempt by responder seen, but"
                  " no reply from originator.",
            "SF": "SF : SYN/FIN completion : Complete connection with normal establishment and termination.",
            "SH": "SH : Originator SYN + FIN : Originator sent a SYN followed by a FIN. SYN ACK was not seen "
                  "from the responder.",
            "SHR": "SHR : Responder SYN ACK + FIN : Responder sent a SYN ACK followed by a FIN. SYN from the "
                   "originator was never seen"
        }

        try:
            return dt_conn_description.get(obj, obj)
        except ValueError:
            LOGGER.error("Cannot convert Connection State %s to description", obj)
        return None


class FilterValidEmail(ValueTransformer):
    """ Validate email address format """
    @staticmethod
    def transform(obj):
        pattern = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
        if pattern.match(str(obj)):
            return obj
        return None


class ToArray(ValueTransformer):
    """A value transformer for expected array values"""
    @staticmethod
    def transform(obj):
        try:
            if isinstance(obj, list):
                return obj
            return [obj]
        except ValueError:
            LOGGER.error("Cannot convert input to array")
