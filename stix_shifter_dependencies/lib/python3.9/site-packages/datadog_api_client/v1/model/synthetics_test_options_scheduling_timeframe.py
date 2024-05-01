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


class SyntheticsTestOptionsSchedulingTimeframe(ModelNormal):
    validations = {
        "day": {
            "inclusive_maximum": 7,
            "inclusive_minimum": 1,
        },
    }

    @cached_property
    def openapi_types(_):
        return {
            "day": (int,),
            "_from": (str,),
            "to": (str,),
        }

    attribute_map = {
        "day": "day",
        "_from": "from",
        "to": "to",
    }

    def __init__(
        self_,
        day: Union[int, UnsetType] = unset,
        _from: Union[str, UnsetType] = unset,
        to: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Object describing a timeframe.

        :param day: Number representing the day of the week.
        :type day: int, optional

        :param _from: The hour of the day on which scheduling starts.
        :type _from: str, optional

        :param to: The hour of the day on which scheduling ends.
        :type to: str, optional
        """
        if day is not unset:
            kwargs["day"] = day
        if _from is not unset:
            kwargs["_from"] = _from
        if to is not unset:
            kwargs["to"] = to
        super().__init__(kwargs)
