#!/usr/bin/python

from onelogin.api.util.utils import str2bool, str2int

from .app import App


class UserApp(App):
    def __init__(self, data):
        super(UserApp, self).__init__(data)
        self.extension = str2bool(data.get('extension', None))
        self.login_id = str2int(data.get('login_id', None))
        # v1
        if 'personal' in data.keys():
            self.personal = str2bool(data.get('personal', None))
        if 'provisioned' in data.keys():
            self.provisioned = str2bool(data.get('provisioned', None))
        # v2
        if 'provisioning_status' in data.keys():
            self.provisioning_status = data.get('provisioning_status', None)
            self.provisioning_state = data.get('provisioning_state', None)
            self.provisioning_enabled = data.get('provisioning_enabled', None)
