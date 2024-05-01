# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class WidgetEventSize(ModelSimple):
    """
    Size to use to display an event.

    :param value: Must be one of ["s", "l"].
    :type value: str
    """

    allowed_values = {
        "s",
        "l",
    }
    SMALL: ClassVar["WidgetEventSize"]
    LARGE: ClassVar["WidgetEventSize"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


WidgetEventSize.SMALL = WidgetEventSize("s")
WidgetEventSize.LARGE = WidgetEventSize("l")
