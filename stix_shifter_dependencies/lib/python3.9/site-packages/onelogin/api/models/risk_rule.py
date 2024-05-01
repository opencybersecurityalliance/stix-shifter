#!/usr/bin/python

from onelogin.api.util.utils import str2int

from .base import Base


class RiskRule(Base):
    def __init__(self, data):
        self.id = str2int(data.get('id', None))
        self.name = data.get('name', None)
        self.description = data.get('description', None)
        self.type = data.get('type', None)
        self.target = data.get('target', None)
        self.source = data.get('source', None)
        self.filters = data.get('filters', None)
