#!/usr/bin/python

from onelogin.api.util.utils import str2int, str2bool

from .base import Base


class EmbedApp(Base):
    def __init__(self, data):
        self.id = str2int(data.get('id', None))
        self.name = data.get('name', '')
        self.icon = data.get('icon', '')
        self.provisioned = str2bool(data.get('provisioned', None))
        self.extension_required = str2bool(data.get('extension_required', None))
        self.login_id = str2int(data.get('login_id', None))
        self.personal = str2bool(data.get('personal', None))
