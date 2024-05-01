#!/usr/bin/python

from onelogin.api.util.utils import str2bool, str2int

from .base import Base


class Connector(Base):
    def __init__(self, data):
        self.id = str2int(data.get('id', None))
        self.name = data.get('name', '')
        self.auth_method = str2int(data.get('auth_method', None))
        self.allows_new_parameters = str2bool(data.get('allows_new_parameters', None))
        self.icon_url = data.get('icon_url', '')
