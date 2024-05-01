# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SyntheticsBrowserErrorType(ModelSimple):
    """
    Error type returned by a browser test.

    :param value: Must be one of ["network", "js"].
    :type value: str
    """

    allowed_values = {
        "network",
        "js",
    }
    NETWORK: ClassVar["SyntheticsBrowserErrorType"]
    JS: ClassVar["SyntheticsBrowserErrorType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SyntheticsBrowserErrorType.NETWORK = SyntheticsBrowserErrorType("network")
SyntheticsBrowserErrorType.JS = SyntheticsBrowserErrorType("js")
