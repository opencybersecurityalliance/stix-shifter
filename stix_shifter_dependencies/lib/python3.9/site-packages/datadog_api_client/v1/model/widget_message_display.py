# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class WidgetMessageDisplay(ModelSimple):
    """
    Amount of log lines to display

    :param value: Must be one of ["inline", "expanded-md", "expanded-lg"].
    :type value: str
    """

    allowed_values = {
        "inline",
        "expanded-md",
        "expanded-lg",
    }
    INLINE: ClassVar["WidgetMessageDisplay"]
    EXPANDED_MEDIUM: ClassVar["WidgetMessageDisplay"]
    EXPANDED_LARGE: ClassVar["WidgetMessageDisplay"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


WidgetMessageDisplay.INLINE = WidgetMessageDisplay("inline")
WidgetMessageDisplay.EXPANDED_MEDIUM = WidgetMessageDisplay("expanded-md")
WidgetMessageDisplay.EXPANDED_LARGE = WidgetMessageDisplay("expanded-lg")
