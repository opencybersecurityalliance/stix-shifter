# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SyntheticsTestCallType(ModelSimple):
    """
    The type of gRPC call to perform.

    :param value: Must be one of ["healthcheck", "unary"].
    :type value: str
    """

    allowed_values = {
        "healthcheck",
        "unary",
    }
    HEALTHCHECK: ClassVar["SyntheticsTestCallType"]
    UNARY: ClassVar["SyntheticsTestCallType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SyntheticsTestCallType.HEALTHCHECK = SyntheticsTestCallType("healthcheck")
SyntheticsTestCallType.UNARY = SyntheticsTestCallType("unary")
