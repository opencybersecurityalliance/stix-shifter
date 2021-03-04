import re
from datetime import datetime, timezone, timedelta
from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger

LOGGER = logger.set_logger(__name__)


class EpochToGuardium(ValueTransformer):
    """A value transformer for Epoch to Guardium timestamp"""

    @staticmethod
    def transform(epoch):
        try:
            return (datetime.fromtimestamp(int(epoch) / 1000, timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))
        except ValueError:
            LOGGER.error("Cannot convert epoch value {} to timestamp".format(epoch))


class GuardiumToTimestamp(ValueTransformer):
    """A value transformer for converting Guardium timestamp to regular timestamp"""

    @staticmethod
    def transform(gdmTime):
        rgx = r"(\d\d\d\d-\d\d-\d\d)\s(\d\d:\d\d:\d\d)"
        mtch = (re.findall(rgx, gdmTime))[0]
        return (mtch[0] + 'T' + mtch[1]) + '.000Z'


class TimestampToGuardium(ValueTransformer):
    """A value transformer for converting  regular timestamp to Guardium timestamp"""

    @staticmethod
    def transform(timestamp):
        rgx = r"(\d\d\d\d-\d\d-\d\d).(\d\d:\d\d:\d\d)"
        mtch = (re.findall(rgx, timestamp))[0]
        return (mtch[0] + ' ' + mtch[1])


class GuardiumQS(ValueTransformer):
    """Send back Policy Violation string"""

    @staticmethod
    def transform(obj):
        return "Policy Violation"


class GuardiumRep(ValueTransformer):
    """Send back Threat Case string"""

    @staticmethod
    def transform(obj):
        return "Threat Case"


class GuardiumMapSeverity(object):
    """A value transformer for converting numeric severity rating to literal """

    @staticmethod
    def transform(severity):
        try:
            num = int(severity)
            if num < 5:
                return "Low"
            elif num > 5:
                return "High"
            else:
                return "Medium"
        except ValueError:
            #LOGGER.error("Cannot convert input to path string")
            return severity


class GuardiumMapSeverityNum(object):
    """A value transformer for converting  severity literal to numeric """

    @staticmethod
    def transform(severity):
        sev = severity.lower()
        if sev == "low":
            return '01'
        elif sev == "high":
            return '09'
        elif sev == "medium":
            return '05'
        else:
            return severity


class TimestampToGuardiumQS(ValueTransformer):
    """A value transformer for converting  regular timestamp to Guardium timestamp"""

    @staticmethod
    def transform(timestamp):
        rgx = r"(\d\d\d\d-\d\d-\d\d).(\d\d:\d\d:\d\d)"
        mtch = (re.findall(rgx, timestamp))[0]
        return mtch[0].replace("-", "") + ' ' + mtch[1]
