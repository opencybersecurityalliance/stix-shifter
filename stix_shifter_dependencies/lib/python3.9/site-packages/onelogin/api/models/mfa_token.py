#!/usr/bin/python

from onelogin.api.util.utils import str2date

from .base import Base

import sys
if sys.version_info[0] >= 3:
    unicode = str


class MFAToken(Base):
    def __init__(self, data):
        self.value = data.get('mfa_token', None)
        self.reusable = data.get('reusable', None)
        self.expires_at = str2date(data.get('expires_at', None))
        if data and 'device_id' in data.keys():
            device_id = data.get('device_id', None)
            if device_id:
                device_id = unicode(device_id)
            self.device_id = device_id
