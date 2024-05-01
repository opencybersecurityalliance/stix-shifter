# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SyntheticsConfigVariableType(ModelSimple):
    """
    Type of the configuration variable.

    :param value: Must be one of ["global", "text"].
    :type value: str
    """

    allowed_values = {
        "global",
        "text",
    }
    GLOBAL: ClassVar["SyntheticsConfigVariableType"]
    TEXT: ClassVar["SyntheticsConfigVariableType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SyntheticsConfigVariableType.GLOBAL = SyntheticsConfigVariableType("global")
SyntheticsConfigVariableType.TEXT = SyntheticsConfigVariableType("text")
