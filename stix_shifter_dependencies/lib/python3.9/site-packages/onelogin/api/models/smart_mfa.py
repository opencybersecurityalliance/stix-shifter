#!/usr/bin/python

from onelogin.api.util.utils import str2int

from .base import Base
from .risk_score import RiskScore


class SmartMFA(Base):
    def __init__(self, data):
        self.user_id = str2int(data.get('user_id', None))
        self.risk = None
        risk = data.get('risk', None)
        if risk:
            if "reasons" in risk.keys():
                risk["triggers"] = risk.pop("reasons")
            self.risk = RiskScore(risk)
        self.mfa = data.get('mfa', None)
