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


class WidgetMarker(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "display_type": (str,),
            "label": (str,),
            "time": (str,),
            "value": (str,),
        }

    attribute_map = {
        "display_type": "display_type",
        "label": "label",
        "time": "time",
        "value": "value",
    }

    def __init__(
        self_,
        value: str,
        display_type: Union[str, UnsetType] = unset,
        label: Union[str, UnsetType] = unset,
        time: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Markers allow you to add visual conditional formatting for your graphs.

        :param display_type: Combination of:

            * A severity error, warning, ok, or info
            * A line type: dashed, solid, or bold
              In this case of a Distribution widget, this can be set to be ``x_axis_percentile``.
        :type display_type: str, optional

        :param label: Label to display over the marker.
        :type label: str, optional

        :param time: Timestamp for the widget.
        :type time: str, optional

        :param value: Value to apply. Can be a single value y = 15 or a range of values 0 < y < 10.
        :type value: str
        """
        if display_type is not unset:
            kwargs["display_type"] = display_type
        if label is not unset:
            kwargs["label"] = label
        if time is not unset:
            kwargs["time"] = time
        super().__init__(kwargs)

        self_.value = value
