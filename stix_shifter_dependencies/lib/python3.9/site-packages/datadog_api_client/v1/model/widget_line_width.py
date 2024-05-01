# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class WidgetLineWidth(ModelSimple):
    """
    Width of line displayed.

    :param value: Must be one of ["normal", "thick", "thin"].
    :type value: str
    """

    allowed_values = {
        "normal",
        "thick",
        "thin",
    }
    NORMAL: ClassVar["WidgetLineWidth"]
    THICK: ClassVar["WidgetLineWidth"]
    THIN: ClassVar["WidgetLineWidth"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


WidgetLineWidth.NORMAL = WidgetLineWidth("normal")
WidgetLineWidth.THICK = WidgetLineWidth("thick")
WidgetLineWidth.THIN = WidgetLineWidth("thin")
