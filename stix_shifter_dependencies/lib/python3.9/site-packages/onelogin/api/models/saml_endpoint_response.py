#!/usr/bin/python

from .base import Base


class SAMLEndpointResponse(Base):
    def __init__(self, status_type, status_message):
        self.type = status_type
        self.message = str(status_message)
        self.mfa = None
        self.saml_response = None
