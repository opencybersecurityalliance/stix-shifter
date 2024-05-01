# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class WidgetColorPreference(ModelSimple):
    """
    Which color to use on the widget.

    :param value: Must be one of ["background", "text"].
    :type value: str
    """

    allowed_values = {
        "background",
        "text",
    }
    BACKGROUND: ClassVar["WidgetColorPreference"]
    TEXT: ClassVar["WidgetColorPreference"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


WidgetColorPreference.BACKGROUND = WidgetColorPreference("background")
WidgetColorPreference.TEXT = WidgetColorPreference("text")
