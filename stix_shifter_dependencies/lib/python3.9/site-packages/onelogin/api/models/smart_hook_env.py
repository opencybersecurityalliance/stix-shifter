#!/usr/bin/python

from onelogin.api.util.utils import str2date

from .base import Base


class SmartHookEnv(Base):
    def __init__(self, data):
        self.id = data.get('id', None)
        self.name = data.get('name', None)
        self.created_at = str2date(data.get('created_at', None))
        self.updated_at = str2date(data.get('updated_at', None))
