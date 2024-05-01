#!/usr/bin/python

from onelogin.api.util.utils import str2bool, str2int, str2date
from .base import Base

import sys
if sys.version_info[0] >= 3:
    unicode = str


class FactorEnrollmentResponse(Base):
    def __init__(self, data):
        if "user_id" in data.keys():
            # v2
            self.id = data.get('id', None)
            self.user_id = str2int(data.get('user_id', None))
        else:
            # v1
            self.user_id = str2int(data.get('id', None))

        device_id = data.get('device_id', None)
        if device_id:
            device_id = unicode(device_id)
        self.device_id = device_id
        self.auth_factor_name = data.get('auth_factor_name', '')
        self.type_display_name = data.get('type_display_name', '')
        self.user_display_name = data.get('user_display_name', '')
        expires_at_data = data.get('state_token_expires_at', None)
        if expires_at_data is None:
            expires_at_data = data.get('expires_at', None)
        self.expires_at = str2date(expires_at_data)

        # v1
        if "state_token" in data.keys():
            self.state_token = data.get('state_token', '')
        if "active" in data.keys():
            self.active = str2bool(data.get('active', False))
        # v2
        if "factor_data" in data.keys():
            self.factor_data = data.get('factor_data', '')
