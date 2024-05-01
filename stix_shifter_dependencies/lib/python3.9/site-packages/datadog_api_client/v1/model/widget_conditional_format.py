# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.widget_comparator import WidgetComparator
    from datadog_api_client.v1.model.widget_palette import WidgetPalette


class WidgetConditionalFormat(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.widget_comparator import WidgetComparator
        from datadog_api_client.v1.model.widget_palette import WidgetPalette

        return {
            "comparator": (WidgetComparator,),
            "custom_bg_color": (str,),
            "custom_fg_color": (str,),
            "hide_value": (bool,),
            "image_url": (str,),
            "metric": (str,),
            "palette": (WidgetPalette,),
            "timeframe": (str,),
            "value": (float,),
        }

    attribute_map = {
        "comparator": "comparator",
        "custom_bg_color": "custom_bg_color",
        "custom_fg_color": "custom_fg_color",
        "hide_value": "hide_value",
        "image_url": "image_url",
        "metric": "metric",
        "palette": "palette",
        "timeframe": "timeframe",
        "value": "value",
    }

    def __init__(
        self_,
        comparator: WidgetComparator,
        palette: WidgetPalette,
        value: float,
        custom_bg_color: Union[str, UnsetType] = unset,
        custom_fg_color: Union[str, UnsetType] = unset,
        hide_value: Union[bool, UnsetType] = unset,
        image_url: Union[str, UnsetType] = unset,
        metric: Union[str, UnsetType] = unset,
        timeframe: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Define a conditional format for the widget.

        :param comparator: Comparator to apply.
        :type comparator: WidgetComparator

        :param custom_bg_color: Color palette to apply to the background, same values available as palette.
        :type custom_bg_color: str, optional

        :param custom_fg_color: Color palette to apply to the foreground, same values available as palette.
        :type custom_fg_color: str, optional

        :param hide_value: True hides values.
        :type hide_value: bool, optional

        :param image_url: Displays an image as the background.
        :type image_url: str, optional

        :param metric: Metric from the request to correlate this conditional format with.
        :type metric: str, optional

        :param palette: Color palette to apply.
        :type palette: WidgetPalette

        :param timeframe: Defines the displayed timeframe.
        :type timeframe: str, optional

        :param value: Value for the comparator.
        :type value: float
        """
        if custom_bg_color is not unset:
            kwargs["custom_bg_color"] = custom_bg_color
        if custom_fg_color is not unset:
            kwargs["custom_fg_color"] = custom_fg_color
        if hide_value is not unset:
            kwargs["hide_value"] = hide_value
        if image_url is not unset:
            kwargs["image_url"] = image_url
        if metric is not unset:
            kwargs["metric"] = metric
        if timeframe is not unset:
            kwargs["timeframe"] = timeframe
        super().__init__(kwargs)

        self_.comparator = comparator
        self_.palette = palette
        self_.value = value
