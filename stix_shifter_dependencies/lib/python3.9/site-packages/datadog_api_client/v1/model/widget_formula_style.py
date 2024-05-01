# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


class WidgetFormulaStyle(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "palette": (str,),
            "palette_index": (int,),
        }

    attribute_map = {
        "palette": "palette",
        "palette_index": "palette_index",
    }

    def __init__(self_, palette: Union[str, UnsetType] = unset, palette_index: Union[int, UnsetType] = unset, **kwargs):
        """
        Styling options for widget formulas.

        :param palette: The color palette used to display the formula. A guide to the available color palettes can be found at https://docs.datadoghq.com/dashboards/guide/widget_colors
        :type palette: str, optional

        :param palette_index: Index specifying which color to use within the palette.
        :type palette_index: int, optional
        """
        if palette is not unset:
            kwargs["palette"] = palette
        if palette_index is not unset:
            kwargs["palette_index"] = palette_index
        super().__init__(kwargs)
