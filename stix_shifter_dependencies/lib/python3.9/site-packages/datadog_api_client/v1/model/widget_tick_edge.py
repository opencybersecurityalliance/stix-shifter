# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class WidgetTickEdge(ModelSimple):
    """
    Define how you want to align the text on the widget.

    :param value: Must be one of ["bottom", "left", "right", "top"].
    :type value: str
    """

    allowed_values = {
        "bottom",
        "left",
        "right",
        "top",
    }
    BOTTOM: ClassVar["WidgetTickEdge"]
    LEFT: ClassVar["WidgetTickEdge"]
    RIGHT: ClassVar["WidgetTickEdge"]
    TOP: ClassVar["WidgetTickEdge"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


WidgetTickEdge.BOTTOM = WidgetTickEdge("bottom")
WidgetTickEdge.LEFT = WidgetTickEdge("left")
WidgetTickEdge.RIGHT = WidgetTickEdge("right")
WidgetTickEdge.TOP = WidgetTickEdge("top")
