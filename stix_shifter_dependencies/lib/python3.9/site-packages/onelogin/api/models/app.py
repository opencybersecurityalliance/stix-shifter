#!/usr/bin/python

from onelogin.api.util.utils import str2bool, str2int

from .base import Base


class App(Base):
    def __init__(self, data):
        self.id = str2int(data.get('id', None))
        self.name = data.get('name', '')
        if "icon" in data.keys():
            self.icon_url = data.get('icon', None)
        else:
            self.icon_url = data.get('icon_url', None)
        self.connector_id = str2int(data.get('connector_id', None))
        if 'extension' in data.keys():
            self.extension = str2bool(data.get('extension', None))
        if 'visible' in data.keys():
            self.visible = str2bool(data.get('visible', None))
        if 'login_id' in data.keys():
            self.login_id = str2int(data.get('login_id', None))
        if 'personal' in data.keys():
            self.personal = str2bool(data.get('personal', None))
        if 'provisioned' in data.keys():
            self.provisioned = str2bool(data.get('provisioned', None))
        if 'provisioning' in data.keys():
            provisioning = data.get('provisioning', None)
            if isinstance(provisioning, dict):
                self.provisioning = provisioning
            else:
                self.provisioning = str2bool(provisioning)
        if 'provisioning_status' in data.keys():
            self.provisioning_status = data.get('provisioning_status', None)
            self.provisioning_state = data.get('provisioning_state', None)
            self.provisioning_enabled = str2bool(data.get('provisioning_enabled', None))
