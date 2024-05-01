#!/usr/bin/python

from onelogin.api.util.utils import str2int, str2bool
from .base import Base


class Brand(Base):
    def __init__(self, data):
        self.id = str2int(data.get('id', None))
        self.name = data.get('name', '')
        self.enabled = str2bool(data.get('enabled', False))
        self.custom_support_enabled = data.get('custom_support_enabled', None)
        self.custom_color = data.get('custom_color', None)
        self.custom_accent_color = data.get('custom_accent_color', None)
        self.custom_masking_color = data.get('custom_masking_color', None)
        self.custom_masking_opacity = str2int(data.get('custom_masking_opacity', None))
        self.enable_custom_label_for_login_screen = str2bool(data.get('enable_custom_label_for_login_screen', None))
        self.custom_label_text_for_login_screen = data.get('custom_label_text_for_login_screen', None)
        self.login_instruction = data.get('login_instruction', None)
        self.login_instruction_title = data.get('login_instruction_title', None)
        self.mfa_enrollment_message = data.get('mfa_enrollment_message', None)
        self.hide_onelogin_footer = str2bool(data.get('hide_onelogin_footer', None))
        self.background = data.get('background', None)
        self.logo = data.get('logo', None)
