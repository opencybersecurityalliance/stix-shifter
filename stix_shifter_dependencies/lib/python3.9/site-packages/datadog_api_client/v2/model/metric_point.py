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


class MetricPoint(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "timestamp": (int,),
            "value": (float,),
        }

    attribute_map = {
        "timestamp": "timestamp",
        "value": "value",
    }

    def __init__(self_, timestamp: Union[int, UnsetType] = unset, value: Union[float, UnsetType] = unset, **kwargs):
        """
        A point object is of the form ``{POSIX_timestamp, numeric_value}``.

        :param timestamp: The timestamp should be in seconds and current.
            Current is defined as not more than 10 minutes in the future or more than 1 hour in the past.
        :type timestamp: int, optional

        :param value: The numeric value format should be a 64bit float gauge-type value.
        :type value: float, optional
        """
        if timestamp is not unset:
            kwargs["timestamp"] = timestamp
        if value is not unset:
            kwargs["value"] = value
        super().__init__(kwargs)
