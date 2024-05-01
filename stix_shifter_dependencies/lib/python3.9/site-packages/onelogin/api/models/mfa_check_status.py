#!/usr/bin/python

from .base import Base

import sys
if sys.version_info[0] >= 3:
    unicode = str


class MFACheckStatus(Base):
    def __init__(self, data):
        self.id = data.get('id', None)
        self.status = data.get('status', None)
        device_id = data.get('device_id', None)
        if device_id:
            device_id = unicode(device_id)
        self.device_id = device_id
