#!/usr/bin/python

from .base import Base


class RiskScore(Base):
    def __init__(self, data):
        self.score = data.get('score', None)
        self.triggers = data.get('triggers', None)
        self.messages = data.get('messages', None)
