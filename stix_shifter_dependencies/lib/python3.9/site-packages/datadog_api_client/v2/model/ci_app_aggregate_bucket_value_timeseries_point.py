# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    datetime,
    unset,
    UnsetType,
)


class CIAppAggregateBucketValueTimeseriesPoint(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "time": (datetime,),
            "value": (float,),
        }

    attribute_map = {
        "time": "time",
        "value": "value",
    }

    def __init__(self_, time: Union[datetime, UnsetType] = unset, value: Union[float, UnsetType] = unset, **kwargs):
        """
        A timeseries point.

        :param time: The time value for this point.
        :type time: datetime, optional

        :param value: The value for this point.
        :type value: float, optional
        """
        if time is not unset:
            kwargs["time"] = time
        if value is not unset:
            kwargs["value"] = value
        super().__init__(kwargs)
