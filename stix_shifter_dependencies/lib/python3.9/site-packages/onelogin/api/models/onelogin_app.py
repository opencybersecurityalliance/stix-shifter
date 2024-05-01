#!/usr/bin/python

from onelogin.api.util.utils import str2int, str2bool, str2date
from .app import App


class OneLoginApp(App):
    def __init__(self, data):
        super(OneLoginApp, self).__init__(data)
        self.connector_id = str2int(data.get('connector_id', None))
        self.visible = str2bool(data.get('visible', None))
        if "extension" in data.keys():
            self.extension = str2bool(data.get('extension', None))

        if "auth_method" in data.keys():
            # V2
            self.auth_method = str2int(data.get('auth_method', None))
            self.auth_method_description = data.get('auth_method_description', None)
            self.description = data.get('description', None)
            self.created_at = str2date(data.get('created_at', None))
            self.updated_at = str2date(data.get('updated_at', None))
            self.tab_id = str2int(data.get('tab_id', None))
            self.configuration = data.get('configuration', None)
            self.allow_assumed_signin = str2bool(data.get('allow_assumed_signin', None))
            self.brand_id = str2int(data.get('brand_id', None))
            self.role_ids = data.get('role_ids', None)
            self.parameters = data.get('parameters', None)
            self.notes = data.get('notes', None)
            self.policy_id = str2int(data.get('policy_id', None))
        if "sso" in data.keys():
            self.sso = data.get('sso', None)
        if "enforcement_point" in data.keys():
            self.enforcement_point = data.get('enforcement_point', None)
