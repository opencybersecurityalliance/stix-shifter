#!/usr/bin/python

from onelogin.api.util.utils import str2int, str2bool, str2date

from .base import Base


class SmartHook(Base):
    def __init__(self, data):
        self.id = data.get('id', None)
        self.type = data.get('type', '')
        self.packages = data.get('packages', None)
        self.runtime = data.get('runtime', None)
        self.context_version = data.get('context_version', None)
        self.retries = str2int(data.get('retries', None))
        self.timeout = str2int(data.get('timeout', None))
        self.disabled = str2bool(data.get('disabled', True))
        self.status = data.get('status', None)
        self.env_vars = data.get('env_vars', None)
        self.conditions = data.get('conditions', None)
        options = data.get('options', None)
        if options:
            self.risk_enabled = str2bool(options.get('risk_enabled', False))
            self.location_enabled = str2bool(options.get('location_enabled', False))
            self.mfa_device_info_enabled = str2bool(options.get('mfa_device_info_enabled', False))
        self.created_at = str2date(data.get('created_at', None))
        self.updated_at = str2date(data.get('updated_at', None))
        self.function = data.get('function', None)
