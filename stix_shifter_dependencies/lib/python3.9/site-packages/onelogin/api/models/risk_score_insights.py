#!/usr/bin/python

from onelogin.api.util.utils import str2int

from .base import Base


class RiskScoreInsights(Base):
    def __init__(self, data):
        self.scores = data.get('scores', None)
        self.total = str2int(data.get('total', None))
