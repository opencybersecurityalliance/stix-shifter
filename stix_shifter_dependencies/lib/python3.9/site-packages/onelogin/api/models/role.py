#!/usr/bin/python

from onelogin.api.util.utils import str2int

from .base import Base


class Role(Base):
    def __init__(self, data):
        self.id = str2int(data.get('id', None))
        self.name = data.get('name', '')
        self.admins = data.get('admins', None)
        self.apps = data.get('apps', None)
        self.users = data.get('users', None)

    def get_admin_ids(self):
        return self.admins

    def get_app_ids(self):
        return self.apps

    def get_user_ids(self):
        return self.users
