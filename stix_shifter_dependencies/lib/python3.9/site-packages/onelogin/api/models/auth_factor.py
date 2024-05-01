#!/usr/bin/python

from onelogin.api.util.utils import str2int

from .base import Base


class AuthFactor(Base):
    def __init__(self, data):
        self.id = str2int(data.get('factor_id', None))
        self.name = data.get('name', '')
        # V2
        if "auth_factor_name" in data.keys():
            self.auth_factor_name = data.get('auth_factor_name', None)
