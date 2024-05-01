# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class WidgetImageSizing(ModelSimple):
    """
    How to size the image on the widget. The values are based on the image `object-fit` CSS properties.
        **Note**: `zoom`, `fit` and `center` values are deprecated.

    :param value: Must be one of ["fill", "contain", "cover", "none", "scale-down", "zoom", "fit", "center"].
    :type value: str
    """

    allowed_values = {
        "fill",
        "contain",
        "cover",
        "none",
        "scale-down",
        "zoom",
        "fit",
        "center",
    }
    FILL: ClassVar["WidgetImageSizing"]
    CONTAIN: ClassVar["WidgetImageSizing"]
    COVER: ClassVar["WidgetImageSizing"]
    NONE: ClassVar["WidgetImageSizing"]
    SCALEDOWN: ClassVar["WidgetImageSizing"]
    ZOOM: ClassVar["WidgetImageSizing"]
    FIT: ClassVar["WidgetImageSizing"]
    CENTER: ClassVar["WidgetImageSizing"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


WidgetImageSizing.FILL = WidgetImageSizing("fill")
WidgetImageSizing.CONTAIN = WidgetImageSizing("contain")
WidgetImageSizing.COVER = WidgetImageSizing("cover")
WidgetImageSizing.NONE = WidgetImageSizing("none")
WidgetImageSizing.SCALEDOWN = WidgetImageSizing("scale-down")
WidgetImageSizing.ZOOM = WidgetImageSizing("zoom")
WidgetImageSizing.FIT = WidgetImageSizing("fit")
WidgetImageSizing.CENTER = WidgetImageSizing("center")
