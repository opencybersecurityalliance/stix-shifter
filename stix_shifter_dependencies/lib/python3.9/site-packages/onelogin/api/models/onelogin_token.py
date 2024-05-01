#!/usr/bin/python

from onelogin.api.util.utils import str2int, str2date
from .base import Base


class OneLoginToken(Base):
    def __init__(self, data):
        self.access_token = data.get('access_token', None)
        self.refresh_token = data.get('refresh_token', None)
        self.account_id = str2int(data.get('account_id', None))
        self.token_type = data.get('token_type', None)
        self.created_at = str2date(data.get('created_at', None))
        self.expires_in = str2int(data.get('expires_in', None))
