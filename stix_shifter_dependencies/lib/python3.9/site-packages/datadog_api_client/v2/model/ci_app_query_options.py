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


class CIAppQueryOptions(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "time_offset": (int,),
            "timezone": (str,),
        }

    attribute_map = {
        "time_offset": "time_offset",
        "timezone": "timezone",
    }

    def __init__(self_, time_offset: Union[int, UnsetType] = unset, timezone: Union[str, UnsetType] = unset, **kwargs):
        """
        Global query options that are used during the query.
        Only supply timezone or time offset, not both. Otherwise, the query fails.

        :param time_offset: The time offset (in seconds) to apply to the query.
        :type time_offset: int, optional

        :param timezone: The timezone can be specified as GMT, UTC, an offset from UTC (like UTC+1), or as a Timezone Database identifier (like America/New_York).
        :type timezone: str, optional
        """
        if time_offset is not unset:
            kwargs["time_offset"] = time_offset
        if timezone is not unset:
            kwargs["timezone"] = timezone
        super().__init__(kwargs)
