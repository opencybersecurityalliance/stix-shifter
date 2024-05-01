#!/usr/bin/python

from onelogin.api.util.utils import str2date

from .base import Base


class SmartHookLog(Base):
    def __init__(self, data):
        self.request_id = data.get('request_id', None)
        self.correlation_id = data.get('correlation_id', None)
        self.created_at = str2date(data.get('created_at', None))
        self.events = data.get('events', None)
