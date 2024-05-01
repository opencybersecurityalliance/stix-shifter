# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class WidgetHorizontalAlign(ModelSimple):
    """
    Horizontal alignment.

    :param value: Must be one of ["center", "left", "right"].
    :type value: str
    """

    allowed_values = {
        "center",
        "left",
        "right",
    }
    CENTER: ClassVar["WidgetHorizontalAlign"]
    LEFT: ClassVar["WidgetHorizontalAlign"]
    RIGHT: ClassVar["WidgetHorizontalAlign"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


WidgetHorizontalAlign.CENTER = WidgetHorizontalAlign("center")
WidgetHorizontalAlign.LEFT = WidgetHorizontalAlign("left")
WidgetHorizontalAlign.RIGHT = WidgetHorizontalAlign("right")
