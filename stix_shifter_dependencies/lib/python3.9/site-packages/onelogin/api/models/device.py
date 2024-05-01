#!/usr/bin/python

from onelogin.api.util.utils import str2int

from .base import Base


class Device(Base):
    def __init__(self, data):
        self.id = str2int(data.get('device_id', None))
        self.type = data.get('device_type', '')
        self.duo_api_hostname = data.get('duo_api_hostname', None)
        self.duo_sig_request = data.get('duo_sig_request', None)
