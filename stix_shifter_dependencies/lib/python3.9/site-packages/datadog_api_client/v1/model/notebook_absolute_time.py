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


class NotebookAbsoluteTime(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "end": (datetime,),
            "live": (bool,),
            "start": (datetime,),
        }

    attribute_map = {
        "end": "end",
        "live": "live",
        "start": "start",
    }

    def __init__(self_, end: datetime, start: datetime, live: Union[bool, UnsetType] = unset, **kwargs):
        """
        Absolute timeframe.

        :param end: The end time.
        :type end: datetime

        :param live: Indicates whether the timeframe should be shifted to end at the current time.
        :type live: bool, optional

        :param start: The start time.
        :type start: datetime
        """
        if live is not unset:
            kwargs["live"] = live
        super().__init__(kwargs)

        self_.end = end
        self_.start = start
