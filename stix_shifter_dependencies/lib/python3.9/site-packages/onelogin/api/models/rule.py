#!/usr/bin/python

from onelogin.api.util.utils import str2int, str2bool

from .base import Base


class Rule(Base):
    def __init__(self, data):
        self.id = str2int(data.get('id', None))
        self.name = data.get('name', None)
        self.match = data.get('match', None)
        self.enabled = str2bool(data.get('enabled', None))
        self.position = str2int(data.get('position', None))
        self.conditions = data.get('conditions', None)
        self.actions = data.get('actions', None)
