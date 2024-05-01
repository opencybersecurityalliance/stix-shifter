# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class WidgetLineType(ModelSimple):
    """
    Type of lines displayed.

    :param value: Must be one of ["dashed", "dotted", "solid"].
    :type value: str
    """

    allowed_values = {
        "dashed",
        "dotted",
        "solid",
    }
    DASHED: ClassVar["WidgetLineType"]
    DOTTED: ClassVar["WidgetLineType"]
    SOLID: ClassVar["WidgetLineType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


WidgetLineType.DASHED = WidgetLineType("dashed")
WidgetLineType.DOTTED = WidgetLineType("dotted")
WidgetLineType.SOLID = WidgetLineType("solid")
