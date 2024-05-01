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


class MonitorOptionsSchedulingOptionsEvaluationWindow(ModelNormal):
    validations = {
        "hour_starts": {
            "inclusive_maximum": 59,
            "inclusive_minimum": 0,
        },
        "month_starts": {
            "inclusive_maximum": 1,
            "inclusive_minimum": 1,
        },
    }

    @cached_property
    def openapi_types(_):
        return {
            "day_starts": (str,),
            "hour_starts": (int,),
            "month_starts": (int,),
        }

    attribute_map = {
        "day_starts": "day_starts",
        "hour_starts": "hour_starts",
        "month_starts": "month_starts",
    }

    def __init__(
        self_,
        day_starts: Union[str, UnsetType] = unset,
        hour_starts: Union[int, UnsetType] = unset,
        month_starts: Union[int, UnsetType] = unset,
        **kwargs,
    ):
        """
        Configuration options for the evaluation window. If ``hour_starts`` is set, no other fields may be set. Otherwise, ``day_starts`` and ``month_starts`` must be set together.

        :param day_starts: The time of the day at which a one day cumulative evaluation window starts. Must be defined in UTC time in ``HH:mm`` format.
        :type day_starts: str, optional

        :param hour_starts: The minute of the hour at which a one hour cumulative evaluation window starts.
        :type hour_starts: int, optional

        :param month_starts: The day of the month at which a one month cumulative evaluation window starts.
        :type month_starts: int, optional
        """
        if day_starts is not unset:
            kwargs["day_starts"] = day_starts
        if hour_starts is not unset:
            kwargs["hour_starts"] = hour_starts
        if month_starts is not unset:
            kwargs["month_starts"] = month_starts
        super().__init__(kwargs)
