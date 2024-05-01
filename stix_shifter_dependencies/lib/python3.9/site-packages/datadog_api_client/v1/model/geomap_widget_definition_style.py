# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


class GeomapWidgetDefinitionStyle(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "palette": (str,),
            "palette_flip": (bool,),
        }

    attribute_map = {
        "palette": "palette",
        "palette_flip": "palette_flip",
    }

    def __init__(self_, palette: str, palette_flip: bool, **kwargs):
        """
        The style to apply to the widget.

        :param palette: The color palette to apply to the widget.
        :type palette: str

        :param palette_flip: Whether to flip the palette tones.
        :type palette_flip: bool
        """
        super().__init__(kwargs)

        self_.palette = palette
        self_.palette_flip = palette_flip
