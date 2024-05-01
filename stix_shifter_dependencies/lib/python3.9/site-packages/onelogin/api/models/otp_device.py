#!/usr/bin/python

from onelogin.api.util.utils import str2bool, str2date

from .base import Base

import sys
if sys.version_info[0] >= 3:
    unicode = str


class OTP_Device(Base):
    def __init__(self, data):
        id_data = data.get('id', None)
        if id_data is None:
            id_data = data.get('device_id', None)
        if id_data:
            id_data = unicode(id_data)
        self.id = id_data
        self.auth_factor_name = data.get('auth_factor_name', '')
        self.type_display_name = data.get('type_display_name', '')
        self.user_display_name = data.get('user_display_name', '')
        self.default = str2bool(data.get('default', False))
        # v1
        if 'active' in data.keys():
            self.active = str2bool(data.get('active', False))
        if 'needs_trigger' in data.keys():
            self.needs_trigger = str2bool(data.get('needs_trigger', False))
        if 'state_token' in data.keys():
            self.state_token = data.get('state_token', None)
        if 'phone_number' in data.keys():
            self.phone_number = data.get('phone_number', '')
        # v2 (enroll factor)
        if 'status' in data.keys():
            self.status = data.get('status', None)
            if self.status == "accepted":
                self.active = str2bool(data.get('active', True))
        if 'expires_at' in data.keys():
            self.expires_at = str2date(data.get('expires_at', None))
        if 'factor_data' in data.keys():
            self.factor_data = data.get('factor_data', None)
