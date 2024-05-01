# -*- coding: utf-8 -*-

""" UrlBuilder class

Copyright (c) 2021, OneLogin, Inc.
All rights reserved.

UrlBuilder class of the OneLogin's Python SDK.

"""
from onelogin.api.util.endpoints import Endpoints

import sys
if sys.version_info[0] >= 3:
    unicode = str
    long = str


class UrlBuilder(object):
    """

    Builds the API URL endpoints for the OneLogin's Python SDK.

    """

    region = 'us'
    subdomain = None

    def __init__(self, region='us', subdomain=None):
        self.region = "us" if region is None else region
        self.subdomain = subdomain

    def get_url(self, base, obj_id=None, extra_id=None, version_id=None):

        if self.subdomain:
            subdomain = self.subdomain
        else:
            subdomain = "api.%s" % self.region

        if obj_id is not None:
            self.validate_id(obj_id)

        if version_id is None:
            if obj_id is None:
                return base % (subdomain)
            elif extra_id is None:
                return base % (subdomain, obj_id)
            else:
                return base % (subdomain, obj_id, extra_id)
        else:
            if obj_id is None:
                return base % (subdomain, version_id)
            elif extra_id is None:
                return base % (subdomain, version_id, obj_id)
            else:
                return base % (subdomain, version_id, obj_id, extra_id)

    def get_version_id(self, api_configuration, base):
        resource_data = Endpoints.matrix.get(base, None)

        version = None
        if resource_data is not None:
            resource = list(resource_data.keys())[0]
            resource_values = list(resource_data.values())[0]
            if resource not in api_configuration.keys():
                version = resource_values[-1]
            elif api_configuration[resource] in resource_values:
                version = api_configuration[resource]
            else:
                version = resource_values[-1]
        return version

    def validate_id(self, resource_id):
        if not (type(resource_id) is str or type(resource_id) is unicode or type(resource_id) is int or type(resource_id) is long):
            raise Exception("Resource id needs to be provided as string or int/long")
        return True
