# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    none_type,
    unset,
    UnsetType,
)


class IncidentSearchResponseNumericFacetDataAggregates(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "max": (float, none_type),
            "min": (float, none_type),
        }

    attribute_map = {
        "max": "max",
        "min": "min",
    }

    def __init__(
        self_,
        max: Union[float, none_type, UnsetType] = unset,
        min: Union[float, none_type, UnsetType] = unset,
        **kwargs,
    ):
        """
        Aggregate information for numeric incident data.

        :param max: Maximum value of the numeric aggregates.
        :type max: float, none_type, optional

        :param min: Minimum value of the numeric aggregates.
        :type min: float, none_type, optional
        """
        if max is not unset:
            kwargs["max"] = max
        if min is not unset:
            kwargs["min"] = min
        super().__init__(kwargs)
