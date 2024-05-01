#!/usr/bin/python

from .base import Base


class RateLimit(Base):
    def __init__(self, data):
        self.limit = data.get('X-RateLimit-Limit', None)
        self.remaining = data.get('X-RateLimit-Remaining', None)
        self.reset = data.get('X-RateLimit-Reset', None)
