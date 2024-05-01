# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SyntheticsBasicAuthOauthClientType(ModelSimple):
    """
    The type of basic authentication to use when performing the test.

    :param value: If omitted defaults to "oauth-client". Must be one of ["oauth-client"].
    :type value: str
    """

    allowed_values = {
        "oauth-client",
    }
    OAUTH_CLIENT: ClassVar["SyntheticsBasicAuthOauthClientType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SyntheticsBasicAuthOauthClientType.OAUTH_CLIENT = SyntheticsBasicAuthOauthClientType("oauth-client")
