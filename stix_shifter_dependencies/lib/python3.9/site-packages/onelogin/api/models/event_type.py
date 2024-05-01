#!/usr/bin/python

from onelogin.api.util.utils import str2int

from .base import Base


class EventType(Base):
    def __init__(self, data):
        self.id = str2int(data.get('id', None))
        self.name = data.get('name', '')
        self.description = data.get('description', '')
