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
    from datadog_api_client.v1.model.sunburst_widget_legend_inline_automatic_type import (
        SunburstWidgetLegendInlineAutomaticType,
    )


class SunburstWidgetLegendInlineAutomatic(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.sunburst_widget_legend_inline_automatic_type import (
            SunburstWidgetLegendInlineAutomaticType,
        )

        return {
            "hide_percent": (bool,),
            "hide_value": (bool,),
            "type": (SunburstWidgetLegendInlineAutomaticType,),
        }

    attribute_map = {
        "hide_percent": "hide_percent",
        "hide_value": "hide_value",
        "type": "type",
    }

    def __init__(
        self_,
        type: SunburstWidgetLegendInlineAutomaticType,
        hide_percent: Union[bool, UnsetType] = unset,
        hide_value: Union[bool, UnsetType] = unset,
        **kwargs,
    ):
        """
        Configuration of inline or automatic legends.

        :param hide_percent: Whether to hide the percentages of the groups.
        :type hide_percent: bool, optional

        :param hide_value: Whether to hide the values of the groups.
        :type hide_value: bool, optional

        :param type: Whether to show the legend inline or let it be automatically generated.
        :type type: SunburstWidgetLegendInlineAutomaticType
        """
        if hide_percent is not unset:
            kwargs["hide_percent"] = hide_percent
        if hide_value is not unset:
            kwargs["hide_value"] = hide_value
        super().__init__(kwargs)

        self_.type = type
