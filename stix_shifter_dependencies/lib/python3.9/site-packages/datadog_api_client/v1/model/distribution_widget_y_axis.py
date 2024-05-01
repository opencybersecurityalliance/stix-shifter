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


class DistributionWidgetYAxis(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "include_zero": (bool,),
            "label": (str,),
            "max": (str,),
            "min": (str,),
            "scale": (str,),
        }

    attribute_map = {
        "include_zero": "include_zero",
        "label": "label",
        "max": "max",
        "min": "min",
        "scale": "scale",
    }

    def __init__(
        self_,
        include_zero: Union[bool, UnsetType] = unset,
        label: Union[str, UnsetType] = unset,
        max: Union[str, UnsetType] = unset,
        min: Union[str, UnsetType] = unset,
        scale: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Y Axis controls for the distribution widget.

        :param include_zero: True includes zero.
        :type include_zero: bool, optional

        :param label: The label of the axis to display on the graph.
        :type label: str, optional

        :param max: Specifies the maximum value to show on the y-axis. It takes a number, or auto for default behavior.
        :type max: str, optional

        :param min: Specifies minimum value to show on the y-axis. It takes a number, or auto for default behavior.
        :type min: str, optional

        :param scale: Specifies the scale type. Possible values are ``linear`` or ``log``.
        :type scale: str, optional
        """
        if include_zero is not unset:
            kwargs["include_zero"] = include_zero
        if label is not unset:
            kwargs["label"] = label
        if max is not unset:
            kwargs["max"] = max
        if min is not unset:
            kwargs["min"] = min
        if scale is not unset:
            kwargs["scale"] = scale
        super().__init__(kwargs)
