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


class LogsListRequestTime(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "_from": (datetime,),
            "timezone": (str,),
            "to": (datetime,),
        }

    attribute_map = {
        "_from": "from",
        "timezone": "timezone",
        "to": "to",
    }

    def __init__(self_, _from: datetime, to: datetime, timezone: Union[str, UnsetType] = unset, **kwargs):
        """
        Timeframe to retrieve the log from.

        :param _from: Minimum timestamp for requested logs.
        :type _from: datetime

        :param timezone: Timezone can be specified both as an offset (for example "UTC+03:00")
            or a regional zone (for example "Europe/Paris").
        :type timezone: str, optional

        :param to: Maximum timestamp for requested logs.
        :type to: datetime
        """
        if timezone is not unset:
            kwargs["timezone"] = timezone
        super().__init__(kwargs)

        self_._from = _from
        self_.to = to
