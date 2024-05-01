#!/usr/bin/python

from onelogin.api.util.utils import str2date

from .base import Base
from .user import User


class SessionTokenInfo(Base):
    def __init__(self, data):
        self.status = data.get('status', '')
        if 'user' in data.keys() and data['user']:
            self.user = User(data['user'])  # Partial info
        self.return_to_url = data.get('return_to_url', '')
        self.expires_at = str2date(data.get('expires_at', None))
        self.session_token = data.get('session_token', '')
